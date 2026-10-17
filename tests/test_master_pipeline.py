"""
Unit and Acceptance Tests for ZMIE Master Knowledge Evolution Pipeline
Validating: Source -> Research -> Data -> Mechanism/Causality -> Living Evidence -> Knowledge Evolution.
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.research.master_pipeline import MasterKnowledgeEvolutionPipeline


class TestMasterKnowledgeEvolutionPipeline(unittest.TestCase):

    def setUp(self):
        self.pipeline = MasterKnowledgeEvolutionPipeline()
        self.client = TestClient(app)

    def test_run_master_pipeline_end_to_end(self):
        res = self.pipeline.run_pipeline(topic="SGLT2_HEART_FAILURE")
        self.assertIsNotNone(res)
        self.assertIn("pipeline_run_id", res)
        self.assertEqual(len(res["unbroken_chain"]), 6)

        stages = [s["stage"] for s in res["unbroken_chain"]]
        self.assertEqual(stages, [
            "1_SOURCE",
            "2_RESEARCH",
            "3_DATA",
            "4_MECHANISM_CAUSALITY",
            "5_LIVING_EVIDENCE",
            "6_KNOWLEDGE_EVOLUTION"
        ])

        # Stage 1 Source
        s1 = res["unbroken_chain"][0]
        self.assertEqual(s1["status"], "ACQUIRED_AND_GOVERNED")

        # Stage 2 Research
        s2 = res["unbroken_chain"][1]
        self.assertEqual(s2["status"], "STUDY_FAMILIES_LINKED")
        self.assertGreaterEqual(len(s2["canonical_study_families"]), 3)

        # Stage 3 Data
        s3 = res["unbroken_chain"][2]
        self.assertEqual(s3["status"], "HARMONIZED_AND_FEDERATED")
        self.assertIn("OMOP CDM v5.4", s3["standards_supported"])

        # Stage 4 Mechanism / Causality
        s4 = res["unbroken_chain"][3]
        self.assertEqual(s4["status"], "VALIDATED_WITH_FIREWALL")
        self.assertEqual(s4["causality_firewall"]["identification_status"], "IDENTIFIED")
        self.assertFalse(s4["causality_firewall"]["collider_stratification_detected"])

        # Stage 5 Living Evidence
        s5 = res["unbroken_chain"][4]
        self.assertEqual(s5["status"], "SYNTHESIS_UPDATED_TO_v2")
        self.assertEqual(s5["trials_pooled_count"], 3)
        self.assertEqual(s5["grade_certainty"], "HIGH")

        # Stage 6 Knowledge Evolution
        s6 = res["unbroken_chain"][5]
        self.assertEqual(s6["status"], "CLAIMS_REVALIDATED_AND_COMMITTED")

    def test_api_endpoint_master_pipeline(self):
        response = self.client.post("/v1/research-network/pipeline/master?topic=SGLT2_HEART_FAILURE")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("unbroken_chain", data)
        self.assertEqual(len(data["unbroken_chain"]), 6)


if __name__ == "__main__":
    unittest.main()
