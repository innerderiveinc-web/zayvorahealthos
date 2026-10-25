"""
ZMIE 3-Tier Hybrid Neural & Semantic Search Engine Acceptance Suite (Phase 2)
Validates:
1. Tier 1: Lexical MeSH & Pharmacological Thesaurus expansion and BM25 scoring with field boosting.
2. Tier 2: Biomedical Dense Neural Vector embeddings (128-dim, unit-normalized) and cosine similarity.
3. Tier 3: Causal Knowledge Graph multi-hop pathfinding (Substance -> Target -> Pathway -> Phenotype).
4. Weighted Reciprocal Rank Fusion (k=60) multi-channel consensus ranking.
5. REST API endpoint `POST /v1/search/hybrid` performance and response schema.
"""

import math
import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.search.query_engine import QueryUnderstandingEngine
from app.search.mesh_thesaurus import MeSHThesaurus
from app.search.neural_vector import NeuralVectorEmbedder
from app.search.causal_graph_search import CausalGraphSearchEngine
from app.search.retrieval_pipeline import HybridRetrievalPipeline


class TestHybridRRFSearchAcceptance(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.mesh_thesaurus = MeSHThesaurus()
        self.causal_engine = CausalGraphSearchEngine()
        self.pipeline = HybridRetrievalPipeline()
        self.query_engine = QueryUnderstandingEngine()

    def test_01_mesh_expansion_and_traditional_synonyms(self):
        """Tier 1: MeSH thesaurus maps botanical/traditional synonyms to canonical concepts."""
        # Botanical Unani/Ayurvedic term
        expansion = self.mesh_thesaurus.expand_query_mesh("Is Darhald effective for Madhumeha?")
        matched_concepts = [c["heading"] for c in expansion["matched_concepts"]]

        # Darhald -> Berberine; Madhumeha -> Diabetes Mellitus, Type 2
        self.assertIn("Berberine", matched_concepts)
        self.assertIn("Diabetes Mellitus, Type 2", matched_concepts)

        # Expanded terms should contain chemical and traditional cross-references
        exp_terms = expansion["expanded_terms"]
        self.assertTrue(any("daruharidra" in t for t in exp_terms))
        self.assertTrue(any("t2dm" in t or "type 2 diabetes" in t for t in exp_terms))

    def test_02_bm25_scoring_with_field_boosting(self):
        """Tier 1: BM25 score reflects title and MeSH boosts with standard saturation."""
        query_terms = ["berberine", "diabetes", "glucose"]
        term_doc_counts = {"berberine": 3, "diabetes": 3, "glucose": 2}

        # Document with matches in title, abstract, and MeSH terms
        score_high, matched_high = MeSHThesaurus.calculate_bm25_score(
            query_terms=query_terms,
            title="Efficacy of Berberine in Patients with Type 2 Diabetes Mellitus",
            abstract="Berberine significantly reduced blood glucose and HbA1c in adult patients.",
            mesh_terms=["Diabetes Mellitus, Type 2", "Berberine", "Blood Glucose"],
            doc_count=10,
            term_doc_counts=term_doc_counts
        )

        # Document with minimal peripheral match
        score_low, matched_low = MeSHThesaurus.calculate_bm25_score(
            query_terms=query_terms,
            title="Rome IV Criteria for Functional Gastrointestinal Disorders",
            abstract="Evaluates recurrent abdominal pain and bowel patterns.",
            mesh_terms=["Irritable Bowel Syndrome"],
            doc_count=10,
            term_doc_counts=term_doc_counts
        )

        self.assertGreater(score_high, score_low)
        self.assertGreater(score_high, 0.5)
        self.assertEqual(score_low, 0.0)
        self.assertIn("berberine", matched_high)

    def test_03_neural_vector_embeddings_and_cosine_similarity(self):
        """Tier 2: 128-dim dense neural vector is unit-normalized and semantic similarity behaves monotonically."""
        vec1 = NeuralVectorEmbedder.embed_text(
            "Berberine activates AMPK and lowers fasting blood glucose in type 2 diabetes mellitus",
            entities=["Berberine", "Type 2 Diabetes Mellitus"]
        )
        vec2 = NeuralVectorEmbedder.embed_text(
            "Metformin activates AMP-activated protein kinase to improve glycemic control and insulin sensitivity",
            entities=["Metformin", "Type 2 Diabetes Mellitus"]
        )
        vec_unrelated = NeuralVectorEmbedder.embed_text(
            "Treatment of severe compound fractures of the tibia with external fixation",
            entities=["Tibia", "Fracture"]
        )

        # Check vector dimensionality and unit norm (L2 = 1.0)
        self.assertEqual(len(vec1), 128)
        norm1 = math.sqrt(sum(x * x for x in vec1))
        self.assertAlmostEqual(norm1, 1.0, places=3)

        # Cosine similarity between related metabolic treatments should be high
        sim_related = NeuralVectorEmbedder.cosine_similarity(vec1, vec2)
        sim_unrelated = NeuralVectorEmbedder.cosine_similarity(vec1, vec_unrelated)

        self.assertGreater(sim_related, 0.40)
        self.assertGreater(sim_related, sim_unrelated)

    def test_04_causal_graph_multi_hop_traversal(self):
        """Tier 3: Causal knowledge graph finds directed mechanistic paths."""
        paths = self.causal_engine.find_causal_paths(start_concept="berberine", target_concept="type 2 diabetes mellitus")
        self.assertGreater(len(paths), 0)

        top_path = paths[0]
        # Should contain intermediate targets such as AMPK or Gluconeogenesis
        self.assertIn("ampk", [n.lower() for n in top_path.path_nodes])
        self.assertGreater(top_path.overall_confidence, 0.70)
        self.assertTrue("ACTIVATES" in top_path.mechanistic_narrative)

    def test_05_rrf_multi_channel_consensus_ranking(self):
        """Multi-channel consensus candidate scores higher in RRF (k=60) than single-channel candidates."""
        sq = self.query_engine.parse_query("What is the clinical evidence for berberine in type 2 diabetes?")
        candidates = self.pipeline.execute_retrieval(sq)

        self.assertGreater(len(candidates), 0)
        # Top candidate should be the verified RCT (PMID:18442638)
        top_cand = sorted(candidates, key=lambda c: c.channel_scores.get("rrf_fusion", 0.0), reverse=True)[0]
        self.assertEqual(top_cand.document_id, "PMID:18442638")

        # Multi-channel check: Should have hits across bm25, vector, and graph
        self.assertGreater(top_cand.channel_scores.get("bm25", 0.0), 0.0)
        self.assertGreater(top_cand.channel_scores.get("vector", 0.0), 0.0)
        self.assertGreater(top_cand.channel_scores.get("graph", 0.0), 0.0)
        self.assertGreater(top_cand.channel_scores.get("rrf_fusion", 0.0), 0.015)

    def test_06_hybrid_search_rest_api_endpoint(self):
        """REST API POST /v1/search/hybrid returns structured 3-tier hybrid scores."""
        headers = {"X-Forwarded-For": "198.51.100.42"}
        payload = {
            "query": "berberine glycemic control and insulin resistance",
            "mode": "evidence"
        }
        resp = self.client.post("/v1/search/hybrid", json=payload, headers=headers)
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertIn("fusion_algorithm", data)
        self.assertIn("mesh_expansion", data)
        self.assertGreater(data["total_results"], 0)

        top_item = data["results"][0]
        self.assertIn("document_id", top_item)
        self.assertIn("channel_scores", top_item)
        scores = top_item["channel_scores"]
        self.assertIn("bm25", scores)
        self.assertIn("neural_vector", scores)
        self.assertIn("causal_graph", scores)
        self.assertIn("rrf_fusion", scores)


if __name__ == "__main__":
    unittest.main()
