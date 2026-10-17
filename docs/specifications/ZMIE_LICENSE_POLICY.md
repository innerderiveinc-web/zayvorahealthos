# ZMIE INTELLECTUAL PROPERTY & LICENSING POLICY
## Sovereign Legal Ingestion Matrix & Copyright Quarantine Architecture

---

### 1. Legal Ingestion Matrix (Class A, Class B, Class C)

ZMIE strictly segregates all biomedical and traditional knowledge artifacts into three legal classes prior to persistent indexing or embedding:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        ZMIE LEGAL RIGHTS MATRIX                        │
├─────────────────┬──────────────┬──────────────┬─────────────┬──────────┤
│ Legal Class     │ Full Text    │ Vector Embed │ Atomic Claim│ Outward  │
│                 │ Storage      │ Generation   │ Extraction  │ DOI Link │
├─────────────────┼──────────────┼──────────────┼─────────────┼──────────┤
│ Class A         │ YES          │ YES          │ YES         │ YES      │
│ (Licensed Full) │ (Encrypted)  │ (Full corpus)│ (Unlimited) │          │
├─────────────────┼──────────────┼──────────────┼─────────────┼──────────┤
│ Class B         │ YES          │ YES          │ YES         │ YES      │
│ (Permitted OA)  │ (Open Store) │ (Open corpus)│ (Unlimited) │          │
├─────────────────┼──────────────┼──────────────┼─────────────┼──────────┤
│ Class C         │ STRICTLY     │ ABSTRACT     │ YES         │ YES      │
│ (Restricted)    │ QUARANTINED  │ ONLY         │ (Factual)   │ (Primary)│
└─────────────────┴──────────────┴──────────────┴─────────────┴──────────┘
```

---

### 2. Class Definitions & Handling Protocols

#### Class A: Licensed Full-Text
- **Scope**: Direct institutional contracts, publisher subscriptions (e.g. Elsevier, SpringerNature, Wiley API licenses), proprietary hospital protocols.
- **Rights**: Full document storage, deep text embeddings, table/figure extraction, semantic chunking.
- **Access Control**: Encrypted at rest, decrypted solely within customer tenant boundary; never leaked across multi-tenant boundaries.

#### Class B: Permitted Open Access
- **Scope**: Creative Commons licenses (CC-BY, CC0, CC-BY-SA, Public Domain, US Federal Works).
- **Rights**: Full text ingestion, public and commercial search indexing, persistent citation caching.
- **Attribution**: Full author and institutional attribution preserved in all exported bibliographies.

#### Class C: Restricted / Closed Access (Zero-Infringement Quarantine)
- **Scope**: Copyrighted literature without active enterprise full-text licenses (subscription journals, paywalled textbooks).
- **Hard Constraints**:
  1. `full_text` is set to `None` and purged from memory buffers immediately after parsing.
  2. Full body sections and paragraph texts are **quarantined and discarded**.
  3. Stored data is limited to: Title, Authors, Publication Year, DOI, PMID, Open Abstract, Atomic Factual Claims, and Outward Canonical Links.
  4. Vector embeddings are generated **exclusively from the permitted abstract and atomic claims**, never from unauthorized full text.
  5. User-facing outputs present factual summaries accompanied by prominent direct citation links to the original publisher paywall.

---

### 3. Factual Extraction & Fair Use Standards

Under international intellectual property law (including US Title 17 § 102(b), EU Directive 96/9/EC, and Berne Convention Article 2(8)), **scientific facts, mathematical formulas, and empirical findings are not copyrightable**:
- ZMIE extracts **atomic claims** (e.g. *"Compound X inhibited enzyme Y with IC50 of 4.2 µM"*), which represent objective scientific observations.
- ZMIE never reproduces original expressive literary structure, figures, or stylistic narrative from Class C works.
