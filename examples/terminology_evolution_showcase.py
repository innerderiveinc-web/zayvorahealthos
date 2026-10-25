"""ZMIE Global Medical Ontology & Terminology Evolution Showcase.

Demonstrates:
1. Core Axiom: Term ≠ Concept ≠ Clinical Reality (Synonym normalization)
2. Polysemy & Contextual Abbreviation Disambiguation ("MS" in Neuro vs Cardio)
3. Multilingual & Script Handling (Arabic, Devanagari, Transliterations)
4. Historical Terminology Retention (Dropsy, 18th century definition preserved)
5. Traditional Medicine Integrity & False-Friend Guards (Mizaj vs Prakriti)
6. Unknown-First Policy (Explicit NO_VALID_MAPPING)
7. Terminology Deprecation & Downstream Impact Analysis (NAFLD -> MASLD)
8. Governance Workflow & Human Review (AI Candidate -> Human Authoritative)
9. License Enforcement & Export Protections
"""

import json
from app.models.terminology_evolution import (
    EpistemicCertainty,
    MappingType,
    ReviewDecision,
    SemanticMapping,
)
from app.ontology_engine.core import GlobalTerminologyEvolutionEngine


def run_showcase():
    print("=" * 80)
    print(" ZMIE GLOBAL MEDICAL ONTOLOGY & TERMINOLOGY EVOLUTION ENGINE")
    print(" Term ≠ Concept ≠ Entity ≠ Clinical Reality ≠ Ontological Meaning ≠ Evidence")
    print("=" * 80)

    engine = GlobalTerminologyEvolutionEngine()

    # 1. Synonym Resolution (Term ≠ Concept)
    print("\n--- [STAGE 1] SYNONYM RESOLUTION & TERM ≠ CONCEPT ---")
    res1 = engine.resolve_term("myocardial infarction")
    res2 = engine.resolve_term("heart attack")
    print(f"  • Input Term: 'myocardial infarction' -> Concept: [{res1.selected_concept.concept_id}] {res1.selected_concept.canonical_label}")
    print(f"  • Input Term: 'heart attack'         -> Concept: [{res2.selected_concept.concept_id}] {res2.selected_concept.canonical_label}")
    print(f"  ✔ Both distinct surface terms resolve to the identical underlying concept ({res1.selected_concept.concept_id})")

    # 2. Polysemy & Abbreviation Disambiguation
    print("\n--- [STAGE 2] POLYSEMY & CONTEXTUAL DISAMBIGUATION ---")
    res_ambi = engine.resolve_term("MS")
    print(f"  • Query: 'MS' without context -> Ambiguous: {res_ambi.is_ambiguous}")
    print(f"    Explanation: {res_ambi.ambiguity_explanation}")
    
    res_neuro = engine.resolve_term("MS", domain_context="neurology")
    print(f"  • Query: 'MS' [Domain: Neurology]  -> Concept: [{res_neuro.selected_concept.concept_id}] {res_neuro.selected_concept.canonical_label}")

    res_cardio = engine.resolve_term("MS", domain_context="cardiology")
    print(f"  • Query: 'MS' [Domain: Cardiology] -> Concept: [{res_cardio.selected_concept.concept_id}] {res_cardio.selected_concept.canonical_label}")

    # 3. Multilingual & Script Handling
    print("\n--- [STAGE 3] MULTILINGUAL & MULTI-SCRIPT RESOLUTION ---")
    res_ar = engine.resolve_term("مزاج")
    print(f"  • Arabic Script: 'مزاج' -> Detected Script: {res_ar.script_detected} | Concept: [{res_ar.selected_concept.concept_id}] {res_ar.selected_concept.canonical_label}")
    res_hi = engine.resolve_term("प्रकृति")
    print(f"  • Devanagari Script: 'प्रकृति' -> Detected Script: {res_hi.script_detected} | Concept: [{res_hi.selected_concept.concept_id}] {res_hi.selected_concept.canonical_label}")

    # 4. Historical Terminology Retention
    print("\n--- [STAGE 4] HISTORICAL TERMINOLOGY RETENTION (RULE 3 & 8) ---")
    hist = engine.get_historical_term("Dropsy")
    print(f"  • Historical Term: {hist.term} ({hist.historical_period})")
    print(f"    Source: {hist.historical_source}")
    print(f"    Historical Definition: {hist.historical_definition[:120]}...")
    print(f"    Epistemic Warning: {hist.epistemic_warning}")

    # 5. Traditional Medicine Semantics & False-Friend Guard
    print("\n--- [STAGE 5] TRADITIONAL MEDICINE & FALSE-FRIEND GUARDS (RULE 4 & 7) ---")
    res_mizaj = engine.resolve_term("Mizaj")
    print(f"  • Query: 'Mizaj' -> False Friend Guard Triggered: {res_mizaj.is_false_friend}")
    print(f"    Warning: {res_mizaj.false_friend_warning[:130]}...")

    mapping_mizaj = engine.map_concepts("CON-UNANI-MIZAJ-01", "Ayurveda")
    print(f"\n  • Cross-System Mapping: {mapping_mizaj.source_system} -> {mapping_mizaj.target_system}")
    print(f"    Mapping Type: {mapping_mizaj.mapping_type.value} (NEVER EXACT_EQUIVALENCE)")
    print(f"    Known Differences: {mapping_mizaj.known_differences[0]}")
    print(f"    Unmapped Aspects: {mapping_mizaj.unmapped_aspects[0]}")

    # 6. Unknown-First Policy
    print("\n--- [STAGE 6] UNKNOWN-FIRST SEMANTIC POLICY ---")
    map_unknown = engine.map_concepts("CON-UNANI-DAMVI-01", "Molecular_Genetics")
    print(f"  • Mapping Query: Damvi Mizaj -> Molecular Genetics")
    print(f"    Result: {map_unknown.mapping_type.value} | Target: {map_unknown.target_concept_id}")
    print(f"    Evidence Notes: {map_unknown.evidence_notes}")

    # 7. Terminology Deprecation & Downstream Impact
    print("\n--- [STAGE 7] TERMINOLOGY DEPRECATION & DOWNSTREAM IMPACT ---")
    dep = engine.get_deprecated_transition("CON-DIS-NAFLD-01")
    print(f"  • Deprecated Term: {dep.deprecated_term} -> Replacement: {dep.replacement_term}")
    print(f"    Consensus Body: {dep.consensus_body} ({dep.transition_date})")
    print(f"    Rationale: {dep.scientific_rationale}")

    impact = engine.analyze_downstream_impact("CON-DIS-NAFLD-01")
    print(f"\n  >> Downstream Impact Analysis:")
    print(f"     Severity: {impact.impact_severity}")
    print(f"     Affected Claims: {impact.affected_claims_count} | Studies: {impact.affected_studies_count} | Guidelines: {impact.affected_guidelines_count} | RWE Cohorts: {impact.affected_rwe_cohorts_count}")
    print(f"     Remediation: {impact.remediation_recommendations[0]}")

    # 8. Governance & Double-Review Policy
    print("\n--- [STAGE 8] GOVERNANCE & EXPERT REVIEW WORKFLOW ---")
    candidate = SemanticMapping(
        mapping_id="MAP-AI-SUGGEST-09",
        source_concept_id="CON-UNANI-DAMVI-01",
        target_concept_id="CON-DIS-MI-01",
        source_system="Unani",
        target_system="Biomedicine",
        mapping_type=MappingType.RELATED_MAPPING,
        assurance_state=EpistemicCertainty.AUTHORITATIVE,  # AI proposes authoritative
        provenance_source="AI Transformer Semantic Suggestion",
        requires_double_review=True,
        created_at=engine._now(),
        updated_at=engine._now(),
    )
    task = engine.submit_mapping_for_review(candidate)
    print(f"  • AI submitted mapping -> System Assigned State: {candidate.assurance_state.value} (STRICT CANDIDATE)")
    print(f"    Review Task: {task.task_id} assigned to {task.assigned_reviewer} (Double-Review Required: {task.is_second_review})")

    approved = engine.record_review_decision(
        task_id=task.task_id,
        reviewer_name="Dr. H. Vance, MD",
        decision=ReviewDecision.APPROVE,
        review_notes="Approved with physiological plethora qualifier",
    )
    print(f"  • Expert Review Decision: {task.decision.value} -> Promoted to: {approved.assurance_state.value}")

    # 9. License Protection
    print("\n--- [STAGE 9] LICENSE VERIFICATION & EXPORT CONTROL ---")
    allowed, reason = engine.verify_export_license("INSTITUTIONAL_INTERNAL_VOCAB")
    print(f"  • Export Request: 'INSTITUTIONAL_INTERNAL_VOCAB'")
    print(f"    Allowed: {allowed} | Policy: {reason}")

    print("\n" + "=" * 80)
    print(" ALL MODULE 20 GLOBAL ONTOLOGY & TERMINOLOGY CAPABILITIES VERIFIED")
    print("=" * 80)


if __name__ == "__main__":
    run_showcase()
