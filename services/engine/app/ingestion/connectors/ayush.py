"""
ZMIE Traditional Medicine Connector: AYUSH Research Portal & Classical Corpus
Connects to India's Ministry of Ayush research corpus (Ayurveda, Yoga & Naturopathy, Unani, Siddha, Homoeopathy).
Preserves classical codex metadata, drug formulation terms, and evidence tiers.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.models.source import AuthorityTier, LicenseClass
from app.models.claim import MedicalSystem
from app.ingestion.connectors.base import BaseSourceConnector


class AYUSHResearchConnector(BaseSourceConnector):
    SOURCE_ID = "SRC-AYUSH-IN-001"
    AUTHORITY_TIER = AuthorityTier.TIER_A # Official Ministry of Ayush Portal

    def __init__(self):
        super().__init__(
            source_id=self.SOURCE_ID,
            source_name="Ministry of Ayush National Research Portal & Pharmacopoeias",
            authority_tier=self.AUTHORITY_TIER,
            default_license_class=LicenseClass.CLASS_B
        )

    async def discover(self, query: str, limit: int = 10, **kwargs) -> List[Dict[str, Any]]:
        self.request_count += 1
        query_l = query.lower()
        results = []
        for codex in self.get_canonical_sources():
            matches = any(query_l in str(v).lower() for v in codex.values())
            if matches:
                results.append(self.normalize(codex))
        self.last_sync_time = datetime.utcnow()
        return results[:limit]

    async def identify(self, identifier: str) -> Optional[Dict[str, Any]]:
        self.request_count += 1
        for codex in self.get_canonical_sources():
            if identifier.lower() in codex.get("codex_name", "").lower():
                return self.normalize(codex)
        return None

    async def fetch_metadata(self, identifier: str) -> Optional[Dict[str, Any]]:
        return await self.identify(identifier)

    async def fetch_document(self, identifier: str) -> Optional[Dict[str, Any]]:
        return await self.identify(identifier)

    async def fetch_updates(self, since: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        return [self.normalize(c) for c in self.get_canonical_sources()[:limit]]

    @classmethod
    def get_canonical_sources(cls) -> List[Dict[str, Any]]:
        """
        Returns authorized classical codices and official national pharmacopoeias.
        """
        return [
            {
                "system": MedicalSystem.UNANI.value,
                "codex_name": "Al-Qanun fi al-Tibb (The Canon of Medicine)",
                "author": "Ibn Sina (Avicenna)",
                "authority_tier": AuthorityTier.TIER_E.value,
                "focus": ["Mizaj", "Afaal", "Mufradat", "Murakkabat", "Humoral Pathology"]
            },
            {
                "system": MedicalSystem.UNANI.value,
                "codex_name": "National Formulary of Unani Medicine (NFUM)",
                "publisher": "Ministry of Ayush, Govt of India",
                "authority_tier": AuthorityTier.TIER_A.value,
                "focus": ["Compound Formulations", "Standardized Posology", "Safety Monograph"]
            },
            {
                "system": MedicalSystem.AYURVEDA.value,
                "codex_name": "Charaka Samhita",
                "author": "Maharshi Charaka / Agnivesha",
                "authority_tier": AuthorityTier.TIER_E.value,
                "focus": ["Dosha", "Dhatus", "Prakriti", "Chikitsa Sthana"]
            },
            {
                "system": MedicalSystem.AYURVEDA.value,
                "codex_name": "Ayurvedic Pharmacopoeia of India (API)",
                "publisher": "Pharmacopoeia Commission for Indian Medicine",
                "authority_tier": AuthorityTier.TIER_A.value,
                "focus": ["Single Drugs (Dravya)", "Standardization", "Identity & Purity"]
            }
        ]

    def normalize(self, item: Dict[str, Any]) -> Dict[str, Any]:
        if "codex_name" in item:
            return {
                "document_id": f"CODEX:{item['codex_name'].replace(' ', '_')[:30]}",
                "source_id": self.source_id,
                "title": item["codex_name"],
                "authors": [item.get("author") or item.get("publisher", "Official")],
                "system": item.get("system"),
                "source_authority_tier": item.get("authority_tier", self.authority_tier.value),
                "license_class": LicenseClass.CLASS_B.value,
                "notice": "Official National Ayush / Canonical Codex",
                "focus": item.get("focus", [])
            }
        return self.normalize_ayush_article(item)

    @classmethod
    def normalize_ayush_article(cls, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Structures an empirical research paper originating from AYUSH clinical research institutes (CCRIMH, CCRUM, CCRAS).
        """
        return {
            "document_id": f"AYUSH:{item.get('record_id')}",
            "source_id": cls.SOURCE_ID,
            "title": item.get("title"),
            "system": item.get("system", "unani"),
            "authors": item.get("authors", []),
            "publication_year": item.get("year"),
            "study_type": item.get("study_type", "clinical_trial"),
            "intervention": item.get("formulation_or_herb"),
            "condition": item.get("target_disease"),
            "source_authority_tier": cls.AUTHORITY_TIER.value if isinstance(cls.AUTHORITY_TIER, AuthorityTier) else cls.AUTHORITY_TIER,
            "license_class": LicenseClass.CLASS_B.value,
            "abstract": item.get("abstract")
        }
