# ZMIE SEARCH EVALUATION & BENCHMARK SPECIFICATION
## Benchmark Datasets, Quality Metrics & Acceptance Validation

---

### 1. Retrieval Quality Metrics (Section 67)

ZMIE monitors eight core information retrieval and safety metrics:

| Metric | Target Standard | Operational Definition |
|---|---|---|
| **Recall@10 (Evidence)** | $\ge 92.0\%$ | Fraction of relevant human RCTs retrieved in top 10 for clinical queries. |
| **NDCG@5 (Clinical Efficacy)** | $\ge 0.88$ | Normalized discounted cumulative gain prioritizing $E_6$ controlled human trials over preclinical. |
| **Safety Retrieval Recall** | $\ge 99.0\%$ | Retrieval of documented CYP interactions and contraindications. |
| **Contradiction Recall** | $\ge 90.0\%$ | Discovery of documented conflicting studies on controversial interventions. |
| **False Equivalence Rate** | $0.0\%$ (Strict Zero) | Prevention of treating functional analogy as exact biological identity. |
| **Zero-Hallucination Rate** | $100\%$ | All citations map to verified indexed documents with valid anchor hashes. |

---

### 2. Section 116 Real-Data Acceptance Matrix

All six real-data acceptance scenarios are verified in [`tests/test_search_acceptance.py`](file:///Users/irfanashraf/Downloads/zmie/tests/test_search_acceptance.py):
- **Test A ("What is IBS?")**: Successfully returns Rome IV criteria and canonical condition entities.
- **Test B ("Human evidence for Berberine")**: Elevates double-blind human RCTs ($E_6$) to rank #1.
- **Test C ("Safety concerns of Berberine")**: Retrieves CYP3A4 competitive inhibition and pregnancy contraindication.
- **Test D ("Compare Unani and Biomedical")**: Renders comparative lens under `FUNCTIONAL_ANALOGY` without false identity.
- **Test E ("Evidence since 2022")**: Enforces temporal window filtering out pre-2022 records.
- **Test F ("Show contradictory evidence")**: Surfaces conflicting pilot trial with dose and formulation disagreement factors.
