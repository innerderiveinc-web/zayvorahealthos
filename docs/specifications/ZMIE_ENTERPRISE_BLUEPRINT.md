# ZMIE — ZAYVORA Medical Intelligence Engine™
## Standalone Enterprise Blueprint & Master System Architecture

---

### Executive Vision & Core Philosophy

> **"Unify the world's medical knowledge without pretending that every medical system says the same thing."**
> 
> *Search once. Understand the evidence. Trace it to the source.*

ZMIE is not a chatbot, not an autonomous diagnostician, and not a flat vector search over scraped medical articles. It is a **living, source-governed medical knowledge and evidence network** that discovers, parses, reconciles, and synthesizes biomedical literature and classical traditional medicine systems (Unani, Ayurveda, TCM, Siddha) while preserving full provenance, epistemological boundaries, evidence context, contradictions, and uncertainty.

---

## 1. System Tenets & Non-Goals

### What ZMIE is NOT (v1 Guardrails)
- **NOT an AI Doctor / Autonomous Diagnostic Agent**: ZMIE does not output prescriptive or patient-specific treatment decisions autonomously. Clinical action lives in separate governed workflows.
- **NOT a Wikipedia clone or Google scraper**: It does not homogenize disparate medical theories into generic encyclopedia summaries.
- **NOT a dumb PDF warehouse**: Raw documents are decomposed into atomic, verifiable claims and graph-linked evidence units.
- **NOT a generic chatbot**: Large Language Models (LLMs) are restricted strictly to **query decomposition, semantic extraction, synthesis, and explanation**—never as the primary repository of unverified factual truth.

### Core Architectural Principle
$$\text{Source Authority} \neq \text{Claim Strength}$$
A paper published in a top-tier journal (High Source Authority) may still rely on an underpowered preclinical sample size ($n=6$) with high risk of bias (Low Claim Strength). ZMIE decouples **Source Authority Rating** from **Claim Evidence Weight**.

---

## 2. Global Topology & Product Interfaces

```
                           ┌─────────────────────────────────────────────────────────┐
                           │         ZMIE — ZAYVORA MEDICAL INTELLIGENCE ENGINE      │
                           └────────────────────────────┬────────────────────────────┘
                                                        │
           ┌────────────────────────────────────────────┼───────────────────────────────────────────┐
           ▼                                            ▼                                           ▼
┌───────────────────────────┐             ┌───────────────────────────┐               ┌───────────────────────────┐
│     Source Intelligence   │             │   Knowledge Intelligence  │               │    Evidence Intelligence  │
│  (Registry, License, PIDs)│             │ (Graph, Meshes, Ontologies)│              │  (PICO, GRADE, Synthesis) │
└─────────────┬─────────────┘             └─────────────┬─────────────┘               └─────────────┬─────────────┘
              │                                         │                                           │
              └─────────────────────────────────────────┼───────────────────────────────────────────┘
                                                        ▼
                                      ┌───────────────────────────────────┐
                                      │     Cross-System Knowledge Layer  │
                                      │ (Modern ↔ Unani ↔ Ayurveda ↔ TCM) │
                                      └─────────────────┬─────────────────┘
                                                        ▼
                                      ┌───────────────────────────────────┐
                                      │     Safety & Contradiction Engine │
                                      └─────────────────┬─────────────────┘
                                                        ▼
                                      ┌───────────────────────────────────┐
                                      │  Multi-Agent Knowledge Orchestrator│
                                      └─────────────────┬─────────────────┘
                                                        ▼
                                      ┌───────────────────────────────────┐
                                      │  Claim & Citation Verification Net │
                                      └─────────────────┬─────────────────┘
                                                        │
         ┌──────────────────────────────┬───────────────┴───────────────┬──────────────────────────────┐
         ▼                              ▼                               ▼                              ▼
┌──────────────────┐          ┌───────────────────┐           ┌───────────────────┐          ┌──────────────────┐
│   Public Search  │          │ Researcher Studio │           │ Clinical Evidence │          │ ZMIE Engine API  │
│  (Search & Why?) │          │  (Deep Workbench) │           │   (Decision Base) │          │  (REST / gRPC)   │
└──────────────────┘          └───────────────────┘           └───────────────────┘          └────────┬─────────┘
                                                                                                      │
                                                                                                      ▼
                                                                                             ┌──────────────────┐
                                                                                             │ ZAYVORA Health OS│
                                                                                             │ (Hakeem Sahab™)  │
                                                                                             └──────────────────┘
```

---

## 3. The Four Knowledge Universes

| Knowledge Universe | Core Entities & Ontologies | Primary Ingestion Anchors |
| :--- | :--- | :--- |
| **Universe 1: Modern Medicine** | Anatomy, Physiology, Pathology, ICD-11, SNOMED CT, LOINC, RxNorm, DrugBank, MeSH, Clinical Trials, Pharmacokinetics | PubMed, MEDLINE, Europe PMC, ClinicalTrials.gov, Cochrane, FDA/EMA |
| **Universe 2: Traditional Medicine** | Unani (*Mizaj*, *Afaal*, *Amraz*, *Mufradat*, *Murakkabat*), Ayurveda (*Dosha*, *Prakriti*, *Dravya*, *Agni*), TCM (*Zang-Fu*, Qi, Meridians, Herbs) | AYUSH Research Portal, WHO TMGL, TKDL, Classical Samhitas, Authorized Pharmacopoeias |
| **Universe 3: Scientific Literature** | Journal Articles, Preprints, Clinical Trials, Systematic Reviews, Meta-Analyses, Dissertations, Patents, Datasets | OpenAlex (320M+ works), Crossref, Europe PMC, Semantic Scholar |
| **Universe 4: Clinical Reality** | Phenotypes, Biomarkers, Vital Signs, Lab Panels, Multi-morbidities, Longitudinal Trajectories, Adverse Events | De-identified clinical cohorts, observational registries, EHR feeds |

---

## 4. Source Hierarchy & Ingestion Governance

Sources receive an immutable identity in the **Source Registry**:
`source_id`, `organization`, `publisher`, `domain`, `jurisdiction`, `authority_class` (Tier A–G), `license_type`, `peer_review_status`, `retraction_monitoring`.

### The 7-Tier Authority Spectrum
- **Tier A (Official Authorities)**: WHO, National Health Ministries, EMA, FDA, ICMR, NICE, Official Guideline bodies.
- **Tier B (Curated Biomedical Repositories)**: NLM, PubMed, PMC, NCBI Bookshelf, Europe PMC.
- **Tier C (Synthesized Evidence)**: Cochrane Reviews, Grade Working Group, Systematic Reviews, Meta-Analyses.
- **Tier D (Primary Empirical Literature)**: Peer-reviewed RCTs, Prospective Cohorts, In-Vivo/In-Vitro studies.
- **Tier E (Canonical Traditional Corpus)**: Authorized Classical Unani treatises (e.g., Al-Qanun fi al-Tibb), Ayurvedic Brihat Trayi (Charaka, Sushruta, Vagbhata), TCM Classics (Huangdi Neijing), Official National Ayurvedic/Unani Pharmacopoeias.
- **Tier F (Academic Institutional Knowledge)**: University Repositories, Medical Theses, Institutional Whitepapers.
- **Tier G (Open Web & Discovery)**: Discovery and supplementary indexing only; quarantined from primary evidence weighting until validated.

---

## 5. Ingestion, Licensing & Document Intelligence

```
RAW ARTIFACT (PDF, XML, HTML, EPUB)
      │
      ▼
[1. License & Rights Check] ──► Class A: Full-Text Licensed (Store & Full Analysis)
      │                     ──► Class B: Permitted OA (Store & Derivative Extraction)
      ▼                     ──► Class C: Restricted (Store metadata + abstract + outward link)
[2. SHA-256 Hash & Immutability Store] (MinIO / S3)
      │
      ▼
[3. Structural Layout Parser] (Section, Paragraph, Table, Figure, Inline Citations)
      │
      ▼
[4. Claim Extraction Pipeline]
      │
      ▼
[5. Atomic Claim Passport Generation]
```

### The Atomic Unit: The Claim Passport
Every medical and scientific fact in ZMIE is stored as a **Claim Passport**:
```json
{
  "claim_id": "CLM-2026-9812A",
  "claim_text": "Berberine chloride activates AMPK phosphorylation, resulting in downregulation of hepatic gluconeogenesis in type 2 diabetic models.",
  "document_id": "DOC-OPENALEX-W428910",
  "source_id": "SRC-PUBMED-3129841",
  "section": "Results / In-vivo Mechanism",
  "study_design": "randomized_controlled_animal_study",
  "population": { "species": "Rattus norvegicus", "condition": "induced_hyperglycemia" },
  "intervention": { "agent": "berberine_chloride", "dose": "100mg/kg", "route": "oral", "duration": "8_weeks" },
  "outcomes": [
    { "biomarker": "HbA1c", "direction": "decreased", "p_value": "<0.01", "effect_size": "-1.4%" }
  ],
  "medical_system": "modern_pharmacology",
  "evidence_tier": "preclinical_in_vivo",
  "limitations": ["small_sample_size", "rodent_model_only"],
  "supporting_sources": ["SRC-PMC-491823"],
  "contradicting_sources": [],
  "retraction_status": "clean",
  "license_status": "cc_by_4_0"
}
```

---

## 6. Cross-System Ontology & Mapping Engine

Traditional concepts are **never force-flattened** into Western biomedical equivalents. They exist in dedicated ontologies linked via explicit **Mapping Relationships**:

```
[ UNANI ONTOLOGY ]           [ CROSS-SYSTEM MAPPING LAYER ]          [ MODERN BIOMEDICAL ]
  Mizaj (Damwi/Hot-Moist) ◄───[ Functional Analogy (0.72) ]─────────► Autonomic / Metabolic Tone
  Mufrad (Zanjabeel)       ◄───[ Direct Phytochemical Target (1.0) ]──► Zingiber officinale (Gingerols)
  Daf-e-Taffun (Anti-rot)  ◄───[ Research Hypothesis (0.64) ]────────► Antimicrobial / Anti-inflammatory
```

### Permitted Mapping States
1. `Exact Equivalence` (e.g., botanical taxon to botanical taxon)
2. `Strong Relatedness`
3. `Partial Overlap`
4. `Functional Analogy` (e.g., *Mizaj Damwi* $\leftrightarrow$ vascular hyper-reactivity)
5. `Historical Association`
6. `Research Hypothesis`
7. `Conflicting / Incompatible Paradigm`
8. `No Validated Mapping`

---

## 7. Deep Research & Contradiction Resolution Engine

When a researcher initiates a study (e.g., *"Berberine vs Metformin in NAFLD"*), the **Multi-Agent Orchestrator** decomposes the investigation into parallel workers:

1. **Search & Terminology Agent**: Expands query across MeSH, SNOMED, Unani, and Ayurvedic synonyms.
2. **Evidence Collector**: Extracts PICO metrics (Population, Intervention, Comparator, Outcome) across clinical trials and systematic reviews.
3. **Contradiction Engine**: Identifies divergence in findings and clusters causes:
   - Population differences (e.g., Asian cohorts vs European cohorts)
   - Dose/formulation differences (bioavailability differences)
   - Study duration and statistical power
   - Risk of bias / sponsorship bias
4. **Citation Validator**: Verifies that every claim in the synthesis is entailed by its cited source passage, preventing hallucination and citation laundering.
5. **Research Gap Identifier**: Highlights unexplored areas (e.g., lack of long-term cardiovascular safety data past 12 months).

---

## 8. Technology Stack & Enterprise Topology

```
Frontend:
  Next.js 15 (App Router, Server Components) + TypeScript + TailwindCSS + Radix UI + Lucide

API & AI Services:
  FastAPI (Python 3.12) + Pydantic v2 + Asyncpg + Celery / Temporal (Workflows)

Data & Graph Tier:
  - PostgreSQL 16: Source Registry, Claim Passports, Document Metadata, User Projects
  - Neo4j 5.x: Knowledge Graph, Cross-System Ontology, Evidence & Citation Graph
  - pgvector / Qdrant: Dense & Sparse Embeddings (hybrid BM25 + dense vector retrieval)
  - Redis 7.x: Semantic Caching, Rate Limiting, Pub/Sub Event Stream
  - MinIO / S3: Immutable Document Store (PDF, TEI-XML, Figures)
```

---

## 9. Implementation Roadmap: 90-Day V1 Execution

```
PHASE 1: Core Foundation & Source Governance (Days 1–30)
  ├── Setup monorepo (FastAPI engine + Next.js UI)
  ├── Implement Source Registry & License Engine (Class A/B/C)
  ├── Bootstrap Connectors: OpenAlex, Europe PMC, PubMed API, AYUSH Research Portal
  └── Database schema migration (PostgreSQL + pgvector + Neo4j)

PHASE 2: Parsing, Extraction & Cross-System Engine (Days 31–60)
  ├── Document Layout Parser (tei-xml, pdf2text)
  ├── LLM Claim Extraction & Claim Passport Generator
  ├── Modern terminology (MeSH, ICD-11) + Unani/Ayurvedic ontologies
  └── Cross-System Mapping Layer & Contradiction Classifier

PHASE 3: Public Search & Research Workbench (Days 61–90)
  ├── Public Search UI ("Why this claim?" audit drawer)
  ├── Research Studio (PICO tables, Evidence Matrix, Graph Visualizer)
  ├── Citation Verification pipeline (Zero-hallucination guardrail)
  └── ZMIE Knowledge API v1 documentation and test suite
```
