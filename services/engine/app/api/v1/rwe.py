"""
ZMIE Research Data Interoperability & Real-World Evidence (RWE) API Router
Prompt 15 Master Implementation.

Provides endpoints for:
- RWD Sources Registry & Data Contracts (Sections 7, 8)
- 9-Dimension Data Quality Auditing & Fit-for-Purpose Gate (Sections 35-46)
- Target Trial Emulation (TTE) & Causal DAGs (Sections 66, 69, 70)
- Causality Firewall & Negative Control Designs (Sections 76, 144, 145)
- Federated Research & Clean Room Small-Cell Suppression (Sections 131-135)
- HL7 FHIR (R4/R5), OHDSI OMOP CDM (v5.4/v5.5), CDISC SDTM (v1.7) Harmonization
- Traditional Medicine Clinical Registry Harmonization (NAMASTE, ICD-11 TM2, Mizaj, Prakriti)
- RWE Cohort Definition & Observational Bias Auditing
- Evidence Graph Bridge & RCT-RWE Triangulation Analysis
"""

from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from app.models.rwe_interop import (
    RWDSourceRecord,
    RWDSourceType,
    RWDDataContract,
    DataQualityReport,
    FitnessForPurposeAssessment,
    TargetTrialProtocol,
    CausalDAG,
    FederatedQueryRequest,
    FederatedQueryResult,
    FHIRBundle,
    RWECohortDefinition,
    RWEEvidenceSummary,
    NAMASTEConcept,
)
from app.rwe.harmonizer import ClinicalDataHarmonizer
from app.rwe.cohort_engine import RWECohortEngine
from app.rwe.evidence_bridge import RWEEvidenceGraphBridge
from app.rwe.quality_engine import DataQualityEngine
from app.rwe.causal_engine import TargetTrialEmulationEngine
from app.rwe.federated_engine import FederatedResearchCleanRoom

router = APIRouter(prefix="/rwe", tags=["Research Data Interoperability & Real-World Evidence (Prompt 15 Master)"])

# Singletons
harmonizer = ClinicalDataHarmonizer()
cohort_engine = RWECohortEngine()
evidence_bridge = RWEEvidenceGraphBridge()
quality_engine = DataQualityEngine()
causal_engine = TargetTrialEmulationEngine()
federated_clean_room = FederatedResearchCleanRoom()

# In-memory source registry
rwd_sources_registry: Dict[str, RWDSourceRecord] = {
    "SRC-OXFORD-EHR": RWDSourceRecord(
        source_id="SRC-OXFORD-EHR",
        source_name="Oxford University Hospitals NHS Trust Clinical Registry",
        organization="Oxford University Hospitals NHS Foundation Trust",
        source_type=RWDSourceType.EHR,
        country="United Kingdom",
        jurisdiction="UK_GDPR",
        data_owner="Oxford NHS Trust",
        data_controller="Oxford NHS Trust",
        data_processor="ZMIE UK Node",
        data_steward="Dr. Alistair Finch",
        dataset_type="LONGITUDINAL_EHR",
        clinical_domain="Cardiology & Metabolic Medicine",
        medical_system="MODERN",
        population="Unselected routine inpatient and outpatient cardiology",
        data_period_start="2018-01-01",
        data_period_end="2024-12-31",
        update_frequency="MONTHLY",
        volume="1.2M patients",
        format="FHIR R5 / OMOP CDM v5.4",
        interface="REST_FHIR_BULK",
        api="https://fhir.ouh.nhs.uk/r5",
        license="NHS_RESEARCH_DATA_SHARING_AGREEMENT_2024",
        consent_model="NATIONAL_DATA_OPT_OUT_GOVERNED",
        privacy_model="PSEUDONYMIZED_TOKENIZED",
        access_model="RBAC_TRE_APPROVED",
        tenant="OUH_RESEARCH_NODE",
        quality_status="VERIFIED_GOLD",
        fitness_for_purpose="FIT",
        version="2.4.0",
        status="ACTIVE"
    ),
    "SRC-NIUM-REG": RWDSourceRecord(
        source_id="SRC-NIUM-REG",
        source_name="National Institute of Unani Medicine Clinical Registry",
        organization="National Institute of Unani Medicine (NIUM)",
        source_type=RWDSourceType.TRADITIONAL_COUNCIL_REGISTRY,
        country="India",
        jurisdiction="INDIA_DISHA_DPDP",
        data_owner="Ministry of AYUSH / NIUM",
        data_controller="Director NIUM",
        data_processor="ZMIE India Sovereign Node",
        data_steward="Prof. Hakim Aslam Siddiqui",
        dataset_type="TRADITIONAL_CLINICAL_REGISTRY",
        clinical_domain="Moalajat (Medicine) & Cardioprotective Formulations",
        medical_system="UNANI",
        population="Patients receiving Khamira Abresham and standard care",
        data_period_start="2020-01-01",
        data_period_end="2024-12-31",
        update_frequency="QUARTERLY",
        volume="42,000 patients",
        format="NAMASTE / ICD-11 TM2 / OMOP Extension",
        interface="REST_SECURE_API",
        api="https://registry.nium.in/v1",
        license="AYUSH_OPEN_RESEARCH_LICENSE",
        consent_model="CLINICAL_TRIAL_REGISTRY_CONSENT",
        privacy_model="DE_IDENTIFIED_TOKENIZED",
        access_model="FEDERATED_CLEAN_ROOM",
        tenant="NIUM_SOVEREIGN_NODE",
        quality_status="VERIFIED_TRADITIONAL_GOLD",
        fitness_for_purpose="FIT",
        version="1.2.0",
        status="ACTIVE"
    )
}


# Request Schemas
class RawEncounterRequest(BaseModel):
    patient_id: str = Field(..., description="Anonymized patient identifier")
    gender: str = Field("male", description="Patient gender")
    birth_date: str = Field("1968-05-12", description="YYYY-MM-DD")
    encounter_date: str = Field("2024-02-15", description="YYYY-MM-DD")
    diagnosis_code: str = Field("I50.9", description="ICD-10 or SNOMED code")
    diagnosis_name: Optional[str] = Field("Heart failure", description="Clinical label")
    labs: List[Dict[str, Any]] = Field(default_factory=lambda: [
        {"code": "HBA1C", "value": 7.2, "unit": "%"},
        {"code": "BNP", "value": 450.0, "unit": "pg/mL"}
    ])
    medications: List[Dict[str, Any]] = Field(default_factory=lambda: [
        {"name": "DAPAGLIFLOZIN", "dosage": "10mg once daily"}
    ])


class TraditionalRecordRequest(BaseModel):
    record_id: Optional[str] = Field(None, description="Record ID")
    patient_id: str = Field("PAT-UNANI-001", description="Patient identifier")
    system: str = Field("UNANI", description="UNANI, AYURVEDA, SIDDHA")
    namaste_code: str = Field("UN-DIS-002", description="NAMASTE / ICD-11 TM2 morbidity code")
    mizaj: Optional[Dict[str, Any]] = Field(default_factory=lambda: {
        "damawi": 4.5,
        "balghami": 7.0,
        "safrawi": 3.0,
        "saudawi": 4.0,
        "dominant": "BALGHAMI",
        "su_e_mizaj": "Su-e-Mizaj Barid Ratab (Cold & Wet Dyscrasia)"
    })
    prakriti: Optional[Dict[str, Any]] = None


class QualityAuditRequest(BaseModel):
    dataset_id: str = Field(..., description="Target dataset identifier")
    source_id: str = Field("SRC-OXFORD-EHR", description="Source facility identifier")
    records: List[Dict[str, Any]] = Field(..., description="Batch of clinical encounter records to audit")


class FitnessCheckRequest(BaseModel):
    research_question: str = Field(..., description="Target clinical or pharmacological research question")
    dataset_id: str = Field(..., description="Target dataset identifier")
    target_population: str = Field(..., description="Target patient population description")
    required_variables: List[str] = Field(..., description="List of required variables for the study")


class CausalityAuditRequest(BaseModel):
    claim_text: str = Field(..., description="Generated statement or assertion to audit")
    study_type: str = Field("OBSERVATIONAL_COHORT", description="Observational, RCT, In-silico")
    has_target_trial_emulation: bool = Field(False, description="Whether an active TTE protocol was followed")


class AnalyzeCohortRequest(BaseModel):
    cohort_id: str = Field(..., description="ID of registered cohort")
    target_n: int = Field(14200, description="Size of target cohort")
    comparator_n: int = Field(28400, description="Size of comparator cohort")
    unadjusted_hazard_ratio: float = Field(0.68, description="Crude HR")
    adjusted_hazard_ratio: float = Field(0.74, description="Propensity-adjusted HR")
    ci_lower: float = Field(0.67, description="95% CI lower bound")
    ci_upper: float = Field(0.82, description="95% CI upper bound")
    p_value: float = Field(0.0001, description="Statistical significance")
    outcome_name: str = Field("Cardiovascular Death or HF Hospitalization", description="Endpoint")
    data_source: str = Field("EHR_FEDERATED", description="Data source type")
    triangulation_status: str = Field("CONCORDANT_WITH_RCT", description="Concordance with RCT")


class TriangulationRequest(BaseModel):
    rwe_id: str = Field(..., description="ID of analyzed RWE study")
    landmark_rct_title: str = Field("DAPA-HF Landmark Phase 3 Trial", description="RCT title")
    landmark_rct_hr: float = Field(0.74, description="RCT Hazard Ratio")
    landmark_rct_ci: List[float] = Field(default_factory=lambda: [0.65, 0.85], description="RCT 95% CI")


# -------------------------------------------------------------
# RWD Sources Registry & Governance (Section 7, 8)
# -------------------------------------------------------------

@router.get("/sources", response_model=List[RWDSourceRecord])
async def list_rwd_sources():
    """Lists all registered authorized Real-World Data (RWD) sources."""
    return list(rwd_sources_registry.values())


@router.get("/sources/{source_id}", response_model=RWDSourceRecord)
async def get_rwd_source(source_id: str):
    """Retrieves metadata, governance, and licensing contract for an RWD source."""
    if source_id not in rwd_sources_registry:
        raise HTTPException(status_code=404, detail=f"RWD source '{source_id}' not found.")
    return rwd_sources_registry[source_id]


# -------------------------------------------------------------
# 9-Dimension Data Quality & Fit-for-Purpose Engine (Sections 35-46)
# -------------------------------------------------------------

@router.post("/quality/audit", response_model=DataQualityReport)
async def audit_data_quality(req: QualityAuditRequest):
    """
    Executes a comprehensive 9-dimension data quality audit and plausibility verification
    (detects impossible ages, date reversals, implausible lab measurements).
    """
    return quality_engine.audit_dataset_quality(
        dataset_id=req.dataset_id,
        records=req.records,
        source_id=req.source_id
    )


@router.post("/quality/fitness-check", response_model=FitnessForPurposeAssessment)
async def check_fitness_for_purpose(req: FitnessCheckRequest):
    """
    Fit-for-Purpose Gatekeeper: Evaluates dataset fitness against the specific research question.
    """
    return quality_engine.evaluate_fitness_for_purpose(
        research_question=req.research_question,
        dataset_id=req.dataset_id,
        target_population=req.target_population,
        required_variables=req.required_variables
    )


# -------------------------------------------------------------
# Target Trial Emulation (TTE) & Causality Firewall (Sections 66, 69, 144)
# -------------------------------------------------------------

@router.post("/tte/protocols", response_model=TargetTrialProtocol)
async def register_target_trial_protocol(protocol: TargetTrialProtocol):
    """Registers an emulated target trial protocol with explicit Time Zero and eligibility."""
    return causal_engine.register_target_trial(protocol)


@router.get("/tte/protocols/{protocol_id}", response_model=TargetTrialProtocol)
async def get_target_trial_protocol(protocol_id: str):
    """Retrieves target trial emulation protocol."""
    if protocol_id not in causal_engine._protocols:
        raise HTTPException(status_code=404, detail=f"TTE Protocol '{protocol_id}' not found.")
    return causal_engine._protocols[protocol_id]


@router.post("/tte/dag", response_model=CausalDAG)
async def register_causal_dag(dag: CausalDAG):
    """Registers a Causal Directed Acyclic Graph (DAG) with explicit confounders and colliders."""
    return causal_engine.register_causal_dag(dag)


@router.post("/tte/audit-claim")
async def audit_causality_claim(req: CausalityAuditRequest):
    """
    Causality Firewall: Rejects claims asserting definitive causality without an active TTE design.
    """
    return causal_engine.audit_causality_claim(
        claim_text=req.claim_text,
        study_type=req.study_type,
        has_tte=req.has_target_trial_emulation
    )


@router.get("/tte/negative-control")
async def get_negative_control_design(exposure: str = Query(...), outcome: str = Query(...)):
    """Synthesizes a negative control exposure and outcome design to calibrate unmeasured confounding."""
    return causal_engine.generate_negative_control_design(target_exposure=exposure, target_outcome=outcome)


# -------------------------------------------------------------
# Federated Research & Privacy Clean Room (Sections 131-135)
# -------------------------------------------------------------

@router.post("/federated/query", response_model=FederatedQueryResult)
async def execute_federated_clean_room_query(req: FederatedQueryRequest):
    """
    Executes a federated multi-institution cohort query with automatic small-cell suppression (< 5).
    """
    return federated_clean_room.execute_federated_query(req)


@router.get("/federated/tokenize")
async def tokenize_patient_identity(patient_id: str = Query(...), facility: str = Query("HOSP_MAIN")):
    """Generates irreversible HMAC-SHA256 research_subject_id."""
    token = federated_clean_room.tokenize_patient_id(patient_id, facility)
    return {
        "raw_patient_id": "***REDACTED***",
        "facility": facility,
        "research_subject_id": token,
        "method": "HMAC_SHA256_SALTED"
    }


# -------------------------------------------------------------
# Multi-Standard Harmonization Endpoints (Sections 12, 16, 18, 56)
# -------------------------------------------------------------

@router.post("/harmonize/raw-to-fhir", response_model=FHIRBundle)
async def raw_to_fhir(req: RawEncounterRequest):
    """Translates raw hospital EHR encounter into a compliant HL7 FHIR Bundle."""
    return harmonizer.raw_to_fhir_bundle(req.model_dump())


@router.post("/harmonize/fhir-to-omop")
async def fhir_to_omop(bundle: FHIRBundle):
    """Maps HL7 FHIR Bundle resources to OHDSI OMOP Common Data Model (v5.4) tables."""
    return harmonizer.fhir_to_omop_cdm(bundle)


@router.post("/harmonize/omop-to-cdisc")
async def omop_to_cdisc(omop_data: Dict[str, Any] = Body(...), study_id: str = Query("ZMIE-RWE-001")):
    """Translates OMOP CDM tables into standard CDISC SDTM domains (DM, LB, EX)."""
    return harmonizer.omop_to_cdisc_sdtm(omop_data, study_id=study_id)


@router.post("/harmonize/traditional")
async def harmonize_traditional(req: TraditionalRecordRequest):
    """Harmonizes traditional clinical registries (Unani Mizaj, Ayurvedic Prakriti, NAMASTE codes)."""
    return harmonizer.harmonize_traditional_record(req.model_dump())


@router.get("/vocabularies/namaste/{code}")
async def get_namaste_concept(code: str):
    """Retrieves NAMASTE / WHO ICD-11 TM2 traditional morbidity concept."""
    concept = harmonizer.get_namaste_concept(code)
    if not concept:
        raise HTTPException(status_code=404, detail=f"NAMASTE concept '{code}' not found.")
    return concept.model_dump()


# -------------------------------------------------------------
# Cohort Definition & Observational Bias Auditing (Sections 48, 67, 93)
# -------------------------------------------------------------

@router.post("/cohorts/define", response_model=RWECohortDefinition)
async def define_cohort(definition: RWECohortDefinition):
    """Registers a new observational cohort study definition."""
    return cohort_engine.define_cohort(definition)


@router.get("/cohorts/{cohort_id}", response_model=RWECohortDefinition)
async def get_cohort(cohort_id: str):
    """Retrieves cohort study definition."""
    coh = cohort_engine.get_cohort(cohort_id)
    if not coh:
        raise HTTPException(status_code=404, detail=f"Cohort '{cohort_id}' not found.")
    return coh


@router.post("/cohorts/analyze", response_model=RWEEvidenceSummary)
async def analyze_cohort(req: AnalyzeCohortRequest):
    """Executes observational cohort analysis, audits for systematic biases, and generates RWE summary."""
    return cohort_engine.analyze_cohort_evidence(
        cohort_id=req.cohort_id,
        target_n=req.target_n,
        comparator_n=req.comparator_n,
        unadjusted_hazard_ratio=req.unadjusted_hazard_ratio,
        adjusted_hazard_ratio=req.adjusted_hazard_ratio,
        ci_lower=req.ci_lower,
        ci_upper=req.ci_upper,
        p_val=req.p_value,
        outcome_name=req.outcome_name,
        data_source=req.data_source,
        triangulation_status=req.triangulation_status
    )


# -------------------------------------------------------------
# Evidence Graph Bridge & Triangulation (Sections 96, 102, 189)
# -------------------------------------------------------------

@router.post("/triangulate")
async def triangulate_rwe_rct(req: TriangulationRequest):
    """Performs scientific triangulation: Compares RWE effect size against an RCT benchmark."""
    rwe_summary = cohort_engine._evidence_cache.get(req.rwe_id)
    if not rwe_summary:
        raise HTTPException(status_code=404, detail=f"RWE summary '{req.rwe_id}' not found in cache. Analyze cohort first.")
    return evidence_bridge.triangulate_with_rct(
        rwe_summary=rwe_summary,
        landmark_rct_title=req.landmark_rct_title,
        landmark_rct_hr=req.landmark_rct_hr,
        landmark_rct_ci=req.landmark_rct_ci
    )
