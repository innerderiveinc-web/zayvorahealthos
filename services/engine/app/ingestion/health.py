"""
ZMIE Source Health & Operational Telemetry Engine
Monitors the operational integrity of all external and sovereign data connectors:
- Health Status: HEALTHY, DEGRADED, UNAVAILABLE, BLOCKED, STALE
- Tracks API rate limits, error budgets, latency, and license contract renewals.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class SourceHealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"
    BLOCKED = "BLOCKED"
    STALE = "STALE"


class SourceHealthMetric(BaseModel):
    source_id: str
    source_name: str
    status: SourceHealthStatus
    latency_ms: float
    error_rate_pct: float
    rate_limit_remaining: int
    rate_limit_reset_seconds: int
    last_heartbeat: datetime = Field(default_factory=datetime.utcnow)
    license_valid_until: Optional[datetime] = None
    issues_detected: List[str] = Field(default_factory=list)


class SourceHealthMonitor:
    """
    Central operational monitor tracking connectivity, error budgets, and license expirations.
    """

    def __init__(self):
        self._metrics: Dict[str, SourceHealthMetric] = {}

    def record_heartbeat(
        self,
        source_id: str,
        source_name: str,
        latency_ms: float,
        errors: int,
        total_requests: int,
        rate_limit_remaining: int = 1000,
        license_valid_until: Optional[datetime] = None
    ) -> SourceHealthMetric:
        """
        Computes real-time health status based on error rates and latency.
        """
        error_rate = (errors / max(total_requests, 1)) * 100
        issues = []
        status = SourceHealthStatus.HEALTHY

        if rate_limit_remaining <= 0:
            status = SourceHealthStatus.BLOCKED
            issues.append("Provider rate limit completely exhausted.")
        elif error_rate > 50:
            status = SourceHealthStatus.UNAVAILABLE
            issues.append(f"High error rate: {error_rate:.1f}% exceeds 50% threshold.")
        elif error_rate > 10 or latency_ms > 2000:
            status = SourceHealthStatus.DEGRADED
            issues.append(f"Elevated latency ({latency_ms}ms) or error rate ({error_rate:.1f}%).")

        if license_valid_until and license_valid_until < datetime.utcnow():
            status = SourceHealthStatus.BLOCKED
            issues.append("Institutional source license expired.")

        metric = SourceHealthMetric(
            source_id=source_id,
            source_name=source_name,
            status=status,
            latency_ms=latency_ms,
            error_rate_pct=error_rate,
            rate_limit_remaining=rate_limit_remaining,
            rate_limit_reset_seconds=60,
            last_heartbeat=datetime.utcnow(),
            license_valid_until=license_valid_until,
            issues_detected=issues
        )
        self._metrics[source_id] = metric
        return metric

    def get_source_health(self, source_id: str) -> Optional[SourceHealthMetric]:
        metric = self._metrics.get(source_id)
        if metric and (datetime.utcnow() - metric.last_heartbeat) > timedelta(hours=24):
            metric.status = SourceHealthStatus.STALE
            metric.issues_detected.append("No telemetry heartbeat received in last 24 hours.")
        return metric

    def get_fleet_report(self) -> Dict[str, Any]:
        """
        Returns full system operational health across all data sources.
        """
        healthy = 0
        degraded = 0
        unavailable = 0
        blocked = 0
        stale = 0

        for metric in self._metrics.values():
            if metric.status == SourceHealthStatus.HEALTHY:
                healthy += 1
            elif metric.status == SourceHealthStatus.DEGRADED:
                degraded += 1
            elif metric.status == SourceHealthStatus.UNAVAILABLE:
                unavailable += 1
            elif metric.status == SourceHealthStatus.BLOCKED:
                blocked += 1
            elif metric.status == SourceHealthStatus.STALE:
                stale += 1

        return {
            "total_monitored_sources": len(self._metrics),
            "healthy_count": healthy,
            "degraded_count": degraded,
            "unavailable_count": unavailable,
            "blocked_count": blocked,
            "stale_count": stale,
            "sources": {k: v.model_dump() for k, v in self._metrics.items()},
            "fleet_status": "OPERATIONAL" if (unavailable + blocked) == 0 else "DEGRADED"
        }
