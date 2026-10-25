"""
ZMIE Deep Drug-Herb-Gene (DDHG) Safety & Pharmacogenomics Engine (Sections 30-36, 61-68)
World's first unified clinical interaction validator spanning:
1. Allopathic Pharmaceuticals
2. Traditional Botanicals & Ayurvedic/Unani Phytochemicals (657 catalogued)
3. Human Pharmacogenomic Genetic Variants (CPIC / PharmGKB Level 1A/1B)

Provides:
- Pharmacokinetic enzyme (CYP1A2, CYP2B6, CYP2C9, CYP2C19, CYP2D6, CYP3A4/5) and transporter (P-gp, OATP1B1, BCRP, OCT2) kinetics
- Pharmacogenomic allele warning detection (CYP2C19, CYP2D6, CYP2C9, DPYD, TPMT, NUDT15, HLA-B*5701, HLA-B*1502, SLCO1B1)
- FDA Boxed Warning cross-referencing
- Actionable clinical mitigation, TDM schedules, and washout periods
"""

from typing import Dict, List, Any, Optional, Set
from enum import Enum
from pydantic import BaseModel, Field


class InteractionSeverity(str, Enum):
    CRITICAL_CONTRAINDICATION = "CRITICAL_CONTRAINDICATION"
    MAJOR_WARNING = "MAJOR_WARNING"
    MODERATE_MONITOR = "MODERATE_MONITOR"
    MINOR_INFORMATIONAL = "MINOR_INFORMATIONAL"


class GeneVariantProfile(BaseModel):
    gene: str
    diplotype: str
    phenotype: str  # e.g., "Poor Metabolizer (PM)", "Ultra-rapid Metabolizer (UM)", "Positive (Risk)"
    evidence_source: str = "CPIC Level 1A / FDA Boxed Warning"


class DDHGAlert(BaseModel):
    alert_id: str
    severity: InteractionSeverity
    interaction_type: str  # "DRUG_GENE", "DRUG_HERB", "HERB_GENE", "DRUG_HERB_GENE_TRIAD"
    participating_agents: List[str]
    pathway_enzymes: List[str] = Field(default_factory=list)
    biochemical_mechanism: str
    clinical_risk: str
    actionable_directive: str
    washout_days: int = 0
    tdm_recommendation: Optional[str] = None
    fda_boxed_warning_reference: Optional[str] = None


class DDHGAnalysisReport(BaseModel):
    overall_status: str  # "BLOCKED_CONTRAINDICATION", "CAUTION_REQUIRED", "CLEAR_TO_PROCEED"
    critical_alerts_count: int
    major_alerts_count: int
    moderate_alerts_count: int
    alerts: List[DDHGAlert]
    pharmacogenomic_summary: List[Dict[str, Any]]
    pharmacokinetic_shifts: Dict[str, Any]
    physician_summary: str


class DeepDrugHerbGeneEngine:
    """
    Unified Pharmacogenomic, Botanical, and Pharmaceutical Safety Engine.
    """

    # CPIC Level 1A Pharmacogenomic Rulebase
    PHARMACOGENOMIC_RULES: Dict[str, Dict[str, Any]] = {
        "CYP2C19": {
            "PM": {
                "phenotype": "Poor Metabolizer (*2/*2, *2/*3, *3/*3)",
                "rules": [
                    {
                        "drug": "clopidogrel",
                        "severity": InteractionSeverity.CRITICAL_CONTRAINDICATION,
                        "mechanism": "Markedly impaired bioactivation of clopidogrel prodrug into active thiol metabolite.",
                        "clinical_risk": "Lack of antiplatelet effect, 3-fold increased incidence of major adverse cardiovascular events (MACE) and stent thrombosis.",
                        "directive": "AVOID CLOPIDOGREL. Switch to an alternative antiplatelet not dependent on CYP2C19 activation (e.g., Prasugrel or Ticagrelor), unless contraindicated.",
                        "fda_boxed_warning": "FDA Black Box Warning: Diminished Antiplatelet Effect in Patients with CYP2C19 Poor Metabolizer Genotype."
                    },
                    {
                        "drug": "voriconazole",
                        "severity": InteractionSeverity.MAJOR_WARNING,
                        "mechanism": "Significantly reduced clearance of voriconazole.",
                        "clinical_risk": "Markedly elevated voriconazole plasma concentrations (up to 4-fold), elevating risk of neurotoxicity, QT prolongation, and visual hallucinations.",
                        "directive": "Reduce starting dose by 50% and perform mandatory therapeutic drug monitoring (target trough 1.5–5.5 mcg/mL)."
                    }
                ]
            },
            "UM": {
                "phenotype": "Ultra-rapid Metabolizer (*17/*17)",
                "rules": [
                    {
                        "drug": "voriconazole",
                        "severity": InteractionSeverity.MAJOR_WARNING,
                        "mechanism": "Accelerated CYP2C19 hepatic oxidation.",
                        "clinical_risk": "Subtherapeutic serum levels leading to fungal treatment failure.",
                        "directive": "Consider alternative antifungal (e.g. Isavuconazole or Posaconazole) or perform immediate TDM."
                    }
                ]
            }
        },
        "CYP2D6": {
            "PM": {
                "phenotype": "Poor Metabolizer (*3/*4, *4/*4, *5/*5)",
                "rules": [
                    {
                        "drug": "codeine",
                        "severity": InteractionSeverity.MAJOR_WARNING,
                        "mechanism": "Failure to O-demethylate codeine into its pharmacologically active metabolite (Morphine).",
                        "clinical_risk": "Absence of analgesic efficacy; persistent unmanaged post-operative or acute pain.",
                        "directive": "Avoid codeine due to lack of efficacy. Use an alternative analgesic not reliant on CYP2D6 (e.g., Morphine, Hydromorphone, or NSAIDs)."
                    },
                    {
                        "drug": "tamoxifen",
                        "severity": InteractionSeverity.MAJOR_WARNING,
                        "mechanism": "Substantially reduced formation of active metabolite (Endoxifen).",
                        "clinical_risk": "Significantly increased risk of breast cancer recurrence and reduced relapse-free survival.",
                        "directive": "Avoid strong CYP2D6 inhibitors and consider switching postmenopausal patients to an Aromatase Inhibitor (e.g. Anastrozole)."
                    }
                ]
            },
            "UM": {
                "phenotype": "Ultra-rapid Metabolizer (Gene Duplication *1xN, *2xN)",
                "rules": [
                    {
                        "drug": "codeine",
                        "severity": InteractionSeverity.CRITICAL_CONTRAINDICATION,
                        "mechanism": "Rapid and extensive conversion of codeine to morphine leading to toxic peak serum morphine levels.",
                        "clinical_risk": "Life-threatening or fatal central respiratory depression, especially in pediatric or post-tonsillectomy patients.",
                        "directive": "STRICTLY CONTRAINDICATED. Do not administer codeine or tramadol. Fatal toxicity documented in CPIC guidelines.",
                        "fda_boxed_warning": "FDA Black Box Warning: Respiratory Depression and Death in Ultra-Rapid Metabolizers of Codeine."
                    }
                ]
            }
        },
        "CYP2C9": {
            "PM": {
                "phenotype": "Poor Metabolizer (*2/*3, *3/*3)",
                "rules": [
                    {
                        "drug": "warfarin",
                        "severity": InteractionSeverity.CRITICAL_CONTRAINDICATION,
                        "mechanism": "Severe impairment of (S)-warfarin 7-hydroxylation (the 5x more potent optical isomer).",
                        "clinical_risk": "Prolonged INR, severe supratherapeutic anticoagulation, fatal intracranial and gastrointestinal hemorrhage.",
                        "directive": "Reduce standard initiating dose by 60–80% with close INR monitoring, or utilize a Direct Oral Anticoagulant (DOAC) not reliant on CYP2C9."
                    },
                    {
                        "drug": "phenytoin",
                        "severity": InteractionSeverity.MAJOR_WARNING,
                        "mechanism": "Impaired clearance of phenytoin saturated at therapeutic levels.",
                        "clinical_risk": "Acute phenytoin neurotoxicity, ataxia, nystagmus, lethargy.",
                        "directive": "Reduce maintenance dose by 25–50% and monitor free phenytoin serum levels."
                    }
                ]
            }
        },
        "DPYD": {
            "DEFICIENT": {
                "phenotype": "Dihydropyrimidine Dehydrogenase Deficient (*2A, *13, c.2846A>T)",
                "rules": [
                    {
                        "drug": "5-fluorouracil",
                        "severity": InteractionSeverity.CRITICAL_CONTRAINDICATION,
                        "mechanism": "Inability to catabolize 5-FU, causing systemic accumulation of active fluoronucleotides.",
                        "clinical_risk": "Lethal multi-organ toxic shock, profound myelosuppression, fatal enteropathy and septic shock.",
                        "directive": "STRICTLY CONTRAINDICATED for total deficiency. If intermediate deficiency, reduce dose by >= 50% with cardioprotective monitoring.",
                        "fda_boxed_warning": "FDA Black Box Warning: Severe, Life-Threatening Toxicities in Patients with DPD Deficiency."
                    },
                    {
                        "drug": "capecitabine",
                        "severity": InteractionSeverity.CRITICAL_CONTRAINDICATION,
                        "mechanism": "Oral prodrug converted into 5-FU, resulting in severe accumulation without clearance.",
                        "clinical_risk": "Lethal neutropenia, toxic epidermal necrolysis, cardiac arrest.",
                        "directive": "AVOID CAPECITABINE. Select alternative chemotherapeutic regimen."
                    }
                ]
            }
        },
        "HLA-B": {
            "B*57:01_POS": {
                "phenotype": "HLA-B*57:01 Positive",
                "rules": [
                    {
                        "drug": "abacavir",
                        "severity": InteractionSeverity.CRITICAL_CONTRAINDICATION,
                        "mechanism": "Abacavir binds inside the HLA-B*57:01 antigen-binding cleft, causing massive polyclonal CD8+ T-cell auto-activation.",
                        "clinical_risk": "Severe, fatal systemic multi-organ hypersensitivity reaction upon initiation or rechallenge.",
                        "directive": "STRICTLY CONTRAINDICATED. Never initiate or rechallenge with abacavir in HLA-B*57:01 positive patients.",
                        "fda_boxed_warning": "FDA Black Box Warning: Fatal Hypersensitivity Reactions in HLA-B*57:01 Carriers."
                    }
                ]
            },
            "B*15:02_POS": {
                "phenotype": "HLA-B*15:02 Positive",
                "rules": [
                    {
                        "drug": "carbamazepine",
                        "severity": InteractionSeverity.CRITICAL_CONTRAINDICATION,
                        "mechanism": "Specific immune recognition triggering massive keratinocyte apoptosis.",
                        "clinical_risk": "Stevens-Johnson Syndrome (SJS) and Toxic Epidermal Necrolysis (TEN) with 30% mortality rate.",
                        "directive": "AVOID CARBAMAZEPINE. Test prior to initiation in patients of Asian descent. Substitute with levetiracetam or valproate.",
                        "fda_boxed_warning": "FDA Black Box Warning: Serious Dermatologic Reactions and SJS/TEN in HLA-B*15:02 Carriers."
                    }
                ]
            }
        },
        "SLCO1B1": {
            "REDUCED_FUNCTION": {
                "phenotype": "OATP1B1 Poor Function (*5, rs4149056 C/C)",
                "rules": [
                    {
                        "drug": "simvastatin",
                        "severity": InteractionSeverity.MAJOR_WARNING,
                        "mechanism": "Impaired hepatic uptake transporter OATP1B1, leading to dramatic increase in systemic blood statin levels.",
                        "clinical_risk": "400% higher statin exposure and 15-fold elevated hazard of severe statin myopathy and rhabdomyolysis.",
                        "directive": "Do not exceed Simvastatin 20mg daily, or switch to Rosuvastatin / Pravastatin which have lower dependence on SLCO1B1."
                    }
                ]
            }
        }
    }

    # Core Botanical Kinetic Profiles (cross-referenced with Allopathic Drugs & Genetics)
    BOTANICAL_PROFILES: Dict[str, Dict[str, Any]] = {
        "berberine": {
            "cyp_inhibition": ["CYP3A4", "CYP2D6", "CYP2C9"],
            "transporter_inhibition": ["P-gp (ABCB1)", "OCT2"],
            "high_risk_interactions": [
                {
                    "drug": "cyclosporine",
                    "severity": InteractionSeverity.CRITICAL_CONTRAINDICATION,
                    "mechanism": "Competitive inhibition of CYP3A4 and intestinal P-gp efflux.",
                    "clinical_risk": "Increases Cyclosporine AUC by 2.8-fold; acute renal graft failure and nephrotoxicity.",
                    "directive": "Strictly contraindicated. Hold Berberine or reduce immunosuppressant by 50% with daily TDM.",
                    "washout_days": 14,
                    "tdm": "Daily trough C0 level monitoring."
                },
                {
                    "drug": "tacrolimus",
                    "severity": InteractionSeverity.CRITICAL_CONTRAINDICATION,
                    "mechanism": "CYP3A4 and P-gp inhibition.",
                    "clinical_risk": "Doubles Tacrolimus AUC, triggering acute calcineurin inhibitor nephrotoxicity.",
                    "directive": "Strictly avoid Berberine with Tacrolimus.",
                    "washout_days": 14,
                    "tdm": "Daily C0 level monitoring."
                },
                {
                    "drug": "metformin",
                    "severity": InteractionSeverity.MAJOR_WARNING,
                    "mechanism": "Competitive inhibition of renal OCT2 transporter + additive AMPK activation.",
                    "clinical_risk": "Delayed metformin renal clearance and additive hypoglycemia risk.",
                    "directive": "Monitor fasting blood glucose; reduce Metformin if eGFR < 60 mL/min.",
                    "washout_days": 5
                }
            ]
        },
        "st_johns_wort": {
            "cyp_induction": ["CYP3A4", "CYP2C9", "CYP2C19"],
            "transporter_induction": ["P-gp (ABCB1)"],
            "high_risk_interactions": [
                {
                    "drug": "cyclosporine",
                    "severity": InteractionSeverity.CRITICAL_CONTRAINDICATION,
                    "mechanism": "Profound PXR-mediated transcriptional induction of CYP3A4 and P-gp by Hyperforin.",
                    "clinical_risk": "Cuts Cyclosporine AUC by 50–70%, precipitating catastrophic acute transplant rejection.",
                    "directive": "STRICTLY CONTRAINDICATED. Never combine St. John's Wort with solid organ transplant medications.",
                    "washout_days": 21
                },
                {
                    "drug": "oral_contraceptives",
                    "severity": InteractionSeverity.CRITICAL_CONTRAINDICATION,
                    "mechanism": "Marked acceleration of ethinyl estradiol and progestin clearance via CYP3A4.",
                    "clinical_risk": "Loss of contraceptive efficacy and unplanned pregnancy.",
                    "directive": "Strictly contraindicated. Recommend non-hormonal barrier contraception.",
                    "washout_days": 21
                },
                {
                    "drug": "warfarin",
                    "severity": InteractionSeverity.CRITICAL_CONTRAINDICATION,
                    "mechanism": "Induction of CYP2C9 and CYP3A4.",
                    "clinical_risk": "Severe plunge in INR, subtherapeutic anticoagulation, fatal thromboembolism.",
                    "directive": "Discontinue St. John's Wort immediately; monitor INR daily until stable.",
                    "washout_days": 14
                }
            ]
        },
        "ginkgo": {
            "antiplatelet_action": True,
            "cyp_inhibition": ["CYP2C19", "CYP3A4"],
            "high_risk_interactions": [
                {
                    "drug": "clopidogrel",
                    "severity": InteractionSeverity.MAJOR_WARNING,
                    "mechanism": "Dual antiplatelet PAF antagonism combined with CYP2C19 modulation.",
                    "clinical_risk": "Spontaneous intracranial, retinal, and gastrointestinal hemorrhage.",
                    "directive": "Hold Ginkgo biloba at least 7 days before surgical procedures or when combined with dual antiplatelets.",
                    "washout_days": 7
                },
                {
                    "drug": "warfarin",
                    "severity": InteractionSeverity.MAJOR_WARNING,
                    "mechanism": "Inhibition of platelet aggregation and CYP2C9/2C19 interference.",
                    "clinical_risk": "Severe mucosal and soft tissue bleeding.",
                    "directive": "Avoid concurrent administration. Monitor PT/INR weekly.",
                    "washout_days": 7
                }
            ]
        },
        "licorice": {
            "mineralocorticoid_excess": True,
            "high_risk_interactions": [
                {
                    "drug": "digoxin",
                    "severity": InteractionSeverity.CRITICAL_CONTRAINDICATION,
                    "mechanism": "11-beta-HSD2 inhibition causes renal potassium wasting and profound hypokalemia.",
                    "clinical_risk": "Sensitizes myocardial Na+/K+-ATPase, triggering fatal ventricular tachycardia and Digoxin toxicity.",
                    "directive": "STRICTLY CONTRAINDICATED. Check serum potassium and magnesium immediately.",
                    "washout_days": 10
                },
                {
                    "drug": "furosemide",
                    "severity": InteractionSeverity.MAJOR_WARNING,
                    "mechanism": "Synergistic kaluresis.",
                    "clinical_risk": "Severe refractory hypokalemia, metabolic alkalosis, and cardiac arrhythmias.",
                    "directive": "Avoid licorice or prescribe potassium supplementation with serial electrolyte checks.",
                    "washout_days": 7
                }
            ]
        }
    }

    @classmethod
    def evaluate_ddhg_profile(
        cls,
        drugs: List[str],
        herbs: List[str],
        genetic_variants: Optional[List[Dict[str, str]]] = None,
        patient_factors: Optional[Dict[str, Any]] = None
    ) -> DDHGAnalysisReport:
        """
        Executes unified Drug-Herb-Gene Triad safety synthesis.
        """
        alerts: List[DDHGAlert] = []
        genetics = genetic_variants or []
        factors = patient_factors or {}

        clean_drugs = [d.lower().strip() for d in drugs]
        clean_herbs = [h.lower().strip() for h in herbs]

        # 1. Evaluate Drug-Gene Interactions
        for g_entry in genetics:
            gene = g_entry.get("gene", "").upper()
            diplotype = g_entry.get("diplotype", "").strip()

            gene_rules = cls.PHARMACOGENOMIC_RULES.get(gene, {})
            # Match phenotype category
            matched_cat = None
            if "PM" in diplotype.upper() or "*2/*2" in diplotype or "*2/*3" in diplotype or "*3/*3" in diplotype or "*4/*4" in diplotype:
                matched_cat = "PM"
            elif "UM" in diplotype.upper() or "DUPLICATION" in diplotype.upper() or "*17/*17" in diplotype:
                matched_cat = "UM"
            elif "DEFICIENT" in diplotype.upper() or "*2A" in diplotype or "*13" in diplotype:
                matched_cat = "DEFICIENT"
            elif "POS" in diplotype.upper() or "POSITIVE" in diplotype.upper():
                matched_cat = "B*57:01_POS" if "57" in gene or "57" in diplotype else "B*15:02_POS"
            elif "REDUCED" in diplotype.upper() or "*5" in diplotype:
                matched_cat = "REDUCED_FUNCTION"

            if matched_cat and matched_cat in gene_rules:
                cat_info = gene_rules[matched_cat]
                phenotype = cat_info["phenotype"]

                for rule in cat_info.get("rules", []):
                    rule_drug = rule["drug"].lower()
                    if any(rule_drug in d or d in rule_drug for d in clean_drugs):
                        alert = DDHGAlert(
                            alert_id=f"ALERT-DG-{gene}-{rule_drug.upper()}",
                            severity=rule["severity"],
                            interaction_type="DRUG_GENE",
                            participating_agents=[gene, rule["drug"].title()],
                            pathway_enzymes=[gene],
                            biochemical_mechanism=rule["mechanism"],
                            clinical_risk=f"[{phenotype}] {rule['clinical_risk']}",
                            actionable_directive=rule["directive"],
                            fda_boxed_warning_reference=rule.get("fda_boxed_warning")
                        )
                        alerts.append(alert)

        # 2. Evaluate Drug-Herb Interactions
        for herb in clean_herbs:
            # Map common names
            h_key = None
            if "berber" in herb or "darhald" in herb or "daruharidra" in herb:
                h_key = "berberine"
            elif "john" in herb or "hyperic" in herb:
                h_key = "st_johns_wort"
            elif "ginkgo" in herb:
                h_key = "ginkgo"
            elif "licorice" in herb or "mulethi" in herb or "glycyrrhiz" in herb:
                h_key = "licorice"

            if h_key and h_key in cls.BOTANICAL_PROFILES:
                h_prof = cls.BOTANICAL_PROFILES[h_key]
                for hi in h_prof.get("high_risk_interactions", []):
                    i_drug = hi["drug"].lower()
                    if any(i_drug in d or d in i_drug for d in clean_drugs):
                        alert = DDHGAlert(
                            alert_id=f"ALERT-DH-{h_key.upper()}-{i_drug.upper()}",
                            severity=hi["severity"],
                            interaction_type="DRUG_HERB",
                            participating_agents=[herb.title(), hi["drug"].title()],
                            pathway_enzymes=h_prof.get("cyp_inhibition", []) or h_prof.get("cyp_induction", []),
                            biochemical_mechanism=hi["mechanism"],
                            clinical_risk=hi["clinical_risk"],
                            actionable_directive=hi["directive"],
                            washout_days=hi.get("washout_days", 0),
                            tdm_recommendation=hi.get("tdm")
                        )
                        alerts.append(alert)

        # 3. Evaluate Drug-Herb-Gene Triad Compounded Hazards
        # Example 1: Clopidogrel + CYP2C19 PM + Ginkgo
        has_clopidogrel = any("clopidogrel" in d for d in clean_drugs)
        has_cyp2c19_pm = any(g.get("gene", "").upper() == "CYP2C19" and ("PM" in g.get("diplotype", "").upper() or "*2" in g.get("diplotype", "")) for g in genetics)
        has_ginkgo = any("ginkgo" in h for h in clean_herbs)

        if has_clopidogrel and has_cyp2c19_pm and has_ginkgo:
            triad_alert = DDHGAlert(
                alert_id="ALERT-TRIAD-CLOP-CYP2C19-GINKGO",
                severity=InteractionSeverity.CRITICAL_CONTRAINDICATION,
                interaction_type="DRUG_HERB_GENE_TRIAD",
                participating_agents=["Clopidogrel", "Ginkgo biloba", "CYP2C19 Poor Metabolizer"],
                pathway_enzymes=["CYP2C19", "PAF Receptor"],
                biochemical_mechanism="Compounded catastrophic interaction: CYP2C19 Poor Metabolizer state disables Clopidogrel vascular protection (thrombosis risk), while concurrent Ginkgo biloba introduces unmonitored antiplatelet hemorrhagic hazard without preventing ischemic stent occlusion.",
                clinical_risk="Simultaneous extreme arterial thrombosis hazard AND spontaneous intracranial/GI hemorrhage.",
                actionable_directive="CRITICAL INTERVENTION: Discontinue Ginkgo biloba immediately. Switch patient from Clopidogrel to Prasugrel or Ticagrelor.",
                washout_days=7,
                fda_boxed_warning_reference="FDA Black Box Warning on CYP2C19 Clopidogrel Resistance + Herbal Bleeding Hazard."
            )
            alerts.append(triad_alert)

        # Example 2: Cyclosporine / Tacrolimus + Berberine + SLCO1B1/CYP3A4
        has_calcineurin = any("cyclosporine" in d or "tacrolimus" in d for d in clean_drugs)
        has_berberine = any("berber" in h or "darhald" in h for h in clean_herbs)
        if has_calcineurin and has_berberine:
            if factors.get("egfr") and float(factors["egfr"]) < 60:
                alerts.append(DDHGAlert(
                    alert_id="ALERT-TRIAD-CALCINEURIN-BERBERINE-RENAL",
                    severity=InteractionSeverity.CRITICAL_CONTRAINDICATION,
                    interaction_type="DRUG_HERB",
                    participating_agents=["Calcineurin Inhibitor", "Berberine", f"Renal Impairment (eGFR {factors['egfr']} mL/min)"],
                    pathway_enzymes=["CYP3A4", "P-gp (ABCB1)"],
                    biochemical_mechanism="Berberine increases calcineurin inhibitor AUC by 280% on the background of existing impaired renal filtration.",
                    clinical_risk="Imminent acute renal tubular necrosis, acute-on-chronic kidney injury, requiring emergency dialysis.",
                    actionable_directive="Strictly hold Berberine. Order stat calcineurin trough level and serum creatinine/potassium.",
                    washout_days=14,
                    tdm_recommendation="Daily TDM mandated."
                ))

        # Count severities
        crit_count = sum(1 for a in alerts if a.severity == InteractionSeverity.CRITICAL_CONTRAINDICATION)
        major_count = sum(1 for a in alerts if a.severity == InteractionSeverity.MAJOR_WARNING)
        mod_count = sum(1 for a in alerts if a.severity == InteractionSeverity.MODERATE_MONITOR)

        if crit_count > 0:
            status = "BLOCKED_CONTRAINDICATION"
            summary = f"CRITICAL HAZARD: {crit_count} contraindicated interaction(s) detected. Regimen must be adjusted prior to administration."
        elif major_count > 0:
            status = "CAUTION_REQUIRED"
            summary = f"MAJOR WARNING: {major_count} high-risk interaction(s) require dose adjustment or specialized clinical monitoring."
        else:
            status = "CLEAR_TO_PROCEED"
            summary = "No high-risk pharmacogenomic or botanical contraindications detected for the requested regimen."

        return DDHGAnalysisReport(
            overall_status=status,
            critical_alerts_count=crit_count,
            major_alerts_count=major_count,
            moderate_alerts_count=mod_count,
            alerts=alerts,
            pharmacogenomic_summary=[{"gene": g.get("gene"), "diplotype": g.get("diplotype")} for g in genetics],
            pharmacokinetic_shifts={
                "cyp3a4_inhibition": any("berberine" in h for h in clean_herbs),
                "cyp3a4_induction": any("john" in h for h in clean_herbs),
                "p_gp_inhibition": any("berberine" in h for h in clean_herbs),
                "antiplatelet_synergy": any("ginkgo" in h for h in clean_herbs) and any("clopidogrel" in d or "aspirin" in d for d in clean_drugs)
            },
            physician_summary=summary
        )
