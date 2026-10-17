"""
ZMIE Enterprise Federated Search API Router (Phase V4)
"""

from fastapi import APIRouter
from app.agents.federated_connector import (
    FederatedKnowledgeConnector,
    FederatedQueryRequest,
    FederatedSearchResponse
)

router = APIRouter(prefix="/enterprise", tags=["Enterprise Federated Search & Private Cloud"])


@router.post("/federated-search", response_model=FederatedSearchResponse)
async def run_enterprise_federated_search(request: FederatedQueryRequest):
    """
    Executes federated evidence search across ZMIE public network + private institutional datasets.
    """
    return await FederatedKnowledgeConnector.execute_federated_search(request)
