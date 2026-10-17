"""
ZMIE Causality, Evidence Ladder & Cross-System Equivalence Firewall
Enforces:
1. Hard barrier against causal overstatement (association != causation).
2. Evidence Ladder language compliance (E4 preclinical cannot claim 'clinically proven').
3. Cross-system equivalence firewall (Unani Mizaj / Ayurveda Dosha != direct molecular pathology).
4. Safe rewrite formulation for exaggerated or overreaching claims.
"""

import re
from typing import Tuple, Optional, List

from app.models.claim import EvidenceGrade


class CausalityAndLanguageFirewall:
    """
    Guards scientific integrity against hyperbolic medical language and false cross-system equivalence.
    """

    # Causal verbs that require definitive human RCT or mechanistic proof
    CAUSAL_VERBS = ["causes", "cures", "treats", "eliminates", "reverses", "eradicates", "proves"]
    CORRELATIONAL_VERBS = ["is associated with", "correlates with", "is linked to", "modulates", "shows preliminary activity in"]

    @classmethod
    def check_causality_and_ladder(
        cls,
        claim_text: str,
        evidence_grade: str
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Evaluates whether claim wording exceeds the epistemic level of the evidence.
        Returns: (is_valid, reason, recommended_rewrite)
        """
        c_lower = claim_text.lower()
        has_causal_verb = any(re.search(rf'\b{verb}\b', c_lower) for verb in cls.CAUSAL_VERBS)

        # Rule 1: 'Cures' or 'eliminates' is virtually never acceptable without definitive cure proof
        if "cures" in c_lower or "eliminates" in c_lower or "reverses diabetes" in c_lower:
            rewrite = re.sub(r'\b(?:cures|eliminates|reverses)\b', "is associated with clinically meaningful improvement in", claim_text, flags=re.IGNORECASE)
            return False, "Causal overreach: Absolute cure / reversal terminology unsupported in chronic biomedical conditions.", rewrite

        # Rule 2: Preclinical / in-vitro / observational evidence cannot justify causal or 'proven' claims
        if evidence_grade in ["preclinical_in_vivo", "in_vitro_mechanistic", "observational_human_evidence", "canonical_traditional_claim", "E4_OBSERVATIONAL_COHORT", "E6_IN_VITRO"]:
            if has_causal_verb or "proven" in c_lower or "clinically established" in c_lower:
                rewrite = claim_text
                for verb in cls.CAUSAL_VERBS:
                    rewrite = re.sub(rf'\b{verb}\b', "is associated with changes in", rewrite, flags=re.IGNORECASE)
                rewrite = re.sub(r'\b(?:proven|clinically established)\b', "investigated in preliminary models of", rewrite, flags=re.IGNORECASE)
                return False, f"Causal overreach: Evidence grade ({evidence_grade}) only supports correlational or preliminary language, not direct causal claims.", rewrite

        return True, "Causality and evidence ladder wording within acceptable boundaries.", None

    @classmethod
    def check_cross_system_equivalence(
        cls,
        claim_text: str
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Flags false equivalences between traditional medical concepts (Mizaj/Dosha)
        and modern biochemical entities unless qualified as an analogy or conceptual parallel.
        """
        c_lower = claim_text.lower()

        # Dangerous false equivalences: "Mizaj is the Unani equivalent of diabetes", "Vata is epinephrine"
        direct_eq_patterns = [
            r'\b(?:mizaj|dosha|dam|safra|balgham|sauda)\s+(?:is\s+the\s+same\s+as|equals|is\s+equivalent\s+to|means)\s+([a-zA-Z\s]+)',
            r'\b(?:unani|ayurvedic)\s+cure\s+for\s+([a-zA-Z\s]+)'
        ]

        for pat in direct_eq_patterns:
            if re.search(pat, c_lower):
                rewrite = re.sub(
                    r'\b(?:is\s+the\s+same\s+as|equals|is\s+equivalent\s+to)\b',
                    "shares functional and conceptual parallels with",
                    claim_text,
                    flags=re.IGNORECASE
                )
                return False, "False equivalence: Traditional holistic paradigms cannot be equated 1:1 with reductionist biochemical entities.", rewrite

        return True, "Cross-system terminology appropriately qualified.", None
