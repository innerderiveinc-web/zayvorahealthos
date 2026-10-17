"""
ZMIE Living Evidence Synthesis & Evidence Update Engine Models
Models for continuous surveillance, structured research questions (PICO/PECO),
study families, dual-screening, risk of bias, meta-analysis, GRADE certainty,
update triggers, versioned snapshots, and PRISMA-compliant flow.
"""

from typing import List, Dict, Any, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field


class ReviewType(str, Enum):
    SYSTEMATIC_REVIEW = "SYSTEMATIC_REVIEW"
    LIVING_SYSTEMATIC_REVIEW = "LIVING_SYSTEMATIC_REVIEW"
    RAPID_REVIEW = "RAPID_REVIEW"
    SCOPING_REVIEW = "SCOPING_REVIEW"
    UMBRELLA_REVIEW = "UMBRELLA_REVIEW"
    META_ANALYSIS = "META_ANALYSIS"
    NETWORK_META_ANALYSIS = "NETWORK_META_ANALYSIS"
    QUALITATIVE_SYNTHESIS = "QUALITATIVE_SYNTHESIS"
    PROGNOSIS_REVIEW = "PROGNOSIS_REVIEW"
    DIAGNOSTIC_ACCURACY_REVIEW = "DIAGNOSTIC_ACCURACY_REVIEW"
    PREVALENCE_REVIEW = "PREVALENCE_REVIEW"
    ETIOLOGY_REVIEW = "ETIOLOGY_REVIEW"
    SAFETY_REVIEW = "SAFETY_REVIEW"
    EVIDENCE_MAP = "EVIDENCE_MAP"
    REAL_WORLD_EVIDENCE_SYNTHESIS = "REAL_WORLD_EVIDENCE_SYNTHESIS"
    MIXED_METHODS_SYNTHESIS = "MIXED_METHODS_SYNTHESIS"


class ReviewStatus(str, Enum):
    DRAFT = "DRAFT"
    PROTOCOL_READY = "PROTOCOL_READY"
    BASELINE_COMPLETE = "BASELINE_COMPLETE"
    LIVING_ACTIVE = "LIVING_ACTIVE"
    UPDATE_IN_PROGRESS = "UPDATE_IN_PROGRESS"
    UPDATE_COMPLETE = "UPDATE_COMPLETE"
    TEMPORARILY_PAUSED = "TEMPORARILY_PAUSED"
    STALE = "STALE"
    COMPLETED = "COMPLETED"
    RETIRED = "RETIRED"
    SUPERSEDED = "SUPERSEDED"


class EvidenceImpactClass(str, Enum):
    NO_IMPACT = "NO_IMPACT"
    LOW_IMPACT = "LOW_IMPACT"
    MODERATE_IMPACT = "MODERATE_IMPACT"
    HIGH_IMPACT = "HIGH_IMPACT"
    CRITICAL_IMPACT = "CRITICAL_IMPACT"


class UpdateTriggerType(str, Enum):
    NEW_RCT = "NEW_RCT"
    NEW_RWE = "NEW_RWE"
    NEW_META_ANALYSIS = "NEW_META_ANALYSIS"
    NEW_GUIDELINE = "NEW_GUIDELINE"
    NEW_SAFETY_SIGNAL = "NEW_SAFETY_SIGNAL"
    RETRACTION = "RETRACTION"
    CORRECTION = "CORRECTION"
    MAJOR_CONTRADICTION = "MAJOR_CONTRADICTION"
    NEW_HIGH_QUALITY_STUDY = "NEW_HIGH_QUALITY_STUDY"
    NEW_TRIAL_RESULT = "NEW_TRIAL_RESULT"


class ScreeningStage(str, Enum):
    NEW = "NEW"
    DUPLICATE_CHECK = "DUPLICATE_CHECK"
    TITLE_ABSTRACT_SCREEN = "TITLE_ABSTRACT_SCREEN"
    FULL_TEXT_SCREEN = "FULL_TEXT_SCREEN"
    INCLUDED = "INCLUDED"
    EXCLUDED = "EXCLUDED"
    UNCERTAIN = "UNCERTAIN"


class ExclusionReason(str, Enum):
    WRONG_POPULATION = "WRONG_POPULATION"
    WRONG_INTERVENTION = "WRONG_INTERVENTION"
    WRONG_COMPARATOR = "WRONG_COMPARATOR"
    WRONG_OUTCOME = "WRONG_OUTCOME"
    WRONG_STUDY_DESIGN = "WRONG_STUDY_DESIGN"
    WRONG_TIMEFRAME = "WRONG_TIMEFRAME"
    DUPLICATE = "DUPLICATE"
    PROTOCOL_ONLY = "PROTOCOL_ONLY"
    NOT_RESEARCH = "NOT_RESEARCH"
    INSUFFICIENT_INFORMATION = "INSUFFICIENT_INFORMATION"
    OUTSIDE_SCOPE = "OUTSIDE_SCOPE"


class RiskOfBiasJudgment(str, Enum):
    LOW_RISK = "LOW_RISK"
    SOME_CONCERNS = "SOME_CONCERNS"
    HIGH_RISK = "HIGH_RISK"
    UNASSESSED = "UNASSESSED"


class CertaintyRating(str, Enum):
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    VERY_LOW = "VERY_LOW"


class ConclusionChangeClass(str, Enum):
    NO_CONCLUSION_CHANGE = "NO_CONCLUSION_CHANGE"
    MINOR_CHANGE = "MINOR_CHANGE"
    MODERATE_CHANGE = "MODERATE_CHANGE"
    MAJOR_CHANGE = "MAJOR_CHANGE"
    CONCLUSION_REVERSED = "CONCLUSION_REVERSED"


# -------------------------------------------------------------
# Structured Research Question (PICO / PECO / Frameworks)
# -------------------------------------------------------------

class StructuredResearchQuestion(BaseModel):
    question_id: str
    version: str = "RQ-v1"
    title: str
    narrative_question: str
    framework: str = "PICO"  # PICO, PECO, PICOT, SPIDER
    population: str
    intervention_or_exposure: str
    comparator: Optional[str] = None
    outcomes: List[str] = Field(default_factory=list)
    time_horizon: Optional[str] = None
    medical_systems: List[str] = Field(default_factory=lambda: ["ALLOPATHIC_CONVENTIONAL"])
    jurisdiction: Optional[str] = None


class EligibilityCriteria(BaseModel):
    eligibility_version: str = "ELIG-v1"
    effective_date: str
    inclusion_criteria: List[str] = Field(default_factory=list)
    exclusion_criteria: List[str] = Field(default_factory=list)
    study_designs_eligible: List[str] = Field(default_factory=list)
    languages_allowed: List[str] = Field(default_factory=lambda: ["en"])
    publication_date_min: Optional[str] = None
    publication_status_allowed: List[str] = Field(default_factory=lambda: ["PEER_REVIEWED", "PREPRINT"])
    changed_by: Optional[str] = None
    change_reason: Optional[str] = None


# -------------------------------------------------------------
# Search Strategy & Surveillance Plan
# -------------------------------------------------------------

class SearchStrategyRecord(BaseModel):
    strategy_id: str
    version: str = "SearchStrategy-v1"
    databases_covered: List[str] = Field(default_factory=list)  # PubMed, Embase, Cochrane, Europe PMC, AYUSH, etc.
    exact_query_string: str
    mesh_terms_and_keywords: List[str] = Field(default_factory=list)
    filters_applied: Dict[str, Any] = Field(default_factory=dict)
    date_window: str


class SurveillancePlan(BaseModel):
    plan_id: str
    frequency_days: int = 7  # e.g., weekly surveillance
    screening_cadence_days: int = 3
    urgent_trigger_threshold: EvidenceImpactClass = EvidenceImpactClass.HIGH_IMPACT
    target_sources: List[str] = Field(default_factory=list)
    active: bool = True
    responsible_lead: str = "ZMIE Evidence Surveillance Worker"


# -------------------------------------------------------------
# Studies, Study Families & Reports
# -------------------------------------------------------------

class StudyReport(BaseModel):
    report_id: str
    report_type: str  # REGISTRY, PROTOCOL, PREPRINT, PRIMARY_ARTICLE, SECONDARY_ANALYSIS, FOLLOW_UP
    title: str
    doi_or_id: str
    publication_year: int
    source_database: str
    is_retracted: bool = False
    is_corrected: bool = False
    retraction_notice_url: Optional[str] = None


class StudyFamily(BaseModel):
    family_id: str
    canonical_study_name: str  # e.g. "DAPA-HF Trial"
    trial_registration_id: Optional[str] = None  # e.g. NCT03036124
    reports: List[StudyReport] = Field(default_factory=list)
    is_active: bool = True


# -------------------------------------------------------------
# Screening Records
# -------------------------------------------------------------

class ScreeningDecision(BaseModel):
    decision_id: str
    study_id: str
    stage: ScreeningStage
    decision: str  # INCLUDE, EXCLUDE, UNCERTAIN
    exclusion_reason: Optional[ExclusionReason] = None
    reviewer_id: str
    is_ai_assisted: bool = False
    ai_confidence: Optional[float] = None
    ai_rationale: Optional[str] = None
    adjudicated: bool = False
    adjudicator_id: Optional[str] = None
    timestamp: str


# -------------------------------------------------------------
# Data Extraction & Risk of Bias
# -------------------------------------------------------------

class ExtractedEffectEstimate(BaseModel):
    outcome_name: str
    effect_measure: str  # RISK_RATIO, ODDS_RATIO, HAZARD_RATIO, MEAN_DIFFERENCE, SMD
    point_estimate: float
    ci_lower: float
    ci_upper: float
    p_value: Optional[float] = None
    events_intervention: Optional[int] = None
    total_intervention: Optional[int] = None
    events_comparator: Optional[int] = None
    total_comparator: Optional[int] = None
    is_figure_derived: bool = False
    digitization_provenance: Optional[str] = None


class StudyExtractionRecord(BaseModel):
    extraction_id: str
    study_id: str
    study_design: str
    sample_size: int
    population_description: str
    intervention_details: Dict[str, Any]
    comparator_details: Dict[str, Any]
    effects: List[ExtractedEffectEstimate] = Field(default_factory=list)
    adverse_events_reported: List[str] = Field(default_factory=list)
    extracted_by: str
    verified_by: Optional[str] = None
    extraction_date: str


class RiskOfBiasAssessment(BaseModel):
    assessment_id: str
    study_id: str
    tool_used: str  # RoB 2, ROBINS-I, QUADAS-2
    domain_judgments: Dict[str, RiskOfBiasJudgment] = Field(default_factory=dict)
    overall_risk: RiskOfBiasJudgment
    assessor_id: str
    rationale: str


# -------------------------------------------------------------
# Synthesis, Meta-Analysis & GRADE Certainty
# -------------------------------------------------------------

class MetaAnalysisResult(BaseModel):
    meta_id: str
    version: str = "MetaAnalysis-v1"
    outcome_name: str
    model_type: str = "RANDOM_EFFECTS"  # FIXED_EFFECT or RANDOM_EFFECTS (DerSimonian-Laird)
    effect_measure: str = "RISK_RATIO"
    pooled_estimate: float
    ci_lower: float
    ci_upper: float
    p_value: float
    i_squared_pct: float  # Heterogeneity (0 - 100%)
    tau_squared: float
    q_statistic: float
    studies_included_count: int
    forest_plot_data: List[Dict[str, Any]] = Field(default_factory=list)  # [{"study": "Study A", "effect": 0.82, "weight_pct": 25.0}]


class GRADECertaintyAssessment(BaseModel):
    assessment_id: str
    version: str = "Certainty-v1"
    outcome_name: str
    risk_of_bias_downgrade: int = 0  # 0, -1, -2
    inconsistency_downgrade: int = 0
    indirectness_downgrade: int = 0
    imprecision_downgrade: int = 0
    publication_bias_downgrade: int = 0
    upgrades_large_effect: int = 0
    final_certainty: CertaintyRating
    rationales: Dict[str, str] = Field(default_factory=dict)


# -------------------------------------------------------------
# PRISMA Screening Flow Counts
# -------------------------------------------------------------

class PRISMAFlowCounts(BaseModel):
    records_identified: int = 0
    duplicates_removed: int = 0
    records_screened_title_abstract: int = 0
    records_excluded_title_abstract: int = 0
    full_text_assessed: int = 0
    full_text_excluded: int = 0
    studies_included_qualitative: int = 0
    studies_included_quantitative_meta: int = 0


# -------------------------------------------------------------
# Update Triggers & Living Review Object
# -------------------------------------------------------------

class UpdateTriggerEvent(BaseModel):
    trigger_id: str
    trigger_type: UpdateTriggerType
    impact_class: EvidenceImpactClass
    source_reference: str
    description: str
    detected_at: str
    action_decision: str  # SCREEN, ASSESS, RECALCULATE, UPDATE_REVIEW, URGENT_UPDATE, NO_ACTION
    decision_rationale: str
    resolved: bool = False


class LivingReviewVersion(BaseModel):
    version_tag: str  # "v1.0", "v2.0"
    publication_date: str
    status: ReviewStatus
    included_studies_count: int
    meta_analyses: List[MetaAnalysisResult] = Field(default_factory=list)
    certainty_assessments: List[GRADECertaintyAssessment] = Field(default_factory=list)
    synthesis_narrative: str
    what_changed_summary: Optional[str] = None
    conclusion_change: ConclusionChangeClass = ConclusionChangeClass.NO_CONCLUSION_CHANGE
    prisma_flow: PRISMAFlowCounts
    approver: Optional[str] = None


class LivingEvidenceSynthesis(BaseModel):
    review_id: str
    current_version_tag: str = "v1.0"
    review_type: ReviewType = ReviewType.LIVING_SYSTEMATIC_REVIEW
    current_status: ReviewStatus = ReviewStatus.LIVING_ACTIVE
    research_question: StructuredResearchQuestion
    eligibility_criteria: EligibilityCriteria
    surveillance_plan: SurveillancePlan
    search_strategy: SearchStrategyRecord
    study_families: List[StudyFamily] = Field(default_factory=list)
    screening_queue: List[ScreeningDecision] = Field(default_factory=list)
    extractions: List[StudyExtractionRecord] = Field(default_factory=list)
    risk_of_bias_records: List[RiskOfBiasAssessment] = Field(default_factory=list)
    active_triggers: List[UpdateTriggerEvent] = Field(default_factory=list)
    versions: List[LivingReviewVersion] = Field(default_factory=list)
    currency_date: str
    pending_evidence_count: int = 0
    staleness_warning: bool = False
    source_coverage_limitations: List[str] = Field(default_factory=list)
    epistemic_disclaimer: str = (
        "Living evidence synthesis provides current summarized scientific data under prespecified protocols. "
        "It does not constitute autonomous clinical prescriptive recommendations."
    )
