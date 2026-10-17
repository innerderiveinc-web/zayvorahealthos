# ZMIE KNOWLEDGE GRAPH ARCHITECTURE SPECIFICATION
## Semantic Core & Tri-Layer Graph Subsystem

---

### 1. Architectural Philosophy

ZMIE's Semantic Core is built to answer complex medical and epistemological questions across modern and traditional medicine without collapsing distinct paradigms:

```text
SOURCE ──> DOCUMENT ──> PASSAGES ──> CLAIMS ──> ENTITIES ──> RELATIONS ──> EVIDENCE ──> ONTOLOGY
                                                                                              │
┌─────────────────────────────────────────────────────────────────────────────────────────────┘
│
▼
┌────────────────────────────────────────────────────────┐
│               TRI-LAYER SEMANTIC GRAPH                 │
├─────────────────────────┬──────────────────────────────┤
│ 1. KNOWLEDGE GRAPH      │ Entities, Concepts, Relations│
│ 2. EVIDENCE GRAPH       │ Claims, Studies, PICO, Grd E │
│ 3. PROVENANCE GRAPH     │ Document, Paragraph Hash, Ver│
└─────────────────────────┴──────────────────────────────┘
```

---

### 2. Tri-Layer Logical Separation

1. **Layer A: Medical Knowledge Graph**:
   - Manages canonical entities, concepts, hierarchies (`IS_A`, `SUBCLASS_OF`, `PART_OF`), controlled predicates, and synonyms across languages.
2. **Layer B: Evidence Graph**:
   - Manages empirical observations, study protocols, PICO contexts (Population, Intervention, Comparator, Outcome), evidence ladders ($E_0$ through $E_6$), support vs contradiction records, and disagreement reason decomposition.
3. **Layer C: Provenance Graph**:
   - Manages immutable lineage from relationship edge back through claim passport, paragraph anchor hash, document version, source authority tier, and legal licensing class.

---

### 3. Separation of Concerns & Guardrails

The architecture strictly decouples:
- **Identity $\neq$ Association $\neq$ Causation $\neq$ Functional Analogy $\neq$ Hypothesis**
- **Source Authority $\neq$ Evidence Strength $\neq$ Extraction Confidence $\neq$ Clinical Relevance**
- **Preclinical Evidence $\neq$ Human Clinical Efficacy**
