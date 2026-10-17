# ZMIE DOCUMENT VERSIONING SPECIFICATION
## Tri-Version Lifecycle, Non-Destructive Guideline History & Mutation Tracking

---

### 1. Tri-Version Lifecycle Schema

ZMIE tracks three orthogonal version dimensions for every knowledge artifact:

1. **`published_version`**:
   - The version string formally declared by the issuing organization or publisher (e.g. `2020.1`, `8th Edition`, `v3-revised`).
2. **`retrieved_version`**:
   - The timestamped snapshot identifier assigned at the moment of acquisition by ZMIE (e.g. `retrieved_20261003_180000`).
3. **`effective_version`**:
   - The active operational version recognized by the clinical decision engine (e.g. `2024.1`, or `2020.1-SUPERSEDED`, or `2022.2-RETRACTED`).

---

### 2. Mutation Classification (`ChangeType`)

When an existing document is re-scanned or a new release is fetched, `DocumentVersionTracker` computes the cryptographic delta and assigns a classification:

| ChangeType | Trigger Condition | Engine Action |
|---|---|---|
| **`NEW`** | First encounter of document identifier in ZMIE. | Full indexing, graph insertion, initial commit created. |
| **`UNCHANGED`** | Cryptographic SHA-256 hash matches previous version exactly. | No modification; updates `last_verified_at` timestamp. |
| **`UPDATED`** | Content modified without explicit retraction or supersession declaration. | Increments version index, computes section-level diff. |
| **`CORRECTED`** | Publisher issues Corrigendum / Erratum notice. | Flags specific affected claims, archives erratum notice. |
| **`SUPERSEDED`** | Issuing authority releases a new guideline version replacing a previous edition. | **Non-destructive update**: Marks older edition as `SUPERSEDED`, points `superseded_by` to the new version, points new version's `supersedes` to the old version. Historical record remains intact. |
| **`RETRACTED`** | Paper or trial is formally retracted due to misconduct or methodological failure. | Document quarantined, dependent claims flagged with clinical warning, removed from primary consensus synthesis. |
| **`REMOVED`** | Legal takedown or right-to-be-forgotten action. | Metadata retained with legal takedown tombstone notice. |

---

### 3. Non-Destructive Guideline Ingestion

A newer clinical guideline **must never silently overwrite an older guideline**:
- Example: If WHO updates hypertension thresholds from 140/90 to 130/80, clinical researchers must still be able to audit decisions made under the previous 2020 guideline.
- ZMIE preserves the full historical chain:
  `GUIDELINE-WHO-HTN-v1` (*SUPERSEDED*) $\longrightarrow$ `GUIDELINE-WHO-HTN-v2` (*ACTIVE*)
- Queries specify whether to evaluate against the *Current Effective* standard or *Historical* standard at a specific date.
