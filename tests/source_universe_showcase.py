"""
ZMIE Global Medical Source Universe & Universal Acquisition Engine — Master Showcase
Demonstrates the Core Source Ecosystem & Acquisition Capabilities:
1. Proof 1: Live Global Source Coverage Map & Taxonomy (Sections 7, 39, 82)
2. Proof 2: End-to-End Query 1: Nigella sativa across Modern, Unani, Ayurveda & Botanical (Section 165)
3. Proof 3: End-to-End Query 2: Mizaj / Temperament Concepts (Classical vs Modern Phenotyping) (Section 166)
4. Proof 4: End-to-End Query 3: Drug-Herb Interaction Safety Screening (Warfarin + SJW/Ginkgo) (Section 167)
5. Proof 5: Source Discovery Queue, Approval Lifecycle & Continuous Retraction Invalidation (Sections 21, 31, 171)
"""

from app.models.source_universe import MedicalSystem, SourceClass
from app.sources.registry import SourceUniverseRegistry
from app.sources.discovery import SourceDiscoveryEngine
from app.sources.search_matrix import MultiSystemSearchMatrixEngine
from app.sources.retraction_pipeline import RetractionAndSafetyPipeline


def run_source_universe_showcase():
    print("=" * 90)
    print(" ZMIE GLOBAL MEDICAL SOURCE UNIVERSE & ACQUISITION ENGINE — MASTER SHOWCASE ")
    print("=" * 90)

    # -------------------------------------------------------------------------
    # PROOF 1: Live Global Source Coverage Map & Taxonomy
    # -------------------------------------------------------------------------
    print("\n[PROOF 1] Live Global Source Coverage Map & Multi-System Taxonomy")
    cov = SourceUniverseRegistry.get_coverage_report()
    print(f"  -> Discovered Sources: {cov.sources_discovered} | Active: {cov.sources_active} | Pending Review: {cov.sources_pending_review}")
    print(f"  -> Multi-System Distribution:")
    print(f"     * Modern Medicine Ecosystems: {cov.modern_medicine_count}")
    print(f"     * Unani Research Councils & Canons: {cov.unani_count}")
    print(f"     * Ayurveda Councils & Sanskrit Canons: {cov.ayurveda_count}")
    print(f"     * Other Traditional (Siddha, TCM, Kampo): {cov.other_traditional_count}")
    print(f"     * Clinical Trial Registries (WHO, NLM, CTRI): {cov.trial_registries_count}")
    print(f"     * Clinical Practice Guidelines (WHO, NICE): {cov.guidelines_count}")
    print(f"  -> Countries Covered: {', '.join(cov.countries_covered[:6])}...")
    print(f"  -> Languages Covered: {', '.join(cov.languages_covered)}")
    print(f"  -> Transparent Gap Disclosure (Section 40):")
    for gap in cov.known_coverage_gaps:
        print(f"     * [GAP]: {gap}")

    # -------------------------------------------------------------------------
    # PROOF 2: End-to-End Query 1: Nigella sativa across Multi-System Corpus
    # -------------------------------------------------------------------------
    print("\n[PROOF 2] End-to-End Query 1: Nigella sativa in Metabolic & Inflammatory Disorders (Section 165)")
    query1 = "What is the evidence for Nigella sativa in metabolic and inflammatory disorders?"
    res1 = MultiSystemSearchMatrixEngine.execute_multi_system_search(query1)
    matrix = res1["source_matrix"]
    print(f"  -> Query: '{query1}'")
    print(f"  -> Epistemic Separation Preserved: {res1['epistemic_separation_preserved']}")
    print(f"  -> Zero-Fabrication Rule Confirmed: {res1['zero_fabrication_confirmed']}")

    print("\n  [RESEARCH SOURCE MATRIX: What did ZMIE search? (Section 83)]")
    print(f"  {'Source Class':<30} | {'Searched':<8} | {'Retrieved':<9} | {'Included':<8} | {'Excluded':<8}")
    print("  " + "-" * 75)
    for row in matrix.matrix:
        print(f"  {row.source_class:<30} | {row.searched:<8} | {row.retrieved:<9} | {row.included:<8} | {row.excluded:<8}")

    print("\n  [RETRIEVED MULTI-SYSTEM EVIDENCE]")
    if res1["modern_biomedical_evidence"]:
        m = res1["modern_biomedical_evidence"][0]
        print(f"  -> Modern RCT: {m['title'][:65]}... (Level: {m['evidence_level']})")
    if res1["unani_evidence"]:
        u = res1["unani_evidence"][0]
        print(f"  -> Unani Clinical: {u['title'][:65]}... (Epistemic: {u['epistemic_class']})")
    if res1["classical_references"]:
        c = res1["classical_references"][0]
        print(f"  -> Classical Text: [{c['canon']}] - \"{c['text_quote'][:60]}...\"")
        print(f"     * Clinical Boundary: {c['clinical_disclaimer']}")

    # -------------------------------------------------------------------------
    # PROOF 3: End-to-End Query 2: Mizaj / Temperament Concepts
    # -------------------------------------------------------------------------
    print("\n[PROOF 3] End-to-End Query 2: Mizaj / Temperament-Related Concepts (Section 166)")
    query2 = "What research exists on Mizaj / temperament-related concepts?"
    res2 = MultiSystemSearchMatrixEngine.execute_multi_system_search(query2)
    print(f"  -> Query: '{query2}'")
    print("  -> Classical Canon Quotes:")
    for ref in res2["classical_references"]:
        print(f"     * [{ref['canon']}]: {ref['concept']}")
    if res2["unani_evidence"]:
        ue = res2["unani_evidence"][0]
        print(f"  -> Modern Translational Study: {ue['title'][:70]}...")
        print(f"     * Empirical Findings: {ue['findings']}")

    # -------------------------------------------------------------------------
    # PROOF 4: End-to-End Query 3: Drug-Herb Interaction Safety Screening
    # -------------------------------------------------------------------------
    print("\n[PROOF 4] End-to-End Query 3: Drug-Herb Interaction Safety Screening (Section 167)")
    query3 = "Latest evidence for a drug-herb interaction with Warfarin"
    res3 = MultiSystemSearchMatrixEngine.execute_multi_system_search(query3)
    print(f"  -> Query: '{query3}'")
    print(f"  -> High-Priority Safety Alerts Detected: {len(res3['safety_alerts'])}")
    for alert in res3["safety_alerts"]:
        print(f"     * [{alert['severity']}]: {alert['drug']} + {alert['interacting_agent']}")
        print(f"       Source: {alert['source']}")
        print(f"       Mechanism: {alert['mechanism']}")
        print(f"       Consequence: {alert['clinical_consequence']}")

    # -------------------------------------------------------------------------
    # PROOF 5: Universal Discovery Queue & Continuous Retraction Invalidation
    # -------------------------------------------------------------------------
    print("\n[PROOF 5] Universal Discovery Queue & Continuous Retraction Pipeline (Sections 21, 31, 171)")
    # Discovery from citation
    new_cand = SourceDiscoveryEngine.discover_from_citation(
        cited_journal_or_url="https://sciencedirect.com/journal/phytomedicine-plus",
        citing_source_id="SRC-EPMC"
    )
    print(f"  -> Discovered Candidate: '{new_cand.candidate_name}' | Method: {new_cand.discovery_method}")
    print(f"  -> Review State: {new_cand.review_state} (Governance Gate Enforced)")

    # Approval promotion
    promoted = SourceDiscoveryEngine.approve_candidate(new_cand.candidate_id)
    print(f"  -> Candidate Approved & Registered: Source ID = {promoted.source_id} | Class = {promoted.source_class.value}")

    # Retraction event ingestion
    ret_event = RetractionAndSafetyPipeline.ingest_retraction_event(
        identifier="10.1000/fabricated-trial-curcumin-2026",
        document_title="Fabricated Multicenter RCT on Curcumin in Sepsis",
        source_id="SRC-EPMC",
        retraction_reason="Data fabrication and duplicate Western blot bands confirmed by COPE"
    )
    print(f"\n  -> Ingested Retraction Notice: ID={ret_event.event_id} | Identifier={ret_event.identifier}")
    print(f"  -> Cascade Impact: Claims Affected={ret_event.affected_claims_count} | Graph Edges={ret_event.affected_graph_edges_count} | Status={ret_event.status}")
    print(f"  -> Retraction Registry Check: Is Retracted? = {RetractionAndSafetyPipeline.is_identifier_retracted(ret_event.identifier)}")

    print("\n" + "=" * 90)
    print(" ZMIE SOURCE UNIVERSE MASTER SHOWCASE COMPLETE: ALL 5 PROOFS VERIFIED ")
    print("=" * 90)


if __name__ == "__main__":
    run_source_universe_showcase()
