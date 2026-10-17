# ZMIE SAFETY & RISK RETRIEVAL SPECIFICATION
## Pharmacovigilance, Interaction Surveillance & Red-Flag Triage

---

### 1. Safety-First Retrieval Strategy (Section 38)

Safety and interaction queries activate an elevated, conservative retrieval strategy:
- Lower threshold for alerting: emerging pharmacokinetic interactions and adverse event case reports are surfaced prominently even if overall evidence level is observational ($E_5$).
- Direct highlighting of Cytochrome P450 (CYP1A2, CYP2C9, CYP2D6, CYP3A4) and P-glycoprotein modulation.

---

### 2. Special Population Safety (Section 40)

When queries involve vulnerable populations, mandatory safety constraints are injected:
1. **Pregnancy & Lactation**:
   - Checks fetal kernicterus risk, teratogenicity, and uterine contraction stimulation.
   - Example: Berberine is flagged as `CONTRAINDICATED in pregnancy/lactation` due to bilirubin displacement.
2. **Pediatrics**:
   - Flags lack of pediatric safety data or juvenile metabolic vulnerability.
3. **Hepatic & Renal Impairment**:
   - Flags clearance alterations, dose adjustment mandates, and hepatotoxicity monitoring.

---

### 3. Red-Flag Urgent Symptom Triage (Section 39)

For potentially life-threatening or emergency symptoms (acute chest pain, stroke signs, sudden thunderclap headache):
- Intercepts general research synthesis and provides recognized urgent evaluation guidance.
- Programmatically prohibits generating autonomous diagnosis or reassuring dismissal.
