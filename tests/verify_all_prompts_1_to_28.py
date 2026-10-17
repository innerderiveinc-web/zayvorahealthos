"""
ZMIE Master Acceptance & Verification Certification Suite (Prompts 1 to 28)
Executes end-to-end programmatic verification across all 28 core subsystems and specifications:

Prompt 01: Core Architecture & Invariant Engine
Prompt 02: Full System Execution & Implementation
Prompt 03: Governed Medical Ingestion & Licensing
Prompt 04: Multi-Paradigm Knowledge & Evidence Graph
Prompt 05: 17-Mode Hybrid Search & Retrieval
Prompt 06: Deep Research Agent & Synthesis
Prompt 07: Truth Firewall & Citation Validation
Prompt 08: Research Workbench & Studio Contracts
Prompt 09: Security, Privacy & Zero-Trust Tenancy
Prompt 10: Red-Team & Adversarial Invariant Defense
Prompt 11: Closed-Loop Active Learning
Prompt 12: Validation Lab & Golden Benchmarks
Prompt 13: Global Source Universe (Tiers A-G)
Prompt 14: Research Discovery & Evolution Cascades
Prompt 15: RWE, FHIR & OMOP CDM Interoperability
Prompt 16: Causal DAGs & Mechanistic Biomarkers
Prompt 17: Living Evidence Synthesis & Retraction
Prompt 18: Global Clinical & Regulatory Intelligence
Prompt 19: In Silico Simulation & Hypothesis Engine
Prompt 20: Ontology Drift & Semantic Evolution
Prompt 21: Data Fabric & Sandboxed Compute
Prompt 22: Collaboration & Conflict-of-Interest
Prompt 23: Federated Privacy & Differential Privacy
Prompt 24: Scientific Agent Operating System
Prompt 25: Scientific Knowledge Operating System (SKOS)
Prompt 26: Scientific Reproducibility & Research Audit
Prompt 27: Enterprise Implementation & Production Build Specification
Prompt 28: Build Execution, Code Generation & Module-by-Module Implementation
"""

import unittest
from datetime import datetime, timezone

from zmie import ZMIEClient
from app.main import app
from app.platform.gateway import APIGatewayEngine


class TestAllPrompts1To28Acceptance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        raw_key, _ = APIGatewayEngine.create_api_key(
            tenant_id="org-zmie-governance",
            owner="admin@zmie.org",
            name="Master Test Suite Key",
            scopes=["knowledge:read", "rag:read", "safety:read", "search:read", "evidence:read"]
        )
        cls.client = ZMIEClient(api_key=raw_key, app_instance=app)

    # --- PROMPT 01: Core Architecture & Invariants ---
    def test_prompt_01_core_architecture_and_invariants(self):
        root = self.client._request("GET", "/")
        self.assertEqual(root["status"], "operational")
        self.assertIn("ZMIE", root["engine"])
        self.assertIn("version", root)

    # --- PROMPT 02: Platform Execution, Gateway & Lifecycles ---
    def test_prompt_02_platform_execution_and_gateway(self):
        health = self.client._request("GET", "/health")
        self.assertEqual(health["status"], "healthy")
        self.assertIn("source_registry", health["subsystems"])
        self.assertEqual(health["subsystems"]["evidence_engine"], "connected")

    # --- PROMPT 03: Governed Medical Ingestion & Licensing ---
    def test_prompt_03_governed_ingestion_and_licensing(self):
        sources = self.client.sources.list()
        self.assertIsInstance(sources, list)
        self.assertGreaterEqual(len(sources), 1)
        first_src = sources[0]
        self.assertIn("authority_level", first_src)
        self.assertIn("license_status", first_src)

    # --- PROMPT 04: Multi-Paradigm Knowledge & Evidence Graph ---
    def test_prompt_04_knowledge_and_evidence_graph(self):
        res = self.client._request("GET", "/v1/graph/entities/CON-MOD-BERBERINE-001/timeline")
        self.assertEqual(res["entity_id"], "CON-MOD-BERBERINE-001")
        self.assertGreaterEqual(len(res["timeline"]), 1)

    # --- PROMPT 05: 17-Mode Hybrid Search & Retrieval ---
    def test_prompt_05_hybrid_search_retrieval(self):
        res = self.client.search(query="Curcumin in rheumatoid arthritis", mode="evidence")
        self.assertIn("query", res)
        self.assertIn("citations", res)
        self.assertGreaterEqual(len(res["citations"]), 1)
        self.assertIn("title", res["citations"][0])

    # --- PROMPT 06: Deep Research Agent & Synthesis ---
    def test_prompt_06_deep_research_agent(self):
        res = self.client._request(
            "POST",
            "/v1/research/investigate",
            json_data={"question": "Metformin anti-inflammatory pathway", "systems": ["modern"]}
        )
        self.assertIn("investigation_id", res)
        self.assertIn("pico_evidence_matrix", res)
        self.assertIn("structured_synthesis", res)

    # --- PROMPT 07: Truth Firewall & Citation Validation ---
    def test_prompt_07_truth_firewall_and_citations(self):
        valid_claim = {
            "claim_text": "Berberine lowered HbA1c by 1.8% after 12 weeks in adult type 2 diabetes.",
            "citation": {
                "source_id": "SRC-101",
                "document_id": "DOC-101",
                "title": "Randomized Trial of Berberine",
                "identifier": "PMID:18442638"
            },
            "passage_text": "In a randomized trial of 116 adult patients with type 2 diabetes, berberine lowered HbA1c by 1.8% after 12 weeks."
        }
        res = self.client._request("POST", "/v1/verify/claim", json_data=valid_claim)
        self.assertIn("verdict", res)
        self.assertEqual(res["verdict"], "PASS")

    # --- PROMPT 08: Research Workbench & Studio Contracts ---
    def test_prompt_08_workbench_contracts(self):
        rag = self.client.rag_context("Curcumin bioavailability")
        self.assertIn("verified_claims", rag)
        self.assertIn("safety_context", rag)
        self.assertIn("citations", rag)

    # --- PROMPT 09: Security, Privacy & Zero-Trust Tenancy ---
    def test_prompt_09_security_and_tenancy(self):
        req = {
            "user_id": "usr-1",
            "tenant_id": "TENANT_A",
            "roles": ["RESEARCHER"],
            "action": "research:read",
            "resource_tenant_id": "TENANT_A"
        }
        res = self.client._request("POST", "/v1/security/evaluate", json_data=req)
        self.assertTrue(res["allowed"])

    # --- PROMPT 10: Red-Team & Adversarial Invariant Defense ---
    def test_prompt_10_red_team_defense(self):
        fake_claim = {
            "claim_text": "Compound XYZ cures all cancers instantly",
            "citation": {
                "source_id": "SRC-FAKE",
                "document_id": "DOC-FAKE",
                "title": "Fabricated Paper",
                "identifier": "10.9999/FAKE_DOI_DOES_NOT_EXIST"
            },
            "passage_text": "Unverified assertion."
        }
        res = self.client._request("POST", "/v1/verify/claim", json_data=fake_claim)
        self.assertIn("verdict", res)
        self.assertIn(res["verdict"], ["BLOCK", "FLAG"])

    # --- PROMPT 11: Closed-Loop Active Learning ---
    def test_prompt_11_closed_loop_learning(self):
        res = self.client._request("POST", "/v1/closed-loop/execute", json_data={"topic": "SGLT2_CARDIOPROTECTION"})
        self.assertIn("cycle_id", res)
        self.assertEqual(res["topic"], "SGLT2_CARDIOPROTECTION")

    # --- PROMPT 12: Validation Lab & Golden Benchmarks ---
    def test_prompt_12_validation_lab(self):
        bench = self.client._request("GET", "/v1/evaluation/benchmarks")
        self.assertIsInstance(bench, list)
        self.assertGreaterEqual(len(bench), 1)

    # --- PROMPT 13: Global Source Universe (Tiers A-G) ---
    def test_prompt_13_global_source_universe(self):
        report = self.client.sources.coverage_report()
        self.assertIn("sources_discovered", report)
        self.assertIn("sources_active", report)

    # --- PROMPT 14: Research Discovery & Evolution Cascades ---
    def test_prompt_14_research_discovery(self):
        gaps = self.client.research_network.gaps()
        self.assertIsInstance(gaps, list)
        frontier = self.client.research_network.frontier()
        self.assertIsInstance(frontier, list)

    # --- PROMPT 15: RWE, FHIR & OMOP CDM Interoperability ---
    def test_prompt_15_rwe_interoperability(self):
        sources = self.client.rwe.list_sources()
        self.assertIsInstance(sources, list)
        raw_encounter = {
            "patient_id": "P-101",
            "gender": "male",
            "birth_date": "1980-01-01",
            "encounter_date": "2024-02-15",
            "diagnosis_code": "I50.9"
        }
        fhir = self.client.rwe.harmonize_raw_to_fhir(raw_encounter)
        self.assertIn("resourceType", fhir)
        self.assertEqual(fhir["resourceType"], "Bundle")

    # --- PROMPT 16: Causal DAGs & Mechanistic Biomarkers ---
    def test_prompt_16_causal_mechanistic(self):
        decomp = self.client.causal.decompose_mechanism({
            "compound_id": "CURCUMIN",
            "target_outcome": "Reduction in systemic inflammatory biomarkers"
        })
        self.assertIn("intervention_or_compound_id", decomp)
        self.assertIn("steps", decomp)

    # --- PROMPT 17: Living Evidence Synthesis & Retraction ---
    def test_prompt_17_living_evidence_synthesis(self):
        reviews = self.client.living_evidence.list()
        self.assertIsInstance(reviews, list)

    # --- PROMPT 18: Global Clinical & Regulatory Intelligence ---
    def test_prompt_18_clinical_regulatory(self):
        guidelines = self.client.clinical_regulatory.list_guidelines()
        self.assertIsInstance(guidelines, list)
        recalls = self.client.clinical_regulatory.list_recalls()
        self.assertIsInstance(recalls, list)

    # --- PROMPT 19: In Silico Simulation & Hypothesis Engine ---
    def test_prompt_19_simulation_hypothesis(self):
        hyps = self.client.simulation.list_hypotheses()
        self.assertIsInstance(hyps, list)

    # --- PROMPT 20: Ontology Drift & Semantic Evolution ---
    def test_prompt_20_ontology_evolution(self):
        res = self.client.terminology.resolve(
            term="Su-i Mizaj",
            context="Unani metabolic syndrome"
        )
        self.assertIn("input_text", res)
        self.assertIn("candidate_concepts", res)

    # --- PROMPT 21: Data Fabric & Sandboxed Compute ---
    def test_prompt_21_scientific_compute(self):
        plan = {
            "plan_id": "PLAN-TEST-HF-01",
            "research_question": "Does SGLT2i reduce cardiac death in HF?",
            "study_design": "Randomized Controlled Trial",
            "target_population": "NYHA II-IV Heart Failure patients",
            "exposure_variable": "sglt2_treatment",
            "comparator_variable": "standard_of_care",
            "outcome_variable": "cardiac_death",
            "covariates": ["baseline_egfr"],
            "statistical_method": "Cox Proportional Hazards Regression",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        res = self.client.compute.plan_analysis(plan)
        self.assertEqual(res["plan_id"], "PLAN-TEST-HF-01")
        self.assertTrue(res["data_leakage_checks_passed"])

    # --- PROMPT 22: Collaboration & Conflict-of-Interest ---
    def test_prompt_22_collaboration_network(self):
        res = self.client.collaboration.resolve_researcher(
            name="Elena Vance",
            institution="Broad Institute"
        )
        self.assertTrue(res["resolved"])

    # --- PROMPT 23: Federated Privacy & Differential Privacy ---
    def test_prompt_23_federated_privacy(self):
        fed_res = self.client.federated.query(
            sites=["site-univ-a", "site-hosp-b"],
            cohort_criteria={"min_age": 40},
            tenant_id="tenant-univ-a",
            user_id="ua-pi"
        )
        self.assertEqual(fed_res["execution_status"], "COMPLETED")

    # --- PROMPT 24: Scientific Agent Operating System ---
    def test_prompt_24_agent_os(self):
        agents_list = self.client.agents.list()
        self.assertIsInstance(agents_list, list)
        self.assertGreaterEqual(len(agents_list), 1)

    # --- PROMPT 25: Scientific Knowledge Operating System (SKOS) ---
    def test_prompt_25_skos_answer_engine(self):
        answer = self.client.skos.answer(
            question="What is the clinical efficacy of Berberine in Type 2 Diabetes?"
        )
        self.assertIn("summary", answer)
        self.assertIn("sections", answer)
        self.assertIn("coverage", answer)
        self.assertIn("provenance_certificate", answer)

    # --- PROMPT 26: Scientific Reproducibility & Research Audit ---
    def test_prompt_26_reproducibility_audit(self):
        snaps = self.client.audit.snapshots.list()
        self.assertIsInstance(snaps, list)
        records = self.client.audit.ledger()
        self.assertIsInstance(records, list)

    # --- PROMPT 27: Enterprise Implementation & Production Build Specification ---
    def test_prompt_27_enterprise_production_spec(self):
        readiness = self.client.spec.readiness()
        self.assertEqual(readiness["overall_status"], "READY")
        self.assertEqual(readiness["total_domains"], 20)
        self.assertEqual(readiness["ready_domains"], 20)

        invariants_eval = self.client.spec.verify_invariants()
        self.assertEqual(invariants_eval["total_invariants"], 10)
        self.assertEqual(invariants_eval["active_invariants"], 10)
        self.assertTrue(invariants_eval["all_passed"])

        adrs = self.client.spec.adrs()
        self.assertGreaterEqual(len(adrs), 15)

    # --- PROMPT 28: Build Execution, Code Generation & Module-by-Module Implementation ---
    def test_prompt_28_build_execution_and_invariants(self):
        telemetry = self.client.admin.telemetry()
        self.assertEqual(telemetry["engine_status"], "OPERATIONAL_NOMINAL")
        self.assertGreater(telemetry["uptime_seconds"], 0)

        quality = self.client.admin.quality_dashboard()
        self.assertIn("human_verified_claims_count", quality)
        self.assertIn("quarantined_retracted_sources", quality)
        self.assertEqual(quality["citation_entailment_failure_rate"], 0.0)

        auth = self.client.tenancy.evaluate(
            user_id="usr-test-28",
            tenant_id="TENANT_PROD",
            roles=["RESEARCHER"],
            action="research:read",
            resource_tenant_id="TENANT_PROD"
        )
        self.assertTrue(auth["allowed"])

    # --- PROMPT 29: Scientific Credibility, Verification, Provenance & Anti-Fabrication Audit Engine ---
    def test_prompt_29_scientific_credibility_and_verification_doctrine(self):
        """Verifies Prompt 29: 14-layer Anti-Fabrication audit, Mandatory Evidence Chain, and Golden Rule."""
        # 1. 14-Layer Anti-Fabrication Audit
        audit_res = self.client.credibility.audit_claim(
            target_object_id="clm-prompt29-01",
            claim_text="Berberine lowers fasting blood glucose by 1.8% in adult diabetics.",
            source_id="SRC-PUBMED-01",
            identifier="PMID:18442638",
            passage_text="In a trial of 116 adult patients with type 2 diabetes, berberine lowered fasting blood glucose by 1.8% after 12 weeks.",
            dataset_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            researcher_orcid="0000-0002-1825-0097",
            calculation_seed=42,
            is_expert_signed=True,
            exact_location="Results Section, Table 2"
        )
        self.assertIn("audit_id", audit_res)
        self.assertEqual(len(audit_res["layers_audited"]), 14)
        self.assertTrue(audit_res["is_authoritative_permitted"])
        self.assertEqual(audit_res["overall_state"], "AUTHORITATIVE")

        # 2. Mandatory Evidence Chain Integrity (incomplete chain demotion)
        chain_incomplete = self.client.credibility.verify_chain({
            "chain_id": "chain-prompt29-broken",
            "claim_id": "clm-broken",
            "claim_text": "Unverified assertion.",
            "evidence_id": None, # Missing evidence!
            "study_or_dataset_id": "PMID:18442638",
            "source_id": "SRC-PUBMED-01",
            "exact_location": None,
            "provenance_hash": None,
            "verification_state": "AUTHORITATIVE"
        })
        self.assertFalse(chain_incomplete["is_complete"])
        self.assertEqual(chain_incomplete["verification_state"], "INSUFFICIENT_EVIDENCE")

    # --- PROMPT 30: Real-Source Verification & Scientific Trust Firewall ---
    def test_prompt_30_real_source_verification_and_trust_firewall(self):
        """Verifies Prompt 30: Canonical registries, synthetic DOI blocking, and epistemic drift."""
        # Genuine source verification
        auth_src = self.client.trust_firewall.verify_source("10.1056/nejmoa2022483")
        self.assertTrue(auth_src["is_authentic"])
        self.assertEqual(auth_src["registry"], "CROSSREF")

        # Fake DOI blocked
        fake_src = self.client.trust_firewall.verify_source("10.9999/fabricated-doi")
        self.assertFalse(fake_src["is_authentic"])

        # Claim trust evaluation
        eval_report = self.client.trust_firewall.evaluate_claim(
            claim_text="The mRNA-1273 vaccine showed 94.1% efficacy at preventing Covid-19 illness.",
            doi="10.1056/nejmoa2022483",
            claimed_passage="The mRNA-1273 vaccine showed 94.1% efficacy at preventing Covid-19 illness, including severe disease."
        )
        self.assertIn(eval_report["trust_decision"], ["ALLOW", "PASSED"])

    # --- PROMPT 31: Continuous Evidence / Knowledge Revalidation ---
    def test_prompt_31_continuous_evidence_revalidation(self):
        """Verifies Prompt 31: Dynamic claim dependency graph and cascade invalidation."""
        delta = self.client.revalidation.ingest_surveillance_event(
            study_id="study-101",
            event_type="STUDY_RETRACTED",
            reason="Fabrication in primary multicenter dataset",
            severity="CRITICAL",
            doi="10.1016/s0140-6736(20)31180-fake"
        )
        self.assertIn("delta_id", delta)
        self.assertEqual(delta["affected_nodes_count"], 4)
        self.assertEqual(delta["new_grade_certainty"], "VERY_LOW")
        self.assertTrue(delta["requires_human_review"])

    # --- PROMPT 32: Production Security + Privacy Hardening ---
    def test_prompt_32_production_security_and_privacy_hardening(self):
        """Verifies Prompt 32: Differential privacy, HIPAA Safe Harbor, and envelope encryption."""
        dp = self.client.security_hardening.apply_differential_privacy(raw_value=120.0, epsilon=0.5)
        self.assertTrue(dp["is_privacy_guaranteed"])
        self.assertNotEqual(dp["noisy_value"], 120.0)

        deid = self.client.security_hardening.deidentify("Patient SSN 000-11-2222, MRN-44556, age 92")
        self.assertIn("[REDACTED_SSN]", deid["sanitized_text"])
        self.assertIn("[REDACTED_MRN]", deid["sanitized_text"])
        self.assertIn("age: 90+", deid["sanitized_text"])

        enc = self.client.security_hardening.envelope_encrypt("tenant-a", "art-1", "sensitive research data")
        self.assertIn("encrypted_dek_b64", enc)

    # --- PROMPT 33: Scientific Benchmarking & Validation ---
    def test_prompt_33_scientific_benchmarking_and_validation(self):
        """Verifies Prompt 33: Golden benchmark batteries with 0% negative-control hallucination."""
        report = self.client.benchmarking.run("NEGATIVE_CONTROLS")
        self.assertEqual(report["accuracy"], 1.0)
        self.assertEqual(report["hallucination_rate"], 0.0)

    # --- PROMPT 34: Production Readiness Audit ---
    def test_prompt_34_production_readiness_audit(self):
        """Verifies Prompt 34: 7-pillar preflight audit and GO certification."""
        cert = self.client.production_readiness.preflight_audit()
        self.assertEqual(cert["verdict"], "GO")
        self.assertTrue(cert["is_production_ready"])
        self.assertEqual(len(cert["digital_signature"]), 64)

    # --- PROMPT 35: Controlled Launch & Continuous Monitoring ---
    def test_prompt_35_controlled_launch_and_continuous_monitoring(self):
        """Verifies Prompt 35: Ring progression (Ring 0 -> Ring 1) and continuous telemetry."""
        plan = self.client.controlled_launch.promote()
        self.assertEqual(plan["current_ring"], "RING_1_PILOT_ACADEMIC")

        telem = self.client.controlled_launch.get_telemetry()
        self.assertEqual(telem["system_health_verdict"], "OPERATIONAL")
        self.assertEqual(telem["active_invariants_count"], 10)


if __name__ == "__main__":
    unittest.main()

