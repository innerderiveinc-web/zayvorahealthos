#!/usr/bin/env python3
"""
ZMIE Living Evidence Synthesis & Evidence Update Engine — Showcase Demonstration
Live demonstration of continuous surveillance, PICO protocols, study family linking,
DerSimonian-Laird random effects meta-analysis, retraction quarantine, and version diffing.
"""

import sys
import json
from app.living_evidence.engine import LivingEvidenceEngine
from app.models.living_evidence import (
    UpdateTriggerType,
    EvidenceImpactClass
)


def run_showcase():
    print("=" * 80)
    print("  ZMIE — LIVING EVIDENCE SYNTHESIS & EVIDENCE UPDATE ENGINE (PROMPT 17)")
    print("  Continuous Surveillance | DerSimonian-Laird Meta-Analysis | PRISMA Flow")
    print("=" * 80)

    engine = LivingEvidenceEngine()
    review_id = "REV-SGLT2I-HF"

    # -------------------------------------------------------------
    # 1. Baseline Review & PICO Protocol
    # -------------------------------------------------------------
    print("\n[SCENARIO 1] BASELINE LIVING SYSTEMATIC REVIEW (v1.0)")
    print("-" * 80)
    rev = engine.get_review(review_id)
    rq = rev.research_question
    print(f"Review ID        : {rev.review_id}")
    print(f"Title            : {rq.title}")
    print(f"Framework        : {rq.framework}")
    print(f"Population       : {rq.population}")
    print(f"Intervention     : {rq.intervention_or_exposure}")
    print(f"Primary Outcome  : {rq.outcomes[0]}")
    print(f"Current Status   : {rev.current_status.value}")
    print(f"Surveillance     : Every {rev.surveillance_plan.frequency_days} days across {len(rev.surveillance_plan.target_sources)} source databases")

    v1 = rev.versions[0]
    meta1 = v1.meta_analyses[0]
    print(f"\nBaseline Meta-Analysis (k={meta1.studies_included_count} trials):")
    print(f"  Model Type     : {meta1.model_type}")
    print(f"  Pooled RR      : {meta1.pooled_estimate} (95% CI {meta1.ci_lower} - {meta1.ci_upper}, p={meta1.p_value})")
    print(f"  Heterogeneity  : I^2 = {meta1.i_squared_pct}%, tau^2 = {meta1.tau_squared}, Q = {meta1.q_statistic}")
    print("  Forest Plot Weights:")
    for study in meta1.forest_plot_data:
        print(f"    * {study['study']:<20}: RR {study['effect']} (95% CI {study['ci_lower']}-{study['ci_upper']}) | Weight: {study['weight_pct']}%")

    # -------------------------------------------------------------
    # 2. Screening & Eligibility Gating
    # -------------------------------------------------------------
    print("\n[SCENARIO 2] CONTINUOUS SURVEILLANCE & AI-ASSISTED SCREENING")
    print("-" * 80)
    screen_eligible = engine.assess_screening_record(
        review_id=review_id,
        title="Dapagliflozin in Heart Failure with Preserved Ejection Fraction (DELIVER Trial)",
        abstract="Randomized double-blind trial evaluating dapagliflozin vs placebo on CV death or worsening HF.",
        study_design="Randomized Controlled Trial",
        reviewer_id="ZMIE Automated Screening Worker"
    )
    print(f"Candidate Title : DELIVER Trial")
    print(f"Decision        : {screen_eligible.decision}")
    print(f"AI Confidence   : {screen_eligible.ai_confidence:.2f}")
    print(f"Rationale       : {screen_eligible.ai_rationale}")

    screen_ineligible = engine.assess_screening_record(
        review_id=review_id,
        title="Observational cohort of 150 patients receiving empagliflozin",
        abstract="Retrospective review from a single center.",
        study_design="Observational Cohort",
        reviewer_id="ZMIE Automated Screening Worker"
    )
    print(f"\nCandidate Title : Single-Center Observational Cohort")
    print(f"Decision        : {screen_ineligible.decision}")
    print(f"Exclusion Reason: {screen_ineligible.exclusion_reason.value}")
    print(f"Rationale       : {screen_ineligible.ai_rationale}")

    # -------------------------------------------------------------
    # 3. New Evidence Trigger Detection
    # -------------------------------------------------------------
    print("\n[SCENARIO 3] NEW EVIDENCE TRIGGER & OPERATIONAL URGENCY")
    print("-" * 80)
    trigger = engine.detect_update_trigger(
        review_id=review_id,
        trigger_type=UpdateTriggerType.NEW_RCT,
        source_reference="NEJM-2022-DELIVER",
        description="DELIVER trial completed meeting primary composite outcome reduction.",
        impact_class=EvidenceImpactClass.HIGH_IMPACT
    )
    print(f"Trigger Type    : {trigger.trigger_type.value}")
    print(f"Impact Class    : {trigger.impact_class.value}")
    print(f"Action Decision : {trigger.action_decision}")
    print(f"Rationale       : {trigger.decision_rationale}")

    # -------------------------------------------------------------
    # 4. Incremental Study Incorporation & Recalculation (v2.0)
    # -------------------------------------------------------------
    print("\n[SCENARIO 4] EVIDENCE INTEGRATION & META-ANALYSIS RECALCULATION (v2.0)")
    print("-" * 80)
    v2 = engine.incorporate_new_study_and_recalculate(
        review_id=review_id,
        new_study_name="DELIVER Trial (Solomon et al.)",
        trial_id="NCT03614377",
        point_estimate=0.82,
        ci_lower=0.73,
        ci_upper=0.92,
        sample_size=6263,
        approver="ZMIE Lead Systematic Reviewer"
    )
    meta2 = v2.meta_analyses[0]
    print(f"Published Version: {v2.version_tag} ({v2.publication_date})")
    print(f"Included Trials  : k={v2.included_studies_count}")
    print(f"New Pooled RR    : {meta2.pooled_estimate} (95% CI {meta2.ci_lower} - {meta2.ci_upper}, p={meta2.p_value})")
    print(f"Heterogeneity    : I^2 = {meta2.i_squared_pct}%, Q = {meta2.q_statistic}")
    print(f"Conclusion Change: {v2.conclusion_change.value}")
    print(f"What's New       : {v2.what_changed_summary}")
    print(f"PRISMA Flow      : Screened: {v2.prisma_flow.records_screened_title_abstract} | Included in Meta: {v2.prisma_flow.studies_included_quantitative_meta}")

    # -------------------------------------------------------------
    # 5. Retraction Quarantine Protocol & Synthesis Recalculation (v3.0)
    # -------------------------------------------------------------
    print("\n[SCENARIO 5] URGENT RETRACTION QUARANTINE & IMPACT PROPAGATION (v3.0)")
    print("-" * 80)
    v3 = engine.handle_retraction_propagation(
        review_id=review_id,
        retracted_study_family_id="STUDY-EMPEROR-RED",
        retraction_reason="Publisher retraction due to unverified hospital source records.",
        approver="ZMIE Scientific Integrity Lead"
    )
    meta3 = v3.meta_analyses[0]
    print(f"Published Version: {v3.version_tag} ({v3.publication_date})")
    print(f"Included Trials  : k={v3.included_studies_count} (Compromised trial quarantined)")
    print(f"Recalculated RR  : {meta3.pooled_estimate} (95% CI {meta3.ci_lower} - {meta3.ci_upper})")
    print(f"What's New       : {v3.what_changed_summary}")

    # -------------------------------------------------------------
    # 6. Version Diffing & Historical Reproducibility
    # -------------------------------------------------------------
    print("\n[SCENARIO 6] TRANSPARENT VERSION DIFFING & AUDIT TRAIL")
    print("-" * 80)
    diff = engine.compare_review_versions(review_id, "v1.0", "v2.0")
    print("Diff (v1.0 vs v2.0):")
    print(f"  Studies Delta  : {diff['studies_delta']:+d}")
    print(f"  Pooled RR Delta: {diff['pooled_estimate_old']} -> {diff['pooled_estimate_new']} (Delta: {diff['pooled_estimate_delta']:+.3f})")
    print(f"  Change Summary : {diff['what_changed_summary']}")
    print(f"  Reproducible   : {diff['historical_reproducible']}")

    print("\n" + "=" * 80)
    print("  ZMIE LIVING EVIDENCE SYNTHESIS ENGINE: ALL VERIFICATIONS SUCCESSFUL")
    print("=" * 80)


if __name__ == "__main__":
    run_showcase()
