"""
ZMIE Clinical Drug-Herb Pharmacokinetic Firewall
Provides instant, allopathic-grade pharmacokinetic and pharmacodynamic hazard evaluation
for traditional botanicals and dravyas when co-administered with modern pharmaceuticals.

Covers:
- Phase I Cytochrome P450 Enzymes (CYP3A4, CYP2C9, CYP2C19, CYP2D6, CYP1A2)
- Transporters: P-glycoprotein (ABCB1), OATP1B1, BCRP, OCT2
- High-Risk Allopathic Drug Classes: Statins, Anticoagulants, Immunosuppressants,
  Oral Hypoglycemics, Sedatives/Anxiolytics, Antiarrhythmics, Chemotherapy.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class DrugHerbAlert(BaseModel):
    severity: str  # "CRITICAL_CONTRAINDICATION", "MAJOR_WARNING", "MODERATE_MONITOR"
    interacting_drug_class: str
    specific_allopathic_drugs: List[str]
    cyp_transporter_pathway: str
    biochemical_mechanism: str
    black_box_clinical_hazard: str
    physician_actionable_directive: str
    washout_window_days: int
    tdm_requirement: Optional[str] = None


class AllopathicDrugHerbFirewall:
    """
    Deterministic clinical decision support module translating botanical bioactives
    into actionable modern biomedical pharmacokinetic hazard profiles for physicians.
    """

    HERB_HAZARD_REGISTRY: Dict[str, List[Dict[str, Any]]] = {
        # 1. Berberis aristata / Berberine / Daruharidra
        "berberine": [
            {
                "severity": "CRITICAL_CONTRAINDICATION",
                "interacting_drug_class": "Calcineurin Inhibitor Immunosuppressants",
                "specific_allopathic_drugs": ["Cyclosporine", "Tacrolimus"],
                "cyp_transporter_pathway": "CYP3A4 Reversible Inhibition + Intestinal P-gp (ABCB1) Efflux Blockade",
                "biochemical_mechanism": "Berberine competitively inhibits CYP3A4 and intestinal P-glycoprotein, impairing presystemic first-pass clearance.",
                "black_box_clinical_hazard": "Surge in calcineurin inhibitor AUC by 2.5–3.0 fold, triggering acute nephrotoxicity, hyperkalemia, and solid organ graft failure.",
                "physician_actionable_directive": "Strictly contraindicated. If co-administered, mandatory daily C0 trough TDM; reduce immunosuppressant dose by 50–60%.",
                "washout_window_days": 14,
                "tdm_requirement": "Daily Cyclosporine/Tacrolimus C0 trough blood concentration monitoring."
            },
            {
                "severity": "MAJOR_WARNING",
                "interacting_drug_class": "HMG-CoA Reductase Inhibitors (Statins)",
                "specific_allopathic_drugs": ["Atorvastatin", "Simvastatin", "Lovastatin"],
                "cyp_transporter_pathway": "Hepatic CYP3A4 + OATP1B1 Hepatic Uptake Inhibition",
                "biochemical_mechanism": "Inhibition of CYP3A4-mediated statin lactone oxidation and OATP1B1 influx.",
                "black_box_clinical_hazard": "Plasma statin AUC elevated by ~70–90%, dramatically amplifying risk of statin-induced myopathy and fatal rhabdomyolysis.",
                "physician_actionable_directive": "Monitor serum creatine kinase (CK). Consider temporary statin dose reduction (e.g. Atorvastatin 20mg -> 10mg) or switch to non-CYP3A4 Pravastatin.",
                "washout_window_days": 7,
                "tdm_requirement": "Baseline and 2-week serum Creatine Kinase (CK) and AST/ALT."
            },
            {
                "severity": "MAJOR_WARNING",
                "interacting_drug_class": "Biguanides & Oral Hypoglycemics",
                "specific_allopathic_drugs": ["Metformin", "Glimepiride", "Gliclazide", "Insulin"],
                "cyp_transporter_pathway": "Renal OCT2 Transporter Competition + Additive AMPK / SUR1 Activation",
                "biochemical_mechanism": "Berberine independently activates AMPK and delays renal excretion of Metformin via OCT2.",
                "black_box_clinical_hazard": "Profound additive hypoglycemia and heightened risk of Metformin-associated lactic acidosis in elderly patients.",
                "physician_actionable_directive": "Intensify home self-monitoring of blood glucose (SMBG). Dose-titrate Metformin downward by 25–50% upon Berberine initiation.",
                "washout_window_days": 5,
                "tdm_requirement": "Frequent capillary blood glucose logs (pre-prandial and 2h post-prandial)."
            }
        ],

        # 2. Glycyrrhiza glabra / Mulethi / Licorice / Asl-us-Soos
        "glycyrrhiza": [
            {
                "severity": "CRITICAL_CONTRAINDICATION",
                "interacting_drug_class": "Cardiac Glycosides & Loop / Thiazide Diuretics",
                "specific_allopathic_drugs": ["Digoxin", "Furosemide", "Hydrochlorothiazide"],
                "cyp_transporter_pathway": "Renal 11-beta-Hydroxysteroid Dehydrogenase Type 2 (11-beta-HSD2) Inhibition",
                "biochemical_mechanism": "Glycyrrhetinic acid inhibits 11-beta-HSD2, preventing conversion of active cortisol to inactive cortisone in distal tubules. Cortisol floods mineralocorticoid receptors.",
                "black_box_clinical_hazard": "Pseudohyperaldosteronism: profound hypokalemia, sodium retention, and severe hypertension. In patients on Digoxin, hypokalemia dramatically provokes fatal Digoxin toxicity and ventricular fibrillation.",
                "physician_actionable_directive": "Strictly contraindicated with Digoxin or kaliuretic diuretics. If co-administered, mandatory weekly serum potassium (K+) check.",
                "washout_window_days": 21,
                "tdm_requirement": "Weekly serum electrolytes (K+, Na+) and Digoxin trough level (< 0.9 ng/mL)."
            },
            {
                "severity": "MAJOR_WARNING",
                "interacting_drug_class": "Antihypertensive Agents (ACEi / ARB / CCB)",
                "specific_allopathic_drugs": ["Ramipril", "Telmisartan", "Amlodipine"],
                "cyp_transporter_pathway": "Mineralocorticoid Receptor Volume Expansion",
                "biochemical_mechanism": "Volume-dependent antagonism of blood pressure control via renal sodium retention.",
                "black_box_clinical_hazard": "Loss of blood pressure control, rebound hypertensive urgency, and peripheral edema.",
                "physician_actionable_directive": "Discontinue Mulethi / Licorice in patients with uncontrolled essential hypertension.",
                "washout_window_days": 14,
                "tdm_requirement": "Ambulatory blood pressure monitoring."
            }
        ],

        # 3. Withania somnifera / Ashwagandha / Asgandh
        "ashwagandha": [
            {
                "severity": "MAJOR_WARNING",
                "interacting_drug_class": "Benzodiazepines, Non-Benzodiazepine Hypnotics & Barbiturates",
                "specific_allopathic_drugs": ["Lorazepam", "Alprazolam", "Clonazepam", "Zolpidem"],
                "cyp_transporter_pathway": "GABA-A Receptor Allosteric Modulation",
                "biochemical_mechanism": "Withanolides exert direct positive allosteric modulation at GABA-A receptor sites, matching sedative pharmacodynamics.",
                "black_box_clinical_hazard": "Excessive central nervous system depression, severe psychomotor slowing, daytime somnolence, and respiratory depression hazard.",
                "physician_actionable_directive": "Advise patient to avoid concurrent ingestion before driving. Reduce bedtime sedative dose by 50% under supervision.",
                "washout_window_days": 7,
                "tdm_requirement": "Clinical Glasgow Coma Scale / Epworth Sleepiness Scale evaluation."
            },
            {
                "severity": "MAJOR_WARNING",
                "interacting_drug_class": "Synthetic Thyroid Hormones",
                "specific_allopathic_drugs": ["Levothyroxine (T4)", "Liothyronine (T3)"],
                "cyp_transporter_pathway": "Hepatic Iodothyronine 5'-Deiodinase Stimulation",
                "biochemical_mechanism": "Ashwagandha stimulates endogenous thyroid hormone synthesis and peripheral T4 to T3 conversion.",
                "black_box_clinical_hazard": "Iatrogenic thyrotoxicosis: resting tachycardia, palpitations, heat intolerance, and cardiac arrhythmias.",
                "physician_actionable_directive": "Re-check serum TSH, Free T3, and Free T4 4 weeks after initiating Ashwagandha; titrate Levothyroxine dose downward.",
                "washout_window_days": 14,
                "tdm_requirement": "Serum TSH and Free T4 panel at 4 weeks."
            }
        ],

        # 4. Curcuma longa / Turmeric / Curcumin / Haridra
        "curcumin": [
            {
                "severity": "CRITICAL_CONTRAINDICATION",
                "interacting_drug_class": "Vitamin K Antagonists & Direct Oral Anticoagulants (DOACs)",
                "specific_allopathic_drugs": ["Warfarin", "Apixaban", "Rivaroxaban", "Dabigatran"],
                "cyp_transporter_pathway": "CYP2C9 Mild Inhibition + Platelet Anti-aggregatory Eicosanoid Inhibition",
                "biochemical_mechanism": "Curcuminoids suppress thromboxane A2 synthesis and inhibit CYP2C9 metabolism of S-warfarin.",
                "black_box_clinical_hazard": "Prolongation of prothrombin time, International Normalized Ratio (INR) supratherapeutic spike (> 4.5), and severe gastrointestinal hemorrhage.",
                "physician_actionable_directive": "Hold high-dose standardized Curcumin extract (> 1g/day) in patients on Warfarin or DOACs. Monitor INR weekly.",
                "washout_window_days": 10,
                "tdm_requirement": "Weekly INR monitoring for Warfarin; monitor for microscopic hematuria/ecchymosis."
            },
            {
                "severity": "MAJOR_WARNING",
                "interacting_drug_class": "Anticancer Chemotherapy (Topoisomerase & Camptothecin)",
                "specific_allopathic_drugs": ["Irinotecan", "Doxorubicin", "Paclitaxel"],
                "cyp_transporter_pathway": "Intestinal BCRP (ABCG2) & P-gp Transporter Modulation",
                "biochemical_mechanism": "Curcumin alters drug efflux transporters and free radical cytotoxic cascades in neoplastic cells.",
                "black_box_clinical_hazard": "Potential attenuation of chemotherapy-induced tumor apoptosis or exacerbated systemic mucosal toxicity.",
                "physician_actionable_directive": "Discontinue high-dose Curcumin supplementation 48 hours prior to and during active chemotherapy infusion cycles.",
                "washout_window_days": 7,
                "tdm_requirement": "Oncologist multidisciplinary sign-off."
            }
        ],

        # 5. Zingiber officinale / Ginger / Zanjabeel / Shunthi
        "ginger": [
            {
                "severity": "MAJOR_WARNING",
                "interacting_drug_class": "Antiplatelet Agents",
                "specific_allopathic_drugs": ["Aspirin", "Clopidogrel", "Ticagrelor"],
                "cyp_transporter_pathway": "Cyclooxygenase-1 (COX-1) & Thromboxane Synthase Competitive Inhibition",
                "biochemical_mechanism": "Gingerols inhibit platelet thromboxane B2 (TXB2) production.",
                "black_box_clinical_hazard": "Additive inhibition of platelet aggregation, prolonged bleeding time, and increased perioperative hemorrhage risk.",
                "physician_actionable_directive": "Mandatory discontinuation of medicinal Ginger extract 7 days prior to elective surgical or dental procedures.",
                "washout_window_days": 7,
                "tdm_requirement": "Bleeding time and complete blood count with platelets."
            }
        ],

        # 6. Commiphora mukul / Guggulu / Muqil
        "guggulu": [
            {
                "severity": "MAJOR_WARNING",
                "interacting_drug_class": "Oral Estrogen-Progestin Contraceptives & Beta-Blockers",
                "specific_allopathic_drugs": ["Ethinylestradiol", "Propranolol", "Diltiazem"],
                "cyp_transporter_pathway": "Hepatic CYP3A4 Enzyme Induction (Pregnane X Receptor PXR Activation)",
                "biochemical_mechanism": "Guggulsterones act as PXR agonists, upregulating hepatic CYP3A4 expression and accelerating drug clearance.",
                "black_box_clinical_hazard": "Subtherapeutic plasma concentrations of oral contraceptives (hazard of unintended pregnancy) and loss of antihypertensive control.",
                "physician_actionable_directive": "Advise barrier contraception when on therapeutic Guggulu. Re-assess blood pressure and heart rate.",
                "washout_window_days": 14,
                "tdm_requirement": "Clinical therapeutic efficacy tracking."
            }
        ],

        # 7. Tinospora cordifolia / Guduchi / Gilo
        "guduchi": [
            {
                "severity": "MAJOR_WARNING",
                "interacting_drug_class": "Oral Hypoglycemic Agents & Systemic Immunosuppressants",
                "specific_allopathic_drugs": ["Metformin", "Prednisone", "Azathioprine"],
                "cyp_transporter_pathway": "Immunostimulatory Macrophage Activation + Pancreatic Beta-Cell Sensitization",
                "biochemical_mechanism": "Polysaccharide fractions stimulate humoral immunity while enhancing peripheral glucose uptake.",
                "black_box_clinical_hazard": "Potential antagonism of therapeutic immunosuppression in autoimmune flareups; additive hypoglycemic hazard.",
                "physician_actionable_directive": "Avoid in active organ transplantation or severe lupus nephritis without specialist approval. Monitor SMBG.",
                "washout_window_days": 7,
                "tdm_requirement": "Blood glucose log and ESR / hs-CRP monitoring."
            }
        ],

        # 8. Allium sativum / Garlic / Seer / Lasuna
        "garlic": [
            {
                "severity": "CRITICAL_CONTRAINDICATION",
                "interacting_drug_class": "Anticoagulants & Protease Inhibitors",
                "specific_allopathic_drugs": ["Warfarin", "Saquinavir", "Atazanavir"],
                "cyp_transporter_pathway": "CYP2C9 / CYP3A4 Induction & Irreversible Platelet Aggregation Inhibition",
                "biochemical_mechanism": "Allicin metabolites irreversibly inhibit platelet aggregation for the lifespan of the platelet (7–10 days).",
                "black_box_clinical_hazard": "Major spontaneous hemorrhagic episodes (retroperitoneal, subdural); profound reduction in protease inhibitor AUC.",
                "physician_actionable_directive": "Hold garlic extracts at least 10–14 days prior to any surgery. Strict avoidance with HIV protease inhibitors.",
                "washout_window_days": 14,
                "tdm_requirement": "INR monitoring and pre-op coagulation panel."
            }
        ],

        # 9. Cassia angustifolia / Senna / Sana Makki
        "senna": [
            {
                "severity": "MAJOR_WARNING",
                "interacting_drug_class": "Cardiac Glycosides, Antiarrhythmics & Corticosteroids",
                "specific_allopathic_drugs": ["Digoxin", "Amiodarone", "Prednisolone"],
                "cyp_transporter_pathway": "Intestinal Colonic Secretory Fluid & Potassium Depletion",
                "biochemical_mechanism": "Sennosides induce severe colonic peristalsis and mucosal fluid secretion, causing rapid potassium loss.",
                "black_box_clinical_hazard": "Hypokalemia-induced Torsades de Pointes or fatal Digoxin toxicity.",
                "physician_actionable_directive": "Never use Senna chronically (> 7 consecutive days). Always check serum potassium in elderly or cardiac patients.",
                "washout_window_days": 3,
                "tdm_requirement": "Serum potassium (K+) check."
            }
        ],

        # 10. Hypericum perforatum / St. John's Wort / Hufariqun
        "hypericum": [
            {
                "severity": "CRITICAL_CONTRAINDICATION",
                "interacting_drug_class": "Calcineurin Inhibitors, Protease Inhibitors, OCPs & DOACs",
                "specific_allopathic_drugs": ["Cyclosporine", "Tacrolimus", "Warfarin", "Rivaroxaban", "Ethinylestradiol"],
                "cyp_transporter_pathway": "Potent Hepatic/Intestinal CYP3A4, CYP2C9 & P-gp (ABCB1) Induction (PXR Activation)",
                "biochemical_mechanism": "Hyperforin is a high-affinity ligand for the Pregnane X Receptor (PXR), dramatically upregulating CYP3A4 and P-gp efflux pump expression.",
                "black_box_clinical_hazard": "Catastrophic plunge in plasma drug concentrations (50–80% AUC reduction), causing solid organ transplant rejection, breakthrough pregnancy, or fatal thromboembolic stroke.",
                "physician_actionable_directive": "Absolute clinical contraindication. If previously ingested, delay organ transplant or restart therapeutic drug monitoring after 14-day clearance.",
                "washout_window_days": 14,
                "tdm_requirement": "Mandatory trough levels for Cyclosporine/Tacrolimus; INR for Warfarin."
            },
            {
                "severity": "CRITICAL_CONTRAINDICATION",
                "interacting_drug_class": "Selective Serotonin Reuptake Inhibitors (SSRIs) & SNRIs",
                "specific_allopathic_drugs": ["Sertraline", "Fluoxetine", "Escitalopram", "Venlafaxine"],
                "cyp_transporter_pathway": "Central Synaptic Serotonin Reuptake Inhibition",
                "biochemical_mechanism": "Hyperforin and hypericin synergistically block neuronal 5-HT reuptake, compounding SSRI pharmacodynamics.",
                "black_box_clinical_hazard": "Fatal Serotonin Syndrome: hyperthermia, autonomic instability, neuromuscular rigidity, clonus, and cardiovascular collapse.",
                "physician_actionable_directive": "Strictly prohibit concurrent use. Emergency intervention: discontinue all serotonergic agents, administer Cyproheptadine 12mg, active cooling.",
                "washout_window_days": 14,
                "tdm_requirement": "Sternbach / Hunter Serotonin Toxicity Criteria evaluation."
            }
        ],

        # 11. Ginkgo biloba / Maidenhair Tree
        "ginkgo": [
            {
                "severity": "CRITICAL_CONTRAINDICATION",
                "interacting_drug_class": "Antiplatelets, Anticoagulants & Thrombolytics",
                "specific_allopathic_drugs": ["Warfarin", "Aspirin", "Clopidogrel", "Apixaban"],
                "cyp_transporter_pathway": "Platelet-Activating Factor (PAF) Antagonism + Mild CYP2C19 Inhibition",
                "biochemical_mechanism": "Ginkgolides A and B competitively antagonize platelet surface PAF receptors, halting ADP-induced platelet aggregation.",
                "black_box_clinical_hazard": "Spontaneous hyphema (anterior chamber ocular bleed), subdural hematoma, and perioperative hemorrhagic shock.",
                "physician_actionable_directive": "Mandatory discontinuation at least 14 days prior to elective surgery. Avoid concurrent dual-antiplatelet or anticoagulation therapy.",
                "washout_window_days": 14,
                "tdm_requirement": "Pre-operative coagulation panel and platelet function assay."
            }
        ],

        # 12. Rauwolfia serpentina / Sarpagandha / Asrol
        "rauwolfia": [
            {
                "severity": "CRITICAL_CONTRAINDICATION",
                "interacting_drug_class": "Monoamine Oxidase Inhibitors (MAOIs) & Central Antihypertensives",
                "specific_allopathic_drugs": ["Phenelzine", "Tranylcypromine", "Clonidine", "Methyldopa"],
                "cyp_transporter_pathway": "Vesicular Monoamine Transporter 2 (VMAT2) Irreversible Blockade",
                "biochemical_mechanism": "Reserpine irreversibly inhibits VMAT2, causing massive initial catecholamine release followed by permanent peripheral/central biogenic amine depletion.",
                "black_box_clinical_hazard": "Severe refractory hypotension, profound bradycardia, acute major depressive episode with suicidal ideation, or paradox hypertensive crisis with MAOIs.",
                "physician_actionable_directive": "Absolute contraindication in depression or with MAOIs. Washout period must extend to 21 days due to slow VMAT vesicle turnover.",
                "washout_window_days": 21,
                "tdm_requirement": "Continuous ECG and ambulatory blood pressure monitoring; psychiatric screening."
            }
        ],

        # 13. Aconitum heterophyllum / Vatsanabha / Atis / Bish
        "aconitum": [
            {
                "severity": "CRITICAL_CONTRAINDICATION",
                "interacting_drug_class": "Antiarrhythmics, Digoxin & QT-Prolonging Pharmacotherapies",
                "specific_allopathic_drugs": ["Digoxin", "Amiodarone", "Flecainide", "Sotalol"],
                "cyp_transporter_pathway": "Cardiac Voltage-Gated Sodium Channels (Nav1.5) Prolonged Activation",
                "biochemical_mechanism": "Aconitine binds to site 2 of voltage-gated Na+ channels, holding them open in an un-inactivated state, provoking intracellular calcium overload.",
                "black_box_clinical_hazard": "Bidirectional ventricular tachycardia, polymorphic VT, ventricular fibrillation, and sudden asystolic cardiac arrest. Mandates Ayurvedic Shodhana before any medicinal use.",
                "physician_actionable_directive": "Strictly contraindicated without verified Ayurvedic/Unani statutory Shodhana (Cow milk/Cow urine boiling). If intoxicated: ICU admission, atropine, amiodarone, ECMO.",
                "washout_window_days": 30,
                "tdm_requirement": "12-lead continuous telemetry ECG and serum cardiac troponin."
            }
        ],

        # 14. Strychnos nux-vomica / Kuchla / Azaraqi
        "strychnos": [
            {
                "severity": "CRITICAL_CONTRAINDICATION",
                "interacting_drug_class": "Neuromuscular Blockers, Anxiolytics & Anticonvulsants",
                "specific_allopathic_drugs": ["Phenytoin", "Levetiracetam", "Baclofen", "Diazepam"],
                "cyp_transporter_pathway": "Spinal Post-Synaptic Glycine Receptor (GlyR) Competitive Antagonism",
                "biochemical_mechanism": "Strychnine competitively blocks inhibitory glycine receptors in spinal motor neurons, causing unchecked sensory-to-motor reflex hyperexcitability.",
                "black_box_clinical_hazard": "Painful tetanic convulsions, opisthotonos, riso sardonicus, and asphyxiation from diaphragmatic spasm while fully conscious. Requires mandatory Tadbeer/Shodhana.",
                "physician_actionable_directive": "Never use unpurified seeds. Hospital management: dark quiet room, IV Diazepam/Lorazepam, neuromuscular paralysis with mechanical ventilation.",
                "washout_window_days": 14,
                "tdm_requirement": "Clinical neuromuscular reflex and arterial blood gas monitoring."
            }
        ],

        # 15. Silybum marianum / Milk Thistle
        "silybum": [
            {
                "severity": "MAJOR_WARNING",
                "interacting_drug_class": "Hepatic CYP2C9 & P-gp Substrates",
                "specific_allopathic_drugs": ["Warfarin", "Losartan", "Glipizide"],
                "cyp_transporter_pathway": "Reversible Hepatic CYP2C9 & P-gp Efflux Inhibition",
                "biochemical_mechanism": "Silibinin moderately inhibits CYP2C9 oxidation of S-warfarin and alters biliary glucuronidation.",
                "black_box_clinical_hazard": "Modest INR prolongation and amplified risk of hypoglycemia with sulfonylureas.",
                "physician_actionable_directive": "Monitor INR baseline and 1 week post-initiation in patients on Warfarin.",
                "washout_window_days": 7,
                "tdm_requirement": "Prothrombin Time / INR."
            }
        ],

        # 16. Gymnema sylvestre / Gurmar
        "gymnema": [
            {
                "severity": "MAJOR_WARNING",
                "interacting_drug_class": "Sulfonylureas, Meglitinides & Exogenous Insulin",
                "specific_allopathic_drugs": ["Glimepiride", "Glipizide", "Insulin Glargine", "Repaglinide"],
                "cyp_transporter_pathway": "Pancreatic Islet Beta-Cell Permeability & Peripheral Influx Stimulation",
                "biochemical_mechanism": "Gymnemic acids enhance endogenous insulin secretion and increase glucose utilization.",
                "black_box_clinical_hazard": "Severe neuroglycopenic hypoglycemia (blood glucose < 54 mg/dL), diaphoretic syncope, and hypoglycemic seizures.",
                "physician_actionable_directive": "Dose-titrate sulfonylurea downward by 25–50% upon initiating Gurmar; mandatory capillary blood glucose logs.",
                "washout_window_days": 5,
                "tdm_requirement": "Frequent self-monitoring of blood glucose (SMBG)."
            }
        ]
    }

    # Generic Fallback Rule Generator for herbs without specialized profiles
    DEFAULT_BOTANICAL_PROFILE = [
        {
            "severity": "MODERATE_MONITOR",
            "interacting_drug_class": "Narrow Therapeutic Index Medications",
            "specific_allopathic_drugs": ["Warfarin", "Levothyroxine", "Digoxin", "Lithium"],
            "cyp_transporter_pathway": "Potential Phase I/II Hepatic Enzyme Competition",
            "biochemical_mechanism": "Unfractionated phytochemical complexes can compete with hepatic clearance or alter intestinal transit time.",
            "black_box_clinical_hazard": "Potential minor alteration of plasma drug steady-state concentrations.",
            "physician_actionable_directive": "Separate ingestion by at least 2 hours. Monitor baseline biomarkers and clinical symptoms.",
            "washout_window_days": 5,
            "tdm_requirement": "Standard periodic therapeutic drug monitoring."
        }
    ]

    @classmethod
    def get_clinical_firewall_report(cls, herb_key_or_name: str) -> Dict[str, Any]:
        """
        Returns full structured Allopathic Clinical Safety & Drug-Herb Interaction report.
        """
        k = herb_key_or_name.lower().strip()
        matched_alerts = []

        # Find direct or substring match
        for registered_key, alerts in cls.HERB_HAZARD_REGISTRY.items():
            if registered_key in k or k in registered_key:
                matched_alerts = alerts
                break

        if not matched_alerts:
            # Check common botanical botanical keys
            if any(term in k for term in ["daruharidra", "darhald", "rasaut", "barberry"]):
                matched_alerts = cls.HERB_HAZARD_REGISTRY["berberine"]
            elif any(term in k for term in ["mulethi", "asl", "soos", "licorice", "yashti"]):
                matched_alerts = cls.HERB_HAZARD_REGISTRY["glycyrrhiza"]
            elif any(term in k for term in ["asgandh", "withania", "somnifera"]):
                matched_alerts = cls.HERB_HAZARD_REGISTRY["ashwagandha"]
            elif any(term in k for term in ["haldi", "turmeric", "haridra", "curcuma"]):
                matched_alerts = cls.HERB_HAZARD_REGISTRY["curcumin"]
            elif any(term in k for term in ["adrak", "sonth", "shunthi", "zanjabeel"]):
                matched_alerts = cls.HERB_HAZARD_REGISTRY["ginger"]
            elif any(term in k for term in ["muqil", "guggul", "commiphora"]):
                matched_alerts = cls.HERB_HAZARD_REGISTRY["guggulu"]
            elif any(term in k for term in ["gilo", "giloy", "guduchi", "amrita"]):
                matched_alerts = cls.HERB_HAZARD_REGISTRY["guduchi"]
            elif any(term in k for term in ["lasun", "garlic", "seer", "lahsun"]):
                matched_alerts = cls.HERB_HAZARD_REGISTRY["garlic"]
            elif any(term in k for term in ["sana", "senna", "sanai"]):
                matched_alerts = cls.HERB_HAZARD_REGISTRY["senna"]
            else:
                matched_alerts = cls.DEFAULT_BOTANICAL_PROFILE

        highest_severity = "MODERATE_MONITOR"
        for a in matched_alerts:
            if a["severity"] == "CRITICAL_CONTRAINDICATION":
                highest_severity = "CRITICAL_CONTRAINDICATION"
                break
            elif a["severity"] == "MAJOR_WARNING" and highest_severity != "CRITICAL_CONTRAINDICATION":
                highest_severity = "MAJOR_WARNING"

        # High-level physician summary
        summary = (
            f"CLINICAL DECISION SUPPORT ALERT [{highest_severity}]: "
            f"This botanical exerts pharmacodynamically active constituents with documented "
            f"liability on hepatic Cytochrome P450 enzymes and/or ABC/SLC drug transporters. "
            f"Attending physicians should review concurrent allopathic regimens for {matched_alerts[0]['interacting_drug_class']}."
        )

        return {
            "herb_key": herb_key_or_name,
            "overall_clinical_hazard_level": highest_severity,
            "physician_clinical_advisory": summary,
            "primary_metabolic_enzymes_affected": list(set([a["cyp_transporter_pathway"].split()[0] for a in matched_alerts])),
            "high_risk_drug_classes": [a["interacting_drug_class"] for a in matched_alerts],
            "specific_high_risk_drugs": sum([a["specific_allopathic_drugs"] for a in matched_alerts], []),
            "mandatory_washout_period_days": max([a["washout_window_days"] for a in matched_alerts]),
            "interaction_alerts": matched_alerts
        }
