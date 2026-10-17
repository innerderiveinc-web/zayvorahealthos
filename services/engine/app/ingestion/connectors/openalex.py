"""
ZMIE Ingestion Connector: OpenAlex
Handles querying and normalizing scholarly objects from OpenAlex (320M+ works corpus)
with strict licensing classification and author/source provenance.
"""

import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.models.source import AuthorityTier, LicenseClass
from app.ingestion.licensing import LicensingIntelligenceEngine
from app.ingestion.connectors.base import BaseSourceConnector


class OpenAlexConnector(BaseSourceConnector):
    BASE_URL = "https://api.openalex.org"

    def __init__(self, mailto: str = "engineering@zmie.org"):
        super().__init__(
            source_id="SRC-OPENALEX-001",
            source_name="OpenAlex Global Scholarly Graph",
            authority_tier=AuthorityTier.TIER_D,
            default_license_class=LicenseClass.CLASS_C
        )
        self.headers = {
            "User-Agent": f"ZMIE-Knowledge-Engine/1.0 (mailto:{mailto})"
        }

    async def discover(self, query: str, limit: int = 10, **kwargs) -> List[Dict[str, Any]]:
        filter_oa = kwargs.get("filter_oa", False)
        return await self.search_works(query=query, limit=limit, filter_oa=filter_oa)

    async def search_works(self, query: str, limit: int = 10, filter_oa: bool = False) -> List[Dict[str, Any]]:
        """
        Searches OpenAlex works with biomedical and clinical filters.
        """
        self.request_count += 1
        params = {
            "search": query,
            "per-page": limit,
            "sort": "relevance_score:desc"
        }
        if filter_oa:
            params["filter"] = "is_oa:true"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(f"{self.BASE_URL}/works", params=params, headers=self.headers)
                resp.raise_for_status()
                data = resp.json()
                results = []
                for item in data.get("results", []):
                    results.append(self.normalize(item))
                self.last_sync_time = datetime.utcnow()
                return results
        except Exception:
            self.error_count += 1
            raise

    async def identify(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Resolves DOI or OpenAlex Work ID (e.g. W12345678 or https://doi.org/10.1016/...)
        """
        self.request_count += 1
        clean_id = identifier.replace("https://openalex.org/", "").replace("https://doi.org/", "")
        lookup = f"https://doi.org/{clean_id}" if "10." in clean_id else clean_id
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(f"{self.BASE_URL}/works/{lookup}", headers=self.headers)
                if resp.status_code == 404:
                    return None
                resp.raise_for_status()
                return self.normalize(resp.json())
        except Exception:
            self.error_count += 1
            return None

    async def fetch_metadata(self, identifier: str) -> Optional[Dict[str, Any]]:
        return await self.identify(identifier)

    async def fetch_document(self, identifier: str) -> Optional[Dict[str, Any]]:
        return await self.identify(identifier)

    async def fetch_updates(self, since: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Fetches recently modified works from OpenAlex.
        """
        self.request_count += 1
        params = {
            "per-page": limit,
            "sort": "publication_date:desc"
        }
        if since:
            params["filter"] = f"from_publication_date:{since}"
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(f"{self.BASE_URL}/works", params=params, headers=self.headers)
                resp.raise_for_status()
                data = resp.json()
                return [self.normalize(item) for item in data.get("results", [])]
        except Exception:
            self.error_count += 1
            return []

    def normalize(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return self.normalize_work(item)

    def normalize_work(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maps OpenAlex raw JSON to ZMIE internal document schema with licensing class.
        """
        open_access = item.get("open_access", {})
        is_oa = open_access.get("is_oa", False)
        oa_status = open_access.get("oa_status")
        
        primary_location = item.get("primary_location") or {}
        raw_license = primary_location.get("license") or oa_status

        license_class = self.check_license(raw_license, is_oa=is_oa)

        doc = {
            "document_id": item.get("id"),
            "doi": item.get("doi"),
            "title": item.get("title"),
            "publication_year": item.get("publication_year"),
            "authors": [a.get("author", {}).get("display_name") for a in item.get("authorships", [])],
            "primary_source_name": primary_location.get("source", {}).get("display_name"),
            "source_authority_tier": self.authority_tier.value,
            "source_id": self.source_id,
            "external_url": item.get("doi") or primary_location.get("landing_page_url"),
            "abstract_inverted_index": item.get("abstract_inverted_index"),
            "is_retracted": item.get("is_retracted", False),
            "license_class": license_class,
            "raw_license": raw_license,
            "citation_count": item.get("cited_by_count", 0),
            "concepts": [c.get("display_name") for c in item.get("concepts", [])[:5]]
        }

        if item.get("abstract_inverted_index"):
            doc["abstract"] = self._reconstruct_abstract(item["abstract_inverted_index"])
        else:
            doc["abstract"] = None

        return LicensingIntelligenceEngine.filter_storage_payload(doc, license_class)

    def _reconstruct_abstract(self, inverted_index: Dict[str, List[int]]) -> str:
        word_positions = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_positions.append((pos, word))
        word_positions.sort(key=lambda x: x[0])
        return " ".join([word for _, word in word_positions])
