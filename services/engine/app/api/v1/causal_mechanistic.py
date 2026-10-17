"""
ZMIE Medical Causal & Mechanistic Intelligence API Router
Endpoints for multi-scale biological decomposition, causal DAG identification,
competing mechanistic hypotheses, traditional formulation networks, and experimental discrimination.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.models.causal_mechanistic import (
    BiologicalScale,
    CausalityState,
    MechanismState,
    ExperimentalValidationLevel,
    MedicalTraditionSystem,
    DAGNode,
    DAGEdge,
    MechanisticProposition,
    CausalProposition,
    CompetingMechanismCluster,
    NextBestExperimentProposal,
    TraditionalMedicineBridge,
    MechanismSnapshot
)
from app.causal_mechanistic.engine import CausalMechanisticEngine

router = APIRouter(prefix="/causal-mechanistic", tags=["Causal & Mechanistic Intelligence"])

# Global engine singleton
_engine_instance = CausalMechanisticEngine()

def get_engine() -> CausalMechanisticEngine:
    return _engine_instance


# -------------------------------------------------------------
# Request Schemas
# -------------------------------------------------------------

class DecomposeRequest(BaseModel):
    compound_id: str
    target_outcome: str = "Reduction in Fasting Blood Glucose / HbA1c"


class DiscriminatingExperimentRequest(BaseModel):
    cluster_id: str


class DAGValidateRequest(BaseModel):
    exposure: str
    outcome: str
    nodes: List[DAGNode]
    edges: List[DAGEdge]
    observed_effect_rr: Optional[float] = None


class TraditionalBridgeRequest(BaseModel):
    native_term: str
    tradition: MedicalTraditionSystem


class SnapshotCreateRequest(BaseModel):
    proposition_id: str


# -------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------

@router.post("/mechanisms/decompose", response_model=MechanisticProposition)
async def decompose_mechanism(
    req: DecomposeRequest,
    engine: CausalMechanisticEngine = Depends(get_engine)
):
    """
    Decomposes an intervention into an ordered multi-scale chain:
    Compound -> Target -> Pathway -> Cellular Phenotype -> Biomarker -> Clinical Outcome.
    Includes translational gap analysis and human PK-plausibility checks.
    """
    return engine.decompose_mechanism(
        intervention_or_compound_id=req.compound_id,
        target_clinical_outcome=req.target_outcome
    )


@router.get("/mechanisms/competing/{compound_id}", response_model=Optional[CompetingMechanismCluster])
async def get_competing_mechanisms(
    compound_id: str,
    engine: CausalMechanisticEngine = Depends(get_engine)
):
    """
    Retrieves competing mechanistic hypotheses for an intervention rather than forcing an artificial consensus.
    """
    cluster = engine.get_competing_mechanisms(compound_id)
    if not cluster:
        raise HTTPException(
            status_code=404,
            detail=f"No competing mechanistic hypotheses cluster found for {compound_id}."
        )
    return cluster


@router.post("/mechanisms/experiments/propose", response_model=NextBestExperimentProposal)
async def propose_discriminating_experiment(
    req: DiscriminatingExperimentRequest,
    engine: CausalMechanisticEngine = Depends(get_engine)
):
    """
    Generates a protocol for an empirical experiment designed to adjudicate
    between competing mechanistic hypotheses.
    """
    prop = engine.propose_discriminating_experiment(req.cluster_id)
    if not prop:
        raise HTTPException(
            status_code=404,
            detail=f"Unable to propose experiment for cluster {req.cluster_id}."
        )
    return prop


@router.post("/causal/dag/validate", response_model=CausalProposition)
async def validate_causal_dag(
    req: DAGValidateRequest,
    engine: CausalMechanisticEngine = Depends(get_engine)
):
    """
    Causality Firewall:
    Validates DAG structure, detects backdoor unmeasured confounding, flags collider stratification,
    and gates causal identification defensibility.
    """
    return engine.validate_causal_dag_and_identification(
        exposure=req.exposure,
        outcome=req.outcome,
        nodes=req.nodes,
        edges=req.edges,
        observed_effect_rr=req.observed_effect_rr
    )


@router.post("/traditional/bridge", response_model=TraditionalMedicineBridge)
async def bridge_traditional_concept(
    req: TraditionalBridgeRequest,
    engine: CausalMechanisticEngine = Depends(get_engine)
):
    """
    Maps native Unani/Ayurveda concepts (Mizaj, Dosha, Akhlat) to modern systems biology correlates
    with explicit epistemic warnings preventing false ontological reduction.
    """
    return engine.bridge_traditional_concept(req.native_term, req.tradition)


@router.get("/traditional/formulations/{formulation_id}/interactions")
async def analyze_formulation_synergy_and_interactions(
    formulation_id: str,
    engine: CausalMechanisticEngine = Depends(get_engine)
):
    """
    Analyzes polyherbal synergy, bioenhancement mechanisms (e.g. Piperine), and pharmacokinetic herb-drug interactions.
    """
    res = engine.analyze_formulation_synergy_and_interactions(formulation_id)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res


@router.get("/entities/compounds/{compound_id}")
async def get_compound(
    compound_id: str,
    engine: CausalMechanisticEngine = Depends(get_engine)
):
    c = engine.get_compound(compound_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Compound {compound_id} not found.")
    return c


@router.get("/entities/targets/{target_id}")
async def get_target(
    target_id: str,
    engine: CausalMechanisticEngine = Depends(get_engine)
):
    t = engine.get_target(target_id)
    if not t:
        raise HTTPException(status_code=404, detail=f"Target {target_id} not found.")
    return t


@router.get("/entities/pathways/{pathway_id}")
async def get_pathway(
    pathway_id: str,
    engine: CausalMechanisticEngine = Depends(get_engine)
):
    p = engine.get_pathway(pathway_id)
    if not p:
        raise HTTPException(status_code=404, detail=f"Pathway {pathway_id} not found.")
    return p


@router.post("/snapshots", response_model=MechanismSnapshot)
async def create_mechanism_snapshot(
    req: SnapshotCreateRequest,
    engine: CausalMechanisticEngine = Depends(get_engine)
):
    try:
        return engine.create_snapshot(req.proposition_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
