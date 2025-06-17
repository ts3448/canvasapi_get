import logging
import time
import threading
from datetime import datetime
from pprint import pformat

import requests

from canvasapi.exceptions import (
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
from canvasapi.util import clean_headers

logger = logging.getLogger(__name__)


class RateLimitState(object):
    """
    Tracks rate limiting state for a Canvas API requester.
    """

    def __init__(self):
        """
        Initialize rate limit tracking state.
        """
        self.remaining_quota = None
        self.last_request_cost = None
        self.last_update = None
        self.total_requests = 0
        self.total_cost = 0.0
        self.throttle_events = 0
        self._lock = threading.Lock()

    def update(self, cost, remaining):
        """
        Update rate limit state from response headers.

        Args:
            cost (float): The cost of the last request from X-Request-Cost header.
            remaining (float): The remaining quota from X-Rate-Limit-Remaining header.
        """
        with self._lock:
            self.last_request_cost = cost
            self.remaining_quota = remaining
            self.last_update = time.time()
            self.total_requests += 1
            if cost is not None:
                self.total_cost += cost

    def record_throttle(self):
        """
        Record a throttling event.
        """
        with self._lock:
            self.throttle_events += 1

    def get_stats(self):
        """
        Get current rate limit statistics.

        Returns:
            dict: Dictionary containing rate limit statistics.
        """
        with self._lock:
            return {
                "remaining_quota": self.remaining_quota,
                "last_request_cost": self.last_request_cost,
                "total_requests": self.total_requests,
                "total_cost": self.total_cost,
                "throttle_events": self.throttle_events,
                "last_update": self.last_update,
            }


class Requester(object):
    """
    Responsible for handling HTTP requests with intelligent rate limiting.
    """

    def __init__(
        self,
        base_url,
        access_token,
        max_retries=3,
        base_delay=1.0,
        max_delay=60.0,
        backoff_factor=2.0,
        enable_rate_limiting=True,
    ):
        """
        Initialize the requester with rate limiting capabilities.

        Args:
            base_url (str): The base URL of the Canvas instance's API.
            access_token (str): The API key to authenticate requests with.
            max_retries (int): Maximum number of retry attempts for rate limited requests.
            base_delay (float): Base delay in seconds for exponential backoff.
            max_delay (float): Maximum delay in seconds between retries.
            backoff_factor (float): Multiplier for exponential backoff.
            enable_rate_limiting (bool): Whether to enable intelligent rate limiting.
        """
        # Preserve the original base url and add "/api/v1" to it
        self.original_url = base_url
        self.base_url = base_url + "/api/v1/"
        self.new_quizzes_url = base_url + "/api/quiz/v1/"
        self.graphql = base_url + "/api/graphql"
        self.access_token = access_token
        self._session = requests.Session()
        self._cache = []

        # Rate limiting configuration
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.enable_rate_limiting = enable_rate_limiting

        # Rate limiting state
        self.rate_limit_state = RateLimitState()

    def _get_request(self, url, headers, params=None):
        """
        Issue a GET request to the specified endpoint with the data provided.

        Args:
            url (str): The URL to request.
            headers (dict): The HTTP headers to send with this request.
            params (dict): The parameters to send with this request.

        Returns:
            requests.Response: The response from the request.
        """
        return self._session.get(url, headers=headers, params=params)

    @staticmethod
    def _parse_rate_limit_headers(response):
        """
        Parse rate limiting headers from the response.

        Args:
            response (requests.Response): The HTTP response object.

        Returns:
            tuple: (request_cost, remaining_quota) as floats or None if not present.
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

    def _calculate_retry_delay(self, attempt, remaining_quota=None):
        """
        Calculate the delay before retrying a rate limited request.

        Args:
            attempt (int): The current retry attempt number (starting from 1).
            remaining_quota (float): The remaining quota if available.

        Returns:
            float: The delay in seconds before retrying.
        """
        # Exponential backoff with jitter
        delay = min(
            self.base_delay * (self.backoff_factor ** (attempt - 1)), self.max_delay
        )

        # If we know the remaining quota is very low, add extra delay
        if remaining_quota is not None and remaining_quota < 1.0:
            delay = max(delay, 5.0)

        # Add small random jitter to prevent thundering herd
        import random

        jitter = random.uniform(0.1, 0.3) * delay
        return delay + jitter

    def _should_retry_request(self, response, attempt):
        """
        Determine if a request should be retried based on the response.

        Args:
            response (requests.Response): The HTTP response object.
            attempt (int): The current attempt number.

        Returns:
            bool: True if the request should be retried.
        """
        if not self.enable_rate_limiting or attempt >= self.max_retries:
            return False

        # Only retry on rate limit errors
        if response.status_code == 403 and b"Rate Limit Exceeded" in response.content:
            return True

        return False

    def _handle_rate_limit_response(self, response):
        """
        Handle a rate limited response by extracting relevant information.

        Args:
            response (requests.Response): The rate limited response.

        Returns:
            float: The remaining quota if available, otherwise None.
        """
        self.rate_limit_state.record_throttle()

        remaining = response.headers.get("X-Rate-Limit-Remaining")
        if remaining:
            try:
                return float(remaining)
            except (ValueError, TypeError):
                pass

        return None

    def _log_rate_limit_stats(self):
        """
        Log current rate limiting statistics.
        """
        stats = self.rate_limit_state.get_stats()
        if stats["total_requests"] > 0:
            avg_cost = stats["total_cost"] / stats["total_requests"]
            logger.debug(
                f"Rate limit stats - Requests: {stats['total_requests']}, "
                f"Avg cost: {avg_cost:.3f}, Throttle events: {stats['throttle_events']}, "
                f"Remaining quota: {stats['remaining_quota']}"
            )

    def request(
        self,
        method,
        endpoint=None,
        headers=None,
        use_auth=True,
        _url=None,
        _kwargs=None,
        **kwargs,
    ):
        """
        Make a request to the Canvas API and return the response with intelligent rate limiting.

        Args:
            method (str): The HTTP method for the request.
            endpoint (str): The endpoint to call.
            headers (dict): Optional HTTP headers to be sent with the request.
            use_auth (bool): Optional flag to remove the authentication
                header from the request.
            _url (str): Optional argument to specify a request type to Canvas
                or to send a request to a URL outside of the Canvas API.
                If set to "new_quizzes", the new quizzes endpoint will be used.
                If set to "graphql", a graphql POST request will be sent.
                If any string URL is provided, it will be used instead of the
                base REST URL.
                If omitted or set to None, the base_url for the instance REST
                endpoint will be used.
                If this is selected and an endpoint is provided, the endpoint
                will be ignored and only the `_url` argument will be used.
            _kwargs (list): A list of 2-tuples representing processed
                keyword arguments to be sent to Canvas as params or data.

        Returns:
            requests.Response: The HTTP response object.

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

        # Check for specific URL endpoints available from Canvas. If not
        # specified, pass the given URL and move on.
        if not _url:
            full_url = "{}{}".format(self.base_url, endpoint)
        elif _url == "new_quizzes":
            full_url = "{}{}".format(self.new_quizzes_url, endpoint)
        elif _url == "graphql":
            full_url = self.graphql
        else:
            full_url = _url

        if not headers:
            headers = {}

        if use_auth:
            auth_header = {"Authorization": "Bearer {}".format(self.access_token)}
            headers.update(auth_header)

        # Convert kwargs into list of 2-tuples and combine with _kwargs.
        _kwargs = _kwargs or []
        _kwargs.extend(kwargs.items())

        # Do any final argument processing before sending to request method.
        for i, kwarg in enumerate(_kwargs):
            kw, arg = kwarg

            # Convert boolean objects to a lowercase string.
            if isinstance(arg, bool):
                _kwargs[i] = (kw, str(arg).lower())

            # Convert any datetime objects into ISO 8601 formatted strings.
            elif isinstance(arg, datetime):
                _kwargs[i] = (kw, arg.isoformat())

        # Retry loop for rate limiting
        attempt = 0
        while attempt <= self.max_retries:
            attempt += 1

            # Call the request method
            logger.info(
                "Request: {method} {url} (attempt {attempt})".format(
                    method=method, url=full_url, attempt=attempt
                )
            )
            logger.debug(
                "Headers: {headers}".format(headers=pformat(clean_headers(headers)))
            )

            if _kwargs:
                logger.debug("Data: {data}".format(data=pformat(_kwargs)))

            response = self._get_request(full_url, headers, params=dict(_kwargs))

            logger.info(
                "Response: {method} {url} {status} (attempt {attempt})".format(
                    method=method,
                    url=full_url,
                    status=response.status_code,
                    attempt=attempt,
                )
            )
            logger.debug(
                "Headers: {headers}".format(
                    headers=pformat(clean_headers(response.headers))
                )
            )

            try:
                logger.debug(
                    "Data: {data}".format(
                        data=pformat(response.content.decode("utf-8"))
                    )
                )
            except UnicodeDecodeError:
                logger.debug("Data: {data}".format(data=pformat(response.content)))
            except AttributeError:
                # response.content is None
                logger.debug("No data")

            # Parse and update rate limiting information
            if self.enable_rate_limiting:
                request_cost, remaining_quota = self._parse_rate_limit_headers(response)
                if request_cost is not None or remaining_quota is not None:
                    self.rate_limit_state.update(request_cost, remaining_quota)

            # Add response to internal cache
            if len(self._cache) > 4:
                self._cache.pop()

            self._cache.insert(0, response)

            # Check if we should retry due to rate limiting
            if self._should_retry_request(response, attempt):
                remaining_quota = self._handle_rate_limit_response(response)

                if attempt <= self.max_retries:
                    delay = self._calculate_retry_delay(attempt, remaining_quota)
                    logger.warning(
                        f"Rate limit exceeded, retrying in {delay:.2f} seconds "
                        f"(attempt {attempt}/{self.max_retries})"
                    )
                    time.sleep(delay)
                    continue
                else:
                    logger.error(
                        f"Rate limit exceeded, max retries ({self.max_retries}) reached"
                    )

            # Handle non-retry error cases
            if response.status_code == 400:
                raise BadRequest(response.text)
            elif response.status_code == 401:
                if "WWW-Authenticate" in response.headers:
                    raise InvalidAccessToken(response.json())
                else:
                    raise Unauthorized(response.json())
            elif response.status_code == 403:
                if b"Rate Limit Exceeded" in response.content:
                    remaining = str(
                        response.headers.get("X-Rate-Limit-Remaining", "Unknown")
                    )
                    raise RateLimitExceeded(
                        "Rate Limit Exceeded. X-Rate-Limit-Remaining: {}".format(
                            remaining
                        )
                    )
                else:
                    raise Forbidden(response.text)
            elif response.status_code == 404:
                raise ResourceDoesNotExist("Not Found")
            elif response.status_code == 409:
                raise Conflict(response.text)
            elif response.status_code == 422:
                raise UnprocessableEntity(response.text)
            elif response.status_code > 400:
                # generic catch-all for error codes
                raise CanvasException(
                    "Encountered an error: status code {}".format(response.status_code)
                )

            # Success - log stats and return
            if self.enable_rate_limiting and logger.isEnabledFor(logging.DEBUG):
                self._log_rate_limit_stats()

            return response

        # This should never be reached due to the loop logic, but included for safety
        raise CanvasException("Unexpected error in request retry logic")

    def get_rate_limit_stats(self):
        """
        Get current rate limiting statistics.

        Returns:
            dict: Dictionary containing rate limit statistics including:
                - remaining_quota: Current remaining API quota
                - last_request_cost: Cost of the last request
                - total_requests: Total number of requests made
                - total_cost: Total cost of all requests
                - throttle_events: Number of times requests were throttled
                - last_update: Timestamp of last rate limit update
        """
        return self.rate_limit_state.get_stats()

    def reset_rate_limit_stats(self):
        """
        Reset rate limiting statistics to initial state.
        """
        self.rate_limit_state = RateLimitState()
        logger.info("Rate limit statistics reset")
