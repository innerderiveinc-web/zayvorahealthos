"""
ZMIE Admin Control Plane API Router (Sections 93, 94 & 95)
"""

from fastapi import APIRouter, Query
from typing import List
from app.agents.admin_service import (
    AdminControlPlaneService,
    SystemTelemetry,
    KnowledgeQualityMetrics,
    ResearchPlatformMetrics,
    AdminAuditLogEntry
)

router = APIRouter(prefix="/admin", tags=["Admin Control Plane & Observability (Sec 93-95)"])


@router.get("/telemetry", response_model=SystemTelemetry)
async def get_system_telemetry():
    """
    Returns live engine health, memory consumption, queue depths, and connection pool status.
    """
    return AdminControlPlaneService.get_system_telemetry()


@router.get("/quality-dashboard", response_model=KnowledgeQualityMetrics)
async def get_knowledge_quality_dashboard():
    """
    Returns Section 94 metrics: Claims, retraction quarantines, review queues, and zero-hallucination stats.
    """
    return AdminControlPlaneService.get_knowledge_quality_metrics()


@router.get("/research-metrics", response_model=ResearchPlatformMetrics)
async def get_research_platform_metrics():
    """
    Returns Section 95 metrics: Research job durations, contradiction detection rates, and gap maps.
    """
    return AdminControlPlaneService.get_research_platform_metrics()


@router.get("/audit-logs", response_model=List[AdminAuditLogEntry])
async def get_audit_trail(limit: int = Query(10, ge=1, le=100)):
    """
    Returns Section 67 audit trail records tracking who, what, and when.
    """
    return AdminControlPlaneService.list_audit_logs(limit=limit)
