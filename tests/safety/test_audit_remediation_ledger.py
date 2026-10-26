"""
Test Suite Verifying Phase 4 Audit Remediation:
- Audit ledger hash covers metadata, previous_state, and new_state (tamper detection)
- Strict genesis validation (genesis hash only allowed at block 0)
- Immutable append-only audit persistence
- Research job persistence preserves pico and created_at fields
- Live /health diagnostic reporting
"""

import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.core.audit import AuditDispatcher, AuditAction, ActorType, get_audit_dispatcher
from app.db.local_storage import LocalPersistentStore


class TestAuditRemediationLedger(unittest.TestCase):

    def test_01_metadata_tampering_detected(self):
        """Modifying event metadata must invalidate cryptographic audit integrity."""
        dispatcher = AuditDispatcher(load_persisted=False)
        ev = dispatcher.dispatch(
            actor="dr_ashraf",
            actor_type=ActorType.USER,
            tenant_id="tenant-aiims",
            object_type="MONOGRAPH",
            object_id="berberine-01",
            action=AuditAction.UPDATE,
            metadata={"reviewed_by": "Dr. Irfan", "version": "1.0"}
        )
        self.assertTrue(dispatcher.verify_integrity())

        # Tamper with metadata
        ev.metadata["version"] = "2.0_UNAUTHORIZED"
        self.assertFalse(
            dispatcher.verify_integrity(),
            "Tampered metadata must cause verify_integrity() to return False"
        )

    def test_02_state_tampering_detected(self):
        """Modifying previous_state or new_state must invalidate audit integrity."""
        dispatcher = AuditDispatcher(load_persisted=False)
        ev = dispatcher.dispatch(
            actor="dr_ashraf",
            actor_type=ActorType.USER,
            tenant_id="tenant-aiims",
            object_type="PRESCRIPTION",
            object_id="rx-101",
            action=AuditAction.CREATE,
            previous_state={"dose": "250mg"},
            new_state={"dose": "500mg"}
        )
        self.assertTrue(dispatcher.verify_integrity())

        # Tamper with new_state
        ev.new_state["dose"] = "1000mg_FORGED"
        self.assertFalse(
            dispatcher.verify_integrity(),
            "Tampered state transition must cause verify_integrity() to return False"
        )

    def test_03_misplaced_genesis_hash_fails(self):
        """A block at index > 0 asserting GENESIS_BLOCK must fail integrity."""
        dispatcher = AuditDispatcher(load_persisted=False)
        dispatcher.dispatch(
            actor="admin",
            actor_type=ActorType.SYSTEM,
            tenant_id="org-system",
            object_type="SYSTEM",
            object_id="sys-01",
            action=AuditAction.CREATE
        )
        ev2 = dispatcher.dispatch(
            actor="admin",
            actor_type=ActorType.SYSTEM,
            tenant_id="org-system",
            object_type="SYSTEM",
            object_id="sys-02",
            action=AuditAction.CREATE
        )
        self.assertTrue(dispatcher.verify_integrity())

        # Forge block 2 to assert genesis hash
        ev2.prev_hash = "GENESIS_BLOCK_00000000000000000000000000000000"
        self.assertFalse(
            dispatcher.verify_integrity(),
            "Misplaced genesis hash in non-genesis block must fail integrity verification"
        )

    def test_04_research_job_pico_and_timestamp_persisted(self):
        """LocalPersistentStore must save and load pico_json and created_at fields."""
        store = LocalPersistentStore.get_instance()
        job_id = "test-job-pico-999"
        job_data = {
            "pico": {"population": "Adults T2D", "intervention": "Berberine 500mg BID"},
            "plan": {"stages": 3},
            "report": {"summary": "Safe and effective"},
            "created_at": "2026-10-21T12:00:00Z"
        }
        store.save_research_job(job_id, "Comparative Efficacy", "COMPLETED", job_data)
        
        all_jobs = store.load_all_research_jobs()
        matched = [j for j in all_jobs if j["job_id"] == job_id]
        self.assertTrue(len(matched) > 0)
        self.assertEqual(matched[0]["pico"]["population"], "Adults T2D")
        self.assertEqual(matched[0]["created_at"], "2026-10-21T12:00:00Z")

    def test_05_health_endpoints_live_state(self):
        """Health endpoints must return live subsystem diagnostics."""
        client = TestClient(app)
        r_health = client.get("/health")
        self.assertEqual(r_health.status_code, 200)
        self.assertIn(r_health.json()["status"], ("healthy", "degraded"))
        self.assertIn("subsystems", r_health.json())

        r_deep = client.get("/health/deep")
        self.assertEqual(r_deep.status_code, 200)
        self.assertIn("local_storage_db", r_deep.json()["diagnostics"])


if __name__ == "__main__":
    unittest.main()
