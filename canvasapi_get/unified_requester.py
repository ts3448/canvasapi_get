"""
Unified HTTP requester that provides synchronous interface while internally using async operations.

This module implements a requester that maintains complete compatibility with the existing
synchronous Canvas API while internally leveraging async operations via the background loop
for improved performance and unified rate limiting.
"""

import logging
import threading
from datetime import datetime
from pprint import pformat
from collections.abc import Mapping

from canvasapi_get.async_requester import AsyncRequester, AsyncResponse
from canvasapi_get.async_rate_limit_state import AsyncRateLimitState
from canvasapi_get.background_loop import get_background_loop
from canvasapi_get.exceptions import CanvasException
from canvasapi_get.util import clean_headers

logger = logging.getLogger(__name__)


class SyncCompatibleResponse:
    """
    Response wrapper that provides requests.Response compatibility for AsyncResponse objects.
    
    This class ensures that async responses behave exactly like requests.Response objects
    to maintain backward compatibility with existing Canvas API code.
    """
    
    def __init__(self, async_response: AsyncResponse):
        """
        Initialize response wrapper with AsyncResponse.
        
        Args:
            async_response: The AsyncResponse object to wrap.
        """
        self._async_response = async_response
        
    @property
    def status_code(self) -> int:
        """Get HTTP status code (requests.Response compatibility)."""
        return self._async_response.status
        
    @property
    def text(self) -> str:
        """Get response text content."""
        return self._async_response.text
        
    @property
    def content(self) -> bytes:
        """Get response content as bytes."""
        return self._async_response._content
        
    @property
    def headers(self) -> Mapping:
        """Get response headers."""
        return self._async_response.headers
        
    @property 
    def links(self) -> dict:
        """Get pagination links from response."""
        return self._async_response.links
        
    def json(self) -> dict:
        """Parse response content as JSON."""
        return self._async_response.json()
        
    def __getattr__(self, name):
        """Delegate any other attribute access to the wrapped response."""
        return getattr(self._async_response, name)


class UnifiedRequester:
    """
    Unified HTTP requester that provides synchronous interface with internal async operations.
    
    This class replaces both the sync Requester and HybridRequester by providing a single
    interface that internally uses async operations via the background loop. It maintains
    complete compatibility with existing synchronous Canvas API code while enabling
    unified rate limiting and improved performance.
    """
    
    def __init__(
        self,
        base_url: str,
        access_token: str,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
        enable_rate_limiting: bool = True,
        base_concurrency: int = 3,
        max_concurrency: int = 10,
    ):
        """
        Initialize the unified requester with rate limiting capabilities.
        
        Args:
            base_url: The base URL of the Canvas instance's API.
            access_token: The API key to authenticate requests with.
            max_retries: Maximum number of retry attempts for rate limited requests.
            base_delay: Base delay in seconds for exponential backoff.
            max_delay: Maximum delay in seconds between retries.
            backoff_factor: Multiplier for exponential backoff.
            enable_rate_limiting: Whether to enable intelligent rate limiting.
            base_concurrency: Default number of concurrent requests.
            max_concurrency: Maximum number of concurrent requests.
        """
        # Store URL configuration for compatibility
        self.original_url = base_url
        self.base_url = base_url + "/api/v1/"
        self.new_quizzes_url = base_url + "/api/quiz/v1/"
        self.graphql = base_url + "/api/graphql"
        self.access_token = access_token
        
        # Create shared rate limiting state
        self.rate_limit_state = AsyncRateLimitState()
        
        # Create internal async requester with shared state
        self._async_requester = AsyncRequester(
            base_url=base_url,
            access_token=access_token,
            max_retries=max_retries,
            base_delay=base_delay,
            max_delay=max_delay,
            backoff_factor=backoff_factor,
            enable_rate_limiting=enable_rate_limiting,
            base_concurrency=base_concurrency,
            max_concurrency=max_concurrency,
        )
        
        # Replace async requester's rate limit state with our shared instance
        self._async_requester.rate_limit_state = self.rate_limit_state
        self._async_requester.coordinator.rate_limit_state = self.rate_limit_state
        
        # Expose coordinator for compatibility
        self.coordinator = self._async_requester.coordinator
        
        # Cache for compatibility
        self._cache = []
        
        # Background loop for sync-to-async bridge
        self._background_loop = get_background_loop()
        
        # Thread safety for cache operations
        self._cache_lock = threading.Lock()
        
    async def _async_request(
        self,
        method: str,
        endpoint: str | None = None,
        headers: dict | None = None,
        use_auth: bool = True,
        _url: str | None = None,
        _kwargs: list | None = None,
        **kwargs
    ) -> AsyncResponse:
        """
        Internal async request method that delegates to AsyncRequester.
        
        Args:
            method: The HTTP method for the request.
            endpoint: The endpoint to call.
            headers: Optional HTTP headers to be sent with the request.
            use_auth: Whether to include authentication header.
            _url: Optional URL override for request type or external URL.
            _kwargs: A list of 2-tuples representing processed keyword arguments.
            **kwargs: Additional parameters to be sent with the request.
            
        Returns:
            AsyncResponse object with the HTTP response.
            
        Raises:
            CanvasException: For various HTTP errors and Canvas-specific issues.
        """
        return await self._async_requester.request(
            method=method,
            endpoint=endpoint,
            headers=headers,
            use_auth=use_auth,
            _url=_url,
            _kwargs=_kwargs,
            **kwargs
        )
        
    def request(
        self,
        method: str,
        endpoint: str | None = None,
        headers: dict | None = None,
        use_auth: bool = True,
        _url: str | None = None,
        _kwargs: list | None = None,
        **kwargs
    ) -> SyncCompatibleResponse:
        """
        Make a synchronous request to the Canvas API using internal async operations.
        
        This method provides the same interface as the original sync Requester while
        internally using async operations via the background loop for improved
        performance and unified rate limiting.
        
        Args:
            method: The HTTP method for the request.
            endpoint: The endpoint to call.
            headers: Optional HTTP headers to be sent with the request.
            use_auth: Whether to include authentication header.
            _url: Optional URL override for request type or external URL.
            _kwargs: A list of 2-tuples representing processed keyword arguments.
            **kwargs: Additional parameters to be sent with the request.
            
        Returns:
            SyncCompatibleResponse object that behaves like requests.Response.
            
        Raises:
            CanvasException: For unsupported HTTP methods or general errors.
            BadRequest: For 400 status code responses.
            InvalidAccessToken: For 401 responses with WWW-Authenticate header.
            Unauthorized: For other 401 responses.
            Forbidden: For 403 responses (excluding rate limits).
            RateLimitExceeded: For rate limit exceeded responses.
            ResourceDoesNotExist: For 404 responses.
            Conflict: For 409 responses.
            UnprocessableEntity: For 422 responses.
        """
        if method.upper() != "GET":
            raise CanvasException(
                f"Unsupported HTTP method: {method}; only GET allowed"
            )
        
        # Log request for compatibility with existing behavior
        if not _url:
            full_url = f"{self.base_url}{endpoint}"
        elif _url == "new_quizzes":
            full_url = f"{self.new_quizzes_url}{endpoint}"
        elif _url == "graphql":
            full_url = self.graphql
        else:
            full_url = _url
            
        logger.info(f"Request: {method} {full_url}")
        
        if headers:
            logger.debug(f"Headers: {pformat(clean_headers(headers))}")
            
        if _kwargs or kwargs:
            combined_kwargs = (_kwargs or []) + list(kwargs.items())
            logger.debug(f"Data: {pformat(combined_kwargs)}")
        
        # Execute async request via background loop
        async_response = self._background_loop.run_coroutine_threadsafe(
            self._async_request(
                method=method,
                endpoint=endpoint,
                headers=headers,
                use_auth=use_auth,
                _url=_url,
                _kwargs=_kwargs,
                **kwargs
            )
        )
        
        # Wrap in compatibility layer
        sync_response = SyncCompatibleResponse(async_response)
        
        # Update cache for compatibility
        with self._cache_lock:
            if len(self._cache) > 4:
                self._cache.pop()
            self._cache.insert(0, sync_response)
        
        logger.info(f"Response: {method} {full_url} {sync_response.status_code}")
        logger.debug(f"Headers: {pformat(clean_headers(dict(sync_response.headers)))}")
        
        try:
            logger.debug(f"Data: {pformat(sync_response.text)}")
        except UnicodeDecodeError:
            logger.debug(f"Data: {pformat(sync_response.content)}")
        except AttributeError:
            logger.debug("No data")
            
        return sync_response
        
    def get_rate_limit_stats(self) -> dict:
        """
        Get current rate limiting statistics.
        
        Returns:
            Dictionary containing rate limit statistics including:
                - remaining_quota: Current remaining API quota
                - last_request_cost: Cost of the last request  
                - total_requests: Total number of requests made
                - total_cost: Total cost of all requests
                - throttle_events: Number of times requests were throttled
                - last_update: Timestamp of last rate limit update
                - coordinator: Coordinator state information
        """
        # Execute async stats retrieval via background loop
        return self._background_loop.run_coroutine_threadsafe(
            self._async_requester.get_rate_limit_stats()
        )
        
    def reset_rate_limit_stats(self) -> None:
        """Reset rate limiting statistics to initial state."""
        self._background_loop.run_coroutine_threadsafe(
            self._async_requester.reset_rate_limit_stats()
        )
        
    def __getattr__(self, name):
        """
        Delegate attribute access to async requester for compatibility.
        
        This ensures that any attributes expected by existing code are available.
        
        Args:
            name: Attribute name to access.
            
        Returns:
            Attribute value from the async requester.
        """
        return getattr(self._async_requester, name)
