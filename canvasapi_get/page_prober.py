"""Page discovery logic for Canvas API pagination with exponential probing."""

import asyncio
import logging
import re
from collections.abc import Sequence

from canvasapi_get.async_requester import AsyncRequester
from canvasapi_get.exceptions import ResourceDoesNotExist

logger = logging.getLogger(__name__)


class PageProber:
    """
    Handles discovery of total pages in Canvas API pagination using exponential probing.

    When Canvas API responses don't include "last" rel links, this class uses exponential
    probing followed by binary search to efficiently discover the total number of pages.
    """

    def __init__(self, requester: AsyncRequester):
        """
        Args:
            requester: An AsyncRequester instance to drive all HTTP calls.
        """
        self._requester = requester

    async def discover_total_pages(
        self,
        first_url: str,
        first_params: dict,
        links: dict | None = None,
        request_method: str = "GET",
        url_override: str | None = None,
    ) -> tuple[int, list[tuple[str, dict]]]:
        """
        Discover the total number of pages and generate all page URLs.

        Returns:
            (total_pages, list_of_page_urls)
        """
        if links:
            # Coerce any yarl.URLs into plain strings
            links = {
                rel: {key: str(val) for key, val in info.items()}
                for rel, info in links.items()
            }

        # Try "last" link first
        if links and "last" in links:
            total = self._extract_page_from_url(links["last"]["url"])
            if total:
                urls = self._generate_page_urls(
                    first_url, first_params, total, url_override
                )
                logger.info(f"Found total pages from last link: {total}")
                return total, urls

        # Otherwise fallback to exponential + binary probing
        logger.info("No 'last' link found, starting exponential probing")
        total = await self._exponential_probe(
            first_url, first_params, request_method, url_override
        )
        urls = self._generate_page_urls(first_url, first_params, total, url_override)
        logger.info(f"Discovered total pages through probing: {total}")
        return total, urls

    def _extract_page_from_url(self, url: str) -> int | None:
        """Extract `page=` from any stringy URL (casts yarl.URL to str)."""
        url = str(url)
        m = re.search(r"[?&]page=(\d+)", url)
        return int(m.group(1)) if m else None

    @staticmethod
    def _generate_page_urls(
        base_url: str,
        base_params: dict,
        total_pages: int,
        url_override: str | None = None,
    ) -> list[tuple[str, dict]]:
        """
        Build (url, params) tuples for pages 2..N.
        """
        urls: list[tuple[str, dict]] = []
        for p in range(2, total_pages + 1):
            params = base_params.copy()
            params["page"] = p
            target = url_override or base_url
            urls.append((target, params))
        return urls

    async def _exponential_probe(
        self,
        base_url: str,
        base_params: dict,
        request_method: str,
        url_override: str | None = None,
    ) -> int:
        """Probe powers of two until we hit an empty/404 page."""
        page = 1
        step = 1
        last_good = 1

        while True:
            page += step
            params = {**base_params, "page": page}
            try:
                resp = (
                    await self._requester.request(
                        request_method,
                        base_url,
                        _url=url_override,
                        **params,
                    )
                    if url_override
                    else await self._requester.request(
                        request_method, base_url, **params
                    )
                )
                data = resp.json()
                if not isinstance(data, Sequence) or not data:
                    break
                last_good = page
                step *= 2
            except ResourceDoesNotExist:
                break

        return await self._binary_search_last_page(
            base_url, base_params, last_good, page, request_method, url_override
        )

    async def _binary_search_last_page(
        self,
        base_url: str,
        base_params: dict,
        low: int,
        high: int,
        request_method: str,
        url_override: str | None,
    ) -> int:
        """Binary-search between last known good and first known bad."""
        while low + 1 < high:
            mid = (low + high) // 2
            params = {**base_params, "page": mid}
            try:
                resp = (
                    await self._requester.request(
                        request_method,
                        base_url,
                        _url=url_override,
                        **params,
                    )
                    if url_override
                    else await self._requester.request(
                        request_method, base_url, **params
                    )
                )
                data = resp.json()
                if not isinstance(data, Sequence) or not data:
                    high = mid
                else:
                    low = mid
            except ResourceDoesNotExist:
                high = mid

        return low

    async def probe_multiple_pages(
        self,
        pages: list[int],
        base_url: str,
        base_params: dict,
        request_method: str,
        url_override: str | None = None,
    ) -> dict[int, bool]:
        """
        Concurrently check reachability of a set of page numbers.
        """
        tasks = [
            asyncio.create_task(
                self._check_page(p, base_url, base_params, request_method, url_override)
            )
            for p in pages
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        status: dict[int, bool] = {}
        for p, r in zip(pages, results):
            if isinstance(r, BaseException):
                logger.warning(f"Error probing page {p}: {r}")
                status[p] = False
            else:
                status[p] = r
        return status

    async def _check_page(
        self,
        page: int,
        base_url: str,
        base_params: dict,
        request_method: str,
        url_override: str | None,
    ) -> bool:
        """
        Return True if this page yields a non-empty sequence, False otherwise.
        """
        params = {**base_params, "page": page}
        try:
            resp = (
                await self._requester.request(
                    request_method,
                    base_url,
                    _url=url_override,
                    **params,
                )
                if url_override
                else await self._requester.request(request_method, base_url, **params)
            )
            data = resp.json()
            return isinstance(data, Sequence) and bool(data)
        except ResourceDoesNotExist:
            return False
