"""
ZMIE Scientific Benchmarking & Validation Models
PROMPT 33 Architecture Implementation
Multi-Domain Golden Batteries & Go/No-Go Decision Matrix
"""

from __future__ import annotations
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field
from datetime import datetime


class ValidationDimension(str, Enum):
    """The 24 Comprehensive Scientific Validation Dimensions (Prompt 33, Clauses 1-5)."""
    SOURCE_AUTHENTICITY = "SOURCE_AUTHENTICITY"
    CITATION_ACCURACY_ATTRIBUTION = "CITATION_ACCURACY_ATTRIBUTION"
    EVIDENCE_GROUNDING_FAITHFULNESS = "EVIDENCE_GROUNDING_FAITHFULNESS"
    CLAIM_ENTAILMENT_NLI = "CLAIM_ENTAILMENT_NLI"
    CAUSAL_MECHANISTIC_SOUNDNESS = "CAUSAL_MECHANISTIC_SOUNDNESS"
    SCIENTIFIC_NUMERICAL_CALCULATION = "SCIENTIFIC_NUMERICAL_CALCULATION"
    UNCERTAINTY_TRANSPARENCY = "UNCERTAINTY_TRANSPARENCY"
    CONTRADICTION_DETECTION = "CONTRADICTION_DETECTION"
    RETRACTION_OUTDATED_SENSITIVITY = "RETRACTION_OUTDATED_SENSITIVITY"
    PICO_EXTRACTIVE_ACCURACY = "PICO_EXTRACTIVE_ACCURACY"
    PHARMACOLOGICAL_DRUG_HERB_SAFETY = "PHARMACOLOGICAL_DRUG_HERB_SAFETY"
    CLINICAL_REASONING_TRIAGE = "CLINICAL_REASONING_TRIAGE"
    REGULATORY_JURISDICTION_SEGREGATION = "REGULATORY_JURISDICTION_SEGREGATION"
    TRADITIONAL_EPISTEMIC_PRESERVATION = "TRADITIONAL_EPISTEMIC_PRESERVATION"
    ONTOLOGICAL_CONSISTENCY = "ONTOLOGICAL_CONSISTENCY"
    STATISTICAL_METHODOLOGY_SOUNDNESS = "STATISTICAL_METHODOLOGY_SOUNDNESS"
    REPRODUCIBILITY_SNAPSHOT_REPLAY = "REPRODUCIBILITY_SNAPSHOT_REPLAY"
    SEARCH_RETRIEVAL_QUALITY = "SEARCH_RETRIEVAL_QUALITY"
    ROBUSTNESS_PERTURBATION = "ROBUSTNESS_PERTURBATION"
    ZERO_HALLUCINATION_NEGATIVE_CONTROLS = "ZERO_HALLUCINATION_NEGATIVE_CONTROLS"
    TENANT_PRIVACY_SECURITY_ISOLATION = "TENANT_PRIVACY_SECURITY_ISOLATION"
    DRIFT_RESISTANCE_TEMPORAL = "DRIFT_RESISTANCE_TEMPORAL"
    COMPUTE_LATENCY_THROUGHPUT = "COMPUTE_LATENCY_THROUGHPUT"
    HUMAN_EXPERT_CONCORDANCE = "HUMAN_EXPERT_CONCORDANCE"


class BenchmarkDatasetType(str, Enum):
    """Golden Benchmark Batteries covering clinical, scientific, safety, and governance domains."""
    MEDQA_USMLE = "MEDQA_USMLE"
    PUBMED_QA = "PUBMED_QA"
    NEGATIVE_CONTROLS = "NEGATIVE_CONTROLS"
    TRADITIONAL_EPISTEMIC = "TRADITIONAL_EPISTEMIC"
    DRUG_HERB_SAFETY = "DRUG_HERB_SAFETY"
    CITATION_FIDELITY = "CITATION_FIDELITY"
    EVIDENCE_EXTRACTION = "EVIDENCE_EXTRACTION"
    SCIENTIFIC_CALCULATION = "SCIENTIFIC_CALCULATION"
    CAUSAL_MECHANISTIC = "CAUSAL_MECHANISTIC"
    REGULATORY_JURISDICTION = "REGULATORY_JURISDICTION"
    REPRODUCIBILITY_REPLAY = "REPRODUCIBILITY_REPLAY"
    SECURITY_PRIVACY_INTEGRITY = "SECURITY_PRIVACY_INTEGRITY"


class BenchmarkItemVerdict(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    UNKNOWN_CORRECT = "UNKNOWN_CORRECT"
    REJECTED_CONTRAINDICATION = "REJECTED_CONTRAINDICATION"
    OVERCLAIM_PREVENTED = "OVERCLAIM_PREVENTED"
    JURISDICTION_SECLUDED = "JURISDICTION_SECLUDED"


class GoNoGoDecision(str, Enum):
    GO = "GO"
    CONDITIONAL = "CONDITIONAL"
    REQUIRES_REMEDIATION = "REQUIRES_REMEDIATION"
    NOT_VALIDATED = "NOT_VALIDATED"
    NO_GO = "NO_GO"


class BenchmarkTestCase(BaseModel):
    case_id: str
    dataset: BenchmarkDatasetType
    prompt_query: str
    expected_answer: str
    expected_status: Optional[str] = None  # e.g. "UNKNOWN", "NO_EVIDENCE", "CONTRAINDICATED"
    acceptable_epistemic_range: Optional[Tuple[float, float]] = None
    target_dimension: Optional[ValidationDimension] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TestCaseResult(BaseModel):
    case_id: str
    verdict: BenchmarkItemVerdict
    actual_response: str
    actual_status: str
    observed_score: float
    hallucination_detected: bool = False
    epistemic_fidelity: float = 1.0
    calculation_error: bool = False
    citation_valid: bool = True
    causal_overclaim_detected: bool = False
    jurisdiction_isolated: bool = True
    details: Dict[str, Any] = Field(default_factory=dict)


class BenchmarkRunReport(BaseModel):
    run_id: str
    dataset: BenchmarkDatasetType
    total_cases: int
    passed_cases: int
    failed_cases: int
    accuracy: float
    hallucination_rate: float
    citation_fidelity: float
    epistemic_distance_preservation: float
    calculation_precision: float = 1.0
    causal_integrity_score: float = 1.0
    jurisdiction_compliance_score: float = 1.0
    duration_ms: float
    case_results: List[TestCaseResult]
    executed_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class DimensionEvaluationResult(BaseModel):
    dimension: ValidationDimension
    status: str
    score: float
    threshold: float
    decision: GoNoGoDecision
    critical_gate: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)


class ScientificValidationReport(BaseModel):
    report_id: str
    suite_version: str = "v33.0.0"
    overall_decision: GoNoGoDecision
    is_production_candidate: bool
    total_batteries: int
    passed_batteries: int
    overall_accuracy: float
    citation_hallucination_rate: float
    calculation_error_rate: float
    epistemic_preservation_score: float
    reproducibility_divergence_rate: float
    cross_tenant_leakage_rate: float
    dimension_evaluations: List[DimensionEvaluationResult]
    battery_reports: Dict[str, BenchmarkRunReport]
    go_no_go_matrix: Dict[str, str]
    certification_hash: str
    duration_ms: float
    executed_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
