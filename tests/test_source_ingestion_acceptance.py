"""
ZMIE Source Acquisition, Licensing & Ingestion Master Acceptance Suite
Validates the full enterprise source acquisition infrastructure:
1. BaseSourceConnector contract adherence
2. OpenAlex, Europe PMC, AYUSH, and ClinicalTrials.gov adapters
3. Class A/B/C Licensing rights matrix & quarantine enforcement
4. Cryptographic SHA-256 hashing & structural section anchors
5. 14-Stage Ingestion Job Lifecycle execution
6. Immutable document versioning & supersession preservation
7. Source health monitoring, error budgets & fleet telemetry
"""

import sys
import unittest
import asyncio
from datetime import datetime

from app.models.source import AuthorityTier, LicenseClass, SourceStatus
from app.models.claim import MedicalSystem, EvidenceGrade
from app.ingestion.connectors.base import BaseSourceConnector
from app.ingestion.connectors.openalex import OpenAlexConnector
from app.ingestion.connectors.europe_pmc import EuropePMCConnector
from app.ingestion.connectors.ayush import AYUSHResearchConnector
from app.ingestion.connectors.clinical_trials import ClinicalTrialsConnector
from app.ingestion.licensing import LicensingIntelligenceEngine
from app.ingestion.parser import DocumentParserService
from app.ingestion.job_runner import IngestionJobRunner, JobStatus, IngestionStage
from app.ingestion.versioning import DocumentVersionTracker, ChangeType
from app.ingestion.health import SourceHealthMonitor, SourceHealthStatus


class TestSourceIngestionAcceptance(unittest.TestCase):

    def test_01_connector_contract_adherence(self):
        """Verifies that all connectors implement BaseSourceConnector contracts."""
        connectors = [
            OpenAlexConnector(),
            EuropePMCConnector(),
            AYUSHResearchConnector(),
            ClinicalTrialsConnector()
        ]
        for conn in connectors:
            self.assertIsInstance(conn, BaseSourceConnector)
            self.assertTrue(hasattr(conn, "discover"))
            self.assertTrue(hasattr(conn, "identify"))
            self.assertTrue(hasattr(conn, "fetch_metadata"))
            self.assertTrue(hasattr(conn, "fetch_document"))
            self.assertTrue(hasattr(conn, "fetch_updates"))
            self.assertTrue(hasattr(conn, "normalize"))
            self.assertTrue(hasattr(conn, "report_status"))
            status = conn.report_status()
            self.assertIn("source_id", status)
            self.assertIn("authority_tier", status)

    def test_02_clinical_trials_connector_normalization(self):
        """Validates ClinicalTrialsConnector extracts PICO structure from registry record."""
        connector = ClinicalTrialsConnector()
        sample_study = {
            "protocolSection": {
                "identificationModule": {
                    "nctId": "NCT09912345",
                    "briefTitle": "Phase 2 Evaluation of Herbal Extract in Type 2 Diabetes",
                    "officialTitle": "Randomized Double-Blind Trial"
                },
                "statusModule": {
                    "overallStatus": "RECRUITING",
                    "studyFirstSubmitDate": "2024-01-15"
                },
                "designModule": {
                    "phases": ["PHASE2"]
                },
                "armsInterventionsModule": {
                    "interventions": [{"type": "DRUG", "name": "Standardized Extract 500mg"}]
                },
                "outcomesModule": {
                    "primaryOutcomes": [{"measure": "HbA1c Reduction", "timeFrame": "12 weeks"}]
                },
                "conditionsModule": {
                    "conditions": ["Type 2 Diabetes Mellitus"]
                }
            }
        }
        normalized = connector.normalize(sample_study)
        self.assertEqual(normalized["trial_id"], "NCT09912345")
        self.assertEqual(normalized["status"], "RECRUITING")
        self.assertEqual(normalized["phase"], "PHASE2")
        self.assertEqual(normalized["license_class"], LicenseClass.CLASS_B.value)
        self.assertIn("DRUG: Standardized Extract 500mg", normalized["interventions"])
        self.assertIn("Type 2 Diabetes Mellitus", normalized["conditions"])

    def test_03_licensing_quarantine_enforcement(self):
        """Ensures Class C documents have raw full-text quarantined and only permitted metadata retained."""
        raw_doc = {
            "title": "Closed Access Journal Study",
            "doi": "10.1016/j.cell.2025.01.001",
            "abstract": "Permitted brief summary of empirical findings.",
            "full_text": "RESTRICTED PROPRIETARY FULL TEXT THAT MUST NEVER BE STORED",
            "sections": ["Full Section 1", "Full Section 2"],
            "license_class": LicenseClass.CLASS_C.value
        }
        filtered = LicensingIntelligenceEngine.filter_storage_payload(raw_doc, LicenseClass.CLASS_C)
        self.assertIsNone(filtered["full_text"])
        self.assertEqual(filtered["sections"], [])
        self.assertEqual(filtered["abstract"], "Permitted brief summary of empirical findings.")
        self.assertIn("Class C", filtered["notice"])

    def test_04_document_parser_and_cryptographic_anchors(self):
        """Validates SHA-256 hash generation and section/paragraph decomposition."""
        content = "SECTION ONE: INTRODUCTION\nThis is paragraph one.\nThis is paragraph two.\nSECTION TWO: METHODS\nThis is paragraph three."
        artifact = DocumentParserService.parse_raw_text(
            document_id="DOC-TEST-001",
            title="Study on Phytochemistry",
            raw_content=content,
            license_str="cc-by-4.0",
            is_oa=True
        )
        self.assertEqual(len(artifact.raw_hash_sha256), 64) # Valid 256-bit hex hash
        self.assertFalse(artifact.is_full_text_quarantined)
        self.assertGreater(artifact.total_paragraphs, 0)

    def test_05_document_versioning_and_supersession(self):
        """Validates version progression: NEW -> UNCHANGED -> SUPERSEDED -> RETRACTED."""
        tracker = DocumentVersionTracker()
        doc_id = "GUIDELINE-WHO-HYPERTENSION"

        # 1. Initial Guideline v1.0
        v1 = tracker.register_version(doc_id, "2020 WHO Hypertension Guidelines: Threshold 140/90", published_version="2020.1")
        self.assertEqual(v1.change_type, ChangeType.NEW)
        self.assertEqual(v1.version_index, 1)

        # 2. Identical re-fetch
        v2 = tracker.register_version(doc_id, "2020 WHO Hypertension Guidelines: Threshold 140/90", published_version="2020.1")
        self.assertEqual(v2.change_type, ChangeType.UNCHANGED)

        # 3. New Guideline Supersedes Older
        v3 = tracker.register_version(doc_id, "2024 WHO Hypertension Guidelines: Threshold 130/80", published_version="2024.1")
        self.assertEqual(v3.change_type, ChangeType.UPDATED)
        self.assertEqual(v3.supersedes, v2.version_id)
        
        # Verify previous version marked as superseded
        history = tracker.get_history(doc_id)
        self.assertEqual(history[1].change_type, ChangeType.SUPERSEDED)

        # 4. Retraction Quarantine
        v4 = tracker.register_version(doc_id, "Retracted text", published_version="2024.1", is_retracted=True, retraction_reason="Data falsification")
        self.assertEqual(v4.change_type, ChangeType.RETRACTED)
        self.assertTrue(v4.is_retracted)

    def test_06_source_health_monitor_and_error_budget(self):
        """Validates health state changes from HEALTHY to DEGRADED and BLOCKED."""
        monitor = SourceHealthMonitor()

        # Healthy
        h1 = monitor.record_heartbeat("SRC-1", "Source Normal", latency_ms=120.0, errors=0, total_requests=100)
        self.assertEqual(h1.status, SourceHealthStatus.HEALTHY)

        # Degraded (high latency)
        h2 = monitor.record_heartbeat("SRC-2", "Source Slow", latency_ms=2500.0, errors=2, total_requests=100)
        self.assertEqual(h2.status, SourceHealthStatus.DEGRADED)

        # Blocked (rate limit exhausted)
        h3 = monitor.record_heartbeat("SRC-3", "Source Exhausted", latency_ms=100.0, errors=10, total_requests=100, rate_limit_remaining=0)
        self.assertEqual(h3.status, SourceHealthStatus.BLOCKED)

        fleet = monitor.get_fleet_report()
        self.assertEqual(fleet["total_monitored_sources"], 3)
        self.assertEqual(fleet["healthy_count"], 1)
        self.assertEqual(fleet["degraded_count"], 1)
        self.assertEqual(fleet["blocked_count"], 1)

    def test_07_ingestion_job_runner_lifecycle(self):
        """Executes full 14-stage ingestion job runner."""
        runner = IngestionJobRunner()
        job = asyncio.run(runner.execute_job(query="diabetes", max_records_per_source=2))
        self.assertEqual(job.status, JobStatus.COMPLETED)
        self.assertGreater(job.metrics.records_acquired, 0)
        self.assertGreater(job.metrics.claims_extracted, 0)
        self.assertIsNotNone(job.completed_at)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSourceIngestionAcceptance)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
