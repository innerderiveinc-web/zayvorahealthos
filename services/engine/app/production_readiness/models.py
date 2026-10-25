"""
ZMIE Production Readiness & Pre-Flight Certification Models
Production Readiness Audit Data Models
Independent Production Gate, 28-Domain Audit Matrix, and Scope Profiles
"""

from __future__ import annotations
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class AuditPillar(str, Enum):
    INVARIANTS = "INVARIANTS"
    ARCHITECTURE = "ARCHITECTURE"
    CRYPTOGRAPHY = "CRYPTOGRAPHY"
    TENANCY_ISOLATION = "TENANCY_ISOLATION"
    RELIABILITY = "RELIABILITY"
    OBSERVABILITY = "OBSERVABILITY"
    COMPLIANCE_GXP = "COMPLIANCE_GXP"


class PillarStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class ProductionScope(str, Enum):
    """The 9 Independent Production Readiness Scopes (Clause 8)."""
    PUBLIC_SEARCH = "PUBLIC_SEARCH"
    PROFESSIONAL_RESEARCH = "PROFESSIONAL_RESEARCH"
    ENTERPRISE_PRIVATE_RESEARCH = "ENTERPRISE_PRIVATE_RESEARCH"
    SCIENTIFIC_COMPUTE = "SCIENTIFIC_COMPUTE"
    CLINICAL_DECISION_SUPPORT = "CLINICAL_DECISION_SUPPORT"
    REGULATORY_INTELLIGENCE = "REGULATORY_INTELLIGENCE"
    AGENTIC_RESEARCH = "AGENTIC_RESEARCH"
    FEDERATED_INTELLIGENCE = "FEDERATED_INTELLIGENCE"
    API_PLATFORM = "API_PLATFORM"


class ReadinessState(str, Enum):
    """Rigorous Production Readiness States (Clause 9)."""
    NOT_EVALUATED = "NOT_EVALUATED"
    NOT_READY = "NOT_READY"
    IN_DEVELOPMENT = "IN_DEVELOPMENT"
    VALIDATION_REQUIRED = "VALIDATION_REQUIRED"
    CONDITIONAL = "CONDITIONAL"
    READY_FOR_INTERNAL = "READY_FOR_INTERNAL"
    READY_FOR_PILOT = "READY_FOR_PILOT"
    READY_FOR_CONTROLLED_PRODUCTION = "READY_FOR_CONTROLLED_PRODUCTION"
    PRODUCTION_READY = "PRODUCTION_READY"
    RESTRICTED = "RESTRICTED"
    BLOCKED = "BLOCKED"
    DEPRECATED = "DEPRECATED"


class AuditDomain(str, Enum):
    """The 28 Comprehensive Production Audit Domains (Clause 260)."""
    ARCHITECTURE = "ARCHITECTURE"
    DATABASE = "DATABASE"
    APIS = "APIS"
    FRONTEND = "FRONTEND"
    SCIENTIFIC_VALIDATION = "SCIENTIFIC_VALIDATION"
    TRUST = "TRUST"
    EVIDENCE = "EVIDENCE"
    SEARCH = "SEARCH"
    DEEP_RESEARCH = "DEEP_RESEARCH"
    CLINICAL = "CLINICAL"
    REGULATORY = "REGULATORY"
    SAFETY = "SAFETY"
    TRADITIONAL_MEDICINE = "TRADITIONAL_MEDICINE"
    DATA = "DATA"
    COMPUTE = "COMPUTE"
    MODELS = "MODELS"
    AGENTS = "AGENTS"
    REPRODUCIBILITY = "REPRODUCIBILITY"
    REVALIDATION = "REVALIDATION"
    SECURITY = "SECURITY"
    PRIVACY = "PRIVACY"
    RELIABILITY = "RELIABILITY"
    DISASTER_RECOVERY = "DISASTER_RECOVERY"
    OBSERVABILITY = "OBSERVABILITY"
    GOVERNANCE = "GOVERNANCE"
    OPERATIONS = "OPERATIONS"
    DOCUMENTATION = "DOCUMENTATION"
    SUPPORT = "SUPPORT"


class PillarEvaluation(BaseModel):
    pillar: AuditPillar
    status: PillarStatus
    score: float = Field(ge=0.0, le=1.0)
    checks_passed: int
    checks_total: int
    details: List[str] = Field(default_factory=list)


class DomainAuditResult(BaseModel):
    domain: AuditDomain
    status: str  # "GO", "CONDITIONAL_GO", "NO_GO"
    blocking_issues: List[str] = Field(default_factory=list)
    evidence: str
    approved_scope: str
    residual_risk: str  # "LOW", "ACCEPTABLE_WITH_CONTROLS", "ELEVATED"


class ScopeReadinessResult(BaseModel):
    scope: ProductionScope
    state: ReadinessState
    decision: str  # "GO", "CONDITIONAL_GO", "NO_GO"
    conditions: List[str] = Field(default_factory=list)
    evidence_summary: str


class RiskItem(BaseModel):
    risk_id: str
    category: str  # "SCIENTIFIC", "SECURITY", "OPERATIONAL", "CLINICAL"
    description: str
    probability: str  # "LOW", "MEDIUM", "HIGH"
    impact: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    controls_in_place: str
    residual_risk: str  # "LOW", "ACCEPTABLE_WITH_CONTROLS"
    owner: str


class BlockerItem(BaseModel):
    blocker_id: str
    severity: str  # "CRITICAL", "HIGH", "MEDIUM"
    issue: str
    owner: str
    status: str  # "RESOLVED", "VERIFIED", "OPEN"
    verification_evidence: str


class ProductionReadinessCertificate(BaseModel):
    certificate_id: str
    verdict: str  # "GO" or "NO_GO"
    readiness_score: float = Field(ge=0.0, le=1.0)
    is_production_ready: bool
    evaluated_pillars: List[PillarEvaluation]
    critical_blockers: List[str] = Field(default_factory=list)
    release_candidate_id: str = "RC-ZMIE-2026.10-PROD-1"
    domain_matrix: Dict[str, DomainAuditResult] = Field(default_factory=dict)
    scope_profiles: Dict[str, ScopeReadinessResult] = Field(default_factory=dict)
    risk_register: List[RiskItem] = Field(default_factory=list)
    blocker_register: List[BlockerItem] = Field(default_factory=list)
    approved_scopes: List[str] = Field(default_factory=list)
    restricted_scopes: List[str] = Field(default_factory=list)
    stop_conditions: List[str] = Field(default_factory=list)
    rollback_plan: Dict[str, Any] = Field(default_factory=dict)
    early_life_monitoring: Dict[str, Any] = Field(default_factory=dict)
    release_manifest: Dict[str, Any] = Field(default_factory=dict)
    issued_by: str = "ZMIE-Enterprise-Readiness-Board"
    auditor_authority: str = "Independent Chief Production Readiness Auditor"
    digital_signature: str
    certified_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
