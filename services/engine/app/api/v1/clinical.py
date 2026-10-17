"""
ZMIE Clinical Decision Support API Router (Phase V3)
Enables integration with ZAYVORA Health OS and clinical EHR workstations.
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any
from app.agents.clinical_bridge import (
    ClinicalCDSBridge,
    ClinicalPatientContext,
    ClinicalGuidanceReport,
    CDSServicesDiscoveryResponse,
    CDSHooksResponse
)

router = APIRouter(prefix="/clinical", tags=["Clinical Decision Support, FHIR R4 & CDS Hooks"])


@router.post("/evaluate-patient", response_model=ClinicalGuidanceReport)
async def evaluate_patient_safety_and_evidence(context: ClinicalPatientContext):
    """
    Evaluates patient phenotype, EHR medications, and lab values against ZMIE medical evidence.
    """
    return ClinicalCDSBridge.evaluate_patient_context(context=context)


@router.post("/fhir/bundle")
async def generate_fhir_r4_bundle(context: ClinicalPatientContext):
    """
    Generates a 100% compliant HL7 FHIR R4 Document Bundle with Composition, Patient,
    DetectedIssue, RiskAssessment, ClinicalImpression, Observation, and Provenance.
    """
    return ClinicalCDSBridge.generate_fhir_r4_bundle(context=context)


@router.get("/fhir/sample-bundle")
async def get_sample_fhir_r4_bundle():
    """
    Returns an audited golden HL7 FHIR R4 Bundle for EHR integration testing.
    """
    sample_ctx = ClinicalPatientContext(
        patient_id="PAT-98421",
        age=64,
        sex="female",
        conditions=["Type 2 Diabetes Mellitus", "Essential Hypertension", "Mild CKD Stage 2"],
        current_medications=[
            {"name": "Metformin", "dose": "1000mg BID"},
            {"name": "Warfarin", "dose": "5mg daily"},
            {"name": "Atorvastatin", "dose": "20mg QHS"}
        ],
        recent_labs={
            "HbA1c": "7.8%",
            "eGFR": "54 mL/min",
            "INR": "2.3"
        },
        proposed_herbal_or_dietary="St. John's Wort"
    )
    return ClinicalCDSBridge.generate_fhir_r4_bundle(context=sample_ctx)


@router.get("/cds-services", response_model=CDSServicesDiscoveryResponse)
async def get_cds_services():
    """
    HL7 CDS Hooks 1.0 Discovery endpoint. Returns catalog of available clinical decision services.
    """
    return ClinicalCDSBridge.get_cds_services_manifest()


@router.post("/cds-services/{service_id}", response_model=CDSHooksResponse)
async def invoke_cds_service(service_id: str, request_data: Dict[str, Any] = Body(...)):
    """
    HL7 CDS Hooks 1.0 Service endpoint. Evaluates drug-herb orders and returns clinical advisory cards.
    """
    return ClinicalCDSBridge.evaluate_cds_hook_request(service_id=service_id, request_data=request_data)
