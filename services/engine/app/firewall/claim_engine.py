"""
ZMIE Atomic Claim Decomposition & Normalization Engine
Splits complex multi-finding medical prose into independently verifiable atomic claims.
Extracts: Subject, Predicate, Object, Population, Intervention, Comparator, Outcome, Effect, Context.
Classifies claim types and potential clinical risk levels.
"""

import re
import uuid
from typing import List, Optional

from app.models.truth_firewall import (
    ClaimType,
    ClaimRiskLevel,
    NormalizedClaim
)


class AtomicClaimEngine:
    """
    Deconstructs composite medical text into atomic claims and normalizes components.
    """

    @classmethod
    def split_into_atomic_claims(cls, text: str) -> List[str]:
        """
        Splits text into atomic assertions.
        Handles semicolons, coordinate clauses with distinct numerical findings or endpoints.
        """
        clean_text = text.strip()
        if not clean_text:
            return []

        # Split sentences first
        raw_sentences = re.split(r'(?<=[.!?])\s+', clean_text)
        atomic_claims: List[str] = []

        for sent in raw_sentences:
            s_clean = sent.strip()
            if not s_clean:
                continue

            # Split on semicolons
            clauses = [c.strip() for c in s_clean.split(";") if c.strip()]
            for clause in clauses:
                # Check for multiple distinct findings joined by "whereas" or "while" or "and additionally"
                sub_clauses = re.split(r'\b(?:whereas|while|additionally|furthermore)\b', clause, flags=re.IGNORECASE)
                for sc in sub_clauses:
                    sc_clean = sc.strip().rstrip(".").strip()
                    if len(sc_clean) > 8:
                        atomic_claims.append(sc_clean)

        return atomic_claims if atomic_claims else [clean_text]

    @classmethod
    def classify_claim_type(cls, claim_text: str) -> ClaimType:
        """
        Assigns controlled claim typology.
        """
        c_lower = claim_text.lower()

        if any(w in c_lower for w in ["contraindicated", "toxic", "adverse", "distress", "safety", "hepatotoxic", "caution", "fatal", "harm"]):
            return ClaimType.SAFETY
        if any(w in c_lower for w in ["causes", "leads to", "induces", "responsible for"]):
            return ClaimType.CAUSAL
        if any(re.search(r'\b(?:p\s*[<=]\s*0\.\d+|\bci\b|\bhr\b|\brr\b|\bor\b)', c_lower) for _ in [1]):
            return ClaimType.STATISTICAL
        if any(char.isdigit() for char in claim_text) and any(w in c_lower for w in ["%", "mg", "g", "reduced by", "increased by", "fold"]):
            return ClaimType.NUMERICAL
        if any(w in c_lower for w in ["unani", "ayurveda", "mizaj", "dosha", "tibb", "charaka", "ibn sina"]):
            return ClaimType.TRADITIONAL_MEDICINE
        if any(w in c_lower for w in ["fda", "ema", "approved", "guideline", "recommends", "who guideline"]):
            return ClaimType.GUIDELINE
        if any(w in c_lower for w in ["mechanism", "pathway", "ampk", "receptor", "inhibits", "activates"]):
            return ClaimType.MECHANISTIC
        if any(w in c_lower for w in ["hypothesis", "theorized", "conjectured", "postulated"]):
            return ClaimType.HYPOTHESIS
        if any(w in c_lower for w in ["associated with", "correlated with", "linked to"]):
            return ClaimType.CORRELATIONAL
        if any(w in c_lower for w in ["rct", "trial", "clinical", "patients", "cohort"]):
            return ClaimType.CLINICAL

        return ClaimType.FACTUAL

    @classmethod
    def classify_risk_level(cls, claim_text: str, claim_type: ClaimType) -> ClaimRiskLevel:
        """
        Assigns risk tier: LOW_RISK, MEDIUM_RISK, HIGH_RISK, CRITICAL_RISK.
        """
        c_lower = claim_text.lower()

        # Critical risk: Pregnancy, lethal toxicities, unapproved fatal cure claims
        if any(w in c_lower for w in ["pregnancy", "pregnant", "lactation", "teratogenic", "fatal", "cure cancer", "kernicterus"]):
            return ClaimRiskLevel.CRITICAL_RISK
        # High risk: Clinical recommendations, dosing, severe contraindications, interactions
        if claim_type in [ClaimType.SAFETY, ClaimType.CAUSAL, ClaimType.GUIDELINE] or any(w in c_lower for w in ["contraindicated", "dose", "mg/day", "drug interaction"]):
            return ClaimRiskLevel.HIGH_RISK
        # Medium risk: Clinical efficacy, statistical numbers
        if claim_type in [ClaimType.CLINICAL, ClaimType.NUMERICAL, ClaimType.STATISTICAL, ClaimType.MECHANISTIC]:
            return ClaimRiskLevel.MEDIUM_RISK

        return ClaimRiskLevel.LOW_RISK

    @classmethod
    def normalize_claim(cls, claim_text: str) -> NormalizedClaim:
        """
        Parses text into structured Subject-Predicate-Object with clinical qualifiers.
        """
        c_lower = claim_text.lower()

        subject = "Intervention"
        predicate = "modulates"
        obj = "Clinical Endpoint"
        population = None
        effect = None

        # Extract numerical effect if present
        effect_match = re.search(r'(\b(?:by\s+)?(?:\d+\.?\d*%\s*|\b\d+\s*mg\b|\bp\s*<\s*0\.\d+\b))', claim_text, re.IGNORECASE)
        if effect_match:
            effect = effect_match.group(1).strip()

        # Extract population
        pop_match = re.search(r'(?:in|among)\s+([a-zA-Z0-9\s\-_]+?)(?:\s+with|\s+patients|\s+adults|\s+cohorts|\.|$)', claim_text, re.IGNORECASE)
        if pop_match:
            population = pop_match.group(0).strip().lstrip("in ").lstrip("among ")

        # Detect predicates
        predicates = ["cures", "causes", "reduces", "lowers", "increases", "activates", "inhibits", "treats", "improves", "is associated with"]
        for p in predicates:
            if p in c_lower:
                predicate = p
                parts = re.split(rf'\b{p}\b', claim_text, flags=re.IGNORECASE, maxsplit=1)
                if len(parts) == 2:
                    subject = parts[0].strip()
                    obj = parts[1].strip()
                break

        return NormalizedClaim(
            subject=subject[:60],
            predicate=predicate,
            object=obj[:80],
            population=population[:60] if population else None,
            intervention=subject[:60],
            outcome=obj[:80],
            effect=effect,
            context="Clinical Investigation"
        )
