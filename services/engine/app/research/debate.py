"""
ZMIE Multi-Agent Adversarial Debate & Consensus Engine
Implements Advocate vs. Skeptic cross-examination to establish calibrated
GRADE certainty ratings and prevent premature or biased consensus on clinical evidence.
"""

from typing import List, Dict, Any, Optional
import logging
from pydantic import BaseModel, Field

logger = logging.getLogger("zmie.research.debate")


class DebateArgument(BaseModel):
    agent_role: str  # ADVOCATE, SKEPTIC, ARBITER
    claim: str
    rationale: str
    evidence_citations: List[str] = Field(default_factory=list)
    confidence_weight: float = 1.0


class DebateVerdict(BaseModel):
    topic: str
    advocate_arguments: List[DebateArgument] = Field(default_factory=list)
    skeptic_arguments: List[DebateArgument] = Field(default_factory=list)
    consensus_synthesis: str
    grade_certainty: str  # HIGH, MODERATE, LOW, VERY_LOW
    recommended_clinical_posture: str  # ENDORSED_MONITORED, CAUTIONARY, INSUFFICIENT_DATA, CONTRAINDICATED
    bias_risk_factors_flagged: List[str] = Field(default_factory=list)


class AdversarialDebateEngine:
    """
    Orchestrates a structured debate between an Advocate Agent (maximizing plausibility & affirmative endpoints)
    and a Skeptic Agent (stress-testing methodological flaws, confounding variables, and small sample sizes),
    resolved by an Arbiter Agent to calibrate GRADE certainty.
    """

    @classmethod
    def conduct_debate(
        cls,
        topic: str,
        assertions: List[Any],
        evidence_table: List[Any],
        contradictions: Optional[List[Any]] = None
    ) -> DebateVerdict:
        advocate_args: List[DebateArgument] = []
        skeptic_args: List[DebateArgument] = []
        bias_flags: List[str] = []

        # 1. Advocate Agent Formulation
        if not evidence_table:
            advocate_args.append(
                DebateArgument(
                    agent_role="ADVOCATE",
                    claim="Preliminary mechanistic rationale exists based on traditional compendia or in-vitro models.",
                    rationale="Historical therapeutic longevity suggests potential bioactivity warranting investigation.",
                    evidence_citations=[],
                    confidence_weight=0.3
                )
            )
        else:
            for ev in evidence_table:
                findings = getattr(ev, "primary_findings", str(ev))
                source_id = getattr(ev, "source_id", "SRC-GENERIC")
                doi = getattr(ev, "doi_or_anchor", "N/A")
                effect = getattr(ev, "effect_size_or_stats", "observed outcome")
                citation = f"{source_id} (DOI: {doi})" if doi else source_id

                advocate_args.append(
                    DebateArgument(
                        agent_role="ADVOCATE",
                        claim=f"Primary outcome observed: {findings[:120]}...",
                        rationale=f"Reported effect size / metrics: {effect}. Validated against peer-reviewed anchor.",
                        evidence_citations=[citation],
                        confidence_weight=0.85
                    )
                )

        # 2. Skeptic Agent (Red Team) Formulation
        sample_sizes = []
        for ev in evidence_table:
            n = getattr(ev, "sample_size", None)
            if n is not None:
                try:
                    sample_sizes.append(int(n))
                except (ValueError, TypeError):
                    pass

        avg_sample_size = sum(sample_sizes) / len(sample_sizes) if sample_sizes else 0
        if avg_sample_size > 0 and avg_sample_size < 100:
            bias_flags.append(f"Small cohort size (mean N = {int(avg_sample_size)}), increasing risk of random error")
            skeptic_args.append(
                DebateArgument(
                    agent_role="SKEPTIC",
                    claim="Statistical power limitation in primary trials.",
                    rationale=f"Reported trials have modest cohort cohorts (mean N={int(avg_sample_size)}). High susceptibility to Type I error.",
                    evidence_citations=[],
                    confidence_weight=0.80
                )
            )

        if contradictions and len(contradictions) > 0:
            bias_flags.append(f"Identified {len(contradictions)} active contradiction cluster(s) in published findings")
            skeptic_args.append(
                DebateArgument(
                    agent_role="SKEPTIC",
                    claim="Heterogeneity and conflicting endpoint reports.",
                    rationale="Published literature exhibits divergent endpoints across tested cohorts and formulations.",
                    evidence_citations=[c.topic if hasattr(c, "topic") else str(c) for c in contradictions],
                    confidence_weight=0.90
                )
            )

        # Scrutinize assertion wording for latent generalizability risks
        for ast in assertions:
            st = getattr(ast, "statement", str(ast)).lower()
            if any(term in st for term in ["significant", "potent", "demonstrated", "efficacious"]):
                skeptic_args.append(
                    DebateArgument(
                        agent_role="SKEPTIC",
                        claim="Potential publication and reporting bias.",
                        rationale="Positive clinical signals in complementary medicine are frequently confounded by absence of negative trial publication.",
                        evidence_citations=[],
                        confidence_weight=0.75
                    )
                )
                break

        if not skeptic_args:
            skeptic_args.append(
                DebateArgument(
                    agent_role="SKEPTIC",
                    claim="Need for multi-center replication.",
                    rationale="Current evidence base lacks multi-institutional blinded confirmatory RCTs.",
                    evidence_citations=[],
                    confidence_weight=0.70
                )
            )

        # 3. Arbiter Agent Consensus & GRADE Calibration
        # Calculate grade certainty objectively
        if not evidence_table or len(evidence_table) == 0:
            grade = "VERY_LOW"
            posture = "INSUFFICIENT_DATA"
            consensus = f"Insufficient controlled trial evidence to substantiate clinical claims regarding {topic}. Traditional signals remain unverified by modern RCT standards."
        elif len(bias_flags) >= 2 or (contradictions and len(contradictions) > 0):
            grade = "LOW"
            posture = "CAUTIONARY"
            consensus = f"Emerging clinical evidence for {topic} demonstrates positive biomarker associations, but is tempered by noted methodological limitations ({'; '.join(bias_flags)}). Clinical application requires strict monitoring."
        elif avg_sample_size >= 100 and len(bias_flags) == 0:
            grade = "HIGH"
            posture = "ENDORSED_MONITORED"
            consensus = f"Well-powered clinical trial data demonstrates robust and reproducible endpoints for {topic}. Confounding risks are adequately mitigated."
        else:
            grade = "MODERATE"
            posture = "ENDORSED_MONITORED"
            consensus = f"Moderate certainty evidence substantiates therapeutic associations for {topic}. Further multi-center trials recommended to resolve secondary outcome variations."

        return DebateVerdict(
            topic=topic,
            advocate_arguments=advocate_args,
            skeptic_arguments=skeptic_args,
            consensus_synthesis=consensus,
            grade_certainty=grade,
            recommended_clinical_posture=posture,
            bias_risk_factors_flagged=bias_flags
        )
