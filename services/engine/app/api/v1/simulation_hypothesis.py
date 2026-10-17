"""ZMIE Medical Knowledge Simulation, Research Hypothesis & Next-Best-Experiment API Router.

Endpoints for:
- Registering and querying scientific hypotheses with strict epistemic status
- Discriminating competing hypotheses via divergent prediction analysis
- Computational simulation sweeps (PK/PD compartmental models under Monte Carlo uncertainty)
- Next-best-experiment design with information gain E[ΔU] and anti-redundancy checks
- Empirical result ingestion and Bayesian hypothesis updating
- Discovering prioritized research opportunities
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.models.simulation_hypothesis import (
    DiscriminatingExperimentReport,
    ExperimentDesignType,
    ExperimentProposal,
    ExperimentResultRecord,
    Hypothesis,
    HypothesisType,
    ResearchOpportunity,
    ScientificModel,
    SimulationRun,
)
from app.simulation_hypothesis.engine import SimulationHypothesisEngine

router = APIRouter(prefix="/simulation-hypothesis", tags=["Simulation, Hypothesis & Next-Best-Experiment"])

_engine_instance = SimulationHypothesisEngine()


def get_engine() -> SimulationHypothesisEngine:
    return _engine_instance


# -------------------------------------------------------------
# Request Schemas
# -------------------------------------------------------------

class DiscriminateRequest(BaseModel):
    hypothesis_id_a: str
    hypothesis_id_b: str


class GenerateHypothesesRequest(BaseModel):
    domain_topic: str
    observed_conflict: str
    candidate_entities: List[str] = Field(default_factory=list)


class RunSimulationRequest(BaseModel):
    model_id: str
    scenario_name: str
    dose_or_perturbation: float = 25.0
    time_points_hours: Optional[List[float]] = None
    monte_carlo_iterations: int = 500


class ProposeExperimentRequest(BaseModel):
    target_hypothesis_id: str
    preferred_design_type: Optional[ExperimentDesignType] = None
    max_cost_tier: str = "HIGH"


class IngestResultRequest(BaseModel):
    proposal_id: str
    observed_direction: str  # DECREASE, INCREASE, NO_CHANGE
    observed_value: float
    confidence_interval: List[float] = Field(default_factory=list)
    p_value: float = 0.005
    laboratory_provenance: Dict[str, Any] = Field(default_factory=dict)


# -------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------

@router.get("/hypotheses", response_model=List[Hypothesis])
async def list_hypotheses(
    hypothesis_type: Optional[HypothesisType] = Query(None, description="Filter by hypothesis type"),
    engine: SimulationHypothesisEngine = Depends(get_engine),
):
    """Lists all registered hypotheses with current epistemic statuses and posteriors."""
    return engine.list_hypotheses(hypothesis_type)


@router.post("/hypotheses", response_model=Hypothesis)
async def create_hypothesis(
    hypothesis: Hypothesis,
    engine: SimulationHypothesisEngine = Depends(get_engine),
):
    """Registers a new scientific hypothesis with explicit falsification criteria and predictions."""
    return engine.create_hypothesis(hypothesis)


@router.get("/hypotheses/{hypothesis_id}", response_model=Hypothesis)
async def get_hypothesis(
    hypothesis_id: str,
    engine: SimulationHypothesisEngine = Depends(get_engine),
):
    """Retrieves full details for a hypothesis including causal DAG links and predictions."""
    hyp = engine.get_hypothesis(hypothesis_id)
    if not hyp:
        raise HTTPException(status_code=404, detail=f"Hypothesis {hypothesis_id} not found.")
    return hyp


@router.post("/hypotheses/competing/discriminate", response_model=DiscriminatingExperimentReport)
async def discriminate_hypotheses(
    req: DiscriminateRequest,
    engine: SimulationHypothesisEngine = Depends(get_engine),
):
    """Analyzes two competing hypotheses, isolates divergent predictions, and generates decisive discriminating experiments."""
    try:
        return engine.discriminate_competing_hypotheses(req.hypothesis_id_a, req.hypothesis_id_b)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/hypotheses/generate-from-conflict", response_model=List[Hypothesis])
async def generate_hypotheses_from_conflict(
    req: GenerateHypothesesRequest,
    engine: SimulationHypothesisEngine = Depends(get_engine),
):
    """Synthesizes competing mechanistic hypotheses from an observed clinical or evidentiary conflict."""
    return engine.generate_mechanistic_hypotheses_from_conflict(
        domain_topic=req.domain_topic,
        observed_conflict=req.observed_conflict,
        candidate_entities=req.candidate_entities,
    )


@router.post("/models", response_model=ScientificModel)
async def register_model(
    model: ScientificModel,
    engine: SimulationHypothesisEngine = Depends(get_engine),
):
    """Registers a computational or mathematical scientific model for simulation."""
    return engine.register_model(model)


@router.post("/simulations/run", response_model=SimulationRun)
async def run_simulation(
    req: RunSimulationRequest,
    engine: SimulationHypothesisEngine = Depends(get_engine),
):
    """Runs a Monte Carlo parametric simulation sweep. Output is strictly tagged MODEL_PREDICTED."""
    try:
        return engine.run_simulation(
            model_id=req.model_id,
            scenario_name=req.scenario_name,
            dose_or_perturbation=req.dose_or_perturbation,
            time_points_hours=req.time_points_hours,
            monte_carlo_iterations=req.monte_carlo_iterations,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/experiments/next-best", response_model=ExperimentProposal)
async def propose_next_best_experiment(
    req: ProposeExperimentRequest,
    engine: SimulationHypothesisEngine = Depends(get_engine),
):
    """Calculates the optimal prospective experiment to maximize information gain E[ΔU].
    
    Includes mandatory anti-redundancy checks and human-researcher review flag.
    """
    try:
        return engine.propose_next_best_experiment(
            target_hypothesis_id=req.target_hypothesis_id,
            preferred_design_type=req.preferred_design_type,
            max_cost_tier=req.max_cost_tier,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/experiments/results", response_model=ExperimentResultRecord)
async def ingest_experiment_result(
    req: IngestResultRequest,
    engine: SimulationHypothesisEngine = Depends(get_engine),
):
    """Ingests empirical study results (OBSERVED status), updates Bayesian posterior, and adjusts competing hypotheses."""
    try:
        return engine.ingest_experiment_result(
            proposal_id=req.proposal_id,
            observed_direction=req.observed_direction,
            observed_value=req.observed_value,
            confidence_interval=req.confidence_interval,
            p_value=req.p_value,
            laboratory_provenance=req.laboratory_provenance,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/opportunities", response_model=List[ResearchOpportunity])
async def discover_research_opportunities(
    engine: SimulationHypothesisEngine = Depends(get_engine),
):
    """Retrieves prioritized research opportunities across high-uncertainty, high-impact clinical domains."""
    return engine.discover_research_opportunities()
