"""
ZMIE Automated Ingestion Tasks REST API Router (Pillar 2)
Provides endpoints for initiating background automated harvesting jobs from
Europe PMC, PubMed Central BioC XML, and Unpaywall.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel, Field

from app.ingestion.tasks import ingestion_task_manager, IngestionTaskRecord
from app.ingestion.celery_app import CELERY_AVAILABLE, REDIS_URL

router = APIRouter(prefix="/ingestion/tasks", tags=["Distributed Automated Ingestion Tasks"])


class HarvestTaskRequest(BaseModel):
    query: str = Field(..., description="Query terms or MeSH headings to harvest")
    source_type: str = Field("pubmed", description="Target source: pubmed, pmc, unpaywall")
    max_records: int = Field(20, ge=1, le=1000, description="Maximum records to harvest")


class QueueStatsResponse(BaseModel):
    celery_available: bool
    broker_url: str
    active_tasks_count: int
    completed_tasks_count: int
    failed_tasks_count: int
    worker_engine_mode: str


@router.post("/harvest", response_model=IngestionTaskRecord)
async def trigger_harvest_task(req: HarvestTaskRequest, background_tasks: BackgroundTasks):
    """
    Triggers an asynchronous background ingestion job to harvest literature from external registries.
    Uses distributed Celery workers when available, or FastAPI async worker.
    """
    task_rec = ingestion_task_manager.create_task(
        task_name=f"{req.source_type}_harvest",
        source_type=req.source_type,
        query=req.query,
        total_requested=req.max_records
    )

    # Queue background processing
    background_tasks.add_task(ingestion_task_manager.execute_harvest_job, task_rec.task_id)

    return task_rec


@router.get("/queue-stats", response_model=QueueStatsResponse)
async def get_queue_stats():
    """
    Returns telemetry on background queues, worker modes, and completed job counts.
    """
    tasks = ingestion_task_manager.list_tasks(limit=1000)
    active = sum(1 for t in tasks if t.status in ("PENDING", "RUNNING"))
    completed = sum(1 for t in tasks if t.status == "COMPLETED")
    failed = sum(1 for t in tasks if t.status == "FAILED")

    return QueueStatsResponse(
        celery_available=CELERY_AVAILABLE,
        broker_url=REDIS_URL.split("@")[-1] if "@" in REDIS_URL else REDIS_URL,
        active_tasks_count=active,
        completed_tasks_count=completed,
        failed_tasks_count=failed,
        worker_engine_mode="Distributed Celery + Redis" if CELERY_AVAILABLE else "Async In-Process Task Engine"
    )


@router.get("/{task_id}/status", response_model=IngestionTaskRecord)
async def get_task_status(task_id: str):
    """
    Polls real-time execution status, licensing classification, and cryptographic batch hash.
    """
    task = ingestion_task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Ingestion task '{task_id}' not found.")
    return task


@router.post("/daily-sync", response_model=IngestionTaskRecord)
async def trigger_daily_open_access_sync(background_tasks: BackgroundTasks):
    """
    Triggers scheduled synchronization of daily open access medical publications.
    """
    task_rec = ingestion_task_manager.create_task(
        task_name="daily_open_access_sync",
        source_type="pubmed",
        query="randomized controlled trial botanical clinical evidence",
        total_requested=50
    )
    background_tasks.add_task(ingestion_task_manager.execute_harvest_job, task_rec.task_id)
    return task_rec
