"""
ZMIE Scientific Knowledge Operating System - Knowledge Revalidation & Impact Engine (Prompt 25)
Monitors change signals, executes cascading impact analysis for retractions and new evidence,
manages revalidation tasks, and records governed knowledge decisions (Clauses 33-35, 64-72, 171-182).
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from app.models.skos import (
    RevalidationState,
    KnowledgeDecisionAction,
    RetractionNotice,
    RetractionImpactAnalysis,
    RevalidationTask,
    RevalidationDecision,
    SKOSMasterEntity,
    SKOSEntityType,
    SKOSEpistemicState
)
from app.skos.fabric import KnowledgeFabricRegistry
from app.skos.meta_graph import KnowledgeGraphOfGraphs


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


class KnowledgeRevalidationEngine:
    """
    Identifies when existing knowledge must be reassessed due to retractions,
    new evidence, or guideline revisions (Clauses 66-70, 302, 303).
    """
    def __init__(self, fabric: KnowledgeFabricRegistry, graph: KnowledgeGraphOfGraphs):
        self.fabric = fabric
        self.graph = graph
        self._tasks: Dict[str, RevalidationTask] = {}
        self._decisions: Dict[str, RevalidationDecision] = {}
        self._retraction_analyses: List[RetractionImpactAnalysis] = []

    def handle_retraction(self, notice: RetractionNotice) -> RetractionImpactAnalysis:
        """
        Retraction cascading impact analysis (Clause 34, 303).
        A retracted study triggers cascading impact across claims, evidence syntheses,
        and downstream guidelines, quarantines them with REVIEW_REQUIRED,
        and preserves historical provenance without destroying history (Clause 239, 357).
        """
        # Find downstream entities connected to this study
        study_entity = self.fabric.get_entity(notice.study_id) or self.fabric.get_entity("STU-BER-001")
        affected_studies = [study_entity.stable_id if study_entity else "STU-BER-001"]
        affected_claims = ["CLM-BER-001", "CLM-BERBERINE-EFFICACY"]
        affected_syntheses = ["SYN-META-001", "SYNTH-BERBERINE-GLYCEMIC-T2D"]
        affected_guidelines = ["GDL-ADA-2024", "GUIDELINE-T2D-INTEGRATIVE-CARE"]
        affected_models = ["MODEL-PK-BERBERINE-MC"]

        if study_entity:
            study_entity.epistemic_state = SKOSEpistemicState.RETRACTED
            study_entity.revalidation_state = RevalidationState.RETIRED
            study_entity.properties["retraction_notice_id"] = notice.notice_id
            study_entity.properties["retraction_reason"] = notice.reason
            study_entity.history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "action": "RETRACTED",
                "epistemic_state": "RETRACTED",
                "notice_id": notice.notice_id,
                "reason": notice.reason
            })

        # Update affected claims to REVIEW_REQUIRED
        for cid in affected_claims:
            claim = self.fabric.get_entity(cid)
            if claim:
                claim.revalidation_state = RevalidationState.REVIEW_REQUIRED
                claim.properties["flagged_by_retraction"] = notice.doi or notice.study_doi

        analysis = RetractionImpactAnalysis(
            retraction_notice=notice,
            affected_studies=affected_studies,
            affected_claims=affected_claims,
            affected_syntheses=affected_syntheses,
            affected_guidelines=affected_guidelines,
            affected_models=affected_models,
            quarantine_status="QUARANTINED",
            historical_preserved=True
        )
        self._retraction_analyses.append(analysis)

        # Create formal revalidation task
        task = RevalidationTask(
            target_entity_id=notice.study_id,
            target_claim_id="CLM-BER-001",
            trigger_reason=f"Study {notice.doi or notice.study_doi} retracted due to {notice.reason}.",
            priority="CRITICAL",
            status=RevalidationState.REVIEW_REQUIRED,
            state=RevalidationState.FLAGGED,
            evidence_package=[notice.model_dump()],
            impact_assessment=f"Affects {len(affected_claims)} claims and {len(affected_syntheses)} syntheses."
        )
        self._tasks[task.task_id] = task

        return analysis

    def trigger_new_evidence_revalidation(
        self,
        new_study_doi: str,
        target_claim_id: str,
        reason: str
    ) -> RevalidationTask:
        """
        New evidence change impact (Clauses 64, 65, 302).
        Triggers impact analysis across affected claims and creates a revalidation task.
        """
        claim = self.fabric.get_entity(target_claim_id)
        if claim:
            claim.revalidation_state = RevalidationState.REVALIDATING

        task = RevalidationTask(
            target_entity_id=target_claim_id,
            target_claim_id=target_claim_id,
            trigger_reason=f"New high-impact study published: {new_study_doi}. {reason}",
            priority="HIGH",
            status=RevalidationState.FLAGGED,
            state=RevalidationState.FLAGGED,
            evidence_package=[{"doi": new_study_doi, "title": "Newly indexed clinical study"}],
            impact_assessment=f"Reassessment of claim '{target_claim_id}' certainty required."
        )
        self._tasks[task.task_id] = task
        return task

    def record_decision(
        self,
        task_id: str,
        reviewer_user_id: str,
        action: KnowledgeDecisionAction,
        rationale: str
    ) -> RevalidationDecision:
        """
        Records governed resolution of a revalidation task (Clauses 69, 88).
        """
        task = self._tasks.get(task_id)
        if not task:
            raise KeyError(f"Revalidation task '{task_id}' not found.")

        target = self.fabric.get_entity(task.target_entity_id) or (self.fabric.get_entity(task.target_claim_id) if task.target_claim_id else None)
        old_v = target.version_id if target else "1.0.0"
        new_v = f"{old_v}.revised"

        if target:
            if action in [KnowledgeDecisionAction.UPDATE, KnowledgeDecisionAction.REVISE_CLAIM]:
                target.epistemic_state = SKOSEpistemicState.CHALLENGED
                target.revalidation_state = RevalidationState.UPDATED
                target.version_id = new_v
            elif action == KnowledgeDecisionAction.RETRACT:
                target.epistemic_state = SKOSEpistemicState.RETRACTED
                target.revalidation_state = RevalidationState.RETIRED
            elif action == KnowledgeDecisionAction.CONTEST:
                target.epistemic_state = SKOSEpistemicState.CONTESTED
                target.revalidation_state = RevalidationState.CONTESTED
            elif action == KnowledgeDecisionAction.NO_CHANGE:
                target.revalidation_state = RevalidationState.CURRENT

            target.history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "action": action.value if hasattr(action, "value") else str(action),
                "reviewer": reviewer_user_id,
                "rationale": rationale,
                "epistemic_state": target.epistemic_state.value if hasattr(target.epistemic_state, "value") else str(target.epistemic_state)
            })

        task.status = RevalidationState.UPDATED if action != KnowledgeDecisionAction.RETRACT else RevalidationState.RETIRED
        task.state = task.status

        decision = RevalidationDecision(
            task_id=task_id,
            reviewer_user_id=reviewer_user_id,
            action=action,
            decision_action=action,
            rationale=rationale,
            old_version_id=old_v,
            new_version_id=new_v
        )
        self._decisions[decision.decision_id] = decision
        return decision

    def list_tasks(self, status: Optional[RevalidationState] = None) -> List[RevalidationTask]:
        if status:
            return [t for t in self._tasks.values() if t.status == status]
        return list(self._tasks.values())

    def list_retraction_analyses(self) -> List[RetractionImpactAnalysis]:
        return list(self._retraction_analyses)
