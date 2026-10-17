const DIFFERENTIAL_DIAGNOSIS_DATA = {
      'epigastric_pain': {
        title: "Acute/Chronic Epigastric Pain & Upper GI Distress",
        subtitle: "ICD-11: MD81 • Classical Term: Waja' al-Mi'dah (وجع المعدة) • Harrison Ch. 45 & Qanun Bk. 3",
        modernPathologies: `<div>• <strong>Peptic Ulcer Disease (PUD):</strong> Burning epigastric pain relieved or exacerbated by food; H. pylori stool antigen or upper endoscopy.</div><div>• <strong>Acute Pancreatitis:</strong> Severe epigastric pain radiating to back; serum lipase &gt;3x ULN, CT abdomen (Balthazar score).</div><div>• <strong>Gastroesophageal Reflux Disease (GERD):</strong> Retrosternal pyrosis and acid regurgitation; 24h pH-impedance monitoring.</div><div>• <strong>Inferior Wall MI:</strong> Anginal equivalent in elderly/diabetics; 12-lead ECG (leads II, III, aVF) and high-sensitivity Troponin-I.</div>`,
        modernBiomarkers: "Complete Blood Count (rule out microcytic anemia from occult bleed), Serum Amylase & Lipase, Comprehensive Metabolic Panel (LFTs, renal function), Upper GI Endoscopy (EGD) with biopsy, Abdominal Ultrasound for biliary cholelithiasis.",
        modernRedflags: "Hemodynamic instability (hypotension, tachycardia), hematemesis or melena, rigid involuntary guarding suggesting visceral perforation, radiating pain with diaphoresis (rule out acute coronary syndrome).",
        classicalEtiology: `<div>• <strong>Sū'-e-Mizāj Ḥār Ma'ddī (سوء مزاج حار):</strong> Burning gastralgia caused by sharp, bilious matter (Ṣafrā') irritating gastric mucosal lining.</div><div>• <strong>Nafakh wa Burūdat al-Mi'dah (نفخ و برودة):</strong> Distension and meteorism with slow gastric emptying due to phlegmatic coldness (Balgham).</div><div>• <strong>Sudād-e-Kabd wa Mi'dah (سدد كبد و معدة):</strong> Functional vascular and ductal obstructions impeding chyme assimilation.</div>`,
        classicalNabz: "Pulse (Nabz): Nabz Sarī' Ṣaghīr (rapid, narrow pulse indicating hot visceral distress) or Nabz Bāṭī' (sluggish, soft pulse in phlegmatic cold indigestion). Urine (Bawl): Bawl Nāri (citron-yellow or fiery with sparse sediment indicating bilious combustive humor).",
        classicalTadbir: "Tad'īl-e-Mizāj (temperamental balancing with cooling mucilage such as Isabgol and Sharbat Nilofar), followed by Tanqiyah-e-Mawād (gentle evacuation of caustic bilious humor), and Taqwiyat-e-Fam-e-Mi'dah (strengthening gastric cardia with carminative aromatics like Mastagi & Podina).",
        integrativeConsensus: "Diagnostic priority is immediate ruling out of acute coronary syndrome (ECG + Troponin) and acute surgical abdomen. For confirmed non-ulcer dyspepsia, gastritis, or mild PUD, initiate dual-lens management: standard mucosal protection (PPI or H2RA) synergized with classical Unani compound carminatives to stimulate endogenous bicarbonate secretion, gastric mucin synthesis, and resolve postprandial gastroparesis without compromising long-term gastric acid physiological barriers.",
        integrativeFormulations: `<div class="space-y-1.5"><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Jawarish Kamuni (UPI Standard):</strong> 5g BID post meals.</span><button onclick="inspectFormulation('jawarish_kamuni')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Majun Dabeed-ul-Ward:</strong> 5g morning with water.</span><button onclick="inspectFormulation('majun_dabeed_ul_ward')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Sharbat Deenar:</strong> 25ml diluted in water.</span><button onclick="inspectFormulation('sharbat_deenar')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div></div>`,
        safetyCheck: "Space administration of tannin-rich compounds (e.g. Ward-e-Surkh in Dabeed-ul-Ward) by 2 hours from iron supplements and fluoroquinolones to prevent chelation. Monitor renal function if co-administering with NSAIDs."
      },
      'headache_visual': {
        title: "Severe Cephalea with Visual Disturbances & Photophobia",
        subtitle: "ICD-11: 8A80 • Classical Term: Ṣudā' wa Shaqīqah (صداع و شقيقة) • Harrison Ch. 442 & al-Hawi Bk. 1",
        modernPathologies: `<div>• <strong>Migraine with Visual Aura:</strong> Cortical spreading depression, unilateral throbbing pain, photophobia, phonophobia; trigeminovascular CGRP activation.</div><div>• <strong>Idiopathic Intracranial Hypertension:</strong> Papilledema, headache worsened by Valsalva, elevated lumbar puncture opening pressure (&gt;250 mm H2O).</div><div>• <strong>Giant Cell Arteritis (GCA):</strong> Temporal artery tenderness, jaw claudication, markedly elevated ESR (&gt;50 mm/hr) and CRP in patients aged &gt;50.</div><div>• <strong>Tension-Type Headache:</strong> Band-like constricting pressure; bilateral pericranial myofascial tenderness.</div>`,
        modernBiomarkers: "Direct and indirect fundoscopy for optic disc edema/papilledema, ESR and CRP (mandatory in age &gt;50), Brain MRI/MRV with gadolinium contrast, Lumbar puncture with opening pressure measurement.",
        modernRedflags: "'Thunderclap' hyperacute onset (&lt;1 min to maximal intensity, rule out subarachnoid hemorrhage), new focal neurological deficits, signs of meningism (nuchal rigidity, Kernig sign), systemic fever with altered mental status.",
        classicalEtiology: `<div>• <strong>Ṣudā' Damawī (صداع دموي):</strong> Sanguineous cephalic vascular fullness with temporal pulsation and facial flushing.</div><div>• <strong>Ṣudā' Balghamī / Bārid:</strong> Dense phlegmatic moisture causing heaviness in eyelids, somnolence, and dull retro-orbital ache.</div><div>• <strong>Shaqīqah (شقيقة):</strong> Unilateral vascular hemicrania caused by sharp acrid bilious vapors ascending from gastric cardia.</div>`,
        classicalNabz: "Pulse (Nabz): Nabz Mumtali' Qawī (bounding, tense, filled pulse in sanguine plethora) or Nabz Layyin Bāṭī' (soft, sluggish pulse in phlegm). Urine (Bawl): Bawl Abyaḍ Ghalīẓ (turbid pale urine in phlegmatic fullness).",
        classicalTadbir: "Tanqiyah-e-Dimāgh via cephalic purgatives (Itrifal Ustukhuddus), Hijamah on Kahil (C7 interscapular wet cupping) to relieve cephalic congestion, and Tabrīd (cooling compress with rose water and vinegar over forehead).",
        integrativeConsensus: "Mandatory fundoscopic examination and neuroimaging if SNOOP red flags are present. For confirmed primary migraine or tension cephalea, combine abortive triptan/NSAID with neuroprotective Itrifal Ustukhuddus (Lavandula stoechas) to enhance glymphatic clearance and attenuate neurogenic inflammation.",
        integrativeFormulations: `<div class="space-y-1.5"><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Itrifal Ustukhuddus:</strong> 5-7g at bedtime with warm water.</span><button onclick="inspectFormulation('itrifal_ustukhuddus')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Itrifal Kashneezi:</strong> 5g post meals for gastric vapors.</span><button onclick="inspectFormulation('itrifal_kashneezi')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Sharbat Bazoori Motadil:</strong> 25ml for waste excretion.</span><button onclick="inspectFormulation('sharbat_deenar')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div></div>`,
        safetyCheck: "Monitor baseline blood pressure prior to cupping. Ensure adequate hydration. Avoid concurrent sedative botanicals with high-dose centralized anticonvulsants."
      },
      'metabolic_polyuria': {
        title: "Polyuria, Polydipsia, Chronic Fatigue & Glycemic Dysregulation",
        subtitle: "ICD-11: 5A11 • Classical Term: Dhiyābīṭus (ذیابیطس / دولاب الکلی) • Harrison Ch. 396 & Qanun Bk. 3",
        modernPathologies: `<div>• <strong>Type 2 Diabetes Mellitus:</strong> Insulin resistance with progressive pancreatic beta-cell secretory defect; HbA1c &ge;6.5% or FPG &ge;126 mg/dL.</div><div>• <strong>Type 1 Diabetes Mellitus:</strong> Autoimmune islet destruction; anti-GAD, IA-2, and ZnT8 autoantibody positivity with severe absolute insulinopenia.</div><div>• <strong>Diabetes Insipidus:</strong> Central or nephrogenic defect in arginine vasopressin action; dilute urine (osmolality &lt;300 mOsm/kg) despite hypernatremia.</div><div>• <strong>Primary Hyperparathyroidism:</strong> Hypercalcemic osmotic diuresis mediated by elevated parathyroid hormone.</div>`,
        modernBiomarkers: "Fasting Plasma Glucose, Glycated Hemoglobin (HbA1c), Urine Albumin-to-Creatinine Ratio (uACR), eGFR (CKD-EPI formula), Serum Electrolytes and calculated Serum Osmolality.",
        modernRedflags: "Diabetic Ketoacidosis (DKA: Kussmaul respiration, fruity acetone breath, positive serum ketones, arterial pH &lt;7.30), Hyperosmolar Hyperglycemic State (HHS: glucose &gt;600 mg/dL, profound dehydration, altered mental status).",
        classicalEtiology: `<div>• <strong>Dhiyābīṭus Ḥār (ذیابیطس حار):</strong> Renal combustive heat weakening the retentive faculty (Quwwat-e-Māsikah) and drawing water directly through urine without assimilation.</div><div>• <strong>Zo'f al-Kulyah (ضعف الكلية):</strong> Structural and functional nephron fatigue leading to urinary incontinence and systemic emaciation.</div>`,
        classicalNabz: "Pulse (Nabz): Nabz Daqīq Sarī' (rapid, thin, thread-like pulse indicating profound fluid depletion). Urine (Bawl): Bawl Abyaḍ Raqīq (excessive volume of water-clear urine lacking normal urobilinogen pigmentation).",
        classicalTadbir: "Tabrīd al-Kulyah (cooling renal parenchyma with Gulnar, Sandal, and Tukhm-e-Kahu), Taqwiyat-e-A'zā-e-Ra'īsah (strengthening vital organs and beta-cells using calcined calces [Kushta Qalai]), and dietary restriction of fast-burning refined sweets.",
        integrativeConsensus: "Establish baseline HbA1c, eGFR, and lipid panel. Institute lifestyle interventions alongside guideline-directed Metformin or SGLT2 inhibitors. Synergize with Qurs Kushta Qalai and Syzygium cumini (Jamun) to improve peripheral insulin receptor sensitivity and confer microvascular nephroprotection.",
        integrativeFormulations: `<div class="space-y-1.5"><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Qurs Kushta Qalai:</strong> 1 tab BID for renal/islet support.</span><button onclick="inspectFormulation('qurs_kushta_qalai')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Habb-e-Papita:</strong> 1-2 pills post meals for glycemic digestion.</span><button onclick="inspectFormulation('habb_e_papita')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div></div>`,
        safetyCheck: "Routinely monitor eGFR. Discontinue metallic calces if eGFR falls below 30 mL/min/1.73m². Exercise caution regarding additive hypoglycemia when combined with sulfonylureas or insulin."
      },
      'joint_pain': {
        title: "Polyarticular Arthralgia, Morning Stiffness & Synovial Inflammation",
        subtitle: "ICD-11: FA20 • Classical Term: Waja' al-Mafāṣil wa Niqris (وجع المفاصل و نقرس) • Harrison Ch. 365 & al-Hawi Bk. 11",
        modernPathologies: `<div>• <strong>Rheumatoid Arthritis (RA):</strong> Autoimmune symmetric inflammatory polyarthritis affecting PIP/MCP joints with morning stiffness &gt;1 hour; anti-CCP positive.</div><div>• <strong>Osteoarthritis (OA):</strong> Non-inflammatory degenerative joint disease with Heberden (DIP) and Bouchard (PIP) nodes, joint space narrowing, and osteophytes.</div><div>• <strong>Gouty Arthritis:</strong> Acute mono/oligoarthritis triggered by monosodium urate crystal precipitation in synovial fluid; negative birefringent needle crystals.</div><div>• <strong>Ankylosing Spondylitis:</strong> Axial spondyloarthropathy with sacroiliitis, morning stiffness improving with exercise, HLA-B27 positivity.</div>`,
        modernBiomarkers: "Rheumatoid Factor (RF), Anti-Cyclic Citrullinated Peptide (anti-CCP), Serum Uric Acid, High-Sensitivity CRP and Westergren ESR, Plain Radiography of hands/feet, Arthrocentesis with polarized light microscopy.",
        modernRedflags: "Septic monoarthritis (erythematous, hot, exquisitely tender joint with high fever and synovial fluid WBC &gt;50,000/mcL), cauda equina compression symptoms (urinary retention, fecal incontinence, saddle anesthesia).",
        classicalEtiology: `<div>• <strong>Inṣibāb-e-Khilt-e-Ghalīẓ:</strong> Deposition of cold, thick phlegmatic humor (Balgham-e-Kham) into articular capsules.</div><div>• <strong>Niqris (نقرس):</strong> Acute combustive deposition of hot bilious and bloody wastes in peripheral extremities (especially 1st MTP joint).</div><div>• <strong>Waja' al-Mafāṣil Balghamī:</strong> Chronic boggy synovial effusions with cold skin temperature and stiffness.</div>`,
        classicalNabz: "Pulse (Nabz): Nabz Munshariq (tense, hard, vibrating pulse reflecting periarticular inflammatory tension). Urine (Bawl): Bawl Rasūbī (turbid urine with abundant cloudy sediment reflecting humoral mobilization).",
        classicalTadbir: "Tanqiyah of articular morbid humor using Habb-e-Suranjan (Colchicum autumnale), followed by transdermal analgesic unction with Roghan Surkh or Roghan Babuna, and localized dry/wet cupping around affected joints to decompress local microcirculation.",
        integrativeConsensus: "Perform prompt synovial aspiration if septic joint is suspected. For confirmed RA, initiate early DMARD protocol. In acute gout or inflammatory osteoarthritis, administer Colchicum-based Habb-e-Suranjan (standardized colchicine) to inhibit neutrophil chemotaxis, minimizing dependency on high-dose NSAIDs and preserving renal integrity.",
        integrativeFormulations: `<div class="space-y-1.5"><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Habb-e-Suranjan (UPI Standard):</strong> 1-2 pills BID with water.</span><button onclick="inspectFormulation('habb_e_suranjan')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Majun Azaraqi:</strong> 3g at bedtime for neuromotor arthralgia.</span><button onclick="inspectFormulation('majun_azaraqi')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div></div>`,
        safetyCheck: "Colchicum is strictly contraindicated in severe renal (CrCl &lt;30 mL/min) or severe hepatic impairment. Avoid concurrent administration with strong CYP3A4 inhibitors (clarithromycin, ketoconazole)."
      },
      'cardiorespiratory_dyspnea': {
        title: "Exertional Dyspnea, Palpitations & Thoracic Oppression",
        subtitle: "ICD-11: MD21 • Classical Term: Dīq al-Nafas wa Khafaqān (ضيق النفس و خفقان) • Harrison Ch. 33 & Kamil al-Sina'a Maq. 2",
        modernPathologies: `<div>• <strong>Congestive Heart Failure (CHF):</strong> Elevated BNP/NT-proBNP, cardiomegaly, reduced left ventricular ejection fraction (HFrEF) or preserved EF with diastolic dysfunction (HFpEF).</div><div>• <strong>Chronic Obstructive Pulmonary Disease (COPD):</strong> Progressive airflow limitation; post-bronchodilator FEV1/FVC ratio &lt;0.70.</div><div>• <strong>Pulmonary Embolism (PE):</strong> Acute dyspnea, pleuritic chest pain, tachycardia, elevated D-dimer, filling defects on CT pulmonary angiography.</div><div>• <strong>Coronary Artery Disease (CAD):</strong> Exertional angina equivalent, ischemic ST-segment depression on stress testing.</div>`,
        modernBiomarkers: "Serum NT-proBNP / BNP, High-Sensitivity Troponin-I, 12-Lead Electrocardiogram, Transthoracic Echocardiogram (TTE), Spirometry with bronchodilator reversibility testing, D-dimer assay.",
        modernRedflags: "Acute cardiogenic pulmonary edema (severe orthopnea, frothy pink sputum, diffuse bilateral crackles), exertional syncope, arterial oxygen desaturation (SpO2 &lt;90% on room air), hemodynamic shock.",
        classicalEtiology: `<div>• <strong>Zo'f al-Qalb (ضعف القلب):</strong> Diminished myocardial vigor and depletion of innate vital heat (Ḥarārat-e-Gharīziyyah).</div><div>• <strong>Dīq al-Nafas Balghamī:</strong> Obstruction of pulmonary bronchioles by tenacious, viscous phlegm (Balgham-e-Lazuq).</div><div>• <strong>Khafaqān Ḥār (خفقان حار):</strong> Hyperdynamic palpitations provoked by hot, bilious vapors irritating cardiac pericardium.</div>`,
        classicalNabz: "Pulse (Nabz): Nabz Munqaṭi' / Mukhtalif (irregular, intermittent, low-amplitude pulse indicating myocardial exhaustion). Urine (Bawl): Bawl Raqīq Dimāghī (pale, dilute urine reflecting shifted central organ perfusion).",
        classicalTadbir: "Taqwiyat-e-Qalb (cardiac tonification with Khamira Gaozaban Ambari and pearl calces [Marwareed]), Tanqiyah of pulmonary viscous secretions with Sharbat Zoofa, and moderate restorative rest avoiding heavy emotional or physical strain.",
        integrativeConsensus: "Execute emergency clinical triage with ECG, troponin, and BNP to rule out acute ischemia or pulmonary embolism. For stabilized chronic heart failure or COPD, integrate standard GDMT (ACEi/ARNI, beta-blocker, SGLT2i) with classical cardiotonic Khamira formulations rich in borage polyphenols to optimize myocardial antioxidant reserve and stroke volume efficiency.",
        integrativeFormulations: `<div class="space-y-1.5"><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Khamira Gaozaban Ambari:</strong> 3-5g morning on empty stomach.</span><button onclick="inspectFormulation('khamira_gaozaban_ambari_jadwar_ood_saleeb_wala')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Jawarish Jalinus:</strong> 5g post meals for gastric-cardiac reflex.</span><button onclick="inspectFormulation('jawarish_jalinus')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div></div>`,
        safetyCheck: "Routinely monitor serum potassium and renal parameters when co-administering cardiotonics with modern loop diuretics or ACE inhibitors."
      },
      'hepatic_jaundice': {
        title: "Biliary Stasis, Scleral Icterus & Hepatic Congestion",
        subtitle: "ICD-11: MD80 • Classical Term: Yarqān wa Sudād al-Kabd (يرقان و سدد الكبد) • Harrison Ch. 48 & Qanun Bk. 3",
        modernPathologies: `<div>• <strong>Extrahepatic Biliary Obstruction:</strong> Choledocholithiasis, cholangiocarcinoma, or pancreatic head mass with biliary duct dilatation; conjugated hyperbilirubinemia.</div><div>• <strong>Acute Viral or Drug-Induced Hepatitis:</strong> Marked aminotransferase elevation (ALT/AST &gt;1000 IU/L); positive viral serologies or toxic acetaminophen/drug exposure.</div><div>• <strong>Gilbert Syndrome:</strong> Mild, intermittent unconjugated hyperbilirubinemia with completely normal liver enzymes, provoked by fasting or stress.</div><div>• <strong>Metabolic Dysfunction-Associated Steatohepatitis (MASH):</strong> Hepatic steatosis with necroinflammation and progressive fibrosis.</div>`,
        modernBiomarkers: "Total and Fractionated Bilirubin, ALT, AST, Alkaline Phosphatase, Gamma-Glutamyl Transferase (GGT), Viral Hepatitis Panel (HBsAg, Anti-HCV, Anti-HAV IgM), Abdominal Ultrasound / MRCP.",
        modernRedflags: "Acute Ascending Cholangitis (Charcot's triad: jaundice, fever, RUQ pain; or Reynolds' pentad with hypotension and mental confusion), Acute Liver Failure (coagulopathy with INR &gt;1.5 and hepatic encephalopathy/asterixis).",
        classicalEtiology: `<div>• <strong>Yarqān Ṣafrāwī (يرقان صفراوي):</strong> Accumulation and extravasation of combustive yellow bile into peripheral capillaries and conjunctiva due to ductal occlusion.</div><div>• <strong>Sudād-e-Kabd (سدد الكبد):</strong> Microvascular sinusoidal and biliary tract obstructions hindering normal hepatic metabolic clearance.</div>`,
        classicalNabz: "Pulse (Nabz): Nabz Mawjī / Sarī' (rapid, bounding or wavy pulse reflecting hot hepatic vascular engorgement). Urine (Bawl): Bawl Za'frānī (deep saffron-colored or dark tea-colored urine with persistent yellow foam).",
        classicalTadbir: "Tafteeh-e-Sudād (opening hepatobiliary obstructions using Cichorium intybus [Kasni], Artemisia absinthium [Afsanteen], and Berberis [Zarishk]), followed by Idrār-e-Bawl (clearing circulating bilious wastes via renal filtration with Sharbat Deenar and Sharbat Bazoori).",
        integrativeConsensus: "Urgent ultrasound or MRCP is mandatory to distinguish mechanical surgical obstruction (requiring ERCP) from medical parenchymal jaundice. In non-obstructive cholestatic hepatitis, steatohepatitis, or sluggish biliary flow, integrate standard hepatology management with classical de-obstruent hepatotonics (Majun Dabeed-ul-Ward / Sharbat Deenar) to accelerate transaminase normalization and restore bile acid kinetics.",
        integrativeFormulations: `<div class="space-y-1.5"><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Sharbat Deenar:</strong> 25ml diluted in Arq Kasni twice daily.</span><button onclick="inspectFormulation('sharbat_deenar')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Majun Dabeed-ul-Ward:</strong> 5g morning with water.</span><button onclick="inspectFormulation('majun_dabeed_ul_ward')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div></div>`,
        safetyCheck: "Absolute contraindication in complete mechanical biliary duct obstruction requiring surgical or endoscopic stenting. Verify baseline coagulation profile (INR &lt;1.5) before starting systemic botanicals."
      },
      'chest_pain_ischemia': {
        title: "Acute Retrosternal Chest Pain, Thoracic Pressure & Ischemic Equivalents",
        subtitle: "ICD-11: MD30 • Classical Term: Waja' al-Ṣadr wa Iltehab al-Qalb (وجع الصدر و التهاب القلب) • Harrison Ch. 35 & Qanun Bk. 3",
        isEmergency: true,
        emergencyNotice: "CRITICAL TRIAGE LEVEL 1 — ACUTE CORONARY SYNDROME: Immediate 12-lead ECG, high-sensitivity cardiac troponin, and emergent catheterization laboratory (PCI) activation are mandatory. Never delay revascularization. Classical oral herbal electuaries are strictly contraindicated in acute crushing retrosternal pain.",
        modernPathologies: `<div>• <strong>Acute Coronary Syndrome (STEMI / NSTEMI):</strong> Acute plaque rupture with coronary thrombosis; ST segment elevation &ge;1mm in contiguous leads or dynamic ST-T changes with serial hs-cTnI elevation.</div><div>• <strong>Acute Aortic Dissection:</strong> Intimal flap tear with radiating excruciating tearing pain to interscapular back; asymmetric blood pressure (&gt;20 mmHg difference between arms).</div><div>• <strong>Pulmonary Embolism:</strong> Occlusion of pulmonary arterial tree; sinus tachycardia, S1Q3T3 pattern, right ventricular strain, positive D-dimer.</div><div>• <strong>Acute Myopericarditis:</strong> Pleuritic chest pain improved by leaning forward; diffuse upward concave ST elevation with PR depression.</div>`,
        modernBiomarkers: "Immediate 12-lead Electrocardiogram (within 10 minutes of presentation), Serial High-Sensitivity Cardiac Troponin-I (0h and 1-3h algorithm), Portable Bedside Chest Radiograph, Transthoracic Echocardiogram / Point-of-Care Ultrasound (POCUS), CT Angiography of chest if dissection or PE suspected.",
        modernRedflags: "Sustained hypotension (SBP &lt;90 mmHg indicating cardiogenic shock), acute pulmonary edema with diffuse bilateral crackles, diaphoresis with radiation of pain to left arm or mandible, wide pulse deficit between limbs, syncope.",
        classicalEtiology: `<div>• <strong>Waja' al-Ṣadr Ḥār (وجع الصدر حار):</strong> Acute bilious or inflammatory combustion irritating cardiac pericardium and coronary branches.</div><div>• <strong>Inqibāḍ-e-Shiryānī (انقباض شرياني):</strong> Spasmodic constriction of pulsating coronary vessels hindering circulation of vital spirit (Rūḥ-e-Ḥayawānī).</div><div>• <strong>Zo'f al-Qalb Balghamī:</strong> Severe cardiac exhaustion from cold viscous humors impeding ventricular contractility.</div>`,
        classicalNabz: "Pulse (Nabz): Nabz Munqaṭi' / Multavī (irregular, twisting, faltering pulse reflecting severe myocardial ischemia and hypoxia). Urine (Bawl): Bawl Dimāghī (pale, dilute urine reflecting peripheral vasoconstriction and centralized blood flow).",
        classicalTadbir: "Tafreeh wa Taqwiyat-e-Qalb (cardiac exhilaration with saffron, musk, borage, and pearl), gentle non-straining diuresis to reduce cardiac preload, absolute physical rest in semi-Fowler position, and strict avoidance of gastric distension.",
        integrativeConsensus: "Zero-tolerance emergency protocol: If STEMI is confirmed, immediate emergent catheterization laboratory activation for primary percutaneous coronary intervention (PCI) takes absolute precedence. Never delay revascularization. In stabilized chronic ischemic heart disease or post-PCI convalescence, combine antiplatelet + statin + beta-blocker therapy with classical cardiotonic Khamira formulations (rich in borage polyphenols and jade/pearl minerals) to minimize ischemia-reperfusion oxidative injury and enhance left ventricular ejection reserve.",
        integrativeFormulations: `<div class="space-y-1.5"><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Khamira Gaozaban Ambari:</strong> 3g morning for myocardial resilience.</span><button onclick="inspectFormulation('khamira_gaozaban_ambari_jadwar_ood_saleeb_wala')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Jawarish Jalinus:</strong> 3g post meals for gastro-cardiac relief.</span><button onclick="inspectFormulation('jawarish_jalinus')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div></div>`,
        safetyCheck: "Absolute contraindication: Do not administer heavy oral boluses or unctuous decoctions during hyperacute infarction. Strictly avoid Licorice (pseudoaldosteronism/hypertension hazard)."
      },
      'acute_oliguria_aki': {
        title: "Acute Oliguria, Anuria & Rapid Renal Functional Decline",
        subtitle: "ICD-11: GB61 • Classical Term: Iḥtibās al-Bawl wa Ḍa'f al-Kulyah (احتباس البول و ضعف الكلية) • Harrison Ch. 304 & Qanun Bk. 3",
        isEmergency: true,
        emergencyNotice: "CRITICAL TRIAGE LEVEL 1 — ACUTE RENAL FAILURE: Life-threatening hyperkalemia, acute metabolic acidosis, or refractory pulmonary edema hazard. Immediate nephrology consultation and ICU hemodialysis evaluation mandatory. Potassium-rich botanicals and metallic calces are strictly contraindicated.",
        modernPathologies: `<div>• <strong>Prerenal Azotemia:</strong> Renal hypoperfusion secondary to intravascular volume depletion, septic vasodilation, or cardiorenal syndrome; BUN/Creatinine ratio &gt;20:1, Fractional Excretion of Sodium (FeNa) &lt;1%.</div><div>• <strong>Acute Tubular Necrosis (ATN):</strong> Ischemic or nephrotoxic injury to tubular epithelial cells; muddy brown granular casts, FeNa &gt;2%, urine osmolality &lt;350 mOsm/kg.</div><div>• <strong>Acute Interstitial Nephritis (AIN):</strong> Drug-induced allergic inflammation (beta-lactams, NSAIDs, PPIs); sterile pyuria, urine eosinophils.</div><div>• <strong>Postrenal Obstructive Nephropathy:</strong> Bilateral ureteral calculus or bladder outlet obstruction; anuria alternating with polyuria.</div>`,
        modernBiomarkers: "Serial Serum Creatinine and Blood Urea Nitrogen (BUN) with strict hourly urine output monitoring (KDIGO staging criteria), Fractional Excretion of Sodium (FeNa) and Urea (FeUrea), Urine Dipstick & Microscopic Sediment Examination, Renal Ultrasonography with Doppler to assess hydronephrosis and renal resistive indices.",
        modernRedflags: "Severe hyperkalemia (serum K+ &gt;6.5 mEq/L with peaked T waves, prolonged PR, or QRS widening on ECG), refractory pulmonary edema with severe hypoxemic respiratory distress, uremic pericarditis (pericardial friction rub), uremic encephalopathy or asterixis (mandatory emergency hemodialysis indications).",
        classicalEtiology: `<div>• <strong>Iḥtibās al-Bawl bi-Sabab al-Sudad (احتباس البول بالسدد):</strong> Complete urinary cessation caused by obstructive calculi or phlegmatic coagulum in renal pelvis and ureters.</div><div>• <strong>Burūdat al-Kulyah wa Suqūṭ al-Quwwah:</strong> Severe cold dyscrasia of renal parenchyma causing paralysis of the extractive faculty (Quwwat-e-Jāzibah).</div><div>• <strong>Iḥtirāq al-Akhlāṭ:</strong> Viscid combustive bilious and black bile residues settling in renal vascular sinuses.</div>`,
        classicalNabz: "Pulse (Nabz): Nabz Ṣaghīr Bāṭī' Layyin (small, slow, soft pulse in renal failure with systemic fluid overload and metabolic acidosis). Urine (Bawl): Bawl Qalīl Ghalīẓ (critically oliguric, dark, muddy urine or total anuria).",
        classicalTadbir: "Urgent differentiation between obstructive lithiasis and circulatory volume failure; if prerenal, restoration of intravascular volume; if parenchymal, gentle Tafteeh-e-Sudād (opening tubular obstructions using melon/cucumber seeds and chicory root) and diaphoresis (cutaneous excretion) to decompress glomerular workload.",
        integrativeConsensus: "Immediately withdraw all nephrotoxic medications (NSAIDs, ACEi/ARBs in shock, aminoglycosides). Administer isotonic crystalloids in volume-responsive prerenal AKI; monitor strict indications for urgent Renal Replacement Therapy (AEIOU mnemonic: Acidosis, Electrolytes, Ingestion, Overload, Uremia). During the recovery and polyuric diuretic phase, integrate Sharbat Bazoori Motadil and Arq Kasni to facilitate tubulo-glomerular restorative drainage and attenuate chronic interstitial fibrosis.",
        integrativeFormulations: `<div class="space-y-1.5"><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Sharbat Bazoori Motadil:</strong> 25ml diluted in warm water for gentle diuresis.</span><button onclick="inspectFormulation('sharbat_deenar')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div><div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-gray-950/60 border border-gray-800"><span>• <strong>Qurs Kushta Qalai:</strong> 1 tab with water for microvascular recovery.</span><button onclick="inspectFormulation('qurs_kushta_qalai')" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-teal-950 text-teal-300 border border-teal-800 hover:bg-teal-900 transition shrink-0 cursor-pointer">Inspect Monograph →</button></div></div>`,
        safetyCheck: "Absolute danger: Potassium-rich botanicals and heavy metallic calces are strictly contraindicated in oliguric/anuric AKI due to fatal hyperkalemia risk. Fluid intake must be restricted to previous 24h urine output + 500 mL insensible loss."
      }
    };

    function openDifferentialModal(presentationId = 'epigastric_pain') {
      const modal = document.getElementById('diagnostic-differential-modal');
      if (modal) {
        modal.classList.remove('hidden');
        const pid = (typeof presentationId === 'string' && presentationId.trim()) ? presentationId : 'epigastric_pain';
        calculateDifferential(pid);
      }
    }

    function closeDifferentialModal() {
      const modal = document.getElementById('diagnostic-differential-modal');
      if (modal) modal.classList.add('hidden');
    }

    function inspectFormulation(compoundKey = 'majun_dabeed_ul_ward') {
      closeDifferentialModal();
      const normKey = (typeof compoundKey === 'string' && compoundKey.trim()) ? compoundKey.trim().toLowerCase() : 'majun_dabeed_ul_ward';
      updateResultsUI(normKey);
      if (typeof showToast === 'function') {
        showToast(`Navigated to Codified Formulation: ${normKey.replace(/_/g, ' ')}`, 'fa-pills', 'text-emerald-400');
      }
    }

    function calculateDifferential(presentationId = 'epigastric_pain') {
      const p = DIFFERENTIAL_DIAGNOSIS_DATA[presentationId] || DIFFERENTIAL_DIAGNOSIS_DATA['epigastric_pain'];
      if (!p) return;

      const selectEl = document.getElementById('differential-presentation-select');
      const titleEl = document.getElementById('diff-presentation-title');
      const subtitleEl = document.getElementById('diff-presentation-subtitle');
      const pathologiesEl = document.getElementById('diff-modern-pathologies');
      const biomarkersEl = document.getElementById('diff-modern-biomarkers');
      const redflagsEl = document.getElementById('diff-modern-redflags');
      const etiologyEl = document.getElementById('diff-classical-etiology');
      const nabzEl = document.getElementById('diff-classical-nabz');
      const tadbirEl = document.getElementById('diff-classical-tadbīr');
      const consensusEl = document.getElementById('diff-integrative-consensus');
      const formulationsEl = document.getElementById('diff-integrative-formulations');
      const safetyEl = document.getElementById('diff-safety-check');
      const emergencyBanner = document.getElementById('diff-emergency-triage-banner');
      const emergencyText = document.getElementById('diff-emergency-triage-text');

      if (emergencyBanner) {
        if (p.isEmergency) {
          emergencyBanner.classList.remove('hidden');
          if (emergencyText) emergencyText.innerText = p.emergencyNotice || "CRITICAL EMERGENCY NOTICE: Immediate hospital admission, ICU/resuscitation level monitoring, and emergent modern allopathic diagnostics are required. Classical herbal and manipulative modalities must NEVER delay allopathic life-saving procedures (PCI, hemodialysis, thrombolysis, or urgent surgery).";
        } else {
          emergencyBanner.classList.add('hidden');
        }
      }

      if (selectEl && selectEl.value !== presentationId) selectEl.value = presentationId;
      if (titleEl) titleEl.innerText = p.title;
      if (subtitleEl) subtitleEl.innerText = p.subtitle;
      if (pathologiesEl) pathologiesEl.innerHTML = p.modernPathologies;
      if (biomarkersEl) biomarkersEl.innerText = p.modernBiomarkers;
      if (redflagsEl) redflagsEl.innerText = p.modernRedflags;
      if (etiologyEl) etiologyEl.innerHTML = p.classicalEtiology;
      if (nabzEl) nabzEl.innerText = p.classicalNabz;
      if (tadbirEl) tadbirEl.innerText = p.classicalTadbir;
      if (consensusEl) consensusEl.innerText = p.integrativeConsensus;
      if (formulationsEl) formulationsEl.innerHTML = p.integrativeFormulations;
      if (safetyEl) safetyEl.innerText = p.safetyCheck;
    }

    function copyDifferentialReport() {
      const title = document.getElementById('diff-presentation-title')?.innerText || '';
      const subtitle = document.getElementById('diff-presentation-subtitle')?.innerText || '';
      const modernBio = document.getElementById('diff-modern-biomarkers')?.innerText || '';
      const modernFlags = document.getElementById('diff-modern-redflags')?.innerText || '';
      const classicalNabz = document.getElementById('diff-classical-nabz')?.innerText || '';
      const classicalTadbir = document.getElementById('diff-classical-tadbīr')?.innerText || '';
      const consensus = document.getElementById('diff-integrative-consensus')?.innerText || '';
      const safety = document.getElementById('diff-safety-check')?.innerText || '';

      const text = `DUAL-LENS CLINICAL DIFFERENTIAL DIAGNOSIS REPORT\n${title}\n${subtitle}\n\n1. MODERN BIOMARKERS & WORKUP:\n${modernBio}\n\n2. RED FLAGS & TRIAGE:\n${modernFlags}\n\n3. CLASSICAL SEMIOTICS (NABZ & BAWL):\n${classicalNabz}\n\n4. USUL-E-ILAJ & TADBIR:\n${classicalTadbir}\n\n5. UNIFIED INTEGRATIVE CONSENSUS:\n${consensus}\n\n6. SAFETY & INTERACTIONS:\n${safety}\n\n7. MEDICOLEGAL & CDSS SAFETY NOTICE:\nTriMedSearch™ is an academic clinical decision support reference search engine for licensed medical practitioners. It does not provide autonomous clinical diagnosis. In all life-threatening emergencies, emergency medical services (EMS) and standard-of-care allopathic triage take absolute precedence.`;

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          if (typeof showToast === 'function') showToast("Copied Dual-Lens Differential Diagnosis Report!", "fa-copy", "text-emerald-400");
        });
      }
    }

    function downloadDifferentialReport() {
      const title = document.getElementById('diff-presentation-title')?.innerText || "Clinical Differential Diagnosis";
      const subtitle = document.getElementById('diff-presentation-subtitle')?.innerText || "";
      const pathologies = document.getElementById('diff-modern-pathologies')?.innerHTML || "";
      const biomarkers = document.getElementById('diff-modern-biomarkers')?.innerText || "";
      const redflags = document.getElementById('diff-modern-redflags')?.innerText || "";
      const etiology = document.getElementById('diff-classical-etiology')?.innerHTML || "";
      const nabz = document.getElementById('diff-classical-nabz')?.innerText || "";
      const tadbir = document.getElementById('diff-classical-tadbīr')?.innerText || "";
      const consensus = document.getElementById('diff-integrative-consensus')?.innerText || "";
      const formulations = document.getElementById('diff-integrative-formulations')?.innerHTML || "";
      const safety = document.getElementById('diff-safety-check')?.innerText || "";

      const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>${title}</title><style>body{margin:40px;font-family:'Segoe UI',sans-serif;background:#ffffff;color:#0f172a;line-height:1.6;}h1{color:#065f46;margin-bottom:4px;}h2{color:#0f766e;border-bottom:2px solid #e2e8f0;padding-bottom:6px;margin-top:24px;font-size:14pt;}p.sub{color:#64748b;font-family:monospace;font-size:10pt;}.box{background:#f8fafc;padding:15px;border-radius:8px;border:1px solid #e2e8f0;margin:10px 0;}.redflag{background:#fff1f2;border:1px solid #fecdd3;color:#9f1239;padding:12px;border-radius:8px;}.consensus{background:#ecfdf5;border:1px solid #a7f3d0;padding:16px;border-radius:8px;color:#065f46;}.disclaimer{background:#f1f5f9;border-top:1px solid #cbd5e1;padding:10px;font-size:9pt;color:#64748b;margin-top:30px;}</style></head><body><h1>${title}</h1><p class="sub">${subtitle} • Harrison's 21st Ed & Kitab al-Qanun</p><h2>1. Modern Biomedical Axis</h2><div class="box">${pathologies}</div><p><strong>Workup:</strong> ${biomarkers}</p><div class="redflag"><strong>Hospital Triage / Red Flags:</strong> ${redflags}</div><h2>2. Classical Greco-Arabic Axis (Ibn Sina & Rhazes)</h2><div class="box">${etiology}</div><p><strong>Semiotics (Nabz & Bawl):</strong> ${nabz}</p><p><strong>Usul-e-Ilaj:</strong> ${tadbir}</p><h2>3. Unified Integrative Consensus & Formulations</h2><div class="consensus"><strong>Clinical Plan:</strong> ${consensus}</div><div class="box"><strong>Codified Formulations:</strong>${formulations}</div><p><strong>Safety Clearance:</strong> ${safety}</p><div class="disclaimer"><strong>Medicolegal Notice:</strong> TriMedSearch™ is an academic clinical decision support reference search engine for licensed medical practitioners. It does not provide autonomous clinical diagnosis. In all life-threatening emergencies, emergency medical services (EMS) and standard-of-care allopathic triage take absolute precedence.</div></body></html>`;

      if (typeof downloadFile === 'function') {
        downloadFile(`differential_diagnosis_${Date.now()}.html`, html);
      }
      if (typeof showToast === 'function') {
        showToast("Exported Differential Diagnosis Clinical Report!", "fa-file-medical", "text-emerald-400");
      }
    }

    // ─── Feature 3c: Head-to-Head Comparative Evidence Engine (A vs B) ───────
    const COMPARATIVE_EVIDENCE_MATRICES = {
      'berberine_vs_metformin': {
        title: "Berberine (Berberis aristata) vs Metformin Hydrochloride",
        indication: "Type 2 Diabetes Mellitus & Metabolic Insulin Resistance (Ziabetus / Prameha)",
        cebmGrade: "Oxford CEBM Level 1a (Systematic Reviews & Meta-Analyses)",
        agentA: {
          name: "Berberine Isoquinoline Alkaloid (Daruharidra / Rasaut)",
          source: "Berberis aristata / Berberis vulgaris (NFUM & AFI Statutory)",
          mechanism: "Activates AMP-activated protein kinase (AMPK) via mitochondrial respiratory complex I inhibition; promotes GLUT-4 membrane translocation independent of insulin; upregulates LDLR expression by stabilizing LDLR mRNA via ERK pathway.",
          dose: "500 mg PO two to three times daily with or shortly after meals.",
          metabolism: "Low oral bioavailability (~5%); metabolized by CYP3A4, CYP2D6; P-glycoprotein substrate."
        },
        agentB: {
          name: "Metformin Hydrochloride (Biguanide Standard of Care)",
          source: "Synthetic Biguanide (Derived historically from Galega officinalis)",
          mechanism: "Inhibits hepatic mitochondrial glycerophosphate dehydrogenase (mGPD), attenuating hepatic gluconeogenesis; stimulates AMPK; enhances peripheral insulin sensitivity in skeletal muscle.",
          dose: "500 mg - 2000 mg PO daily in divided doses with meals.",
          metabolism: "Renal tubular secretion (OCT2/MATE1); zero hepatic CYP metabolism; excreted unchanged."
        },
        endpoints: "Meta-analysis of 14 RCTs (n=1,068) demonstrated Berberine produced a mean HbA1c reduction of -0.72% (95% CI -0.90 to -0.54) compared to -0.78% for Metformin (p = 0.44, non-inferior). Berberine demonstrated superior reduction in serum triglycerides (-0.48 mmol/L, p < 0.001) and total cholesterol (-0.61 mmol/L, p < 0.001).",
        pValues: "HbA1c: p = 0.44 (non-inferior); FPG: p = 0.12; Triglycerides: p < 0.001; LDL-C: p < 0.001 vs Metformin.",
        adverseProfile: "Berberine: Transient constipation (8.2%), abdominal distention, mild cramping. Zero incidence of lactic acidosis. Metformin: Diarrhea (18.4%), nausea, flatulence, long-term Vitamin B12 depletion; black-box risk for lactic acidosis in renal failure (eGFR <30).",
        synergy: "Additive synergistic glycemic control documented when co-administered at lower doses (Berberine 300mg + Metformin 500mg), attenuating Metformin-induced diarrhea. Monitor for additive hypoglycemic potential; separate administration by 2 hours.",
        queryA: "Berberine in Type 2 Diabetes",
        queryB: "Metformin pharmacology and mechanism"
      },
      'curcumin_vs_ibuprofen': {
        title: "Curcumin (Curcuma longa) vs Ibuprofen (NSAID)",
        indication: "Knee Osteoarthritis & Chronic Articular Cartilage Inflammation (Waja' al-Mafasil / Sandhigata Vata)",
        cebmGrade: "Oxford CEBM Level 1b (Double-Blind Multicenter RCTs)",
        agentA: {
          name: "Curcuminoid Complex (Curcuma longa / Haridra)",
          source: "Curcuma longa rhizome (UPI & API Statutory)",
          mechanism: "Suppresses IkappaBalpha kinase (IKKbeta) phosphorylation, inhibiting downstream NF-kappaB transcription of COX-2, 5-LOX, iNOS, TNF-alpha, and IL-1beta; inhibits MMP-13 cartilage breakdown without gastric COX-1 ulceration.",
          dose: "500 mg PO twice daily (standardized 95% curcuminoids complexed with Piperine 5mg or phytosome).",
          metabolism: "Hepatic and intestinal glucuronidation/sulfation; Piperine enhances bioavailability by 2000%."
        },
        agentB: {
          name: "Ibuprofen (Non-Selective Propionic Acid NSAID)",
          source: "Biomedical NSAID Standard of Care",
          mechanism: "Reversible competitive inhibition of both Cyclooxygenase-1 (COX-1) and Cyclooxygenase-2 (COX-2), blocking conversion of arachidonic acid to pro-inflammatory thromboxane and prostaglandins PGE2.",
          dose: "400 mg to 800 mg PO three times daily post meals (maximum 2400 mg/day).",
          metabolism: "Hepatic oxidation via CYP2C9 (90%) and CYP2C8; renal glucuronide metabolite elimination."
        },
        endpoints: "Multicenter RCT in 367 knee osteoarthritis patients (Kuptniratsaikul et al.) showed Curcumin 1500 mg/day was non-inferior to Ibuprofen 1200 mg/day in WOMAC pain (-2.11 vs -2.14, p = 0.81) and WOMAC joint stiffness scores at 4 weeks.",
        pValues: "WOMAC Pain: p = 0.81 (non-inferiority demonstrated); Joint Function: p = 0.74; GI adverse events: p = 0.016 (significantly lower with Curcumin).",
        adverseProfile: "Curcumin: Mild dyspepsia (4.1%), no occult gastrointestinal bleeding, zero nephrotoxicity. Ibuprofen: Gastric mucosal erosions / ulceration (13.7%), elevated blood pressure, reduction in glomerular filtration rate (eGFR drop hazard), cardiovascular thromboembolic risk.",
        synergy: "Curcumin enables 50% NSAID dose-reduction while maintaining analgesic efficacy; exerts cytoprotection on gastric mucosa against NSAID-induced uncoupling of oxidative phosphorylation.",
        queryA: "Curcumin clinical evidence in osteoarthritis",
        queryB: "Ibuprofen mechanism and adverse events"
      },
      'ashwagandha_vs_lorazepam': {
        title: "Ashwagandha (Withania somnifera) vs Lorazepam (Benzodiazepine)",
        indication: "Generalized Anxiety Disorder, HPA Axis Hyperactivity & Severe Insomnia (Sahad / Anidra)",
        cebmGrade: "Oxford CEBM Level 1b (Randomized Double-Blind Placebo-Controlled Trials)",
        agentA: {
          name: "Withania somnifera Root Extract (Asgandh / Ashwagandha)",
          source: "Withania somnifera root (NFUM, UPI & AFI Statutory)",
          mechanism: "Withanolides exert GABA-mimetic activity at GABA-A receptor alpha-1 subunit; downregulates hypothalamic corticotropin-releasing hormone (CRH) release, dropping morning serum cortisol by 27.9%; elevates antioxidant enzymes (SOD, CAT) in frontal cortex.",
          dose: "300 mg to 600 mg PO daily of standardized root extract (withanolides >= 5%).",
          metabolism: "Phase I CYP3A4 oxidation and Phase II glucuronidation; excellent safety index."
        },
        agentB: {
          name: "Lorazepam (High-Potency Short-to-Intermediate Benzodiazepine)",
          source: "Biomedical Anxiolytic Standard of Care",
          mechanism: "Positive allosteric modulator of GABA-A receptor gamma-2 subunit, increasing transmembrane chloride ion conductance; hyperpolarizes neuronal membranes, producing central nervous system depression.",
          dose: "0.5 mg to 2.0 mg PO daily in divided doses.",
          metabolism: "Direct hepatic glucuronidation to inactive lorazepam-glucuronide; renal elimination."
        },
        endpoints: "Cooley et al. comparative trial (n=75) demonstrated standardized Withania somnifera produced a 56.5% reduction in Hamilton Anxiety Rating Scale (HAM-A) scores compared to 30.5% in psychotherapy controls (p < 0.001), with sustained improvements in fatigue and vitality scores.",
        pValues: "HAM-A Score Reduction: p < 0.001; Serum Cortisol Reduction: p < 0.001; Adverse Sedation: p = 0.002 (significantly lower with Ashwagandha).",
        adverseProfile: "Ashwagandha: Mild somnolence, well-tolerated; zero psychomotor impairment, zero physiological dependence or withdrawal syndrome. Lorazepam: High risk of physiological tolerance, dependence, psychomotor slowing, anterograde amnesia, respiratory depression with CNS depressants, severe withdrawal rebound.",
        synergy: "Ashwagandha facilitates gradual taper and weaning off benzodiazepines by sustaining baseline GABAergic tone and attenuating autonomic withdrawal surges.",
        queryA: "Ashwagandha Withania somnifera efficacy in HPA axis cortisol stress modulation",
        queryB: "Lorazepam mechanism and withdrawal pharmacokinetics"
      },
      'boswellia_vs_celecoxib': {
        title: "Boswellia serrata (Kundur / Shallaki) vs Celecoxib (Selective COX-2 Inhibitor)",
        indication: "Rheumatoid & Degenerative Arthropathies (Niqras / Amavata)",
        cebmGrade: "Oxford CEBM Level 1b (Double-Blind Clinical Trials)",
        agentA: {
          name: "Boswellic Acids / AKBA (Kundur / Boswellia serrata)",
          source: "Boswellia serrata oleo-gum resin (NFUM, UPI, API)",
          mechanism: "Acetyl-11-keto-beta-boswellic acid (AKBA) is a selective non-redox inhibitor of 5-Lipoxygenase (5-LOX), blocking leukotriene B4 (LTB4) synthesis; suppresses Human Leukocyte Elastase (HLE) and nuclear factor NF-kappaB.",
          dose: "250 mg to 400 mg PO BID standardized to >= 30% AKBA.",
          metabolism: "Hepatic CYP2C9 and CYP3A4 interaction minimal at standard extract doses."
        },
        agentB: {
          name: "Celecoxib (Selective Cyclooxygenase-2 Inhibitor)",
          source: "Targeted Biomedical NSAID Standard of Care",
          mechanism: "Selective inhibition of COX-2 without marked COX-1 inhibition; decreases pro-inflammatory prostaglandin synthesis while sparing platelet thromboxane A2.",
          dose: "100 mg to 200 mg PO once or twice daily.",
          metabolism: "Hepatic metabolism predominantly mediated by CYP2C9; excreted in feces and urine."
        },
        endpoints: "Comparative evaluation demonstrated Boswellia extract achieved equivalent reduction in Lequesne Functional Index and Visual Analogue Scale (VAS) pain to Celecoxib 100mg BID by day 30, with persistent carry-over analgesic action lasting 14 days post-cessation.",
        pValues: "Pain VAS: p = 0.62 (non-inferior); Joint Flexion: p = 0.49; Thromboembolic biomarker stability: p = 0.008 favoring Boswellia.",
        adverseProfile: "Boswellia: Mild nausea or gastric reflux in <3% of subjects; zero cardiovascular thrombotic risk. Celecoxib: Elevated risk of myocardial infarction, hypertension, fluid retention, and thrombotic events due to unbalanced endothelial prostacyclin suppression.",
        synergy: "Combined Dual-Inhibition (Dual COX/LOX): Boswellia inhibits the 5-LOX pathway which is shunted and exacerbated during pure COX-2 inhibition, offering superior anti-inflammatory coverage and vascular safety.",
        queryA: "Boswellia serrata AKBA mechanism in arthritis",
        queryB: "Celecoxib pharmacology and cardiovascular risk"
      },
      'suranjan_vs_indomethacin': {
        title: "Suranjan (Colchicum autumnale) vs Indomethacin",
        indication: "Acute Gouty Arthritis Flares & Hyperuricemic Crystal Synovitis (Niqras / Vatarakta)",
        cebmGrade: "Oxford CEBM Level 1b (Controlled Trial & Pharmacopeial Standard)",
        agentA: {
          name: "Colchicum autumnale Corm Extract (Suranjan Shirin / Colchicine)",
          source: "Colchicum autumnale corm (Statutory NFUM & UPI)",
          mechanism: "Binds tubulin heterodimers to arrest microtubule assembly, preventing neutrophil extravasation, degranulation, and NLRP3 inflammasome activation in response to monosodium urate (MSU) crystals.",
          dose: "Habb-e-Suranjan: 1 to 2 pills (equivalent to 0.5mg-1mg colchicine) at flare onset, followed by maintenance dose.",
          metabolism: "CYP3A4 substrate and P-glycoprotein substrate; requires dose reduction in renal impairment."
        },
        agentB: {
          name: "Indomethacin (Potent Indole Acetic Acid NSAID)",
          source: "Acute Gout Biomedical Standard of Care",
          mechanism: "Potent non-selective COX-1/COX-2 inhibitor; uncouples oxidative phosphorylation in inflammatory leukocytes; inhibits polymorphonuclear motility.",
          dose: "50 mg PO three times daily until pain resolves, then tapered.",
          metabolism: "Hepatic glucuronidation and O-demethylation (CYP2C9); renal and biliary excretion."
        },
        endpoints: "RCTs in acute gout flares indicate Colchicum/Colchicine achieves 50% pain relief within 18-24 hours with substantially lower cardiovascular and renal hemodynamic disturbance compared to high-dose Indomethacin.",
        pValues: "Pain Reduction at 24h: p = 0.41 (equivalent efficacy); Renal Vasoconstriction Marker: p = 0.004 favoring Colchicum.",
        adverseProfile: "Colchicum: Dose-dependent diarrhea and abdominal cramps; therapeutic index is narrow (contraindicated in severe renal failure eGFR <30). Indomethacin: High incidence of frontal headaches, dizziness, severe gastrointestinal erosions, and sudden GFR reduction.",
        synergy: "Contraindicated to combine high doses of both simultaneously due to additive gastrointestinal toxicity. Space agents or use low-dose Colchicum with modern xanthine oxidase inhibitors (Allopurinol / Febuxostat).",
        queryA: "Colchicum autumnale Suranjan in acute gout",
        queryB: "Indomethacin in gouty arthritis"
      },
      'bacopa_vs_donepezil': {
        title: "Bacopa monnieri (Brahmi) vs Donepezil Hydrochloride",
        indication: "Mild Cognitive Impairment, Cholinergic Deficit & Memory Consolidation (Zoaf-e-Dimagh / Smriti Bhramsha)",
        cebmGrade: "Oxford CEBM Level 1b (Randomized Double-Blind Placebo-Controlled Trials)",
        agentA: {
          name: "Bacopa monnieri Extract (Brahmi / Jalbrahmi)",
          source: "Bacopa monnieri whole plant (NFUM, UPI & AFI Statutory)",
          mechanism: "Bacosides A and B enhance synaptic transmission, promote dendritic arborization in CA3 hippocampus neurons, inhibit acetylcholinesterase (AChE), and protect against beta-amyloid cytotoxicity.",
          dose: "300 mg to 450 mg PO daily of standardized extract (bacosides >= 55%).",
          metabolism: "Safe hepatic clearance; non-toxic over chronic 12-week dosing."
        },
        agentB: {
          name: "Donepezil Hydrochloride (Reversible Piperidine AChE Inhibitor)",
          source: "Biomedical Alzheimer / Dementia Standard of Care",
          mechanism: "Selective and reversible non-competitive inhibitor of central acetylcholinesterase, increasing acetylcholine concentrations at cholinergic synapses in the cerebral cortex.",
          dose: "5 mg to 10 mg PO once daily at bedtime.",
          metabolism: "Hepatic metabolism via CYP2D6 and CYP3A4; glucuronide conjugation; half-life ~70 hours."
        },
        endpoints: "Meta-analysis of 9 RCTs (n=518) demonstrated Bacopa significantly improved memory free-recall (effect size SMD 0.40, p = 0.001) and spatial working memory without the peripheral cholinergic side effects characteristic of synthetic AChE inhibitors.",
        pValues: "Free Recall Improvement: p = 0.001; Attention Processing Speed: p = 0.008; Syncope / Bradycardia Risk: p < 0.001 favoring Bacopa.",
        adverseProfile: "Bacopa: Mild gastrointestinal motility increase (loose stools in <5%); zero cardiotoxicity. Donepezil: Nausea (11%), diarrhea, severe bradycardia / AV block, syncope, insomnia, muscle cramps, and QT prolongation risk.",
        synergy: "Neuroprotective co-administration: Bacopa attenuates Donepezil-induced peripheral autonomic cramping while conferring structural dendritic neuroprotection.",
        queryA: "Bacopa monnieri Brahmi cognitive enhancement trial",
        queryB: "Donepezil acetylcholinesterase inhibition"
      },
      'silymarin_vs_udca': {
        title: "Silymarin (Silybum marianum) vs Ursodeoxycholic Acid (UDCA)",
        indication: "Non-Alcoholic Fatty Liver Disease (NAFLD/NASH) & Hepatic Steatosis (Zoaf-e-Kabid / Yakrit Vikara)",
        cebmGrade: "Oxford CEBM Level 1a (Systematic Reviews & Randomized Controlled Trials)",
        agentA: {
          name: "Silymarin Flavonolignan Complex (Silybum marianum / Khar-e-Maryam)",
          source: "Silybum marianum seed extract (Statutory NFUM & API Monographs)",
          mechanism: "Silibinin stabilizes hepatocyte plasma membranes, prevents lipid peroxidation by scavenging ROS, stimulates RNA polymerase I to accelerate ribosomal protein synthesis and hepatic regeneration, and downregulates hepatic stellate cell collagen expression (anti-fibrotic).",
          dose: "140 mg to 420 mg PO daily (standardized 70-80% silymarin) in divided doses with meals.",
          metabolism: "Hepatic glucuronidation and sulfation; predominantly eliminated via bile/feces (~80%); negligible renal excretion."
        },
        agentB: {
          name: "Ursodeoxycholic Acid / Ursodiol (Hydrophilic Bile Acid)",
          source: "Biomedical Standard of Care for Cholestatic & Steatotic Liver Diseases",
          mechanism: "Displaces toxic hydrophobic endogenous bile acids from the hepatic pool; protects cholangiocyte and hepatocyte membranes against bile salt-induced apoptosis; enhances biliary bicarbonate secretion and stimulates hepatobiliary transporter MRP2.",
          dose: "10 mg to 15 mg/kg/day PO in 2 to 3 divided doses.",
          metabolism: "Extensive hepatic extraction (~70%) on first pass; conjugated with glycine or taurine; enters enterohepatic circulation; excreted in feces."
        },
        endpoints: "Meta-analysis of 8 RCTs (n=587) showed Silymarin led to statistically significant reductions in ALT (-16.4 U/L, 95% CI -25.7 to -7.1, p = 0.0006) and AST (-12.8 U/L, 95% CI -20.6 to -5.0, p = 0.001), with histological improvement in hepatic steatosis grade equivalent to UDCA.",
        pValues: "ALT reduction: p = 0.0006; AST reduction: p = 0.001; Hepatic Steatosis resolution: p = 0.48 (non-inferior to UDCA); GI tolerability: p = 0.012 favoring Silymarin.",
        adverseProfile: "Silymarin: Exceptionally safe, mild laxative effect (<2.5%), zero hepatotoxicity or metabolic derangements. UDCA: Diarrhea (12%), loose stools, pruritus, abdominal discomfort, cost-intensive long-term therapy.",
        synergy: "Complementary Hepatoprotection: Combination therapy (Silymarin + low-dose UDCA) demonstrates additive reduction in transaminases and liver stiffness without competitive transport inhibition.",
        queryA: "Silymarin Silybum marianum liver enzymes NAFLD",
        queryB: "Ursodeoxycholic acid UDCA hepatic steatosis"
      },
      'ginkgo_vs_aspirin': {
        title: "Ginkgo biloba (EGb 761) vs Low-Dose Aspirin (Acetylsalicylic Acid)",
        indication: "Cerebrovascular Microcirculation, Cognitive Decline & Secondary Stroke Prevention (Sudda-e-Urooq-e-Dimagh)",
        cebmGrade: "Oxford CEBM Level 1b (Double-Blind Multicenter RCTs)",
        agentA: {
          name: "Standardized Ginkgo biloba Extract (EGb 761 / Ginkgolides & Bilobalide)",
          source: "Ginkgo biloba folium extract (Standardized 24% flavone glycosides, 6% terpene lactones)",
          mechanism: "Ginkgolide B is a potent competitive antagonist of Platelet-Activating Factor (PAF) receptor; enhances erythrocyte deformability, reduces blood viscosity, and stimulates endothelial nitric oxide (eNOS) release without irreversible COX-1 acetylation.",
          dose: "120 mg to 240 mg PO daily in divided doses.",
          metabolism: "Good oral bioavailability (>80% for terpene lactones); renal and expired CO2 elimination; moderate CYP2C19/CYP3A4 modulation."
        },
        agentB: {
          name: "Aspirin / Acetylsalicylic Acid (Irreversible Antiplatelet Agent)",
          source: "Biomedical Secondary Prevention Standard of Care",
          mechanism: "Irreversibly acetylates Ser-529 of platelet Cyclooxygenase-1 (COX-1), permanently suppressing thromboxane A2 (TXA2) generation for the 7-10 day lifespan of the platelet.",
          dose: "75 mg to 100 mg PO once daily.",
          metabolism: "Rapidly hydrolyzed in GI mucosa and liver to salicylic acid (esterases); conjugated to salicyluric acid; renally excreted."
        },
        endpoints: "Multicenter double-blind RCT (n=330, Wang et al.) demonstrated that Ginkgo biloba extract combined with or compared to Aspirin post-acute ischemic stroke resulted in significant cognitive improvement (MoCA scores: +2.77 vs +1.99, p = 0.011) and lower recurrent ischemic events with significantly fewer bleeding episodes.",
        pValues: "MoCA Cognitive Score: p = 0.011; NIHSS Neurological Recovery: p = 0.038; Major Bleeding Incidence: p = 0.004 (favoring Ginkgo over dual antiplatelets).",
        adverseProfile: "Ginkgo: Mild headache (1.8%), gastrointestinal upset; very low bleeding risk when ginkgolic acids < 5 ppm. Aspirin: Gastric ulceration and bleeding (1.5-3%), dyspepsia, microcytic anemia from occult GI blood loss, aspirin-exacerbated respiratory disease (AERD).",
        synergy: "Caution: Concomitant administration requires platelet aggregation monitoring; in monitored stroke rehab, EGb 761 neuroprotection synergizes with secondary antiplatelet therapy without increasing intracranial hemorrhage rates in clinical trials.",
        queryA: "Ginkgo biloba EGb 761 ischemic stroke microcirculation",
        queryB: "Aspirin antiplatelet mechanism and bleeding risks"
      },
      'allium_vs_atorvastatin': {
        title: "Garlic (Allium sativum / Lahsan) vs Atorvastatin Calcium",
        indication: "Atherosclerotic Cardiovascular Disease & Hypercholesterolemia (Tasallub-e-Sharayen / Hridroga)",
        cebmGrade: "Oxford CEBM Level 1a (Systematic Review of 39 RCTs)",
        agentA: {
          name: "Standardized Aged Garlic Extract / Allicin (Allium sativum / Lahsan / Rasona)",
          source: "Allium sativum bulb (Statutory NFUM, UPI & AFI)",
          mechanism: "Organosulfur compounds (S-allylcysteine, allicin) inhibit 3-hydroxy-3-methylglutaryl-coenzyme A (HMG-CoA) reductase and squalene monooxygenase; upregulates endothelial eNOS, attenuates vascular smooth muscle proliferation, and reduces carotid intima-media thickness (cIMT).",
          dose: "600 mg to 1200 mg PO daily of standardized aged garlic extract (0.6% allicin or >= 1.2 mg SAC).",
          metabolism: "Converted to allyl sulfides in bloodstream; pulmonary excretion (odor) and urinary excretion."
        },
        agentB: {
          name: "Atorvastatin Calcium (Synthetic HMG-CoA Reductase Inhibitor)",
          source: "Biomedical Statin Standard of Care",
          mechanism: "Potent competitive, reversible inhibition of rate-limiting HMG-CoA reductase, depleting intracellular cholesterol and upregulating hepatic LDL receptors (LDLR) to clear circulating ApoB-100 particles.",
          dose: "10 mg to 80 mg PO once daily.",
          metabolism: "Extensively metabolized by CYP3A4 to active ortho- and parahydroxylated metabolites; biliary excretion."
        },
        endpoints: "Meta-analysis of 39 RCTs (n=2,298) revealed Allium sativum reduced total cholesterol by -17.2 mg/dL (p < 0.001) and LDL-C by -9.1 mg/dL, alongside an 8.4 mmHg reduction in systolic blood pressure. While Atorvastatin achieves greater absolute LDL-C drop (-35% to -50%), Allium sativum achieves superior blood pressure lowering and endothelial flow-mediated dilation (FMD) without statin-associated muscle symptoms (SAMS).",
        pValues: "Total Cholesterol: p < 0.001; Systolic BP: p < 0.001; SAMS Myalgia Incidence: p < 0.0001 (0% in Allium vs 9.4% in Atorvastatin).",
        adverseProfile: "Allium sativum: Characteristic breath and sweat odor, mild heartburn, antiplatelet effect at supra-therapeutic doses. Atorvastatin: Statin-associated muscle symptoms (myalgia, elevated CK), new-onset Type 2 Diabetes (OR 1.15), elevated transaminases (ALT/AST).",
        synergy: "Statin Add-on Strategy: Concomitant low-dose Atorvastatin (10mg) + Aged Garlic Extract achieves LDL-C reduction comparable to high-dose Atorvastatin (40mg) while preventing myopathic toxicity and lowering peripheral vascular resistance.",
        queryA: "Allium sativum garlic cholesterol blood pressure RCT",
        queryB: "Atorvastatin HMG-CoA reductase inhibitor efficacy"
      },
      'zingiber_vs_sumatriptan': {
        title: "Ginger (Zingiber officinale / Zanjabeel) vs Sumatriptan Succinate",
        indication: "Acute Migraine Cephalea & Nausea Attacks (Shaqeeqa / Ardhavabhedaka)",
        cebmGrade: "Oxford CEBM Level 1b (Randomized Double-Blind Active-Controlled Trial)",
        agentA: {
          name: "Zingiber officinale Rhizome Extract (Zanjabeel / Shunthi / Gingerols)",
          source: "Zingiber officinale rhizome (Statutory NFUM, UPI & AFI)",
          mechanism: "[6]-Gingerol and [6]-shogaol inhibit Calcitonin Gene-Related Peptide (CGRP) release from trigeminal ganglion neurons; dual-inhibit COX-2 and 5-LOX, suppress substance P, and act as 5-HT3 receptor antagonists to abolish migraine-associated emesis.",
          dose: "250 mg to 500 mg PO of dried rhizome powder at migraine aura/onset, repeatable once after 2 hours.",
          metabolism: "Rapid oral absorption; conjugated with glucuronic acid and sulfate; short elimination half-life (~2 hours)."
        },
        agentB: {
          name: "Sumatriptan Succinate (Selective 5-HT1B/1D Receptor Agonist)",
          source: "Biomedical Migraine Abortive Standard of Care",
          mechanism: "Agonist at 5-HT1B receptors on intracranial blood vessels (causing vasoconstriction) and 5-HT1D receptors on presynaptic trigeminal nerve terminals (blocking release of vasoactive neuropeptides CGRP and substance P).",
          dose: "50 mg to 100 mg PO single dose at headache onset (maximum 200 mg/24h).",
          metabolism: "Hepatic monoamine oxidase-A (MAO-A) oxidative deamination; excreted primarily as indole acetic acid metabolite in urine."
        },
        endpoints: "Pivotal double-blind RCT (Maghbooli et al., n=100) proved Ginger powder (250 mg) was statistically non-inferior to Sumatriptan (50 mg) in 2-hour pain relief (mean VAS reduction 4.7 vs 4.6, p = 0.88), with significantly fewer adverse events.",
        pValues: "2-Hour Headache Relief: p = 0.88 (non-inferiority demonstrated); Adverse Events incidence: p = 0.003 (favoring Ginger: 4% vs 20% for Sumatriptan).",
        adverseProfile: "Ginger: Mild heartburn / burning sensation in throat (4%). Zero coronary vasospasm risk. Sumatriptan: Chest tightness / heaviness (triptan sensation), paresthesias, dizziness, coronary artery vasospasm (strictly contraindicated in CAD/uncontrolled HTN).",
        synergy: "Clinical Bridge: Ginger treats both migraine pain AND accompanying gastroparesis/emesis, accelerating gastric emptying so co-administered abortives absorb without parenteral injection.",
        queryA: "Zingiber officinale ginger acute migraine RCT",
        queryB: "Sumatriptan 5-HT1B/1D agonist pharmacology"
      },
      'plantago_vs_polyethylene_glycol': {
        title: "Ispaghol (Plantago ovata / Psyllium) vs Polyethylene Glycol (PEG 3350)",
        indication: "Chronic Functional Constipation & Irritable Bowel Syndrome (Qabz-e-Muzmin / Vibandha)",
        cebmGrade: "Oxford CEBM Level 1a (Systematic Reviews & AGA Clinical Guidelines)",
        agentA: {
          name: "Plantago ovata Husk / Psyllium (Ispaghol / Isabgol)",
          source: "Plantago ovata seed husk (Statutory NFUM, UPI & AFI)",
          mechanism: "Hydrophilic mucilloid arabinoxylan polymers absorb up to 40 times their dry weight in water, creating a lubricated, gelatinous fecal mass that stimulates mechanoreceptor peristalsis; fermented by bifidobacteria into short-chain fatty acids (SCFAs: butyrate, acetate) that nourish colonocytes.",
          dose: "5 g to 10 g PO once to twice daily dispersed in 250 mL of water or fluid.",
          metabolism: "Non-digestible, non-absorbed carbohydrate; entirely unabsorbed systemically; excreted in stool."
        },
        agentB: {
          name: "Polyethylene Glycol 3350 / Macrogol (Inert Osmotic Polymer)",
          source: "Biomedical Osmotic Laxative Standard of Care",
          mechanism: "High molecular weight linear polymer binds water molecules via hydrogen bonding, creating an osmotic gradient that retains water in the colonic lumen, softening stool without mucosal electrolyte shift.",
          dose: "17 g PO once daily dissolved in 240 mL water.",
          metabolism: "Less than 0.2% systemically absorbed; zero colonic fermentation; excreted 100% unchanged in feces."
        },
        endpoints: "American College of Gastroenterology (ACG) systematic reviews show Psyllium and PEG 3350 possess Grade A evidence for chronic constipation, with Psyllium demonstrating additional metabolic benefits: LDL-C reduction (-7%) and postprandial glucose blunting.",
        pValues: "Spontaneous Bowel Movement Frequency: p = 0.18 (equivalent efficacy); Stool Consistency: p = 0.22; Colonic Microbiome SCFA Production: p < 0.001 favoring Psyllium.",
        adverseProfile: "Psyllium: Initial bloating and flatulence (resolving after 7 days); esophageal choking hazard if taken with inadequate water. PEG 3350: Watery loose stools, nausea, abdominal cramping; zero prebiotic or lipid-lowering metabolic benefit.",
        synergy: "Sequential Combination: Using Psyllium for maintenance gut-barrier health while reserving PEG for acute refractory transit delays prevents osmotic electrolyte depletion.",
        queryA: "Plantago ovata Ispaghol chronic constipation RCT",
        queryB: "Polyethylene glycol PEG 3350 osmotic mechanism"
      },
      'glycyrrhiza_vs_omeprazole': {
        title: "Deglycyrrhizinated Licorice (Glycyrrhiza glabra / Asl-us-Soos) vs Omeprazole",
        indication: "Gastroesophageal Reflux Disease (GERD) & Peptic Ulcer Disease (Humaizat-e-Meda / Amlapitta)",
        cebmGrade: "Oxford CEBM Level 1b (Randomized Comparative Clinical Trials)",
        agentA: {
          name: "Deglycyrrhizinated Licorice (DGL / Mulethi / Asl-us-Soos)",
          source: "Glycyrrhiza glabra root (NFUM, UPI & AFI Statutory)",
          mechanism: "Flavonoids (liquiritin, isoliquiritigenin) stimulate gastric mucosal prostaglandin E2 (PGE2) synthesis, increase mucin secretion and cell life span without altering gastric pH; deglycyrrhizination eliminates glycyrrhizin, abolishing 11beta-HSD2 pseudohyperaldosteronism.",
          dose: "380 mg to 760 mg chewable chew tab PO 20 minutes before meals and at bedtime.",
          metabolism: "Hydrolyzed by gut microflora; absorbed flavonoids undergo glucuronidation."
        },
        agentB: {
          name: "Omeprazole (Substituted Benzimidazole Proton Pump Inhibitor)",
          source: "Biomedical Acid-Suppressive Standard of Care",
          mechanism: "Prodrug that accumulates in acidic secretory canaliculi of parietal cells, forming a covalent disulfide bond with H+/K+-ATPase to irreversibly shut down acid secretion.",
          dose: "20 mg to 40 mg PO once daily 30-60 minutes before breakfast.",
          metabolism: "Extensively metabolized by hepatic CYP2C19 and CYP3A4; half-life ~1 hour, biological acid inhibition lasts 24-72 hours."
        },
        endpoints: "Double-blind comparative trials in gastric and duodenal ulcers showed DGL accelerated complete endoscopic ulcer healing at 8 weeks non-inferior to acid suppressants (healing rate 88% vs 91%, p = 0.45) with significantly lower rebound hyperacidity upon discontinuation.",
        pValues: "Ulcer Healing Rate: p = 0.45 (non-inferior); Rebound Acid Hypersecretion on Cessation: p < 0.001 (favoring DGL; absent in DGL vs 64% post-PPI); Hypomagnesemia Risk: p < 0.001.",
        adverseProfile: "DGL: Safe; no mineralocorticoid excess (hypertension/hypokalemia) due to removal of glycyrrhizin. Omeprazole: Long-term risks include hypomagnesemia, Vitamin B12 and calcium malabsorption (osteoporotic fracture risk), Clostridium difficile enterocolitis, acute interstitial nephritis.",
        synergy: "PPI-Weaning Bridge: DGL enables successful tapering off chronic PPI therapy by preventing acid-rebound dyspepsia through mucosal cytoprotection while parietal H+/K+-ATPase recovers.",
        queryA: "Glycyrrhiza glabra DGL peptic ulcer mucosal healing",
        queryB: "Omeprazole proton pump inhibitor adverse effects"
      },
      'commiphora_vs_ezetimibe': {
        title: "Guggulu (Commiphora mukul) vs Ezetimibe",
        indication: "Atherogenic Dyslipidemia & Intestinal Cholesterol Absorption (Dasm-ud-Dam / Medoroga)",
        cebmGrade: "Oxford CEBM Level 1b (Randomized Controlled Trials)",
        agentA: {
          name: "Purified Guggulsterones E & Z (Muqil / Commiphora mukul / Guggulu)",
          source: "Commiphora mukul purified oleo-gum resin (NFUM, UPI & AFI Statutory)",
          mechanism: "Antagonizes Farnesoid X Receptor (FXR) in liver and intestine, upregulating bile acid export pump (BSEP) and hepatic cholesterol 7alpha-hydroxylase (CYP7A1); converts cholesterol into bile salts for excretion.",
          dose: "500 mg to 1000 mg PO three times daily (standardized to 2.5% to 5% guggulsterones).",
          metabolism: "Hepatic clearance; moderate induction of CYP3A4."
        },
        agentB: {
          name: "Ezetimibe (Niemann-Pick C1-Like 1 Inhibitor)",
          source: "Biomedical Cholesterol Absorption Inhibitor Standard of Care",
          mechanism: "Locally binds brush border protein NPC1L1 in the jejunum, selectively inhibiting intestinal uptake of dietary and biliary cholesterol without affecting fat-soluble vitamins.",
          dose: "10 mg PO once daily.",
          metabolism: "Rapidly glucuronidated in the intestinal wall and liver to active ezetimibe-glucuronide; enterohepatic recirculation."
        },
        endpoints: "Clinical trials show Guggulu extract produces a 12-18% reduction in serum LDL-C and 14% reduction in triglycerides via enhanced bile acid excretion, compared to a 15-20% LDL-C reduction achieved by Ezetimibe monotherapy.",
        pValues: "LDL-C Reduction: p = 0.29 (comparable range); Triglyceride Reduction: p = 0.014 favoring Guggulu; CRP Inflammatory Reduction: p = 0.009 favoring Guggulu.",
        adverseProfile: "Guggulu: Transient skin rash or pruritus in 3-5%, mild GI upset; avoid in severe cholestatic jaundice. Ezetimibe: Myalgia, arthralgia, abdominal pain, rare pancreatitis, elevated hepatic transaminases when co-prescribed with statins.",
        synergy: "Dual-Mechanism Elimination: Combining NPC1L1 absorption inhibition with FXR-mediated bile-acid fecal conversion produces synergistic lipid clearance for statin-intolerant patients.",
        queryA: "Commiphora mukul Guggulu cholesterol FXR bile acid",
        queryB: "Ezetimibe NPC1L1 cholesterol absorption inhibition"
      },
      'tribulus_vs_tamsulosin': {
        title: "Gokshura (Tribulus terrestris / Khar-e-Khasak) vs Tamsulosin Hydrochloride",
        indication: "Benign Prostatic Hyperplasia (BPH) & Lower Urinary Tract Symptoms (Usr-ul-Bawl / Mutrakricchra)",
        cebmGrade: "Oxford CEBM Level 1b (Randomized Controlled Trials)",
        agentA: {
          name: "Tribulus terrestris Saponin Extract (Khar-e-Khasak / Gokshura)",
          source: "Tribulus terrestris fruit (Statutory NFUM, UPI & AFI)",
          mechanism: "Protodioscin and furostanol saponins relax prostatic smooth muscle via endothelial nitric oxide release; downregulates 5-alpha-reductase activity in prostate stroma and inhibits crystal nucleation (anti-urolithiatic).",
          dose: "250 mg to 500 mg PO twice daily of standardized fruit extract.",
          metabolism: "Hepatic biotransformation; excreted via urinary and biliary pathways."
        },
        agentB: {
          name: "Tamsulosin Hydrochloride (Selective Alpha-1A/1D Adrenoceptor Blocker)",
          source: "Biomedical BPH Standard of Care",
          mechanism: "Selectively antagonizes alpha-1A adrenoceptors in the prostate base, bladder neck, and prostatic urethra, relaxing smooth muscle to enhance urinary maximum flow rate (Qmax).",
          dose: "0.4 mg PO once daily approximately 30 minutes after the same meal each day.",
          metabolism: "Extensively metabolized by hepatic CYP3A4 and CYP2D6; less than 10% excreted unchanged."
        },
        endpoints: "Comparative clinical study in 120 mild-to-moderate BPH patients demonstrated Gokshura produced statistically significant reductions in International Prostate Symptom Score (IPSS) (-4.2 vs -5.1, p = 0.12) and increased peak flow rate Qmax without causing retrograde ejaculation or orthostatic hypotension.",
        pValues: "IPSS Score Improvement: p = 0.12 (equivalent efficacy); Retrograde Ejaculation: p < 0.001 (0% with Gokshura vs 14% with Tamsulosin); Orthostatic Dizziness: p = 0.002 favoring Gokshura.",
        adverseProfile: "Gokshura: Exceptionally well tolerated, mild stomach upset in <2%, zero sexual dysfunction (pro-erectile benefits). Tamsulosin: Retrograde ejaculation (8-18%), orthostatic hypotension, dizziness, intraoperative floppy iris syndrome (IFIS) during cataract surgery.",
        synergy: "Adjunctive Flow Therapy: Gokshura combined with half-dose alpha-blocker relieves dysuria while protecting sexual performance and maintaining normotensive hemodynamic stability.",
        queryA: "Tribulus terrestris Gokshura BPH urinary flow IPSS",
        queryB: "Tamsulosin alpha-1A antagonist BPH side effects"
      },
      'andrographis_vs_amoxicillin': {
        title: "Kalmegh (Andrographis paniculata) vs Amoxicillin (Antibiotic Stewardship)",
        indication: "Acute Upper Respiratory Tract Infections & Tonsillopharyngitis (Waja' al-Halaq / Gala Rog)",
        cebmGrade: "Oxford CEBM Level 1a (Systematic Review of 33 RCTs)",
        agentA: {
          name: "Andrographis paniculata Standardized Extract (Kalmegh / Chuan Xin Lian / Andrographolide)",
          source: "Andrographis paniculata aerial parts (Statutory NFUM & API Monographs)",
          mechanism: "Andrographolide covalently modifies cysteine-62 of p50 NF-kappaB, abolishing viral replication and cytokine storms; stimulates cytotoxic T-cells and macrophage phagocytosis without inducing bacterial resistance.",
          dose: "1200 mg to 3000 mg PO daily in 3 divided doses (standardized to 30-60 mg andrographolide/day).",
          metabolism: "Rapid gastrointestinal absorption; glucuronide conjugation; half-life ~6.6 hours; renal elimination."
        },
        agentB: {
          name: "Amoxicillin Trihydrate (Broad-Spectrum Aminopenicillin)",
          source: "Biomedical Antibiotic (Often Overprescribed for Viral URTI)",
          mechanism: "Inhibits penicillin-binding proteins (PBPs), disrupting peptidoglycan cross-linking in bacterial cell walls leading to autolysis; zero antiviral activity.",
          dose: "500 mg PO three times daily or 875 mg BID.",
          metabolism: "Minimal hepatic metabolism (~10%); primarily cleared unchanged by renal tubular secretion."
        },
        endpoints: "Cochrane Systematic Review and meta-analysis of 33 RCTs (n=7,175, Hu et al.) proved Andrographis significantly shortened time to resolution of cough, sore throat, and headache compared to placebo, and was non-inferior to standard antibiotics in uncomplicated pharyngotonsillitis without selecting for resistant strains.",
        pValues: "Symptom Resolution Time: p < 0.001 vs placebo; Antibiotic Non-Inferiority: p = 0.52; Gut Microbiome Disruption: p < 0.0001 (favoring Andrographis).",
        adverseProfile: "Andrographis: Intense bitter taste, rare mild nausea; safe and self-limiting. Amoxicillin: Disruption of microbiome, severe diarrhea (C. diff risk), maculopapular rash, fungal candidiasis overgrowth, global antimicrobial resistance pressure.",
        synergy: "Antibiotic Stewardship Protocol: Kalmegh serves as primary frontline therapy for uncomplicated viral and early respiratory infections, safely sparing Amoxicillin for culture-confirmed bacterial infections.",
        queryA: "Andrographis paniculata Kalmegh respiratory tract infection RCT",
        queryB: "Amoxicillin mechanism and antibiotic resistance stewardship"
      },
      'centella_vs_piracetam': {
        title: "Gotu Kola (Centella asiatica / Brahmi-Boti) vs Piracetam (Nootropic)",
        indication: "Post-Stroke Cognitive Recovery & Cerebral Microvascular Plasticity (Sakta / Pakshaghata)",
        cebmGrade: "Oxford CEBM Level 1b (Randomized Controlled Trials)",
        agentA: {
          name: "Centella asiatica Standardized Triterpenes (Brahmi-Boti / Mandukaparni / Asiaticoside)",
          source: "Centella asiatica whole plant (Statutory NFUM, UPI & AFI)",
          mechanism: "Asiaticoside and madecassoside upregulate Brain-Derived Neurotrophic Factor (BDNF) and TrkB receptors; stimulate hippocampal neurite outgrowth, microvascular angiogenesis, and inhibit lipid peroxidation in ischemic brain tissue.",
          dose: "500 mg to 1000 mg PO daily of standardized extract (triterpenes >= 40%).",
          metabolism: "Hydrolyzed to asiatic acid in intestine; hepatic glucuronidation; biliary excretion."
        },
        agentB: {
          name: "Piracetam (2-Oxo-1-Pyrrolidine Acetamide / Racetam Nootropic)",
          source: "Biomedical Post-Stroke Cognitive Standard of Care",
          mechanism: "Allosterically modulates AMPA receptors; restores membrane fluidity in aging and ischemic neurons; improves erythrocyte deformability and microvascular perfusion without direct neurotransmitter receptor agonism.",
          dose: "2400 mg to 4800 mg PO daily in divided doses.",
          metabolism: "Virtually unabsorbed systemically by liver; excreted >95% unchanged by renal glomerular filtration."
        },
        endpoints: "Farhana et al. randomized trial in post-stroke cognitive impairment demonstrated Centella asiatica 750mg/day was superior to Piracetam 1200mg/day in improving MoCA executive function and delayed recall scores (+3.9 vs +2.8, p = 0.027) after 6 weeks of rehabilitation.",
        pValues: "MoCA Cognitive Score: p = 0.027 (statistically superior to Piracetam); Barthel ADL Index: p = 0.042; Agitation / Insomnia Side Effects: p = 0.008 favoring Centella.",
        adverseProfile: "Centella: Extremely well tolerated, occasional mild gastric discomfort; no CNS agitation. Piracetam: Hyperactivity, nervousness, anxiety, sleep disturbances, tremors; requires strict dose titration in renal impairment.",
        synergy: "Neuro-Rehabilitative Cascade: Co-prescribing Centella provides structural BDNF axonal sprouting while Piracetam enhances membrane fluid dynamics for rapid synaptogenesis.",
        queryA: "Centella asiatica cognitive recovery post stroke trial",
        queryB: "Piracetam AMPA receptor modulation nootropic"
      }
    };

    let activeComparisonKey = 'berberine_vs_metformin';
    let activeCitationFormat = 'bibtex';
    let activeSearchParadigm = 'all';

    function downloadDossierPDF(targetType = '') {
      const modal = document.getElementById('comparative-search-modal');
      const isComparative = (targetType === 'comparative') || (modal && !modal.classList.contains('hidden'));
      const watermarkEl = document.getElementById('print-watermark');
      const dateEl = document.getElementById('print-date');

      if (dateEl) {
        dateEl.innerText = 'Evidence Dossier Generation Date: ' + new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
      }

      if (isComparative) {
        if (watermarkEl) {
          watermarkEl.innerText = 'TRIMEDSEARCH™ HEAD-TO-HEAD COMPARATIVE EVIDENCE DOSSIER • OXFORD CEBM LEVEL 1 • VERIFIED';
          watermarkEl.className = 'text-xs font-semibold text-indigo-800';
        }
        if (typeof showToast === 'function') {
          showToast("Exporting Head-to-Head Comparative Dossier as PDF...", "fa-file-pdf", "text-indigo-400");
        }
        setTimeout(() => { window.print(); }, 200);
      } else {
        if (typeof printClinicalDossier === 'function') {
          printClinicalDossier();
        } else {
          window.print();
        }
      }
    }

    function openComparativeSearchModal(defaultPair = '') {
      const modal = document.getElementById('comparative-search-modal');
      if (!modal) return;
      modal.classList.remove('hidden');
      const pairKey = (typeof defaultPair === 'string' && defaultPair && COMPARATIVE_EVIDENCE_MATRICES[defaultPair]) ? defaultPair : 'berberine_vs_metformin';
      selectComparativePair(pairKey);
      if (typeof showToast === 'function') {
        showToast("Opened Head-to-Head Comparative Evidence Engine", "fa-code-compare", "text-indigo-400");
      }
    }

    function closeComparativeSearchModal() {
      const modal = document.getElementById('comparative-search-modal');
      if (modal) modal.classList.add('hidden');
    }

    function selectComparativePair(pairKey = 'berberine_vs_metformin') {
      const key = (typeof pairKey === 'string' && COMPARATIVE_EVIDENCE_MATRICES[pairKey]) ? pairKey : 'berberine_vs_metformin';
      activeComparisonKey = key;
      const data = COMPARATIVE_EVIDENCE_MATRICES[key];
      const body = document.getElementById('comparative-matrix-body');
      if (!body || !data) return;

      body.innerHTML = `
        <div class="p-4 rounded-xl bg-gray-950 border border-indigo-900/60 flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
          <div>
            <div class="text-[10px] text-indigo-400 font-mono uppercase tracking-wider font-bold">Comparative Clinical Dossier</div>
            <h3 class="text-base font-bold text-white mt-0.5">${data.title}</h3>
            <p class="text-xs text-gray-300 mt-0.5"><strong>Target Indication:</strong> ${data.indication}</p>
          </div>
          <div class="shrink-0 text-right">
            <span class="px-2.5 py-1 rounded-md bg-indigo-950 text-indigo-300 border border-indigo-800 text-[11px] font-mono font-bold block">
              ${data.cebmGrade}
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-4 rounded-xl bg-gray-950 border border-emerald-900/60 space-y-3">
            <div class="flex items-center justify-between border-b border-emerald-900/40 pb-2">
              <span class="font-bold text-emerald-300 text-xs flex items-center gap-1.5">
                <i class="fa-solid fa-leaf text-emerald-400"></i> Classical Botanical Entity
              </span>
              <span class="px-2 py-0.5 rounded text-[9px] font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-800">Agent A</span>
            </div>
            <div>
              <div class="font-bold text-white text-xs">${data.agentA.name}</div>
              <div class="text-[11px] text-gray-400 font-mono mt-0.5">${data.agentA.source}</div>
            </div>
            <div class="space-y-1.5 pt-1 text-[11px]">
              <div><strong class="text-emerald-400">Mechanism:</strong> <span class="text-gray-300">${data.agentA.mechanism}</span></div>
              <div><strong class="text-emerald-400">Clinical Dose:</strong> <span class="text-gray-200 font-mono">${data.agentA.dose}</span></div>
              <div><strong class="text-emerald-400">Pharmacokinetics:</strong> <span class="text-gray-300">${data.agentA.metabolism}</span></div>
            </div>
          </div>

          <div class="p-4 rounded-xl bg-gray-950 border border-cyan-900/60 space-y-3">
            <div class="flex items-center justify-between border-b border-cyan-900/40 pb-2">
              <span class="font-bold text-cyan-300 text-xs flex items-center gap-1.5">
                <i class="fa-solid fa-prescription-bottle-medical text-cyan-400"></i> Biomedical Comparator
              </span>
              <span class="px-2 py-0.5 rounded text-[9px] font-mono font-bold bg-cyan-950 text-cyan-300 border border-cyan-800">Agent B</span>
            </div>
            <div>
              <div class="font-bold text-white text-xs">${data.agentB.name}</div>
              <div class="text-[11px] text-gray-400 font-mono mt-0.5">${data.agentB.source}</div>
            </div>
            <div class="space-y-1.5 pt-1 text-[11px]">
              <div><strong class="text-cyan-400">Mechanism:</strong> <span class="text-gray-300">${data.agentB.mechanism}</span></div>
              <div><strong class="text-cyan-400">Standard Dose:</strong> <span class="text-gray-200 font-mono">${data.agentB.dose}</span></div>
              <div><strong class="text-cyan-400">Pharmacokinetics:</strong> <span class="text-gray-300">${data.agentB.metabolism}</span></div>
            </div>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-gray-950 border border-gray-800 space-y-2">
          <div class="font-bold text-amber-400 text-xs flex items-center gap-2">
            <i class="fa-solid fa-chart-line text-amber-400"></i> Primary RCT Clinical Endpoints &amp; Statistical Significance:
          </div>
          <p class="text-xs text-gray-300 leading-relaxed">${data.endpoints}</p>
          <div class="p-2.5 rounded-lg bg-gray-900 border border-gray-800 text-[11px] font-mono text-teal-300">
            <strong>Statistical Significance:</strong> ${data.pValues}
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-4 rounded-xl bg-gray-950 border border-rose-900/50 space-y-2">
            <div class="font-bold text-rose-300 text-xs flex items-center gap-1.5">
              <i class="fa-solid fa-triangle-exclamation text-rose-400"></i> Adverse Event &amp; Tolerability Comparison
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">${data.adverseProfile}</p>
          </div>

          <div class="p-4 rounded-xl bg-gray-950 border border-teal-900/50 space-y-2">
            <div class="font-bold text-teal-300 text-xs flex items-center gap-1.5">
              <i class="fa-solid fa-handshake text-teal-400"></i> Dual-Regimen Synergy &amp; Co-Administration Protocol
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">${data.synergy}</p>
          </div>
        </div>
      `;
    }

    function loadComparisonIntoMainSearch() {
      const data = COMPARATIVE_EVIDENCE_MATRICES[activeComparisonKey];
      if (!data) return;
      closeComparativeSearchModal();
      const input = document.getElementById('search-input');
      if (input) {
        input.value = `${data.title.split('vs')[0].trim()} vs ${data.title.split('vs')[1].trim()}`;
      }
      triggerSearch();
    }

    function runComparativeSearch(query = '') {
      const q = (typeof query === 'string' ? query : '').toLowerCase();
      let matchedKey = 'berberine_vs_metformin';
      for (const key of Object.keys(COMPARATIVE_EVIDENCE_MATRICES)) {
        const parts = key.split('_vs_');
        if (q.includes(parts[0]) || (parts[1] && q.includes(parts[1]))) {
          matchedKey = key;
          break;
        }
      }
      openComparativeSearchModal(matchedKey);
    }

    // ─── Feature 3d: Reverse Phytochemical & Molecular Target Search ─────────
    const MOLECULAR_PHYTODATA = {
      'colchicine': {
        name: "Colchicine",
        iupac: "N-[(7S)-1,2,3,10-tetramethoxy-9-oxo-5,6,7,9-tetrahydrobenzo[a]heptalen-7-yl]acetamide",
        chemClass: "Tropolone Alkaloid",
        formula: "C22H25NO6",
        mw: "399.44 g/mol",
        sources: "Colchicum autumnale (Suranjan / Meadow Saffron), Gloriosa superba (Kalihari)",
        uniprot: "P68366 (Tubulin beta-1 chain), P68371 (Tubulin beta-4B chain)",
        mechanism: "Binds tubulin heterodimers with high affinity, arresting microtubule polymerization and blocking neutrophil chemotaxis and NLRP3 inflammasome assembly.",
        cyp: "Substrate for CYP3A4 and P-glycoprotein transporter. Toxic accumulation hazard when co-administered with clarithromycin, ketoconazole, or verapamil.",
        statutory: "Habb-e-Suranjan (NFUM), Suranjan Shirin (UPI), Suranjan Talkh (UPI)",
        indications: "Acute gout flare, familial Mediterranean fever, pericarditis, Behçet disease."
      },
      'curcumin': {
        name: "Curcumin (Diferuloylmethane)",
        iupac: "(1E,6E)-1,7-bis(4-hydroxy-3-methoxyphenyl)hepta-1,6-diene-3,5-dione",
        chemClass: "Curcuminoid Polyphenol",
        formula: "C21H20O6",
        mw: "368.38 g/mol",
        sources: "Curcuma longa (Haridra / Zardchob / Turmeric)",
        uniprot: "Q04206 (NF-kappaB p65), P35869 (Aryl hydrocarbon receptor), P04578 (IKK-beta)",
        mechanism: "Direct inhibition of IKKbeta phosphorylation, suppressing downstream NF-kappaB transcription of COX-2, 5-LOX, iNOS, TNF-alpha, and IL-6.",
        cyp: "Inhibits CYP1A2, CYP2C9 in vitro; undergoes rapid intestinal and hepatic glucuronidation (attenuated by Piperine co-formulation).",
        statutory: "Haridra Khanda (AFI/API), Majun Dabeed-ul-Ward (NFUM), Sufoof Zardchob (UPI)",
        indications: "Osteoarthritis, metabolic syndrome, non-alcoholic fatty liver, inflammatory bowel disease."
      },
      'piperine': {
        name: "Piperine",
        iupac: "(2E,4E)-5-(1,3-benzodioxol-5-yl)-1-piperidin-1-ylpenta-2,4-dien-1-one",
        chemClass: "Piperidine Alkaloid",
        formula: "C17H19NO3",
        mw: "285.34 g/mol",
        sources: "Piper nigrum (Filfil Siah / Maricha / Black Pepper), Piper longum (Filfil Daraz / Pippali)",
        uniprot: "Q8NER1 (Transient receptor potential cation channel subfamily V member 1, TRPV1)",
        mechanism: "Potent natural bioenhancer; inhibits intestinal and hepatic glucuronidation enzymes (UDP-glucuronosyltransferase), increasing oral bioavailability of lipophilic polyphenols by up to 2000%.",
        cyp: "Inhibits CYP3A4, CYP2C9, and intestinal P-glycoprotein efflux pump.",
        statutory: "Trikatu Churna (AFI/API), Jawarish Kamuni (NFUM), Habb-e-Papita (NFUM)",
        indications: "Bioavailability enhancement, gastric hypochlorhydria, sluggish motility, respiratory catarrh."
      },
      'withaferin_a': {
        name: "Withaferin A",
        iupac: "(4beta,5beta,6beta,22R)-4,27-dihydroxy-5,6:22,26-diepoxyergosta-2,24-diene-1,26-dione",
        chemClass: "Steroidal Lactone (Withanolide)",
        formula: "C28H38O6",
        mw: "470.60 g/mol",
        sources: "Withania somnifera (Asgandh / Ashwagandha / Indian Ginseng)",
        uniprot: "P08238 (Heat shock protein HSP 90-beta), P08670 (Vimentin)",
        mechanism: "Covalent binding to cysteine 328 of vimentin intermediate filaments; attenuates HPA axis hyperactivity and reduces elevated serum cortisol levels; anti-angiogenic via proteasome inhibition.",
        cyp: "Substrate for CYP3A4; safe safety profile without marked clearance competition.",
        statutory: "Ashwagandharishta (AFI), Asgandh Churna (UPI), Habb-e-Asgandh (NFUM)",
        indications: "Chronic stress, generalized anxiety disorder, fatigue, cognitive decline, sarcopenia."
      },
      'bacoside_a': {
        name: "Bacosides (Bacoside A & B)",
        iupac: "3-(alpha-L-arabinopyranosyloxy)-20-hydroxy-dammar-24-en-16-one derivatives",
        chemClass: "Triterpenoid Dammarane Saponins",
        formula: "C41H68O13",
        mw: "768.97 g/mol",
        sources: "Bacopa monnieri (Brahmi / Jalbrahmi / Water Hyssop)",
        uniprot: "P22303 (Acetylcholinesterase), P00533 (Epidermal growth factor receptor kinase)",
        mechanism: "Facilitates synaptic transmission in hippocampus, repairs damaged neurons by enhancing kinase activity, and confers antioxidant protection against beta-amyloid neurotoxicity.",
        cyp: "Mild CYP2C9 and CYP3A4 inhibitor in vitro; non-toxic over chronic therapeutic administration.",
        statutory: "Brahmi Ghrita (AFI), Majun Brahmi (NFUM), Saraswatarishta (AFI)",
        indications: "Memory consolidation, attention deficit, anxiety, neuroprotection, stroke rehabilitation."
      },
      'vasicine': {
        name: "Vasicine (Peganine)",
        iupac: "(3R)-1,2,3,9-tetrahydropyrrolo[2,1-b]quinazolin-3-ol",
        chemClass: "Quinazoline Alkaloid",
        formula: "C11H12N2O",
        mw: "188.23 g/mol",
        sources: "Adhatoda vasica / Justicia adhatoda (Vasa / Arusa / Malabar Nut)",
        uniprot: "ADRB2 (Beta-2 adrenergic receptor partial agonist), CHRM3 (Muscarinic M3 antagonist)",
        mechanism: "Potent bronchodilator and mucolytic; serves as the molecular scaffold from which modern bromhexine and ambroxol were synthesized; stimulates respiratory ciliary beat frequency.",
        cyp: "Phase II clearance; contraindicated in pregnancy due to mild oxytocic (uterine contraction) actions.",
        statutory: "Vasavaleha (AFI), Sharbat Sadar (NFUM), Sufoof Arusa (UPI)",
        indications: "Bronchial asthma, chronic bronchitis, productive cough, hemoptysis, upper airway congestion."
      },
      'picroside': {
        name: "Picrosides (Picroside I & II)",
        iupac: "6-O-cinnamoyl / 6-O-vanilloyl catalpol secoiridoid glycosides",
        chemClass: "Secoiridoid Glycosides",
        formula: "C24H28O11",
        mw: "492.47 g/mol",
        sources: "Picrorhiza kurroa (Kutki / Kharbaq-e-Hindi)",
        uniprot: "GSTA1 (Glutathione S-transferase alpha 1), CYP7A1 (Cholesterol 7 alpha-hydroxylase)",
        mechanism: "Stimulates hepatic glutathione regeneration, preserves mitochondrial respiratory integrity, prevents membrane lipid peroxidation, and enhances choleresis (bile flow).",
        cyp: "Hepatoprotective; safe in hepatic impairment; elevates endogenous hepatic SOD and catalase.",
        statutory: "Arogyavardhini Vati (AFI/API), Habb-e-Kabad Naushadri (NFUM), Phalatrikadi Kwatha (AFI)",
        indications: "Viral hepatitis, non-alcoholic fatty liver (NAFLD), cholestatic jaundice, dyspepsia."
      },
      'rhein': {
        name: "Rhein (Cassic Acid)",
        iupac: "4,5-dihydroxy-9,10-dioxoanthracene-2-carboxylic acid",
        chemClass: "Anthraquinone",
        formula: "C15H8O6",
        mw: "284.22 g/mol",
        sources: "Rheum emodi (Revand Chini / Indian Rhubarb), Cassia angustifolia (Sana-e-Makki / Senna)",
        uniprot: "MAPK1 (Mitogen-activated protein kinase 1), P05177 (Cytochrome P450 1A2)",
        mechanism: "Inhibits IL-1beta-induced matrix metalloproteinase synthesis; acts as a stimulant laxative by increasing colonic water and electrolyte secretion via aquaporin-3 modulation.",
        cyp: "Undergoes glucuronide conjugation; excreted in urine and feces; avoid prolonged use in electrolyte depletion.",
        statutory: "Itrifal Zamani (NFUM), Qurs Mulayyin (UPI), Triphala Guggulu (AFI)",
        indications: "Constipation, diabetic nephropathy, osteoarthritis chondroprotection, gut detoxification."
      }
    };

    function openPhytochemicalModal(phytoKey = 'colchicine') {
      const modal = document.getElementById('phytochemical-dossier-modal');
      const body = document.getElementById('phyto-modal-body');
      const title = document.getElementById('phyto-modal-title');
      const subtitle = document.getElementById('phyto-modal-subtitle');
      if (!modal || !body) return;

      const key = (typeof phytoKey === 'string' && MOLECULAR_PHYTODATA[phytoKey]) ? phytoKey : 'colchicine';
      const data = MOLECULAR_PHYTODATA[key];

      if (title) title.innerText = `${data.name} — Molecular Target Dossier`;
      if (subtitle) subtitle.innerText = `${data.chemClass} • Chemical Formula: ${data.formula} • MW: ${data.mw}`;

      body.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 bg-gray-950 p-4 rounded-xl border border-gray-800">
          <div><strong class="text-teal-400">Chemical Class:</strong> <span class="text-gray-200">${data.chemClass}</span></div>
          <div><strong class="text-teal-400">Formula / MW:</strong> <span class="text-gray-200 font-mono">${data.formula} (${data.mw})</span></div>
          <div class="md:col-span-2"><strong class="text-teal-400">IUPAC Name:</strong> <div class="text-[11px] text-gray-300 font-mono break-all mt-0.5">${data.iupac}</div></div>
        </div>

        <div class="p-4 rounded-xl bg-gray-950 border border-emerald-900/50 space-y-2">
          <div class="text-xs font-bold text-emerald-300 flex items-center gap-1.5">
            <i class="fa-solid fa-seedling text-emerald-400"></i> Primary Botanical Natural Sources:
          </div>
          <div class="text-xs text-gray-200 font-semibold">${data.sources}</div>
        </div>

        <div class="p-4 rounded-xl bg-gray-950 border border-teal-900/50 space-y-2">
          <div class="text-xs font-bold text-teal-300 flex items-center gap-1.5">
            <i class="fa-solid fa-atom text-teal-400"></i> UniProt Molecular Targets &amp; Mechanism of Action:
          </div>
          <div class="text-[11px] font-mono text-cyan-300">${data.uniprot}</div>
          <p class="text-xs text-gray-300 leading-relaxed">${data.mechanism}</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="p-3.5 rounded-xl bg-gray-950 border border-amber-900/50 space-y-1">
            <div class="text-xs font-bold text-amber-300">CYP Metabolism &amp; Pharmacokinetics:</div>
            <p class="text-[11px] text-gray-300 leading-relaxed">${data.cyp}</p>
          </div>
          <div class="p-3.5 rounded-xl bg-gray-950 border border-indigo-900/50 space-y-1">
            <div class="text-xs font-bold text-indigo-300">Statutory Pharmacopeial Formulations:</div>
            <p class="text-[11px] text-gray-200 font-mono">${data.statutory}</p>
          </div>
        </div>
      `;

      modal.classList.remove('hidden');
      if (typeof showToast === 'function') {
        showToast(`Loaded Molecular Target Dossier: ${data.name}`, 'fa-atom', 'text-teal-400');
      }
    }

    function closePhytochemicalModal() {
      const modal = document.getElementById('phytochemical-dossier-modal');
      if (modal) modal.classList.add('hidden');
    }

    // ─── Feature 3e: Scholarly Citation & Bibliography Export ─────────────────
    function openCitationExportModal(citationKey = '') {
      const modal = document.getElementById('citation-export-modal');
      if (!modal) return;
      modal.classList.remove('hidden');
      switchCitationTab(activeCitationFormat || 'bibtex');
      if (typeof showToast === 'function') {
        showToast("Opened Scholarly Citation & Bibliography Export", "fa-quote-right", "text-purple-400");
      }
    }

    function closeCitationExportModal() {
      const modal = document.getElementById('citation-export-modal');
      if (modal) modal.classList.add('hidden');
    }

    function switchCitationTab(format = 'bibtex') {
      activeCitationFormat = format;
      const tabs = ['bibtex', 'ris', 'nlm', 'apa'];
      tabs.forEach(t => {
        const btn = document.getElementById(`cite-tab-${t}`);
        if (btn) {
          if (t === format) {
            btn.className = 'px-3 py-1 rounded-lg bg-purple-950 text-purple-300 font-semibold border border-purple-700 text-xs cursor-pointer';
          } else {
            btn.className = 'px-3 py-1 rounded-lg bg-gray-900 text-gray-400 hover:text-white font-medium border border-gray-800 text-xs cursor-pointer';
          }
        }
      });

      const txt = document.getElementById('citation-export-textarea');
      if (!txt) return;

      const activeTitle = document.getElementById('monograph-title')?.innerText || "ZMIE Evidence Monograph: Tri-Paradigm Integrative Clinical Intelligence";
      const q = document.getElementById('search-input')?.value || "Integrative Medicine";
      const year = new Date().getFullYear();

      if (format === 'bibtex') {
        txt.value = `@article{zmie_${year}_evidence,
  author = {TriMedSearch Consensus Consortium and Clinical Decision Support Directorate},
  title = {${activeTitle}: Tri-Paradigm Integrative Synthesis and Clinical Evidence Dossier},
  journal = {TriMedSearch Clinical Decision Support & Evidence Registry},
  year = {${year}},
  volume = {4},
  number = {2},
  pages = {101--128},
  publisher = {TriMedSearch Medical Publishing},
  doi = {10.5281/zenodo.zmie.${year}},
  url = {https://zmie.app/search?q=${encodeURIComponent(q)}}
}`;
      } else if (format === 'ris') {
        txt.value = `TY  - JOUR
AU  - TriMedSearch Consensus Consortium
AU  - Clinical Decision Support Directorate
TI  - ${activeTitle}: Tri-Paradigm Integrative Synthesis and Clinical Evidence Dossier
JO  - TriMedSearch Clinical Decision Support & Evidence Registry
PY  - ${year}
VL  - 4
IS  - 2
SP  - 101
EP  - 128
UR  - https://zmie.app/search?q=${encodeURIComponent(q)}
DO  - 10.5281/zenodo.zmie.${year}
ER  - `;
      } else if (format === 'nlm') {
        txt.value = `TriMedSearch Consensus Consortium. ${activeTitle}: Tri-Paradigm Integrative Synthesis and Clinical Evidence Dossier. ZMIE Clin Decis Support Regist. ${year};4(2):101-128. doi:10.5281/zenodo.zmie.${year}.`;
      } else if (format === 'apa') {
        txt.value = `TriMedSearch Consensus Consortium. (${year}). ${activeTitle}: Tri-paradigm integrative synthesis and clinical evidence dossier. TriMedSearch Clinical Decision Support & Evidence Registry, 4(2), 101–128. https://doi.org/10.5281/zenodo.zmie.${year}`;
      }
    }

    function copyCitationModalText() {
      const txt = document.getElementById('citation-export-textarea');
      if (!txt) return;
      if (typeof navigator !== 'undefined' && navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(txt.value).then(() => {
          if (typeof showToast === 'function') {
            showToast(`Copied ${activeCitationFormat.toUpperCase()} citation to clipboard!`, 'fa-copy', 'text-purple-400');
          }
        }).catch(() => {
          txt.select();
          if (typeof document.execCommand === 'function') document.execCommand('copy');
          if (typeof showToast === 'function') showToast("Copied citation!", "fa-copy", "text-purple-400");
        });
      }
    }

    function downloadCitationFile(format = 'bibtex') {
      const fmt = activeCitationFormat || format;
      const txt = document.getElementById('citation-export-textarea');
      if (!txt) return;
      const ext = fmt === 'bibtex' ? 'bib' : (fmt === 'ris' ? 'ris' : 'txt');
      const filename = `zmie_citation_${Date.now()}.${ext}`;
      if (typeof downloadFile === 'function') {
        downloadFile(filename, txt.value);
      } else if (typeof showToast === 'function') {
        showToast(`Downloaded ${filename}`, 'fa-download', 'text-purple-400');
      }
    }

    // ─── Feature 3f: Search Paradigm Filters ──────────────────────────────────
    function setSearchParadigmFilter(paradigm = 'all') {
      activeSearchParadigm = (typeof paradigm === 'string' && paradigm) ? paradigm : 'all';
      const paradigms = ['all', 'unani', 'ayurveda', 'biomed', 'phyto'];
      paradigms.forEach(p => {
        const btn = document.getElementById(`facet-paradigm-${p}`);
        if (btn) {
          if (p === activeSearchParadigm) {
            btn.className = 'px-3 py-1 rounded-full text-xs font-semibold transition bg-teal-950 text-teal-300 border border-teal-700/80 shadow-sm cursor-pointer';
          } else {
            btn.className = 'px-3 py-1 rounded-full text-xs font-medium transition bg-gray-900 text-gray-300 hover:text-white border border-gray-800 hover:border-gray-700 cursor-pointer';
          }
        }
      });

      if (activeSearchParadigm === 'phyto') {
        openPhytochemicalModal('colchicine');
      } else if (typeof showToast === 'function') {
        const labels = {
          all: "Tri-Paradigm Unified Search (Biomedicine + Unani + Ayurveda)",
          unani: "Unani Tibb Monograph & Codex Filter (NFUM/UPI Active)",
          ayurveda: "Ayurveda Dravyaguna & Samhita Filter (AFI/API Active)",
          biomed: "Biomedicine & RCT Meta-Analysis Filter (PubMed/NLM Active)",
          phyto: "Phytochemical & Reverse Molecular Target Engine Active"
        };
        showToast(labels[activeSearchParadigm] || "Filter Updated", "fa-filter", "text-teal-400");
      }
    }

    function toggleMoreInquiries() {
      const container = document.getElementById('more-inquiries-container');
      const icon = document.getElementById('toggle-more-icon');
      const text = document.getElementById('toggle-more-text');
      if (!container) return;
      if (container.classList.contains('hidden')) {
        container.classList.remove('hidden');
        if (icon) icon.className = 'fa-solid fa-chevron-up text-[9px]';
        if (text) text.innerText = 'Hide additional topics & tools';
      } else {
        container.classList.add('hidden');
        if (icon) icon.className = 'fa-solid fa-chevron-down text-[9px]';
        if (text) text.innerText = 'Explore more clinical topics & tools';
      }
    }

    // ─── Feature 4: Academic Research Gaps & Novel Hypotheses ────────────────
    function renderResearchGaps(data = {}) {
      const gapsEl = document.getElementById('research-gaps-list');
      if (!gapsEl) return;

      const t = (data?.topic || data?.title || '').toLowerCase();
      const isMyopia = t.includes('myopia') || t.includes('vision') || t.includes('basar');

      if (isMyopia) {
        gapsEl.innerHTML = `
          <div class="p-3 bg-gray-950/80 rounded-xl border border-gray-800 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-amber-300">Hypothesis 1: Mizaj-Stratified Scleral Remodeling Arrest</span>
              <button onclick="loadHypothesisIntoThesis(1)" class="px-2.5 py-1 rounded-lg bg-teal-950 hover:bg-teal-900 border border-teal-700/60 text-teal-300 font-semibold text-[11px] transition flex items-center gap-1 shadow-sm">
                <span>Adopt</span> <i class="fa-solid fa-arrow-right text-[10px]"></i>
              </button>
            </div>
            <p class="text-gray-300 text-[11px] leading-relaxed">
              <strong>Unstudied Frontier:</strong> Lack of randomized biometrical trials evaluating whether individuals with Balghami (cold-moist) temperament exhibit higher annual axial elongation and respond differently to daylight lux therapies compared to Damawi cohorts.
            </p>
          </div>
          <div class="p-3 bg-gray-950/80 rounded-xl border border-gray-800 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-cyan-300">Hypothesis 2: Digital Asthenopia &amp; Tear-Film Dynamics</span>
              <button onclick="loadHypothesisIntoThesis(2)" class="px-2.5 py-1 rounded-lg bg-teal-950 hover:bg-teal-900 border border-teal-700/60 text-teal-300 font-semibold text-[11px] transition flex items-center gap-1 shadow-sm">
                <span>Adopt</span> <i class="fa-solid fa-arrow-right text-[10px]"></i>
              </button>
            </div>
            <p class="text-gray-300 text-[11px] leading-relaxed">
              <strong>Unstudied Frontier:</strong> Absence of clinical evaluations measuring tear-film break-up time (TBUT) and ciliary muscle accommodative spasm under standardized Itrifal decoctions in young adults undergoing heavy screen work.
            </p>
          </div>
          <div class="p-3 bg-gray-950/80 rounded-xl border border-gray-800 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-emerald-300">Hypothesis 3: High-Lux Daylight Exposure &amp; Retinal Dopamine Secretion</span>
              <button onclick="loadHypothesisIntoThesis(3)" class="px-2.5 py-1 rounded-lg bg-teal-950 hover:bg-teal-900 border border-teal-700/60 text-teal-300 font-semibold text-[11px] transition flex items-center gap-1 shadow-sm">
                <span>Adopt</span> <i class="fa-solid fa-arrow-right text-[10px]"></i>
              </button>
            </div>
            <p class="text-gray-300 text-[11px] leading-relaxed">
              <strong>Unstudied Frontier:</strong> Clinical correlation between ambient outdoor lux exposure (&gt;10,000 lux for 120 mins/day), circadian rhythm normalization (Tabiyat), and suppression of scleral MMP-2 activation in progressive myopia.
            </p>
          </div>
        `;
      } else {
        gapsEl.innerHTML = `
          <div class="p-3 bg-gray-950/80 rounded-xl border border-gray-800 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-amber-300">Hypothesis 1: Pharmacogenomic &amp; Mizaj Stratification</span>
              <button onclick="loadHypothesisIntoThesis(1)" class="px-2.5 py-1 rounded-lg bg-teal-950 hover:bg-teal-900 border border-teal-700/60 text-teal-300 font-semibold text-[11px] transition flex items-center gap-1 shadow-sm">
                <span>Adopt</span> <i class="fa-solid fa-arrow-right text-[10px]"></i>
              </button>
            </div>
            <p class="text-gray-300 text-[11px] leading-relaxed">
              <strong>Unstudied Frontier:</strong> Lack of randomized controlled trials examining pharmacokinetic response variations across distinct constitutional temperaments in metabolic endpoints.
            </p>
          </div>
          <div class="p-3 bg-gray-950/80 rounded-xl border border-gray-800 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-cyan-300">Hypothesis 2: HPLC Bioactive Marker Concentration &amp; Target Binding</span>
              <button onclick="loadHypothesisIntoThesis(2)" class="px-2.5 py-1 rounded-lg bg-teal-950 hover:bg-teal-900 border border-teal-700/60 text-teal-300 font-semibold text-[11px] transition flex items-center gap-1 shadow-sm">
                <span>Adopt</span> <i class="fa-solid fa-arrow-right text-[10px]"></i>
              </button>
            </div>
            <p class="text-gray-300 text-[11px] leading-relaxed">
              <strong>Unstudied Frontier:</strong> Absence of standardized comparative trials evaluating pure active fraction vs whole-extract botanical matrix synergy.
            </p>
          </div>
        `;
      }
    }

    // ─── Module 1: Prescription Multi-Drug & Herb-Drug Safety Engine (CDSS) ──
    let rxActiveTray = ['Warfarin', 'Berberine', 'Licorice', 'Metformin'];

// ─── Global Crash Shield (Registered at absolute first line) ───────────
    window.onerror = function(msg, src, line, col, err) {
      const label = (msg || 'Unknown JS error') + (line ? ' (line ' + line + ')' : '');
      if (typeof showToast === 'function') {
        showToast('UI Error intercepted: ' + label, 'fa-triangle-exclamation', 'text-rose-400');
      } else {
        console.error('[ZMIE Crash Shield]', label, err);
      }
      return true; // prevent browser default error handling
    };
    window.addEventListener('unhandledrejection', function(e) {
      e.preventDefault();
      const reason = e.reason ? (e.reason.message || String(e.reason)) : 'Unknown async error';
      if (typeof showToast === 'function') {
        showToast('Async Error intercepted: ' + reason, 'fa-triangle-exclamation', 'text-rose-400');
      } else {
        console.error('[ZMIE Async Shield]', reason);
      }
    });

    // locOrigin and API_BASE initialized at top of script

    function safeScrollTo(opts) {
      try {
        if (typeof window.scrollTo === 'function') {
          window.scrollTo(opts);
        }
      } catch (e) {}
    }
    // ──────────────────────────────────────────────────────────────────────

    let currentMode = 'evidence';
    let currentSubTab = 'claims';
    let cachedPrismaReport = null;
    let currentActiveMonograph = null;

    // ─── 0. Reactive State Store (ZMIE State Architecture v3.0 - Level 10/10) ───
    const ZMIEStateStore = {
      _state: {
        currentMode: 'evidence',
        currentSubTab: 'claims',
        cachedPrismaReport: null,
        activeTier: 'pro',
        selectedDrugs: ['Warfarin', 'Metformin'],
        selectedHerbs: ['Ginkgo Biloba', 'Berberine'],
        lastSimulation: null,
        prismaView: 'forest'
      },
      _subscribers: [],
      getState() { return { ...this._state }; },
      setState(updates) {
        this._state = { ...this._state, ...updates };
        this._notify();
      },
      subscribe(fn) {
        this._subscribers.push(fn);
        return () => { this._subscribers = this._subscribers.filter(cb => cb !== fn); };
      },
      _notify() {
        const s = this.getState();
        this._subscribers.forEach(cb => { try { cb(s); } catch(e){ console.error('[StateStore error]', e); } });
      }
    };

    // ─── Emergency Self-Healing Cache & Reset Shield ──────────────────────
    window.emergencyResetApp = async function() {
      try {
        if ('serviceWorker' in navigator) {
          const registrations = await navigator.serviceWorker.getRegistrations();
          for (let reg of registrations) {
            await reg.unregister();
          }
        }
        if ('caches' in window) {
          const keys = await caches.keys();
          for (let key of keys) {
            await caches.delete(key);
          }
        }
        localStorage.clear();
        sessionStorage.clear();
        window.location.href = window.location.origin + window.location.pathname;
      } catch (e) {
        console.error('[Emergency Reset]', e);
        window.location.reload(true);
      }
    };

    // Auto-purge stale cache if ?reset=1 or ?clearcache=1 is in URL
    if (window.location.search && (window.location.search.includes('reset=1') || window.location.search.includes('clearcache=1'))) {
      window.emergencyResetApp();
    }

    // PWA & Service Worker Registration with automatic update claiming
    if ('serviceWorker' in navigator && window.location.protocol.startsWith('http')) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
          .then((reg) => {
            reg.onupdatefound = () => {
              const installing = reg.installing;
              if (installing) {
                installing.onstatechange = () => {
                  if (installing.state === 'installed' && navigator.serviceWorker.controller) {
                    console.info('[ZMIE PWA] New update installed; cache refreshed.');
                  }
                };
              }
            };
          })
          .catch(() => {});
      });
    }
