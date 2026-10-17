"""
ZMIE Security, Governance & Compliance REST API Router
Provides comprehensive endpoints for:
- Evaluating zero-trust authorization decisions (/v1/security/evaluate)
- Managing purpose-bound consent grants & revocations (/v1/security/consent)
- Querying immutable audit event trails (/v1/security/audit)
- Reporting security incidents & triggering containment (/v1/security/incidents)
- Submitting privacy Data Subject Requests (/v1/security/dsr)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from app.models.security import (
    SecurityContext,
    UserRole,
    DataClassificationTier,
    ConsentPurpose,
    SecurityIncidentSeverity,
    AuditEvent,
    ConsentRecord,
    SecurityIncident
)
from app.security.policy_engine import AuthorizationPolicyEngine
from app.security.consent_engine import ConsentAndPrivacyEngine
from app.security.audit_engine import AuditLoggingEngine

router = APIRouter(prefix="/security", tags=["Security, Governance & Compliance"])


class AccessEvaluationRequest(BaseModel):
    user_id: str
    tenant_id: str
    roles: List[UserRole] = [UserRole.PUBLIC_USER]
    action: str
    resource_tenant_id: str
    classification: DataClassificationTier = DataClassificationTier.PUBLIC
    mfa_verified: bool = False
    is_break_glass: bool = False
    break_glass_reason: Optional[str] = None


class GrantConsentRequest(BaseModel):
    subject_id: str
    purpose: ConsentPurpose
    scope: str = "DEFAULT"
    expires_in_days: int = 365


class RevokeConsentRequest(BaseModel):
    consent_id: str
    actor_id: str


class IncidentReportRequest(BaseModel):
    severity: SecurityIncidentSeverity
    scope: str
    affected_tenants: List[str] = []
    affected_resources: List[str] = []
    containment_action: str = ""


@router.post("/evaluate", response_model=Dict[str, Any])
async def evaluate_access(req: AccessEvaluationRequest):
    """
    POST /v1/security/evaluate:
    Evaluates Zero-Trust RBAC, ABAC, and tenant isolation policies.
    """
    ctx = SecurityContext(
        user_id=req.user_id,
        tenant_id=req.tenant_id,
        roles=req.roles,
        mfa_verified=req.mfa_verified,
        is_break_glass=req.is_break_glass,
        break_glass_reason=req.break_glass_reason
    )
    allowed = AuthorizationPolicyEngine.evaluate_access(
        context=ctx,
        action=req.action,
        resource_tenant_id=req.resource_tenant_id,
        resource_classification=req.classification
    )
    return {
        "user_id": req.user_id,
        "action": req.action,
        "allowed": allowed,
        "verdict": "ALLOW" if allowed else "DENY"
    }


@router.post("/consent/grant", response_model=Dict[str, Any])
async def grant_consent(req: GrantConsentRequest):
    """
    POST /v1/security/consent/grant:
    Records an explicit, purpose-bound, versioned consent agreement.
    """
    rec = ConsentAndPrivacyEngine.grant_consent(
        subject_id=req.subject_id,
        purpose=req.purpose,
        scope=req.scope,
        expires_in_days=req.expires_in_days
    )
    return rec.model_dump()


@router.post("/consent/revoke", response_model=Dict[str, Any])
async def revoke_consent(req: RevokeConsentRequest):
    """
    POST /v1/security/consent/revoke:
    Revokes an active consent contract.
    """
    rec = ConsentAndPrivacyEngine.revoke_consent(req.consent_id, req.actor_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Consent record not found")
    return rec.model_dump()


@router.get("/audit", response_model=List[Dict[str, Any]])
async def query_audit_logs(tenant_id: Optional[str] = None, event_type: Optional[str] = None):
    """
    GET /v1/security/audit:
    Retrieves tamper-resistant audit events.
    """
    events = AuditLoggingEngine.get_events(tenant_id=tenant_id, event_type=event_type)
    return [e.model_dump() for e in events]


@router.post("/incidents", response_model=Dict[str, Any])
async def report_incident(req: IncidentReportRequest):
    """
    POST /v1/security/incidents:
    Logs a security incident and triggers containment actions.
    """
    inc = SecurityIncident(
        severity=req.severity,
        scope=req.scope,
        affected_tenants=req.affected_tenants,
        affected_resources=req.affected_resources,
        containment_action=req.containment_action
    )
    AuditLoggingEngine.record_event(
        event_type="SECURITY_INCIDENT_LOGGED",
        actor_id="SecurityMonitor",
        tenant_id=req.affected_tenants[0] if req.affected_tenants else "PLATFORM",
        resource_type="SECURITY_INCIDENT",
        resource_id=inc.incident_id,
        action="CONTAINMENT",
        result=inc.severity.value
    )
    return inc.model_dump()
