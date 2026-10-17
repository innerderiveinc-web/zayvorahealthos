"""ZMIE Scientific Data Fabric & Computational Research Engine API Router.

Endpoints for:
- Data Fabric Ingestion & Profiling
- Immutable Dataset Snapshots
- Analysis Planning & Data Leakage Checks
- Reproducible Computational Execution (Statistical modeling, strictly COMPUTED state)
- Reproducibility Engine & Computational Certificates
- Computation Diffing (Run A vs Run B)
- End-to-End Data Lineage Tracing
- Human-Gated Candidate Claim Evidence Promotion
- License Verification
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.models.scientific_compute import (
    AnalysisPlan,
    CandidateClaim,
    ComputationDiff,
    ComputationJob,
    ComputationalCertificate,
    DataLineageGraph,
    DataQualityReport,
    Dataset,
    DatasetSnapshot,
)
from app.scientific_compute.engine import ScientificDataFabricEngine

router = APIRouter(prefix="/compute", tags=["Scientific Data Fabric & Computational Engine"])

_engine_instance = ScientificDataFabricEngine()


def get_engine() -> ScientificDataFabricEngine:
    return _engine_instance


# -------------------------------------------------------------
# Request Schemas
# -------------------------------------------------------------

class RunWorkflowRequest(BaseModel):
    plan_id: str
    snapshot_id: str
    custom_parameters: Optional[Dict[str, Any]] = None


class GenerateClaimRequest(BaseModel):
    artifact_id: str


class PromoteClaimRequest(BaseModel):
    claim_id: str
    reviewer_name: str
    approve: bool = True


# -------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------

@router.post("/datasets/ingest")
async def ingest_scientific_dataset(
    dataset: Dataset,
    engine: ScientificDataFabricEngine = Depends(get_engine),
):
    """Ingests dataset into data fabric and returns quality profile assessment."""
    ds, report = engine.ingest_dataset(dataset)
    return {
        "dataset": ds,
        "quality_report": report,
    }


@router.get("/datasets/{dataset_id}", response_model=Dataset)
async def get_dataset(
    dataset_id: str,
    engine: ScientificDataFabricEngine = Depends(get_engine),
):
    """Retrieves dataset schema, fields, and privacy classification."""
    ds = engine._datasets.get(dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found.")
    return ds


@router.post("/datasets/{dataset_id}/snapshot", response_model=DatasetSnapshot)
async def create_dataset_snapshot(
    dataset_id: str,
    version_tag: str = Query("v1.0", description="Version tag for snapshot"),
    engine: ScientificDataFabricEngine = Depends(get_engine),
):
    """Creates an immutable, pinned cryptographic snapshot for scientific reproducibility."""
    try:
        return engine.create_snapshot(dataset_id, version_tag)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/analyses/plan", response_model=AnalysisPlan)
async def register_analysis_plan(
    plan: AnalysisPlan,
    engine: ScientificDataFabricEngine = Depends(get_engine),
):
    """Registers a preregistered computational analysis protocol with data leakage checking."""
    return engine.register_analysis_plan(plan)


@router.post("/workflows/run", response_model=ComputationJob)
async def execute_computational_workflow(
    req: RunWorkflowRequest,
    engine: ScientificDataFabricEngine = Depends(get_engine),
):
    """Executes a containerized statistical modeling run. Output is strictly tagged COMPUTED."""
    try:
        return engine.execute_analysis_workflow(
            plan_id=req.plan_id,
            snapshot_id=req.snapshot_id,
            custom_parameters=req.custom_parameters,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/runs/{run_id}", response_model=ComputationJob)
async def get_computation_run(
    run_id: str,
    engine: ScientificDataFabricEngine = Depends(get_engine),
):
    """Retrieves computational run details, effect estimates, and execution logs."""
    job = engine._jobs.get(run_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Computation run {run_id} not found.")
    return job


@router.post("/runs/{run_id}/reproduce")
async def reproduce_computation_run(
    run_id: str,
    engine: ScientificDataFabricEngine = Depends(get_engine),
):
    """Re-executes identical run from immutable snapshot and issues a signed ComputationalCertificate."""
    try:
        reproduced_job, cert = engine.reproduce_run(run_id)
        return {
            "reproduced_job": reproduced_job,
            "certificate": cert,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/runs/diff", response_model=ComputationDiff)
async def get_computation_diff(
    run_a: str = Query(..., description="Run ID A"),
    run_b: str = Query(..., description="Run ID B"),
    engine: ScientificDataFabricEngine = Depends(get_engine),
):
    """Calculates exact differences between two runs across data, code, parameters, and findings."""
    try:
        return engine.compute_diff(run_a, run_b)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/lineage/{run_id}", response_model=DataLineageGraph)
async def get_data_lineage_graph(
    run_id: str,
    engine: ScientificDataFabricEngine = Depends(get_engine),
):
    """Traces complete end-to-end directed lineage graph from raw data source to effect estimate."""
    try:
        return engine.trace_data_lineage(run_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/claims/candidate", response_model=CandidateClaim)
async def generate_candidate_claim(
    req: GenerateClaimRequest,
    engine: ScientificDataFabricEngine = Depends(get_engine),
):
    """Constructs a candidate scientific claim from computational output. Gated by human review."""
    try:
        return engine.generate_candidate_claim(req.artifact_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/claims/promote", response_model=CandidateClaim)
async def review_and_promote_claim(
    req: PromoteClaimRequest,
    engine: ScientificDataFabricEngine = Depends(get_engine),
):
    """Human expert review action promoting or rejecting claim for Evidence Graph integration."""
    try:
        return engine.review_and_promote_claim(req.claim_id, req.reviewer_name, req.approve)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/licenses/verify")
async def verify_dataset_license(
    dataset_id: str = Query(..., description="Dataset ID to check license"),
    engine: ScientificDataFabricEngine = Depends(get_engine),
):
    """Verifies intellectual property and data usage agreements before data export."""
    allowed, reason = engine.verify_dataset_export_permission(dataset_id)
    return {
        "dataset_id": dataset_id,
        "export_allowed": allowed,
        "policy_message": reason,
    }
