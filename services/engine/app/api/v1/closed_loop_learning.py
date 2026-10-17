"""ZMIE Scientific Closed-Loop Discovery & Autonomous Knowledge Learning API Router.

Endpoints for:
- Executing the complete 5-stage loop:
  SCIENTIFIC KNOWLEDGE -> HYPOTHESIS -> EXPERIMENT -> EVIDENCE -> KNOWLEDGE LEARNING SYSTEM
- Inspecting immutable knowledge snapshots and entropy deltas
- Retrieving cycle execution reports
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.models.closed_loop_learning import (
    ClosedLoopCycleExecution,
    KnowledgeStateSnapshot,
)
from app.research.closed_loop_learning import ScientificClosedLoopLearningEngine

router = APIRouter(prefix="/closed-loop", tags=["Scientific Closed-Loop Learning System"])

_engine_instance = ScientificClosedLoopLearningEngine()


def get_engine() -> ScientificClosedLoopLearningEngine:
    return _engine_instance


# -------------------------------------------------------------
# Request Schemas
# -------------------------------------------------------------

class ExecuteCycleRequest(BaseModel):
    topic: str = "SGLT2_CARDIOPROTECTION"
    target_hypothesis_id: str = "HYP-SGLT2-NHE1"
    competing_hypothesis_id: str = "HYP-SGLT2-HEMO"
    simulated_dose_mg: float = 25.0
    observed_delta_pct: float = -28.5
    observed_p_value: float = 0.0015
    lab_provenance: Optional[Dict[str, Any]] = None


# -------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------

@router.post("/execute", response_model=ClosedLoopCycleExecution)
async def execute_closed_loop_cycle(
    req: ExecuteCycleRequest,
    engine: ScientificClosedLoopLearningEngine = Depends(get_engine),
):
    """Executes the complete 5-stage scientific discovery and knowledge learning continuum."""
    try:
        return engine.execute_closed_loop_cycle(
            topic=req.topic,
            target_hypothesis_id=req.target_hypothesis_id,
            competing_hypothesis_id=req.competing_hypothesis_id,
            simulated_dose_mg=req.simulated_dose_mg,
            observed_delta_pct=req.observed_delta_pct,
            observed_p_value=req.observed_p_value,
            lab_provenance=req.lab_provenance,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/executions", response_model=List[ClosedLoopCycleExecution])
async def list_cycle_executions(
    engine: ScientificClosedLoopLearningEngine = Depends(get_engine),
):
    """Retrieves all past executed closed-loop discovery and learning cycles."""
    return engine.list_cycle_executions()


@router.get("/executions/{cycle_id}", response_model=ClosedLoopCycleExecution)
async def get_cycle_execution(
    cycle_id: str,
    engine: ScientificClosedLoopLearningEngine = Depends(get_engine),
):
    """Retrieves a specific closed-loop cycle execution report."""
    cycle = engine.get_cycle_execution(cycle_id)
    if not cycle:
        raise HTTPException(status_code=404, detail=f"Closed-loop cycle {cycle_id} not found.")
    return cycle


@router.get("/snapshot", response_model=KnowledgeStateSnapshot)
async def capture_knowledge_snapshot(
    topic: str = Query("GENERAL_MEDICAL", description="Topic domain for knowledge state snapshot"),
    engine: ScientificClosedLoopLearningEngine = Depends(get_engine),
):
    """Captures an immutable snapshot of current scientific knowledge state and calculates Shannon entropy."""
    return engine.capture_knowledge_snapshot(topic)
