"""
ZMIE Admin Control Plane API Router (Sections 93, 94 & 95)
"""

from fastapi import APIRouter, Query, Depends
from typing import List
from app.agents.admin_service import (
    AdminControlPlaneService,
    SystemTelemetry,
    KnowledgeQualityMetrics,
    ResearchPlatformMetrics,
    AdminAuditLogEntry
)
from app.core.security import SecurityService, AuthContext, UserRole

router = APIRouter(prefix="/admin", tags=["Admin Control Plane & Observability (Sec 93-95)"])


@router.get("/telemetry", response_model=SystemTelemetry)
async def get_system_telemetry(auth: AuthContext = Depends(SecurityService.require_role([UserRole.ADMIN]))):
    """
    Returns live engine health, memory consumption, queue depths, and connection pool status.
    Protected: Requires PLATFORM_ADMIN role.
    """
    return AdminControlPlaneService.get_system_telemetry()


@router.get("/quality-dashboard", response_model=KnowledgeQualityMetrics)
async def get_knowledge_quality_dashboard(auth: AuthContext = Depends(SecurityService.require_role([UserRole.ADMIN, UserRole.RESEARCHER]))):
    """
    Returns Section 94 metrics: Claims, retraction quarantines, review queues, and zero-hallucination stats.
    Protected: Requires ADMIN or RESEARCHER role.
    """
    return AdminControlPlaneService.get_knowledge_quality_metrics()


@router.get("/research-metrics", response_model=ResearchPlatformMetrics)
async def get_research_platform_metrics(auth: AuthContext = Depends(SecurityService.require_role([UserRole.ADMIN, UserRole.RESEARCHER]))):
    """
    Returns Section 95 metrics: Research job durations, contradiction detection rates, and gap maps.
    Protected: Requires ADMIN or RESEARCHER role.
    """
    return AdminControlPlaneService.get_research_platform_metrics()


@router.get("/audit-logs", response_model=List[AdminAuditLogEntry])
async def get_audit_trail(
    limit: int = Query(10, ge=1, le=100),
    auth: AuthContext = Depends(SecurityService.require_role([UserRole.ADMIN]))
):
    """
    Returns Section 67 audit trail records tracking who, what, and when.
    Protected: Requires PLATFORM_ADMIN role.
    """
    return AdminControlPlaneService.list_audit_logs(limit=limit)
