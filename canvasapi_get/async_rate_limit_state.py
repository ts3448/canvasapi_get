"""Thread-safe async rate limiting state management for Canvas API requests."""

import asyncio
import threading
import time
import logging
from collections.abc import Mapping

logger = logging.getLogger(__name__)


class AsyncRateLimitState:
    """
    Thread-safe rate limiting state tracker for async Canvas API requests.
    
    This class manages rate limit information from Canvas API response headers and provides
    statistics for monitoring API usage patterns. All operations are thread-safe and can
    be safely accessed from multiple contexts including background loops.
    """

    def __init__(self):
        """Initialize thread-safe async rate limit tracking state."""
        self.remaining_quota: float | None = None
        self.last_request_cost: float | None = None
        self.last_update: float | None = None
        self.total_requests: int = 0
        self.total_cost: float = 0.0
        self.throttle_events: int = 0
        
        # Async lock for async contexts - lazily initialized
        self._async_lock: asyncio.Lock | None = None
        
        # Thread lock for cross-context safety
        self._thread_lock = threading.RLock()
        
        # Performance metrics
        self._request_times: list[float] = []
        self._max_request_history = 100
        
        # Health monitoring
        self._consecutive_throttles = 0
        self._last_throttle_time: float | None = None
        self._health_score = 100.0  # 0-100 scale

    async def _ensure_async_lock(self) -> asyncio.Lock:
        """Ensure async lock exists for current event loop."""
        if self._async_lock is None:
            self._async_lock = asyncio.Lock()
        return self._async_lock

    async def update(self, cost: float | None, remaining: float | None) -> None:
        """
        Update rate limit state from response headers in thread-safe manner.

        Args:
            cost: The cost of the last request from X-Request-Cost header.
            remaining: The remaining quota from X-Rate-Limit-Remaining header.
        """
        current_time = time.time()
        
        async_lock = await self._ensure_async_lock()
        async with async_lock:
            with self._thread_lock:
                # Update basic state
                self.last_request_cost = cost
                self.remaining_quota = remaining
                self.last_update = current_time
                self.total_requests += 1
                
                if cost is not None:
                    self.total_cost += cost
                
                # Track request timing for performance analysis
                self._request_times.append(current_time)
                if len(self._request_times) > self._max_request_history:
                    self._request_times.pop(0)
                
                # Update health score based on quota
                self._update_health_score(remaining)
                
                # Reset consecutive throttles on successful request
                self._consecutive_throttles = 0
                
                logger.debug(
                    f"Rate limit updated - Cost: {cost}, Remaining: {remaining}, "
                    f"Health: {self._health_score:.1f}%"
                )

    async def record_throttle(self) -> None:
        """Record a throttling event with enhanced tracking."""
        current_time = time.time()
        
        async_lock = await self._ensure_async_lock()
        async with async_lock:
            with self._thread_lock:
                self.throttle_events += 1
                self._consecutive_throttles += 1
                self._last_throttle_time = current_time
                
                # Reduce health score based on throttling severity
                throttle_penalty = min(20.0, self._consecutive_throttles * 5.0)
                self._health_score = max(0.0, self._health_score - throttle_penalty)
                
                logger.warning(
                    f"Throttle event recorded - Total: {self.throttle_events}, "
                    f"Consecutive: {self._consecutive_throttles}, Health: {self._health_score:.1f}%"
                )

    async def get_stats(self) -> Mapping[str, float | int | None]:
        """
        Get comprehensive rate limit statistics in thread-safe manner.

        Returns:
            Dictionary containing detailed rate limit statistics including:
            - remaining_quota: Current remaining API quota
            - last_request_cost: Cost of the last request
            - total_requests: Total number of requests made
            - total_cost: Total cost of all requests
            - throttle_events: Number of times requests were throttled
            - last_update: Timestamp of last rate limit update
            - health_score: Current health score (0-100)
            - consecutive_throttles: Number of consecutive throttle events
            - avg_request_cost: Average cost per request
            - request_rate: Recent request rate (requests per second)
        """
        async_lock = await self._ensure_async_lock()
        async with async_lock:
            with self._thread_lock:
                avg_cost = (
                    self.total_cost / self.total_requests 
                    if self.total_requests > 0 
                    else 0.0
                )
                
                # Calculate recent request rate
                request_rate = self._calculate_request_rate()
                
                return {
                    "remaining_quota": self.remaining_quota,
                    "last_request_cost": self.last_request_cost,
                    "total_requests": self.total_requests,
                    "total_cost": self.total_cost,
                    "throttle_events": self.throttle_events,
                    "last_update": self.last_update,
                    "health_score": self._health_score,
                    "consecutive_throttles": self._consecutive_throttles,
                    "avg_request_cost": avg_cost,
                    "request_rate": request_rate,
                    "last_throttle_time": self._last_throttle_time,
                }

    async def get_remaining_quota(self) -> float | None:
        """
        Get the current remaining quota in a thread-safe manner.

        Returns:
            The remaining quota or None if not yet determined.
        """
        async_lock = await self._ensure_async_lock()
        async with async_lock:
            with self._thread_lock:
                return self.remaining_quota

    async def get_health_score(self) -> float:
        """
        Get the current health score (0-100) indicating rate limiting performance.

        Returns:
            Health score from 0 (unhealthy) to 100 (excellent).
        """
        async_lock = await self._ensure_async_lock()
        async with async_lock:
            with self._thread_lock:
                return self._health_score

    async def is_healthy(self, threshold: float = 50.0) -> bool:
        """
        Check if the rate limiting state is considered healthy.

        Args:
            threshold: Minimum health score to consider healthy.

        Returns:
            True if health score is above threshold.
        """
        health = await self.get_health_score()
        return health >= threshold

    async def reset(self) -> None:
        """Reset all rate limiting statistics to initial state in thread-safe manner."""
        async_lock = await self._ensure_async_lock()
        async with async_lock:
            with self._thread_lock:
                self.remaining_quota = None
                self.last_request_cost = None
                self.last_update = None
                self.total_requests = 0
                self.total_cost = 0.0
                self.throttle_events = 0
                self._consecutive_throttles = 0
                self._last_throttle_time = None
                self._health_score = 100.0
                self._request_times.clear()
                
                logger.info("Rate limit state reset to initial values")

    def _update_health_score(self, remaining_quota: float | None) -> None:
        """
        Update health score based on current quota and throttling patterns.
        
        Args:
            remaining_quota: Current remaining API quota.
        """
        if remaining_quota is None:
            return
            
        # Quota-based health scoring
        if remaining_quota > 100:
            quota_score = 100.0
        elif remaining_quota > 50:
            quota_score = 80.0 + (remaining_quota - 50) * 0.4
        elif remaining_quota > 20:
            quota_score = 50.0 + (remaining_quota - 20) * 1.0
        elif remaining_quota > 5:
            quota_score = 20.0 + (remaining_quota - 5) * 2.0
        else:
            quota_score = max(0.0, remaining_quota * 4.0)
        
        # Gradual recovery towards quota-based score
        target_score = quota_score
        recovery_rate = 0.1  # 10% recovery per update
        
        if self._health_score < target_score:
            # Recover gradually
            self._health_score = min(
                target_score,
                self._health_score + (target_score - self._health_score) * recovery_rate
            )
        else:
            # Immediate adjustment downward if quota drops
            self._health_score = target_score

    def _calculate_request_rate(self) -> float:
        """
        Calculate recent request rate based on timing history.
        
        Returns:
            Requests per second over recent history.
        """
        if len(self._request_times) < 2:
            return 0.0
            
        current_time = time.time()
        # Consider only requests in the last 60 seconds
        recent_times = [
            t for t in self._request_times 
            if current_time - t <= 60.0
        ]
        
        if len(recent_times) < 2:
            return 0.0
            
        time_span = recent_times[-1] - recent_times[0]
        if time_span <= 0:
            return 0.0
            
        return (len(recent_times) - 1) / time_span

    def get_sync_stats(self) -> Mapping[str, float | int | None]:
        """
        Get basic statistics synchronously for cross-context access.
        
        This method provides thread-safe access to basic stats without requiring
        an async context, useful for debugging and monitoring from sync contexts.

        Returns:
            Dictionary with basic rate limiting statistics.
        """
        with self._thread_lock:
            return {
                "remaining_quota": self.remaining_quota,
                "total_requests": self.total_requests,
                "throttle_events": self.throttle_events,
                "health_score": self._health_score,
                "consecutive_throttles": self._consecutive_throttles,
            }
