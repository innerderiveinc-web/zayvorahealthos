"""
ZMIE Knowledge Graph, Evidence Graph & Medical Ontology Acceptance Suite
Validates the full semantic intelligence core:
1. Concept lifecycle, hierarchy, synonyms & merge/split governance
2. Cross-system epistemic mapping & false equivalence safeguards
3. First-class Unani and Ayurveda domain models
4. Evidence Ladder E0-E6 & rich edge qualifiers
5. Contradiction preservation & disagreement analysis
6. "Why this relationship exists?" evidence explanation
7. "What am I missing?" gap engine
8. Claim Trace reverse provenance
9. Multi-hop traversal & causality protection
10. Retraction impact propagation & AI grounding firewall
"""

import sys
import unittest
from datetime import datetime

from app.models.graph import (
    CanonicalConcept, MedicalTerm, ConceptLifecycleStatus,
    SynonymType, ControlledPredicate, EvidenceLadder, EvidenceStatus,
    KnowledgeStatus, CrossSystemMappingType, InferenceType
)
from app.models.claim import MedicalSystem, StudyDesign, PICOContext
from app.ontology.manager import OntologyManager
from app.ontology.cross_system import CrossSystemMappingEngine
from app.ontology.unani import MizajClassification, UnaniDegree, UnaniMizajEntity
from app.ontology.ayurveda import DoshaType, AgniState, AyurvedicRasa, AyurvedicVirya
from app.graph.engine import MedicalKnowledgeGraphEngine
from app.graph.grounding import AIGroundingPacketEngine, GraphSafetyFirewall


class TestGraphOntologyAcceptance(unittest.TestCase):

    def setUp(self):
        self.ontology_mgr = OntologyManager()
        self.cross_sys_engine = CrossSystemMappingEngine()
        self.graph_engine = MedicalKnowledgeGraphEngine(self.ontology_mgr)
        self.grounding_engine = AIGroundingPacketEngine(self.graph_engine)

    def test_01_ontology_lifecycle_and_multilingual_synonyms(self):
        """Verifies concept registration, multilingual aliases, and merge/split governance."""
        # 1. Resolve terms
        c_ibs = self.ontology_mgr.resolve_term("IBS")
        self.assertIsNotNone(c_ibs)
        self.assertEqual(c_ibs.canonical_name, "Irritable Bowel Syndrome")
        self.assertEqual(c_ibs.entity_class, "Condition")

        # Multilingual alias check
        arabic_term = [t for t in c_ibs.terms if t.language == "ar"][0]
        self.assertIn("القولون العصبي", arabic_term.term_text)

        # 2. Concept Merge Governance (Section 33)
        temp_concept = CanonicalConcept(
            concept_id="CON-TEMP-001",
            canonical_name="Colonic Neurosis",
            medical_system=MedicalSystem.MODERN,
            entity_class="Condition",
            definition="Obsolete terminology for functional bowel distress.",
            terms=[MedicalTerm(term_id="TRM-99", concept_id="CON-TEMP-001", term_text="Colonic Neurosis", language="en", script="Latin")]
        )
        self.ontology_mgr.register_concept(temp_concept)
        survivor = self.ontology_mgr.merge_concepts(
            survivor_id="CON-MOD-IBS-001",
            retired_id="CON-TEMP-001",
            rationale="Identical functional disease entity; obsolete 1950s terminology",
            reviewer="HAKEEM-DR-ALVI"
        )
        self.assertEqual(self.ontology_mgr.get_concept("CON-TEMP-001").lifecycle_status, ConceptLifecycleStatus.MERGED)
        # Resolved merged term points to survivor
        self.assertEqual(self.ontology_mgr.resolve_term("Colonic Neurosis").concept_id, "CON-MOD-IBS-001")

    def test_02_cross_system_mapping_and_false_equivalence_safeguard(self):
        """Validates that functional analogies are NEVER falsely promoted to exact equivalences."""
        # Check Exact Botanical Equivalence
        bot_check = self.cross_sys_engine.validate_equivalence_safeguard("CON-UNANI-DARHALD", "CON-AYUR-DARUHARIDRA")
        self.assertTrue(bot_check["is_exact_equivalence"])
        self.assertEqual(bot_check["mapping_type"], CrossSystemMappingType.EXACT_EQUIVALENCE.value)

        # Check Functional Analogy (Zoaf-e-Meda <-> Mandagni)
        path_check = self.cross_sys_engine.validate_equivalence_safeguard("CON-UNANI-ZOAFF-MEDA", "CON-AYUR-MANDAGNI")
        self.assertFalse(path_check["is_exact_equivalence"])
        self.assertEqual(path_check["mapping_type"], CrossSystemMappingType.FUNCTIONAL_ANALOGY.value)
        self.assertIn("CORRESPONDING ANALOGY", path_check["allowed_presentation"])

        # Check Comparative Lens
        lens = self.cross_sys_engine.generate_comparative_lens("digestion")
        self.assertIn("modern_biomedicine", lens.system_perspectives)
        self.assertIn("unani_tibb", lens.system_perspectives)
        self.assertIn("ayurveda", lens.system_perspectives)
        self.assertIn("tcm", lens.system_perspectives)
        self.assertGreater(len(lens.shared_themes), 0)
        self.assertGreater(len(lens.fundamental_divergences), 0)
        self.assertIn("SAFEGUARD", lens.safeguard_notice)

    def test_03_first_class_unani_and_ayurveda_models(self):
        """Validates Unani and Ayurveda entity models without biomedical reductionism."""
        # Unani Mizaj Model
        mizaj = UnaniMizajEntity(
            mizaj_id="MIZAJ-DAMWI-01",
            classification=MizajClassification.DAMWI,
            qualities=["Harr", "Ratab"], # Hot & Moist
            physiological_tendencies=["Hyper-vascularity", "Elevated vital heat"]
        )
        self.assertEqual(mizaj.classification.value, "damwi")
        self.assertIn("Harr", mizaj.qualities)

        # Ayurveda Dosha & Agni Model
        self.assertEqual(DoshaType.PITTA.value, "pitta")
        self.assertEqual(AgniState.MANDAGNI.value, "mandagni")
        self.assertEqual(AyurvedicRasa.TIKTA.value, "tikta")
        self.assertEqual(AyurvedicVirya.USHNA.value, "ushna")

    def test_04_why_this_relationship_evidence_explanation(self):
        """Validates 'Why This Relationship Exists?' feature with supporting & conflicting studies."""
        explanation = self.graph_engine.explain_why_relationship("REL-BERB-T2D-001")
        self.assertEqual(explanation.relation_id, "REL-BERB-T2D-001")
        self.assertEqual(explanation.evidence_level, EvidenceLadder.E6_CONTROLLED_CLINICAL.value)
        self.assertEqual(explanation.supporting_studies_count, 2)
        self.assertEqual(explanation.contradicting_studies_count, 1)
        self.assertGreater(len(explanation.disagreement_reasons), 0)
        self.assertIn("different dose", explanation.disagreement_reasons[0])
        self.assertIsNotNone(explanation.causality_warning)

    def test_05_what_am_i_missing_gap_engine(self):
        """Validates 'What Am I Missing?' engine detecting evidence gaps and missing endpoints."""
        gap_report = self.graph_engine.what_am_i_missing("berberine")
        self.assertGreater(len(gap_report.known_dimensions), 0)
        self.assertGreater(len(gap_report.missing_critical_gaps), 0)
        # Check critical gaps
        gaps_text = " ".join(gap_report.missing_critical_gaps)
        self.assertIn("Pediatric", gaps_text)
        self.assertIn("pregnancy", gaps_text.lower())

    def test_06_claim_trace_reverse_provenance(self):
        """Validates reverse traversal: Claim -> Source -> Document -> Anchor -> Evidence -> Relation."""
        trace = self.graph_engine.trace_claim("CLM-RCT-BERB-01")
        self.assertIsNotNone(trace)
        self.assertEqual(trace.source_id, "SRC-NLM-001")
        self.assertEqual(trace.document_id, "PMID:18442638")
        self.assertEqual(trace.paragraph_anchor_hash, "8a1c90df44b1234a")
        self.assertEqual(trace.evidence_id, "EVD-BERB-01")
        self.assertEqual(trace.quarantine_status, "ACTIVE_VERIFIED")

    def test_07_multi_hop_traversal_and_causality_protection(self):
        """Validates path search and verifies that transitive association edges do not infer causality."""
        path = self.graph_engine.find_path("CON-MOD-BERBERINE-001", "CON-MOD-T2D-001")
        self.assertIsNotNone(path)
        self.assertEqual(path.path_type, "DIRECTLY_SOURCED")
        self.assertEqual(path.hop_count, 1)
        # Predicate is MAY_TREAT, so causality is not claimed as verified
        self.assertFalse(path.causality_valid)

    def test_08_retraction_impact_propagation(self):
        """Validates downstream impact when a study is retracted."""
        retract_report = self.graph_engine.propagate_retraction_impact("PMID:18442638")
        self.assertEqual(retract_report.retracted_document_id, "PMID:18442638")
        self.assertIn("CLM-RCT-BERB-01", retract_report.affected_claims)
        self.assertIn("REL-BERB-T2D-001", retract_report.affected_relations)
        self.assertIn("RES-T2D-METABOLIC-01", retract_report.dependent_research_projects)

        # Relation should now be RETRACTED in the graph
        rel = self.graph_engine.get_relation("REL-BERB-T2D-001")
        self.assertEqual(rel.knowledge_status, KnowledgeStatus.RETRACTED)

    def test_09_ai_grounding_packet_and_firewall(self):
        """Validates structured AI evidence packet generation and firewall interception."""
        packet = self.grounding_engine.build_grounding_packet("Berberine")
        self.assertIn("supported_facts", packet.model_dump())
        self.assertIn("clinical_context", packet.model_dump())
        self.assertIn("active_conflicts_and_contradictions", packet.model_dump())
        self.assertIn("explicit_unknowns_and_blindspots", packet.model_dump())
        self.assertEqual(packet.safety_firewall_verdict, "CLEARED")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGraphOntologyAcceptance)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
