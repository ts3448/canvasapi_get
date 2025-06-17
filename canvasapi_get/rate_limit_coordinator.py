"""Global coordination of rate limits across concurrent Canvas API requests."""

import asyncio
import logging
from collections.abc import Mapping

from canvasapi_get.async_rate_limit_state import AsyncRateLimitState

logger = logging.getLogger(__name__)


class RateLimitCoordinator:
    """
    Coordinates rate limiting across multiple concurrent Canvas API requests.
    
    This class manages a global semaphore that dynamically adjusts based on
    remaining API quota to prevent rate limit violations while maximizing
    throughput.
    """

    def __init__(
        self,
        rate_limit_state: AsyncRateLimitState,
        base_concurrency: int = 3,
        max_concurrency: int = 10,
        min_concurrency: int = 1,
    ):
        """
        Initialize the rate limit coordinator.

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
        
        self._semaphore = asyncio.Semaphore(base_concurrency)
        self._current_limit = base_concurrency
        self._adjustment_lock = asyncio.Lock()
        self._circuit_breaker_event = asyncio.Event()
        self._circuit_breaker_event.set()  # Start in "open" state (requests allowed)

    async def acquire(self) -> None:
        """
        Acquire permission to make a request.
        
        This method will block if the circuit breaker is tripped or if the
        semaphore limit is reached.
        """
        # Wait for circuit breaker to be open
        await self._circuit_breaker_event.wait()
        
        # Acquire semaphore permit
        await self._semaphore.acquire()

    def release(self) -> None:
        """Release the request permit."""
        self._semaphore.release()

    async def adjust_concurrency(self) -> None:
        """
        Adjust the concurrency limit based on current rate limit state.
        
        This method should be called after each request to dynamically
        adjust the semaphore based on remaining quota.
        """
        async with self._adjustment_lock:
            remaining_quota = await self.rate_limit_state.get_remaining_quota()
            
            if remaining_quota is None:
                # No quota information yet, use base concurrency
                new_limit = self.base_concurrency
            elif remaining_quota < 5:
                # Critical quota - emergency mode
                new_limit = self.min_concurrency
                logger.warning(f"Critical quota remaining: {remaining_quota}, reducing to emergency concurrency")
            elif remaining_quota < 20:
                # Low quota - conservative approach
                new_limit = min(self.base_concurrency, max(self.min_concurrency, int(remaining_quota // 3)))
                logger.info(f"Low quota remaining: {remaining_quota}, reducing concurrency to {new_limit}")
            elif remaining_quota < 50:
                # Medium quota - moderate concurrency
                new_limit = min(self.max_concurrency // 2, max(self.base_concurrency, int(remaining_quota // 5)))
            else:
                # High quota - allow maximum concurrency
                new_limit = min(self.max_concurrency, max(self.base_concurrency, int(remaining_quota // 10)))
                
            await self._adjust_semaphore_limit(new_limit)

    async def _adjust_semaphore_limit(self, new_limit: int) -> None:
        """
        Adjust the semaphore limit by creating a new semaphore if needed.

        Args:
            new_limit: The new concurrency limit to set.
        """
        if new_limit != self._current_limit:
            logger.debug(f"Adjusting concurrency from {self._current_limit} to {new_limit}")
            
            # Create new semaphore with adjusted limit
            old_semaphore = self._semaphore
            self._semaphore = asyncio.Semaphore(new_limit)
            self._current_limit = new_limit
            
            # If we're increasing the limit, we don't need to wait for old requests
            # If we're decreasing, the new semaphore will naturally limit new requests

    async def trip_circuit_breaker(self, recovery_delay: float = 5.0) -> None:
        """
        Trip the circuit breaker to pause all requests.

        Args:
            recovery_delay: How long to wait before allowing requests again.
        """
        logger.warning(f"Circuit breaker tripped, pausing all requests for {recovery_delay}s")
        await self.rate_limit_state.record_throttle()
        
        # Clear the event to block all new requests
        self._circuit_breaker_event.clear()
        
        # Wait for recovery period
        await asyncio.sleep(recovery_delay)
        
        # Re-enable requests
        self._circuit_breaker_event.set()
        logger.info("Circuit breaker recovered, resuming requests")

    async def get_current_concurrency(self) -> int:
        """
        Get the current concurrency limit.

        Returns:
            Current maximum number of concurrent requests allowed.
        """
        async with self._adjustment_lock:
            return self._current_limit

    async def get_stats(self) -> Mapping[str, int | bool]:
        """
        Get coordinator statistics.

        Returns:
            Dictionary containing coordinator state information.
        """
        return {
            "current_concurrency": self._current_limit,
            "max_concurrency": self.max_concurrency,
            "min_concurrency": self.min_concurrency,
            "circuit_breaker_open": self._circuit_breaker_event.is_set(),
            "available_permits": self._semaphore._value if hasattr(self._semaphore, '_value') else 0,
        }
