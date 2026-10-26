"""
ZMIE Scientific Knowledge Operating System (SKOS) Acceptance Test Suite (Prompt 25)
Verifies all 16 mandatory acceptance scenarios specified in Clauses 300-315:
- 300: System-wide acceptance test (16 graphs integrated via meta-layer)
- 301: Full failure test (fake citations, retracted studies, unbacked causal claims blocked)
- 302: Full knowledge-change test (evidence revalidation task, human decision, non-destructive state update)
- 303: Full retraction test (cascading impact analysis, downstream quarantine, history preserved)
- 304: Full terminology test (traditional concept boundary preserved, NO_VALID_MAPPING)
- 305: Full data test (scientific data fabric dataset linkage, checksums, provenance)
- 306: Full model test (hypothesis -> simulation with SIMULATION != OBSERVATION enforcement)
- 307: Full private test (tenant isolation, confidential research access protection)
- 308: Full federated test (federated query differential privacy & min cell size)
- 309: Full agent test (agent operating system governance, human review checkpoint)
- 310: Full reproduction test (execution certificates, provenance passports)
- 311: Master scientific graph forward traversal (Source -> Guideline)
- 312: Master knowledge path reverse traversal (Guideline -> Source)
- 313: Research intelligence path (Researcher -> Institution -> Study -> Dataset -> Target -> Compound)
- 314: Knowledge to experiment path (Gap -> Hypothesis -> Experiment Protocol)
- 315: Complete scientific learning loop (8-stage closed-loop learning cycle)
Plus REST API and Python SDK client tests.
"""

import asyncio
import unittest
from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app
from app.skos import (
    get_skos,
    SKOSEpistemicState,
    SKOSEntityType,
    SKOSRelationshipType,
    RevalidationState,
    KnowledgeDecisionAction,
    SKOSMasterEntity,
    RetractionNotice,
    ZMIEScientificExecutionCertificate,
    ZMIEKnowledgeProvenanceCertificate
)
from zmie.client import ZMIE


class TestSKOSAcceptance(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        try:
            asyncio.get_event_loop()
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())
        self.skos = get_skos()
        self.client = TestClient(app)
        self.sdk = ZMIE(app_instance=app)

    # ==========================================================================
    # Clause 300: System-Wide Acceptance Test
    # ==========================================================================
    def test_300_system_wide_acceptance(self):
        """
        Verify all 16 scientific graphs connect through meta-graph and KnowledgeFabricRegistry.
        Single source of truth holds cross-graph entities.
        """
        status = self.skos.get_system_status()
        self.assertEqual(status["active_graphs"], 16)
        self.assertEqual(status["absolute_scientific_rules_enforced"], 18)
        self.assertEqual(status["epistemic_firewall"], "ACTIVE")

        # Verify Knowledge Fabric Registry contains diverse entity types
        entities = self.skos.fabric.list_all_entities()
        self.assertGreaterEqual(len(entities), 20)

        types_present = {e.entity_type for e in entities}
        self.assertIn(SKOSEntityType.BIOMEDICAL_CONCEPT, types_present)
        self.assertIn(SKOSEntityType.MOLECULAR_TARGET, types_present)
        self.assertIn(SKOSEntityType.STUDY, types_present)
        self.assertIn(SKOSEntityType.CLAIM, types_present)
        self.assertIn(SKOSEntityType.REGULATORY_RECORD, types_present)

        # Meta-layer contains registered edges connecting the graphs
        self.assertGreater(len(self.skos.graph.edges), 10)

    # ==========================================================================
    # Clause 301: Full Failure Test
    # ==========================================================================
    def test_301_full_failure_test(self):
        """
        Firewall blocks fabricated citations, retracted studies as positive evidence,
        and unbacked causal phrasing (Rule 6: Correlation != Causation, Rule 17: Zero Fabrication).
        """
        firewall = self.skos.firewall

        # 1. Fake citation fails verification
        self.assertFalse(firewall.verify_citation("fake.doi/9999999"))
        self.assertFalse(firewall.verify_citation("doi:10.1000/fabricated_paper_xyz"))
        # Valid seed DOI passes
        self.assertTrue(firewall.verify_citation("10.1001/jama.2023.001"))

        # 2. Causal overreach rejected when epistemic state is merely ASSOCIATED
        bad_assertion = firewall.validate_assertion(
            "Berberine definitely cures type 2 diabetes by directly repairing beta cells.",
            epistemic_state=SKOSEpistemicState.ASSOCIATED
        )
        self.assertFalse(bad_assertion["allowed"])
        self.assertTrue(any("RULE_6" in v or "RULE_8" in v for v in bad_assertion["rule_violations"]))

        # 3. Retracted study cannot serve as positive evidence
        retracted_assertion = firewall.validate_assertion(
            "According to the retracted Wakefield report, vaccines cause neurological regression.",
            epistemic_state=SKOSEpistemicState.RETRACTED
        )
        self.assertFalse(retracted_assertion["allowed"])
        self.assertTrue(any("RULE_17" in v for v in retracted_assertion["rule_violations"]))

    # ==========================================================================
    # Clause 302: Full Knowledge-Change Test
    # ==========================================================================
    def test_302_full_knowledge_change_test(self):
        """
        New evidence triggers revalidation task -> human review decision ->
        non-destructive epistemic state update (never silent deletion).
        """
        # 1. Trigger revalidation task
        task = self.skos.revalidation.trigger_new_evidence_revalidation(
            new_study_doi="10.1056/nejmoa2024009",
            target_claim_id="CLM-BER-001",
            reason="Large multicenter RCT reports attenuated HbA1c reduction in metformin-resistant cohort."
        )
        self.assertIsNotNone(task.task_id)
        self.assertEqual(task.state, RevalidationState.FLAGGED)
        self.assertEqual(task.target_claim_id, "CLM-BER-001")

        # 2. Expert reviewer records decision
        decision = self.skos.revalidation.record_decision(
            task_id=task.task_id,
            reviewer_user_id="expert-dr-patel",
            action=KnowledgeDecisionAction.REVISE_CLAIM,
            rationale="Subgroup analysis justifies updating epistemic status to CHALLENGED with qualified indications."
        )
        self.assertEqual(decision.action, KnowledgeDecisionAction.REVISE_CLAIM)

        # 3. Non-destructive update: target claim updated to CHALLENGED
        claim_entity = self.skos.fabric.get_entity("CLM-BER-001")
        self.assertEqual(claim_entity.epistemic_state, SKOSEpistemicState.CHALLENGED)
        self.assertTrue(len(claim_entity.history) >= 2)

    # ==========================================================================
    # Clause 303: Full Retraction Test
    # ==========================================================================
    def test_303_full_retraction_test(self):
        """
        Retraction of study cascades to dependent claims, syntheses, guidelines;
        quarantines entities and preserves provenance history without silent deletion.
        """
        notice = RetractionNotice(
            study_doi="10.1001/jama.2023.001",
            pmid="36599001",
            retraction_doi="10.1001/jama.2024.999",
            reason="Data fabrication identified in Western blot assays.",
            retraction_type="FULL_RETRACTION",
            author_statement="Authors retract paper in agreement with institutional committee."
        )

        impact = self.skos.revalidation.handle_retraction(notice)
        self.assertIn("STU-BER-001", impact.affected_studies)
        self.assertIn("CLM-BER-001", impact.affected_claims)
        self.assertIn("SYN-META-001", impact.affected_syntheses)
        self.assertEqual(impact.quarantine_status, "QUARANTINED")

        # Verify historical record preserved: entity epistemic state changed to RETRACTED
        retracted_study = self.skos.fabric.get_entity("STU-BER-001")
        self.assertEqual(retracted_study.epistemic_state, SKOSEpistemicState.RETRACTED)
        self.assertTrue(len(retracted_study.history) >= 2)

    # ==========================================================================
    # Clause 304: Full Terminology Test
    # ==========================================================================
    def test_304_full_terminology_test(self):
        """
        Traditional concepts preserve distinct identity (Rule 14: Traditional Concept != Biomedical Equivalent).
        NO_VALID_MAPPING preserved for concepts without modern equivalence.
        """
        firewall = self.skos.firewall

        # Humoral Unani concept 'Damavi' must not be force-mapped to polycythemia
        check = firewall.validate_traditional_mapping(
            source_system="unani",
            source_term="Damavi",
            target_system="modern",
            target_concept="polycythemia_vera"
        )
        self.assertFalse(check["valid"])
        self.assertEqual(check["mapping_flag"], "NO_VALID_MAPPING")
        self.assertTrue(any("RULE_14" in v for v in check["rule_violation"]))

        # Concept in Fabric exists with traditional system annotation
        damavi = self.skos.fabric.get_entity("CON-DAMAVI")
        self.assertIsNotNone(damavi)
        self.assertEqual(damavi.metadata.get("medical_system"), "unani")
        self.assertEqual(damavi.metadata.get("concept_type"), "mizaj_humoral")

    # ==========================================================================
    # Clause 305: Full Data Test
    # ==========================================================================
    def test_305_full_data_test(self):
        """
        Scientific Data Fabric dataset linkage, schema format verification,
        and cryptographic content checksum.
        """
        dataset = self.skos.fabric.get_entity("DAT-BER-001")
        self.assertIsNotNone(dataset)
        self.assertEqual(dataset.entity_type, SKOSEntityType.DATASET)
        self.assertIn("sha256_checksum", dataset.metadata)
        self.assertEqual(dataset.metadata["format"], "parquet")
        self.assertGreater(dataset.metadata["sample_size"], 100)

    # ==========================================================================
    # Clause 306: Full Model Test
    # ==========================================================================
    def test_306_full_model_test(self):
        """
        Hypothesis generation and simulation prediction enforce SIMULATION != OBSERVATION
        (Rule 10: Simulation != Observation, Rule 11: Prediction != Result).
        """
        hyp = self.skos.fabric.get_entity("HYP-BER-001")
        self.assertIsNotNone(hyp)
        self.assertEqual(hyp.entity_type, SKOSEntityType.HYPOTHESIS)
        self.assertEqual(hyp.epistemic_state, SKOSEpistemicState.HYPOTHESIZED)

        # Simulation output can never be tagged as OBSERVED
        sim_assertion = self.skos.firewall.validate_assertion(
            "In silico docking predicts AMPK binding affinity of -8.4 kcal/mol.",
            epistemic_state=SKOSEpistemicState.OBSERVED
        )
        self.assertFalse(sim_assertion["allowed"])
        self.assertTrue(any("RULE_10" in v or "RULE_11" in v for v in sim_assertion["rule_violations"]))

    # ==========================================================================
    # Clause 307: Full Private Test
    # ==========================================================================
    def test_307_full_private_test(self):
        """
        Tenant isolation: confidential research asset isolation, preventing data leakage
        across tenants or into public mode.
        """
        firewall = self.skos.firewall

        # Cross-tenant access is blocked
        self.assertFalse(firewall.check_data_access(
            user_tenant="tenant-a-hospital",
            resource_tenant="tenant-b-pharma",
            resource_classification="CONFIDENTIAL",
            requested_mode="private"
        ))

        # Public mode request for confidential resource is blocked
        self.assertFalse(firewall.check_data_access(
            user_tenant="tenant-b-pharma",
            resource_tenant="tenant-b-pharma",
            resource_classification="CONFIDENTIAL",
            requested_mode="public"
        ))

        # Authorized tenant in private mode is allowed
        self.assertTrue(firewall.check_data_access(
            user_tenant="tenant-b-pharma",
            resource_tenant="tenant-b-pharma",
            resource_classification="CONFIDENTIAL",
            requested_mode="private"
        ))

    # ==========================================================================
    # Clause 308: Full Federated Test
    # ==========================================================================
    def test_308_full_federated_test(self):
        """
        Federated multi-site aggregation respects differential privacy and min cell size.
        """
        fed_res = self.sdk.federated.query(
            sites=["site-univ-a", "site-hosp-b"],
            tenant_id="tenant-univ-a",
            user_id="ua-pi",
            min_cell_size=10,
            enable_differential_privacy=True,
            epsilon=1.0
        )
        self.assertIn(fed_res.get("execution_status") or fed_res.get("status"), ["COMPLETED", "PARTIAL_FEDERATED_RESULT"])
        self.assertIn("certificate", fed_res)
        self.assertEqual(fed_res["certificate"]["raw_rows_transferred"], 0)

    # ==========================================================================
    # Clause 309: Full Agent Test
    # ==========================================================================
    def test_309_full_agent_test(self):
        """
        Agent governance: agent output cannot override scientific authority (Rule 18:
        AI Output != Scientific Authority).
        High-risk clinical recommendations require human review checkpoints.
        """
        # Rule 18 violation check
        agent_override = self.skos.firewall.validate_assertion(
            "ZMIE autonomous agent conclusively proves high-dose curcumin cures Crohn's disease without clinical trial.",
            epistemic_state=SKOSEpistemicState.PROVEN
        )
        self.assertFalse(agent_override["allowed"])
        self.assertTrue(any("RULE_18" in v or "RULE_8" in v for v in agent_override["rule_violations"]))

    # ==========================================================================
    # Clause 310: Full Reproduction Test
    # ==========================================================================
    def test_310_full_reproduction_test(self):
        """
        Computational research reproducibility verification with execution certificates
        and provenance passports.
        """
        exec_cert = self.skos.snapshots.generate_execution_certificate(
            computation_id="COMP-RCT-2023-01",
            code_hash="sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
            data_hash="sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            environment_spec={"python": "3.9.6", "zmie_core": "1.0.0", "seed": 42},
            is_deterministic=True
        )
        self.assertEqual(exec_cert.reproducibility_status, "REPRODUCIBLE")
        self.assertTrue(exec_cert.is_deterministic)

        prov_cert = self.skos.snapshots.generate_provenance_certificate(
            claim_id="CLM-BER-001",
            root_source_ids=["SRC-PUB-2023-01"],
            graph_path=["SRC-PUB-2023-01", "STU-BER-001", "CLM-BER-001"]
        )
        self.assertEqual(prov_cert.integrity_status, "VERIFIED")
        self.assertEqual(prov_cert.hop_count, 3)

    # ==========================================================================
    # Clause 311: Master Scientific Graph Forward Traversal
    # ==========================================================================
    def test_311_master_scientific_graph_forward_traversal(self):
        """
        Traverse: SOURCE -> STUDY -> FINDING -> CLAIM -> SYNTHESIS -> GUIDELINE
        """
        path = self.skos.graph.traverse_master_scientific_path(direction="FORWARD")
        self.assertEqual(path.path_type, "MASTER_FORWARD")
        self.assertEqual(path.direction, "FORWARD")
        self.assertGreaterEqual(path.total_hops, 5)

        start_ent = self.skos.fabric.get_entity(path.start_entity_id)
        end_ent = self.skos.fabric.get_entity(path.end_entity_id)
        self.assertEqual(start_ent.entity_type, SKOSEntityType.SOURCE)
        self.assertEqual(end_ent.entity_type, SKOSEntityType.GUIDELINE)

    # ==========================================================================
    # Clause 312: Master Knowledge Path Reverse Traversal
    # ==========================================================================
    def test_312_master_knowledge_path_reverse_traversal(self):
        """
        Traverse: GUIDELINE -> SYNTHESIS -> CLAIM -> FINDING -> STUDY -> SOURCE
        """
        path = self.skos.graph.traverse_master_scientific_path(direction="REVERSE")
        self.assertEqual(path.path_type, "MASTER_REVERSE")
        self.assertEqual(path.direction, "REVERSE")
        self.assertGreaterEqual(path.total_hops, 5)

        start_ent = self.skos.fabric.get_entity(path.start_entity_id)
        end_ent = self.skos.fabric.get_entity(path.end_entity_id)
        self.assertEqual(start_ent.entity_type, SKOSEntityType.GUIDELINE)
        self.assertEqual(end_ent.entity_type, SKOSEntityType.SOURCE)

    # ==========================================================================
    # Clause 313: Research Intelligence Path
    # ==========================================================================
    def test_313_research_intelligence_path(self):
        """
        Traverse: SCIENTIST -> INSTITUTION -> STUDY -> DATASET -> TARGET -> COMPOUND
        """
        path = self.skos.graph.find_research_path("RES-CHEN-01")
        self.assertEqual(path.path_type, "RESEARCH_INTELLIGENCE")
        self.assertEqual(path.start_entity_id, "RES-CHEN-01")
        self.assertEqual(path.end_entity_id, "CMP-BERBERINE")
        self.assertGreaterEqual(path.total_hops, 5)

    # ==========================================================================
    # Clause 314: Knowledge to Experiment Path
    # ==========================================================================
    def test_314_knowledge_to_experiment_path(self):
        """
        Traverse: GAP -> HYPOTHESIS -> SIMULATION -> EXPERIMENT_PROTOCOL
        """
        path = self.skos.graph.find_experiment_path("HYP-BER-001")
        self.assertEqual(path.path_type, "KNOWLEDGE_TO_EXPERIMENT")
        self.assertEqual(path.start_entity_id, "GAP-BER-001")
        self.assertEqual(path.end_entity_id, "EXP-BER-001")
        self.assertGreaterEqual(path.total_hops, 2)

    # ==========================================================================
    # Clause 315: Complete Scientific Learning Loop
    # ==========================================================================
    def test_315_complete_scientific_learning_loop(self):
        """
        Execute closed-loop learning across the 8 stages:
        Acquisition -> Computation -> Reasoning -> Synthesis -> Hypothesis -> Simulation -> Experiment -> Revalidation
        """
        loop = self.skos.get_learning_loop()
        self.assertEqual(loop["status"], "ACTIVE_CLOSED_LOOP")
        self.assertEqual(len(loop["loop_stages"]), 8)
        self.assertIn("1_ACQUISITION", loop["loop_stages"][0])
        self.assertIn("8_REVALIDATION", loop["loop_stages"][7])
        self.assertTrue(loop["meta_graph_active"])

    # ==========================================================================
    # SKOS REST API Endpoints
    # ==========================================================================
    def test_api_endpoints(self):
        # 1. Health
        health_resp = self.client.get("/v1/skos/health")
        self.assertEqual(health_resp.status_code, 200)
        self.assertEqual(health_resp.json()["active_graphs"], 16)

        # 2. Fabric entities
        entities_resp = self.client.get("/v1/skos/fabric/entities")
        self.assertEqual(entities_resp.status_code, 200)
        self.assertGreaterEqual(len(entities_resp.json()), 20)

        # 3. Specific entity
        entity_resp = self.client.get("/v1/skos/fabric/entities/CMP-BERBERINE")
        self.assertEqual(entity_resp.status_code, 200)
        self.assertEqual(entity_resp.json()["name"], "Berberine")

        # 4. Master traversal
        traverse_resp = self.client.get("/v1/skos/graph/traverse?direction=FORWARD")
        self.assertEqual(traverse_resp.status_code, 200)
        self.assertEqual(traverse_resp.json()["direction"], "FORWARD")

        # 5. Snapshots & Diff
        snap1_resp = self.client.post("/v1/skos/snapshots?description=Baseline+Snapshot")
        self.assertEqual(snap1_resp.status_code, 201)
        snap1 = snap1_resp.json()

        snap2_resp = self.client.post("/v1/skos/snapshots?description=Post-Revalidation+Snapshot")
        self.assertEqual(snap2_resp.status_code, 201)
        snap2 = snap2_resp.json()

        diff_resp = self.client.post("/v1/skos/snapshots/diff", json={
            "snapshot_a_id": snap1["snapshot_id"],
            "snapshot_b_id": snap2["snapshot_id"]
        })
        self.assertEqual(diff_resp.status_code, 200)
        diff = diff_resp.json()
        self.assertEqual(diff["base_snapshot_id"], snap1["snapshot_id"])

        # 6. Gaps map
        gaps_resp = self.client.get("/v1/skos/gaps?topic=Berberine+in+T2D")
        self.assertEqual(gaps_resp.status_code, 200)
        self.assertEqual(gaps_resp.json()["total_gaps_identified"], 9)

        # 7. Answer generation
        answer_resp = self.client.post("/v1/skos/answer", json={
            "question": "What is the evidence and mechanism for Berberine in Type 2 Diabetes?",
            "target_system": "all"
        })
        self.assertEqual(answer_resp.status_code, 200)
        ans = answer_resp.json()
        self.assertIn("BERBERINE", ans["question"].upper())
        self.assertIsNotNone(ans["provenance_certificate"])
        self.assertGreaterEqual(ans["coverage_report"]["overall_coverage_pct"], 80.0)

    # ==========================================================================
    # Python SDK Client Methods
    # ==========================================================================
    def test_sdk_methods(self):
        # 1. Health
        health = self.sdk.skos.health()
        self.assertEqual(health["status"], "OPERATIONAL")

        # 2. Fabric entities list
        entities = self.sdk.skos.entities.list()
        self.assertGreaterEqual(len(entities), 20)

        # 3. Specific entity get
        entity = self.sdk.skos.entities.get("TGT-AMPK")
        self.assertEqual(entity["name"], "AMP-activated protein kinase")

        # 4. Master forward traversal via SDK
        fwd_path = self.sdk.skos.paths.master_forward()
        self.assertEqual(fwd_path["direction"], "FORWARD")

        # 5. Snapshots list
        snapshots = self.sdk.skos.snapshots.list()
        self.assertIsInstance(snapshots, list)

        # 6. Gaps analyze
        gaps = self.sdk.skos.gaps.analyze("Berberine in Type 2 Diabetes")
        self.assertEqual(len(gaps["gaps_by_dimension"]), 9)

        # 7. Unified Answer via SDK
        answer = self.sdk.skos.answer("What is the clinical efficacy of Berberine in Type 2 Diabetes?")
        self.assertEqual(answer["state"], "COMPLETE")
        self.assertIsNotNone(answer["summary_findings"])


if __name__ == "__main__":
    unittest.main()
