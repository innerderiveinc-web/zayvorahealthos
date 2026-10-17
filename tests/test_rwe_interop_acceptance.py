"""
Acceptance Test Suite for Prompt 15 Master:
ZMIE Research Data Interoperability & Real-World Evidence (RWE) Engine.
"""

import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.rwe.harmonizer import ClinicalDataHarmonizer
from app.rwe.cohort_engine import RWECohortEngine
from app.rwe.evidence_bridge import RWEEvidenceGraphBridge
from app.rwe.quality_engine import DataQualityEngine
from app.rwe.causal_engine import TargetTrialEmulationEngine
from app.rwe.federated_engine import FederatedResearchCleanRoom
from app.models.rwe_interop import (
    RWECohortDefinition,
    FHIRBundle,
    FederatedQueryRequest,
    TargetTrialProtocol,
    CausalDAG,
    FitForPurposeState
)
from app.models.graph import EvidenceLadder


class TestRWEInteropMasterAcceptance(unittest.TestCase):
    """Rigorous acceptance tests for Prompt 15 Master RWE & Data Interoperability engine."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.harmonizer = ClinicalDataHarmonizer()
        cls.cohort_engine = RWECohortEngine()
        cls.evidence_bridge = RWEEvidenceGraphBridge()
        cls.quality_engine = DataQualityEngine()
        cls.causal_engine = TargetTrialEmulationEngine()
        cls.federated_clean_room = FederatedResearchCleanRoom()

    def test_01_raw_to_fhir_bundle(self):
        """Verifies ingestion and transformation of raw EHR encounter into HL7 FHIR Bundle."""
        raw_encounter = {
            "patient_id": "P-90210",
            "gender": "male",
            "birth_date": "1965-04-12",
            "encounter_date": "2024-03-01",
            "diagnosis_code": "I50.9",
            "diagnosis_name": "Heart failure",
            "labs": [
                {"code": "HBA1C", "value": 7.4, "unit": "%"},
                {"code": "BNP", "value": 520.0, "unit": "pg/mL"}
            ],
            "medications": [
                {"name": "DAPAGLIFLOZIN", "dosage": "10mg daily"}
            ]
        }
        bundle = self.harmonizer.raw_to_fhir_bundle(raw_encounter)
        self.assertIsInstance(bundle, FHIRBundle)
        self.assertEqual(bundle.resourceType, "Bundle")
        self.assertEqual(bundle.total, 5)

        types = [item["resource"]["resourceType"] for item in bundle.entry]
        self.assertIn("Patient", types)
        self.assertIn("Condition", types)
        self.assertIn("Observation", types)
        self.assertIn("MedicationStatement", types)

    def test_02_fhir_to_omop_cdm_mapping(self):
        """Verifies transformation from HL7 FHIR to OHDSI OMOP CDM v5.4 tables and concept mapping."""
        raw_encounter = {
            "patient_id": "P-90210",
            "gender": "female",
            "birth_date": "1972-11-20",
            "diagnosis_code": "I50.9",
            "labs": [{"code": "HBA1C", "value": 6.8, "unit": "%"}],
            "medications": [{"name": "DAPAGLIFLOZIN", "dosage": "10mg"}]
        }
        bundle = self.harmonizer.raw_to_fhir_bundle(raw_encounter)
        omop = self.harmonizer.fhir_to_omop_cdm(bundle)

        self.assertEqual(omop["omop_version"], "5.4")
        self.assertEqual(len(omop["person"]), 1)
        self.assertEqual(omop["person"][0]["gender_concept_id"], 8532)
        self.assertEqual(omop["person"][0]["year_of_birth"], 1972)

        self.assertEqual(omop["condition_occurrence"][0]["condition_concept_id"], 316139)
        self.assertEqual(omop["drug_exposure"][0]["drug_concept_id"], 43534760)
        self.assertEqual(omop["measurement"][0]["measurement_concept_id"], 3004410)

    def test_03_omop_to_cdisc_sdtm_mapping(self):
        """Verifies transformation from OMOP CDM to CDISC SDTM tabular domains (DM, LB, EX)."""
        omop_data = {
            "person": [{"person_id": 1001, "gender_concept_id": 8507, "year_of_birth": 1960}],
            "measurement": [{"person_id": 1001, "measurement_source_value": "HBA1C", "value_as_number": 7.5, "measurement_date": "2024-01-15"}],
            "drug_exposure": [{"person_id": 1001, "drug_source_value": "Dapagliflozin", "drug_exposure_start_date": "2024-01-15"}]
        }
        sdtm = self.harmonizer.omop_to_cdisc_sdtm(omop_data, study_id="ZMIE-HF-RWE")

        self.assertEqual(sdtm["study_id"], "ZMIE-HF-RWE")
        self.assertEqual(len(sdtm["DM"]), 1)
        self.assertEqual(sdtm["DM"][0]["SEX"], "M")
        self.assertEqual(sdtm["DM"][0]["ARMCD"], "RWE_OBS")

        self.assertEqual(len(sdtm["LB"]), 1)
        self.assertEqual(sdtm["LB"][0]["LBTESTCD"], "HBA1C")
        self.assertEqual(sdtm["LB"][0]["LBSTRESN"], 7.5)

        self.assertEqual(len(sdtm["EX"]), 1)
        self.assertEqual(sdtm["EX"][0]["EXTRT"], "Dapagliflozin")

    def test_04_traditional_registry_harmonization(self):
        """Verifies traditional medicine clinical registry harmonization (NAMASTE / TM2 / Mizaj)."""
        unani_raw = {
            "record_id": "REC-NIUM-001",
            "patient_id": "PAT-U-101",
            "system": "UNANI",
            "namaste_code": "UN-DIS-002",
            "mizaj": {
                "damawi": 4.0,
                "balghami": 7.5,
                "safrawi": 3.0,
                "saudawi": 4.5,
                "dominant": "BALGHAMI",
                "su_e_mizaj": "Su-e-Mizaj Barid Ratab"
            }
        }
        result = self.harmonizer.harmonize_traditional_record(unani_raw)

        self.assertEqual(result["system"], "UNANI")
        self.assertIsNotNone(result["namaste_concept"])
        self.assertEqual(result["namaste_concept"]["term_english"], "Zof-e-Qalb (Cardiac Debility / Heart Failure)")
        self.assertEqual(result["icd11_tm2_alignment"], "TM2-UN-I50")
        self.assertEqual(result["snomed_partial_mapping"], "84114007")

        self.assertIn("mizaj_assessment", result)
        self.assertEqual(result["mizaj_assessment"]["dominant_mizaj"], "BALGHAMI")
        self.assertIn("epistemic_warning", result)

    def test_05_data_quality_audit_9_dimensions_and_plausibility(self):
        """Verifies dedicated Data Quality Engine auditing 9 dimensions and flagging plausibility violations."""
        records = [
            {"patient_id": "P-VALID", "age": 62, "encounter_date": "2024-01-10", "diagnosis_code": "I50.9", "labs": [{"code": "HBA1C", "value": 7.2}]},
            {"patient_id": "P-BAD-AGE", "age": 145, "encounter_date": "2024-01-11", "diagnosis_code": "I50.9", "labs": []},  # Impossible age!
            {"patient_id": "P-FUTURE", "age": 45, "encounter_date": "2099-01-01", "diagnosis_code": "I50.9", "labs": []},  # Future date!
            {"patient_id": "P-IMPLAUSIBLE-LAB", "age": 55, "encounter_date": "2024-01-12", "diagnosis_code": "I50.9", "labs": [{"code": "HBA1C", "value": 28.5}]},  # Implausible HbA1c!
        ]
        report = self.quality_engine.audit_dataset_quality("DATASET_AUDIT_01", records)
        self.assertEqual(report.total_records, 4)
        self.assertGreaterEqual(len(report.plausibility_violations), 3)

        violation_types = [v["type"] for v in report.plausibility_violations]
        self.assertIn("IMPLAUSIBLE_AGE", violation_types)
        self.assertIn("FUTURE_DATE_ERROR", violation_types)
        self.assertIn("IMPLAUSIBLE_LAB_VALUE", violation_types)
        self.assertIsNotNone(report.dimension_scores.completeness)
        self.assertIsNotNone(report.dimension_scores.plausibility)

    def test_06_fitness_for_purpose_gate(self):
        """Verifies Fit-for-Purpose Gatekeeper before dataset is accepted for analysis."""
        assessment = self.quality_engine.evaluate_fitness_for_purpose(
            research_question="Comparative Effectiveness of SGLT2i in HFpEF",
            dataset_id="DATASET_HF_01",
            target_population="Adults with HFpEF",
            required_variables=["age", "sex", "lvef", "sglt2_exposure", "hf_hospitalization"]
        )
        self.assertEqual(assessment.status, FitForPurposeState.FIT)
        self.assertGreaterEqual(assessment.measured_quality, 85.0)

    def test_07_target_trial_emulation_and_causal_dag(self):
        """Verifies Target Trial Emulation (TTE) protocol and Causal DAG registration."""
        tte = self.causal_engine._protocols.get("tte_sglt2_hfpef_pragmatic")
        self.assertIsNotNone(tte)
        self.assertEqual(tte.follow_up_period_days, 730)
        self.assertIn("New-User Design", " ".join(tte.eligibility_criteria))

        dag = self.causal_engine._dags.get("dag_sglt2_cardiovascular_protection")
        self.assertIsNotNone(dag)
        self.assertIn("SGLT2_Inhibitor_Exposure", dag.exposure_nodes)
        self.assertIn("Hospital_Encounter_Selection", dag.colliders)

    def test_08_causality_firewall(self):
        """Verifies that the Causality Firewall blocks ungrounded causal claims from purely observational data."""
        # 1. Prohibited claim without TTE -> Must be blocked!
        audit_blocked = self.causal_engine.audit_causality_claim(
            claim_text="Observational EHR analysis causes complete eradication of heart failure mortality.",
            study_type="OBSERVATIONAL_COHORT",
            has_tte=False
        )
        self.assertFalse(audit_blocked["claim_permitted"])
        self.assertEqual(audit_blocked["verdict"], "CAUSALITY_VIOLATION_BLOCKED")

        # 2. Compliant claim -> Must pass!
        audit_passed = self.causal_engine.audit_causality_claim(
            claim_text="SGLT2 inhibitors were associated with reduced cardiovascular death in routine clinical practice.",
            study_type="OBSERVATIONAL_COHORT",
            has_tte=False
        )
        self.assertTrue(audit_passed["claim_permitted"])
        self.assertEqual(audit_passed["verdict"], "CLAIM_GOVERNANCE_PASSED")

    def test_09_federated_clean_room_and_small_cell_suppression(self):
        """Verifies federated query execution with small-cell disclosure suppression (< 5 subjects)."""
        req = FederatedQueryRequest(
            participating_nodes=["HOSP_OXFORD", "HOSP_BRIGHAM", "NIUM_BLR"],
            cohort_criteria={"cohort_key": "rare_cardiomyopathy_pediatric"},
            privacy_cell_threshold=5
        )
        result = self.federated_clean_room.execute_federated_query(req)
        # All three nodes have < 5 cases (3, 2, 1) -> All 3 must be suppressed!
        self.assertEqual(result.small_cells_suppressed_count, 3)
        self.assertEqual(result.total_eligible_patients, 0)
        self.assertIn("K_ANONYMITY_PROTECTED", result.privacy_guarantee)

        # Tokenization test
        token = self.federated_clean_room.tokenize_patient_id("MRN-998877", "HOSP_OXFORD")
        self.assertTrue(token.startswith("SUBJ-"))
        self.assertEqual(len(token), 21)

    def test_10_rwe_cohort_definition_and_bias_audit(self):
        """Verifies RWE cohort definition, propensity covariates, and bias auditing."""
        cohort = self.cohort_engine.get_cohort("coh_sglt2_hf_registry")
        self.assertIsNotNone(cohort)
        self.assertGreaterEqual(len(cohort.propensity_score_covariates), 5)

        summary = self.cohort_engine.analyze_cohort_evidence(
            cohort_id="coh_sglt2_hf_registry",
            target_n=15000,
            comparator_n=30000,
            unadjusted_hazard_ratio=0.69,
            adjusted_hazard_ratio=0.74,
            ci_lower=0.67,
            ci_upper=0.82,
            p_val=0.0001
        )
        self.assertEqual(summary.evidence_ladder_tier, "E5_HUMAN_OBSERVATIONAL_RWE")
        self.assertEqual(summary.hazard_ratio_or_relative_risk, 0.74)
        self.assertTrue(summary.bias_audit.immortal_time_bias_protected)
        self.assertIsNotNone(summary.provenance_hash)

    def test_11_evidence_graph_bridge_and_triangulation(self):
        """Verifies conversion of RWE summary into EvidenceObject and triangulation against landmark RCTs."""
        summary = self.cohort_engine.analyze_cohort_evidence(
            cohort_id="coh_sglt2_hf_registry",
            target_n=15000,
            comparator_n=30000,
            unadjusted_hazard_ratio=0.69,
            adjusted_hazard_ratio=0.74
        )

        ev_obj = self.evidence_bridge.bridge_rwe_to_evidence_graph(
            rwe_summary=summary,
            intervention_concept="Dapagliflozin",
            disease_concept="Heart Failure"
        )
        self.assertEqual(ev_obj.evidence_level, EvidenceLadder.E5_HUMAN_OBSERVATIONAL)
        self.assertEqual(ev_obj.sample_size, 45000)
        self.assertIn("Dapagliflozin", ev_obj.pico_context.intervention_agent)

        triangulation = self.evidence_bridge.triangulate_with_rct(
            rwe_summary=summary,
            landmark_rct_title="DAPA-HF Landmark Trial",
            landmark_rct_hr=0.74,
            landmark_rct_ci=[0.65, 0.85]
        )
        self.assertTrue(triangulation["is_concordant"])
        self.assertEqual(triangulation["verdict"], "HIGHLY_CONCORDANT")
        self.assertEqual(triangulation["effect_size_delta"], 0.0)

    def test_12_master_rest_api_endpoints(self):
        """Verifies FastAPI REST API endpoints for Prompt 15 Master RWE layer."""
        # 1. RWD Sources
        resp_sources = self.client.get("/v1/rwe/sources")
        self.assertEqual(resp_sources.status_code, 200)
        self.assertGreaterEqual(len(resp_sources.json()), 2)

        # 2. Data Quality Audit API
        resp_audit = self.client.post("/v1/rwe/quality/audit", json={
            "dataset_id": "DS-TEST-API",
            "source_id": "SRC-OXFORD-EHR",
            "records": [
                {"patient_id": "P-1", "gender": "female", "age": 70, "encounter_date": "2024-01-01", "diagnosis_code": "I50.9"}
            ]
        })
        self.assertEqual(resp_audit.status_code, 200)
        self.assertEqual(resp_audit.json()["overall_status"], "QUALITY_PASSED")

        # 3. TTE Protocol API
        resp_tte = self.client.get("/v1/rwe/tte/protocols/tte_sglt2_hfpef_pragmatic")
        self.assertEqual(resp_tte.status_code, 200)
        self.assertIn("Emulated Pragmatic Target Trial", resp_tte.json()["study_title"])

        # 4. Causality Audit API
        resp_causal = self.client.post("/v1/rwe/tte/audit-claim", json={
            "claim_text": "SGLT2 inhibitors were associated with reduced hospitalization.",
            "study_type": "OBSERVATIONAL_COHORT",
            "has_target_trial_emulation": False
        })
        self.assertEqual(resp_causal.status_code, 200)
        self.assertTrue(resp_causal.json()["claim_permitted"])

        # 5. Federated Query API
        resp_fed = self.client.post("/v1/rwe/federated/query", json={
            "participating_nodes": ["HOSP_OXFORD", "HOSP_BRIGHAM"],
            "cohort_criteria": {"cohort_key": "heart_failure_sglt2"},
            "privacy_cell_threshold": 5
        })
        self.assertEqual(resp_fed.status_code, 200)
        self.assertGreater(resp_fed.json()["total_eligible_patients"], 10000)

        # 6. Federated Tokenize API
        resp_tok = self.client.get("/v1/rwe/federated/tokenize?patient_id=PT-1234&facility=OXFORD")
        self.assertEqual(resp_tok.status_code, 200)
        self.assertIn("SUBJ-", resp_tok.json()["research_subject_id"])


if __name__ == "__main__":
    unittest.main()
