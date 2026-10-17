"""
ZMIE Consent & Privacy Management Engine
Manages:
- Granular, purpose-specific, versioned consent records (ABDM-ready architecture)
- Immediate revocation processing without compromising legal retention obligations
- Data Subject Requests (DSR) lifecycle (Access, Portability, Deletion, Restriction)
- Privacy audit trail
"""

from typing import List, Dict, Any, Optional
import hashlib
from datetime import datetime, timedelta

from app.models.security import (
    ConsentRecord,
    ConsentStatus,
    ConsentPurpose,
    DataSubjectRequest
)
from app.security.audit_engine import AuditLoggingEngine


class ConsentAndPrivacyEngine:
    """
    Manages granular consent contracts and privacy workflows for ZMIE.
    """

    _consent_store: Dict[str, ConsentRecord] = {}
    _dsr_store: Dict[str, DataSubjectRequest] = {}

    @classmethod
    def grant_consent(
        cls,
        subject_id: str,
        purpose: ConsentPurpose,
        scope: str = "DEFAULT",
        policy_version: str = "v1.0",
        expires_in_days: int = 365
    ) -> ConsentRecord:
        """
        Records explicitly granted consent with cryptographic proof hash.
        """
        now = datetime.utcnow()
        expires_at = now + timedelta(days=expires_in_days)
        proof_payload = f"{subject_id}:{purpose.value}:{scope}:{now.isoformat()}"
        proof_hash = hashlib.sha256(proof_payload.encode()).hexdigest()

        rec = ConsentRecord(
            subject_id=subject_id,
            purpose=purpose,
            scope=scope,
            policy_version=policy_version,
            status=ConsentStatus.GRANTED,
            granted_at=now,
            expires_at=expires_at,
            proof_hash=proof_hash
        )
        cls._consent_store[rec.consent_id] = rec

        AuditLoggingEngine.record_event(
            event_type="CONSENT_GRANTED",
            actor_id=subject_id,
            tenant_id="PRIVACY_TENANT",
            resource_type="CONSENT_RECORD",
            resource_id=rec.consent_id,
            action=purpose.value,
            result="GRANTED",
            after_state=proof_hash
        )
        return rec

    @classmethod
    def revoke_consent(cls, consent_id: str, actor_id: str) -> Optional[ConsentRecord]:
        """
        Revokes an existing consent contract, halting future processing.
        """
        rec = cls._consent_store.get(consent_id)
        if not rec:
            return None

        rec.status = ConsentStatus.WITHDRAWN
        rec.withdrawn_at = datetime.utcnow()

        AuditLoggingEngine.record_event(
            event_type="CONSENT_WITHDRAWN",
            actor_id=actor_id,
            tenant_id="PRIVACY_TENANT",
            resource_type="CONSENT_RECORD",
            resource_id=consent_id,
            action=rec.purpose.value,
            result="WITHDRAWN"
        )
        return rec

    @classmethod
    def check_consent(cls, subject_id: str, purpose: ConsentPurpose) -> bool:
        """
        Evaluates whether valid, active, non-expired consent exists for a subject and purpose.
        """
        now = datetime.utcnow()
        for rec in cls._consent_store.values():
            if rec.subject_id == subject_id and rec.purpose == purpose:
                if rec.status == ConsentStatus.GRANTED:
                    if rec.expires_at and rec.expires_at < now:
                        rec.status = ConsentStatus.EXPIRED
                        return False
                    return True
        return False

    @classmethod
    def submit_data_subject_request(
        cls,
        subject_id: str,
        request_type: str,
        scope: str = "ALL"
    ) -> DataSubjectRequest:
        """
        Creates a formal Data Subject Request (Access, Deletion, Restriction).
        """
        req = DataSubjectRequest(
            subject_id=subject_id,
            request_type=request_type.upper(),
            scope=scope,
            status="PENDING",
            submitted_at=datetime.utcnow()
        )
        cls._dsr_store[req.request_id] = req

        AuditLoggingEngine.record_event(
            event_type="DATA_SUBJECT_REQUEST_SUBMITTED",
            actor_id=subject_id,
            tenant_id="PRIVACY_TENANT",
            resource_type="DSR",
            resource_id=req.request_id,
            action=req.request_type,
            result="SUBMITTED"
        )
        return req
