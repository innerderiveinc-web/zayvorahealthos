# ZMIE CANONICAL DEDUPLICATION SPECIFICATION
## Cross-Repository Identity Resolution & Version Preservation

---

### 1. Cross-Repository Deduplication (Section 28)

Identical biomedical studies frequently appear simultaneously across multiple repositories (PubMed, Europe PMC, OpenAlex, Crossref, Publisher portals). ZMIE executes deterministic entity deduplication:

$$\text{Identity Matching Key} = \text{DOI} \lor \text{PMID} \lor \text{NCT\_ID} \lor (\text{TitleSimilarity} \ge 0.95 \land \text{AuthorMatch})$$

- **Non-Destructive Provenance**: When duplicates are merged into a canonical result, originating source representations are **never deleted**.
- A merged record stores:
  $$\text{canonical\_publication} \longrightarrow [\text{source}_1 (\text{NLM}), \text{source}_2 (\text{Europe PMC}), \text{source}_3 (\text{OpenAlex})]$$

---

### 2. Version-Aware Deduplication (Section 29)

The engine strictly distinguishes:
- `PREPRINT` (e.g. bioRxiv, medRxiv)
- `ACCEPTED_MANUSCRIPT`
- `VERSION_OF_RECORD` (Formal published journal paper)
- `CORRIGENDUM / ERRATUM`
- Preprints and formal versions of record are linked via supersession edges, never collapsed into identical objects.
