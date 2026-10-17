# ZMIE PROVENANCE MODEL SPECIFICATION
## Cryptographic Provenance, Content Anchors & Zero Citation Laundering

---

### 1. Provenance Hierarchy

Every assertion emitted by ZMIE maintains an unbroken, verifiable audit trail back to its originating authority:

```text
SOURCE REGISTRY (e.g. SRC-NLM-001)
     │
     ▼
DOCUMENT IDENTIFIER (e.g. DOI: 10.1016/j.jep.2023.116540)
     │
     ▼
CONTENT HASH (SHA-256: 4f8b2...a90)
     │
     ▼
STRUCTURAL SECTION (e.g. "Results - Glucose Metabolism")
     │
     ▼
PARAGRAPH ANCHOR HASH (16-character SHA-256: a1e8f902cb44567d)
     │
     ▼
ATOMIC CLAIM PASSPORT (CLM-2026-X882)
     │
     ▼
AI SYNTHESIS EXPLANATION
```

---

### 2. Zero Citation Laundering Principle

In conventional LLM-based medical tools, "citation laundering" occurs when:
1. An LLM hallucinates a medical claim.
2. A retrieval mechanism conducts a post-hoc search for keywords in the hallucinated claim.
3. The LLM attaches an unrelated or tangentially related DOI as a citation, deceiving the clinician.

**ZMIE Hard Architecture Rule**:
- The Source and Claim Passport are **strictly upstream** of answer generation.
- No sentence is emitted in search or research synthesis without a verifiable `ClaimPassport` possessing:
  - Non-null `source_id`
  - Non-null `document_id`
  - Non-null `paragraph_hash`
  - Explicit `context` (PICO parameters)
- The **Citation Validator Agent** performs an automated Natural Language Entailment (NLE) score between the claim text and the exact anchored source text snippet. If entailment score is `< 0.80`, publication is aborted.

---

### 3. Structural Anchor Hashes

When documents are parsed via `DocumentParserService`, each paragraph is deterministically hashed:
$$\text{anchor\_hash} = \text{SHA256}(\text{normalized\_paragraph\_text})[0:16]$$
This allows exact verification of the exact sentence or paragraph from which a clinical fact was derived, even across revisions and format conversions.
