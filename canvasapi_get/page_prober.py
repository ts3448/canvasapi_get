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
        Initialize the page prober.

        Args:
            requester: The async requester to use for probing requests.
        """
        self.requester = requester

    async def discover_total_pages(
        self,
        first_url: str,
        first_params: dict,
        links: dict | None = None,
        request_method: str = "GET",
        url_override: str | None = None,
    ) -> tuple[int, list[str]]:
        """
        Discover the total number of pages and generate all page URLs.

        Args:
            first_url: The base URL for pagination requests.
            first_params: Parameters for the first request.
            links: Link header data from the first response.
            request_method: HTTP method to use for requests.
            url_override: URL override for special endpoints.

        Returns:
            Tuple of (total_pages, list_of_page_urls).

        Raises:
            CanvasException: If unable to determine total pages.
        """
        # First, try to extract from links if available
        if links and "last" in links:
            total_pages = self._extract_page_from_url(links["last"]["url"])
            if total_pages:
                page_urls = self._generate_page_urls(first_url, first_params, total_pages, url_override)
                logger.info(f"Found total pages from last link: {total_pages}")
                return total_pages, page_urls

        # Fallback to exponential probing
        logger.info("No 'last' link found, starting exponential probing")
        total_pages = await self._exponential_probe(first_url, first_params, request_method, url_override)
        page_urls = self._generate_page_urls(first_url, first_params, total_pages, url_override)
        
        logger.info(f"Discovered total pages through probing: {total_pages}")
        return total_pages, page_urls

    def _extract_page_from_url(self, url: str) -> int | None:
        """
        Extract page number from a URL.

        Args:
            url: The URL to extract page number from.

        Returns:
            The page number or None if not found.
        """
        # Look for page parameter in URL
        page_match = re.search(r'[?&]page=(\d+)', url)
        if page_match:
            return int(page_match.group(1))
        return None

    def _generate_page_urls(
        self, 
        base_url: str, 
        base_params: dict, 
        total_pages: int,
        url_override: str | None = None,
    ) -> list[str]:
        """
        Generate URLs for all pages.

        Args:
            base_url: The base URL for requests.
            base_params: Base parameters for requests.
            total_pages: Total number of pages to generate.
            url_override: URL override for special endpoints.

        Returns:
            List of URLs for pages 2 through total_pages (page 1 already fetched).
        """
        page_urls = []
        
        for page_num in range(2, total_pages + 1):
            # Create params for this page
            page_params = base_params.copy()
            page_params["page"] = page_num
            
            # Build URL with parameters
            if url_override == "new_quizzes":
                full_url = f"{self.requester.new_quizzes_url}{base_url}"
            elif url_override == "graphql":
                full_url = self.requester.graphql
            elif url_override:
                full_url = url_override
            else:
                full_url = f"{self.requester.base_url}{base_url}"
            
            # Add parameters to URL
            param_string = "&".join([f"{k}={v}" for k, v in page_params.items()])
            separator = "&" if "?" in full_url else "?"
            page_url = f"{full_url}{separator}{param_string}"
            
            page_urls.append(page_url)
        
        return page_urls

    async def _exponential_probe(
        self,
        base_url: str,
        base_params: dict,
        request_method: str,
        url_override: str | None,
    ) -> int:
        """
        Use exponential probing to find the last page.

        Args:
            base_url: The base URL for requests.
            base_params: Base parameters for requests.
            request_method: HTTP method to use.
            url_override: URL override for special endpoints.

        Returns:
            The total number of pages.

        Raises:
            CanvasException: If probing fails or no pages exist.
        """
        # Start exponential probing
        page = 2
        last_successful_page = 1
        
        logger.debug("Starting exponential probe sequence")
        
        while True:
            try:
                exists = await self._probe_page_exists(
                    base_url, base_params, page, request_method, url_override
                )
                
                if exists:
                    last_successful_page = page
                    logger.debug(f"Page {page} exists, continuing probe")
                    page *= 2  # Exponential increase
                else:
                    logger.debug(f"Page {page} does not exist, starting binary search")
                    break
                    
            except Exception as e:
                logger.warning(f"Error probing page {page}: {e}")
                break
        
        # Binary search between last_successful_page and page
        if last_successful_page == page // 2:
            # Binary search to find exact boundary
            return await self._binary_search_last_page(
                base_url, base_params, last_successful_page, page - 1, request_method, url_override
            )
        else:
            return last_successful_page

    async def _binary_search_last_page(
        self,
        base_url: str,
        base_params: dict,
        low: int,
        high: int,
        request_method: str,
        url_override: str | None,
    ) -> int:
        """
        Binary search to find the exact last page.

        Args:
            base_url: The base URL for requests.
            base_params: Base parameters for requests.
            low: Lower bound for search (known to exist).
            high: Upper bound for search (known to not exist).
            request_method: HTTP method to use.
            url_override: URL override for special endpoints.

        Returns:
            The exact last page number.
        """
        logger.debug(f"Binary searching between pages {low} and {high}")
        
        while low < high - 1:
            mid = (low + high) // 2
            
            try:
                exists = await self._probe_page_exists(
                    base_url, base_params, mid, request_method, url_override
                )
                
                if exists:
                    low = mid
                    logger.debug(f"Page {mid} exists, searching upper half")
                else:
                    high = mid
                    logger.debug(f"Page {mid} does not exist, searching lower half")
                    
            except Exception as e:
                logger.warning(f"Error in binary search at page {mid}: {e}")
                high = mid
        
        return low

    async def _probe_page_exists(
        self,
        base_url: str,
        base_params: dict,
        page: int,
        request_method: str,
        url_override: str | None,
    ) -> bool:
        """
        Check if a specific page exists.

        Args:
            base_url: The base URL for requests.
            base_params: Base parameters for requests.
            page: Page number to check.
            request_method: HTTP method to use.
            url_override: URL override for special endpoints.

        Returns:
            True if the page exists, False otherwise.
        """
        try:
            # Create parameters for this page
            params = base_params.copy()
            params["page"] = page
            
            # Make the request
            response = await self.requester.request(
                request_method,
                base_url,
                _url=url_override,
                **params
            )
            
            # Check if we got data
            response_data = await response.json()
            
            # If response is a list, check if it's empty
            if isinstance(response_data, list):
                return len(response_data) > 0
            
            # If response is a dict, check for data in common pagination patterns
            if isinstance(response_data, dict):
                # Check common pagination response patterns
                for key in ["data", "results", "items"]:
                    if key in response_data:
                        data = response_data[key]
                        if isinstance(data, list):
                            return len(data) > 0
                
                # If no pagination wrapper, assume non-empty dict means data exists
                return len(response_data) > 0
            
            # Fallback: any response means page exists
            return True
            
        except ResourceDoesNotExist:
            # 404 means page doesn't exist
            return False
        except Exception as e:
            logger.warning(f"Unexpected error probing page {page}: {e}")
            # On unexpected errors, assume page doesn't exist to be safe
            return False

    async def probe_batch(
        self,
        base_url: str,
        base_params: dict,
        pages: Sequence[int],
        request_method: str = "GET",
        url_override: str | None = None,
    ) -> dict[int, bool]:
        """
        Probe multiple pages concurrently.

        Args:
            base_url: The base URL for requests.
            base_params: Base parameters for requests.
            pages: Sequence of page numbers to probe.
            request_method: HTTP method to use.
            url_override: URL override for special endpoints.

        Returns:
            Dictionary mapping page numbers to existence status.
        """
        logger.debug(f"Batch probing pages: {list(pages)}")
        
        tasks = [
            self._probe_page_exists(base_url, base_params, page, request_method, url_override)
            for page in pages
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        page_status = {}
        for page, result in zip(pages, results):
            if isinstance(result, Exception):
                logger.warning(f"Error probing page {page}: {result}")
                page_status[page] = False
            else:
                page_status[page] = result
        
        return page_status
