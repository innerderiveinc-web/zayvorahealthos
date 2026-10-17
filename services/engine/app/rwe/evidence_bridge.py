"""
ZMIE Real-World Evidence (RWE) to Evidence Graph Bridge
Prompt 15 Implementation.

Converts RWE observational study summaries into structured ZMIE Evidence Objects,
injects them into the Knowledge & Evidence Graph with E5 grading, and performs
Triangulation Analysis against existing Randomized Controlled Trials (RCTs).
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from app.models.rwe_interop import RWEEvidenceSummary
from app.models.graph import EvidenceObject, EvidenceLadder, EvidenceStatus
from app.models.claim import StudyDesign, PICOContext, MedicalSystem


class RWEEvidenceGraphBridge:
    """
    Bridges real-world observational registry datasets into the ZMIE Evidence Graph,
    preserving strict epistemic tiers and triangulating RWE findings against RCTs.
    """

    def __init__(self, graph_engine=None):
        self.graph_engine = graph_engine
        self._bridged_evidence: Dict[str, EvidenceObject] = {}

    def bridge_rwe_to_evidence_graph(
        self,
        rwe_summary: RWEEvidenceSummary,
        intervention_concept: str = "Dapagliflozin",
        comparator_concept: str = "Standard of Care",
        disease_concept: str = "Heart Failure",
        medical_system: MedicalSystem = MedicalSystem.MODERN
    ) -> EvidenceObject:
        """
        Converts RWEEvidenceSummary into an EvidenceObject with E5_HUMAN_OBSERVATIONAL grade.
        """
        evidence_id = f"EVID-RWE-{rwe_summary.rwe_id}"

        pico = PICOContext(
            population_species="human",
            age_group="adult",
            condition_or_phenotype=disease_concept,
            intervention_agent=intervention_concept,
            comparator=comparator_concept,
        )

        findings_text = (
            f"Real-World Evidence from {rwe_summary.data_source_type} (N={rwe_summary.target_cohort_size + rwe_summary.comparator_cohort_size:,}): "
            f"{intervention_concept} vs {comparator_concept} demonstrated Hazard Ratio of "
            f"{rwe_summary.hazard_ratio_or_relative_risk:.2f} (95% CI: [{rwe_summary.confidence_interval_95[0]:.2f}, {rwe_summary.confidence_interval_95[1]:.2f}], p={rwe_summary.p_value}). "
            f"Bias audit status: Selection Risk {rwe_summary.bias_audit.selection_bias_risk.value}, Confounding Risk {rwe_summary.bias_audit.confounding_by_indication.value}. "
            f"Triangulation: {rwe_summary.triangulation_with_rct_status}."
        )

        evidence_obj = EvidenceObject(
            evidence_id=evidence_id,
            claim_id=f"CLM-RWE-{rwe_summary.rwe_id}",
            study_id=f"STUDY-RWE-{rwe_summary.rwe_id}",
            study_type=StudyDesign.PROSPECTIVE_COHORT,
            evidence_level=EvidenceLadder.E5_HUMAN_OBSERVATIONAL,
            evidence_status=EvidenceStatus.SUPPORTS,
            pico_context=pico,
            effect_measure="Hazard Ratio",
            effect_value=rwe_summary.hazard_ratio_or_relative_risk,
            confidence_interval=f"95% CI [{rwe_summary.confidence_interval_95[0]:.2f}, {rwe_summary.confidence_interval_95[1]:.2f}]",
            p_value=rwe_summary.p_value,
            sample_size=rwe_summary.target_cohort_size + rwe_summary.comparator_cohort_size,
            source_id="SRC-RWE-REGISTRY-01",
            document_id=f"RWE-SOURCE-{rwe_summary.rwe_id}",
            paragraph_anchor_hash=rwe_summary.provenance_hash,
            is_retracted=False
        )

        self._bridged_evidence[evidence_id] = evidence_obj

        # If a graph_engine is provided, register in graph engine's evidence store
        if self.graph_engine and hasattr(self.graph_engine, "_evidence_store"):
            self.graph_engine._evidence_store[evidence_id] = evidence_obj

        return evidence_obj

    def triangulate_with_rct(
        self,
        rwe_summary: RWEEvidenceSummary,
        landmark_rct_title: str = "DAPA-HF Landmark Phase 3 Trial",
        landmark_rct_hr: float = 0.74,
        landmark_rct_ci: List[float] = [0.65, 0.85]
    ) -> Dict[str, Any]:
        """
        Performs scientific triangulation: Compares RWE effect size against RCT benchmark.
        Confirms routine practice generalizability or flags divergence.
        """
        rwe_hr = rwe_summary.hazard_ratio_or_relative_risk
        delta = abs(rwe_hr - landmark_rct_hr)

        is_concordant = delta <= 0.08
        verdict = "HIGHLY_CONCORDANT" if is_concordant else "DIVERGENT_INVESTIGATION_REQUIRED"

        analysis = (
            f"Triangulation Analysis: RWE HR {rwe_hr:.2f} (95% CI {rwe_summary.confidence_interval_95}) vs "
            f"RCT HR {landmark_rct_hr:.2f} (95% CI {landmark_rct_ci}). "
            f"Effect size difference: {delta:.3f}. "
            f"{'Confirms that efficacy established in randomized trial cohorts translates effectively into unselected routine healthcare populations.' if is_concordant else 'Divergence observed; evaluate pragmatic compliance and baseline multimorbidity differences.'}"
        )

        return {
            "rwe_id": rwe_summary.rwe_id,
            "rwe_hr": rwe_hr,
            "rct_benchmark_title": landmark_rct_title,
            "rct_hr": landmark_rct_hr,
            "effect_size_delta": round(delta, 3),
            "verdict": verdict,
            "is_concordant": is_concordant,
            "scientific_interpretation": analysis
        }
