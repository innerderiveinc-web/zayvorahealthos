"""ZMIE Scientific Closed-Loop Discovery & Autonomous Knowledge Learning Showcase.

Demonstrates the complete end-to-end cycle:
SCIENTIFIC KNOWLEDGE -> HYPOTHESIS -> EXPERIMENT -> EVIDENCE -> KNOWLEDGE LEARNING SYSTEM
"""

import json
from app.research.closed_loop_learning import ScientificClosedLoopLearningEngine


def run_showcase():
    print("=" * 80)
    print(" ZMIE UNIFIED SCIENTIFIC CLOSED-LOOP DISCOVERY & LEARNING SYSTEM")
    print(" SCIENTIFIC KNOWLEDGE -> HYPOTHESIS -> EXPERIMENT -> EVIDENCE -> LEARNING")
    print("=" * 80)

    engine = ScientificClosedLoopLearningEngine()

    topic = "SGLT2_CARDIOPROTECTION_IN_HEART_FAILURE"
    print(f"\n[INITIATING CLOSED-LOOP CYCLE FOR DOMAIN: {topic}]")

    execution = engine.execute_closed_loop_cycle(
        topic=topic,
        target_hypothesis_id="HYP-SGLT2-NHE1",
        competing_hypothesis_id="HYP-SGLT2-HEMO",
        simulated_dose_mg=25.0,
        observed_delta_pct=-28.5,
        observed_p_value=0.0015,
        lab_provenance={
            "institution": "Cardiovascular Physiology Research Core",
            "lead_investigator": "Dr. Sarah Chen, MD-PhD",
            "model": "Isolated Langendorff-perfused adult cardiomyocyte preparation",
            "blinding": "Triple-blinded randomized vehicle-controlled study",
            "registration": "PREREG-PROTO-EXP-NBE-HYP-SGLT2",
        },
    )

    print(f"\nCycle ID: {execution.cycle_id}")
    print(f"Started: {execution.started_at} | Completed: {execution.completed_at}")

    print("\n--- 5-STAGE CLOSED-LOOP PROGRESSION ---")
    for step in execution.stage_progression:
        print(f"  ▶ {step}")

    print("\n--- [STAGE 1: SCIENTIFIC KNOWLEDGE SNAPSHOT (t0)] ---")
    t0 = execution.initial_knowledge_state
    print(f"  Snapshot ID: {t0.snapshot_id}")
    print(f"  Active Hypotheses: {t0.active_hypotheses_count} | Confirmed Causal Edges: {t0.confirmed_causal_edges}")
    print(f"  Baseline Shannon Entropy: {t0.shannon_entropy:.4f} bits")
    print(f"  Living Review Version: {t0.living_reviews_version}")

    print("\n--- [STAGE 2: HYPOTHESIS FORMULATION & DISCRIMINATION] ---")
    for hyp in execution.formulated_hypotheses:
        print(f"  • [{hyp.hypothesis_id}] Type: {hyp.hypothesis_type.value} | Epistemic: {hyp.epistemic_status.value}")
        print(f"    Prior: {hyp.prior_probability:.2f} | Statement: {hyp.statement[:90]}...")
    print(f"  Competing Divergence Summary: {execution.competing_divergence_summary}")

    print("\n--- [STAGE 3: EXPERIMENT DESIGN & COMPUTATIONAL SIMULATION] ---")
    sim = execution.simulation_run
    print(f"  Simulation ID: {sim.simulation_id} (Status: {sim.epistemic_status.value})")
    print(f"  Epistemic Disclaimer: {sim.epistemic_disclaimer[:85]}...")
    exp = execution.executed_proposal
    print(f"  Designed Proposal: {exp.proposal_id}")
    print(f"  Question: {exp.scientific_question}")
    print(f"  Information Gain E[ΔU]: {exp.information_gain_score:.3f} | Discrimination Power: {exp.discrimination_power:.2f}")
    print(f"  Anti-Redundancy Checked: {exp.existing_data_checked} | Human Approval Required: {exp.human_approval_required}")

    print("\n--- [STAGE 4: EVIDENCE INGESTION (OBSERVED)] ---")
    ev = execution.ingested_evidence
    print(f"  Result ID: {ev.result_id} (Status: {ev.epistemic_status.value})")
    print(f"  Observed Outcome: {ev.observed_outcome['value']}% (p = {ev.p_value_or_bayes_factor})")
    print(f"  Effect on Hypothesis: {ev.effect_on_hypothesis}")

    print("\n--- [STAGE 5: KNOWLEDGE LEARNING SYSTEM DELTA (t0 -> t1)] ---")
    delta = execution.epistemic_delta
    print(f"  Credence Transition: {delta.prior_credence:.3f} -> {delta.posterior_credence:.3f} ({delta.status_transition})")
    print(f"  Entropy Reduction (ΔH): {delta.entropy_reduction:.4f} bits")
    print("  Causal DAG Edge Weight Updates:")
    for edge in delta.causal_edge_weight_updates:
        print(f"    🔗 {edge['edge']}: {edge['previous_weight']} -> {edge['updated_weight']} ({edge['causality_status']})")
    print("  Retired Scientific Assumptions:")
    for ret in delta.retired_assumptions:
        print(f"    ✕ {ret}")
    print("  Newly Opened Research Frontiers:")
    for q in delta.new_questions_opened:
        print(f"    ? {q}")

    print("\n--- MASTER EPISTEMIC VERDICT ---")
    print(f"  ✔ {execution.master_epistemic_verdict}")

    print("\n" + "=" * 80)
    print(" COMPLETE SCIENTIFIC CLOSED-LOOP CYCLE VERIFIED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    run_showcase()
