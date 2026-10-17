"""
ZMIE Global Medical Knowledge Network API Router (Phase V5)
"""

from fastapi import APIRouter, Query
from app.agents.global_network import GlobalKnowledgeNetworkRouter, GlobalNetworkQueryResponse

router = APIRouter(prefix="/global-network", tags=["Global Medical Knowledge Network (Phase V5)"])


@router.get("/federate", response_model=GlobalNetworkQueryResponse)
async def query_global_sovereign_network(q: str = Query(..., description="Global cross-jurisdictional medical query")):
    """
    Federates query across WHO, Ministry of Ayush/TKDL, NLM, and Europe PMC sovereign nodes.
    """
    return GlobalKnowledgeNetworkRouter.federate_global_network(query=q)
