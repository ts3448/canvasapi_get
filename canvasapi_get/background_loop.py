"""
Background event loop infrastructure for unified sync/async Canvas API operations.

This module provides a singleton background thread with its own event loop that enables
synchronous code to internally use asynchronous operations for better performance while
maintaining a simple synchronous interface.
"""

import asyncio
import atexit
import threading
import logging
from collections.abc import Coroutine
from concurrent.futures import Future
from typing import Any

logger = logging.getLogger(__name__)

# Module-level singleton instances
_background_loop_instance: "BackgroundLoop | None" = None
_background_loop_lock = threading.Lock()


class BackgroundLoop:
    """
    A singleton background thread running its own asyncio event loop.

    This enables synchronous code to execute async operations by delegating
    them to a dedicated background thread, avoiding "wrong loop" errors and
    providing a bridge between sync and async execution contexts.
    """

    def __init__(self):
        """
        Initialize the background loop infrastructure.

        Creates a new thread with its own event loop for executing async operations
        from synchronous contexts.
        """
        self._thread: threading.Thread | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._ready_event = threading.Event()
        self._shutdown_event = threading.Event()
        self._started = False

    def start(self) -> None:
        """
        Start the background thread and event loop.

        This method is idempotent - calling it multiple times has no effect
        if the loop is already running.

        Raises:
            RuntimeError: If there's an error starting the background thread.
        """
        if self._started:
            return

        self._started = True
        logger.debug("Starting background event loop thread")

        # Create and start the background thread
        self._thread = threading.Thread(
            target=self._run_loop, name="CanvasAPI-BackgroundLoop", daemon=True
        )
        self._thread.start()

        # Wait for the loop to be ready
        if not self._ready_event.wait(timeout=10.0):
            raise RuntimeError("Background loop failed to start within 10 seconds")

        logger.debug("Background event loop is ready")

    def _run_loop(self) -> None:
        """
        Run the event loop in the background thread.

        This method runs in the background thread and should not be called directly.
        """
        try:
            # Create a new event loop for this thread
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

            logger.debug("Background event loop created")

            # Signal that the loop is ready
            self._ready_event.set()

            # Run until shutdown is requested
            self._loop.run_forever()

        except Exception as e:
            logger.error(f"Background event loop encountered an error: {e}")
            self._ready_event.set()  # Unblock waiting threads
        finally:
            # Cleanup
            if self._loop and not self._loop.is_closed():
                try:
                    # Cancel all remaining tasks
                    pending = asyncio.all_tasks(self._loop)
                    if pending:
                        logger.debug(f"Cancelling {len(pending)} pending tasks")
                        for task in pending:
                            task.cancel()

                        # Wait briefly for cancellation to complete
                        if pending:
                            self._loop.run_until_complete(
                                asyncio.gather(*pending, return_exceptions=True)
                            )
                finally:
                    self._loop.close()
                    logger.debug("Background event loop closed")

    def stop(self) -> None:
        """
        Stop the background thread and event loop.

        This method blocks until the background thread has fully stopped.
        It's safe to call multiple times.
        """
        if not self._started or self._shutdown_event.is_set():
            return

        logger.debug("Stopping background event loop")
        self._shutdown_event.set()

        if self._loop and not self._loop.is_closed():
            # Schedule the loop to stop

            # noinspection PyTypeChecker
            self._loop.call_soon_threadsafe(self._loop.stop, *())

        # Wait for the thread to finish
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)
            if self._thread.is_alive():
                logger.warning("Background thread did not stop within 5 seconds")

        logger.debug("Background event loop stopped")

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """
        Get the event loop instance.

        Returns:
            The asyncio event loop running in the background thread.

        Raises:
            RuntimeError: If the background loop is not running.
        """
        if not self._started or not self._loop:
            raise RuntimeError("Background loop is not running. Call start() first.")
        return self._loop

    @property
    def is_running(self) -> bool:
        """
        Check if the background loop is currently running.

        Returns:
            True if the background loop is active, False otherwise.
        """
        return (
            self._started
            and self._loop is not None
            and not self._loop.is_closed()
            and not self._shutdown_event.is_set()
        )

    def run_coroutine_threadsafe(self, coro: Coroutine) -> Any:
        """
        Execute a coroutine in the background loop from a synchronous context.

        This is the main bridge between sync and async code. It schedules the
        coroutine to run in the background thread and blocks until completion.

        Args:
            coro: The coroutine to execute.

        Returns:
            The result of the coroutine execution.

        Raises:
            RuntimeError: If the background loop is not running.
            Exception: Any exception raised by the coroutine.
        """
        if not self.is_running:
            raise RuntimeError("Background loop is not running")

        # Schedule the coroutine and wait for completion
        future: Future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        
        # Add timeout to prevent indefinite blocking
        # Use a reasonable timeout that's longer than typical request timeouts
        try:
            return future.result(timeout=60.0)  # 60 second timeout
        except asyncio.TimeoutError:
            # Cancel the future to clean up resources
            future.cancel()
            raise RuntimeError(
                "Coroutine execution timed out after 60 seconds. "
                "This may indicate a deadlock or network connectivity issue."
            )


def get_background_loop() -> BackgroundLoop:
    """
    Get the singleton background loop instance.

    This function ensures only one background loop exists per process and
    handles lazy initialization with proper thread safety.

    Returns:
        The singleton BackgroundLoop instance.
    """
    global _background_loop_instance

    # Double-checked locking pattern for thread-safe singleton
    if _background_loop_instance is None:
        with _background_loop_lock:
            if _background_loop_instance is None:
                _background_loop_instance = BackgroundLoop()
                _background_loop_instance.start()

                # Register cleanup function to run at exit
                atexit.register(_cleanup_background_loop)

    return _background_loop_instance


def _cleanup_background_loop() -> None:
    """
    Cleanup function called at process exit.

    Ensures the background loop is properly stopped when the process exits,
    preventing resource leaks and zombie threads.
    """
    global _background_loop_instance

    if _background_loop_instance is not None:
        logger.debug("Cleaning up background loop at exit")
        _background_loop_instance.stop()
        _background_loop_instance = None


def run_coroutine_threadsafe(coro: Coroutine) -> Any:
    """
    Convenience function to run a coroutine in the background loop.

    This is a shortcut for get_background_loop().run_coroutine_threadsafe(coro).
    It automatically handles getting the singleton instance and executing the coroutine.

    Args:
        coro: The coroutine to execute.

    Returns:
        The result of the coroutine execution.

    Raises:
        RuntimeError: If the background loop cannot be started.
        Exception: Any exception raised by the coroutine.
    """
    background_loop = get_background_loop()
    return background_loop.run_coroutine_threadsafe(coro)
