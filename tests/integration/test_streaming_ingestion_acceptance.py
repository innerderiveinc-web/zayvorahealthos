"""
ZMIE Biomedical Streaming Ingestion Acceptance Tests
Validates real-time concurrent multi-source streaming, cross-registry deduplication,
and fail-closed integrity across PubMed, Europe PMC, ClinicalTrials.gov, and OpenAlex.
"""

import unittest
import asyncio
from fastapi.testclient import TestClient

from app.main import app
from app.ingestion.streaming import BiomedicalStreamingIngestionEngine


class TestStreamingIngestionAcceptance(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.engine = BiomedicalStreamingIngestionEngine()

    def test_01_streaming_ingestion_event_flow(self):
        """Verifies that the async generator emits structured pipeline events."""
        async def run_stream():
            events = []
            async for ev in self.engine.stream_ingest("berberine diabetes", max_records_per_source=2):
                events.append(ev)
            return events

        events = asyncio.run(run_stream())
        self.assertGreater(len(events), 2)

        # 1. First event must be PIPELINE_INIT
        self.assertEqual(events[0]["event_type"], "PIPELINE_INIT")
        self.assertIn("PubMed", events[0]["payload"]["sources"])

        # 2. Last event must be PIPELINE_COMPLETE
        self.assertEqual(events[-1]["event_type"], "PIPELINE_COMPLETE")
        self.assertIn("duration_ms", events[-1]["payload"])
        self.assertEqual(events[-1]["payload"]["audit_integrity"], "VALID")

        # 3. Verify recorded records
        record_events = [e for e in events if e["event_type"] == "RECORD_INGESTED"]
        self.assertGreater(len(record_events), 0)
        first_rec = record_events[0]["payload"]["record"]
        self.assertTrue("title" in first_rec)

    def test_02_cross_registry_deduplication(self):
        """Ensures that records with identical DOI or PMID are deduplicated across sources."""
        async def run_stream():
            events = []
            async for ev in self.engine.stream_ingest("metabolic glucose", max_records_per_source=3):
                events.append(ev)
            return events

        events = asyncio.run(run_stream())
        keys = set()
        for ev in events:
            if ev["event_type"] == "RECORD_INGESTED":
                k = ev["payload"]["dedup_key"]
                self.assertNotIn(k, keys, f"Duplicate key {k} was emitted as new record!")
                keys.add(k)

    def test_03_harvest_endpoint_rest_contract(self):
        """Validates synchronous aggregation POST /v1/ingestion/harvest endpoint."""
        resp = self.client.post(
            "/v1/ingestion/harvest",
            json={"query": "berberine", "max_records_per_source": 2}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["query"], "berberine")
        self.assertGreaterEqual(data["total_records"], 1)
        self.assertIn("deduplication_ratio", data)
        self.assertIn("records", data)

    def test_04_sse_stream_endpoint(self):
        """Validates Server-Sent Events GET /v1/ingestion/stream endpoint."""
        resp = self.client.get("/v1/ingestion/stream?query=ashwagandha&max_per_source=2")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/event-stream", resp.headers["content-type"])
        body = resp.text
        self.assertIn("data: {", body)
        self.assertIn("PIPELINE_INIT", body)
        self.assertIn("PIPELINE_COMPLETE", body)

    def test_05_fail_closed_zero_fabrication(self):
        """Validates that arbitrary nonsense query terms return 0 fabricated records."""
        async def run_stream():
            events = []
            async for ev in self.engine.stream_ingest("xyzzz_completely_fictional_unobtainium_molecule", max_records_per_source=3):
                events.append(ev)
            return events

        events = asyncio.run(run_stream())
        record_events = [e for e in events if e["event_type"] == "RECORD_INGESTED"]
        self.assertEqual(len(record_events), 0, "Engine fabricated records for non-existent scientific query!")
        self.assertEqual(events[-1]["payload"]["total_unique_records"], 0)


if __name__ == "__main__":
    unittest.main()
