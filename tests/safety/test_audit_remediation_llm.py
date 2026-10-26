"""
Test Suite Verifying Phase 3 Audit Remediation (LLM Gateway & Data Egress):
- Verification that offline/failed LLM returns fail-closed diagnostic and ZERO false human trials
- Verification that Data Egress policy blocks RESTRICTED and PHI data
- Verification that structured extraction strictly fails closed rather than returning unvalidated mocks
"""

import unittest
import asyncio
from pydantic import BaseModel, Field
from app.core.llm_gateway import (
    LLMGateway,
    ModelUnavailableError,
    ExtractionFailedError,
    DataEgressViolationError
)


class MockClinicalExtraction(BaseModel):
    herb_name: str
    target_receptor: str
    verified_rct: bool = False


class TestAuditRemediationLLM(unittest.TestCase):

    def test_01_no_fabricated_human_trials_in_fallback(self):
        """Offline synthesis must NOT assert human clinical trials or physiological validation."""
        synthesis = LLMGateway.generate_synthesis(
            query="Fumaria parviflora in Hepatic Cirrhosis",
            evidence_context="No direct human clinical trials found."
        )
        self.assertIn("[MODEL_UNAVAILABLE]", synthesis)
        self.assertNotIn("verified human trials", synthesis.lower())
        self.assertNotIn("physiological mechanisms", synthesis.lower())

    def test_02_data_egress_blocks_restricted_and_phi(self):
        """Outbound LLM dispatch must default-deny RESTRICTED or PHI data."""
        with self.assertRaises(DataEgressViolationError):
            LLMGateway.check_data_egress_authorization(
                data="Patient John Doe DOB 1975-04-12 SSN 123-45-6789",
                classification="PHI"
            )

        with self.assertRaises(DataEgressViolationError):
            LLMGateway.check_data_egress_authorization(
                data="Proprietary military phytochemistry formula",
                classification="RESTRICTED"
            )

        # Public data should pass egress check
        self.assertTrue(
            LLMGateway.check_data_egress_authorization(
                data="Berberine pharmacological mechanism in AMPK activation",
                classification="PUBLIC"
            )
        )

    def test_03_structured_extraction_fails_closed(self):
        """Structured data extraction must fail closed instead of returning unvalidated mock."""
        async def run_extraction():
            return await LLMGateway.extract_structured_data(
                prompt="Raw unverified text",
                response_model=MockClinicalExtraction
            )

        # In unconfigured / mock test environment without live key, must raise ExtractionFailedError
        with self.assertRaises(ExtractionFailedError):
            asyncio.run(run_extraction())


if __name__ == "__main__":
    unittest.main()
