"""
Acceptance Tests for ZMIE Commercial Billing & Institutional Procurement Subsystem
"""

import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestCommercialBillingAcceptance(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_01_list_available_plans(self):
        resp = self.client.get("/v1/billing/plans")
        self.assertEqual(resp.status_code, 200)
        plans = resp.json()
        self.assertGreaterEqual(len(plans), 3)
        plan_ids = [p["plan_id"] for p in plans]
        self.assertIn("free_community", plan_ids)
        self.assertIn("pro_monthly", plan_ids)
        self.assertIn("hospital_enterprise", plan_ids)

    def test_02_process_pro_monthly_checkout(self):
        payload = {
            "plan_id": "pro_monthly",
            "customer_name": "Dr. Irfan Ashraf",
            "customer_email": "dr.ashraf@hospital.org",
            "card_last4": "4242"
        }
        resp = self.client.post("/v1/billing/checkout", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "active")
        self.assertTrue(data["subscription_id"].startswith("sub_zmie_"))
        self.assertEqual(data["amount_charged_usd"], 29.0)
        self.assertEqual(data["billing_cycle"], "Monthly")
        self.assertTrue(len(data["cryptographic_receipt_signature"]) > 20)

    def test_03_process_pro_annual_with_promo(self):
        payload = {
            "plan_id": "pro_annual",
            "customer_name": "Dr. Irfan Ashraf",
            "customer_email": "dr.ashraf@hospital.org",
            "card_last4": "1234",
            "promo_code": "CLINICIAN10"
        }
        resp = self.client.post("/v1/billing/checkout", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "active")
        # 290 - 10% = 261.0
        self.assertEqual(data["amount_charged_usd"], 261.0)
        self.assertEqual(data["billing_cycle"], "Annual")

    def test_04_process_enterprise_inquiry_and_tenant_sizing(self):
        payload = {
            "organization_name": "Cleveland Clinic Health",
            "contact_name": "Dr. Michael Chen, VP Clinical Systems",
            "work_email": "mchen@ccf.org",
            "clinician_seats": 75,
            "ehr_system": "Epic Systems",
            "request_baa": True
        }
        resp = self.client.post("/v1/billing/enterprise-inquiry", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "pilot_provisioned")
        self.assertIn("tenant-cleveland-clinic-ctu", data["provisioned_pilot_tenant_id"])
        # Base 9500 + (75 - 25)*120 = 9500 + 6000 = 15500
        self.assertEqual(data["annual_estimate_usd"], 15500.0)
        self.assertEqual(data["baa_contract_status"], "EXECUTABLE_DRAFT_READY")
        self.assertTrue(len(data["cryptographic_proposal_hash"]) > 20)

if __name__ == "__main__":
    unittest.main()
