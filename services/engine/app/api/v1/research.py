"""
ZMIE Research Workbench API Router
Provides comprehensive endpoints for:
- Initiating & orchestrating deep research jobs
- Inspecting Research Plans, PICO frameworks, and search matrices
- Reviewing Evidence Tables and Screening Logs
- Analyzing Contradictions & Divergences
- Exploring Research Gaps & Next-Best-Research-Questions
- Generating & retrieving full evidence reports
- Capturing snapshots & computing diffs
"""

import json
import asyncio
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from app.models.research import (
    ResearchJob,
    ResearchPlan,
    ResearchReport,
    ResearchSnapshot,
    ResearchDiff,
    EvidenceTableEntry,
    ContradictionCluster,
    ResearchGapRecord
)
from app.research.engine import DeepResearchOperatingEngine
from app.agents.orchestrator import DeepResearchAgent, DeepResearchReport

router = APIRouter(prefix="/research", tags=["Research Workbench & Deep Investigation"])


class CreateResearchRequest(BaseModel):
    question: str = Field(..., description="Biomedical or cross-system medical question to investigate")
    systems: List[str] = Field(default=["modern", "unani", "ayurveda"], description="Target medical systems")
    budget_limit: int = Field(default=100, description="Maximum candidate sources to screen")
    execute_immediately: bool = Field(default=True, description="Whether to run the autonomous research loop immediately")


# Backward compatibility alias for legacy investigation callers and test showcases
ResearchRequest = CreateResearchRequest



class DiffRequest(BaseModel):
    base_snapshot_id: str
    target_snapshot_id: str


@router.post("", response_model=Dict[str, Any])
@router.post("/jobs", response_model=Dict[str, Any])
async def create_research_job(req: CreateResearchRequest):
    """
    POST /v1/research or /v1/research/jobs:
    Initiates a new research job, extracts PICO, builds pre-flight ResearchPlan,
    and optionally executes the autonomous multi-agent research loop.
    """
    try:
        job = await DeepResearchOperatingEngine.create_research_job(
            question=req.question,
            target_systems=req.systems,
            budget_limit=req.budget_limit
        )

        report = None
        if req.execute_immediately:
            report = await DeepResearchOperatingEngine.execute_investigation(job.job_id)

        return {
            "status": "success",
            "job_id": job.job_id,
            "state": job.state.value,
            "plan_id": job.plan.plan_id if job.plan else None,
            "report_id": report.report_id if report else None,
            "job": job.model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create research job: {str(e)}")


@router.get("/jobs", response_model=List[Dict[str, Any]])
async def list_research_jobs():
    """
    Lists all active or past research jobs.
    """
    jobs = DeepResearchOperatingEngine.list_jobs()
    return [j.model_dump() for j in jobs]


@router.post("/stream")
async def stream_research_investigation(req: CreateResearchRequest):
    """
    POST /v1/research/stream:
    Server-Sent Events (SSE) streaming endpoint for live research investigations.
    Yields stage-by-stage micro-telemetry and progressive narrative token streaming.
    """
    async def event_generator():
        try:
            yield f"data: {json.dumps({'type': 'stage', 'stage': 1, 'message': 'Stage 1: Formulating PICO parameters & extraction mesh'})}\n\n"
            await asyncio.sleep(0.06)

            job = await DeepResearchOperatingEngine.create_research_job(
                question=req.question,
                target_systems=req.systems,
                budget_limit=req.budget_limit
            )

            yield f"data: {json.dumps({'type': 'stage', 'stage': 2, 'message': 'Stage 2: Verifying against PubMed, Cochrane, and WHO registries'})}\n\n"
            await asyncio.sleep(0.06)

            yield f"data: {json.dumps({'type': 'stage', 'stage': 3, 'message': 'Stage 3: Calibrating Cochrane RoB 2.0 & Bayesian epistemic weights'})}\n\n"
            await asyncio.sleep(0.06)

            report = await DeepResearchOperatingEngine.execute_investigation(job.job_id)

            yield f"data: {json.dumps({'type': 'stage', 'stage': 4, 'message': 'Stage 4: Sealing SHA-256 Merkle Provenance Ledger'})}\n\n"
            await asyncio.sleep(0.05)

            # Progressive narrative word stream
            narrative = (report.narrative_synthesis or "Clinical evidence appraisal completed.") if report else ""
            words = narrative.split()
            for i in range(0, len(words), 3):
                chunk = words[i:i+3]
                yield f"data: {json.dumps({'type': 'token', 'text': ' '.join(chunk) + ' '})}\n\n"
                await asyncio.sleep(0.015)

            yield f"data: {json.dumps({'type': 'complete', 'job': job.model_dump(), 'report': report.model_dump() if report else None})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/alerts/check")
async def check_research_alerts(terms: str = Query(..., description="Comma-separated topics or terms to monitor")):
    """
    GET /v1/research/alerts/check:
    Checks NCBI PubMed database for recent research publications on monitored terms.
    Returns active alert updates for clinician notifications.
    """
    from app.sources.pubmed_client import NCBIPubMedClient
    client = NCBIPubMedClient()
    results = []
    term_list = [t.strip() for t in terms.split(",") if t.strip()]
    for term in term_list[:5]:
        articles = client.search_and_fetch(f"{term} [Title/Abstract]", max_results=3)
        results.append({
            "term": term,
            "count": len(articles),
            "latest_pmid": getattr(articles[0], 'pmid', None) if articles else None,
            "latest_title": getattr(articles[0], 'title', None) if articles else None,
            "latest_date": getattr(articles[0], 'pub_date', None) if articles else None,
            "has_new_evidence": len(articles) > 0
        })
    return {"status": "success", "alerts": results}


@router.get("/autocomplete")
async def get_mesh_autocomplete(q: str = Query(..., min_length=2)):
    """
    GET /v1/research/autocomplete:
    Returns matching Medical Subject Headings (MeSH) and verified botanical taxa.
    """
    TAXONOMY = [
        {"term": "Berberine", "type": "Botanical Alkaloid", "category": "botanical", "icon": "🌿", "hint": "AMPK activator, metabolic & glucose control"},
        {"term": "Metformin", "type": "Biguanide", "category": "drug", "icon": "💊", "hint": "First-line oral antihyperglycemic"},
        {"term": "Ashwagandha (Withania somnifera)", "type": "Adaptogen", "category": "botanical", "icon": "🌿", "hint": "Cortisol modulator, GABAergic anxiolytic"},
        {"term": "Warfarin", "type": "Anticoagulant", "category": "drug", "icon": "🩸", "hint": "Vitamin K antagonist (VKORC1)"},
        {"term": "Curcumin (Curcuma longa)", "type": "Polyphenol", "category": "botanical", "icon": "🌿", "hint": "NF-κB & COX-2 anti-inflammatory"},
        {"term": "Ginkgo biloba", "type": "Extract EGb 761", "category": "botanical", "icon": "🌿", "hint": "Platelet activating factor antagonist"},
        {"term": "St. John's Wort (Hypericum perforatum)", "type": "Phytomedicine", "category": "botanical", "icon": "🌿", "hint": "Potent CYP3A4 & P-gp inducer"},
        {"term": "Type 2 Diabetes Mellitus", "type": "Endocrine Condition", "category": "condition", "icon": "🩺", "hint": "MeSH D003924: Insulin resistance"},
        {"term": "Major Depressive Disorder", "type": "Psychiatric Condition", "category": "condition", "icon": "🩺", "hint": "MeSH D003866: Affective disorder"},
        {"term": "Atorvastatin", "type": "HMG-CoA Reductase", "category": "drug", "icon": "💊", "hint": "Lipid lowering, CYP3A4 substrate"},
        {"term": "Milk Thistle (Silymarin)", "type": "Hepatoprotective", "category": "botanical", "icon": "🌿", "hint": "Silybum marianum, membrane stabilizer"},
        {"term": "Coenzyme Q10 (Ubiquinone)", "type": "Antioxidant", "category": "supplement", "icon": "✨", "hint": "Mitochondrial electron transport chain"},
        {"term": "Omega-3 Fatty Acids (EPA/DHA)", "type": "Essential Lipid", "category": "supplement", "icon": "🐟", "hint": "Triglyceride lowering & cardio-protective"},
        {"term": "Digoxin", "type": "Cardiac Glycoside", "category": "drug", "icon": "🫀", "hint": "Narrow therapeutic index, P-gp substrate"}
    ]
    q_lower = q.lower()
    matches = [t for t in TAXONOMY if q_lower in t["term"].lower() or q_lower in t["type"].lower() or q_lower in t["hint"].lower()]
    return {"status": "success", "query": q, "results": matches}


@router.get("/{job_id}", response_model=Dict[str, Any])
async def get_research_job(job_id: str):
    """
    GET /v1/research/{job_id}:
    Retrieves high-level metadata and state for a specific research job.
    """
    job = DeepResearchOperatingEngine.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    return job.model_dump()


@router.get("/{job_id}/plan", response_model=Dict[str, Any])
async def get_research_plan(job_id: str):
    """
    GET /v1/research/{job_id}/plan:
    Returns the decomposed PICO framework, sub-questions, inclusion/exclusion criteria, and search matrix.
    """
    job = DeepResearchOperatingEngine.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    if not job.plan:
        raise HTTPException(status_code=404, detail=f"Plan for job {job_id} not generated yet")
    return job.plan.model_dump()


@router.get("/{job_id}/evidence", response_model=List[Dict[str, Any]])
async def get_research_evidence(job_id: str):
    """
    GET /v1/research/{job_id}/evidence:
    Returns the structured Evidence Table extracted during study screening.
    """
    job = DeepResearchOperatingEngine.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    return [e.model_dump() for e in job.evidence_table]


@router.get("/{job_id}/conflicts", response_model=List[Dict[str, Any]])
async def get_research_conflicts(job_id: str):
    """
    GET /v1/research/{job_id}/conflicts:
    Returns identified contradiction clusters and root-cause divergence analyses.
    """
    job = DeepResearchOperatingEngine.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    return [c.model_dump() for c in job.contradictions]


@router.get("/{job_id}/gaps", response_model=Dict[str, Any])
async def get_research_gaps(job_id: str):
    """
    GET /v1/research/{job_id}/gaps:
    Returns unaddressed clinical/pharmacological blindspots and next-best research questions.
    """
    job = DeepResearchOperatingEngine.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    return {
        "job_id": job_id,
        "gaps": [g.model_dump() for g in job.gaps],
        "next_best_questions": [q.model_dump() for q in job.next_questions]
    }


@router.get("/{job_id}/report", response_model=Dict[str, Any])
async def get_research_report(job_id: str):
    """
    GET /v1/research/{job_id}/report:
    Returns the comprehensive synthesized research report including narrative, assertions, and citation audits.
    """
    job = DeepResearchOperatingEngine.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    if not job.report:
        raise HTTPException(status_code=404, detail=f"Report for job {job_id} not compiled yet")
    return job.report.model_dump()


@router.post("/{job_id}/snapshot", response_model=Dict[str, Any])
async def create_job_snapshot(job_id: str):
    """
    POST /v1/research/{job_id}/snapshot:
    Captures an immutable snapshot checkpoint of the job.
    """
    try:
        snap = DeepResearchOperatingEngine.create_snapshot(job_id)
        return snap.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{job_id}/diff", response_model=Dict[str, Any])
async def diff_job_snapshots(job_id: str, diff_req: DiffRequest):
    """
    POST /v1/research/{job_id}/diff:
    Computes differences between two snapshots of the research job.
    """
    try:
        diff = DeepResearchOperatingEngine.compute_diff(
            job_id=job_id,
            base_snap_id=diff_req.base_snapshot_id,
            target_snap_id=diff_req.target_snapshot_id
        )
        return diff.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Backward compatibility endpoint for legacy investigation
@router.post("/investigate", response_model=DeepResearchReport)
async def start_deep_investigation(request: CreateResearchRequest):
    """
    Legacy compatibility investigation endpoint.
    """
    return await DeepResearchAgent.run_investigation(
        question=request.question,
        target_systems=request.systems
    )


class PRISMAGenerateRequest(BaseModel):
    pico_query: str = Field(..., description="PICO clinical query for systematic review generation")
    filters: Optional[Dict[str, Any]] = None


@router.post("/prisma-generator", response_model=Dict[str, Any])
async def generate_prisma_systematic_review(req: PRISMAGenerateRequest):
    """
    POST /v1/research/prisma-generator:
    Generates an automated PRISMA 2020 Statement compliant Systematic Review,
    RoB 2 Risk of Bias Matrix, and Inverse-Variance Meta-Analysis Forest Plot data.
    """
    from app.research.prisma_engine import PRISMA2020Engine
    report = PRISMA2020Engine.generate_review(pico_query=req.pico_query, filters=req.filters)
    return report.model_dump()


