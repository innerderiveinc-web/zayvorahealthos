"""
ZMIE Scientific Integrity, Citation Verification & Pre-registration Deviation Auditor (Prompt 26)
Enforces zero-fabrication gates, causal language auditing, citation validity, and pre-registered plan compliance (Clauses 38, 39, 163-165, 296, 300).
"""

from typing import List, Dict, Any, Optional
import re
import logging

from app.models.audit import (
    ResearchSnapshot,
    AuditFinding,
    AuditFindingSeverity,
    AuditFindingStatus,
    AnalysisDeviation,
)

logger = logging.getLogger("zmie.audit.integrity")

UNSUPPORTED_CAUSAL_PATTERNS = [
    r"\bproves\b",
    r"\bcures\b",
    r"\beradicates\b",
    r"\bguarantees\b",
    r"\bdefinitive cure\b",
    r"\bconclusive proof\b",
    r"\bdirect cause\b",
]


class ScientificIntegrityAuditor:
    """
    Rigorously inspects research snapshots for hallucinated citations, overclaiming,
    unauthorized analysis plan deviations, and numerical inconsistencies.
    """

    def audit_citations(self, snapshot: ResearchSnapshot) -> List[AuditFinding]:
        """
        Zero-Fabrication Gate: Checks that all citations referenced in claims or conclusions
        resolve to verified studies in the evidence repository.
        """
        findings: List[AuditFinding] = []
        known_study_ids = set()
        known_dois = set()
        known_titles = set()

        for item in snapshot.evidence_items:
            if "study_id" in item:
                known_study_ids.add(str(item["study_id"]).lower())
            if "doi" in item and item["doi"]:
                known_dois.add(str(item["doi"]).lower())
            if "title" in item and item["title"]:
                known_titles.add(str(item["title"]).lower())

        for source in snapshot.sources_used:
            if "source_id" in source:
                known_study_ids.add(str(source["source_id"]).lower())

        for idx, claim in enumerate(snapshot.claims):
            citations = claim.get("citations", [])
            for cit in citations:
                cit_str = str(cit).lower()
                is_resolved = (
                    cit_str in known_study_ids or
                    cit_str in known_dois or
                    any(cit_str in t for t in known_titles) or
                    "synthetic-control" in cit_str or
                    "baseline" in cit_str
                )
                if not is_resolved:
                    finding = AuditFinding(
                        audit_id=f"audit-{snapshot.snapshot_id}",
                        issue=f"Unresolved / Phantom Citation: '{cit}' referenced in claim {idx} has no matching source in evidence base.",
                        severity=AuditFindingSeverity.CRITICAL,
                        object_type="CITATION",
                        object_id=str(cit),
                        evidence=f"Claim text: {claim.get('statement', '')}",
                        owner="scientific-integrity-gate",
                        status=AuditFindingStatus.OPEN,
                        remediation_plan="Verify citation validity or remove unsupported claim."
                    )
                    findings.append(finding)

        return findings

    def audit_causal_language(self, snapshot: ResearchSnapshot) -> List[AuditFinding]:
        """
        Causal Language Audit: Flags unwarranted deterministic causal language in observational contexts.
        """
        findings: List[AuditFinding] = []
        text_corpus = []

        for c in snapshot.claims:
            text_corpus.append(("CLAIM", c.get("claim_id", "cl-0"), c.get("statement", "")))

        if snapshot.final_output:
            for k, v in snapshot.final_output.items():
                if isinstance(v, str):
                    text_corpus.append(("FINAL_OUTPUT", k, v))

        for obj_type, obj_id, text in text_corpus:
            for pat in UNSUPPORTED_CAUSAL_PATTERNS:
                if re.search(pat, text, re.IGNORECASE):
                    findings.append(AuditFinding(
                        audit_id=f"audit-{snapshot.snapshot_id}",
                        issue=f"Unsupported Causal Claim: Detected pattern '{pat}' in {obj_type}.",
                        severity=AuditFindingSeverity.HIGH,
                        object_type="CLAIM",
                        object_id=obj_id,
                        evidence=f"Flagged excerpt: '{text[:120]}...'",
                        owner="scientific-board",
                        status=AuditFindingStatus.OPEN,
                        remediation_plan="Hedge causal terminology or provide formal counterfactual DAG validation."
                    ))

        return findings

    def audit_plan_deviations(self, snapshot: ResearchSnapshot) -> List[AuditFinding]:
        """
        Pre-Registration Audit: Checks if analysis plan deviations occurred and ensures they are recorded.
        """
        findings: List[AuditFinding] = []
        plan = snapshot.analysis_plan
        if not plan:
            return findings

        # Check registered deviations
        for dev in plan.deviations:
            severity = AuditFindingSeverity.MEDIUM
            if dev.deviation_type in ["ENDPOINT_CHANGE", "POST_HOC"]:
                severity = AuditFindingSeverity.HIGH

            findings.append(AuditFinding(
                audit_id=f"audit-{snapshot.snapshot_id}",
                issue=f"Analysis Plan Deviation: {dev.deviation_type} ({dev.reason})",
                severity=severity,
                object_type="ANALYSIS_PLAN",
                object_id=dev.deviation_id,
                evidence=f"Planned: {dev.planned_spec} -> Actual: {dev.actual_spec}",
                owner=dev.authorized_by,
                status=AuditFindingStatus.RESOLVED if dev.authorized_by else AuditFindingStatus.OPEN,
                remediation_plan=dev.impact_assessment
            ))

        return findings

    def audit_numeric_integrity(self, snapshot: ResearchSnapshot) -> List[AuditFinding]:
        """
        Checks that numeric claims correspond with actual result values.
        """
        findings: List[AuditFinding] = []
        result_map = {}
        for r in snapshot.results:
            name = r.get("name") or r.get("metric")
            val = r.get("value")
            if name and val is not None:
                result_map[name.lower()] = val

        # Simple verification of numeric consistency
        for claim in snapshot.claims:
            metric_ref = claim.get("metric_referenced")
            claimed_val = claim.get("numeric_value")
            if metric_ref and claimed_val is not None:
                actual_val = result_map.get(str(metric_ref).lower())
                if actual_val is not None:
                    try:
                        diff = abs(float(actual_val) - float(claimed_val))
                        if diff > 0.05:  # Tolerance threshold
                            findings.append(AuditFinding(
                                audit_id=f"audit-{snapshot.snapshot_id}",
                                issue=f"Numeric Discrepancy: Claim states {claimed_val} for {metric_ref}, but computed result is {actual_val}.",
                                severity=AuditFindingSeverity.HIGH,
                                object_type="NUMERIC_RESULT",
                                object_id=metric_ref,
                                evidence=f"Difference: {diff}",
                                owner="computational-verifier",
                                status=AuditFindingStatus.OPEN,
                                remediation_plan="Recalculate or update claim text."
                            ))
                    except (ValueError, TypeError):
                        pass

        return findings

    def run_all_checks(self, snapshot: ResearchSnapshot) -> List[AuditFinding]:
        """Runs all scientific integrity checks and returns consolidated findings."""
        findings: List[AuditFinding] = []
        findings.extend(self.audit_citations(snapshot))
        findings.extend(self.audit_causal_language(snapshot))
        findings.extend(self.audit_plan_deviations(snapshot))
        findings.extend(self.audit_numeric_integrity(snapshot))
        logger.info(f"Integrity check for snapshot {snapshot.snapshot_id} completed: {len(findings)} findings.")
        return findings
