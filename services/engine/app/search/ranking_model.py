"""
ZMIE Multi-Dimensional Ranking Model & Score Explanation Engine (Sections 20-27)
Calculates configurable composite relevance incorporating:
- Query-Intent Adaptive Weighting (EVIDENCE, SAFETY, GUIDELINE, TRADITIONAL)
- Evidence Ladder Priority (E6 > E5 > E4 > E3 > E2 > E1 > E0)
- Source Authority Tiering (Tier A > B > C > D > E > F > G)
- Contextual Freshness
- "Why This Result?" human-readable explanation translation
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.source import AuthorityTier
from app.models.graph import EvidenceLadder
from app.models.claim import MedicalSystem
from app.search.query_engine import StructuredQuery, QueryIntent
from app.search.retrieval_pipeline import RetrievalCandidate


class ScoredSearchResult(BaseModel):
    candidate: RetrievalCandidate
    final_score: float
    component_scores: Dict[str, float]
    why_this_result: str
    evidence_badge: str
    authority_badge: str


class MultiDimensionalRankingEngine:
    """
    Reranks candidate pools based on query intent and multi-dimensional medical signals.
    """

    AUTHORITY_WEIGHTS = {
        AuthorityTier.TIER_A.value: 1.0,
        AuthorityTier.TIER_B.value: 0.90,
        AuthorityTier.TIER_C.value: 0.85,
        AuthorityTier.TIER_D.value: 0.75,
        AuthorityTier.TIER_E.value: 0.85, # Classical canonical codex
        AuthorityTier.TIER_F.value: 0.50,
        AuthorityTier.TIER_G.value: 0.10
    }

    EVIDENCE_WEIGHTS = {
        EvidenceLadder.E6_CONTROLLED_CLINICAL.value: 1.0,
        EvidenceLadder.E5_HUMAN_OBSERVATIONAL.value: 0.80,
        EvidenceLadder.E4_IN_VIVO_PRECLINICAL.value: 0.60,
        EvidenceLadder.E3_IN_VITRO.value: 0.40,
        EvidenceLadder.E2_COMPUTATIONAL.value: 0.25,
        EvidenceLadder.E1_LITERATURE_ASSOCIATION.value: 0.15,
        EvidenceLadder.E0_AI_HYPOTHESIS.value: 0.05,
        "canonical_traditional_claim": 0.85
    }

    @classmethod
    def rerank_candidates(cls, candidates: List[RetrievalCandidate], sq: StructuredQuery) -> List[ScoredSearchResult]:
        scored_results: List[ScoredSearchResult] = []
        current_year = 2026

        for cand in candidates:
            # 1. Base Relevance Scores from channels
            lexical_score = cand.channel_scores.get("lexical", 0.0)
            entity_score = cand.channel_scores.get("entity", 0.0)
            graph_score = cand.channel_scores.get("graph", 0.0)
            safety_score = cand.channel_scores.get("safety", 0.0)

            # 2. Source Authority Score
            auth_score = cls.AUTHORITY_WEIGHTS.get(cand.authority_tier, 0.5)

            # 3. Evidence Quality Score
            evd_score = cls.EVIDENCE_WEIGHTS.get(cand.evidence_level, 0.4)

            # 4. Contextual Freshness Score
            # For classical codices, age is not penalized; for guidelines/trials, recent is favored
            if cand.authority_tier == AuthorityTier.TIER_E.value or "classical" in str(cand.study_type).lower():
                freshness_score = 0.90
            elif cand.publication_year:
                age = max(0, current_year - cand.publication_year)
                freshness_score = max(0.2, 1.0 - (age * 0.04)) # ~25 years decays to 0.2
            else:
                freshness_score = 0.5

            # 5. Intent-Adaptive Weighting (Section 23, 24)
            w_lex = 0.20
            w_ent = 0.20
            w_auth = 0.15
            w_evd = 0.20
            w_graph = 0.15
            w_fresh = 0.10

            if QueryIntent.EVIDENCE in sq.intents or QueryIntent.TREATMENT_RESEARCH in sq.intents:
                w_evd = 0.35
                w_auth = 0.20
                w_lex = 0.15
                w_ent = 0.15
                w_fresh = 0.15

            elif QueryIntent.SAFETY in sq.intents or QueryIntent.INTERACTION in sq.intents:
                w_auth = 0.30
                w_evd = 0.25
                if safety_score > 0:
                    evd_score += 0.5 # Boost safety documentation

            elif QueryIntent.TRADITIONAL_MEDICINE in sq.intents:
                if cand.medical_system in (MedicalSystem.UNANI.value, MedicalSystem.AYURVEDA.value, MedicalSystem.TCM.value):
                    auth_score += 0.25

            # Compute Final Composite Score
            final = (
                (lexical_score * w_lex) +
                (entity_score * w_ent) +
                (auth_score * w_auth) +
                (evd_score * w_evd) +
                (graph_score * w_graph) +
                (freshness_score * w_fresh)
            )

            # Retraction penalty if present
            if cand.is_retracted:
                final -= 1.0

            # Component score breakdown (Section 26)
            components = {
                "lexical": round(lexical_score, 3),
                "entity": round(entity_score, 3),
                "authority": round(auth_score, 3),
                "evidence": round(evd_score, 3),
                "graph": round(graph_score, 3),
                "freshness": round(freshness_score, 3),
                "bm25": round(float(cand.channel_scores.get("bm25", lexical_score)), 3),
                "vector": round(float(cand.channel_scores.get("vector", entity_score)), 3),
                "rrf_fusion": round(float(cand.channel_scores.get("rrf_fusion", 0.0)), 6)
            }

            # Human-readable "Why This Result?" translation (Section 27)
            why_text = cls._generate_why_explanation(cand, sq, components)

            evd_badge = cand.evidence_level or "unclassified"
            auth_badge = f"{cand.source_organization} ({cand.authority_tier})"

            scored_results.append(ScoredSearchResult(
                candidate=cand,
                final_score=round(final, 3),
                component_scores=components,
                why_this_result=why_text,
                evidence_badge=evd_badge,
                authority_badge=auth_badge
            ))

        # Sort descending by final score
        scored_results.sort(key=lambda x: x.final_score, reverse=True)
        return scored_results

    @classmethod
    def _generate_why_explanation(cls, cand: RetrievalCandidate, sq: StructuredQuery, components: Dict[str, float]) -> str:
        reasons = []
        if components["evidence"] >= 0.8:
            reasons.append(f"High-quality controlled clinical evidence ({cand.study_type or 'human study'})")
        if components["authority"] >= 0.8:
            reasons.append(f"Authoritative statutory or indexed repository ({cand.source_organization})")
        if components["entity"] >= 0.8:
            reasons.append(f"Direct concept match on query entities ({', '.join(sq.entities)})")
        if cand.channel_scores.get("safety", 0) > 0:
            reasons.append("High-priority clinical safety / interaction record")
        if cand.medical_system in (MedicalSystem.UNANI.value, MedicalSystem.AYURVEDA.value):
            reasons.append(f"Canonical classical codex ({cand.medical_system.title()})")

        return " | ".join(reasons) if reasons else "Keyword and semantic correlation with query terms."
