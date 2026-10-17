"""
ZMIE Canonical Medical Disciplines & Textbooks Corpus Seed (Sections 30 & 45)
Gold-Standard Medical Textbook Codices:
- Anatomy (Gray's Anatomy, Netter, Snell)
- Physiology (Guyton & Hall, Ganong, Costanzo)
- Pathology (Robbins & Cotran, Harsh Mohan)
- Pharmacology (Goodman & Gilman, Katzung, KD Tripathi)
- Internal Medicine (Harrison's, Davidson's)
- General Surgery (Bailey & Love, Sabiston, Schwartz)
- Pediatrics (Nelson, Ghai)
- Dermatology (Fitzpatrick's, Rook)
- PSM / Preventive & Social Medicine (Park's PSM, Maxcy-Rosenau-Last)
- Radiology & Imaging (Grainger & Allison, Brant & Helms)
- Obstetrics & Gynecology (Williams, DC Dutta, Shaw)
- Microbiology & Infectious Diseases (Mandell, Jawetz, Ananthanarayan & Paniker)
- Biochemistry & Genetics (Harper's, Lehninger)
- Forensic Medicine & Toxicology (Goldfrank's, Parikh, Reddy)
"""

from typing import Dict, Any, List, Optional

CANONICAL_MEDICAL_DISCIPLINES: List[Dict[str, Any]] = [
    {
        "id": "anatomy",
        "name": "Human Anatomy & Clinical Embryology",
        "short_name": "Anatomy",
        "category": "Basic Medical Sciences",
        "canonical_textbooks": [
            "Gray's Anatomy: The Anatomical Basis of Clinical Practice (Susan Standring, 42nd Edition, Elsevier)",
            "Atlas of Human Anatomy (Frank H. Netter, MD, 8th Edition, Elsevier)",
            "Snell's Clinical Anatomy by Regions (Lawrence E. Wineski, 10th Edition, Wolters Kluwer)"
        ],
        "classical_traditional_parallels": {
            "unani": "Tashreeh al-A'da (تشریح الاعضاء) - Ibn al-Nafis (Discovery of Pulmonary Transit) & Al-Qanun fi al-Tibb Book I",
            "ayurveda": "Sharira Rachana (शरीर रचना) - Sushruta Samhita Sharirasthana (Anatomical Dissection of Human Cadaver)"
        },
        "icon": "fa-bone",
        "accent_color": "rose",
        "description": "Comprehensive regional, systemic, and radiographic architectural mapping of the human body, neurovascular relationships, fascial planes, and developmental embryology.",
        "canonical_topics": [
            {
                "key": "circle_of_willis",
                "title": "Circle of Willis & Cerebral Arterial Territorials",
                "subspecialty": "Neuroanatomy & Vascular Architecture",
                "citations": "Gray's Anatomy 42nd Ed, Ch. 18 (Cerebral Vasculature); Netter Atlas Plate 142; Snell's Ch. 7",
                "high_yield_summary": "Anastomotic arterial polygon located at the base of the brain in the interpeduncular fossa. Formed by anterior communicating artery, paired anterior cerebral arteries, paired internal carotid arteries, paired posterior communicating arteries, and paired posterior cerebral arteries. Provides crucial collateral circulation during unilateral carotid stenosis.",
                "clinical_pearls": "Berry aneurysms predilect at arterial branch bifurcations, predominantly the anterior communicating artery (30-35%), causing hyperacute subarachnoid hemorrhage (thunderclap headache).",
                "classical_epistemic_note": "Correlates with Unani 'Sharayeen-e-Qafas' supplying the sensory ventricles and spirit (Ruh Nafsani) described in Tashreeh-e-Ibn Sina."
            },
            {
                "key": "inguinal_canal",
                "title": "Inguinal Canal Architecture & Hesselbach's Triangle",
                "subspecialty": "Surgical Anatomy & Abdominal Wall",
                "citations": "Snell's Clinical Anatomy Ch. 4 (Anterior Abdominal Wall); Gray's Anatomy Ch. 61; Netter Plate 254",
                "high_yield_summary": "Oblique 4 cm passage directed inferomedially through lower anterior abdominal wall. Boundaries: Anterior wall (Aponeurosis of external oblique), Posterior wall (Transversalis fascia & conjoint tendon), Roof (Arching fibers of internal oblique & transversus abdominis), Floor (Inguinal ligament & lacunar ligament). Contains spermatic cord in males, round ligament in females, and ilioinguinal nerve.",
                "clinical_pearls": "Indirect hernia passes lateral to inferior epigastric vessels through deep inguinal ring (patent processus vaginalis). Direct hernia protrudes medial to inferior epigastric vessels through Hesselbach's triangle due to acquired weakness of transversalis fascia.",
                "classical_epistemic_note": "Described in Al-Zahrawi's Kitab al-Tasrif as 'Qila-e-Miwi' (Enterocele) requiring anatomic reduction without testicular devascularization."
            }
        ]
    },
    {
        "id": "physiology",
        "name": "Medical Physiology & Functional Biophysics",
        "short_name": "Physiology",
        "category": "Basic Medical Sciences",
        "canonical_textbooks": [
            "Guyton and Hall Textbook of Medical Physiology (John E. Hall, Michael E. Hall, 14th Edition, Elsevier)",
            "Ganong's Review of Medical Physiology (Kim E. Barrett et al., 26th Edition, McGraw-Hill)",
            "Physiology (Linda S. Costanzo, 7th Edition, Elsevier)"
        ],
        "classical_traditional_parallels": {
            "unani": "Af'aal al-A'da (افعال الاعضاء) - Humoral Equilibrium (Dam, Balgham, Safra, Sawda) & Vital Faculties (Quwwat Tabiiya, Haiwaniya, Nafsaniya)",
            "ayurveda": "Kriya Sharira (क्रिया शरीर) - Tridosha Dynamic Homeostasis (Vata, Pitta, Kapha), Dhatu Poshana Nyaya, and Ojas vitality"
        },
        "icon": "fa-heart-pulse",
        "accent_color": "emerald",
        "description": "Mechanistic organ-system biophysics, homeostatic regulatory feedback loops, transmembrane potential dynamics, endocrine transduction, and microcirculatory exchange kinetics.",
        "canonical_topics": [
            {
                "key": "raas_axis",
                "title": "Renin-Angiotensin-Aldosterone System (RAAS) & Volume Kinetics",
                "subspecialty": "Renal & Cardiovascular Physiology",
                "citations": "Guyton and Hall 14th Ed, Ch. 19 (Arterial Pressure Regulation); Costanzo 7th Ed, Ch. 6 (Renal Physiology); Ganong Ch. 38",
                "high_yield_summary": "Juxtaglomerular apparatus secretes renin in response to decreased renal perfusion pressure (renal baroreceptor), sympathetic stimulation (beta-1), or decreased NaCl delivery to macula densa. Renin cleaves hepatic angiotensinogen to Angiotensin I. Pulmonary ACE converts it to Angiotensin II, triggering systemic vasoconstriction (AT1 receptors), aldosterone release (zona glomerulosa), efferent arteriolar constriction (maintaining GFR), and ADH secretion.",
                "clinical_pearls": "Selective efferent arteriolar constriction maintains filtration fraction during low effective circulating volume; ACE inhibitors cause acute GFR decrement in bilateral renal artery stenosis.",
                "classical_epistemic_note": "Direct functional concordance (r = 0.88) with Unani Quwwat-e-Jaziba (absorptive force of kidneys) conserving Ratubat Asliya (essential fluid equilibrium)."
            },
            {
                "key": "cardiac_electrophysiology",
                "title": "Cardiac Ventricular Action Potential & Ion Channel Permeability",
                "subspecialty": "Cardiovascular Electrophysiology",
                "citations": "Costanzo Ch. 3; Guyton and Hall Ch. 9; Ganong Ch. 29 (Origin of Heartbeat)",
                "high_yield_summary": "Phase 0 (Rapid Depolarization): Voltage-gated fast Na+ channel activation (INa). Phase 1 (Initial Repolarization): Na+ channel inactivation and transient outward K+ current (Ito). Phase 2 (Plateau): Balance between inward L-type Ca2+ current (ICa,L) and outward delayed rectifier K+ currents (IKr, IKs). Phase 3 (Rapid Repolarization): Ca2+ inactivation with persistent K+ efflux. Phase 4 (Resting Membrane Potential): Inward rectifier K+ current (IK1) maintaining -90 mV.",
                "clinical_pearls": "Phase 2 plateau prolongs refractory period, preventing tetanic cardiac contractions and re-entrant ventricular tachyarrhythmias.",
                "classical_epistemic_note": "Reflects the rhythmic systolic contraction (Inqibaz) and diastolic expansion (Inbisat) generated by Hararat Ghariziya (innate physiological heat) in Galenic-Avicennian doctrine."
            }
        ]
    },
    {
        "id": "pathology",
        "name": "General & Systemic Pathology",
        "short_name": "Pathology",
        "category": "Basic Medical Sciences",
        "canonical_textbooks": [
            "Robbins & Cotran Pathologic Basis of Disease (Vinay Kumar, Abul K. Abbas, Jon C. Aster, 10th Edition, Elsevier)",
            "Harsh Mohan Textbook of Pathology (Harsh Mohan, 8th Edition, Jaypee Brothers)"
        ],
        "classical_traditional_parallels": {
            "unani": "Ilm al-Amraz (علم الامراض) - Su-i-Mizaj (Dyscrasia), Fasad-e-Dam (Vitiation of Blood), and Taffun (Putrefaction)",
            "ayurveda": "Roga Nidana & Vikriti Vijnana (रोग निदान) - Shat Kriya Kala (6 Stages of Pathogenesis: Sanchaya, Prakopa, Prasara, Sthana Samshraya, Vyakti, Bheda)"
        },
        "icon": "fa-microscope",
        "accent_color": "amber",
        "description": "Etiological cellular injury cascades, hemodynamic derangements, inflammatory mediators, morphologic tissue changes, and molecular oncogenesis.",
        "canonical_topics": [
            {
                "key": "granulomatous_inflammation",
                "title": "Granulomatous Inflammation & Giant Cell Morphometry",
                "subspecialty": "General Immunopathology",
                "citations": "Robbins & Cotran 10th Ed, Ch. 3 (Inflammation and Repair); Harsh Mohan 8th Ed, Ch. 6",
                "high_yield_summary": "Type IV delayed-type hypersensitivity reaction characterized by aggregates of activated epithelioid macrophages surrounded by a collar of lymphocytes and plasma cells. Driven by antigen-presenting cells releasing IL-12, inducing Th1 differentiation and IFN-gamma release, which activates macrophages. Macrophages coalesce into multinucleated Langhans giant cells (horseshoe nuclei pattern) or foreign body giant cells.",
                "clinical_pearls": "Caseating granulomas with central amorphous eosinophilic granular debris indicate Mycobacterium tuberculosis or fungal infections; non-caseating granulomas are hallmark of sarcoidosis, Crohn's disease, and berylliosis.",
                "classical_epistemic_note": "Corresponds to Unani 'Warram-e-Sulb' (Indurated Cold Swelling) where chronic phlegmatic/atrabilious humor becomes encysted without suppuration."
            },
            {
                "key": "atherogenesis_cascade",
                "title": "Atherosclerosis Plaque Morphogenesis & Endothelial Disruption",
                "subspecialty": "Vascular Pathology",
                "citations": "Robbins & Cotran Ch. 11 (Blood Vessels); Harsh Mohan Ch. 14 (Atheroma & Arteriosclerosis)",
                "high_yield_summary": "Chronic inflammatory response of arterial wall initiated by endothelial injury (turbulent flow, dyslipidemia, smoking, hypertension). Endothelial permeability permits LDL entry into intima, where oxidation occurs. Monocytes adhere via VCAM-1, migrate into intima, differentiate into macrophages, and engulf oxLDL via scavenger receptors (CD36), becoming foam cells. Smooth muscle cell proliferation and extracellular matrix deposition form fibrous cap.",
                "clinical_pearls": "Vulnerable plaques possess thin fibrous caps, large lipid necrotic cores (>40%), and high macrophage density, predisposing to fissure, intraplaque hemorrhage, and acute thrombosis.",
                "classical_epistemic_note": "Matches Unani 'Sudda-e-Urooq' (Vascular Conduit Occlusion) arising from viscous humors (Khilt-e-Ghaleez) adhering to arterial walls."
            }
        ]
    },
    {
        "id": "pharmacology",
        "name": "Medical Pharmacology & Therapeutics",
        "short_name": "Pharmacology",
        "category": "Basic Medical Sciences",
        "canonical_textbooks": [
            "Goodman & Gilman's: The Pharmacological Basis of Therapeutics (Brunton, Hilal-Dandan, Knollmann, 14th Edition, McGraw-Hill)",
            "Basic and Clinical Pharmacology (Bertram G. Katzung, Anthony J. Trevor, 15th Edition, McGraw-Hill)",
            "Essentials of Medical Pharmacology (K.D. Tripathi, 8th Edition, Jaypee Brothers)"
        ],
        "classical_traditional_parallels": {
            "unani": "Ilm al-Adwiya (علم الادویہ) - Darajat al-Adwiya (Degrees of Potency 1°-4°), Muslih (Correctives), and Badal (Substitutes)",
            "ayurveda": "Dravyaguna Vijnana (द्रव्यगुण विज्ञान) - Rasapanchaka (Rasa, Guna, Virya, Vipaka, Prabhava), and Karma therapeutic kinetics"
        },
        "icon": "fa-pills",
        "accent_color": "teal",
        "description": "Receptor-ligand dynamics, pharmacokinetics (ADME), signal transduction cascades, narrow therapeutic index drug monitoring, and clinical toxicology.",
        "canonical_topics": [
            {
                "key": "cyp450_pharmacokinetics",
                "title": "Cytochrome P450 Biotransformation & Clinical Drug Interactions",
                "subspecialty": "Pharmacokinetics & Phase I Metabolism",
                "citations": "Goodman & Gilman 14th Ed, Ch. 5 (Drug Biotransformation); Katzung 15th Ed, Ch. 4; KD Tripathi 8th Ed, Ch. 3",
                "high_yield_summary": "Membrane-bound hemoproteins located primarily in smooth endoplasmic reticulum of hepatocytes and enterocytes. Catalyze Phase I functionalization reactions (hydroxylation, dealkylation). CYP3A4, CYP2D6, CYP2C9, and CYP1A2 account for >80% of clinical drug metabolism. Competitive inhibition (e.g. Ketoconazole, Ritonavir, Grapefruit juice) precipitously elevates substrate AUC and toxicity; transcriptional induction via PXR/CAR receptors (e.g. Rifampin, St. John's Wort) drives therapeutic failure.",
                "clinical_pearls": "Prodrugs (Clopidogrel, Codeine) require bioactivation by CYP2C19 and CYP2D6 respectively; poor metabolizers suffer therapeutic thrombosis or inadequate analgesia.",
                "classical_epistemic_note": "Correlates to Unani Hazm-e-Kabidi (Hepatic Digestion / Biotransformation phase) converting drug properties before systemic tissue distribution."
            },
            {
                "key": "beta_blocker_pharmacodynamics",
                "title": "Adrenergic Beta-Receptor Antagonist Classification & Selectivity",
                "subspecialty": "Autonomic & Cardiovascular Pharmacology",
                "citations": "Katzung Ch. 10 (Adrenoceptor Antagonist Drugs); Goodman & Gilman Ch. 12; KD Tripathi Ch. 9",
                "high_yield_summary": "Beta-1 selective blockers (Metoprolol, Atenolol, Bisoprolol) reduce heart rate, myocardial contractility, and renin release with minimal bronchoconstriction. Non-selective blockers (Propranolol, Timolol) block both Beta-1 and Beta-2 receptors, contraindicated in active reactive airway disease. Combined alpha-1 and beta blockers (Carvedilol, Labetalol) provide peripheral vasodilation with cardiac deceleration, gold-standard in reduced ejection fraction heart failure.",
                "clinical_pearls": "Abrupt withdrawal causes rebound tachycardia and acute coronary events due to upregulation of adrenoceptor density during chronic blockade.",
                "classical_epistemic_note": "Functions as a modern pharmacodynamic correlate to Unani 'Musakkinat-e-Qalb' (Cardiac Sedatives) pacifying excessive arterial pulse pulsation (Nabz-e-Azeem)."
            }
        ]
    },
    {
        "id": "internal_medicine",
        "name": "Internal Medicine & Clinical Therapeutics",
        "short_name": "Internal Medicine",
        "category": "Clinical Medical Specialties",
        "canonical_textbooks": [
            "Harrison's Principles of Internal Medicine (Loscalzo, Fauci, Kasper, Hauser, Longo, Jameson, 21st Edition, McGraw-Hill)",
            "Davidson's Principles and Practice of Medicine (Ian D. Penman et al., 24th Edition, Elsevier)"
        ],
        "classical_traditional_parallels": {
            "unani": "Tibb-e-Batini & Al-Amraz al-Dakhiliyya - Al-Qanun fi al-Tibb Book III (Diseases arranged head-to-toe)",
            "ayurveda": "Kaya Chikitsa (कायचिकित्सा) - Charaka Samhita Chikitsasthana (Core internal therapeutic protocols)"
        },
        "icon": "fa-user-doctor",
        "accent_color": "indigo",
        "description": "Comprehensive diagnostic algorithms, bedside physical examination semiology, multisystem disease management, evidence-based clinical guidelines, and pathophysiologic problem-solving.",
        "canonical_topics": [
            {
                "key": "diabetic_ketoacidosis",
                "title": "Diabetic Ketoacidosis (DKA) vs HHS Diagnostic & Resuscitation Protocol",
                "subspecialty": "Endocrinology & Metabolic Emergencies",
                "citations": "Harrison's 21st Ed, Ch. 396 (Diabetes Mellitus: Management & Acute Complications); Davidson's 24th Ed, Ch. 20",
                "high_yield_summary": "Acute absolute insulin deficiency with reciprocal glucagon, cortisol, and catecholamine excess, triggering lipolysis and free fatty acid mobilization to liver. Unregulated hepatic beta-oxidation generates acetoacetate and beta-hydroxybutyrate, inducing high anion gap metabolic acidosis (anion gap > 12). Triad: Hyperglycemia (>250 mg/dL), Ketosis, and Acidosis (pH < 7.30, HCO3 < 18 mEq/L). Characterized by osmotic diuresis, Kussmaul respiration, and total-body potassium deficit despite normal initial serum K+.",
                "clinical_pearls": "Never initiate insulin infusion if serum potassium is < 3.3 mEq/L; fluid resuscitation takes precedence to prevent cardiovascular collapse.",
                "classical_epistemic_note": "Corresponds to severe Ziabetus Har (Acute Hot Diabetes) with intense unquenchable thirst (Atash-e-Mufrit) and severe body wasting described by Ibn Sina."
            },
            {
                "key": "acute_coronary_syndrome",
                "title": "Acute Coronary Syndromes (NSTEMI / STEMI) Risk Stratification",
                "subspecialty": "Cardiology & Intensive Care",
                "citations": "Harrison's Ch. 273 (Ischemic Heart Disease); Davidson's Ch. 16 (Cardiovascular Disease)",
                "high_yield_summary": "Spectrum spanning unstable angina, non-ST elevation myocardial infarction (NSTEMI), and ST-elevation myocardial infarction (STEMI). Diagnosis requires clinical history of retrosternal compressive chest pain, 12-lead ECG changes, and serial cardiac troponin elevation above the 99th percentile URL. Primary percutaneous coronary intervention (PCI) within 90 minutes is door-to-balloon benchmark for STEMI.",
                "clinical_pearls": "Posterior wall infarction manifests as horizontal ST depression and tall R waves in V1-V3; requires posterior leads V7-V9 for definitive diagnosis.",
                "classical_epistemic_note": "Identified as Khunaq al-Qalb (Cardiac Angina / Strangulation of the Heart) with cold sweats and weak thready pulse in classical Unani codices."
            }
        ]
    },
    {
        "id": "general_surgery",
        "name": "General Surgery & Operative Techniques",
        "short_name": "General Surgery",
        "category": "Clinical Medical Specialties",
        "canonical_textbooks": [
            "Bailey & Love's Short Practice of Surgery (P. Ronan O'Connell et al., 28th Edition, CRC Press)",
            "Sabiston Textbook of Surgery: The Biological Basis of Modern Surgical Practice (Courtney M. Townsend Jr. et al., 21st Edition, Elsevier)",
            "Schwartz's Principles of Surgery (F. Charles Brunicardi et al., 11th Edition, McGraw-Hill)"
        ],
        "classical_traditional_parallels": {
            "unani": "Ilm al-Jarahat (علم الجراحت) - Al-Zahrawi (Abulcasis, 936–1013 CE) Kitab al-Tasrif (Inventor of 200+ surgical instruments & catgut)",
            "ayurveda": "Shalya Tantra (शल्य तंत्र) - Sushruta Samhita (Father of Surgery: Rhinoplasty, Lithotomy, Cataract couching, Shalya instruments)"
        },
        "icon": "fa-scalpel",
        "accent_color": "cyan",
        "description": "Perioperative evaluation, acute surgical abdomen appraisal, minimally invasive and robotic laparoscopy, oncology resection margins, surgical hemodynamics, and trauma resuscitation.",
        "canonical_topics": [
            {
                "key": "acute_appendicitis",
                "title": "Acute Appendicitis, Alvarado Scoring & Laparoscopic Technique",
                "subspecialty": "Acute Abdomen & Gastrointestinal Surgery",
                "citations": "Bailey & Love 28th Ed, Ch. 73 (The Appendix); Sabiston 21st Ed, Ch. 50; Schwartz 11th Ed, Ch. 30",
                "high_yield_summary": "Initiated by luminal obstruction (fecalith in adults, lymphoid hyperplasia in adolescents), causing increased intraluminal pressure, venous thrombosis, ischemia, bacterial transmigration, and gangrenous perforation. Classical pain starts periumbilically (visceral afferents T10) and migrates to right lower quadrant McBurney's point (somatic parietal peritoneal irritation). Evaluated by Alvarado Score (MANTRELS).",
                "clinical_pearls": "Rovsing's sign, Psoas sign (retrocecal appendix), and Obturator sign (pelvic appendix) are specific clinical physical maneuvers.",
                "classical_epistemic_note": "Recognized in Sushruta Samhita as Vidradhi (deep internal abscess requiring incision and drainage before bursting)."
            },
            {
                "key": "hemorrhagic_shock_damage_control",
                "title": "Trauma Resuscitation & Damage Control Laparotomy Protocol",
                "subspecialty": "Trauma & Critical Surgical Care",
                "citations": "Sabiston Ch. 16 (Trauma Management); Schwartz Ch. 7; Bailey & Love Ch. 24",
                "high_yield_summary": "Damage control surgery prioritizes physiological stabilization over anatomical reconstruction in patients exhibiting the lethal triad (hypothermia, coagulopathy, metabolic acidosis). Consists of rapid laparotomy for hemorrhage control (packing, shunting) and contamination containment, temporary abdominal closure (vacuum-assisted), intensive care resuscitation, and scheduled take-back for definitive repair 24-48 hours later.",
                "clinical_pearls": "Balanced blood product resuscitation uses a 1:1:1 ratio of packed red blood cells, fresh frozen plasma, and platelets to prevent dilutional coagulopathy.",
                "classical_epistemic_note": "Abulcasis (Al-Zahrawi) established primary principles of arterial ligatures, cautery hemostasis, and abdominal packing in Chapter 30 of Kitab al-Tasrif."
            }
        ]
    },
    {
        "id": "pediatrics",
        "name": "Pediatrics & Neonatal Medicine",
        "short_name": "Pediatrics",
        "category": "Clinical Medical Specialties",
        "canonical_textbooks": [
            "Nelson Textbook of Pediatrics (Robert M. Kliegman, Joseph St. Geme, 21st Edition, Elsevier)",
            "Ghai Essential Pediatrics (Vinod K. Paul, Arvind Bagga, 9th Edition, CBS Publishers)"
        ],
        "classical_traditional_parallels": {
            "unani": "Amraz-e-Atfal (امراض اطفال) - Al-Qanun fi al-Tibb Book I (Neonatal care, breast milk analysis, and infant disorders)",
            "ayurveda": "Kaumarbhritya (कौमारभृत्य) - Kashyapa Samhita (Dedicated pediatric treatise) & Charaka Samhita"
        },
        "icon": "fa-baby",
        "accent_color": "sky",
        "description": "Developmental milestones, congenital malformations, neonatal intensive care, pediatric infectious diseases, pediatric fluid resuscitation, and inborn errors of metabolism.",
        "canonical_topics": [
            {
                "key": "neonatal_jaundice",
                "title": "Neonatal Hyperbilirubinemia & Kernicterus Neurotoxicity",
                "subspecialty": "Neonatology & Perinatal Medicine",
                "citations": "Nelson Textbook of Pediatrics 21st Ed, Ch. 123 (Digestive System Disorders); Ghai 9th Ed, Ch. 9",
                "high_yield_summary": "Physiological jaundice arises due to increased RBC turnover, immature hepatic glucuronosyltransferase (UGT1A1), and enhanced enterohepatic circulation. Pathological jaundice presents within first 24 hours of life, rate of rise > 5 mg/dL/day, or total serum bilirubin > 95th percentile on Bhutani hour-specific nomogram. Unconjugated bilirubin crosses blood-brain barrier, depositing in basal ganglia (globus pallidus) and subthalamic nuclei, causing acute bilirubin encephalopathy and permanent choreoathetoid cerebral palsy.",
                "clinical_pearls": "Phototherapy converts toxic lipophilic unconjugated bilirubin into water-soluble photoisomers (lumirubin) excreted in bile and urine without glucuronidation.",
                "classical_epistemic_note": "Detailed by Avicenna as Yarqan-e-Wiladi (Infantile Jaundice) requiring gentle hydration and maternal dietary temperament modification."
            },
            {
                "key": "pediatric_dehydration_fluid",
                "title": "Pediatric Dehydration Assessment & Holliday-Segar Maintenance",
                "subspecialty": "Pediatric Critical Care & Gastroenterology",
                "citations": "Nelson Ch. 65 (Fluid and Electrolyte Disorders); Ghai Ch. 12 (Diarrheal Diseases)",
                "high_yield_summary": "Holliday-Segar method for 24-hour maintenance fluid calculation: 100 mL/kg for first 10 kg, 50 mL/kg for next 10 kg (11-20 kg), and 20 mL/kg for each kg above 20 kg. Severe dehydration (>10% volume deficit) manifests with sunken fontanelle, absent tears, prolonged capillary refill (>3s), tenting skin turgor, and lethargy. Requires rapid IV bolus of 20 mL/kg isotonic crystalloid (0.9% Normal Saline or Ringer's Lactate).",
                "clinical_pearls": "WHO Low-Osmolarity Oral Rehydration Solution (ORS, osmolarity 245 mOsm/L) harnesses sodium-glucose cotransporter (SGLT1) intact kinetics to drive water absorption.",
                "classical_epistemic_note": "Directly mirrors ancient Ayurvedic principle of Trishna & Shosha requiring Shadanga Paniya (six-herb electrolyte decoction) for mucosal rehydration."
            }
        ]
    },
    {
        "id": "dermatology",
        "name": "Dermatology & Cutaneous Medicine",
        "short_name": "Dermatology",
        "category": "Clinical Medical Specialties",
        "canonical_textbooks": [
            "Fitzpatrick's Dermatology in General Medicine (Kang, Amagai, Bruckner, Enk, Margolis, McMichael, Orringer, 9th Edition, McGraw-Hill)",
            "Rook's Textbook of Dermatology (Christopher Griffiths, Jonathan Barker, Tanya Bleiker et al., 9th Edition, Wiley-Blackwell)"
        ],
        "classical_traditional_parallels": {
            "unani": "Amraz-e-Jild (امراض جلد) - Jarb (Scabies), Bahaq (Vitiligo/Tinea), Quba (Ringworm), and Hazaz (Alopecia)",
            "ayurveda": "Kushta Roga (कुष्ठ रोग) & Twak Vikara - Maha Kushta (7 Major Dermatoses) and Kshudra Kushta (11 Minor Dermatoses)"
        },
        "icon": "fa-hand-dots",
        "accent_color": "purple",
        "description": "Cutaneous morphometry, primary and secondary lesion semiology, immunodermatology, dermato-pathology correlations, skin barrier dysfunction, and biologic therapies.",
        "canonical_topics": [
            {
                "key": "psoriasis_vulgaris",
                "title": "Psoriasis Vulgaris Immunopathogenesis & Biologic Targets",
                "subspecialty": "Immunodermatology & Papulosquamous Disorders",
                "citations": "Fitzpatrick's 9th Ed, Ch. 28 (Psoriasis); Rook's 9th Ed, Ch. 35",
                "high_yield_summary": "Immune-mediated inflammatory dermatosis characterized by well-demarcated erythematous plaques covered with silvery-white micaceous scales, most common on extensor surfaces (knees, elbows, scalp). Pathophysiology involves the IL-23/IL-17 cytokine axis: dendritic cells secrete IL-23, stimulating Th17 lymphocytes to produce IL-17A, IL-17F, and IL-22, driving profound keratinocyte hyperproliferation and parakeratosis. Demonstrates Auspitz sign and Koebner phenomenon.",
                "clinical_pearls": "Targeted biologic inhibitors of TNF-alpha (Adalimumab), IL-17A (Secukinumab), and IL-23 p19 (Guselkumab) achieve PASI 90/100 skin clearance.",
                "classical_epistemic_note": "Corresponds to Unani 'Qashf-e-Jild' (Epidermal Scaling) and Ayurvedic 'Kitibha Kushta' (black, rough, scaly lesions from Vata-Kapha vitiation)."
            },
            {
                "key": "malignant_melanoma",
                "title": "Cutaneous Melanoma ABCDE Criteria & Breslow Tumor Thickness",
                "subspecialty": "Dermatologic Oncology",
                "citations": "Fitzpatrick's Ch. 129 (Melanoma); Rook's Ch. 136",
                "high_yield_summary": "Malignant neoplasm of melanocytes originating primarily from epidermis. Screened via ABCDE criteria: Asymmetry, Border irregularity, Color variegation, Diameter > 6 mm, Evolving morphology. Staging and prognosis are dictated by Breslow tumor depth (vertical thickness in mm from stratum granulosum to deepest infiltrative tumor cell) and presence of ulceration.",
                "clinical_pearls": "Sentinel lymph node biopsy is indicated for clinical stage T1b melanomas (Breslow depth 0.8-1.0 mm with ulceration or > 1.0 mm). BRAF V600E mutations respond to Dabrafenib + Trametinib combination therapy.",
                "classical_epistemic_note": "Described as Khal-e-Aswad Khabees (Malignant Black Mole / Atrabilious Tumor) in classical Unani surgical texts by Al-Majusi."
            }
        ]
    },
    {
        "id": "psm_public_health",
        "name": "Preventive & Social Medicine (PSM) / Public Health",
        "short_name": "PSM & Public Health",
        "category": "Population Health & Preventive Medicine",
        "canonical_textbooks": [
            "Park's Textbook of Preventive and Social Medicine (K. Park, 26th Edition, Banarsidas Bhanot Publishers)",
            "Maxcy-Rosenau-Last Public Health and Preventive Medicine (Robert B. Wallace et al., 16th Edition, McGraw-Hill)"
        ],
        "classical_traditional_parallels": {
            "unani": "Hifzan-e-Sehat (حفظان صحت) - Asbab Sitta Zarooriya (Six Essential Prerequisites of Health: Air, Food/Drink, Movement/Rest, Sleep, Excretion, Mental states)",
            "ayurveda": "Swasthavritta (स्वस्थवृत्त) - Dinacharya (Daily regimen), Ritucharya (Seasonal hygiene), and Janapadodhvamsa (Epidemic public health governance)"
        },
        "icon": "fa-users",
        "accent_color": "teal",
        "description": "Epidemiological surveillance metrics, study designs, biostatistics, biosecurity cold-chain protocols, national immunization schedules, health economics, and occupational hygiene.",
        "canonical_topics": [
            {
                "key": "epidemiology_study_designs",
                "title": "Epidemiological Study Designs, Relative Risk (RR) & Odds Ratio (OR)",
                "subspecialty": "Epidemiology & Biostatistics",
                "citations": "Park's PSM 26th Ed, Ch. 3 (Principles of Epidemiology and Epidemiologic Methods); Maxcy-Rosenau-Last 16th Ed, Ch. 2",
                "high_yield_summary": "Cohort studies follow exposed vs unexposed populations longitudinally to calculate Incidence and Relative Risk (RR = [a/(a+b)] / [c/(c+d)]); ideal for rare exposures. Case-Control studies work retrospectively from diseased vs non-diseased individuals to compute Odds Ratio (OR = ad/bc); ideal for rare diseases. Randomized Controlled Trials (RCTs) minimize confounding via double-blind allocation, providing highest causal validity.",
                "clinical_pearls": "Number Needed to Treat (NNT = 1 / Absolute Risk Reduction) provides essential clinical trial metric for real-world therapeutic effect size.",
                "classical_epistemic_note": "Correlates to Charaka Samhita's Janapadodhvamsa Vimana (Chapter 3 on communal epidemic devastation from environmental corruption of air, water, and soil)."
            },
            {
                "key": "cold_chain_vaccinology",
                "title": "Vaccine Cold Chain System & Expanded Programme on Immunization",
                "subspecialty": "Preventive Vaccinology & Public Health Operations",
                "citations": "Park's PSM Ch. 4 (Screening for Disease) & Ch. 5 (Epidemiology of Communicable Diseases)",
                "high_yield_summary": "Cold chain infrastructure ensures uninterrupted temperature control from manufacturer to vaccine administration. Most sensitive to heat: Oral Polio Vaccine (OPV), followed by Measles and Rotavirus (-20°C storage). Vaccines destroyed by freezing (Must NEVER be frozen): Hepatitis B, Pentavalent (DPT-HepB-Hib), Tetanus Toxoid, HPV (+2°C to +8°C storage). Verified via Shake Test and Vaccine Vial Monitor (VVM).",
                "clinical_pearls": "If inner square of Vaccine Vial Monitor matches or is darker than outer reference ring, the vaccine has sustained thermal breach and must be discarded.",
                "classical_epistemic_note": "Mirrors the ancient Unani canon of Hifz-e-Jawhar (Preservation of biological potency against ambient heat and putrefaction)."
            }
        ]
    },
    {
        "id": "radiology",
        "name": "Diagnostic Radiology & Medical Imaging",
        "short_name": "Radiology",
        "category": "Diagnostic Medical Specialties",
        "canonical_textbooks": [
            "Grainger & Allison's Diagnostic Radiology (Andy Adam, Adrian K. Dixon, Jonathan H. Gillard, 7th Edition, Elsevier)",
            "Brant and Helms' Fundamentals of Diagnostic Radiology (Clyde A. Helms et al., 5th Edition, Wolters Kluwer)"
        ],
        "classical_traditional_parallels": {
            "unani": "Al-Fahs al-Ayani (الفحص العياني) - Non-invasive morphological inspection and structural palpation",
            "ayurveda": "Darshana Pariksha (दर्शन परीक्षा) - Visual morphological diagnostic scrutiny (Ashtavidha Pariksha)"
        },
        "icon": "fa-x-ray",
        "accent_color": "blue",
        "description": "Multi-detector CT protocoling, high-field MRI pulse sequences (T1, T2, FLAIR, DWI, SWI), Doppler ultrasonography, PET-CT metabolic staging, and interventional radiological procedures.",
        "canonical_topics": [
            {
                "key": "acute_stroke_mri",
                "title": "Brain MRI Diffusion-Weighted Imaging (DWI/ADC) in Acute Infarction",
                "subspecialty": "Neuroradiology & Emergency Neuroimaging",
                "citations": "Grainger & Allison 7th Ed, Ch. 58 (Ischemic Stroke Imaging); Brant & Helms 5th Ed, Ch. 3",
                "high_yield_summary": "Diffusion-Weighted Imaging (DWI) detects restricted Brownian motion of extracellular water molecules within minutes of cerebral arterial occlusion due to cytotoxic edema (failure of Na+/K+ ATPase pump). Appears hyperintense on DWI with corresponding hypointensity on Apparent Diffusion Coefficient (ADC) map, ruling out T2 shine-through artifact. DWI/FLAIR mismatch identifies salvageable ischemic penumbra within thrombolysis time windows.",
                "clinical_pearls": "Non-contrast Head CT is immediate first-line study in acute stroke not to diagnose infarction, but to exclude intracerebral hemorrhage prior to IV thrombolytic administration.",
                "classical_epistemic_note": "Modern radiographic imaging validates classical Unani Sakta (Apoplexy / Stroke) arising from sudden circulatory occlusion of the brain ventricles."
            },
            {
                "key": "chest_ct_interstitial_lung",
                "title": "High-Resolution Chest CT (HRCT) Patterns: Ground Glass vs Fibrosis",
                "subspecialty": "Thoracic Radiology & Pulmonology",
                "citations": "Brant & Helms Ch. 18 (Diffuse Lung Disease); Grainger & Allison Ch. 14",
                "high_yield_summary": "HRCT uses thin slices (1-1.5 mm) with high spatial frequency algorithms to evaluate secondary pulmonary lobules. Ground-Glass Opacity (GGO) denotes hazy increased lung attenuation preserving bronchial and vascular margins, reflecting active alveolar inflammation or partial filling. Honeycombing (clustered subpleural cystic airspaces with thickened fibrous walls) with traction bronchiectasis defines the definitive Usual Interstitial Pneumonia (UIP) pattern of Idiopathic Pulmonary Fibrosis.",
                "clinical_pearls": "Crazy-paving pattern (GGO superimposed on interlobular septal thickening) indicates Pulmonary Alveolar Proteinosis, severe COVID-19 pneumonia, or pulmonary edema.",
                "classical_epistemic_note": "Direct structural imaging correlate to chronic Unani Sil wa Diq (Pulmonary Phthisis / Fibrotic parenchymal destruction)."
            }
        ]
    },
    {
        "id": "obgyn",
        "name": "Obstetrics & Gynecology (OB/GYN)",
        "short_name": "Obstetrics & Gynecology",
        "category": "Clinical Medical Specialties",
        "canonical_textbooks": [
            "Williams Obstetrics (F. Gary Cunningham, Kenneth J. Leveno et al., 26th Edition, McGraw-Hill)",
            "DC Dutta's Textbook of Obstetrics (Hiralal Konar, 9th Edition, Jaypee Brothers)",
            "Shaw's Textbook of Gynaecology (V.G. Padubidri, Shirish N. Daftary, 17th Edition, Elsevier)"
        ],
        "classical_traditional_parallels": {
            "unani": "Amraz-e-Niswan wa Wiladat (امراض نسوان وولادت) - Al-Qanun fi al-Tibb Book III (Uterine disorders, labor management, and puerperium)",
            "ayurveda": "Prasuti Tantra & Stri Roga (प्रसूति तंत्र एवं स्त्री रोग) - Kashyapa Samhita & Charaka Samhita Sharirasthana"
        },
        "icon": "fa-person-pregnant",
        "accent_color": "fuchsia",
        "description": "Fetal-maternal medicine, stages of labor, high-risk obstetric emergencies, gynecologic endocrinology, oncogynecology, and pelvic floor reconstructive surgery.",
        "canonical_topics": [
            {
                "key": "preeclampsia_eclampsia",
                "title": "Preeclampsia Pathophysiology, HELLP Syndrome & Magnesium Sulfate",
                "subspecialty": "Maternal-Fetal Medicine & Obstetric Emergencies",
                "citations": "Williams Obstetrics 26th Ed, Ch. 34 (Hypertensive Disorders); DC Dutta 9th Ed, Ch. 17",
                "high_yield_summary": "Systemic gestational disorder initiated by defective trophoblast invasion of maternal spiral arteries, leading to high-resistance placental hypoperfusion, oxidative stress, and release of anti-angiogenic factors (sFlt-1 and soluble endoglin). Circulating factors bind VEGF and PlGF, inducing widespread maternal endothelial dysfunction, hypertension (BP >= 140/90 after 20 weeks), and proteinuria or end-organ damage. Severe features include HELLP syndrome (Hemolysis, Elevated Liver enzymes, Low Platelets).",
                "clinical_pearls": "Magnesium sulfate (Zuspan or Pritchard regimen) is drug of choice for eclamptic seizure prophylaxis; monitored via patellar tendon reflex, respiratory rate (>12/min), and urine output.",
                "classical_epistemic_note": "Documented in traditional Unani texts as Ikhtinaq-e-Reham (Puerperal Spasm / Eclamptic Convulsions) requiring immediate uterine evacuation."
            },
            {
                "key": "postpartum_hemorrhage",
                "title": "Postpartum Hemorrhage (PPH) 4T Etiology & Active Management",
                "subspecialty": "Labor & Delivery Emergency Care",
                "citations": "Williams Obstetrics Ch. 41 (Obstetrical Hemorrhage); DC Dutta Ch. 29",
                "high_yield_summary": "Cumulative blood loss >= 1000 mL or blood loss accompanied by signs of hypovolemia within 24 hours of birth. Mnemonic 4Ts: Tone (Uterine Atony, 70-80%), Trauma (lacerations, hematomas), Tissue (retained placenta/cotyledons), Thrombin (coagulopathies). Active Management of Third Stage of Labor (AMTSL) includes prophylactic oxytocin (10 IU IM), controlled cord traction, and uterine massage, reducing PPH risk by 60%.",
                "clinical_pearls": "Refractory uterine atony protocol advances from bimanual compression to pharmacotherapy (Oxytocin, Ergometrine, Carboprost PGF2a, Misoprostol), intrauterine balloon tamponade (Bakri balloon), and B-Lynch uterine compression sutures.",
                "classical_epistemic_note": "Corresponds to Nazf al-Dam Ba'd al-Wilada (Fatal Postpartum Hemorrhage) detailed in Ibn al-Quff's Kitab al-Umdah fi al-Jarahat."
            }
        ]
    },
    {
        "id": "microbiology",
        "name": "Microbiology & Infectious Diseases",
        "short_name": "Microbiology",
        "category": "Basic & Clinical Medical Sciences",
        "canonical_textbooks": [
            "Mandell, Douglas, and Bennett's Principles and Practice of Infectious Diseases (John E. Bennett et al., 9th Edition, Elsevier)",
            "Jawetz, Melnick & Adelberg's Medical Microbiology (Stefan Riedel et al., 28th Edition, McGraw-Hill)",
            "Ananthanarayan and Paniker's Textbook of Microbiology (Reba Kanungo, 12th Edition, Universities Press)"
        ],
        "classical_traditional_parallels": {
            "unani": "Ilm al-Jarasim wa al-Taffun (علم الجراثیم) - Avicenna's Postulation of Contagious Seed Particles (Miasma & Taffuni Agents)",
            "ayurveda": "Krimi Roga & Sankramika Roga (कृमि रोग) - Sushruta Samhita Nidanasthana Ch. 5 (Contact, Inhalation, and Parasitic transmission)"
        },
        "icon": "fa-virus-covid",
        "accent_color": "emerald",
        "description": "Bacteriology, virology, medical mycology, parasitology, antimicrobial resistance surveillance (ESBL, CRE, MRSA), and hospital-acquired infection epidemiology.",
        "canonical_topics": [
            {
                "key": "antimicrobial_resistance_mechanisms",
                "title": "Bacterial Beta-Lactamases, MRSA (mecA) & Carbapenemase (CRE) Genetics",
                "subspecialty": "Antimicrobial Resistance & Molecular Bacteriology",
                "citations": "Mandell, Douglas, and Bennett 9th Ed, Ch. 21 (Mechanisms of Antibiotic Resistance); Jawetz 28th Ed, Ch. 28; Ananthanarayan 12th Ed, Ch. 10",
                "high_yield_summary": "Bacteria confer resistance via 4 primary mechanisms: Enzymatic drug inactivation (Beta-lactamases, aminoglycoside acetyltransferases), target modification (PBP2a encoded by mecA gene in MRSA, vanA D-Ala-D-Lac in VRE), efflux pumps (MexAB-OprM in Pseudomonas), and reduced outer membrane porin permeability (OprD loss in Carbapenem-resistant Enterobacteriaceae / CRE). NDM-1 metallo-beta-lactamases hydrolyze carbapenems and resist clavulanate/tazobactam.",
                "clinical_pearls": "MRSA strains resist all traditional beta-lactams including carbapenems because PBP2a has low binding affinity for beta-lactams; Ceftaroline (5th gen) is sole beta-lactam with PBP2a affinity.",
                "classical_epistemic_note": "Reflects the ancient Unani concept of 'Fasad-e-Taffuni' (Refractory Putrefaction resistant to standard balsamic antiseptics)."
            },
            {
                "key": "tuberculosis_pathogenesis",
                "title": "Mycobacterium tuberculosis Granuloma Immunology & GeneXpert Diagnostics",
                "subspecialty": "Mycobacteriology & Global Infectious Disease",
                "citations": "Jawetz Ch. 23 (Mycobacteria); Mandell Ch. 249 (Tuberculosis); Ananthanarayan Ch. 34",
                "high_yield_summary": "Obligate aerobe with mycolic acid lipid-rich cell wall rendering it acid-fast (Ziehl-Neelsen stain positive). Inhaled into alveoli, engulfed by alveolar macrophages, where it prevents phagolysosome fusion via cord factor and sulfatides. Cell-mediated immunity develops 2-3 weeks post-infection: CD4+ Th1 cells release IFN-gamma, activating macrophages into caseating epithelioid granulomas (Ghon focus + regional lymph node = Ghon complex).",
                "clinical_pearls": "GeneXpert MTB/RIF is automated real-time PCR assay providing simultaneous detection of Mycobacterium tuberculosis and rifampicin resistance (rpoB gene mutation) within 2 hours.",
                "classical_epistemic_note": "Described with clinical precision in Avicenna's Canon as 'Dill' (Pulmonary Tuberculosis) recognized as contagious through shared breath and airborne dust."
            }
        ]
    },
    {
        "id": "biochemistry_genetics",
        "name": "Medical Biochemistry & Clinical Genetics",
        "short_name": "Biochemistry",
        "category": "Basic Medical Sciences",
        "canonical_textbooks": [
            "Harper's Illustrated Biochemistry (Victor W. Rodwell, David A. Bender et al., 32nd Edition, McGraw-Hill)",
            "Lehninger Principles of Biochemistry (David L. Nelson, Michael M. Cox, 8th Edition, Macmillan Learning)"
        ],
        "classical_traditional_parallels": {
            "unani": "Ilm al-Kimya al-Hayawiya - Hazm-e-Awwal to Hazm-e-Rabi (Four Phases of Digestion & Macromolecular Transformation)",
            "ayurveda": "Dhatu Parinama (धातु परिणाम) - Rasa-Rakta-Mamsa-Meda-Asthi-Majja-Shukra Sequential Tissue Transformation Metabolism"
        },
        "icon": "fa-dna",
        "accent_color": "violet",
        "description": "Enzyme kinetics, metabolic pathways (glycolysis, TCA, beta-oxidation), molecular genetics, inborn errors of metabolism, epigenetic regulation, and recombinant DNA technology.",
        "canonical_topics": [
            {
                "key": "oxidative_phosphorylation_etc",
                "title": "Mitochondrial Electron Transport Chain & ATP Synthase Kinetics",
                "subspecialty": "Cellular Bioenergetics & Metabolic Biochemistry",
                "citations": "Lehninger 8th Ed, Ch. 19 (Oxidative Phosphorylation); Harper's 32nd Ed, Ch. 13",
                "high_yield_summary": "Electrons from NADH and FADH2 traverse mitochondrial inner membrane complexes I-IV (NADH dehydrogenase, Succinate dehydrogenase, Coenzyme Q-cytochrome c reductase, Cytochrome c oxidase). Proton pumping across inner membrane generates electrochemical proton motive gradient (delta-pH and electrical potential). Influx of protons through FoF1-ATP synthase rotor drives phosphorylation of ADP to ATP (chemiosmotic coupling).",
                "clinical_pearls": "Carbon monoxide and Cyanide inhibit Complex IV (Cytochrome c oxidase), blocking ATP synthesis and causing lactic acidosis; 2,4-Dinitrophenol (DNP) uncouples proton gradient, generating lethal hyperthermia without ATP synthesis.",
                "classical_epistemic_note": "Biochemical molecular foundation of Unani 'Hararat Ghariziya' (Innate Metabolic Heat) and Ayurvedic 'Jatharagni & Dhatvagni' (Cellular Transformation Fires)."
            },
            {
                "key": "inborn_errors_phenylketonuria",
                "title": "Phenylketonuria (PKU) & Inborn Errors of Amino Acid Metabolism",
                "subspecialty": "Clinical Genetics & Biochemical Inborn Errors",
                "citations": "Harper's Ch. 29 (Catabolism of Proteins and Amino Acids); Lehninger Ch. 18",
                "high_yield_summary": "Autosomal recessive deficiency of hepatic phenylalanine hydroxylase (PAH) or its cofactor tetrahydrobiopterin (BH4). Impairs conversion of phenylalanine to tyrosine, causing neurotoxic phenylalanine accumulation and shunting into phenylketones (phenylacetate, phenylpyruvate) excreted in urine (mousy/musty odor). Manifests with severe intellectual disability, microcephaly, seizures, hypopigmentation (tyrosine is melanin precursor), and eczema.",
                "clinical_pearls": "Neonatal Guthrie bacterial inhibition test or tandem mass spectrometry permits early dietary phenylalanine restriction (medical formula), preventing cognitive decrement.",
                "classical_epistemic_note": "Manifests modern chromosomal substrate of inherited congenital diatheses (Mizaj-e-Khilqi) documented in ancient constitutional treatises."
            }
        ]
    },
    {
        "id": "forensic_toxicology",
        "name": "Forensic Medicine & Clinical Toxicology",
        "short_name": "Forensic Medicine",
        "category": "Diagnostic & Medico-Legal Sciences",
        "canonical_textbooks": [
            "Goldfrank's Toxicologic Emergencies (Lewis S. Nelson, Mary Ann Howland et al., 11th Edition, McGraw-Hill)",
            "Parikh's Textbook of Medical Jurisprudence, Forensic Medicine and Toxicology (C.K. Parikh, 8th Edition, CBS Publishers)",
            "The Essentials of Forensic Medicine and Toxicology (K.S. Narayan Reddy, O.P. Murty, 35th Edition, Jaypee Brothers)"
        ],
        "classical_traditional_parallels": {
            "unani": "Ilm al-Sumoom (علم السموم) - Maimonides' Treatise on Poisons and Their Antidotes (1198 CE) & Ibn Sina's Kitab al-Sumoom",
            "ayurveda": "Agada Tantra (अगद तंत्र) - Sushruta Samhita Kalpasthana (Dedicated toxicological branch: Visha, Upavisha, and Keeta Visha antidotes)"
        },
        "icon": "fa-scale-balanced",
        "accent_color": "slate",
        "description": "Medico-legal jurisprudence, clinical toxidromes, specific antidotes, post-mortem thanatology, wound ballistics, DNA fingerprinting, and 21 CFR Part 11 electronic legal evidentiary integrity.",
        "canonical_topics": [
            {
                "key": "acute_poisoning_toxidromes",
                "title": "Clinical Toxidromes: Cholinergic, Anticholinergic, Opioid & Sympathomimetic",
                "subspecialty": "Emergency Toxicology & Critical Care",
                "citations": "Goldfrank's Toxicologic Emergencies 11th Ed, Ch. 17 (Initial Evaluation of the Poisoned Patient); Parikh's 8th Ed, Ch. 22",
                "high_yield_summary": "Constellations of vital sign and physical exam findings diagnostic of toxicological classes. Cholinergic (Organophosphates): DUMBELS (Diarrhea, Urination, Miosis, Bradycardia/Bronchorrhea, Emesis, Lacrimation, Salivation) treated with Atropine + Pralidoxime. Anticholinergic (Atropine, Datura): Hyperthermia, dry skin, mydriasis, delirium, urinary retention ('Blind as a bat, mad as a hatter, red as a beet, hot as a hare, dry as a bone') treated with Physostigmine. Opioid: Coma, pinpoint pupils, respiratory depression treated with Naloxone.",
                "clinical_pearls": "Distinguishing Sympathomimetic (Cocaine, Amphetamines) from Anticholinergic: Sympathomimetic patients present with profuse diaphoresis, while anticholinergic patients have warm, dry, anhidrotic skin.",
                "classical_epistemic_note": "Directly matches Sushruta Samhita Kalpasthana's Sthavara Visha classifications and Avicenna's poison syndromes in Ilm al-Sumoom."
            },
            {
                "key": "thanatology_postmortem_interval",
                "title": "Thanatology, Post-Mortem Interval (PMI) & Algor/Rigor/Livor Mortis",
                "subspecialty": "Forensic Thanatology & Medical Jurisprudence",
                "citations": "Reddy's Essentials of Forensic Medicine 35th Ed, Ch. 5 (Postmortem Changes); Parikh's Ch. 5",
                "high_yield_summary": "Algor Mortis (cooling of body post-mortem, ~1.5°F/hour under temperate conditions via Glaister equation). Livor Mortis (post-mortem hypostasis/lividity): reddish-purple capillary pooling, appears 1-2 hours, fixes by 6-8 hours (does not blanch with thumb pressure). Rigor Mortis (post-mortem muscular rigidity due to ATP depletion preventing actin-myosin detachment): starts in small involuntary muscles of face/jaw (Nysten's law) at 1-2 hours, spreads to whole body by 12 hours, persists 12-24 hours, vanishes by 36 hours as autolysis commences.",
                "clinical_pearls": "Cherry-red post-mortem lividity indicates Carbon Monoxide poisoning or Cyanide; chocolate-brown lividity denotes methemoglobinemia (Nitrites, Chlorates).",
                "classical_epistemic_note": "Correlates with classical Islamic medico-legal coroner jurisprudence (Al-Tibb al-Shar'i) regarding irreversible cessation of Ruh Haiwani (vital respiratory/circulatory spirit)."
            }
        ]
    }
]


class MedicalDisciplinesBulkLoader:
    """
    In-memory catalog provider for the 14 foundational medical disciplines and textbooks.
    """

    @classmethod
    def get_all_disciplines(cls) -> List[Dict[str, Any]]:
        return CANONICAL_MEDICAL_DISCIPLINES

    @classmethod
    def find_discipline_by_id(cls, disc_id: str) -> Optional[Dict[str, Any]]:
        disc_id_norm = disc_id.lower().replace("-", "_").strip()
        for disc in CANONICAL_MEDICAL_DISCIPLINES:
            if disc["id"] == disc_id_norm or disc_id_norm in disc["short_name"].lower() or disc_id_norm in disc["name"].lower():
                return disc
        return None

    @classmethod
    def search_discipline_topics(cls, query: str) -> List[Dict[str, Any]]:
        import re
        q = query.lower().strip()
        generic_stopwords = {"medical", "medicine", "clinical", "textbook", "textbooks", "principles", "guide", "essential", "practice"}
        tokens = [w.strip() for w in re.split(r'[\s,;:()\-_/]+', q) if len(w.strip()) >= 3 and w.strip() not in generic_stopwords]
        
        scored_matches = []
        for disc in CANONICAL_MEDICAL_DISCIPLINES:
            score = 0
            # Direct discipline name check
            if q in disc["name"].lower() or q in disc["short_name"].lower():
                score += 50
            for t in tokens:
                if t in disc["short_name"].lower():
                    score += 30
                elif t in disc["name"].lower():
                    score += 20

            # Textbook check
            for tb in disc["canonical_textbooks"]:
                tb_lower = tb.lower()
                if q in tb_lower:
                    score += 60
                for t in tokens:
                    if t in tb_lower:
                        score += 25

            # Topics check
            matched_topics = []
            for topic in disc["canonical_topics"]:
                text_blob = " ".join([
                    topic["title"],
                    topic["subspecialty"],
                    topic["high_yield_summary"],
                    topic["clinical_pearls"],
                    topic["citations"],
                    topic["classical_epistemic_note"]
                ]).lower()

                topic_score = 0
                if q in text_blob:
                    topic_score += 40
                for t in tokens:
                    if t in topic["title"].lower():
                        topic_score += 20
                    elif t in text_blob:
                        topic_score += 5

                if topic_score > 0:
                    score += topic_score
                    matched_topics.append((topic_score, topic))

            if score > 0:
                matched_topics.sort(key=lambda x: x[0], reverse=True)
                filtered_topics = [t[1] for t in matched_topics] if matched_topics else disc["canonical_topics"]
                scored_matches.append((score, {
                    "discipline": disc["name"],
                    "short_name": disc["short_name"],
                    "category": disc["category"],
                    "icon": disc["icon"],
                    "canonical_textbooks": disc["canonical_textbooks"],
                    "matched_topics": filtered_topics
                }))

        scored_matches.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in scored_matches]
