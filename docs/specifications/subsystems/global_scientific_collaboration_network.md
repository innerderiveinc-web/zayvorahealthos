# ZMIE Global Scientific Collaboration & Research Network Engine

## Overview & Scientific Mission

The **ZMIE Global Scientific Collaboration & Research Network Engine** (Prompt 22 Implementation) transforms ZMIE from a passive indexer of bibliographic citations into a living scientific collaboration intelligence operating layer:

$$\text{Who is actually connected to what scientific work, expertise, institution, project, dataset, technology, grant, trial, laboratory, and research frontier?}$$

Rather than reducing researchers to crude publication counts or subjective prestige indices, ZMIE models the multi-dimensional, temporal, and evidence-backed fabric of global scientific production across modern biomedicine, systems biology, and traditional medical paradigms (Unani Medicine, Ayurveda, and Traditional Chinese Medicine).

---

## Core Non-Negotiable Epistemic Principles & Boundaries

ZMIE operates under strict epistemic firewalls that distinguish between observed factual data and ungrounded inferences:

1. **State Disambiguation**:
   $$\text{PUBLICLY\_OBSERVED} \neq \text{INFERRED} \neq \text{UNKNOWN / PRIVATE}$$

2. **Negative Proof Fallacy Guard**:
   $$\text{"No public publication found"} \neq \text{"Not researching this"}$$
   An absence in indexed commercial databases (PubMed, Scopus) indicates `SPARSE_IN_INDEXED_SOURCES`. It does **not** assert nonexistence or absence in regional councils, historical pharmacopoeias, or private research archives.

3. **Expertise Evidence Fallacy Guard**:
   $$\text{"Published once on X"} \neq \text{"Expert in X"}$$
   Expertise is multi-dimensional (`DOMAIN`, `TOPIC`, `METHOD`, `TECHNOLOGY`, `DISEASE`, `POPULATION`, `GEOGRAPHY`) and requires persistent, verified trial, grant, and publication output evidence.

4. **Collaboration Fallacy Guard**:
   $$\text{"Co-authored once"} \neq \text{"Active ongoing collaboration"}$$
   Co-authorship is an observed historical artifact. Ongoing collaboration requires recency decay scoring, shared ongoing clinical trials, or co-investigated grant awards.

5. **Institutional Endorsement Fallacy Guard**:
   $$\text{"Affiliated with Institution X"} \neq \text{"Institution officially endorses researcher's claims"}$$

6. **Anti-Ranking Policy Guarantee**:
   ZMIE strictly bans arbitrary researcher rankings (`"Top Scientist"`, `"Best Researcher"`, `"#1 Expert"`). Any attempt to generate subjective rankings triggers the `ForbiddenRankingException`.

---

## Architectural Subsystems

```text
                               ┌────────────────────────────────────────────────────────┐
                               │     ZMIE Global Scientific Collaboration Engine        │
                               └──────────────────────────┬─────────────────────────────┘
                                                          │
          ┌───────────────────────┬───────────────────────┼───────────────────────┬───────────────────────┐
          ▼                       ▼                       ▼                       ▼                       ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│    Identity      │    │    Temporal      │    │ Multi-Dimensional│    │  Collaboration   │    │ Cross-Disciplinary│
│  Disambiguation  │    │  Affiliations    │    │    Expertise     │    │ Topology & Decay │    │     Bridges      │
│  & ORCID Guard   │    │  & Provenance    │    │ & Anti-Ranking   │    │ (1st/2nd Degree) │    │ & Clusters       │
└──────────────────┘    └──────────────────┘    └──────────────────┘    └──────────────────┘    └──────────────────┘
          │                       │                       │                       │                       │
          └───────────────────────┴───────────────────────┼───────────────────────┴───────────────────────┘
                                                          ▼
                                        ┌──────────────────────────────────┐
                                        │    Snapshotting, Graph Diff,     │
                                        │   & Multi-Tenant Firewall        │
                                        └──────────────────────────────────┘
```

### 1. Disambiguated Identity Resolution
- Direct authoritative matching via verified ORCID (`0000-0002-1234-5678`).
- Multi-signal heuristic matching (canonical names, transliterated aliases, institutional affiliations, topic overlap).
- **Contestation Guard**: When multiple distinct individuals share names without distinguishing ORCID, entities are marked `CONTESTED` to prevent false merges.
- Unindexed individuals are captured as prospective `CANDIDATE` nodes without false identity linkage.

### 2. Chronological Temporal Affiliations
- Tracks chronological history with explicit `start_year`, `end_year`, and `is_current` flags.
- Distinguishes appointment statuses: `PRIMARY`, `SECONDARY`, `VISITING`, `EMERITUS`, `HISTORICAL`.
- Preserves appointment provenance sources (`FACULTY_REGISTRY`, `CLINICAL_TRIAL_AGREEMENT`, `GRANT_AWARD`).

### 3. Multi-Dimensional Evidence-Backed Expertise
- Indexes expertise along seven dimensions: `DOMAIN`, `TOPIC`, `METHOD`, `TECHNOLOGY`, `DISEASE`, `POPULATION`, `GEOGRAPHY`.
- Backed strictly by persistent source identifiers (e.g. trial registries `CTRI/2021/04/032111`, `NCT04561288`, `doi:10.1016/j.jep.2023.116543`, `NIH-R01-DK128901`).
- Enforces the `verify_no_subjective_ranking()` firewall.

### 4. Collaboration Topology & Recency Decay
- Tracks collaboration types: `COAUTHORED`, `COINVESTIGATED`, `COFUNDED`, `CODEVELOPED`, `SHARED_DATASET`, `SHARED_PROJECT`, `SHARED_TRIAL`, `SHARED_METHOD`, `CONSORTIUM_MEMBER`.
- Time-decay weighting based on activity recency:
  $$\text{weight} = e^{-0.1 \times (\text{current\_year} - \text{last\_active\_year})}$$
- Distinguishes direct 1st-degree collaborators from 2nd-degree indirect collaborator networks.

### 5. Cross-Disciplinary Bridge Discovery
- Unearths researcher nodes spanning disparate epistemological domains (e.g. Unani Medicine + UPLC-MS/MS Phytochemistry + Metabolic Pharmacology; or Clinical Oncology + AI).
- Highlights vital translational conduits often missed by siloed academic databases.

### 6. Research Clusters & Thematic Collaboratories
- Detects dense topological subgraphs connecting researchers, institutions, shared methodologies, and joint clinical trials.
- Reports cluster cohesion metrics, dominant analytical methods, and active member registries.

### 7. Epistemic Research Gap Mapping
- Distinguishes `WELL_REPRESENTED`, `EMERGING`, and `SPARSE_IN_INDEXED_SOURCES`.
- Appends mandatory epistemic disclaimer preventing the misinterpretation of unindexed regional literature as nonexistent research.
- Recommends actionable investigative inquiry paths (e.g., querying traditional medicine councils, regional archives, or historical pharmacopoeias).

### 8. Network Snapshotting & Graph Diffing
- Versioned point-in-time network snapshots (`Baseline-2024` vs `Evolution-2025`).
- Precise diff engine isolating new researcher nodes, emerging collaboration edges, strengthened partnerships, and cluster evolutions.

### 9. Multi-Tenant Privacy Firewall
- Zero web scraping of private communications.
- Complete multi-tenant isolation: `TENANT_PRIVATE` entities and collaboration edges are strictly invisible to public queries or foreign tenant queries.

---

## REST API Reference (`/v1/network`)

| Endpoint | Method | Description |
|---|---|---|
| `/v1/network/researchers/resolve` | `POST` | Disambiguates researcher identity via ORCID, name variants, institutional cues, and topic hints |
| `/v1/network/researchers/{id}` | `GET` | Retrieves full researcher identity profile and evidence-backed expertise |
| `/v1/network/researchers/{id}/timeline` | `GET` | Retrieves chronological temporal affiliations with start/end years and provenance |
| `/v1/network/researchers/{id}/collaborations`| `GET` | Retrieves direct (1st degree) and indirect (2nd degree) collaboration graph with recency decay |
| `/v1/network/institutions/{id}` | `GET` | Retrieves disambiguated institutional identity, departments, and labs |
| `/v1/network/expertise/search` | `POST` | Searches evidence-backed expertise with strict anti-ranking guarantees |
| `/v1/network/bridges/cross-disciplinary` | `GET` | Discovers researchers spanning multiple distinct disciplines |
| `/v1/network/clusters` | `GET` | Discovers thematic research clusters and institutional collaboratories |
| `/v1/network/gaps` | `GET` | Evaluates public literature representation (`SPARSE_IN_INDEXED_SOURCES`) |
| `/v1/network/snapshot` | `POST` | Captures immutable point-in-time network snapshot |
| `/v1/network/diff` | `GET` | Computes topological diff between two network snapshots |

---

## Verification & Conformance

- **Unit & Acceptance Suite**: `tests/test_collaboration_network_acceptance.py` (21 tests, 100% passing).
- **Showcase & Demonstration**: `tests/collaboration_network_showcase.py` (Verified end-to-end).
- **Full Engine Regression**: 192 / 192 tests passing across all 22 subsystem prompts in 0.248s.
- **Route Count**: 232 registered FastAPI endpoints.
