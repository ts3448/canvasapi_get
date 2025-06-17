"""
Simplified paginated list implementation with automatic concurrent fetching.

This module provides paginated access to Canvas API responses using internal async
operations for concurrent page fetching while maintaining a synchronous interface.
All pagination now automatically uses concurrent fetching for optimal performance.
"""

from __future__ import annotations

import asyncio
import re
import logging
from collections.abc import Iterable, Iterator
from concurrent.futures import Future

from canvasapi_get.background_loop import get_background_loop
from canvasapi_get.exceptions import ResourceDoesNotExist

logger = logging.getLogger(__name__)


class PaginatedList(Iterable):
    """
    Abstracts pagination of Canvas API with automatic concurrent page fetching.
    
    This class provides a synchronous interface while internally using async
    operations via the background loop for concurrent page fetching. All users
    automatically benefit from improved performance without code changes.
    """

    def __getitem__(self, index: int | slice):
        assert isinstance(index, (int, slice))
        if isinstance(index, int):
            if index < 0:
                raise IndexError("Cannot negative index a PaginatedList")
            self._get_up_to_index(index)
            return self._elements[index]
        else:
            return self._Slice(self, index)

    def __init__(
        self,
        content_class,
        requester,
        request_method,
        first_url,
        extra_attribs=None,
        _root=None,
        _url_override=None,
        **kwargs,
    ):
        """
        Initialize paginated list with automatic concurrent fetching.

        Args:
            content_class: The expected type to return in the list.
            requester: The unified requester to pass HTTP requests through.
            request_method: HTTP request method.
            first_url: Canvas endpoint for the initial request.
            extra_attribs: Extra data to include in the request.
            _root: Specify a nested property from Canvas for the resulting list.
            _url_override: "new_quizzes" or "graphql" for specific Canvas endpoints.
            **kwargs: Additional request parameters.
        """
        self._elements: list = []
        self._content_class = content_class
        self._requester = requester
        self._request_method = request_method
        self._first_url = first_url
        self._first_params = kwargs or {}
        self._first_params["per_page"] = kwargs.get("per_page", 100)
        self._extra_attribs = extra_attribs or {}
        self._root = _root
        self._url_override = _url_override

        # State tracking
        self._total_pages: int | None = None
        self._next_url: str | None = first_url
        self._next_params = self._first_params.copy()

        # Fetch all pages concurrently using background loop
        self._fetch_all_pages_concurrently()

    def _fetch_all_pages_concurrently(self) -> None:
        """
        Fetch all pages concurrently using background loop for async operations.
        
        This method discovers total pages and fetches them all concurrently
        while maintaining a synchronous interface for backward compatibility.
        """
        background_loop = get_background_loop()
        
        # Execute async concurrent fetching via background loop
        all_items = background_loop.run_coroutine_threadsafe(
            self._async_fetch_all_pages()
        )
        
        self._elements = all_items

    async def _async_fetch_all_pages(self) -> list:
        """
        Async implementation of concurrent page fetching.
        
        Returns:
            List of all items from all pages.
        """
        # Fetch first page to get pagination info and data
        first_response = await self._async_fetch_page(1)
        first_items = self._process_page_data(first_response)
        
        # Discover total pages from response
        links = getattr(first_response, "links", {})
        total_pages = await self._discover_total_pages(first_response, links)
        
        if total_pages == 1:
            return first_items
            
        # Fetch remaining pages concurrently
        tasks = []
        for page_num in range(2, total_pages + 1):
            task = asyncio.create_task(
                self._async_fetch_page_with_retry(page_num),
                name=f"fetch_page_{page_num}"
            )
            tasks.append(task)
            
        # Wait for all pages to complete
        remaining_pages = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine all items in page order
        all_items = first_items.copy()
        for page_num, result in enumerate(remaining_pages, start=2):
            if isinstance(result, Exception):
                logger.error(f"Failed to fetch page {page_num}: {result}")
                # Continue with other pages, don't fail entire pagination
            else:
                all_items.extend(result)
                
        return all_items

    async def _async_fetch_page(self, page_num: int):
        """
        Fetch a specific page using the requester's async capabilities.
        
        Args:
            page_num: The page number to fetch.
            
        Returns:
            Response object for the page.
        """
        params = self._first_params.copy()
        params["page"] = page_num
        
        # Use requester's internal async capabilities via background loop
        # The UnifiedRequester will handle the async execution internally
        return await self._requester._async_request(
            self._request_method,
            self._first_url,
            _url=self._url_override,
            **params
        )

    async def _async_fetch_page_with_retry(self, page_num: int) -> list:
        """
        Fetch a specific page with retry logic.
        
        Args:
            page_num: The page number to fetch.
            
        Returns:
            List of processed items from the page.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await self._async_fetch_page(page_num)
                return self._process_page_data(response)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                    
                delay = 2 ** attempt  # Exponential backoff
                logger.warning(
                    f"Retry {attempt + 1}/{max_retries} for page {page_num} after {delay}s: {e}"
                )
                await asyncio.sleep(delay)
        return []

    async def _discover_total_pages(self, first_response, links: dict) -> int:
        """
        Discover total number of pages from response metadata.
        
        Args:
            first_response: The first page response.
            links: Pagination links from response.
            
        Returns:
            Total number of pages.
        """
        # Try to get total pages from "last" link
        if links and "last" in links:
            last_url = links["last"].get("url", "")
            page_match = re.search(r"[?&]page=(\d+)", str(last_url))
            if page_match:
                return int(page_match.group(1))
                
        # Fallback to exponential probing if no last link
        return await self._exponential_probe_pages()

    async def _exponential_probe_pages(self) -> int:
        """
        Use exponential probing to discover total pages.
        
        Returns:
            Total number of pages discovered.
        """
        page = 1
        step = 1
        last_good = 1
        
        while True:
            page += step
            try:
                response = await self._async_fetch_page(page)
                data = response.json()
                
                # Check if page has data
                if self._root:
                    data = data.get(self._root, [])
                    
                if not data:
                    break
                    
                last_good = page
                step *= 2
                
            except (ResourceDoesNotExist, Exception):
                break
                
        # Binary search between last_good and page for exact boundary
        return await self._binary_search_last_page(last_good, page)

    async def _binary_search_last_page(self, low: int, high: int) -> int:
        """
        Binary search to find the exact last page.
        
        Args:
            low: Known good page number.
            high: Known bad page number.
            
        Returns:
            The actual last page number.
        """
        while low + 1 < high:
            mid = (low + high) // 2
            try:
                response = await self._async_fetch_page(mid)
                data = response.json()
                
                if self._root:
                    data = data.get(self._root, [])
                    
                if not data:
                    high = mid
                else:
                    low = mid
                    
            except (ResourceDoesNotExist, Exception):
                high = mid
                
        return low

    def _process_page_data(self, response) -> list:
        """
        Process response data into content objects.
        
        Args:
            response: The response to process.
            
        Returns:
            List of content objects.
            
        Raises:
            ValueError: If root key is missing from response.
        """
        data = response.json()
        
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

    def __len__(self):
        """Return the total number of items across all pages."""
        return len(self._elements)

    def __iter__(self) -> Iterator:
        """Iterate over all items from all pages."""
        for element in self._elements:
            yield element

    def __repr__(self) -> str:
        """String representation of the paginated list."""
        return f"<PaginatedList of type {self._content_class.__name__}>"

    def _get_up_to_index(self, index: int) -> None:
        """
        Ensure elements are available up to the specified index.
        
        Args:
            index: The index to ensure is available.
        """
        # All elements are already fetched during initialization
        pass

    def _grow(self) -> list:
        """
        Legacy method for compatibility - no longer needed.
        
        Returns:
            Empty list since all pages are fetched during initialization.
        """
        return []

    def _has_next(self) -> bool:
        """
        Legacy method for compatibility - always False since all pages are fetched.
        
        Returns:
            False since all pages are fetched during initialization.
        """
        return False

    def _is_larger_than(self, index: int) -> bool:
        """
        Check if the list has more elements than the given index.
        
        Args:
            index: The index to check against.
            
        Returns:
            True if the list has more elements than the index.
        """
        return len(self._elements) > index

    class _Slice(Iterable):
        """Slice implementation for PaginatedList."""
        
        def __init__(self, the_list: PaginatedList, the_slice: slice):
            """
            Initialize slice wrapper.
            
            Args:
                the_list: The PaginatedList to slice.
                the_slice: The slice object.
            """
            self._list = the_list
            self._start = the_slice.start or 0
            self._stop = the_slice.stop
            self._step = the_slice.step or 1

            if self._start < 0 or (self._stop is not None and self._stop < 0):
                raise IndexError("Cannot negative index a PaginatedList slice")

        def __iter__(self) -> Iterator:
            """
            Iterate over the slice.
            
            Yields:
                Items from the sliced range.
            """
            index = self._start
            while not self._finished(index):
                if self._list._is_larger_than(index):
                    try:
                        yield self._list[index]
                    except IndexError:
                        return
                    index += self._step
                else:
                    return

        def _finished(self, index: int) -> bool:
            """
            Check if the slice iteration is finished.
            
            Args:
                index: Current index.
                
            Returns:
                True if iteration should stop.
            """
            return self._stop is not None and index >= self._stop
