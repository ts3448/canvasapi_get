"""Async HTTP requester with intelligent rate limiting for Canvas API."""

import asyncio
import logging
import random
import ssl
from datetime import datetime
from pprint import pformat

import aiohttp
import certifi

from canvasapi_get.async_rate_limit_state import AsyncRateLimitState
from canvasapi_get.rate_limit_coordinator import RateLimitCoordinator
from canvasapi_get.exceptions import (
    BadRequest,
    CanvasException,
    Conflict,
    Forbidden,
    InvalidAccessToken,
    RateLimitExceeded,
    ResourceDoesNotExist,
    Unauthorized,
    UnprocessableEntity,
)
from canvasapi_get.util import clean_headers

logger = logging.getLogger(__name__)


# Create a new response object with the content for return
class AsyncResponse:
    def __init__(self, original_response, content):
        self.status = original_response.status
        self.headers = original_response.headers
        self.links = getattr(original_response, "links", {})
        self._content = content

    def json(self) -> dict:
        """Parse response content as JSON.

        Returns:
            Parsed JSON data.
        """
        import json

        return json.loads(self._content.decode("utf-8"))

    @property
    def text(self):
        return self._content.decode("utf-8")


class AsyncRequester:
    """
    Async HTTP requester with intelligent rate limiting for Canvas API requests.

    This class handles HTTP requests with dynamic concurrency control, exponential
    backoff, and circuit breaker patterns to maximize throughput while respecting
    Canvas rate limits.
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
        session: aiohttp.ClientSession | None = None,
    ):
        """
        Initialize the async requester with rate limiting capabilities.

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
            session: Optional existing aiohttp session to use.
        """
        # Preserve the original base url and add "/api/v1" to it
        self.original_url = base_url
        self.base_url = base_url + "/api/v1/"
        self.new_quizzes_url = base_url + "/api/quiz/v1/"
        self.graphql = base_url + "/api/graphql"
        self.access_token = access_token

        # HTTP session management
        self._session = session
        self._owns_session = session is None
        self._session_lock = asyncio.Lock()

        # Cache for responses
        self._cache: list = []

        # Rate limiting configuration
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.enable_rate_limiting = enable_rate_limiting

        # Rate limiting state and coordination
        self.rate_limit_state = AsyncRateLimitState()
        self.coordinator = RateLimitCoordinator(
            self.rate_limit_state,
            base_concurrency=base_concurrency,
            max_concurrency=max_concurrency,
        )

    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def _ensure_session(self) -> None:
        """Ensure aiohttp session is available."""
        async with self._session_lock:
            if self._session is None or self._session.closed:
                ssl_context = ssl.create_default_context(cafile=certifi.where())
                connector = aiohttp.TCPConnector(
                    ssl=ssl_context,
                    limit=100,
                    limit_per_host=30,
                )
                timeout = aiohttp.ClientTimeout(total=300, connect=30)
                self._session = aiohttp.ClientSession(
                    connector=connector,
                    timeout=timeout,
                    raise_for_status=False,
                )

    async def close(self) -> None:
        """Close the HTTP session if we own it."""
        if self._owns_session and self._session and not self._session.closed:
            await self._session.close()

    @staticmethod
    def _parse_rate_limit_headers(
        response: aiohttp.ClientResponse,
    ) -> tuple[float | None, float | None]:
        """
        Parse rate limiting headers from the response.

        Args:
            response: The HTTP response object.

        Returns:
            Tuple of (request_cost, remaining_quota) as floats or None if not present.
        """
        request_cost = None
        remaining_quota = None

        cost_header = response.headers.get("X-Request-Cost")
        if cost_header:
            try:
                request_cost = float(cost_header)
            except (ValueError, TypeError):
                logger.warning(f"Invalid X-Request-Cost header value: {cost_header}")

        remaining_header = response.headers.get("X-Rate-Limit-Remaining")
        if remaining_header:
            try:
                remaining_quota = float(remaining_header)
            except (ValueError, TypeError):
                logger.warning(
                    f"Invalid X-Rate-Limit-Remaining header value: {remaining_header}"
                )

        return request_cost, remaining_quota

    def _calculate_retry_delay(
        self, attempt: int, remaining_quota: float | None = None
    ) -> float:
        """
        Calculate the delay before retrying a rate limited request.

        Args:
            attempt: The current retry attempt number (starting from 1).
            remaining_quota: The remaining quota if available.

        Returns:
            The delay in seconds before retrying.
        """
        # Exponential backoff with jitter
        delay = min(
            self.base_delay * (self.backoff_factor ** (attempt - 1)), self.max_delay
        )

        # If we know the remaining quota is very low, add extra delay
        if remaining_quota is not None and remaining_quota < 1.0:
            delay = max(delay, 5.0)

        # Add small random jitter to prevent thundering herd
        jitter = random.uniform(0.1, 0.3) * delay
        return delay + jitter

    def _should_retry_request(
        self, response: aiohttp.ClientResponse, attempt: int
    ) -> bool:
        """
        Determine if a request should be retried based on the response.

        Args:
            response: The HTTP response object.
            attempt: The current attempt number.

        Returns:
            True if the request should be retried.
        """
        if not self.enable_rate_limiting or attempt >= self.max_retries:
            return False

        # Only retry on rate limit errors
        return response.status == 403

    async def _handle_rate_limit_response(
        self, response: aiohttp.ClientResponse
    ) -> float | None:
        """
        Handle a rate limited response by extracting relevant information.

        Args:
            response: The rate limited response.

        Returns:
            The remaining quota if available, otherwise None.
        """
        await self.rate_limit_state.record_throttle()

        remaining = response.headers.get("X-Rate-Limit-Remaining")
        if remaining:
            try:
                return float(remaining)
            except (ValueError, TypeError):
                pass

        return None

    async def _log_rate_limit_stats(self) -> None:
        """Log current rate limiting statistics."""
        stats = await self.rate_limit_state.get_stats()
        if stats["total_requests"] > 0:
            avg_cost = stats["total_cost"] / stats["total_requests"]
            logger.debug(
                f"Rate limit stats - Requests: {stats['total_requests']}, "
                f"Avg cost: {avg_cost:.3f}, Throttle events: {stats['throttle_events']}, "
                f"Remaining quota: {stats['remaining_quota']}"
            )

    async def request(
        self,
        method: str,
        endpoint: str | None = None,
        headers: dict | None = None,
        use_auth: bool = True,
        _url: str | None = None,
        _kwargs: list | None = None,
        **kwargs,
    ) -> AsyncResponse:
        """
        Make an async request to the Canvas API with intelligent rate limiting.

        Args:
            method: The HTTP method for the request.
            endpoint: The endpoint to call.
            headers: Optional HTTP headers to be sent with the request.
            use_auth: Optional flag to remove the authentication header.
            _url: Optional argument to specify request type or external URL.
            _kwargs: A list of 2-tuples representing processed keyword arguments.
            **kwargs: Additional parameters to be sent with the request.

        Returns:
            The HTTP response object.

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

        await self._ensure_session()

        # Build URL
        if not _url:
            full_url = f"{self.base_url}{endpoint}"
        elif _url == "new_quizzes":
            full_url = f"{self.new_quizzes_url}{endpoint}"
        elif _url == "graphql":
            full_url = self.graphql
        else:
            full_url = _url

        # Build headers
        if not headers:
            headers = {}

        if use_auth:
            auth_header = {"Authorization": f"Bearer {self.access_token}"}
            headers.update(auth_header)

        # Process kwargs
        _kwargs = _kwargs or []
        _kwargs.extend(kwargs.items())

        # Process arguments
        for i, kwarg in enumerate(_kwargs):
            kw, arg = kwarg

            # Convert boolean objects to lowercase string
            if isinstance(arg, bool):
                _kwargs[i] = (kw, str(arg).lower())

            # Convert datetime objects to ISO 8601 strings
            elif isinstance(arg, datetime):
                _kwargs[i] = (kw, arg.isoformat())

        params = dict(_kwargs) if _kwargs else None

        # Acquire permission from coordinator
        if self.enable_rate_limiting:
            await self.coordinator.acquire()

        try:
            # Retry loop for rate limiting
            attempt = 0
            while attempt <= self.max_retries:
                attempt += 1

                logger.info(f"Request: {method} {full_url} (attempt {attempt})")
                logger.debug(f"Headers: {pformat(clean_headers(headers))}")

                if params:
                    logger.debug(f"Params: {pformat(params)}")

                # Make the request
                async with self._session.get(
                    full_url, headers=headers, params=params
                ) as response:
                    # Read response content
                    response_content = await response.read()

                    logger.info(
                        f"Response: {method} {full_url} {response.status} (attempt {attempt})"
                    )
                    logger.debug(
                        f"Response Headers: {pformat(clean_headers(dict(response.headers)))}"
                    )

                    try:
                        logger.debug(
                            f"Response Data: {pformat(response_content.decode('utf-8'))}"
                        )
                    except UnicodeDecodeError:
                        logger.debug(f"Response Data: {pformat(response_content)}")

                    # Parse and update rate limiting information
                    if self.enable_rate_limiting:
                        request_cost, remaining_quota = self._parse_rate_limit_headers(
                            response
                        )
                        if request_cost is not None or remaining_quota is not None:
                            await self.rate_limit_state.update(
                                request_cost, remaining_quota
                            )
                            await self.coordinator.adjust_concurrency()

                    # Add to cache
                    if len(self._cache) > 4:
                        self._cache.pop()
                    self._cache.insert(0, response)

                    # Check if we should retry due to rate limiting
                    if self._should_retry_request(response, attempt):
                        remaining_quota = await self._handle_rate_limit_response(
                            response
                        )

                        if attempt <= self.max_retries:
                            # Trip circuit breaker and wait
                            delay = self._calculate_retry_delay(
                                attempt, remaining_quota
                            )
                            await self.coordinator.trip_circuit_breaker(delay)
                            continue
                        else:
                            logger.error(
                                f"Rate limit exceeded, max retries ({self.max_retries}) reached"
                            )

                    # Handle error responses
                    if response.status == 400:
                        raise BadRequest(
                            response_content.decode("utf-8", errors="ignore")
                        )
                    elif response.status == 401:
                        if "WWW-Authenticate" in response.headers:
                            response_json = await response.json()
                            raise InvalidAccessToken(response_json)
                        else:
                            response_json = await response.json()
                            raise Unauthorized(response_json)
                    elif response.status == 403:
                        if b"Rate Limit Exceeded" in response_content:
                            remaining = str(
                                response.headers.get(
                                    "X-Rate-Limit-Remaining", "Unknown"
                                )
                            )
                            raise RateLimitExceeded(
                                f"Rate Limit Exceeded. X-Rate-Limit-Remaining: {remaining}"
                            )
                        else:
                            raise Forbidden(
                                response_content.decode("utf-8", errors="ignore")
                            )
                    elif response.status == 404:
                        raise ResourceDoesNotExist("Not Found")
                    elif response.status == 409:
                        raise Conflict(
                            response_content.decode("utf-8", errors="ignore")
                        )
                    elif response.status == 422:
                        raise UnprocessableEntity(
                            response_content.decode("utf-8", errors="ignore")
                        )
                    elif response.status > 400:
                        raise CanvasException(
                            f"Encountered an error: status code {response.status}"
                        )

                    # Success - log stats and return
                    if self.enable_rate_limiting and logger.isEnabledFor(logging.DEBUG):
                        await self._log_rate_limit_stats()

                    return AsyncResponse(response, response_content)

        finally:
            # Always release the permit
            if self.enable_rate_limiting:
                self.coordinator.release()

        # This should never be reached
        raise CanvasException("Unexpected error in request retry logic")

    async def get_rate_limit_stats(self) -> dict:
        """
        Get current rate limiting statistics.

        Returns:
            Dictionary containing rate limit statistics and coordinator state.
        """
        rate_stats = await self.rate_limit_state.get_stats()
        coordinator_stats = await self.coordinator.get_stats()

        return {
            **rate_stats,
            "coordinator": coordinator_stats,
        }

    async def reset_rate_limit_stats(self) -> None:
        """Reset rate limiting statistics to initial state."""
        await self.rate_limit_state.reset()
        logger.info("Rate limit statistics reset")
