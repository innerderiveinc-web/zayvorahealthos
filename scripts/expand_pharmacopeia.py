#!/usr/bin/env python3
"""
Expand Qarabadeen & Ayurvedic Pharmacopeia
Injects 60 comprehensive classical formulations into qarabadeen_master_library.json & catalog_seed.json
"""
import json
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MASTER_LIB_PATH = os.path.join(ROOT_DIR, "services", "data", "qarabadeen_master_library.json")
CATALOG_SEED_PATH = os.path.join(ROOT_DIR, "catalog_seed.json")

NEW_FORMULATIONS = [
    # ── UNANI FORMULATIONS (NFUM / UPI) ──
    {
        "compound_key": "khamira_marwareed",
        "canonical_title": "خمیرہ مروارید (Khamira Marwareed)",
        "transliterated_name": "Khamira Marwareed",
        "dosage_form": "Khamira (Electuary / Semisolid)",
        "therapeutic_category": "Muqawwi-e-Qalb wa Aaza-e-Raeesah (Cardiotonic & Neuro-Psychic Exhilarant)",
        "temperament": "Mo'tadil Ma'il ba Hararat (Balanced with mild vital warmth)",
        "classical_standard": "NFUM Part I (5.10) / Qarabadeen Qaderi",
        "primary_indications": [
            "Zoaf-e-Qalb (Myocardial asthenia & palpitations)",
            "Khafqan (Cardiac tachyarrhythmia & autonomic panic)",
            "Convalescence following acute infectious diseases (Typhoid, Measles)",
            "Mal-ul-Khulya (Melancholia & psychic distress)"
        ],
        "key_ingredients": [
            {"ingredient": "Marwareed Nasufta (Purified calcined Pearl / Mytilus margaritiferus)", "ratio": "Principal mineral agent"},
            {"ingredient": "Yashab Sabz (Green Jade calx)", "ratio": "Cardioprotective gem mineral"},
            {"ingredient": "Kahruba Shamai (Amber resin)", "ratio": "Hemostatic & cardiac stimulant"},
            {"ingredient": "Zafran (Crocus sativus)", "ratio": "Vital cardiac exhilarant"},
            {"ingredient": "Arq Gaozaban (Borago officinalis aqua)", "ratio": "Exhilarant liquid vehicle"}
        ],
        "standard_dosage": "3 to 5 grams once or twice daily on an empty stomach with milk or Arq Gaozaban.",
        "modern_pharmacology_correlation": "Rich in bioavailable calcium carbonate matrix, micro-trace minerals, and crocin flavonoids; exhibits anti-arrhythmic, neuroprotective, and free-radical quenching properties.",
        "safety_and_precautions": "Contains sugar base (Qiwam). Diabetic patients require caloric monitoring."
    },
    {
        "compound_key": "khamira_gaozaban_ambari_jawaharwala",
        "canonical_title": "خمیرہ گاؤزبان عنبری جواہر والا (Khamira Gaozaban Ambari Jawaharwala)",
        "transliterated_name": "Khamira Gaozaban Ambari Jawaharwala",
        "dosage_form": "Khamira (Gem-enriched Confection)",
        "therapeutic_category": "Muqawwi-e-Dimagh wa Qalb (Cephalic & Myocardial Tonic)",
        "temperament": "Garm 1° / Tar 1° (Mildly Warm & Humid)",
        "classical_standard": "NFUM Part I (5.7) / Bayaz-e-Kabir",
        "primary_indications": [
            "Zoaf-e-Dimagh (Cerebral exhaustion & mental fatigue)",
            "Nisyan (Impaired memory & executive dysfunction)",
            "Khafqan-e-Qalb (Palpitations & cardiac neurosis)",
            "Chronic visual strain & mental asthenia"
        ],
        "key_ingredients": [
            {"ingredient": "Gaozaban (Borago officinalis flowers/leaves)", "ratio": "Principal cephalic & cordiotonic herb"},
            {"ingredient": "Gul-e-Gaozaban (Borage flowers)", "ratio": "Cardiotonic flavones"},
            {"ingredient": "Kashneez Khushk (Coriandrum sativum)", "ratio": "Gastric vapor suppressor"},
            {"ingredient": "Abresham Muqarraz (Bombyx mori silk cocoon)", "ratio": "Endothelial nitric oxide stimulant"},
            {"ingredient": "Amber Ashhab (Ambra grasea)", "ratio": "Potent nervine stimulant"},
            {"ingredient": "Marwareed & Yashab (Pearls & Jade)", "ratio": "Mineral cellular tonic"}
        ],
        "standard_dosage": "3 to 5 grams in the morning with lukewarm milk or water.",
        "modern_pharmacology_correlation": "Modulates central monoamine neurotransmission; silk peptides and borage flavones enhance cerebral perfusion and mitigate oxidative stress in hippocampal neurons.",
        "safety_and_precautions": "Avoid during pregnancy due to trace Amber content."
    },
    {
        "compound_key": "khamira_sandal_sada",
        "canonical_title": "خمیرہ صندل سادہ (Khamira Sandal Sada)",
        "transliterated_name": "Khamira Sandal Sada",
        "dosage_form": "Khamira (Electuary)",
        "therapeutic_category": "Mubarrid wa Mufarreh-e-Qalb (Cardio-refrigerant & Antipyretic Exhilarant)",
        "temperament": "Barid 2° / Yabis 2° (Cold & Dry)",
        "classical_standard": "NFUM Part I (5.14) / Ilaj-ul-Amraz",
        "primary_indications": [
            "Hararat-e-Qalb (Excessive cardiac heat & hot palpitations)",
            "Ghatayan (Nausea with bilious flushing)",
            "Thirst & burning micturition due to systemic Pitta/Safra excess"
        ],
        "key_ingredients": [
            {"ingredient": "Sandal Safaid (Santalum album wood)", "ratio": "Principal refrigerant"},
            {"ingredient": "Kishneez Khushk (Coriandrum sativum)", "ratio": "Cooling carminative"},
            {"ingredient": "Arq Gulab (Rosa damascena distillate)", "ratio": "Distillate vehicle"}
        ],
        "standard_dosage": "5 to 10 grams twice daily with cool water or Arq Gulab.",
        "modern_pharmacology_correlation": "Alpha-santalol content provides central sedative, mild hypotensive, and anti-inflammatory effects.",
        "safety_and_precautions": "Contraindicated in severe cold-dyscrasia asthmatic states."
    },
    {
        "compound_key": "itrifal_kishneezi",
        "canonical_title": "اطریفل کشنیزی (Itrifal Kishneezi)",
        "transliterated_name": "Itrifal Kishneezi",
        "dosage_form": "Itrifal (Triphala Electuary)",
        "therapeutic_category": "Mani-e-Bukharat-e-Meda (Anti-reflux, Gastric Vapor Suppressor & Cephalic Tonic)",
        "temperament": "Barid 1° / Yabis 2° (Cooling & Astringent)",
        "classical_standard": "NFUM Part I (5.22) / Qarabadeen Azam",
        "primary_indications": [
            "Bukharat-e-Meda (Gastro-esophageal acid vapors causing headache)",
            "Suda-e-Meda (Gastric cephalea & postprandial dizziness)",
            "Chronic flatulence & hyperacidity",
            "Bleeding hemorrhoids (Bawaseer Damiya)"
        ],
        "key_ingredients": [
            {"ingredient": "Kishneez Khushk (Coriandrum sativum seed)", "ratio": "Principal acid-vapor suppressor"},
            {"ingredient": "Post Halela Zard (Terminalia chebula yellow)", "ratio": "Gentle bowel regulator"},
            {"ingredient": "Post Halela Siah (Terminalia chebula black)", "ratio": "Gastric tonic"},
            {"ingredient": "Post Balela (Terminalia bellerica)", "ratio": "Astringent mucoprotective"},
            {"ingredient": "Amla (Phyllanthus emblica)", "ratio": "Bioflavonoids & antioxidant"}
        ],
        "standard_dosage": "5 to 10 grams at bedtime with lukewarm water.",
        "modern_pharmacology_correlation": "Coriander linalool suppresses H. pylori growth and inhibits transient lower esophageal sphincter relaxations (TLESRs); tannins promote gastric mucosal re-epithelialization.",
        "safety_and_precautions": "Safe for extended geriatric and adult use; monitor in severe chronic constipation."
    },
    {
        "compound_key": "itrifal_shahtara",
        "canonical_title": "اطریفل شاہترہ (Itrifal Shahtara)",
        "transliterated_name": "Itrifal Shahtara",
        "dosage_form": "Itrifal (Electuary)",
        "therapeutic_category": "Musaffi-e-Dam (Blood Purifier & Dermatological Depurative)",
        "temperament": "Mo'tadil Ma'il ba Burudat (Mildly Cooling & Depurative)",
        "classical_standard": "NFUM Part I (5.24) / Qarabadeen Kabir",
        "primary_indications": [
            "Fasad-e-Dam (Blood dyscrasias & systemic toxemia)",
            "Jarab wa Hikka (Pruritus, chronic urticaria & scabies)",
            "Busoor (Acne vulgaris, boils & pustular dermatoses)",
            "Chronic allergic eczema"
        ],
        "key_ingredients": [
            {"ingredient": "Shahtara (Fumaria parviflora)", "ratio": "Principal blood purifier & hepatobiliary stimulant"},
            {"ingredient": "Chiraita (Swertia chirata)", "ratio": "Bitter anti-inflammatory"},
            {"ingredient": "Post Halela Zard & Balela & Amla", "ratio": "Triphala depurative matrix"},
            {"ingredient": "Sana Makki (Cassia angustifolia)", "ratio": "Gentle systemic eliminator"}
        ],
        "standard_dosage": "5 to 10 grams in the morning and at bedtime with water.",
        "modern_pharmacology_correlation": "Fumaric acid esters and swertiamarin downregulate Th1/Th17 cutaneous inflammatory cytokines, promoting epidermal clearance in plaque psoriasis and eczema.",
        "safety_and_precautions": "Excessive doses may cause loose stools due to trace senna."
    },
    {
        "compound_key": "itrifal_zamani",
        "canonical_title": "اطریفل زمانی (Itrifal Zamani)",
        "transliterated_name": "Itrifal Zamani",
        "dosage_form": "Itrifal (Electuary)",
        "therapeutic_category": "Mushil-e-Akhlat-e-Salasa (Tri-humoral Purgative & Deobstruent)",
        "temperament": "Garm 1° / Yabis 1° (Mildly Warm)",
        "classical_standard": "NFUM Part I (5.25) / Bayaz-e-Kabir",
        "primary_indications": [
            "Qabz-e-Muzmin (Chronic refractory constipation)",
            "Suda-e-Muzmin (Chronic headache linked to colonic toxemia)",
            "Nazla-e-Muzmin (Chronic catarrh & phlegmatic congestion)",
            "Joint pain associated with metabolic waste accumulation"
        ],
        "key_ingredients": [
            {"ingredient": "Post Halela Zard & Kabli & Siah", "ratio": "Comprehensive Chebula rinds"},
            {"ingredient": "Turbud Safaid (Operculina turpethum)", "ratio": "Phlegm and bile purgative"},
            {"ingredient": "Saqmonia (Convolvulus scammonia)", "ratio": "Hydragogue cathartic"},
            {"ingredient": "Gul-e-Surkh (Rosa damascena)", "ratio": "Gastric protector"},
            {"ingredient": "Sena (Cassia angustifolia)", "ratio": "Peristalsis activator"}
        ],
        "standard_dosage": "5 to 10 grams at bedtime with lukewarm water or milk.",
        "modern_pharmacology_correlation": "Stimulates colonic secretomotor neurons via sennosides and turpethin resins; accelerates transit time without mucosal blunting.",
        "safety_and_precautions": "Contraindicated in pregnancy, intestinal obstruction, and acute appendicitis."
    },
    {
        "compound_key": "jawarish_jalinoos",
        "canonical_title": "جوارش جالینوس (Jawarish Jalinoos)",
        "transliterated_name": "Jawarish Jalinoos",
        "dosage_form": "Jawarish (Digestive Confection)",
        "therapeutic_category": "Muqawwi-e-Aaza-e-Batinah (Master Visceral, Stomach, Liver & Bladder Tonic)",
        "temperament": "Garm 2° / Khushk 2° (Warm & Desiccant)",
        "classical_standard": "NFUM Part I (6.11) / Qarabadeen Kabir / Galenic Codex",
        "primary_indications": [
            "Zoaf-e-Meda wa Jigar (Cold gastric atony & sluggish hepatic metabolism)",
            "Zoaf-e-Masana wa Salas-ul-Bawl (Urinary incontinence, nocturia & bladder atony)",
            "Daft-e-Riyah wa Nafakh (Chronic flatulence, abdominal distension)",
            "Premature hair graying & geriatric physical debility"
        ],
        "key_ingredients": [
            {"ingredient": "Mastagi Roomi (Pistacia lentiscus resin)", "ratio": "Mucosal astringent"},
            {"ingredient": "Zanjabeel (Zingiber officinale)", "ratio": "Metabolic thermogenic"},
            {"ingredient": "Filfil Siah & Darfilfil (Piper nigrum & longum)", "ratio": "Bioavailability enhancers"},
            {"ingredient": "Darchini (Cinnamomum zeylanicum)", "ratio": "Microvascular stimulant"},
            {"ingredient": "Qaranfal (Syzygium aromaticum cloves)", "ratio": "Antispasmodic carminative"},
            {"ingredient": "Zafran (Crocus sativus)", "ratio": "Vital cardiac exhilarant"}
        ],
        "standard_dosage": "5 grams twice daily after meals with water or Arq Badiyan.",
        "modern_pharmacology_correlation": "Piperine, gingerols, and cinnamaldehyde increase gastric mucosal blood flow, enhance digestive enzyme secretion (pepsin, amylase, lipase), and increase bladder detrusor tone.",
        "safety_and_precautions": "Use caution in active peptic ulceration or severe hot gastric dyscrasia."
    },
    {
        "compound_key": "jawarish_shahi",
        "canonical_title": "جوارش شاہی (Jawarish Shahi)",
        "transliterated_name": "Jawarish Shahi",
        "dosage_form": "Jawarish (Digestive Confection)",
        "therapeutic_category": "Muqawwi-e-Qalb wa Meda (Cardio-Gastric Tonic & Mild Exhilarant)",
        "temperament": "Mo'tadil Ma'il ba Burudat (Mildly Cooling)",
        "classical_standard": "NFUM Part I (6.13) / Ilaj-ul-Amraz",
        "primary_indications": [
            "Zoaf-e-Qalb wa Meda (Postprandial palpitations & weak digestion)",
            "Khafqan (Cardiac anxiety accompanying dyspepsia)",
            "Burning epigastric sensation & nausea"
        ],
        "key_ingredients": [
            {"ingredient": "Murabba Halela (Terminalia chebula preserve)", "ratio": "Digestive restorative"},
            {"ingredient": "Murabba Amla (Phyllanthus emblica preserve)", "ratio": "Antioxidant base"},
            {"ingredient": "Kishneez Khushk (Coriandrum sativum)", "ratio": "Cooling carminative"},
            {"ingredient": "Ilaichi Khurd (Elettaria cardamomum)", "ratio": "Aromatic digestive"},
            {"ingredient": "Arq Gaozaban (Borage water)", "ratio": "Cardiotonic vehicle"}
        ],
        "standard_dosage": "5 to 10 grams after meals with water.",
        "modern_pharmacology_correlation": "Combines polyphenols from emblica fruits and volatile terpenes from cardamom; promotes gastro-protection without inducing acid rebound.",
        "safety_and_precautions": "Safe for regular use; well-tolerated in geriatric patients."
    },
    {
        "compound_key": "jawarish_mastagi",
        "canonical_title": "جوارش مصطگی (Jawarish Mastagi)",
        "transliterated_name": "Jawarish Mastagi",
        "dosage_form": "Jawarish (Confection)",
        "therapeutic_category": "Muqawwi-e-Meda wa Habis-e-Is-haal (Gastric Tonic & Anti-diarrheal)",
        "temperament": "Garm 2° / Khushk 2° (Warm & Desiccant)",
        "classical_standard": "NFUM Part I (6.14) / Qarabadeen Azam",
        "primary_indications": [
            "Zoaf-e-Hazm (Impaired protein and lipid digestion)",
            "Salas-ul-Bawl (Urinary incontinence and frequency)",
            "Is-haal-e-Muzmin (Chronic non-infectious loose stools & IBS-D)",
            "Excessive salivation & phlegmatic regurgitation"
        ],
        "key_ingredients": [
            {"ingredient": "Mastagi Roomi (Pistacia lentiscus tears)", "ratio": "High-concentration resin matrix"},
            {"ingredient": "Gulab Arq (Rose distillate)", "ratio": "Aromatic binder"},
            {"ingredient": "Qand Safaid (Refined sugar syrup)", "ratio": "Qiwam base"}
        ],
        "standard_dosage": "5 to 7 grams morning and evening before meals with water.",
        "modern_pharmacology_correlation": "Mastic gum triterpenes inhibit H. pylori vacuolating cytotoxin (VacA) and downregulate TNF-alpha in intestinal epithelial cells, consolidating mucosal barrier integrity.",
        "safety_and_precautions": "Avoid in patients with severe intestinal stenosis."
    },
    {
        "compound_key": "jawarish_amla",
        "canonical_title": "جوارش آملہ (Jawarish Amla)",
        "transliterated_name": "Jawarish Amla",
        "dosage_form": "Jawarish (Confection)",
        "therapeutic_category": "Muqawwi-e-Meda wa Habis-e-Dam (Gastric Tonic & Hemostatic)",
        "temperament": "Barid 1° / Yabis 2° (Cool & Astringent)",
        "classical_standard": "NFUM Part I (6.4) / Qarabadeen Qaderi",
        "primary_indications": [
            "Zoaf-e-Meda (Hyperchlorhydria & gastric erosion)",
            "Bawaseer Damiya (Bleeding hemorrhoids)",
            "Khafqan Safrawi (Palpitations provoked by bilious heat)",
            "Chronic gingival bleeding"
        ],
        "key_ingredients": [
            {"ingredient": "Amla Khushk (Phyllanthus emblica dried fruit)", "ratio": "Astringent bioflavonoid base"},
            {"ingredient": "Post Halela Zard (Terminalia chebula)", "ratio": "Astringent tonic"},
            {"ingredient": "Gul-e-Surkh (Rosa damascena)", "ratio": "Anti-inflammatory floral agent"},
            {"ingredient": "Zanjabeel & Zafran", "ratio": "Aromatic modifiers"}
        ],
        "standard_dosage": "5 to 10 grams twice daily after food with water.",
        "modern_pharmacology_correlation": "Rich in emblicanin A & B ellagitannins; stabilizes endothelial capillary walls and attenuates gastric mucosal ulcer indices.",
        "safety_and_precautions": "Safe across all adult age groups."
    },
    {
        "compound_key": "habb_e_shifa",
        "canonical_title": "حب شفاء (Habb-e-Shifa)",
        "transliterated_name": "Habb-e-Shifa",
        "dosage_form": "Habb (Pill)",
        "therapeutic_category": "Daf-e-Humma wa Musakkin-e-Waja (Antipyretic, Analgesic & Febrifuge)",
        "temperament": "Garm 2° / Khushk 2° (Warm & Dry)",
        "classical_standard": "NFUM Part I (2.41) / Qarabadeen Azam",
        "primary_indications": [
            "Humma-e-Ufooniya (Infectious & malarial fevers)",
            "Suda-e-Barid (Tension headache & neuralgic pain)",
            "Inflammatory musculoskeletal arthralgia",
            "Acute catarrhal fever"
        ],
        "key_ingredients": [
            {"ingredient": "Tukhm-e-Dhatura Mudabbar (Detoxified Datura metel seeds)", "ratio": "Potent antispasmodic/analgesic"},
            {"ingredient": "Rewand Chini (Rheum emodi)", "ratio": "Hepatobiliary deobstruent"},
            {"ingredient": "Zanjabeel (Zingiber officinale)", "ratio": "Thermogenic bio-enhancer"},
            {"ingredient": "Samagh-e-Arabi (Acacia arabica gum)", "ratio": "Binding excipient"}
        ],
        "standard_dosage": "1 pill (approx. 250 mg) once or twice daily with lukewarm water.",
        "modern_pharmacology_correlation": "Tropane alkaloids (hyoscyamine, scopolamine) provide peripheral muscarinic blockade, while emodin anthraquinones suppress pyrogenic prostaglandins.",
        "safety_and_precautions": "Contraindicated in glaucoma, benign prostatic hyperplasia (BPH), cardiac arrhythmias, and pregnancy."
    },
    {
        "compound_key": "habb_e_kabid_naushadri",
        "canonical_title": "حب کبد نوشادری (Habb-e-Kabid Naushadri)",
        "transliterated_name": "Habb-e-Kabid Naushadri",
        "dosage_form": "Habb (Pill)",
        "therapeutic_category": "Kasir-e-Riyah wa Mufattih-e-Sudad-e-Kabid (Hepatic Deobstruent & Carminative)",
        "temperament": "Garm 2° / Khushk 2° (Warm & Desiccant)",
        "classical_standard": "NFUM Part I (2.29) / Qarabadeen Ihsani",
        "primary_indications": [
            "Zoaf-e-Kabid (Hepatic insufficiency & sluggish biliary output)",
            "Nafakh-e-Shikam (Abdominal meteorism & tympanites)",
            "Anorexia & dyspepsia associated with chronic liver disease",
            "Splenomegaly & portal congestion"
        ],
        "key_ingredients": [
            {"ingredient": "Naushadar (Ammonium chloride)", "ratio": "Principal osmotic deobstruent"},
            {"ingredient": "Namak Siah (Black salt)", "ratio": "Carminative electrolyte"},
            {"ingredient": "Filfil Siah (Piper nigrum)", "ratio": "Digestive stimulant"},
            {"ingredient": "Halela Siah & Zard", "ratio": "Hepatic cleansing rinds"}
        ],
        "standard_dosage": "1 to 2 pills twice daily after meals with water.",
        "modern_pharmacology_correlation": "Ammonium chloride and black salt stimulate secretin and gastrin release; promotes digestive fluid secretion and reduces biliary sludge.",
        "safety_and_precautions": "Use caution in severe metabolic acidosis, severe renal impairment, or hyperchloremia."
    },
    {
        "compound_key": "habb_e_tinkar",
        "canonical_title": "حب تنکار (Habb-e-Tinkar)",
        "transliterated_name": "Habb-e-Tinkar",
        "dosage_form": "Habb (Pill)",
        "therapeutic_category": "Mushil-e-Balgham wa Mulayyin (Phlegm Laxative & Carminative)",
        "temperament": "Garm 2° / Khushk 2° (Warm & Dry)",
        "classical_standard": "NFUM Part I (2.50) / Bayaz-e-Kabir",
        "primary_indications": [
            "Qabz-e-Muzmin (Atonic constipation)",
            "Qolanj (Intestinal colic caused by viscid phlegm)",
            "Gastric heaviness & anorexia"
        ],
        "key_ingredients": [
            {"ingredient": "Suhaga Mudabbar / Tinkar (Purified Borax)", "ratio": "Alkaline carminative deobstruent"},
            {"ingredient": "Elwa / Musabbar (Aloe barbadensis dried juice)", "ratio": "Stimulant laxative"},
            {"ingredient": "Filfil Siah (Piper nigrum)", "ratio": "Digestive catalyst"},
            {"ingredient": "Ajwain Desi (Trachyspermum ammi)", "ratio": "Thymol antispasmodic"}
        ],
        "standard_dosage": "1 to 2 pills at bedtime with lukewarm water.",
        "modern_pharmacology_correlation": "Aloin anthraquinones stimulate colonic mucosal peristalsis; thymol provides smooth muscle spasmolysis to eliminate cramping.",
        "safety_and_precautions": "Avoid during pregnancy, lactation, and active inflammatory bowel flare-ups."
    },
    {
        "compound_key": "habb_e_asgand",
        "canonical_title": "حب اسگند (Habb-e-Asgand)",
        "transliterated_name": "Habb-e-Asgand",
        "dosage_form": "Habb (Pill)",
        "therapeutic_category": "Musakkin-e-Waja-ul-Mafasil (Anti-arthritic & Nervine Restorative)",
        "temperament": "Garm 2° / Khushk 2° (Warm & Dry)",
        "classical_standard": "NFUM Part I (2.5) / Qarabadeen Azam",
        "primary_indications": [
            "Waja-ul-Mafasil (Osteoarthritis, rheumatoid arthritis, gout)",
            "Irq-un-Nasa (Sciatica & lumbar radiculopathy)",
            "Rikkat-e-Mani wa Zoaf-e-Bah (Oligospermia & sexual debility)",
            "General muscular asthenia"
        ],
        "key_ingredients": [
            {"ingredient": "Asgand Nagori (Withania somnifera)", "ratio": "Principal adaptogen & anti-inflammatory"},
            {"ingredient": "Suranjan Shireen (Colchicum autumnale sweet)", "ratio": "Mild anti-gout agent"},
            {"ingredient": "Musli Safaid & Siah", "ratio": "Nutritive tonics"},
            {"ingredient": "Zanjabeel (Zingiber officinale)", "ratio": "Analgesic bio-enhancer"}
        ],
        "standard_dosage": "1 to 2 pills twice daily with warm milk or water.",
        "modern_pharmacology_correlation": "Withanolides inhibit COX-2 and NF-kB signaling; withaferin A protects articular chondrocytes from proteoglycan depletion.",
        "safety_and_precautions": "Caution in thyroid disorders (Withania increases circulating T4/T3)."
    },
    {
        "compound_key": "sharbat_bazoori_motadil",
        "canonical_title": "شربت بزوری معتدل (Sharbat Bazoori Motadil)",
        "transliterated_name": "Sharbat Bazoori Motadil",
        "dosage_form": "Sharbat (Syrup)",
        "therapeutic_category": "Mudirr-e-Bawl wa Mufattih-e-Sudad (Diuretic, Lithotriptic & Hepato-Renal Depurative)",
        "temperament": "Mo'tadil (Balanced)",
        "classical_standard": "NFUM Part I (10.15) / UPI Part II Vol IV",
        "primary_indications": [
            "Ihtibas-e-Bawl (Oliguria & dysuria)",
            "Sozash-e-Bawl (Urinary tract burning & crystalluria)",
            "Warm-e-Kabid wa Kulyah (Hepato-renal congestion)",
            "Ascites & dependent peripheral edema"
        ],
        "key_ingredients": [
            {"ingredient": "Tukhm-e-Khyarain (Cucumis sativus & melo seeds)", "ratio": "Cooling diuretic seeds"},
            {"ingredient": "Tukhm-e-Kharpaza (Cucumis melo seed)", "ratio": "Renal flushing agent"},
            {"ingredient": "Tukhm-e-Kasni (Cichorium intybus seed)", "ratio": "Hepatic deobstruent"},
            {"ingredient": "Bekh-e-Kasni (Cichorium intybus root)", "ratio": "Diuretic bitter"},
            {"ingredient": "Bekh-e-Badiyan (Foeniculum vulgare root)", "ratio": "Carminative diuretic"}
        ],
        "standard_dosage": "25 to 50 ml mixed with 150 ml of lukewarm or fresh water twice daily.",
        "modern_pharmacology_correlation": "Flavonoids and organic potassium salts induce aquaresis without depleting sodium; accelerates renal uric acid clearance and urinary crystal dissolution.",
        "safety_and_precautions": "Contains cane sugar syrup (Qiwam). Diabetic patients should utilize sugar-free decoction equivalents."
    },
    {
        "compound_key": "sharbat_anar",
        "canonical_title": "شربت انار (Sharbat Anar)",
        "transliterated_name": "Sharbat Anar",
        "dosage_form": "Sharbat (Fruit Syrup)",
        "therapeutic_category": "Musakkin-e-Safra wa Muqawwi-e-Meda (Bile Pacifier, Hepato-Gastric Tonic & Antiemetic)",
        "temperament": "Barid 2° / Yabis 1° (Cool & Astringent)",
        "classical_standard": "NFUM Part I (10.3) / Qarabadeen Kabir",
        "primary_indications": [
            "Ghalba-e-Safra (Excessive bilious humor provoking nausea and vomiting)",
            "Qay wa Ghatayan (Pregnancy and bilious morning sickness)",
            "Atash-e-Mufrit (Morbid excessive polydipsia)",
            "Diarrhea associated with intestinal inflammation"
        ],
        "key_ingredients": [
            {"ingredient": "Ab-e-Anar Shireen (Punica granatum sweet juice)", "ratio": "Electrolyte & polyphenol base"},
            {"ingredient": "Ab-e-Anar Tursh (Punica granatum sour juice)", "ratio": "Acidic astringent vehicle"},
            {"ingredient": "Qand Safaid (Refined sugar)", "ratio": "Syrup base"}
        ],
        "standard_dosage": "25 to 50 ml diluted with chilled or normal water twice daily.",
        "modern_pharmacology_correlation": "Punicalagin ellagitannins exhibit potent gastric cytoprotection, scavenge superoxide radicals, and inhibit 5-HT3 enteric serotonin receptors to suppress nausea.",
        "safety_and_precautions": "Safe in pregnancy; highly recommended for hyperemesis gravidarum."
    },
    {
        "compound_key": "sharbat_faulad",
        "canonical_title": "شربت فولاد (Sharbat Faulad)",
        "transliterated_name": "Sharbat Faulad",
        "dosage_form": "Sharbat (Mineral Tonic Syrup)",
        "therapeutic_category": "Muwallid-e-Dam wa Muqawwi-e-Jigar (Hematinic, Erythropoietic & Hepatic Tonic)",
        "temperament": "Garm 1° / Khushk 2° (Mildly Warm & Desiccant)",
        "classical_standard": "NFUM Part I (10.9) / Bayaz-e-Kabir",
        "primary_indications": [
            "Su-ul-Qinya wa Khillat-e-Dam (Microcytic hypochromic anemia & pallor)",
            "Zoaf-e-Jigar (Hepatic sluggishness leading to impaired hematopoiesis)",
            "General debility, anorexia & post-infectious convalescence"
        ],
        "key_ingredients": [
            {"ingredient": "Buraada-e-Faulad / Iron rust / filings (Processed Iron)", "ratio": "Elemental iron micro-particles"},
            {"ingredient": "Sirka Desi (Fermented cane vinegar)", "ratio": "Organic acetic acid solubilizer"},
            {"ingredient": "Zafran & Mastagi & Qaranfal", "ratio": "Aromatic digestive synergists"}
        ],
        "standard_dosage": "10 to 15 ml diluted with water or milk twice daily after meals.",
        "modern_pharmacology_correlation": "Organic ferrous acetate complexes provide superior duodenal absorption with significantly lower incidence of epigastric pain or severe constipation compared to synthetic ferrous sulfate.",
        "safety_and_precautions": "Do not co-administer simultaneously with dairy or tetracyclines; space by 2 hours."
    },
    {
        "compound_key": "sharbat_unnab",
        "canonical_title": "شربت عناب (Sharbat Unnab)",
        "transliterated_name": "Sharbat Unnab",
        "dosage_form": "Sharbat (Syrup)",
        "therapeutic_category": "Musaffi-e-Dam wa Musakkin-e-Sual (Blood Purifier & Antitussive Demulcent)",
        "temperament": "Mo'tadil Ma'il ba Burudat (Mildly Cooling & Demulcent)",
        "classical_standard": "NFUM Part I (10.22) / Qarabadeen Azam",
        "primary_indications": [
            "Sual-e-Haar (Dry irritant cough & bronchitis)",
            "Hiddat-e-Dam (Blood heat, prickly heat, furunculosis)",
            "Nazla wa Zukam (Catarrhal pharyngitis & dry rhinitis)"
        ],
        "key_ingredients": [
            {"ingredient": "Unnab (Zizyphus jujuba fruit)", "ratio": "Principal mucilaginous demulcent"},
            {"ingredient": "Qand Safaid (Sugar syrup)", "ratio": "Excipient base"}
        ],
        "standard_dosage": "25 to 50 ml diluted with warm water twice daily.",
        "modern_pharmacology_correlation": "Zizyphus polysaccharides coat inflamed pharyngeal receptors, suppress capsaicin-induced cough reflexes, and exhibit immunostimulatory macrophage activation.",
        "safety_and_precautions": "Safe across pediatric and adult populations."
    },
    {
        "compound_key": "sharbat_toot_siah",
        "canonical_title": "شربت توت سیاہ (Sharbat Toot Siah)",
        "transliterated_name": "Sharbat Toot Siah",
        "dosage_form": "Sharbat (Berry Syrup)",
        "therapeutic_category": "Daf-e-Khuzaq wa Warm-e-Halaq (Anti-pharyngitis, Anti-laryngitis & Vocal Cord Demulcent)",
        "temperament": "Barid 2° / Yabis 1° (Cool & Astringent)",
        "classical_standard": "NFUM Part I (10.21) / Qarabadeen Kabir",
        "primary_indications": [
            "Khuzaq (Acute catarrhal tonsillitis & pharyngitis)",
            "Bohat-us-Sawt (Hoarseness of voice, aphonia & vocal cord fatigue)",
            "Diphtheritic irritation & mouth ulcers"
        ],
        "key_ingredients": [
            {"ingredient": "Toot Siah (Morus nigra black mulberry concentrated juice)", "ratio": "Anthocyanin rich active berry base"},
            {"ingredient": "Qand Safaid", "ratio": "Demulcent syrup matrix"}
        ],
        "standard_dosage": "15 to 25 ml slowly sipped or gargled undiluted, 3 to 4 times daily.",
        "modern_pharmacology_correlation": "Cyanidin-3-glucoside and rutin flavonoids provide direct topical anti-inflammatory and bactericidal effects against Streptococcus pyogenes while soothing vocal fold mucosa.",
        "safety_and_precautions": "Avoid immediately drinking cold water after swallowing to maximize local mucosal contact time."
    },
    {
        "compound_key": "majun_falasifa",
        "canonical_title": "معجون فلاسفہ (Majun Falasifa)",
        "transliterated_name": "Majun Falasifa",
        "dosage_form": "Majun (Electuary)",
        "therapeutic_category": "Muqawwi-e-Asab, Kulyah wa Masana (Nervine, Renal, Bladder & Geriatric Tonic)",
        "temperament": "Garm 2° / Khushk 2° (Warm & Dry)",
        "classical_standard": "NFUM Part I (4.15) / Qarabadeen-e-Qadeem",
        "primary_indications": [
            "Zoaf-e-Kulyah wa Masana (Renal asthenia, polyuria & bladder sphincter weakness)",
            "Salas-ul-Bawl (Urinary incontinence & geriatric nocturia)",
            "Zoaf-e-Asab (Peripheral neuropathy & cognitive fatigue)",
            "Waja-ul-Zahr (Lumbago, chronic lower back pain)"
        ],
        "key_ingredients": [
            {"ingredient": "Maghz Chilgoza (Pinus gerardiana pine nuts)", "ratio": "Neuro-nutritive lipid"},
            {"ingredient": "Tukhm-e-Babuna (Matricaria chamomilla seeds)", "ratio": "Antispasmodic carminative"},
            {"ingredient": "Filfil Siah & Darfilfil", "ratio": "Metabolic catalysts"},
            {"ingredient": "Salab Misri (Orchis latifolia)", "ratio": "Aphrodisiac restorative"},
            {"ingredient": "Post Halela Zard & Amla", "ratio": "Digestive regulators"}
        ],
        "standard_dosage": "5 to 10 grams in the morning or at bedtime with lukewarm milk.",
        "modern_pharmacology_correlation": "Improves neuromuscular synaptic transmission and bladder neck muscular tone; enhances peripheral nitric oxide synthesis and protects renal tubular architecture from chronic oxidative decay.",
        "safety_and_precautions": "Avoid in patients with acute inflammatory fever or active hematuria."
    },
    {
        "compound_key": "majun_chobchini",
        "canonical_title": "معجون چوب چینی (Majun Chobchini)",
        "transliterated_name": "Majun Chobchini",
        "dosage_form": "Majun (Electuary)",
        "therapeutic_category": "Musaffi-e-Dam wa Daf-e-Waja-ul-Mafasil (Blood Depurative, Anti-arthritic & Alterative)",
        "temperament": "Garm 2° / Khushk 2° (Warm & Desiccant)",
        "classical_standard": "NFUM Part I (4.7) / Qarabadeen Kabir",
        "primary_indications": [
            "Waja-ul-Mafasil Muzmin (Chronic polyarthritis, rheumatoid conditions)",
            "Niqras (Chronic gouty arthropathy & tophi)",
            "Irq-un-Nasa (Chronic sciatica)",
            "Syphilitic skin lesions & chronic constitutional toxemia"
        ],
        "key_ingredients": [
            {"ingredient": "Chobchini (Smilax china rhizome)", "ratio": "Principal anti-spirochetal and alterative saponin base"},
            {"ingredient": "Suranjan Shireen (Colchicum autumnale)", "ratio": "Anti-inflammatory purine clearing agent"},
            {"ingredient": "Sana Makki & Asgand & Zanjabeel", "ratio": "Depurative & analgesic synergists"}
        ],
        "standard_dosage": "5 to 7 grams twice daily with warm milk or decoction of Ushba.",
        "modern_pharmacology_correlation": "Smilax steroidal saponins bind bacterial endotoxins within the gut lumen and downregulate serum matrix metalloproteinases (MMP-1, MMP-3) in synovial tissue.",
        "safety_and_precautions": "Maintain adequate daily water intake; monitor renal function if used chronically."
    },
    {
        "compound_key": "majun_suranjan",
        "canonical_title": "معجون سرنجان (Majun Suranjan)",
        "transliterated_name": "Majun Suranjan",
        "dosage_form": "Majun (Electuary)",
        "therapeutic_category": "Daf-e-Niqras wa Musakkin-e-Waja-ul-Mafasil (Anti-gout, Anti-arthritic & Uric Acid Depurative)",
        "temperament": "Garm 2° / Khushk 2° (Warm & Dry)",
        "classical_standard": "NFUM Part I (4.32) / Qarabadeen Azam",
        "primary_indications": [
            "Niqras (Acute & chronic gouty arthritis)",
            "Waja-ul-Mafasil (Joint stiffness & inflammatory swelling)",
            "Sciatica & chronic lumbar myositis"
        ],
        "key_ingredients": [
            {"ingredient": "Suranjan Shireen (Colchicum autumnale sweet)", "ratio": "Colchicine alkaloid source"},
            {"ingredient": "Post Halela Zard (Terminalia chebula)", "ratio": "Humoral evacuator"},
            {"ingredient": "Turbud Safaid (Operculina turpethum)", "ratio": "Hydragogue purgative"},
            {"ingredient": "Sheham-e-Hanzal (Citrullus colocynthis pulp)", "ratio": "Potent anti-inflammatory purgative"},
            {"ingredient": "Zanjabeel (Zingiber officinale)", "ratio": "Thermogenic bio-enhancer"}
        ],
        "standard_dosage": "5 grams at bedtime with lukewarm water.",
        "modern_pharmacology_correlation": "Suppresses neutrophil microtubule extravasation and inhibits NLRP3 inflammasome cleaving of pro-IL-1beta in urate crystal deposition sites.",
        "safety_and_precautions": "Contraindicated in eGFR <30 mL/min, severe diarrhea, active pregnancy, and concurrent macrolide antibiotic therapy."
    },
    {
        "compound_key": "majun_kundur",
        "canonical_title": "معجون کندر (Majun Kundur)",
        "transliterated_name": "Majun Kundur",
        "dosage_form": "Majun (Electuary)",
        "therapeutic_category": "Habis-e-Bawl wa Muqawwi-e-Masana (Bladder Sphincter Tonic & Anti-incontinence)",
        "temperament": "Garm 2° / Khushk 2° (Warm & Astringent)",
        "classical_standard": "NFUM Part I (4.26) / Bayaz-e-Kabir",
        "primary_indications": [
            "Salas-ul-Bawl (Urinary incontinence, stress incontinence)",
            "Bawl fil Firash (Nocturnal enuresis in children & young adults)",
            "Zoaf-e-Quwwat-e-Masika Masana (Atony of bladder retentive faculty)"
        ],
        "key_ingredients": [
            {"ingredient": "Kundur (Boswellia serrata oleo-gum-resin)", "ratio": "Principal astringent resin"},
            {"ingredient": "Juft Baloot (Quercus infectoria acorn cups)", "ratio": "Potent tannin astringent"},
            {"ingredient": "Post Halela Zard & Zanjabeel", "ratio": "Digestive restoratives"}
        ],
        "standard_dosage": "5 grams twice daily with lukewarm water or milk.",
        "modern_pharmacology_correlation": "Boswellic acids and condensed tannins tighten visceral mucosal sphincters, decrease detrusor hyperreflexia, and inhibit 5-lipoxygenase mediated pelvic floor inflammation.",
        "safety_and_precautions": "Avoid during acute bacterial cystitis until infection is resolved."
    },
    {
        "compound_key": "roghan_badam_shirin",
        "canonical_title": "روغن بادام شیریں (Roghan Badam Shirin)",
        "transliterated_name": "Roghan Badam Shirin",
        "dosage_form": "Roghan (Cold-Pressed Fixed Oil)",
        "therapeutic_category": "Muqawwi-e-Dimagh, Munawwim wa Mulayyin (Nervine Restorative, Somnifacient & Emollient Laxative)",
        "temperament": "Mo'tadil Ma'il ba Rutubat (Balanced & Intensely Moistening)",
        "classical_standard": "NFUM Part I (8.4) / UPI Part I",
        "primary_indications": [
            "Yubosat-e-Dimagh (Cerebral dryness provoking intractable insomnia & anxiety)",
            "Qabz-e-Yabis (Dry, spastic constipation)",
            "Chronic dry cough & hoarseness of voice",
            "Scalp dryness & mental exhaustion (applied topically and intranasally as Saoot)"
        ],
        "key_ingredients": [
            {"ingredient": "Maghz Badam Shireen (Prunus amygdalus dulcis kernel)", "ratio": "100% pure cold-pressed virgin oil"}
        ],
        "standard_dosage": "Oral: 5 to 10 ml in 200 ml of warm milk at bedtime. Intranasal: 2 drops in each nostril before sleep.",
        "modern_pharmacology_correlation": "High concentrations of oleic acid (omega-9), linoleic acid, and alpha-tocopherol enhance blood-brain barrier phospholipid integrity, modulate cortical GABA receptors, and soften colonic fecal matter.",
        "safety_and_precautions": "Contraindicated in individuals with confirmed tree nut anaphylaxis."
    },
    {
        "compound_key": "tiryaq_e_arba",
        "canonical_title": "تریاق اربعہ (Tiryaq-e-Arba)",
        "transliterated_name": "Tiryaq-e-Arba",
        "dosage_form": "Tiryaq (Theriac / Electuary)",
        "therapeutic_category": "Daf-e-Sumoom wa Mufattih-e-Sudad (Quadruplex Antidote, Antispasmodic & Neuro-protective)",
        "temperament": "Garm 3° / Khushk 3° (Strongly Warm & Desiccant)",
        "classical_standard": "NFUM Part I (11.1) / Galenic & Avicennian Pharmacopeia",
        "primary_indications": [
            "Falij wa Laqwa (Ischemic stroke, hemiplegia, facial nerve paralysis)",
            "Khadar wa Waja-ul-Asab (Peripheral numbness & neuralgic cold dyscrasia)",
            "Muscular spasms & visceral cold colic",
            "Antidote to animal and vegetable cold poisons"
        ],
        "key_ingredients": [
            {"ingredient": "Habbal Ghar (Laurus nobilis laurel berries)", "ratio": "Potent antispasmodic aromatic"},
            {"ingredient": "Zarawand Mudaharaj (Aristolochia rotunda)", "ratio": "Classical deobstruent"},
            {"ingredient": "Murr Makki (Commiphora myrrha gum-resin)", "ratio": "Antimicrobial & tissue preserver"},
            {"ingredient": "Juntiana (Gentiana lutea root)", "ratio": "Bitter neuro-stimulant"},
            {"ingredient": "Asal Khalis (Pure honey matrix)", "ratio": "Electuary base"}
        ],
        "standard_dosage": "1 to 2 grams once daily with Arq Gaozaban or lukewarm water.",
        "modern_pharmacology_correlation": "1,8-cineole and gentiopicroside stimulate corticospinal motor neurons, enhance microvascular reperfusion, and provide powerful neuro-immunomodulatory effects in chronic neurodegenerative states.",
        "safety_and_precautions": "High potency. Strictly contraindicated in pregnancy, acute fever, and severe bilious heat states."
    },

    # ── AYURVEDIC FORMULATIONS (AFI / API) ──
    {
        "compound_key": "arogyavardhini_vati",
        "canonical_title": "आरोग्यवर्धिनी वटी (Arogyavardhini Vati)",
        "transliterated_name": "Arogyavardhini Vati",
        "dosage_form": "Vati / Gutika (Tablet)",
        "therapeutic_category": "Deepana, Pachana, Yakrit-Pliharogahara (Master Hepatoprotective & Metabolic Catalyst)",
        "temperament": "Ushna & Teekshna (Tridosha Shamaka, particularly Kapha-Pitta)",
        "classical_standard": "Rasendrasara Samgraha / AFI Part I (20:4)",
        "primary_indications": [
            "Yakrit Vikara (Hepatic dysfunction, hepatitis, fatty liver/NAFLD)",
            "Medoroga (Metabolic syndrome, hyperlipidemia, obesity)",
            "Kushtha (Chronic inflammatory dermatoses, eczema, psoriasis)",
            "Jirna Jwara (Chronic low-grade fevers & malabsorption)"
        ],
        "key_ingredients": [
            {"ingredient": "Shuddha Parada & Gandhaka (Kajjali)", "ratio": "Bioavailability catalytic mineral base"},
            {"ingredient": "Lauha Bhasma & Tamra Bhasma & Abhraka Bhasma", "ratio": "Calcined therapeutic metallic micro-complexes"},
            {"ingredient": "Triphala & Shilajit & Guggulu", "ratio": "Depurative & hypolipidemic matrix"},
            {"ingredient": "Chitramooka (Plumbago zeylanica)", "ratio": "Digestive fire stimulant"},
            {"ingredient": "Katuki (Picrorhiza kurroa)", "ratio": "50% bulk principal cholagogue herb"}
        ],
        "standard_dosage": "250 to 500 mg (1-2 tablets) twice daily after meals with lukewarm water or Punarnavadi Kashayam.",
        "modern_pharmacology_correlation": "Picrosides I & II stimulate hepatocyte regeneration, normalize elevated ALT/AST/bilirubin, downregulate SREBP-1c in hepatic steatosis, and inhibit lipid peroxidation.",
        "safety_and_precautions": "Contraindicated in severe kidney disease (eGFR <30 mL/min) and pregnancy due to mineral calx content."
    },
    {
        "compound_key": "chyavanprash",
        "canonical_title": "च्यवनप्राश (Chyavanprash Rasayana)",
        "transliterated_name": "Chyavanprash",
        "dosage_form": "Avaleha (Nutritive Herbal Jam)",
        "therapeutic_category": "Rasayana, Balya wa Kasa-Shwasahara (Immuno-modulator, Respiratory & Longevity Tonic)",
        "temperament": "Tridosha Shamaka (Balancing to Vata, Pitta, and Kapha)",
        "classical_standard": "Charaka Samhita Chikitsasthana 1:1 / AFI Part I (3:11)",
        "primary_indications": [
            "Dhatukshaya (General tissue debility, physical and mental exhaustion)",
            "Kasa wa Shwasa (Recurrent respiratory tract infections, bronchial asthma)",
            "Ojas Kshaya (Depleted cellular immunity)",
            "Geriatric restorative & pediatric convalescence"
        ],
        "key_ingredients": [
            {"ingredient": "Amalaki (Phyllanthus emblica fresh fruits)", "ratio": "Principal bioflavonoid & natural Vitamin C matrix"},
            {"ingredient": "Dashamula (Ten classical rejuvenative roots)", "ratio": "Neuro-muscular tonic"},
            {"ingredient": "Ashtavarga & Pippali & Guduchi", "ratio": "Immunomodulatory herbal group"},
            {"ingredient": "Ghrita & Til Taila & Madhu", "ratio": "Lipophilic absorption vehicle"}
        ],
        "standard_dosage": "10 to 15 grams once or twice daily, ideally followed by a cup of warm milk.",
        "modern_pharmacology_correlation": "Enhances natural killer (NK) cell activity, phagocytic index, and mucosal IgA secretion; rich in polyphenols that reverse telomeric oxidative shortening.",
        "safety_and_precautions": "Diabetic individuals require sugar-free Chyavanprash formulations."
    },
    {
        "compound_key": "ashwagandharishta",
        "canonical_title": "अश्वगन्धारिष्ट (Ashwagandharishta)",
        "transliterated_name": "Ashwagandharishta",
        "dosage_form": "Arishta (Naturally Fermented Biomedical Elixir)",
        "therapeutic_category": "Medhya, Balya, Rasayana (Nervine Adaptogen, Anxiolytic & Restorative)",
        "temperament": "Ushna Virya / Madhura Vipaka (Vata-Kapha Shamaka)",
        "classical_standard": "Bhaishajya Ratnavali / AFI Part I (1:4)",
        "primary_indications": [
            "Murchha wa Apasmara (Syncope, neurosis, panic disorders)",
            "Unmada (Anxiety neurosis, depressive exhaustion, insomnia)",
            "Karshya (Cachexia, involuntary weight loss & general weakness)",
            "Shukradosha (Asthenozoospermia & sexual asthenia)"
        ],
        "key_ingredients": [
            {"ingredient": "Ashwagandha (Withania somnifera)", "ratio": "Principal adaptogen"},
            {"ingredient": "Mushali & Manjistha & Haridra", "ratio": "Depuratives & rejuvenators"},
            {"ingredient": "Yashtimadhu & Rasna & Vidari", "ratio": "Nervine balancers"},
            {"ingredient": "Dhataki Pushpa (Woodfordia fruticosa)", "ratio": "Natural self-generating fermentation catalyst"}
        ],
        "standard_dosage": "15 to 25 ml with an equal quantity of water twice daily immediately after meals.",
        "modern_pharmacology_correlation": "Fermentation yields withanolide aglycones with heightened blood-brain barrier permeability; modulates central GABA-A receptors and normalizes hypothalamic-pituitary-adrenal (HPA) cortisol axes.",
        "safety_and_precautions": "Contains 5-10% self-generated natural alcohol; use with caution in active hyperacidity."
    },
    {
        "compound_key": "saraswatarishta",
        "canonical_title": "सारस्वतारिष्ट (Saraswatarishta)",
        "transliterated_name": "Saraswatarishta",
        "dosage_form": "Arishta (Fermented Nootropic Elixir)",
        "therapeutic_category": "Medhya Rasayana, Smritisada (Cognitive Enhancer, Nootropic & Vocal Tonic)",
        "temperament": "Tridosha Shamaka (Sattvic & Nervine Harmonizer)",
        "classical_standard": "Bhaishajya Ratnavali / AFI Part I (1:36)",
        "primary_indications": [
            "Smriti Kshaya (Dementia, Alzheimer-type cognitive decline, amnesia)",
            "Manodosa (Anxiety, neurogenic stuttering, performance stage fear)",
            "Svarabheda (Hoarseness of voice & vocal fatigue in singers/speakers)",
            "Attention Deficit Hyperactivity Disorder (ADHD) in adolescents"
        ],
        "key_ingredients": [
            {"ingredient": "Brahmi (Bacopa monnieri)", "ratio": "Principal nootropic bacoside herb"},
            {"ingredient": "Shatavari & Vidari & Ashwagandha", "ratio": "Neuro-nutritive adaptogens"},
            {"ingredient": "Vacha (Acorus calamus)", "ratio": "Speech & cerebral clarity enhancer"},
            {"ingredient": "Swarna Vark (Pure Gold Leaf)", "ratio": "Cognitive catalyst in traditional preparations"}
        ],
        "standard_dosage": "12 to 24 ml with equal quantity of water twice daily after food.",
        "modern_pharmacology_correlation": "Bacosides A & B promote dendritic arborization, facilitate synaptic transmission in hippocampal cholinergic neurons, and inhibit acetylcholinesterase (AChE).",
        "safety_and_precautions": "Well-tolerated; take after meals to avoid mild gastric irritation from Vacha."
    },
    {
        "compound_key": "avipattikar_churna",
        "canonical_title": "अविपत्तिकर चूर्ण (Avipattikar Churna)",
        "transliterated_name": "Avipattikar Churna",
        "dosage_form": "Churna (Micronized Herbal Powder)",
        "therapeutic_category": "Amlapitta-hara, Pitta-Virechana (Antacid, Anti-reflux & Mild Laxative)",
        "temperament": "Sheeta Virya / Madhura Vipaka (Potent Pitta Pacifier)",
        "classical_standard": "Bhaishajya Ratnavali Amlapittadhikara / AFI Part I (7:2)",
        "primary_indications": [
            "Amlapitta (Gastroesophageal reflux disease, non-ulcer dyspepsia, hyperchlorhydria)",
            "Chhardi (Acid vomiting & burning regurgitation)",
            "Vibandha (Constipation associated with high gastric Pitta heat)",
            "Urinary burning & hot flushes"
        ],
        "key_ingredients": [
            {"ingredient": "Trikatu (Shunthi, Maricha, Pippali)", "ratio": "Metabolic stimulant balance"},
            {"ingredient": "Triphala (Haritaki, Bibhitaki, Amalaki)", "ratio": "Gentle mucosal cleansing"},
            {"ingredient": "Musta & Vidanga & Ela & Patra", "ratio": "Carminative antispasmodics"},
            {"ingredient": "Trivrit (Operculina turpethum)", "ratio": "Gentle Pitta-purgative resin"},
            {"ingredient": "Sharkara (Cane sugar)", "ratio": "50% soothing refrigerant base"}
        ],
        "standard_dosage": "3 to 6 grams twice daily before or after meals with cold/lukewarm water or honey.",
        "modern_pharmacology_correlation": "Neutralizes excess free gastric hydrochloric acid, accelerates gastric emptying time, and provides mucosal cytoprotection via prostaglandin stimulation.",
        "safety_and_precautions": "Caution in diabetic patients due to high sugar component."
    },
    {
        "compound_key": "brahmi_ghrita",
        "canonical_title": "ब्राह्मी घृत (Brahmi Ghrita)",
        "transliterated_name": "Brahmi Ghrita",
        "dosage_form": "Ghrita (Medicated Cow Ghee)",
        "therapeutic_category": "Medhya Rasayana, Apasmara-Unmadahara (Neuro-Psychiatric & Anti-epileptic Lipid)",
        "temperament": "Sheeta Virya (Pitta-Vata Shamaka, crosses Blood-Brain Barrier)",
        "classical_standard": "Ashtanga Hridaya Uttarasthana / AFI Part I (6:32)",
        "primary_indications": [
            "Apasmara (Epilepsy, seizure disorders, post-ictal cognitive fog)",
            "Unmada (Bipolar disorder, chronic schizophrenia adjunct, anxiety)",
            "Vak-Gadha (Speech delay, stuttering & intellectual impairment in children)",
            "Chronic neurodegenerative memory decline"
        ],
        "key_ingredients": [
            {"ingredient": "Brahmi Svarasa (Bacopa monnieri fresh leaf juice)", "ratio": "Primary bioactive lipid-soluble extract"},
            {"ingredient": "Go-Ghrita (Pure Indigenous Cow Ghee)", "ratio": "Lipophilic blood-brain barrier carrier"},
            {"ingredient": "Vacha & Kushtha & Shankhapushpi", "ratio": "Synergistic nootropic herbs"}
        ],
        "standard_dosage": "5 to 10 grams on an empty stomach in the morning with warm milk or lukewarm water.",
        "modern_pharmacology_correlation": "Short- and medium-chain fatty acids in cow ghee escort bacoside saponins across lipophilic cerebral microvessels; suppresses pentylenetetrazol-induced kindling and upregulates brain-derived neurotrophic factor (BDNF).",
        "safety_and_precautions": "Monitor serum lipid profile during prolonged usage in hyperlipidemic patients."
    },
    {
        "compound_key": "mahasudarshan_churna",
        "canonical_title": "महासुदर्शन चूर्ण (Mahasudarshan Churna)",
        "transliterated_name": "Mahasudarshan Churna",
        "dosage_form": "Churna (Polyherbal Bitter Powder)",
        "therapeutic_category": "Sarva Jwarahara, Pitta-rechaka (Broad-Spectrum Antipyretic, Antimalarial & Hepatic Detoxifier)",
        "temperament": "Sheeta Virya / Tikta Rasa (Potent Pitta-Kapha Depurative)",
        "classical_standard": "Sharangadhara Samhita Madhyamakhanda / AFI Part I (7:26)",
        "primary_indications": [
            "Sarva Jwara (Acute viral fevers, malaria, typhoid, dengue, fever of unknown origin)",
            "Yakrit-Pliha Vikara (Spleno-hepatomegaly, toxic jaundice)",
            "Agnimandya (Loss of appetite following systemic infections)",
            "Metabolic toxemia & inflammatory skin eruptions"
        ],
        "key_ingredients": [
            {"ingredient": "Kiratatikta (Swertia chirata)", "ratio": "50% principal bitter antipyretic core"},
            {"ingredient": "Fifty-three classical bitter herbs (Triphala, Trikatu, Haridra, Guduchi, Nimba)", "ratio": "Comprehensive phytotherapeutic matrix"}
        ],
        "standard_dosage": "2 to 4 grams twice or thrice daily with lukewarm water.",
        "modern_pharmacology_correlation": "Amarogentin and swertiamarin block cyclooxygenase-2 (COX-2) in hypothalamic thermoregulatory centers, suppress pro-inflammatory IL-6/TNF-alpha, and exhibit direct schizonticidal and viral replication inhibitory properties.",
        "safety_and_precautions": "Intensely bitter taste; can be encapsulated. Safe for short-term and medium-term acute care."
    },
    {
        "compound_key": "sitopaladi_churna",
        "canonical_title": "सितोपलादि चूर्ण (Sitopaladi Churna)",
        "transliterated_name": "Sitopaladi Churna",
        "dosage_form": "Churna (Expectorant Powder)",
        "therapeutic_category": "Kasa-Shwasa-hara, Deepana (Broncho-pulmonary Tonic, Expectorant & Antiallergic)",
        "temperament": "Sheeta Virya / Madhura Vipaka (Pitta-Vata Balancing)",
        "classical_standard": "Sharangadhara Samhita Madhyamakhanda / AFI Part I (7:34)",
        "primary_indications": [
            "Kasa (Chronic dry & productive bronchitis, allergic cough)",
            "Shwasa (Bronchial asthma & exertional dyspnea)",
            "Kshaya (Pulmonary tuberculosis convalescence)",
            "Burning sensations in hands & feet (Hasta-pada daha)",
            "Anorexia & feverish feeling"
        ],
        "key_ingredients": [
            {"ingredient": "Sitopala (Rock sugar crystal powder)", "ratio": "16 parts (Soothing base)"},
            {"ingredient": "Vamshalochana (Bambusa arundinacea silica)", "ratio": "8 parts (Pulmonary restorative)"},
            {"ingredient": "Pippali (Piper longum)", "ratio": "4 parts (Bronchodilator & bioavailability enhancer)"},
            {"ingredient": "Ela (Elettaria cardamomum)", "ratio": "2 parts (Carminative bronchodilator)"},
            {"ingredient": "Twak (Cinnamomum zeylanicum)", "ratio": "1 part (Antimicrobial)"}
        ],
        "standard_dosage": "2 to 4 grams, 2 to 3 times daily with honey and pure cow ghee.",
        "modern_pharmacology_correlation": "Piperine relaxes bronchial smooth muscles; bamboo silica provides natural cellular repair of alveolar membranes; inhibits mast cell degranulation and histamine release.",
        "safety_and_precautions": "Extremely safe in pediatrics, pregnancy, and elderly. Diabetic patients require sugar-free alternatives."
    },
    {
        "compound_key": "punarnavadi_kashayam",
        "canonical_title": "पुनर्नवादि कषायम् (Punarnavadi Kashayam)",
        "transliterated_name": "Punarnavadi Kashayam",
        "dosage_form": "Kashayam (Decoction / Liquid Extract)",
        "therapeutic_category": "Shophahara, Mutravirechaniya (Systemic Anti-edematous, Diuretic & Nephroprotective)",
        "temperament": "Ushna Virya / Katu-Tikta Rasa (Kapha-Vata Shamaka)",
        "classical_standard": "Sahasrayoga / AFI Part I (4:20)",
        "primary_indications": [
            "Sarvanga Shopha (Anasarca, dependent pedal edema, renal edema)",
            "Jalodara (Ascites in cirrhosis and nephrotic syndrome)",
            "Mutrakricchra (Dysuria, oliguria, chronic glomerulonephritis)",
            "Pandu (Anemia associated with fluid retention)"
        ],
        "key_ingredients": [
            {"ingredient": "Punarnava (Boerhavia diffusa)", "ratio": "Principal aquaretic & nephro-regenerative herb"},
            {"ingredient": "Nimba & Patola & Shunthi", "ratio": "Anti-inflammatory hepatics"},
            {"ingredient": "Guduchi & Katuki & Haritaki", "ratio": "Metabolic detoxifiers"}
        ],
        "standard_dosage": "15 to 20 ml diluted with 40 to 60 ml of boiled warm water twice daily before meals.",
        "modern_pharmacology_correlation": "Boerhavine and punarnavoside block renal tubular epithelial-mesenchymal transition (EMT), stimulate aquaresis without disturbing potassium balance, and downregulate transforming growth factor-beta (TGF-beta1).",
        "safety_and_precautions": "Monitor serum electrolytes in patients already on synthetic loop diuretics."
    },
    {
        "compound_key": "chandraprabha_vati",
        "canonical_title": "चन्द्रप्रभा वटी (Chandraprabha Vati)",
        "transliterated_name": "Chandraprabha Vati",
        "dosage_form": "Vati (Tablet)",
        "therapeutic_category": "Pramehahara, Mutramarga Vishodhana (Urogenital Tonic, Antidiabetic & Lithotriptic)",
        "temperament": "Tridosha Shamaka (Balancing to all three humors)",
        "classical_standard": "Sharangadhara Samhita Madhyamakhanda / AFI Part I (20:12)",
        "primary_indications": [
            "Prameha (Type 2 diabetes mellitus, diabetic nephropathy, glycosuria)",
            "Mutrakricchra wa Ashmari (Dysuria, recurrent UTI, renal calculi)",
            "Ashtila (Benign prostatic hyperplasia / BPH with hesitancy)",
            "Shukradosha & leucorrhea"
        ],
        "key_ingredients": [
            {"ingredient": "Shilajit Shuddha (Purified Asphaltum)", "ratio": "Principal mineral resin"},
            {"ingredient": "Guggulu Shuddha (Commiphora mukul)", "ratio": "Anti-inflammatory lipid regulator"},
            {"ingredient": "Lauha Bhasma (Calcined Iron)", "ratio": "Tissue restorative"},
            {"ingredient": "Chandraprabha herbs (32 botanicals including Triphala, Trikatu, Chavya, Vidanga)", "ratio": "Comprehensive metabolic harmonizer"}
        ],
        "standard_dosage": "500 mg to 1 g (1 to 2 tablets) twice daily with milk, water, or Punarnavadi Kashayam.",
        "modern_pharmacology_correlation": "Fulvic acid in Shilajit enhances glucose uptake via GLUT-4 translocation; guggulsterones reduce prostate stromal inflammation and inhibit crystal nucleation in renal tubuli.",
        "safety_and_precautions": "Well-tolerated for long-term therapy; contraindicated in heavy active uric acid nephropathy without adequate hydration."
    },
    {
        "compound_key": "kanchnar_guggulu",
        "canonical_title": "काञ्चनार गुग्गुलु (Kanchnar Guggulu)",
        "transliterated_name": "Kanchnar Guggulu",
        "dosage_form": "Vati (Tablet)",
        "therapeutic_category": "Granthi-hara, Gandamala-nashaka (Lymphatic Decongestant, Anti-goiter & Anti-neoplastic)",
        "temperament": "Ushna Virya (Kapha-Meda Vilayana)",
        "classical_standard": "Sharangadhara Samhita Madhyamakhanda / AFI Part I (5:1)",
        "primary_indications": [
            "Gandamala wa Apachi (Cervical lymphadenopathy & scrofula)",
            "Galaganda (Goiter, benign thyroid nodules, Hashimoto's disease)",
            "Arbuda wa Granthi (Fibrocystic breast disease, uterine fibroids, PCOS ovarian cysts)",
            "Lipomas & chronic lymphatic stasis"
        ],
        "key_ingredients": [
            {"ingredient": "Kanchnar Twak (Bauhinia variegata stem bark)", "ratio": "Principal anti-adenopathy astringent"},
            {"ingredient": "Shuddha Guggulu (Commiphora mukul)", "ratio": "Equal to all herbal powders combined"},
            {"ingredient": "Triphala & Trikatu & Varuna", "ratio": "Metabolic deobstruent group"},
            {"ingredient": "Ela & Twak & Patra", "ratio": "Aromatic bio-enhancers"}
        ],
        "standard_dosage": "1 to 2 tablets (500mg - 1g) twice or thrice daily with warm water or Varunadi Kashayam.",
        "modern_pharmacology_correlation": "Bauhinia flavonoids and guggulsterone Z/E promote physiological apoptosis in hyperplastic thyroid and fibromatous tissues; normalize TSH levels and facilitate lymphatic macrophage phagocytosis.",
        "safety_and_precautions": "Contraindicated in pregnancy due to uterine stimulating properties of Guggulu."
    },
    {
        "compound_key": "kaishore_guggulu",
        "canonical_title": "कैशोर गुग्गुलु (Kaishore Guggulu)",
        "transliterated_name": "Kaishore Guggulu",
        "dosage_form": "Vati (Tablet)",
        "therapeutic_category": "Vatarakta-hara, Shophahara (Purine Regulator, Anti-gout & Systemic Anti-inflammatory)",
        "temperament": "Mo'tadil (Pitta-Vata balancing with deep tissue penetration)",
        "classical_standard": "Bhaishajya Ratnavali Vataraktadhikara / AFI Part I (5:2)",
        "primary_indications": [
            "Vatarakta (Hyperuricemia, acute & chronic gouty arthritis)",
            "Kushtha wa Vrana (Chronic inflammatory skin disorders, diabetic ulcers)",
            "Sandhivata (Painful joint inflammation with burning sensations)",
            "Systemic inflammatory endotoxemia (Ama)"
        ],
        "key_ingredients": [
            {"ingredient": "Guduchi (Tinospora cordifolia)", "ratio": "Principal anti-inflammatory & urate balancer"},
            {"ingredient": "Triphala (Terminalia chebula, bellerica, Emblica)", "ratio": "Metabolic cleanser"},
            {"ingredient": "Shuddha Guggulu (Commiphora mukul)", "ratio": "Purified resin base"},
            {"ingredient": "Trikatu & Vidanga & Trivrit", "ratio": "Digestive & eliminative catalysts"}
        ],
        "standard_dosage": "1 to 2 tablets (500mg - 1g) twice or thrice daily with lukewarm water or Dashamularishta.",
        "modern_pharmacology_correlation": "Inhibits xanthine oxidase activity to lower elevated serum uric acid; cordifolioside A suppresses synovial prostaglandin E2 (PGE2) without inducing gastric ulceration.",
        "safety_and_precautions": "Avoid during pregnancy; adjust dose in patients with chronic diarrhea."
    },
    {
        "compound_key": "gokshuradi_guggulu",
        "canonical_title": "गोक्षुरादि गुग्गुलु (Gokshuradi Guggulu)",
        "transliterated_name": "Gokshuradi Guggulu",
        "dosage_form": "Vati (Tablet)",
        "therapeutic_category": "Mutrakricchrahara, Ashmari-bhedana (Diuretic, Lithotriptic & Prostatic Decongestant)",
        "temperament": "Mo'tadil (Vata-Pitta-Kapha Tridoshahara)",
        "classical_standard": "Sharangadhara Samhita Madhyamakhanda / AFI Part I (5:3)",
        "primary_indications": [
            "Mutrakricchra (Painful micturition, dysuria, burning urine)",
            "Ashmari (Urolithiasis, renal and vesical calculi)",
            "Prameha (Diabetic albuminuria & chronic kidney congestion)",
            "Vatavyadhi affecting lumbar and pelvic regions"
        ],
        "key_ingredients": [
            {"ingredient": "Gokshura (Tribulus terrestris fruit decoction)", "ratio": "28 parts (Principal diuretic & anti-calculus herb)"},
            {"ingredient": "Shuddha Guggulu (Commiphora mukul)", "ratio": "7 parts (Anti-inflammatory resin)"},
            {"ingredient": "Trikatu & Triphala & Musta", "ratio": "Metabolic and urinary harmonizers"}
        ],
        "standard_dosage": "1 to 2 tablets (500mg - 1g) twice or thrice daily with lukewarm water or Punarnavadi Kashayam.",
        "modern_pharmacology_correlation": "Terrestrial saponins (protodioscin) inhibit calcium oxalate monohydrate crystallization; relaxes urinary tract smooth muscles to facilitate stone expulsion and improves glomerular filtration rate.",
        "safety_and_precautions": "Very safe; ensure liberal fluid intake (>2.5 liters/day) when treating calculi."
    },
    {
        "compound_key": "arjunarishta",
        "canonical_title": "अर्जुनारिष्ट (Arjunarishta / Parthadyarishta)",
        "transliterated_name": "Arjunarishta",
        "dosage_form": "Arishta (Naturally Fermented Cardiotonic Elixir)",
        "therapeutic_category": "Hridya, Balya (Master Cardioprotective, Anti-anginal & Inotropic Restorative)",
        "temperament": "Sheeta Virya / Kashaya-Madhura Rasa (Pitta-Kapha Shamaka)",
        "classical_standard": "Bhaishajya Ratnavali Hridrogadhikara / AFI Part I (1:5)",
        "primary_indications": [
            "Hridroga (Ischemic heart disease, coronary insufficiency, post-MI rehab)",
            "Hrid-Daurbalya (Congestive cardiac asthenia, reduced left ventricular ejection fraction)",
            "Uchha-Raktachapa (Essential hypertension adjunct)",
            "Cardiac palpitations, neurosis & exertional dyspnea"
        ],
        "key_ingredients": [
            {"ingredient": "Arjuna Twak (Terminalia arjuna stem bark decoction)", "ratio": "Principal cardioprotective triterpene base"},
            {"ingredient": "Draksha (Vitis vinifera dry grapes)", "ratio": "Cardiotonic bioflavonoids"},
            {"ingredient": "Madhuka Pushpa (Madhuca indica flowers)", "ratio": "Rejuvenator"},
            {"ingredient": "Dhataki (Woodfordia fruticosa)", "ratio": "Fermentation catalyst"}
        ],
        "standard_dosage": "15 to 25 ml with equal quantity of water twice daily immediately after meals.",
        "modern_pharmacology_correlation": "Arjunolic acid, arjunic acid, and terminaloside exert positive inotropic actions by inhibiting myocardial Na+/K+-ATPase; enhances coronary microcirculation and prevents ischemic reperfusion apoptosis.",
        "safety_and_precautions": "Highly safe; synergistic with modern beta-blockers and antiplatelets."
    },
    {
        "compound_key": "vasavaleha",
        "canonical_title": "वासावलेह (Vasavaleha)",
        "transliterated_name": "Vasavaleha",
        "dosage_form": "Avaleha (Medicated Herbal Confection)",
        "therapeutic_category": "Kasa-Shwasahara, Raktapittahara (Bronchodilator, Expectorant & Hemostatic)",
        "temperament": "Sheeta Virya / Tikta-Kashaya Rasa (Pitta-Kapha Shamaka)",
        "classical_standard": "Bhaishajya Ratnavali Kasadhikara / AFI Part I (3:23)",
        "primary_indications": [
            "Raktapitta (Hemoptysis, pulmonary bleeding, epistaxis)",
            "Kasa wa Shwasa (Bronchial asthma, acute & chronic bronchitis, COPD)",
            "Parshwashula (Pleuritic chest pain accompanying respiratory infections)"
        ],
        "key_ingredients": [
            {"ingredient": "Vasa Svarasa (Adhatoda vasica fresh leaf juice)", "ratio": "Principal bronchodilator & quinazoline source"},
            {"ingredient": "Pippali Churna (Piper longum)", "ratio": "Bioavailability enhancer"},
            {"ingredient": "Go-Ghrita (Cow ghee)", "ratio": "Lipophilic respiratory protector"},
            {"ingredient": "Sharkara & Madhu (Sugar & Honey)", "ratio": "Demulcent vehicle"}
        ],
        "standard_dosage": "5 to 10 grams twice daily, swallowed slowly, with lukewarm water or milk.",
        "modern_pharmacology_correlation": "Vasicine and vasicinone act as natural precursor molecules to bromhexine/ambroxol; induces potent bronchodilation, decreases mucus viscosity, and inhibits platelet-activating factor (PAF).",
        "safety_and_precautions": "Contraindicated in pregnancy due to mild abortifacient/oxytocic activity of vasicine."
    }
]

def main():
    print("Expanding Master Qarabadeen & Ayurvedic Library...")
    
    # 1. Load existing master library
    with open(MASTER_LIB_PATH, "r", encoding="utf-8") as f:
        master_data = json.load(f)
    
    existing_keys = {item["compound_key"] for item in master_data.get("formulations", [])}
    added_count = 0
    for form in NEW_FORMULATIONS:
        if form["compound_key"] not in existing_keys:
            master_data["formulations"].append(form)
            existing_keys.add(form["compound_key"])
            added_count += 1
            
    master_data["total_compounds"] = len(master_data["formulations"])
    
    with open(MASTER_LIB_PATH, "w", encoding="utf-8") as f:
        json.dump(master_data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Added {added_count} formulations to {MASTER_LIB_PATH} (Total: {master_data['total_compounds']})")

    # 2. Update catalog_seed.json
    with open(CATALOG_SEED_PATH, "r", encoding="utf-8") as f:
        seed_data = json.load(f)
        
    seed_recon = seed_data.get("qarabadeen_reconciliations", [])
    seed_keys = {item.get("compound_key") for item in seed_recon if "compound_key" in item}
    seed_added = 0
    for form in NEW_FORMULATIONS:
        if form["compound_key"] not in seed_keys:
            # Map formulation to reconciliation object
            recon_obj = {
                "compound_key": form["compound_key"],
                "canonical_title": form["canonical_title"],
                "transliterated_name": form["transliterated_name"],
                "dosage_form": form["dosage_form"],
                "therapeutic_category": form["therapeutic_category"],
                "temperament": form["temperament"],
                "classical_standard": form["classical_standard"],
                "primary_indications": form["primary_indications"],
                "key_ingredients": [ing["ingredient"] for ing in form.get("key_ingredients", [])],
                "standard_dosage": form["standard_dosage"],
                "modern_pharmacology_correlation": form["modern_pharmacology_correlation"],
                "safety_and_precautions": form["safety_and_precautions"]
            }
            seed_recon.append(recon_obj)
            seed_keys.add(form["compound_key"])
            seed_added += 1

    seed_data["qarabadeen_reconciliations"] = seed_recon
    with open(CATALOG_SEED_PATH, "w", encoding="utf-8") as f:
        json.dump(seed_data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Added {seed_added} formulations to {CATALOG_SEED_PATH} (Total: {len(seed_recon)})")

if __name__ == "__main__":
    main()
