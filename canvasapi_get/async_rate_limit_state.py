"""Async-safe rate limiting state management for Canvas API requests."""

import asyncio
import time
from collections.abc import Mapping


class AsyncRateLimitState:
    """
    Tracks rate limiting state for async Canvas API requests with thread-safe operations.
    
    This class manages rate limit information from Canvas API response headers and provides
    statistics for monitoring API usage patterns.
    """

    def __init__(self):
        """Initialize async rate limit tracking state."""
        self.remaining_quota: float | None = None
        self.last_request_cost: float | None = None
        self.last_update: float | None = None
        self.total_requests: int = 0
        self.total_cost: float = 0.0
        self.throttle_events: int = 0
        self._lock: asyncio.Lock = asyncio.Lock()

    async def update(self, cost: float | None, remaining: float | None) -> None:
        """
        Update rate limit state from response headers.

        Args:
            cost: The cost of the last request from X-Request-Cost header.
            remaining: The remaining quota from X-Rate-Limit-Remaining header.
        """
        async with self._lock:
            self.last_request_cost = cost
            self.remaining_quota = remaining
            self.last_update = time.time()
            self.total_requests += 1
            if cost is not None:
                self.total_cost += cost

    async def record_throttle(self) -> None:
        """Record a throttling event."""
        async with self._lock:
            self.throttle_events += 1

    async def get_stats(self) -> Mapping[str, float | int | None]:
        """
        Get current rate limit statistics.

        Returns:
            Dictionary containing rate limit statistics including:
            - remaining_quota: Current remaining API quota
            - last_request_cost: Cost of the last request
            - total_requests: Total number of requests made
            - total_cost: Total cost of all requests
            - throttle_events: Number of times requests were throttled
            - last_update: Timestamp of last rate limit update
        """
        async with self._lock:
            return {
                "remaining_quota": self.remaining_quota,
                "last_request_cost": self.last_request_cost,
                "total_requests": self.total_requests,
                "total_cost": self.total_cost,
                "throttle_events": self.throttle_events,
                "last_update": self.last_update,
            }

    async def get_remaining_quota(self) -> float | None:
        """
        Get the current remaining quota in a thread-safe manner.

        Returns:
            The remaining quota or None if not yet determined.
        """
        async with self._lock:
            return self.remaining_quota

    async def reset(self) -> None:
        """Reset all rate limiting statistics to initial state."""
        async with self._lock:
            self.remaining_quota = None
            self.last_request_cost = None
            self.last_update = None
            self.total_requests = 0
            self.total_cost = 0.0
            self.throttle_events = 0
