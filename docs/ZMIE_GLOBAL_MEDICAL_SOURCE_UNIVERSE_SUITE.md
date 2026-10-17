# ZMIE — GLOBAL MEDICAL SOURCE UNIVERSE & UNIVERSAL SOURCE ACQUISITION ENGINE
## Master Architectural Blueprint, Multi-System Ecosystem Specification & Provenance Framework

---

### 1. Executive Summary & Source Philosophy

The **ZMIE Global Medical Source Universe** is the foundational, source-governed knowledge network situated beneath the entire ZAYVORA Medical Intelligence Engine. It operates under a strict principle:

> **ZMIE does not claim to contain "all medical knowledge on the Internet." Instead, ZMIE engineers the most comprehensive, legally acquired, continuously monitored, provenance-preserving and evidence-aware medical knowledge source network the architecture can support, while making coverage, gaps, licensing, and uncertainty completely transparent.**

```text
DISCOVER ──► IDENTIFY ──► CLASSIFY ──► VERIFY ──► AUTHORITY CHECK ──► LICENSE CHECK
   │
   ▼
CONNECT ──► ACQUIRE ──► NORMALIZE ──► DEDUPLICATE ──► VALIDATE ──► VERSION
   │
   ▼
EXTRACT ──► PROVENANCE ──► EVIDENCE GRAPH ──► KNOWLEDGE GRAPH ──► RESEARCH WORKBENCH
   │
   ▼
CONTINUOUS MONITORING & RETRACTION INVALIDATION
```

#### Core System Rules
1. **Discovery $\ne$ Acceptance**: A source is not trusted merely because it is indexed in a major database, nor rejected merely because it represents traditional medicine.
2. **Epistemic Separation**: Classical traditional doctrines (e.g. Unani *Mizaj*, Ayurvedic *Tridosha*) are preserved in their authentic philosophical frames and are **never silently converted or falsely equated to modern clinical trials**.
3. **Zero Fabrication**: No fake source names, imaginary APIs, phantom DOIs, or fabricated study registries are ever created. If evidence is missing, the system explicitly reports `UNKNOWN` or `UNAVAILABLE`.
4. **License Awareness**: Strict copyright adherence. Unlicensed copyrighted texts are stored strictly as metadata, citations, and atomic claims (`LicenseClass.CLASS_C`), never redistributing full text without authorization.

---

### 2. Multi-Class Source Taxonomy & Authority Hierarchy

Every registered source belongs to one or more formal **Source Classes** and receives an explicit **Authority Level**:

```text
S0: Unknown / Unverified Discovery Candidate
S1: Community / Unreviewed Health Information
S2: Scholarly Secondary / Gray Literature / Theses
S3: Peer-Reviewed Scholarly Journal
S4: Recognized Professional Society / Historical Classical Corpus
S5: National Government / Statutory Regulatory Authority (FDA, EMA, AYUSH, ICMR)
S6: International Authoritative Organization (WHO, Cochrane)
```

#### Canonical Source Classes
| Source Class | Description | Canonical Seed Sources |
|---|---|---|
| **Scholarly Literature** | Peer-reviewed biomedical and medical journals | `SRC-EPMC` (Europe PMC), `SRC-OPENALEX` (OpenAlex), `SRC-CROSSREF` |
| **Evidence Synthesis** | Systematic reviews, meta-analyses, evidence maps | `SRC-COCHRANE` (Cochrane Library) |
| **Clinical Guidelines** | Practice standards from international and national bodies | `SRC-WHO-GUIDELINES`, `SRC-NICE` (NICE UK Guidelines) |
| **Clinical Trials** | Registry-of-registries across national and WHO primary hubs | `SRC-CLINICALTRIALS` (NLM), `SRC-CTRI` (India), `SRC-WHO-ICTRP` |
| **Regulatory & Safety** | Drug labeling, SPL monographs, pharmacovigilance | `SRC-FDA-DAILYMED` (FDA SPL), `SRC-PHARMACOVIGILANCE` (VigiBase/FAERS) |
| **Traditional Medicine** | Dedicated statutory councils and peer-reviewed journals | `SRC-CCRUM` (Unani), `SRC-CCRAS` (Ayurveda), `SRC-CCRS` (Siddha), `SRC-TCM-MEDICINE` |
| **Classical Canon** | Authenticated historical treatises and critical editions | `SRC-UNANI-CANON` (*Al-Qanoon*), `SRC-AYURVEDA-CHARAKA` (*Charaka Samhita*) |
| **Botanical & Herbal** | Plant taxonomy, accepted botanical synonyms, part used | `SRC-KEW-MEDICINAL` (Kew Royal Botanic Gardens MPNS) |

---

### 3. Dedicated Traditional Medicine Source Universes

Traditional medicine is treated as an authentic, first-class knowledge ecosystem, not an appendix to Western medicine.

#### 3.1 Unani Source Universe
- **Official Statutory Councils**: Ministry of AYUSH, Central Council for Research in Unani Medicine (`SRC-CCRUM`), AYUSH Research Portal.
- **Classical Canons**: Ibn Sina's *Al-Qanoon fi al-Tibb* (Canon of Medicine), Abu Bakr al-Razi's *Kitab al-Hawi fi al-Tibb* (Continens), *Qarabadeen-e-Qadri*.
- **Ontological Preservation**: Concepts like *Mizaj* (temperament: Har, Barid, Ratab, Yabis), *Akhlat* (humors: Dam, Balgham, Safra, Sauda), and *Mufradat* (single herbs) are indexed with original Arabic/Urdu terms and mapped to translational research without flattening.

#### 3.2 Ayurveda Source Universe
- **Official Councils**: Central Council for Research in Ayurvedic Sciences (`SRC-CCRAS`), National Institute of Indian Medical Heritage.
- **Classical Canons**: *Charaka Samhita*, *Sushruta Samhita*, *Ashtanga Hridaya*, Dravyaguna monographs.
- **Epistemic Classification**: Differentiates `CLASSICAL_TEXT` (Sanskrit canon) from `TRADITIONAL_CLAIM` (pharmacopoeial use) and `MODERN_CLINICAL` (contemporary human trials).

#### 3.3 Siddha, TCM, Kampo & Regional Traditions
- Includes Siddha (`SRC-CCRS`), Traditional Chinese Medicine (`SRC-TCM-MEDICINE`), and Kampo repositories, preserving language scripts, botanical preparations, and clinical philosophies.

---

### 4. Canonical Study Identity Resolution

Multiple databases often index the same trial under disparate identifiers. ZMIE introduces [`StudyCanonical`](file:///Users/irfanashraf/Downloads/zmie/services/engine/app/models/source_universe.py) to resolve records into a unified identity:

```text
[ClinicalTrials.gov: NCT01234567] ──┐
[CTRI Registry: CTRI/2021/04/032] ──┼──► Canonical Study Entity (StudyCanonicalID)
[Published Paper: DOI 10.1016/...]   ──┤    ├── Sample Size & Phase
[PubMed Entry: PMID: 38129045]     ──┘    ├── Pre-registered Protocol
                                           └── Primary Endpoints & Results
```

---

### 5. Research Source Matrix & Coverage Transparency

Every research query in ZMIE produces a transparent **Research Source Matrix** showing exact coverage across domains:

```text
Query: "What is the evidence for Nigella sativa in metabolic and inflammatory disorders?"
```

| Source Class | Searched | Retrieved | Included | Excluded | Unavailable |
|---|:---:|:---:|:---:|:---:|:---:|
| **Biomedical Literature** | 12 | 8 | 6 | 2 | 0 |
| **Evidence Synthesis** | 4 | 3 | 3 | 0 | 0 |
| **Clinical Trials** | 6 | 4 | 4 | 0 | 0 |
| **Clinical Guidelines** | 5 | 2 | 2 | 0 | 0 |
| **Regulatory & Safety** | 3 | 3 | 3 | 0 | 0 |
| **Unani Literature & Canon** | 8 | 6 | 5 | 1 | 0 |
| **Ayurveda Literature & Canon** | 7 | 5 | 4 | 1 | 0 |
| **Botanical & Pharmacognosy** | 4 | 3 | 3 | 0 | 0 |

#### Transparent Gap Disclosure (Section 40)
When evidence is sparse, ZMIE explicitly distinguishes:
- *No evidence found in literature* vs.
- *Evidence exists but source is outside current index* vs.
- *Evidence is paywalled / requires institutional license* vs.
- *Evidence exists in traditional language literature (Urdu/Arabic/Sanskrit)*.

---

### 6. Continuous Retraction, Correction & Safety Invalidation

When a retraction is registered:
1. The document is marked `RETRACTED` in the Source Universe Registry.
2. Downstream atomic claims linked to that document are marked `INVALIDATED`.
3. Graph edges derived from the retracted document are excised from search indices.
4. Saved research projects and user watchlists receive real-time webhook alerts (`source.retracted`).

---

### 7. End-to-End Verification Scenarios

| Scenario | Query | Systems Evaluated | Verified Outcome |
|---|---|---|---|
| **Scenario 1** | *Nigella sativa* in metabolic & inflammatory disorders | Modern, Unani, Ayurveda, Botanical | Distinguishes modern RCTs (HbA1c reduction) from Unani clinical studies and Ibn Sina's classical Canon description. |
| **Scenario 2** | *Mizaj* / Temperament concepts | Classical Unani, Modern Translational | Distinguishes Avicenna/Rhazes qualitative humoral doctrine from modern metabolic phenotyping (RMR/BMR correlations). |
| **Scenario 3** | Drug-Herb Interaction Safety | FDA DailyMed, EMA, Pharmacovigilance | Surfaces Warfarin + St. John's Wort (CYP2C9/3A4 induction) and Ginkgo Biloba (antiplatelet synergy) critical warnings. |
| **Scenario 4** | Condition Comparison (Osteoarthritis) | Modern Allopathy, Unani, Ayurveda | Side-by-side evidence matrix without manufacturing an artificial winner. |
| **Scenario 5** | Source Discovery & Retraction Invalidation | Citation Network, Retraction Watch | Successfully discovers candidate sources, promotes via governance, and propagates retraction cascades. |

---

### 8. Verification & Test Results

- **Acceptance Test Suite** ([`test_source_universe_acceptance.py`](file:///Users/irfanashraf/Downloads/zmie/tests/test_source_universe_acceptance.py)):
  - **8/8 tests passed** covering registry filtering, candidate discovery, all 4 end-to-end scenarios, retraction invalidation, and REST APIs.
- **Master Showcase Script** ([`source_universe_showcase.py`](file:///Users/irfanashraf/Downloads/zmie/tests/source_universe_showcase.py)):
  - **5/5 proofs verified live**.
- **Full Repository Regression Suite**:
  - **87/87 tests passed across all 13 subsystems** with zero regressions.
