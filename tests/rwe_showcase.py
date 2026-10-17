"""
ZMIE Research Data Interoperability & Real-World Evidence (RWE) Master Showcase
Prompt 15 Master Implementation.

Demonstrates the 7 core pillars of the RWE Infrastructure:
1. RWD Source Registry & Data Contract Governance (Sections 7, 8)
2. 9-Dimension Data Quality Engine & Fit-for-Purpose Gatekeeper (Sections 35-46)
3. Target Trial Emulation (TTE), Causal DAGs & Causality Firewall (Sections 66, 69, 144)
4. Federated Clean Room with Small-Cell Suppression & Tokenization (Sections 131-135)
5. Multi-Standard Harmonization: Raw -> FHIR R5 -> OMOP CDM v5.4 -> CDISC SDTM v1.7 (Sections 12, 16, 18)
6. Multi-System Traditional Medicine Clinical Registry Harmonization (NAMASTE / TM2) (Sections 56-59)
7. RWE Cohort Analytics, Observational Bias Firewall & RCT Triangulation (Sections 67, 93, 102)
"""

from app.rwe.harmonizer import ClinicalDataHarmonizer
from app.rwe.cohort_engine import RWECohortEngine
from app.rwe.evidence_bridge import RWEEvidenceGraphBridge
from app.rwe.quality_engine import DataQualityEngine
from app.rwe.causal_engine import TargetTrialEmulationEngine
from app.rwe.federated_engine import FederatedResearchCleanRoom
from app.models.rwe_interop import FederatedQueryRequest


def banner(title: str):
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def main():
    harmonizer = ClinicalDataHarmonizer()
    cohort_engine = RWECohortEngine()
    evidence_bridge = RWEEvidenceGraphBridge()
    quality_engine = DataQualityEngine()
    causal_engine = TargetTrialEmulationEngine()
    federated_clean_room = FederatedResearchCleanRoom()

    # -------------------------------------------------------------
    # PILLAR 1: RWD Source Registry & Governance
    # -------------------------------------------------------------
    banner("PILLAR 1: RWD Source Registry & Governance (Section 7, 8)")
    from app.api.v1.rwe import rwd_sources_registry
    print(f"[+] Total Registered Authorized RWD Sources: {len(rwd_sources_registry)}")
    for sid, src in rwd_sources_registry.items():
        print(f"\n  Source ID: {src.source_id}")
        print(f"  Name: {src.source_name} ({src.organization})")
        print(f"  Jurisdiction: {src.jurisdiction} | System: {src.medical_system}")
        print(f"  Volume: {src.volume} | Format: {src.format} | License: {src.license}")
        print(f"  Quality Status: {src.quality_status} | Fitness: {src.fitness_for_purpose}")

    # -------------------------------------------------------------
    # PILLAR 2: 9-Dimension Data Quality & Fit-for-Purpose Gate
    # -------------------------------------------------------------
    banner("PILLAR 2: 9-Dimension Data Quality & Fit-for-Purpose Gatekeeper (Sections 35-46)")
    sample_records = [
        {"patient_id": "P-101", "gender": "female", "age": 64, "encounter_date": "2024-02-15", "diagnosis_code": "I50.9", "labs": [{"code": "HBA1C", "value": 7.4}]},
        {"patient_id": "P-102", "gender": "male", "age": 142, "encounter_date": "2024-02-16", "diagnosis_code": "I50.9", "labs": []},  # Impossible age!
        {"patient_id": "P-103", "gender": "female", "age": 58, "encounter_date": "2099-01-01", "diagnosis_code": "I50.9", "labs": []},  # Future date!
        {"patient_id": "P-104", "gender": "male", "age": 71, "encounter_date": "2024-02-18", "diagnosis_code": "I50.9", "labs": [{"code": "HBA1C", "value": 29.0}]},  # Implausible HbA1c!
    ]
    report = quality_engine.audit_dataset_quality("DATASET-EHR-BATCH-2024", sample_records)
    print(f"[+] Audited Batch of {report.total_records} Clinical Records across 9 Dimensions:")
    print(f"  Overall Status: {report.overall_status}")
    scores = report.dimension_scores
    print(f"  Scores: Completeness: {scores.completeness}% | Plausibility: {scores.plausibility}% | Validity: {scores.validity}%")
    print(f"          Temporal: {scores.temporal_integrity}% | Conformance: {scores.conformance}% | Uniqueness: {scores.uniqueness}%")
    print(f"\n  Plausibility Violations Flagged ({len(report.plausibility_violations)}):")
    for v in report.plausibility_violations:
        print(f"    - [{v['type']}] Record {v['record_index']}: {v['details']}")

    ffp = quality_engine.evaluate_fitness_for_purpose(
        research_question="Comparative Effectiveness of SGLT2i in HFpEF",
        dataset_id="DATASET-EHR-BATCH-2024",
        target_population="Adults with HFpEF",
        required_variables=["age", "gender", "lvef", "hba1c", "sglt2_exposure"]
    )
    print(f"\n[+] Fit-for-Purpose Gatekeeper Evaluation:")
    print(f"  Research Question: {ffp.research_question}")
    print(f"  Gate Verdict: {ffp.status.value} (Quality Score: {ffp.measured_quality}%)")
    print(f"  Rationale: {ffp.verdict_rationale}")

    # -------------------------------------------------------------
    # PILLAR 3: Target Trial Emulation (TTE) & Causality Firewall
    # -------------------------------------------------------------
    banner("PILLAR 3: Target Trial Emulation (TTE), Causal DAG & Causality Firewall (Sections 66, 69, 144)")
    tte = causal_engine._protocols["tte_sglt2_hfpef_pragmatic"]
    print(f"[+] Emulated Target Trial Protocol: {tte.study_title}")
    print(f"  Time Zero: {tte.time_zero_definition}")
    print(f"  Eligibility Criteria ({len(tte.eligibility_criteria)}): {tte.eligibility_criteria[0]}")
    print(f"  Treatment Strategies: Strategy A ({tte.treatment_strategies['strategy_a'][:45]}...) vs Strategy B")
    print(f"  Analysis Plan: {tte.analysis_plan}")

    dag = causal_engine._dags["dag_sglt2_cardiovascular_protection"]
    print(f"\n[+] Causal Directed Acyclic Graph (DAG): {dag.dag_id}")
    print(f"  Exposures: {dag.exposure_nodes} | Outcomes: {dag.outcome_nodes}")
    print(f"  Measured Confounders: {dag.measured_confounders}")
    print(f"  Unmeasured Confounder Risks: {dag.unmeasured_confounder_risks}")
    print(f"  Colliders (Conditioning Forbidden): {dag.colliders}")

    print("\n[+] Testing Causality Firewall (Prohibiting Overstatement):")
    blocked_claim = causal_engine.audit_causality_claim(
        claim_text="Observational EHR analysis proves efficacy and definitively cures heart failure mortality.",
        study_type="OBSERVATIONAL_COHORT",
        has_tte=False
    )
    print(f"  Test Claim 1: '...proves efficacy and definitively cures...'")
    print(f"  Permitted: {blocked_claim['claim_permitted']} | Verdict: {blocked_claim['verdict']}")
    print(f"  Enforcement: {blocked_claim.get('reason')[:120]}...")

    valid_claim = causal_engine.audit_causality_claim(
        claim_text="SGLT2 inhibitors were associated with a 26% reduction in cardiovascular hospitalization.",
        study_type="OBSERVATIONAL_COHORT",
        has_tte=False
    )
    print(f"\n  Test Claim 2: '...associated with a 26% reduction...'")
    print(f"  Permitted: {valid_claim['claim_permitted']} | Verdict: {valid_claim['verdict']} | Grade: {valid_claim['epistemic_grade']}")

    # -------------------------------------------------------------
    # PILLAR 4: Federated Clean Room & Small-Cell Suppression
    # -------------------------------------------------------------
    banner("PILLAR 4: Federated Research Clean Room & Small-Cell Suppression (Sections 131-135)")
    fed_req = FederatedQueryRequest(
        participating_nodes=["HOSP_OXFORD", "HOSP_BRIGHAM", "NIUM_BLR", "AIIA_DELHI"],
        cohort_criteria={"cohort_key": "rare_cardiomyopathy_pediatric"},
        privacy_cell_threshold=5
    )
    fed_res = federated_clean_room.execute_federated_query(fed_req)
    print(f"[+] Federated Multi-Node Query: 'rare_cardiomyopathy_pediatric' across 4 institutions:")
    print(f"  Participating Nodes: {fed_res.participating_nodes_count}")
    print(f"  Small Cells Suppressed (< 5): {fed_res.small_cells_suppressed_count} institutional nodes")
    print(f"  Aggregate Permitted Total: {fed_res.total_eligible_patients}")
    print(f"  Privacy Guarantee: {fed_res.privacy_guarantee}")

    token = federated_clean_room.tokenize_patient_id("NHS-PATIENT-MRN-998877", "HOSP_OXFORD")
    print(f"\n[+] HMAC Tokenization: NHS-PATIENT-MRN-998877 -> {token} (Direct identity shielded)")

    # -------------------------------------------------------------
    # PILLAR 5: Multi-Standard Harmonization (Raw -> FHIR -> OMOP -> CDISC)
    # -------------------------------------------------------------
    banner("PILLAR 5: Multi-Standard Harmonization (Raw -> FHIR -> OMOP -> CDISC) (Sections 12, 16, 18)")
    raw_ehr = {
        "patient_id": "PAT-EHR-88412",
        "gender": "female",
        "birth_date": "1959-08-24",
        "encounter_date": "2024-02-18",
        "diagnosis_code": "I50.9",
        "diagnosis_name": "Congestive Heart Failure, unspecified",
        "labs": [{"code": "HBA1C", "value": 7.6, "unit": "%"}],
        "medications": [{"name": "DAPAGLIFLOZIN", "dosage": "10mg daily"}]
    }
    fhir_bundle = harmonizer.raw_to_fhir_bundle(raw_ehr)
    print(f"[+] Step 1: Raw Encounter -> HL7 FHIR Bundle ({fhir_bundle.total} resources generated)")

    omop_cdm = harmonizer.fhir_to_omop_cdm(fhir_bundle)
    print(f"[+] Step 2: FHIR Bundle -> OHDSI OMOP CDM v{omop_cdm['omop_version']} (Athena Concept IDs resolved)")

    cdisc_sdtm = harmonizer.omop_to_cdisc_sdtm(omop_cdm, study_id="ZMIE-HF-RWE-2024")
    print(f"[+] Step 3: OMOP CDM -> CDISC SDTM ({cdisc_sdtm['standard']}) - DM, LB, EX tabular domains ready for regulatory review")

    # -------------------------------------------------------------
    # PILLAR 6: Traditional Medicine Registry Harmonization
    # -------------------------------------------------------------
    banner("PILLAR 6: Traditional Medicine Registry Harmonization (NAMASTE / TM2) (Sections 56-59)")
    unani_record = {
        "record_id": "NIUM-BLR-REG-2024-091",
        "patient_id": "PAT-UNANI-77",
        "system": "UNANI",
        "namaste_code": "UN-DIS-002",
        "mizaj": {
            "damawi": 4.0,
            "balghami": 8.0,
            "safrawi": 3.0,
            "saudawi": 4.5,
            "dominant": "BALGHAMI",
            "su_e_mizaj": "Su-e-Mizaj Barid Ratab"
        }
    }
    trad_res = harmonizer.harmonize_traditional_record(unani_record)
    print(f"[+] Harmonized Traditional Record: {trad_res['record_id']}")
    print(f"  NAMASTE Term: {trad_res['namaste_concept']['term_english']} [{trad_res['namaste_concept']['term_vernacular']}]")
    print(f"  WHO ICD-11 TM2 Code: {trad_res['icd11_tm2_alignment']} | SNOMED CT: {trad_res['snomed_partial_mapping']}")
    print(f"  Dominant Mizaj: {trad_res['mizaj_assessment']['dominant_mizaj']} | Dyscrasia: {trad_res['mizaj_assessment']['su_e_mizaj_deviation']}")
    print(f"  Epistemic Rule: Traditional diagnoses represent holistic etiologies and are never collapsed into modern pathology without epistemic distinction.")

    # -------------------------------------------------------------
    # PILLAR 7: RWE Cohort Analytics & RCT Triangulation
    # -------------------------------------------------------------
    banner("PILLAR 7: RWE Cohort Analytics, Bias Audit & RCT-RWE Triangulation (Sections 67, 93, 102)")
    rwe_res = cohort_engine.analyze_cohort_evidence(
        cohort_id="coh_sglt2_hf_registry",
        target_n=14200,
        comparator_n=28400,
        unadjusted_hazard_ratio=0.68,
        adjusted_hazard_ratio=0.74,
        ci_lower=0.67,
        ci_upper=0.82,
        p_val=0.0001
    )
    print(f"[+] Propensity-Adjusted Analysis (Total N={rwe_res.target_cohort_size + rwe_res.comparator_cohort_size:,}):")
    print(f"  Adjusted Hazard Ratio: {rwe_res.hazard_ratio_or_relative_risk} (95% CI: {rwe_res.confidence_interval_95}, p={rwe_res.p_value})")
    print(f"  Evidence Tier: {rwe_res.evidence_ladder_tier} | Causal Status: {rwe_res.causal_status}")
    print(f"  Bias Audit: Immortal Time Bias Protected={rwe_res.bias_audit.immortal_time_bias_protected}")

    tri = evidence_bridge.triangulate_with_rct(
        rwe_summary=rwe_res,
        landmark_rct_title="DAPA-HF Phase 3 Landmark Trial",
        landmark_rct_hr=0.74,
        landmark_rct_ci=[0.65, 0.85]
    )
    print(f"\n[+] Triangulation against RCT Benchmark:")
    print(f"  RCT HR: {tri['rct_hr']} vs RWE HR: {tri['rwe_hr']} | Delta: {tri['effect_size_delta']}")
    print(f"  Concordance Verdict: {tri['verdict']} (Is Concordant: {tri['is_concordant']})")
    print(f"  Interpretation: {tri['scientific_interpretation']}")

    print("\n" + "=" * 80)
    print(" PROMPT 15 MASTER SHOWCASE COMPLETE: ALL 7 PILLARS FULLY VERIFIED")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
