"""
ZMIE Ayurveda Epistemic Ontology Model (Section 6)
Provides first-class representation of classical Ayurvedic concepts:
Prakriti, Vikriti, Dosha, Dhatu, Mala, Agni, Ama, Srotas, Rasa, Guna, Virya, Vipaka, Karma, Dravya, Yoga, Chikitsa.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class DoshaType(str, Enum):
    VATA = "vata"       # Biological kinetic principle (Akasha + Vayu)
    PITTA = "pitta"     # Biological thermal/transformation principle (Tejas + Jala)
    KAPHA = "kapha"     # Biological cohesive/structural principle (Jala + Prithvi)


class AgniState(str, Enum):
    SAMAGNI = "samagni"         # Balanced, optimal digestive fire
    MANDAGNI = "mandagni"       # Sluggish, hypoactive digestive fire (causes Ama)
    TIKSHNAGNI = "tikshnagni"   # Hyperactive, voracious digestive fire
    VISHAMAGNI = "vishamagni"   # Irregular, fluctuating digestive fire


class AyurvedicRasa(str, Enum):
    MADHURA = "madhura"   # Sweet
    AMLA = "amla"         # Sour
    LAVANA = "lavana"     # Salty
    TIKTA = "tikta"       # Bitter
    KATU = "katu"         # Pungent
    KASHAYA = "kashaya"   # Astringent


class AyurvedicVirya(str, Enum):
    USHNA = "ushna"       # Hot potency
    SHITA = "shita"       # Cold potency


class AyurvedicVipaka(str, Enum):
    MADHURA = "madhura"   # Sweet post-digestive effect
    AMLA = "amla"         # Sour post-digestive effect
    KATU = "katu"         # Pungent post-digestive effect


class AyurvedicDravya(BaseModel):
    """
    Dravya: Single Ayurvedic medicinal substance monograph.
    """
    dravya_id: str
    sanskrit_name: str
    devanagari_script: str
    botanical_name: str
    rasa: List[AyurvedicRasa]
    guna: List[str] = Field(..., description="Attributes: e.g. Guru, Laghu, Ruksha, Snigdha")
    virya: AyurvedicVirya
    vipaka: AyurvedicVipaka
    prabhava: Optional[str] = Field(None, description="Inherent unique pharmacological action overriding standard attributes")
    dosha_karma: List[str] = Field(..., description="Action on doshas: e.g. Kaphapitta Shamaka, Vata Vardhaka")
    dhatu_target: List[str] = Field(..., description="Target tissues: Rasa, Rakta, Mamsa, Meda, Asthi, Majja, Shukra")
    srotas_channel: List[str] = Field(..., description="Microcirculatory channels affected: e.g. Annavaha, Rasavaha")
    shodhana: Optional[str] = Field(None, description="Purification or detox process required prior to therapeutic administration")
    classical_reference: str = "Ayurvedic Pharmacopoeia of India (API) Part I / Charaka Samhita"


class AyurvedicYoga(BaseModel):
    """
    Yoga: Ayurvedic compound formulation monograph.
    """
    yoga_id: str
    formula_name: str
    dosage_form: str = Field(..., description="'Vati', 'Taila', 'Ghrita', 'Churna', 'Asava', 'Arishta', 'Bhasma'")
    indications: List[str]
    ingredients: List[str]
    dosha_action: str
    standard_codex: str = "Ayurvedic Formulary of India (AFI)"
