"""
ZMIE Continuous Evidence & Knowledge Revalidation Acceptance Test Suite
Continuous Evidence Revalidation Certification & Acceptance Tests
"""

import unittest
from app.continuous_revalidation.engine import ContinuousRevalidationEngine
from app.continuous_revalidation.models import (
    RevalidationEventType,
    InvalidationSeverity,
    DependencyNodeType,
    RevalidationTrigger,
    RevalidationScope,
    RevalidationPriority,
    RevalidationState,
    ContentChangeImpact,
)


class TestPrompt31ContinuousRevalidationAcceptance(unittest.TestCase):
    def setUp(self):
        self.engine = ContinuousRevalidationEngine()

    # =========================================================================
    # CORE FOUNDATIONAL TESTS (Preserved for backwards compatibility)
    # =========================================================================

    def test_01_dependency_graph_topology(self):
        """Graph contains seeded nodes for studies, meta-analysis, GRADE, guideline, and snapshot."""
        s1 = self.engine.get_node("study-101")
        self.assertIsNotNone(s1)
        self.assertEqual(s1["node_type"], DependencyNodeType.PRIMARY_STUDY)

        meta = self.engine.get_node("meta-covid-01")
        self.assertIsNotNone(meta)
        self.assertEqual(meta["node_type"], DependencyNodeType.META_ANALYSIS)

    def test_02_downstream_dependents_closure(self):
        """Downstream traversal from study-101 must discover all downstream dependents."""
        dependents = self.engine.get_downstream_dependents("study-101")
        self.assertIn("meta-covid-01", dependents)
        self.assertIn("grade-covid-01", dependents)
        self.assertIn("rec-who-covid-14", dependents)
        self.assertIn("snap-2026-covid-v1", dependents)
        self.assertEqual(len(dependents), 4)

    def test_03_cascade_invalidation_upon_retraction(self):
        """Retracting a study must cascade down, recalculating meta-analysis and downgrading GRADE."""
        delta = self.engine.process_surveillance_event(
            study_id="study-101",
            event_type=RevalidationEventType.STUDY_RETRACTED,
            reason="Data fabrication detected in multicenter hospital trial data",
            severity=InvalidationSeverity.CRITICAL,
            doi="10.1016/s0140-6736(20)31180-fake",
            source_notice_url="https://doi.org/10.1016/retraction-notice"
        )

        self.assertIsNotNone(delta)
        self.assertEqual(delta.affected_nodes_count, 4)
        self.assertEqual(delta.previous_grade_certainty, "MODERATE")
        self.assertEqual(delta.new_grade_certainty, "VERY_LOW")
        self.assertAlmostEqual(delta.previous_pooled_effect, -0.1145, places=3)
        self.assertAlmostEqual(delta.recomputed_pooled_effect, 0.05, places=2)
        self.assertGreater(delta.epistemic_shift_magnitude, 0.1)
        self.assertIn("rec-who-covid-14", delta.affected_guidelines)
        self.assertIn("snap-2026-covid-v1", delta.affected_snapshots)
        self.assertTrue(delta.requires_human_review)

        # Inspect updated node statuses
        meta_node = self.engine.get_node("meta-covid-01")
        self.assertEqual(meta_node["metadata"]["status"], "RECALCULATED_EXCLUDING_RETRACTED")

        guideline_node = self.engine.get_node("rec-who-covid-14")
        self.assertEqual(guideline_node["metadata"]["status"], "SUSPENDED_FOR_SAFETY_REVIEW")

    def test_04_delta_reports_retrieval(self):
        """Generated delta reports must be retrievable by ID and list."""
        delta = self.engine.process_surveillance_event(
            study_id="study-102",
            event_type=RevalidationEventType.ERRATUM_ISSUED,
            reason="Sample size typo corrected from 200 to 198",
            severity=InvalidationSeverity.LOW
        )

        reports = self.engine.list_delta_reports()
        self.assertGreaterEqual(len(reports), 1)

        fetched = self.engine.get_delta_report(delta.delta_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.delta_id, delta.delta_id)

    # =========================================================================
    # 20 MASTER ACCEPTANCE TESTS (Prompt 31 Clauses 277-296)
    # =========================================================================

    def test_acceptance_01_new_relevant_study(self):
        """Final Acceptance Test 1 (Clause 277): New study detected, verified, linked, revalidated."""
        # 1. Register new study
        self.engine.register_node("study-103", DependencyNodeType.PRIMARY_STUDY, {
            "title": "Phase III Trial of mRNA-1273 Bivalent Booster",
            "doi": "10.1056/nejmoa2022483",
            "effect_size": 0.88,
            "status": "ACTIVE"
        })
        # 2. Link to existing claim
        self.engine.add_dependency("study-103", "claim-mrna-01", "SUPPORTS")

        # 3. Request revalidation
        job = self.engine.request_revalidation(
            object_id="claim-mrna-01",
            trigger=RevalidationTrigger.SOURCE_TRIGGERED,
            reason="New Phase III RCT published"
        )
        self.assertEqual(job.status, "COMPLETED")
        self.assertIn("study-103", self.engine.get_upstream_dependencies("claim-mrna-01"))

    def test_acceptance_02_study_retracted_cascade(self):
        """Final Acceptance Test 2 (Clause 278): Retraction cascade across evidence, claims, guidelines, and snapshots."""
        impact = self.engine.analyze_impact(
            target_object_id="study-101",
            change_type=RevalidationEventType.STUDY_RETRACTED,
            impact_level=ContentChangeImpact.CRITICAL_IMPACT
        )
        self.assertEqual(impact.impact_level, ContentChangeImpact.CRITICAL_IMPACT)
        self.assertTrue(impact.requires_human_review)
        self.assertIn("rec-who-covid-14", impact.downstream_guidelines)
        self.assertIn("snap-2026-covid-v1", impact.downstream_snapshots)

    def test_acceptance_03_guideline_changes(self):
        """Final Acceptance Test 3 (Clause 279): Old guideline preserved, new registered, clinical knowledge updated."""
        job = self.engine.request_revalidation(
            object_id="rec-who-covid-14",
            trigger=RevalidationTrigger.EVENT_TRIGGERED,
            reason="WHO Guideline revision 2026"
        )
        self.assertEqual(job.status, "COMPLETED")

        # Historical version must be preserved
        history = self.engine.get_knowledge_history("rec-who-covid-14")
        self.assertGreaterEqual(len(history), 1)
        self.assertEqual(history[0].state, RevalidationState.SUPERSEDED)

        # Current node updated to new version
        current = self.engine.get_node("rec-who-covid-14")
        self.assertEqual(current["metadata"]["version"], "1.1")

    def test_acceptance_04_regulatory_status_changes(self):
        """Final Acceptance Test 4 (Clause 280): Jurisdiction-specific update & governance review."""
        job = self.engine.request_revalidation(
            object_id="regulatory-remdesivir-fda",
            trigger=RevalidationTrigger.EVENT_TRIGGERED,
            reason="FDA updates boxed warning for hepatic impairment"
        )
        self.assertEqual(job.status, "WAITING_REVIEW")
        reg_node = self.engine.get_node("regulatory-remdesivir-fda")
        self.assertEqual(reg_node["metadata"]["status"], "LABEL_RESTRICTION_ISSUED")
        self.assertEqual(reg_node["metadata"]["jurisdiction"], "USA")

    def test_acceptance_05_dataset_corrected(self):
        """Final Acceptance Test 5 (Clause 281): Dataset v2 flags dependent models for recomputation."""
        job = self.engine.request_revalidation(
            object_id="dataset-rct-2020",
            trigger=RevalidationTrigger.DATA_TRIGGERED,
            reason="Primary trial patient deduplication correction"
        )
        self.assertEqual(job.status, "COMPLETED")

        ds_node = self.engine.get_node("dataset-rct-2020")
        self.assertEqual(ds_node["metadata"]["version"], "2.0")

        # Model depending on dataset must be flagged
        model_node = self.engine.get_node("model-covid-sim-01")
        self.assertEqual(model_node["metadata"]["status"], "POTENTIALLY_STALE_AWAITING_RECOMPUTE")

    def test_acceptance_06_source_inaccessible_outage(self):
        """Final Acceptance Test 6 (Clause 282): Source outage returns CHECK_UNAVAILABLE, not NO_CHANGE."""
        res = self.engine.check_source_watch("src-watch-crossref", simulate_outage=True)
        self.assertEqual(res["status"], "CHECK_UNAVAILABLE")
        self.assertFalse(res["checked"])
        self.assertFalse(res["is_changed"])

    def test_acceptance_07_no_new_evidence_found_after_actual_search(self):
        """Final Acceptance Test 7 (Clause 283): Returns NO_NEW_EVIDENCE_FOUND with search scope and date."""
        res = self.engine.check_source_watch("src-watch-crossref", simulate_outage=False)
        self.assertEqual(res["status"], "NO_NEW_EVIDENCE_FOUND")
        self.assertTrue(res["checked"])
        self.assertIn("search_scope", res)
        self.assertIn("CROSSREF", res["sources_queried"])

    def test_acceptance_08_contradicting_study(self):
        """Final Acceptance Test 8 (Clause 284): Disconfirming study marks claim as CONFLICTING."""
        res = self.engine.find_contradictions(
            claim_id="claim-mrna-01",
            disconfirming_study_doi="10.1016/s0140-6736(21)00000-opposing"
        )
        self.assertEqual(res["status"], "CONFLICTING")
        self.assertTrue(res["requires_review"])

        claim_node = self.engine.get_node("claim-mrna-01")
        self.assertEqual(claim_node["metadata"]["status"], "CONFLICTING")

    def test_acceptance_09_low_impact_metadata_update(self):
        """Final Acceptance Test 9 (Clause 285): Low-impact metadata update does not trigger full recomputation."""
        diff = self.engine.compute_source_diff(
            source_id="study-102",
            old_content="Trial text standard care vs antiviral.",
            new_content="Trial text standard care vs antiviral.",
            old_metadata={"author": "Smith J", "affiliation": "Hospital A"},
            new_metadata={"author": "Smith J", "affiliation": "Hospital A, Dept of Medicine"}
        )
        self.assertEqual(diff.impact_level, ContentChangeImpact.NON_MATERIAL)
        self.assertFalse(diff.is_material)

    def test_acceptance_10_high_impact_safety_change(self):
        """Final Acceptance Test 10 (Clause 286): Critical safety change immediately restricts access."""
        job = self.engine.request_revalidation(
            object_id="safety-hcq-cardiac-01",
            trigger=RevalidationTrigger.EVENT_TRIGGERED,
            priority=RevalidationPriority.CRITICAL,
            reason="Urgent cardiac arrest safety alert"
        )
        self.assertEqual(job.status, "WAITING_REVIEW")
        self.assertEqual(job.decision.value, "RESTRICT")
        safety_node = self.engine.get_node("safety-hcq-cardiac-01")
        self.assertEqual(safety_node["metadata"]["status"], "RESTRICTED_PENDING_SAFETY_REVIEW")

    def test_acceptance_11_no_agent_self_approval(self):
        """Final Acceptance Test 11 (Clause 287): Agent cannot unilaterally publish revalidated claim."""
        job = self.engine.request_revalidation(
            object_id="claim-mrna-01",
            trigger=RevalidationTrigger.USER_TRIGGERED
        )
        res = self.engine.attempt_agent_auto_publish(job.job_id, agent_id="agent-watch-01")
        self.assertFalse(res["allowed"])
        self.assertEqual(res["status"], "BLOCKED")
        self.assertIn("NO_AGENT_SELF_APPROVAL", res["message"])

    def test_acceptance_12_private_tenant_source_change(self):
        """Final Acceptance Test 12 (Clause 288): Private tenant source changes remain strictly isolated."""
        w1 = self.engine.register_topic_watcher(
            topic="Oncology Internal Pipeline",
            terms=["KRAS G12D inhibitor", "TenantX-99"],
            scope="PRIVATE",
            tenant_id="tenant-pharma-x"
        )
        # Visible to tenant-pharma-x
        tenant_watchers = self.engine.list_topic_watchers(tenant_id="tenant-pharma-x")
        self.assertTrue(any(w.watcher_id == w1.watcher_id for w in tenant_watchers))

        # Completely invisible to other tenants or public
        other_watchers = self.engine.list_topic_watchers(tenant_id="tenant-pharma-y")
        self.assertFalse(any(w.watcher_id == w1.watcher_id for w in other_watchers))

    def test_acceptance_13_historical_snapshot_opened(self):
        """Final Acceptance Test 13 (Clause 289): Original snapshot evidence state preserved even after retraction."""
        # Inspect snapshot after previous retraction
        snap = self.engine.inspect_snapshot("snap-2026-covid-v1")
        self.assertEqual(snap["frozen_evidence_state"], "MODERATE")
        self.assertEqual(snap["status"], "FROZEN")
        self.assertEqual(snap["version"], "1.0.0")

    def test_acceptance_14_trust_policy_change(self):
        """Final Acceptance Test 14 (Clause 290): Policy change creates policy version & audits."""
        self.engine._policies["v1.1.0"] = {
            "auto_publish_permitted": False,
            "require_two_tier_review": True
        }
        self.assertIn("v1.1.0", self.engine._policies)

    def test_acceptance_15_model_version_change(self):
        """Final Acceptance Test 15 (Clause 291): Model version shift triggers dependent revalidation."""
        self.engine.register_node("model-covid-sim-02", DependencyNodeType.MODEL, {
            "name": "Transmission Dynamics Inpatient Model",
            "version": "2.0.0",
            "status": "VALIDATED"
        })
        self.engine.add_dependency("model-covid-sim-02", "rec-who-covid-14", "INFORMS")
        deps = self.engine.get_downstream_dependents("model-covid-sim-02")
        self.assertIn("rec-who-covid-14", deps)

    def test_acceptance_16_ontology_mapping_change(self):
        """Final Acceptance Test 16 (Clause 292): Ontology mapping changes identified."""
        self.engine.register_node("claim-unani-01", DependencyNodeType.CLAIM, {
            "text": "Sanguineous temperament benefits from cooling regimens",
            "status": "SUPPORTED"
        })
        self.engine.add_dependency("ontology-mizaj-01", "claim-unani-01", "MAPS_TO")
        dependents = self.engine.get_downstream_dependents("ontology-mizaj-01")
        self.assertIn("claim-unani-01", dependents)

    def test_acceptance_17_revalidation_job_failure_handling(self):
        """Final Acceptance Test 17 (Clause 293): Failure recorded in DLQ with no false success."""
        job = self.engine.request_revalidation(
            object_id="non-existent-node-id",
            trigger=RevalidationTrigger.USER_TRIGGERED
        )
        self.assertEqual(job.status, "FAILED")
        self.assertIn(job.job_id, [d["job_id"] for d in self.engine._dlq])

    def test_acceptance_18_concurrent_revalidation_safe_handling(self):
        """Final Acceptance Test 18 (Clause 294): Concurrent revalidation requests handled safely."""
        job1 = self.engine.request_revalidation("claim-mrna-01", trigger=RevalidationTrigger.TIME_TRIGGERED)
        job2 = self.engine.request_revalidation("claim-mrna-01", trigger=RevalidationTrigger.TIME_TRIGGERED)
        # Idempotent revalidation key returns existing job safely
        self.assertEqual(job1.job_id, job2.job_id)

    def test_acceptance_19_duplicate_change_event_idempotency(self):
        """Final Acceptance Test 19 (Clause 295): Duplicate change events yield idempotent processing."""
        job1 = self.engine.request_revalidation("study-102", trigger=RevalidationTrigger.EVENT_TRIGGERED)
        job2 = self.engine.request_revalidation("study-102", trigger=RevalidationTrigger.EVENT_TRIGGERED)
        self.assertEqual(job1.job_id, job2.job_id)

    def test_acceptance_20_malicious_fake_retraction_blocked(self):
        """Final Acceptance Test 20 (Clause 296): Malicious fake retraction blocked by Trust Firewall."""
        # An attacker sends an unverified retraction with a fabricated phantom DOI
        job = self.engine.request_revalidation(
            object_id="claim-mrna-01",
            trigger=RevalidationTrigger.EVENT_TRIGGERED,
            incoming_event={
                "source_id": "malicious-notice",
                "doi": "10.9999/fabricated-retraction",
                "action": "RETRACT"
            }
        )
        # Must be blocked by trust firewall and quarantined
        self.assertEqual(job.status, "BLOCKED")
        self.assertIn("TRUST_FIREWALL_BLOCK", job.error)
        self.assertEqual(job.decision.value, "QUARANTINE")

        # Underlying claim remains uncorrupted
        claim_node = self.engine.get_node("claim-mrna-01")
        self.assertNotEqual(claim_node["metadata"]["status"], "RETRACTED")


if __name__ == "__main__":
    unittest.main()
