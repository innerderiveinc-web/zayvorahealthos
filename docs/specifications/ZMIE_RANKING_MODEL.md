# ZMIE RANKING MODEL & SCORE EXPLANATION SPECIFICATION
## Intent-Adaptive Multi-Dimensional Reranking & Human-Readable Explanations

---

### 1. Multi-Dimensional Scoring Formula (Section 25)

ZMIE rejects single-dimension BM25 or cosine similarity scores. Candidates are ranked using a multi-dimensional objective function:

$$\text{FinalScore} = w_{\text{lex}} S_{\text{lex}} + w_{\text{ent}} S_{\text{ent}} + w_{\text{auth}} S_{\text{auth}} + w_{\text{evd}} S_{\text{evd}} + w_{\text{graph}} S_{\text{graph}} + w_{\text{fresh}} S_{\text{fresh}} - P_{\text{retract}}$$

Where:
- $S_{\text{auth}}$ is determined by Source Authority Tier ($1.0$ for Tier A statutory bodies; $0.9$ for Tier B repositories; $0.85$ for Tier E classical codices).
- $S_{\text{evd}}$ is determined by the Evidence Ladder ($1.0$ for $E_6$ human RCTs; $0.8$ for $E_5$ observational; $0.6$ for $E_4$ preclinical; $0.4$ for $E_3$ in-vitro).
- $S_{\text{fresh}}$ is context-dependent: decays over 25 years for modern clinical guidelines, but remains $0.90$ for canonical traditional codices.
- $P_{\text{retract}} = 1.0$ penalty if retracted.

---

### 2. Intent-Adaptive Weighting Profiles (Section 24)

| Query Intent Profile | $w_{\text{evd}}$ | $w_{\text{auth}}$ | $w_{\text{lex}}$ | $w_{\text{ent}}$ | $w_{\text{fresh}}$ | Ranking Focus |
|---|---|---|---|---|---|---|
| **EVIDENCE / TREATMENT** | **0.35** | **0.20** | 0.15 | 0.15 | 0.15 | Human double-blind RCTs and meta-analyses. |
| **SAFETY / INTERACTION** | 0.25 | **0.30** | 0.15 | 0.15 | 0.15 | Regulatory alerts, CYP450, contraindications. |
| **GUIDELINE** | 0.20 | **0.40** | 0.15 | 0.15 | 0.10 | Tier A statutory guidance (WHO, CDSCO, FDA). |
| **TRADITIONAL MEDICINE** | 0.20 | **0.35** | 0.15 | 0.15 | 0.15 | Canonical codices (*Al-Qanun*, *Charaka*). |
| **MECHANISM** | 0.20 | 0.20 | 0.20 | **0.25** | 0.15 | Receptor binding, target pathways ($E_3, E_4$). |

---

### 3. "Why This Result?" Human-Readable Explanation (Section 27)

Every ranked result translates component scores into clear clinical reasons:
> *"High-quality controlled clinical evidence (double_blind_rct) | Authoritative statutory repository (National Library of Medicine / PubMed) | Direct concept match on query entities (Berberine, Type 2 Diabetes Mellitus)"*
