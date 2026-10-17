"""
ZMIE Official Python SDK Comprehensive Acceptance Tests
Verifies both legacy client contracts and enterprise namespaces (Prompts 1-27).
"""

import unittest
from zmie import ZMIEClient as EnterpriseClient
from zmie_sdk import ZMIEClient as LegacyClient
from app.main import app


class TestSDKComprehensive(unittest.TestCase):

    def test_legacy_sdk_initialization_and_shapes(self):
        client = LegacyClient(base_url="http://localhost:8000", api_key="test-key")
        self.assertEqual(client.base_url, "http://localhost:8000")
        self.assertEqual(client.headers["Authorization"], "Bearer test-key")
        self.assertTrue(hasattr(client, "search"))
        self.assertTrue(hasattr(client, "audit_claim"))
        self.assertTrue(hasattr(client, "deep_investigation"))
        self.assertTrue(hasattr(client, "evaluate_safety"))
        self.assertTrue(hasattr(client, "compare_systems"))

    def test_enterprise_sdk_all_prompt_namespaces(self):
        """Verifies that the enterprise ZMIEClient exposes first-class namespaces for all Prompts 1-27."""
        client = EnterpriseClient(api_key="zmie-adm-key-0001", app_instance=app)

        # Core search & intelligence methods (Prompts 1-12)
        self.assertTrue(hasattr(client, "rag_context"))
        self.assertTrue(hasattr(client, "intelligence_query"))
        self.assertTrue(hasattr(client, "search"))
        self.assertTrue(hasattr(client, "check_safety"))

        # Prompt 13: Global Source Universe
        self.assertTrue(hasattr(client, "sources"))
        sources_list = client.sources.list()
        self.assertIsInstance(sources_list, list)

        # Prompt 14: Research Discovery Network
        self.assertTrue(hasattr(client, "research_network"))
        gaps = client.research_network.gaps()
        self.assertIsInstance(gaps, list)

        # Prompt 15: RWE & Interoperability
        self.assertTrue(hasattr(client, "rwe"))
        rwe_sources = client.rwe.list_sources()
        self.assertIsInstance(rwe_sources, list)

        # Prompt 16: Causal & Mechanistic Intelligence
        self.assertTrue(hasattr(client, "causal"))
        self.assertTrue(callable(client.causal.decompose_mechanism))

        # Prompt 17: Living Evidence Synthesis
        self.assertTrue(hasattr(client, "living_evidence"))
        reviews = client.living_evidence.list()
        self.assertIsInstance(reviews, list)

        # Prompt 18: Clinical & Regulatory Intelligence
        self.assertTrue(hasattr(client, "clinical_regulatory"))
        guidelines = client.clinical_regulatory.list_guidelines()
        self.assertIsInstance(guidelines, list)

        # Prompt 19: Scientific Simulation & Hypotheses
        self.assertTrue(hasattr(client, "simulation"))
        hypotheses = client.simulation.list_hypotheses()
        self.assertIsInstance(hypotheses, list)

        # Prompt 20: Ontology & Terminology Evolution
        self.assertTrue(hasattr(client, "terminology"))
        self.assertTrue(callable(client.terminology.resolve))

        # Prompt 21: Scientific Data Fabric & Compute
        self.assertTrue(hasattr(client, "compute"))
        self.assertTrue(callable(client.compute.plan_analysis))

        # Prompt 22: Collaboration Network
        self.assertTrue(hasattr(client, "collaboration"))
        self.assertTrue(callable(client.collaboration.resolve_researcher))

        # Prompt 23: Federated & Private Research Intelligence
        self.assertTrue(hasattr(client, "federated"))
        self.assertTrue(hasattr(client, "private"))

        # Prompt 24: Scientific Agent Operating System
        self.assertTrue(hasattr(client, "agents"))
        self.assertTrue(hasattr(client, "agent_tasks"))
        self.assertTrue(hasattr(client, "tools"))

        # Prompt 25: Scientific Knowledge Operating System (SKOS)
        self.assertTrue(hasattr(client, "skos"))
        self.assertTrue(callable(client.skos.answer))

        # Prompt 26: Scientific Reproducibility & Research Audit
        self.assertTrue(hasattr(client, "audit"))
        self.assertTrue(callable(client.audit.ledger))
        self.assertTrue(callable(client.audit.verify))

        # Prompt 27: Enterprise Production Build Specification
        self.assertTrue(hasattr(client, "spec"))
        layers = client.spec.layers()
        self.assertIsInstance(layers, list)
        self.assertGreaterEqual(len(layers), 10)


if __name__ == "__main__":
    unittest.main()
