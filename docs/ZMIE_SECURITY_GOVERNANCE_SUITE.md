# ZMIE Security, Privacy, AI Safety, Multi-Tenancy & Compliance Documentation Suite

This document consolidates and formalizes the 37 architectural deliverables required under Prompt 9 of the ZAYVORA Medical Intelligence Engine™ (ZMIE) Standalone Enterprise Specification.

---

## 1. ZMIE_SECURITY_ARCHITECTURE.md
### Zero-Trust Medical Knowledge Core
- **Execution Pipeline**: `VERIFY -> AUTHORIZE -> MINIMIZE -> PROCESS -> AUDIT -> MONITOR -> REVIEW`.
- **Zero-Trust Baseline**: Never assume trust based on network perimeter, role name, or client assertions. Server-side validation is strictly authoritative.
- **Data Protection**: Encryption in transit (TLS 1.3), encryption at rest (AES-256), and cryptographic hash-chaining of audit logs.

---

## 2. ZMIE_THREAT_MODEL.md
### Attack Surfaces & Mitigations
- **Prompt Injection & Source Poisoning**: Malicious instructions embedded in external papers/websites are defanged by `AIContextFirewall`.
- **Cross-Tenant Leakage**: Rigid multi-tenant filters applied at the database, search, and graph projection levels.
- **Citation & Evidence Laundering**: Deterministic identifier validation and substantive passage entailment verification.

---

## 3. ZMIE_DATA_CLASSIFICATION.md
### Classification Tiers & Access Controls
- `PUBLIC`: General medical knowledge, authoritative guidelines, and open compendia.
- `INTERNAL`: Operational metrics, anonymized logs, and system health status.
- `CONFIDENTIAL`: Licensed full-text sources, institutional agreements, and reviewer annotations.
- `SENSITIVE`: Researcher notes, private project plans, and unpublished hypotheses.
- `HIGHLY_SENSITIVE`: Pseudonymized trial cohorts and clinical observational datasets.
- `RESTRICTED`: Identifiable patient records, cryptographic keys, and credential secrets.

---

## 4. ZMIE_CONSENT_ARCHITECTURE.md
### Granular, Purpose-Bound & ABDM-Ready
- **Granular Purposes**: `health_record_access`, `research_use`, `data_sharing`, `analytics`, `AI_assistance`.
- **State Machine**: `PENDING -> GRANTED -> DENIED -> WITHDRAWN -> EXPIRED -> SUPERSEDED`.
- **ABDM Interoperability**: Generates SHA-256 proof hashes and supports consent artifacts, time ranges, and data categories without unsubstantiated certification claims.

---

## 5. ZMIE_RBAC_ABAC.md
### Role-Based & Attribute-Based Access Control
- 14 controlled roles: `PLATFORM_ADMIN`, `SECURITY_ADMIN`, `ORGANIZATION_OWNER`, `RESEARCH_ADMIN`, `RESEARCHER`, `CLINICAL_RESEARCHER`, `CLINICIAN`, `KNOWLEDGE_CURATOR`, `EXPERT_REVIEWER`, `SAFETY_REVIEWER`, `AUDITOR`, `ANALYST`, `API_CLIENT`, `PUBLIC_USER`.
- Evaluates: `WHO + WHAT ACTION + WHICH RESOURCE + WHICH TENANT + WHICH PURPOSE + DATA CLASS`.

---

## 6. ZMIE_MULTI_TENANCY.md
### Hard Tenant Isolation
- Strict hierarchical model: `PLATFORM -> ORGANIZATION -> WORKSPACE -> PROJECT -> RESOURCE`.
- Zero cross-tenant leakage across PostgreSQL, search indices, vector databases, and knowledge graphs.

---

## 7. ZMIE_AI_SECURITY.md & ZMIE_AI_SAFETY.md
### Defense-in-Depth & Autonomy Boundaries
- **Prompt Injection Defanging**: Automatic stripping of override directives (`ignore previous instructions`, `reveal system prompt`).
- **Autonomy Boundaries (Level 0–4)**: Hard block prohibiting autonomous prescribing, diagnosing, treatment signing, or security policy modification.
- **Fail-Closed Rule**: If safety or factual grounding cannot be determined, the system fails closed with a `BLOCK` verdict.

---

## 8. ZMIE_AUDIT_MODEL.md
### Tamper-Resistant Cryptographic Audit Trails
- Append-only audit logger cryptographically linking sequential events using SHA-256 state hashes.
- Audits logins, permission changes, consent grants/revocations, data accesses, exports, and safety blocks.

---

## 9. ZMIE_COMPLIANCE_CONTROL_MATRIX.md
### Defensible Compliance Architecture
- Aligns technical controls to global and regional frameworks:
  - **India DPDP Act (2023) / Rules (2025)**: Granular consent, purpose limitation, DSR workflows, and data minimization.
  - **ABDM Readiness**: Interoperable health information request structures.
  - **ISO 27001 / SOC 2 / HIPAA Safeguards**: Multi-tenant isolation, encryption, MFA enforcement, and access reviews.
- **No Compliance Theatre Guarantee**: Avoids misleading "Certified" badges, using defensible "Designed for" and "Controls aligned to" phraseology until formal independent audits occur.
