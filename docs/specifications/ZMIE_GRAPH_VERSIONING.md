# ZMIE GRAPH VERSIONING & KNOWLEDGE DIFF SPECIFICATION
## Versioned Graph Releases, Deterministic Rebuilds & Impact Analysis

---

### 1. Release Manifest Model (Section 65)

Every formal knowledge graph release publishes a cryptographic manifest containing:
- **`graph_version`**: e.g. `2026.2.0`
- **`knowledge_version`**: Commit hash of the underlying relational database state.
- **`ontology_version`**: Version tag of the cross-system concept definitions.
- **`evidence_version`**: Version tag of the trial and study indexing corpus.
- **`release_date`**: ISO 8601 UTC timestamp.
- **`change_set_summary`**: Quantitative count of new concepts, edges, and evidence additions.
- **`review_status`**: Sign-off certification from the Medical Governance Council.

---

### 2. Knowledge Diff Engine (Section 63)

Researchers can compare any two historical releases:

$$\Delta = \text{Diff}(\text{Release}_A, \text{Release}_B)$$

The engine computes:
1. **New Concepts**: Added pharmacological agents, conditions, or newly digitized classical terms.
2. **Deprecated / Merged Concepts**: Obsolete or harmonized concepts.
3. **New Relations**: Newly identified clinical efficacy or mechanistic edges.
4. **Modified Evidence Grades**: Upgraded (e.g. $E_5 \rightarrow E_6$) or downgraded relations.
5. **New Contradictions**: Divergent clinical trial results indexed between releases.
6. **Retracted Evidence**: Quarantined studies and invalidations.

---

### 3. Deterministic Graph Rebuild (Section 66)

Given:
$$\text{Relational Store}(K) + \text{Ontology Release}(O) + \text{Projection Version}(G)$$
ZMIE's projection workers deterministically recreate the exact graph database projection state identically on any server, ensuring full reproducibility and auditability.
