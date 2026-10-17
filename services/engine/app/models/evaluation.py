"""
ZMIE Evaluation, Benchmarking & Scientific Validation Lab Models
Defines contracts for:
- Benchmarks, Benchmark Versions, Datasets, and Test Cases
- Evaluator Runs, Case Results, and State Machine
- Metric Registries and Multidimensional Scorecards
- Standardized Error Taxonomy & Root-Cause Analysis
- Scientific Experiments, Ablations, and System Comparisons
- Reviewer Panels, Double-Review & Adjudication
- Production Release Quality Gates (Go / Go with Limitations / No-Go)
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class EvaluationState(str, Enum):
    PASS = "PASS"
    PASS_WITH_LIMITATIONS = "PASS_WITH_LIMITATIONS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"
    NOT_TESTED = "NOT_TESTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class ReleaseGateVerdict(str, Enum):
    GO = "GO"
    GO_WITH_LIMITATIONS = "GO_WITH_LIMITATIONS"
    NO_GO = "NO_GO"


class BenchmarkDomain(str, Enum):
    GENERAL_MEDICAL = "GENERAL_MEDICAL"
    MEDICAL_SEARCH = "MEDICAL_SEARCH"
    EVIDENCE_RETRIEVAL = "EVIDENCE_RETRIEVAL"
    CITATION = "CITATION"
    CLAIM_VERIFICATION = "CLAIM_VERIFICATION"
    DEEP_RESEARCH = "DEEP_RESEARCH"
    SAFETY = "SAFETY"
    PHARMACOLOGY = "PHARMACOLOGY"
    CLINICAL_TRIALS = "CLINICAL_TRIALS"
    GUIDELINES = "GUIDELINES"
    KNOWLEDGE_GRAPH = "KNOWLEDGE_GRAPH"
    ONTOLOGY = "ONTOLOGY"
    UNANI = "UNANI"
    AYURVEDA = "AYURVEDA"
    TCM = "TCM"
    CROSS_SYSTEM = "CROSS_SYSTEM"
    HISTORICAL_MEDICINE = "HISTORICAL_MEDICINE"
    MULTILINGUAL = "MULTILINGUAL"
    RESEARCH_GAPS = "RESEARCH_GAPS"
    SCIENTIFIC_INTEGRITY = "SCIENTIFIC_INTEGRITY"
    SECURITY = "SECURITY"
    PRIVACY = "PRIVACY"
    RELIABILITY = "RELIABILITY"


class ErrorTaxonomy(str, Enum):
    RETRIEVAL_MISS = "RETRIEVAL_MISS"
    WRONG_ENTITY = "WRONG_ENTITY"
    WRONG_RELATION = "WRONG_RELATION"
    WRONG_EVIDENCE = "WRONG_EVIDENCE"
    WRONG_SOURCE = "WRONG_SOURCE"
    CITATION_ERROR = "CITATION_ERROR"
    CITATION_INCOMPLETE = "CITATION_INCOMPLETE"
    CONTEXT_LOSS = "CONTEXT_LOSS"
    CAUSAL_OVERREACH = "CAUSAL_OVERREACH"
    EVIDENCE_INFLATION = "EVIDENCE_INFLATION"
    FALSE_EQUIVALENCE = "FALSE_EQUIVALENCE"
    RETRACTION_MISS = "RETRACTION_MISS"
    SAFETY_MISS = "SAFETY_MISS"
    SAFETY_HALLUCINATION = "SAFETY_HALLUCINATION"
    NUMERICAL_ERROR = "NUMERICAL_ERROR"
    TEMPORAL_ERROR = "TEMPORAL_ERROR"
    JURISDICTION_ERROR = "JURISDICTION_ERROR"
    HALLUCINATION = "HALLUCINATION"
    UNSUPPORTED_CLAIM = "UNSUPPORTED_CLAIM"


class BenchmarkCase(BaseModel):
    case_id: str = Field(default_factory=lambda: f"case-{uuid.uuid4().hex[:8]}")
    domain: BenchmarkDomain
    question_or_prompt: str
    expected_entities: List[str] = Field(default_factory=list)
    expected_claims: List[str] = Field(default_factory=list)
    expected_evidence_levels: List[str] = Field(default_factory=list)
    expected_citation_ids: List[str] = Field(default_factory=list)
    expected_safety_warnings: List[str] = Field(default_factory=list)
    expected_uncertainty: bool = False
    adversarial_type: Optional[str] = None  # false_premise, ambiguity, hallucination_trap, retraction
    difficulty: str = "MEDIUM"


class BenchmarkDataset(BaseModel):
    dataset_id: str = Field(default_factory=lambda: f"ds-{uuid.uuid4().hex[:8]}")
    name: str
    version: str = "v1.0"
    domain: BenchmarkDomain
    dataset_type: str = "REAL"  # REAL, SYNTHETIC, DE_IDENTIFIED, MIXED
    cases: List[BenchmarkCase] = Field(default_factory=list)
    immutable: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Benchmark(BaseModel):
    benchmark_id: str = Field(default_factory=lambda: f"bmk-{uuid.uuid4().hex[:8]}")
    name: str
    description: str
    domain: BenchmarkDomain
    task_type: str  # retrieval, verification, synthesis, safety, cross_system
    version: str = "v1.0"
    owner: str = "ZMIE Scientific Validation Board"
    dataset_ids: List[str] = Field(default_factory=list)
    status: str = "PRODUCTION"  # DRAFT, INTERNAL, VALIDATED, PRODUCTION, PRIVATE_HOLDOUT
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MetricDefinition(BaseModel):
    metric_id: str
    name: str
    definition: str
    formula: str
    domain: str
    higher_is_better: bool = True
    unit: str = "ratio"


class CaseEvaluationResult(BaseModel):
    case_id: str
    status: EvaluationState
    system_output: str
    metrics: Dict[str, float] = Field(default_factory=dict)
    errors_detected: List[ErrorTaxonomy] = Field(default_factory=list)
    root_cause_stage: Optional[str] = None  # retrieval, ontology, graph, source, extraction, reasoning, verification
    root_cause_description: Optional[str] = None
    first_failure_detail: Optional[str] = None


class EvaluationRun(BaseModel):
    run_id: str = Field(default_factory=lambda: f"run-{uuid.uuid4().hex[:8]}")
    benchmark_id: str
    benchmark_version: str
    system_version: str = "ZMIE-1.0.0"
    model_version: str = "claude-3-5-sonnet"
    knowledge_version: str = "2026.10"
    ontology_version: str = "v1.0"
    graph_version: str = "v1.0"
    retrieval_version: str = "v1.0"
    prompt_version: str = "v6.0"
    environment: str = "validation_lab"
    status: str = "COMPLETED"  # QUEUED, RUNNING, PARTIAL, COMPLETED, FAILED
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    case_results: List[CaseEvaluationResult] = Field(default_factory=list)
    aggregated_metrics: Dict[str, float] = Field(default_factory=dict)
    dimension_scores: Dict[str, EvaluationState] = Field(default_factory=dict)
    limitations: List[str] = Field(default_factory=list)


class Experiment(BaseModel):
    experiment_id: str = Field(default_factory=lambda: f"exp-{uuid.uuid4().hex[:8]}")
    name: str
    hypothesis: str
    objective: str
    dataset_id: str
    primary_metric: str
    secondary_metrics: List[str] = Field(default_factory=list)
    system_configurations: List[Dict[str, Any]] = Field(default_factory=list)
    status: str = "REGISTERED"  # REGISTERED, RUNNING, COMPLETED
    pre_registered: bool = True
    results: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ReleaseScorecard(BaseModel):
    verdict: ReleaseGateVerdict
    system_version: str
    knowledge_version: str
    evaluation_date: datetime = Field(default_factory=datetime.utcnow)
    dimension_statuses: Dict[str, EvaluationState] = Field(default_factory=dict)
    blockers: List[str] = Field(default_factory=list)
    limitations: List[Dict[str, str]] = Field(default_factory=list)  # {scope, impact, workaround, owner}
    rationale: str
