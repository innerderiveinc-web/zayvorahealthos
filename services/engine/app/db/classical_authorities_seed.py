"""
ZMIE / ZAYVORA Classical Knowledge Base & Authoritative Hierarchy (Levels 1 to 6)
Codifies authentic classical authorities, formularies, pharmacopoeias, and modern evidence:

UNANI TIBB HIERARCHY:
- LEVEL 1: Original Classical Sources (Ibn Sina, Al-Razi, Al-Majusi, Al-Jurjani, Nafis al-Kirmani)
- LEVEL 2: Classical Unani Materia Medica (Makhzan al-Adwiya, Ikhtiyarat-i Badi'i, Mufradat works)
- LEVEL 3: Classical Formularies / Qarabadeen (Qarabadeen-e-Azam, Qarabadeen-e-Qadri, Qarabadeen-e-Jadid, etc.)
- LEVEL 4: Official Indian Unani Standards (UPI, NFUM, CCRUM, Ministry of AYUSH)
- LEVEL 5: Modern Scientific Evidence (Pharmacology, Toxicology, Human RCTs, Systematic Reviews)
- LEVEL 6: Contemporary Textbooks & Clinical Compendia (Saidla, Moalijat, Ilmul Advia)

AYURVEDA HIERARCHY:
- Brihat Trayi & Early Medical Tradition: Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya, Ashtanga Sangraha, Bhela, Kashyapa
- Laghu Trayi & Nidana: Madhava Nidana, Sharngadhara Samhita, Bhavaprakasha
- Dravyaguna Nighantus: Bhavaprakasha Nighantu, Dhanvantari Nighantu, Raja Nighantu, Kaiyadeva Nighantu
- Bhaishajya Kalpana: Sharngadhara Samhita, Bhaishajya Ratnavali, Chakradatta, Yoga Ratnakara, Rasaratna Samuccaya
- Rasashastra: Rasaratna Samuccaya, Rasa Tarangini, Rasendra Sara Sangraha, AFI
- Official Regulatory Standards: Ayurvedic Pharmacopoeia of India (API), Ayurvedic Formulary of India (AFI), CCRAS, Ministry of AYUSH
"""

from typing import List, Dict, Any, Optional
from enum import Enum


class AuthorityLevel(str, Enum):
    LEVEL_1 = "Level 1: Original Classical Sources"
    LEVEL_2 = "Level 2: Classical Materia Medica / Mufradat"
    LEVEL_3 = "Level 3: Classical Formularies / Qarabadeen"
    LEVEL_4 = "Level 4: Official Regulatory & Pharmacopoeial Standards"
    LEVEL_5 = "Level 5: Modern Scientific Evidence & Clinical Trials"
    LEVEL_6 = "Level 6: Contemporary Institutional Textbooks & Reviews"


# -----------------------------------------------------------------------------
# 1. UNANI CLASSICAL AUTHORITIES REGISTRY
# -----------------------------------------------------------------------------

UNANI_CLASSICAL_AUTHORITIES: List[Dict[str, Any]] = [
    # LEVEL 1 — Original Classical Sources
    {
        "id": "canon_ibn_sina",
        "title": "Al-Qanun fi al-Tibb (The Canon of Medicine / القانون في الطب)",
        "author": "Abu Ali al-Husayn ibn Sina (Avicenna)",
        "era": "1025 CE (5th Century AH)",
        "language": "Arabic (Classical)",
        "level": AuthorityLevel.LEVEL_1.value,
        "category": "Core Classical Foundation",
        "importance": "Foundational medical theory, Mizaj (temperament 1°-4°), Akhlat (humors), Afaal (functions), etiology, simples (Book 2), and compounds (Book 5).",
        "key_volumes": [
            "Book 1 (Kulliyat): General principles, anatomy, physiology, etiology, hygiene",
            "Book 2 (Mufradat): Materia medica (approx 800 simple drugs)",
            "Book 3 (Amraz-e-Juz'iyya): Head-to-toe organ pathology and therapeutics",
            "Book 4 (Amraz-e-Aamiyya): Systemic diseases, fevers, crisis, toxicology, surgery",
            "Book 5 (Qarabadeen): Compound formularies and compound medications"
        ],
        "epistemic_priority": 100
    },
    {
        "id": "al_hawi_razi",
        "title": "Kitab al-Hawi fi al-Tibb (The Comprehensive Book on Medicine / كتاب الحاوي في الطب)",
        "author": "Abu Bakr Muhammad ibn Zakariyya al-Razi (Rhazes)",
        "era": "9th–10th Century CE (250–313 AH)",
        "language": "Arabic (Classical)",
        "level": AuthorityLevel.LEVEL_1.value,
        "category": "Clinical Case Records & Critical Reasoning",
        "importance": "Monolithic clinical compilation in 23+ volumes; essential for empirical disease observation, differential diagnosis, and therapeutic clinical reasoning.",
        "key_volumes": [
            "Clinical case records with patient-by-patient daily observations",
            "Critical cross-examination of Greek, Indian, and early Islamic clinical opinions",
            "Extensive therapeutics, pharmacotherapy, and toxicology"
        ],
        "epistemic_priority": 98
    },
    {
        "id": "kamil_al_sanaa_majusi",
        "title": "Kamil al-Sana'a al-Tibbiyya (The Complete Medical Art / Al-Kitab al-Maliki / كامل الصناعة الطبية)",
        "author": "Ali ibn al-Abbas al-Majusi (Haly Abbas)",
        "era": "10th Century CE (384 AH)",
        "language": "Arabic (Classical)",
        "level": AuthorityLevel.LEVEL_1.value,
        "category": "Systematic Pre-Avicennian Textbook",
        "importance": "Major early comprehensive medical text divided systematically into Theoretical Medicine (Juz Nazari) and Practical Medicine (Juz Amali).",
        "key_volumes": [
            "Part 1 (Theoretical): Anatomy, physiology, pulse, urine, disease classification",
            "Part 2 (Practical): Hygiene, dietetics, internal therapeutics, surgery, and pharmacology"
        ],
        "epistemic_priority": 95
    },
    {
        "id": "zakhira_khwarazm_jurjani",
        "title": "Zakhira-i Khwarazm Shahi (Treasure of Khwarazm Shah / ذخیره خوارزمشاهی)",
        "author": "Sayyid Ismail Jurjani (Zayn al-Din Jurjani)",
        "era": "1110 CE (6th Century AH)",
        "language": "Persian (Classical Farsi)",
        "level": AuthorityLevel.LEVEL_1.value,
        "category": "Persian Medical Encyclopedia",
        "importance": "The most monumental Persian Unani medical encyclopedia; 10 expansive discourses (Kitabs) covering theory, diagnosis, pulse, diet, disease management, and pharmacy.",
        "key_volumes": [
            "Discourse 1-4: General principles, hygiene, disease signs, pulse/uroscopy",
            "Discourse 5-6: Fevers, localized organ diseases head to foot",
            "Discourse 7-9: Surgery, wounds, poisons, cosmetics",
            "Discourse 10 (Qarabadeen): Classical Persian compound pharmacology and preparations"
        ],
        "epistemic_priority": 93
    },
    {
        "id": "sharh_al_asbab_kirmani",
        "title": "Sharh al-Asbab wa'l-Alamat (Commentary on Causes and Signs / شرح الأسباب والعلامات)",
        "author": "Burhan al-Din Nafis ibn Awad al-Kirmani (Allama Nafis)",
        "era": "1424 CE (827 AH)",
        "language": "Arabic (Classical)",
        "level": AuthorityLevel.LEVEL_1.value,
        "category": "Advanced Pathology & Symptomatology",
        "importance": "Masterwork on etiology (Asbab), semiology (Alamat), and symptomatic clinical pathology; definitive textbook for Mahiyat-ul-Amraz.",
        "key_volumes": [
            "In-depth analysis of Najib al-Din Samarqandi's Asbab wa Alamat",
            "Humoral pathophysiology of organ derangements and morbid matter disposition"
        ],
        "epistemic_priority": 91
    },

    # LEVEL 2 — Classical Unani Materia Medica / Mufradat
    {
        "id": "makhzan_al_adwiya",
        "title": "Makhzan al-Adwiya / Makhzan-ul-Advia (Storehouse of Medicaments / مخزن الادویہ)",
        "author": "Mir Muhammad Husain Khan Aqili Alavi Khorasani Shirazi",
        "era": "1777 CE (1191 AH)",
        "language": "Persian / Urdu Translations",
        "level": AuthorityLevel.LEVEL_2.value,
        "category": "Comprehensive Materia Medica",
        "importance": "Extremely authoritative late classical Materia Medica codex. Contains exhaustive monographs specifying names in 10+ languages, botanical identity, Mizaj, Afaal, Musleh, Badal, and dosage.",
        "key_volumes": [
            "Monographs organized alphabetically (Alif to Ye)",
            "Systematic notation of temperamental degrees, therapeutic actions, correctives, substitutes, and toxicities"
        ],
        "epistemic_priority": 88
    },
    {
        "id": "ikhtiyarat_i_badii",
        "title": "Ikhtiyarat-i Badi'i (Selections for Princess Badi' al-Jamal / اختیارات بدیعی)",
        "author": "Ziauddin Ali ibn Husayn Ansari al-Shirazi (Haji Zayn al-Attar)",
        "era": "1369 CE (770 AH)",
        "language": "Persian (Classical)",
        "level": AuthorityLevel.LEVEL_2.value,
        "category": "Classical Materia Medica & Pharmacy",
        "importance": "Landmark Persian Materia Medica divided into two parts: Simple Drugs (Mufradat) and Compound Formulations (Murakkabat).",
        "key_volumes": [
            "Part 1: Simple medicaments with origins, physical descriptions, and therapeutic actions",
            "Part 2: Specialized compound pharmaceutical electuaries, syrups, and ointments"
        ],
        "epistemic_priority": 85
    },

    # LEVEL 3 — Classical Formularies / Qarabadeen
    {
        "id": "qarabadeen_e_azam",
        "title": "Qarabadeen-e-Azam (قرابادین اعظم)",
        "author": "Hakim Muhammad Azam Khan (Nazim-i Jahan)",
        "era": "19th Century CE (1269 AH)",
        "language": "Persian / Urdu",
        "level": AuthorityLevel.LEVEL_3.value,
        "category": "Classical Formulary Codex",
        "importance": "The most extensive pharmacopoeia of compound formulations in later Unani medicine; encyclopedic Nuskha repository with exact weights and methods.",
        "key_volumes": [
            "Khamiras, Majuns, Itrifalat, Sharbat, Jawarishat, Habb, and Tila formulations"
        ],
        "epistemic_priority": 80
    },
    {
        "id": "qarabadeen_e_qadri",
        "title": "Qarabadeen-e-Qadri (قرابادین قادری)",
        "author": "Hakim Muhammad Akbar Arzani",
        "era": "1718 CE (1130 AH)",
        "language": "Persian / Urdu",
        "level": AuthorityLevel.LEVEL_3.value,
        "category": "Classical Formulary Codex",
        "importance": "Standard practical formulary detailing clinical preparations, precise compounding steps, and therapeutic doses.",
        "key_volumes": [
            "Compound formulations arranged by pharmaceutical dosage forms"
        ],
        "epistemic_priority": 78
    },
    {
        "id": "qarabadeen_e_jadid",
        "title": "Qarabadeen-e-Jadid (قرابادین جدید)",
        "author": "Hakim Muhammad Kabiruddin",
        "era": "20th Century CE",
        "language": "Urdu",
        "level": AuthorityLevel.LEVEL_3.value,
        "category": "Modern-Standardized Classical Formulary",
        "importance": "Standardized modern compilation of classical formulations with metrology conversions into metric weights and clear indications.",
        "key_volumes": [
            "Standardized recipes for modern dispensary and institutional practice"
        ],
        "epistemic_priority": 76
    },
    {
        "id": "qarabadeen_e_najm_ul_ghani",
        "title": "Qarabadeen-e-Najm-ul-Ghani (Khaza'in al-Adwiya / قرابادین نجم الغنی)",
        "author": "Hakim Najm al-Ghani Rampuri",
        "era": "Early 20th Century CE",
        "language": "Urdu",
        "level": AuthorityLevel.LEVEL_3.value,
        "category": "Comprehensive Formulary & Materia Medica",
        "importance": "Renowned for bridging classical Mughal-era formulations with early modern pharmacognosy and regional botanical identities.",
        "key_volumes": [
            "Comprehensive compound formulas, dosage modifications, and clinical commentary"
        ],
        "epistemic_priority": 75
    },
    {
        "id": "qarabadeen_e_shifai",
        "title": "Qarabadeen-e-Shifa'i (Tibb-e-Shifa'i / قرابادین شفائی)",
        "author": "Muzaffar ibn Muhammad al-Husayni Shifa'i",
        "era": "16th Century CE",
        "language": "Persian",
        "level": AuthorityLevel.LEVEL_3.value,
        "category": "Safavid-Era Pharmacopoeia",
        "importance": "Classic Safavid medical formulary heavily referenced across South Asian and Middle Eastern Unani compounding.",
        "key_volumes": [
            "Electuaries, distilled waters (Arqiyat), and specialized powders (Sufuf)"
        ],
        "epistemic_priority": 73
    },
    {
        "id": "qarabadeen_e_azam_wa_akmal",
        "title": "Qarabadeen-e-Azam wa Akmal / Regional Qarabadeen Compendia",
        "author": "Hakim Muhammad Akmal Khan / Regional Compilers",
        "era": "18th–19th Century CE",
        "language": "Persian / Urdu",
        "level": AuthorityLevel.LEVEL_3.value,
        "category": "Regional Formulary Editions",
        "importance": "Crucial for identifying regional variations in drug nomenclature, traditional weights (Masha, Ratti, Misqal), and local excipient substitutions.",
        "key_volumes": [
            "Regional South Asian variants and traditional compounding traditions"
        ],
        "epistemic_priority": 70
    },

    # LEVEL 4 — Official Indian Unani Standards
    {
        "id": "upi_official",
        "title": "Unani Pharmacopoeia of India (UPI) — Parts I & II",
        "author": "Unani Pharmacopoeia Committee, Ministry of AYUSH, Government of India",
        "era": "Modern Statutory Publication (Ongoing)",
        "language": "English / Urdu",
        "level": AuthorityLevel.LEVEL_4.value,
        "category": "Statutory Pharmacopoeial Standard",
        "importance": "Official legal and pharmacopoeial authority under the Drugs & Cosmetics Act, 1940. Defines identity, purity, TLC/HPTLC profiles, foreign matter, ash limits, and assay standards.",
        "key_volumes": [
            "Part I: Single Drugs (Mufradat) — Volumes I to VI",
            "Part II: Compound Formulations (Murakkabat) — Volumes I to IV"
        ],
        "epistemic_priority": 85
    },
    {
        "id": "nfum_official",
        "title": "National Formulary of Unani Medicine (NFUM) — Parts I to VI",
        "author": "Ministry of AYUSH / Central Council for Research in Unani Medicine (CCRUM)",
        "era": "Modern Statutory Publication",
        "language": "English / Urdu",
        "level": AuthorityLevel.LEVEL_4.value,
        "category": "National Statutory Formulary",
        "importance": "Definitive national repository of approved compound formulations (Nuskha), legal batch compositions, method of manufacture, and shelf-life parameters.",
        "key_volumes": [
            "Standardized proportions, excipients, and quality parameters for hundreds of classic compounds"
        ],
        "epistemic_priority": 83
    },
    {
        "id": "ccrum_publications",
        "title": "Central Council for Research in Unani Medicine (CCRUM) Research Monographs",
        "author": "CCRUM, Ministry of AYUSH",
        "era": "Modern Research Council (1978–Present)",
        "language": "English",
        "level": AuthorityLevel.LEVEL_4.value,
        "category": "Official Research Council Monographs",
        "importance": "Clinical trial validation, standardization of single/compound drugs, ethnobotanical surveys, and safety validation of classical formulations.",
        "key_volumes": [
            "Standardization of Single Drugs of Unani Medicine",
            "Clinical Studies in Vitiligo (Bars), Rheumatoid Arthritis (Waja-ul-Mafasil), and Diabetes (Ziabetes)"
        ],
        "epistemic_priority": 82
    }
]


# -----------------------------------------------------------------------------
# 2. AYURVEDIC CLASSICAL AUTHORITIES REGISTRY
# -----------------------------------------------------------------------------

AYURVEDA_CLASSICAL_AUTHORITIES: List[Dict[str, Any]] = [
    # Brihat Trayi & Early Traditions
    {
        "id": "charaka_samhita",
        "title": "Charaka Samhita (चरक संहिता)",
        "author": "Agnivesha / Acharya Charaka / Dridhabala",
        "era": "Classical Era (approx. 2nd Century BCE - 2nd Century CE)",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_1.value,
        "category": "Brihat Trayi — Internal Medicine",
        "importance": "Supreme authority on Kaya Chikitsa (Internal Medicine), Tridosha theory, Dhatu physiology, etiology (Nidana), and extensive therapeutics across 8 Sthanas.",
        "key_volumes": [
            "Sutrasthana (Philosophical foundations, diet, 50 Mahakashayas)",
            "Nidanasthana (Etiology of 8 major disorders)",
            "Vimanasthana (Dosage, clinical examination, epistemology / Pramana)",
            "Sharirasthana (Anatomy, embryology, mind-body connection)",
            "Indriyasthana (Prognosis and fatal signs / Arishta Lakshana)",
            "Chikitsasthana (Therapeutics of clinical conditions)",
            "Kalpasthana (Formulations and pharmacy for Panchakarma)",
            "Siddhisthana (Management of therapeutic complications)"
        ],
        "epistemic_priority": 100
    },
    {
        "id": "sushruta_samhita",
        "title": "Sushruta Samhita (सुश्रुत संहिता)",
        "author": "Acharya Sushruta / Nagarjuna",
        "era": "Classical Era (approx. 6th Century BCE - 4th Century CE)",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_1.value,
        "category": "Brihat Trayi — Surgery & Surgical Topography",
        "importance": "Supreme authority on Shalya Tantra (Surgery), surgical instruments (Yantra/Shastra), dissection, Marmas (vital anatomical points), and reconstructive rhinoplasty.",
        "key_volumes": [
            "Sutrasthana (Surgical training, instruments, caustic alkalis / Kshara, Agnikarma)",
            "Nidanasthana (Surgical pathology, fractures, calculi, fistulae)",
            "Sharirasthana (Anatomy, dissection methodology, 107 Marma points)",
            "Chikitsasthana (Operative procedures, wound care / Vrana Chikitsa)",
            "Kalpasthana (Toxicology / Agada Tantra and venomous bites)",
            "Uttaratantra (Ophthalmology / Shalakya, pediatrics, internal medicine)"
        ],
        "epistemic_priority": 98
    },
    {
        "id": "ashtanga_hridaya",
        "title": "Ashtanga Hridaya (अष्टाङ्ग हृदय)",
        "author": "Acharya Vagbhata",
        "era": "approx. 6th–7th Century CE",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_1.value,
        "category": "Brihat Trayi — Poetic Clinical Synthesis",
        "importance": "The most widely practiced and memorized synthesis combining the insights of Charaka and Sushruta into elegant, crystal-clear verse.",
        "key_volumes": [
            "Sutrasthana, Sharirasthana, Nidanasthana, Chikitsasthana, Kalpa-Siddhi, and Uttarasthana"
        ],
        "epistemic_priority": 96
    },
    {
        "id": "ashtanga_sangraha",
        "title": "Ashtanga Sangraha (अष्टाङ्ग संग्रह)",
        "author": "Vriddha Vagbhata",
        "era": "approx. 6th Century CE",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_1.value,
        "category": "Brihat Trayi — Comprehensive Compendium",
        "importance": "Comprehensive prose-and-verse compendium detailing all eight branches (Ashtanga) of Ayurveda with rich historical and therapeutic nuances.",
        "key_volumes": [
            "Detailed exposition across all 6 Sthanas with prose commentaries"
        ],
        "epistemic_priority": 94
    },
    {
        "id": "bhela_samhita",
        "title": "Bhela Samhita (भेल संहिता)",
        "author": "Acharya Bhela (Disciple of Punarvasu Atreya)",
        "era": "Early Classical Era",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_1.value,
        "category": "Early Atreya Tradition",
        "importance": "Rare and foundational contemporary of the original Agnivesha Tantra; critical for independent validation of Atreya teachings.",
        "key_volumes": [
            "Early therapeutic concepts and distinct perspectives on Alochaka Pitta"
        ],
        "epistemic_priority": 90
    },
    {
        "id": "kashyapa_samhita",
        "title": "Kashyapa Samhita (Vriddha Jivakiya Tantra / काश्यप संहिता)",
        "author": "Acharya Kashyapa / Vriddha Jivaka",
        "era": "Classical Era",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_1.value,
        "category": "Kaumarbhritya & Stri Roga",
        "importance": "The preeminent classical authority on pediatrics (Kaumarbhritya), neonatology, obstetrics (Prasuti Tantra), and gynecological disorders.",
        "key_volumes": [
            "Phakka Roga (pediatric malnutrition), dentition disorders, Lehana (pediatric electuaries)"
        ],
        "epistemic_priority": 92
    },

    # Laghu Trayi & Diagnostics
    {
        "id": "madhava_nidana",
        "title": "Madhava Nidana (Rogavinishchaya / माधव निदान)",
        "author": "Acharya Madhavakara",
        "era": "8th Century CE",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_1.value,
        "category": "Laghu Trayi — Clinical Diagnostics",
        "importance": "Definitive classical authority on disease diagnosis, clinical stages (Shat Kriya Kala), five diagnostic tools (Pancha Nidana), and differential diagnosis.",
        "key_volumes": [
            "Nidana, Purvarupa, Rupa, Upashaya, and Samprapti for over 70 disease entities"
        ],
        "epistemic_priority": 93
    },
    {
        "id": "sharngadhara_samhita",
        "title": "Sharngadhara Samhita (शारङ्गधर संहिता)",
        "author": "Acharya Sharngadhara",
        "era": "14th Century CE",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_3.value,
        "category": "Laghu Trayi — Formulations & Pharmacy",
        "importance": "Cornerstone text of Ayurvedic pharmaceutics (Bhaishajya Kalpana). Introduced detailed pulse examination (Nadi Pariksha) and refined pharmaceutical processing.",
        "key_volumes": [
            "Prathama Khanda (Pharmacology, metrology, Nadi examination)",
            "Madhyama Khanda (Kashaya, Svarasa, Hima, Phanta, Asava-Arishta, Bhasma preparation)",
            "Uttara Khanda (Panchakarma procedures and ocular/nasal preparations)"
        ],
        "epistemic_priority": 91
    },

    # Dravyaguna Nighantus
    {
        "id": "bhavaprakasha_nighantu",
        "title": "Bhavaprakasha Nighantu (भावप्रकाश निघण्टु)",
        "author": "Acharya Bhavamishra",
        "era": "16th Century CE",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_2.value,
        "category": "Laghu Trayi & Master Dravyaguna Nighantu",
        "importance": "The supreme, most widely cited Materia Medica (Dravyaguna) encyclopedia in Ayurveda. Details plant taxonomy, synonyms, Rasapanchaka, and first documented Phiranga Roga (Syphilis).",
        "key_volumes": [
            "Haritakyadi Varga, Karpuradi Varga, Guduchyadi Varga, Vatadi Varga, Dhatvadi Varga"
        ],
        "epistemic_priority": 95
    },
    {
        "id": "dhanvantari_nighantu",
        "title": "Dhanvantari Nighantu (धन्वन्तरि निघण्टु)",
        "author": "Dhanvantari Tradition (Early medieval)",
        "era": "approx. 10th–11th Century CE",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_2.value,
        "category": "Early Classical Dravyaguna Nighantu",
        "importance": "One of the oldest and most authentic Nighantu codices; 7 Vargas classifying medicinal substances, properties, and classical synonyms.",
        "key_volumes": [
            "Guduchyadi, Shatapushpadi, Chandanadi, Karaviradi, Amradi, Suvarnadi, and Mishrakadi Vargas"
        ],
        "epistemic_priority": 88
    },
    {
        "id": "raja_nighantu",
        "title": "Raja Nighantu (Abhidhana Chudamani / राज निघण्टु)",
        "author": "Pandit Narahari",
        "era": "14th Century CE",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_2.value,
        "category": "Lexicographical Dravyaguna Codex",
        "importance": "Renowned for exhaustive botanical synonyms (Namakarna based on habit, habitat, morphological markers) and precise medicinal actions.",
        "key_volumes": [
            "24 comprehensive Vargas with deep botanical categorization and regional terminology"
        ],
        "epistemic_priority": 86
    },
    {
        "id": "kaiyadeva_nighantu",
        "title": "Kaiyadeva Nighantu (Pathyapathya Vibodhaka / कैयदेव निघण्टु)",
        "author": "Acharya Kaiyadeva",
        "era": "15th Century CE",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_2.value,
        "category": "Dietetics & Dravyaguna Codex",
        "importance": "Exquisite emphasis on dietary substances, wholesome vs unwholesome foods (Pathya-Apathya), and detailed actions of medicinal plants.",
        "key_volumes": [
            "Aushadha Varga, Dhatu Varga, Dhanya Varga, Pakvanna Varga, and Vihara Varga"
        ],
        "epistemic_priority": 85
    },

    # Bhaishajya Kalpana (Formulations)
    {
        "id": "bhaishajya_ratnavali",
        "title": "Bhaishajya Ratnavali (भैषज्य रत्नावली)",
        "author": "Kaviraj Govinda Das Sen",
        "era": "18th–19th Century CE",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_3.value,
        "category": "Comprehensive Ayurvedic Pharmacopoeia",
        "importance": "The most widely consulted practical formulation compendium in modern Ayurvedic clinical practice; contains hundreds of definitive compound prescriptions.",
        "key_volumes": [
            "Chapters dedicated to specific disease therapeutics (Jwara, Grahani, Prameha, Amavata)"
        ],
        "epistemic_priority": 92
    },
    {
        "id": "chakradatta",
        "title": "Chakradatta (Chikitsa Sangraha / चक्रदत्त)",
        "author": "Acharya Chakrapani Datta (Commentator on Charaka & Sushruta)",
        "era": "11th Century CE",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_3.value,
        "category": "Therapeutic & Formulary Manual",
        "importance": "Pioneered systematic integration of metallo-mineral formulations (Rasa preparations) into general clinical therapeutics.",
        "key_volumes": [
            "Practical formulations arranged disease by disease with commentary"
        ],
        "epistemic_priority": 90
    },
    {
        "id": "yoga_ratnakara",
        "title": "Yoga Ratnakara (योग रत्नाकर)",
        "author": "Mayurasuri (Anonymous author tradition)",
        "era": "17th Century CE",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_3.value,
        "category": "Clinical Compendium & Eightfold Diagnosis",
        "importance": "First classical text to formally codify the Ashta Sthana Pariksha (Eightfold clinical examination: Nadi, Mutra, Mala, Jihva, Shabda, Sparsha, Druk, Akruti).",
        "key_volumes": [
            "Diagnostic procedures and comprehensive drug compounding recipes"
        ],
        "epistemic_priority": 89
    },

    # Rasashastra (Metallo-mineral & Iatrochemistry)
    {
        "id": "rasaratna_samuccaya",
        "title": "Rasaratna Samuccaya (रसरत्न समुच्चय)",
        "author": "Acharya Vagbhata (Son of Simhagupta / Rasa-Vagbhata)",
        "era": "13th Century CE",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_3.value,
        "category": "Supreme Rasashastra Codex",
        "importance": "The quintessential masterwork on Ayurvedic alchemy and metallo-mineral pharmaceutics: laboratory construction (Rasashala), apparatuses (Yantras), crucible purification (Shodhana), and incineration (Marana).",
        "key_volumes": [
            "Purification and Bhasma incineration of Parada (Mercury), Maharasa, Uparasa, and metals"
        ],
        "epistemic_priority": 94
    },
    {
        "id": "rasa_tarangini",
        "title": "Rasa Tarangini (रस तरङ्गिणी)",
        "author": "Sadananda Sharma",
        "era": "Late 19th / Early 20th Century CE",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_3.value,
        "category": "Modern-Standardized Rasashastra Manual",
        "importance": "Modern classic for standardizing Rasashastra processes, metric temperatures, and toxicological safety handling for mineral compounds.",
        "key_volumes": [
            "24 Tarangas detailing exact incineration criteria and quality testing (Varitaratva, Rekhapurnatva)"
        ],
        "epistemic_priority": 88
    },
    {
        "id": "rasendra_sara_sangraha",
        "title": "Rasendra Sara Sangraha (रसेन्द्र सार संग्रह)",
        "author": "Acharya Gopalakrishna Bhatta",
        "era": "16th Century CE",
        "language": "Sanskrit",
        "level": AuthorityLevel.LEVEL_3.value,
        "category": "Applied Rasashastra Therapeutics",
        "importance": "Practical bedside manual for clinical administration and therapeutic combinations of Rasa preparations.",
        "key_volumes": [
            "Formulations categorized by therapeutic indication and dosage safeguards"
        ],
        "epistemic_priority": 85
    },

    # Official Indian Ayurvedic References (Regulatory & Standards)
    {
        "id": "api_official",
        "title": "Ayurvedic Pharmacopoeia of India (API) — Parts I & II",
        "author": "Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H), Ministry of AYUSH",
        "era": "Modern Statutory Publication (Ongoing)",
        "language": "English",
        "level": AuthorityLevel.LEVEL_4.value,
        "category": "Statutory Pharmacopoeial Standard",
        "importance": "Official legal standards under the Drugs and Cosmetics Act, 1940. Prescribes macroscopic, microscopic, chemical assay, TLC/HPTLC fingerprinting, heavy metal limits, and microbial limits.",
        "key_volumes": [
            "Part I: Single Drugs (Dravyas) — Volumes I to X (600+ monographs)",
            "Part II: Formulations (Yogas) — Volumes I to IV"
        ],
        "epistemic_priority": 88
    },
    {
        "id": "afi_official",
        "title": "Ayurvedic Formulary of India (AFI) — Parts I, II & III",
        "author": "Ministry of AYUSH, Government of India",
        "era": "Modern Statutory Formulary",
        "language": "English",
        "level": AuthorityLevel.LEVEL_4.value,
        "category": "National Statutory Formulary",
        "importance": "Definitive statutory formulation book of India. Standardizes classical recipes from Charaka, Sushruta, Sharngadhara, and Bhaishajya Ratnavali for legal industrial manufacture.",
        "key_volumes": [
            "Asava, Arishta, Avaleha, Bhasma, Ghrita, Taila, Churna, and Vati compound standards"
        ],
        "epistemic_priority": 86
    },
    {
        "id": "ccras_publications",
        "title": "Central Council for Research in Ayurvedic Sciences (CCRAS) Monographs",
        "author": "CCRAS, Ministry of AYUSH",
        "era": "Modern Statutory Research Council",
        "language": "English",
        "level": AuthorityLevel.LEVEL_4.value,
        "category": "Official Research Council Monographs",
        "importance": "Preclinical pharmacology, toxicity profiles, clinical validation trials (AYUSH 64, AYUSH 82), and pharmacognostic monographs.",
        "key_volumes": [
            "Evidence-based clinical efficacy reports, safety dossiers, and pharmacovigilance reports"
        ],
        "epistemic_priority": 84
    }
]


# -----------------------------------------------------------------------------
# 3. BULK LOADER & SEARCH ENGINE FOR CLASSICAL AUTHORITIES
# -----------------------------------------------------------------------------

class ClassicalAuthoritiesBulkLoader:
    """
    Manages and exposes the complete authoritative hierarchy of classical texts,
    Qarabadeens, Nighantus, and official pharmacopoeias.
    """

    @classmethod
    def get_all_authorities(cls) -> Dict[str, Any]:
        return {
            "unani": UNANI_CLASSICAL_AUTHORITIES,
            "ayurveda": AYURVEDA_CLASSICAL_AUTHORITIES,
            "hierarchy_doctrine": {
                "level_1": "Original Classical Sources (Ibn Sina, Al-Razi, Majusi, Jurjani, Nafis; Charaka, Sushruta, Vagbhata)",
                "level_2": "Classical Materia Medica (Makhzan al-Adwiya, Ikhtiyarat-i Badi'i; Bhavaprakasha, Dhanvantari, Raja Nighantus)",
                "level_3": "Classical Formularies (Qarabadeen-e-Azam, Qadri, Jadid; Bhaishajya Ratnavali, Sharngadhara, Rasaratna Samuccaya)",
                "level_4": "Official Indian Standards (UPI, NFUM, CCRUM; API, AFI, CCRAS, AYUSH)",
                "level_5": "Modern Scientific Evidence (Molecular Pharmacology, Toxicology, Human RCTs, Systematic Reviews)",
                "level_6": "Contemporary Institutional Textbooks (Used for commentary; NEVER overrides Levels 1–5)"
            }
        }

    @classmethod
    def get_unani_authorities(cls) -> List[Dict[str, Any]]:
        return UNANI_CLASSICAL_AUTHORITIES

    @classmethod
    def get_ayurveda_authorities(cls) -> List[Dict[str, Any]]:
        return AYURVEDA_CLASSICAL_AUTHORITIES

    @classmethod
    def get_qarabadeen_registry(cls) -> List[Dict[str, Any]]:
        """Returns exclusively Level 3 formulation & Qarabadeen literature."""
        return [
            auth for auth in UNANI_CLASSICAL_AUTHORITIES
            if "Qarabadeen" in auth["title"] or auth["level"] == AuthorityLevel.LEVEL_3.value
        ]

    @classmethod
    def get_official_standards_registry(cls) -> Dict[str, List[Dict[str, Any]]]:
        """Returns Level 4 statutory pharmacopoeias (UPI, NFUM, API, AFI, etc.)."""
        return {
            "unani_standards": [
                auth for auth in UNANI_CLASSICAL_AUTHORITIES
                if auth["level"] == AuthorityLevel.LEVEL_4.value
            ],
            "ayurveda_standards": [
                auth for auth in AYURVEDA_CLASSICAL_AUTHORITIES
                if auth["level"] == AuthorityLevel.LEVEL_4.value
            ]
        }

    @classmethod
    def search_authorities(cls, query: str) -> List[Dict[str, Any]]:
        """Searches across both Unani and Ayurvedic authorities, authors, and texts."""
        q_tokens = [w for w in query.lower().strip().split() if len(w) > 2]
        if not q_tokens:
            return UNANI_CLASSICAL_AUTHORITIES[:5] + AYURVEDA_CLASSICAL_AUTHORITIES[:5]

        combined = [
            {**auth, "tradition": "Unani Tibb"} for auth in UNANI_CLASSICAL_AUTHORITIES
        ] + [
            {**auth, "tradition": "Ayurveda"} for auth in AYURVEDA_CLASSICAL_AUTHORITIES
        ]

        scored_results = []
        for item in combined:
            score = 0
            text_corpus = (
                f"{item['title']} {item['author']} {item['category']} {item['importance']} "
                f"{' '.join(item.get('key_volumes', []))} {item['tradition']} {item['level']}"
            ).lower()

            for token in q_tokens:
                if token in item['title'].lower():
                    score += 50
                elif token in item['author'].lower():
                    score += 45
                elif token in item['category'].lower():
                    score += 25
                elif token in text_corpus:
                    score += 15

            if score > 0:
                scored_results.append((score, item))

        scored_results.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored_results]
