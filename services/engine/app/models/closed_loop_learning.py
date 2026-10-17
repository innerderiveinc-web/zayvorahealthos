"""ZMIE Scientific Knowledge Closed-Loop Learning System Models.

Defines schemas for the complete 5-stage discovery and learning cycle:
SCIENTIFIC KNOWLEDGE -> HYPOTHESIS -> EXPERIMENT -> EVIDENCE -> KNOWLEDGE LEARNING SYSTEM
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from app.models.simulation_hypothesis import (
    EpistemicStatus,
    ExperimentProposal,
    ExperimentResultRecord,
    Hypothesis,
    SimulationRun,
)


class LearningLoopStage(str, Enum):
    """The 5 distinct phases of the scientific discovery cycle."""
    SCIENTIFIC_KNOWLEDGE = "1_SCIENTIFIC_KNOWLEDGE"
    HYPOTHESIS_FORMULATION = "2_HYPOTHESIS_FORMULATION"
    EXPERIMENT_DESIGN = "3_EXPERIMENT_DESIGN"
    EVIDENCE_INGESTION = "4_EVIDENCE_INGESTION"
    KNOWLEDGE_LEARNING = "5_KNOWLEDGE_LEARNING"


class KnowledgeStateSnapshot(BaseModel):
    """Immutable snapshot of the knowledge system at time t."""
    snapshot_id: str
    topic: str
    active_hypotheses_count: int
    confirmed_causal_edges: int
    unresolved_uncertainties_count: int
    shannon_entropy: float
    living_reviews_version: str
    regulatory_guideline_alignment: str
    timestamp: str


class EpistemicDelta(BaseModel):
    """Explicit delta explaining how knowledge evolved from t to t+1."""
    delta_id: str
    hypothesis_id: str
    prior_credence: float
    posterior_credence: float
    status_transition: str  # e.g., "PROPOSED -> SUPPORTED" or "UNDER_TEST -> WEAKENED"
    causal_edge_weight_updates: List[Dict[str, Any]] = Field(default_factory=list)
    living_evidence_impact: str  # e.g. "REINFORCED_POOLED_EFFECT" or "CONCLUSION_UNCHANGED"
    entropy_reduction: float  # ΔH = H_before - H_after
    retired_assumptions: List[str] = Field(default_factory=list)
    new_questions_opened: List[str] = Field(default_factory=list)


class ClosedLoopCycleExecution(BaseModel):
    """Complete traceable trajectory of a full closed-loop learning cycle."""
    cycle_id: str
    topic: str
    stage_progression: List[str] = Field(default_factory=list)
    initial_knowledge_state: KnowledgeStateSnapshot
    formulated_hypotheses: List[Hypothesis]
    competing_divergence_summary: Optional[str] = None
    simulation_run: Optional[SimulationRun] = None
    executed_proposal: ExperimentProposal
    ingested_evidence: ExperimentResultRecord
    epistemic_delta: EpistemicDelta
    updated_knowledge_state: KnowledgeStateSnapshot
    master_epistemic_verdict: str
    started_at: str
    completed_at: str
