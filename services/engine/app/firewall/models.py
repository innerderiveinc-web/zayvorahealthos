"""
ZMIE Scientific Trust Firewall & Real-Source Verification Models
Scientific Trust Firewall & Real-Source Verification Data Models
"""

from __future__ import annotations
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


# --- Enums for Sections 5, 6, 7, 14, 17, 18, 24, 25, 27, 29, 42, 48, 65 ---

class VerificationState(str, Enum):
    # Standard states (Section 6)
    UNKNOWN = "UNKNOWN"
    UNVERIFIED = "UNVERIFIED"
    CANDIDATE = "CANDIDATE"
    PARTIALLY_VERIFIED = "PARTIALLY_VERIFIED"
    SOURCE_VERIFIED = "SOURCE_VERIFIED"
    EVIDENCE_VERIFIED = "EVIDENCE_VERIFIED"
    CROSS_VERIFIED = "CROSS_VERIFIED"
    EXPERT_REVIEWED = "EXPERT_REVIEWED"
    AUTHORITATIVE = "AUTHORITATIVE"

    # Negative / Exception states
    CONTESTED = "CONTESTED"
    CONFLICTING = "CONFLICTING"
    REJECTED = "REJECTED"
    RETRACTED = "RETRACTED"
    INVALID = "INVALID"
    SUPERSEDED = "SUPERSEDED"
    UNAVAILABLE = "UNAVAILABLE"
    INACCESSIBLE = "INACCESSIBLE"
    QUARANTINED = "QUARANTINED"


class AssuranceLevel(str, Enum):
    """Section 7: Separate assurance dimension from verification state."""
    A0_UNKNOWN = "A0_UNKNOWN"
    A1_SOURCE_LEVEL = "A1_SOURCE_LEVEL"
    A2_CONTENT_LEVEL = "A2_CONTENT_LEVEL"
    A3_CLAIM_LEVEL = "A3_CLAIM_LEVEL"
    A4_MULTI_SOURCE_VERIFIED = "A4_MULTI_SOURCE_VERIFIED"
    A5_EXPERT_GOVERNANCE_ASSURED = "A5_EXPERT_GOVERNANCE_ASSURED"


class SourceAccessState(str, Enum):
    """Section 14: Source access availability states."""
    FULLY_ACCESSIBLE = "FULLY_ACCESSIBLE"
    PARTIALLY_ACCESSIBLE = "PARTIALLY_ACCESSIBLE"
    METADATA_ONLY = "METADATA_ONLY"
    ABSTRACT_ONLY = "ABSTRACT_ONLY"
    SNIPPET_ONLY = "SNIPPET_ONLY"
    PAYWALLED = "PAYWALLED"
    UNAVAILABLE = "UNAVAILABLE"
    REMOVED = "REMOVED"
    RESTRICTED = "RESTRICTED"


class CitationStatus(str, Enum):
    """Section 17: Citation validity and status."""
    VALID = "VALID"
    PARTIALLY_SUPPORTING = "PARTIALLY_SUPPORTING"
    WEAKLY_SUPPORTING = "WEAKLY_SUPPORTING"
    NOT_SUPPORTING = "NOT_SUPPORTING"
    MISATTRIBUTED = "MISATTRIBUTED"
    BROKEN = "BROKEN"
    UNVERIFIED = "UNVERIFIED"
    OUTDATED = "OUTDATED"
    RETRACTED = "RETRACTED"


class ClaimEntailmentState(str, Enum):
    """Section 18: Claim-to-citation entailment."""
    DIRECTLY_SUPPORTED = "DIRECTLY_SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTING"
    INDIRECTLY_RELATED = "INDIRECTLY_RELATED"
    CONTEXTUAL_ONLY = "CONTEXTUAL_ONLY"
    NOT_SUPPORTED = "NOT_SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    UNKNOWN = "UNKNOWN"


class ComputationResultState(str, Enum):
    """Section 24: Computation result states."""
    CALCULATED = "CALCULATED"
    VALIDATED_CALCULATION = "VALIDATED_CALCULATION"
    SIMULATED = "SIMULATED"
    MODEL_PREDICTION = "MODEL_PREDICTION"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


class ExperimentClaimState(str, Enum):
    """Section 25: Experiment claim states."""
    PROPOSED_EXPERIMENT = "PROPOSED_EXPERIMENT"
    SIMULATED_EXPERIMENT = "SIMULATED_EXPERIMENT"
    EXECUTED_EXPERIMENT = "EXECUTED_EXPERIMENT"
    OBSERVED_RESULT = "OBSERVED_RESULT"
    VALIDATED_RESULT = "VALIDATED_RESULT"


class DatasetStatus(str, Enum):
    """Section 27: Dataset authenticity status."""
    DISCOVERED = "DISCOVERED"
    REGISTERED = "REGISTERED"
    INGESTED = "INGESTED"
    VALIDATED = "VALIDATED"
    QUARANTINED = "QUARANTINED"
    APPROVED = "APPROVED"
    SUPERSEDED = "SUPERSEDED"
    RETRACTED = "RETRACTED"


class ResearcherIdentityState(str, Enum):
    """Section 29: Researcher identity resolution."""
    VERIFIED_IDENTITY = "VERIFIED_IDENTITY"
    PROBABLE_IDENTITY = "PROBABLE_IDENTITY"
    AMBIGUOUS_IDENTITY = "AMBIGUOUS_IDENTITY"
    UNKNOWN_IDENTITY = "UNKNOWN_IDENTITY"


class TraditionalMappingStatus(str, Enum):
    """Section 42: Traditional to biomedical mapping firewall."""
    EXACT_EQUIVALENCE = "EXACT_EQUIVALENCE"
    PARTIAL_EQUIVALENCE = "PARTIAL_EQUIVALENCE"
    RELATED = "RELATED"
    HISTORICAL_CORRESPONDENCE = "HISTORICAL_CORRESPONDENCE"
    TRADITIONAL_CORRESPONDENCE = "TRADITIONAL_CORRESPONDENCE"
    CANDIDATE = "CANDIDATE"
    NO_VALID_MAPPING = "NO_VALID_MAPPING"
    CONTESTED = "CONTESTED"


class ToolExecutionState(str, Enum):
    """Section 48: Tool result validation states."""
    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    REJECTED = "REJECTED"
    UNKNOWN = "UNKNOWN"


class TrustDecision(str, Enum):
    """Section 65: Trust Decision Engine outputs."""
    ALLOW = "ALLOW"
    ALLOW_WITH_LABEL = "ALLOW_WITH_LABEL"
    RESTRICT = "RESTRICT"
    REQUIRE_REVIEW = "REQUIRE_REVIEW"
    QUARANTINE = "QUARANTINE"
    REJECT = "REJECT"


class CanonicalSourceRegistry(str, Enum):
    CROSSREF = "CROSSREF"
    PUBMED_NLM = "PUBMED_NLM"
    CLINICAL_TRIALS_GOV = "CLINICAL_TRIALS_GOV"
    OPENALEX = "OPENALEX"
    TKDL = "TKDL"
    WHO_IRIS = "WHO_IRIS"
    FDA_ORANGE_BOOK = "FDA_ORANGE_BOOK"
    EMA_EPAR = "EMA_EPAR"


# Backward compatibility alias
TrustFirewallDecision = TrustDecision


# --- Section 5: Canonical TrustAssessment Model ---

class TrustAssessment(BaseModel):
    trust_assessment_id: str
    object_type: str  # "source", "claim", "evidence", "dataset", "computation", etc.
    object_id: str
    assessment_type: str = "COMPREHENSIVE_FIREWALL_EVALUATION"
    status: VerificationState = VerificationState.UNVERIFIED
    assurance_level: AssuranceLevel = AssuranceLevel.A0_UNKNOWN
    source_reference: Optional[str] = None
    verification_method: str = "DETERMINISTIC_REGISTRY_AND_ENTAILMENT"
    verification_timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    verified_by: str = "ZMIE-Scientific-Trust-Firewall"
    evidence_reference: Optional[str] = None
    conflict_state: str = "NONE"  # "NONE", "CONFLICTING", "CONTESTED"
    temporal_state: str = "CURRENT"  # "CURRENT", "OUTDATED", "SUPERSEDED"
    license_state: str = "VERIFIED_ACCESSIBLE"
    availability_state: SourceAccessState = SourceAccessState.FULLY_ACCESSIBLE
    integrity_state: str = "CRYPTOGRAPHICALLY_VERIFIED"
    notes: List[str] = Field(default_factory=list)
    version: str = "1.0.0"
    tenant_id: str = "system"


# --- Section 65 & 144: Trust Decision Explanation ---

class TrustDecisionReport(BaseModel):
    decision_id: str
    object_id: str
    object_type: str
    decision: TrustDecision
    rules_evaluated: List[str]
    failed_rules: List[str]
    assessment: TrustAssessment
    epistemic_drift_score: float = 0.0
    verified_passage_hash: Optional[str] = None
    decision_reason: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


# --- Backward compatibility models ---

class SourceVerificationResult(BaseModel):
    is_authentic: bool
    registry: CanonicalSourceRegistry
    identifier: str
    doi: Optional[str] = None
    pmid: Optional[str] = None
    title: Optional[str] = None
    journal: Optional[str] = None
    issn: Optional[str] = None
    publication_year: Optional[int] = None
    is_retracted: bool = False
    retraction_notice_url: Optional[str] = None
    is_predatory_venue: bool = False
    paper_mill_risk: str = "LOW"
    content_hash_match: bool = False
    verification_score: float = Field(ge=0.0, le=1.0)
    flags: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class FirewallEvaluationReport(BaseModel):
    evaluation_id: str
    claim_id: Optional[str] = None
    claim_text: str
    doi_examined: Optional[str] = None
    trust_decision: TrustDecision
    rules_evaluated: List[str]
    failed_rules: List[str]
    epistemic_drift_score: float = Field(ge=0.0, le=1.0)
    verified_passage_hash: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class SourceLedgerEntry(BaseModel):
    ledger_id: str
    identifier: str
    registry: CanonicalSourceRegistry
    title: str
    canonical_hash: str
    verified_by: str
    trust_tier: str
    first_verified_at: str
    last_synced_at: str
    tamper_proof_hmac: str


# --- Section 93: Quarantine Item ---

class QuarantineItem(BaseModel):
    quarantine_id: str
    object_id: str
    object_type: str
    reason: str
    detection_rule: str
    source_identifier: Optional[str] = None
    quarantined_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    reviewer: Optional[str] = None
    resolution_status: str = "PENDING_REVIEW"
    tenant_id: str = "system"


# --- Section 101: Trust Incident ---

class TrustIncident(BaseModel):
    incident_id: str
    incident_type: str  # "FABRICATED_CITATION", "UNAUTHORIZED_PROMOTION", "SOURCE_RETRACTED", etc.
    severity: str = "HIGH"
    object_id: str
    summary: str
    affected_outputs: List[str] = Field(default_factory=list)
    detected_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    status: str = "ACTIVE"
    resolution_actions_taken: List[str] = Field(default_factory=list)


# --- Section 178: Scientific Trust Certificate ---

class ScientificTrustCertificate(BaseModel):
    certificate_id: str
    object_id: str
    object_type: str
    version: str
    verification_state: VerificationState
    assurance_level: AssuranceLevel
    evidence_state: str
    provenance_hash: str
    last_verification: str
    review_state: str
    policy_version: str
    digital_signature: str
    issued_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


# --- Section 77: Scientific Trust Graph Node & Edge ---

class TrustGraphNode(BaseModel):
    node_id: str
    node_type: str  # "Source", "Claim", "Evidence", "Researcher", "Study", etc.
    label: str
    verification_state: VerificationState
    assurance_level: AssuranceLevel
    provenance_hash: Optional[str] = None


class TrustGraphEdge(BaseModel):
    source_id: str
    target_id: str
    relation: str  # "AUTHORED_BY", "SUPPORTS", "CONTRADICTS", "VERIFIES", "DEPENDS_ON", "RETRACTS"
    provenance_id: Optional[str] = None
