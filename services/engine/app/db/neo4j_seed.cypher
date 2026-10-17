// ZMIE Neo4j Graph Cypher Initial Constraints and Cross-System Ontology Seed

// 1. Uniqueness Constraints
CREATE CONSTRAINT unique_concept IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT unique_document IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE;
CREATE CONSTRAINT unique_claim IF NOT EXISTS FOR (cl:Claim) REQUIRE cl.id IS UNIQUE;

// 2. Cross-System Concept Nodes Seed
CREATE (mizaj:Concept:Unani {
    id: "CON-UNANI-MIZAJ-DAMWI",
    canonical_name: "Mizaj Damwi (Sanguinous/Hot & Moist)",
    system: "unani_tibb",
    category: "constitutional_temperament",
    definition: "Dominance of Dam (Blood) characterized by warmth, vascular fullness, and robust metabolic activity."
});

CREATE (prakriti:Concept:Ayurveda {
    id: "CON-AYUR-PITTA-PRAKRITI",
    canonical_name: "Pitta Prakriti",
    system: "ayurveda",
    category: "constitutional_dosha",
    definition: "Predominance of Pitta Dosha governing digestion, metabolism, systemic temperature, and transformation."
});

CREATE (metabolism:Concept:Modern {
    id: "CON-BIOMED-METABOLIC-TONE",
    canonical_name: "Basal Metabolic Rate & Autonomic Vascular Reactivity",
    system: "modern_biomedicine",
    category: "physiology",
    definition: "Endocrine and sympathetic neurovascular set-point regulating thermogenesis and glucose homeostasis."
});

// 3. Cross-System Mapping Relationships (Preserving Epistemic Integrity)
MATCH (u:Concept {id: "CON-UNANI-MIZAJ-DAMWI"}), (a:Concept {id: "CON-AYUR-PITTA-PRAKRITI"})
CREATE (u)-[:MAPPED_TO {
    state: "PARTIAL_OVERLAP",
    confidence: 0.74,
    epistemic_rationale: "Both represent metabolic heat and active circulation, but Pitta centers on digestion/transformation whereas Damwi centers on vascular humors."
}]->(a);

MATCH (u:Concept {id: "CON-UNANI-MIZAJ-DAMWI"}), (m:Concept {id: "CON-BIOMED-METABOLIC-TONE"})
CREATE (u)-[:MAPPED_TO {
    state: "FUNCTIONAL_ANALOGY",
    confidence: 0.68,
    epistemic_rationale: "Functional analogy to sympathetic predominance and elevated basal metabolic heat."
}]->(m);
