"""
ZMIE Deep Research & Evidence Synthesis Models
Defines complete data models for the Autonomous Medical Research Operating Engine:
PICO structuring, research plans, screening matrices, evidence tables,
contradiction topologies, research gaps, next-best research questions, snapshots, and reports.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from app.models.claim import EvidenceGrade, MedicalSystem
from app.models.source import AuthorityTier


class ResearchJobState(str, Enum):
    DRAFT = "DRAFT"
    QUEUED = "QUEUED"
    PLANNING = "PLANNING"
    SEARCHING = "SEARCHING"
    SCREENING = "SCREENING"
    EXTRACTING = "EXTRACTING"
    ANALYZING = "ANALYZING"
    SYNTHESIZING = "SYNTHESIZING"
    VALIDATING = "VALIDATING"
    COMPLETED = "COMPLETED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"


class AssertionType(str, Enum):
    FACT = "FACT"
    SYNTHESIS = "SYNTHESIS"
    INFERENCE = "INFERENCE"
    HYPOTHESIS = "HYPOTHESIS"
    UNKNOWN = "UNKNOWN"


class ContradictionType(str, Enum):
    DIRECT_OUTCOME = "DIRECT_OUTCOME"
    DOSE_DEPENDENT = "DOSE_DEPENDENT"
    POPULATION_SPECIFIC = "POPULATION_SPECIFIC"
    FORMULATION_EXTRACT = "FORMULATION_EXTRACT"
    TEMPORAL_DURATION = "TEMPORAL_DURATION"
    METHODOLOGICAL_BIAS = "METHODOLOGICAL_BIAS"
    CROSS_SYSTEM_ONTOLOGY = "CROSS_SYSTEM_ONTOLOGY"


class PICOFramework(BaseModel):
    population: str = Field(..., description="Target patient population or biological system")
    intervention: str = Field(..., description="Intervention, formulation, or compound evaluated")
    comparator: Optional[str] = Field(None, description="Active control, placebo, or standard of care")
    outcomes: List[str] = Field(default_factory=list, description="Primary and secondary clinical or biomarker endpoints")
    target_systems: List[MedicalSystem] = Field(
        default=[MedicalSystem.MODERN, MedicalSystem.UNANI, MedicalSystem.AYURVEDA],
        description="Medical systems queried"
    )


class InclusionExclusionCriteria(BaseModel):
    inclusion: List[str] = Field(default_factory=list, description="Rules for including studies")
    exclusion: List[str] = Field(default_factory=list, description="Rules for excluding studies")
    min_evidence_grade: EvidenceGrade = Field(default=EvidenceGrade.CANONICAL_TRADITIONAL)
    allowed_systems: List[str] = Field(default_factory=lambda: ["modern", "unani", "ayurveda"])


class SearchMatrixItem(BaseModel):
    sub_question: str
    target_domains: List[str]
    mesh_terms: List[str]
    traditional_terms: List[str]
    retrieval_strategy: str = "HYBRID_SEMANTIC_LEXICAL"


class ResearchPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"plan-{uuid.uuid4().hex[:8]}")
    title: str
    primary_question: str
    sub_questions: List[str] = Field(default_factory=list)
    pico: PICOFramework
    criteria: InclusionExclusionCriteria
    search_matrix: List[SearchMatrixItem] = Field(default_factory=list)
    budget_limit_sources: int = 100
    plan_version: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ScreeningDecision(BaseModel):
    source_id: str
    title: str
    verdict: str  # INCLUDED, EXCLUDED, QUARANTINED
    exclusion_reason: Optional[str] = None
    applied_rule: Optional[str] = None
    confidence: float = 1.0


class EvidenceTableEntry(BaseModel):
    evidence_id: str
    source_id: str
    study_title: str
    study_design: str
    evidence_grade: str
    population: str
    intervention: str
    comparator: Optional[str] = None
    duration: Optional[str] = None
    sample_size: Optional[int] = None
    primary_findings: str
    effect_size_or_stats: Optional[str] = None
    safety_adverse_events: Optional[str] = None
    risk_of_bias: str = "LOW"
    source_authority: str = "TIER_B"
    medical_system: str = "MODERN"
    doi_or_anchor: Optional[str] = None


class ContradictionCluster(BaseModel):
    cluster_id: str
    topic: str
    contradiction_type: ContradictionType
    divergence_summary: str
    position_a: Dict[str, Any]  # evidence_ids, summary, population, grade
    position_b: Dict[str, Any]  # evidence_ids, summary, population, grade
    probable_root_cause: str
    resolution_pathway: Optional[str] = None


class ResearchGapRecord(BaseModel):
    gap_id: str
    category: str  # TRIAL_PHASE, POPULATION, PHARMACOKINETIC, FORMULATION, DURATION, CROSS_SYSTEM
    description: str
    clinical_significance: str
    evidence_deficiency: str
    priority: str = "HIGH"  # CRITICAL, HIGH, MEDIUM, LOW


class NextBestResearchQuestion(BaseModel):
    question_id: str
    question_text: str
    rationale: str
    target_gap_id: str
    proposed_methodology: str
    anticipated_impact: str


class GroundedAssertion(BaseModel):
    assertion_id: str
    statement: str
    assertion_type: AssertionType
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    supporting_citations: List[str] = Field(default_factory=list)
    confidence_score: float = 1.0
    epistemic_status: str = "CONFIRMED"  # CONFIRMED, PROVISIONAL, CONFLICTED, UNVERIFIED


class ResearchReport(BaseModel):
    report_id: str = Field(default_factory=lambda: f"rep-{uuid.uuid4().hex[:8]}")
    job_id: str
    title: str
    executive_summary: str
    primary_question: str
    plan_summary: Dict[str, Any]
    flow_metrics: Dict[str, int] = Field(
        default_factory=lambda: {
            "discovered": 0,
            "screened": 0,
            "included": 0,
            "excluded": 0,
            "evidence_items": 0,
        }
    )
    pico_matrix: PICOFramework
    evidence_table: List[EvidenceTableEntry] = Field(default_factory=list)
    contradictions: List[ContradictionCluster] = Field(default_factory=list)
    safety_findings: Dict[str, Any] = Field(default_factory=dict)
    research_gaps: List[ResearchGapRecord] = Field(default_factory=list)
    next_best_questions: List[NextBestResearchQuestion] = Field(default_factory=list)
    assertions: List[GroundedAssertion] = Field(default_factory=list)
    citation_audit: List[Dict[str, Any]] = Field(default_factory=list)
    reflection_audit: List[Dict[str, Any]] = Field(default_factory=list)
    react_tools_invoked: List[str] = Field(default_factory=list)
    auto_repaired_count: int = 0
    adversarial_debate: Optional[Dict[str, Any]] = None
    narrative_synthesis: str = ""
    reproducibility_hash: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ResearchSnapshot(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: f"snap-{uuid.uuid4().hex[:8]}")
    job_id: str
    snapshot_version: int
    state: ResearchJobState
    plan: Optional[ResearchPlan] = None
    report: Optional[ResearchReport] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ResearchDiff(BaseModel):
    job_id: str
    base_snapshot_id: str
    target_snapshot_id: str
    added_evidence_count: int
    removed_evidence_count: int
    new_contradictions: List[str] = Field(default_factory=list)
    resolved_contradictions: List[str] = Field(default_factory=list)
    new_gaps: List[str] = Field(default_factory=list)
    diff_summary: str


class ResearchJob(BaseModel):
    job_id: str = Field(default_factory=lambda: f"job-{uuid.uuid4().hex[:8]}")
    title: str
    question: str
    target_systems: List[str] = Field(default_factory=lambda: ["modern", "unani", "ayurveda"])
    state: ResearchJobState = ResearchJobState.DRAFT
    plan: Optional[ResearchPlan] = None
    screening_log: List[ScreeningDecision] = Field(default_factory=list)
    evidence_table: List[EvidenceTableEntry] = Field(default_factory=list)
    contradictions: List[ContradictionCluster] = Field(default_factory=list)
    gaps: List[ResearchGapRecord] = Field(default_factory=list)
    next_questions: List[NextBestResearchQuestion] = Field(default_factory=list)
    report: Optional[ResearchReport] = None
    snapshots: List[ResearchSnapshot] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
