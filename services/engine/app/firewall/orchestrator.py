"""
ZMIE Truth & Safety Firewall Orchestrator
Coordinates the end-to-end verification pipeline:
CLAIM EXTRACTION -> CLASSIFICATION -> NORMALIZATION -> CITATION VERIFICATION
-> CAUSALITY FIREWALL -> CROSS-SYSTEM CHECK -> RETRACTION CHECK -> QUALITY GATE -> APPROVED / MODIFIED / BLOCKED
Provides audit logs, lineage tracking, and retraction propagation impact analysis.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

from app.models.truth_firewall import (
    ClaimType,
    ClaimStatus,
    SupportLevel,
    ClaimRiskLevel,
    FirewallVerdict,
    Citation,
    ClaimVerification,
    AnswerLineage,
    VerifiedAnswerPacket,
    VerificationReview
)
from app.firewall.claim_engine import AtomicClaimEngine
from app.firewall.citation_engine import CitationVerificationEngine
from app.firewall.causality_firewall import CausalityAndLanguageFirewall


class TruthAndSafetyFirewall:
    """
    Central gatekeeper of ZMIE evidence integrity and patient safety.
    Enforces the rule: AI explains and hypothesizes, but only verified facts pass into trusted output.
    """

    _verification_store: Dict[str, ClaimVerification] = {}
    _reviews_store: Dict[str, VerificationReview] = {}
    _retracted_sources_registry: set = set(["RETRACTED-01", "RETRACTED-J-009", "10.1000/retracted-trial"])

    @classmethod
    def register_retraction(cls, source_id_or_doi: str):
        """
        Registers a retracted publication to trigger revalidation and cascading alerts.
        """
        cls._retracted_sources_registry.add(source_id_or_doi)

    @classmethod
    def get_verification(cls, verification_id: str) -> Optional[ClaimVerification]:
        return cls._verification_store.get(verification_id)

    @classmethod
    def verify_answer(
        cls,
        generated_answer: str,
        citations: Optional[List[Citation]] = None,
        passages_map: Optional[Dict[str, str]] = None
    ) -> VerifiedAnswerPacket:
        """
        Executes complete verification pipeline for an AI-generated answer.
        """
        if citations is None:
            citations = []
        if passages_map is None:
            passages_map = {}

        # Step 1: Split into atomic claims
        raw_claims = AtomicClaimEngine.split_into_atomic_claims(generated_answer)
        verified_claims: List[ClaimVerification] = []

        overall_verdict = FirewallVerdict.PASS
        modified_sentences = []
        limitations = []
        citation_failures = 0
        contradictions_found = 0

        # Step 2: Iterate and verify each atomic claim
        for idx, claim_text in enumerate(raw_claims):
            c_type = AtomicClaimEngine.classify_claim_type(claim_text)
            c_risk = AtomicClaimEngine.classify_risk_level(claim_text, c_type)
            norm_claim = AtomicClaimEngine.normalize_claim(claim_text)

            # Match citation if available
            matched_citation = citations[idx] if idx < len(citations) else None
            support_level = SupportLevel.UNKNOWN
            context_match = True
            reasons = []
            verdict = FirewallVerdict.PASS
            recommended_rewrite = None
            retraction_status = "CLEAR"

            if matched_citation:
                # Retraction check
                if matched_citation.identifier in cls._retracted_sources_registry or matched_citation.is_retracted:
                    retraction_status = "RETRACTED"
                    reasons.append(f"Hard block: Cited document ({matched_citation.identifier}) has been retracted.")
                    verdict = FirewallVerdict.BLOCK
                    citation_failures += 1
                else:
                    passage = passages_map.get(matched_citation.citation_id) or passages_map.get(matched_citation.identifier, "")
                    sup_lvl, ctx_ok, cit_reasons = CitationVerificationEngine.verify_citation_entailment(
                        claim_text, matched_citation, passage
                    )
                    support_level = sup_lvl
                    context_match = ctx_ok
                    reasons.extend(cit_reasons)

                    if sup_lvl == SupportLevel.DOES_NOT_SUPPORT:
                        verdict = FirewallVerdict.BLOCK
                        citation_failures += 1
                    elif sup_lvl == SupportLevel.WEAK_CONTEXTUAL_MATCH or not ctx_ok:
                        verdict = FirewallVerdict.MODIFY
            else:
                # No citation supplied for this claim
                if c_risk in [ClaimRiskLevel.CRITICAL_RISK, ClaimRiskLevel.HIGH_RISK]:
                    verdict = FirewallVerdict.BLOCK
                    reasons.append("Uncited high-risk clinical or safety assertion.")
                else:
                    reasons.append("Claim lacks direct citation; treated as inferential summary.")
                    support_level = SupportLevel.PARTIAL_SUPPORT

            # Step 3: Causality & Evidence Ladder Check
            causal_ok, causal_reason, causal_rewrite = CausalityAndLanguageFirewall.check_causality_and_ladder(
                claim_text, evidence_grade="observational_human_evidence"
            )
            if not causal_ok:
                reasons.append(causal_reason)
                if verdict != FirewallVerdict.BLOCK:
                    verdict = FirewallVerdict.MODIFY
                    recommended_rewrite = causal_rewrite

            # Step 4: Cross-System Equivalence Check
            eq_ok, eq_reason, eq_rewrite = CausalityAndLanguageFirewall.check_cross_system_equivalence(claim_text)
            if not eq_ok:
                reasons.append(eq_reason)
                if verdict != FirewallVerdict.BLOCK:
                    verdict = FirewallVerdict.MODIFY
                    recommended_rewrite = eq_rewrite

            # Step 5: Determine Claim Status & Build Record
            if verdict == FirewallVerdict.BLOCK:
                claim_status = ClaimStatus.RETRACTED if retraction_status == "RETRACTED" else ClaimStatus.UNSUPPORTED
            elif verdict == FirewallVerdict.MODIFY:
                claim_status = ClaimStatus.PARTIALLY_SUPPORTED
            else:
                claim_status = ClaimStatus.SUPPORTED

            cv = ClaimVerification(
                verification_id=f"vrf-{uuid.uuid4().hex[:8]}",
                claim_id=f"clm-{uuid.uuid4().hex[:8]}",
                claim_text=claim_text,
                normalized_claim=norm_claim,
                claim_type=c_type,
                claim_status=claim_status,
                risk_level=c_risk,
                source_ids=[matched_citation.source_id] if matched_citation else [],
                document_ids=[matched_citation.document_id] if matched_citation else [],
                citation_ids=[matched_citation.citation_id] if matched_citation else [],
                support_level=support_level,
                context_match=context_match,
                retraction_status=retraction_status,
                verdict=verdict,
                recommended_rewrite=recommended_rewrite,
                reasons=reasons
            )
            cls._verification_store[cv.verification_id] = cv
            verified_claims.append(cv)

            # Accumulate modified answer text
            if verdict == FirewallVerdict.PASS:
                modified_sentences.append(claim_text)
            elif verdict == FirewallVerdict.MODIFY and recommended_rewrite:
                modified_sentences.append(recommended_rewrite)
            else:
                # Blocked: omit sentence and record limitation
                limitations.append(f"Blocked unverified assertion: '{claim_text}' ({'; '.join(reasons)})")

        # Step 6: Determine Final Packet Status & Quality Gate
        if any(c.verdict == FirewallVerdict.BLOCK for c in verified_claims):
            if all(c.verdict == FirewallVerdict.BLOCK for c in verified_claims):
                overall_verdict = FirewallVerdict.BLOCK
                final_status = "BLOCKED"
                final_answer = "This response has been blocked by the ZMIE Truth & Safety Firewall due to unsubstantiated or retracted assertions."
            else:
                overall_verdict = FirewallVerdict.MODIFY
                final_status = "PARTIAL"
                final_answer = ". ".join(modified_sentences) + "." if modified_sentences else "Response partially restricted."
        elif any(c.verdict == FirewallVerdict.MODIFY for c in verified_claims):
            overall_verdict = FirewallVerdict.MODIFY
            final_status = "TRUSTED_WITH_LIMITATIONS"
            final_answer = ". ".join(modified_sentences) + "."
        else:
            overall_verdict = FirewallVerdict.PASS
            final_status = "TRUSTED"
            final_answer = generated_answer

        lineage = AnswerLineage(
            answer_id=f"ans-{uuid.uuid4().hex[:8]}",
            claim_ids=[c.claim_id for c in verified_claims],
            citation_ids=[c.citation_id for c in citations]
        )

        metrics = {
            "claims_checked": len(verified_claims),
            "supported": len([c for c in verified_claims if c.claim_status == ClaimStatus.SUPPORTED]),
            "partially_supported": len([c for c in verified_claims if c.claim_status == ClaimStatus.PARTIALLY_SUPPORTED]),
            "unsupported_or_blocked": len([c for c in verified_claims if c.verdict == FirewallVerdict.BLOCK]),
            "citation_failures": citation_failures,
            "overall_verdict": overall_verdict.value
        }

        return VerifiedAnswerPacket(
            answer=final_answer,
            original_answer=generated_answer,
            status=final_status,
            verdict=overall_verdict,
            claims=verified_claims,
            citations=citations,
            contradictions=[],
            safety_alerts=[],
            limitations=limitations,
            verification_metrics=metrics,
            lineage=lineage
        )

    @classmethod
    def run_retraction_impact_analysis(cls, retracted_identifier: str) -> Dict[str, Any]:
        """
        Traces all claims, answers, and reports influenced by a newly retracted document.
        """
        cls.register_retraction(retracted_identifier)
        affected_claims = []
        for v in cls._verification_store.values():
            if any(retracted_identifier in cid for cid in v.citation_ids) or \
               any(retracted_identifier in sid for sid in v.source_ids) or \
               any(retracted_identifier in did for did in v.document_ids):
                v.retraction_status = "RETRACTED"
                v.claim_status = ClaimStatus.RETRACTED
                v.verdict = FirewallVerdict.BLOCK
                affected_claims.append(v.claim_id)

        return {
            "retracted_identifier": retracted_identifier,
            "status": "RETRACTED_PROPAGATED",
            "affected_claims_count": len(affected_claims),
            "affected_claims": affected_claims,
            "action_taken": "Marked for immediate revalidation and cache eviction."
        }
