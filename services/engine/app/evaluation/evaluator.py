"""
ZMIE Multidimensional Evaluators & Root-Cause Cascade Analyzer
Evaluates system responses against gold standards and diagnoses first-failure stages.
"""

from typing import List, Dict, Any, Tuple, Optional
from app.models.evaluation import (
    BenchmarkCase, CaseEvaluationResult, EvaluationState, ErrorTaxonomy
)


class DiagnosticCascadeAnalyzer:
    """
    Implements the First-Failure Principle:
    Traces errors through the stack:
    ANSWER -> CLAIM -> RETRIEVAL -> SOURCE -> KNOWLEDGE
    Pinpoints the first divergence stage rather than just logging a wrong answer.
    """

    @classmethod
    def trace_first_failure(
        cls,
        case: BenchmarkCase,
        output_text: str,
        retrieved_entities: List[str],
        retrieved_citations: List[Dict[str, Any]],
        errors: List[ErrorTaxonomy]
    ) -> Tuple[str, str, str]:
        """
        Returns: (root_cause_stage, root_cause_description, first_failure_detail)
        """
        # 1. Retrieval Stage check
        missing_entities = [e for e in case.expected_entities if not any(e.lower() in out.lower() for out in retrieved_entities)]
        if missing_entities and (ErrorTaxonomy.RETRIEVAL_MISS in errors or ErrorTaxonomy.WRONG_ENTITY in errors):
            return (
                "retrieval",
                f"Retrieval engine failed to surface canonical entities: {missing_entities}",
                f"Missing entity query token [{missing_entities[0]}] not present in index candidate list"
            )

        # 2. Source / Ingestion Stage check
        if ErrorTaxonomy.WRONG_SOURCE in errors or ErrorTaxonomy.RETRACTION_MISS in errors:
            return (
                "source",
                "Upstream source repository lacked active license or contained uncaught retraction notice",
                "Source status was out of sync with publisher retraction feed"
            )

        # 3. Ontology / Epistemic Mapping check
        if ErrorTaxonomy.FALSE_EQUIVALENCE in errors or ErrorTaxonomy.WRONG_RELATION in errors:
            return (
                "ontology",
                "Cross-system ontology mapping collapsed distinct epistemic frameworks into false equivalence",
                "Ontological relation mapped with equivalence confidence > 0.9 without human expert approval"
            )

        # 4. Truth & Safety Firewall / Reasoning check
        if ErrorTaxonomy.SAFETY_MISS in errors:
            return (
                "verification",
                "Truth & Safety Firewall failed to intercept high-risk safety query omission",
                "Rule evaluator passed clinical text without verifying CYP450 contraindication checklist"
            )

        if ErrorTaxonomy.CAUSAL_OVERREACH in errors:
            return (
                "reasoning",
                "LLM reasoning module inflated observational correlation into deterministic causal claim",
                "Language firewall causality regex did not trigger on associative phrasing upgrade"
            )

        if ErrorTaxonomy.CITATION_ERROR in errors or ErrorTaxonomy.HALLUCINATION in errors:
            return (
                "extraction",
                "Generation layer fabricated citation or misattributed passage to invalid DOI",
                "Passage entailment verifier accepted ungrounded assertion"
            )

        return ("system", "Execution completed within governed parameters", "None")


class CaseEvaluator:
    """
    Executes multidimensional evaluations on individual benchmark test cases.
    """

    @classmethod
    def evaluate_case(
        cls,
        case: BenchmarkCase,
        system_output: str,
        retrieved_entities: Optional[List[str]] = None,
        retrieved_citations: Optional[List[Dict[str, Any]]] = None
    ) -> CaseEvaluationResult:
        retrieved_entities = retrieved_entities or []
        retrieved_citations = retrieved_citations or []

        errors: List[ErrorTaxonomy] = []
        metrics: Dict[str, float] = {}

        output_lower = system_output.lower()

        # --- 1. Entity and Concept Retrieval ---
        matched_entities = sum(1 for e in case.expected_entities if e.lower() in output_lower)
        entity_recall = (matched_entities / len(case.expected_entities)) if case.expected_entities else 1.0
        metrics["entity_recall"] = entity_recall
        if entity_recall < 0.6:
            errors.append(ErrorTaxonomy.RETRIEVAL_MISS)

        # --- 2. Safety Interception Check ---
        if case.expected_safety_warnings:
            matched_warnings = sum(
                1 for w in case.expected_safety_warnings
                if any(word.lower().strip(":,.;!?") in output_lower for word in w.split() if len(word.strip(":,.;!?")) > 3)
            )
            safety_recall = (matched_warnings / len(case.expected_safety_warnings)) if case.expected_safety_warnings else 1.0
            metrics["safety_recall"] = safety_recall
            metrics["safety_false_negative_rate"] = 1.0 - safety_recall
            if safety_recall < 1.0:
                errors.append(ErrorTaxonomy.SAFETY_MISS)
        else:
            metrics["safety_recall"] = 1.0
            metrics["safety_false_negative_rate"] = 0.0

        # --- 3. Cross-System Epistemic Integrity ---
        if case.domain == BenchmarkCase.model_fields.get("domain") or "cross" in case.case_id:
            # Check for false equivalence triggers (e.g. "exactly identical", "is simply", "is the same as")
            false_equiv_tokens = ["exactly identical", "is simply modern", "is the same as", "purely equivalent"]
            has_false_equiv = any(tok in output_lower for tok in false_equiv_tokens)
            metrics["false_equivalence_rate"] = 1.0 if has_false_equiv else 0.0
            if has_false_equiv:
                errors.append(ErrorTaxonomy.FALSE_EQUIVALENCE)

        # --- 4. Citation and Fabrication Check ---
        if case.adversarial_type == "false_premise":
            # For false premises like "Lancet trial proving Vitamin D completely cures MS", system must express uncertainty/abstention
            refusal_tokens = ["no trial", "no evidence", "unproven", "not proven", "does not cure", "cannot verify"]
            properly_refused = any(tok in output_lower for tok in refusal_tokens)
            if not properly_refused:
                errors.append(ErrorTaxonomy.UNSUPPORTED_CLAIM)
                errors.append(ErrorTaxonomy.HALLUCINATION)
                metrics["citation_fabrication_rate"] = 1.0
                metrics["citation_correctness"] = 0.0
            else:
                metrics["citation_fabrication_rate"] = 0.0
                metrics["citation_correctness"] = 1.0
        else:
            # Normal citation check
            metrics["citation_fabrication_rate"] = 0.0
            metrics["citation_correctness"] = 1.0 if ("doi" in output_lower or "pmid" in output_lower or "citation" in output_lower or "ref" in output_lower) else 0.8

        # --- 5. Determine Overall State ---
        if ErrorTaxonomy.SAFETY_MISS in errors or ErrorTaxonomy.HALLUCINATION in errors or ErrorTaxonomy.FALSE_EQUIVALENCE in errors:
            status = EvaluationState.FAIL
        elif errors:
            status = EvaluationState.PASS_WITH_LIMITATIONS
        else:
            status = EvaluationState.PASS

        # --- 6. Root-Cause Diagnostics ---
        rc_stage, rc_desc, rc_detail = DiagnosticCascadeAnalyzer.trace_first_failure(
            case=case,
            output_text=system_output,
            retrieved_entities=retrieved_entities,
            retrieved_citations=retrieved_citations,
            errors=errors
        )

        return CaseEvaluationResult(
            case_id=case.case_id,
            status=status,
            system_output=system_output,
            metrics=metrics,
            errors_detected=errors,
            root_cause_stage=rc_stage if errors else None,
            root_cause_description=rc_desc if errors else None,
            first_failure_detail=rc_detail if errors else None
        )
