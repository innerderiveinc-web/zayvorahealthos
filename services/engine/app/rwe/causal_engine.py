"""
ZMIE Target Trial Emulation (TTE) & Causal Inference Engine
Prompt 15 Master Implementation.

Implements:
1. Target Trial Emulation (TTE) Protocol Definition (Hernán & Robins framework)
2. Causal Directed Acyclic Graphs (DAGs) with confounders, mediators, and colliders
3. Negative Control Exposure / Outcome sensitivity designs
4. Strict Causality Firewall preventing illegitimate extrapolation of associations into causal assertions
"""

from typing import List, Dict, Any, Optional
import uuid

from app.models.rwe_interop import TargetTrialProtocol, CausalDAG


class TargetTrialEmulationEngine:
    """
    Formulates and audits target trial emulation protocols, causal DAGs,
    and safeguards scientific validity against confounding and immortal time bias.
    """

    def __init__(self):
        self._protocols: Dict[str, TargetTrialProtocol] = {}
        self._dags: Dict[str, CausalDAG] = {}
        self._seed_default_protocols()

    def _seed_default_protocols(self):
        """Seed representative TTE protocols and DAGs."""
        tte_sglt2 = TargetTrialProtocol(
            protocol_id="tte_sglt2_hfpef_pragmatic",
            study_title="Emulated Pragmatic Target Trial: SGLT2 Inhibitors vs Active Comparator in Routine HFpEF Care",
            eligibility_criteria=[
                "Age >= 18 at Time Zero",
                "LVEF >= 50% documented within 6 months prior",
                "Elevated NT-proBNP (> 300 pg/mL in sinus rhythm, > 900 pg/mL in AF)",
                "No SGLT2i exposure in previous 365 days (New-User Design)"
            ],
            treatment_strategies={
                "strategy_a": "Initiate Dapagliflozin 10mg within 14 days of diagnosis and continue",
                "strategy_b": "Initiate standard active comparator (GLP-1 RA or standard diuretic regimen) and continue"
            },
            assignment_procedure="Propensity-score matched pseudo-randomization based on 18 baseline prognostic covariates",
            time_zero_definition="Date of first dispensing of strategy medication (synchronous with eligibility baseline)",
            follow_up_period_days=730,
            outcome_definitions=[
                "Primary: Composite of cardiovascular death or hospitalization for heart failure",
                "Secondary: All-cause mortality, change in eGFR over 2 years"
            ],
            causal_contrast="Observational analog of Intention-to-Treat (ITT) effect and Per-Protocol effect",
            analysis_plan="Inverse Probability of Treatment Weighting (IPTW) Cox proportional hazards regression",
            censoring_rules=[
                "Censored at administrative study end date (2024-12-31)",
                "Censored at loss to follow-up (> 90 days without EHR encounter)",
                "Censored at switch of treatment strategy (per-protocol analysis only)"
            ]
        )
        self._protocols[tte_sglt2.protocol_id] = tte_sglt2

        dag_sglt2 = CausalDAG(
            dag_id="dag_sglt2_cardiovascular_protection",
            exposure_nodes=["SGLT2_Inhibitor_Exposure"],
            mediator_nodes=["Myocardial_Energetics", "Natriuresis_Plasma_Volume", "Renal_Hyperfiltration_Reduction"],
            outcome_nodes=["Cardiovascular_Mortality", "Heart_Failure_Hospitalization"],
            measured_confounders=["Age", "Baseline_eGFR", "Diabetes_Duration", "Hypertension", "Prior_MI", "BMI"],
            unmeasured_confounder_risks=["Dietary_Sodium_Adherence", "Subclinical_Frailty", "Over-the-counter_NSAID_Use"],
            colliders=["Hospital_Encounter_Selection"],
            effect_modifiers=["Baseline_HbA1c", "Gender", "Baseline_CKD_Stage"],
            edges=[
                {"from": "Age", "to": "SGLT2_Inhibitor_Exposure"},
                {"from": "Age", "to": "Cardiovascular_Mortality"},
                {"from": "Baseline_eGFR", "to": "SGLT2_Inhibitor_Exposure"},
                {"from": "Baseline_eGFR", "to": "Cardiovascular_Mortality"},
                {"from": "SGLT2_Inhibitor_Exposure", "to": "Myocardial_Energetics"},
                {"from": "Myocardial_Energetics", "to": "Heart_Failure_Hospitalization"},
                {"from": "SGLT2_Inhibitor_Exposure", "to": "Heart_Failure_Hospitalization"},
            ],
            testable_implications=[
                "Adjusting for Age and Baseline_eGFR d-separates backdoor paths between exposure and primary outcome.",
                "Conditioning on Hospital_Encounter_Selection (Collider) induces spurious association."
            ]
        )
        self._dags[dag_sglt2.dag_id] = dag_sglt2

    def register_target_trial(self, protocol: TargetTrialProtocol) -> TargetTrialProtocol:
        self._protocols[protocol.protocol_id] = protocol
        return protocol

    def register_causal_dag(self, dag: CausalDAG) -> CausalDAG:
        self._dags[dag.dag_id] = dag
        return dag

    def audit_causality_claim(self, claim_text: str, study_type: str, has_tte: bool) -> Dict[str, Any]:
        """
        Causality Firewall: Rejects illegitimate claims asserting 'causes' or 'proves efficacy'
        from purely observational or predictive models.
        """
        claim_lower = claim_text.lower()
        prohibited_words = ["causes", "proven cure", "guarantees", "proves efficacy", "definitively shows that drug cures"]

        violations = [w for w in prohibited_words if w in claim_lower]

        if violations and not has_tte:
            return {
                "claim_permitted": False,
                "verdict": "CAUSALITY_VIOLATION_BLOCKED",
                "reason": (
                    f"Observational RWE without an active Target Trial Emulation (TTE) protocol "
                    f"cannot claim causal certainty. Detected prohibited terminology: {violations}. "
                    f"Must rephrase as 'associated with', 'observed in real-world practice', or 'causal hypothesis'."
                ),
                "safe_rephrased_statement": f"In an observational cohort, the intervention was associated with favorable endpoints."
            }

        return {
            "claim_permitted": True,
            "verdict": "CLAIM_GOVERNANCE_PASSED",
            "study_type": study_type,
            "has_target_trial_emulation": has_tte,
            "epistemic_grade": "OBSERVATIONAL_CAUSAL_INFERENCE" if has_tte else "ASSOCIATIONAL_EPIDEMIOLOGY"
        }

    def generate_negative_control_design(self, target_exposure: str, target_outcome: str) -> Dict[str, Any]:
        """
        Synthesizes a Negative Control Exposure & Outcome design to calibrate
        residual confounding and unmeasured bias.
        """
        return {
            "target_exposure": target_exposure,
            "target_outcome": target_outcome,
            "negative_control_exposure": {
                "agent": "Influenza_Vaccination_in_Summer" if "SGLT2" in target_exposure else "Vitamin_B12_Supplementation",
                "hypothesis": "No biologically plausible mechanism should link negative control to primary cardiac outcome. Non-null HR reveals unmeasured healthy user bias."
            },
            "negative_control_outcome": {
                "endpoint": "Accidental_Trauma_Fracture",
                "hypothesis": "Cardiovascular drug should have true null effect on accidental trauma. Observed hazard ratio divergence indicates confounding by frailty."
            },
            "interpretation_guideline": "If negative control outcome yields HR significantly different from 1.0 (p < 0.05), primary effect estimate must be calibrated down."
        }
