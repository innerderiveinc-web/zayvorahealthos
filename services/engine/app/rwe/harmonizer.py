"""
ZMIE Research Data Harmonization Engine
Prompt 15 Implementation.

Performs multi-standard harmonization across:
- Raw Clinical EHR/Encounter JSON
- HL7 FHIR (R4/R5) Resources
- OHDSI OMOP Common Data Model (v5.4)
- CDISC SDTM Study Data Tabulation Domains
- Traditional Medicine Standards (NAMASTE, WHO ICD-11 TM2, Mizaj, Prakriti)
"""

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.models.rwe_interop import (
    FHIRPatient,
    FHIRCondition,
    FHIRObservation,
    FHIRMedicationStatement,
    FHIRBundle,
    FHIRCoding,
    FHIRCodeableConcept,
    FHIRQuantity,
    OMOPPerson,
    OMOPConditionOccurrence,
    OMOPDrugExposure,
    OMOPMeasurement,
    OMOPConcept,
    CDISCDemographics,
    CDISCLaboratory,
    CDISCExposure,
    CDISCAdverseEvent,
    NAMASTEConcept,
    MizajAssessmentRecord,
    PrakritiAssessmentRecord,
    TraditionalCompoundExposure,
)


class ClinicalDataHarmonizer:
    """
    Translates raw EHR encounters into HL7 FHIR, maps FHIR into OHDSI OMOP CDM,
    converts OMOP records into CDISC SDTM domains, and harmonizes traditional
    medical registries (NAMASTE/ICD-11 TM2).
    """

    def __init__(self):
        self._vocabularies: Dict[str, Dict[str, Any]] = self._init_standard_vocabularies()
        self._namaste_registry: Dict[str, NAMASTEConcept] = self._init_namaste_registry()

    def _init_standard_vocabularies(self) -> Dict[str, Dict[str, Any]]:
        """Pre-loaded clinical ontology mappings (SNOMED, RxNorm, LOINC, ICD-10)."""
        return {
            # Conditions
            "I50.9": {"omop_id": 316139, "snomed": "84114007", "name": "Heart failure"},
            "E11.9": {"omop_id": 201826, "snomed": "44054006", "name": "Type 2 diabetes mellitus"},
            "I10": {"omop_id": 320128, "snomed": "38341003", "name": "Essential hypertension"},
            # Drugs
            "DAPAGLIFLOZIN": {"omop_id": 43534760, "rxnorm": "1488564", "name": "Dapagliflozin 10 MG Oral Tablet"},
            "METFORMIN": {"omop_id": 1503297, "rxnorm": "860975", "name": "Metformin hydrochloride 500 MG Oral Tablet"},
            # Labs
            "HBA1C": {"omop_id": 3004410, "loinc": "4548-4", "name": "Hemoglobin A1c/Hemoglobin.total in Blood"},
            "BNP": {"omop_id": 3009106, "loinc": "30934-4", "name": "Brain natriuretic peptide in Serum or Plasma"},
            "CREATININE": {"omop_id": 3016723, "loinc": "2160-0", "name": "Creatinine in Serum or Plasma"},
        }

    def _init_namaste_registry(self) -> Dict[str, NAMASTEConcept]:
        """NAMASTE & WHO ICD-11 TM2 traditional concepts."""
        return {
            "UN-DIS-001": NAMASTEConcept(
                namaste_code="UN-DIS-001",
                system="UNANI",
                term_english="Ziabetus Shakari (Diabetes Mellitus)",
                term_vernacular="ذیابیطس شکری",
                clinical_definition="A metabolic disorder characterized by polydipsia, polyuria, and excessive thirst due to weakness of Quwwat-e-Ghadhiya and renal faculty.",
                icd11_tm2_code="TM2-UN-E11",
                mapped_snomed_concept="44054006"
            ),
            "UN-DIS-002": NAMASTEConcept(
                namaste_code="UN-DIS-002",
                system="UNANI",
                term_english="Zof-e-Qalb (Cardiac Debility / Heart Failure)",
                term_vernacular="ضعف قلب",
                clinical_definition="General or specific functional weakness of the myocardium manifesting as dyspnea, palpitation (Khafqan), and peripheral edema.",
                icd11_tm2_code="TM2-UN-I50",
                mapped_snomed_concept="84114007"
            ),
            "AY-DIS-001": NAMASTEConcept(
                namaste_code="AY-DIS-001",
                system="AYURVEDA",
                term_english="Madhumeha (Diabetes)",
                term_vernacular="मधुमेह",
                clinical_definition="Vataja Prameha subtype with sweet, astringent urine and progressive tissue dhatu kshaya.",
                icd11_tm2_code="TM2-AY-E11",
                mapped_snomed_concept="44054006"
            ),
            "AY-DIS-002": NAMASTEConcept(
                namaste_code="AY-DIS-002",
                system="AYURVEDA",
                term_english="Hridroga (Heart Disease)",
                term_vernacular="हृद्रोग",
                clinical_definition="Chest pain, heaviness, and cardiac functional compromise due to Dosha vitiation in the Hridaya marma.",
                icd11_tm2_code="TM2-AY-I50",
                mapped_snomed_concept="84114007"
            )
        }

    # -------------------------------------------------------------
    # Raw EHR -> HL7 FHIR Bundle
    # -------------------------------------------------------------

    def raw_to_fhir_bundle(self, raw_encounter: Dict[str, Any]) -> FHIRBundle:
        """
        Translates a raw hospital EHR encounter into a compliant HL7 FHIR Bundle.
        """
        patient_id = raw_encounter.get("patient_id", f"pat-{uuid.uuid4().hex[:6]}")
        entries: List[Dict[str, Any]] = []

        # 1. FHIR Patient
        fhir_patient = FHIRPatient(
            id=patient_id,
            gender=raw_encounter.get("gender", "unknown").lower(),
            birthDate=raw_encounter.get("birth_date", "1975-01-01"),
        )
        entries.append({"resource": fhir_patient.model_dump(), "fullUrl": f"urn:uuid:{fhir_patient.id}"})

        # 2. FHIR Condition
        if "diagnosis_code" in raw_encounter:
            code_str = raw_encounter["diagnosis_code"]
            vocab = self._vocabularies.get(code_str, {"snomed": "UNKNOWN", "name": raw_encounter.get("diagnosis_name", "Clinical condition")})
            condition = FHIRCondition(
                id=f"cond-{uuid.uuid4().hex[:6]}",
                code=FHIRCodeableConcept(
                    coding=[
                        FHIRCoding(system="http://hl7.org/fhir/sid/icd-10", code=code_str, display=vocab["name"]),
                        FHIRCoding(system="http://snomed.info/sct", code=vocab["snomed"], display=vocab["name"])
                    ],
                    text=vocab["name"]
                ),
                subject={"reference": f"Patient/{patient_id}"},
                onsetDateTime=raw_encounter.get("encounter_date", datetime.utcnow().strftime("%Y-%m-%d"))
            )
            entries.append({"resource": condition.model_dump()})

        # 3. FHIR Observation (Labs)
        for lab in raw_encounter.get("labs", []):
            lab_code = lab.get("code", "HBA1C").upper()
            vocab_lab = self._vocabularies.get(lab_code, {"loinc": "UNKNOWN", "name": lab_code})
            obs = FHIRObservation(
                id=f"obs-{uuid.uuid4().hex[:6]}",
                code=FHIRCodeableConcept(
                    coding=[FHIRCoding(system="http://loinc.org", code=vocab_lab["loinc"], display=vocab_lab["name"])],
                    text=vocab_lab["name"]
                ),
                subject={"reference": f"Patient/{patient_id}"},
                effectiveDateTime=raw_encounter.get("encounter_date", datetime.utcnow().strftime("%Y-%m-%d")),
                valueQuantity=FHIRQuantity(
                    value=float(lab.get("value", 0.0)),
                    unit=lab.get("unit", "units"),
                    code=lab.get("unit", "units")
                )
            )
            entries.append({"resource": obs.model_dump()})

        # 4. FHIR MedicationStatement
        for med in raw_encounter.get("medications", []):
            med_code = med.get("name", "DAPAGLIFLOZIN").upper()
            vocab_med = self._vocabularies.get(med_code, {"rxnorm": "UNKNOWN", "name": med_code})
            stmt = FHIRMedicationStatement(
                id=f"med-{uuid.uuid4().hex[:6]}",
                medicationCodeableConcept=FHIRCodeableConcept(
                    coding=[FHIRCoding(system="http://www.nlm.nih.gov/research/umls/rxnorm", code=vocab_med["rxnorm"], display=vocab_med["name"])],
                    text=vocab_med["name"]
                ),
                subject={"reference": f"Patient/{patient_id}"},
                effectiveDateTime=raw_encounter.get("encounter_date", datetime.utcnow().strftime("%Y-%m-%d")),
                dosage=[{"text": med.get("dosage", "Standard dose")}]
            )
            entries.append({"resource": stmt.model_dump()})

        return FHIRBundle(entry=entries, total=len(entries))

    # -------------------------------------------------------------
    # FHIR Bundle -> OHDSI OMOP CDM (v5.4)
    # -------------------------------------------------------------

    def fhir_to_omop_cdm(self, bundle: FHIRBundle) -> Dict[str, Any]:
        """
        Converts FHIR resources into standardized OMOP CDM v5.4 tables.
        """
        persons: List[OMOPPerson] = []
        conditions: List[OMOPConditionOccurrence] = []
        drugs: List[OMOPDrugExposure] = []
        measurements: List[OMOPMeasurement] = []

        person_int_id = 1001

        for item in bundle.entry:
            res = item.get("resource", {})
            rtype = res.get("resourceType")

            if rtype == "Patient":
                gender_str = res.get("gender", "unknown")
                gender_cid = 8507 if gender_str == "male" else (8532 if gender_str == "female" else 0)
                birth_year = int(res.get("birthDate", "1980-01-01").split("-")[0])
                persons.append(OMOPPerson(
                    person_id=person_int_id,
                    gender_concept_id=gender_cid,
                    year_of_birth=birth_year,
                    person_source_value=res.get("id"),
                    gender_source_value=gender_str
                ))

            elif rtype == "Condition":
                code_obj = res.get("code", {})
                source_code = ""
                concept_id = 0
                for c in code_obj.get("coding", []):
                    if c.get("code") in self._vocabularies:
                        concept_id = self._vocabularies[c["code"]]["omop_id"]
                        source_code = c["code"]
                        break
                conditions.append(OMOPConditionOccurrence(
                    condition_occurrence_id=int(uuid.uuid4().int % 100000000),
                    person_id=person_int_id,
                    condition_concept_id=concept_id,
                    condition_start_date=res.get("onsetDateTime", "2024-01-01"),
                    condition_source_value=source_code or code_obj.get("text", "Condition")
                ))

            elif rtype == "MedicationStatement":
                med_obj = res.get("medicationCodeableConcept", {})
                drug_concept_id = 0
                source_val = med_obj.get("text", "")
                for k, v in self._vocabularies.items():
                    if k in source_val.upper():
                        drug_concept_id = v["omop_id"]
                        break
                drugs.append(OMOPDrugExposure(
                    drug_exposure_id=int(uuid.uuid4().int % 100000000),
                    person_id=person_int_id,
                    drug_concept_id=drug_concept_id,
                    drug_exposure_start_date=res.get("effectiveDateTime", "2024-01-01"),
                    drug_source_value=source_val
                ))

            elif rtype == "Observation":
                obs_code = res.get("code", {})
                meas_concept_id = 0
                source_val = obs_code.get("text", "")
                for c in obs_code.get("coding", []):
                    code_val = c.get("code", "")
                    for k, v in self._vocabularies.items():
                        if code_val == v.get("loinc") or k in source_val.upper() or v.get("name", "").lower() in source_val.lower():
                            meas_concept_id = v["omop_id"]
                            break
                    if meas_concept_id != 0:
                        break
                if meas_concept_id == 0:
                    for k, v in self._vocabularies.items():
                        if k in source_val.upper() or v.get("name", "").lower() in source_val.lower():
                            meas_concept_id = v["omop_id"]
                            break
                val_num = None
                if "valueQuantity" in res:
                    val_num = res["valueQuantity"].get("value")
                measurements.append(OMOPMeasurement(
                    measurement_id=int(uuid.uuid4().int % 100000000),
                    person_id=person_int_id,
                    measurement_concept_id=meas_concept_id,
                    measurement_date=res.get("effectiveDateTime", "2024-01-01"),
                    value_as_number=val_num,
                    measurement_source_value=source_val
                ))

        return {
            "omop_version": "5.4",
            "person": [p.model_dump() for p in persons],
            "condition_occurrence": [c.model_dump() for c in conditions],
            "drug_exposure": [d.model_dump() for d in drugs],
            "measurement": [m.model_dump() for m in measurements],
        }

    # -------------------------------------------------------------
    # OMOP CDM -> CDISC SDTM Domains
    # -------------------------------------------------------------

    def omop_to_cdisc_sdtm(self, omop_data: Dict[str, Any], study_id: str = "ZMIE-RWE-001") -> Dict[str, Any]:
        """
        Translates OMOP CDM records into standard CDISC SDTM tabular domains (DM, LB, EX).
        """
        sdtm_dm: List[CDISCDemographics] = []
        sdtm_lb: List[CDISCLaboratory] = []
        sdtm_ex: List[CDISCExposure] = []

        # Demographics (DM)
        for p in omop_data.get("person", []):
            sex_char = "M" if p.get("gender_concept_id") == 8507 else ("F" if p.get("gender_concept_id") == 8532 else "U")
            current_year = datetime.utcnow().year
            age_calc = current_year - p.get("year_of_birth", 1980)
            sdtm_dm.append(CDISCDemographics(
                STUDYID=study_id,
                USUBJID=f"{study_id}-{p['person_id']}",
                SUBJID=str(p["person_id"]),
                SEX=sex_char,
                AGE=age_calc,
                ARMCD="RWE_OBS"
            ))

        # Laboratory (LB)
        lb_seq = 1
        for m in omop_data.get("measurement", []):
            sdtm_lb.append(CDISCLaboratory(
                STUDYID=study_id,
                USUBJID=f"{study_id}-{m['person_id']}",
                LBSEQ=lb_seq,
                LBTESTCD=m.get("measurement_source_value", "LAB"),
                LBTEST=m.get("measurement_source_value", "LAB"),
                LBORRES=str(m.get("value_as_number", "")),
                LBORRESU="mg/dL",
                LBSTRESN=m.get("value_as_number"),
                LBSTRESU="mg/dL",
                LBDTC=m.get("measurement_date", "2024-01-01")
            ))
            lb_seq += 1

        # Exposure (EX)
        ex_seq = 1
        for d in omop_data.get("drug_exposure", []):
            sdtm_ex.append(CDISCExposure(
                STUDYID=study_id,
                USUBJID=f"{study_id}-{d['person_id']}",
                EXSEQ=ex_seq,
                EXTRT=d.get("drug_source_value", "DRUG"),
                EXDOSE=10.0,
                EXDOSU="MG",
                EXDOSFRM="TABLET",
                EXSTDTC=d.get("drug_exposure_start_date", "2024-01-01")
            ))
            ex_seq += 1

        return {
            "study_id": study_id,
            "standard": "CDISC SDTM v1.7",
            "DM": [dm.model_dump() for dm in sdtm_dm],
            "LB": [lb.model_dump() for lb in sdtm_lb],
            "EX": [ex.model_dump() for ex in sdtm_ex]
        }

    # -------------------------------------------------------------
    # Traditional Medicine Clinical Registry Harmonizer
    # -------------------------------------------------------------

    def harmonize_traditional_record(self, raw_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Harmonizes traditional clinical registries (Unani Mizaj, Ayurvedic Prakriti, NAMASTE codes).
        """
        code = raw_record.get("namaste_code")
        namaste_match = self._namaste_registry.get(code)

        result: Dict[str, Any] = {
            "record_id": raw_record.get("record_id", f"trad-{uuid.uuid4().hex[:6]}"),
            "system": raw_record.get("system", "UNANI").upper(),
            "namaste_concept": namaste_match.model_dump() if namaste_match else None,
            "icd11_tm2_alignment": namaste_match.icd11_tm2_code if namaste_match else None,
            "snomed_partial_mapping": namaste_match.mapped_snomed_concept if namaste_match else None,
            "epistemic_warning": (
                "TRADITIONAL SYSTEM CLINICAL ALIGNMENT: Traditional diagnoses (e.g. Mizaj, Prakriti, Dhatukshaya) "
                "represent distinct constitutional and holistic etiologies. Mappings to ICD-11 TM2 or SNOMED are partial "
                "phenotypic cross-references and do not collapse the distinct traditional ontology."
            )
        }

        # Handle Mizaj if present
        if raw_record.get("mizaj") is not None:
            m = raw_record["mizaj"]
            mizaj_rec = MizajAssessmentRecord(
                assessment_id=f"mizaj-{uuid.uuid4().hex[:6]}",
                person_identifier=raw_record.get("patient_id", "P-01"),
                evaluation_date=raw_record.get("date", datetime.utcnow().strftime("%Y-%m-%d")),
                damawi_sanguine_score=float(m.get("damawi", 5.0)),
                balghami_phlegmatic_score=float(m.get("balghami", 5.0)),
                safrawi_choleric_score=float(m.get("safrawi", 5.0)),
                saudawi_melancholic_score=float(m.get("saudawi", 5.0)),
                dominant_mizaj=m.get("dominant", "DAMAWI"),
                su_e_mizaj_deviation=m.get("su_e_mizaj")
            )
            result["mizaj_assessment"] = mizaj_rec.model_dump()

        # Handle Prakriti if present
        if raw_record.get("prakriti") is not None:
            p = raw_record["prakriti"]
            prakriti_rec = PrakritiAssessmentRecord(
                assessment_id=f"prakriti-{uuid.uuid4().hex[:6]}",
                person_identifier=raw_record.get("patient_id", "P-01"),
                evaluation_date=raw_record.get("date", datetime.utcnow().strftime("%Y-%m-%d")),
                vata_score=float(p.get("vata", 4.0)),
                pitta_score=float(p.get("pitta", 5.0)),
                kapha_score=float(p.get("kapha", 4.0)),
                dominant_prakriti=p.get("dominant", "PITTA"),
                vikriti_imbalance=p.get("vikriti")
            )
            result["prakriti_assessment"] = prakriti_rec.model_dump()

        return result

    def get_namaste_concept(self, code: str) -> Optional[NAMASTEConcept]:
        return self._namaste_registry.get(code)
