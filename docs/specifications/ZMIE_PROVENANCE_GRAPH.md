# ZMIE PROVENANCE GRAPH & CLAIM TRACE SPECIFICATION
## Unbroken Lineage, Deterministic Anchors & Reverse Traversal Architecture

---

### 1. Reverse Traversal Architecture (Section 21)

Every synthesized response and graph relationship in ZMIE can be traversed backwards to its exact textual and institutional origin:

```text
RELATIONSHIP EDGE (e.g. REL-BERB-T2D-001)
       │
       ▼
EVIDENCE OBJECT (e.g. EVD-BERB-01)
       │
       ▼
ATOMIC CLAIM PASSPORT (e.g. CLM-RCT-BERB-01)
       │
       ▼
PARAGRAPH ANCHOR HASH (SHA-256[0:16]: 8a1c90df44b1234a)
       │
       ▼
DOCUMENT SECTION & PAGE (Section: "Results - Glycemic Control", Page: 488)
       │
       ▼
DOCUMENT VERSION (DOI: 10.1016/j.metabol.2008.01.013, Version: 1.0)
       │
       ▼
SOURCE REGISTRY (SRC-NLM-001, Tier B, Class B)
```

---

### 2. Precise Structural Anchoring (Section 22)

Where document formats permit (XML, HTML, tagged PDF), ZMIE records:
- **`section_name`**: Document heading or clinical trial protocol section.
- **`page_number`**: Canonical page in original journal issue.
- **`paragraph_anchor_hash`**: 16-character SHA-256 hash derived deterministically from normalized paragraph text.
- **`character_start` / `character_end`**: Exact character offsets of the atomic assertion.

---

### 3. Claim Trace API & Signature UX (Section 49)

When a clinician, researcher, or auditor clicks on a claim in ZMIE:
1. The **Claim Trace modal** renders the complete verification passport.
2. Displays the exact quoted sentence alongside the paragraph anchor hash.
3. Shows the external DOI/PMID canonical link.
4. Confirms that the claim has passed automated Natural Language Entailment verification ($\text{NLE} \ge 0.85$).
5. Displays quarantine status (`ACTIVE_VERIFIED` vs `QUARANTINED_RETRACTED`).
