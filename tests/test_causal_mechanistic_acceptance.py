"""
ZMIE Medical Causal & Mechanistic Intelligence Acceptance Tests
Validating multi-scale biological decomposition, translational gap detection,
causality firewall / DAG identification gating, competing hypothesis adjudication,
and traditional medicine epistemic parity.
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.models.causal_mechanistic import (
    BiologicalScale,
    CausalityState,
    MechanismState,
    ExperimentalValidationLevel,
    CausalIdentificationStatus,
    MedicalTraditionSystem,
    DAGNode,
    DAGEdge
)
from app.causal_mechanistic.engine import CausalMechanisticEngine


class TestCausalMechanisticAcceptance(unittest.TestCase):

    def setUp(self):
        self.engine = CausalMechanisticEngine()
        self.client = TestClient(app)

    # -------------------------------------------------------------
    # 1. Biological Decomposition & Entity Lookups
    # -------------------------------------------------------------

    def test_entity_records_and_adme_profiles(self):
        berb = self.engine.get_compound("BERBERINE")
        self.assertIsNotNone(berb)
        self.assertEqual(berb.canonical_name, "Berberine")
        self.assertIsNotNone(berb.pk_adme)
        self.assertEqual(berb.pk_adme.cmax_human_achievable_umol, 0.07)
        self.assertEqual(berb.pk_adme.absorption_bioavailability_pct, 5.0)

        ampk = self.engine.get_target("AMPK")
        self.assertIsNotNone(ampk)
        self.assertEqual(ampk.gene_symbol, "PRKAA1")
        self.assertGreater(ampk.species_homology_mouse_pct, 90.0)

        pathway = self.engine.get_pathway("AMPK_SIGNALING")
        self.assertIsNotNone(pathway)
        self.assertEqual(pathway.domain, "Metabolism")

    def test_multi_scale_decomposition_berberine(self):
        prop = self.engine.decompose_mechanism("BERBERINE", "Type 2 Diabetes Glycemic Control")
        self.assertIsNotNone(prop)
        self.assertEqual(prop.intervention_or_compound_id, "BERBERINE")
        self.assertEqual(len(prop.steps), 4)

        # Scale transitions
        scales = [step.source_scale for step in prop.steps]
        self.assertIn(BiologicalScale.SUBATOMIC_CHEMICAL, scales)
        self.assertIn(BiologicalScale.MOLECULAR_TARGET, scales)
        self.assertIn(BiologicalScale.PATHWAY_NETWORK, scales)

        # In-vitro vs human plasma mismatch flagged
        step1 = prop.steps[0]
        self.assertEqual(step1.target_entity_id, "AMPK")
        self.assertFalse(step1.is_pk_plausible)
        self.assertGreater(step1.concentration_tested_umol, step1.human_achievable_cmax_umol)

    # -------------------------------------------------------------
    # 2. Translational Gap & PK Plausibility
    # -------------------------------------------------------------

    def test_translational_gap_detection(self):
        # Berberine has a significant translational gap for systemic direct target engagement
        prop_berb = self.engine.decompose_mechanism("BERBERINE", "HbA1c Reduction")
        gap = prop_berb.translational_gap
        self.assertTrue(gap.has_gap)
        self.assertIn("IN_VITRO_CONCENTRATION_EXCEEDS_HUMAN_CMAX", gap.flags)
        self.assertGreater(gap.in_vitro_vs_human_cmax_ratio, 100.0)
        self.assertFalse(gap.target_engagement_in_human_proven)
        self.assertEqual(prop_berb.mechanism_state, MechanismState.SUPPORTED_WITH_LIMITATIONS)

        # Dapagliflozin achieves complete therapeutic target engagement at human Cmax
        prop_dapa = self.engine.decompose_mechanism("DAPAGLIFLOZIN", "HbA1c Reduction")
        gap_dapa = prop_dapa.translational_gap
        self.assertFalse(gap_dapa.has_gap)
        self.assertTrue(gap_dapa.target_engagement_in_human_proven)
        self.assertEqual(prop_dapa.mechanism_state, MechanismState.HUMAN_MECHANISTIC_EVIDENCE)

    # -------------------------------------------------------------
    # 3. Causality Firewall & DAG Identification Gating
    # -------------------------------------------------------------

    def test_causal_dag_identification_satisfied(self):
        nodes = [
            DAGNode(node_id="X", label="SGLT2 Inhibitor", node_type="EXPOSURE", observed=True),
            DAGNode(node_id="Y", label="Cardiovascular Mortality", node_type="OUTCOME", observed=True),
            DAGNode(node_id="Z1", label="Baseline HbA1c", node_type="CONFOUNDER", observed=True),
            DAGNode(node_id="Z2", label="Baseline eGFR", node_type="CONFOUNDER", observed=True),
        ]
        edges = [
            DAGEdge(source_node_id="Z1", target_node_id="X"),
            DAGEdge(source_node_id="Z1", target_node_id="Y"),
            DAGEdge(source_node_id="Z2", target_node_id="X"),
            DAGEdge(source_node_id="Z2", target_node_id="Y"),
            DAGEdge(source_node_id="X", target_node_id="Y"),
        ]

        prop = self.engine.validate_causal_dag_and_identification(
            exposure="SGLT2 Inhibitor",
            outcome="Cardiovascular Mortality",
            nodes=nodes,
            edges=edges,
            observed_effect_rr=0.72
        )

        self.assertEqual(prop.identification_status, CausalIdentificationStatus.IDENTIFIED)
        self.assertEqual(prop.causality_state, CausalityState.CAUSALLY_SUPPORTED)
        self.assertFalse(prop.unmeasured_confounding_suspected)
        self.assertFalse(prop.collider_stratification_detected)
        self.assertIsNotNone(prop.e_value)
        self.assertGreater(prop.e_value, 1.5)  # E-value for RR=0.72 (1/0.72 = 1.39 -> ~2.1)
        self.assertIsNotNone(prop.target_trial)

    def test_causal_dag_collider_conditioning_flagged(self):
        # Conditioning on a collider node introduces selection/collider bias
        nodes = [
            DAGNode(node_id="X", label="Statin Therapy", node_type="EXPOSURE", observed=True),
            DAGNode(node_id="Y", label="Coronary Artery Calcification", node_type="OUTCOME", observed=True),
            DAGNode(node_id="C", label="Hospital Admission", node_type="COLLIDER", observed=True),
        ]
        edges = [
            DAGEdge(source_node_id="X", target_node_id="C"),
            DAGEdge(source_node_id="Y", target_node_id="C"),
            DAGEdge(source_node_id="X", target_node_id="Y"),
        ]

        prop = self.engine.validate_causal_dag_and_identification(
            exposure="Statin Therapy",
            outcome="Coronary Artery Calcification",
            nodes=nodes,
            edges=edges,
            observed_effect_rr=1.15
        )

        self.assertEqual(prop.identification_status, CausalIdentificationStatus.IDENTIFICATION_NOT_ESTABLISHED)
        self.assertEqual(prop.causality_state, CausalityState.CAUSALLY_CONTESTED)
        self.assertTrue(prop.collider_stratification_detected)
        self.assertIn("CRITICAL CAUSALITY FIREWALL ALERT", prop.epistemic_disclaimer)

    def test_causal_dag_unmeasured_confounding_gating(self):
        nodes = [
            DAGNode(node_id="X", label="Dietary Pattern", node_type="EXPOSURE", observed=True),
            DAGNode(node_id="Y", label="Longevity", node_type="OUTCOME", observed=True),
            DAGNode(node_id="U", label="Socioeconomic & Health Seeking Behavior", node_type="CONFOUNDER", observed=False),
        ]
        edges = [
            DAGEdge(source_node_id="U", target_node_id="X"),
            DAGEdge(source_node_id="U", target_node_id="Y"),
            DAGEdge(source_node_id="X", target_node_id="Y"),
        ]

        prop = self.engine.validate_causal_dag_and_identification(
            exposure="Dietary Pattern",
            outcome="Longevity",
            nodes=nodes,
            edges=edges,
            observed_effect_rr=1.20
        )

        self.assertEqual(prop.identification_status, CausalIdentificationStatus.CONDITIONAL_ON_UNOBSERVED)
        self.assertEqual(prop.causality_state, CausalityState.ASSOCIATED)
        self.assertTrue(prop.unmeasured_confounding_suspected)

    # -------------------------------------------------------------
    # 4. Competing Mechanisms & Discriminating Experiments
    # -------------------------------------------------------------

    def test_competing_mechanisms_and_experiment_proposal(self):
        cluster = self.engine.get_competing_mechanisms("BERBERINE")
        self.assertIsNotNone(cluster)
        self.assertEqual(cluster.cluster_id, "CLUSTER-BERBERINE-METABOLIC")
        self.assertEqual(len(cluster.competing_hypotheses), 1)
        self.assertIn("UNRESOLVED_COMPETING", cluster.resolution_status)

        # Propose discriminating experiment
        exp = self.engine.propose_discriminating_experiment("CLUSTER-BERBERINE-METABOLIC")
        self.assertIsNotNone(exp)
        self.assertEqual(exp.recommended_experimental_model, ExperimentalValidationLevel.ANIMAL_IN_VIVO)
        self.assertIn("germ-free", exp.research_question.lower())
        self.assertIn("GLP-1", exp.discriminating_biomarker_or_readout)
        self.assertGreater(exp.feasibility_score, 0.7)

    # -------------------------------------------------------------
    # 5. Traditional Medicine Parity & Formulations
    # -------------------------------------------------------------

    def test_traditional_medicine_bridging(self):
        # Unani Mizaj
        bridge_mizaj = self.engine.bridge_traditional_concept("Mizaj", MedicalTraditionSystem.UNANI)
        self.assertEqual(bridge_mizaj.tradition, MedicalTraditionSystem.UNANI)
        self.assertEqual(bridge_mizaj.bridge_relation_type, "CONCEPTUALLY_RELATED")
        self.assertIn("Metabolic-autonomic", bridge_mizaj.modern_biological_correlate)
        self.assertIn("holistic", bridge_mizaj.epistemic_warning.lower())

        # Ayurveda Vata
        bridge_vata = self.engine.bridge_traditional_concept("Vata Dosha", MedicalTraditionSystem.AYURVEDA)
        self.assertEqual(bridge_vata.tradition, MedicalTraditionSystem.AYURVEDA)
        self.assertEqual(bridge_vata.bridge_relation_type, "CONCEPTUALLY_RELATED")
        self.assertIn("Neurological signaling", bridge_vata.modern_biological_correlate)

    def test_polyherbal_formulation_synergy_and_bioenhancer(self):
        res = self.engine.analyze_formulation_synergy_and_interactions("TRIPHALA_TRIKATU")
        self.assertEqual(res["tradition"], MedicalTraditionSystem.AYURVEDA)
        self.assertTrue(res["bioenhancer_present"])
        self.assertIn("2.5x", res["bioavailability_amplification"])
        self.assertIn("CYP3A4", res["herb_drug_interactions"][0])
        self.assertIn("Warfarin", res["safety_advisory"])

    # -------------------------------------------------------------
    # 6. Snapshots & Evolutionary Diffing
    # -------------------------------------------------------------

    def test_snapshots_and_knowledge_diffing(self):
        prop = self.engine.decompose_mechanism("BERBERINE", "Glycemic control")
        snap1 = self.engine.create_snapshot(prop.proposition_id)

        # Simulate evidence progression
        prop.mechanism_state = MechanismState.HUMAN_MECHANISTIC_EVIDENCE
        prop.confidence_score = 0.91
        snap2 = self.engine.create_snapshot(prop.proposition_id)

        diff = self.engine.diff_snapshots(snap1, snap2)
        self.assertTrue(diff.changed_state)
        self.assertIn("SUPPORTED_WITH_LIMITATIONS -> HUMAN_MECHANISTIC_EVIDENCE", diff.state_transition)

    # -------------------------------------------------------------
    # 7. REST API Endpoints Integration
    # -------------------------------------------------------------

    def test_api_endpoints(self):
        # 1. Decompose endpoint
        res = self.client.post("/v1/causal-mechanistic/mechanisms/decompose", json={
            "compound_id": "BERBERINE",
            "target_outcome": "Fasting Blood Glucose"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["intervention_or_compound_id"], "BERBERINE")
        self.assertTrue(data["translational_gap"]["has_gap"])

        # 2. Competing hypotheses endpoint
        res = self.client.get("/v1/causal-mechanistic/mechanisms/competing/BERBERINE")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["cluster_id"], "CLUSTER-BERBERINE-METABOLIC")

        # 3. Discriminating experiment proposal endpoint
        res = self.client.post("/v1/causal-mechanistic/mechanisms/experiments/propose", json={
            "cluster_id": "CLUSTER-BERBERINE-METABOLIC"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("germ-free", data["design_protocol"].lower())

        # 4. DAG validate endpoint
        res = self.client.post("/v1/causal-mechanistic/causal/dag/validate", json={
            "exposure": "Metformin",
            "outcome": "Cardiovascular Death",
            "nodes": [
                {"node_id": "EXP", "label": "Metformin", "node_type": "EXPOSURE", "observed": True},
                {"node_id": "OUT", "label": "Cardiovascular Death", "node_type": "OUTCOME", "observed": True},
                {"node_id": "CONF", "label": "Age", "node_type": "CONFOUNDER", "observed": True}
            ],
            "edges": [
                {"source_node_id": "CONF", "target_node_id": "EXP", "direction": "DIRECTED", "assumed": True},
                {"source_node_id": "CONF", "target_node_id": "OUT", "direction": "DIRECTED", "assumed": True},
                {"source_node_id": "EXP", "target_node_id": "OUT", "direction": "DIRECTED", "assumed": True}
            ],
            "observed_effect_rr": 0.85
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["identification_status"], "IDENTIFIED")

        # 5. Traditional bridge endpoint
        res = self.client.post("/v1/causal-mechanistic/traditional/bridge", json={
            "native_term": "Mizaj",
            "tradition": "UNANI"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["bridge_relation_type"], "CONCEPTUALLY_RELATED")

        # 6. Traditional formulation interactions endpoint
        res = self.client.get("/v1/causal-mechanistic/traditional/formulations/TRIPHALA_TRIKATU/interactions")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["bioenhancer_present"])

        # 7. Entity lookups
        res = self.client.get("/v1/causal-mechanistic/entities/compounds/BERBERINE")
        self.assertEqual(res.status_code, 200)
        res = self.client.get("/v1/causal-mechanistic/entities/targets/AMPK")
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
