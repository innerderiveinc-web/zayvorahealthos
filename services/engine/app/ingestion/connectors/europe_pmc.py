"""
ZMIE Ingestion Connector: Europe PMC & PubMed
Europe PMC provides REST APIs for biomedical literature, annotations, full-text open access XML,
and grants from major international funders.
"""

import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.models.source import AuthorityTier, LicenseClass
from app.ingestion.licensing import LicensingIntelligenceEngine
from app.ingestion.connectors.base import BaseSourceConnector


class EuropePMCConnector(BaseSourceConnector):
    BASE_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest"

    def __init__(self):
        super().__init__(
            source_id="SRC-EPMC-001",
            source_name="Europe PMC / PubMed Biomedical Archive",
            authority_tier=AuthorityTier.TIER_B,
            default_license_class=LicenseClass.CLASS_C
        )

    async def discover(self, query: str, limit: int = 10, **kwargs) -> List[Dict[str, Any]]:
        return await self.search_articles(query=query, limit=limit)

    async def search_articles(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Queries Europe PMC REST API.
        """
        self.request_count += 1
        params = {
            "query": query,
            "format": "json",
            "pageSize": limit,
            "resultType": "core"
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(f"{self.BASE_URL}/search", params=params)
                resp.raise_for_status()
                data = resp.json()
                result_list = data.get("resultList", {}).get("result", [])
                
                normalized = []
                for item in result_list:
                    normalized.append(self.normalize(item))
                self.last_sync_time = datetime.utcnow()
                return normalized
        except Exception:
            self.error_count += 1
            raise

    async def identify(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Looks up by PMID or PMCID or DOI in Europe PMC.
        """
        self.request_count += 1
        query = f"EXT_ID:{identifier}" if identifier.isdigit() else f"DOI:{identifier}"
        results = await self.search_articles(query=query, limit=1)
        return results[0] if results else None

    async def fetch_metadata(self, identifier: str) -> Optional[Dict[str, Any]]:
        return await self.identify(identifier)

    async def fetch_document(self, identifier: str) -> Optional[Dict[str, Any]]:
        return await self.identify(identifier)

    async def fetch_updates(self, since: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        query = f"FIRST_PDATE:[{since} TO *]" if since else "sort_date:y"
        return await self.search_articles(query=query, limit=limit)

    def normalize(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return self.normalize_record(item)

    def normalize_record(self, item: Dict[str, Any]) -> Dict[str, Any]:
        is_oa = item.get("isOpenAccess") == "Y"
        in_epmc = item.get("inEPMC") == "Y"
        raw_license = item.get("license")

        license_class = self.check_license(raw_license, is_oa=is_oa)

        doc = {
            "document_id": f"PMID:{item.get('pmid')}" if item.get("pmid") else f"EPMC:{item.get('id')}",
            "pmid": item.get("pmid"),
            "pmcid": item.get("pmcid"),
            "doi": item.get("doi"),
            "title": item.get("title"),
            "authors": [item.get("authorString")] if item.get("authorString") else [],
            "publication_year": int(item.get("pubYear")) if str(item.get("pubYear", "")).isdigit() else None,
            "source_authority_tier": self.authority_tier.value,
            "source_id": self.source_id,
            "external_url": f"https://europepmc.org/article/{item.get('source', 'MED')}/{item.get('id')}",
            "abstract": item.get("abstractText"),
            "is_retracted": item.get("hasRetraction") == "Y",
            "license_class": license_class
        }

        return LicensingIntelligenceEngine.filter_storage_payload(doc, license_class)
