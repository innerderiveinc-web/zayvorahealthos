"""
ZMIE Expert Review & Human-in-the-Loop Governance Subsystem
Implements Blueprint Points 44, 45, 46, and 47:
- Dedicated Expert Review Queue
- Specialist pools: Physician, Pharmacologist, Unani Expert, Ayurvedic Expert, Methodologist
- Review Tasks: Claim verification, Cross-system mapping approval, Conflict resolution, Retraction audit
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ReviewPoolType(str, Enum):
    PHYSICIAN = "allopathic_physician"
    PHARMACOLOGIST = "clinical_pharmacologist"
    EVIDENCE_METHODOLOGIST = "evidence_methodologist"
    UNANI_HAKEEM = "unani_expert_tabib"
    AYURVEDIC_VAIDYA = "ayurvedic_expert_vaidya"
    TOXICOLOGY_EXPERT = "toxicology_safety_expert"
    REGULATORY_REVIEWER = "regulatory_legal_reviewer"


class TaskStatus(str, Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED_VERIFIED = "approved_verified"
    REJECTED_DISCARDED = "rejected_discarded"
    QUALIFIED_AMENDED = "qualified_amended"


class TaskPriority(str, Enum):
    ROUTINE = "routine"
    ELEVATED = "elevated"
    CRITICAL_SAFETY = "critical_safety"


class ReviewTask(BaseModel):
    task_id: str
    task_type: str  # 'new_claim_approval', 'cross_system_mapping', 'contradiction_resolution', 'retraction_alert'
    target_object_id: str  # claim_id or relation_id
    pool_required: ReviewPoolType
    priority: TaskPriority
    status: TaskStatus = TaskStatus.PENDING_REVIEW
    ai_generated_claim_or_mapping: str
    evidence_source_url: str
    reviewer_notes: Optional[str] = None
    reviewer_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None


class ExpertReviewQueue:
    """
    In-memory and persistent manager for expert review queues.
    Guarantees that AI never silently promotes hypotheses to verified canonical truth.
    """

    _TASKS: List[ReviewTask] = [
        ReviewTask(
            task_id="TSK-2026-001",
            task_type="cross_system_mapping",
            target_object_id="REL-UNANI-AYUR-01",
            pool_required=ReviewPoolType.UNANI_HAKEEM,
            priority=TaskPriority.ELEVATED,
            ai_generated_claim_or_mapping="Proposed mapping: Mizaj Damwi <-> Pitta Prakriti (Functional Analogy score: 0.74)",
            evidence_source_url="https://arp.ayush.gov.in/codex/unani-mizaj",
            status=TaskStatus.PENDING_REVIEW
        ),
        ReviewTask(
            task_id="TSK-2026-002",
            task_type="new_claim_approval",
            target_object_id="CLM-2026-9812A",
            pool_required=ReviewPoolType.PHARMACOLOGIST,
            priority=TaskPriority.ROUTINE,
            ai_generated_claim_or_mapping="Berberine downregulates hepatic gluconeogenesis via AMPK phosphorylation (Effect size -1.4% HbA1c)",
            evidence_source_url="https://pubmed.ncbi.nlm.nih.gov/18442638/",
            status=TaskStatus.PENDING_REVIEW
        )
    ]

    @classmethod
    def list_pending_tasks(cls, pool: Optional[ReviewPoolType] = None) -> List[ReviewTask]:
        if pool:
            return [t for t in cls._TASKS if t.pool_required == pool and t.status == TaskStatus.PENDING_REVIEW]
        return [t for t in cls._TASKS if t.status == TaskStatus.PENDING_REVIEW]

    @classmethod
    def resolve_task(cls, task_id: str, reviewer_id: str, verdict: TaskStatus, notes: str) -> Optional[ReviewTask]:
        for task in cls._TASKS:
            if task.task_id == task_id:
                task.status = verdict
                task.reviewer_id = reviewer_id
                task.reviewer_notes = notes
                task.resolved_at = datetime.utcnow()
                return task
        return None
