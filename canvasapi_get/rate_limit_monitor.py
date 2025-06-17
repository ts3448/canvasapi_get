"""Comprehensive monitoring and observability for Canvas API rate limiting."""

import asyncio
import logging
import time
import threading
from collections.abc import Mapping
from datetime import datetime, timedelta

from canvasapi_get.async_rate_limit_state import AsyncRateLimitState
from canvasapi_get.rate_limit_coordinator import RateLimitCoordinator

logger = logging.getLogger(__name__)


class RateLimitMonitor:
    """
    Advanced monitoring system for Canvas API rate limiting performance.
    
    Provides comprehensive observability, alerting, and performance analysis
    for rate limiting operations across all execution contexts.
    """

    def __init__(
        self,
        rate_limit_state: AsyncRateLimitState,
        coordinator: RateLimitCoordinator,
        alert_threshold: float = 30.0,
        monitor_interval: float = 60.0,
    ):
        """
        Initialize the rate limit monitor.

        Args:
            rate_limit_state: The rate limit state to monitor.
            coordinator: The coordinator to monitor.
            alert_threshold: Health score threshold for alerts.
            monitor_interval: Monitoring check interval in seconds.
        """
        self.rate_limit_state = rate_limit_state
        self.coordinator = coordinator
        self.alert_threshold = alert_threshold
        self.monitor_interval = monitor_interval
        
        # Monitoring state
        self._monitoring_active = False
        self._monitor_task: asyncio.Task | None = None
        self._thread_lock = threading.Lock()
        
        # Alert tracking
        self._alerts_sent: list[tuple[float, str]] = []
        self._alert_cooldown = 300.0  # 5 minutes between same alert types
        
        # Performance history
        self._performance_snapshots: list[dict] = []
        self._max_snapshots = 288  # 24 hours of 5-minute snapshots
        
        # Trend analysis
        self._trend_window = 1800.0  # 30 minutes for trend analysis

    async def start_monitoring(self) -> None:
        """Start the background monitoring task."""
        if self._monitoring_active:
            logger.warning("Rate limit monitoring is already active")
            return
            
        self._monitoring_active = True
        self._monitor_task = asyncio.create_task(self._monitor_loop())
        logger.info(f"Rate limit monitoring started (interval: {self.monitor_interval}s)")

    async def stop_monitoring(self) -> None:
        """Stop the background monitoring task."""
        if not self._monitoring_active:
            return
            
        self._monitoring_active = False
        
        if self._monitor_task and not self._monitor_task.done():
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
                
        logger.info("Rate limit monitoring stopped")

    async def get_performance_report(self) -> dict[str, any]:
        """
        Generate comprehensive performance report.

        Returns:
            Dictionary containing detailed performance analysis.
        """
        with self._thread_lock:
            if not self._performance_snapshots:
                return {"error": "No performance data available"}
            
            latest = self._performance_snapshots[-1]
            
            # Calculate trends
            trends = self._calculate_trends()
            
            # Generate summary statistics
            summary = self._generate_summary_stats()
            
            return {
                "timestamp": latest["timestamp"],
                "current_status": latest,
                "trends": trends,
                "summary": summary,
                "alert_history": self._get_recent_alerts(),
            }

    def get_sync_status(self) -> dict[str, any]:
        """
        Get current status synchronously for cross-context access.

        Returns:
            Dictionary with current rate limiting status.
        """
        with self._thread_lock:
            rate_stats = self.rate_limit_state.get_sync_stats()
            coordinator_stats = self.coordinator.get_sync_health_status()
            
            return {
                "monitoring_active": self._monitoring_active,
                "rate_limit": rate_stats,
                "coordinator": coordinator_stats,
                "snapshots_collected": len(self._performance_snapshots),
            }

    async def _monitor_loop(self) -> None:
        """Main monitoring loop that runs continuously."""
        while self._monitoring_active:
            try:
                await self._perform_monitoring_check()
                await asyncio.sleep(self.monitor_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(self.monitor_interval)

    async def _perform_monitoring_check(self) -> None:
        """Perform a comprehensive monitoring check."""
        current_time = time.time()
        
        # Collect current metrics
        rate_stats = await self.rate_limit_state.get_stats()
        coordinator_stats = await self.coordinator.get_stats()
        health_status = await self.coordinator.get_health_status()
        
        # Create performance snapshot
        snapshot = {
            "timestamp": current_time,
            "rate_limit": rate_stats,
            "coordinator": coordinator_stats,
            "health": health_status,
        }
        
        # Store snapshot
        with self._thread_lock:
            self._performance_snapshots.append(snapshot)
            if len(self._performance_snapshots) > self._max_snapshots:
                self._performance_snapshots.pop(0)
        
        # Check for alert conditions
        await self._check_alert_conditions(snapshot)
        
        # Log monitoring summary
        self._log_monitoring_summary(snapshot)

    async def _check_alert_conditions(self, snapshot: dict) -> None:
        """
        Check for conditions that warrant alerts.

        Args:
            snapshot: Current performance snapshot.
        """
        current_time = snapshot["timestamp"]
        health = snapshot["health"]
        
        # Critical health alert
        if health["overall_health"] < self.alert_threshold:
            await self._send_alert(
                "critical_health",
                f"Rate limiting health critically low: {health['overall_health']:.1f}%",
                current_time
            )
        
        # Circuit breaker alert
        if not health["circuit_breaker_healthy"]:
            await self._send_alert(
                "circuit_breaker",
                "Circuit breaker is currently tripped",
                current_time
            )
        
        # High utilization alert
        if not health["utilization_healthy"]:
            utilization = snapshot["coordinator"]["utilization"]
            await self._send_alert(
                "high_utilization",
                f"Concurrency utilization critically high: {utilization:.1%}",
                current_time
            )

    async def _send_alert(self, alert_type: str, message: str, timestamp: float) -> None:
        """
        Send an alert if not in cooldown period.

        Args:
            alert_type: Type of alert being sent.
            message: Alert message.
            timestamp: When the alert condition was detected.
        """
        with self._thread_lock:
            # Check if we're in cooldown for this alert type
            recent_alerts = [
                (t, atype) for t, atype in self._alerts_sent
                if timestamp - t < self._alert_cooldown and atype == alert_type
            ]
            
            if recent_alerts:
                logger.debug(f"Alert '{alert_type}' suppressed due to cooldown")
                return
            
            # Send the alert
            logger.warning(f"RATE LIMIT ALERT [{alert_type}]: {message}")
            
            # Record the alert
            self._alerts_sent.append((timestamp, alert_type))
            
            # Clean old alerts
            cutoff = timestamp - (self._alert_cooldown * 10)  # Keep 10x cooldown period
            self._alerts_sent = [
                (t, atype) for t, atype in self._alerts_sent if t > cutoff
            ]

    def _log_monitoring_summary(self, snapshot: dict) -> None:
        """
        Log a summary of current monitoring state.

        Args:
            snapshot: Current performance snapshot.
        """
        health = snapshot["health"]
        rate_stats = snapshot["rate_limit"]
        coordinator_stats = snapshot["coordinator"]
        
        logger.info(
            f"Rate Limit Monitor - Health: {health['overall_health']:.1f}% "
            f"({health['status']}), Quota: {rate_stats.get('remaining_quota', 'Unknown')}, "
            f"Concurrency: {coordinator_stats['current_concurrency']}, "
            f"Requests: {rate_stats['total_requests']}, "
            f"Throttles: {rate_stats['throttle_events']}"
        )

    def _calculate_trends(self) -> dict[str, any]:
        """
        Calculate performance trends over the trend window.

        Returns:
            Dictionary containing trend analysis.
        """
        if len(self._performance_snapshots) < 2:
            return {"error": "Insufficient data for trend analysis"}
        
        current_time = self._performance_snapshots[-1]["timestamp"]
        cutoff_time = current_time - self._trend_window
        
        # Get snapshots within trend window
        trend_snapshots = [
            s for s in self._performance_snapshots if s["timestamp"] > cutoff_time
        ]
        
        if len(trend_snapshots) < 2:
            return {"error": "Insufficient recent data for trend analysis"}
        
        # Calculate health trend
        health_values = [s["health"]["overall_health"] for s in trend_snapshots]
        health_trend = "improving" if health_values[-1] > health_values[0] else "declining"
        
        # Calculate request rate trend
        request_counts = [s["rate_limit"]["total_requests"] for s in trend_snapshots]
        request_rate = (request_counts[-1] - request_counts[0]) / (len(trend_snapshots) - 1)
        
        # Calculate throttle trend
        throttle_counts = [s["rate_limit"]["throttle_events"] for s in trend_snapshots]
        throttle_trend = "increasing" if throttle_counts[-1] > throttle_counts[0] else "stable"
        
        return {
            "window_minutes": self._trend_window / 60,
            "health_trend": health_trend,
            "health_change": health_values[-1] - health_values[0],
            "request_rate": request_rate,
            "throttle_trend": throttle_trend,
            "throttle_increase": throttle_counts[-1] - throttle_counts[0],
        }

    def _generate_summary_stats(self) -> dict[str, any]:
        """
        Generate summary statistics from historical data.

        Returns:
            Dictionary containing summary statistics.
        """
        if not self._performance_snapshots:
            return {"error": "No performance data available"}
        
        # Health statistics
        health_scores = [s["health"]["overall_health"] for s in self._performance_snapshots]
        avg_health = sum(health_scores) / len(health_scores)
        min_health = min(health_scores)
        max_health = max(health_scores)
        
        # Request statistics
        latest_requests = self._performance_snapshots[-1]["rate_limit"]["total_requests"]
        latest_throttles = self._performance_snapshots[-1]["rate_limit"]["throttle_events"]
        
        # Concurrency statistics
        concurrency_values = [s["coordinator"]["current_concurrency"] for s in self._performance_snapshots]
        avg_concurrency = sum(concurrency_values) / len(concurrency_values)
        
        return {
            "data_points": len(self._performance_snapshots),
            "health": {
                "average": avg_health,
                "minimum": min_health,
                "maximum": max_health,
            },
            "requests": {
                "total": latest_requests,
                "throttled": latest_throttles,
                "throttle_rate": latest_throttles / max(1, latest_requests),
            },
            "concurrency": {
                "average": avg_concurrency,
                "current": concurrency_values[-1],
            },
        }

    def _get_recent_alerts(self) -> list[dict]:
        """
        Get recent alerts for the performance report.

        Returns:
            List of recent alert information.
        """
        current_time = time.time()
        recent_cutoff = current_time - 3600  # Last hour
        
        recent_alerts = [
            {
                "timestamp": t,
                "type": alert_type,
                "time_ago_seconds": current_time - t,
            }
            for t, alert_type in self._alerts_sent
            if t > recent_cutoff
        ]
        
        return sorted(recent_alerts, key=lambda x: x["timestamp"], reverse=True)
