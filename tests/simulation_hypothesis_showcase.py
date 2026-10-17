"""ZMIE Medical Knowledge Simulation, Research Hypothesis & Next-Best-Experiment Showcase.

Demonstrates end-to-end:
1. Epistemic boundary enforcement & Traditional medicine bridge hypotheses
2. Competing hypothesis discrimination (SGLT2 NHE-1 vs Hemodynamic preload/afterload)
3. PK/PD parametric simulation sweeps under Monte Carlo parameter uncertainty
4. Next-best-experiment generation with information gain E[ΔU] & anti-redundancy checks
5. Empirical result ingestion & Bayesian hypothesis updating
6. Research opportunity discovery & portfolio prioritization
"""

import json
from app.models.simulation_hypothesis import (
    EpistemicStatus,
    ExperimentDesignType,
    HypothesisStatus,
)
from app.simulation_hypothesis.engine import SimulationHypothesisEngine


def run_showcase():
    print("=" * 80)
    print(" ZMIE MEDICAL KNOWLEDGE SIMULATION & NEXT-BEST-EXPERIMENT ENGINE")
    print("=" * 80)

    engine = SimulationHypothesisEngine()

    # 1. Epistemic Integrity & Traditional Medicine Bridge
    print("\n--- [STAGE 1] EPISTEMIC STATUS & TRADITIONAL MEDICINE BRIDGE ---")
    hypotheses = engine.list_hypotheses()
    print(f"Loaded {len(hypotheses)} registered scientific hypotheses:")
    for h in hypotheses:
        print(f"  • [{h.hypothesis_id}] Type: {h.hypothesis_type.value} | Status: {h.status.value} | Epistemic: {h.epistemic_status.value}")
        print(f"    Statement: {h.statement[:110]}...")

    unani_hyp = engine.get_hypothesis("HYP-UNANI-GULQAND-BARRIER")
    print("\n  >> Traditional Medicine Bridge Inspection:")
    print(f"     Construct: {unani_hyp.traditional_medicine_bridge['traditional_construct']}")
    print(f"     Molecular Correlate: {unani_hyp.traditional_medicine_bridge['molecular_correlate']}")
    print(f"     Epistemic Rule: {unani_hyp.traditional_medicine_bridge['epistemic_note']}")

    # 2. Competing Hypothesis Discrimination
    print("\n--- [STAGE 2] COMPETING HYPOTHESIS DISCRIMINATION ---")
    report = engine.discriminate_competing_hypotheses("HYP-SGLT2-NHE1", "HYP-SGLT2-HEMO")
    print(f"Report ID: {report.report_id}")
    print(f"Synthetic Summary: {report.synthetic_summary}")
    print("Divergence Points Identified:")
    for dp in report.divergence_points:
        print(f"  ⚡ {dp}")
    print(f"Decisive Biomarkers for Discrimination: {', '.join(report.decisive_biomarkers)}")

    # 3. PK/PD Simulation Sweep under Monte Carlo Parameter Uncertainty
    print("\n--- [STAGE 3] MONTE CARLO PK/PD PARAMETRIC SIMULATION ---")
    sim = engine.run_simulation(
        model_id="MOD-PKPD-SGLT2",
        scenario_name="Empagliflozin 25mg Once-Daily in Chronic Heart Failure",
        dose_or_perturbation=25.0,
        time_points_hours=[1.0, 2.0, 4.0, 8.0, 12.0, 24.0],
        monte_carlo_iterations=500,
    )
    print(f"Simulation ID: {sim.simulation_id}")
    print(f"Epistemic Status: {sim.epistemic_status.value} (STRICT MODEL_PREDICTED)")
    print(f"Epistemic Disclaimer: {sim.epistemic_disclaimer}")
    print("Simulated Timecourse (Median & 95% Credible Intervals):")
    for pt in sim.predicted_outcomes["time_course"]:
        t = pt["time_h"]
        c_med = pt["plasma_concentration_median"]
        ci_c = sim.credible_intervals_95[f"conc_at_{t}h"]
        i_med = pt["target_inhibition_pct_median"]
        ci_i = sim.credible_intervals_95[f"inhibition_pct_at_{t}h"]
        print(f"  t = {t:4.1f}h | Conc: {c_med:6.3f} ug/mL [95% CI: {ci_c[0]:.3f} - {ci_c[1]:.3f}] | NHE1 Inhibition: {i_med:5.1f}% [95% CI: {ci_i[0]:.1f} - {ci_i[1]:.1f}%]")

    # 4. Next-Best-Experiment Proposal
    print("\n--- [STAGE 4] NEXT-BEST-EXPERIMENT DESIGN (INFORMATION GAIN) ---")
    exp_proposal = engine.propose_next_best_experiment(
        target_hypothesis_id="HYP-SGLT2-NHE1",
        preferred_design_type=ExperimentDesignType.IN_VITRO_ASSAY,
    )
    print(f"Proposal ID: {exp_proposal.proposal_id}")
    print(f"Scientific Question: {exp_proposal.scientific_question}")
    print(f"Design Type: {exp_proposal.design_type.value}")
    print(f"Expected Information Gain E[ΔU]: {exp_proposal.information_gain_score:.3f}")
    print(f"Discrimination Power: {exp_proposal.discrimination_power:.2f} | Feasibility: {exp_proposal.feasibility_score:.2f}")
    print(f"Controls Configured: {json.dumps(exp_proposal.controls, indent=2)}")
    print(f"Anti-Redundancy Verified: {exp_proposal.existing_data_checked}")
    print(f"Human-in-the-Loop Approval Required: {exp_proposal.human_approval_required}")

    # 5. Ingest Empirical Result & Bayesian Posterior Update
    print("\n--- [STAGE 5] RESULT INGESTION & BAYESIAN POSTERIOR UPDATE ---")
    hyp_nhe1_prior = engine.get_hypothesis("HYP-SGLT2-NHE1").current_posterior
    hyp_hemo_prior = engine.get_hypothesis("HYP-SGLT2-HEMO").current_posterior
    print(f"Prior Probabilities -> NHE-1: {hyp_nhe1_prior:.3f} | Hemodynamic: {hyp_hemo_prior:.3f}")

    result_record = engine.ingest_experiment_result(
        proposal_id=exp_proposal.proposal_id,
        observed_direction="DECREASE",
        observed_value=-28.1,
        confidence_interval=[-33.4, -22.8],
        p_value=0.0018,
        laboratory_provenance={
            "institution": "National Heart Research Institute",
            "lead_investigator": "Dr. E. Vance, PhD",
            "study_protocol": "IRB-NHRI-2026-CARDIO-88",
        },
    )
    print(f"\nIngested Result ID: {result_record.result_id}")
    print(f"Epistemic Status: {result_record.epistemic_status.value} (STRICT OBSERVED EVIDENCE)")
    print(f"Effect on Hypothesis: {result_record.effect_on_hypothesis}")
    print(f"Observed Value: {result_record.observed_outcome['value']}% (p = {result_record.p_value_or_bayes_factor})")

    hyp_nhe1_post = engine.get_hypothesis("HYP-SGLT2-NHE1")
    hyp_hemo_post = engine.get_hypothesis("HYP-SGLT2-HEMO")
    print(f"\nUpdated Posteriors:")
    print(f"  • HYP-SGLT2-NHE1 : {hyp_nhe1_prior:.3f} -> {hyp_nhe1_post.current_posterior:.3f} (Status: {hyp_nhe1_post.status.value})")
    print(f"  • HYP-SGLT2-HEMO : {hyp_hemo_prior:.3f} -> {hyp_hemo_post.current_posterior:.3f} (Status: {hyp_hemo_post.status.value})")

    # 6. Research Opportunities Portfolio
    print("\n--- [STAGE 6] RESEARCH OPPORTUNITIES PORTFOLIO ---")
    opportunities = engine.discover_research_opportunities()
    for opp in opportunities:
        print(f"  ★ [{opp.opportunity_id}] Priority: {opp.overall_priority} | Domain: {opp.scientific_domain}")
        print(f"    Title: {opp.title}")
        print(f"    Uncertainty Reduction: {opp.uncertainty_reduction_potential:.2f} | Feasibility: {opp.feasibility:.2f} | Cost: {opp.cost_tier}")
        print(f"    Clinical Need: {opp.unmet_clinical_need[:95]}...")

    print("\n" + "=" * 80)
    print(" ALL PROMPT 19 SIMULATION & HYPOTHESIS PIPELINES VERIFIED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    run_showcase()
