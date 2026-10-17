"""
ZMIE Federated Research & Privacy Clean Room Engine
Prompt 15 Master Implementation.

Executes privacy-preserving federated queries across hospital nodes without
centralizing raw patient data. Enforces:
- HMAC Tokenization & Pseudonymization (research_subject_id)
- Small-Cell Suppression (counts < 5 obscured to prevent linkage attacks)
- Multi-site Clean Room aggregation
"""

import hmac
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.models.rwe_interop import FederatedQueryRequest, FederatedQueryResult


class FederatedResearchCleanRoom:
    """
    Simulates and orchestrates multi-site federated research queries with strict
    k-anonymity and small-cell disclosure protection.
    """

    def __init__(self, salt: str = "ZMIE_SOVEREIGN_FEDERATION_SALT_2026"):
        self.salt = salt.encode("utf-8")
        self._node_catalogs: Dict[str, Dict[str, int]] = {
            "HOSP_OXFORD": {
                "heart_failure_sglt2": 14200,
                "type2_diabetes": 38400,
                "rare_cardiomyopathy_pediatric": 3,  # Small cell to test suppression!
            },
            "HOSP_BRIGHAM": {
                "heart_failure_sglt2": 18900,
                "type2_diabetes": 45100,
                "rare_cardiomyopathy_pediatric": 2,  # Small cell to test suppression!
            },
            "NIUM_BLR": {
                "heart_failure_sglt2": 2100,
                "khamira_abresham_exposure": 8400,
                "su_e_mizaj_cardiac": 6200,
                "rare_cardiomyopathy_pediatric": 1,  # Small cell to test suppression!
            },
            "AIIA_DELHI": {
                "heart_failure_sglt2": 3100,
                "hridroga_ayurveda": 9100,
                "rare_cardiomyopathy_pediatric": 4,  # Small cell to test suppression!
            }
        }

    def tokenize_patient_id(self, raw_patient_id: str, source_facility: str) -> str:
        """
        Generates irreversible research_subject_id via HMAC-SHA256 tokenization.
        Prevents exposure of direct hospital MRNs in analytics.
        """
        msg = f"{source_facility}:{raw_patient_id}".encode("utf-8")
        token = hmac.new(self.salt, msg, hashlib.sha256).hexdigest()[:16]
        return f"SUBJ-{token.upper()}"

    def execute_federated_query(self, req: FederatedQueryRequest) -> FederatedQueryResult:
        """
        Executes federated count query across participating nodes, applying
        small-cell suppression for counts below threshold.
        """
        condition_key = req.cohort_criteria.get("cohort_key", "heart_failure_sglt2")
        threshold = req.privacy_cell_threshold

        contributions: Dict[str, int] = {}
        total_eligible = 0
        suppressed_cells = 0

        for node in req.participating_nodes:
            if node in self._node_catalogs:
                raw_count = self._node_catalogs[node].get(condition_key, 0)
                if raw_count < threshold:
                    # Small-cell suppression
                    suppressed_cells += 1
                    contributions[node] = 0  # Zeroed or obscured for privacy protection
                else:
                    contributions[node] = raw_count
                    total_eligible += raw_count

        return FederatedQueryResult(
            query_id=req.query_id,
            total_eligible_patients=total_eligible,
            participating_nodes_count=len(req.participating_nodes),
            node_contributions=contributions,
            small_cells_suppressed_count=suppressed_cells,
            privacy_guarantee=(
                f"K_ANONYMITY_PROTECTED: Any institutional cell with < {threshold} subjects "
                f"is strictly suppressed to prevent re-identification linkage attacks."
            ),
            execution_timestamp=datetime.utcnow()
        )
