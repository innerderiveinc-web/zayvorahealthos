"""
ZMIE Deep Research Operating Engine Showcase (Prompt 6 Deliverable)
Demonstrates the 5 required end-to-end research workflows:
1. Demo 1: Core Research Investigation (Intervention X in Condition Y)
2. Demo 2: Traditional Medicine & Cross-System Investigation (Unani vs Modern Biomedicine)
3. Demo 3: Research Gap Prioritization & Next-Best-Question Formulation
4. Demo 4: Contradiction & Trial Divergence Topography (No forced consensus)
5. Demo 5: Safety Intelligence & Pharmacovigilance Audit
"""

import asyncio
import json
from app.research.engine import DeepResearchOperatingEngine
from app.research.planner import ResearchPlannerAgent
from app.research.screening import ScreeningAndExtractionAgent
from app.research.synthesis import SynthesisAndContradictionAgent


async def run_deep_research_showcase():
    print("=" * 80)
    print(" ZMIE DEEP RESEARCH ENGINE — MASTER END-TO-END SHOWCASE (PROMPT 6) ")
    print("=" * 80)

    # -------------------------------------------------------------
    # DEMO 1: Core Research (Intervention X in Condition Y)
    # -------------------------------------------------------------
    print("\n[DEMO 1] Core Research Investigation: Berberine vs Metformin in Type 2 Diabetes")
    q1 = "What is the clinical efficacy and glycemic impact of Berberine compared to Metformin in Type 2 Diabetes?"
    job1 = await DeepResearchOperatingEngine.create_research_job(
        question=q1,
        target_systems=["modern", "unani", "ayurveda"],
        budget_limit=50
    )
    print(f"  -> Generated ResearchPlan ID: {job1.plan.plan_id}")
    print(f"  -> Decomposed PICO Intervention: {job1.plan.pico.intervention}")
    print(f"  -> PICO Population: {job1.plan.pico.population}")
    print(f"  -> Extracted Sub-Questions ({len(job1.plan.sub_questions)}):")
    for sq in job1.plan.sub_questions[:2]:
        print(f"     * {sq}")

    rep1 = await DeepResearchOperatingEngine.execute_investigation(job1.job_id)
    print(f"  -> Autonomous Pipeline Completed: State = {job1.state.value}")
    print(f"  -> Screened: {rep1.flow_metrics['screened']} | Included: {rep1.flow_metrics['included']} | Excluded: {rep1.flow_metrics['excluded']}")
    print(f"  -> Structured Evidence Table Entries ({len(rep1.evidence_table)}):")
    for row in rep1.evidence_table[:2]:
        print(f"     * [{row.source_id}] {row.study_title[:55]}... | Grade: {row.evidence_grade} | Finding: {row.primary_findings[:60]}...")
    print(f"  -> Reproducibility Hash: {rep1.reproducibility_hash[:16]}... (SHA-256)")

    # -------------------------------------------------------------
    # DEMO 2: Traditional Medicine (Unani vs Modern Biomedical)
    # -------------------------------------------------------------
    print("\n[DEMO 2] Traditional Medicine & Cross-System Investigation: Darhald / Berberis in Ziabetus")
    q2 = "How does Unani Mizaj theory for Darhald (Berberis aristata) correlate with modern AMPK activation in metabolic syndrome?"
    job2 = await DeepResearchOperatingEngine.create_research_job(
        question=q2,
        target_systems=["unani", "modern"],
        budget_limit=30
    )
    rep2 = await DeepResearchOperatingEngine.execute_investigation(job2.job_id)
    print(f"  -> Multi-System Plan Created: {job2.plan.title}")
    unani_entries = [e for e in rep2.evidence_table if e.medical_system == "UNANI"]
    print(f"  -> Unani Compendial Entries Preserved: {len(unani_entries)}")
    for ue in unani_entries:
        print(f"     * [{ue.source_id}] {ue.study_title} ({ue.study_design})")
    print(f"  -> Grounded Assertions Count: {len(rep2.assertions)}")
    for ast in rep2.assertions:
        print(f"     * [{ast.assertion_type.value}] {ast.statement[:75]}... (Status: {ast.epistemic_status})")

    # -------------------------------------------------------------
    # DEMO 3: Research Gaps & Next-Best-Question Heuristics
    # -------------------------------------------------------------
    print("\n[DEMO 3] Autonomous Research Gap Discovery & Next-Best-Question Prioritization")
    print(f"  -> Identified Critical Gaps ({len(rep1.research_gaps)}):")
    for gap in rep1.research_gaps:
        print(f"     * [{gap.priority}] {gap.category}: {gap.description[:75]}...")
        print(f"       Deficiency: {gap.evidence_deficiency}")
    print(f"  -> Formulated Next-Best Research Questions ({len(rep1.next_best_questions)}):")
    for nbq in rep1.next_best_questions:
        print(f"     * Question: {nbq.question_text}")
        print(f"       Design: {nbq.proposed_methodology[:80]}...")
        print(f"       Impact: {nbq.anticipated_impact}")

    # -------------------------------------------------------------
    # DEMO 4: Contradiction & Trial Divergence Topography
    # -------------------------------------------------------------
    print("\n[DEMO 4] Contradiction Analysis: No Forced Consensus Principle")
    print(f"  -> Active Contradiction Clusters ({len(rep1.contradictions)}):")
    for cntr in rep1.contradictions:
        print(f"     * Cluster Topic: {cntr.topic} ({cntr.contradiction_type.value})")
        print(f"       Divergence: {cntr.divergence_summary}")
        print(f"       Root Cause: {cntr.probable_root_cause}")
        print(f"       Resolution: {cntr.resolution_pathway}")

    # -------------------------------------------------------------
    # DEMO 5: Safety Intelligence & Pharmacovigilance Review
    # -------------------------------------------------------------
    print("\n[DEMO 5] Safety Intelligence & Drug Interaction Audit")
    safety = rep1.safety_findings
    print(f"  -> Safety Classification: {safety.get('safety_status')}")
    print(f"  -> Pregnancy / Lactation Alert: {safety.get('pregnancy_lactation_alert')}")
    print(f"  -> Cytochrome P450 Interactions: {safety.get('cyp_interactions')}")
    print(f"  -> Warnings: {safety.get('warnings')}")

    # Snapshot and Diff verification
    snap1 = job1.snapshots[0]
    snap2 = DeepResearchOperatingEngine.create_snapshot(job1.job_id)
    diff = DeepResearchOperatingEngine.compute_diff(job1.job_id, snap1.snapshot_id, snap2.snapshot_id)
    print(f"\n[SNAPSHOT & DIFF] Computed Job Version Diff:")
    print(f"  -> Summary: {diff.diff_summary}")
    print(f"  -> Target Snapshot: {diff.target_snapshot_id} (Version {snap2.snapshot_version})")

    print("\n" + "=" * 80)
    print(" ALL 5 PROMPT 6 DEEP RESEARCH SHOWCASE DEMONSTRATIONS COMPLETED SUCCESSFULLY! ")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(run_deep_research_showcase())
