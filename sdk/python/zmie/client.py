"""
Official ZMIE Python SDK Client
Connects to the ZMIE Medical Knowledge Infrastructure Platform via REST API or local TestClient.
"""

from typing import Dict, Any, List, Optional, Union
import json
import hmac
import hashlib
import time
import httpx


class ZMIE:
    """
    Official Python SDK for ZMIE Medical Knowledge Infrastructure Platform.
    
    Usage:
        client = ZMIE(api_key="zmie_prod_...", base_url="http://localhost:8000")
        context = client.rag_context("Curcumin in inflammatory arthritis")
        intel = client.intelligence_query("Black seed (Nigella sativa)", systems=["modern", "unani"])
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "http://localhost:8000",
        app_instance: Optional[Any] = None,
        timeout: float = 30.0
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = {
            "User-Agent": "ZMIE-Platform-SDK/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        if api_key:
            self.headers["X-API-Key"] = api_key
            self.headers["Authorization"] = f"Bearer {api_key}"

        # If an in-memory FastAPI app instance is supplied (for unit/integration testing without network daemon)
        self.app_instance = app_instance
        self._test_client = None
        if app_instance is not None:
            from fastapi.testclient import TestClient
            self._test_client = TestClient(app_instance)

    def _request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if self._test_client is not None:
            resp = self._test_client.request(
                method=method,
                url=path,
                params=params,
                json=json_data,
                headers=self.headers
            )
            resp.raise_for_status()
            return resp.json()
        else:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                resp = client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json_data,
                    headers=self.headers
                )
                resp.raise_for_status()
                return resp.json()

    # --- Platform & RAG Context ---

    def rag_context(
        self,
        query: str,
        evidence_minimum: str = "E5",
        max_items: int = 15,
        include_safety: bool = True,
        include_contradictions: bool = True
    ) -> Dict[str, Any]:
        """
        Retrieves a provenance-anchored RAG context packet for grounding LLMs.
        """
        payload = {
            "query": query,
            "evidence_minimum": evidence_minimum,
            "max_items": max_items,
            "include_safety": include_safety,
            "include_contradictions": include_contradictions
        }
        return self._request("POST", "/v1/platform/rag/context", json_data=payload)

    def intelligence_query(
        self,
        query: str,
        systems: Optional[List[str]] = None,
        mode: str = "evidence",
        strict_verification: bool = True
    ) -> Dict[str, Any]:
        """
        Executes unified multi-system medical intelligence query across Modern, Unani, and Ayurveda.
        """
        payload = {
            "query": query,
            "systems": systems or ["modern", "unani", "ayurveda"],
            "mode": mode,
            "strict_verification": strict_verification
        }
        return self._request("POST", "/v1/platform/intelligence/query", json_data=payload)

    def route_ai(
        self,
        task_type: str,
        prompt: str,
        context_packet: Optional[Dict[str, Any]] = None,
        force_model: Optional[str] = None,
        simulate_failure: bool = False
    ) -> Dict[str, Any]:
        """
        Routes generation through ZMIE AI Gateway with automatic model failover and firewall verification.
        """
        payload = {
            "task_type": task_type,
            "prompt": prompt,
            "context_packet": context_packet,
            "force_model": force_model,
            "simulate_failure": simulate_failure
        }
        return self._request("POST", "/v1/platform/ai/route", json_data=payload)

    # --- Knowledge & Search ---

    def search(self, query: str, mode: str = "public") -> Dict[str, Any]:
        """
        Unified search across biomedical evidence and traditional knowledge.
        """
        return self._request("GET", "/v1/search", params={"q": query, "mode": mode})

    def check_safety(
        self,
        substance: str,
        medications: Optional[List[str]] = None,
        conditions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluates CYP450 drug interactions, contraindications, and clinical red-flags.
        """
        payload = {
            "substance": substance,
            "medications": medications or [],
            "patient_conditions": conditions or []
        }
        return self._request("POST", "/v1/safety/evaluate", json_data=payload)

    # --- Webhooks & Keys ---

    def create_api_key(self, tenant_id: str, owner: str, name: str, scopes: Optional[List[str]] = None) -> Dict[str, Any]:
        payload = {
            "tenant_id": tenant_id,
            "owner": owner,
            "name": name,
            "scopes": scopes or ["knowledge:read", "search:read", "evidence:read"]
        }
        return self._request("POST", "/v1/platform/keys", json_data=payload)

    def revoke_api_key(self, credential_id: str) -> Dict[str, Any]:
        return self._request("DELETE", f"/v1/platform/keys/{credential_id}")

    def create_webhook(self, tenant_id: str, target_url: str, secret_key: Optional[str] = None, events: Optional[List[str]] = None) -> Dict[str, Any]:
        payload = {
            "tenant_id": tenant_id,
            "target_url": target_url,
            "secret_key": secret_key,
            "subscribed_events": events or ["source.retracted", "safety.alert"]
        }
        return self._request("POST", "/v1/platform/webhooks", json_data=payload)

    # --- Static Signature Security Verifier ---

    @staticmethod
    def verify_webhook_signature(
        payload: Union[bytes, str],
        secret: str,
        signature: str,
        timestamp: int,
        tolerance_seconds: int = 300
    ) -> bool:
        """
        Validates incoming ZMIE webhook HMAC-SHA256 signature with replay defense.
        """
        current_time = int(time.time())
        if abs(current_time - timestamp) > tolerance_seconds:
            return False

        payload_bytes = payload.encode("utf-8") if isinstance(payload, str) else payload
        message = f"t={timestamp}.".encode("utf-8") + payload_bytes
        expected = hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)



    # --- Prompt 23: Enterprise Federated & Private Intelligence Namespaces ---

    @property
    def private(self) -> "_PrivateNamespace":
        return _PrivateNamespace(self)

    @property
    def access(self) -> "_AccessNamespace":
        return _AccessNamespace(self)

    @property
    def federated(self) -> "_FederatedNamespace":
        return _FederatedNamespace(self)

    @property
    def sharing(self) -> "_SharingNamespace":
        return _SharingNamespace(self)

    @property
    def release(self) -> "_ReleaseNamespace":
        return _ReleaseNamespace(self)

    @property
    def audit(self) -> "_AuditNamespace":
        return _AuditNamespace(self)

    # --- Prompt 24: Scientific Agent Operating System Namespaces ---

    @property
    def agents(self) -> "_AgentsNamespace":
        return _AgentsNamespace(self)

    @property
    def agent_tasks(self) -> "_AgentTasksNamespace":
        return _AgentTasksNamespace(self)

    @property
    def research(self) -> "_ResearchNamespace":
        return _ResearchNamespace(self)

    @property
    def reviews(self) -> "_ReviewsNamespace":
        return _ReviewsNamespace(self)

    @property
    def tools(self) -> "_ToolsNamespace":
        return _ToolsNamespace(self)

    @property
    def agent_incidents(self) -> "_AgentIncidentsNamespace":
        return _AgentIncidentsNamespace(self)

    @property
    def skos(self) -> "_SKOSNamespace":
        return _SKOSNamespace(self)

    # --- Prompt 27: Enterprise Implementation & Production Build Spec ---

    @property
    def spec(self) -> "_SpecNamespace":
        return _SpecNamespace(self)

    # --- Prompts 13-22: Specialized Scientific Intelligence Subsystems ---

    @property
    def sources(self) -> "_SourcesNamespace":
        return _SourcesNamespace(self)

    @property
    def research_network(self) -> "_ResearchNetworkNamespace":
        return _ResearchNetworkNamespace(self)

    @property
    def rwe(self) -> "_RWENamespace":
        return _RWENamespace(self)

    @property
    def causal(self) -> "_CausalNamespace":
        return _CausalNamespace(self)

    @property
    def living_evidence(self) -> "_LivingEvidenceNamespace":
        return _LivingEvidenceNamespace(self)

    @property
    def clinical_regulatory(self) -> "_ClinicalRegulatoryNamespace":
        return _ClinicalRegulatoryNamespace(self)

    @property
    def simulation(self) -> "_SimulationNamespace":
        return _SimulationNamespace(self)

    @property
    def terminology(self) -> "_TerminologyNamespace":
        return _TerminologyNamespace(self)

    @property
    def compute(self) -> "_ComputeNamespace":
        return _ComputeNamespace(self)

    @property
    def collaboration(self) -> "_CollaborationNamespace":
        return _CollaborationNamespace(self)

    @property
    def admin(self) -> "_AdminNamespace":
        return _AdminNamespace(self)

    @property
    def tenancy(self) -> "_TenancyNamespace":
        return _TenancyNamespace(self)

    @property
    def credibility(self) -> "_CredibilityNamespace":
        return _CredibilityNamespace(self)

    @property
    def trust_firewall(self) -> "_TrustFirewallNamespace":
        return _TrustFirewallNamespace(self)

    @property
    def trust(self) -> "_TrustFirewallNamespace":
        return self.trust_firewall

    @property
    def revalidation(self) -> "_RevalidationNamespace":
        return _RevalidationNamespace(self)

    @property
    def security_hardening(self) -> "_SecurityHardeningNamespace":
        return _SecurityHardeningNamespace(self)

    @property
    def benchmarking(self) -> "_BenchmarkingNamespace":
        return _BenchmarkingNamespace(self)

    @property
    def production_readiness(self) -> "_ProductionReadinessNamespace":
        return _ProductionReadinessNamespace(self)

    @property
    def controlled_launch(self) -> "_ControlledLaunchNamespace":
        return _ControlledLaunchNamespace(self)

    @property
    def lifecycle(self) -> "_LifecycleNamespace":
        return _LifecycleNamespace(self)




class _PrivateSubresource:
    def __init__(self, client: ZMIE, path: str):
        self._client = client
        self._path = path

    def list(self, tenant_id: Optional[str] = None, user_id: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
        headers = {}
        if tenant_id: headers["X-Tenant-ID"] = tenant_id
        if user_id: headers["X-User-ID"] = user_id
        if project_id: headers["X-Project-ID"] = project_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            return self._client._request("GET", self._path)
        finally:
            self._client.headers = old

    def search(self, query: str, tenant_id: Optional[str] = None, user_id: Optional[str] = None,
               project_id: Optional[str] = None) -> Dict[str, Any]:
        return self._client.private.search(query, tenant_id=tenant_id, user_id=user_id, project_id=project_id)


class _PrivateNamespace:
    def __init__(self, client: ZMIE):
        self._client = client
        self.datasets = _PrivateSubresource(client, "/v1/private/datasets")
        self.documents = _PrivateSubresource(client, "/v1/private/documents")
        self.knowledge = _PrivateSubresource(client, "/v1/private/knowledge")

    def search(self, query: str, tenant_id: Optional[str] = None, user_id: Optional[str] = None,
               project_id: Optional[str] = None) -> Dict[str, Any]:
        headers = {}
        if tenant_id: headers["X-Tenant-ID"] = tenant_id
        if user_id: headers["X-User-ID"] = user_id
        if project_id: headers["X-Project-ID"] = project_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            body = {"query": query, "scope": {"tenant_id": tenant_id, "project_id": project_id}}
            return self._client._request("POST", "/v1/private/search", json_data=body)
        finally:
            self._client.headers = old


class _AccessNamespace:
    def __init__(self, client: ZMIE):
        self._client = client

    def request(self, project_id: str, resource_id: str, purpose: str, duration_days: int = 30,
                operations: Optional[List[str]] = None, tenant_id: Optional[str] = None,
                user_id: Optional[str] = None) -> Dict[str, Any]:
        headers = {}
        if tenant_id: headers["X-Tenant-ID"] = tenant_id
        if user_id: headers["X-User-ID"] = user_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            return self._client._request("POST", "/v1/access/request", json_data={
                "project_id": project_id, "resource_id": resource_id, "purpose": purpose,
                "duration_days": duration_days, "operations": operations or ["READ"]
            })
        finally:
            self._client.headers = old

    def approve(self, request_id: str, approve: bool = True, tenant_id: Optional[str] = None,
                user_id: Optional[str] = None) -> Dict[str, Any]:
        headers = {}
        if tenant_id: headers["X-Tenant-ID"] = tenant_id
        if user_id: headers["X-User-ID"] = user_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            return self._client._request("POST", "/v1/access/decide", json_data={"request_id": request_id, "approve": approve})
        finally:
            self._client.headers = old


class _FederatedNamespace:
    def __init__(self, client: ZMIE):
        self._client = client

    def query(self, sites: List[str], cohort_criteria: Optional[Dict[str, Any]] = None,
              query_type: str = "AGGREGATE_COHORT", allowed_output: str = "AGGREGATE_ONLY",
              min_cell_size: int = 10, enable_differential_privacy: bool = False, epsilon: float = 1.0,
              tenant_id: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
        headers = {}
        if tenant_id: headers["X-Tenant-ID"] = tenant_id
        if user_id: headers["X-User-ID"] = user_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            return self._client._request("POST", "/v1/federated/query", json_data={
                "sites": sites, "cohort_criteria": cohort_criteria or {}, "query_type": query_type,
                "allowed_output": allowed_output, "min_cell_size": min_cell_size,
                "enable_differential_privacy": enable_differential_privacy, "epsilon": epsilon
            })
        finally:
            self._client.headers = old

    def run(self, run_id: str, tenant_id: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
        headers = {}
        if tenant_id: headers["X-Tenant-ID"] = tenant_id
        if user_id: headers["X-User-ID"] = user_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            return self._client._request("GET", f"/v1/federated/jobs/{run_id}")
        finally:
            self._client.headers = old


class _SharingNamespace:
    def __init__(self, client: ZMIE):
        self._client = client

    def request(self, partner_tenant_id: str, purpose: str, allowed_operations: List[str],
                shared_project_id: Optional[str] = None, dataset_ids: Optional[List[str]] = None,
                tenant_id: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
        headers = {}
        if tenant_id: headers["X-Tenant-ID"] = tenant_id
        if user_id: headers["X-User-ID"] = user_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            return self._client._request("POST", "/v1/sharing/request", json_data={
                "partner_tenant_id": partner_tenant_id, "purpose": purpose,
                "allowed_operations": allowed_operations, "shared_project_id": shared_project_id,
                "dataset_ids": dataset_ids or []
            })
        finally:
            self._client.headers = old


class _ReleaseNamespace:
    def __init__(self, client: ZMIE):
        self._client = client

    def request(self, object_id: str, license: str = "CC-BY-4.0", tenant_id: Optional[str] = None,
                user_id: Optional[str] = None) -> Dict[str, Any]:
        headers = {}
        if tenant_id: headers["X-Tenant-ID"] = tenant_id
        if user_id: headers["X-User-ID"] = user_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            return self._client._request("POST", "/v1/release/request", json_data={"object_id": object_id, "license": license})
        finally:
            self._client.headers = old


class _AgentsNamespace:
    def __init__(self, client: ZMIE):
        self._client = client

    def list(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/agents")

    def get(self, agent_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/agents/{agent_id}")

    def register(self, agent_def: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/agents", json_data=agent_def)


class _AgentTasksNamespace:
    def __init__(self, client: ZMIE):
        self._client = client

    def create(self, agent_id: str, goal: str, inputs: Optional[Dict[str, Any]] = None,
               tenant_id: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
        headers = {}
        if tenant_id: headers["X-Tenant-ID"] = tenant_id
        if user_id: headers["X-User-ID"] = user_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            return self._client._request("POST", "/v1/agent-tasks", json_data={
                "agent_id": agent_id, "goal": goal, "inputs": inputs or {}, "tenant_id": tenant_id
            })
        finally:
            self._client.headers = old

    def get(self, task_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/agent-tasks/{task_id}")

    def cancel(self, task_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        headers = {}
        if user_id: headers["X-User-ID"] = user_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            return self._client._request("POST", f"/v1/agent-tasks/{task_id}/cancel")
        finally:
            self._client.headers = old


class _ResearchNamespace:
    def __init__(self, client: ZMIE):
        self._client = client

    def plan(self, question: str, tenant_id: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
        headers = {}
        if tenant_id: headers["X-Tenant-ID"] = tenant_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            return self._client._request("POST", "/v1/research/plan", json_data={
                "question": question, "tenant_id": tenant_id, "project_id": project_id
            })
        finally:
            self._client.headers = old

    def run(self, question: str, tenant_id: Optional[str] = None, project_id: Optional[str] = None,
            simulate_failure_subtask_id: Optional[str] = None) -> Dict[str, Any]:
        headers = {}
        if tenant_id: headers["X-Tenant-ID"] = tenant_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            return self._client._request("POST", "/v1/research/run", json_data={
                "question": question, "tenant_id": tenant_id, "project_id": project_id,
                "simulate_failure_subtask_id": simulate_failure_subtask_id
            })
        finally:
            self._client.headers = old

    def get_run(self, run_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/research/runs/{run_id}")

    def get_trace(self, run_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/agent-runs/{run_id}/trace")


class _ReviewsNamespace:
    def __init__(self, client: ZMIE):
        self._client = client

    def submit(self, task_id: str, triggering_agent_id: str, reason: str, recommendation: str,
               risks: Optional[List[str]] = None, uncertainties: Optional[List[str]] = None) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/reviews", json_data={
            "task_id": task_id, "triggering_agent_id": triggering_agent_id,
            "reason": reason, "recommendation": recommendation,
            "risks": risks or [], "uncertainties": uncertainties or []
        })

    def approve(self, review_id: str, reviewer_user_id: str, rationale: str) -> Dict[str, Any]:
        return self._client._request("POST", f"/v1/reviews/{review_id}/approve", json_data={
            "reviewer_user_id": reviewer_user_id, "rationale": rationale
        })

    def reject(self, review_id: str, reviewer_user_id: str, rationale: str) -> Dict[str, Any]:
        return self._client._request("POST", f"/v1/reviews/{review_id}/reject", json_data={
            "reviewer_user_id": reviewer_user_id, "rationale": rationale
        })


class _ToolsNamespace:
    def __init__(self, client: ZMIE):
        self._client = client

    def list(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/agent-tools")

    def policies(self) -> Dict[str, Any]:
        return self._client._request("GET", "/v1/agent-policies")


class _AgentIncidentsNamespace:
    def __init__(self, client: ZMIE):
        self._client = client

    def list(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/agent-incidents")

    def metrics(self, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {"agent_id": agent_id} if agent_id else None
        return self._client._request("GET", "/v1/agent-metrics", params=params)


# --- Prompt 25: SKOS Namespaces ---

class _SKOSEntitiesSubresource:
    def __init__(self, client: ZMIE):
        self._client = client

    def list(self, entity_type: Optional[str] = None, tenant_id: Optional[str] = None) -> List[Dict[str, Any]]:
        headers = {}
        if tenant_id:
            headers["X-Tenant-ID"] = tenant_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            params = {"entity_type": entity_type} if entity_type else None
            return self._client._request("GET", "/v1/skos/fabric/entities", params=params)
        finally:
            self._client.headers = old

    def get(self, entity_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/skos/fabric/entities/{entity_id}")


class _SKOSPathsSubresource:
    def __init__(self, client: ZMIE):
        self._client = client

    def get(self, path_type: str, start_id: Optional[str] = None, end_id: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if start_id:
            params["start_id"] = start_id
        if end_id:
            params["end_id"] = end_id
        return self._client._request("GET", f"/v1/skos/graph/paths/{path_type}", params=params)

    def traverse(self, direction: str = "FORWARD") -> Dict[str, Any]:
        return self._client._request("GET", "/v1/skos/graph/traverse", params={"direction": direction})

    def evidence(self, claim_id: str = "CLM-BER-001") -> Dict[str, Any]:
        return self.get("EVIDENCE", start_id=claim_id)

    def research(self, entity_id: str = "STU-BER-001") -> Dict[str, Any]:
        return self.get("RESEARCH", start_id=entity_id)

    def mechanism(self, start_id: str = "CMP-BERBERINE", end_id: str = "TGT-AMPK") -> Dict[str, Any]:
        return self.get("MECHANISM", start_id=start_id, end_id=end_id)

    def causal(self, start_id: str = "CMP-BERBERINE", end_id: str = "CON-T2D") -> Dict[str, Any]:
        return self.get("CAUSAL", start_id=start_id, end_id=end_id)

    def safety(self, entity_id: str = "CMP-BERBERINE") -> Dict[str, Any]:
        return self.get("SAFETY", start_id=entity_id)

    def terminology(self, concept_id: str = "CON-T2D") -> Dict[str, Any]:
        return self.get("TERMINOLOGY", start_id=concept_id)

    def experiment(self, hypothesis_id: str = "HYP-BER-001") -> Dict[str, Any]:
        return self.get("EXPERIMENT", start_id=hypothesis_id)

    def master_forward(self) -> Dict[str, Any]:
        return self.traverse(direction="FORWARD")

    def master_reverse(self) -> Dict[str, Any]:
        return self.traverse(direction="REVERSE")


class _SKOSRevalidationsSubresource:
    def __init__(self, client: ZMIE):
        self._client = client

    def trigger(self, new_study_doi: str, target_claim_id: str, reason: str) -> Dict[str, Any]:
        payload = {
            "new_study_doi": new_study_doi,
            "target_claim_id": target_claim_id,
            "reason": reason
        }
        return self._client._request("POST", "/v1/skos/revalidation/trigger", json_data=payload)

    def list(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/skos/revalidation/tasks")

    def decide(self, task_id: str, reviewer_user_id: str, action: str, rationale: str) -> Dict[str, Any]:
        payload = {
            "reviewer_user_id": reviewer_user_id,
            "action": action,
            "rationale": rationale
        }
        return self._client._request("POST", f"/v1/skos/revalidation/tasks/{task_id}/decide", json_data=payload)


class _SKOSRetractionsSubresource:
    def __init__(self, client: ZMIE):
        self._client = client

    def analyze(self, notice: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/skos/retractions/impact", json_data=notice)

    def list(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/skos/retractions")


class _SKOSSnapshotsSubresource:
    def __init__(self, client: ZMIE):
        self._client = client

    def list(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/skos/snapshots")

    def create(self, description: str = "Master Knowledge Snapshot", tenant_id: Optional[str] = None) -> Dict[str, Any]:
        headers = {}
        if tenant_id:
            headers["X-Tenant-ID"] = tenant_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            return self._client._request("POST", "/v1/skos/snapshots", params={"description": description})
        finally:
            self._client.headers = old

    def diff(self, snapshot_a_id: str, snapshot_b_id: str) -> Dict[str, Any]:
        payload = {
            "snapshot_a_id": snapshot_a_id,
            "snapshot_b_id": snapshot_b_id
        }
        return self._client._request("POST", "/v1/skos/snapshots/diff", json_data=payload)


class _SKOSGapsSubresource:
    def __init__(self, client: ZMIE):
        self._client = client

    def analyze(self, topic: str = "Berberine in Type 2 Diabetes") -> Dict[str, Any]:
        return self._client._request("GET", "/v1/skos/gaps", params={"topic": topic})


class _SKOSNamespace:
    """
    ZMIE Scientific Knowledge Operating System (SKOS) SDK Namespace.
    Unified access to Knowledge Fabric, Graph of Graphs traversals,
    Knowledge Revalidation, Retraction Impact, Snapshots, Gaps,
    Unified Scientific Answers, and the Learning Loop.
    """
    def __init__(self, client: ZMIE):
        self._client = client
        self.entities = _SKOSEntitiesSubresource(client)
        self.paths = _SKOSPathsSubresource(client)
        self.revalidation = _SKOSRevalidationsSubresource(client)
        self.retractions = _SKOSRetractionsSubresource(client)
        self.snapshots = _SKOSSnapshotsSubresource(client)
        self.gaps = _SKOSGapsSubresource(client)

    def health(self) -> Dict[str, Any]:
        return self._client._request("GET", "/v1/skos/health")

    def answer(self, question: str, target_system: str = "all", simulate_partial: bool = False) -> Dict[str, Any]:
        payload = {
            "question": question,
            "target_system": target_system,
            "simulate_partial": simulate_partial
        }
        return self._client._request("POST", "/v1/skos/answer", json_data=payload)

    def learning_loop(self) -> Dict[str, Any]:
        return self._client._request("GET", "/v1/skos/learning-loop")


# ==============================================================================
# Prompt 26: Scientific Reproducibility & Research Audit SDK Namespaces
# ==============================================================================

class _AuditSnapshotsSubresource:
    def __init__(self, client: ZMIE):
        self._client = client

    def get(self, snapshot_id: str, include_raw_data: bool = True, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        params = {"include_raw_data": include_raw_data}
        headers = {}
        if tenant_id:
            headers["X-Tenant-ID"] = tenant_id
        # Temporarily pass headers if present
        if headers and self._client._test_client is not None:
            self._client._test_client.headers.update(headers)
        res = self._client._request("GET", f"/v1/audit/snapshots/{snapshot_id}", params=params)
        return res

    def list(self, project_id: Optional[str] = None, tenant_id: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if project_id:
            params["project_id"] = project_id
        headers = {}
        if tenant_id:
            headers["X-Tenant-ID"] = tenant_id
        if headers and self._client._test_client is not None:
            self._client._test_client.headers.update(headers)
        return self._client._request("GET", "/v1/audit/snapshots", params=params)

    def create(self, snapshot: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/audit/snapshots", json_data={"snapshot": snapshot})

    def create_child(self, parent_snapshot_id: str, updates: Dict[str, Any], created_by: str = "zmie-research-updater", tenant_id: Optional[str] = None) -> Dict[str, Any]:
        payload = {"updates": updates, "created_by": created_by}
        headers = {}
        if tenant_id:
            headers["X-Tenant-ID"] = tenant_id
        if headers and self._client._test_client is not None:
            self._client._test_client.headers.update(headers)
        return self._client._request("POST", f"/v1/audit/snapshots/{parent_snapshot_id}/child", json_data=payload)

    def manifest(self, snapshot_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/audit/snapshots/{snapshot_id}/manifest")

    def lineage(self, snapshot_id: str) -> List[Dict[str, Any]]:
        return self._client._request("GET", f"/v1/audit/snapshots/{snapshot_id}/lineage")


class _AuditEventsSubresource:
    def __init__(self, client: ZMIE):
        self._client = client

    def record(
        self,
        audit_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        actor_id: str = "agent-researcher-01",
        reason: str = "",
        before_state: Optional[Dict[str, Any]] = None,
        after_state: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        payload = {
            "audit_id": audit_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "actor_id": actor_id,
            "reason": reason,
            "before_state": before_state,
            "after_state": after_state
        }
        return self._client._request("POST", "/v1/audit/events", json_data=payload)

    def list(self, audit_id: str, resource_id: Optional[str] = None, action: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if resource_id: params["resource_id"] = resource_id
        if action: params["action"] = action
        return self._client._request("GET", f"/v1/audit/events/{audit_id}", params=params)

    def verify(self, audit_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/audit/events/{audit_id}/verify")


class _AuditProvenanceSubresource:
    def __init__(self, client: ZMIE):
        self._client = client

    def get_trace(self, snapshot_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/audit/provenance/{snapshot_id}")

    def backward(self, snapshot_id: str, node_id: str) -> List[Dict[str, Any]]:
        return self._client._request("GET", f"/v1/audit/provenance/{snapshot_id}/backward", params={"node_id": node_id})

    def forward(self, snapshot_id: str, node_id: str) -> List[Dict[str, Any]]:
        return self._client._request("GET", f"/v1/audit/provenance/{snapshot_id}/forward", params={"node_id": node_id})


class _AuditReproduceSubresource:
    def __init__(self, client: ZMIE):
        self._client = client

    def run(self, snapshot_id: str, mode: str = "SANDBOX", simulated_drift: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {"mode": mode, "simulated_drift": simulated_drift}
        return self._client._request("POST", f"/v1/audit/reproduce/{snapshot_id}", json_data=payload)

    def get_run(self, run_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/audit/reproduce/runs/{run_id}")


class _AuditCertificatesSubresource:
    def __init__(self, client: ZMIE):
        self._client = client

    def issue(self, audit_id: str) -> Dict[str, Any]:
        return self._client._request("POST", f"/v1/audit/certificates/{audit_id}")

    def packet(self, audit_id: str, format: str = "json") -> Any:
        return self._client._request("GET", f"/v1/audit/certificates/{audit_id}/packet", params={"format": format})


class _AuditRecordsSubresource:
    def __init__(self, client: ZMIE):
        self._client = client

    def create(self, snapshot_id: str, researcher: str, study_name: str, project_id: Optional[str] = None) -> Dict[str, Any]:
        payload = {
            "snapshot_id": snapshot_id,
            "researcher": researcher,
            "study_name": study_name,
            "project_id": project_id
        }
        return self._client._request("POST", "/v1/audit/records", json_data=payload)

    def get(self, audit_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/audit/records/{audit_id}")

    def set_hold(self, audit_id: str, hold: bool) -> Dict[str, Any]:
        return self._client._request("POST", f"/v1/audit/records/{audit_id}/hold", json_data={"hold": hold})

    def list(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/audit/records")



class _AuditNamespace:
    """
    ZMIE Scientific Reproducibility & Research Audit SDK Namespace (Prompt 26).
    Unified access to immutable snapshots, hash-chain event verification,
    bidirectional execution traces, sandbox reproduction, and official certificates.
    """
    def __init__(self, client: ZMIE):
        self._client = client
        self.snapshots = _AuditSnapshotsSubresource(client)
        self.events = _AuditEventsSubresource(client)
        self.provenance = _AuditProvenanceSubresource(client)
        self.reproduce = _AuditReproduceSubresource(client)
        self.certificates = _AuditCertificatesSubresource(client)
        self.records = _AuditRecordsSubresource(client)

    def diff(self, old_snapshot_id: str, new_snapshot_id: str) -> Dict[str, Any]:
        payload = {"old_snapshot_id": old_snapshot_id, "new_snapshot_id": new_snapshot_id}
        return self._client._request("POST", "/v1/audit/diff", json_data=payload)

    def verify_chain(self, audit_id: str) -> Dict[str, Any]:
        return self.events.verify(audit_id)

    def verify(self, audit_id: str) -> Dict[str, Any]:
        return self.verify_chain(audit_id)

    def ledger(self) -> List[Dict[str, Any]]:
        return self.records.list()

    def query(self, tenant_id: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:

        """Queries private/federated audit logs (Prompt 23 backwards compatibility)."""
        headers = {}
        if tenant_id: headers["X-Tenant-ID"] = tenant_id
        if user_id: headers["X-User-ID"] = user_id
        old = self._client.headers.copy()
        self._client.headers.update(headers)
        try:
            return self._client._request("GET", "/v1/audit/private")
        finally:
            self._client.headers = old


# ==============================================================================
# Prompt 27: Enterprise Specification & Production Build SDK Namespace
# ==============================================================================

class _SpecNamespace:
    """
    ZMIE Enterprise Specification & Production Build SDK Namespace (Prompt 27).
    Unified access to Master Architecture Map, ADR Registry, Platform Invariants,
    Deployment Capability Matrix, Master Build Matrix, and Production Readiness.
    """
    def __init__(self, client: ZMIE):
        self._client = client

    def layers(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/spec/architecture/layers")

    def layer(self, layer_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/spec/architecture/layers/{layer_id}")

    def adrs(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/spec/architecture/adrs")

    def adr(self, adr_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/spec/architecture/adrs/{adr_id}")

    def invariants(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/spec/invariants")

    def verify_invariants(self) -> Dict[str, Any]:
        return self._client._request("GET", "/v1/spec/invariants/verify")

    def deployment_matrix(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/spec/deployment/matrix")

    def build_matrix(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/spec/build-matrix")

    def readiness(self) -> Dict[str, Any]:
        return self._client._request("GET", "/v1/spec/readiness")


# ==============================================================================
# Prompts 13-22: Specialized Scientific Intelligence Subsystem Namespaces
# ==============================================================================

class _SourcesNamespace:
    """Prompt 13: Global Medical Source Universe & Ingestion Registry"""
    def __init__(self, client: ZMIE):
        self._client = client

    def list(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/sources")

    def get(self, source_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/sources/{source_id}")

    def coverage_report(self) -> Dict[str, Any]:
        return self._client._request("GET", "/v1/sources/coverage/report")

    def search(self, query: str, authority_tier: Optional[str] = None) -> List[Dict[str, Any]]:
        payload = {"query": query, "authority_tier": authority_tier}
        return self._client._request("POST", "/v1/sources/search", json_data=payload)

    def report_retraction(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/sources/retractions/event", json_data=event_data)

    def list_retractions(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/sources/retractions/events")


class _ResearchNetworkNamespace:
    """Prompt 14: Global Research Discovery Network & Knowledge Evolution"""
    def __init__(self, client: ZMIE):
        self._client = client

    def get_researcher(self, researcher_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/research-network/researchers/{researcher_id}")

    def disambiguate(self, name: str, organization: Optional[str] = None) -> List[Dict[str, Any]]:
        payload = {"name": name, "organization": organization}
        return self._client._request("POST", "/v1/research-network/researchers/disambiguate", json_data=payload)

    def get_institution(self, institution_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/research-network/institutions/{institution_id}")

    def who_is_researching(self, topic: str) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/research-network/who-is-researching", params={"topic": topic})

    def gaps(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/research-network/gaps")

    def frontier(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/research-network/frontier")

    def cascade(self, root_id: str, change_type: str = "NEW_FINDING") -> Dict[str, Any]:
        payload = {"root_id": root_id, "change_type": change_type}
        return self._client._request("POST", "/v1/research-network/evolution/cascade", json_data=payload)

    def snapshots(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/research-network/evolution/snapshots")


class _RWENamespace:
    """Prompt 15: Real-World Evidence & Multi-System Data Interoperability"""
    def __init__(self, client: ZMIE):
        self._client = client

    def list_sources(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/rwe/sources")

    def get_source(self, source_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/rwe/sources/{source_id}")

    def audit_quality(self, source_id: str) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/rwe/quality/audit", json_data={"source_id": source_id})

    def define_cohort(self, cohort_def: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/rwe/cohorts/define", json_data=cohort_def)

    def get_cohort(self, cohort_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/rwe/cohorts/{cohort_id}")

    def analyze_cohort(self, cohort_id: str, outcome_measure: str) -> Dict[str, Any]:
        payload = {"cohort_id": cohort_id, "outcome_measure": outcome_measure}
        return self._client._request("POST", "/v1/rwe/cohorts/analyze", json_data=payload)

    def harmonize_raw_to_fhir(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/rwe/harmonize/raw-to-fhir", json_data=payload)

    def create_target_trial_protocol(self, protocol_def: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/rwe/tte/protocols", json_data=protocol_def)


class _CausalNamespace:
    """Prompt 16: Medical Causal & Mechanistic Intelligence"""
    def __init__(self, client: ZMIE):
        self._client = client

    def decompose_mechanism(self, proposition: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/causal-mechanistic/mechanisms/decompose", json_data=proposition)

    def competing_mechanisms(self, compound_id: str) -> Optional[Dict[str, Any]]:
        return self._client._request("GET", f"/v1/causal-mechanistic/mechanisms/competing/{compound_id}")

    def validate_dag(self, dag_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/causal-mechanistic/causal/dag/validate", json_data=dag_data)

    def bridge_traditional(self, bridge_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/causal-mechanistic/traditional/bridge", json_data=bridge_data)


class _LivingEvidenceNamespace:
    """Prompt 17: Living Evidence Synthesis & Update Engine"""
    def __init__(self, client: ZMIE):
        self._client = client

    def list(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/living-evidence")

    def get(self, review_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/living-evidence/{review_id}")

    def start_living(self, review_id: str) -> Dict[str, Any]:
        return self._client._request("POST", f"/v1/living-evidence/{review_id}/start-living")

    def pause(self, review_id: str) -> Dict[str, Any]:
        return self._client._request("POST", f"/v1/living-evidence/{review_id}/pause")

    def incorporate(self, review_id: str, evidence_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", f"/v1/living-evidence/{review_id}/incorporate", json_data=evidence_data)

    def retract(self, review_id: str, notice: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", f"/v1/living-evidence/{review_id}/retract", json_data=notice)


class _ClinicalRegulatoryNamespace:
    """Prompt 18: Global Clinical & Regulatory Intelligence"""
    def __init__(self, client: ZMIE):
        self._client = client

    def get_product(self, product_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/clinical-regulatory/products/{product_id}")

    def compare_jurisdictions(self, product_id: str, jurisdiction_a: str = "FDA", jurisdiction_b: str = "EMA") -> Dict[str, Any]:
        payload = {"product_id": product_id, "jurisdiction_a": jurisdiction_a, "jurisdiction_b": jurisdiction_b}
        return self._client._request("POST", "/v1/clinical-regulatory/compare", json_data=payload)

    def diff_labels(self, product_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/clinical-regulatory/labels/{product_id}/diff")

    def list_guidelines(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/clinical-regulatory/guidelines")

    def check_claims(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/clinical-regulatory/claims/check", json_data=claim_data)

    def list_recalls(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/clinical-regulatory/recalls")


class _SimulationNamespace:
    """Prompt 19: Scientific Simulation, Hypothesis & In Silico Trials"""
    def __init__(self, client: ZMIE):
        self._client = client

    def list_hypotheses(self) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/simulation-hypothesis/hypotheses")

    def create_hypothesis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/simulation-hypothesis/hypotheses", json_data=data)

    def get_hypothesis(self, hypothesis_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/simulation-hypothesis/hypotheses/{hypothesis_id}")

    def run_simulation(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/simulation-hypothesis/simulations/run", json_data=payload)

    def next_best_experiment(self, hypothesis_ids: List[str]) -> Dict[str, Any]:
        payload = {"competing_hypothesis_ids": hypothesis_ids}
        return self._client._request("POST", "/v1/simulation-hypothesis/experiments/next-best", json_data=payload)


class _TerminologyNamespace:
    """Prompt 20: Global Medical Ontology & Terminology Evolution"""
    def __init__(self, client: ZMIE):
        self._client = client

    def resolve(self, term: str, context: Optional[str] = None) -> Dict[str, Any]:
        payload = {"text": term, "domain_context": context}
        return self._client._request("POST", "/v1/terminology/resolve", json_data=payload)

    def map(self, source_concept: str, target_system: str) -> Dict[str, Any]:
        payload = {"source_concept_id": source_concept, "target_system": target_system}
        return self._client._request("POST", "/v1/terminology/map", json_data=payload)

    def historical(self, term: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/terminology/historical/{term}")

    def diff(self, source_ontology: str, target_ontology: str) -> Dict[str, Any]:
        params = {"source_ontology": source_ontology, "target_ontology": target_ontology}
        return self._client._request("GET", "/v1/terminology/ontologies/diff", params=params)


class _ComputeNamespace:
    """Prompt 21: Scientific Data Fabric & Computational Research Engine"""
    def __init__(self, client: ZMIE):
        self._client = client

    def plan_analysis(self, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/compute/analyses/plan", json_data=plan_data)

    def run_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/compute/workflows/run", json_data=workflow_data)

    def get_run(self, run_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/compute/runs/{run_id}")

    def reproduce(self, run_id: str) -> Dict[str, Any]:
        return self._client._request("POST", f"/v1/compute/runs/{run_id}/reproduce")

    def get_lineage(self, run_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/compute/lineage/{run_id}")


class _CollaborationNamespace:
    """Prompt 22: Global Scientific Collaboration & Research Network"""
    def __init__(self, client: ZMIE):
        self._client = client

    def resolve_researcher(self, name: str, institution: Optional[str] = None) -> Dict[str, Any]:
        payload = {"raw_name": name, "institution_hint": institution}
        return self._client._request("POST", "/v1/network/researchers/resolve", json_data=payload)

    def get_researcher(self, researcher_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/network/researchers/{researcher_id}")

    def timeline(self, researcher_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/network/researchers/{researcher_id}/timeline")

    def collaborations(self, researcher_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/v1/network/researchers/{researcher_id}/collaborations")

    def search_expertise(self, topic: str) -> Dict[str, Any]:
        payload = {"topic": topic}
        return self._client._request("POST", "/v1/network/expertise/search", json_data=payload)


class _AdminNamespace:
    """ZMIE Admin Control Plane & Observability (Prompt 28 Module 31)"""
    def __init__(self, client: ZMIE):
        self._client = client

    def telemetry(self) -> Dict[str, Any]:
        return self._client._request("GET", "/v1/admin/telemetry")

    def quality_dashboard(self) -> Dict[str, Any]:
        return self._client._request("GET", "/v1/admin/quality-dashboard")

    def research_metrics(self) -> Dict[str, Any]:
        return self._client._request("GET", "/v1/admin/research-metrics")

    def audit_logs(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._client._request("GET", "/v1/admin/audit-logs", params={"limit": limit})


class _TenancyNamespace:
    """ZMIE Identity, Tenancy & Security Gateway (Prompt 28 Modules 02-04, Clause 16)"""
    def __init__(self, client: ZMIE):
        self._client = client

    def evaluate(
        self,
        user_id: str,
        tenant_id: str,
        roles: List[str],
        action: str,
        resource_tenant_id: str
    ) -> Dict[str, Any]:
        payload = {
            "user_id": user_id,
            "tenant_id": tenant_id,
            "roles": roles,
            "action": action,
            "resource_tenant_id": resource_tenant_id
        }
        return self._client._request("POST", "/v1/security/evaluate", json_data=payload)

    def exchange_token(
        self,
        user_id: str,
        tenant_id: str,
        roles: List[str],
        scopes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        payload = {
            "user_id": user_id,
            "tenant_id": tenant_id,
            "roles": roles,
            "scopes": scopes or ["read"]
        }
        return self._client._request("POST", "/v1/security/tokens/exchange", json_data=payload)


class _CredibilityNamespace:
    """Prompt 29: Scientific Credibility, Verification, Provenance & Anti-Fabrication Engine."""
    def __init__(self, client: ZMIE):
        self._client = client

    def audit_claim(
        self,
        target_object_id: str,
        claim_text: str,
        source_id: Optional[str] = None,
        identifier: Optional[str] = None,
        passage_text: Optional[str] = None,
        dataset_hash: Optional[str] = None,
        researcher_orcid: Optional[str] = None,
        drug_name: Optional[str] = None,
        traditional_mapping: Optional[Dict[str, Any]] = None,
        calculation_seed: Optional[int] = None,
        is_ai_generated: bool = False,
        is_expert_signed: bool = False,
        exact_location: Optional[str] = None
    ) -> Dict[str, Any]:
        """Runs the complete 14-layer Anti-Fabrication & Scientific Credibility Audit."""
        payload = {
            "target_object_id": target_object_id,
            "claim_text": claim_text,
            "source_id": source_id,
            "identifier": identifier,
            "passage_text": passage_text,
            "dataset_hash": dataset_hash,
            "researcher_orcid": researcher_orcid,
            "drug_name": drug_name,
            "traditional_mapping": traditional_mapping,
            "calculation_seed": calculation_seed,
            "is_ai_generated": is_ai_generated,
            "is_expert_signed": is_expert_signed,
            "exact_location": exact_location
        }
        return self._client._request("POST", "/v1/credibility/audit", json_data=payload)

    def verify_chain(self, chain_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verifies the mandatory 7-link Evidence Chain."""
        return self._client._request("POST", "/v1/credibility/chain/verify", json_data={"chain": chain_data})

    def transition_state(
        self,
        object_id: str,
        target_state: str,
        proof_payload: Optional[Dict[str, Any]] = None,
        actor_id: str = "system"
    ) -> Dict[str, Any]:
        """Transitions object verification state through strict lifecycle ladder."""
        payload = {
            "object_id": object_id,
            "target_state": target_state,
            "proof_payload": proof_payload or {},
            "actor_id": actor_id
        }
        return self._client._request("POST", "/v1/credibility/transition", json_data=payload)

    def get_state(self, object_id: str) -> Dict[str, Any]:
        """Retrieves current verification state for an object."""
        return self._client._request("GET", f"/v1/credibility/states/{object_id}")

    def get_audit(self, audit_id: str) -> Dict[str, Any]:
        """Retrieves cryptographic credibility audit report."""
        return self._client._request("GET", f"/v1/credibility/audits/{audit_id}")


class _TrustFirewallNamespace:
    """Prompt 30: Real-Source Verification & Scientific Trust Firewall."""
    def __init__(self, client: ZMIE):
        self._client = client

    def verify_source(self, identifier: str) -> Dict[str, Any]:
        """Verifies DOI/citation against canonical registries and retraction lists."""
        return self._client._request("POST", "/v1/trust-firewall/verify-source", json_data={"identifier": identifier})

    def evaluate_claim(
        self,
        claim_text: str,
        doi: Optional[str] = None,
        claimed_passage: Optional[str] = None
    ) -> Dict[str, Any]:
        """Evaluates claim veracity, citation integrity, and epistemic drift."""
        payload = {
            "claim_text": claim_text,
            "doi": doi,
            "claimed_passage": claimed_passage
        }
        return self._client._request("POST", "/v1/trust-firewall/evaluate-claim", json_data=payload)

    def list_ledger(self) -> List[Dict[str, Any]]:
        """Lists canonical verified source ledger with tamper-proof HMAC signatures."""
        return self._client._request("GET", "/v1/trust-firewall/ledger")

    def get_ledger_entry(self, identifier: str) -> Dict[str, Any]:
        """Gets verified source ledger entry by identifier."""
        return self._client._request("GET", f"/v1/trust-firewall/ledger/{identifier}")

    def assess(
        self,
        object_id: str,
        object_type: str = "claim",
        claim_text: Optional[str] = None,
        source_id: Optional[str] = None,
        claimed_passage: Optional[str] = None,
        is_simulation: bool = False,
        traditional_mapping: Optional[str] = None,
        regulatory_claim: Optional[str] = None,
        tenant_id: str = "system",
        is_public_release: bool = False
    ) -> Dict[str, Any]:
        """Executes comprehensive Trust Decision Engine evaluation across all gates."""
        payload = {
            "object_id": object_id,
            "object_type": object_type,
            "claim_text": claim_text,
            "source_id": source_id,
            "claimed_passage": claimed_passage,
            "is_simulation": is_simulation,
            "traditional_mapping": traditional_mapping,
            "regulatory_claim": regulatory_claim,
            "tenant_id": tenant_id,
            "is_public_release": is_public_release
        }
        return self._client._request("POST", "/v1/trust-firewall/assess", json_data=payload)

    def list_quarantine(self) -> List[Dict[str, Any]]:
        """Lists quarantined items failing trust firewall gates."""
        return self._client._request("GET", "/v1/trust-firewall/quarantine")

    def list_incidents(self) -> List[Dict[str, Any]]:
        """Lists recorded scientific trust incidents."""
        return self._client._request("GET", "/v1/trust-firewall/incidents")

    def get_history(self, object_id: str) -> List[Dict[str, Any]]:
        """Retrieves trust assessment history for temporal reconstruction."""
        return self._client._request("GET", f"/v1/trust-firewall/history/{object_id}")

    def get_certificate(self, object_id: str) -> Dict[str, Any]:
        """Retrieves signed Scientific Trust Certificate."""
        return self._client._request("GET", f"/v1/trust-firewall/certificates/{object_id}")


class _RevalidationNamespace:
    """Prompt 31: Continuous Evidence & Knowledge Revalidation."""
    def __init__(self, client: ZMIE):
        self._client = client

    def ingest_surveillance_event(
        self,
        study_id: str,
        event_type: str,
        reason: str,
        severity: str = "CRITICAL",
        doi: Optional[str] = None,
        source_notice_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Ingests retraction/erratum and executes downstream cascade invalidation."""
        payload = {
            "study_id": study_id,
            "event_type": event_type,
            "reason": reason,
            "severity": severity,
            "doi": doi,
            "source_notice_url": source_notice_url
        }
        return self._client._request("POST", "/v1/continuous-revalidation/surveillance-events", json_data=payload)

    def list_deltas(self) -> List[Dict[str, Any]]:
        """Lists living evidence delta reports."""
        return self._client._request("GET", "/v1/continuous-revalidation/deltas")

    def get_delta(self, delta_id: str) -> Dict[str, Any]:
        """Gets single evidence delta report by ID."""
        return self._client._request("GET", f"/v1/continuous-revalidation/deltas/{delta_id}")

    def get_dependents(self, node_id: str) -> Dict[str, Any]:
        """Gets all downstream dependents for a graph node."""
        return self._client._request("GET", f"/v1/continuous-revalidation/dependents/{node_id}")

    def get_node(self, node_id: str) -> Dict[str, Any]:
        """Gets graph node details."""
        return self._client._request("GET", f"/v1/continuous-revalidation/nodes/{node_id}")

    def request_revalidation(
        self,
        object_id: str,
        trigger: str = "USER_TRIGGERED",
        scope: str = "DEPENDENCIES",
        priority: str = "NORMAL",
        reason: str = "Standard revalidation request",
        tenant_id: Optional[str] = None,
        incoming_event: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Requests and orchestrates a revalidation job with idempotency and trust verification."""
        payload = {
            "object_id": object_id,
            "trigger": trigger,
            "scope": scope,
            "priority": priority,
            "reason": reason,
            "tenant_id": tenant_id,
            "incoming_event": incoming_event
        }
        return self._client._request("POST", "/v1/continuous-revalidation/request", json_data=payload)

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """Gets revalidation job status."""
        return self._client._request("GET", f"/v1/continuous-revalidation/jobs/{job_id}")

    def approve_job(self, job_id: str, reviewer_id: str, comment: str = "Approved") -> Dict[str, Any]:
        """Applies human review approval to revalidation job."""
        return self._client._request("POST", f"/v1/continuous-revalidation/jobs/{job_id}/approve", json_data={"reviewer_id": reviewer_id, "comment_or_reason": comment})

    def reject_job(self, job_id: str, reviewer_id: str, reason: str) -> Dict[str, Any]:
        """Rejects revalidation result."""
        return self._client._request("POST", f"/v1/continuous-revalidation/jobs/{job_id}/reject", json_data={"reviewer_id": reviewer_id, "comment_or_reason": reason})

    def compute_source_diff(
        self,
        source_id: str,
        old_content: str,
        new_content: str,
        old_metadata: Optional[Dict[str, Any]] = None,
        new_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Computes multi-dimensional diff and impact classification."""
        payload = {
            "source_id": source_id,
            "old_content": old_content,
            "new_content": new_content,
            "old_metadata": old_metadata,
            "new_metadata": new_metadata
        }
        return self._client._request("POST", "/v1/continuous-revalidation/source-diff", json_data=payload)

    def run_impact_analysis(
        self,
        target_object_id: str,
        change_type: str = "NEW_STUDY_PUBLISHED",
        impact_level: str = "MODERATE_IMPACT",
        trigger_event_id: str = "evt-manual"
    ) -> Dict[str, Any]:
        """Runs dependency-aware impact analysis down the knowledge fabric."""
        payload = {
            "target_object_id": target_object_id,
            "change_type": change_type,
            "impact_level": impact_level,
            "trigger_event_id": trigger_event_id
        }
        return self._client._request("POST", "/v1/continuous-revalidation/impact-analysis", json_data=payload)

    def register_source_watch(
        self,
        watch_id: str,
        source_id: str,
        provider: str = "CROSSREF",
        schedule: str = "0 0 * * *",
        owner: str = "SYSTEM"
    ) -> Dict[str, Any]:
        """Registers a source watcher."""
        payload = {
            "watch_id": watch_id,
            "source_id": source_id,
            "provider": provider,
            "schedule": schedule,
            "owner": owner
        }
        return self._client._request("POST", "/v1/continuous-revalidation/source-watches", json_data=payload)

    def list_source_watches(self) -> List[Dict[str, Any]]:
        """Lists active source watches."""
        return self._client._request("GET", "/v1/continuous-revalidation/source-watches")

    def check_source_watch(self, watch_id: str, simulate_outage: bool = False) -> Dict[str, Any]:
        """Executes source watch check."""
        return self._client._request("POST", f"/v1/continuous-revalidation/source-watches/{watch_id}/check?simulate_outage={str(simulate_outage).lower()}")

    def register_topic_watcher(
        self,
        topic: str,
        terms: List[str],
        entities: Optional[List[str]] = None,
        scope: str = "PUBLIC",
        tenant_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Registers a topic watcher."""
        payload = {
            "topic": topic,
            "terms": terms,
            "entities": entities,
            "scope": scope,
            "tenant_id": tenant_id
        }
        return self._client._request("POST", "/v1/continuous-revalidation/topic-watchers", json_data=payload)

    def list_topic_watchers(self, tenant_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists topic watchers, respecting tenant boundary."""
        url = "/v1/continuous-revalidation/topic-watchers"
        if tenant_id:
            url += f"?tenant_id={tenant_id}"
        return self._client._request("GET", url)

    def search_contradictions(self, claim_id: str, disconfirming_study_doi: Optional[str] = None) -> Dict[str, Any]:
        """Executes explicit negative evidence / contradiction search."""
        payload = {"claim_id": claim_id, "disconfirming_study_doi": disconfirming_study_doi}
        return self._client._request("POST", "/v1/continuous-revalidation/contradictions/search", json_data=payload)

    def get_knowledge_history(self, node_id: str) -> List[Dict[str, Any]]:
        """Retrieves historical versions of a knowledge node."""
        return self._client._request("GET", f"/v1/continuous-revalidation/knowledge/{node_id}/history")

    def get_knowledge_health(self, node_id: str) -> Dict[str, Any]:
        """Retrieves multidimensional health profile of a knowledge node."""
        return self._client._request("GET", f"/v1/continuous-revalidation/knowledge/{node_id}/health")

    def inspect_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        """Inspects frozen research snapshot."""
        return self._client._request("GET", f"/v1/continuous-revalidation/snapshots/{snapshot_id}")

    def issue_certificate(self, job_id: str, reviewer: str = "LEAD_SCIENTIFIC_REVIEWER") -> Dict[str, Any]:
        """Issues an HMAC-signed revalidation certificate."""
        return self._client._request("POST", f"/v1/continuous-revalidation/jobs/{job_id}/certificate?reviewer={reviewer}")

    def get_what_changed(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves central what changed feed."""
        return self._client._request("GET", f"/v1/continuous-revalidation/feed/what-changed?limit={limit}")


class _SecurityHardeningNamespace:
    """Prompt 32: Production Security & Privacy Hardening."""
    def __init__(self, client: ZMIE):
        self._client = client

    def apply_differential_privacy(
        self,
        raw_value: float,
        epsilon: float = 0.5,
        delta: float = 1e-5,
        sensitivity: float = 1.0
    ) -> Dict[str, Any]:
        """Injects Laplace differential privacy noise."""
        payload = {
            "raw_value": raw_value,
            "epsilon": epsilon,
            "delta": delta,
            "sensitivity": sensitivity
        }
        return self._client._request("POST", "/v1/security-hardening/differential-privacy", json_data=payload)

    def deidentify(self, raw_text: str, jitter_dates: bool = True) -> Dict[str, Any]:
        """Redacts HIPAA 18-identifiers and jitters dates."""
        payload = {"raw_text": raw_text, "jitter_dates": jitter_dates}
        return self._client._request("POST", "/v1/security-hardening/deidentify", json_data=payload)

    def envelope_encrypt(
        self,
        tenant_id: str,
        artifact_id: str,
        plaintext_data: str,
        kms_key_id: str = "kms-key-zmie-master-01"
    ) -> Dict[str, Any]:
        """Performs envelope encryption with DEK wrapped by KMS master key."""
        payload = {
            "tenant_id": tenant_id,
            "artifact_id": artifact_id,
            "plaintext_data": plaintext_data,
            "kms_key_id": kms_key_id
        }
        return self._client._request("POST", "/v1/security-hardening/envelope-encrypt", json_data=payload)

    def break_glass(
        self,
        tenant_id: str,
        patient_cohort_id: str,
        physician_id: str,
        compliance_officer_id: str,
        clinical_justification: str
    ) -> Dict[str, Any]:
        """Executes dual-authorization break-glass emergency override."""
        payload = {
            "tenant_id": tenant_id,
            "patient_cohort_id": patient_cohort_id,
            "physician_id": physician_id,
            "compliance_officer_id": compliance_officer_id,
            "clinical_justification": clinical_justification
        }
        return self._client._request("POST", "/v1/security-hardening/break-glass", json_data=payload)

    def scan_prompt(self, user_prompt: str) -> Dict[str, Any]:
        """Scans for prompt injection and prohibited CBRN instructions."""
        return self._client._request("POST", "/v1/security-hardening/scan-prompt", json_data={"user_prompt": user_prompt})

    def evaluate_access(
        self,
        identity: str,
        caller_tenant_id: str,
        resource_id: str,
        action: str,
        classification: str = "INTERNAL",
        user_roles: Optional[List[str]] = None,
        resource_tenant_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Evaluates Zero Trust context-aware access decision with default deny."""
        payload = {
            "identity": identity,
            "caller_tenant_id": caller_tenant_id,
            "resource_id": resource_id,
            "action": action,
            "classification": classification,
            "user_roles": user_roles,
            "resource_tenant_id": resource_tenant_id
        }
        return self._client._request("POST", "/v1/security-hardening/access/evaluate", json_data=payload)

    def register_credential(
        self,
        tenant_id: str,
        owner: str,
        scope: str,
        secret_plaintext: str,
        ttl_days: int = 90
    ) -> Dict[str, Any]:
        """Registers a credential with SHA-256 hash storage."""
        payload = {
            "tenant_id": tenant_id,
            "owner": owner,
            "scope": scope,
            "secret_plaintext": secret_plaintext,
            "ttl_days": ttl_days
        }
        return self._client._request("POST", "/v1/security-hardening/credentials/register", json_data=payload)

    def rotate_credential(self, key_id: str, new_secret_plaintext: str) -> Dict[str, Any]:
        """Rotates a credential and deprecates old key."""
        return self._client._request("POST", "/v1/security-hardening/credentials/rotate", json_data={"key_id": key_id, "new_secret_plaintext": new_secret_plaintext})

    def revoke_credential(self, key_id: str, reason: str = "Manual revocation") -> Dict[str, Any]:
        """Revokes a credential immediately."""
        return self._client._request("POST", "/v1/security-hardening/credentials/revoke", json_data={"key_id": key_id, "reason": reason})

    def evaluate_model_routing(
        self,
        tenant_id: str,
        model_provider: str,
        context_text: str,
        classification: str = "INTERNAL"
    ) -> Dict[str, Any]:
        """Evaluates external model transmission firewall."""
        payload = {
            "tenant_id": tenant_id,
            "model_provider": model_provider,
            "context_text": context_text,
            "classification": classification
        }
        return self._client._request("POST", "/v1/security-hardening/model-firewall/evaluate", json_data=payload)

    def evaluate_agent_action(
        self,
        agent_id: str,
        action_type: str,
        tool_name: str,
        token_cost: int = 100
    ) -> Dict[str, Any]:
        """Evaluates agent sandbox permissions and budget limits."""
        payload = {
            "agent_id": agent_id,
            "action_type": action_type,
            "tool_name": tool_name,
            "token_cost": token_cost
        }
        return self._client._request("POST", "/v1/security-hardening/agent-firewall/evaluate", json_data=payload)

    def verify_webhook(
        self,
        payload_text: str,
        signature: str,
        timestamp: float,
        nonce: str
    ) -> Dict[str, Any]:
        """Verifies webhook HMAC signature with replay protection."""
        payload = {
            "payload_text": payload_text,
            "signature": signature,
            "timestamp": timestamp,
            "nonce": nonce
        }
        return self._client._request("POST", "/v1/security-hardening/webhooks/verify", json_data=payload)

    def create_incident(
        self,
        title: str,
        severity: str,
        affected_assets: List[str],
        apply_quarantine: bool = True
    ) -> Dict[str, Any]:
        """Creates a security incident and optionally isolates assets."""
        payload = {
            "title": title,
            "severity": severity,
            "affected_assets": affected_assets,
            "apply_quarantine": apply_quarantine
        }
        return self._client._request("POST", "/v1/security-hardening/incidents", json_data=payload)

    def resolve_incident(self, incident_id: str, root_cause: str = "Patched and verified") -> Dict[str, Any]:
        """Resolves security incident and lifts quarantine."""
        return self._client._request("POST", f"/v1/security-hardening/incidents/{incident_id}/resolve", json_data={"incident_id": incident_id, "root_cause": root_cause})

    def simulate_dr(self, component: str, snapshot_payload: str) -> Dict[str, Any]:
        """Executes disaster recovery simulation."""
        return self._client._request("POST", "/v1/security-hardening/disaster-recovery/simulate", json_data={"component": component, "snapshot_payload": snapshot_payload})

    def simulate_outage(self, service_name: str) -> Dict[str, Any]:
        """Demonstrates safe degradation without fabrication."""
        return self._client._request("GET", f"/v1/security-hardening/outage/simulate/{service_name}")

    def place_legal_hold(self, record_id: str, tenant_id: str) -> Dict[str, Any]:
        """Places legal hold on data record."""
        return self._client._request("POST", "/v1/security-hardening/retention/legal-hold", json_data={"record_id": record_id, "tenant_id": tenant_id})

    def delete_record(self, record_id: str) -> Dict[str, Any]:
        """Attempts record deletion, blocked under legal hold."""
        return self._client._request("DELETE", f"/v1/security-hardening/retention/records/{record_id}")

    def list_findings(self) -> List[Dict[str, Any]]:
        """Lists security findings."""
        return self._client._request("GET", "/v1/security-hardening/findings")

    def get_scorecard(self) -> Dict[str, Any]:
        """Gets platform security scorecard."""
        return self._client._request("GET", "/v1/security-hardening/scorecard")

    def evaluate_release_gate(self) -> Dict[str, Any]:
        """Evaluates production security release gate."""
        return self._client._request("GET", "/v1/security-hardening/release-gate")


class _BenchmarkingNamespace:
    """Prompt 33: Scientific Benchmarking & Validation."""
    def __init__(self, client: ZMIE):
        self._client = client

    def run(self, dataset: str = "NEGATIVE_CONTROLS") -> Dict[str, Any]:
        """Runs standardized scientific benchmark suite across golden test batteries."""
        return self._client._request("POST", "/v1/benchmarking/run", json_data={"dataset": dataset})

    def list_reports(self) -> List[Dict[str, Any]]:
        """Lists all executed benchmark run reports."""
        return self._client._request("GET", "/v1/benchmarking/reports")

    def get_report(self, run_id: str) -> Dict[str, Any]:
        """Gets benchmark report by ID."""
        return self._client._request("GET", f"/v1/benchmarking/reports/{run_id}")

    def generate_validation_report(self) -> Dict[str, Any]:
        """Generates comprehensive scientific validation report across all 24 dimensions."""
        return self._client._request("POST", "/v1/benchmarking/validation-report")

    def list_validation_reports(self) -> List[Dict[str, Any]]:
        """Lists all comprehensive scientific validation reports."""
        return self._client._request("GET", "/v1/benchmarking/validation-reports")

    def get_validation_report(self, report_id: str) -> Dict[str, Any]:
        """Gets scientific validation report by ID."""
        return self._client._request("GET", f"/v1/benchmarking/validation-reports/{report_id}")

    def get_go_no_go_matrix(self) -> Dict[str, str]:
        """Gets latest production Go / No-Go decision matrix."""
        return self._client._request("GET", "/v1/benchmarking/go-no-go-matrix")

    def list_datasets(self) -> List[str]:
        """Lists available golden benchmark datasets."""
        return self._client._request("GET", "/v1/benchmarking/datasets")


class _ProductionReadinessNamespace:
    """Prompt 34: Production Readiness Audit."""
    def __init__(self, client: ZMIE):
        self._client = client

    def preflight_audit(self) -> Dict[str, Any]:
        """Executes 7-pillar preflight readiness audit and returns signed certificate."""
        return self._client._request("POST", "/v1/production-readiness/preflight-audit")

    def list_certificates(self) -> List[Dict[str, Any]]:
        """Lists all issued production readiness certificates."""
        return self._client._request("GET", "/v1/production-readiness/certificates")

    def get_certificate(self, cert_id: str) -> Dict[str, Any]:
        """Gets certificate by ID."""
        return self._client._request("GET", f"/v1/production-readiness/certificates/{cert_id}")

    def get_domains(self) -> Dict[str, Any]:
        """Gets comprehensive 28-domain production readiness matrix."""
        return self._client._request("GET", "/v1/production-readiness/domains")

    def get_scopes(self) -> Dict[str, Any]:
        """Gets targeted 9 production readiness scope profiles."""
        return self._client._request("GET", "/v1/production-readiness/scopes")

    def get_manifest(self) -> Dict[str, Any]:
        """Gets release candidate manifest with hashes."""
        return self._client._request("GET", "/v1/production-readiness/manifest")

    def get_risks(self) -> List[Dict[str, Any]]:
        """Gets active production risk register."""
        return self._client._request("GET", "/v1/production-readiness/risks")

    def get_blockers(self) -> List[Dict[str, Any]]:
        """Gets verified production blocker registry."""
        return self._client._request("GET", "/v1/production-readiness/blockers")


class _ControlledLaunchNamespace:
    """Prompt 35: Controlled Launch & Continuous Monitoring."""
    def __init__(self, client: ZMIE):
        self._client = client

    def get_plan(self) -> Dict[str, Any]:
        """Gets progressive ring rollout plan and canary telemetry."""
        return self._client._request("GET", "/v1/controlled-launch/plan")

    def promote(self) -> Dict[str, Any]:
        """Promotes rollout to next delivery ring."""
        return self._client._request("POST", "/v1/controlled-launch/promote")

    def rollback(self, reason: str) -> Dict[str, Any]:
        """Triggers circuit breaker rollback to safe ring."""
        return self._client._request("POST", "/v1/controlled-launch/rollback", json_data={"reason": reason})

    def get_telemetry(self) -> Dict[str, Any]:
        """Gets real-time continuous health monitoring telemetry."""
        return self._client._request("GET", "/v1/controlled-launch/telemetry")

    def simulate_tripwire(self, cause: str = "CITATION_FABRICATION_DETECTED", details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Simulates automated tripwire condition triggering circuit breaker rollback."""
        return self._client._request("POST", "/v1/controlled-launch/simulate-tripwire", json_data={"cause": cause, "details": details or {}})

    def get_daemons(self) -> List[Dict[str, Any]]:
        """Gets status of all 5 autonomous monitoring daemons."""
        return self._client._request("GET", "/v1/controlled-launch/daemons")

    def get_slos(self) -> Dict[str, Any]:
        """Gets platform SLOs, canary metrics, and remaining error budget."""
        return self._client._request("GET", "/v1/controlled-launch/slos")

    def generate_launch_report(self) -> Dict[str, Any]:
        """Clause 317: Produces the official ZMIE Controlled Production Launch Report with signed governance authorization."""
        return self._client._request("POST", "/v1/controlled-launch/launch-report")

    def issue_scope_certificate(self) -> Dict[str, Any]:
        """Clause 297: Issues the official cryptographic ZMIE Production Scope Certificate."""
        return self._client._request("POST", "/v1/controlled-launch/scope-certificate")

    def log_incident(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clauses 137-148: Logs production incident. If severity is P0, automatically executes rollback."""
        return self._client._request("POST", "/v1/controlled-launch/incidents", json_data=incident_data)


class _LifecycleNamespace:
    """Master Production Lifecycle: Production -> Monitor -> Revalidate -> Benchmark -> Audit -> Improve -> Release"""
    def __init__(self, client: ZMIE):
        self._client = client

    def run(self, initial_version: str = "v1.0.0", target_version: str = "v1.1.0") -> Dict[str, Any]:
        """Executes the complete 7-stage master production lifecycle atomically."""
        return self._client._request("POST", "/v1/lifecycle/run", json_data={
            "initial_version": initial_version,
            "target_version": target_version
        })

    def get_stages(self) -> Dict[str, Any]:
        """Gets summary and sequence of the 7 master lifecycle stages."""
        return self._client._request("GET", "/v1/lifecycle/stages")


# Alias
ZMIEClient = ZMIE


