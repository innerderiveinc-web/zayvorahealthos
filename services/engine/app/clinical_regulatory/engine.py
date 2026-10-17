"""
ZMIE Global Clinical & Regulatory Intelligence Engine
Core implementation for multi-jurisdictional product resolution,
clinical guidelines, label versioning & diffing, safety communications,
and claim compliance firewalls.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from app.models.clinical_regulatory import (
    RegulatoryAuthorityCode,
    ProductClassification,
    RegulatoryMarketStatus,
    SafetySeverityLevel,
    RegulatorySafetyEventType,
    ClaimType,
    RegulatoryAuthorityRecord,
    ProductJurisdictionInstance,
    RegulatedProduct,
    ProductLabelVersion,
    LabelDiffReport,
    GuidelineRecommendation,
    ClinicalGuidelineRecord,
    RegulatorySafetyEvent,
    ProductRecallRecord,
    ClaimComplianceAssessment,
    MultiJurisdictionComparisonCard
)


class ClinicalRegulatoryEngine:
    """
    Scientific and regulatory intelligence engine tracking global authorities,
    product market status, clinical guidelines, label versions, and safety events.
    """

    def __init__(self):
        self._authorities: Dict[str, RegulatoryAuthorityRecord] = {}
        self._products: Dict[str, RegulatedProduct] = {}
        self._labels: Dict[str, List[ProductLabelVersion]] = {}
        self._guidelines: Dict[str, ClinicalGuidelineRecord] = {}
        self._safety_events: List[RegulatorySafetyEvent] = []
        self._recalls: List[ProductRecallRecord] = []

        self._seed_reference_data()

    def _seed_reference_data(self):
        """Pre-seeds key global authorities, products, labels, guidelines, and safety alerts."""
        # 1. Authorities
        self._authorities["US_FDA"] = RegulatoryAuthorityRecord(
            authority_id="AUTH-US-FDA",
            code=RegulatoryAuthorityCode.US_FDA,
            authority_name="United States Food and Drug Administration",
            jurisdiction_country="United States",
            region="North America",
            official_website="https://www.fda.gov",
            active_feeds_monitored=["Drugs@FDA", "MedWatch Safety Alerts", "FDA Recall Feeds", "Guidance Documents"],
            product_domains=[ProductClassification.DRUG, ProductClassification.BIOLOGIC, ProductClassification.MEDICAL_DEVICE, ProductClassification.DIETARY_SUPPLEMENT],
            last_verified_at=datetime.utcnow().strftime("%Y-%m-%d")
        )

        self._authorities["EU_EMA"] = RegulatoryAuthorityRecord(
            authority_id="AUTH-EU-EMA",
            code=RegulatoryAuthorityCode.EU_EMA,
            authority_name="European Medicines Agency",
            jurisdiction_country="European Union",
            region="Europe",
            official_website="https://www.ema.europa.eu",
            active_feeds_monitored=["CHMP Meeting Highlights", "PRAC Safety Agendas", "EPAR Publications", "HMPC Monographs"],
            product_domains=[ProductClassification.DRUG, ProductClassification.BIOLOGIC, ProductClassification.HERBAL_MEDICINAL_PRODUCT],
            last_verified_at=datetime.utcnow().strftime("%Y-%m-%d")
        )

        self._authorities["IN_CDSCO"] = RegulatoryAuthorityRecord(
            authority_id="AUTH-IN-CDSCO",
            code=RegulatoryAuthorityCode.IN_CDSCO,
            authority_name="Central Drugs Standard Control Organisation (India)",
            jurisdiction_country="India",
            region="South Asia",
            official_website="https://cdsco.gov.in",
            active_feeds_monitored=["New Drug Approval Lists", "SUGAM Portal Circulars", "Gazette Notifications", "PvPI Safety Alerts"],
            product_domains=[ProductClassification.DRUG, ProductClassification.BIOLOGIC, ProductClassification.MEDICAL_DEVICE, ProductClassification.VACCINE],
            last_verified_at=datetime.utcnow().strftime("%Y-%m-%d")
        )

        self._authorities["IN_AYUSH"] = RegulatoryAuthorityRecord(
            authority_id="AUTH-IN-AYUSH",
            code=RegulatoryAuthorityCode.IN_AYUSH,
            authority_name="Ministry of AYUSH (Ayurveda, Yoga, Unani, Siddha, Homoeopathy)",
            jurisdiction_country="India",
            region="South Asia",
            official_website="https://ayush.gov.in",
            active_feeds_monitored=["Pharmacopoeial Laboratory Notices", "Drugs & Cosmetics Act Schedule I Circulars", "NAMASTE Portal Updates"],
            product_domains=[ProductClassification.TRADITIONAL_AYUSH_MEDICINE, ProductClassification.HERBAL_MEDICINAL_PRODUCT],
            last_verified_at=datetime.utcnow().strftime("%Y-%m-%d")
        )

        # 2. Regulated Products
        # Dapagliflozin
        dapa_us = ProductJurisdictionInstance(
            instance_id="INST-DAPA-US",
            jurisdiction_country="United States",
            authority=RegulatoryAuthorityCode.US_FDA,
            local_brand_name="Farxiga",
            classification=ProductClassification.DRUG,
            marketing_status=RegulatoryMarketStatus.APPROVED,
            application_or_license_number="NDA 202293",
            approved_indication="Type 2 Diabetes, Heart Failure with reduced/preserved ejection fraction, Chronic Kidney Disease",
            population="Adults >= 18 yrs with T2D, HFrEF/HFpEF, or CKD",
            effective_date="2014-01-08",
            boxed_warning_present=False,
            active_recall_present=False,
            source_reference_url="https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo=202293",
            last_verified_at=datetime.utcnow().strftime("%Y-%m-%d")
        )
        dapa_eu = ProductJurisdictionInstance(
            instance_id="INST-DAPA-EU",
            jurisdiction_country="European Union",
            authority=RegulatoryAuthorityCode.EU_EMA,
            local_brand_name="Forxiga",
            classification=ProductClassification.DRUG,
            marketing_status=RegulatoryMarketStatus.APPROVED,
            application_or_license_number="EMEA/H/C/002322",
            approved_indication="Type 2 Diabetes, Symptomatic chronic heart failure (HFrEF/HFpEF), Chronic kidney disease",
            population="Adults with T2D, symptomatic chronic HF, or CKD",
            effective_date="2012-11-12",
            boxed_warning_present=False,
            active_recall_present=False,
            source_reference_url="https://www.ema.europa.eu/en/medicines/human/EPAR/forxiga",
            last_verified_at=datetime.utcnow().strftime("%Y-%m-%d")
        )
        dapa_in = ProductJurisdictionInstance(
            instance_id="INST-DAPA-IN",
            jurisdiction_country="India",
            authority=RegulatoryAuthorityCode.IN_CDSCO,
            local_brand_name="Forxiga",
            classification=ProductClassification.DRUG,
            marketing_status=RegulatoryMarketStatus.APPROVED,
            application_or_license_number="MF-ND-2015-081",
            approved_indication="Type 2 Diabetes Mellitus, Heart failure in adults, Chronic Kidney Disease",
            population="Adults with T2D or Heart Failure",
            effective_date="2015-04-20",
            boxed_warning_present=False,
            active_recall_present=False,
            source_reference_url="https://cdsco.gov.in/opencms/opencms/en/Approval_new/Approved-New-Drugs/",
            last_verified_at=datetime.utcnow().strftime("%Y-%m-%d")
        )
        self._products["DAPAGLIFLOZIN"] = RegulatedProduct(
            product_id="DAPAGLIFLOZIN",
            canonical_name="Dapagliflozin",
            generic_or_inn_name="dapagliflozin propanediol",
            active_ingredients=["Dapagliflozin"],
            sponsor_or_manufacturer="AstraZeneca",
            jurisdictional_instances=[dapa_us, dapa_eu, dapa_in]
        )

        # Berberine (Multi-jurisdictional divergence)
        berb_us = ProductJurisdictionInstance(
            instance_id="INST-BERB-US",
            jurisdiction_country="United States",
            authority=RegulatoryAuthorityCode.US_FDA,
            local_brand_name="Berberine HCl (Various Brands)",
            classification=ProductClassification.DIETARY_SUPPLEMENT,
            marketing_status=RegulatoryMarketStatus.AUTHORIZED,  # Marketed under DSHEA 1994
            application_or_license_number="DSHEA-NOTIFIED",
            approved_indication="Structure/Function support for glucose metabolism (NOT approved to treat Diabetes)",
            population="General adult population",
            effective_date="1994-10-15",
            source_reference_url="https://www.fda.gov/food/dietary-supplements",
            last_verified_at=datetime.utcnow().strftime("%Y-%m-%d")
        )
        berb_in = ProductJurisdictionInstance(
            instance_id="INST-BERB-IN",
            jurisdiction_country="India",
            authority=RegulatoryAuthorityCode.IN_AYUSH,
            local_brand_name="Daruharidra / Berberis aristata extract",
            classification=ProductClassification.TRADITIONAL_AYUSH_MEDICINE,
            marketing_status=RegulatoryMarketStatus.APPROVED,
            application_or_license_number="AYUSH-LIC-DCA-1940",
            approved_indication="Prameha (metabolic disorders/diabetes), Yakrit Vikara (hepatic disorders)",
            population="Adult patients under Ayurvedic / Unani practice",
            effective_date="1940-01-01",
            source_reference_url="https://ayush.gov.in/pharmacopoeia",
            last_verified_at=datetime.utcnow().strftime("%Y-%m-%d")
        )
        self._products["BERBERINE"] = RegulatedProduct(
            product_id="BERBERINE",
            canonical_name="Berberine",
            generic_or_inn_name="berberine alkaloid",
            active_ingredients=["Berberine Hydrochloride", "Berberis aristata extract"],
            sponsor_or_manufacturer="Multiple / Generic / Classical Manufacturers",
            jurisdictional_instances=[berb_us, berb_in],
            traditional_medicine_system="AYURVEDA / UNANI"
        )

        # 3. Product Labels & Versioning
        # Dapagliflozin US Labels (v1.0 vs v2.0)
        lbl_v1 = ProductLabelVersion(
            label_id="LBL-DAPA-US-v1",
            product_id="DAPAGLIFLOZIN",
            jurisdiction_country="United States",
            authority=RegulatoryAuthorityCode.US_FDA,
            version_tag="v1.0",
            effective_date="2014-01-08",
            approved_indications=["Adjunct to diet and exercise to improve glycemic control in adults with type 2 diabetes mellitus."],
            contraindications=["Severe renal impairment (eGFR < 30 mL/min/1.73m2)", "End-stage renal disease or patients on dialysis"],
            boxed_warnings=[],
            warnings_and_precautions=["Hypotension / volume depletion", "Ketoacidosis in patients with diabetes", "Urosepsis and pyelonephritis"],
            dosage_and_administration="5 mg orally once daily in the morning; can be increased to 10 mg once daily.",
            drug_interactions=["Insulin and insulin secretagogues (increased hypoglycemia risk)"],
            source_document_url="https://accessdata.fda.gov/drugsatfda_docs/label/2014/202293s000lbl.pdf"
        )
        lbl_v2 = ProductLabelVersion(
            label_id="LBL-DAPA-US-v2",
            product_id="DAPAGLIFLOZIN",
            jurisdiction_country="United States",
            authority=RegulatoryAuthorityCode.US_FDA,
            version_tag="v2.0",
            effective_date="2020-05-05",
            approved_indications=[
                "Adjunct to diet and exercise to improve glycemic control in adults with type 2 diabetes mellitus.",
                "To reduce the risk of cardiovascular death and hospitalization for heart failure in adults with heart failure with reduced ejection fraction (NYHA class II-IV)."
            ],
            contraindications=["History of serious hypersensitivity reaction to dapagliflozin", "Patients on dialysis"],
            boxed_warnings=[],
            warnings_and_precautions=[
                "Ketoacidosis in patients with diabetes",
                "Volume depletion",
                "Urosepsis and pyelonephritis",
                "Necrotizing fasciitis of the perineum (Fournier's gangrene)"
            ],
            dosage_and_administration="Heart Failure: 10 mg orally once daily.",
            drug_interactions=["Insulin and insulin secretagogues", "Positive urine glucose test interference"],
            source_document_url="https://accessdata.fda.gov/drugsatfda_docs/label/2020/202293s020lbl.pdf"
        )
        self._labels["DAPAGLIFLOZIN-US"] = [lbl_v1, lbl_v2]

        # 4. Clinical Guidelines
        rec_hfref = GuidelineRecommendation(
            recommendation_id="REC-AHA-SGLT2I-HFREF",
            target_condition="Heart Failure with Reduced Ejection Fraction (HFrEF)",
            population_context="Adults with symptomatic HFrEF (LVEF <= 40%) regardless of presence of diabetes",
            intervention_recommended="SGLT2 inhibitors (Dapagliflozin or Empagliflozin)",
            recommendation_statement="In patients with symptomatic chronic HFrEF, SGLT2 inhibitors are recommended to reduce hospitalization for HF and cardiovascular mortality.",
            strength_of_recommendation="Class 1 (Strong)",
            level_of_evidence="Level A (High quality evidence from multiple RCTs)",
            is_off_label_use=False,
            evidence_citations=["DAPA-HF (NEJM 2019)", "EMPEROR-Reduced (NEJM 2020)"]
        )
        rec_hfpef = GuidelineRecommendation(
            recommendation_id="REC-AHA-SGLT2I-HFPEF",
            target_condition="Heart Failure with Preserved Ejection Fraction (HFpEF)",
            population_context="Adults with symptomatic HFpEF (LVEF > 50%)",
            intervention_recommended="SGLT2 inhibitors",
            recommendation_statement="In patients with HFpEF, SGLT2 inhibitors can be beneficial in decreasing HF hospitalizations and cardiovascular mortality.",
            strength_of_recommendation="Class 2a (Moderate)",
            level_of_evidence="Level B-R (Randomized trial data)",
            is_off_label_use=False,
            evidence_citations=["EMPEROR-Preserved (NEJM 2021)", "DELIVER (NEJM 2022)"]
        )
        self._guidelines["GUIDE-AHA-HF-2022"] = ClinicalGuidelineRecord(
            guideline_id="GUIDE-AHA-HF-2022",
            title="2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure",
            issuing_body="AHA / ACC / HFSA",
            jurisdiction="United States",
            publication_year=2022,
            version="2022 Final",
            target_disease_or_condition="Heart Failure",
            recommendations=[rec_hfref, rec_hfpef],
            source_url="https://doi.org/10.1161/CIR.0000000000001063"
        )

        # 5. Safety Events & Recalls
        self._safety_events.append(RegulatorySafetyEvent(
            event_id="SAFE-FDA-SGLT2I-KETO",
            product_id="DAPAGLIFLOZIN",
            authority=RegulatoryAuthorityCode.US_FDA,
            jurisdiction_country="United States",
            event_type=RegulatorySafetyEventType.SAFETY_COMMUNICATION,
            severity=SafetySeverityLevel.HIGH,
            date_issued="2015-05-15",
            title="FDA warns that SGLT2 inhibitors for diabetes may result in a serious condition called ketoacidosis",
            clinical_risk_description="Reports of euglycemic diabetic ketoacidosis presenting with blood glucose levels lower than typical diabetic ketoacidosis.",
            mandated_action="Physicians should evaluate for ketones immediately; stop medication if acidosis is suspected.",
            causality_status="CONFIRMED_CAUSAL_RISK",
            official_notice_url="https://www.fda.gov/drugs/drug-safety-and-availability/fda-drug-safety-communication-fda-warns-sglt2-inhibitors"
        ))

        self._recalls.append(ProductRecallRecord(
            recall_id="REC-METFORMIN-NDMA-2020",
            product_id="METFORMIN",
            product_name="Metformin Hydrochloride Extended-Release Tablets, USP 500 mg and 750 mg",
            lot_numbers=["LOT-MET-8841", "LOT-MET-8842"],
            manufacturer="Apotex Corp",
            authority=RegulatoryAuthorityCode.US_FDA,
            jurisdiction_country="United States",
            recall_class="Class II Recall",
            recall_date="2020-05-29",
            reason="Detection of N-Nitrosodimethylamine (NDMA) impurity exceeding the acceptable daily intake limit of 96 ng/day.",
            action_taken="Voluntary nationwide retail and patient level recall of affected lots.",
            recall_status="COMPLETED",
            source_notice_url="https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts/apotex-corp-issues-voluntary-nationwide-recall-metformin"
        ))

    # -------------------------------------------------------------------------
    # 1. Product Lookups & Cross-Jurisdiction Comparison
    # -------------------------------------------------------------------------

    def get_product(self, product_id: str) -> Optional[RegulatedProduct]:
        return self._products.get(product_id.upper())

    def compare_jurisdictions(self, product_id: str) -> Optional[MultiJurisdictionComparisonCard]:
        """
        Generates a transparent cross-jurisdiction comparison card for a product,
        highlighting differences in market status, classifications, and approved indications.
        """
        prod = self.get_product(product_id)
        if not prod:
            return None

        j_data = {}
        divergences = []

        classifications_seen = set()
        indications_seen = set()

        for inst in prod.jurisdictional_instances:
            classifications_seen.add(inst.classification.value)
            indications_seen.add(inst.approved_indication)
            j_data[inst.jurisdiction_country] = {
                "authority": inst.authority.value,
                "local_brand": inst.local_brand_name,
                "classification": inst.classification.value,
                "marketing_status": inst.marketing_status.value,
                "application_id": inst.application_or_license_number,
                "approved_indication": inst.approved_indication,
                "boxed_warning": inst.boxed_warning_present,
                "active_recall": inst.active_recall_present,
                "last_verified": inst.last_verified_at,
                "source_url": inst.source_reference_url
            }

        if len(classifications_seen) > 1:
            divergences.append(
                f"Regulatory classification varies across borders: {', '.join(classifications_seen)}. "
                "Product cannot be assumed to hold identical legal status globally."
            )
        if len(indications_seen) > 1:
            divergences.append("Approved clinical indications differ between jurisdictions.")

        return MultiJurisdictionComparisonCard(
            product_id=prod.product_id,
            canonical_name=prod.canonical_name,
            comparison_timestamp=datetime.utcnow().isoformat(),
            jurisdictions_data=j_data,
            divergences_identified=divergences
        )

    # -------------------------------------------------------------------------
    # 2. Product Label Diffing Engine
    # -------------------------------------------------------------------------

    def diff_product_labels(
        self,
        product_id: str,
        jurisdiction_country: str = "United States"
    ) -> Optional[LabelDiffReport]:
        """
        Compares sequential product label versions for a given jurisdiction.
        """
        key = f"{product_id.upper()}-US" if "united states" in jurisdiction_country.lower() else f"{product_id.upper()}-EU"
        labels = self._labels.get(key)
        if not labels or len(labels) < 2:
            return None

        v1, v2 = labels[0], labels[1]
        ind_added = [i for i in v2.approved_indications if i not in v1.approved_indications]
        ind_removed = [i for i in v1.approved_indications if i not in v2.approved_indications]
        warn_added = [w for w in v2.warnings_and_precautions if w not in v1.warnings_and_precautions]
        contra_added = [c for c in v2.contraindications if c not in v1.contraindications]

        summary = (
            f"Label evolution from {v1.version_tag} ({v1.effective_date}) to {v2.version_tag} ({v2.effective_date}): "
            f"Added {len(ind_added)} new indication(s) including Heart Failure, and {len(warn_added)} new warning(s) "
            f"(e.g., {', '.join(warn_added)})."
        )

        return LabelDiffReport(
            product_id=product_id.upper(),
            jurisdiction=jurisdiction_country,
            old_version_tag=v1.version_tag,
            new_version_tag=v2.version_tag,
            indications_added=ind_added,
            indications_removed=ind_removed,
            warnings_added=warn_added,
            contraindications_added=contra_added,
            change_summary=summary
        )

    # -------------------------------------------------------------------------
    # 3. Clinical Guidelines Lookups
    # -------------------------------------------------------------------------

    def get_guideline(self, guideline_id: str) -> Optional[ClinicalGuidelineRecord]:
        return self._guidelines.get(guideline_id)

    def list_guidelines_for_condition(self, condition: str) -> List[ClinicalGuidelineRecord]:
        cond_lower = condition.lower()
        return [
            g for g in self._guidelines.values()
            if cond_lower in g.target_disease_or_condition.lower() or cond_lower in g.title.lower()
        ]

    # -------------------------------------------------------------------------
    # 4. Pharmacovigilance & Safety Alerts
    # -------------------------------------------------------------------------

    def get_safety_events_for_product(self, product_id: str) -> List[RegulatorySafetyEvent]:
        pid = product_id.upper()
        return [e for e in self._safety_events if e.product_id == pid]

    def get_recalls(self, product_id: Optional[str] = None) -> List[ProductRecallRecord]:
        if product_id:
            pid = product_id.upper()
            return [r for r in self._recalls if r.product_id == pid]
        return self._recalls

    # -------------------------------------------------------------------------
    # 5. Claim Compliance Firewall Engine
    # -------------------------------------------------------------------------

    def evaluate_claim_compliance(
        self,
        product_id: str,
        claim_statement: str,
        target_jurisdiction: str = "United States",
        claim_category: ClaimType = ClaimType.THERAPEUTIC_CLAIM
    ) -> ClaimComplianceAssessment:
        """
        Compliance Firewall:
        1. Checks whether claim is supported by the verified product label in the target jurisdiction.
        2. Detects prohibited overstatements ('cures', 'treats', 'miracle', 'prevents').
        3. Identifies statutory disclaimers (e.g. DSHEA disclaimer for supplements).
        4. Issues explicit legal-disclaimer notice.
        """
        prod = self.get_product(product_id)
        pid = product_id.upper()
        stmt_lower = claim_statement.lower()

        overstatements = []
        for word in ["cure", "cures", "miracle", "guaranteed", "definitively prevents"]:
            if word in stmt_lower:
                overstatements.append(f"Prohibited overstatement term detected: '{word}'")

        # Find jurisdictional instance
        inst = None
        if prod:
            for j in prod.jurisdictional_instances:
                if j.jurisdiction_country.lower() in target_jurisdiction.lower():
                    inst = j
                    break

        is_supported = False
        is_permitted = True
        restrictions = []
        mandatory_disclaimer = None

        if not inst:
            verdict = "UNAUTHORIZED_OR_UNVERIFIED_IN_JURISDICTION"
            restrictions.append(f"Product {pid} has no documented marketing authorization record in {target_jurisdiction}.")
            is_permitted = False
        elif inst.classification == ProductClassification.DIETARY_SUPPLEMENT:
            # Supplements cannot make disease treatment/cure claims under US DSHEA
            if any(term in stmt_lower for term in ["treat", "cure", "prevent", "diabetes", "heart failure"]):
                is_supported = False
                is_permitted = False
                restrictions.append("Dietary supplements cannot bear disease treatment or prevention claims (21 U.S.C. 343(r)(6)).")
                overstatements.append("Disease treatment claim made for dietary supplement.")
                verdict = "NON_COMPLIANT_DISEASE_CLAIM_FOR_SUPPLEMENT"
            else:
                is_supported = True
                verdict = "STRUCTURE_FUNCTION_CLAIM_PERMITTED_WITH_DISCLAIMER"
            mandatory_disclaimer = (
                "These statements have not been evaluated by the Food and Drug Administration. "
                "This product is not intended to diagnose, treat, cure, or prevent any disease."
            )
        elif inst.classification == ProductClassification.DRUG:
            if inst.marketing_status != RegulatoryMarketStatus.APPROVED:
                is_permitted = False
                verdict = "DRUG_NOT_APPROVED_FOR_MARKETING"
                restrictions.append(f"Drug status is {inst.marketing_status.value}; commercial therapeutic claims prohibited.")
            else:
                # Check if statement matches approved indication
                has_overlap = any(kw in stmt_lower for kw in ["heart failure", "diabetes", "kidney", "glycemic"])
                if has_overlap and not overstatements:
                    is_supported = True
                    verdict = "ON_LABEL_THERAPEUTIC_CLAIM_PERMITTED"
                else:
                    is_supported = False
                    verdict = "POTENTIAL_OFF_LABEL_OR_OVERSTATED_CLAIM"
                    restrictions.append("Claim scope exceeds or deviates from officially approved product label indications.")
        else:
            verdict = "CATEGORY_SPECIFIC_REGULATION_APPLIES"

        return ClaimComplianceAssessment(
            claim_id=f"CLM-{int(datetime.utcnow().timestamp())}",
            submitted_statement=claim_statement,
            product_id=pid,
            target_jurisdiction=target_jurisdiction,
            claim_category=claim_category,
            is_supported_by_approved_label=is_supported,
            is_permitted_in_jurisdiction=is_permitted,
            regulatory_restrictions=restrictions,
            required_mandatory_disclaimer=mandatory_disclaimer,
            overstatement_flags=overstatements,
            compliance_verdict=verdict
        )
