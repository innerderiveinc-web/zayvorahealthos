"""ZMIE Scientific Data Fabric & Computational Research Engine Models.

Defines schemas for:
- Explicit Scientific States (OBSERVED, COMPUTED, DERIVED, MODELED, SIMULATED, etc.)
- Data Fabric Objects (Dataset, DatasetVersion, DatasetSnapshot, DataField, DataQualityReport)
- Data Lineage & Provenance
- Analysis Plans & Preregistration
- Computational Workflows, Runtime Environments, and Execution Runs
- Statistical Estimates (Hazard Ratio, Risk Ratio, CI, P-value, Estimands)
- Computational Certificates & Reproducibility Verification
- Computation Diffing (Run A vs Run B)
- Candidate Claims & Evidence Promotion Gating
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class ScientificState(str, Enum):
    """Rigorous scientific boundaries preventing computed results from masquerading as raw observation."""
    OBSERVED = "OBSERVED"
    MEASURED = "MEASURED"
    REPORTED = "REPORTED"
    DERIVED = "DERIVED"
    COMPUTED = "COMPUTED"
    MODELED = "MODELED"
    SIMULATED = "SIMULATED"
    PREDICTED = "PREDICTED"
    INFERRED = "INFERRED"
    HYPOTHESIZED = "HYPOTHESIZED"
    VALIDATED = "VALIDATED"


class PrivacyClassification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    SENSITIVE = "SENSITIVE"
    PHI = "PHI"
    PII = "PII"
    HIGHLY_RESTRICTED = "HIGHLY_RESTRICTED"


class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    AUTHORIZED = "AUTHORIZED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"


# -------------------------------------------------------------
# Data Fabric Models
# -------------------------------------------------------------

class DataField(BaseModel):
    """Schema definition for an individual scientific variable."""
    field_name: str
    data_type: str  # numeric, categorical, datetime, string
    semantic_type: str  # e.g. Exposure, Outcome, Confounder, Biomarker
    unit: Optional[str] = None
    normalized_unit: Optional[str] = None
    ontology_concept_id: Optional[str] = None  # Bound to Prompt 20 concept
    missing_count: int = 0
    missing_pct: float = 0.0


class DataQualityReport(BaseModel):
    """Multi-dimensional assessment of dataset integrity."""
    report_id: str
    dataset_id: str
    total_records: int
    completeness_score: float = Field(..., ge=0.0, le=1.0)
    duplicate_records_count: int = 0
    missingness_mechanisms: Dict[str, str] = Field(default_factory=dict)  # e.g. {"biomarker_x": "MAR"}
    unit_consistency_valid: bool = True
    range_check_anomalies: List[str] = Field(default_factory=list)
    fitness_for_purpose: str = "HIGH"  # HIGH, MODERATE, LOW, UNUSABLE
    generated_at: str


class Dataset(BaseModel):
    """First-class dataset asset in the scientific data fabric."""
    dataset_id: str
    name: str
    description: str
    publisher_or_institution: str
    domain: str  # Clinical, Trial, Pharmacological, RWE, Omics
    privacy_class: PrivacyClassification = PrivacyClassification.INTERNAL
    license_type: str = "OPEN_RESEARCH"
    fields: List[DataField] = Field(default_factory=list)
    records_count: int = 0
    current_version: str = "v1.0"
    is_synthetic: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: str
    updated_at: str


class DatasetSnapshot(BaseModel):
    """Immutable, pinned dataset state for scientific reproducibility."""
    snapshot_id: str
    dataset_id: str
    version_tag: str
    records_count: int
    content_sha256: str
    fields_schema_hash: str
    pinned_at: str


# -------------------------------------------------------------
# Analysis Planning & Computation Models
# -------------------------------------------------------------

class RuntimeEnvironment(BaseModel):
    """Preserved runtime environment for deterministic execution."""
    container_image: str = "zmie-scientific-runtime:v2.4-py3.9"
    os_kernel: str = "Linux x86_64"
    python_version: str = "3.9.6"
    dependencies: Dict[str, str] = Field(default_factory=dict)  # {"numpy": "1.26.4", "scipy": "1.13.0"}
    random_seed: int = 42
    environment_sha256: str = "sha256:8f4c28b7e21a"


class AnalysisPlan(BaseModel):
    """Preregistered scientific computational protocol."""
    plan_id: str
    research_question: str
    hypothesis_id: Optional[str] = None
    study_design: str  # RCT, Cohort, Case-Control, Target Trial Emulation
    target_population: str
    exposure_variable: str
    comparator_variable: str
    outcome_variable: str
    covariates: List[str] = Field(default_factory=list)
    statistical_method: str  # Cox Proportional Hazards, Logistic Regression, Meta-Analysis
    data_leakage_checks_passed: bool = True
    preregistration_status: str = "REGISTERED"
    created_at: str


class EffectEstimate(BaseModel):
    """Structured statistical estimate produced by computation."""
    estimate_id: str
    measure_type: str  # HAZARD_RATIO, RISK_RATIO, ODDS_RATIO, MEAN_DIFFERENCE
    point_estimate: float
    confidence_interval_95: List[float]  # [lower, upper]
    p_value: float
    standard_error: float
    sample_size: int
    events_count: Optional[int] = None
    scientific_state: ScientificState = ScientificState.COMPUTED
    estimand_definition: str
    adjustment_set: List[str] = Field(default_factory=list)


class ResultArtifact(BaseModel):
    """Output artifact generated by a computational run."""
    artifact_id: str
    run_id: str
    artifact_type: str  # STATISTICAL_ESTIMATE, SURVIVAL_CURVE, FOREST_PLOT, TABLE
    scientific_state: ScientificState = ScientificState.COMPUTED
    effect_estimate: Optional[EffectEstimate] = None
    output_summary: Dict[str, Any] = Field(default_factory=dict)
    checksum: str
    created_at: str


class ComputationJob(BaseModel):
    """Trackable computational execution job."""
    job_id: str
    plan_id: str
    dataset_snapshot_id: str
    status: JobStatus = JobStatus.QUEUED
    runtime_environment: RuntimeEnvironment
    code_hash: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    results: List[ResultArtifact] = Field(default_factory=list)
    execution_logs: List[str] = Field(default_factory=list)
    reproduced_from_run_id: Optional[str] = None


class ComputationalCertificate(BaseModel):
    """Cryptographic attestation certifying reproducible computation."""
    certificate_id: str
    run_id: str
    dataset_snapshot_hash: str
    code_hash: str
    runtime_hash: str
    seed: int
    reproducibility_verdict: str  # FULLY_REPRODUCIBLE, NUMERICALLY_CONCORDANT
    relative_divergence: float = 0.0
    certified_at: str


class ComputationDiff(BaseModel):
    """Quantified difference between two computational runs."""
    diff_id: str
    run_a_id: str
    run_b_id: str
    dataset_version_changed: bool
    code_changed: bool
    parameters_changed: bool
    effect_estimate_delta: float
    p_value_delta: float
    conclusion_concordance: bool
    narrative_summary: str


# -------------------------------------------------------------
# Data Lineage & Evidence Promotion
# -------------------------------------------------------------

class LineageNode(BaseModel):
    node_id: str
    label: str
    node_type: str  # RAW_DATASET, NORMALIZED_DATASET, SNAPSHOT, WORKFLOW, RUN, ESTIMATE, EVIDENCE, CLAIM
    scientific_state: ScientificState


class LineageEdge(BaseModel):
    source_id: str
    target_id: str
    transformation: str


class DataLineageGraph(BaseModel):
    graph_id: str
    nodes: List[LineageNode]
    edges: List[LineageEdge]
    root_source: str
    terminal_claim: Optional[str] = None


class CandidateClaim(BaseModel):
    """Gated scientific claim awaiting human governance before knowledge release."""
    claim_id: str
    statement: str
    source_artifact_id: str
    effect_estimate: EffectEstimate
    scientific_state: ScientificState = ScientificState.DERIVED
    human_review_status: str = "PENDING_REVIEW"  # PENDING_REVIEW, APPROVED, REJECTED
    reviewed_by: Optional[str] = None
    promoted_to_evidence_graph: bool = False
    created_at: str
