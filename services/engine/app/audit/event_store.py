"""
ZMIE Audit Event Store & Tamper-Evident Hash Chain (Prompt 26)
Maintains append-only audit event streams with cryptographic SHA256 chaining.
Guarantees full tamper detection and event sequence verification (Clauses 11-14, 225, 262).
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib
import logging

from app.models.audit import AuditEvent, AuditEventType, AuditActorType

logger = logging.getLogger("zmie.audit.event_store")


class AuditEventStore:
    """
    Cryptographically chained, append-only audit event store.
    Guarantees that once an event is recorded, any mutation, deletion, or reordering
    is immediately detected by verify_chain().
    """

    def __init__(self):
        # Key: audit_id -> List of AuditEvent
        self._chains: Dict[str, List[AuditEvent]] = {}

    def record_event(
        self,
        audit_id: str,
        action: AuditEventType,
        resource_type: str,
        resource_id: str,
        actor_type: AuditActorType = AuditActorType.AGENT,
        actor_id: str = "agent-researcher-01",
        before_state: Optional[Dict[str, Any]] = None,
        after_state: Optional[Dict[str, Any]] = None,
        reason: str = "",
        agent_id: Optional[str] = None,
        model_id: Optional[str] = None,
        tool_id: Optional[str] = None,
        policy_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> AuditEvent:
        """
        Appends a new event to the specified audit hash chain.
        Automatically links to previous event hash.
        """
        if audit_id not in self._chains:
            self._chains[audit_id] = []

        chain = self._chains[audit_id]
        if chain:
            previous_hash = chain[-1].event_hash
        else:
            previous_hash = "GENESIS_EVENT"

        event = AuditEvent(
            audit_id=audit_id,
            timestamp=datetime.utcnow(),
            actor_type=actor_type,
            actor_id=actor_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            before_state=before_state,
            after_state=after_state,
            reason=reason,
            agent_id=agent_id,
            model_id=model_id,
            tool_id=tool_id,
            policy_id=policy_id,
            tenant_id=tenant_id,
            project_id=project_id,
            previous_event_hash=previous_hash,
        )

        chain.append(event)
        logger.debug(f"Recorded audit event {event.event_id} on chain {audit_id}: {action.value}")
        return event

    def get_events(
        self,
        audit_id: str,
        resource_id: Optional[str] = None,
        action: Optional[AuditEventType] = None,
        actor_id: Optional[str] = None,
        limit: int = 1000
    ) -> List[AuditEvent]:
        """Queries events in an audit chain with optional filters."""
        chain = self._chains.get(audit_id, [])
        results = []
        for ev in chain:
            if resource_id and ev.resource_id != resource_id:
                continue
            if action and ev.action != action:
                continue
            if actor_id and ev.actor_id != actor_id:
                continue
            results.append(ev)
            if len(results) >= limit:
                break
        return results

    def verify_chain(self, audit_id: str) -> Dict[str, Any]:
        """
        Rigorously verifies cryptographic hash integrity and causal sequence of an audit chain.
        Returns a verification report indicating whether the chain is tamper-free.
        """
        chain = self._chains.get(audit_id, [])
        if not chain:
            return {
                "audit_id": audit_id,
                "is_valid": True,
                "total_events": 0,
                "tampered": False,
                "message": "Empty chain (no events recorded)."
            }

        expected_previous_hash = "GENESIS_EVENT"

        for idx, event in enumerate(chain):
            # Check 1: Previous hash link
            if event.previous_event_hash != expected_previous_hash:
                return {
                    "audit_id": audit_id,
                    "is_valid": False,
                    "tampered": True,
                    "failed_step": idx,
                    "event_id": event.event_id,
                    "error": "CHAIN_BROKEN_PREVIOUS_HASH_MISMATCH",
                    "expected_previous": expected_previous_hash,
                    "actual_previous": event.previous_event_hash,
                    "message": f"Tamper detected at event index {idx}: previous event hash mismatch."
                }

            # Check 2: Event hash recalculation
            recomputed = event.compute_hash()
            if event.event_hash != recomputed:
                return {
                    "audit_id": audit_id,
                    "is_valid": False,
                    "tampered": True,
                    "failed_step": idx,
                    "event_id": event.event_id,
                    "error": "EVENT_HASH_MUTATED",
                    "expected_hash": recomputed,
                    "actual_hash": event.event_hash,
                    "message": f"Tamper detected at event index {idx}: stored event hash does not match content."
                }

            expected_previous_hash = event.event_hash

        return {
            "audit_id": audit_id,
            "is_valid": True,
            "total_events": len(chain),
            "tampered": False,
            "head_hash": chain[-1].event_hash,
            "genesis_verified": True,
            "message": "Audit chain is valid, continuous, and cryptographically tamper-free."
        }

    def corrupt_event_for_testing(self, audit_id: str, event_index: int, new_action: AuditEventType) -> bool:
        """Utility for security red-team tests to simulate unauthorized tampering."""
        chain = self._chains.get(audit_id, [])
        if 0 <= event_index < len(chain):
            chain[event_index].action = new_action
            return True
        return False
