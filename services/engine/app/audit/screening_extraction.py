"""
ZMIE Screening & Data Extraction Audit Manager (Prompt 26)
Enforces standardized exclusion reasons, PRISMA flow compliance, source vs normalized extraction tracking,
and double-extraction discrepancy resolution (Clauses 26-35).
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from app.models.audit import (
    ScreeningDecision,
    ExclusionReason,
    ExtractionRecord,
    ExtractionDisagreement,
    AuditActorType,
)

logger = logging.getLogger("zmie.audit.screening_extraction")


class ScreeningAuditManager:
    """
    Manages and audits systematic screening decisions with strict PRISMA compliance.
    """

    def __init__(self):
        # Key: study_id -> ScreeningDecision
        self._decisions: Dict[str, ScreeningDecision] = {}

    def record_decision(
        self,
        study_id: str,
        study_title: str,
        decision: str,
        screener_id: str = "screener-01",
        screener_type: AuditActorType = AuditActorType.AGENT,
        reason: Optional[ExclusionReason] = None,
        detailed_reason: str = "",
        doi: Optional[str] = None,
        pmid: Optional[str] = None,
        criteria_used: Optional[List[str]] = None,
        is_duplicate: bool = False,
        duplicate_of_id: Optional[str] = None,
    ) -> ScreeningDecision:
        """
        Records a screening decision.
        If decision is EXCLUDED, reason MUST be specified.
        """
        decision_upper = decision.upper()
        if decision_upper == "EXCLUDED" and reason is None:
            raise ValueError(
                f"Exclusion of study '{study_title}' ({study_id}) requires an explicit ExclusionReason. "
                "Unjustified exclusion is prohibited in research audit."
            )

        rec = ScreeningDecision(
            study_id=study_id,
            study_title=study_title,
            doi=doi,
            pmid=pmid,
            decision=decision_upper,
            reason=reason,
            detailed_reason=detailed_reason,
            screener_id=screener_id,
            screener_type=screener_type,
            criteria_used=criteria_used or [],
            is_duplicate=is_duplicate,
            duplicate_of_id=duplicate_of_id,
            timestamp=datetime.utcnow()
        )
        self._decisions[study_id] = rec
        return rec

    def get_decision(self, study_id: str) -> Optional[ScreeningDecision]:
        return self._decisions.get(study_id)

    def list_decisions(self) -> List[ScreeningDecision]:
        return list(self._decisions.values())

    def get_prisma_flow_summary(self) -> Dict[str, Any]:
        """Generates PRISMA-compliant screening flow statistics."""
        total = len(self._decisions)
        included = sum(1 for d in self._decisions.values() if d.decision == "INCLUDED")
        excluded = sum(1 for d in self._decisions.values() if d.decision == "EXCLUDED")
        uncertain = sum(1 for d in self._decisions.values() if d.decision == "UNCERTAIN")
        duplicates = sum(1 for d in self._decisions.values() if d.is_duplicate)

        reasons_breakdown: Dict[str, int] = {}
        for d in self._decisions.values():
            if d.decision == "EXCLUDED" and d.reason:
                val = d.reason.value if hasattr(d.reason, "value") else str(d.reason)
                reasons_breakdown[val] = reasons_breakdown.get(val, 0) + 1

        return {
            "total_screened": total,
            "included": included,
            "excluded": excluded,
            "uncertain": uncertain,
            "duplicates_removed": duplicates,
            "exclusion_reasons": reasons_breakdown
        }


class ExtractionAuditManager:
    """
    Manages data extractions and double-extraction discrepancy reconciliation.
    Preserves exact original source text alongside normalized values.
    """

    def __init__(self):
        self._extractions: Dict[str, ExtractionRecord] = {}
        self._disagreements: Dict[str, ExtractionDisagreement] = {}

    def record_extraction(
        self,
        study_id: str,
        field_name: str,
        original_source_value: Any,
        normalized_value: Any,
        normalization_method: str = "DIRECT_CONVERSION",
        unit: Optional[str] = None,
        page_or_table: Optional[str] = None,
        extractor_id: str = "extractor-01",
        extractor_type: AuditActorType = AuditActorType.AGENT,
        review_state: str = "UNVERIFIED"
    ) -> ExtractionRecord:
        """Records an auditable extraction item."""
        rec = ExtractionRecord(
            study_id=study_id,
            field_name=field_name,
            original_source_value=original_source_value,
            normalized_value=normalized_value,
            normalization_method=normalization_method,
            unit=unit,
            page_or_table=page_or_table,
            extractor_id=extractor_id,
            extractor_type=extractor_type,
            review_state=review_state,
            timestamp=datetime.utcnow()
        )
        self._extractions[rec.record_id] = rec
        return rec

    def get_extractions_for_study(self, study_id: str) -> List[ExtractionRecord]:
        return [e for e in self._extractions.values() if e.study_id == study_id]

    def record_double_extraction(
        self,
        study_id: str,
        field_name: str,
        reviewer_a_id: str,
        reviewer_a_val: Any,
        reviewer_b_id: str,
        reviewer_b_val: Any
    ) -> Optional[ExtractionDisagreement]:
        """
        Compares extractions from two independent reviewers.
        If values differ, registers an ExtractionDisagreement for board resolution.
        """
        if reviewer_a_val == reviewer_b_val:
            # Consensus reached immediately
            self.record_extraction(
                study_id=study_id,
                field_name=field_name,
                original_source_value=reviewer_a_val,
                normalized_value=reviewer_a_val,
                extractor_id=f"{reviewer_a_id}+{reviewer_b_id}",
                review_state="CONSENSUS_VERIFIED"
            )
            return None

        disagreement = ExtractionDisagreement(
            field_name=field_name,
            study_id=study_id,
            reviewer_a_id=reviewer_a_id,
            reviewer_a_val=reviewer_a_val,
            reviewer_b_id=reviewer_b_id,
            reviewer_b_val=reviewer_b_val,
            resolved=False
        )
        self._disagreements[disagreement.disagreement_id] = disagreement
        logger.warning(
            f"Extraction disagreement detected on study {study_id}, field '{field_name}': "
            f"'{reviewer_a_val}' vs '{reviewer_b_val}'"
        )
        return disagreement

    def resolve_disagreement(
        self,
        disagreement_id: str,
        resolution_val: Any,
        resolver_id: str,
        rationale: str
    ) -> ExtractionDisagreement:
        """Documents formal resolution of an extraction discrepancy."""
        if disagreement_id not in self._disagreements:
            raise KeyError(f"Disagreement {disagreement_id} not found.")

        dis = self._disagreements[disagreement_id]
        dis.resolution_val = resolution_val
        dis.resolver_id = resolver_id
        dis.rationale = rationale
        dis.resolved = True
        dis.timestamp = datetime.utcnow()

        # Update extraction repository with the resolved value
        self.record_extraction(
            study_id=dis.study_id,
            field_name=dis.field_name,
            original_source_value=f"RESOLVED: {resolution_val}",
            normalized_value=resolution_val,
            normalization_method="CONSENSUS_ADJUDICATION",
            extractor_id=resolver_id,
            review_state="ADJUDICATED"
        )

        logger.info(f"Resolved extraction disagreement {disagreement_id} by {resolver_id}")
        return dis

    def get_open_disagreements(self) -> List[ExtractionDisagreement]:
        return [d for d in self._disagreements.values() if not d.resolved]
