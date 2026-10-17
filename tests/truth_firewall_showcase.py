"""
ZMIE Truth, Claim Validation & Safety Firewall Showcase (Prompt 7 Deliverable)
Demonstrates:
1. Demo 1: Full Pipeline Verification across Diverse Claims (Numerical, Clinical, Traditional, Safety, Causality).
2. Demo 2: Failure & Anti-Hallucination Protections (Fabricated citations, wrong numbers, causal inflation, false equivalence).
3. Demo 3: Retraction Propagation and Cascading Impact Analysis across Knowledge Artifacts.
4. Demo 4: Cross-System Equivalence Firewall (Mizaj / Dosha qualified analogy vs false equivalence).
"""

import json
from app.models.truth_firewall import Citation, FirewallVerdict
from app.firewall.orchestrator import TruthAndSafetyFirewall
from app.firewall.citation_engine import CitationVerificationEngine
from app.firewall.causality_firewall import CausalityAndLanguageFirewall


def run_truth_firewall_showcase():
    print("=" * 80)
    print(" ZMIE TRUTH, EVIDENCE INTEGRITY & SAFETY FIREWALL — MASTER SHOWCASE (PROMPT 7) ")
    print("=" * 80)

    # -------------------------------------------------------------
    # DEMO 1: End-to-End Multidimensional Answer Verification
    # -------------------------------------------------------------
    print("\n[DEMO 1] End-to-End Multidimensional Answer Verification")
    answer_text = (
        "Berberine lowered fasting blood glucose by 1.8% in adult patients with type 2 diabetes. "
        "Darhald has been utilized in Unani Tibb for hot-type metabolic disorders. "
        "High-dose berberine causes gastrointestinal cramping and is contraindicated during pregnancy."
    )
    citations = [
        Citation(
            source_id="SRC-101",
            document_id="DOC-101",
            title="Randomized trial of berberine in diabetes",
            identifier="PMID:18442638"
        ),
        Citation(
            source_id="SRC-UNANI-01",
            document_id="DOC-UNANI-01",
            title="Kitab al-Hawi Fi al-Tibb",
            identifier="UNANI-CCUM-09"
        ),
        Citation(
            source_id="SRC-SAFETY-01",
            document_id="DOC-SAFETY-01",
            title="Pharmacovigilance review of berberine salts",
            identifier="PMID:25861268"
        )
    ]
    passages = {
        "PMID:18442638": "In a randomized trial of 116 adult patients with type 2 diabetes, berberine lowered fasting blood glucose by 1.8% after 12 weeks.",
        "UNANI-CCUM-09": "Classical Unani codices document Darhald for managing hot temperament disorders and liver debility.",
        "PMID:25861268": "High-dose berberine may induce gastrointestinal cramping and is contraindicated during pregnancy due to uterine stimulation."
    }

    packet1 = TruthAndSafetyFirewall.verify_answer(answer_text, citations, passages)
    print(f"  -> Original Answer: {answer_text[:65]}...")
    print(f"  -> Firewall Status: {packet1.status} | Verdict: {packet1.verdict.value}")
    print(f"  -> Claims Checked: {packet1.verification_metrics['claims_checked']} (Supported: {packet1.verification_metrics['supported']})")
    for clm in packet1.claims:
        print(f"     * [{clm.claim_type.value}] '{clm.claim_text[:50]}...' -> Status: {clm.claim_status.value} (Risk: {clm.risk_level.value})")

    # -------------------------------------------------------------
    # DEMO 2: Failure & Anti-Hallucination Protections
    # -------------------------------------------------------------
    print("\n[DEMO 2] Failure & Anti-Hallucination Protections")
    adversarial_claims = [
        ("Fabricated Citation", "Berberine cures diabetes", Citation(source_id="S1", document_id="D1", title="Bogus", identifier="FAKE_DOI_123456"), "Passage text"),
        ("Wrong Number", "Berberine reduced HbA1c by 45%", citations[0], "Study observed berberine lowered HbA1c by 1.8% in patients."),
        ("Causal Overreach", "Observational findings prove berberine cures neuropathy permanently", None, None),
        ("Retracted Source", "Berberine nanocapsules reverse beta-cell death", Citation(source_id="S3", document_id="D3", title="Retracted paper", identifier="10.1000/retracted-trial", is_retracted=True), "Data"),
        ("Unsupported Safety", "Berberine can be safely administered at any mega-dose without monitoring", None, None)
    ]

    for label, text, cit, passg in adversarial_claims:
        print(f"\n  [Adversarial Check: {label}]")
        print(f"  Assertion: '{text}'")
        c_list = [cit] if cit else []
        p_map = {cit.identifier: passg} if cit and passg else {}
        pkt = TruthAndSafetyFirewall.verify_answer(text, c_list, p_map)
        first_clm = pkt.claims[0]
        print(f"  -> Verdict: {pkt.verdict.value} | Claim Status: {first_clm.claim_status.value}")
        print(f"  -> Reasons: {first_clm.reasons}")
        if first_clm.recommended_rewrite:
            print(f"  -> Recommended Safe Rewrite: '{first_clm.recommended_rewrite}'")

    # -------------------------------------------------------------
    # DEMO 3: Retraction Propagation Impact Analysis
    # -------------------------------------------------------------
    print("\n[DEMO 3] Retraction Propagation & Cascading Impact Analysis")
    impact = TruthAndSafetyFirewall.run_retraction_impact_analysis("PMID:18442638")
    print(f"  -> Retracted Identifier: {impact['retracted_identifier']}")
    print(f"  -> Cascading Action: {impact['action_taken']}")
    print(f"  -> Affected Active Claims Count: {impact['affected_claims_count']}")

    # -------------------------------------------------------------
    # DEMO 4: Cross-System Equivalence Firewall
    # -------------------------------------------------------------
    print("\n[DEMO 4] Cross-System Equivalence Firewall")
    cross_claim = "Unani Mizaj is equivalent to insulin resistance syndrome."
    ok, reason, rewrite = CausalityAndLanguageFirewall.check_cross_system_equivalence(cross_claim)
    print(f"  -> Raw Claim: '{cross_claim}'")
    print(f"  -> Allowed: {ok} | Reason: {reason}")
    print(f"  -> Compliant Qualified Rewrite: '{rewrite}'")

    print("\n" + "=" * 80)
    print(" ALL TRUTH & SAFETY FIREWALL DEMONSTRATIONS COMPLETED SUCCESSFULLY! ")
    print("=" * 80)


if __name__ == "__main__":
    run_truth_firewall_showcase()
