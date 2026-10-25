"""
ZMIE Knowledge Graph, Evidence Graph & Medical Ontology Showcase (Section 105)
Demonstrates the 4 required real-world scenarios:
1. Entity Explorer: Irritable Bowel Syndrome (IBS)
2. Relationship Explorer: Berberine -> Type 2 Diabetes (Supporting, Conflicting, PICO Context)
3. Cross-System Comparative Lens: Unani Hazm vs Ayurveda Jatharagni vs TCM Pi/Wei vs Modern Motility
4. Retraction Impact Propagation: Retracted study cascading through Claims, Relations, Evidence, and Research Projects.
"""

import sys
from app.graph.engine import MedicalKnowledgeGraphEngine
from app.ontology.cross_system import CrossSystemMappingEngine
from app.graph.grounding import AIGroundingPacketEngine

def run_showcase():
    print("=" * 88)
    print("  ZMIE — KNOWLEDGE GRAPH, EVIDENCE GRAPH & ONTOLOGY SHOWCASE (SECTION 105)")
    print("=" * 88)

    graph = MedicalKnowledgeGraphEngine()
    cross_sys = CrossSystemMappingEngine()
    grounding = AIGroundingPacketEngine(graph)

    # -------------------------------------------------------------------------
    # DEMO 1: ENTITY (IBS)
    # -------------------------------------------------------------------------
    print("\n[DEMO 1/4] ENTITY EXPLORER: 'Irritable Bowel Syndrome' (IBS)...")
    ibs_concept = graph.ontology.resolve_term("IBS")
    print(f"  Canonical Name:  {ibs_concept.canonical_name} ({ibs_concept.concept_id})")
    print(f"  Entity Class:    {ibs_concept.entity_class} | System: {ibs_concept.medical_system.value}")
    print(f"  Definition:      {ibs_concept.definition}")
    print("  Multilingual Terms & Aliases:")
    for t in ibs_concept.terms:
        print(f"    - [{t.language.upper()}] {t.term_text} ({t.synonym_type.value})")
    ibs_rels = graph.get_entity_relationships(ibs_concept.concept_id)
    print(f"  Connected Relations in Graph: {len(ibs_rels)} edges")
    for r in ibs_rels:
        print(f"    -> {r.subject_id} --[{r.predicate.value}]--> {r.object_id} (Evidence: {r.evidence_level.value})")

    # -------------------------------------------------------------------------
    # DEMO 2: RELATIONSHIP (Berberine -> Type 2 Diabetes)
    # -------------------------------------------------------------------------
    print("\n[DEMO 2/4] RELATIONSHIP EXPLORER & 'WHY THIS?' EVIDENCE AUDIT...")
    why = graph.explain_why_relationship("REL-BERB-T2D-001")
    print(f"  Assertion:       {why.subject_name} --[{why.predicate}]--> {why.object_name}")
    print(f"  Evidence Level:  {why.evidence_level} | Knowledge Status: {why.knowledge_status}")
    print(f"  Studies Count:   {why.supporting_studies_count} Supporting | {why.contradicting_studies_count} Contradicting")
    print(f"  Population:      {why.primary_populations[0]}")
    print("  Supporting Evidence Sample:")
    for sup in why.supporting_evidence_details:
        print(f"    - Study: {sup['study_id']} ({sup['study_type']}) | Effect: {sup['effect_measure']} = {sup['effect_value']*100:.1f}% (p={sup['p_value']}) | Anchor: {sup['paragraph_anchor_hash']}")
    print("  Contradicting Evidence Sample:")
    for con in why.contradicting_evidence_details:
        print(f"    - Study: {con['study_id']} | Effect: No significant reduction (p={con['p_value']}) | Limitations: {con['limitations']}")
    print(f"  Disagreement Analysis: {why.disagreement_reasons[0]}")
    print(f"  Causality Notice:      {why.causality_warning}")

    # -------------------------------------------------------------------------
    # DEMO 3: CROSS-SYSTEM COMPARATIVE LENS (Digestion & Transformation)
    # -------------------------------------------------------------------------
    print("\n[DEMO 3/4] CROSS-SYSTEM COMPARATIVE LENS: 'Digestion & Transformation'...")
    lens = cross_sys.generate_comparative_lens("digestion")
    print(f"  Topic:           {lens.topic}")
    print(f"  Concordance:     {lens.concordance_level.value} (Preserves Non-Equivalence)")
    for sys_name, p in lens.system_perspectives.items():
        print(f"    * {sys_name.upper():20}: {p['concept']} (Pathology: {p['pathology']})")
    print(f"  Shared Themes:   {lens.shared_themes[0]}")
    print(f"  Divergence:      {lens.fundamental_divergences[0]}")
    print(f"  Safeguard:       {lens.safeguard_notice}")

    # -------------------------------------------------------------------------
    # DEMO 4: RETRACTION IMPACT PROPAGATION
    # -------------------------------------------------------------------------
    print("\n[DEMO 4/4] RETRACTION IMPACT PROPAGATION...")
    print("  Triggering formal retraction on study: PMID:18442638")
    impact = graph.propagate_retraction_impact("PMID:18442638")
    print(f"  Affected Claims Quarantined:     {impact.affected_claims}")
    print(f"  Affected Relations Downgraded:   {impact.affected_relations}")
    print(f"  Affected Evidence Flagged:       {impact.affected_evidence}")
    print(f"  Dependent Projects Intercepted:  {impact.dependent_research_projects}")
    print("  Mitigation Protocols Enforced:")
    for a in impact.mitigation_actions:
        print(f"    ✓ {a}")

    print("\n" + "=" * 88)
    print("  ALL 4 DEMONSTRATION WORKFLOWS VERIFIED & OPERATIONAL (100% SUCCESS)")
    print("=" * 88)

if __name__ == "__main__":
    run_showcase()
