"""ZMIE Medical Knowledge Simulation, Research Hypothesis & Next-Best-Experiment Engine Acceptance Tests.

Verifies:
1. Epistemic status enforcement (OBSERVED, MODEL_PREDICTED, HYPOTHESIZED, ACTUALLY_TESTED never conflated)
2. Hypothesis generation & traditional medicine bridge hypotheses (Unani/Ayurveda)
3. Competing hypothesis discrimination (identifies divergent predictions & decisive endpoints)
4. Scientific simulation execution (Monte Carlo PK/PD parameter uncertainty, 95% CIs, MODEL_PREDICTED disclaimer)
5. Next-best-experiment design (Information Gain E[ΔU], anti-redundancy check, control groups, human-approval guarantee)
6. Empirical result ingestion & Bayesian posterior updating (supports/weakens competing hypotheses)
7. Research opportunity discovery
8. FastAPI REST endpoints verification
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.models.simulation_hypothesis import (
    EpistemicStatus,
    ExperimentDesignType,
    HypothesisStatus,
    HypothesisType,
)
from app.simulation_hypothesis.engine import SimulationHypothesisEngine


class TestSimulationHypothesisAcceptance(unittest.TestCase):
    """Rigorous acceptance test suite for Prompt 19 Simulation & Hypothesis Engine."""

    def setUp(self):
        self.engine = SimulationHypothesisEngine()
        self.client = TestClient(app)

    def test_01_epistemic_status_and_seeded_hypotheses(self):
        """Verifies seeded hypotheses maintain strict epistemic status and falsification criteria."""
        hypotheses = self.engine.list_hypotheses()
        self.assertGreaterEqual(len(hypotheses), 3)

        ids = [h.hypothesis_id for h in hypotheses]
        self.assertIn("HYP-SGLT2-NHE1", ids)
        self.assertIn("HYP-SGLT2-HEMO", ids)
        self.assertIn("HYP-UNANI-GULQAND-BARRIER", ids)

        nhe1 = self.engine.get_hypothesis("HYP-SGLT2-NHE1")
        self.assertIsNotNone(nhe1)
        self.assertEqual(nhe1.hypothesis_type, HypothesisType.MECHANISTIC)
        self.assertEqual(nhe1.epistemic_status, EpistemicStatus.HYPOTHESIZED)
        self.assertGreater(len(nhe1.predictions), 0)
        self.assertEqual(nhe1.predictions[0].epistemic_status, EpistemicStatus.MODEL_PREDICTED)
        self.assertGreater(len(nhe1.falsification_criteria), 0)

    def test_02_traditional_medicine_bridge_hypothesis(self):
        """Verifies traditional medicine bridge hypothesis maintains native conceptual framework without retrofitting."""
        hyp_unani = self.engine.get_hypothesis("HYP-UNANI-GULQAND-BARRIER")
        self.assertIsNotNone(hyp_unani)
        self.assertEqual(hyp_unani.hypothesis_type, HypothesisType.TRADITIONAL_BRIDGE)
        self.assertIsNotNone(hyp_unani.traditional_medicine_bridge)

        bridge = hyp_unani.traditional_medicine_bridge
        self.assertIn("traditional_construct", bridge)
        self.assertIn("Hararat", bridge["traditional_construct"])
        self.assertIn("molecular_correlate", bridge)
        self.assertIn("epistemic_note", bridge)
        self.assertIn("without modern retrospective retrofitting", bridge["epistemic_note"])

    def test_03_competing_hypothesis_discrimination(self):
        """Verifies automated discrimination between competing hypotheses generates decisive experiments."""
        report = self.engine.discriminate_competing_hypotheses("HYP-SGLT2-NHE1", "HYP-SGLT2-HEMO")
        self.assertIsNotNone(report)
        self.assertGreater(len(report.divergence_points), 0)
        self.assertGreater(len(report.recommended_experiments), 0)

        exp = report.recommended_experiments[0]
        self.assertGreater(exp.information_gain_score, 0.8)
        self.assertGreater(exp.discrimination_power, 0.8)
        self.assertIn("HYP-SGLT2-NHE1", exp.expected_outcomes)
        self.assertIn("HYP-SGLT2-HEMO", exp.expected_outcomes)
        self.assertTrue(exp.existing_data_checked)
        self.assertTrue(exp.human_approval_required)

    def test_04_computational_simulation_monte_carlo_sweep(self):
        """Verifies PK/PD simulation under parameter uncertainty tags output strictly as MODEL_PREDICTED."""
        sim = self.engine.run_simulation(
            model_id="MOD-PKPD-SGLT2",
            scenario_name="Standard Therapeutic Dose 25mg Empagliflozin",
            dose_or_perturbation=25.0,
            time_points_hours=[1.0, 2.0, 4.0, 8.0, 24.0],
            monte_carlo_iterations=200,
        )

        self.assertIsNotNone(sim)
        self.assertEqual(sim.epistemic_status, EpistemicStatus.MODEL_PREDICTED)
        self.assertIn("SIMULATION ONLY", sim.epistemic_disclaimer)
        self.assertIn("time_course", sim.predicted_outcomes)
        self.assertEqual(len(sim.predicted_outcomes["time_course"]), 5)

        # Verify credible intervals are computed
        self.assertIn("conc_at_2.0h", sim.credible_intervals_95)
        ci = sim.credible_intervals_95["conc_at_2.0h"]
        self.assertEqual(len(ci), 2)
        self.assertLessEqual(ci[0], ci[1])

    def test_05_next_best_experiment_design(self):
        """Verifies next-best-experiment incorporates information gain, complete controls, and anti-redundancy."""
        proposal = self.engine.propose_next_best_experiment(
            target_hypothesis_id="HYP-SGLT2-NHE1",
            preferred_design_type=ExperimentDesignType.IN_VITRO_ASSAY,
        )

        self.assertIsNotNone(proposal)
        self.assertGreater(proposal.information_gain_score, 0.5)
        self.assertIn("positive_control", proposal.controls)
        self.assertIn("negative_control", proposal.controls)
        self.assertTrue(proposal.existing_data_checked)
        self.assertTrue(proposal.human_approval_required)

    def test_06_result_ingestion_and_bayesian_posterior_updating(self):
        """Verifies ingestion of empirical data (OBSERVED status) updates Bayesian posteriors and weakens competitors."""
        # 1. Propose experiment
        proposal = self.engine.propose_next_best_experiment("HYP-SGLT2-NHE1")

        hyp_nhe1_before = self.engine.get_hypothesis("HYP-SGLT2-NHE1")
        hyp_hemo_before = self.engine.get_hypothesis("HYP-SGLT2-HEMO")
        prior_nhe1 = hyp_nhe1_before.current_posterior
        prior_hemo = hyp_hemo_before.current_posterior

        # 2. Ingest empirical result supporting NHE-1 hypothesis (observed reduction in diastolic Ca2+ in isolated heart)
        result = self.engine.ingest_experiment_result(
            proposal_id=proposal.proposal_id,
            observed_direction="DECREASE",
            observed_value=-29.4,
            confidence_interval=[-34.2, -24.6],
            p_value=0.002,
            laboratory_provenance={
                "lab_name": "Cardiovascular Research Core",
                "instrument": "IonOptix MyoCam-S & Fluorometry",
                "run_id": "EXP-2026-NHE1-094",
            },
        )

        self.assertEqual(result.epistemic_status, EpistemicStatus.OBSERVED)
        self.assertEqual(result.effect_on_hypothesis, "SUPPORTS")
        self.assertGreater(result.updated_posterior, prior_nhe1)

        # 3. Check hypothesis status update
        hyp_nhe1_after = self.engine.get_hypothesis("HYP-SGLT2-NHE1")
        self.assertEqual(hyp_nhe1_after.status, HypothesisStatus.SUPPORTED)

        # 4. Check competitor hypothesis weakened
        hyp_hemo_after = self.engine.get_hypothesis("HYP-SGLT2-HEMO")
        self.assertLess(hyp_hemo_after.current_posterior, prior_hemo)
        self.assertEqual(hyp_hemo_after.status, HypothesisStatus.WEAKENED)

    def test_07_research_opportunities_discovery(self):
        """Verifies discovery of prioritized research opportunities."""
        opportunities = self.engine.discover_research_opportunities()
        self.assertGreaterEqual(len(opportunities), 3)

        domains = [o.scientific_domain for o in opportunities]
        self.assertIn("Cardiovascular Pharmacology", domains)
        self.assertIn("Integrative Gastroenterology & Traditional Medicine", domains)

    def test_08_fastapi_rest_endpoints(self):
        """Verifies all FastAPI simulation-hypothesis REST endpoints operate correctly."""
        # GET /v1/simulation-hypothesis/hypotheses
        resp = self.client.get("/v1/simulation-hypothesis/hypotheses")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 3)

        # POST /v1/simulation-hypothesis/hypotheses/competing/discriminate
        resp_disc = self.client.post(
            "/v1/simulation-hypothesis/hypotheses/competing/discriminate",
            json={
                "hypothesis_id_a": "HYP-SGLT2-NHE1",
                "hypothesis_id_b": "HYP-SGLT2-HEMO",
            },
        )
        self.assertEqual(resp_disc.status_code, 200)
        disc_data = resp_disc.json()
        self.assertIn("divergence_points", disc_data)
        self.assertIn("recommended_experiments", disc_data)

        # POST /v1/simulation-hypothesis/simulations/run
        resp_sim = self.client.post(
            "/v1/simulation-hypothesis/simulations/run",
            json={
                "model_id": "MOD-PKPD-SGLT2",
                "scenario_name": "API Test Simulation",
                "dose_or_perturbation": 10.0,
                "monte_carlo_iterations": 100,
            },
        )
        self.assertEqual(resp_sim.status_code, 200)
        sim_data = resp_sim.json()
        self.assertEqual(sim_data["epistemic_status"], "MODEL_PREDICTED")
        self.assertIn("time_course", sim_data["predicted_outcomes"])

        # POST /v1/simulation-hypothesis/experiments/next-best
        resp_exp = self.client.post(
            "/v1/simulation-hypothesis/experiments/next-best",
            json={"target_hypothesis_id": "HYP-SGLT2-NHE1"},
        )
        self.assertEqual(resp_exp.status_code, 200)
        exp_data = resp_exp.json()
        self.assertIn("proposal_id", exp_data)
        self.assertTrue(exp_data["human_approval_required"])

        # GET /v1/simulation-hypothesis/opportunities
        resp_opp = self.client.get("/v1/simulation-hypothesis/opportunities")
        self.assertEqual(resp_opp.status_code, 200)
        opp_data = resp_opp.json()
        self.assertIsInstance(opp_data, list)
        self.assertGreaterEqual(len(opp_data), 3)


if __name__ == "__main__":
    unittest.main()
