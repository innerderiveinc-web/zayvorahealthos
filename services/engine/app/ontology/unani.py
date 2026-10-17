"""
ZMIE Unani Tibb Epistemic Ontology Model (Section 5)
Provides first-class representation of classical Greco-Arab medical concepts
without reductive flattening into modern biomedical terminology.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class MizajClassification(str, Enum):
    DAMWI = "damwi"                 # Sanguine: Hot & Moist (Harr Ratab)
    SAFRAWI = "safrawi"             # Choleric: Hot & Dry (Harr Yabis)
    BALGHAMI = "balghami"           # Phlegmatic: Cold & Moist (Barid Ratab)
    SAWDAWI = "sawdawi"             # Melancholic: Cold & Dry (Barid Yabis)
    MOTADIL = "motadil"             # Balanced / Equable (Mizaj-e-Adil)


class KhiltType(str, Enum):
    DAM = "dam"                     # Blood (Air element / Hot & Moist)
    SAFRA = "safra"                 # Yellow Bile (Fire element / Hot & Dry)
    BALGHAM = "balgham"             # Phlegm (Water element / Cold & Moist)
    SAWDA = "sawda"                 # Black Bile (Earth element / Cold & Dry)


class QuwwatType(str, Enum):
    QUWWAT_E_TABIYYA = "quwwat_e_tabiyya"       # Natural / Vegetative Faculty (Nutrition, Growth)
    QUWWAT_E_HAZIMA = "quwwat_e_hazima"         # Digestive Faculty (Stomach & Liver)
    QUWWAT_E_HAYWANIYYA = "quwwat_e_haywaniyya" # Vital Faculty (Heart, Circulation, Respiration)
    QUWWAT_E_NAFSANIYYA = "quwwat_e_nafsaniyya" # Psychic / Nervous Faculty (Brain, Sensation, Movement)
    QUWWAT_E_MUDABBIRA = "quwwat_e_mudabbira"   # Innate Self-Healing / Homeostatic Nature (Tabiat)


class UnaniDegree(str, Enum):
    DARJA_AWWAL = "darja_awwal"     # 1st Degree: Action imperceptible in health, therapeutic in illness
    DARJA_DOM = "darja_dom"         # 2nd Degree: Perceptible physiological action, non-toxic
    DARJA_SOM = "darja_som"         # 3rd Degree: Strong physiological perturbation, potent drug
    DARJA_CHAHARUM = "darja_chaharum"# 4th Degree: Highly toxic or lethal without corrective (Muslih)


class UnaniMizajEntity(BaseModel):
    mizaj_id: str
    classification: MizajClassification
    qualities: List[str] = Field(..., description="e.g. ['Harr', 'Ratab'] (Hot & Moist)")
    physiological_tendencies: List[str] = Field(default_factory=list)
    vulnerabilities: List[str] = Field(default_factory=list)
    classical_codex: str = "Al-Qanun fi al-Tibb, Book I"


class UnaniMufradDawa(BaseModel):
    """
    Mufradat: Single natural drug monograph.
    """
    drug_id: str
    canonical_unani_name: str
    original_script: str
    botanical_or_mineral_name: str
    mizaj_qualities: List[str]
    darja: UnaniDegree
    afaal: List[str] = Field(..., description="Pharmacological actions (e.g. Daf-e-Taffun, Muhallil, Musaffi)")
    therapeutic_uses: List[str]
    muslih: Optional[str] = Field(None, description="Corrective agent mitigating side effects (e.g. Kateera, Honey)")
    badal: Optional[str] = Field(None, description="Substitute drug with analogous temperament and actions")
    standard_dosage: str


class UnaniMurakkabFormula(BaseModel):
    """
    Murakkabat: Compound formulation monograph.
    """
    formula_id: str
    canonical_name: str
    original_script: str
    dosage_form: str = Field(..., description="'Majun', 'Khamira', 'Itrifal', 'Sharbat', 'Arq', 'Habb'")
    primary_indication: str
    key_constituents: List[str]
    afaal: List[str]
    mizaj_summary: str
    standard_source: str = "National Formulary of Unani Medicine (NFUM)"


class AsbabSittaZarooriya(BaseModel):
    """
    The Six Essential Prerequisites of Health in Unani Medicine.
    """
    factor_name: str
    original_arabic: str
    clinical_guideline: str
