"""
ZMIE Public Knowledge REST API Client SDK (Python)
Provides high-level idiomatic Python bindings for medical researchers,
biotech teams, and clinical systems integrating with ZMIE.
"""

from typing import Dict, Any, List, Optional
import httpx
from pydantic import BaseModel


class ZMIEClient:
    """
    Official Python SDK for the ZMIE Knowledge & Evidence Infrastructure.
    """

    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "User-Agent": "ZMIE-Python-SDK/1.0",
            "Accept": "application/json"
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def search(self, query: str, mode: str = "public") -> Dict[str, Any]:
        """
        Unified Search across biomedical evidence and traditional codices.
        """
        with httpx.Client(base_url=self.base_url, timeout=30.0) as client:
            resp = client.get("/v1/search", params={"q": query, "mode": mode}, headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    def audit_claim(self, claim_id: str) -> Dict[str, Any]:
        """
        "Why This Claim?" atomic provenance passport audit.
        """
        with httpx.Client(base_url=self.base_url, timeout=15.0) as client:
            resp = client.get(f"/v1/search/why-this/{claim_id}", headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    def deep_investigation(self, question: str, systems: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Runs the multi-step Deep Research Agent.
        """
        payload = {
            "question": question,
            "systems": systems or ["modern", "unani", "ayurveda"]
        }
        with httpx.Client(base_url=self.base_url, timeout=60.0) as client:
            resp = client.post("/v1/research/investigate", json=payload, headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    def evaluate_safety(
        self,
        substance: str,
        medications: Optional[List[str]] = None,
        conditions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Screens for CYP450 interactions, contraindications, and emergency red-flags.
        """
        payload = {
            "substance": substance,
            "medications": medications or [],
            "patient_conditions": conditions or []
        }
        with httpx.Client(base_url=self.base_url, timeout=15.0) as client:
            resp = client.post("/v1/safety/evaluate", json=payload, headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    def compare_systems(self, topic: str) -> Dict[str, Any]:
        """
        Side-by-side epistemological comparison across Modern, Unani, Ayurveda, and TCM.
        """
        with httpx.Client(base_url=self.base_url, timeout=15.0) as client:
            resp = client.get("/v1/ontology/compare", params={"topic": topic}, headers=self.headers)
            resp.raise_for_status()
            return resp.json()
