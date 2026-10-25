"""
ZMIE Scientific Benchmarking & Validation Acceptance Test Suite
Scientific Benchmarking Certification — Multi-Domain Golden Batteries
"""

import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.benchmarking.engine import ScientificBenchmarkingEngine
from app.benchmarking.models import (
    BenchmarkDatasetType,
    BenchmarkItemVerdict,
    ValidationDimension,
    GoNoGoDecision,
)
from zmie import ZMIEClient
from app.platform.gateway import APIGatewayEngine


class TestPrompt33BenchmarkingAcceptance(unittest.TestCase):
    def setUp(self):
        self.engine = ScientificBenchmarkingEngine()
        raw_key, _ = APIGatewayEngine.create_api_key(
            tenant_id="tenant-benchmarking",
            owner="benchmark@zmie.org",
            name="Benchmarking Test Key",
            scopes=["knowledge:read", "rag:read", "safety:read", "search:read", "evidence:read"]
        )
        self.sdk_client = ZMIEClient(api_key=raw_key, app_instance=app)

    def test_01_negative_controls_zero_hallucination(self):
        """Negative controls benchmark MUST return UNKNOWN with strictly 0% hallucination rate (INV-01)."""
        report = self.engine.run_benchmark_suite(BenchmarkDatasetType.NEGATIVE_CONTROLS)
        self.assertEqual(report.total_cases, 3)
        self.assertEqual(report.passed_cases, 3)
        self.assertEqual(report.failed_cases, 0)
        self.assertEqual(report.accuracy, 1.0)
        self.assertEqual(report.hallucination_rate, 0.0)
        for res in report.case_results:
            self.assertEqual(res.verdict, BenchmarkItemVerdict.UNKNOWN_CORRECT)
            self.assertEqual(res.actual_status, "UNKNOWN")
            self.assertFalse(res.hallucination_detected)

    def test_02_medqa_usmle_clinical_reasoning(self):
        """MedQA benchmark must correctly identify myocardial infarction, hypertension, and croup management."""
        report = self.engine.run_benchmark_suite(BenchmarkDatasetType.MEDQA_USMLE)
        self.assertEqual(report.accuracy, 1.0)
        self.assertEqual(report.failed_cases, 0)
        self.assertEqual(report.citation_fidelity, 1.0)
        for res in report.case_results:
            self.assertEqual(res.verdict, BenchmarkItemVerdict.PASSED)
            self.assertEqual(res.actual_status, "CLINICALLY_VALIDATED")

    def test_03_traditional_epistemic_preservation(self):
        """Traditional medicine benchmark must preserve epistemic distance without 1:1 false equivalences."""
        report = self.engine.run_benchmark_suite(BenchmarkDatasetType.TRADITIONAL_EPISTEMIC)
        self.assertEqual(report.accuracy, 1.0)
        self.assertGreaterEqual(report.epistemic_distance_preservation, 0.70)
        case_res = report.case_results[0]
        self.assertIn("0.78", case_res.actual_response)
        self.assertEqual(case_res.actual_status, "EPISTEMIC_DISTANCE_PRESERVED")

    def test_04_drug_herb_interaction_safety(self):
        """Drug-herb safety benchmark must detect potent CYP3A4 induction and bleeding contraindications."""
        report = self.engine.run_benchmark_suite(BenchmarkDatasetType.DRUG_HERB_SAFETY)
        self.assertEqual(report.accuracy, 1.0)
        case_res1 = report.case_results[0]
        self.assertEqual(case_res1.actual_status, "CONTRAINDICATED")
        self.assertIn("CYP3A4", case_res1.actual_response)

        case_res2 = report.case_results[1]
        self.assertEqual(case_res2.actual_status, "CONTRAINDICATED")
        self.assertIn("bleeding", case_res2.actual_response.lower())

    def test_05_benchmark_report_retrieval(self):
        """Benchmark reports must be stored and retrievable by run_id."""
        report = self.engine.run_benchmark_suite(BenchmarkDatasetType.NEGATIVE_CONTROLS)
        fetched = self.engine.get_run_report(report.run_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.run_id, report.run_id)

        all_reports = self.engine.list_run_reports()
        self.assertGreaterEqual(len(all_reports), 1)

    def test_06_citation_fidelity_fabrication_rejection(self):
        """Citation fidelity battery must detect and reject fabricated DOIs while validating canonical ones."""
        report = self.engine.run_benchmark_suite(BenchmarkDatasetType.CITATION_FIDELITY)
        self.assertEqual(report.accuracy, 1.0)
        self.assertEqual(report.total_cases, 2)
        # Check fabricated DOI rejection
        fake_cite_res = next(r for r in report.case_results if r.case_id == "cite-001")
        self.assertEqual(fake_cite_res.actual_status, "REJECTED_UNAUTHENTIC")
        self.assertFalse(fake_cite_res.citation_valid)
        self.assertIn("FABRICATED_CITATION_DETECTED", fake_cite_res.actual_response)

        # Check canonical DOI verification
        real_cite_res = next(r for r in report.case_results if r.case_id == "cite-002")
        self.assertEqual(real_cite_res.actual_status, "SOURCE_VERIFIED")
        self.assertTrue(real_cite_res.citation_valid)

    def test_07_scientific_numerical_calculation_precision(self):
        """Scientific calculation battery must verify ARR, NNT, and CrCl with 0% calculation error."""
        report = self.engine.run_benchmark_suite(BenchmarkDatasetType.SCIENTIFIC_CALCULATION)
        self.assertEqual(report.accuracy, 1.0)
        self.assertEqual(report.calculation_precision, 1.0)
        for res in report.case_results:
            self.assertFalse(res.calculation_error)
            self.assertEqual(res.actual_status, "CALCULATION_VERIFIED")
        # Check specific values
        arr_res = next(r for r in report.case_results if r.case_id == "calc-001")
        self.assertIn("ARR = 0.04", arr_res.actual_response)
        self.assertIn("NNT = 25.0", arr_res.actual_response)

    def test_08_causal_mechanistic_overclaim_prevention(self):
        """Causal mechanistic battery must block causal overclaims and in-vitro extrapolations."""
        report = self.engine.run_benchmark_suite(BenchmarkDatasetType.CAUSAL_MECHANISTIC)
        self.assertEqual(report.accuracy, 1.0)
        self.assertEqual(report.causal_integrity_score, 1.0)
        for res in report.case_results:
            self.assertEqual(res.verdict, BenchmarkItemVerdict.OVERCLAIM_PREVENTED)
            self.assertEqual(res.actual_status, "OVERCLAIM_PREVENTED")
            self.assertFalse(res.causal_overclaim_detected)

    def test_09_regulatory_jurisdiction_segregation(self):
        """Regulatory jurisdiction battery must isolate EMA vs US FDA and CDSCO regulatory boundaries."""
        report = self.engine.run_benchmark_suite(BenchmarkDatasetType.REGULATORY_JURISDICTION)
        self.assertEqual(report.accuracy, 1.0)
        self.assertEqual(report.jurisdiction_compliance_score, 1.0)
        for res in report.case_results:
            self.assertEqual(res.verdict, BenchmarkItemVerdict.JURISDICTION_SECLUDED)
            self.assertEqual(res.actual_status, "JURISDICTION_SECLUDED")
            self.assertTrue(res.jurisdiction_isolated)

    def test_10_reproducibility_deterministic_replay(self):
        """Reproducibility replay battery must verify bit-identical output hash matches with 0.0% divergence."""
        report = self.engine.run_benchmark_suite(BenchmarkDatasetType.REPRODUCIBILITY_REPLAY)
        self.assertEqual(report.accuracy, 1.0)
        case_res = report.case_results[0]
        self.assertEqual(case_res.actual_status, "REPRODUCIBLE")
        self.assertIn("divergence_rate=0.0%", case_res.actual_response)

    def test_11_cross_tenant_isolation_and_security_defense(self):
        """Security and privacy integrity battery must enforce tenant barrier and reject adversarial injection."""
        report = self.engine.run_benchmark_suite(BenchmarkDatasetType.SECURITY_PRIVACY_INTEGRITY)
        self.assertEqual(report.accuracy, 1.0)
        tenant_res = next(r for r in report.case_results if r.case_id == "sec-001")
        self.assertEqual(tenant_res.actual_status, "ISOLATION_ENFORCED")

        prompt_res = next(r for r in report.case_results if r.case_id == "sec-002")
        self.assertEqual(prompt_res.actual_status, "FABRICATION_REJECTED")

    def test_12_evidence_extraction_pico_accuracy(self):
        """Evidence extraction battery must extract PICO parameters, odds ratios, and sample sizes accurately."""
        report = self.engine.run_benchmark_suite(BenchmarkDatasetType.EVIDENCE_EXTRACTION)
        self.assertEqual(report.accuracy, 1.0)
        for res in report.case_results:
            self.assertEqual(res.actual_status, "PICO_EXTRACTED_EXACT")

    def test_13_comprehensive_validation_report_and_go_no_go_matrix(self):
        """Validation report generator must evaluate all 24 dimensions and produce an unambiguous GO decision."""
        val_report = self.engine.generate_scientific_validation_report()
        self.assertIsNotNone(val_report.report_id)
        self.assertEqual(val_report.overall_decision, GoNoGoDecision.GO)
        self.assertTrue(val_report.is_production_candidate)
        self.assertEqual(val_report.total_batteries, len(BenchmarkDatasetType))
        self.assertEqual(val_report.passed_batteries, len(BenchmarkDatasetType))
        self.assertEqual(val_report.citation_hallucination_rate, 0.0)
        self.assertEqual(val_report.calculation_error_rate, 0.0)
        self.assertEqual(val_report.reproducibility_divergence_rate, 0.0)
        self.assertEqual(val_report.cross_tenant_leakage_rate, 0.0)
        self.assertEqual(len(val_report.dimension_evaluations), 24)
        self.assertEqual(len(val_report.go_no_go_matrix), 24)
        self.assertEqual(len(val_report.certification_hash), 64)

        # Check critical dimensions are GO
        self.assertEqual(val_report.go_no_go_matrix[ValidationDimension.ZERO_HALLUCINATION_NEGATIVE_CONTROLS.value], "GO")
        self.assertEqual(val_report.go_no_go_matrix[ValidationDimension.CITATION_ACCURACY_ATTRIBUTION.value], "GO")
        self.assertEqual(val_report.go_no_go_matrix[ValidationDimension.SCIENTIFIC_NUMERICAL_CALCULATION.value], "GO")
        self.assertEqual(val_report.go_no_go_matrix[ValidationDimension.PHARMACOLOGICAL_DRUG_HERB_SAFETY.value], "GO")
        self.assertEqual(val_report.go_no_go_matrix[ValidationDimension.TENANT_PRIVACY_SECURITY_ISOLATION.value], "GO")

    def test_14_fastapi_and_sdk_integration(self):
        """FastAPI endpoints and SDK client methods must provide end-to-end access to validation & matrices."""
        # Test SDK list datasets
        datasets = self.sdk_client.benchmarking.list_datasets()
        self.assertIn("NEGATIVE_CONTROLS", datasets)
        self.assertIn("CITATION_FIDELITY", datasets)
        self.assertIn("SCIENTIFIC_CALCULATION", datasets)

        # Test SDK run benchmark
        run_res = self.sdk_client.benchmarking.run("NEGATIVE_CONTROLS")
        self.assertEqual(run_res["accuracy"], 1.0)
        self.assertEqual(run_res["hallucination_rate"], 0.0)

        # Test SDK generate validation report
        val_rep = self.sdk_client.benchmarking.generate_validation_report()
        self.assertEqual(val_rep["overall_decision"], "GO")
        self.assertTrue(val_rep["is_production_candidate"])
        self.assertEqual(len(val_rep["dimension_evaluations"]), 24)

        # Test SDK get Go/No-Go matrix
        matrix = self.sdk_client.benchmarking.get_go_no_go_matrix()
        self.assertIn("ZERO_HALLUCINATION_NEGATIVE_CONTROLS", matrix)
        self.assertEqual(matrix["ZERO_HALLUCINATION_NEGATIVE_CONTROLS"], "GO")


if __name__ == "__main__":
    unittest.main()
