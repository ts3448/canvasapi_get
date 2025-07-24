"""Enhanced global coordination of rate limits across concurrent Canvas API requests."""

import asyncio
import logging
import threading
import time
from collections.abc import Mapping

from canvasapi_get.async_rate_limit_state import AsyncRateLimitState

logger = logging.getLogger(__name__)


class RateLimitCoordinator:
    """
    Thread-safe coordinator for rate limiting across multiple concurrent Canvas API requests.
    
    This class manages global semaphores that dynamically adjust based on remaining API quota
    to prevent rate limit violations while maximizing throughput. Enhanced with comprehensive
    monitoring, health tracking, and cross-context thread safety.
    """

    def __init__(
        self,
        rate_limit_state: AsyncRateLimitState,
        base_concurrency: int = 3,
        max_concurrency: int = 10,
        min_concurrency: int = 1,
    ):
        """
        Initialize the enhanced rate limit coordinator.

        Args:
            rate_limit_state: Shared rate limit state tracker.
            base_concurrency: Default number of concurrent requests.
            max_concurrency: Maximum allowed concurrent requests.
            min_concurrency: Minimum concurrent requests (emergency mode).
        """
        self.rate_limit_state = rate_limit_state
        self.base_concurrency = base_concurrency
        self.max_concurrency = max_concurrency
        self.min_concurrency = min_concurrency
        
        # Core semaphore management - lazily initialized
        self._semaphore: asyncio.Semaphore | None = None
        self._current_limit = base_concurrency
        self._adjustment_lock: asyncio.Lock | None = None
        self._circuit_breaker_event: asyncio.Event | None = None
        
        # Thread safety for cross-context operations
        self._thread_lock = threading.RLock()
        
        # Enhanced monitoring and health tracking
        self._total_acquires = 0
        self._total_releases = 0
        self._circuit_breaker_trips = 0
        self._last_adjustment_time: float | None = None
        self._adjustment_history: list[tuple[float, int]] = []  # (timestamp, concurrency)
        self._max_history = 50
        
        # Performance metrics
        self._acquire_times: list[float] = []
        self._release_times: list[float] = []
        self._max_timing_history = 100
        
        # Health monitoring
        self._coordinator_health = 100.0
        self._last_health_update = time.time()

    async def _ensure_async_primitives(self) -> tuple[asyncio.Semaphore, asyncio.Lock, asyncio.Event]:
        """Ensure async primitives exist for current event loop."""
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self._current_limit)
        if self._adjustment_lock is None:
            self._adjustment_lock = asyncio.Lock()
        if self._circuit_breaker_event is None:
            self._circuit_breaker_event = asyncio.Event()
            self._circuit_breaker_event.set()  # Start in "open" state (requests allowed)
        return self._semaphore, self._adjustment_lock, self._circuit_breaker_event

    async def acquire(self) -> None:
        """
        Acquire permission to make a request with enhanced monitoring.
        
        This method will block if the circuit breaker is tripped or if the
        semaphore limit is reached. Tracks acquisition timing for performance analysis.
        """
        acquire_start = time.time()
        
        logger.debug("RateLimitCoordinator.acquire() called")
        
        # Ensure async primitives exist
        logger.debug("About to call _ensure_async_primitives()")
        semaphore, _, circuit_breaker_event = await self._ensure_async_primitives()
        logger.debug(f"Async primitives ensured - semaphore has {semaphore._value} permits available")
        
        # Wait for circuit breaker to be open
        logger.debug("About to wait for circuit breaker event")
        await circuit_breaker_event.wait()
        logger.debug("Circuit breaker event passed")
        
        # Acquire semaphore permit
        logger.debug("About to acquire semaphore permit")
        await semaphore.acquire()
        logger.debug("Semaphore permit acquired")
        
        # Track metrics
        acquire_end = time.time()
        with self._thread_lock:
            self._total_acquires += 1
            self._acquire_times.append(acquire_end - acquire_start)
            if len(self._acquire_times) > self._max_timing_history:
                self._acquire_times.pop(0)
        
        logger.debug(f"Semaphore acquired (#{self._total_acquires})")

    def release(self) -> None:
        """Release the request permit with enhanced tracking."""
        release_time = time.time()
        
        # Release semaphore permit - only if it exists
        if self._semaphore is not None:
            self._semaphore.release()
        
        # Track metrics
        with self._thread_lock:
            self._total_releases += 1
            self._release_times.append(release_time)
            if len(self._release_times) > self._max_timing_history:
                self._release_times.pop(0)
        
        logger.debug(f"Semaphore released (#{self._total_releases})")

    async def adjust_concurrency(self) -> None:
        """
        Adjust the concurrency limit based on current rate limit state with enhanced logic.
        
        This method uses sophisticated algorithms to dynamically adjust concurrency based on
        quota, health scores, and historical performance patterns.
        """
        _, adjustment_lock, _ = await self._ensure_async_primitives()
        async with adjustment_lock:
            with self._thread_lock:
                current_time = time.time()
                remaining_quota = await self.rate_limit_state.get_remaining_quota()
                health_score = await self.rate_limit_state.get_health_score()
                
                # Calculate new limit using enhanced algorithm
                new_limit = await self._calculate_optimal_concurrency(
                    remaining_quota, health_score
                )
                
                # Only adjust if there's a meaningful change
                if abs(new_limit - self._current_limit) >= 1:
                    await self._adjust_semaphore_limit(new_limit)
                    
                    # Record adjustment in history
                    self._adjustment_history.append((current_time, new_limit))
                    if len(self._adjustment_history) > self._max_history:
                        self._adjustment_history.pop(0)
                    
                    self._last_adjustment_time = current_time
                
                # Update coordinator health
                self._update_coordinator_health(health_score)

    async def _calculate_optimal_concurrency(
        self, remaining_quota: float | None, health_score: float
    ) -> int:
        """
        Calculate optimal concurrency using advanced algorithms.

        Args:
            remaining_quota: Current remaining API quota.
            health_score: Current health score (0-100).

        Returns:
            Optimal concurrency limit.
        """
        # Base calculation on quota
        if remaining_quota is None:
            quota_based_limit = self.base_concurrency
        elif remaining_quota < 5:
            quota_based_limit = self.min_concurrency
        elif remaining_quota < 20:
            quota_based_limit = min(
                self.base_concurrency, 
                max(self.min_concurrency, int(remaining_quota // 3))
            )
        elif remaining_quota < 50:
            quota_based_limit = min(
                self.max_concurrency // 2,
                max(self.base_concurrency, int(remaining_quota // 5))
            )
        else:
            quota_based_limit = min(
                self.max_concurrency,
                max(self.base_concurrency, int(remaining_quota // 8))
            )
        
        # Adjust based on health score
        health_modifier = health_score / 100.0
        health_adjusted_limit = int(quota_based_limit * health_modifier)
        
        # Ensure we don't go below minimum
        final_limit = max(self.min_concurrency, health_adjusted_limit)
        
        # Cap at maximum
        final_limit = min(self.max_concurrency, final_limit)
        
        logger.debug(
            f"Concurrency calculation - Quota: {remaining_quota}, "
            f"Health: {health_score:.1f}%, Quota-based: {quota_based_limit}, "
            f"Health-adjusted: {health_adjusted_limit}, Final: {final_limit}"
        )
        
        return final_limit

    async def _adjust_semaphore_limit(self, new_limit: int) -> None:
        """
        Adjust the semaphore limit with enhanced error handling.

        Args:
            new_limit: The new concurrency limit to set.
        """
        if new_limit != self._current_limit:
            old_limit = self._current_limit
            
            try:
                # Create new semaphore with adjusted limit
                self._semaphore = asyncio.Semaphore(new_limit)
                self._current_limit = new_limit
                
                logger.info(
                    f"Concurrency adjusted from {old_limit} to {new_limit} "
                    f"(Range: {self.min_concurrency}-{self.max_concurrency})"
                )
                
            except Exception as e:
                logger.error(f"Failed to adjust semaphore limit to {new_limit}: {e}")
                # Keep old semaphore if adjustment fails

    async def trip_circuit_breaker(self, recovery_delay: float = 5.0) -> None:
        """
        Trip the circuit breaker to pause all requests with enhanced monitoring.

        Args:
            recovery_delay: How long to wait before allowing requests again.
        """
        with self._thread_lock:
            self._circuit_breaker_trips += 1
        
        logger.warning(
            f"Circuit breaker tripped (#{self._circuit_breaker_trips}), "
            f"pausing all requests for {recovery_delay}s"
        )
        
        await self.rate_limit_state.record_throttle()
        
        # Ensure circuit breaker exists
        _, _, circuit_breaker_event = await self._ensure_async_primitives()
        
        # Clear the event to block all new requests
        circuit_breaker_event.clear()
        
        try:
            # Wait for recovery period
            await asyncio.sleep(recovery_delay)
        finally:
            # Always re-enable requests
            circuit_breaker_event.set()
            logger.info("Circuit breaker recovered, resuming requests")

    async def get_current_concurrency(self) -> int:
        """
        Get the current concurrency limit in thread-safe manner.

        Returns:
            Current maximum number of concurrent requests allowed.
        """
        _, adjustment_lock, _ = await self._ensure_async_primitives()
        async with adjustment_lock:
            with self._thread_lock:
                return self._current_limit

    async def get_stats(self) -> Mapping[str, int | float | bool]:
        """
        Get comprehensive coordinator statistics.

        Returns:
            Dictionary containing detailed coordinator state information.
        """
        with self._thread_lock:
            # Calculate utilization metrics
            utilization = (
                (self._total_acquires - self._total_releases) / self._current_limit
                if self._current_limit > 0 else 0.0
            )
            
            # Calculate average acquire/release times
            avg_acquire_time = (
                sum(self._acquire_times) / len(self._acquire_times)
                if self._acquire_times else 0.0
            )
            
            recent_adjustments = len([
                adj for adj in self._adjustment_history
                if time.time() - adj[0] <= 300  # Last 5 minutes
            ])
            
            return {
                "current_concurrency": self._current_limit,
                "max_concurrency": self.max_concurrency,
                "min_concurrency": self.min_concurrency,
                "base_concurrency": self.base_concurrency,
                "circuit_breaker_open": self._circuit_breaker_event.is_set() if self._circuit_breaker_event else True,
                "available_permits": getattr(self._semaphore, '_value', 0) if self._semaphore else 0,
                "total_acquires": self._total_acquires,
                "total_releases": self._total_releases,
                "circuit_breaker_trips": self._circuit_breaker_trips,
                "utilization": min(1.0, max(0.0, utilization)),
                "avg_acquire_time": avg_acquire_time,
                "recent_adjustments": recent_adjustments,
                "coordinator_health": self._coordinator_health,
                "last_adjustment_time": self._last_adjustment_time,
            }

    async def get_health_status(self) -> dict[str, float | bool | str]:
        """
        Get detailed health status of the coordinator.

        Returns:
            Dictionary with health indicators and status.
        """
        with self._thread_lock:
            stats = await self.get_stats()
            rate_limit_health = await self.rate_limit_state.get_health_score()
            
            # Determine overall health status
            overall_health = (self._coordinator_health + rate_limit_health) / 2.0
            
            if overall_health >= 80:
                status = "excellent"
            elif overall_health >= 60:
                status = "good"
            elif overall_health >= 40:
                status = "fair"
            elif overall_health >= 20:
                status = "poor"
            else:
                status = "critical"
            
            return {
                "overall_health": overall_health,
                "coordinator_health": self._coordinator_health,
                "rate_limit_health": rate_limit_health,
                "status": status,
                "circuit_breaker_healthy": self._circuit_breaker_event.is_set() if self._circuit_breaker_event else True,
                "utilization_healthy": stats["utilization"] < 0.9,
                "adjustment_frequency_healthy": stats["recent_adjustments"] < 10,
            }

    def _update_coordinator_health(self, rate_limit_health: float) -> None:
        """
        Update coordinator health based on performance metrics.

        Args:
            rate_limit_health: Current rate limit health score.
        """
        current_time = time.time()
        
        # Base health on rate limit health
        target_health = rate_limit_health
        
        # Adjust based on circuit breaker trips
        if self._circuit_breaker_trips > 0:
            trip_penalty = min(30.0, self._circuit_breaker_trips * 10.0)
            target_health = max(0.0, target_health - trip_penalty)
        
        # Adjust based on utilization
        utilization = (
            (self._total_acquires - self._total_releases) / self._current_limit
            if self._current_limit > 0 else 0.0
        )
        
        if utilization > 0.95:
            target_health = max(0.0, target_health - 10.0)
        
        # Gradual health recovery
        recovery_rate = 0.05  # 5% recovery per update
        time_since_update = current_time - self._last_health_update
        
        if time_since_update > 60.0:  # Reset if too much time has passed
            self._coordinator_health = target_health
        elif self._coordinator_health < target_health:
            recovery = min(
                target_health - self._coordinator_health,
                recovery_rate * (target_health - self._coordinator_health)
            )
            self._coordinator_health += recovery
        else:
            self._coordinator_health = target_health
        
        self._last_health_update = current_time

    def get_sync_health_status(self) -> dict[str, float | str]:
        """
        Get basic health status synchronously for cross-context monitoring.

        Returns:
            Dictionary with essential health indicators.
        """
        with self._thread_lock:
            overall_health = self._coordinator_health
            
            if overall_health >= 80:
                status = "excellent"
            elif overall_health >= 60:
                status = "good"
            elif overall_health >= 40:
                status = "fair"
            elif overall_health >= 20:
                status = "poor"
            else:
                status = "critical"
            
            return {
                "coordinator_health": self._coordinator_health,
                "status": status,
                "current_concurrency": self._current_limit,
                "circuit_breaker_trips": self._circuit_breaker_trips,
            }
