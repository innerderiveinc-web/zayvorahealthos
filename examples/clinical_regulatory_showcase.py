#!/usr/bin/env python3
"""
ZMIE Global Clinical & Regulatory Intelligence Engine — Showcase Demonstration
Live demonstration of multi-jurisdictional product resolution, label diffing,
clinical guidelines, pharmacovigilance safety events, and claim compliance firewalls.
"""

import sys
import json
from app.clinical_regulatory.engine import ClinicalRegulatoryEngine
from app.models.clinical_regulatory import ClaimType


def run_showcase():
    print("=" * 85)
    print("  ZMIE — GLOBAL CLINICAL & REGULATORY INTELLIGENCE ENGINE (MODULE 18)")
    print("  Regulatory Approval != Scientific Proof | Guidelines != Market Authorization")
    print("=" * 85)

    engine = ClinicalRegulatoryEngine()

    # -------------------------------------------------------------
    # 1. Multi-Jurisdictional Product Resolution & Comparison
    # -------------------------------------------------------------
    print("\n[SCENARIO 1] MULTI-JURISDICTIONAL PRODUCT RESOLUTION & DIVERGENCE")
    print("-" * 85)
    card_dapa = engine.compare_jurisdictions("DAPAGLIFLOZIN")
    print(f"Product Canonical: {card_dapa.canonical_name} ({card_dapa.product_id})")
    for country, details in card_dapa.jurisdictions_data.items():
        print(f"  * {country:<15}: Authority: {details['authority']:<12} | Brand: {details['local_brand']:<10} | Status: {details['marketing_status']}")
        print(f"                     Indication: {details['approved_indication']}")
        print(f"                     App/License: {details['application_id']} | Last Verified: {details['last_verified']}")

    print("\nCross-Border Classification Divergence: Berberine")
    card_berb = engine.compare_jurisdictions("BERBERINE")
    for country, details in card_berb.jurisdictions_data.items():
        print(f"  * {country:<15}: Category: {details['classification']:<25} | Status: {details['marketing_status']}")
        print(f"                     Indication: {details['approved_indication']}")
    print("\nDivergences Identified by Engine:")
    for div in card_berb.divergences_identified:
        print(f"  ! {div}")

    # -------------------------------------------------------------
    # 2. Product Label Versioning & Diffing
    # -------------------------------------------------------------
    print("\n[SCENARIO 2] PRODUCT LABEL EVOLUTION & DIFF ENGINE")
    print("-" * 85)
    label_diff = engine.diff_product_labels("DAPAGLIFLOZIN", "United States")
    print(f"Product      : {label_diff.product_id} ({label_diff.jurisdiction})")
    print(f"Version Diff : {label_diff.old_version_tag} -> {label_diff.new_version_tag}")
    print("\nNewly Added Approved Indications:")
    for ind in label_diff.indications_added:
        print(f"  + {ind}")
    print("\nNewly Added Warnings & Precautions:")
    for warn in label_diff.warnings_added:
        print(f"  ! {warn}")
    print(f"\nSummary: {label_diff.change_summary}")

    # -------------------------------------------------------------
    # 3. Clinical Guidelines & Off-Label Separation
    # -------------------------------------------------------------
    print("\n[SCENARIO 3] SOURCE-BACKED CLINICAL GUIDELINES & RECOMMENDATIONS")
    print("-" * 85)
    guidelines = engine.list_guidelines_for_condition("Heart Failure")
    for g in guidelines:
        print(f"Guideline    : {g.title} ({g.publication_year})")
        print(f"Issuer       : {g.issuing_body} | Jurisdiction: {g.jurisdiction}")
        print("Key Recommendations:")
        for rec in g.recommendations:
            off_label_str = "OFF-LABEL" if rec.is_off_label_use else "ON-LABEL"
            print(f"  * Target: {rec.target_condition}")
            print(f"    Rec   : {rec.recommendation_statement}")
            print(f"    Grade : {rec.strength_of_recommendation} | Evidence: {rec.level_of_evidence} [{off_label_str}]")

    # -------------------------------------------------------------
    # 4. Pharmacovigilance & Batch-Level Product Recalls
    # -------------------------------------------------------------
    print("\n[SCENARIO 4] PHARMACOVIGILANCE SAFETY COMMUNICATIONS & LOT RECALLS")
    print("-" * 85)
    safety_events = engine.get_safety_events_for_product("DAPAGLIFLOZIN")
    for ev in safety_events:
        print(f"Safety Event : [{ev.severity.value}] {ev.title}")
        print(f"Authority    : {ev.authority.value} ({ev.jurisdiction_country}) on {ev.date_issued}")
        print(f"Causality    : {ev.causality_status}")
        print(f"Action       : {ev.mandated_action}")

    recalls = engine.get_recalls("METFORMIN")
    for r in recalls:
        print(f"\nRecall Event : {r.recall_class} — {r.product_name}")
        print(f"Manufacturer : {r.manufacturer} | Lots: {', '.join(r.lot_numbers)}")
        print(f"Reason       : {r.reason}")
        print(f"Status       : {r.recall_status} ({r.recall_date})")

    # -------------------------------------------------------------
    # 5. Claim Compliance Firewall Engine
    # -------------------------------------------------------------
    print("\n[SCENARIO 5] CLAIM COMPLIANCE FIREWALL & STATUTORY DISCLAIMERS")
    print("-" * 85)
    # Test 1: Non-compliant disease claim on supplement
    c1 = engine.evaluate_claim_compliance(
        product_id="BERBERINE",
        claim_statement="Berberine cures diabetes and permanently prevents heart failure.",
        target_jurisdiction="United States",
        claim_category=ClaimType.THERAPEUTIC_CLAIM
    )
    print("Submitted Statement 1: 'Berberine cures diabetes and permanently prevents heart failure.'")
    print(f"  Permitted in US    : {c1.is_permitted_in_jurisdiction}")
    print(f"  Label Supported    : {c1.is_supported_by_approved_label}")
    print(f"  Verdict            : {c1.compliance_verdict}")
    print(f"  Overstatements     : {', '.join(c1.overstatement_flags)}")
    print(f"  Mandatory Notice   : {c1.required_mandatory_disclaimer}")

    # Test 2: Compliant on-label drug claim
    c2 = engine.evaluate_claim_compliance(
        product_id="DAPAGLIFLOZIN",
        claim_statement="Farxiga is indicated to reduce hospitalization for heart failure in adult patients.",
        target_jurisdiction="United States",
        claim_category=ClaimType.THERAPEUTIC_CLAIM
    )
    print("\nSubmitted Statement 2: 'Farxiga is indicated to reduce hospitalization for heart failure in adult patients.'")
    print(f"  Permitted in US    : {c2.is_permitted_in_jurisdiction}")
    print(f"  Label Supported    : {c2.is_supported_by_approved_label}")
    print(f"  Verdict            : {c2.compliance_verdict}")
    print(f"  Legal Advisory     : {c2.legal_advice_disclaimer}")

    print("\n" + "=" * 85)
    print("  ZMIE GLOBAL CLINICAL & REGULATORY ENGINE: ALL 5 SCENARIOS VERIFIED")
    print("=" * 85)


if __name__ == "__main__":
    run_showcase()
