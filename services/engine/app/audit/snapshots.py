"""
ZMIE Research Snapshot Storage & Immutability Engine (Prompt 26)
Guarantees strict immutability of publication-grade research states,
manages parent-child snapshot lineage, and computes scientific answer diffs (Clauses 5-9, 94-96, 280).
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import copy
import logging

from app.models.audit import ResearchSnapshot, ScientificAnswerDiff, ResearchStatus

logger = logging.getLogger("zmie.audit.snapshots")


class SnapshotManager:
    """
    Manages immutable Research Snapshots.
    Publication-grade snapshots are locked and can NEVER be overwritten.
    Any correction or evolutionary change must create a new child snapshot.
    """

    def __init__(self):
        self._snapshots: Dict[str, ResearchSnapshot] = {}

    def save_snapshot(self, snapshot: ResearchSnapshot) -> ResearchSnapshot:
        """Saves a new research snapshot, locking it by default."""
        if snapshot.snapshot_id in self._snapshots:
            existing = self._snapshots[snapshot.snapshot_id]
            if existing.is_locked:
                raise ValueError(
                    f"Snapshot {snapshot.snapshot_id} is locked and immutable. "
                    "In-place modifications are strictly prohibited. Create a child snapshot instead."
                )
        # Ensure locked and manifest hash computed
        snapshot.is_locked = True
        if not snapshot.manifest_hash:
            snapshot.manifest_hash = snapshot.compute_manifest_hash()
        self._snapshots[snapshot.snapshot_id] = snapshot
        logger.info(f"Saved immutable snapshot {snapshot.snapshot_id} (version {snapshot.version})")
        return snapshot

    def get_snapshot(self, snapshot_id: str) -> Optional[ResearchSnapshot]:
        """Retrieves a snapshot by ID."""
        return self._snapshots.get(snapshot_id)

    def list_snapshots(
        self,
        project_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        status: Optional[ResearchStatus] = None,
    ) -> List[ResearchSnapshot]:
        """Lists snapshots with optional filtering."""
        results = []
        for snap in self._snapshots.values():
            if project_id and snap.project_id != project_id:
                continue
            if tenant_id and snap.tenant_id != tenant_id:
                continue
            if status and snap.status != status:
                continue
            results.append(snap)
        return results

    def create_child_snapshot(
        self,
        parent_snapshot_id: str,
        updates: Dict[str, Any],
        created_by: str = "zmie-research-updater",
        version_bump: str = "minor"
    ) -> ResearchSnapshot:
        """
        Creates an immutable child snapshot derived from an existing parent snapshot.
        Enforces provenance lineage without modifying the parent.
        """
        parent = self.get_snapshot(parent_snapshot_id)
        if not parent:
            raise KeyError(f"Parent snapshot {parent_snapshot_id} does not exist.")

        # Compute next version
        old_ver = parent.version
        parts = [int(p) for p in old_ver.split(".") if p.isdigit()]
        if len(parts) != 3:
            parts = [1, 0, 0]

        if version_bump == "major":
            new_version = f"{parts[0] + 1}.0.0"
        elif version_bump == "minor":
            new_version = f"{parts[0]}.{parts[1] + 1}.0"
        else:
            new_version = f"{parts[0]}.{parts[1]}.{parts[2] + 1}"

        # Shallow copy dictionary of parent data
        data = parent.model_dump()
        # Apply updates
        data.update(updates)

        # Update metadata for child
        import uuid
        data["snapshot_id"] = f"rs-{uuid.uuid4().hex[:12]}"
        data["parent_snapshot_id"] = parent.snapshot_id
        data["version"] = new_version
        data["created_at"] = datetime.utcnow()
        data["created_by"] = created_by
        data["is_locked"] = True
        data["manifest_hash"] = ""  # Trigger recomputation

        child = ResearchSnapshot(**data)
        child.manifest_hash = child.compute_manifest_hash()
        self._snapshots[child.snapshot_id] = child
        logger.info(f"Created child snapshot {child.snapshot_id} (v{child.version}) from parent {parent_snapshot_id}")
        return child

    def get_lineage(self, snapshot_id: str) -> List[ResearchSnapshot]:
        """Returns the full ancestry chain from the genesis root to the given snapshot."""
        lineage = []
        curr_id = snapshot_id
        visited = set()

        while curr_id and curr_id not in visited:
            visited.add(curr_id)
            snap = self.get_snapshot(curr_id)
            if not snap:
                break
            lineage.append(snap)
            curr_id = snap.parent_snapshot_id

        lineage.reverse()  # Oldest root first, requested snapshot last
        return lineage

    def compute_answer_diff(
        self,
        old_snapshot_id: str,
        new_snapshot_id: str
    ) -> ScientificAnswerDiff:
        """
        Computes a structured diff explaining why and how scientific answers and conclusions
        evolved between two snapshots (Clauses 94-96).
        """
        old_snap = self.get_snapshot(old_snapshot_id)
        new_snap = self.get_snapshot(new_snapshot_id)

        if not old_snap:
            raise KeyError(f"Old snapshot {old_snapshot_id} not found.")
        if not new_snap:
            raise KeyError(f"New snapshot {new_snapshot_id} not found.")

        old_out = old_snap.final_output.get("conclusion") or old_snap.final_output.get("summary") or "Baseline scientific synthesis"
        new_out = new_snap.final_output.get("conclusion") or new_snap.final_output.get("summary") or "Updated scientific synthesis"

        # Evidence diff
        old_evidence_ids = {e.get("study_id") or e.get("id") or str(idx): e for idx, e in enumerate(old_snap.evidence_items)}
        new_evidence_ids = {e.get("study_id") or e.get("id") or str(idx): e for idx, e in enumerate(new_snap.evidence_items)}

        added_studies = [e for k, e in new_evidence_ids.items() if k not in old_evidence_ids]
        removed_studies = [e for k, e in old_evidence_ids.items() if k not in new_evidence_ids]

        evidence_diff = []
        for s in added_studies:
            evidence_diff.append({"action": "STUDY_ADDED", "title": s.get("title", "Untitled"), "id": s.get("study_id")})
        for s in removed_studies:
            evidence_diff.append({"action": "STUDY_REMOVED_OR_RETRACTED", "title": s.get("title", "Untitled"), "id": s.get("study_id")})

        # Upstream causes
        causes = []
        if added_studies:
            causes.append(f"Added {len(added_studies)} newly published evidence studies.")
        if removed_studies:
            causes.append(f"Removed or retracted {len(removed_studies)} previously included studies.")
        if old_snap.code_provenance and new_snap.code_provenance and old_snap.code_provenance.checksum != new_snap.code_provenance.checksum:
            causes.append("Computational analysis code pipeline was updated.")
        if old_snap.environment.random_seed != new_snap.environment.random_seed:
            causes.append("Computational random seed changed.")

        summary = (
            f"Transition from v{old_snap.version} to v{new_snap.version}: "
            f"{len(causes)} upstream factors identified affecting conclusions."
        )

        return ScientificAnswerDiff(
            old_snapshot_id=old_snapshot_id,
            new_snapshot_id=new_snapshot_id,
            question=new_snap.research_question,
            old_conclusion=str(old_out),
            new_conclusion=str(new_out),
            changes_summary=summary,
            upstream_causes=causes or ["No major structural variance detected."],
            evidence_diff=evidence_diff,
            data_diff=[],
            code_diff=[]
        )
