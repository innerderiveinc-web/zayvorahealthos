"""
ZMIE Production Security & Privacy Hardening Models
Enterprise Zero-Trust Security & Privacy Data Models

Implements canonical models for:
- Data Classification (Clause 13)
- Zero Trust Access Decisions & Evaluation (Clauses 15, 23-26)
- Credential Registry & Rotation (Clauses 20, 37-39)
- External Model Routing Firewall (Clauses 52-56)
- Agent Action Security & Sandbox (Clauses 60-71)
- Security Findings & Scorecards (Clauses 250-255)
- Security Incident Response & Quarantine (Clauses 118-123)
- Disaster Recovery & Resilience (Clauses 124-144)
- Retention & Legal Hold (Clauses 160-163)
- Security Release Gates (Clauses 273-276)
- Backwards compatible models (Privacy, PHI, Encryption, Break-Glass, Injection)
"""

from __future__ import annotations
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


# --- CLAUSE 13: Data Classification ---
class DataClassification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"
    HIGHLY_SENSITIVE = "HIGHLY_SENSITIVE"


# --- CLAUSE 15, 26: Access Decision ---
class AccessDecision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_MFA = "REQUIRE_MFA"
    REQUIRE_REVIEW = "REQUIRE_REVIEW"


class AccessEvaluationResult(BaseModel):
    decision: AccessDecision
    identity: str
    tenant_id: str
    resource: str
    action: str
    classification: DataClassification
    reason: str
    audit_id: str = Field(default_factory=lambda: f"audit-acc-{uuid.uuid4().hex[:10]}")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


# --- CLAUSE 20, 37-39: Credential Registry ---
class CredentialStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ROTATED = "ROTATED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"


class CredentialRecord(BaseModel):
    key_id: str = Field(default_factory=lambda: f"key-{uuid.uuid4().hex[:10]}")
    tenant_id: str
    owner: str
    scope: str
    key_hash: str
    status: CredentialStatus = CredentialStatus.ACTIVE
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    expires_at: str
    last_used_at: Optional[str] = None
    rotated_at: Optional[str] = None


# --- CLAUSE 52-56: External Model Firewall ---
class ModelRoutingDecision(BaseModel):
    is_allowed: bool
    model_provider: str
    data_classification: DataClassification
    risk_level: str
    reason: str
    redacted_context_preview: Optional[str] = None
    audit_id: str = Field(default_factory=lambda: f"audit-model-{uuid.uuid4().hex[:10]}")


# --- CLAUSE 60-71: Agent Security Model ---
class AgentSecurityEvaluation(BaseModel):
    agent_id: str
    action: str
    is_allowed: bool
    budget_remaining: int
    risk_score: float
    reason: str
    action_taken: str  # ALLOW, BLOCK, QUARANTINE


# --- CLAUSE 252-255: Security Findings ---
class SecurityFindingSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class SecurityFindingStatus(str, Enum):
    OPEN = "OPEN"
    IN_REVIEW = "IN_REVIEW"
    REMEDIATED = "REMEDIATED"
    ACCEPTED_RISK = "ACCEPTED_RISK"


class SecurityFinding(BaseModel):
    finding_id: str = Field(default_factory=lambda: f"find-{uuid.uuid4().hex[:10]}")
    severity: SecurityFindingSeverity
    asset: str
    description: str
    owner: str
    status: SecurityFindingStatus = SecurityFindingStatus.OPEN
    remediation: str
    due_date: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


# --- CLAUSE 118-123: Security Incident Response ---
class IncidentSeverity(str, Enum):
    P0_CRITICAL = "P0_CRITICAL"
    P1_HIGH = "P1_HIGH"
    P2_MEDIUM = "P2_MEDIUM"
    P3_LOW = "P3_LOW"


class SecurityIncident(BaseModel):
    incident_id: str = Field(default_factory=lambda: f"inc-{uuid.uuid4().hex[:10]}")
    title: str
    severity: IncidentSeverity
    status: str = "DETECTED"  # DETECTED, CONTAINED, RESOLVED
    affected_assets: List[str]
    quarantine_applied: bool = False
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    resolved_at: Optional[str] = None
    root_cause: Optional[str] = None


# --- CLAUSE 124-144: Disaster Recovery & Resilience ---
class DisasterRecoveryTestResult(BaseModel):
    recovery_id: str = Field(default_factory=lambda: f"dr-{uuid.uuid4().hex[:10]}")
    component: str
    status: str  # RECOVERED, FAILED
    rpo_achieved_seconds: float
    rto_achieved_seconds: float
    data_integrity_verified: bool
    snapshot_hash: str
    executed_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


# --- CLAUSE 160-163: Data Retention & Legal Hold ---
class RetentionState(str, Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    EXPIRED = "EXPIRED"
    LEGAL_HOLD = "LEGAL_HOLD"
    DELETED = "DELETED"


class RetentionRecord(BaseModel):
    record_id: str
    tenant_id: str
    state: RetentionState = RetentionState.ACTIVE
    legal_hold: bool = False
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    expires_at: str


# --- CLAUSE 273-276: Security Release Gate ---
class SecurityReleaseGateResult(BaseModel):
    is_approved: bool
    blockers: List[str]
    critical_findings_count: int
    tenant_isolation_verified: bool
    secrets_exposed_count: int
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


# =========================================================================
# BACKWARDS COMPATIBLE MODELS
# =========================================================================

class PrivacyMechanism(str, Enum):
    LAPLACE = "LAPLACE"
    GAUSSIAN = "GAUSSIAN"


class PHIIdentifierType(str, Enum):
    NAME = "NAME"
    MRN = "MRN"
    DATE = "DATE"
    LOCATION = "LOCATION"
    PHONE = "PHONE"
    EMAIL = "EMAIL"
    SSN = "SSN"
    AGE_OVER_89 = "AGE_OVER_89"


class DeidentificationResult(BaseModel):
    original_text_hash: str
    sanitized_text: str
    identifiers_redacted: List[Dict[str, Any]]
    date_jitter_applied_days: Optional[int] = None
    compliance_standard: str = "HIPAA_SAFE_HARBOR_18_IDENTIFIERS"
    processed_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class DifferentialPrivacyQueryResult(BaseModel):
    raw_value: float
    noisy_value: float
    epsilon: float
    delta: float
    sensitivity: float
    mechanism: PrivacyMechanism
    noise_magnitude: float
    is_privacy_guaranteed: bool = True
    privacy_budget_consumed: float


class EnvelopeEncryptedArtifact(BaseModel):
    artifact_id: str
    tenant_id: str
    encrypted_dek_b64: str
    iv_b64: str
    ciphertext_b64: str
    auth_tag_b64: str
    kms_key_id: str
    algorithm: str = "AES-256-GCM"
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class BreakGlassAuthorization(BaseModel):
    request_id: str
    tenant_id: str
    patient_cohort_id: str
    physician_id: str
    compliance_officer_id: str
    clinical_justification: str
    is_approved: bool
    granted_at: str
    expires_at: str
    tamper_proof_audit_signature: str


class PromptInjectionScanResult(BaseModel):
    is_safe: bool
    risk_score: float = Field(ge=0.0, le=1.0)
    detected_attack_vectors: List[str]
    action: str  # "ALLOW", "FLAG", "BLOCK"
