# ZMIE Global Clinical & Regulatory Intelligence Suite
## Multi-Jurisdictional Authorization, Clinical Guidelines, Label Evolution & Pharmacovigilance

> **The Non-Negotiable Epistemic Maxims:**
> $$\text{Regulatory Approval} \ne \text{Scientific Proof}$$
> $$\text{Guideline Recommendation} \ne \text{Regulatory Authorization}$$
> $$\text{Regulatory Non-Approval} \ne \text{Scientific Falsehood}$$
> $$\text{Clinical Evidence} \ne \text{Regulatory Decision}$$
> $$\text{Safety Signal} \ne \text{Confirmed Causality}$$
> $$\text{Traditional Medicine Registration} \ne \text{Modern Pharmaceutical Approval}$$
> $$\text{Market Authorization in Country A} \ne \text{Global Authorization}$$
>
> *Regulatory intelligence is source-verified and informational; it does not constitute formal legal counsel or autonomous clinical prescribing.*

---

## 1. Executive Summary & Epistemic Boundaries

The **ZMIE Global Clinical & Regulatory Intelligence Engine** (Prompt 18) introduces a dedicated regulatory, clinical guidance, and pharmacovigilance intelligence layer into the platform.

It connects:
$$\text{RESEARCH} \longrightarrow \text{CLINICAL EVIDENCE} \longrightarrow \text{CLINICAL GUIDANCE} \longrightarrow \text{REGULATORY STATE} \longrightarrow \text{PRODUCT LIFECYCLE} \longrightarrow \text{SAFETY} \longrightarrow \text{REAL-WORLD EVIDENCE} \longrightarrow \text{REGULATORY CONTEXT}$$

While maintaining strict epistemic firewalls:
1. **No Global Generalization:** Never claim a product is "globally approved" or "FDA approved" without specifying the jurisdiction, authority, application/license number, approved indication, and effective date.
2. **Clinical vs Regulatory Independence:** A clinical guideline (e.g., AHA/ACC) may recommend an off-label use based on RCT evidence, but this must never be portrayed as formal regulatory approval.
3. **Safety Signal Separation:** Adverse event reports and statistical disproportionality signals are labeled `OBSERVED_SAFETY_SIGNAL` and strictly separated from `CONFIRMED_CAUSAL_RISK`.
4. **Traditional Medicine Parity:** Traditional products (Unani, Ayurveda, TCM) retain their native legal categories (e.g., India Drugs & Cosmetics Act 1940 Schedule I, AYUSH licenses) and are never falsely rewritten as conventional pharmaceuticals.
5. **No Legal Certification:** The system provides source-grounded regulatory information with uncertainty metrics, never claiming "your product is legally compliant."

---

## 2. Core Architecture & Global Authority Universe

```text
GLOBAL REGULATORY AUTHORITIES
  ├── US FDA (Drugs, Biologics, Devices, Dietary Supplements, MedWatch, DSHEA)
  ├── EU EMA (CHMP, PRAC Safety Agendas, HMPC Herbal Monographs, EPARs)
  ├── UK MHRA (Yellow Card, Device & Drug Regulations)
  ├── India CDSCO / DCGI (SUGAM, New Drugs Division, Gazette Notices, PvPI)
  ├── India Ministry of AYUSH (Ayurveda, Unani, Siddha, Homoeopathy, NAMASTE)
  ├── Japan PMDA / MHLW (Review Reports, Safety, Recalls)
  └── WHO (Global Benchmarking, Prequalification, Traditional Medicine Standards)
          │
          ▼
MULTI-JURISDICTIONAL PRODUCT RESOLUTION
  [RegulatedProduct -> ProductJurisdictionInstance per Country]
          │
          ▼
REGULATORY LIFECYCLE & LABEL DIFF ENGINE
  [Label-v1.0 -> Label-v2.0 (New Indications, Boxed Warnings, Contraindications)]
          │
          ▼
CLINICAL GUIDELINES & PATHWAYS
  [AHA/ACC, ESC, NICE, WHO, ICMR (Class of Recommendation, Level of Evidence)]
          │
          ▼
PHARMACOVIGILANCE & SAFETY COMMAND
  [Safety Communications, Dear HCP Letters, Lot/Batch Recalls]
          │
          ▼
CLAIM COMPLIANCE & LEGAL FIREWALL
  [Label Matching, Overstatement Detection, Statutory Disclaimers]
```

---

## 3. Key Subsystems

### 3.1 Multi-Jurisdictional Product Resolution & Comparison
Products often have different legal classifications, brand names, indications, and license holders across borders:
- **Dapagliflozin:** Approved as prescription drug for T2D, HFrEF/HFpEF, and CKD in the US (Farxiga, FDA NDA 202293), EU (Forxiga, EMA EMEA/H/C/002322), and India (Forxiga, CDSCO MF-ND-2015-081).
- **Berberine:** Regulated as a **Dietary Supplement** in the US under DSHEA 1994 (permitted only for structure/function claims; prohibited from disease claims) vs as a **Traditional AYUSH Medicine** in India (*Daruharidra* / *Berberis aristata* under Drugs & Cosmetics Act 1940 Schedule I).
- The engine generates a transparent `MultiJurisdictionComparisonCard` explicitly flagging cross-border classification divergences.

### 3.2 Product Label Versioning & Diff Engine
Labels evolve over time as post-marketing trials and pharmacovigilance findings emerge:
- Tracks `EFFECTIVE_FROM`, `EFFECTIVE_UNTIL`, indications, contraindications, boxed warnings, and dosage.
- Automated diff engine detects:
  - **Indications Added:** (e.g., Dapagliflozin US Label v1.0 $\rightarrow$ v2.0 added Heart Failure with reduced ejection fraction).
  - **Warnings Added:** (e.g., added warnings for necrotizing fasciitis of the perineum / Fournier's gangrene and volume depletion).

### 3.3 Clinical Guidelines Engine
- Maps source-backed clinical guidelines (AHA/ACC/HFSA 2022, ESC 2021/2023, NICE, ICMR).
- Extracts recommendation strength (`Class 1`, `Class 2a`, `Strong`) and certainty (`Level A`, `Level B-R`).
- Explicitly flags whether a guideline recommendation is `ON-LABEL` or `OFF-LABEL` relative to the approved jurisdictional label.

### 3.4 Pharmacovigilance & Batch-Level Product Recalls
- **Safety Events:** Ingests FDA MedWatch, EMA PRAC, and CDSCO PvPI safety communications (e.g. euglycemic diabetic ketoacidosis risk for SGLT2i).
- **Product Recalls:** Tracks lot numbers, manufacturers, recall classes (`Class I`, `Class II`, `Class III`), reasons (e.g. NDMA impurity exceeding acceptable intake limits), and current status (`ACTIVE`, `COMPLETED`).

### 3.5 Claim Compliance Firewall
- Evaluates user or enterprise promotional statements against verified product labels in target jurisdictions.
- Enforces DSHEA statutory limits: dietary supplements cannot claim to diagnose, treat, cure, or prevent any disease.
- Detects promotional overstatement terms: `"cures"`, `"miracle"`, `"guaranteed"`, `"permanently prevents"`.
- Appends required statutory notices (e.g. FDA DSHEA disclaimer) and mandatory legal advisories.

---

## 4. REST API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/v1/clinical-regulatory/products/{id}` | Retrieve verified product profile with all jurisdictional instances |
| `POST` | `/v1/clinical-regulatory/compare` | Compare a product across jurisdictions (US, EU, India, etc.) |
| `GET` | `/v1/clinical-regulatory/labels/{id}/diff` | Compare sequential label versions, showing added indications and warnings |
| `GET` | `/v1/clinical-regulatory/guidelines` | Query source-backed clinical guidelines and recommendation grades |
| `GET` | `/v1/clinical-regulatory/safety/{id}` | Query pharmacovigilance safety communications and boxed warnings |
| `GET` | `/v1/clinical-regulatory/recalls` | Query official lot/batch-level recall notices |
| `POST` | `/v1/clinical-regulatory/claims/check` | Claim compliance firewall: label matching and overstatement detection |

---

## 5. Verification Results

- **Unit & Acceptance Suite**: [`test_clinical_regulatory_acceptance.py`](file:///Users/irfanashraf/Downloads/zmie/tests/test_clinical_regulatory_acceptance.py) (9/9 tests passing in 0.02s).
- **End-to-End Showcase**: [`clinical_regulatory_showcase.py`](file:///Users/irfanashraf/Downloads/zmie/tests/clinical_regulatory_showcase.py) verifying all 5 operational scenarios.
- **Full Regression Suite**: **139 / 139 tests passing** across all 18 ZMIE subsystems.
