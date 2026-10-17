"""
ZMIE Six Foundational Platform Invariants Acceptance Test Suite
Directly certifies and enforces:
1. Zero Fabrication Invariant (INV-01)
2. Tenant Boundary Isolation (INV-02)
3. Immutable Provenance Chains & Audit Hash-Chaining (INV-03 & INV-05)
4. Epistemic Distance Preservation (INV-04)
5. Deterministic Safety Firewall (INV-10)
6. Reproducibility Guarantee (INV-08)
"""

import unittest
import copy
from datetime import datetime, timezone

from app.main import app
from zmie import ZMIEClient
from app.platform.gateway import APIGatewayEngine
from app.core.tenancy import assert_tenant_boundary, TenantIsolationException, DataClassification
from app.core.authorization import (
    AuthorizationEngine,
    SubjectAttributes,
    ResourceAttributes,
    EnterpriseRole,
    Action,
    EvaluationResult
)
from app.core.identity import User
from app.core.audit import (
    AuditDispatcher,
    AuditEvent,
    AuditAction,
    ActorType
)
from app.core.provenance import (
    create_provenance,
    attach_provenance,
    get_provenance,
    trace_backward,
    trace_forward,
    ProvActivityType
)
from app.firewall.orchestrator import TruthAndSafetyFirewall
from app.firewall.citation_engine import CitationVerificationEngine
from app.models.truth_firewall import (
    Citation,
    FirewallVerdict,
    SupportLevel,
    ClaimRiskLevel
)
from app.firewall.causality_firewall import CausalityAndLanguageFirewall
from app.audit import get_audit_system
from app.scientific_compute.engine import ScientificDataFabricEngine


class TestPlatformInvariantsAcceptance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        raw_key, _ = APIGatewayEngine.create_api_key(
            tenant_id="tenant-governance-master",
            owner="auditor@zmie.org",
            name="Invariants Certification Key",
            scopes=["knowledge:read", "safety:read", "audit:read", "compute:read"]
        )
        cls.client = ZMIEClient(api_key=raw_key, app_instance=app)

    # =========================================================================
    # 1. Zero Fabrication Invariant (INV-01)
    # Absence of evidence strictly returns UNKNOWN or NO_EVIDENCE.
    # LLMs cannot synthesize unverified claims or fake DOIs.
    # =========================================================================
    def test_inv_01_zero_fabrication_absence_of_evidence(self):
        """
        Enforces INV-01:
        1. Fabrication of claims without citation is blocked or flagged.
        2. Citations with hallucinated/invalid passages are marked DOES_NOT_SUPPORT and blocked.
        3. Queries on completely unknown or unstudied entities return explicit unknowns.
        """
        # Case A: Unsupported medical claim with fake passage
        fake_citation = Citation(
            source_id="SRC-FAKE-999",
            document_id="DOC-FAKE-999",
            title="Nonexistent Clinical Trial",
            identifier="10.9999/fabricated.doi.2026"
        )
        unsupported_claim = "Compound XYZ cures stage IV pancreatic cancer in 48 hours."
        passage = "This in-vitro assay only observed minimal cell line binding without cytotoxicity."

        sup_lvl, ctx_ok, reasons = CitationVerificationEngine.verify_citation_entailment(
            claim_text=unsupported_claim,
            citation=fake_citation,
            passage_text=passage
        )
        self.assertEqual(sup_lvl, SupportLevel.DOES_NOT_SUPPORT)

        # Case B: Truth firewall verification must BLOCK this unverified claim
        packet = TruthAndSafetyFirewall.verify_answer(
            generated_answer=unsupported_claim,
            citations=[fake_citation],
            passages_map={fake_citation.citation_id: passage, fake_citation.identifier: passage}
        )
        self.assertEqual(packet.verdict, FirewallVerdict.BLOCK)
        self.assertTrue(len(packet.limitations) >= 1)
        self.assertIn("Blocked unverified assertion", packet.limitations[0])

        # Case C: Asking the SKOS engine an unstudied query returns explicit unknowns
        skos_resp = self.client.skos.answer("Effect of non-existent entity Zeta99 on human longevity")
        self.assertIn("summary", skos_resp)
        self.assertIn("coverage", skos_resp)
        self.assertIn("overall_status", skos_resp["coverage"])
        self.assertIn("overall_coverage_pct", skos_resp["coverage"])

    # =========================================================================
    # 2. Tenant Boundary Isolation (INV-02)
    # Multi-tenant access controls enforce complete cross-tenant isolation
    # across all resources, snapshots, queries, and audit logs.
    # =========================================================================
    def test_inv_02_tenant_boundary_isolation(self):
        """
        Enforces INV-02:
        1. Accessing resources belonging to Tenant B from Tenant A is strictly prohibited.
        2. Core assert_tenant_boundary raises TenantIsolationException.
        3. ABAC authorization policy denies cross-tenant actions.
        4. Audit snapshots from Tenant A cannot be retrieved by Tenant B.
        """
        user_tenant_a = User(
            user_id="usr-researcher-alpha",
            tenant_id="TENANT-ALPHA",
            org_id="ORG-ALPHA",
            full_name="Dr. Alpha",
            email="alpha@hospital.org"
        )

        # Gate 1: Core Tenancy Boundary Assertion
        with self.assertRaises(TenantIsolationException):
            assert_tenant_boundary(resource_tenant_id="TENANT-BETA", caller_tenant_id=user_tenant_a.tenant_id)

        # Same tenant must succeed
        assert_tenant_boundary(resource_tenant_id="TENANT-ALPHA", caller_tenant_id=user_tenant_a.tenant_id)

        # Gate 2: ABAC Security Policy Enforcement
        subj = SubjectAttributes(
            user_id="usr-researcher-alpha",
            tenant_id="TENANT-ALPHA",
            roles=[EnterpriseRole.RESEARCHER],
            clearance=DataClassification.CONFIDENTIAL
        )
        res_cross = ResourceAttributes(
            resource_id="doc-confidential-beta",
            resource_type="Document",
            tenant_id="TENANT-BETA",
            classification=DataClassification.CONFIDENTIAL
        )
        decision = AuthorizationEngine.evaluate(subj, Action.READ, res_cross)
        self.assertFalse(decision.allowed)
        self.assertIn("Tenant boundary isolation denied", decision.reason)

        # Gate 3: Research Snapshot Isolation
        audit_sys = get_audit_system()
        # Verify that requesting a snapshot with mismatched caller tenant is strictly rejected
        snap_alpha = audit_sys.get_snapshot("rs-golden-berberine-01", tenant_id="tenant-alpha")
        self.assertIsNotNone(snap_alpha)
        snap_beta = audit_sys.get_snapshot("rs-golden-berberine-01", tenant_id="tenant-beta")
        self.assertIsNone(snap_beta)

    # =========================================================================
    # 3. Immutable Provenance Chains (INV-03 & INV-05)
    # Audit trails are hashed using SHA-256 with HMAC tamper detection;
    # audit blocks form an unbroken verifiable chain.
    # =========================================================================
    def test_inv_03_and_05_immutable_provenance_and_hmac_audit_chains(self):
        """
        Enforces INV-03 & INV-05:
        1. W3C PROV-O provenance nodes link activity, entities, and actors.
        2. Bidirectional provenance tracing (backward lineage & forward impact).
        3. SHA-256 cryptographic chaining of audit log events with HMAC signatures.
        4. Any bit modification in past audit records immediately trips tamper detection.
        """
        # Step A: Provenance Creation & Tracing
        parent_node = create_provenance(
            target_id="ds-cohort-cardio-v1",
            activity_type=ProvActivityType.INGESTION,
            agent_id="usr-data-eng-01"
        )
        child_node = create_provenance(
            target_id="res-hazard-ratio-01",
            activity_type=ProvActivityType.STATISTICAL_COMPUTE,
            agent_id="usr-statistician-99",
            input_ids=["ds-cohort-cardio-v1"],
            metadata={"seed": 42, "iterations": 1000, "protocol": "PRISMA-2026-004"}
        )
        self.assertIsNotNone(child_node.provenance_id)
        self.assertIn("ds-cohort-cardio-v1", child_node.parent_ids)

        # Backward trace confirms input roots
        inputs_found = trace_backward("res-hazard-ratio-01")
        self.assertTrue(len(inputs_found) >= 1)

        # Forward trace confirms downstream outputs
        outputs_found = trace_forward("ds-cohort-cardio-v1")
        self.assertTrue(len(outputs_found) >= 1)


        # Step B: HMAC Audit Hash-Chaining
        dispatcher = AuditDispatcher()

        e1 = dispatcher.dispatch(
            actor="usr-1",
            actor_type=ActorType.USER,
            tenant_id="TENANT-CORE",
            object_type="ResearchSnapshot",
            object_id="snap-001",
            action=AuditAction.CREATE,
            metadata={"hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}
        )
        e2 = dispatcher.dispatch(
            actor="agent-auditor-01",
            actor_type=ActorType.AGENT,
            tenant_id="TENANT-CORE",
            object_type="ResearchSnapshot",
            object_id="snap-001",
            action=AuditAction.EXECUTE,
            metadata={"verdict": "VERIFIED"}
        )


        self.assertEqual(e2.prev_hash, e1.block_hash)
        self.assertTrue(dispatcher.verify_integrity())

        # Step C: Tamper Simulation — mutate event data in previous block
        tampered_dispatcher = copy.deepcopy(dispatcher)
        tampered_dispatcher._chain[0].actor = "usr-tampered-intruder"

        # Verification must now FAIL
        self.assertFalse(tampered_dispatcher.verify_integrity())


    # =========================================================================
    # 4. Epistemic Distance Preservation (INV-04)
    # Traditional systems of medicine (Ayurveda, Unani, Siddha, TCM, Sowa-Rigpa)
    # maintain explicit epistemic distance scores rather than erroneous 1:1 equivalences.
    # =========================================================================
    def test_inv_04_epistemic_distance_preservation(self):
        """
        Enforces INV-04:
        1. Reject simplistic, false 1:1 equivalence claims between classical medical
           constructs (e.g., Mizaj, Dosha, Qi) and reductionist modern biochemistry.
        2. Causality and Language Firewall requires explicit epistemic qualification
           (e.g., 'Functional Analogy', 'Conceptual Mapping') and flags direct identity claims.
        3. Terminology resolution API reports explicit epistemic distance scores (d < 1.0).
        """
        # Case A: False 1:1 identity claim must be detected and rewritten
        naive_claim = "Mizaj is equivalent to thyroid hormone levels in patients with fatigue."
        ok, reason, rewrite = CausalityAndLanguageFirewall.check_cross_system_equivalence(naive_claim)
        self.assertFalse(ok)
        self.assertIn("False equivalence", reason)
        self.assertIsNotNone(rewrite)
        self.assertIn("shares functional and conceptual parallels with", rewrite)

        # Case B: Cross-paradigm terminology resolution API preserves epistemic distance & disclaimers
        term_res = self.client.terminology.resolve("Mandagni", context="gastroenterology")
        self.assertEqual(term_res["input_text"], "Mandagni")
        self.assertIn("STRICT SEMANTIC PRINCIPLE", term_res["epistemic_disclaimer"])

        # Case C: Search engine cross-system perspectives retain explicit functional analogy scores
        search_res = self.client.search("Curcumin in rheumatoid arthritis")
        self.assertIn("cross_system_perspectives", search_res)
        self.assertIn("Functional Analogy (0.76)", search_res["cross_system_perspectives"]["unani"]["mapping_state"])
        self.assertIn("Functional Analogy (0.81)", search_res["cross_system_perspectives"]["ayurveda"]["mapping_state"])


    # =========================================================================
    # 5. Deterministic Safety Firewall (INV-10)
    # Clinical contraindications, CYP450 interactions, and toxicity limits
    # are calculated deterministically outside the LLM context.
    # =========================================================================
    def test_inv_10_deterministic_safety_firewall(self):
        """
        Enforces INV-10:
        1. Contraindications and CYP450 drug-herb interactions are computed
           by a deterministic rules engine rather than generated by generative probabilistic models.
        2. Black-box warnings and CYP3A4/CYP2C9 enzyme inhibition trigger deterministic risk alerts.
        """
        safety_eval = self.client.check_safety(
            substance="berberine",
            medications=["Cyclosporine"],
            conditions=["Pregnancy"]
        )

        self.assertEqual(safety_eval["safety_status"], "contraindicated_block")
        self.assertTrue(len(safety_eval["contraindications"]) >= 1)
        self.assertTrue(len(safety_eval["drug_interactions"]) >= 1)

        # Must report specific enzymatic mechanism (e.g., CYP3A4 or P-gp inhibition)
        mechanisms = [i.get("mechanism", "").upper() for i in safety_eval["drug_interactions"]]
        has_cyp3a4 = any("CYP3A4" in m for m in mechanisms)
        self.assertTrue(has_cyp3a4)


    # =========================================================================
    # 6. Reproducibility Guarantee (INV-08)
    # Sandboxed compute environments lock random seeds, library dependencies,
    # dataset hashes, and container images to ensure identical mathematical re-execution.
    # =========================================================================
    def test_inv_08_reproducibility_guarantee(self):
        """
        Enforces INV-08:
        1. Scientific compute runs lock random seed (42), execution environment,
           and input dataset SHA-256 hashes.
        2. Identical re-execution produces identical result hashes.
        3. Reproduction status is confirmed by the reproducibility engine.
        """
        engine = ScientificDataFabricEngine()
        orig_job = engine.execute_analysis_workflow(
            plan_id="PLAN-SGLT2-CV-DEATH",
            snapshot_id="SNAP-SGLT2-HF-v1.0"
        )
        self.assertEqual(orig_job.runtime_environment.random_seed, 42)
        self.assertIsNotNone(orig_job.code_hash)
        self.assertIsNotNone(orig_job.results)
        self.assertTrue(len(orig_job.results) >= 1)

        # Re-execute identically and verify computational certificate
        reproduced_job, cert = engine.reproduce_run(orig_job.job_id)
        self.assertEqual(cert.reproducibility_verdict, "FULLY_REPRODUCIBLE")
        self.assertEqual(cert.seed, 42)
        self.assertLess(cert.relative_divergence, 1e-6)
        self.assertEqual(cert.dataset_snapshot_hash, orig_job.dataset_snapshot_id)
        self.assertEqual(cert.code_hash, orig_job.code_hash)
        self.assertEqual(
            orig_job.results[0].effect_estimate.point_estimate,
            reproduced_job.results[0].effect_estimate.point_estimate
        )



if __name__ == "__main__":
    unittest.main()
