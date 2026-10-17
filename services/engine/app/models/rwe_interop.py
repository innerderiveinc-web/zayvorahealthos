"""
ZMIE Research Data Interoperability & Real-World Evidence (RWE) Models
Prompt 15 Master Implementation.

Defines:
1. RWD Source Registry & Data Contracts (Section 7, 8)
2. Four-Tier Source-Preserving Architecture (RAW, NORMALIZED, STANDARDIZED, ANALYTIC) (Section 9)
3. HL7 FHIR (R4/R5) Resources (Section 12, 13)
4. OHDSI OMOP CDM (v5.4/v5.5) Clinical Data Tables & Concept Mappings (Section 16, 17)
5. CDISC SDTM/ADaM Study Data Tabulation Domains & Define-XML (Section 18, 21)
6. Data Quality & Fitness-for-Purpose Models (Section 35, 45, 46)
7. Target Trial Emulation (TTE) & Causal DAG Models (Section 66, 69, 70)
8. Multi-System Traditional Medicine Clinical Registry Models (NAMASTE, ICD-11 TM2, Mizaj, Prakriti) (Section 56-59)
9. Federated Research & Privacy Clean Room Models (Section 131-135)
10. RWE Cohort Definitions, Bias Auditing & Evidence Graph Bridge Entities (Section 48, 67, 93)
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, date
import uuid


# -------------------------------------------------------------
# 1. RWD Sources Registry & Data Contracts (Sections 7, 8)
# -------------------------------------------------------------

class RWDSourceType(str, Enum):
    EHR = "EHR"
    EMR = "EMR"
    HOSPITAL_INFORMATION_SYSTEM = "HOSPITAL_INFORMATION_SYSTEM"
    CLINICAL_REGISTRY = "CLINICAL_REGISTRY"
    LABORATORY_LIS = "LABORATORY_LIS"
    PHARMACY_DISPENSING = "PHARMACY_DISPENSING"
    INSURANCE_CLAIMS = "INSURANCE_CLAIMS"
    CLINICAL_TRIAL_DATASET = "CLINICAL_TRIAL_DATASET"
    WEARABLE_DEVICE = "WEARABLE_DEVICE"
    PATIENT_REPORTED = "PATIENT_REPORTED"
    PUBLIC_HEALTH = "PUBLIC_HEALTH"
    TRADITIONAL_COUNCIL_REGISTRY = "TRADITIONAL_COUNCIL_REGISTRY"


class DataClassification(str, Enum):
    PUBLIC = "PUBLIC"
    OPEN_RESEARCH = "OPEN_RESEARCH"
    RESTRICTED_RESEARCH = "RESTRICTED_RESEARCH"
    CONFIDENTIAL = "CONFIDENTIAL"
    SENSITIVE = "SENSITIVE"
    PATIENT_DATA = "PATIENT_DATA"
    HIGHLY_RESTRICTED = "HIGHLY_RESTRICTED"


class RWDSourceRecord(BaseModel):
    """Registry entry for an authorized Real-World Data (RWD) source (Section 7)."""
    source_id: str
    source_name: str
    organization: str
    source_type: RWDSourceType
    country: str
    jurisdiction: str
    data_owner: str
    data_controller: str
    data_processor: str
    data_steward: str
    dataset_type: str
    clinical_domain: str
    medical_system: str = "MODERN"  # MODERN, UNANI, AYURVEDA, SIDDHA, TCM, INTEGRATIVE
    population: str
    data_period_start: str
    data_period_end: str
    update_frequency: str = "MONTHLY"
    volume: str
    format: str = "FHIR/OMOP"
    interface: str = "REST_API"
    api: str
    license: str
    consent_model: str = "BROAD_RESEARCH_CONSENT"
    privacy_model: str = "PSEUDONYMIZED_TOKENIZED"
    access_model: str = "RBAC_ABAC_FEDERATED"
    tenant: str = "SHARED_GOVERNED"
    quality_status: str = "VERIFIED"
    fitness_for_purpose: str = "FIT"
    last_ingestion: datetime = Field(default_factory=datetime.utcnow)
    last_quality_check: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"
    status: str = "ACTIVE"


class RWDDataContract(BaseModel):
    """Formal data contract for an incoming RWD dataset (Section 8)."""
    contract_id: str
    source_id: str
    schema_definition: Dict[str, Any]
    field_definitions: List[Dict[str, Any]]
    units: List[str]
    terminologies: List[str]  # SNOMED, LOINC, RxNorm, ICD10, NAMASTE
    expected_frequency: str
    allowed_values: Dict[str, List[Any]] = Field(default_factory=dict)
    missingness_expectations: Dict[str, float] = Field(default_factory=dict)
    temporal_semantics: str = "UTC_TIMESTAMP"
    provenance: str
    license: str
    privacy_classification: DataClassification = DataClassification.RESTRICTED_RESEARCH
    retention_policy: str = "7_YEARS_AUDIT"
    update_behavior: str = "APPEND_VERSIONED"


# -------------------------------------------------------------
# 2. Four-Tier Source-Preserving Architecture (Section 9)
# -------------------------------------------------------------

class SourceDataTier(str, Enum):
    RAW = "RAW"
    NORMALIZED = "NORMALIZED"
    STANDARDIZED = "STANDARDIZED"
    ANALYTIC = "ANALYTIC"


class SourceDataLayerRecord(BaseModel):
    """Preserves raw, normalized, standardized and analytic representations (Section 9)."""
    layer_id: str = Field(default_factory=lambda: f"lay-{uuid.uuid4().hex[:8]}")
    dataset_id: str
    tier: SourceDataTier
    payload: Dict[str, Any]
    storage_uri: str
    version: int = 1
    provenance_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# -------------------------------------------------------------
# 3. Data Quality & Fitness-for-Purpose (Sections 35-46)
# -------------------------------------------------------------

class FitForPurposeState(str, Enum):
    FIT = "FIT"
    PARTIALLY_FIT = "PARTIALLY_FIT"
    NOT_FIT = "NOT_FIT"
    UNKNOWN = "UNKNOWN"


class DataQualityDimensionScores(BaseModel):
    completeness: float = Field(ge=0.0, le=100.0)
    consistency: float = Field(ge=0.0, le=100.0)
    validity: float = Field(ge=0.0, le=100.0)
    uniqueness: float = Field(ge=0.0, le=100.0)
    plausibility: float = Field(ge=0.0, le=100.0)
    conformance: float = Field(ge=0.0, le=100.0)
    temporal_integrity: float = Field(ge=0.0, le=100.0)
    provenance: float = Field(ge=0.0, le=100.0)
    representativeness: float = Field(ge=0.0, le=100.0)


class DataQualityReport(BaseModel):
    """Detailed quality report covering all 9 dimensions and plausibility checks (Section 36)."""
    report_id: str = Field(default_factory=lambda: f"dqr-{uuid.uuid4().hex[:8]}")
    dataset_id: str
    source_id: str
    total_records: int
    dimension_scores: DataQualityDimensionScores
    plausibility_violations: List[Dict[str, Any]] = Field(default_factory=list)  # impossible ages, date reversals, unit errors
    missingness_summary: Dict[str, float] = Field(default_factory=dict)
    outlier_count: int = 0
    passed_rules_count: int = 0
    failed_rules_count: int = 0
    known_limitations: List[str] = Field(default_factory=list)
    overall_status: str = "QUALITY_PASSED"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FitnessForPurposeAssessment(BaseModel):
    """Fit-for-Purpose Gate evaluating dataset against specific research question (Section 45, 46)."""
    assessment_id: str = Field(default_factory=lambda: f"ffp-{uuid.uuid4().hex[:8]}")
    research_question: str
    dataset_id: str
    target_population: str
    required_variables: List[str]
    status: FitForPurposeState
    minimum_quality_threshold: float = 85.0
    measured_quality: float
    bias_risks_identified: List[str] = Field(default_factory=list)
    verdict_rationale: str
    assessed_at: datetime = Field(default_factory=datetime.utcnow)


# -------------------------------------------------------------
# 4. HL7 FHIR (R4/R5) Data Models (Sections 12-14)
# -------------------------------------------------------------

class FHIRIdentifier(BaseModel):
    system: str
    value: str
    use: str = "official"


class FHIRCoding(BaseModel):
    system: str
    code: str
    display: str


class FHIRCodeableConcept(BaseModel):
    coding: List[FHIRCoding] = Field(default_factory=list)
    text: Optional[str] = None


class FHIRQuantity(BaseModel):
    value: float
    unit: str
    system: str = "http://unitsofmeasure.org"
    code: str


class FHIRPatient(BaseModel):
    resourceType: str = "Patient"
    id: str
    identifier: List[FHIRIdentifier] = Field(default_factory=list)
    active: bool = True
    gender: str
    birthDate: Optional[str] = None
    deceasedBoolean: bool = False
    meta: Dict[str, Any] = Field(default_factory=lambda: {"profile": ["http://hl7.org/fhir/StructureDefinition/Patient"]})


class FHIRCondition(BaseModel):
    resourceType: str = "Condition"
    id: str
    clinicalStatus: str = "active"
    verificationStatus: str = "confirmed"
    category: List[FHIRCodeableConcept] = Field(default_factory=list)
    code: FHIRCodeableConcept
    subject: Dict[str, str]
    onsetDateTime: Optional[str] = None


class FHIRObservation(BaseModel):
    resourceType: str = "Observation"
    id: str
    status: str = "final"
    category: List[FHIRCodeableConcept] = Field(default_factory=list)
    code: FHIRCodeableConcept
    subject: Dict[str, str]
    effectiveDateTime: Optional[str] = None
    valueQuantity: Optional[FHIRQuantity] = None
    valueString: Optional[str] = None
    referenceRange: List[Dict[str, Any]] = Field(default_factory=list)


class FHIRMedicationStatement(BaseModel):
    resourceType: str = "MedicationStatement"
    id: str
    status: str = "active"
    medicationCodeableConcept: FHIRCodeableConcept
    subject: Dict[str, str]
    effectiveDateTime: Optional[str] = None
    dosage: List[Dict[str, Any]] = Field(default_factory=list)


class FHIRResearchStudy(BaseModel):
    resourceType: str = "ResearchStudy"
    id: str
    title: str
    status: str = "active"
    condition: List[FHIRCodeableConcept] = Field(default_factory=list)
    principalInvestigator: Optional[Dict[str, str]] = None
    sponsor: Optional[Dict[str, str]] = None


class FHIRBundle(BaseModel):
    resourceType: str = "Bundle"
    id: str = Field(default_factory=lambda: f"bundle-{uuid.uuid4().hex[:8]}")
    type: str = "collection"
    entry: List[Dict[str, Any]] = Field(default_factory=list)
    total: int = 0


# -------------------------------------------------------------
# 5. OHDSI OMOP Common Data Model (CDM v5.4/v5.5) (Sections 16, 17)
# -------------------------------------------------------------

class OMOPConcept(BaseModel):
    concept_id: int
    concept_name: str
    domain_id: str
    vocabulary_id: str
    concept_class_id: str
    standard_concept: Optional[str] = "S"
    concept_code: str


class OMOPPerson(BaseModel):
    person_id: int
    gender_concept_id: int
    year_of_birth: int
    month_of_birth: Optional[int] = None
    day_of_birth: Optional[int] = None
    race_concept_id: int = 0
    ethnicity_concept_id: int = 0
    person_source_value: Optional[str] = None
    gender_source_value: Optional[str] = None


class OMOPConditionOccurrence(BaseModel):
    condition_occurrence_id: int
    person_id: int
    condition_concept_id: int
    condition_start_date: str
    condition_end_date: Optional[str] = None
    condition_type_concept_id: int = 32817
    stop_reason: Optional[str] = None
    condition_source_value: Optional[str] = None
    condition_source_concept_id: Optional[int] = None


class OMOPDrugExposure(BaseModel):
    drug_exposure_id: int
    person_id: int
    drug_concept_id: int
    drug_exposure_start_date: str
    drug_exposure_end_date: Optional[str] = None
    drug_type_concept_id: int = 38000177
    quantity: Optional[float] = None
    days_supply: Optional[int] = None
    dose_unit_source_value: Optional[str] = None
    drug_source_value: Optional[str] = None


class OMOPMeasurement(BaseModel):
    measurement_id: int
    person_id: int
    measurement_concept_id: int
    measurement_date: str
    measurement_datetime: Optional[str] = None
    measurement_type_concept_id: int = 44818702
    operator_concept_id: Optional[int] = None
    value_as_number: Optional[float] = None
    value_as_concept_id: Optional[int] = None
    unit_concept_id: Optional[int] = None
    range_low: Optional[float] = None
    range_high: Optional[float] = None
    measurement_source_value: Optional[str] = None


# -------------------------------------------------------------
# 6. CDISC SDTM/ADaM Study Data Tabulation Models (Sections 18-21)
# -------------------------------------------------------------

class CDISCDemographics(BaseModel):
    STUDYID: str
    DOMAIN: str = "DM"
    USUBJID: str
    SUBJID: str
    RFSTDTC: Optional[str] = None
    AGE: Optional[int] = None
    AGEU: str = "YEARS"
    SEX: str
    ARMCD: Optional[str] = None
    ARM: Optional[str] = None


class CDISCAdverseEvent(BaseModel):
    STUDYID: str
    DOMAIN: str = "AE"
    USUBJID: str
    AESEQ: int
    AETERM: str
    AEDECOD: str
    AESEV: str
    AESER: str
    AEREL: str
    AESTDTC: str


class CDISCLaboratory(BaseModel):
    STUDYID: str
    DOMAIN: str = "LB"
    USUBJID: str
    LBSEQ: int
    LBTESTCD: str
    LBTEST: str
    LBORRES: str
    LBORRESU: str
    LBSTRESN: Optional[float] = None
    LBSTRESU: Optional[str] = None
    LBDTC: str


class CDISCExposure(BaseModel):
    STUDYID: str
    DOMAIN: str = "EX"
    USUBJID: str
    EXSEQ: int
    EXTRT: str
    EXDOSE: float
    EXDOSU: str
    EXDOSFRM: str
    EXSTDTC: str


# -------------------------------------------------------------
# 7. Target Trial Emulation (TTE) & Causal DAGs (Sections 66, 69, 70)
# -------------------------------------------------------------

class TargetTrialProtocol(BaseModel):
    """Explicit research-design specification for Target Trial Emulation (Section 66)."""
    protocol_id: str = Field(default_factory=lambda: f"tte-{uuid.uuid4().hex[:8]}")
    study_title: str
    eligibility_criteria: List[str]
    treatment_strategies: Dict[str, str]  # {"arm_a": "SGLT2i initiated within 30 days", "arm_b": "Active comparator standard care"}
    assignment_procedure: str = "Propensity score matching at Time Zero"
    time_zero_definition: str = "Date of first eligible prescription/dispensing meeting inclusion criteria"
    follow_up_period_days: int = 730
    outcome_definitions: List[str]
    causal_contrast: str = "Per-protocol and Intention-to-treat observational analogs"
    analysis_plan: str = "Weighted Cox proportional hazards model with stabilized IPTW"
    censoring_rules: List[str] = Field(default_factory=list)
    version: str = "1.0"


class CausalDAG(BaseModel):
    """Directed Acyclic Graph (DAG) for explicit causal assumptions (Sections 69, 70)."""
    dag_id: str = Field(default_factory=lambda: f"dag-{uuid.uuid4().hex[:8]}")
    exposure_nodes: List[str]
    mediator_nodes: List[str] = Field(default_factory=list)
    outcome_nodes: List[str]
    measured_confounders: List[str] = Field(default_factory=list)
    unmeasured_confounder_risks: List[str] = Field(default_factory=list)
    colliders: List[str] = Field(default_factory=list)
    effect_modifiers: List[str] = Field(default_factory=list)
    edges: List[Dict[str, str]] = Field(default_factory=list)  # [{"from": "A", "to": "Y"}]
    testable_implications: List[str] = Field(default_factory=list)


# -------------------------------------------------------------
# 8. Federated Research & Privacy Clean Room (Sections 131-135)
# -------------------------------------------------------------

class FederatedQueryRequest(BaseModel):
    """Privacy-preserving federated query across participating institutions (Sections 131-133)."""
    query_id: str = Field(default_factory=lambda: f"fed-q-{uuid.uuid4().hex[:8]}")
    participating_nodes: List[str]  # e.g., ["HOSP_OXFORD", "HOSP_BRIGHAM", "NIUM_BLR"]
    cohort_criteria: Dict[str, Any]
    privacy_cell_threshold: int = 5  # Small-cell suppression threshold
    differential_privacy_epsilon: Optional[float] = None


class FederatedQueryResult(BaseModel):
    """Aggregate result from multi-site clean rooms with small-cell disclosure protection."""
    query_id: str
    total_eligible_patients: int
    participating_nodes_count: int
    node_contributions: Dict[str, int]
    small_cells_suppressed_count: int
    privacy_guarantee: str = "K_ANONYMITY_SMALL_CELL_SUPPRESSED"
    execution_timestamp: datetime = Field(default_factory=datetime.utcnow)


# -------------------------------------------------------------
# 9. Multi-System Traditional Medicine Models (Sections 56-59)
# -------------------------------------------------------------

class NAMASTEConcept(BaseModel):
    namaste_code: str
    system: str  # UNANI, AYURVEDA, SIDDHA
    term_english: str
    term_vernacular: str
    clinical_definition: str
    icd11_tm2_code: Optional[str] = None
    mapped_snomed_concept: Optional[str] = None


class MizajAssessmentRecord(BaseModel):
    assessment_id: str
    person_identifier: str
    evaluation_date: str
    damawi_sanguine_score: float
    balghami_phlegmatic_score: float
    safrawi_choleric_score: float
    saudawi_melancholic_score: float
    dominant_mizaj: str
    su_e_mizaj_deviation: Optional[str] = None
    clinical_notes: Optional[str] = None


class PrakritiAssessmentRecord(BaseModel):
    assessment_id: str
    person_identifier: str
    evaluation_date: str
    vata_score: float
    pitta_score: float
    kapha_score: float
    dominant_prakriti: str
    vikriti_imbalance: Optional[str] = None
    clinical_notes: Optional[str] = None


class TraditionalCompoundExposure(BaseModel):
    exposure_id: str
    person_identifier: str
    medical_system: str
    classical_formulation_name: str
    pharmacopeia_reference: str
    batch_number: Optional[str] = None
    anupana_adjuvant: Optional[str] = None
    daily_dose_grams: float
    duration_days: int
    start_date: str


# -------------------------------------------------------------
# 10. RWE Cohort & Bias Auditing & Evidence Summary (Sections 48, 67, 93)
# -------------------------------------------------------------

class BiasRiskLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL_UNADJUSTED = "CRITICAL_UNADJUSTED"


class ObservationalBiasAudit(BaseModel):
    selection_bias_risk: BiasRiskLevel = BiasRiskLevel.LOW
    confounding_by_indication: BiasRiskLevel = BiasRiskLevel.LOW
    immortal_time_bias_protected: bool = True
    channeling_bias_detected: bool = False
    attrition_rate_percent: float = 0.0
    audit_summary: str = ""


class RWECohortDefinition(BaseModel):
    cohort_id: str = Field(default_factory=lambda: f"coh-{uuid.uuid4().hex[:8]}")
    cohort_name: str
    target_condition_codes: List[str] = Field(default_factory=list)
    index_exposure_codes: List[str] = Field(default_factory=list)
    comparator_exposure_codes: List[str] = Field(default_factory=list)
    inclusion_criteria: List[str] = Field(default_factory=list)
    exclusion_criteria: List[str] = Field(default_factory=list)
    observation_window_days: int = 365
    propensity_score_covariates: List[str] = Field(default_factory=list)


class RWEEvidenceSummary(BaseModel):
    """Structured real-world evidence output bridged into ZMIE Evidence Graph (Section 93)."""
    rwe_id: str = Field(default_factory=lambda: f"rwe-{uuid.uuid4().hex[:8]}")
    study_title: str
    target_cohort_size: int
    comparator_cohort_size: int
    primary_outcome_name: str
    hazard_ratio_or_relative_risk: float
    confidence_interval_95: List[float]
    p_value: float
    absolute_risk_reduction_percent: Optional[float] = None
    data_source_type: str
    evidence_ladder_tier: str = "E5_HUMAN_OBSERVATIONAL_RWE"
    bias_audit: ObservationalBiasAudit
    triangulation_with_rct_status: str
    causal_status: str = "OBSERVATIONAL_ASSOCIATION_CONTROLLED"  # Never automatic proven causation
    provenance_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
