"""
ZMIE Distributed Background Ingestion Tasks Acceptance Suite (Pillar 2)
Tests:
1. IngestionTaskManager task creation, lifecycle transitions, and batch SHA-256 hashing.
2. Background harvesting from PubMed/Europe PMC and PMC BioC XML.
3. License classification breakdown (Classes A, B, C).
4. REST API Endpoints:
   - POST /v1/ingestion/tasks/harvest
   - GET /v1/ingestion/tasks/{task_id}/status
   - GET /v1/ingestion/tasks/queue-stats
   - POST /v1/ingestion/tasks/daily-sync
"""

import unittest
import asyncio
from fastapi.testclient import TestClient

from app.main import app
from app.ingestion.tasks import ingestion_task_manager


class TestCeleryIngestionWorkerAcceptance(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_01_create_and_retrieve_task(self):
        """TaskManager correctly initializes a pending task record."""
        task = ingestion_task_manager.create_task(
            task_name="test_harvest",
            source_type="pubmed",
            query="curcumin gastrointestinal",
            total_requested=5
        )
        self.assertIsNotNone(task.task_id)
        self.assertEqual(task.status, "PENDING")
        self.assertEqual(task.source_type, "pubmed")

        fetched = ingestion_task_manager.get_task(task.task_id)
        self.assertEqual(fetched.task_id, task.task_id)

    def test_02_execute_harvest_job_lifecycle(self):
        """Executing harvest job transitions to COMPLETED and generates cryptographic batch hash."""
        task = ingestion_task_manager.create_task(
            task_name="test_execution",
            source_type="pubmed",
            query="berberine glucose ampk",
            total_requested=2
        )

        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(ingestion_task_manager.execute_harvest_job(task.task_id))
        finally:
            loop.close()

        updated = ingestion_task_manager.get_task(task.task_id)
        self.assertEqual(updated.status, "COMPLETED")
        self.assertGreater(updated.items_processed, 0)
        self.assertIsNotNone(updated.batch_sha256)
        self.assertEqual(len(updated.batch_sha256), 64) # SHA-256 length
        self.assertIn("CLASS_B", updated.license_distribution)

    def test_03_rest_api_trigger_harvest(self):
        """POST /v1/ingestion/tasks/harvest schedules a background ingestion job."""
        resp = self.client.post(
            "/v1/ingestion/tasks/harvest",
            json={
                "query": "ashwagandha stress adaptogen",
                "source_type": "pubmed",
                "max_records": 3
            }
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("task_id", data)
        self.assertEqual(data["source_type"], "pubmed")
        self.assertIn(data["status"], ("PENDING", "RUNNING", "COMPLETED"))

    def test_04_rest_api_get_task_status(self):
        """GET /v1/ingestion/tasks/{task_id}/status returns task progress."""
        task = ingestion_task_manager.create_task(
            task_name="status_test",
            source_type="pmc",
            query="PMC3285145",
            total_requested=1
        )
        # Run job
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(ingestion_task_manager.execute_harvest_job(task.task_id))
        finally:
            loop.close()

        resp = self.client.get(f"/v1/ingestion/tasks/{task.task_id}/status")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["task_id"], task.task_id)
        self.assertEqual(data["status"], "COMPLETED")
        self.assertEqual(data["items_processed"], 1)

    def test_05_rest_api_queue_stats(self):
        """GET /v1/ingestion/tasks/queue-stats returns queue health and counts."""
        resp = self.client.get("/v1/ingestion/tasks/queue-stats")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("worker_engine_mode", data)
        self.assertIn("completed_tasks_count", data)
        self.assertGreaterEqual(data["completed_tasks_count"], 0)

    def test_06_rest_api_daily_sync(self):
        """POST /v1/ingestion/tasks/daily-sync triggers scheduled open access sync."""
        resp = self.client.post("/v1/ingestion/tasks/daily-sync")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["task_name"], "daily_open_access_sync")
        self.assertIn("task_id", data)

    def test_07_rest_api_task_not_found(self):
        """GET /v1/ingestion/tasks/invalid-id returns 404."""
        resp = self.client.get("/v1/ingestion/tasks/nonexistent-id-9999/status")
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
