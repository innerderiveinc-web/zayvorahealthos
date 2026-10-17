# Contributing to ZMIE (ZAYVORA Medical Intelligence Engine)

Thank you for your interest in contributing to **ZMIE** — the enterprise-grade Scientific Knowledge Operating System for Medicine and Life Sciences.

ZMIE enforces rigorous scientific standards, security boundaries, and enterprise software engineering practices. Please review this guide thoroughly before submitting any code, documentation, or architecture proposals.

---

## 1. Code of Conduct & Scientific Integrity Rider

ZMIE operates under a strict **Zero-Fabrication Doctrine**:
- **Never fabricate scientific literature, clinical trials, dosages, or molecular pathways.**
- If evidence is uncertain, inconclusive, or conflicting, it must be explicitly represented as `UNCERTAIN`, `DISPUTED`, or `UNKNOWN`.
- Traditional medicine concepts (Unani, Ayurveda, TCM) must never be falsely conflated with modern biochemical targets without explicit mechanistic justification and epistemic distance scoring.
- Never bypass or weaken tenant boundaries, privacy-preserving aggregation layers, or HIPAA/GDPR safeguards.

---

## 2. Branching Strategy

ZMIE uses a structured branch model (per Prompt 28 Clause 87):

- `main`: Protected production branch. All merges require passed CI, security checks, and 2 peer approvals.
- `release/vX.Y.Z`: Release candidate stabilization branch.
- `feature/<module-id>-<slug>`: Active feature work (e.g., `feature/mod-02-jwt-auth`).
- `fix/<issue-id>-<slug>`: Bug fixes (e.g., `fix/sec-tenant-isolation-leak`).
- `hotfix/<cve-or-incident>`: Critical production hotfixes cherry-picked to `main` and active release branches.

---

## 3. Commit Message Standards

ZMIE strictly adheres to Conventional Commits:

```text
<type>(<scope>): <short description>

[optional detailed body explaining scientific/engineering rationale]

[optional issue/ticket reference]
```

Valid `<type>` values:
- `feat`: New module, endpoint, or engine capability.
- `fix`: Bug fix, logic correction, or security patch.
- `docs`: Documentation updates, architecture decision records.
- `test`: Addition or modification of unit, integration, or acceptance tests.
- `refactor`: Code reorganization with zero change to external API contracts.
- `perf`: Computational performance or latency optimization.
- `sec`: Security hardening, RBAC/ABAC updates, vulnerability fixes.
- `chore`: Dependency updates, tooling, or build configuration.

Examples:
- `feat(auth): implement JWT RS256 token issuance and ABAC policy engine`
- `fix(rwe): eliminate Pydantic V2 model_dump deprecation in FHIR bundle export`
- `test(isolation): add 4-way cross-tenant boundary regression suite`

---

## 4. Pull Request Checklist & Template

Every Pull Request must fill out the standard PR template (Clause 85):

```markdown
### Summary of Changes
- Detailed bullet points of modifications

### Module Reference
- [ ] Module ID: (e.g., MODULE 02 — Identity & Authentication)
- [ ] Prompt Clause(s): (e.g., Clauses 13, 15, 16)

### Invariant Verification
- [ ] INV-01: Zero Fabrication Verified (No fake data or synthetic citations)
- [ ] INV-02: Tenant Isolation Enforced (No cross-tenant data leakage)
- [ ] INV-03: Immutable Provenance Logged (All state changes emit audit events)
- [ ] INV-04: Epistemic Distance Preserved (No false traditional-biomedical conflation)

### Testing & Quality Gates
- [ ] Unit Tests Passed (`make test`)
- [ ] Acceptance Suite Passed (`make test-acceptance`)
- [ ] Lint & Typecheck Passed (`make lint`, `make typecheck`)
- [ ] 0 Regressions across existing 288+ test baseline
```

---

## 5. Local Development Workflow

1. **Bootstrap Environment:**
   ```bash
   make dev
   ```
2. **Run All Verification Suites:**
   ```bash
   make verify-all
   ```
3. **Execute Single Acceptance Test:**
   ```bash
   .venv/bin/python3 -m unittest tests/test_production_build_acceptance.py
   ```
