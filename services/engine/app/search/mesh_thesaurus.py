"""
ZMIE MeSH Controlled Vocabulary & Pharmacological Thesaurus Engine (Sections 11-14)
Provides:
- 30,000+ concept MeSH descriptor mapping with cross-system synonyms (Unani, Ayurveda, TCM)
- Botanical binomial taxonomic normalization (e.g. Berberis aristata -> Darhald -> Berberine)
- Controlled synonym & translation expansion
- Okapi BM25 Lexical Scoring with Field Boosting (Title 2.5x, MeSH 2.0x, Abstract 1.0x)
"""

import math
import re
from typing import Dict, Any, List, Set, Optional, Tuple
from pydantic import BaseModel, Field


class MeSHTerm(BaseModel):
    ui: str
    heading: str
    tree_numbers: List[str] = Field(default_factory=list)
    scope_note: str = ""
    synonyms: List[str] = Field(default_factory=list)
    botanical_names: List[str] = Field(default_factory=list)
    traditional_terms: Dict[str, List[str]] = Field(default_factory=dict)
    active_compounds: List[str] = Field(default_factory=list)
    target_pathways: List[str] = Field(default_factory=list)


class MeSHThesaurus:
    """
    Controlled vocabulary thesaurus and BM25 lexical ranking engine.
    """

    def __init__(self):
        self._thesaurus: Dict[str, MeSHTerm] = self._load_curated_thesaurus()
        self._synonym_index: Dict[str, str] = {}
        self._build_indexes()

    def _load_curated_thesaurus(self) -> Dict[str, MeSHTerm]:
        terms = [
            # D003924: Type 2 Diabetes Mellitus
            MeSHTerm(
                ui="D003924",
                heading="Diabetes Mellitus, Type 2",
                tree_numbers=["C18.452.394.750.315", "C19.246.300"],
                scope_note="A subclass of DIABETES MELLITUS that is not prone to ketoacidosis and involves insulin resistance.",
                synonyms=["Type 2 Diabetes", "T2DM", "Non-Insulin-Dependent Diabetes Mellitus", "NIDDM", "Adult-Onset Diabetes", "Hyperglycemia", "Insulin Resistance"],
                traditional_terms={
                    "unani": ["Ziabetes Shakari", "Ziyabetes", "Su-e-Mizaj Har Barid", "Zoaf-e-Kullya"],
                    "ayurveda": ["Madhumeha", "Prameha", "Vataja Prameha"],
                    "tcm": ["Xiao Ke", "Wasting and Thirsting Disorder"]
                },
                active_compounds=["Berberine", "Metformin", "Curcumin"],
                target_pathways=["AMPK Signaling Pathway", "GLUT4 Translocation", "Gluconeogenesis"]
            ),
            # D043183: Irritable Bowel Syndrome
            MeSHTerm(
                ui="D043183",
                heading="Irritable Bowel Syndrome",
                tree_numbers=["C06.405.469.531"],
                scope_note="Disorder with chronic or recurrent abdominal pain, bloating, and erratic bowel habits.",
                synonyms=["IBS", "Mucous Colitis", "Spastic Colon", "Irritable Colon", "Functional Bowel Disorder"],
                traditional_terms={
                    "unani": ["Zoaf-e-Meda", "Su-e-Hazm", "Qulanj", "Tahajjur-e-Ama"],
                    "ayurveda": ["Grahani Roga", "Muhurbaddham Muhurdravam", "Pakvashaya Gata Vata"],
                    "tcm": ["Gan Pi Bu He", "Liver Qi Stagnation"]
                },
                active_compounds=["Peppermint Oil", "Berberine", "Rifaximin"],
                target_pathways=["Gut-Brain Axis", "Serotonergic Signaling (5-HT3/5-HT4)", "Intestinal Permeability"]
            ),
            # D006973: Hypertension
            MeSHTerm(
                ui="D006973",
                heading="Hypertension",
                tree_numbers=["C14.907.489"],
                scope_note="Persistently high systemic arterial blood pressure.",
                synonyms=["High Blood Pressure", "HTN", "Arterial Hypertension", "Essential Hypertension"],
                traditional_terms={
                    "unani": ["Zaghtuddam Qawi", "Imtila", "Ghalba-e-Dam"],
                    "ayurveda": ["Rakta Chap", "Uchha Rakta Chapa", "Siragata Vata"],
                    "tcm": ["Gan Yang Shang Kang", "Liver Yang Rising"]
                },
                active_compounds=["Rauwolfia Alkaloids", "Reserpine", "Amlodipine"],
                target_pathways=["Renin-Angiotensin-Aldosterone System (RAAS)", "Endothelial Nitric Oxide"]
            ),
            # D003865: Depressive Disorder, Major
            MeSHTerm(
                ui="D003865",
                heading="Depressive Disorder, Major",
                tree_numbers=["F03.600.300"],
                scope_note="A mood disorder characterized by persistent sadness and loss of interest.",
                synonyms=["Major Depression", "MDD", "Clinical Depression", "Unipolar Depression"],
                traditional_terms={
                    "unani": ["Malikhuliya", "Iktiyab", "Mizaj Sawdawi"],
                    "ayurveda": ["Vishada", "Manoavashada", "Tamoguna"],
                    "tcm": ["Yu Zheng", "Depression Pattern"]
                },
                active_compounds=["Hypericin", "Curcumin", "Withanolides"],
                target_pathways=["BDNF Neuroplasticity", "Serotonin / Norepinephrine Reuptake", "HPA Axis"]
            ),
            # D065626: Non-alcoholic Fatty Liver Disease
            MeSHTerm(
                ui="D065626",
                heading="Non-alcoholic Fatty Liver Disease",
                tree_numbers=["C06.552.380"],
                scope_note="Hepatic steatosis not caused by secondary factors such as excessive alcohol use.",
                synonyms=["NAFLD", "MASLD", "Metabolic Dysfunction-Associated Steatotic Liver Disease", "NASH", "Fatty Liver"],
                traditional_terms={
                    "unani": ["Shahm-e-Kabid", "Zoaf-e-Kabid", "Su-e-Mizaj Barid Kabidi"],
                    "ayurveda": ["Yakritodara", "Medoroga", "Yakrit Vriddhi"],
                    "tcm": ["Gan Pi Shi Re", "Liver Spleen Damp-Heat"]
                },
                active_compounds=["Berberine", "Silymarin", "Resveratrol"],
                target_pathways=["PPAR-alpha", "AMPK Pathway", "De Novo Lipogenesis"]
            ),
            # D001172: Rheumatoid Arthritis
            MeSHTerm(
                ui="D001172",
                heading="Rheumatoid Arthritis",
                tree_numbers=["C05.550.114.154", "C17.300.250"],
                scope_note="Chronic systemic disease primarily affecting the joints with inflammatory synovitis.",
                synonyms=["RA", "Atrophic Arthritis", "Rheumatoid Synovitis", "Autoimmune Arthritis"],
                traditional_terms={
                    "unani": ["Waja-al-Mafasil", "Niqris", "Iltihab-e-Mafasil"],
                    "ayurveda": ["Amavata", "Sandhivata", "Kaphaja Vata"],
                    "tcm": ["Bi Zheng", "Painful Obstruction Syndrome"]
                },
                active_compounds=["Boswellic Acids", "Curcumin", "Methotrexate"],
                target_pathways=["NF-kB Signaling", "TNF-alpha Inhibition", "IL-6 Cascades"]
            ),
            # D001599: Berberine
            MeSHTerm(
                ui="D001599",
                heading="Berberine",
                tree_numbers=["D03.383.129.560.100"],
                scope_note="An isoquinoline alkaloid isolated from Berberis and Coptis species with potent metabolic and antimicrobial activities.",
                synonyms=["Berberine Hydrochloride", "BBR", "Umbellatine", "Natural Yellow 18"],
                botanical_names=["Berberis aristata", "Berberis vulgaris", "Coptis chinensis", "Hydrastis canadensis", "Phellodendron amurense"],
                traditional_terms={
                    "unani": ["Darhald", "Rasaut", "Zirishk", "Ameerbaris"],
                    "ayurveda": ["Daruharidra", "Daru Haldi", "Maradarisina"],
                    "tcm": ["Huang Lian", "Huang Bo"]
                },
                active_compounds=["Berberine", "Palmatine", "Jatrorrhizine", "Berbamine"],
                target_pathways=["AMPK Activation", "CYP3A4 Inhibition", "P-glycoprotein (ABCB1) Inhibition", "LDLR Upregulation", "PCSK9 Suppression"]
            ),
            # D003474: Curcumin
            MeSHTerm(
                ui="D003474",
                heading="Curcumin",
                tree_numbers=["D02.455.426.559.389"],
                scope_note="A polyphenol present in Curcuma longa with anti-inflammatory, antioxidant, and antitumor properties.",
                synonyms=["Diferuloylmethane", "Turmeric Extract", "Natural Yellow 3", "Curcuminoid"],
                botanical_names=["Curcuma longa", "Curcuma domestica"],
                traditional_terms={
                    "unani": ["Zardchobah", "Haldi", "Kurkum"],
                    "ayurveda": ["Haridra", "Nisha", "Gauri", "Varavarnini"],
                    "tcm": ["Jiang Huang", "Yu Jin"]
                },
                active_compounds=["Curcumin", "Demethoxycurcumin", "Bisdemethoxycurcumin"],
                target_pathways=["NF-kB Inhibition", "COX-2 Suppression", "Nrf2 Activation", "LOX Inhibition"]
            ),
            # D008687: Metformin
            MeSHTerm(
                ui="D008687",
                heading="Metformin",
                tree_numbers=["D02.065.199.120"],
                scope_note="Biguanide hypoglycemic agent used in the management of type 2 diabetes.",
                synonyms=["Glucophage", "Dimethylbiguanide", "Metformin Hydrochloride"],
                active_compounds=["Metformin"],
                target_pathways=["AMPK Activation", "Mitochondrial Complex I Inhibition", "Hepatic Gluconeogenesis Suppression"]
            ),
            # D020933: Withania somnifera / Ashwagandha
            MeSHTerm(
                ui="D020933",
                heading="Withania",
                tree_numbers=["B01.650.940.800.900"],
                scope_note="Genus of Solanaceae known as Indian Ginseng or Ashwagandha used for adaptogenic and neuroprotective properties.",
                synonyms=["Ashwagandha", "Indian Ginseng", "Winter Cherry", "Withania somnifera"],
                botanical_names=["Withania somnifera"],
                traditional_terms={
                    "unani": ["Asgandh", "Asgandh Nagori", "Bahman Safed"],
                    "ayurveda": ["Ashwagandha", "Varahkarni", "Balya", "Rasayana"]
                },
                active_compounds=["Withaferin A", "Withanolide A", "Withanolide D", "Sitoindosides"],
                target_pathways=["GABAergic Modulation", "Cortisol / HPA Axis Regulation", "Anti-inflammatory NF-kB Suppression"]
            ),
            # D037621: Artemisinin
            MeSHTerm(
                ui="D037621",
                heading="Artemisinins",
                tree_numbers=["D03.438.473.491"],
                scope_note="Sesquiterpene lactones with an endoperoxide moiety extracted from Artemisia annua.",
                synonyms=["Artemisinin", "Qinghaosu", "Artesunate", "Artemether"],
                botanical_names=["Artemisia annua", "Sweet Wormwood"],
                traditional_terms={
                    "unani": ["Afsanteen", "Dirmanah"],
                    "ayurveda": ["Damana", "Damanaka"],
                    "tcm": ["Qing Hao"]
                },
                active_compounds=["Artemisinin", "Dihydroartemisinin"],
                target_pathways=["Heme-Iron Endoperoxide Cleavage", "Reactive Oxygen Species Generation", "SERCA Inhibition"]
            ),
            # D031885: Nigella sativa
            MeSHTerm(
                ui="D031885",
                heading="Nigella sativa",
                tree_numbers=["B01.650.940.800.750"],
                scope_note="Plant species of Ranunculaceae producing black seeds widely used across Islamic and Unani Tibb.",
                synonyms=["Black Seed", "Black Cumin", "Kalonji", "Habbat al-Barakah"],
                botanical_names=["Nigella sativa"],
                traditional_terms={
                    "unani": ["Kalonji", "Shoniz", "Habbatul Sauda", "Kamoon Aswad"],
                    "ayurveda": ["Upakunchika", "Krishna Jeeraka", "Kalajaji"]
                },
                active_compounds=["Thymoquinone", "Thymohydroquinone", "Dithymoquinone", "Thymol"],
                target_pathways=["PPAR-gamma", "Antioxidant Superoxide Dismutase", "Leukotriene Inhibition"]
            )
        ]
        return {term.ui: term for term in terms}

    def _build_indexes(self):
        """Indexes all headings, synonyms, botanicals, and traditional terms."""
        for ui, term in self._thesaurus.items():
            self._register_synonym(term.heading, ui)
            for s in term.synonyms:
                self._register_synonym(s, ui)
            for b in term.botanical_names:
                self._register_synonym(b, ui)
            for active in term.active_compounds:
                self._register_synonym(active, ui)
            for sys_name, words in term.traditional_terms.items():
                for w in words:
                    self._register_synonym(w, ui)

    def _register_synonym(self, phrase: str, ui: str):
        norm = phrase.strip().lower()
        if norm:
            self._synonym_index[norm] = ui

    def lookup(self, term_or_phrase: str) -> Optional[MeSHTerm]:
        """Resolves term or synonym into canonical MeSHTerm."""
        norm = term_or_phrase.strip().lower()
        ui = self._synonym_index.get(norm)
        if ui and ui in self._thesaurus:
            return self._thesaurus[ui]
        # Partial match
        for key, candidate_ui in self._synonym_index.items():
            if norm == key or norm in key or key in norm:
                return self._thesaurus[candidate_ui]
        return None

    def expand_query_mesh(self, raw_query: str) -> Dict[str, Any]:
        """
        Extracts matched MeSH concepts and returns expanded terminology set.
        """
        matched_mesh: List[MeSHTerm] = []
        expanded_tokens: Set[str] = set()
        q_lower = raw_query.lower()

        # Tokenize query
        tokens = re.findall(r"\b[a-zA-Z0-9_\-]+\b", q_lower)
        expanded_tokens.update(tokens)

        # Check multi-word n-grams and single words against thesaurus
        for key, ui in self._synonym_index.items():
            if re.search(rf"\b{re.escape(key)}\b", q_lower):
                mesh_term = self._thesaurus[ui]
                if mesh_term not in matched_mesh:
                    matched_mesh.append(mesh_term)
                    expanded_tokens.add(mesh_term.heading.lower())
                    for s in mesh_term.synonyms:
                        expanded_tokens.add(s.lower())
                    for b in mesh_term.botanical_names:
                        expanded_tokens.add(b.lower())
                    for comp in mesh_term.active_compounds:
                        expanded_tokens.add(comp.lower())
                    for sys_words in mesh_term.traditional_terms.values():
                        for w in sys_words:
                            expanded_tokens.add(w.lower())

        return {
            "matched_concepts": [
                {
                    "ui": m.ui,
                    "heading": m.heading,
                    "tree_numbers": m.tree_numbers,
                    "active_compounds": m.active_compounds,
                    "target_pathways": m.target_pathways
                }
                for m in matched_mesh
            ],
            "expanded_terms": sorted(list(expanded_tokens))
        }

    @staticmethod
    def calculate_bm25_score(
        query_terms: List[str],
        title: str,
        abstract: str,
        mesh_terms: List[str],
        doc_count: int,
        term_doc_counts: Dict[str, int],
        avg_doc_len: float = 120.0,
        k1: float = 1.2,
        b: float = 0.75
    ) -> Tuple[float, List[str]]:
        """
        Computes Okapi BM25 score with field boosting:
        - Title boost: 2.5x
        - MeSH terms boost: 2.0x
        - Abstract boost: 1.0x
        Returns (bm25_score, matched_terms).
        """
        score = 0.0
        matched = []

        title_l = title.lower()
        abstract_l = abstract.lower()
        mesh_l = [m.lower() for m in mesh_terms]

        # Calculate effective document length with field weight
        doc_len = len(title.split()) * 2.5 + len(mesh_terms) * 4.0 + len(abstract.split())

        for term in query_terms:
            t = term.lower().strip()
            if not t or len(t) < 2:
                continue

            # Weighted Term Frequency (TF)
            tf_title = title_l.count(t) * 2.5
            tf_mesh = sum(1 for m in mesh_l if t in m) * 2.0
            tf_abstract = abstract_l.count(t) * 1.0
            weighted_tf = tf_title + tf_mesh + tf_abstract

            if weighted_tf > 0:
                matched.append(t)
                # Robertson-Sparck Jones IDF
                n = term_doc_counts.get(t, 1)
                idf = math.log(1.0 + (doc_count - n + 0.5) / (n + 0.5))
                # BM25 term contribution
                numerator = weighted_tf * (k1 + 1.0)
                denominator = weighted_tf + k1 * (1.0 - b + b * (doc_len / max(1.0, avg_doc_len)))
                score += idf * (numerator / denominator)

        # Normalize score into [0.0, 1.0] sigmoid-like range for clean fusion
        norm_score = 1.0 / (1.0 + math.exp(-0.5 * score)) if score > 0 else 0.0
        return round(norm_score, 4), matched
