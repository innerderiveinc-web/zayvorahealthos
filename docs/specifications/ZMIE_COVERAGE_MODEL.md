# ZMIE SOURCE COVERAGE & EVIDENCE BLINDSPOTS MODEL
## Transparent Coverage Auditing & Explicit Retrieval Uncertainty

---

### 1. The Principle of Radical Transparency

Commercial search engines and medical chatbots frequently give users a false sense of completeness by stating: *"Based on all current medical research..."*
ZMIE firmly rejects this practice. No search system has access to all medical research.

Every research workbench investigation in ZMIE produces a mandatory **`SourceCoverageReport`**:
- **`overall_coverage_percentage`**: Ratio of queried data sources to total target sources in the medical domain.
- **`full_text_coverage_ratio`**: Proportion of identified studies where full text was accessible and legally parsed vs metadata/abstract only.
- **`latest_indexed_date`**: Exact timestamp of the freshest record indexed for this topic.
- **`sources_successfully_queried`**: List of operational endpoints with record counts.
- **`sources_unavailable_or_restricted`**: Specific namespaces that could not be reached (e.g. paywalled commercial databases, sovereign registries requiring special credentials).
- **`known_blindspots`**: Explicit bulleted caveats highlighting what the engine did not see.

---

### 2. Coverage Calculation Formula

$$\text{CoveragePct} = \frac{|\text{Sources Successfully Queried}|}{|\text{Target Sources Targeted}|} \times 100$$

$$\text{FullTextRatio} = \frac{|\text{Class A \& Class B Records}|}{|\text{Total Records Screened}|}$$

---

### 3. User-Facing Disclosure Standards

When synthesized research findings are displayed:
1. If $\text{FullTextRatio} < 0.50$, the interface displays an **Uncertainty Banner**:
   > *"Notice: 62% of identified literature in this domain is published behind commercial paywalls (Class C). Synthesis is derived from published peer-reviewed abstracts and registered trial outcomes. Original publisher links are provided for manual verification."*
2. If traditional codex databases have not yet indexed a rare herb, ZMIE explicitly states:
   > *"No canonical monograph found in Unani (NFUM) or Ayurvedic (API) pharmacopoeias for this species. Classical evidence grade is marked INSUFFICIENT."*
