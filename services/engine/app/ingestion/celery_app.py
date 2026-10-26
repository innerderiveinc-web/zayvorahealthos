"""
ZMIE Enterprise Distributed Ingestion Worker & Celery Configuration (Pillar 2)
Provides asynchronous background task orchestration for massive PubMed, PMC,
and Unpaywall harvesting pipelines.
"""

import os
from typing import Dict, Any

# Celery import with safe fallback for lightweight runtime environments
try:
    from celery import Celery
    CELERY_AVAILABLE = True
except ImportError:
    Celery = None
    CELERY_AVAILABLE = False


REDIS_URL = os.getenv("REDIS_URL", os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"))

if CELERY_AVAILABLE:
    celery_app = Celery(
        "zmie_ingestion",
        broker=REDIS_URL,
        backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1"),
        include=["app.ingestion.tasks"]
    )

    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_acks_late=True,
        worker_prefetch_multiplier=1,
        task_routes={
            "app.ingestion.tasks.task_harvest_pubmed": {"queue": "pubmed_harvest"},
            "app.ingestion.tasks.task_harvest_unpaywall_batch": {"queue": "unpaywall_resolve"},
            "app.ingestion.tasks.task_daily_open_access_sync": {"queue": "scheduled_sync"}
        }
    )
else:
    celery_app = None
