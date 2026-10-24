"""
ZMIE Qarabadeen Polyherbal Formulation Engine
Provides querying, ingredient decomposition, and multi-component safety screening
for the 50 classical compound formulations (Murakkabat) from the Unani & Ayurvedic pharmacopoeias.
"""

from typing import List, Dict, Any, Optional
import os
import json
import logging
import re

logger = logging.getLogger("zmie.sources.qarabadeen")


class QarabadeenEngine:
    """Master engine for polyherbal compound formulations and multi-component interaction screening."""

    _instance: Optional["QarabadeenEngine"] = None

    def __init__(self, data_path: Optional[str] = None):
        self._data_path = data_path or self._resolve_path()
        self._formulations: Dict[str, Dict[str, Any]] = {}
        self._load_corpus()

    @classmethod
    def get_instance(cls) -> "QarabadeenEngine":
        if cls._instance is None:
            cls._instance = QarabadeenEngine()
        return cls._instance

    def _resolve_path(self) -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
        p = os.path.join(base_dir, "services", "data", "qarabadeen_master_library.json")
        if os.path.exists(p):
            return p
        alt = "services/data/qarabadeen_master_library.json"
        return alt

    def _load_corpus(self) -> None:
        if not os.path.exists(self._data_path):
            logger.warning("Qarabadeen data file not found at %s", self._data_path)
            return

        try:
            with open(self._data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            forms = data.get("formulations", [])
            for item in forms:
                key = item.get("compound_key")
                if key:
                    self._formulations[key] = item
            logger.info("Loaded %d classical polyherbal formulations into QarabadeenEngine", len(self._formulations))
        except Exception as e:
            logger.error("Failed to load Qarabadeen master library: %s", str(e))

    def list_all_keys(self) -> List[str]:
        return list(self._formulations.keys())

    def get_formulation(self, compound_key: str) -> Optional[Dict[str, Any]]:
        return self._formulations.get(compound_key)

    def search_formulations(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Searches across compound keys, titles, transliterated names, and indications."""
        q = query.lower().strip()
        tokens = [t for t in re.findall(r'[a-zA-Z0-9_\-]+', q) if len(t) >= 3 and t not in ["evaluate", "formulation", "interactions", "with", "from", "and", "the"]]
        matches = []
        for key, form in self._formulations.items():
            title = form.get("canonical_title", "").lower()
            trans = form.get("transliterated_name", "").lower()
            category = form.get("therapeutic_category", "").lower()
            inds = [str(x).lower() for x in form.get("primary_indications", [])]
            ingredients = [str(x.get("ingredient", "")).lower() for x in form.get("key_ingredients", [])]

            score = 0
            if q in key or q in trans or q in title:
                score += 20

            for tok in tokens:
                if tok in key:
                    score += 8
                if tok in trans:
                    score += 8
                if tok in title:
                    score += 6
                if any(tok in i for i in inds):
                    score += 4
                if any(tok in ing for ing in ingredients):
                    score += 3
                if tok in category:
                    score += 2

            if score > 0:
                matches.append((score, form))

        matches.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in matches[:limit]]

    def extract_constituent_botanicals(self, compound_key: str) -> List[str]:
        """Extracts cleaned individual botanical common and latin names from a formulation."""
        form = self.get_formulation(compound_key)
        if not form:
            return []

        botanicals = []
        for ing in form.get("key_ingredients", []):
            raw = ing.get("ingredient", "")
            # e.g. "Gul-e-Surkh (Rosa damascena petals)" -> "Rosa damascena", "Gul-e-Surkh"
            if "(" in raw and ")" in raw:
                main_part = raw[:raw.index("(")].strip()
                inner_part = raw[raw.index("(") + 1:raw.index(")")].strip()
                botanicals.append(main_part)
                botanicals.append(inner_part)
            else:
                botanicals.append(raw.strip())
        return list(dict.fromkeys(botanicals))

    def screen_compound_safety(self, compound_key: str, modern_drugs: List[str]) -> Dict[str, Any]:
        """
        Decomposes the polyherbal compound into its constituent botanical components
        and screens each against modern drugs via SafetyAgent.
        """
        form = self.get_formulation(compound_key)
        if not form:
            return {
                "compound_key": compound_key,
                "found": False,
                "interactions": [],
                "summary": "Formulation not found in master library."
            }

        constituents = self.extract_constituent_botanicals(compound_key)
        interactions = []

        try:
            from app.agents.safety_agent import SafetyIntelligenceEngine
            for herb in constituents:
                assessment = SafetyIntelligenceEngine.evaluate_safety(
                    entity=herb,
                    concurrent_medications=modern_drugs
                )
                if assessment.safety_status.value in ["HIGH_RISK", "CONTRAINDICATED", "MODERATE_RISK", "CRITICAL_HAZARD", "CAUTION"]:
                    interactions.append({
                        "constituent_herb": herb,
                        "modern_drugs": modern_drugs,
                        "severity": assessment.safety_status.value,
                        "mechanism": getattr(assessment, "clinical_summary", "Metabolic clearance modulation"),
                        "recommendation": getattr(assessment, "clinical_summary", "Monitor clinical parameters.")
                    })
        except Exception as e:
            logger.warning("Safety screening error for compound %s: %s", compound_key, str(e))

        return {
            "compound_key": compound_key,
            "found": True,
            "canonical_title": form.get("canonical_title"),
            "transliterated_name": form.get("transliterated_name"),
            "temperament": form.get("temperament"),
            "total_constituents_evaluated": len(constituents),
            "interactions_found_count": len(interactions),
            "interactions": interactions,
            "classical_safety_note": form.get("safety_and_precautions", "Follow classical NFUM dosage guidance.")
        }


_engine_singleton: Optional[QarabadeenEngine] = None

def get_qarabadeen_engine() -> QarabadeenEngine:
    global _engine_singleton
    if _engine_singleton is None:
        _engine_singleton = QarabadeenEngine.get_instance()
    return _engine_singleton
