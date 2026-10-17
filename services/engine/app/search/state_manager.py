"""
ZMIE Search State, History, Snapshots & Alerts Engine (Sections 54-60)
Supports:
1. Private search history & telemetry
2. Saved search queries with parameters
3. Search alerts for continuous surveillance
4. Search Snapshots (freezes exact query & results state for research reproducibility)
5. "What Changed?" search diff engine
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from pydantic import BaseModel, Field

from app.search.search_modes import SearchModeResult


class SavedSearchRecord(BaseModel):
    saved_id: str = Field(default_factory=lambda: f"SAVED-{uuid.uuid4().hex[:8].upper()}")
    user_id: str
    query_text: str
    mode: str
    filters: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SearchAlertSubscription(BaseModel):
    alert_id: str = Field(default_factory=lambda: f"ALERT-{uuid.uuid4().hex[:8].upper()}")
    user_id: str
    query_topic: str
    target_evidence_level: str = "E6_controlled_clinical_evidence"
    frequency: str = "daily" # daily, weekly
    is_active: bool = True
    last_triggered_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SearchSnapshot(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: f"SNAP-{uuid.uuid4().hex[:8].upper()}")
    query_text: str
    knowledge_version: str = "2026.1"
    ranking_version: str = "v1.2.0"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    result_document_ids: List[str] = Field(default_factory=list)
    top_results_summary: List[Dict[str, Any]] = Field(default_factory=list)


class SearchStateManager:
    """
    Manages user search state, persistent snapshots, and surveillance alerts.
    """

    def __init__(self):
        self._history: List[Dict[str, Any]] = []
        self._saved_searches: Dict[str, SavedSearchRecord] = {}
        self._alerts: Dict[str, SearchAlertSubscription] = {}
        self._snapshots: Dict[str, SearchSnapshot] = {}

    def record_history(self, user_id: str, query: str, mode: str, result_count: int):
        self._history.append({
            "history_id": f"HIST-{uuid.uuid4().hex[:8].upper()}",
            "user_id": user_id,
            "query": query,
            "mode": mode,
            "result_count": result_count,
            "timestamp": datetime.utcnow()
        })

    def get_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        user_hist = [h for h in self._history if h["user_id"] == user_id]
        return user_hist[-limit:]

    def save_search(self, user_id: str, query: str, mode: str, filters: Optional[Dict[str, Any]] = None) -> SavedSearchRecord:
        record = SavedSearchRecord(
            user_id=user_id,
            query_text=query,
            mode=mode,
            filters=filters or {}
        )
        self._saved_searches[record.saved_id] = record
        return record

    def get_saved_searches(self, user_id: str) -> List[SavedSearchRecord]:
        return [s for s in self._saved_searches.values() if s.user_id == user_id]

    def create_alert(self, user_id: str, topic: str, min_level: str = "E6_controlled_clinical_evidence") -> SearchAlertSubscription:
        alert = SearchAlertSubscription(
            user_id=user_id,
            query_topic=topic,
            target_evidence_level=min_level
        )
        self._alerts[alert.alert_id] = alert
        return alert

    def get_alerts(self, user_id: str) -> List[SearchAlertSubscription]:
        return [a for a in self._alerts.values() if a.user_id == user_id]

    def create_snapshot(self, result: SearchModeResult) -> SearchSnapshot:
        """
        Signature Feature: Freeze exact search state for research reproducibility (Section 58).
        """
        doc_ids = [r.candidate.document_id for r in result.ranked_results]
        summaries = [
            {
                "document_id": r.candidate.document_id,
                "title": r.candidate.title,
                "score": r.final_score,
                "evidence_level": r.candidate.evidence_level
            }
            for r in result.ranked_results[:5]
        ]

        snap = SearchSnapshot(
            query_text=result.query,
            result_document_ids=doc_ids,
            top_results_summary=summaries
        )
        self._snapshots[snap.snapshot_id] = snap
        return snap

    def get_snapshot(self, snapshot_id: str) -> Optional[SearchSnapshot]:
        return self._snapshots.get(snapshot_id)

    def diff_snapshots(self, snapshot_id_a: str, snapshot_id_b: str) -> Dict[str, Any]:
        """
        Signature Feature: "What Changed?" Search Diff (Section 59).
        """
        snap_a = self.get_snapshot(snapshot_id_a)
        snap_b = self.get_snapshot(snapshot_id_b)

        if not snap_a or not snap_b:
            return {"error": "Both snapshots must exist to compute diff."}

        set_a = set(snap_a.result_document_ids)
        set_b = set(snap_b.result_document_ids)

        new_docs = list(set_b - set_a)
        removed_docs = list(set_a - set_b)
        retained_docs = list(set_a & set_b)

        return {
            "snapshot_a": snapshot_id_a,
            "snapshot_b": snapshot_id_b,
            "query": snap_b.query_text,
            "new_studies_indexed": new_docs,
            "removed_or_superseded_studies": removed_docs,
            "unchanged_studies": retained_docs,
            "summary": f"Detected {len(new_docs)} newly indexed studies and {len(removed_docs)} superseded/removed studies."
        }
