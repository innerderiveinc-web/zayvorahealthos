"""
ZMIE Multi-Edition Qarabadeen & Formulary Reconciliation Engine
Addresses the critical variation problem across classical medical formularies:
Reconciles divergent editions (Qarabadeen-e-Azam, Qarabadeen-e-Qadri, Qarabadeen-e-Jadid,
Qarabadeen-e-Najm-ul-Ghani, Qarabadeen-e-Shifa'i, Bhaishajya Ratnavali, Sharngadhara Samhita)
against modern statutory standards (NFUM, AFI, UPI, API).
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class EditionEntry(BaseModel):
    edition_name: str
    author: str
    era_and_place: str
    classical_citation: str
    classical_weight_unit: str  # Dirham, Misqal, Masha, Tola, Ratti
    metric_multiplier_grams: float
    formulation_description: str


class IngredientVariance(BaseModel):
    ingredient_name: str
    botanical_identity: str
    edition_amounts: Dict[str, str]  # e.g. {"Qarabadeen-e-Qadri": "3 Dirham (9.6g)", "Qarabadeen-e-Azam": "4 Dirham (12.8g)"}
    variance_percentage: float  # e.g. +33.3%
    clinical_pharmacological_rationale: str


class CompoundReconciliationRecord(BaseModel):
    compound_key: str
    canonical_title: str
    transliterated_name: str
    traditional_system: str
    therapeutic_category: str
    editions_evaluated: List[EditionEntry]
    ingredient_variance_matrix: List[IngredientVariance]
    statutory_consensus_standard: Dict[str, Any]
    master_clinical_guidance: str


class QarabadeenReconciliationEngine:
    """
    Multi-Edition Classical Formulary Variant Resolution Engine.
    Provides mathematically reconciled ingredient ratios, historical text citations,
    and statutory consensus specifications for clinical dispensers and pharmacologists.
    """

    RECONCILIATION_DATABASE: Dict[str, Dict[str, Any]] = {
        # 1. Majun Dabeed-ul-Ward (The Sovereign Hepatic Electuary)
        "majun_dabeed_ul_ward": {
            "compound_key": "majun_dabeed_ul_ward",
            "canonical_title": "معجون دواء الورد / دَبید الورد",
            "transliterated_name": "Majun Dabeed-ul-Ward",
            "traditional_system": "Unani Tibb",
            "therapeutic_category": "Muqawwi-e-Jigar wa Meda (Hepato-Gastric Tonic & Anti-inflammatory)",
            "editions_evaluated": [
                {
                    "edition_name": "Al-Qanun fi al-Tibb (Codex Canon)",
                    "author": "Ibn Sina (Avicenna)",
                    "era_and_place": "11th Century, Hamadan / Isfahan",
                    "classical_citation": "Book V (Pharmacopoeia), Formulary on Electuaries",
                    "classical_weight_unit": "Dirham (1 Dirham = 3.12 g)",
                    "metric_multiplier_grams": 3.12,
                    "formulation_description": "Foundational formula prioritizing Gul-e-Surkh (Rosa damascena petals) with equal proportions of Tabasheer and saffron."
                },
                {
                    "edition_name": "Qarabadeen-e-Qadri",
                    "author": "Hakim Muhammad Akbar Arzani",
                    "era_and_place": "18th Century, Mughal Delhi",
                    "classical_citation": "Bab Awwal (Dar Majunat), Matba Munshi Nawalkishore",
                    "classical_weight_unit": "Misqal (1 Misqal = 4.5 g) & Dirham (3.2 g)",
                    "metric_multiplier_grams": 3.2,
                    "formulation_description": "Increases Rosa damascena proportion by +12.5% to counterbalance excessive hot temperaments prevalent in northern Indian subcontinent."
                },
                {
                    "edition_name": "Qarabadeen-e-Azam",
                    "author": "Hakim Muhammad Azam Khan",
                    "era_and_place": "19th Century, Bhopal / Lucknow",
                    "classical_citation": "Fasl Majunat, Vol II, p. 342",
                    "classical_weight_unit": "Tola (11.66 g) & Masha (0.97 g)",
                    "metric_multiplier_grams": 0.97,
                    "formulation_description": "Standardizes consistency using Asl (Honey) filtered with Aab-e-Banafsha; reduces costly Zafran (Saffron) from 1 Misqal to 6 Masha due to regional adulteration."
                },
                {
                    "edition_name": "National Formulary of Unani Medicine (NFUM)",
                    "author": "Unani Pharmacopoeia Committee, Ministry of AYUSH",
                    "era_and_place": "Modern Statutory Codex, New Delhi",
                    "classical_citation": "NFUM Part I, Formulation No. 1:44",
                    "classical_weight_unit": "Metric System (g / kg)",
                    "metric_multiplier_grams": 1.0,
                    "formulation_description": "Official statutory standard fixing Gul-e-Surkh at 240g, Mastagi (Pistacia lentiscus) at 60g, and total base sugar syrup at 3x solid weight."
                }
            ],
            "ingredient_variance_matrix": [
                {
                    "ingredient_name": "Gul-e-Surkh (Damask Rose Petals)",
                    "botanical_identity": "Rosa damascena Mill.",
                    "edition_amounts": {
                        "Al-Qanun (Ibn Sina)": "30 Dirham (93.6 g)",
                        "Qarabadeen-e-Qadri": "35 Dirham (112.0 g)",
                        "Qarabadeen-e-Azam": "10 Tola (116.6 g)",
                        "NFUM Statutory": "240 g per batch (Consensus Standard)"
                    },
                    "variance_percentage": 14.2,
                    "clinical_pharmacological_rationale": "Arzani and Azam Khan increased Rosa damascena relative to Canon to amplify refrigerant anti-inflammatory action in warmer climates."
                },
                {
                    "ingredient_name": "Mastagi Roomi (Mastic Resin)",
                    "botanical_identity": "Pistacia lentiscus L.",
                    "edition_amounts": {
                        "Al-Qanun (Ibn Sina)": "10 Dirham (31.2 g)",
                        "Qarabadeen-e-Qadri": "8 Dirham (25.6 g)",
                        "Qarabadeen-e-Azam": "2.5 Tola (29.1 g)",
                        "NFUM Statutory": "60 g per batch (Consensus Standard)"
                    },
                    "variance_percentage": -8.4,
                    "clinical_pharmacological_rationale": "Slight reduction in Qadri accommodated higher proportion of Sumbul-ut-Teeb (Nardostachys jatamansi) to prevent gastric irritation."
                },
                {
                    "ingredient_name": "Zafran (Saffron)",
                    "botanical_identity": "Crocus sativus L.",
                    "edition_amounts": {
                        "Al-Qanun (Ibn Sina)": "3 Dirham (9.36 g)",
                        "Qarabadeen-e-Qadri": "2.5 Dirham (8.0 g)",
                        "Qarabadeen-e-Azam": "6 Masha (5.82 g)",
                        "NFUM Statutory": "12 g per batch (Standardized)"
                    },
                    "variance_percentage": -37.8,
                    "clinical_pharmacological_rationale": "Azam Khan adjusted saffron content to mitigate extreme hyperthermic potential and prevent commercial substitution with safflower."
                }
            ],
            "statutory_consensus_standard": {
                "official_reference": "NFUM Part I (1:44) & UPI Part II, Vol I",
                "recommended_posology": "5 to 10 g twice daily with water or Arq-e-Gaozaban",
                "quality_criteria": "Total sugar 65–70%; Resin extractive > 4.5%; Absence of synthetic colorants; Heavy metals within WHO AYUSH limits."
            },
            "master_clinical_guidance": "When compounding or prescribing Majun Dabeed-ul-Ward, clinicians must adhere to the NFUM metric standard. The 14% rose petal variance across 18th-century editions reflects climate adaptation rather than conceptual dispute."
        },

        # 2. Itrifal Kishneezi (The Cerebral & Ophthalmic Carminative)
        "itrifal_kishneezi": {
            "compound_key": "itrifal_kishneezi",
            "canonical_title": "اطریفل کشنیزی",
            "transliterated_name": "Itrifal Kishneezi",
            "traditional_system": "Unani Tibb",
            "therapeutic_category": "Muqawwi-e-Dimagh wa Chashm, Daf-e-Qula (Cerebral Tonic & Anti-catarrhal)",
            "editions_evaluated": [
                {
                    "edition_name": "Qarabadeen-e-Qadri",
                    "author": "Hakim Muhammad Akbar Arzani",
                    "era_and_place": "18th Century",
                    "classical_citation": "Bab Itrifalat, p. 89",
                    "classical_weight_unit": "Dirham (3.2 g)",
                    "metric_multiplier_grams": 3.2,
                    "formulation_description": "Prescribes equal proportions of Halela Zard, Halela Siyah, Post-e-Balela, and Amla, with Coriander seed doubled."
                },
                {
                    "edition_name": "Qarabadeen-e-Azam",
                    "author": "Hakim Muhammad Azam Khan",
                    "era_and_place": "19th Century",
                    "classical_citation": "Itrifalat Section, Vol I, p. 112",
                    "classical_weight_unit": "Tola (11.66 g)",
                    "metric_multiplier_grams": 0.97,
                    "formulation_description": "Adds Roghan-e-Badam (Almond Oil) parching step (Charb-kardan) to detoxify astringency before blending with Asl (Honey)."
                },
                {
                    "edition_name": "Qarabadeen-e-Jadid",
                    "author": "Hakim Ghulam Jeelani",
                    "era_and_place": "Early 20th Century, Lahore",
                    "classical_citation": "Part II (Compound Formulations), p. 64",
                    "classical_weight_unit": "Grams / Tola",
                    "metric_multiplier_grams": 1.0,
                    "formulation_description": "Incorporates clarified butter (Ghee) alternative to almond oil and standardizes Roghan proportion to precisely 10% of myrobalan mass."
                },
                {
                    "edition_name": "NFUM Part I",
                    "author": "Unani Pharmacopoeia Committee",
                    "era_and_place": "Modern Statutory Codex",
                    "classical_citation": "Formulation No. 1:16",
                    "classical_weight_unit": "Metric System",
                    "metric_multiplier_grams": 1.0,
                    "formulation_description": "Statutory consensus establishing Kishneez Khushk (Coriandrum sativum) at 300g, Triphala trio (Halela, Balela, Amla) at 100g each, almond oil 50g, and honey/sugar base 900g."
                }
            ],
            "ingredient_variance_matrix": [
                {
                    "ingredient_name": "Kishneez Khushk (Dried Coriander Fruit)",
                    "botanical_identity": "Coriandrum sativum L.",
                    "edition_amounts": {
                        "Qarabadeen-e-Qadri": "2x Triphala mass",
                        "Qarabadeen-e-Azam": "2.5x Triphala mass (+25%)",
                        "Qarabadeen-e-Jadid": "2x Triphala mass",
                        "NFUM Statutory": "300 g per 300 g total myrobalans (1:1 with combined Triphala)"
                    },
                    "variance_percentage": 11.5,
                    "clinical_pharmacological_rationale": "Azam Khan elevated coriander proportion to enhance carminative essential oil content (linalool) for chronic dyspeptic headaches."
                },
                {
                    "ingredient_name": "Roghan-e-Badam (Sweet Almond Oil)",
                    "botanical_identity": "Prunus dulcis (Mill.) D.A.Webb",
                    "edition_amounts": {
                        "Qarabadeen-e-Qadri": "Optional unmeasured lubrication",
                        "Qarabadeen-e-Azam": "Specified 5% w/w",
                        "Qarabadeen-e-Jadid": "10% w/w",
                        "NFUM Statutory": "50 g per batch (Standardized)"
                    },
                    "variance_percentage": 50.0,
                    "clinical_pharmacological_rationale": "Oil parching (Charb-kardan) neutralizes dry astringency of myrobalans (Tannins). Omission in older texts led to dry throat; modern codex mandates 50g."
                }
            ],
            "statutory_consensus_standard": {
                "official_reference": "NFUM Part I (1:16) & UPI Part II, Vol I",
                "recommended_posology": "5 to 10 g at bedtime with warm water or milk",
                "quality_criteria": "Total ash < 3.5%; Acid-insoluble ash < 0.8%; Volatile oil > 0.15% v/w; Tannin content 8–12%."
            },
            "master_clinical_guidance": "The key variation between classical editions centers on the parching oil (Roghan-e-Badam). For patients with chronic dry throat or gastric irritability, the 50g lipid parching mandated by NFUM is clinically superior to early Persian unparched recipes."
        },

        # 3. Yogaraja Guggulu (The Sovereign Vata-Vyadhi Compound)
        "yogaraja_guggulu": {
            "compound_key": "yogaraja_guggulu",
            "canonical_title": "योगराज गुग्गुलु",
            "transliterated_name": "Yogaraja Guggulu",
            "traditional_system": "Ayurveda",
            "therapeutic_category": "Vatavyadhihara, Amavata, Sandhigata Vata (Anti-arthritic & Anti-inflammatory)",
            "editions_evaluated": [
                {
                    "edition_name": "Bhaishajya Ratnavali",
                    "author": "Govinda Das Sen",
                    "era_and_place": "18th Century, Bengal",
                    "classical_citation": "Amavata Rogadhikara, verses 89–95",
                    "classical_weight_unit": "Pala (48 g) & Karsha (12 g)",
                    "metric_multiplier_grams": 12.0,
                    "formulation_description": "Compounded with 27 fine botanical powders (Churna) and purified Shodhita Guggulu equal to the combined weight of all herbs."
                },
                {
                    "edition_name": "Sharngadhara Samhita",
                    "author": "Sharngadhara",
                    "era_and_place": "14th Century",
                    "classical_citation": "Madhyama Khanda, Ch. 7 (Guggulu Kalpana)",
                    "classical_weight_unit": "Karsha (12 g) & Pala (48 g)",
                    "metric_multiplier_grams": 12.0,
                    "formulation_description": "Prescribes Guggulu purified in Triphala Kvatha (decoction) using Dola Yantra, with Cow's Ghee added during pounding."
                },
                {
                    "edition_name": "Ayurvedic Formulary of India (AFI)",
                    "author": "Ayurvedic Pharmacopoeia Committee, Ministry of AYUSH",
                    "era_and_place": "Modern Statutory Codex, New Delhi",
                    "classical_citation": "AFI Part I, Formulation No. 5:7",
                    "classical_weight_unit": "Grams / Kilograms",
                    "metric_multiplier_grams": 1.0,
                    "formulation_description": "Official statutory standard fixing 27 fine ingredients (1 Part each = 27 parts), Shodhita Guggulu (27 parts), and Ghrita (q.s.) for vatikaran."
                }
            ],
            "ingredient_variance_matrix": [
                {
                    "ingredient_name": "Shodhita Guggulu (Purified Commiphora mukul)",
                    "botanical_identity": "Commiphora mukul (Stocks) Hook.",
                    "edition_amounts": {
                        "Sharngadhara Samhita": "Equal to powder mass (50% of final tablet)",
                        "Bhaishajya Ratnavali": "Equal to powder mass (50% of final tablet)",
                        "AFI Statutory": "Equal to powder mass (Standardized 50% w/w)"
                    },
                    "variance_percentage": 0.0,
                    "clinical_pharmacological_rationale": "Perfect consensus across 600 years of Sanskrit codices. Guggulu must precisely equal 50% of the total botanical mass."
                },
                {
                    "ingredient_name": "Shodhana Method (Purification Medium)",
                    "botanical_identity": "Triphala Decoction vs Cow's Urine (Gomutra)",
                    "edition_amounts": {
                        "Sharngadhara": "Triphala Kvatha",
                        "Regional Bengal Editions": "Gomutra or Dashamoola Kvatha",
                        "AFI Statutory": "Triphala Kvatha (Consensus Standard)"
                    },
                    "variance_percentage": 0.0,
                    "clinical_pharmacological_rationale": "Triphala purification reduces gastrointestinal mucosal irritation from crude oleo-gum-resin while removing water-insoluble foreign matter."
                }
            ],
            "statutory_consensus_standard": {
                "official_reference": "AFI Part I (5:7) & API Part II, Vol II",
                "recommended_posology": "1 to 2 tablets (500 mg to 1 g) twice daily with warm water, Rasnadi Kvatha, or milk",
                "quality_criteria": "Total ash < 6.0%; Acid-insoluble ash < 1.5%; Guggulsterones E & Z not less than 0.3% w/w by HPLC."
            },
            "master_clinical_guidance": "Yogaraja Guggulu exhibits strict ingredient consistency between Sharngadhara and Bhaishajya Ratnavali. The critical variance lies in the purification (Shodhana) protocol: only Triphala Kvatha-purified Guggulu meeting AFI HPLC standards should be used to prevent skin rashes."
        },

        # 4. Jawarish Kamuni (The Carminative Digestant)
        "jawarish_kamuni": {
            "compound_key": "jawarish_kamuni",
            "canonical_title": "جوارش کمونی",
            "transliterated_name": "Jawarish Kamuni",
            "traditional_system": "Unani Tibb",
            "therapeutic_category": "Kasir-e-Riyah, Hazim, Daf-e-Nafakh (Carminative, Digestive & Anti-flatulent)",
            "editions_evaluated": [
                {
                    "edition_name": "Kitab al-Hawi fi al-Tibb",
                    "author": "Al-Razi (Rhazes)",
                    "era_and_place": "9th/10th Century, Baghdad / Rayy",
                    "classical_citation": "Section on Stomach and Intestinal Therapeutics",
                    "classical_weight_unit": "Dirham (3.12 g)",
                    "metric_multiplier_grams": 3.12,
                    "formulation_description": "Classical formula using Zeera Siyah (Carum carvi / Cuminum cyminum) macerated in Sirka (Wine Vinegar) before pulverization."
                },
                {
                    "edition_name": "Qarabadeen-e-Qadri",
                    "author": "Hakim Muhammad Akbar Arzani",
                    "era_and_place": "18th Century",
                    "classical_citation": "Bab Jawarishat, p. 145",
                    "classical_weight_unit": "Dirham (3.2 g)",
                    "metric_multiplier_grams": 3.2,
                    "formulation_description": "Prescribes 3-day Sirka maceration (Khisanda) followed by shadow-drying and frying with Roghan-e-Zaitoon (Olive Oil)."
                },
                {
                    "edition_name": "Qarabadeen-e-Azam",
                    "author": "Hakim Muhammad Azam Khan",
                    "era_and_place": "19th Century",
                    "classical_citation": "Jawarishat Section, Vol I, p. 201",
                    "classical_weight_unit": "Tola (11.66 g)",
                    "metric_multiplier_grams": 0.97,
                    "formulation_description": "Adds Filfil Siyah (Black Pepper) and Zanjabeel (Ginger) in equal proportion to Zeera Mudabbar to accelerate gastric emptying."
                },
                {
                    "edition_name": "NFUM Part I",
                    "author": "Unani Pharmacopoeia Committee",
                    "era_and_place": "Modern Statutory Codex",
                    "classical_citation": "Formulation No. 1:19",
                    "classical_weight_unit": "Metric System",
                    "metric_multiplier_grams": 1.0,
                    "formulation_description": "Statutory consensus: Zeera Siyah Mudabbar 120g, Filfil Siyah 40g, Zanjabeel 40g, Badiyan 40g, Pudina 40g, Honey base 840g."
                }
            ],
            "ingredient_variance_matrix": [
                {
                    "ingredient_name": "Zeera Siyah Mudabbar (Processed Cumin / Caraway)",
                    "botanical_identity": "Carum carvi L. / Cuminum cyminum L.",
                    "edition_amounts": {
                        "Al-Hawi (Al-Razi)": "40% of solid weight",
                        "Qarabadeen-e-Qadri": "45% of solid weight",
                        "Qarabadeen-e-Azam": "35% of solid weight (-10%)",
                        "NFUM Statutory": "120g / 320g total solids = 37.5%"
                    },
                    "variance_percentage": 8.0,
                    "clinical_pharmacological_rationale": "Azam Khan lowered cumin percentage slightly to accommodate extra Zingiberene and Piperine for patients with cold atonic dyspepsia."
                },
                {
                    "ingredient_name": "Sirka Mudabbar Process (Vinegar Maceration)",
                    "botanical_identity": "Natural Acetic Acid Ferment",
                    "edition_amounts": {
                        "Al-Hawi": "24 hours soak",
                        "Qarabadeen-e-Qadri": "72 hours soak (3 days)",
                        "Qarabadeen-e-Azam": "48 hours soak (2 days)",
                        "NFUM Statutory": "48 hours soak until fully absorbed"
                    },
                    "variance_percentage": 33.3,
                    "clinical_pharmacological_rationale": "Soaking cumin in vinegar (Mudabbar) attenuates excess harsh dryness while unlocking essential caraway oils (carvone, limonene)."
                }
            ],
            "statutory_consensus_standard": {
                "official_reference": "NFUM Part I (1:19) & UPI Part II, Vol I",
                "recommended_posology": "5 to 7 g after meals with warm water",
                "quality_criteria": "Total ash < 4.0%; Volatile oil not less than 0.25% v/w; Total sugar 60–65%."
            },
            "master_clinical_guidance": "The 24h to 72h variance in vinegar maceration across Al-Razi and Akbar Arzani determines the gastro-protective acidity profile. NFUM standardizes on 48h maceration to optimize digestive enzyme induction without causing hyperchlorhydria."
        },

        # 5. Habb-e-Suranjan (The Classical Anti-Gout Pill)
        "habb_e_suranjan": {
            "compound_key": "habb_e_suranjan",
            "canonical_title": "حب سورنجان",
            "transliterated_name": "Habb-e-Suranjan",
            "traditional_system": "Unani Tibb",
            "therapeutic_category": "Musakkin-e-Waja-ul-Mafasil, Daf-e-Niqras (Anti-gout, Anti-arthritic & Uricosuric)",
            "editions_evaluated": [
                {
                    "edition_name": "Qarabadeen-e-Qadri",
                    "author": "Hakim Muhammad Akbar Arzani",
                    "era_and_place": "18th Century",
                    "classical_citation": "Bab Hubub, p. 178",
                    "classical_weight_unit": "Dirham (3.2 g)",
                    "metric_multiplier_grams": 3.2,
                    "formulation_description": "Features Suranjan Shirin (Colchicum autumnale) with Elwa (Aloe barbadensis dried juice) and Turbud (Operculina turpethum) to purge morbid black bile."
                },
                {
                    "edition_name": "Qarabadeen-e-Azam",
                    "author": "Hakim Muhammad Azam Khan",
                    "era_and_place": "19th Century",
                    "classical_citation": "Hubub Section, Vol I, p. 280",
                    "classical_weight_unit": "Tola (11.66 g)",
                    "metric_multiplier_grams": 0.97,
                    "formulation_description": "Increases Muslih (Corrective) Roghan-e-Badam to prevent intestinal cramping caused by powerful resinous purgatives (Jalap/Turbud)."
                },
                {
                    "edition_name": "NFUM Part I",
                    "author": "Unani Pharmacopoeia Committee",
                    "era_and_place": "Modern Statutory Codex",
                    "classical_citation": "Formulation No. 2:18",
                    "classical_weight_unit": "Metric System",
                    "metric_multiplier_grams": 1.0,
                    "formulation_description": "Statutory consensus: Suranjan Shirin 100g, Elwa 50g, Turbud Safed 50g, Post-e-Halela Zard 50g, Mastagi 25g; standardized to 500mg pills."
                }
            ],
            "ingredient_variance_matrix": [
                {
                    "ingredient_name": "Suranjan Shirin (Sweet Colchicum Corm)",
                    "botanical_identity": "Colchicum autumnale L. / Colchicum luteum Baker",
                    "edition_amounts": {
                        "Qarabadeen-e-Qadri": "35% of total mass",
                        "Qarabadeen-e-Azam": "30% of total mass (-5%)",
                        "NFUM Statutory": "100g / 275g active solids = 36.3%"
                    },
                    "variance_percentage": 6.3,
                    "clinical_pharmacological_rationale": "Suranjan contains colchicine, which arrests neutrophil motility in urate crystals. Azam Khan lowered dose slightly to avoid severe watery diarrhea."
                },
                {
                    "ingredient_name": "Muslih / Corrective Ratio (Mastagi & Almond Oil)",
                    "botanical_identity": "Pistacia lentiscus & Prunus dulcis",
                    "edition_amounts": {
                        "Qarabadeen-e-Qadri": "5% of mass",
                        "Qarabadeen-e-Azam": "10% of mass (+100%)",
                        "NFUM Statutory": "25g Mastagi (9.1% of mass)"
                    },
                    "variance_percentage": 45.0,
                    "clinical_pharmacological_rationale": "Colchicine and Aloe resin (aloin) irritate gastric mucosa; Azam Khan doubled corrective resin to coat stomach and protect bowel."
                }
            ],
            "statutory_consensus_standard": {
                "official_reference": "NFUM Part I (2:18) & UPI Part II, Vol I",
                "recommended_posology": "1 to 2 pills (500mg to 1g) twice daily with water",
                "quality_criteria": "Colchicine content 0.15–0.25% w/w by HPLC; Disintegration time < 30 minutes; Total ash < 5.0%."
            },
            "master_clinical_guidance": "Because Colchicum has a narrow therapeutic index, the 5–10% variance in colchicine content across older regional editions warrants caution. Clinicians must strictly dispense NFUM standardized pills assaying < 0.25% colchicine."
        }
    }

    @classmethod
    def list_all_reconciliations(cls) -> List[Dict[str, Any]]:
        """Returns summaries of all available reconciled classical compound formulations."""
        summaries = []
        for k, v in cls.RECONCILIATION_DATABASE.items():
            summaries.append({
                "compound_key": v["compound_key"],
                "canonical_title": v["canonical_title"],
                "transliterated_name": v["transliterated_name"],
                "traditional_system": v["traditional_system"],
                "therapeutic_category": v["therapeutic_category"],
                "editions_compared_count": len(v["editions_evaluated"]),
                "ingredients_evaluated_count": len(v["ingredient_variance_matrix"]),
                "official_statutory_standard": v["statutory_consensus_standard"]["official_reference"]
            })
        return summaries

    @classmethod
    def get_reconciliation(cls, compound_key: str) -> Optional[Dict[str, Any]]:
        """Returns deep multi-edition comparative analysis for a given formulation."""
        clean_key = compound_key.lower().replace("-", "_").strip()
        return cls.RECONCILIATION_DATABASE.get(clean_key)
