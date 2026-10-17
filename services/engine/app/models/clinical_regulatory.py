"""
ZMIE Global Clinical & Regulatory Intelligence Engine Models
Models for multi-jurisdictional product authorization, clinical guidelines,
label versioning, pharmacovigilance safety events, recalls, and traditional medicine regulation.
"""

from typing import List, Dict, Any, Optional, Union
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class RegulatoryAuthorityCode(str, Enum):
    US_FDA = "US_FDA"
    EU_EMA = "EU_EMA"
    UK_MHRA = "UK_MHRA"
    IN_CDSCO = "IN_CDSCO"
    JP_PMDA = "JP_PMDA"
    CA_HEALTH_CANADA = "CA_HEALTH_CANADA"
    AU_TGA = "AU_TGA"
    WHO = "WHO"
    IN_AYUSH = "IN_AYUSH"


class ProductClassification(str, Enum):
    DRUG = "DRUG"
    BIOLOGIC = "BIOLOGIC"
    VACCINE = "VACCINE"
    MEDICAL_DEVICE = "MEDICAL_DEVICE"
    IVD = "IVD"
    DIGITAL_HEALTH_SAMD = "DIGITAL_HEALTH_SAMD"
    AI_ENABLED_DEVICE = "AI_ENABLED_DEVICE"
    HERBAL_MEDICINAL_PRODUCT = "HERBAL_MEDICINAL_PRODUCT"
    TRADITIONAL_AYUSH_MEDICINE = "TRADITIONAL_AYUSH_MEDICINE"
    DIETARY_SUPPLEMENT = "DIETARY_SUPPLEMENT"
    NUTRACEUTICAL = "NUTRACEUTICAL"
    COSMETIC = "COSMETIC"


class RegulatoryMarketStatus(str, Enum):
    NOT_SUBMITTED = "NOT_SUBMITTED"
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    AUTHORIZED = "AUTHORIZED"
    APPROVED = "APPROVED"
    CONDITIONALLY_AUTHORIZED = "CONDITIONALLY_AUTHORIZED"
    EMERGENCY_AUTHORIZATION = "EMERGENCY_AUTHORIZATION"
    LIMITED_AUTHORIZATION = "LIMITED_AUTHORIZATION"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"
    DISCONTINUED = "DISCONTINUED"
    RECALLED = "RECALLED"
    RESTRICTED = "RESTRICTED"
    CURRENT_STATUS_NOT_VERIFIED = "CURRENT_STATUS_NOT_VERIFIED"
    UNKNOWN = "UNKNOWN"


class SafetySeverityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class RegulatorySafetyEventType(str, Enum):
    BOXED_WARNING = "BOXED_WARNING"
    SAFETY_COMMUNICATION = "SAFETY_COMMUNICATION"
    CONTRAINDICATION_ADDED = "CONTRAINDICATION_ADDED"
    CLASS_I_RECALL = "CLASS_I_RECALL"
    CLASS_II_RECALL = "CLASS_II_RECALL"
    CLASS_III_RECALL = "CLASS_III_RECALL"
    INDICATION_RESTRICTION = "INDICATION_RESTRICTION"
    DEAR_HEALTHCARE_PROFESSIONAL_LETTER = "DEAR_HEALTHCARE_PROFESSIONAL_LETTER"
    POST_MARKET_STUDY_MANDATE = "POST_MARKET_STUDY_MANDATE"


class ClaimType(str, Enum):
    THERAPEUTIC_CLAIM = "THERAPEUTIC_CLAIM"
    HEALTH_CLAIM = "HEALTH_CLAIM"
    STRUCTURE_FUNCTION_CLAIM = "STRUCTURE_FUNCTION_CLAIM"
    TRADITIONAL_USE_CLAIM = "TRADITIONAL_USE_CLAIM"
    NUTRITIONAL_CLAIM = "NUTRITIONAL_CLAIM"
    DIAGNOSTIC_CLAIM = "DIAGNOSTIC_CLAIM"


# -------------------------------------------------------------
# 1. Authority & Source Registries
# -------------------------------------------------------------

class RegulatoryAuthorityRecord(BaseModel):
    authority_id: str
    code: RegulatoryAuthorityCode
    authority_name: str
    jurisdiction_country: str
    region: str
    official_website: str
    active_feeds_monitored: List[str] = Field(default_factory=list)
    product_domains: List[ProductClassification] = Field(default_factory=list)
    status: str = "ACTIVE_MONITORED"
    last_verified_at: str


# -------------------------------------------------------------
# 2. Product Identity & Jurisdictional Instances
# -------------------------------------------------------------

class ProductJurisdictionInstance(BaseModel):
    instance_id: str
    jurisdiction_country: str
    authority: RegulatoryAuthorityCode
    local_brand_name: str
    classification: ProductClassification
    marketing_status: RegulatoryMarketStatus
    application_or_license_number: str
    approved_indication: str
    population: str
    effective_date: str
    expiration_date: Optional[str] = None
    boxed_warning_present: bool = False
    active_recall_present: bool = False
    source_reference_url: str
    last_verified_at: str


class RegulatedProduct(BaseModel):
    product_id: str
    canonical_name: str
    generic_or_inn_name: str
    active_ingredients: List[str] = Field(default_factory=list)
    sponsor_or_manufacturer: str
    jurisdictional_instances: List[ProductJurisdictionInstance] = Field(default_factory=list)
    traditional_medicine_system: Optional[str] = None  # UNANI, AYURVEDA, etc.


# -------------------------------------------------------------
# 3. Product Label & Versioning
# -------------------------------------------------------------

class ProductLabelVersion(BaseModel):
    label_id: str
    product_id: str
    jurisdiction_country: str
    authority: RegulatoryAuthorityCode
    version_tag: str  # "Label-v2.1"
    effective_date: str
    approved_indications: List[str] = Field(default_factory=list)
    contraindications: List[str] = Field(default_factory=list)
    boxed_warnings: List[str] = Field(default_factory=list)
    warnings_and_precautions: List[str] = Field(default_factory=list)
    dosage_and_administration: str
    drug_interactions: List[str] = Field(default_factory=list)
    source_document_url: str


class LabelDiffReport(BaseModel):
    product_id: str
    jurisdiction: str
    old_version_tag: str
    new_version_tag: str
    indications_added: List[str] = Field(default_factory=list)
    indications_removed: List[str] = Field(default_factory=list)
    warnings_added: List[str] = Field(default_factory=list)
    contraindications_added: List[str] = Field(default_factory=list)
    change_summary: str


# -------------------------------------------------------------
# 4. Clinical Guidelines & Recommendations
# -------------------------------------------------------------

class GuidelineRecommendation(BaseModel):
    recommendation_id: str
    target_condition: str
    population_context: str
    intervention_recommended: str
    comparator_context: Optional[str] = None
    recommendation_statement: str
    strength_of_recommendation: str  # Class I, Class IIa, Class IIb, Strong, Conditional
    level_of_evidence: str  # Level A, Level B-R, High, Moderate
    is_off_label_use: bool = False
    evidence_citations: List[str] = Field(default_factory=list)


class ClinicalGuidelineRecord(BaseModel):
    guideline_id: str
    title: str
    issuing_body: str  # AHA/ACC, ESC, NICE, WHO, ICMR, etc.
    jurisdiction: str  # US, EU, UK, Global, India
    publication_year: int
    version: str = "v1.0"
    target_disease_or_condition: str
    recommendations: List[GuidelineRecommendation] = Field(default_factory=list)
    superseded_by: Optional[str] = None
    source_url: str


# -------------------------------------------------------------
# 5. Pharmacovigilance & Safety Events
# -------------------------------------------------------------

class RegulatorySafetyEvent(BaseModel):
    event_id: str
    product_id: str
    authority: RegulatoryAuthorityCode
    jurisdiction_country: str
    event_type: RegulatorySafetyEventType
    severity: SafetySeverityLevel
    date_issued: str
    title: str
    clinical_risk_description: str
    mandated_action: str
    causality_status: str = "OBSERVED_SAFETY_SIGNAL"  # OBSERVED_SAFETY_SIGNAL vs CONFIRMED_CAUSAL_RISK
    batch_or_lot_numbers: List[str] = Field(default_factory=list)
    official_notice_url: str


class ProductRecallRecord(BaseModel):
    recall_id: str
    product_id: str
    product_name: str
    lot_numbers: List[str] = Field(default_factory=list)
    manufacturer: str
    authority: RegulatoryAuthorityCode
    jurisdiction_country: str
    recall_class: str  # Class I (life-threatening), Class II, Class III
    recall_date: str
    reason: str
    action_taken: str
    recall_status: str = "ACTIVE"  # ACTIVE, COMPLETED, TERMINATED
    source_notice_url: str


# -------------------------------------------------------------
# 6. Claim Compliance & Legal Firewall
# -------------------------------------------------------------

class ClaimComplianceAssessment(BaseModel):
    claim_id: str
    submitted_statement: str
    product_id: str
    target_jurisdiction: str
    claim_category: ClaimType
    is_supported_by_approved_label: bool
    is_permitted_in_jurisdiction: bool
    regulatory_restrictions: List[str] = Field(default_factory=list)
    required_mandatory_disclaimer: Optional[str] = None
    overstatement_flags: List[str] = Field(default_factory=list)
    compliance_verdict: str
    legal_advice_disclaimer: str = (
        "Regulatory intelligence is informational and source-based. "
        "It does not constitute formal legal counsel or guaranteed compliance certification."
    )


# -------------------------------------------------------------
# 7. Multi-Jurisdiction Comparison Snapshot
# -------------------------------------------------------------

class MultiJurisdictionComparisonCard(BaseModel):
    product_id: str
    canonical_name: str
    comparison_timestamp: str
    jurisdictions_data: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    divergences_identified: List[str] = Field(default_factory=list)
    epistemic_note: str = (
        "Regulatory status, approved indications, and safety warnings vary by jurisdiction. "
        "Authorization in one country does not imply global authorization."
    )
