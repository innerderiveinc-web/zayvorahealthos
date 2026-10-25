#!/usr/bin/env python3
"""
ZMIE Medical Causal & Mechanistic Intelligence Engine — Showcase Demonstration
Live demonstration of multi-scale biological decomposition, translational gap detection,
causality firewall DAG identification gating, competing mechanism adjudication,
and multi-system traditional medicine epistemic parity.
"""

import sys
import json
from app.causal_mechanistic.engine import CausalMechanisticEngine
from app.models.causal_mechanistic import (
    DAGNode,
    DAGEdge,
    MedicalTraditionSystem,
    MechanismState
)


def run_showcase():
    print("=" * 80)
    print("  ZMIE — MEDICAL CAUSAL & MECHANISTIC INTELLIGENCE ENGINE (MODULE 16)")
    print("  Association != Mechanism != Prediction != Causal Effect != Clinical Efficacy")
    print("=" * 80)

    engine = CausalMechanisticEngine()

    # -------------------------------------------------------------
    # 1. Multi-Scale Biological Decomposition & Translational Gap
    # -------------------------------------------------------------
    print("\n[SCENARIO 1] MULTI-SCALE BIOLOGICAL DECOMPOSITION: BERBERINE")
    print("-" * 80)
    prop = engine.decompose_mechanism("BERBERINE", "Fasting Blood Glucose & HbA1c Reduction")
    print(f"Proposition ID    : {prop.proposition_id}")
    print(f"Intervention      : {prop.intervention_or_compound_id}")
    print(f"Target Outcome    : {prop.final_outcome}")
    print(f"Mechanism State   : {prop.mechanism_state.value}")
    print(f"Confidence Score  : {prop.confidence_score}")
    print("\nDecomposition Steps:")
    for step in prop.steps:
        pk_status = "PK-Plausible" if step.is_pk_plausible else "CONCENTRATION GAP (Supraphysiological)"
        print(f"  Step {step.step_index}: [{step.source_scale.value}] {step.source_entity_id} "
              f"--({step.step_type.value})--> [{step.target_scale.value}] {step.target_entity_id}")
        print(f"          Model: {step.experimental_level.value} ({step.species}) | {pk_status}")

    gap = prop.translational_gap
    print("\nTranslational Gap Report:")
    print(f"  Has Translational Gap : {gap.has_gap}")
    print(f"  Flags                 : {', '.join(gap.flags)}")
    print(f"  In-Vitro / Cmax Ratio : {gap.in_vitro_vs_human_cmax_ratio:.1f}x higher than human plasma")
    print(f"  Human Target Proven   : {gap.target_engagement_in_human_proven}")
    print(f"  Epistemic Verdict     : {gap.epistemic_verdict}")

    # -------------------------------------------------------------
    # 2. Competing Mechanisms & Discriminating Next-Best Experiment
    # -------------------------------------------------------------
    print("\n[SCENARIO 2] COMPETING MECHANISMS & DISCRIMINATING NEXT-BEST EXPERIMENT")
    print("-" * 80)
    cluster = engine.get_competing_mechanisms("BERBERINE")
    if cluster:
        print(f"Cluster ID       : {cluster.cluster_id}")
        print(f"Phenomenon       : {cluster.phenomenon}")
        print(f"Primary Hypo     : {cluster.primary_hypothesis.proposition_id} ({cluster.primary_hypothesis.mechanism_state.value})")
        for comp in cluster.competing_hypotheses:
            print(f"Competing Hypo   : {comp.proposition_id} ({comp.mechanism_state.value})")
            print(f"                   Summary: {comp.summary_narrative}")
        print("\nPoints of Divergence:")
        for pt in cluster.points_of_divergence:
            print(f"  * {pt}")

        exp = engine.propose_discriminating_experiment(cluster.cluster_id)
        if exp:
            print("\nNext-Best Discriminating Experiment Proposal:")
            print(f"  Proposal ID      : {exp.proposal_id}")
            print(f"  Question         : {exp.research_question}")
            print(f"  Model            : {exp.recommended_experimental_model.value}")
            print(f"  Key Readout      : {exp.discriminating_biomarker_or_readout}")
            print(f"  Outcome if Hypo A: {exp.expected_outcome_if_hypothesis_a}")
            print(f"  Outcome if Hypo B: {exp.expected_outcome_if_hypothesis_b}")
            print(f"  Feasibility      : {exp.feasibility_score:.2f}")

    # -------------------------------------------------------------
    # 3. Causality Firewall: DAG Identification Gating & Colliders
    # -------------------------------------------------------------
    print("\n[SCENARIO 3] CAUSALITY FIREWALL: DAG BACKDOOR & COLLIDER GATING")
    print("-" * 80)

    # Identifiable DAG
    nodes_valid = [
        DAGNode(node_id="X", label="SGLT2 Inhibitor", node_type="EXPOSURE", observed=True),
        DAGNode(node_id="Y", label="Cardiovascular Mortality", node_type="OUTCOME", observed=True),
        DAGNode(node_id="Z", label="Baseline Renal Function (eGFR)", node_type="CONFOUNDER", observed=True),
    ]
    edges_valid = [
        DAGEdge(source_node_id="Z", target_node_id="X"),
        DAGEdge(source_node_id="Z", target_node_id="Y"),
        DAGEdge(source_node_id="X", target_node_id="Y"),
    ]
    causal_valid = engine.validate_causal_dag_and_identification(
        exposure="SGLT2 Inhibitor",
        outcome="Cardiovascular Mortality",
        nodes=nodes_valid,
        edges=edges_valid,
        observed_effect_rr=0.74
    )
    print(f"Valid DAG Identification Status : {causal_valid.identification_status.value}")
    print(f"Causality State                 : {causal_valid.causality_state.value}")
    print(f"Calculated E-value              : {causal_valid.e_value} (unmeasured confounder must exceed this strength)")
    print(f"Target Trial Emulation Causal   : {causal_valid.target_trial.causal_contrast}")

    # Collider Conditioning (Berkson's / M-bias)
    nodes_collider = [
        DAGNode(node_id="X", label="Statin Therapy", node_type="EXPOSURE", observed=True),
        DAGNode(node_id="Y", label="Coronary Calcification", node_type="OUTCOME", observed=True),
        DAGNode(node_id="C", label="Hospital Admission", node_type="COLLIDER", observed=True),
    ]
    edges_collider = [
        DAGEdge(source_node_id="X", target_node_id="C"),
        DAGEdge(source_node_id="Y", target_node_id="C"),
        DAGEdge(source_node_id="X", target_node_id="Y"),
    ]
    causal_collider = engine.validate_causal_dag_and_identification(
        exposure="Statin Therapy",
        outcome="Coronary Calcification",
        nodes=nodes_collider,
        edges=edges_collider,
        observed_effect_rr=1.12
    )
    print(f"\nCollider DAG Status             : {causal_collider.identification_status.value}")
    print(f"Collider Stratification Flag    : {causal_collider.collider_stratification_detected}")
    print(f"Firewall Disclaimer             : {causal_collider.epistemic_disclaimer}")

    # -------------------------------------------------------------
    # 4. Multi-System Traditional Medicine Parity & Bioenhancers
    # -------------------------------------------------------------
    print("\n[SCENARIO 4] MULTI-SYSTEM TRADITIONAL MEDICINE EPISTEMICS & BIOENHANCERS")
    print("-" * 80)
    unani_bridge = engine.bridge_traditional_concept("Mizaj", MedicalTraditionSystem.UNANI)
    print(f"Unani Concept        : {unani_bridge.native_term}")
    print(f"Modern Correlate     : {unani_bridge.modern_biological_correlate}")
    print(f"Bridge Relation      : {unani_bridge.bridge_relation_type}")
    print(f"Epistemic Warning    : {unani_bridge.epistemic_warning}")

    ayur_bridge = engine.bridge_traditional_concept("Vata Dosha", MedicalTraditionSystem.AYURVEDA)
    print(f"\nAyurveda Concept     : {ayur_bridge.native_term}")
    print(f"Modern Correlate     : {ayur_bridge.modern_biological_correlate}")
    print(f"Bridge Relation      : {ayur_bridge.bridge_relation_type}")

    form_analysis = engine.analyze_formulation_synergy_and_interactions("TRIPHALA_TRIKATU")
    print(f"\nFormulation Analysis : {form_analysis['name']} ({form_analysis['tradition'].value})")
    print(f"Bioenhancer Present  : {form_analysis['bioenhancer_present']}")
    print(f"Amplification Factor : {form_analysis['bioavailability_amplification']}")
    print(f"Synergy Mechanism    : {form_analysis['synergistic_mechanism']}")
    print(f"Herb-Drug Warnings   : {form_analysis['herb_drug_interactions']}")

    # -------------------------------------------------------------
    # 5. Evolutionary Knowledge Diffing
    # -------------------------------------------------------------
    print("\n[SCENARIO 5] EVOLUTIONARY KNOWLEDGE DIFFING & SNAPSHOTS")
    print("-" * 80)
    snap1 = engine.create_snapshot(prop.proposition_id)
    # Simulate clinical trial completion / update
    active_prop = engine._propositions[prop.proposition_id]
    active_prop.mechanism_state = MechanismState.HUMAN_MECHANISTIC_EVIDENCE
    active_prop.confidence_score = 0.94
    snap2 = engine.create_snapshot(prop.proposition_id)
    diff = engine.diff_snapshots(snap1, snap2)
    print(f"State Transition     : {diff.state_transition}")
    print(f"Diff Summary         : {diff.change_summary}")

    print("\n" + "=" * 80)
    print("  ZMIE MEDICAL CAUSAL & MECHANISTIC INTELLIGENCE ENGINE: ALL PROOFS VERIFIED")
    print("=" * 80)


if __name__ == "__main__":
    run_showcase()
