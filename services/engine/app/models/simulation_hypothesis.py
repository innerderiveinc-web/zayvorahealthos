"""ZMIE Medical Knowledge Simulation, Research Hypothesis & Next-Best-Experiment Engine Data Models.

Defines schemas for:
- Epistemic status enforcement (OBSERVED, REPORTED, SUPPORTED_BY_EVIDENCE, MODEL_PREDICTED, HYPOTHESIZED, ACTUALLY_TESTED)
- Hypotheses (mechanistic, causal, predictive, translational, traditional bridge)
- Scientific Models (DAGs, kinetic, PK/PD, systems dynamics)
- Simulation Runs (Monte Carlo sweeps, parameter uncertainty, strictly MODEL_PREDICTED)
- Experiment Proposals & Discriminating Experiments (Information Gain, Falsification, Feasibility, Cost, Ethical Governance)
- Experiment Result Records (Bayesian posterior updating, knowledge graph propagation)
- Multi-dimensional Research Opportunities
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class EpistemicStatus(str, Enum):
    """Rigorous epistemic boundaries preventing blurring between simulation and reality."""
    OBSERVED = "OBSERVED"
    REPORTED = "REPORTED"
    SUPPORTED_BY_EVIDENCE = "SUPPORTED_BY_EVIDENCE"
    MODEL_PREDICTED = "MODEL_PREDICTED"
    HYPOTHESIZED = "HYPOTHESIZED"
    ACTUALLY_TESTED = "ACTUALLY_TESTED"


class HypothesisType(str, Enum):
    """Class of scientific hypothesis."""
    MECHANISTIC = "MECHANISTIC"
    CAUSAL = "CAUSAL"
    PREDICTIVE = "PREDICTIVE"
    TRANSLATIONAL = "TRANSLATIONAL"
    TRADITIONAL_BRIDGE = "TRADITIONAL_BRIDGE"
    PHENOTYPIC_SUBGROUP = "PHENOTYPIC_SUBGROUP"


class HypothesisStatus(str, Enum):
    """Lifecycle state of scientific hypothesis."""
    PROPOSED = "PROPOSED"
    UNDER_TEST = "UNDER_TEST"
    SUPPORTED = "SUPPORTED"
    CONTESTED = "CONTESTED"
    WEAKENED = "WEAKENED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"


class HypothesisOrigin(str, Enum):
    """Provenance origin of hypothesis."""
    LITERATURE_DERIVED = "LITERATURE_DERIVED"
    EVIDENCE_DERIVED = "EVIDENCE_DERIVED"
    GRAPH_MINED = "GRAPH_MINED"
    AI_GENERATED = "AI_GENERATED"
    ANALOGICAL = "ANALOGICAL"
    TRADITIONAL_BRIDGE = "TRADITIONAL_BRIDGE"


class ObservablePrediction(BaseModel):
    """Concrete, falsifiable prediction deduced from a hypothesis."""
    prediction_id: str
    statement: str
    target_biomarker_or_endpoint: str
    direction_of_effect: str  # e.g., "INCREASE", "DECREASE", "NO_CHANGE", "BIPHASIC"
    quantitative_estimate: Optional[float] = None
    confidence_interval: Optional[List[float]] = None  # e.g. [lower, upper]
    measurement_context: str  # e.g., "Plasma LC-MS at 4h", "Echocardiogram LVEF at 12w"
    epistemic_status: EpistemicStatus = EpistemicStatus.MODEL_PREDICTED
    decisive_for_discrimination: bool = False


class DisconfirmingCriterion(BaseModel):
    """Explicit threshold or outcome that would disconfirm or severely weaken the hypothesis."""
    criterion_id: str
    observation_condition: str
    falsification_threshold: str
    epistemic_weight: float = Field(default=0.8, ge=0.0, le=1.0)


class Hypothesis(BaseModel):
    """Formal representation of a testable scientific hypothesis."""
    hypothesis_id: str
    statement: str
    hypothesis_type: HypothesisType
    status: HypothesisStatus = HypothesisStatus.PROPOSED
    origin: HypothesisOrigin
    assumptions: List[str] = Field(default_factory=list)
    causal_mechanistic_links: List[Dict[str, Any]] = Field(default_factory=list)
    predictions: List[ObservablePrediction] = Field(default_factory=list)
    falsification_criteria: List[DisconfirmingCriterion] = Field(default_factory=list)
    prior_probability: float = Field(default=0.5, ge=0.0, le=1.0)
    current_posterior: float = Field(default=0.5, ge=0.0, le=1.0)
    epistemic_status: EpistemicStatus = EpistemicStatus.HYPOTHESIZED
    competing_hypothesis_ids: List[str] = Field(default_factory=list)
    traditional_medicine_bridge: Optional[Dict[str, Any]] = None  # Native Unani/Ayurvedic mapping without retrofitting
    version: str = "v1.0"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: str
    updated_at: str


class ScientificModel(BaseModel):
    """Computational/mathematical/causal representation supporting simulation."""
    model_id: str
    name: str
    model_type: str  # e.g. "CAUSAL_DAG", "PK_PD_COMPARTMENTAL", "SYSTEMS_DYNAMICS", "METABOLIC_FLUX"
    parameters: List[Dict[str, Any]] = Field(default_factory=list)  # includes name, value, is_measured, distribution
    equations_or_structure: List[str] = Field(default_factory=list)
    associated_hypothesis_ids: List[str] = Field(default_factory=list)
    epistemic_status: EpistemicStatus = EpistemicStatus.MODEL_PREDICTED


class SimulationRun(BaseModel):
    """Outcome of a computational simulation sweep under parameter uncertainty."""
    simulation_id: str
    model_id: str
    scenario_name: str
    parameters_used: Dict[str, Any] = Field(default_factory=dict)
    monte_carlo_iterations: int = 1000
    predicted_outcomes: Dict[str, Any] = Field(default_factory=dict)
    credible_intervals_95: Dict[str, List[float]] = Field(default_factory=dict)
    epistemic_status: EpistemicStatus = EpistemicStatus.MODEL_PREDICTED
    epistemic_disclaimer: str = (
        "SIMULATION ONLY: STRICT EPISTEMIC BOUNDARY: This is a computational simulation result (MODEL_PREDICTED). "
        "It does NOT represent observed patient or laboratory evidence."
    )
    timestamp: str


class ExperimentDesignType(str, Enum):
    """Classification of prospective experimental architectures."""
    IN_VITRO_ASSAY = "IN_VITRO_ASSAY"
    IN_VIVO_ANIMAL = "IN_VIVO_ANIMAL"
    CLINICAL_TRIAL = "CLINICAL_TRIAL"
    RWE_OBSERVATIONAL_COHORT = "RWE_OBSERVATIONAL_COHORT"
    IN_SILICO_PERTURBATION = "IN_SILICO_PERTURBATION"


class ExperimentProposal(BaseModel):
    """Actionable scientific study proposal optimized for information gain and falsification."""
    proposal_id: str
    scientific_question: str
    target_hypothesis_id: str
    competing_hypothesis_ids: List[str] = Field(default_factory=list)
    design_type: ExperimentDesignType
    intervention: str
    comparator: str
    controls: Dict[str, str] = Field(default_factory=dict)  # positive, negative, vehicle
    endpoint: str
    expected_outcomes: Dict[str, str] = Field(default_factory=dict)  # Outcomes under Hyp A vs Hyp B
    information_gain_score: float = Field(default=0.7, ge=0.0, le=1.0)  # E[ΔU] Expected uncertainty reduction
    discrimination_power: float = Field(default=0.8, ge=0.0, le=1.0)
    feasibility_score: float = Field(default=0.8, ge=0.0, le=1.0)
    estimated_cost_tier: str = "MEDIUM"  # LOW, MEDIUM, HIGH, EXTREME
    ethical_risk_tier: str = "LOW"  # MINIMAL, LOW, MODERATE, HIGH_IRB_MANDATED
    preregistration_protocol: Optional[str] = None
    existing_data_checked: bool = True  # Verified no redundant literature/RWE exists
    human_approval_required: bool = True  # Strict: human researcher must review/approve
    recommendation_rationale: str = ""


class DiscriminatingExperimentReport(BaseModel):
    """Comparative analysis contrasting two or more competing hypotheses to find decisive tests."""
    report_id: str
    competing_hypotheses: List[Dict[str, Any]]
    divergence_points: List[str]
    decisive_biomarkers: List[str]
    recommended_experiments: List[ExperimentProposal]
    synthetic_summary: str


class ExperimentResultRecord(BaseModel):
    """Empirical or observational readout ingested to update hypothesis credence."""
    result_id: str
    proposal_id: str
    hypothesis_id: str
    observed_outcome: Dict[str, Any]
    confidence_interval: Optional[List[float]] = None
    p_value_or_bayes_factor: Optional[float] = None
    epistemic_status: EpistemicStatus = EpistemicStatus.OBSERVED  # Strictly OBSERVED or ACTUALLY_TESTED
    effect_on_hypothesis: str  # SUPPORTS, WEAKENS, REFUTES, INCONCLUSIVE
    prior_probability: float
    updated_posterior: float
    evidence_provenance: Dict[str, Any] = Field(default_factory=dict)
    recorded_at: str


class ResearchOpportunity(BaseModel):
    """Multi-dimensional priority ranking for scientific investigation."""
    opportunity_id: str
    scientific_domain: str
    title: str
    hypothesis_cluster: List[str]
    uncertainty_reduction_potential: float
    unmet_clinical_need: str
    feasibility: float
    cost_tier: str
    overall_priority: str  # HIGH, MEDIUM, LOW
    rationale: str
