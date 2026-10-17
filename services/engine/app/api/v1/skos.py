"""
ZMIE Scientific Knowledge Operating System REST API Gateway (Prompt 25)
Exposes the master Knowledge Fabric, Graph of Graphs Traversal Paths,
Revalidation Engine, Retraction Cascades, Snapshots, Diffs, Gaps,
Unified Answers, and Learning Loop (Clauses 124-130, 345).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Header, Query, status
from pydantic import BaseModel, Field

from app.skos import (
    get_skos,
    SKOSMasterEntity,
    SKOSEntityType,
    TraversalPath,
    ZMIEKnowledgeSnapshot,
    ScientificKnowledgeDiff,
    KnowledgeGapMap,
    RetractionNotice,
    RetractionImpactAnalysis,
    RevalidationTask,
    RevalidationDecision,
    KnowledgeDecisionAction,
    SKOSAnswer
)

router = APIRouter(prefix="/skos", tags=["Scientific Knowledge Operating System"])


# ==============================================================================
# Request / Response Schemas
# ==============================================================================

class AnswerRequest(BaseModel):
    question: str
    target_system: str = "all"
    simulate_partial: bool = False


class TriggerRevalidationRequest(BaseModel):
    new_study_doi: str
    target_claim_id: str
    reason: str


class DecideRevalidationRequest(BaseModel):
    reviewer_user_id: str
    action: KnowledgeDecisionAction
    rationale: str


class DiffRequest(BaseModel):
    snapshot_a_id: str
    snapshot_b_id: str


# ==============================================================================
# 1. Knowledge Fabric & Master Entity Endpoints (Clauses 6-10, 125)
# ==============================================================================

@router.get("/fabric/entities", response_model=List[SKOSMasterEntity])
def list_entities(
    entity_type: Optional[SKOSEntityType] = Query(None),
    x_tenant_id: Optional[str] = Header(None)
):
    skos = get_skos()
    if entity_type:
        return skos.fabric.list_entities_by_type(entity_type)
    return skos.fabric.list_all_entities(tenant_id=x_tenant_id)


@router.get("/fabric/entities/{id}", response_model=SKOSMasterEntity)
def get_entity(id: str):
    skos = get_skos()
    ent = skos.fabric.get_entity(id)
    if not ent:
        raise HTTPException(status_code=404, detail=f"Entity '{id}' not found in Knowledge Fabric.")
    return ent


# ==============================================================================
# 2. Graph of Graphs & Multi-Hop Paths (Clauses 55-60, 127, 311-314)
# ==============================================================================

@router.get("/graph/paths/{path_type}", response_model=TraversalPath)
def get_traversal_path(
    path_type: str,
    start_id: Optional[str] = Query(None),
    end_id: Optional[str] = Query(None)
):
    skos = get_skos()
    return skos.get_path(path_type, start_id=start_id, end_id=end_id)


@router.get("/graph/traverse", response_model=TraversalPath)
def traverse_master_path(direction: str = Query("FORWARD")):
    skos = get_skos()
    return skos.graph.traverse_master_scientific_path(direction=direction)


# ==============================================================================
# 3. Knowledge Revalidation & Retraction Impact (Clauses 34, 64-70, 128, 303)
# ==============================================================================

@router.post("/revalidation/trigger", response_model=RevalidationTask)
def trigger_revalidation(req: TriggerRevalidationRequest):
    skos = get_skos()
    return skos.revalidation.trigger_new_evidence_revalidation(
        new_study_doi=req.new_study_doi,
        target_claim_id=req.target_claim_id,
        reason=req.reason
    )


@router.get("/revalidation/tasks", response_model=List[RevalidationTask])
def list_revalidation_tasks():
    skos = get_skos()
    return skos.revalidation.list_tasks()


@router.post("/revalidation/tasks/{id}/decide", response_model=RevalidationDecision)
def decide_revalidation(id: str, req: DecideRevalidationRequest):
    skos = get_skos()
    try:
        return skos.revalidation.record_decision(
            task_id=id,
            reviewer_user_id=req.reviewer_user_id,
            action=req.action,
            rationale=req.rationale
        )
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Revalidation task '{id}' not found.")


@router.post("/retractions/impact", response_model=RetractionImpactAnalysis)
def analyze_retraction_impact(notice: RetractionNotice):
    skos = get_skos()
    return skos.revalidation.handle_retraction(notice)


@router.get("/retractions", response_model=List[RetractionImpactAnalysis])
def list_retractions():
    skos = get_skos()
    return skos.revalidation.list_retraction_analyses()


# ==============================================================================
# 4. Snapshots, Diffs & Gaps (Clauses 13, 14, 62, 71)
# ==============================================================================

@router.get("/snapshots", response_model=List[ZMIEKnowledgeSnapshot])
def list_snapshots():
    skos = get_skos()
    return skos.snapshots.list_snapshots()


@router.post("/snapshots", response_model=ZMIEKnowledgeSnapshot, status_code=status.HTTP_201_CREATED)
def create_snapshot(
    description: str = "Master Knowledge Snapshot",
    x_tenant_id: Optional[str] = Header(None)
):
    skos = get_skos()
    return skos.snapshots.create_snapshot(tenant_id=x_tenant_id, description=description)


@router.post("/snapshots/diff", response_model=ScientificKnowledgeDiff)
def compute_snapshot_diff(req: DiffRequest):
    skos = get_skos()
    return skos.snapshots.compute_diff(req.snapshot_a_id, req.snapshot_b_id)


@router.get("/gaps", response_model=KnowledgeGapMap)
def get_knowledge_gap_map(topic: str = Query("Berberine in Type 2 Diabetes")):
    skos = get_skos()
    return skos.gap_engine.analyze_gaps(topic=topic)


# ==============================================================================
# 5. Unified Scientific Answer & Learning Loop (Clauses 161-168, 315)
# ==============================================================================

@router.post("/answer", response_model=SKOSAnswer)
async def generate_answer(req: AnswerRequest):
    skos = get_skos()
    return await skos.answer(
        question=req.question,
        target_system=req.target_system,
        simulate_partial=req.simulate_partial
    )


@router.get("/learning-loop")
def get_learning_loop():
    skos = get_skos()
    return skos.get_learning_loop()


@router.get("/health")
def get_system_health():
    return {
        "status": "OPERATIONAL",
        "subsystem": "ZMIE Scientific Knowledge Operating System (SKOS)",
        "version": "1.0.0 Enterprise",
        "active_graphs": 16,
        "absolute_scientific_rules_enforced": 18,
        "epistemic_firewall": "ACTIVE",
        "zero_fabrication_gate": "ENFORCED",
        "negative_proof_fallacy_guard": "ENFORCED"
    }
