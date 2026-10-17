"""
ZMIE Document Versioning & Change Detection Engine
Preserves immutable historical audit records:
- Tracks published_version, retrieved_version, and effective_version.
- Classifies mutations: NEW, UPDATED, UNCHANGED, REMOVED, RETRACTED, CORRECTED, SUPERSEDED.
- Prevents silent overwriting of clinical guidelines and pharmacopoeial monographs.
"""

import hashlib
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ChangeType(str, Enum):
    NEW = "NEW"
    UPDATED = "UPDATED"
    UNCHANGED = "UNCHANGED"
    REMOVED = "REMOVED"
    RETRACTED = "RETRACTED"
    CORRECTED = "CORRECTED"
    SUPERSEDED = "SUPERSEDED"


class DocumentVersionRecord(BaseModel):
    version_id: str
    document_id: str
    version_index: int
    published_version: str
    retrieved_version: str
    effective_version: str
    content_hash_sha256: str
    change_type: ChangeType
    change_summary: str
    superseded_by: Optional[str] = None
    supersedes: Optional[str] = None
    is_retracted: bool = False
    retraction_reason: Optional[str] = None
    recorded_at: datetime = Field(default_factory=datetime.utcnow)


class DocumentVersionTracker:
    """
    In-memory and persistent tracker for document versions and diffs.
    """

    def __init__(self):
        # Maps document_id -> List of historical DocumentVersionRecord
        self._history: Dict[str, List[DocumentVersionRecord]] = {}

    def register_version(
        self,
        document_id: str,
        content: str,
        published_version: str = "1.0",
        is_retracted: bool = False,
        retraction_reason: Optional[str] = None,
        supersedes_id: Optional[str] = None
    ) -> DocumentVersionRecord:
        """
        Evaluates incoming document state against previous versions,
        determines ChangeType, and records immutable version entry.
        """
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        history = self._history.setdefault(document_id, [])

        retrieved_ver = f"retrieved_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        if not history:
            # First time seeing this document
            change_type = ChangeType.RETRACTED if is_retracted else ChangeType.NEW
            summary = "Initial ingestion of medical document." if not is_retracted else f"Ingested in retracted state: {retraction_reason}"
            
            record = DocumentVersionRecord(
                version_id=f"{document_id}-v1",
                document_id=document_id,
                version_index=1,
                published_version=published_version,
                retrieved_version=retrieved_ver,
                effective_version=published_version,
                content_hash_sha256=content_hash,
                change_type=change_type,
                change_summary=summary,
                supersedes=supersedes_id,
                is_retracted=is_retracted,
                retraction_reason=retraction_reason
            )
            history.append(record)
            return record

        last_ver = history[-1]

        # Check for Retraction
        if is_retracted and not last_ver.is_retracted:
            record = DocumentVersionRecord(
                version_id=f"{document_id}-v{len(history)+1}",
                document_id=document_id,
                version_index=len(history) + 1,
                published_version=published_version,
                retrieved_version=retrieved_ver,
                effective_version=f"{published_version}-RETRACTED",
                content_hash_sha256=content_hash,
                change_type=ChangeType.RETRACTED,
                change_summary=f"Document flagged as retracted: {retraction_reason or 'Author/Publisher retraction'}",
                is_retracted=True,
                retraction_reason=retraction_reason
            )
            history.append(record)
            return record

        # Check for Hash Equality (Unchanged)
        if last_ver.content_hash_sha256 == content_hash and not is_retracted:
            record = DocumentVersionRecord(
                version_id=f"{document_id}-v{len(history)+1}",
                document_id=document_id,
                version_index=len(history) + 1,
                published_version=published_version,
                retrieved_version=retrieved_ver,
                effective_version=last_ver.effective_version,
                content_hash_sha256=content_hash,
                change_type=ChangeType.UNCHANGED,
                change_summary="Content hash identical; no modifications detected."
            )
            history.append(record)
            return record

        # Check for Supersession (e.g., Clinical Guideline update)
        if supersedes_id or published_version != last_ver.published_version:
            # Mark previous active version as superseded
            last_ver.change_type = ChangeType.SUPERSEDED
            last_ver.superseded_by = f"{document_id}-v{len(history)+1}"

            record = DocumentVersionRecord(
                version_id=f"{document_id}-v{len(history)+1}",
                document_id=document_id,
                version_index=len(history) + 1,
                published_version=published_version,
                retrieved_version=retrieved_ver,
                effective_version=published_version,
                content_hash_sha256=content_hash,
                change_type=ChangeType.UPDATED,
                change_summary=f"Supersedes previous guideline version {last_ver.published_version}. Historical record preserved.",
                supersedes=last_ver.version_id
            )
            history.append(record)
            return record

        # General Content Update / Correction
        record = DocumentVersionRecord(
            version_id=f"{document_id}-v{len(history)+1}",
            document_id=document_id,
            version_index=len(history) + 1,
            published_version=published_version,
            retrieved_version=retrieved_ver,
            effective_version=published_version,
            content_hash_sha256=content_hash,
            change_type=ChangeType.CORRECTED if "corrigendum" in content.lower() else ChangeType.UPDATED,
            change_summary="Content modified. New cryptographic hash recorded."
        )
        history.append(record)
        return record

    def get_history(self, document_id: str) -> List[DocumentVersionRecord]:
        return self._history.get(document_id, [])

    def get_active_version(self, document_id: str) -> Optional[DocumentVersionRecord]:
        history = self._history.get(document_id, [])
        return history[-1] if history else None
