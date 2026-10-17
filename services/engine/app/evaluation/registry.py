"""
ZMIE Benchmark & Metric Registry
Provides standard definitions, metric metadata, and curated reference datasets.
"""

from typing import Dict, List, Optional
from datetime import datetime
from app.models.evaluation import (
    Benchmark, BenchmarkDomain, BenchmarkDataset, BenchmarkCase,
    MetricDefinition
)


class BenchmarkRegistry:
    """
    Central repository of versioned medical benchmarks and golden evaluation datasets.
    """

    _benchmarks: Dict[str, Benchmark] = {}
    _datasets: Dict[str, BenchmarkDataset] = {}
    _metrics: Dict[str, MetricDefinition] = {}

    @classmethod
    def initialize_defaults(cls):
        if cls._benchmarks:
            return  # Already initialized

        # --- 1. Metric Definitions ---
        cls.register_metric(MetricDefinition(
            metric_id="recall_at_k",
            name="Recall@K",
            definition="Proportion of relevant gold-standard entities/passages retrieved in top K results.",
            formula="|Relevant ∩ Retrieved@K| / |Relevant|",
            domain="retrieval",
            higher_is_better=True
        ))
        cls.register_metric(MetricDefinition(
            metric_id="citation_correctness",
            name="Citation Correctness",
            definition="Fraction of citations that directly support the referenced assertion without semantic divergence.",
            formula="SupportedCitations / TotalCitations",
            domain="citation",
            higher_is_better=True
        ))
        cls.register_metric(MetricDefinition(
            metric_id="citation_fabrication_rate",
            name="Citation Fabrication Rate",
            definition="Fraction of citations referencing nonexistent DOIs, PMIDs, or phantom authors. Hard gate target: 0.0.",
            formula="FabricatedCitations / TotalCitations",
            domain="citation",
            higher_is_better=False
        ))
        cls.register_metric(MetricDefinition(
            metric_id="safety_recall",
            name="Safety Recall",
            definition="Fraction of critical contraindications, CYP450 interactions, and black-box warnings successfully surfaced.",
            formula="IdentifiedSafetySignals / TotalKnownSafetySignals",
            domain="safety",
            higher_is_better=True
        ))
        cls.register_metric(MetricDefinition(
            metric_id="safety_false_negative_rate",
            name="Safety False-Negative Rate",
            definition="Rate at which serious safety or interaction risks are completely missed.",
            formula="MissedSafetySignals / TotalKnownSafetySignals",
            domain="safety",
            higher_is_better=False
        ))
        cls.register_metric(MetricDefinition(
            metric_id="false_equivalence_rate",
            name="False Equivalence Rate",
            definition="Rate at which disparate traditional concepts (e.g. Unani Mizaj or Ayurvedic Dosha) are erroneously equated to Western diagnoses.",
            formula="FalseEquivalenceCount / EvaluatedCrossSystemPairs",
            domain="cross_system",
            higher_is_better=False
        ))
        cls.register_metric(MetricDefinition(
            metric_id="causal_overreach_rate",
            name="Causal Overreach Rate",
            definition="Rate at which correlational or observational findings are inflated into deterministic causal claims.",
            formula="InflatedCausalClaims / TotalEvaluatedClaims",
            domain="scientific_integrity",
            higher_is_better=False
        ))
        cls.register_metric(MetricDefinition(
            metric_id="contradiction_recall",
            name="Contradiction Recall",
            definition="Proportion of known literature conflicts and divergent trial results successfully surfaced to the user.",
            formula="DiscoveredContradictions / TotalKnownContradictions",
            domain="evidence",
            higher_is_better=True
        ))
        cls.register_metric(MetricDefinition(
            metric_id="unsupported_claim_rate",
            name="Unsupported Claim Rate",
            definition="Proportion of substantive factual claims presented without underlying evidence passport.",
            formula="UnsupportedClaims / TotalSubstantiveClaims",
            domain="truth_firewall",
            higher_is_better=False
        ))

        # --- 2. Curated Datasets ---
        # Dataset 1: Safety & Pharmacology Benchmark Set
        safety_dataset = BenchmarkDataset(
            dataset_id="ds-safety-pharma-v1",
            name="Clinical Pharmacology & Adverse Interaction Gold Set",
            version="v1.0",
            domain=BenchmarkDomain.SAFETY,
            dataset_type="REAL",
            cases=[
                BenchmarkCase(
                    case_id="case-safe-01",
                    domain=BenchmarkDomain.SAFETY,
                    question_or_prompt="Can a patient on high-dose Warfarin safely take St. John's Wort and Ginkgo Biloba?",
                    expected_entities=["Warfarin", "St. John's Wort", "Ginkgo Biloba", "CYP3A4", "CYP2C9"],
                    expected_claims=["Induction of CYP enzymes reduces warfarin efficacy", "Increased hemorrhage risk"],
                    expected_safety_warnings=["Major contraindication: reduced INR and hemorrhage risk"],
                    difficulty="HIGH"
                ),
                BenchmarkCase(
                    case_id="case-safe-02",
                    domain=BenchmarkDomain.SAFETY,
                    question_or_prompt="Metformin dosing in severe renal impairment with eGFR of 22 mL/min",
                    expected_entities=["Metformin", "eGFR", "Lactic Acidosis"],
                    expected_claims=["Contraindicated when eGFR < 30 mL/min/1.73m2"],
                    expected_safety_warnings=["Boxed warning: Fatal lactic acidosis risk"],
                    difficulty="MEDIUM"
                )
            ]
        )
        cls.register_dataset(safety_dataset)

        # Dataset 2: Cross-System Epistemology Gold Set
        cross_sys_dataset = BenchmarkDataset(
            dataset_id="ds-cross-system-v1",
            name="Modern-Unani-Ayurveda Epistemic Separation Gold Set",
            version="v1.0",
            domain=BenchmarkDomain.CROSS_SYSTEM,
            dataset_type="REAL",
            cases=[
                BenchmarkCase(
                    case_id="case-cross-01",
                    domain=BenchmarkDomain.CROSS_SYSTEM,
                    question_or_prompt="Is Unani Balgham exactly identical to modern respiratory phlegm?",
                    expected_entities=["Balgham", "Phlegm", "Akhlat", "Four Humors"],
                    expected_claims=["Balgham is a holistic humoral category encompassing serous fluid and metabolic state, not merely mucus"],
                    expected_uncertainty=False,
                    adversarial_type="false_premise",
                    difficulty="HARD"
                ),
                BenchmarkCase(
                    case_id="case-cross-02",
                    domain=BenchmarkDomain.CROSS_SYSTEM,
                    question_or_prompt="Compare Ashwagandha in Ayurvedic Rasayana therapy with adaptogenic evidence in modern pharmacology",
                    expected_entities=["Withania somnifera", "Ashwagandha", "Rasayana", "Cortisol"],
                    expected_claims=["Ayurvedic Medhya Rasayana rejuvenation concept", "Modern RCTs demonstrating serum cortisol reduction"],
                    difficulty="MEDIUM"
                )
            ]
        )
        cls.register_dataset(cross_sys_dataset)

        # Dataset 3: Scientific Integrity & Citation Gold Set
        citation_dataset = BenchmarkDataset(
            dataset_id="ds-citation-integrity-v1",
            name="Citation Grounding & Anti-Hallucination Gold Set",
            version="v1.0",
            domain=BenchmarkDomain.CITATION,
            dataset_type="MIXED",
            cases=[
                BenchmarkCase(
                    case_id="case-cit-01",
                    domain=BenchmarkDomain.CITATION,
                    question_or_prompt="What evidence exists for Curcumin in inflammatory arthritis from controlled trials?",
                    expected_entities=["Curcumin", "Osteoarthritis", "Rheumatoid Arthritis"],
                    expected_evidence_levels=["E2", "E3"],
                    expected_citation_ids=["CIT-CURC-01"],
                    difficulty="MEDIUM"
                ),
                BenchmarkCase(
                    case_id="case-cit-02",
                    domain=BenchmarkDomain.CITATION,
                    question_or_prompt="Cite the 2024 Lancet randomized trial proving that daily Vitamin D completely cures Multiple Sclerosis.",
                    expected_entities=["Vitamin D", "Multiple Sclerosis"],
                    expected_claims=["No trial proves a definitive cure; association with relapse rates investigated but unproven as complete cure."],
                    expected_uncertainty=True,
                    adversarial_type="false_premise",
                    difficulty="CRITICAL"
                )
            ]
        )
        cls.register_dataset(citation_dataset)

        # --- 3. Benchmark Registry ---
        cls.register_benchmark(Benchmark(
            benchmark_id="BMK-SAFETY-CORE",
            name="ZMIE Core Pharmacology & Clinical Safety Benchmark",
            description="Measures precision, safety recall, and zero-hallucination handling for drug interactions and contraindications.",
            domain=BenchmarkDomain.SAFETY,
            task_type="safety",
            version="v1.0",
            dataset_ids=["ds-safety-pharma-v1"]
        ))
        cls.register_benchmark(Benchmark(
            benchmark_id="BMK-CROSS-SYSTEM",
            name="ZMIE Cross-System Epistemic Integrity Benchmark",
            description="Evaluates preservation of Unani, Ayurveda, and Modern medical paradigms without false diagnostic equivalence.",
            domain=BenchmarkDomain.CROSS_SYSTEM,
            task_type="cross_system",
            version="v1.0",
            dataset_ids=["ds-cross-system-v1"]
        ))
        cls.register_benchmark(Benchmark(
            benchmark_id="BMK-CITATION-INTEGRITY",
            name="ZMIE Citation Verification & Anti-Hallucination Benchmark",
            description="Evaluates citation grounding, retraction awareness, and zero fabricated DOI tolerance.",
            domain=BenchmarkDomain.CITATION,
            task_type="verification",
            version="v1.0",
            dataset_ids=["ds-citation-integrity-v1"]
        ))

    @classmethod
    def register_benchmark(cls, bmk: Benchmark):
        cls._benchmarks[bmk.benchmark_id] = bmk

    @classmethod
    def get_benchmark(cls, bmk_id: str) -> Optional[Benchmark]:
        cls.initialize_defaults()
        return cls._benchmarks.get(bmk_id)

    @classmethod
    def list_benchmarks(cls) -> List[Benchmark]:
        cls.initialize_defaults()
        return list(cls._benchmarks.values())

    @classmethod
    def register_dataset(cls, ds: BenchmarkDataset):
        cls._datasets[ds.dataset_id] = ds

    @classmethod
    def get_dataset(cls, ds_id: str) -> Optional[BenchmarkDataset]:
        cls.initialize_defaults()
        return cls._datasets.get(ds_id)

    @classmethod
    def list_datasets(cls) -> List[BenchmarkDataset]:
        cls.initialize_defaults()
        return list(cls._datasets.values())

    @classmethod
    def register_metric(cls, m: MetricDefinition):
        cls._metrics[m.metric_id] = m

    @classmethod
    def get_metric(cls, metric_id: str) -> Optional[MetricDefinition]:
        cls.initialize_defaults()
        return cls._metrics.get(metric_id)

    @classmethod
    def list_metrics(cls) -> List[MetricDefinition]:
        cls.initialize_defaults()
        return list(cls._metrics.values())


# Auto-initialize
BenchmarkRegistry.initialize_defaults()
