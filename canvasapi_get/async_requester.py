"""Async HTTP requester with intelligent rate limiting for Canvas API."""

import asyncio
import logging
import random
import ssl
import threading
import weakref
from datetime import datetime
from pprint import pformat

import aiohttp
import aiodns
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
        self.links = self._parse_link_header(original_response.headers)
        self.content = content

    def json(self) -> dict:
        """Parse response content as JSON.

        Returns:
            Parsed JSON data.
        """
        import json

        return json.loads(self.content.decode("utf-8"))

    @property
    def text(self):
        return self.content.decode("utf-8")

    def _parse_link_header(self, headers) -> dict:
        """
        Parse HTTP Link header into a dictionary of rel -> url mappings.

        Canvas returns pagination links in standard HTTP Link header format:
        Link: <https://canvas.example.com/api/v1/courses/1/assignments?page=2>; rel="next",
              <https://canvas.example.com/api/v1/courses/1/assignments?page=5>; rel="last"

        Args:
            headers: HTTP headers dictionary

        Returns:
            Dictionary mapping rel values to URL information:
            {"next": {"url": "https://..."}, "last": {"url": "https://..."}}
        """
        import re

        link_header = headers.get("Link") or headers.get("link")
        if not link_header:
            return {}

        links = {}
        # Parse each link in the header
        # Pattern matches: <URL>; rel="relation"
        link_pattern = r'<([^>]+)>;\s*rel="([^"]+)"'

        for match in re.finditer(link_pattern, link_header):
            url, rel = match.groups()
            links[rel] = {"url": url}

        return links


class AsyncRequester:
    """
    Async HTTP requester with intelligent rate limiting for Canvas API requests.

    This class handles HTTP requests with dynamic concurrency control, exponential
    backoff, and circuit breaker patterns to maximize throughput while respecting
    Canvas rate limits. Enhanced with per-loop session management for background
    loop compatibility.
    """

    # Class-level session registry for all AsyncRequester instances
    _session_registry: dict[asyncio.AbstractEventLoop, aiohttp.ClientSession] = {}
    _registry_lock = threading.Lock()
    _cleanup_callbacks: dict[asyncio.AbstractEventLoop, list] = {}

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
            session: Optional existing aiohttp session to use (deprecated in favor of per-loop sessions).
        """
        # Preserve the original base url and add "/api/v1" to it
        self.original_url = base_url
        self.base_url = base_url + "/api/v1/"
        self.new_quizzes_url = base_url + "/api/quiz/v1/"
        self.graphql = base_url + "/api/graphql"
        self.access_token = access_token

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

        # Store session configuration for per-loop session creation
        self._session_config = {
            "ssl_context": ssl.create_default_context(cafile=certifi.where()),
            "connector_kwargs": {
                "limit": 100,
                "limit_per_host": 30,
            },
            "timeout": aiohttp.ClientTimeout(total=300, connect=30),
        }

        # If a session was provided, we'll use it as a fallback but prefer per-loop sessions
        self._fallback_session = session

    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        # Note: We don't close per-loop sessions here as they may be shared
        # Session cleanup is handled by loop shutdown hooks
        pass

    @classmethod
    def _get_current_loop(cls) -> asyncio.AbstractEventLoop | None:
        """
        Get the currently running event loop.

        Returns:

            The current event loop or None if no loop is running.
        """
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            return None

    @classmethod
    def _create_session_for_loop(
        cls, loop: asyncio.AbstractEventLoop
    ) -> aiohttp.ClientSession:
        """
        Create a new aiohttp session for the specified loop with async DNS resolution.

        Args:
            loop: The event loop to create the session for.

        Returns:
            A new aiohttp ClientSession configured for Canvas API use.
        """
        # TLS + cert bundle
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        # Enhanced connector with async DNS and better error handling
        connector = aiohttp.TCPConnector(
            ssl=ssl_context,
            resolver=aiohttp.AsyncResolver(),  # Use default async resolver
            limit=100,
            limit_per_host=30,
            enable_cleanup_closed=True,  # Clean up closed connections
            force_close=False,  # Allow connection reuse
            ttl_dns_cache=300,  # DNS cache for 5 minutes
            use_dns_cache=True,
        )

        # Reasonable timeouts for Canvas API
        timeout = aiohttp.ClientTimeout(
            total=120,  # Total request timeout: 2 minutes
            connect=30,  # DNS/TCP/TLS handshake: 30 seconds
            sock_read=60,  # Server response timeout: 60 seconds
            sock_connect=10,  # Socket connection: 10 seconds
        )

        session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            raise_for_status=False,
            loop=loop,  # Explicitly bind to the loop
        )

        logger.debug(
            f"Created new aiohttp session for loop {id(loop)} "
            f"with async DNS resolver and timeout={timeout!r}"
        )
        return session

    @classmethod
    def _register_loop_cleanup(cls, loop: asyncio.AbstractEventLoop) -> None:
        """
        Register cleanup callback for when the event loop shuts down.

        Args:
            loop: The event loop to register cleanup for.
        """

        def cleanup_session():
            """Cleanup callback to remove session when loop shuts down."""
            with cls._registry_lock:
                session = cls._session_registry.pop(loop, None)
                if session and not session.closed:
                    # Schedule session closure in the loop if it's still running
                    try:
                        if not loop.is_closed():
                            loop.create_task(session.close())
                    except RuntimeError:
                        # Loop is already closed, session will be garbage collected
                        pass

                # Remove cleanup callbacks for this loop
                cls._cleanup_callbacks.pop(loop, None)

            logger.debug(f"Cleaned up session for loop {id(loop)}")

        # Use weak reference to avoid keeping the loop alive
        loop_ref = weakref.ref(loop, lambda ref: cleanup_session())

        # Store cleanup callback
        with cls._registry_lock:
            if loop not in cls._cleanup_callbacks:
                cls._cleanup_callbacks[loop] = []
            cls._cleanup_callbacks[loop].append(cleanup_session)

    @classmethod
    def _get_session_for_loop(
        cls, loop: asyncio.AbstractEventLoop
    ) -> aiohttp.ClientSession:
        """
        Get or create an aiohttp session for the specified event loop.

        Args:
            loop: The event loop to get a session for.

        Returns:
            An aiohttp ClientSession associated with the specified loop.
        """
        need_cleanup_registration = False

        with cls._registry_lock:
            # Check if we already have a session for this loop
            session = cls._session_registry.get(loop)

            if session is None or session.closed:
                # Create new session for this loop
                session = cls._create_session_for_loop(loop)
                cls._session_registry[loop] = session
                need_cleanup_registration = True

        # Register cleanup callback outside the lock to avoid deadlock
        if need_cleanup_registration:
            cls._register_loop_cleanup(loop)

        return session

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """
        Ensure an aiohttp session is available for the current loop.

        Returns:
            An aiohttp ClientSession ready for use.

        Raises:
            RuntimeError: If no event loop is running and no fallback session available.
        """
        current_loop = self._get_current_loop()

        if current_loop is not None:
            # We're in an async context, use per-loop session
            return self._get_session_for_loop(current_loop)

        elif self._fallback_session is not None and not self._fallback_session.closed:
            # Use fallback session if available
            logger.debug("Using fallback session (no running event loop)")
            return self._fallback_session

        else:
            raise RuntimeError(
                "No event loop is running and no fallback session available. "
                "AsyncRequester must be used within an async context."
            )

    @classmethod
    async def cleanup_all_sessions(cls) -> None:
        """
        Cleanup all sessions in the registry.

        This is typically called during application shutdown.
        """
        with cls._registry_lock:
            sessions_to_close = list(cls._session_registry.values())
            cls._session_registry.clear()
            cls._cleanup_callbacks.clear()

        # Close all sessions
        for session in sessions_to_close:
            if not session.closed:
                try:
                    await session.close()
                except Exception as e:
                    logger.warning(f"Error closing session during cleanup: {e}")

        logger.debug("Cleaned up all AsyncRequester sessions")

    async def close(self) -> None:
        """Close any fallback session owned by this instance."""
        if self._fallback_session is not None and not self._fallback_session.closed:
            await self._fallback_session.close()
            logger.debug("Closed fallback session")

    @staticmethod
    def _parse_rate_limit_headers(
        response: aiohttp.ClientResponse,
    ) -> tuple[float | None, float | None]:
        """
        Parse Canvas API rate limiting headers from the response.

        Canvas provides two main rate limiting headers:
        - X-Request-Cost: Cost of the current request (float)
        - X-Rate-Limit-Remaining: Remaining quota in the bucket (float)

        Headers are case-insensitive per HTTP/1.1 specification, and Canvas
        may return different capitalizations.

        Args:
            response: The HTTP response object.

        Returns:
            Tuple of (request_cost, remaining_quota) as floats or None if not present.
        """
        request_cost = None
        remaining_quota = None

        # Canvas rate limit headers - check both standard and lowercased versions
        # Headers are case-insensitive per HTTP/1.1 spec
        cost_header = response.headers.get("X-Request-Cost") or response.headers.get(
            "x-request-cost"
        )
        if cost_header:
            try:
                cost_value = float(cost_header.strip())
                # Canvas should return non-negative costs
                if cost_value >= 0:
                    request_cost = cost_value
                else:
                    logger.warning(
                        f"Invalid X-Request-Cost value (negative): {cost_header}"
                    )
            except (ValueError, TypeError):
                logger.warning(f"Invalid X-Request-Cost header value: {cost_header}")

        remaining_header = response.headers.get(
            "X-Rate-Limit-Remaining"
        ) or response.headers.get("x-rate-limit-remaining")
        if remaining_header:
            try:
                remaining_value = float(remaining_header.strip())
                # Remaining quota should be non-negative
                if remaining_value >= 0:
                    remaining_quota = remaining_value
                else:
                    logger.warning(
                        f"Invalid X-Rate-Limit-Remaining value (negative): {remaining_header}"
                    )
            except (ValueError, TypeError):
                logger.warning(
                    f"Invalid X-Rate-Limit-Remaining header value: {remaining_header}"
                )

        # Log comprehensive rate limit information for debugging
        if request_cost is not None or remaining_quota is not None:
            logger.debug(
                f"Rate limit info - Cost: {request_cost}, Remaining: {remaining_quota}, "
                f"Status: {response.status}, URL: {response.url}"
            )

        return request_cost, remaining_quota

    def _create_error_context(
        self,
        response: aiohttp.ClientResponse,
        full_url: str,
        method: str,
        params: dict | None = None,
    ) -> dict:
        """
        Create standardized error context for debugging.

        Args:
            response: The HTTP response object
            full_url: The full URL that was requested
            method: The HTTP method used
            params: The request parameters (optional)

        Returns:
            Dictionary containing error context information
        """
        context = {
            "url": full_url,
            "method": method,
            "status_code": response.status,
            "headers": dict(response.headers),
        }

        if params:
            # Sanitize parameters for logging (remove sensitive data)
            safe_params = params.copy()
            # Don't log access tokens or other sensitive parameters
            for key in list(safe_params.keys()):
                if any(
                    sensitive in key.lower()
                    for sensitive in ["token", "password", "secret", "key"]
                ):
                    safe_params[key] = "***REDACTED***"
            context["params"] = safe_params

        return context

    def _get_error_message_from_response(self, response_content: bytes) -> str:
        """
        Extract a meaningful error message from Canvas API response.

        Args:
            response_content: Raw response content bytes

        Returns:
            Formatted error message string
        """
        try:
            # Try to decode as UTF-8 first
            text_content = response_content.decode("utf-8")

            # Try to parse as JSON to get structured error
            import json

            try:
                error_data = json.loads(text_content)
                if isinstance(error_data, dict):
                    # Canvas often returns errors in 'errors' or 'message' fields
                    if "errors" in error_data:
                        errors = error_data["errors"]
                        if isinstance(errors, list) and errors:
                            return "; ".join(str(err) for err in errors)
                        elif isinstance(errors, dict):
                            return "; ".join(f"{k}: {v}" for k, v in errors.items())
                        else:
                            return str(errors)
                    elif "message" in error_data:
                        return str(error_data["message"])
                    elif "error" in error_data:
                        return str(error_data["error"])

                # If JSON but no standard error fields, return the whole thing
                return str(error_data)

            except json.JSONDecodeError:
                # Not JSON, return the text content
                return (
                    text_content[:500] + "..."
                    if len(text_content) > 500
                    else text_content
                )

        except UnicodeDecodeError:
            # Fallback for non-UTF8 content
            return f"<Binary content, {len(response_content)} bytes>"

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

        Note: This library is intentionally GET-only for read-only Canvas API access.
        It was derived from the full canvasapi library but modified to only support
        GET operations for safer, read-only interactions with Canvas data.

        Args:
            method: The HTTP method for the request (must be "GET").
            endpoint: The endpoint to call.
            headers: Optional HTTP headers to be sent with the request.
            use_auth: Optional flag to remove the authentication header.
            _url: Optional argument to specify request type or external URL.
            _kwargs: A list of 2-tuples representing processed keyword arguments.
            **kwargs: Additional parameters to be sent with the request.

        Returns:
            The HTTP response object.

        Raises:
            CanvasException: For unsupported HTTP methods (only GET is supported) or general errors.
            BadRequest: For 400 status code responses.
            InvalidAccessToken: For 401 responses with WWW-Authenticate header.
            Unauthorized: For other 401 responses.
            Forbidden: For 403 responses (excluding rate limits).
            RateLimitExceeded: For rate limit exceeded responses.
            ResourceDoesNotExist: For 404 responses.
            Conflict: For 409 responses.
            UnprocessableEntity: For 422 responses.
            RuntimeError: If no session is available.
        """
        if method.upper() != "GET":
            raise CanvasException(
                f"Unsupported HTTP method: {method}. This library only supports GET "
                f"requests for read-only Canvas API access. For full CRUD operations, "
                f"use the complete 'canvasapi' library instead."
            )

        session = await self._ensure_session()
        logger.debug("Session ensured successfully")

        # Build URL
        logger.debug("Building URL...")
        if not _url:
            full_url = f"{self.base_url}{endpoint}"
        elif _url == "new_quizzes":
            full_url = f"{self.new_quizzes_url}{endpoint}"
        elif _url == "graphql":
            full_url = self.graphql
        else:
            full_url = _url
        logger.debug(f"URL built: {full_url}")

        # Build headers
        logger.debug("Building headers...")
        if not headers:
            headers = {}

        if use_auth:
            auth_header = {"Authorization": f"Bearer {self.access_token}"}
            headers.update(auth_header)
        logger.debug("Headers built successfully")

        # Process kwargs
        logger.debug("Processing kwargs...")
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
        logger.debug("Kwargs processed successfully")

        # Acquire permission from coordinator
        logger.debug(
            f"About to acquire rate limiting permission (enable_rate_limiting={self.enable_rate_limiting})"
        )
        if self.enable_rate_limiting:
            logger.debug("Calling coordinator.acquire()...")
            await self.coordinator.acquire()
            logger.debug("Coordinator.acquire() completed")

        try:
            # Retry loop for rate limiting
            attempt = 0
            while attempt <= self.max_retries:
                attempt += 1

                logger.info(f"Request: {method} {full_url} (attempt {attempt})")
                logger.debug(f"Headers: {pformat(clean_headers(headers))}")

                if params:
                    logger.debug(f"Params: {pformat(params)}")

                # Make the request with detailed logging
                logger.debug(f"About to make HTTP request to: {full_url}")
                logger.debug(f"Session timeout config: {session.timeout}")
                logger.debug(f"Session connector config: {session.connector}")

                async with session.get(
                    full_url, headers=headers, params=params
                ) as response:
                    logger.debug(
                        f"HTTP request completed with status: {response.status}"
                    )
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

                    # Handle error responses with standardized error context
                    if response.status >= 400:
                        error_context = self._create_error_context(
                            response, full_url, method, params
                        )
                        error_message = self._get_error_message_from_response(
                            response_content
                        )

                        logger.debug(f"HTTP error response: {error_context}")

                        if response.status == 400:
                            raise BadRequest(
                                f"Bad Request: {error_message}. Context: {error_context}"
                            )
                        elif response.status == 401:
                            if "WWW-Authenticate" in response.headers:
                                raise InvalidAccessToken(
                                    f"Invalid Access Token: {error_message}. Context: {error_context}"
                                )
                            else:
                                raise Unauthorized(
                                    f"Unauthorized: {error_message}. Context: {error_context}"
                                )
                        elif response.status == 403:
                            if b"Rate Limit Exceeded" in response_content:
                                remaining = response.headers.get(
                                    "X-Rate-Limit-Remaining", "Unknown"
                                )
                                raise RateLimitExceeded(
                                    f"Rate Limit Exceeded. X-Rate-Limit-Remaining: {remaining}. "
                                    f"Context: {error_context}"
                                )
                            else:
                                raise Forbidden(
                                    f"Forbidden: {error_message}. Context: {error_context}"
                                )
                        elif response.status == 404:
                            raise ResourceDoesNotExist(
                                f"Resource Not Found: {error_message}. Context: {error_context}"
                            )
                        elif response.status == 409:
                            raise Conflict(
                                f"Conflict: {error_message}. Context: {error_context}"
                            )
                        elif response.status == 422:
                            raise UnprocessableEntity(
                                f"Unprocessable Entity: {error_message}. Context: {error_context}"
                            )
                        else:
                            # Generic error handler for other 4xx/5xx codes
                            raise CanvasException(
                                f"HTTP {response.status}: {error_message}. Context: {error_context}"
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
