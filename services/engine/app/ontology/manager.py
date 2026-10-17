"""
ZMIE Ontology Lifecycle, Terminology & Governance Manager (Sections 30-34)
Maintains:
- Concept Lifecycle: PROPOSED -> ACTIVE -> DEPRECATED -> SUPERSEDED -> MERGED -> SPLIT
- Merge & Split Governance (preserves historical references without destruction)
- Multilingual Terminology and Synonym indexing (Arabic, Urdu, Sanskrit, Chinese, Latin, English)
- Versioned Ontology Releases
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.graph import (
    CanonicalConcept, MedicalTerm, ConceptLifecycleStatus,
    SynonymType, HierarchyPredicate
)
from app.models.claim import MedicalSystem


class OntologyRelease(BaseModel):
    ontology_version: str
    release_date: datetime = Field(default_factory=datetime.utcnow)
    total_concepts: int
    total_terms: int
    new_concepts: List[str] = Field(default_factory=list)
    deprecated_concepts: List[str] = Field(default_factory=list)
    merged_concepts: List[Dict[str, Any]] = Field(default_factory=list)
    split_concepts: List[Dict[str, Any]] = Field(default_factory=list)
    reviewers: List[str] = Field(default_factory=list)


class OntologyManager:
    """
    Central manager for canonical concept registration, term synonym resolution,
    and lifecycle mutations.
    """

    def __init__(self):
        self._concepts: Dict[str, CanonicalConcept] = {}
        self._term_index: Dict[str, str] = {} # term_text_lower -> concept_id
        self._releases: List[OntologyRelease] = []
        self._seed_core_ontology()

    def _seed_core_ontology(self):
        # 1. Condition: Irritable Bowel Syndrome (IBS)
        ibs_concept = CanonicalConcept(
            concept_id="CON-MOD-IBS-001",
            canonical_name="Irritable Bowel Syndrome",
            medical_system=MedicalSystem.MODERN,
            entity_class="Condition",
            definition="A functional gastrointestinal disorder characterized by recurrent abdominal pain associated with defecation or a change in bowel habits.",
            lifecycle_status=ConceptLifecycleStatus.ACTIVE,
            classical_references=["Rome IV Diagnostic Criteria"],
            terms=[
                MedicalTerm(term_id="TRM-01", concept_id="CON-MOD-IBS-001", term_text="Irritable Bowel Syndrome", language="en", script="Latin", is_preferred=True),
                MedicalTerm(term_id="TRM-02", concept_id="CON-MOD-IBS-001", term_text="IBS", language="en", script="Latin", synonym_type=SynonymType.ABBREVIATION),
                MedicalTerm(term_id="TRM-03", concept_id="CON-MOD-IBS-001", term_text="Spastic Colon", language="en", script="Latin", synonym_type=SynonymType.HISTORICAL_NAME),
                MedicalTerm(term_id="TRM-04", concept_id="CON-MOD-IBS-001", term_text="متلازمة القولون العصبي", language="ar", script="Arabic/Nastaliq", synonym_type=SynonymType.TRANSLATION),
                MedicalTerm(term_id="TRM-05", concept_id="CON-MOD-IBS-001", term_text="Grahani Roga (Functional correlate)", language="sa", script="Devanagari", synonym_type=SynonymType.REGIONAL_NAME)
            ]
        )
        self.register_concept(ibs_concept)

        # 2. Compound: Berberine
        berberine_concept = CanonicalConcept(
            concept_id="CON-MOD-BERBERINE-001",
            canonical_name="Berberine",
            medical_system=MedicalSystem.MODERN,
            entity_class="Compound",
            definition="A quaternary ammonium salt from the protoberberine group of benzylisoquinoline alkaloids found in plants such as Berberis.",
            lifecycle_status=ConceptLifecycleStatus.ACTIVE,
            terms=[
                MedicalTerm(term_id="TRM-10", concept_id="CON-MOD-BERBERINE-001", term_text="Berberine", language="en", script="Latin", is_preferred=True),
                MedicalTerm(term_id="TRM-11", concept_id="CON-MOD-BERBERINE-001", term_text="Berberine hydrochloride", language="en", script="Latin", synonym_type=SynonymType.SCIENTIFIC_NAME),
                MedicalTerm(term_id="TRM-12", concept_id="CON-MOD-BERBERINE-001", term_text="بربرين", language="ar", script="Arabic/Nastaliq", synonym_type=SynonymType.TRANSLATION)
            ]
        )
        self.register_concept(berberine_concept)

        # 3. Condition: Type 2 Diabetes Mellitus
        t2d_concept = CanonicalConcept(
            concept_id="CON-MOD-T2D-001",
            canonical_name="Type 2 Diabetes Mellitus",
            medical_system=MedicalSystem.MODERN,
            entity_class="Condition",
            definition="A chronic metabolic condition characterized by insulin resistance and relative lack of insulin.",
            lifecycle_status=ConceptLifecycleStatus.ACTIVE,
            parent_concept_ids=["CON-MOD-DM-001"],
            terms=[
                MedicalTerm(term_id="TRM-20", concept_id="CON-MOD-T2D-001", term_text="Type 2 Diabetes Mellitus", language="en", script="Latin", is_preferred=True),
                MedicalTerm(term_id="TRM-21", concept_id="CON-MOD-T2D-001", term_text="T2DM", language="en", script="Latin", synonym_type=SynonymType.ABBREVIATION),
                MedicalTerm(term_id="TRM-22", concept_id="CON-MOD-T2D-001", term_text="Non-insulin dependent diabetes mellitus", language="en", script="Latin", synonym_type=SynonymType.HISTORICAL_NAME),
                MedicalTerm(term_id="TRM-23", concept_id="CON-MOD-T2D-001", term_text="Ziabetus Shakari", language="ur", script="Arabic/Nastaliq", synonym_type=SynonymType.TRANSLATION),
                MedicalTerm(term_id="TRM-24", concept_id="CON-MOD-T2D-001", term_text="Madhumeha", language="sa", script="Devanagari", synonym_type=SynonymType.REGIONAL_NAME)
            ]
        )
        self.register_concept(t2d_concept)

    def register_concept(self, concept: CanonicalConcept):
        self._concepts[concept.concept_id] = concept
        for t in concept.terms:
            self._term_index[t.term_text.lower().strip()] = concept.concept_id

    def get_concept(self, concept_id: str) -> Optional[CanonicalConcept]:
        return self._concepts.get(concept_id)

    def resolve_term(self, text: str) -> Optional[CanonicalConcept]:
        clean = text.lower().strip()
        concept_id = self._term_index.get(clean)
        if concept_id:
            return self._concepts.get(concept_id)
        # Prefix / partial lookup
        for term_str, cid in self._term_index.items():
            if clean in term_str or term_str in clean:
                return self._concepts.get(cid)
        return None

    def merge_concepts(self, survivor_id: str, retired_id: str, rationale: str, reviewer: str) -> CanonicalConcept:
        """
        Merge Governance (Section 33):
        Retires retired_id, retains mapping history, and merges terms into survivor_id.
        """
        survivor = self._concepts.get(survivor_id)
        retired = self._concepts.get(retired_id)
        if not survivor or not retired:
            raise ValueError("Both concept IDs must exist for merge.")

        retired.lifecycle_status = ConceptLifecycleStatus.MERGED
        retired.updated_at = datetime.utcnow()
        retired.definition += f" [MERGED into {survivor_id}: {rationale}]"

        # Transfer terms
        for term in retired.terms:
            survivor.terms.append(term)
            self._term_index[term.term_text.lower().strip()] = survivor_id

        survivor.updated_at = datetime.utcnow()
        return survivor

    def split_concept(self, source_id: str, new_concepts: List[CanonicalConcept], rationale: str, reviewer: str):
        """
        Split Governance (Section 34):
        Marks source concept as SPLIT, retains historical link, registers daughter concepts.
        """
        source = self._concepts.get(source_id)
        if not source:
            raise ValueError(f"Concept {source_id} not found.")

        source.lifecycle_status = ConceptLifecycleStatus.SPLIT
        source.updated_at = datetime.utcnow()
        source.definition += f" [SPLIT into {[c.concept_id for c in new_concepts]}: {rationale}]"

        for nc in new_concepts:
            self.register_concept(nc)

    def deprecate_concept(self, concept_id: str, reason: str, reviewer: str):
        c = self._concepts.get(concept_id)
        if c:
            c.lifecycle_status = ConceptLifecycleStatus.DEPRECATED
            c.updated_at = datetime.utcnow()
            c.definition += f" [DEPRECATED: {reason}]"

    def release_version(self, version_tag: str, reviewers: List[str]) -> OntologyRelease:
        release = OntologyRelease(
            ontology_version=version_tag,
            total_concepts=len(self._concepts),
            total_terms=len(self._term_index),
            new_concepts=[c.concept_id for c in self._concepts.values() if c.lifecycle_status == ConceptLifecycleStatus.ACTIVE],
            deprecated_concepts=[c.concept_id for c in self._concepts.values() if c.lifecycle_status == ConceptLifecycleStatus.DEPRECATED],
            reviewers=reviewers
        )
        self._releases.append(release)
        return release
