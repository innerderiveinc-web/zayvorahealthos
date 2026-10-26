"""
ZMIE Distributed Background Ingestion Tasks (Pillar 2)
Executes large-scale automated harvesting of PubMed, PMC BioC XML,
and Unpaywall Open Access papers with cryptographic provenance tracking.
Supports dual-mode execution:
1. Distributed Celery + Redis workers in cloud enterprise environments.
2. Async In-Memory Task Manager when operating in zero-dependency edge mode.
"""

import asyncio
import hashlib
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from app.ingestion.connectors.europe_pmc import EuropePMCConnector
from app.ingestion.connectors.pmc_fulltext import PMCFullTextConnector
from app.ingestion.connectors.unpaywall import UnpaywallConnector
from app.models.source import LicenseClass


class IngestionTaskRecord(BaseModel):
    task_id: str
    task_name: str
    status: str # PENDING, RUNNING, COMPLETED, FAILED
    source_type: str
    query: str
    total_requested: int
    items_processed: int
    license_distribution: Dict[str, int]
    batch_sha256: str
    started_at: str
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    records: List[Dict[str, Any]] = []


class IngestionTaskManager:
    """
    Manages in-memory task states and provides dual-mode execution.
    """
    _instance = None
    _tasks: Dict[str, IngestionTaskRecord] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IngestionTaskManager, cls).__new__(cls)
            cls._instance._tasks = {}
        return cls._instance

    def create_task(self, task_name: str, source_type: str, query: str, total_requested: int) -> IngestionTaskRecord:
        task_id = f"task-ingest-{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc).isoformat()
        rec = IngestionTaskRecord(
            task_id=task_id,
            task_name=task_name,
            status="PENDING",
            source_type=source_type,
            query=query,
            total_requested=total_requested,
            items_processed=0,
            license_distribution={"CLASS_A": 0, "CLASS_B": 0, "CLASS_C": 0},
            batch_sha256="",
            started_at=now,
            records=[]
        )
        self._tasks[task_id] = rec
        return rec

    def get_task(self, task_id: str) -> Optional[IngestionTaskRecord]:
        return self._tasks.get(task_id)

    def list_tasks(self, limit: int = 20) -> List[IngestionTaskRecord]:
        return list(self._tasks.values())[-limit:]

    async def execute_harvest_job(self, task_id: str):
        task = self.get_task(task_id)
        if not task:
            return

        task.status = "RUNNING"
        processed_records = []
        hasher = hashlib.sha256()

        try:
            if task.source_type.lower() in ("pmc", "pubmed_central", "bioc"):
                connector = PMCFullTextConnector()
                results = await connector.discover(task.query, limit=task.total_requested)
            elif task.source_type.lower() == "unpaywall":
                connector = UnpaywallConnector()
                results = await connector.discover(task.query, limit=task.total_requested)
            else: # Default to Europe PMC / PubMed
                connector = EuropePMCConnector()
                results = await connector.discover(task.query, limit=task.total_requested)

            for item in results:
                lic = item.get("license_class", LicenseClass.CLASS_C.value)
                if lic == LicenseClass.CLASS_A.value:
                    task.license_distribution["CLASS_A"] += 1
                elif lic == LicenseClass.CLASS_B.value:
                    task.license_distribution["CLASS_B"] += 1
                else:
                    task.license_distribution["CLASS_C"] += 1

                hasher.update(str(item.get("document_id", "")).encode("utf-8"))
                processed_records.append({
                    "document_id": item.get("document_id"),
                    "title": item.get("title"),
                    "publication_year": item.get("publication_year"),
                    "license_class": lic
                })

            task.items_processed = len(processed_records)
            task.records = processed_records
            task.batch_sha256 = hasher.hexdigest()
            task.status = "COMPLETED"
            task.completed_at = datetime.now(timezone.utc).isoformat()
        except Exception as e:
            task.status = "FAILED"
            task.error_message = str(e)
            task.completed_at = datetime.now(timezone.utc).isoformat()


# Global Singleton Manager
ingestion_task_manager = IngestionTaskManager()


# Celery Task Bindings (Used when worker runs via `celery -A app.ingestion.celery_app worker`)
try:
    from app.ingestion.celery_app import celery_app, CELERY_AVAILABLE
    if CELERY_AVAILABLE and celery_app:
        @celery_app.task(name="app.ingestion.tasks.task_harvest_pubmed", bind=True)
        def task_harvest_pubmed(self, query: str, max_records: int = 50):
            task_rec = ingestion_task_manager.create_task("pubmed_harvest", "pubmed", query, max_records)
            asyncio.run(ingestion_task_manager.execute_harvest_job(task_rec.task_id))
            return task_rec.dict()

        @celery_app.task(name="app.ingestion.tasks.task_harvest_unpaywall_batch", bind=True)
        def task_harvest_unpaywall_batch(self, query: str, max_records: int = 50):
            task_rec = ingestion_task_manager.create_task("unpaywall_resolve", "unpaywall", query, max_records)
            asyncio.run(ingestion_task_manager.execute_harvest_job(task_rec.task_id))
            return task_rec.dict()

        @celery_app.task(name="app.ingestion.tasks.task_daily_open_access_sync", bind=True)
        def task_daily_open_access_sync(self):
            task_rec = ingestion_task_manager.create_task("daily_oa_sync", "pubmed", "clinical trials botanical", 100)
            asyncio.run(ingestion_task_manager.execute_harvest_job(task_rec.task_id))
            return task_rec.dict()
except Exception:
    pass
