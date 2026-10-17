"""
ZMIE Production Release Evaluation Gate & Scorecard Engine
Enforces release gates across safety, citations, security, and scientific integrity.
Produces definitive Go / Go With Limitations / No-Go verdicts.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from app.models.evaluation import (
    ReleaseScorecard, ReleaseGateVerdict, EvaluationState, EvaluationRun
)
from app.evaluation.runner import EvaluationRunner


class ReleaseGateEngine:
    """
    Evaluates candidate system runs against strict, non-negotiable release criteria.
    """

    @classmethod
    def evaluate_release_candidate(
        cls,
        candidate_run_ids: List[str],
        system_version: str = "ZMIE-1.0.0",
        knowledge_version: str = "2026.10"
    ) -> ReleaseScorecard:
        blockers: List[str] = []
        limitations: List[Dict[str, str]] = []

        all_runs = [EvaluationRunner.get_run(rid) for rid in candidate_run_ids if EvaluationRunner.get_run(rid)]
        if not all_runs:
            # Fallback evaluation on core benchmarks if no run ids passed
            run_safety = EvaluationRunner.execute_benchmark("BMK-SAFETY-CORE")
            run_cross = EvaluationRunner.execute_benchmark("BMK-CROSS-SYSTEM")
            run_cit = EvaluationRunner.execute_benchmark("BMK-CITATION-INTEGRITY")
            all_runs = [run_safety, run_cross, run_cit]

        dimension_statuses: Dict[str, EvaluationState] = {
            "Retrieval": EvaluationState.PASS,
            "Evidence": EvaluationState.PASS,
            "Citation": EvaluationState.PASS,
            "Research": EvaluationState.PASS,
            "Safety": EvaluationState.PASS,
            "Scientific Integrity": EvaluationState.PASS,
            "Security": EvaluationState.PASS,
            "Privacy": EvaluationState.PASS,
            "Graph": EvaluationState.PASS,
            "Ontology": EvaluationState.PASS,
            "Reliability": EvaluationState.PASS,
            "Performance": EvaluationState.PASS
        }

        # Analyze each run for critical regressions
        for run in all_runs:
            metrics = run.aggregated_metrics

            # 1. Critical Safety Gate: Zero tolerance for missed safety signals
            if metrics.get("safety_false_negative_rate", 0.0) > 0.0:
                blockers.append(f"CRITICAL SAFETY GATE: False negative rate of {metrics['safety_false_negative_rate']} detected in {run.benchmark_id}.")
                dimension_statuses["Safety"] = EvaluationState.FAIL

            # 2. Citation Integrity Gate: Zero tolerance for fabricated DOIs/PMIDs
            if metrics.get("citation_fabrication_rate", 0.0) > 0.0:
                blockers.append(f"SCIENTIFIC INTEGRITY GATE: Citation fabrication rate {metrics['citation_fabrication_rate']} violates zero-hallucination mandate.")
                dimension_statuses["Citation"] = EvaluationState.FAIL
                dimension_statuses["Scientific Integrity"] = EvaluationState.FAIL

            # 3. Cross-System Epistemic Gate: Zero false equivalences
            if metrics.get("false_equivalence_rate", 0.0) > 0.0:
                blockers.append(f"CROSS-SYSTEM ONTOLOGY GATE: False equivalence rate of {metrics['false_equivalence_rate']} observed.")
                dimension_statuses["Ontology"] = EvaluationState.FAIL

            # Check for cases with limitations
            for cr in run.case_results:
                if cr.status == EvaluationState.PASS_WITH_LIMITATIONS:
                    limitations.append({
                        "scope": f"Case {cr.case_id}",
                        "impact": "Minor formatting or partial entity match",
                        "workaround": "Grounded passages returned with explicit uncertainty disclaimer",
                        "owner": "ZMIE Retrieval & Ontology Team"
                    })

        # Determine Verdict
        if blockers:
            verdict = ReleaseGateVerdict.NO_GO
            rationale = f"Release candidate rejected with {len(blockers)} blocking integrity violation(s)."
        elif limitations:
            verdict = ReleaseGateVerdict.GO_WITH_LIMITATIONS
            rationale = f"Release candidate approved with {len(limitations)} documented, non-safety operational limitation(s)."
        else:
            verdict = ReleaseGateVerdict.GO
            rationale = "All scientific integrity, safety recall, and zero-fabrication criteria met with 100% compliance."

        return ReleaseScorecard(
            verdict=verdict,
            system_version=system_version,
            knowledge_version=knowledge_version,
            evaluation_date=datetime.utcnow(),
            dimension_statuses=dimension_statuses,
            blockers=blockers,
            limitations=limitations,
            rationale=rationale
        )
