# ZMIE SOURCE REGISTRY SPECIFICATION
## Enterprise Medical & Scientific Knowledge Sources Catalog

---

### 1. Source Classification & Authority Tiers

ZMIE classifies every external and sovereign data provider into an explicit **Authority Tier (Tier A through Tier G)**. Source Authority is an indicator of institutional governance and provenance, strictly decoupled from empirical evidence grading.

| Tier | Category | Description | Primary Sources & Namespaces |
|---|---|---|---|
| **Tier A** | Official / Statutory / Regulatory | International and national statutory public health authorities, ministries, pharmacopoeias, and guideline bodies. | World Health Organization (WHO), US FDA, EMA, Ministry of Ayush (Govt of India), CDSCO, Pharmacopoeia Commission for Indian Medicine (PCIM&H), British Pharmacopoeia. |
| **Tier B** | Biomedical Repositories & Registries | Curated national and international biomedical databases, full-text repositories, and trial registries. | National Library of Medicine (NLM / PubMed), Europe PMC, PMC Open Access subset, ClinicalTrials.gov, WHO ICTRP, CTRI. |
| **Tier C** | Evidence Synthesis & Systematic Reviews | Curated secondary and tertiary evidence synthesis bodies. | Cochrane Library, Campbell Collaboration, PROSPERO, Epistemonikos. |
| **Tier D** | Primary Empirical Scholarly Graph | Peer-reviewed journals, open-access and subscription literature indexed across global bibliographic graphs. | OpenAlex (320M+ scholarly works), Crossref, Europe PMC / PubMed bibliographic records, DOI registry. |
| **Tier E** | Canonical Classical Codices | Classical medical manuscripts, historical pharmacopoeias, and traditional medical treatises. | *Al-Qanun fi al-Tibb* (Ibn Sina), *Kitab al-Hawi* (al-Razi), *Charaka Samhita*, *Sushruta Samhita*, *Huangdi Neijing*, National Formularies (NFUM, API). |
| **Tier F** | Institutional Repositories | Academic theses, university medical libraries, and hospital working papers. | PubMed Central Preprints, institutional DSpace/EPrints repositories, university dissertations. |
| **Tier G** | General Contextual Discovery | General web resources, news, and secondary commentary. | Strictly quarantined from medical claim synthesis and evidence scoring; used exclusively for discovery triage. |

---

### 2. Registered Data Connectors

```text
┌────────────────────────────────────────────────────────────────────────┐
│                     ZMIE FEDERATED SOURCE REGISTRY                     │
├──────────────────────────┬───────────────────────┬────────────┬────────┤
│ Source Identifier        │ Organization          │ Tier       │ Class  │
├──────────────────────────┼───────────────────────┼────────────┼────────┤
│ SRC-WHO-GLOBAL-001       │ World Health Org      │ Tier A     │ B      │
│ SRC-AYUSH-IN-001         │ Ministry of Ayush     │ Tier A / E │ B      │
│ SRC-CLINICALTRIALS-US-001│ NLM / NIH             │ Tier B     │ B      │
│ SRC-EPMC-001             │ EMBL-EBI / Europe PMC │ Tier B     │ C / B  │
│ SRC-OPENALEX-001         │ OurResearch OpenAlex  │ Tier D     │ C / B  │
│ SRC-COCHRANE-001         │ Cochrane Collab       │ Tier C     │ C      │
│ SRC-UNANI-CANON-001      │ Canonical Corpus      │ Tier E     │ B      │
│ SRC-AYUR-CHARAKA-001     │ Canonical Corpus      │ Tier E     │ B      │
└──────────────────────────┴───────────────────────┴────────────┴────────┘
```

---

### 3. Registry Metadata Schema

Each source registered in ZMIE must adhere to the `SourceRegistryEntry` schema:

1. **`source_id`**: Persistent UUID or canonical URN (e.g. `SRC-OPENALEX-001`).
2. **`organization`**: Operating legal entity or agency.
3. **`domain`**: Primary DNS domain or namespace.
4. **`jurisdiction`**: ISO 3166-1 alpha-2 country code or `GLOBAL`.
5. **`authority_tier`**: Enum (`TIER_A` to `TIER_G`).
6. **`license_class`**: Enum (`CLASS_A`, `CLASS_B`, `CLASS_C`).
7. **`peer_review_governed`**: Boolean flag indicating mandatory editorial governance.
8. **`retraction_monitored`**: Boolean flag indicating continuous surveillance for notices of retraction or corrigenda.
9. **`update_frequency`**: Cadence string (`realtime`, `daily`, `weekly`, `monthly`, `static`).
10. **`provenance_url`**: Canonical endpoint or gateway URI.
