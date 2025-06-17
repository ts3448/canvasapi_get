"""Async paginated list implementation with concurrent page fetching."""

import asyncio
import logging
from collections.abc import AsyncIterable, AsyncIterator

from canvasapi_get.async_requester import AsyncRequester, AsyncResponse
from canvasapi_get.page_prober import PageProber

logger = logging.getLogger(__name__)


class AsyncPaginatedList(AsyncIterable):
    """
    Async implementation of paginated Canvas API responses with concurrent fetching.

    This class fetches all pages concurrently using exponential probing for page
    discovery when needed, while respecting Canvas API rate limits through the
    async requester's coordination system.
    """

    def __init__(
        self,
        content_class: type,
        requester: AsyncRequester,
        request_method: str,
        first_url: str,
        extra_attribs: dict | None = None,
        _root: str | None = None,
        _url_override: str | None = None,
        **kwargs,
    ):
        """
        Initialize async paginated list.

        Args:
            content_class: The expected type to return in the list.
            requester: The async requester to pass HTTP requests through.
            request_method: HTTP request method.
            first_url: Canvas endpoint for the initial request.
            extra_attribs: Extra data to include in the request.
            _root: Specify a nested property from Canvas for the resulting list.
            _url_override: Endpoint override for special Canvas endpoints.
            **kwargs: Additional request parameters.
        """
        self._content_class = content_class
        self._requester = requester
        self._request_method = request_method
        self._first_url = first_url
        self._first_params = kwargs or {}
        self._first_params["per_page"] = kwargs.get("per_page", 100)
        self._extra_attribs = extra_attribs or {}
        self._root = _root
        self._url_override = _url_override

        # Page storage and state
        self._pages: dict[int, list] = {}  # page_number -> list of items
        self._total_pages: int | None = None
        self._page_urls: list[str] = []
        self._fetch_complete = False
        self._fetch_lock = asyncio.Lock()
        self._prober = PageProber(requester)

        # Progress tracking
        self._pages_fetched = 0
        self._fetch_errors: dict[int, Exception] = {}

    async def fetch_all(self) -> None:
        """
        Fetch all pages concurrently.

        This method discovers the total number of pages and then fetches
        all remaining pages concurrently while respecting rate limits.

        Raises:
            CanvasException: If fetching fails or times out.
        """
        async with self._fetch_lock:
            if self._fetch_complete:
                return

            # Fetch first page to get pagination info
            logger.info("Fetching first page to discover pagination")
            first_response = await self._fetch_page(1)

            # Store first page data
            self._pages[1] = self._process_page_data(first_response)
            self._pages_fetched = 1

            # Discover total pages
            links = getattr(first_response, "links", {})
            self._total_pages, self._page_urls = (
                await self._prober.discover_total_pages(
                    self._first_url,
                    self._first_params,
                    links,
                    self._request_method,
                    self._url_override,
                )
            )

            logger.info(
                f"Discovered {self._total_pages} total pages, fetching {len(self._page_urls)} remaining"
            )

            if self._total_pages == 1:
                self._fetch_complete = True
                return

            # Fetch remaining pages concurrently
            await self._fetch_remaining_pages()
            self._fetch_complete = True

    async def _fetch_remaining_pages(self) -> None:
        """
        Fetch all remaining pages concurrently.

        Creates tasks for all remaining pages and fetches them with
        proper error handling and progress tracking.
        """
        if not self._page_urls:
            return

        # Create tasks for all remaining pages
        tasks = []
        for page_num in range(2, self._total_pages + 1):
            task = asyncio.create_task(
                self._fetch_page_with_retry(page_num), name=f"fetch_page_{page_num}"
            )
            tasks.append(task)

        # Wait for all pages to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results and track errors
        for page_num, result in enumerate(results, start=2):
            if isinstance(result, Exception):
                logger.error(f"Failed to fetch page {page_num}: {result}")
                self._fetch_errors[page_num] = result
            else:
                self._pages[page_num] = result
                self._pages_fetched += 1

        if self._fetch_errors:
            logger.warning(
                f"Failed to fetch {len(self._fetch_errors)} pages out of {self._total_pages}"
            )

    async def _fetch_page_with_retry(self, page_num: int) -> list | None:
        """
        Fetch a specific page with retry logic.

        Args:
            page_num: The page number to fetch.

        Returns:
            List of processed items from the page.

        Raises:
            Exception: If all retry attempts fail.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await self._fetch_page(page_num)
                return self._process_page_data(response)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e

                delay = 2**attempt  # Exponential backoff
                logger.warning(
                    f"Retry {attempt + 1}/{max_retries} for page {page_num} after {delay}s: {e}"
                )
                await asyncio.sleep(delay)
        return None

    async def _fetch_page(self, page_num: int) -> AsyncResponse:
        """
        Fetch a specific page.

        Args:
            page_num: The page number to fetch.

        Returns:
            The async response object.
        """
        params = self._first_params.copy()
        params["page"] = page_num

        return await self._requester.request(
            self._request_method, self._first_url, _url=self._url_override, **params
        )

    def _process_page_data(self, response: AsyncResponse) -> list:
        """
        Process response data into content objects.

        Args:
            response: The response to process.

        Returns:
            List of content objects.

        Raises:
            ValueError: If root key is missing from response.
        """
        import asyncio

        # Get response data (need to handle async json())
        if asyncio.iscoroutine(response.json()):
            # This shouldn't happen in our wrapper, but handle it
            raise RuntimeError(
                "Response.json() returned coroutine - this should not happen"
            )

        data = response.json() if callable(response.json) else response.json

        if self._root:
            try:
                data = data[self._root]
            except KeyError as exc:
                raise ValueError(
                    f"The key <{self._root}> does not exist in the response."
                ) from exc

        content = []
        for element in data:
            if element is not None:
                element.update(self._extra_attribs)
                content.append(self._content_class(self._requester, element))

        return content

    async def __aiter__(self) -> AsyncIterator:
        """
        Async iterator over all items in all pages.

        Yields:
            Individual content objects from all pages.
        """
        # Ensure all pages are fetched
        await self.fetch_all()

        # Yield items in page order
        for page_num in range(1, self._total_pages + 1):
            if page_num in self._pages:
                for item in self._pages[page_num]:
                    yield item
            elif page_num in self._fetch_errors:
                logger.warning(
                    f"Skipping page {page_num} due to fetch error: {self._fetch_errors[page_num]}"
                )

    async def to_list(self) -> list:
        """
        Convert to a regular list containing all items.

        Returns:
            List of all content objects from all pages.
        """
        items = []
        async for item in self:
            items.append(item)
        return items

    async def get_page(self, page_num: int) -> list:
        """
        Get items from a specific page.

        Args:
            page_num: The page number to retrieve.

        Returns:
            List of items from the specified page.

        Raises:
            ValueError: If page number is invalid.
            RuntimeError: If page failed to fetch.
        """
        await self.fetch_all()

        if page_num < 1 or (self._total_pages and page_num > self._total_pages):
            raise ValueError(f"Page {page_num} is out of range (1-{self._total_pages})")

        if page_num in self._fetch_errors:
            raise RuntimeError(
                f"Page {page_num} failed to fetch: {self._fetch_errors[page_num]}"
            )

        return self._pages.get(page_num, [])

    async def get_stats(self) -> dict[str, int | float | bool]:
        """
        Get statistics about the pagination fetch process.

        Returns:
            Dictionary containing fetch statistics.
        """
        return {
            "total_pages": self._total_pages or 0,
            "pages_fetched": self._pages_fetched,
            "pages_failed": len(self._fetch_errors),
            "fetch_complete": self._fetch_complete,
            "success_rate": (
                self._pages_fetched / (self._total_pages or 1)
                if self._total_pages
                else 0.0
            ),
        }

    def __repr__(self) -> str:
        """String representation of the paginated list."""
        return f"<AsyncPaginatedList of type {self._content_class.__name__}>"
