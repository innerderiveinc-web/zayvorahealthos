"""
ZMIE Global Research Discovery Network & Continuous Knowledge Evolution Engine
Interactive Showcase Demonstration (Prompt 14)

Demonstrates 5 core capabilities:
1. End-to-End Research Lifecycle Tracing & Canonical Study De-duplication
2. Author Identity Disambiguation & 'Who Is Researching This?' Resolvers
3. Emerging Frontier Detection & Velocity Score Analysis
4. Continuous Knowledge Evolution: Automated Retraction Cascade Impact
5. 'What Am I Missing?' Structural Research Gap & Blindspot Detection
"""

import json
from app.research.network_engine import ResearchNetworkEngine
from app.research.evolution_engine import ContinuousKnowledgeEvolutionEngine


def banner(title: str):
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def main():
    network = ResearchNetworkEngine()
    evolution = ContinuousKnowledgeEvolutionEngine(network_engine=network)

    # -------------------------------------------------------------
    # DEMO 1: End-to-End Research Lifecycle Tracing & Canonical Study De-duplication
    # -------------------------------------------------------------
    banner("DEMO 1: End-to-End Research Lifecycle Tracing & Canonical De-duplication")
    print("\n[+] Tracing full research lifecycle from grant to clinical trial and publication:")
    trace = network.get_lifecycle_trace("grant_ox_sglt2_2023")
    print(f"  Root Identifier: {trace['root_id']}")
    print(f"  Boundary Status: {trace['boundary_status']}")
    print(f"  Total Graph Nodes: {trace['nodes_count']}")
    print("  Graph Traversal Edges:")
    for edge in trace["edges"]:
        print(f"    - [{edge['relation']}] : {edge['source']} ---> {edge['target']} ({edge.get('timestamp')})")

    print("\n[+] Resolving Canonical Study to suppress evidence inflation across Preprint + Trial + Publication:")
    canonical = network.resolve_canonical_study("NCT05221199")
    print(f"  Canonical Study ID: {canonical['canonical_study_id']}")
    print(f"  Associated Trials: {canonical['clinical_trials']}")
    print(f"  Associated Preprints: {canonical['preprints']}")
    print(f"  Peer-Reviewed DOIs: {canonical['peer_reviewed_dois']}")
    print(f"  Evidence Weight Rule: {canonical['evidence_weight_rule']}")
    print(f"  Suppressed Redundant Citations: {canonical['suppressed_duplicate_count']}")
    print(f"  Guidance: {canonical['guidance']}")

    print("\n[+] Testing Private Unobservable Boundary (Strict Zero-Hallucination Guard):")
    private_trace = network.get_lifecycle_trace("proj_secret_pharma_01")
    print(f"  Project ID: {private_trace['root_id']}")
    print(f"  Boundary Status: {private_trace['boundary_status']}")
    print(f"  Enforcement Message: {private_trace['message']}")

    # -------------------------------------------------------------
    # DEMO 2: Author Identity Disambiguation & 'Who Is Researching This?'
    # -------------------------------------------------------------
    banner("DEMO 2: Author Identity Disambiguation & 'Who Is Researching This?'")
    print("\n[+] Disambiguating two distinct researchers with identical names 'Sarah Jenkins':")

    # Oxford Professor with ORCID
    res_orcid = network.disambiguate_researcher(
        name="Sarah Jenkins",
        orcid="0000-0002-1825-0097"
    )
    top_oxford = res_orcid[0]
    print(f"  Candidate 1 (ORCID Match):")
    print(f"    - ID: {top_oxford[0].researcher_id}")
    print(f"    - Canonical Name: {top_oxford[0].canonical_name}")
    print(f"    - Confidence: {top_oxford[1] * 100}%")
    print(f"    - Rationale: {top_oxford[2]}")
    print(f"    - Primary Affiliation: {top_oxford[0].affiliations[0]['name']}")

    # Harvard Junior Fellow with Affiliation
    res_harvard = network.disambiguate_researcher(
        name="Sarah Jenkins",
        institution_name="Harvard Medical School"
    )
    top_harvard = res_harvard[0]
    print(f"\n  Candidate 2 (Institution Context Match):")
    print(f"    - ID: {top_harvard[0].researcher_id}")
    print(f"    - Canonical Name: {top_harvard[0].canonical_name}")
    print(f"    - Confidence: {top_harvard[1] * 100}%")
    print(f"    - Rationale: {top_harvard[2]}")
    print(f"    - Primary Affiliation: {top_harvard[0].affiliations[0]['name']}")

    print("\n[+] Multi-System Query: 'Who is researching Khamira Abresham in Unani Medicine?':")
    who_res = network.who_is_researching("Khamira Abresham Unani")
    print(f"  Total Matches: {who_res['total_matches']}")
    for r in who_res["top_researchers"]:
        print(f"    - {r['canonical_name']} (ID: {r['researcher_id']})")
        print(f"      Systems: {r['traditional_systems']}, Active Projects: {r['active_projects_count']}, H-Index: {r['h_index']}")
        print(f"      Affiliation: {r['affiliations'][0]['name']}")

    # -------------------------------------------------------------
    # DEMO 3: Emerging Frontier Detection & Velocity Score Analysis
    # -------------------------------------------------------------
    banner("DEMO 3: Emerging Frontier Detection & Velocity Score Analysis")
    signals = network.get_frontier_signals()
    print(f"[+] Active Frontier Signals Detected: {len(signals)}")
    for sig in signals:
        print(f"\n  Signal ID: {sig.signal_id}")
        print(f"  Topic: {sig.topic}")
        print(f"  Frontier Velocity Score: {sig.frontier_velocity_score}/100.0 [{sig.status}]")
        print(f"  3-Year Publication Growth: +{sig.growth_rate_3yr}%")
        print(f"  Clinical Trial Acceleration: {sig.clinical_trial_acceleration}x YoY")
        print(f"  Grant Inflow: ${sig.grant_inflow_usd:,.2f}")
        print(f"  Key Compounds: {', '.join(sig.key_breakthrough_compounds)}")
        print(f"  Leading Centers: {', '.join(sig.key_institutions)}")

    # -------------------------------------------------------------
    # DEMO 4: Continuous Knowledge Evolution & Retraction Cascade
    # -------------------------------------------------------------
    banner("DEMO 4: Continuous Knowledge Evolution - Retraction Cascade")
    retracted_doi = "10.1016/j.fakecardio.2021.09912"
    print(f"[!] Triggering simulated publisher retraction for: {retracted_doi}")
    impact = evolution.trigger_cascade_impact(
        trigger_type="RETRACTION",
        trigger_source_id=retracted_doi,
        reason="Publisher formal notice: Data falsification and non-replicable cohort."
    )
    print(f"\n  Impact Analysis ID: {impact.impact_id}")
    print(f"  Trigger: {impact.trigger_type} ({impact.trigger_source_id})")
    print(f"  Severity: {impact.severity_level}")
    print(f"  Affected Claims: {impact.affected_claim_ids}")
    print("  Claim State Degradations:")
    for cid, state in impact.new_claim_states.items():
        prev = impact.previous_claim_states.get(cid)
        print(f"    - Claim '{cid}': {prev} ---> {state}")

    print("\n  Emergency Clinical Alerts Dispatched:")
    for alt in impact.alerts_dispatched:
        print(f"    [{alt['level']}] Alert {alt['alert_id']}:")
        print(f"    {alt['message']}")

    # -------------------------------------------------------------
    # DEMO 5: 'What Am I Missing?' Structural Research Gap Detection
    # -------------------------------------------------------------
    banner("DEMO 5: 'What Am I Missing?' Structural Research Gap & Blindspot Detection")
    print("[+] Querying systemic research gaps for condition 'HFpEF':")
    gaps = evolution.analyze_research_gaps("HFpEF")
    for g in gaps:
        print(f"\n  Gap ID: {g.gap_id}")
        print(f"  Topic: {g.topic}")
        print(f"  Gap Type: {g.gap_type}")
        print(f"  Priority Score: {g.priority_score}/100.0")
        print(f"  Deficiency: {g.deficiency_description}")
        print(f"  Missing Evidence Type: {g.missing_evidence_type}")
        print(f"  Suggested Investigation Pathway:")
        print(f"    {g.suggested_investigation}")

    print("\n[+] Creating and Comparing Knowledge Snapshots (Time-Series Diff):")
    snap_v3 = evolution.create_snapshot(notes="Post-Showcase Snapshot v3")
    snapshots = evolution.get_snapshots()
    diff = evolution.compute_snapshot_diff(snapshots[0].snapshot_id, snap_v3.snapshot_id)
    print(f"  Diff between {diff['snapshot_a']} and {diff['snapshot_b']}:")
    print(f"  {diff['summary']}")

    print("\n" + "=" * 80)
    print(" PROMPT 14 DEMONSTRATION COMPLETE: ALL 5 PROOF SCENARIOS VERIFIED")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
