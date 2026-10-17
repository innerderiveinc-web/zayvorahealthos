# ZMIE MODERN MEDICAL ONTOLOGY SPECIFICATION
## Biomedical Semantic Classes, Hierarchies & Standards Mapping

---

### 1. Semantic Classes & Taxonomy

ZMIE structures modern biomedicine across sixteen core classes:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   BIOMEDICAL SEMANTIC DOMAINS                          │
├─────────────────────┬──────────────────────────────────────────────────┤
│ Clinical Pathology  │ Disease, Disorder, Condition, Syndrome, Phenotype│
├─────────────────────┼──────────────────────────────────────────────────┤
│ Clinical Phenotype  │ Symptom (Subjective), Sign (Objective), Finding  │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Anatomy & Physiology│ AnatomicalStructure, PhysiologicalProcess, Tissue│
├─────────────────────┼──────────────────────────────────────────────────┤
│ Molecular Biology   │ BiologicalPathway, Gene, Protein, Enzyme, Target │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Pharmacology        │ Molecule, Drug, Biologic, NaturalExtract, Vehicle│
├─────────────────────┼──────────────────────────────────────────────────┤
│ Diagnostics         │ Biomarker, LaboratoryTest, ImagingModality       │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Therapeutics        │ Intervention, Procedure, Device, DietaryProtocol │
└─────────────────────┴──────────────────────────────────────────────────┘
```

---

### 2. External Standard Vocabularies & Mapping

Where legally permitted, canonical concepts map to international reference ontologies:
- **Diseases & Conditions**: ICD-10-CM / ICD-11, SNOMED-CT, MeSH Diseases.
- **Pharmacological Agents**: RxNorm, ChEBI, DrugBank, PubChem CID.
- **Genes & Proteins**: HGNC, UniProt, Entrez Gene.
- **Pathways**: Reactome, KEGG, Gene Ontology (GO).
- **Laboratory Measures**: LOINC, UCUM units of measure.

---

### 3. Hierarchy Rules

- **`IS_A`**: Strict subsumption (e.g. *Type 2 Diabetes Mellitus* $\xrightarrow{\text{IS\_A}}$ *Diabetes Mellitus*).
- **`PART_OF`**: Mereological containment (e.g. *Islets of Langerhans* $\xrightarrow{\text{PART\_OF}}$ *Pancreas*).
- **`LOCATED_IN`**: Spatial distribution (e.g. *Peyers Patches* $\xrightarrow{\text{LOCATED\_IN}}$ *Ileum*).
- Subsumption relationships are strictly transitively inheritable, whereas associative edges are not.
