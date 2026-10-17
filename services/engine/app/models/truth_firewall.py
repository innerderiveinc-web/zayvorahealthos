"""
ZMIE Truth, Evidence Integrity, Citation Verification & Safety Firewall Models
Comprehensive schemas for:
- Claim classification, decomposition, and atomicity
- Normalization (subject, predicate, object, population, intervention, outcome, effect, context)
- Citation objects with full document provenance
- ClaimVerification records with multi-dimensional audits
- Truth Firewall verdicts: PASS, MODIFY, BLOCK
- Human reviews and audit event lineage
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class ClaimType(str, Enum):
    FACTUAL = "FACTUAL"
    NUMERICAL = "NUMERICAL"
    STATISTICAL = "STATISTICAL"
    CLINICAL = "CLINICAL"
    SAFETY = "SAFETY"
    PHARMACOLOGICAL = "PHARMACOLOGICAL"
    MECHANISTIC = "MECHANISTIC"
    HISTORICAL = "HISTORICAL"
    TRADITIONAL_MEDICINE = "TRADITIONAL_MEDICINE"
    REGULATORY = "REGULATORY"
    GUIDELINE = "GUIDELINE"
    COMPARATIVE = "COMPARATIVE"
    CAUSAL = "CAUSAL"
    CORRELATIONAL = "CORRELATIONAL"
    TEMPORAL = "TEMPORAL"
    DEFINITIONAL = "DEFINITIONAL"
    INFERENTIAL = "INFERENTIAL"
    HYPOTHESIS = "HYPOTHESIS"
    RECOMMENDATION = "RECOMMENDATION"
    UNKNOWN = "UNKNOWN"


class ClaimStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    UNVERIFIED = "UNVERIFIED"
    CONTRADICTED = "CONTRADICTED"
    CONTEXT_MISMATCH = "CONTEXT_MISMATCH"
    OUTDATED = "OUTDATED"
    RETRACTED = "RETRACTED"
    LICENSE_BLOCKED = "LICENSE_BLOCKED"
    INFERENCE = "INFERENCE"
    HYPOTHESIS = "HYPOTHESIS"
    UNKNOWN = "UNKNOWN"


class SupportLevel(str, Enum):
    DIRECT_SUPPORT = "DIRECT_SUPPORT"
    STRONG_CONTEXTUAL_SUPPORT = "STRONG_CONTEXTUAL_SUPPORT"
    PARTIAL_SUPPORT = "PARTIAL_SUPPORT"
    WEAK_CONTEXTUAL_MATCH = "WEAK_CONTEXTUAL_MATCH"
    DOES_NOT_SUPPORT = "DOES_NOT_SUPPORT"
    UNKNOWN = "UNKNOWN"


class ClaimRiskLevel(str, Enum):
    LOW_RISK = "LOW_RISK"
    MEDIUM_RISK = "MEDIUM_RISK"
    HIGH_RISK = "HIGH_RISK"
    CRITICAL_RISK = "CRITICAL_RISK"


class SourceAuthorityTier(str, Enum):
    TIER_1_GUIDELINE_META = "TIER_1_GUIDELINE_META"          # Guidelines, Systematic Reviews, Meta-Analyses, Regulatory
    TIER_2_HUMAN_RCT = "TIER_2_HUMAN_RCT"                    # RCTs, Prospective Clinical Cohorts
    TIER_3_OBSERVATIONAL = "TIER_3_OBSERVATIONAL"            # Retrospective, Case-Control, Cross-Sectional
    TIER_4_PRECLINICAL = "TIER_4_PRECLINICAL"                # In-vivo animal pharmacology
    TIER_5_IN_VITRO = "TIER_5_IN_VITRO"                      # In-vitro cell assays, enzyme kinetics
    TIER_6_TRADITIONAL_TEXT = "TIER_6_TRADITIONAL_TEXT"      # Canonical codices (Avicenna, Charaka, etc.)
    TIER_7_SECONDARY = "TIER_7_SECONDARY"                    # Secondary commentaries, textbooks


class VeracityState(str, Enum):
    VERIFIED = "VERIFIED"          # 🟢 Directly supported by reliable source
    SUPPORTED = "SUPPORTED"        # 🔵 Multiple credible sources
    LIMITED = "LIMITED"            # 🟡 Limited human evidence
    PRELIMINARY = "PRELIMINARY"    # 🟠 Early / mechanistic evidence
    TRADITIONAL = "TRADITIONAL"    # 🟣 Traditional medical literature
    HYPOTHESIS = "HYPOTHESIS"      # ⚪ Proposed clinical interpretation
    CONTRADICTED = "CONTRADICTED"  # 🔴 Reliable evidence conflicts
    UNKNOWN = "UNKNOWN"            # ⚫ Insufficient evidence


class PatientApplicabilityResult(BaseModel):
    applicability_score: int = Field(..., ge=0, le=100, description="0-100 applicability index")
    applicability_tier: str = Field(..., description="'HIGH', 'MODERATE', 'LOW', 'CONTRAINDICATED'")
    study_demographics: Dict[str, Any] = Field(default_factory=dict)
    patient_context: Dict[str, Any] = Field(default_factory=dict)
    alignment_factors: List[Dict[str, Any]] = Field(default_factory=list)
    extrapolation_warnings: List[str] = Field(default_factory=list)


class FirewallVerdict(str, Enum):
    PASS = "PASS"
    MODIFY = "MODIFY"
    BLOCK = "BLOCK"


class NormalizedClaim(BaseModel):
    subject: str = Field(..., description="Entity or intervention")
    predicate: str = Field(..., description="Action, relationship, or effect verb")
    object: str = Field(..., description="Target outcome, disease, or biological marker")
    population: Optional[str] = Field(None, description="Patient group, species, or demographic")
    intervention: Optional[str] = Field(None, description="Specific dose, formulation, or treatment")
    comparator: Optional[str] = Field(None, description="Control or comparative agent")
    outcome: Optional[str] = Field(None, description="Target endpoint")
    effect: Optional[str] = Field(None, description="Magnitude, percentage, or quantitative effect")
    time: Optional[str] = Field(None, description="Duration or follow-up timeframe")
    context: Optional[str] = Field(None, description="Clinical setting or study design condition")


class Citation(BaseModel):
    citation_id: str = Field(default_factory=lambda: f"cit-{uuid.uuid4().hex[:8]}")
    claim_id: Optional[str] = None
    source_id: str
    document_id: str
    document_version_id: Optional[str] = "v1.0"
    title: str
    authors: List[str] = Field(default_factory=list)
    publication_date: Optional[str] = None
    identifier: str = Field(..., description="DOI, PMID, or canonical accession")
    location: Optional[str] = None
    page: Optional[str] = None
    section: Optional[str] = None
    paragraph: Optional[str] = None
    anchor_hash: Optional[str] = None
    retrieval_timestamp: datetime = Field(default_factory=datetime.utcnow)
    is_retracted: bool = False
    is_corrected: bool = False


class ClaimVerification(BaseModel):
    verification_id: str = Field(default_factory=lambda: f"vrf-{uuid.uuid4().hex[:8]}")
    claim_id: str = Field(default_factory=lambda: f"clm-{uuid.uuid4().hex[:8]}")
    claim_text: str
    normalized_claim: Optional[NormalizedClaim] = None
    claim_type: ClaimType = ClaimType.FACTUAL
    claim_status: ClaimStatus = ClaimStatus.UNVERIFIED
    veracity_state: VeracityState = VeracityState.VERIFIED
    authority_tier: SourceAuthorityTier = SourceAuthorityTier.TIER_2_HUMAN_RCT
    risk_level: ClaimRiskLevel = ClaimRiskLevel.MEDIUM_RISK

    source_ids: List[str] = Field(default_factory=list)
    document_ids: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    citation_ids: List[str] = Field(default_factory=list)

    support_level: SupportLevel = SupportLevel.UNKNOWN
    context_match: bool = True
    temporal_match: bool = True
    source_status: str = "ACTIVE"
    retraction_status: str = "CLEAR"  # CLEAR, RETRACTED, CORRECTED, SUPERSEDED

    contradiction_status: str = "NONE_FOUND"  # NONE_FOUND, DIVERGENCE_DETECTED, CONTRADICTED
    causality_status: str = "VALID"           # VALID, CAUSAL_OVERREACH, INFLATED
    safety_status: str = "PASS"               # PASS, WARNING, CONTRAINDICATED, BLOCKED
    license_status: str = "PERMITTED"         # PERMITTED, RESTRICTED, PROHIBITED

    confidence_scores: Dict[str, float] = Field(
        default_factory=lambda: {
            "citation_confidence": 1.0,
            "semantic_support_confidence": 1.0,
            "context_match_confidence": 1.0,
            "evidence_confidence": 1.0
        }
    )

    verdict: FirewallVerdict = FirewallVerdict.PASS
    recommended_rewrite: Optional[str] = None
    reasons: List[str] = Field(default_factory=list)

    verified_at: datetime = Field(default_factory=datetime.utcnow)
    verifier_version: str = "v1.0.0-truth-firewall"
    knowledge_version: str = "2026.10"


class VerificationReview(BaseModel):
    review_id: str = Field(default_factory=lambda: f"rev-{uuid.uuid4().hex[:8]}")
    claim_id: str
    reviewer: str
    decision: str  # APPROVE, APPROVE_WITH_MODIFICATION, REJECT, REQUEST_MORE_EVIDENCE, ESCALATE
    reason: str
    comment: Optional[str] = None
    evidence_references: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AnswerLineage(BaseModel):
    answer_id: str
    answer_version: int = 1
    knowledge_version: str = "2026.10"
    retrieval_version: str = "v1.0"
    model: str = "zmIE-verified-engine"
    prompt_version: str = "v6.0"
    verification_version: str = "v1.0"
    claim_ids: List[str] = Field(default_factory=list)
    citation_ids: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class VerifiedAnswerPacket(BaseModel):
    answer: str
    original_answer: str
    status: str  # TRUSTED, TRUSTED_WITH_LIMITATIONS, PARTIAL, BLOCKED
    verdict: FirewallVerdict
    claims: List[ClaimVerification] = Field(default_factory=list)
    citations: List[Citation] = Field(default_factory=list)
    contradictions: List[Dict[str, Any]] = Field(default_factory=list)
    safety_alerts: List[Dict[str, Any]] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    verification_metrics: Dict[str, Any] = Field(default_factory=dict)
    lineage: AnswerLineage
