# ZMIE Source Governance & Licensing Policy

## 1. Source Hierarchy (Tiers A–G)
- **Tier A**: Official Authorities & Regulators (WHO, National Ministries, Guidelines).
- **Tier B**: Curated Biomedical Repositories (NLM, PubMed Central, Europe PMC).
- **Tier C**: Evidence Syntheses (Systematic Reviews, Meta-Analyses, Cochrane).
- **Tier D**: Primary Empirical Literature (RCTs, Cohorts).
- **Tier E**: Canonical Traditional Corpora (Al-Qanun fi al-Tibb, Charaka Samhita, NFUM, API).
- **Tier F**: Academic Theses & Institutional Repositories.
- **Tier G**: General Web (Quarantined from direct evidence scoring).

## 2. Licensing Compliance Classes
- **Class A (Full-Text Licensed)**: Explicit contract allowing storage, full-text NLP, and vector indexing.
- **Class B (Open Access Permitted)**: CC-BY, CC0, or public domain allowing derivative analysis.
- **Class C (Restricted / Subscription)**: Proprietary or closed-access materials. Full text is strictly quarantined (`full_text = None`). Only legally permissible metadata, citations, and atomic extracted claims are stored.
