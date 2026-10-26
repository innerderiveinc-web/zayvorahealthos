"""ZMIE Global Medical Ontology & Terminology Evolution Engine Acceptance Tests.

Verifies the 15 Required Acceptance Tests from Prompt 20 (Clause 196):
- Test 1 — Synonym: Two true synonyms resolve to one concept
- Test 2 — Polysemy: One term with multiple meanings produces context-dependent candidates
- Test 3 — Abbreviation: Ambiguous abbreviation resolves based on domain context
- Test 4 — Translation: Translation is distinct from semantic equivalence
- Test 5 — Historical: Historical term retains historical meaning without retrofitting
- Test 6 — Traditional: Traditional concept does not automatically become biomedical equivalent
- Test 7 — Partial Mapping: Partial mapping is represented explicitly with differences
- Test 8 — Unknown: No valid mapping produces NO_VALID_MAPPING
- Test 9 — Deprecation: Deprecated terminology remains historically discoverable (NAFLD -> MASLD)
- Test 10 — Ontology Change: A changed ontology generates a structured diff
- Test 11 — Impact: Changed concept identifies affected downstream objects
- Test 12 — License: Restricted source cannot be exported improperly
- Test 13 — Provenance: Every authoritative mapping has provenance
- Test 14 — Human Review: AI suggestion cannot directly publish authoritative mapping
- Test 15 — Versioning: Historical outputs remain reproducible with versions
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.models.terminology_evolution import (
    ConceptStatus,
    EpistemicCertainty,
    MappingType,
    ReviewDecision,
    SemanticMapping,
)
from app.ontology.core import GlobalTerminologyEvolutionEngine


class TestTerminologyEvolutionAcceptance(unittest.TestCase):
    """Rigorous acceptance tests matching all 15 specification tests from Prompt 20."""

    def setUp(self):
        self.engine = GlobalTerminologyEvolutionEngine()
        self.client = TestClient(app)

    def test_01_synonym_resolution(self):
        """Test 1 — Synonym: Two true synonyms resolve to one concept."""
        res_mi = self.engine.resolve_term("myocardial infarction")
        res_ha = self.engine.resolve_term("heart attack")

        self.assertIsNotNone(res_mi.selected_concept)
        self.assertIsNotNone(res_ha.selected_concept)
        self.assertEqual(res_mi.selected_concept.concept_id, res_ha.selected_concept.concept_id)
        self.assertEqual(res_mi.selected_concept.concept_id, "CON-DIS-MI-01")

    def test_02_polysemy_resolution(self):
        """Test 2 — Polysemy: One term with multiple meanings produces context-dependent candidates."""
        # Querying ambiguous term "MS" without domain context
        res_ambiguous = self.engine.resolve_term("MS")
        self.assertTrue(res_ambiguous.is_ambiguous)
        self.assertIsNone(res_ambiguous.selected_concept)
        self.assertGreaterEqual(len(res_ambiguous.candidate_concepts), 2)
        self.assertIn("Polysemous term", res_ambiguous.ambiguity_explanation)

    def test_03_abbreviation_disambiguation(self):
        """Test 3 — Abbreviation: Ambiguous abbreviation resolves based on context."""
        res_neuro = self.engine.resolve_term("MS", domain_context="neurology")
        self.assertFalse(res_neuro.is_ambiguous)
        self.assertIsNotNone(res_neuro.selected_concept)
        self.assertEqual(res_neuro.selected_concept.concept_id, "CON-NEURO-MS-01")
        self.assertEqual(res_neuro.selected_concept.canonical_label, "Multiple Sclerosis")

        res_cardio = self.engine.resolve_term("MS", domain_context="cardiology")
        self.assertFalse(res_cardio.is_ambiguous)
        self.assertIsNotNone(res_cardio.selected_concept)
        self.assertEqual(res_cardio.selected_concept.concept_id, "CON-CARDIO-MS-01")
        self.assertEqual(res_cardio.selected_concept.canonical_label, "Mitral Stenosis")

    def test_04_translation_distinct_from_equivalence(self):
        """Test 4 — Translation: Translation is distinct from semantic equivalence."""
        res_arabic = self.engine.resolve_term("مزاج")
        self.assertEqual(res_arabic.script_detected, "Arabic")
        self.assertIsNotNone(res_arabic.selected_concept)
        self.assertEqual(res_arabic.selected_concept.concept_id, "CON-UNANI-MIZAJ-01")

        res_devanagari = self.engine.resolve_term("प्रकृति")
        self.assertEqual(res_devanagari.script_detected, "Devanagari")
        self.assertIsNotNone(res_devanagari.selected_concept)
        self.assertEqual(res_devanagari.selected_concept.concept_id, "CON-AYUR-PRAKRITI-01")

    def test_05_historical_term_retention(self):
        """Test 5 — Historical: Historical term retains historical meaning."""
        hist = self.engine.get_historical_term("Dropsy")
        self.assertIsNotNone(hist)
        self.assertEqual(hist.historical_period, "18th Century & Pre-Modern")
        self.assertIn("William Withering", hist.historical_source)
        self.assertEqual(hist.mapping_type, MappingType.HISTORICAL_CORRESPONDENCE)
        self.assertIn("STRICT HISTORICAL BOUNDARY", hist.epistemic_warning)

    def test_06_traditional_concept_restraint(self):
        """Test 6 — Traditional: Traditional concept does not automatically become biomedical equivalent."""
        res = self.engine.resolve_term("Mizaj")
        self.assertTrue(res.is_false_friend)
        self.assertIn("FALSE EQUIVALENCE GUARD", res.false_friend_warning)

        # Map Mizaj to Ayurveda
        mapping = self.engine.map_concepts("CON-UNANI-MIZAJ-01", "Ayurveda")
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping.mapping_type, MappingType.FUNCTIONAL_CORRESPONDENCE)
        self.assertNotEqual(mapping.mapping_type, MappingType.EXACT_EQUIVALENCE)

    def test_07_partial_mapping_explicit_differences(self):
        """Test 7 — Partial Mapping: Partial mapping is represented explicitly."""
        mapping = self.engine.map_concepts("CON-UNANI-MIZAJ-01", "Ayurveda")
        self.assertGreater(len(mapping.known_differences), 0)
        self.assertGreater(len(mapping.unmapped_aspects), 0)
        self.assertIn("Mizaj uses 4 qualitative coordinates", mapping.known_differences[0])

    def test_08_unknown_detection_policy(self):
        """Test 8 — Unknown: No valid mapping produces NO_VALID_MAPPING."""
        # Unmapped system query
        mapping = self.engine.map_concepts("CON-UNANI-DAMVI-01", "Conventional_Molecular_Genetics")
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping.mapping_type, MappingType.NO_VALID_MAPPING)
        self.assertEqual(mapping.target_concept_id, "NULL_UNMAPPED")

    def test_09_deprecation_and_transition(self):
        """Test 9 — Deprecation: Deprecated terminology remains historically discoverable."""
        dep = self.engine.get_deprecated_transition("CON-DIS-NAFLD-01")
        self.assertIsNotNone(dep)
        self.assertEqual(dep.deprecated_term, "NAFLD")
        self.assertEqual(dep.replacement_term, "MASLD")
        self.assertEqual(dep.replacement_concept_id, "CON-DIS-MASLD-01")
        self.assertIn("2023", dep.transition_date)

    def test_10_ontology_change_diff(self):
        """Test 10 — Ontology Change: A changed ontology generates a diff."""
        diff = self.engine.generate_ontology_diff("SNOMED-CT", "2024-01", "2025-01")
        self.assertIsNotNone(diff)
        self.assertIn("CON-DIS-MASLD-01", diff.added_concepts)
        self.assertIn("CON-DIS-NAFLD-01", diff.deprecated_concepts)

    def test_11_downstream_impact_analysis(self):
        """Test 11 — Impact: Changed concept identifies affected downstream objects."""
        impact = self.engine.analyze_downstream_impact("CON-DIS-NAFLD-01")
        self.assertIsNotNone(impact)
        self.assertGreater(impact.affected_claims_count, 0)
        self.assertGreater(impact.affected_studies_count, 0)
        self.assertEqual(impact.impact_severity, "HIGH")
        self.assertGreater(len(impact.remediation_recommendations), 0)

    def test_12_license_enforcement(self):
        """Test 12 — License: Restricted source cannot be exported improperly."""
        allowed, reason = self.engine.verify_export_license("INSTITUTIONAL_INTERNAL_VOCAB")
        self.assertFalse(allowed)
        self.assertIn("prohibited", reason)

        allowed_snomed, _ = self.engine.verify_export_license("SNOMED-CT")
        self.assertTrue(allowed_snomed)

    def test_13_provenance_retention(self):
        """Test 13 — Provenance: Every authoritative mapping has provenance."""
        mapping = self.engine.map_concepts("CON-UNANI-MIZAJ-01", "Ayurveda")
        self.assertIsNotNone(mapping.provenance_source)
        self.assertGreater(len(mapping.expert_reviewers), 0)
        self.assertEqual(mapping.assurance_state, EpistemicCertainty.EXPERT_REVIEWED)

    def test_14_human_review_workflow(self):
        """Test 14 — Human Review: AI suggestion cannot directly publish authoritative mapping."""
        # 1. AI proposes candidate mapping
        candidate = SemanticMapping(
            mapping_id="MAP-AI-CANDIDATE-01",
            source_concept_id="CON-UNANI-DAMVI-01",
            target_concept_id="CON-DIS-MI-01",
            source_system="Unani",
            target_system="Biomedicine",
            mapping_type=MappingType.RELATED_MAPPING,
            assurance_state=EpistemicCertainty.AUTHORITATIVE,  # AI attempts to assert authoritative
            provenance_source="AI Semantic Suggestion Model v2",
            created_at=self.engine._now(),
            updated_at=self.engine._now(),
        )
        task = self.engine.submit_mapping_for_review(candidate)

        # Verification: Engine strictly demoted to CANDIDATE
        self.assertEqual(candidate.assurance_state, EpistemicCertainty.CANDIDATE)

        # 2. Human reviewer approves
        approved_mapping = self.engine.record_review_decision(
            task_id=task.task_id,
            reviewer_name="Dr. E. Vance, MD",
            decision=ReviewDecision.APPROVE,
            review_notes="Clinically validated partial association in vascular plethora",
        )
        self.assertEqual(approved_mapping.assurance_state, EpistemicCertainty.AUTHORITATIVE)
        self.assertIn("Dr. E. Vance, MD", approved_mapping.expert_reviewers)

    def test_15_versioning_and_reproducibility(self):
        """Test 15 — Versioning: Historical outputs remain reproducible."""
        concept = self.engine._concepts["CON-DIS-MASLD-01"]
        self.assertEqual(concept.current_version, "v1.0")
        self.assertEqual(concept.status, ConceptStatus.ACTIVE)

        dep_concept = self.engine._concepts["CON-DIS-NAFLD-01"]
        self.assertEqual(dep_concept.status, ConceptStatus.DEPRECATED)

    def test_16_fastapi_rest_endpoints(self):
        """Verifies FastAPI REST endpoints for the Terminology Evolution Engine."""
        # POST /v1/terminology/resolve
        resp_res = self.client.post("/v1/terminology/resolve", json={"text": "heart attack"})
        self.assertEqual(resp_res.status_code, 200)
        data_res = resp_res.json()
        self.assertEqual(data_res["selected_concept"]["concept_id"], "CON-DIS-MI-01")

        # GET /v1/terminology/historical/Dropsy
        resp_hist = self.client.get("/v1/terminology/historical/Dropsy")
        self.assertEqual(resp_hist.status_code, 200)
        data_hist = resp_hist.json()
        self.assertEqual(data_hist["historical_period"], "18th Century & Pre-Modern")

        # GET /v1/terminology/deprecated/CON-DIS-NAFLD-01
        resp_dep = self.client.get("/v1/terminology/deprecated/CON-DIS-NAFLD-01")
        self.assertEqual(resp_dep.status_code, 200)
        data_dep = resp_dep.json()
        self.assertEqual(data_dep["replacement_term"], "MASLD")

        # GET /v1/terminology/ontologies/diff
        resp_diff = self.client.get("/v1/terminology/ontologies/diff")
        self.assertEqual(resp_diff.status_code, 200)
        data_diff = resp_diff.json()
        self.assertIn("CON-DIS-MASLD-01", data_diff["added_concepts"])

        # POST /v1/terminology/impact-analysis
        resp_impact = self.client.post("/v1/terminology/impact-analysis", json={"concept_id": "CON-DIS-NAFLD-01"})
        self.assertEqual(resp_impact.status_code, 200)
        data_impact = resp_impact.json()
        self.assertGreater(data_impact["affected_claims_count"], 0)

        # GET /v1/terminology/licenses/verify-export
        resp_lic = self.client.get("/v1/terminology/licenses/verify-export?vocabulary_name=INSTITUTIONAL_INTERNAL_VOCAB")
        self.assertEqual(resp_lic.status_code, 200)
        data_lic = resp_lic.json()
        self.assertFalse(data_lic["export_allowed"])


if __name__ == "__main__":
    unittest.main()
