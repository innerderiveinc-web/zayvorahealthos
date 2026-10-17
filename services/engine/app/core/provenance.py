"""
ZMIE Enterprise Canonical Provenance Engine (PROV-O Compliant)
Prompt 28 — MODULE 07 (Provenance Foundation) & Clause 20

Provides universal provenance operations:
- create_provenance()
- attach_provenance()
- get_provenance()
- trace_backward()
- trace_forward()

Ensures all scientific, clinical, and computational mutations share an interoperable
cryptographic lineage graph.
"""

import hashlib
import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any, Set
from pydantic import BaseModel, Field


class ProvActivityType(str, Enum):
    INGESTION = "ingestion"
    PARSING = "parsing"
    ENTITY_EXTRACTION = "entity_extraction"
    CLAIM_SYNTHESIS = "claim_synthesis"
    STATISTICAL_COMPUTE = "statistical_compute"
    IN_SILICO_SIMULATION = "in_silico_simulation"
    RETRACTION_INVALIDATION = "retraction_invalidation"
    HUMAN_CURATION = "human_curation"


class ProvenanceNode(BaseModel):
    provenance_id: str
    target_id: str
    activity_type: ProvActivityType
    agent_id: str  # User, model, or background daemon
    parent_ids: List[str] = Field(default_factory=list)  # Backward inputs (wasDerivedFrom)
    child_ids: List[str] = Field(default_factory=list)   # Forward outputs
    metadata: Dict[str, Any] = Field(default_factory=dict)
    content_hash: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProvenanceGraph:
    """In-memory or persistent PROV-O compliant lineage storage."""
    def __init__(self):
        self._nodes: Dict[str, ProvenanceNode] = {}
        self._target_to_prov: Dict[str, str] = {}

    def create_provenance(
        self,
        target_id: str,
        activity_type: ProvActivityType,
        agent_id: str,
        input_ids: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ProvenanceNode:
        """Creates an immutable provenance node and links it to its inputs."""
        input_ids = input_ids or []
        meta = metadata or {}
        
        # Compute deterministic hash of inputs, agent, and target
        hash_input = f"{target_id}:{activity_type.value}:{agent_id}:{','.join(sorted(input_ids))}:{json.dumps(meta, sort_keys=True, default=str)}"
        content_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()
        
        prov_id = f"prov-{uuid.uuid4().hex[:12]}"
        node = ProvenanceNode(
            provenance_id=prov_id,
            target_id=target_id,
            activity_type=activity_type,
            agent_id=agent_id,
            parent_ids=input_ids,
            child_ids=[],
            metadata=meta,
            content_hash=content_hash,
            timestamp=datetime.now(timezone.utc)
        )
        
        self._nodes[prov_id] = node
        self._target_to_prov[target_id] = prov_id
        
        # Link child references in parents
        for pid in input_ids:
            parent_prov_id = self._target_to_prov.get(pid, pid)
            if parent_prov_id in self._nodes:
                if prov_id not in self._nodes[parent_prov_id].child_ids:
                    self._nodes[parent_prov_id].child_ids.append(prov_id)

        return node

    def attach_provenance(self, resource_dict: Dict[str, Any], prov_node: ProvenanceNode) -> Dict[str, Any]:
        """Attaches provenance metadata and verification hash directly to a domain resource."""
        resource_dict["provenance_id"] = prov_node.provenance_id
        resource_dict["provenance_hash"] = prov_node.content_hash
        resource_dict["lineage_parents"] = prov_node.parent_ids
        return resource_dict

    def get_provenance(self, provenance_or_target_id: str) -> Optional[ProvenanceNode]:
        """Retrieves a provenance record by either provenance_id or target_id."""
        if provenance_or_target_id in self._nodes:
            return self._nodes[provenance_or_target_id]
        if provenance_or_target_id in self._target_to_prov:
            prov_id = self._target_to_prov[provenance_or_target_id]
            return self._nodes.get(prov_id)
        return None

    def trace_backward(self, target_or_prov_id: str, max_depth: int = 10) -> List[ProvenanceNode]:
        """
        Traces backward ancestry from an entity to all foundational source inputs.
        """
        root_node = self.get_provenance(target_or_prov_id)
        if not root_node:
            return []

        visited: Set[str] = set()
        lineage: List[ProvenanceNode] = []
        queue = [(root_node, 0)]

        while queue:
            curr_node, depth = queue.pop(0)
            if curr_node.provenance_id in visited or depth > max_depth:
                continue
            visited.add(curr_node.provenance_id)
            lineage.append(curr_node)

            for parent_target in curr_node.parent_ids:
                pnode = self.get_provenance(parent_target)
                if pnode and pnode.provenance_id not in visited:
                    queue.append((pnode, depth + 1))

        return lineage

    def trace_forward(self, target_or_prov_id: str, max_depth: int = 10) -> List[ProvenanceNode]:
        """
        Traces forward lineage to identify all downstream claims or computations
        derived from this entity (essential for retraction impact analysis).
        """
        root_node = self.get_provenance(target_or_prov_id)
        if not root_node:
            return []

        visited: Set[str] = set()
        impact: List[ProvenanceNode] = []
        queue = [(root_node, 0)]

        while queue:
            curr_node, depth = queue.pop(0)
            if curr_node.provenance_id in visited or depth > max_depth:
                continue
            visited.add(curr_node.provenance_id)
            impact.append(curr_node)

            for child_prov_id in curr_node.child_ids:
                cnode = self.get_provenance(child_prov_id)
                if cnode and cnode.provenance_id not in visited:
                    queue.append((cnode, depth + 1))

        return impact


# Singleton Global Provenance Engine Instance
_global_provenance_engine: Optional[ProvenanceGraph] = None


def get_provenance_engine() -> ProvenanceGraph:
    global _global_provenance_engine
    if _global_provenance_engine is None:
        _global_provenance_engine = ProvenanceGraph()
    return _global_provenance_engine


# Canonical Global Shortcuts
def create_provenance(
    target_id: str,
    activity_type: ProvActivityType,
    agent_id: str,
    input_ids: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> ProvenanceNode:
    return get_provenance_engine().create_provenance(target_id, activity_type, agent_id, input_ids, metadata)


def attach_provenance(resource_dict: Dict[str, Any], prov_node: ProvenanceNode) -> Dict[str, Any]:
    return get_provenance_engine().attach_provenance(resource_dict, prov_node)


def get_provenance(provenance_or_target_id: str) -> Optional[ProvenanceNode]:
    return get_provenance_engine().get_provenance(provenance_or_target_id)


def trace_backward(target_or_prov_id: str, max_depth: int = 10) -> List[ProvenanceNode]:
    return get_provenance_engine().trace_backward(target_or_prov_id, max_depth)


def trace_forward(target_or_prov_id: str, max_depth: int = 10) -> List[ProvenanceNode]:
    return get_provenance_engine().trace_forward(target_or_prov_id, max_depth)
