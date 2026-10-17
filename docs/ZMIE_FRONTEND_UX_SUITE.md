# ZMIE Medical Encyclopedia, Research Workbench & Evidence Map UI/UX Documentation Suite

This document formalizes the 13 required design, UX, and frontend architectural deliverables under Prompt 8 of the ZAYVORA Medical Intelligence Engine™ (ZMIE) Standalone Enterprise Specification.

---

## 1. ZMIE_DESIGN_SYSTEM.md
### Visual Identity, Tokens & Medical Esthetics
- **Design Philosophy**: Calm, Precise, Academic, Trustworthy, and Research-Grade. Rejects neon sci-fi aesthetics and generic chatbot cards.
- **Color Palette**: Dark Medical Navy background (`bg-slate-950`), Deep Slate panels (`bg-slate-900`), Medical Teal accents (`text-teal-400`, `bg-teal-500`), Muted Emerald for confirmed evidence, Indigo for trial divergences, and Amber for safety alerts.
- **Typography**: High-readability clean sans (`font-sans`) paired with monospaced numerical data (`font-mono`) and serif clinical excerpts (`font-serif italic`).

---

## 2. ZMIE_UX_ARCHITECTURE.md
### Core Principles & User Journeys
The interface visually answers five fundamental questions:
1. **WHAT DO WE KNOW?** (Governed Executive Synthesis)
2. **HOW DO WE KNOW IT?** (Direct Citation & Document Anchor Passages)
3. **WHAT EVIDENCE SUPPORTS IT?** (Structured Evidence Table with Study Designs, $n$, and Grades)
4. **WHERE DOES IT CONFLICT?** (Dedicated 'Where Evidence Differs' Contradiction Section)
5. **WHAT IS STILL UNKNOWN?** (What Remains Uncertain & Research Gap Maps)

---

## 3. ZMIE_INFORMATION_ARCHITECTURE.md
### Product Navigation & Canonical Routes
- Primary product modes: `SEARCH`, `MEDICINE`, `RESEARCH`, `EVIDENCE`, `GRAPH`, `SOURCES`, `COMPARE`.
- Canonical URLs:
  - `/` (Search-first entry point & Ask Medicine)
  - `/medicine/{slug}` (Governed Medical Encyclopedia)
  - `/research/{jobId}` (Autonomous Research Workbench)
  - `/evidence` (Tabular trial evidence explorer)
  - `/graph` (Tri-layer knowledge & evidence graph)
  - `/sources` (Provenance-tracked source registry)
  - `/compare` (Cross-system conceptual comparison)

---

## 4. ZMIE_SEARCH_UX.md
### Search-First Experience & Mode Switching
- Features "Ask Medicine" search input with mode selector:
  - **Search**: Executive synthesis and quick evidence overview.
  - **Evidence**: Dense tabular matrix of clinical and compendial studies.
  - **Safety**: Pharmacovigilance, contraindications, and CYP450 interactions.
  - **Compare**: Multi-tradition conceptual mapping with Equivalence Firewall safeguards.
  - **Deep Research**: Autonomous investigation loop with inspectable PICO plan.

---

## 5. ZMIE_ENCYCLOPEDIA_UX.md
### Governed Topic Pages
- Structured sections: Overview, Symptoms, Mechanism, Evaluation, Management, Safety, Evidence Matrix, Traditional Perspectives, Uncertainties, and Sources.
- Never displays free-form hallucinated prose; all assertions link to underlying Claim objects.

---

## 6. ZMIE_RESEARCH_WORKBENCH.md
### Multi-Stage Operating Workspace
- Exposes inspectable `ResearchPlan` before deep synthesis:
  - PICO Framework deconstruction.
  - Prioritized sub-questions (efficacy, mechanisms, safety, traditional concepts).
  - Explicit inclusion and exclusion rules.
  - Real-time status reporting (`PLANNING`, `SEARCHING`, `SCREENING`, `EXTRACTING`, `COMPLETED`).

---

## 7. ZMIE_EVIDENCE_MAP_UX.md
### Structured Evidence Table Specifications
- Columns: `Study`, `Design`, `Population`, `N`, `Intervention`, `Key Findings`, `Grade`, and `Safety`.
- Replaces vague confidence scores with the standardized ZMIE Evidence Ladder ($E_0$–$E_6$).

---

## 8. ZMIE_KNOWLEDGE_GRAPH_UX.md
### Focus-Entity Tri-Layer Visualization
- Renders focused subgraphs rather than dense unnavigable "hairballs".
- Color-coded and typed entity nodes: `COMPOUND`, `PLANT`, `CONDITION`, `UNANI CONCEPT`, `TARGET / PATHWAY`.
- Edges explicitly document relationship type and supporting Evidence Grade.

---

## 9. ZMIE_CLAIM_TRACE_UX.md
### Signature Side-Drawer Provenance Inspector
- Users can click any asserted fact or button to open the **Claim Trace Drawer**:
  - Displays the exact normalized medical components (`Subject`, `Predicate`, `Object`, `Effect`).
  - Highlights the cited source document and exact verbatim anchor passage.
  - Surfaces known study limitations and epistemic uncertainties.

---

## 10. ZMIE_SOURCE_EXPLORER_UX.md
### Transparency & Authority Tiers
- Displays source authority tier (Tier A/B/C/D), licensing boundaries, and last-checked sync timestamps.
- Zero fabrication guarantee: displays only real-world identifiers (PMID, DOI, ClinicalTrials.gov, CCRUM).

---

## 11. ZMIE_ACCESSIBILITY.md
### WCAG & A11y Standards
- High contrast foreground/background ratios exceeding WCAG AAA standards.
- Visual status indicators paired with explicit textual labels and font-mono badges (not color alone).
- Clean semantic HTML structure with keyboard-friendly drawer dismissal.

---

## 12. ZMIE_RESPONSIVE_SYSTEM.md
### Desktop & Mobile Layouts
- Fluid responsive design from mobile devices ($390\text{px}$) up to ultra-wide displays ($1440\text{px}+$):
  - Desktop: Dense multi-column tables, side-by-side comparison, and floating inspector drawers.
  - Mobile: Collapsible card layouts, vertically stacked evidence summaries, and full-screen drawer overlays.

---

## 13. ZMIE_FRONTEND_ARCHITECTURE.md
### React/Next.js Component Hierarchy & State
- Pure decoupled component architecture:
  - `NavigationHeader` (Unified top navigation)
  - `StatusBadge` (Consistent state representation)
  - `ClaimTraceDrawer` (Provenance inspector)
  - `EvidenceTable` (Tabular trial browser)
  - `ContradictionSection` (Divergence visualizer)
  - `ResearchWorkspace` (Autonomous research plan viewer)
  - `KnowledgeGraphViewer` (Tri-layer graph explorer)
