# ZMIE GRAPH-AWARE RETRIEVAL SPECIFICATION
## Graph Expansion, Controlled Traversals & Query-to-Graph Planning

---

### 1. Graph as a Retrieval Aid (Section 35)

The Knowledge Graph in ZMIE is not merely a database; it acts as an active retrieval expander:
- **Synonym & Taxonomy Expansion**: Expands concept queries across hierarchical ancestors and multilingual terms.
- **Relational Discovery**: Retrieves documents connected to directly linked targets and pathways (e.g. *Compound X* $\xrightarrow{\text{TARGETS}}$ *Protein Y* $\xrightarrow{\text{MODULATES}}$ *Pathway Z* $\xrightarrow{\text{IMPLICATED\_IN}}$ *Condition A*).
- **Cross-System Correspondences**: Discovers parallel classical monographs through governed `FUNCTIONAL_ANALOGY` edges.

---

### 2. Query-to-Graph Planner (Section 37)

The query planner converts structured clinical questions into graph constraints:

$$\text{Query: "Human evidence for Berberine in NAFLD"}$$
$$\Downarrow$$
$$\text{Entity: Berberine (CON-MOD-BERBERINE-001)}$$
$$\text{Condition: NAFLD (CON-MOD-NAFLD-001)}$$
$$\text{Evidence Level: } \ge E_5\text{ (Human observational or controlled RCT)}$$
$$\text{Predicate Filter: } [\text{TREATS}, \text{MAY\_TREAT}, \text{MODULATES}]$$

---

### 3. Graph Path Diversity Control (Section 85)

To prevent flooding downstream AI with redundant paths, the graph retrieval channel:
- Caps maximum hop depth at $k=2$ for standard queries and $k=3$ for deep research.
- Prunes collinear or parallel redundant paths, returning distinct mechanistic branches.
