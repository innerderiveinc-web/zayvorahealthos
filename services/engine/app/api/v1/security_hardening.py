"""
ZMIE Production Security & Privacy Hardening FastAPI Router
Zero-Trust Security & Hardening REST Gateway
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.security.engine import ProductionSecurityHardeningEngine
from app.security.models import (
    DifferentialPrivacyQueryResult,
    DeidentificationResult,
    EnvelopeEncryptedArtifact,
    BreakGlassAuthorization,
    PromptInjectionScanResult,
    DataClassification,
    AccessDecision,
    AccessEvaluationResult,
    CredentialRecord,
    ModelRoutingDecision,
    AgentSecurityEvaluation,
    SecurityFinding,
    SecurityFindingSeverity,
    SecurityIncident,
    IncidentSeverity,
    DisasterRecoveryTestResult,
    RetentionRecord,
    SecurityReleaseGateResult,
)

router = APIRouter(prefix="/security-hardening", tags=["Production Security & Privacy Hardening"])

# Global singleton
_security_engine = ProductionSecurityHardeningEngine()


def get_security_engine() -> ProductionSecurityHardeningEngine:
    return _security_engine


# --- Request DTOs ---

class DifferentialPrivacyRequest(BaseModel):
    raw_value: float
    epsilon: float = 0.5
    delta: float = 1e-5
    sensitivity: float = 1.0


class DeidentifyRequest(BaseModel):
    raw_text: str
    jitter_dates: bool = True


class EnvelopeEncryptRequest(BaseModel):
    tenant_id: str
    artifact_id: str
    plaintext_data: str
    kms_key_id: str = "kms-key-zmie-master-01"


class BreakGlassRequest(BaseModel):
    tenant_id: str
    patient_cohort_id: str
    physician_id: str
    compliance_officer_id: str
    clinical_justification: str


class ScanPromptRequest(BaseModel):
    user_prompt: str


class AccessEvaluationRequest(BaseModel):
    identity: str
    caller_tenant_id: str
    resource_id: str
    action: str
    classification: DataClassification = DataClassification.INTERNAL
    user_roles: Optional[List[str]] = None
    resource_tenant_id: Optional[str] = None


class CredentialRegisterRequest(BaseModel):
    tenant_id: str
    owner: str
    scope: str
    secret_plaintext: str
    ttl_days: int = 90


class CredentialRotateRequest(BaseModel):
    key_id: str
    new_secret_plaintext: str


class CredentialRevokeRequest(BaseModel):
    key_id: str
    reason: str = "Manual revocation"


class ModelRoutingRequest(BaseModel):
    tenant_id: str
    model_provider: str
    context_text: str
    classification: DataClassification = DataClassification.INTERNAL


class AgentSecurityRequest(BaseModel):
    agent_id: str
    action_type: str
    tool_name: str
    token_cost: int = 100


class WebhookVerifyRequest(BaseModel):
    payload_text: str
    signature: str
    timestamp: float
    nonce: str


class CreateIncidentRequest(BaseModel):
    title: str
    severity: IncidentSeverity
    affected_assets: List[str]
    apply_quarantine: bool = True


class ResolveIncidentRequest(BaseModel):
    incident_id: str
    root_cause: str


class DisasterRecoveryRequest(BaseModel):
    component: str
    snapshot_payload: str


class LegalHoldRequest(BaseModel):
    record_id: str
    tenant_id: str


# =========================================================================
# EXISTING ENDPOINTS (Backwards Compatible)
# =========================================================================

@router.post("/differential-privacy", response_model=DifferentialPrivacyQueryResult)
def apply_differential_privacy(
    req: DifferentialPrivacyRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.apply_differential_privacy(
        raw_value=req.raw_value,
        epsilon=req.epsilon,
        delta=req.delta,
        sensitivity=req.sensitivity
    )


@router.post("/deidentify", response_model=DeidentificationResult)
def deidentify_clinical_text(
    req: DeidentifyRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.deidentify_clinical_text(
        raw_text=req.raw_text,
        jitter_dates=req.jitter_dates
    )


@router.post("/envelope-encrypt", response_model=EnvelopeEncryptedArtifact)
def envelope_encrypt(
    req: EnvelopeEncryptRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.envelope_encrypt(
        tenant_id=req.tenant_id,
        artifact_id=req.artifact_id,
        plaintext_data=req.plaintext_data,
        kms_key_id=req.kms_key_id
    )


@router.post("/break-glass", response_model=BreakGlassAuthorization)
def request_break_glass_access(
    req: BreakGlassRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.request_break_glass_access(
        tenant_id=req.tenant_id,
        patient_cohort_id=req.patient_cohort_id,
        physician_id=req.physician_id,
        compliance_officer_id=req.compliance_officer_id,
        clinical_justification=req.clinical_justification
    )


@router.post("/scan-prompt", response_model=PromptInjectionScanResult)
def scan_prompt(
    req: ScanPromptRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.scan_for_adversarial_prompt(req.user_prompt)


# =========================================================================
# ZERO TRUST & ACCESS EVALUATION (Clauses 15, 23-30)
# =========================================================================

@router.post("/access/evaluate", response_model=AccessEvaluationResult)
def evaluate_access(
    req: AccessEvaluationRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.evaluate_access(
        identity=req.identity,
        caller_tenant_id=req.caller_tenant_id,
        resource_id=req.resource_id,
        action=req.action,
        classification=req.classification,
        user_roles=req.user_roles,
        resource_tenant_id=req.resource_tenant_id
    )


# =========================================================================
# CREDENTIALS & SECRETS (Clauses 20, 37-39)
# =========================================================================

@router.post("/credentials/register", response_model=CredentialRecord)
def register_credential(
    req: CredentialRegisterRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.register_credential(
        tenant_id=req.tenant_id,
        owner=req.owner,
        scope=req.scope,
        secret_plaintext=req.secret_plaintext,
        ttl_days=req.ttl_days
    )


@router.post("/credentials/rotate", response_model=CredentialRecord)
def rotate_credential(
    req: CredentialRotateRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    try:
        return engine.rotate_credential(req.key_id, req.new_secret_plaintext)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/credentials/revoke")
def revoke_credential(
    req: CredentialRevokeRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    try:
        return engine.revoke_credential(req.key_id, req.reason)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# =========================================================================
# EXTERNAL MODEL & AGENT FIREWALLS (Clauses 52-71)
# =========================================================================

@router.post("/model-firewall/evaluate", response_model=ModelRoutingDecision)
def evaluate_model_routing(
    req: ModelRoutingRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.evaluate_model_routing(
        tenant_id=req.tenant_id,
        model_provider=req.model_provider,
        context_text=req.context_text,
        classification=req.classification
    )


@router.post("/agent-firewall/evaluate", response_model=AgentSecurityEvaluation)
def evaluate_agent_action(
    req: AgentSecurityRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.evaluate_agent_action(
        agent_id=req.agent_id,
        action_type=req.action_type,
        tool_name=req.tool_name,
        token_cost=req.token_cost
    )


# =========================================================================
# WEBHOOK SECURITY & REPLAY DEFENSE (Clauses 83-90)
# =========================================================================

@router.post("/webhooks/verify")
def verify_webhook(
    req: WebhookVerifyRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    res = engine.verify_webhook_signature(
        payload_bytes=req.payload_text.encode("utf-8"),
        signature=req.signature,
        timestamp=req.timestamp,
        nonce=req.nonce
    )
    if not res["is_valid"]:
        raise HTTPException(status_code=400, detail=res["reason"])
    return res


# =========================================================================
# INCIDENTS & QUARANTINE (Clauses 118-123)
# =========================================================================

@router.post("/incidents", response_model=SecurityIncident)
def create_incident(
    req: CreateIncidentRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.create_security_incident(
        title=req.title,
        severity=req.severity,
        affected_assets=req.affected_assets,
        apply_quarantine=req.apply_quarantine
    )


@router.post("/incidents/{incident_id}/resolve")
def resolve_incident(
    incident_id: str,
    root_cause: str = "Patched and verified",
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    try:
        return engine.resolve_security_incident(incident_id, root_cause)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# =========================================================================
# RESILIENCE, DR & SAFE DEGRADATION (Clauses 124-144)
# =========================================================================

@router.post("/disaster-recovery/simulate", response_model=DisasterRecoveryTestResult)
def simulate_dr(
    req: DisasterRecoveryRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.simulate_disaster_recovery(req.component, req.snapshot_payload)


@router.get("/outage/simulate/{service_name}")
def simulate_outage(
    service_name: str,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.simulate_service_outage(service_name)


# =========================================================================
# RETENTION & LEGAL HOLD (Clauses 160-163)
# =========================================================================

@router.post("/retention/legal-hold", response_model=RetentionRecord)
def place_legal_hold(
    req: LegalHoldRequest,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    # Register first if needed
    if req.record_id not in engine._retention_records:
        engine.apply_retention_policy(req.record_id, req.tenant_id)
    return engine.place_legal_hold(req.record_id)


@router.delete("/retention/records/{record_id}")
def delete_record(
    record_id: str,
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    res = engine.attempt_deletion(record_id)
    if res.get("status") == "BLOCKED":
        raise HTTPException(status_code=403, detail=res["reason"])
    return res


# =========================================================================
# FINDINGS, SCORECARD & RELEASE GATE (Clauses 250-255, 273-276)
# =========================================================================

@router.get("/findings", response_model=List[SecurityFinding])
def list_findings(
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.list_security_findings()


@router.get("/scorecard")
def get_scorecard(
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.get_security_scorecard()


@router.get("/release-gate", response_model=SecurityReleaseGateResult)
def evaluate_release_gate(
    engine: ProductionSecurityHardeningEngine = Depends(get_security_engine)
):
    return engine.evaluate_production_security_gate()
