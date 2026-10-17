#!/usr/bin/env python3
"""
Enrich Mufradat Monographs with Complete Classical & Pharmacopoeial Parameters
================================================================================
Adds:
1. part_used (Hissa-e-Musta'mala / Prayojya Anga)
2. language_synonyms (Mutradif Naam ba-lihaz-e-zaban: Arabic, Persian, Sanskrit, Urdu, Hindi, English)
3. mahiyat (Classical Physical Examination: Color, Odour, Taste/Zaiqa/Rasa, Appearance/Texture)
4. badraqah (Anupana / Vehicle & Administration Mode)
5. muddat_taseer (Potency Duration / Shelf Life / Qoowat Baqi Rehne ki Muddat)
6. target_organs (Mutassir Aza / Systems Affected)
7. adulterants (Milawat ki Shanakht & Market Substitutes)
"""

import json
import os
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CATALOG_PATH = os.path.join(ROOT_DIR, "catalog_seed.json")
WORKBENCH_PATH = os.path.join(ROOT_DIR, "workbench.html")

HERB_ENRICHMENTS = {
    "berberine": {
        "part_used": "Dried stem wood, roots, and purified aqueous extract (Rasaut / Satva)",
        "language_synonyms": {
            "arabic": "Ambarbaris (عنبر باریس) / Araq-us-Sufr (عرق الصفر)",
            "persian": "Zarishk (زرشک) / Chob-Zard (چوب زرد)",
            "sanskrit": "Daruharidra (दारुहरिद्रा) / Katankateri / Peetadru",
            "urdu": "Darhald / Rasaut (دارہلد / رسوت)",
            "hindi": "Daru Haldi / Rasaut (दारुहल्दी / रसौत)",
            "english": "Indian Barberry / Tree Turmeric"
        },
        "mahiyat": {
            "color": "Yellowish-brown bark externally; intense bright sulfur-yellow internally",
            "odour": "Faint, characteristic bitter-woody",
            "taste": "Intensely bitter and astringent (Talkh / Tikta, Kashaya)",
            "appearance": "Hard, cylindrical, furrowed woody pieces with rough fissured cork and fibrous starchy fracture"
        },
        "badraqah": "Shahad (Honey), Roghan-e-Badam (Sweet Almond Oil), ya Sharbat-e-Banafsha",
        "muddat_taseer": "Khushk Lakri / Chhaal: 3 saal; Purified Rasaut extract: 5–7 saal; Safuf / Churna: 6 mahina",
        "target_organs": "Meda (Stomach), Jigar (Liver), Aam Damvi Dauran (Systemic Circulation), Am'aa (Intestines)",
        "adulterants": "Coscinium fenestratum (False Calumba / Jhar-ki-Hald), Berberis vulgaris bark, and exhausted wood colored with yellow dyes"
    },
    "guggulu": {
        "part_used": "Purified oleo-gum-resin exudate (Samagh-e-Muqil / Shuddha Guggulu Niryasa)",
        "language_synonyms": {
            "arabic": "Muqil (مقل) / Qafal (قفال)",
            "persian": "Boi-e-Jahudan (بوئے جہوداں)",
            "sanskrit": "Guggulu (गुग्गुलु) / Devadhupa / Mahishaksha",
            "urdu": "Muqil / Guggul (مقل / گوگل)",
            "hindi": "Guggul / Guggulu (गुग्गुल)",
            "english": "Indian Bdellium Tree / Guggul Resin"
        },
        "mahiyat": {
            "color": "Golden-amber to dark reddish-brown translucent tears or agglutinated masses",
            "odour": "Balsamic, pleasantly aromatic when warmed or ignited",
            "taste": "Bitter, astringent, acrid with warm balsamic aftertaste",
            "appearance": "Viscid, sticky gum-resin that softens with the warmth of fingers and burns with fragrant smoke"
        },
        "badraqah": "Triphala Kashaya, Ushnodaka (neem garam pani), ya Shahad (Honey)",
        "muddat_taseer": "Purified resin: Increases in therapeutic potency with age (Purana Guggulu retains efficacy up to 5–10 saal)",
        "target_organs": "Mafasil (Joints), Urooq (Vascular Endothelium), Meda (Stomach), Sharayeento-Qalb (Cardiovascular)",
        "adulterants": "Boswellia serrata (Kundur/Salai resin), Commiphora caudata, or synthetic petroleum-derived resins"
    },
    "ashwagandha": {
        "part_used": "Dried mature roots (Bikh-e-Asgandh / Radix / Ashwagandha Mula)",
        "language_synonyms": {
            "arabic": "Kaknaj-e-Hindi (کاکنج ہندی)",
            "persian": "Bahman-e-Surkh / Asgandh (اسگندھ)",
            "sanskrit": "Ashwagandha (अश्वगंधा) / Varahkarni / Hayagandha",
            "urdu": "Asgandh Nagori (اسگندھ ناگوری)",
            "hindi": "Ashwagandha / Asgandh (अश्वगंधा)",
            "english": "Indian Ginseng / Winter Cherry"
        },
        "mahiyat": {
            "color": "Pale yellowish-cream to light grayish-brown externally; creamy-white internally",
            "odour": "Strong, horse-like characteristic (Hayagandha)",
            "taste": "Sweetish, mucilaginous, followed by slight bitterness and acridity",
            "appearance": "Straight, cylindrical, conical tapering roots, 10–20 cm long with starchy, short fracture"
        },
        "badraqah": "Sheer-e-Gao (Cow's Milk), Roghan-e-Zard (Ghee), ya Shahad (Honey)",
        "muddat_taseer": "Salim jadd (Whole root): 2 saal; Safuf / Churna: 6 mahina",
        "target_organs": "Asab-o-Dimagh (CNS & Brain), Majja Dhatu (Nervine axis), Ghudad-e-Nukhamiya (HPA axis), Baah (Reproductive tract)",
        "adulterants": "Withania coagulans roots, Solanum melongena roots, or non-Nagori fibrous exhausted roots"
    },
    "guduchi": {
        "part_used": "Dried mature stem and purified aqueous starchy extract (Sat-e-Gilo / Guduchi Satva)",
        "language_synonyms": {
            "arabic": "Gilo (گلو) / Qalb-un-Nabaat (قلب النبات)",
            "persian": "Gilo (گلو)",
            "sanskrit": "Guduchi (गुडूची) / Amrita / Chhinnaruha",
            "urdu": "Gilo / Sat-e-Gilo (گلو / ست گلو)",
            "hindi": "Giloy / Guruch (गिलोय)",
            "english": "Heart-leaved Moonseed / Tinospora"
        },
        "mahiyat": {
            "color": "Creamy-buff to grayish-brown with prominent lenticels; Sat-e-Gilo is chalky glistening white",
            "odour": "Faint, pleasant botanical odour",
            "taste": "Distinctly bitter (Talkh / Tikta)",
            "appearance": "Cylindrical succulent grooved stems showing wheel-like radial medullary rays in transverse fracture"
        },
        "badraqah": "Shahad (Honey), Neem garam doodh, ya Arq-e-Gaozaban",
        "muddat_taseer": "Khushk tana (Dried stem): 2 saal; Sat-e-Gilo (Starch extract): 3–5 saal; Safuf: 6 mahina",
        "target_organs": "Jigar (Liver), Tehal (Spleen), Khoon (Hematopoietic system), Nizam-e-Munafiat (Immune system)",
        "adulterants": "Tinospora crispa or Tinospora sinensis (which have rougher stems and differing bitter alkaloid profiles)"
    },
    "ginger": {
        "part_used": "Rhizome (Fresh: Adrak / Zanjabeel Ratab; Dried: Sonth / Zanjabeel Yabis / Shunthi)",
        "language_synonyms": {
            "arabic": "Zanjabeel (زنجبیل)",
            "persian": "Shengbeez (شنگویز) / Zanjabeel",
            "sanskrit": "Ardraka (fresh), Shunthi (शुण्ठी), Vishvabheshaja",
            "urdu": "Zanjabeel / Sonth / Adrak (زنجبیل / سونٹھ / ادرک)",
            "hindi": "Adrak / Sonth (अदरक / सोंठ)",
            "english": "Ginger / Dried Ginger Rhizome"
        },
        "mahiyat": {
            "color": "Buff-yellow to pale brown externally; yellowish-white fibrous fracture",
            "odour": "Strongly aromatic, characteristic pungent",
            "taste": "Fiery pungent and warm (Har / Katu)",
            "appearance": "Horizontally laterally compressed, palmately lobed branched rhizomes with short fibrous fracture"
        },
        "badraqah": "Neem garam pani, Shahad (Honey), ya Namak Siyah (Black Salt)",
        "muddat_taseer": "Khushk Sonth: 2 saal; Safuf-e-Sonth: 6 mahina; Taza Adrak: 2–3 hafte",
        "target_organs": "Meda (Stomach), Am'aa (Intestines), Qasbat-ur-Riya (Bronchial tract), Mafasil (Joints)",
        "adulterants": "Spent ginger (exhausted of gingerols/oleoresin), bleached with sulfur or lime"
    },
    "curcumin": {
        "part_used": "Cured and dried rhizome (Bikh-e-Zardchob / Rhizoma / Haridra)",
        "language_synonyms": {
            "arabic": "Kurkum (کرکم) / Urooq-us-Sufr (عروق الصفر)",
            "persian": "Zardchob (زردچوب)",
            "sanskrit": "Haridra (हरिद्रा) / Nisha / Gauri / Peeta",
            "urdu": "Zardchob / Haldi (زردچوب / ہلدی)",
            "hindi": "Haldi (हल्दी)",
            "english": "Turmeric / Indian Saffron"
        },
        "mahiyat": {
            "color": "Deep yellowish-orange to reddish-brown externally; bright golden-orange internally",
            "odour": "Aromatic, pepper-like characteristic",
            "taste": "Warm, spicy, slightly bitter and pungent (Katu / Tikta)",
            "appearance": "Oblong, ovate or cylindrical rounded tubercles with transverse ridges and dense horny fracture"
        },
        "badraqah": "Filfil Siah (Piperine/Black Pepper) + Ghee/Milk as essential bioenhancer lipid vehicle",
        "muddat_taseer": "Salim Ganthian (Whole rhizome): 2–3 saal; Safuf / Haldi powder: 6–12 mahina",
        "target_organs": "Khoon (Blood circulation), Mafasil (Joints), Jigar-o-Mararah (Liver & Biliary tract), Jild (Skin)",
        "adulterants": "Curcuma aromatica, Curcuma zedoaria (Kachur), lead chromate / metanil yellow chemical dyes"
    },
    "ginkgo biloba": {
        "part_used": "Standardized dried fan-shaped leaves (Barg-e-Ginkgo / Ginkgo Folium)",
        "language_synonyms": {
            "arabic": "Shajarat-ul-Hayat (شجرة الحیات) / Ginkgo",
            "persian": "Derakht-e-Chehel Dokhtar (درخت چهل دختر)",
            "sanskrit": "Ginkgo (गिंको) / Vriksha-vishesha",
            "urdu": "Ginkgo Biloba / Shajarat-ul-Hayat (جنگکو / شجرة الحیات)",
            "hindi": "Ginkgo (जिन्कगो बिलोबा)",
            "english": "Maidenhair Tree / Ginkgo Biloba"
        },
        "mahiyat": {
            "color": "Yellowish-green to dark olive green",
            "odour": "Faint, herb-like",
            "taste": "Slightly bitter and astringent",
            "appearance": "Distinctive two-lobed, fan-shaped glabrous leaves with radiating dichotomous venation"
        },
        "badraqah": "Pani ke sath khane ke baad (Postprandial water administration)",
        "muddat_taseer": "Standardized extract (EGb 761): 3 saal; Khushk barg: 1–2 saal",
        "target_organs": "Dimagh-o-Aza-e-Dimaghiya (Cerebrovascular tree), Urooq-e-Shariya (Microcirculation), Qalb (Cardiovascular)",
        "adulterants": "Leaves spiked with cheap synthetic rutin, quercetin, or Sophora japonica extract to artificially inflate flavonol HPLC counts"
    },
    "st. john's wort": {
        "part_used": "Dried flowering aerial tops (Azhar wa Auraq-e-Hufariqoon / Hyperici herba)",
        "language_synonyms": {
            "arabic": "Hufariqoon (ہوفاریقون) / Hashishat-ul-Qalb (حشیشة القلب)",
            "persian": "Hufariqoon / Gol-e-Rai (گل راعی)",
            "sanskrit": "Hufariqoon (हुफारीकून)",
            "urdu": "Hufariqoon / Dazi (ہوفاریقون / دازی)",
            "hindi": "St. John's Wort / Chhanv-Dhoop",
            "english": "St. John's Wort / Amber Touch-and-Heal"
        },
        "mahiyat": {
            "color": "Greenish-yellow stems with bright golden-yellow 5-petaled flowers",
            "odour": "Aromatic, balsam-like resinous",
            "taste": "Astringent, bitter, slightly acrid",
            "appearance": "Two-edged branched stems with opposite oblong leaves bearing translucent glandular dots (perforations)"
        },
        "badraqah": "Sharbat-e-Seb, Honey, ya Arq-e-Baidmushk",
        "muddat_taseer": "Khushk phool wa barg: 1 saal; Standardized extract: 2–3 saal",
        "target_organs": "Nizam-e-Asbi (Central nervous system), Jigar (Hepatic CYP enzymes - potent PXR inducer), Dimagh",
        "adulterants": "Other non-perforated Hypericum species (H. maculatum, H. hirsutum) lacking hyperforin/hypericin content"
    },
    "garlic": {
        "part_used": "Fresh or dehydrated bulb cloves (Seer / Lehsun / Rasona Bulbus)",
        "language_synonyms": {
            "arabic": "Foom (فوم) / Saum (ثوم)",
            "persian": "Seer (سیر)",
            "sanskrit": "Lashuna (लशुन) / Rasona / Ugragandha",
            "urdu": "Seer / Lehsun (سیر / لہسن)",
            "hindi": "Lehsun (लहसुन)",
            "english": "Garlic / Stinking Rose"
        },
        "mahiyat": {
            "color": "Whitish to pinkish-purple papery tunic enclosing yellowish-white fleshy cloves",
            "odour": "Strong, penetrating, characteristic alliacious sulfurous",
            "taste": "Pungent, burning, acrid (Har / Katu)",
            "appearance": "Subglobose compound bulb consisting of 8–20 curved sessile bulblets (cloves)"
        },
        "badraqah": "Sheer-e-Gao (boiled in cow's milk), Sirka (Vinegar), ya Roghan-e-Zaitoon",
        "muddat_taseer": "Taza bulb: 6 mahina; Dehydrated powder: 1 saal; Aged extract: 3 saal",
        "target_organs": "Qalb-o-Sharayeento (Cardiovascular & Endothelium), Safaihat-e-Dam (Platelets), Meda (Stomach)",
        "adulterants": "Allium chinense or exhausted garlic flakes deodorized with solvent extraction"
    },
    "licorice": {
        "part_used": "Dried peeled or unpeeled roots and subterranean stolons (Bikh-e-Asl-us-Soos / Radix / Yashtimadhu)",
        "language_synonyms": {
            "arabic": "Asl-us-Soos (اصل السوس)",
            "persian": "Bekh-e-Mahk (بیخ مہک)",
            "sanskrit": "Yashtimadhu (यष्टिमधु) / Madhuka / Klitaka",
            "urdu": "Asl-us-Soos / Mulethi (اصل السوس / ملٹھی)",
            "hindi": "Mulethi / Jethimadh (मुलेठी)",
            "english": "Licorice / Sweetwood"
        },
        "mahiyat": {
            "color": "Grayish-brown to dark brown bark externally; fibrous lemon-yellow internally",
            "odour": "Faint, characteristic sweet earthy",
            "taste": "Intensely sweet, soothing, followed by slight acridity",
            "appearance": "Long, cylindrical, flexible fibrous woody roots and running stolons"
        },
        "badraqah": "Gulqand, Sharbat-e-Gaozaban, ya Sheer-e-Gao",
        "muddat_taseer": "Salim jadd: 3 saal; Rab-us-Soos (Extract): 5 saal; Safuf: 6–12 mahina",
        "target_organs": "Ghisha-e-Mukhatai (Mucosal membranes of gut and respiratory tract), Qasbat-ur-Riya (Lungs), Ghudad-e-Fauq-ul-Kulyah (Adrenal cortex)",
        "adulterants": "Roots of Abrus precatorius (Gunja roots), Glycyrrhiza uralensis, or Manchurian licorice"
    },
    "gymnema": {
        "part_used": "Dried mature leaves (Barg-e-Gurmar / Meshashringi Patra)",
        "language_synonyms": {
            "arabic": "Gurmar (گڑمار) / Khatm-us-Sukkar",
            "persian": "Gormar (گرمار)",
            "sanskrit": "Meshashringi (मेषशृङ्गी) / Madhunashini",
            "urdu": "Gurmar Booti (گڑمار بوٹی)",
            "hindi": "Gurmar (गुड़मार)",
            "english": "Cowplant / Gymnema / Sugar Destroyer"
        },
        "mahiyat": {
            "color": "Greenish to yellowish-green",
            "odour": "Pleasant, aromatic dried-leaf odour",
            "taste": "Slightly bitter and astringent; temporarily anesthetizes sweet taste receptors on tongue",
            "appearance": "Opposited, ovate or elliptic-oblong pubescent leaves with acute or acuminate apex"
        },
        "badraqah": "Neem garam pani ya Jamun ki guthli ka jushanda",
        "muddat_taseer": "Khushk barg: 1–2 saal; Safuf: 6 mahina; Standardized extract (Gymnemic acid 25%): 3 saal",
        "target_organs": "Labiabah (Pancreatic beta-cells), Meda-o-Am'aa (Intestinal glucose transporters), Zaban (Taste buds)",
        "adulterants": "Leaves of other Asclepiadaceae plants lacking gymnemic acid sweetness-blocking action"
    },
    "green tea": {
        "part_used": "Unfermented, steam-treated or pan-fired dried leaves and leaf buds (Barg-e-Chai Sabz / Theae folium)",
        "language_synonyms": {
            "arabic": "Shai Akhdar (شاي أخضر)",
            "persian": "Chai Sabz (چائے سبز)",
            "sanskrit": "Chaha (चाह) / Patra-vishesha",
            "urdu": "Chai Sabz / Green Tea (چائے سبز)",
            "hindi": "Hari Chai / Green Tea (हरी चाय)",
            "english": "Green Tea / Unfermented Tea"
        },
        "mahiyat": {
            "color": "Dark olive-green to silvery-green twisted rolled leaves",
            "odour": "Pleasantly grassy, vegetative aromatic",
            "taste": "Astringent, slightly bitter followed by sweet vegetal finish",
            "appearance": "Young, lanceolate to elliptical serrate leaves rolled or curled into thin wiry shapes"
        },
        "badraqah": "Kashana / Joshanda (Infusion in hot water at 75–85°C)",
        "muddat_taseer": "Khushk barg (in vacuum/sealed tin): 1 saal; EGCG extract: 2 saal",
        "target_organs": "Qalb-o-Urooq (Cardiovascular & Endothelium), Jigar (Liver), Nizam-e-Tahawwul (Metabolism)",
        "adulterants": "Exhausted tea leaves re-colored with copper salts or mixed with old fermented black tea leaves"
    },
    "milk thistle": {
        "part_used": "Dried ripe seeds/fruits freed from pappus (Tukhm-e-Khaar-e-Maryam / Silybi mariani fructus)",
        "language_synonyms": {
            "arabic": "Shookat-ul-Baiza (شوکة البیضاء) / Khaar-e-Maryam",
            "persian": "Khaar-e-Maryam (خار مریم)",
            "sanskrit": "Dugdha-Kantaka (दुग्ध कंटक)",
            "urdu": "Khaar-e-Maryam / Milk Thistle (خار مریم)",
            "hindi": "Milk Thistle (दूधिया कंटीला)",
            "english": "Milk Thistle / Holy Thistle / St. Mary's Thistle"
        },
        "mahiyat": {
            "color": "Glossy dark brownish-black to mottled grey with yellow apical rim",
            "odour": "Faint, oily characteristic",
            "taste": "Oily, bitter (Talkh)"
        ,
            "appearance": "Obovate, flattened achenes, 6–7 mm long with smooth hard pericarp and white oily endosperm"
        },
        "badraqah": "Pani ke sath khane ke darmiyan (Administered with meals or lecithin for absorption)",
        "muddat_taseer": "Salim beej (Seeds): 2 saal; Standardized Silymarin 80% extract: 3 saal",
        "target_organs": "Jigar (Hepatocytes), Mararah (Gallbladder), Ghisha-e-Khalwi (Cellular membranes)",
        "adulterants": "Seeds of Carduus or Onopordum species with zero silymarin flavonoid content"
    },
    "kava": {
        "part_used": "Dried peeled and cut rhizome and rootstock (Bikh-e-Kava / Piperis methystici rhizoma)",
        "language_synonyms": {
            "arabic": "Filfil-e-Kava (فلفل کاوا) / Kava",
            "persian": "Kava (کاوا)",
            "sanskrit": "Kava-Mula (कावा मूल)",
            "urdu": "Kava Kava (کاوا کاوا)",
            "hindi": "Kava (कावा)",
            "english": "Kava Kava / Kawa Root"
        },
        "mahiyat": {
            "color": "Light yellowish-buff to grayish-brown externally; pale cream internally",
            "odour": "Pleasant, lilaceous, characteristic spicy",
            "taste": "Bitter, pungent, producing temporary tongue and lip numbness/paresthesia",
            "appearance": "Irregular knotty woody rhizome pieces with numerous adventitious roots"
        },
        "badraqah": "Water emulsion or coconut milk (lipophilic vehicle for kavalactone emulsification)",
        "muddat_taseer": "Dried rootstock: 2 saal; Standardized extract (30% kavalactones): 3 saal",
        "target_organs": "Dimagh (Limbic system, GABA-A receptor pathways), Asab (Peripheral nerves), Azlaat (Skeletal muscles)",
        "adulterants": "Toxic aerial stems and leaves of Piper methysticum (which contain toxic alkaloid pipermethystine)"
    },
    "valerian": {
        "part_used": "Dried subterranean rhizomes, roots, and stolons (Bikh-e-Asarun / Tagara Mula / Valerianae radix)",
        "language_synonyms": {
            "arabic": "Asarun (اسارون) / Sumbul-e-Rumi (سنبل رومی)",
            "persian": "Asarun (اسارون)",
            "sanskrit": "Tagara (तगर) / Nata / Kalanusari",
            "urdu": "Asarun / Tagar / Valerian (اسارون / تگر)",
            "hindi": "Tagar / Sugandhabala (तगर)",
            "english": "Valerian / All-Heal / Garden Heliotrope"
        },
        "mahiyat": {
            "color": "Yellowish-brown to dark brown externally; whitish-buff internally",
            "odour": "Penetrating, unpleasant characteristic isovaleric odour (resembling aged cheese)",
            "taste": "Camphoraceous, sweetish, slightly bitter and spicy",
            "appearance": "Short obconical rhizome, 2–5 cm long, surrounded by numerous tangled brittle roots"
        },
        "badraqah": "Sharbat-e-Banafsha, Arq-e-Gaozaban, ya Neem garam doodh",
        "muddat_taseer": "Khushk jadd: 1–2 saal; Safuf / Tincture: 1 saal; Standardized extract: 2–3 saal",
        "target_organs": "Dimagh-o-Asab (CNS, sleep architecture), Azlaat (Smooth muscle antispasmodic)",
        "adulterants": "Valeriana wallichii (Indian Valerian / Tagara) or roots of other Valerianaceae species"
    },
    "ginseng": {
        "part_used": "Cured and dried mature root with rootlets (Bikh-e-Jinseng / Radix / Ginseng Radix)",
        "language_synonyms": {
            "arabic": "Jinseng (جنسنج) / Jinsah",
            "persian": "Jinseng (جنسنگ)",
            "sanskrit": "Jinseng (जिनसेंग) / Vrishya-vishesha",
            "urdu": "Jinseng / Panax Ginseng (جنسنگ)",
            "hindi": "Ginseng (जिनसेंग)",
            "english": "Asian Ginseng / Korean Red Ginseng"
        },
        "mahiyat": {
            "color": "Pale yellowish-white (White Ginseng) or translucent reddish-brown (Red Ginseng)",
            "odour": "Faint, pleasantly aromatic, characteristic sweet",
            "taste": "Sweetish mucilaginous, followed by slight bitterness",
            "appearance": "Spindle-shaped or cylindrical fleshy root, often bifurcated (anthropomorphic shape)"
        },
        "badraqah": "Shahad (Honey), Warm water, ya Arq-e-Gulab",
        "muddat_taseer": "Red Ginseng (steamed): 3–5 saal; White Ginseng: 2 saal; Extract: 3 saal",
        "target_organs": "Qalb-o-Dimagh (Brain & Vital organs), Ghudad-e-Nukhamiya (HPA axis), Hararat-e-Ghariziyya (Innate heat)",
        "adulterants": "Roots of Codonopsis pilosula (Dang Shen), Panax quinquefolius, or Mirabilis jalapa"
    },
    "echinacea": {
        "part_used": "Fresh or dried whole flowering aerial plant and roots (Echinaceae purpureae herba et radix)",
        "language_synonyms": {
            "arabic": "Shookat-e-Arghawani (شوکة ارجوانی) / Echinacea",
            "persian": "Echinacea (اکیناسه)",
            "sanskrit": "Echinacea (इकिनेसिया)",
            "urdu": "Echinacea / Shookat-e-Arghawani (اشیناسیا)",
            "hindi": "Echinacea (इकिनेसिया)",
            "english": "Purple Coneflower / Echinacea"
        },
        "mahiyat": {
            "color": "Greenish stems with purple cone-centered flowers; dark brown fibrous roots",
            "odour": "Faint, pleasant herbal",
            "taste": "Sweetish, producing a distinctive tingling or numbing sensation on tongue",
            "appearance": "Hirsute branched stems with rough ovate leaves and conical daisy-like flower heads"
        },
        "badraqah": "Neem garam pani ya Shahad (Honey)",
        "muddat_taseer": "Khushk jadd wa barg: 1–2 saal; Standardized extract: 3 saal",
        "target_organs": "Nizam-e-Munafiat (Immune system), Qasbat-ur-Riya (Upper respiratory tract), Jild (Skin)",
        "adulterants": "Parthenium integrifolium roots (Missouri snakeroot) or non-medicinal Echinacea species"
    },
    "goldenseal": {
        "part_used": "Dried rhizome and fine fibrous rootlets (Hydrastis rhizoma et radix)",
        "language_synonyms": {
            "arabic": "Zard Chob-e-Kanadi (زرد چوب کینیڈی) / Khatm-uz-Zahab",
            "persian": "Zard Chob-e-Kanadi (زرد چوب کانادایی)",
            "sanskrit": "Peeta-Mula (पीतमूल)",
            "urdu": "Goldenseal / Zard Chob-e-Kanadi (گولڈن سیل)",
            "hindi": "Goldenseal (गोल्डनसील)",
            "english": "Goldenseal / Yellow Puccoon / Ground Raspberry"
        },
        "mahiyat": {
            "color": "Yellowish-brown externally; bright golden-yellow with green tint internally",
            "odour": "Strong, distinctive earthy pungent",
            "taste": "Intensely, tenaciously bitter (Shadeed Talkh)",
            "appearance": "Sub-cylindrical, knotty, contorted rhizome, 1–6 cm long with cup-shaped stem scars"
        },
        "badraqah": "Shahad (Honey) ya Sharbat-e-Banafsha",
        "muddat_taseer": "Khushk rhizome: 2–3 saal; Safuf: 6 mahina; Standardized hydrastine extract: 3 saal",
        "target_organs": "Ghisha-e-Mukhatai (Mucous membranes), Meda (Stomach), Jigar (Liver), Am'aa (Intestines)",
        "adulterants": "Coptis trifolia (Goldthread), Berberis species, or Aristolochia serpentaria"
    },
    "black cohosh": {
        "part_used": "Dried rhizome and roots (Cimicifugae racemosae rhizoma et radix)",
        "language_synonyms": {
            "arabic": "Sanbal-e-Aswad (سنبل اسود) / Cimicifuga",
            "persian": "Sanbal-e-Siah (سنبل سیاه)",
            "sanskrit": "Krishna-Koshaki (कृष्ण कोषकी)",
            "urdu": "Black Cohosh / Sanbal-e-Aswad (بلیک کوہوش)",
            "hindi": "Black Cohosh (ब्लैक कोहोश)",
            "english": "Black Cohosh / Black Bugbane / Rattleroot"
        },
        "mahiyat": {
            "color": "Dark brown to blackish-brown externally; grayish-white horny fracture internally",
            "odour": "Heavy, somewhat disagreeable",
            "taste": "Bitter, acrid, followed by astringency",
            "appearance": "Hard, knotty, horizontally elongated rhizome with cup-shaped scars and branched roots"
        },
        "badraqah": "Pani ke sath khane ke baad (Administered with meals)",
        "muddat_taseer": "Khushk rhizome: 2 saal; Isopropanolic extract (Remifemin spec): 3 saal",
        "target_organs": "Rehm (Uterus), Ghudad-e-Nizam-e-Zanana (Ovaries & neuroendocrine axis), Dimagh (Hypothalamic vasomotor)",
        "adulterants": "Actaea podocarpa, Actaea pachypoda, or Chinese Actaea species"
    },
    "hawthorn": {
        "part_used": "Dried false fruits (berries), leaves, and flowering branch tips (Crataegi fructus cum flore)",
        "language_synonyms": {
            "arabic": "Za'roor (زعرور) / Shookat-ul-Ahmar (شوکة الاحمر)",
            "persian": "Za'roor (زعرور)",
            "sanskrit": "Za'roor (ज़अरूर) / Hrid-Kantaka",
            "urdu": "Za'roor / Hawthorn (زعرور / ہاوتھورن)",
            "hindi": "Hawthorn / Za'roor (हावथॉर्न)",
            "english": "Hawthorn / Mayblossom / Whitethorn"
        },
        "mahiyat": {
            "color": "Dark red to purplish-brown ovate berries; greenish leaves with white petals",
            "odour": "Faint, pleasant fruity floral",
            "taste": "Acidic, sweetish, mucilaginous and slightly astringent (Kashaya / Qabiz)",
            "appearance": "Subglobose false fruit with 1–3 stony pyrenes and persisting calyx remnants"
        },
        "badraqah": "Sharbat-e-Seb, Arq-e-Gulab, ya Honey",
        "muddat_taseer": "Khushk phool wa barg: 1 saal; Khushk samar (Berries): 2 saal; Standardized extract: 3 saal",
        "target_organs": "Qalb (Myocardium & Coronary arteries), Sharayeento (Peripheral vasculature), Fishaar-ud-Dam (Blood pressure)",
        "adulterants": "Crataegus oxyacantha berries substituted with other Pyracantha or Sorbus berries"
    },
    "feverfew": {
        "part_used": "Dried aerial flowering parts and leaves (Tanaceti parthenii herba)",
        "language_synonyms": {
            "arabic": "Aqhawan (اقحوان) / Baboona-e-Kohi (بابونہ کوہی)",
            "persian": "Aqhawan (اقحوان)",
            "sanskrit": "Aqhawan (अकहवान)",
            "urdu": "Aqhawan / Feverfew (اقحوان / فیورفیو)",
            "hindi": "Feverfew (फीवरफ्यू)",
            "english": "Feverfew / Bachelor's Buttons / Featherfoil"
        },
        "mahiyat": {
            "color": "Bright light-green leaves with white ray florets and yellow disc florets",
            "odour": "Strong, pungent, characteristic aromatic camphoraceous",
            "taste": "Extremely bitter, warm and acrid",
            "appearance": "Pinnately divided bipinnate leaves with small daisy-like composite flower heads"
        },
        "badraqah": "Sharbat-e-Banafsha ya Shahad (Honey) ke sath",
        "muddat_taseer": "Khushk booti: 1 saal; Standardized parthenolide (0.2%) extract: 2–3 saal",
        "target_organs": "Urooq-e-Dimaghiya (Cerebral blood vessels), Safaihat-e-Dam (Platelets), Nizam-e-Asbi (Pain pathways)",
        "adulterants": "Matricaria chamomilla or Tanacetum vulgare (Tansy) lacking parthenolide migraine activity"
    },
    "saw palmetto": {
        "part_used": "Ripe, partially dried berries/fruits (Sabalis serrulatae fructus / Samar-e-Sabal)",
        "language_synonyms": {
            "arabic": "Sabal (سابل) / Nakhl-e-Munjami (نخل منجمی)",
            "persian": "Sabal (سابل)",
            "sanskrit": "Sabal (सबल)",
            "urdu": "Saw Palmetto / Sabal (سا پالمیٹو / سابل)",
            "hindi": "Saw Palmetto (सॉ पाल्मेटो)",
            "english": "Saw Palmetto / Dwarf Palm / Cabbage Palm"
        },
        "mahiyat": {
            "color": "Deep brownish-black to purplish-black with dull luster",
            "odour": "Pungent, characteristic rancid-cheesy aromatic",
            "taste": "Sweetish, oily, followed by acrid pungent sensation",
            "appearance": "Ellipsoid or subglobose drupe, 1.5–3 cm long, with wrinkled shriveled pericarp and hard seed"
        },
        "badraqah": "Administered with meals containing dietary fats for liposterolic absorption",
        "muddat_taseer": "Dried whole berries: 2 saal; CO2 lipidic extract (85–95% fatty acids): 3 saal",
        "target_organs": "Ghuda-e-Mazi (Prostate gland), Masana (Urinary bladder neck), Follicles-e-Moo (Hair follicles / DHT axis)",
        "adulterants": "Berries of Serenoa substituted with cheap palm drupes or adulterated with coconut oil to mimic fatty acid spectra"
    },
    "piperine": {
        "part_used": "Dried mature unripe fruits (Filfil Siah / Maricha Phala / Piperis nigri fructus)",
        "language_synonyms": {
            "arabic": "Filfil Aswad (فلفل اسود)",
            "persian": "Filfil Siah (فلفل سیاہ)",
            "sanskrit": "Maricha (मरिच) / Ushana / Krishna",
            "urdu": "Filfil Siah / Kali Mirch (فلفل سیاہ / کالی مرچ)",
            "hindi": "Kali Mirch (काली मिर्च)",
            "english": "Black Pepper / Piperine Extract"
        },
        "mahiyat": {
            "color": "Dark brownish-black to grayish-black deeply reticulated surface; whitish-buff seed internally",
            "odour": "Intensely aromatic, stimulating spicy",
            "taste": "Sharply hot, biting pungent (Har / Katu)",
            "appearance": "Subglobose berry, 3.5–6 mm diameter with coarsely wrinkled surface"
        },
        "badraqah": "Shahad (Honey), Ghee, ya Arq-e-Zira (premier classical Badraqah / Vehicle for other herbs)",
        "muddat_taseer": "Salim Kali Mirch: 3–4 saal; Safuf / Powder: 6 mahina; Pure Piperine 95%: 3 saal",
        "target_organs": "Meda (Gastric mucosa), Jigar (Hepatic portal vein & UGT/P-gp clearance enzymes), Am'aa (Intestinal enterocytes)",
        "adulterants": "Papaya seeds (Carica papaya), exhausted pepper corns, or wild Piper attenuatum"
    },
    "bitter melon": {
        "part_used": "Fresh or dried mature green fruit and seeds (Samar wa Tukhm-e-Karela / Karavellaka Phala)",
        "language_synonyms": {
            "arabic": "Qissa-ul-Barri (قثاء البري) / Karela",
            "persian": "Karela (کریلا)",
            "sanskrit": "Karavellaka (कारवेल्लक) / Sushavi / Kathilla",
            "urdu": "Karela / Samar-e-Karela (کریلا)",
            "hindi": "Karela (करेला)",
            "english": "Bitter Melon / Bitter Gourd / Balsam Pear"
        },
        "mahiyat": {
            "color": "Bright green to dark green externally; white spongy pulp enclosing flattened seeds",
            "odour": "Vegetal, slightly pungent",
            "taste": "Intensely bitter (Shadeed Talkh / Tikta)",
            "appearance": "Oblong, ridged, tuberculate, warty cylindrical fruit tapering at both ends"
        },
        "badraqah": "Taza Aab-e-Karela (Fresh juice), Jamun guthli safuf, ya Neem garam pani",
        "muddat_taseer": "Khushk phaliyan (Dried slices): 1 saal; Taza phal: 1 hafta; Safuf: 6 mahina",
        "target_organs": "Labiabah (Pancreatic islets), Meda (Stomach), Jigar (Liver), Khoon (Glucose clearance)",
        "adulterants": "Momordica dioica (Kantola) or non-bitter cucurbits"
    },
    "fenugreek": {
        "part_used": "Dried ripe seeds (Tukhm-e-Hulba / Methika Beeja / Trigonellae foeni-graeci semen)",
        "language_synonyms": {
            "arabic": "Hulba (حلبة)",
            "persian": "Shanbalid (شنبلیلہ)",
            "sanskrit": "Methika (मेथिका) / Chandrika / Bahupatrika",
            "urdu": "Hulba / Methi Dana (حلبہ / میتھی دانہ)",
            "hindi": "Methi Dana (मेथी दाना)",
            "english": "Fenugreek Seed / Greek Hay"
        },
        "mahiyat": {
            "color": "Yellowish-brown to golden-amber",
            "odour": "Strongly characteristic, maple-like aromatic sweet spicy",
            "taste": "Mucilaginous, bitter, slightly astringent (Talkh / Tikta)",
            "appearance": "Rhomboidal, flattened hard seeds, 3–5 mm long, divided into two unequal lobes by a deep diagonal groove"
        },
        "badraqah": "Neem garam doodh, Joshanda (Decoction), ya Arq-e-Saunf",
        "muddat_taseer": "Salim beej (Whole seeds): 3 saal; Safuf / Powder: 6–12 mahina",
        "target_organs": "Meda-o-Am'aa (Intestinal transit & glucose absorptive surface), Pistan (Mammary glands), Jigar (Lipid metabolism)",
        "adulterants": "Weed seeds of Melilotus or Medicago species mixed with bulk commercial lots"
    },
    "cinnamon": {
        "part_used": "Dried inner bark of shoots freed from outer cork (Post-e-Darchini / Tvak / Cinnamomi cortex)",
        "language_synonyms": {
            "arabic": "Qirfah (قرفة) / Darchini",
            "persian": "Darchini (دارچینی)",
            "sanskrit": "Tvak (त्वक्) / Chocha / Varanga",
            "urdu": "Darchini (دارچینی)",
            "hindi": "Dalchini (दालचीनी)",
            "english": "True Cinnamon / Ceylon Cinnamon"
        },
        "mahiyat": {
            "color": "Pale yellowish-brown to golden-tan smooth surface",
            "odour": "Delicately fragrant, sweet aromatic",
            "taste": "Warm, delightfully sweet, followed by gentle spiciness",
            "appearance": "Compound quills composed of multiple paper-thin inner bark layers tightly rolled into a compact cylinder"
        },
        "badraqah": "Sheer-e-Gao (Warm Milk), Shahad (Honey), ya Arq-e-Gulab",
        "muddat_taseer": "Salim Quills: 3 saal; Safuf / Powder: 6 mahina",
        "target_organs": "Qalb-o-Dimagh (Heart & Brain), Meda (Stomach), Urooq (Endothelium), Insuline receptors",
        "adulterants": "Cassia bark (Cinnamomum cassia / Chinese Cinnamon), which is thicker, single-quilled, rough, and high in hepatotoxic coumarin"
    },
    "grapefruit extract": {
        "part_used": "Standardized seed and inner membranous peel extract (Tukhm wa Post-e-Naranj / Citri paradisi semen)",
        "language_synonyms": {
            "arabic": "Naranj Hindi (نارنج ہندی) / Utruj Kabeer (اترج کبیر)",
            "persian": "Grapefruit / Naranj",
            "sanskrit": "Madhukarkati (मधुकर्कटी)",
            "urdu": "Grapefruit Extract / Naranj (گریپ فروٹ)",
            "hindi": "Chakotara (चकोतरा)",
            "english": "Grapefruit Seed Extract / Pomelo Citrus"
        },
        "mahiyat": {
            "color": "Pale yellow to amber viscid liquid or light yellowish fine powder",
            "odour": "Faint, pleasant citrus aromatic",
            "taste": "Extremely bitter and astringent (Talkh / Tikta)",
            "appearance": "Concentrated bioflavonoid and naringin dry extract or glycerite formulation"
        },
        "badraqah": "Aab-e-Sada (Diluted abundantly in room-temperature water)",
        "muddat_taseer": "Standardized liquid glycerite: 2 saal; Dry extract: 3 saal",
        "target_organs": "Am'aa (Intestinal enterocyte CYP3A4 & P-gp irreversible mechanism-based inactivator), Jigar (Liver)",
        "adulterants": "Commercial extracts adulterated with synthetic synthetic antimicrobial preservatives (benzethonium chloride, triclosan)"
    },
    "rhodiola rosea": {
        "part_used": "Dried subterranean rhizome and roots (Rhodiolae roseae rhizoma et radix / Bikh-e-Rhodiola)",
        "language_synonyms": {
            "arabic": "Asl-e-Zahabi (اصل ذہبی) / Rhodiola",
            "persian": "Rhodiola (رودیولا)",
            "sanskrit": "Rhodiola (रोडियोला) / Suvarna-Mula",
            "urdu": "Rhodiola / Asl-e-Zahabi (روڈیولا / اصل ذہبی)",
            "hindi": "Rhodiola / Golden Root (रोडियोला)",
            "english": "Golden Root / Arctic Root / Rose Root"
        },
        "mahiyat": {
            "color": "Rusty golden-brown externally; pale yellowish-amber internally",
            "odour": "Sweet, distinct rose-like aroma upon peeling or powdering",
            "taste": "Astringent, bitter, followed by cooling sweetish aftertaste",
            "appearance": "Fleshy compact rhizome covered with scaly leaf bases and branching fibrous rootlets"
        },
        "badraqah": "Aab-e-Sada (Water taken on an empty stomach in the morning)",
        "muddat_taseer": "Khushk rhizome: 2–3 saal; Standardized extract (3% rosavins, 1% salidroside): 3 saal",
        "target_organs": "Dimagh (Monoaminergic neurochemical axis), Asab (Autonomic nervous system), HPA Axis, Qalb",
        "adulterants": "Rhodiola crenulata or Rhodiola serrata (which contain salidroside but lack active rosavins)"
    },
    "holy basil": {
        "part_used": "Fresh and dried whole aerial herb, leaves, and seeds (Barg wa Tukhm-e-Raihan / Tulasi Patra)",
        "language_synonyms": {
            "arabic": "Raihan (ریحان) / Habaq (حبق)",
            "persian": "Shah-e-Saparam (شاہسپرم) / Raihan",
            "sanskrit": "Tulasi (तुलसी) / Surasa / Vishnupriya",
            "urdu": "Raihan / Tulsi (ریحان / تلسی)",
            "hindi": "Tulsi (तुलसी)",
            "english": "Holy Basil / Sacred Basil"
        },
        "mahiyat": {
            "color": "Purplish-green to dark green ovate leaves with purple stems (Krishna Tulsi) or bright green (Rama Tulsi)",
            "odour": "Intensely aromatic, clove-like, spicy floral",
            "taste": "Warm, pungent, slightly sweet and astringent (Katu / Tikta)",
            "appearance": "Branching shrub with opposite elliptic-oblong serrate glandular leaves and purple raceme verticillasters"
        },
        "badraqah": "Shahad (Honey), Neem garam doodh, ya Joshanda (Warm tea)",
        "muddat_taseer": "Khushk barg: 1 saal; Taza barg: 3 din; Safuf: 6 mahina; Oil / Extract: 2 saal",
        "target_organs": "Qasbat-ur-Riya (Bronchial airway), Qalb (Cardiovascular & stress resilience), Meda (Digestive fire)",
        "adulterants": "Ocimum basilicum (Sweet Basil) or Ocimum canum leaves lacking eugenol/ursolic acid pharmacological profile"
    },
    "shilajit": {
        "part_used": "Purified mineralo-organic bitumen exudate (Shuddha Shilajatu / Salajit Musaffa / Asphaltum punjabianum)",
        "language_synonyms": {
            "arabic": "Hajar-ul-Moomia (حجر المومیا) / Salajit",
            "persian": "Moomiaee (مومیائی)",
            "sanskrit": "Shilajatu (शिलाजतु) / Adrija / Gireesha",
            "urdu": "Salajit / Shilajit (سلاجیت)",
            "hindi": "Shilajit (शिलाजीत)",
            "english": "Mineral Pitch / Shilajit / Asphaltum"
        },
        "mahiyat": {
            "color": "Pitch-black to dark brownish-black glistening lustrous surface",
            "odour": "Characteristic cow-urine like (Gomutra-gandhi) pungent bituminous odour",
            "taste": "Bitter, acrid, salty, astringent with persistent mineral aftertaste",
            "appearance": "Viscous gummy tar that solidifies at low temperatures and dissolves 100% in warm water without residue"
        },
        "badraqah": "Sheer-e-Gao (Warm Cow's Milk), Honey, Triphala Kashaya, ya Doodh-Ghee",
        "muddat_taseer": "Salajit Musaffa (Purified mineral pitch): An-mutanahi (Indefinite shelf life; exceeds 10–20 saal if kept hermetic)",
        "target_organs": "Kulyah (Kidneys & Urogenital), Asab (Nervine stamina), Mitochondria (Cellular ATP), Majja Dhatu",
        "adulterants": "Crude unpurified shilajit containing heavy metals/mycotoxins, synthetic coal tar, or brown sugar/gum adulterations"
    },
    "triphala": {
        "part_used": "Equal proportions of dried pericarp of Haritaki (Halela Zard), Bibhitaki (Balela), and Amalaki (Amla) without seeds",
        "language_synonyms": {
            "arabic": "Itrifal Sazaj (اطریفل ساذج) / Salasah Thimar",
            "persian": "Itrifal (اطریفل)",
            "sanskrit": "Triphala (त्रिफला) / Phalatrikam / Vara",
            "urdu": "Triphala / Itrifal (اطریفل / تریپھلا)",
            "hindi": "Triphala (त्रिफला)",
            "english": "Three Fruits Compound / Triphala"
        },
        "mahiyat": {
            "color": "Yellowish-brown to grayish-brown homogeneous fine powder",
            "odour": "Pleasant, characteristic fruity sour",
            "taste": "All tastes except salty: Astringent, sour, sweet, bitter, and pungent (Kashaya / Amla pradhana)",
            "appearance": "Finely pulverized compound powder of dried three myrobalan rinds"
        },
        "badraqah": "Neem garam doodh, Ushnodaka (Warm water), Shahad (Honey), ya Roghan-e-Badam",
        "muddat_taseer": "Safuf / Churna: 6 mahina; Itrifal Majun (in Honey/Qawam base): 2–3 saal",
        "target_organs": "Am'aa (Colon & Intestinal peristalsis), Meda (Stomach), Basarat (Ocular vision), Jigar (Liver detoxification)",
        "adulterants": "Inclusion of heavy inert seeds (kernels) in place of pericarp pulp to add weight, or exhausted tannery myrobalan waste"
    },
    "senna": {
        "part_used": "Dried leaflets and mature legumes/pods (Barg wa Phali-e-Sana / Sennae folium et fructus)",
        "language_synonyms": {
            "arabic": "Sana Makki (سنا مکی)",
            "persian": "Sana (سنا)",
            "sanskrit": "Markandika (मार्कण्डिका) / Swarnapatri",
            "urdu": "Sanay Makki (سنائے مکی)",
            "hindi": "Sanay (सनाय)",
            "english": "Alexandrian Senna / Tinnevelly Senna"
        },
        "mahiyat": {
            "color": "Yellowish-green to brownish-green thin leaflets; brown flat pods",
            "odour": "Faint, characteristic tea-like",
            "taste": "Mucilaginous, sweetish at first, then distinctly bitter and nauseous",
            "appearance": "Lanceolate to ovate-lanceolate inequilateral leaflets, 2–4 cm long with prominent reticulate venation"
        },
        "badraqah": "Gulqand, Roghan-e-Badam, ya Anisoon (Anise seed) to prevent griping (Musleh-e-Mughes)",
        "muddat_taseer": "Khushk patti: 1 saal; Standardized sennoside extract: 2–3 saal; Safuf: 6 mahina",
        "target_organs": "Am'aa-e-Ghaleezah (Colon - peristaltic stimulation via myenteric plexus), Meda",
        "adulterants": "Cassia obovata (Dog senna), Cassia auriculata (Palthe senna), or leaves of Arghel (Solenostemma argel)"
    },
    "astragalus": {
        "part_used": "Dried sliced root (Bikh-e-Astragalus / Astragali membranacei radix)",
        "language_synonyms": {
            "arabic": "Asl-ul-Quwwat (اصل القوة) / Astragalus",
            "persian": "Astragalus (گون)",
            "sanskrit": "Astragalus (अस्ट्रागालस)",
            "urdu": "Astragalus / Asl-ul-Quwwat (اسٹراگالس)",
            "hindi": "Astragalus (अस्ट्रागालस)",
            "english": "Milk Vetch / Astragalus / Yellow Leader (Huang Qi)"
        },
        "mahiyat": {
            "color": "Pale yellowish-brown externally; fibrous yellowish-white internally with radial wood rays",
            "odour": "Faint, pleasant sweet legume-like",
            "taste": "Mildly sweet, mucilaginous, pleasant starchy",
            "appearance": "Long, flexible cylindrical tongue-like slices with fibrous feathered fracture"
        },
        "badraqah": "Joshanda (Decoction in water) ya Shahad (Honey)",
        "muddat_taseer": "Khushk katliyan (Slices): 2 saal; Standardized polysaccharide extract: 3 saal",
        "target_organs": "Nizam-e-Munafiat (Bone marrow & immune axis), Kulyah (Renal podocytes), Qalb (Cardiovascular)",
        "adulterants": "Roots of non-medicinal Astragalus species or Medicago sativa (alfalfa) roots"
    },
    "resveratrol": {
        "part_used": "Standardized dried rhizome extract of Japanese knotweed (Bikh-e-Huzhang / Polygoni cuspidati rhizoma)",
        "language_synonyms": {
            "arabic": "Huzhang (ہوجانگ) / Resveratrol",
            "persian": "Resveratrol (رزوراترول)",
            "sanskrit": "Resveratrol (रेस्वेराट्रोल)",
            "urdu": "Resveratrol / Huzhang (رسویراٹرول / ہوجانگ)",
            "hindi": "Resveratrol (रेस्वेराट्रोल)",
            "english": "Japanese Knotweed Extract / Trans-Resveratrol"
        },
        "mahiyat": {
            "color": "Light beige to off-white fine crystalline powder (Pure trans-resveratrol 98%)",
            "odour": "Practically odourless",
            "taste": "Slightly bitter and astringent",
            "appearance": "Fine microcrystalline powder derived from ethanolic rhizome extraction"
        },
        "badraqah": "Administered with a dietary fat meal (olive oil, yogurt) to stimulate micellar bile absorption",
        "muddat_taseer": "Pure trans-resveratrol powder (protected from UV light): 2–3 saal",
        "target_organs": "Urooq-e-Dam (Vascular endothelium), SIRT1 pathways, Qalb (Cardiomyocytes), Jigar",
        "adulterants": "Synthetic cis-resveratrol isomers or unpurified root powders high in laxative emodin"
    },
    "quercetin": {
        "part_used": "Purified bioflavonoid aglycone derived from Sophora japonica flower buds (Azhar-e-Huaihua / Sophorae japonicae flos)",
        "language_synonyms": {
            "arabic": "Huaihua (ہوائی ہوا) / Quercetin",
            "persian": "Quercetin (کوئرستین)",
            "sanskrit": "Quercetin (क्वेरसेटिन)",
            "urdu": "Quercetin / Azhar-e-Huaihua (کوئرسٹن)",
            "hindi": "Quercetin (क्वेरसेटिन)",
            "english": "Quercetin Dihydrate / Sophora Flavonoid"
        },
        "mahiyat": {
            "color": "Brilliant bright yellow to greenish-yellow crystalline powder",
            "odour": "Odourless",
            "taste": "Tenaciously bitter (Talkh)",
            "appearance": "Fine acicular microcrystalline powder insoluble in cold water"
        },
        "badraqah": "Bromelain + Vitamin C (Ascorbic acid) as synergistic absorption bioenhancers",
        "muddat_taseer": "Dry sealed dihydrate powder: 3 saal",
        "target_organs": "Khulaya-e-Mast (Mast cells / Histamine stabilization), Urooq (Capillary permeability), Lungs",
        "adulterants": "Crude unhydrolyzed rutin sold as quercetin, or synthetic yellow dyes"
    }
}

def update_catalog():
    print(f"Reading {CATALOG_PATH}...")
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Enrich Monographs
    monos = data.get("monographs", {})
    enriched_count = 0
    for k, info in HERB_ENRICHMENTS.items():
        if k in monos:
            m = monos[k]
            m["part_used"] = info["part_used"]
            m["language_synonyms"] = info["language_synonyms"]
            m["mahiyat"] = info["mahiyat"]
            m["badraqah"] = info["badraqah"]
            m["muddat_taseer"] = info["muddat_taseer"]
            m["target_organs"] = info["target_organs"]
            m["adulterants"] = info["adulterants"]
            enriched_count += 1

    print(f"✓ Enriched {enriched_count} monographs in catalog_seed.json")

    # 2. Enrich Entries
    entries = data.get("entries", [])
    entry_count = 0
    for entry in entries:
        k = entry.get("key", "")
        if k in HERB_ENRICHMENTS:
            info = HERB_ENRICHMENTS[k]
            entry["part_used"] = info["part_used"]
            entry["language_synonyms"] = info["language_synonyms"]
            entry["mahiyat"] = info["mahiyat"]
            entry["badraqah"] = info["badraqah"]
            entry["muddat_taseer"] = info["muddat_taseer"]
            entry["target_organs"] = info["target_organs"]
            entry["adulterants"] = info["adulterants"]
            entry_count += 1

    print(f"✓ Enriched {entry_count} entries in catalog_seed.json")

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✓ Successfully saved updated catalog_seed.json")

if __name__ == "__main__":
    update_catalog()
