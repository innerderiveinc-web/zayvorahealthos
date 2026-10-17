"""
ZMIE Scientific Credibility, Verification & Provenance Models
Prompt 29 — Credibility Doctrine, Epistemic Levels & Verification Lifecycle
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field


class VerificationState(str, Enum):
    """
    Non-negotiable verification states for every scientific object in ZMIE.
    Strictly hierarchical progression with explicit branch/decay states.
    """
    # Progressive Lifecycle Ladder
    UNVERIFIED = "UNVERIFIED"
    CANDIDATE = "CANDIDATE"
    SOURCE_VERIFIED = "SOURCE_VERIFIED"
    EVIDENCE_SUPPORTED = "EVIDENCE_SUPPORTED"
    EXPERT_REVIEWED = "EXPERT_REVIEWED"
    AUTHORITATIVE = "AUTHORITATIVE"

    # Branch, Conflict & Decay States
    CONTESTED = "CONTESTED"
    CONFLICTING = "CONFLICTING"
    OUTDATED = "OUTDATED"
    RETRACTED = "RETRACTED"
    SUPERSEDED = "SUPERSEDED"
    REJECTED = "REJECTED"

    # Valid Non-Failure Explicit States
    UNKNOWN = "UNKNOWN"
    NOT_FOUND = "NOT_FOUND"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    SOURCE_INACCESSIBLE = "SOURCE_INACCESSIBLE"


class EpistemicSeparationLevels(BaseModel):
    """
    The Golden Rule:
    SOURCE EXISTS ≠ SOURCE IS AUTHENTIC ≠ CLAIM IS SUPPORTED ≠ CLAIM IS TRUE ≠ CLINICALLY VALID ≠ REGULATORY APPROVED.
    Every dimension is tracked and evaluated independently.
    """
    source_exists: bool = False
    source_is_authentic: bool = False
    claim_is_supported: bool = False
    claim_is_true: bool = False
    claim_is_clinically_valid: bool = False
    claim_is_regulatory_approved: bool = False
    evaluation_notes: List[str] = Field(default_factory=list)


class EvidenceChain(BaseModel):
    """
    Mandatory Evidence Chain:
    CLAIM -> EVIDENCE -> STUDY/DATA -> SOURCE -> EXACT LOCATION -> PROVENANCE -> VERIFICATION STATUS
    If ANY link is incomplete, the system strictly outputs 'Evidence insufficient / verification incomplete'.
    """
    chain_id: str
    claim_id: str
    claim_text: str
    evidence_id: Optional[str] = None
    study_or_dataset_id: Optional[str] = None
    source_id: Optional[str] = None
    exact_location: Optional[str] = None  # e.g., "Page 12, Paragraph 3, Table 2"
    provenance_hash: Optional[str] = None
    verification_state: VerificationState = VerificationState.UNVERIFIED
    is_complete: bool = False
    deficiency_reasons: List[str] = Field(default_factory=list)


class LayerAuditResult(BaseModel):
    """Result of auditing one of the 14 Anti-Fabrication Layers."""
    layer_number: int
    layer_name: str
    status: Literal["PASS", "FAIL", "FLAGGED", "UNKNOWN"]
    details: str
    reasons: List[str] = Field(default_factory=list)
    proof_reference: Optional[str] = None


class CredibilityAuditReport(BaseModel):
    """Comprehensive 14-Layer Anti-Fabrication Audit Report."""
    audit_id: str
    target_object_id: str
    target_object_type: str
    overall_state: VerificationState
    is_authoritative_permitted: bool
    epistemic_levels: EpistemicSeparationLevels
    evidence_chain: EvidenceChain
    layers_audited: List[LayerAuditResult]
    audit_timestamp: datetime = Field(default_factory=datetime.utcnow)
    tamper_evident_hmac: str
