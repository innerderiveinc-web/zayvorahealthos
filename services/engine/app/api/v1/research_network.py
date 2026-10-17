"""
ZMIE Global Research Discovery Network & Continuous Knowledge Evolution API Router
Prompt 14 Implementation.

Provides endpoints for:
- Researcher discovery, disambiguation, and profiling
- Institutional research footprint and clinical trial capacity
- Full lifecycle tracing (Grant -> Project -> Trial -> Preprint -> Publication -> Patent)
- Canonical study resolution and evidence de-duplication
- Frontier & emerging research signal tracking
- Multi-system research discovery (Modern, Unani, Ayurveda, etc.)
- Continuous knowledge evolution cascade impact analysis
- Revalidation queue processing
- Research gap and blindspot analysis
- Knowledge snapshot creation and version diffing
"""

from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from app.models.research_network import (
    Researcher,
    ResearchInstitution,
    GrantRecord,
    ClinicalTrialRecord,
    PreprintRecord,
    ThesisRecord,
    DatasetRecord,
    PatentRecord,
    ResearchProject,
    ResearchSignal,
    ResearchGapAnalysis,
    EvolutionImpactAnalysis,
    KnowledgeSnapshot,
)
from app.research.network_engine import ResearchNetworkEngine
from app.research.evolution_engine import ContinuousKnowledgeEvolutionEngine

router = APIRouter(prefix="/research-network", tags=["Global Research Discovery & Continuous Evolution (Prompt 14)"])

# Singletons for memory engine persistence
network_engine = ResearchNetworkEngine()
evolution_engine = ContinuousKnowledgeEvolutionEngine(network_engine=network_engine)


# Request schemas
class DisambiguationRequest(BaseModel):
    name: str = Field(..., description="Researcher name to disambiguate")
    orcid: Optional[str] = Field(None, description="Optional ORCID ID")
    institution_name: Optional[str] = Field(None, description="Optional affiliated institution")
    subject_area: Optional[str] = Field(None, description="Optional subject area or disease domain")


class CascadeImpactRequest(BaseModel):
    trigger_type: str = Field(..., description="RETRACTION, NEW_STUDY, GUIDELINE_CHANGE, TRIAL_TERMINATION, SAFETY_SIGNAL")
    trigger_source_id: str = Field(..., description="DOI, Trial ID, Document ID or Publication anchor")
    reason: Optional[str] = Field("Automated continuous surveillance trigger", description="Justification/provenance")


class RevalidateEnqueueRequest(BaseModel):
    item_id: str = Field(..., description="ID of claim, relation, or study to revalidate")
    item_type: str = Field(..., description="CLAIM, RELATION, STUDY")
    priority: str = Field(default="HIGH", description="CRITICAL, HIGH, MEDIUM, LOW")
    rationale: str = Field(..., description="Reason for revalidation")


class SnapshotDiffRequest(BaseModel):
    snapshot_a_id: str = Field(..., description="Base snapshot ID")
    snapshot_b_id: str = Field(..., description="Target snapshot ID")


# -------------------------------------------------------------
# Entity Lookups & Profiling
# -------------------------------------------------------------

@router.get("/researchers/{researcher_id}", response_model=Researcher)
async def get_researcher(researcher_id: str):
    """Retrieves full researcher profile including ORCID, affiliations, metrics and traditional lineages."""
    res = network_engine.get_researcher(researcher_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Researcher '{researcher_id}' not found.")
    return res


@router.post("/researchers/disambiguate")
async def disambiguate_researcher(req: DisambiguationRequest):
    """
    Disambiguates researcher name against candidate records using composite keys
    (ORCID, institution, co-authorship, subject overlap). Prevents identity collision.
    """
    candidates = network_engine.disambiguate_researcher(
        name=req.name,
        orcid=req.orcid,
        institution_name=req.institution_name,
        subject_area=req.subject_area
    )
    return {
        "query": req.model_dump(),
        "candidates_count": len(candidates),
        "results": [
            {
                "researcher": c[0].model_dump(),
                "confidence_score": c[1],
                "disambiguation_rationale": c[2]
            }
            for c in candidates
        ]
    }


@router.get("/institutions/{institution_id}", response_model=ResearchInstitution)
async def get_institution(institution_id: str):
    """Retrieves institutional research footprint, active trial counts, and ROR identifiers."""
    inst = network_engine.get_institution(institution_id)
    if not inst:
        raise HTTPException(status_code=404, detail=f"Institution '{institution_id}' not found.")
    return inst


@router.get("/projects/{project_id}", response_model=ResearchProject)
async def get_project(project_id: str):
    """Retrieves project record, checking private/unobservable boundary constraints."""
    proj = network_engine.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found.")
    return proj


# -------------------------------------------------------------
# Query Resolvers: Who & Where
# -------------------------------------------------------------

@router.get("/who-is-researching")
async def who_is_researching(q: str = Query(..., description="Topic, condition, or drug query"), limit: int = 10):
    """
    Resolves: 'Who is researching this topic?'
    Returns top active researchers with verification score, active projects, and traditional lineage.
    """
    return network_engine.who_is_researching(query=q, limit=limit)


@router.get("/where-is-research-happening")
async def where_is_research_happening(q: str = Query("", description="Optional topic query")):
    """
    Resolves: 'Where is this research happening globally?'
    Returns global institutional distribution, active trial counts, and funding footprint.
    """
    return network_engine.where_is_research_happening(query=q)


# -------------------------------------------------------------
# Lifecycle Tracing & Canonical Study De-duplication
# -------------------------------------------------------------

@router.get("/canonical-study/{identifier}")
async def resolve_canonical_study(identifier: str):
    """
    Resolves a trial ID, preprint, or project to its Canonical Study cluster.
    Suppresses duplicate counting of preprints, trial registrations, and final journal publications.
    """
    return network_engine.resolve_canonical_study(identifier)


@router.get("/lifecycle/{root_id}")
async def get_lifecycle_trace(root_id: str):
    """
    Traverses complete research lifecycle forward and backward:
    Grant -> Project -> Protocol -> Trial -> Preprint -> Publication -> Patent.
    Enforces PRIVATE_UNOBSERVABLE boundaries for confidential projects.
    """
    return network_engine.get_lifecycle_trace(root_id)


# -------------------------------------------------------------
# Frontier & Emerging Research Signals
# -------------------------------------------------------------

@router.get("/frontier", response_model=List[ResearchSignal])
async def get_frontier_signals():
    """Retrieves high-velocity frontier research signals and emerging paradigm shifts."""
    return network_engine.get_frontier_signals()


# -------------------------------------------------------------
# Research Gaps & Blindspots
# -------------------------------------------------------------

@router.get("/gaps", response_model=List[ResearchGapAnalysis])
async def get_research_gaps(topic: Optional[str] = Query(None, description="Optional topic filter")):
    """
    'What Am I Missing?' engine. Identifies structural gaps:
    methodological deficits, population exclusions, unresolved contradictions, and traditional underinvestigation.
    """
    return evolution_engine.analyze_research_gaps(topic=topic)


# -------------------------------------------------------------
# Continuous Knowledge Evolution & Cascade Impact
# -------------------------------------------------------------

@router.post("/evolution/cascade", response_model=EvolutionImpactAnalysis)
async def trigger_cascade_impact(req: CascadeImpactRequest):
    """
    Simulates or executes a cascade impact analysis across dependent claims,
    evidence graph edges, and active projects when a trigger occurs (e.g. RETRACTION).
    """
    return evolution_engine.trigger_cascade_impact(
        trigger_type=req.trigger_type,
        trigger_source_id=req.trigger_source_id,
        reason=req.reason
    )


@router.post("/evolution/revalidate/enqueue")
async def enqueue_revalidation(req: RevalidateEnqueueRequest):
    """Enqueues an item into the prioritized revalidation queue."""
    return evolution_engine.enqueue_revalidation(
        item_id=req.item_id,
        item_type=req.item_type,
        priority=req.priority,
        rationale=req.rationale
    )


@router.post("/evolution/revalidate/process")
async def process_revalidation_queue(max_items: int = Query(10, description="Max items to process")):
    """Processes pending items from the revalidation queue in order of priority."""
    return evolution_engine.process_revalidation_queue(max_items=max_items)


@router.get("/evolution/snapshots", response_model=List[KnowledgeSnapshot])
async def get_snapshots():
    """Lists versioned knowledge snapshots."""
    return evolution_engine.get_snapshots()


@router.post("/evolution/snapshots")
async def create_snapshot(notes: str = Body("", embed=True)):
    """Captures an atomic snapshot of current medical knowledge states."""
    return evolution_engine.create_snapshot(notes=notes)


@router.post("/evolution/diff")
async def compute_snapshot_diff(req: SnapshotDiffRequest):
    """Computes differential metrics between two knowledge snapshots."""
    return evolution_engine.compute_snapshot_diff(req.snapshot_a_id, req.snapshot_b_id)


# -------------------------------------------------------------
# Master End-to-End Pipeline
# Source -> Research -> Data -> Mechanism/Causality -> Living Evidence -> Knowledge Evolution
# -------------------------------------------------------------

from app.research.master_pipeline import MasterKnowledgeEvolutionPipeline
master_pipeline_instance = MasterKnowledgeEvolutionPipeline(
    research_engine=network_engine,
    evolution_engine=evolution_engine
)

@router.post("/pipeline/master")
async def run_master_knowledge_evolution_pipeline(topic: str = Query("SGLT2_HEART_FAILURE", description="Clinical topic or intervention to trace")):
    """
    Executes the unbroken 6-stage scientific knowledge pipeline:
    Source -> Research -> Data -> Mechanism/Causality -> Living Evidence -> Knowledge Evolution.
    """
    return master_pipeline_instance.run_pipeline(topic=topic)
