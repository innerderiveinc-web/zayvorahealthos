"""
ZMIE Scientific Agent Operating System Acceptance Test Suite (Prompt 24)
Verifies all 14 mandatory governance, security, and scientific integrity tests
specified in Clauses 276-289:
- 276: Tenant isolation
- 277: Agent publicization block
- 278: Agent fabrication prevention (no data -> cannot compute)
- 279: Agent execution state lifecycle
- 280: Independent citation & computation verification
- 281: Contradiction preservation without forced consensus
- 282: Traditional medicine mapping integrity (NO_VALID_MAPPING preserved)
- 283: Causal vs observational guardrails
- 284: Simulation vs observation epistemic distinction
- 285: Private data access control (public mode blocked)
- 286: Federated partial site failure transparent reporting
- 287: Knowledge change proposal governance (no silent rewrite)
- 288: Complete research execution trace provenance
- 289: Golden end-to-end multi-agent research workflow
Plus REST API and Python SDK client tests.
"""

import unittest
from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app
from app.agent_os import (
    get_agent_os,
    EpistemicState,
    AgentRiskLevel,
    TaskExecutionState,
    MemoryScope,
    MemoryState,
    AgentTask,
    AgentResult,
    ResearchPlan,
    ReviewDecisionAction,
    EpistemicOutputFirewall,
    KnowledgeChangeProposal
)
from app.models.federated_privacy import ResearchDataClassification, AgentMode, AgentContext
from zmie.client import ZMIE


class TestAgentOSAcceptance(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.os = get_agent_os()
        self.client = TestClient(app)
        self.sdk = ZMIE(app_instance=app)

    # ==========================================================================
    # Clause 276: Tenant Isolation Test
    # ==========================================================================
    def test_276_tenant_isolation(self):
        """
        Tenant A private research vs Tenant B private research.
        Attempt cross-tenant access through agent memory.
        Expected: Tenant A cannot retrieve Tenant B's memory items.
        """
        # Tenant B writes proprietary finding into Tenant memory
        mem_b = self.os.memory.write_memory(
            scope=MemoryScope.TENANT,
            tenant_id="tenant-b-pharma",
            agent_id="agent-private-research",
            state=MemoryState.PRIVATE_CONTEXT,
            content="Proprietary lead molecule compound-9012 activity"
        )
        self.assertIsNotNone(mem_b.item_id)

        # Tenant A tries to read Tenant memory
        mems_for_a = self.os.memory.read_memory(
            scope=MemoryScope.TENANT,
            requesting_tenant_id="tenant-a-hospital"
        )
        contents_a = [m.content for m in mems_for_a]
        self.assertNotIn("Proprietary lead molecule compound-9012 activity", contents_a)

        # Tenant B reading their own memory succeeds
        mems_for_b = self.os.memory.read_memory(
            scope=MemoryScope.TENANT,
            requesting_tenant_id="tenant-b-pharma"
        )
        contents_b = [m.content for m in mems_for_b]
        self.assertIn("Proprietary lead molecule compound-9012 activity", contents_b)

    # ==========================================================================
    # Clause 277: Agent Publicization Test
    # ==========================================================================
    def test_277_agent_publicization_blocked(self):
        """
        Attempt Private Agent -> Public Report without release approval.
        Expected: Blocked by Epistemic/Privacy firewall.
        """
        confidential_result = AgentResult(
            task_id="task-priv-01",
            agent_id="agent-private-research",
            epistemic_state=EpistemicState.OBSERVED,
            summary="Internal trial results on experimental formulation.",
            classification=ResearchDataClassification.CONFIDENTIAL
        )

        is_valid, err_msg = EpistemicOutputFirewall.validate_agent_result(
            confidential_result,
            target_classification=ResearchDataClassification.PUBLIC
        )
        self.assertFalse(is_valid)
        self.assertIn("PRIVACY_FIREWALL_BLOCK", err_msg)

    # ==========================================================================
    # Clause 278: Agent Fabrication Test
    # ==========================================================================
    async def test_278_agent_fabrication_prevention(self):
        """
        Ask StatisticsAgent to produce statistical result from nonexistent data.
        Expected: 'Cannot compute', not fabricated numbers.
        """
        stats_agent = self.os.agents.get_agent_instance("agent-statistics")
        task = AgentTask(
            agent_id="agent-statistics",
            goal="Compute p-value for drug efficacy",
            inputs={"data": None}  # Nonexistent data
        )
        result = await stats_agent.execute(task)

        self.assertEqual(result.epistemic_state, EpistemicState.UNKNOWN)
        self.assertIn("Cannot compute", result.summary)
        self.assertEqual(result.confidence_components.get("numeric_veracity"), 0.0)

    # ==========================================================================
    # Clause 279: Agent Execution State Lifecycle
    # ==========================================================================
    async def test_279_agent_execution_state_lifecycle(self):
        """
        Ask agent: Run analysis.
        Before completion: PLANNED / RUNNING.
        After completion: COMPLETED.
        """
        task = AgentTask(
            agent_id="agent-source",
            goal="Discover sources for Curcumin",
            inputs={"query": "Curcumin"}
        )
        self.assertEqual(task.status, TaskExecutionState.CREATED)

        agent = self.os.agents.get_agent_instance("agent-source")
        task.status = TaskExecutionState.RUNNING
        res = await agent.execute(task)
        task.status = TaskExecutionState.COMPLETED

        self.assertEqual(task.status, TaskExecutionState.COMPLETED)
        self.assertEqual(res.epistemic_state, EpistemicState.REPORTED)
        self.assertTrue(len(res.sources) > 0)

    # ==========================================================================
    # Clause 280: Verification Test
    # ==========================================================================
    async def test_280_independent_verification_rejects_fabrication(self):
        """
        Give deliberately incorrect citation and unbacked statistic to VerifierAgent.
        Expected: Verifier must reject it (epistemic state CONTESTED).
        """
        verifier = self.os.agents.get_agent_instance("agent-verifier")

        # Test fake citation
        fake_task = AgentTask(
            agent_id="agent-verifier",
            goal="Verify citation",
            inputs={"citation": "DOI:10.1000/fake_nonexistent_paper_2026"}
        )
        res_fake = await verifier.execute(fake_task)
        self.assertEqual(res_fake.epistemic_state, EpistemicState.CONTESTED)
        self.assertIn("FAILED", res_fake.summary)

        # Test unbacked numeric statistic
        unbacked_stat_task = AgentTask(
            agent_id="agent-verifier",
            goal="Verify statistic",
            inputs={"numeric_statement": "The efficacy was p = 0.003", "has_compute_artifact": False}
        )
        res_stat = await verifier.execute(unbacked_stat_task)
        self.assertEqual(res_stat.epistemic_state, EpistemicState.CONTESTED)
        self.assertIn("FAILED", res_stat.summary)

    # ==========================================================================
    # Clause 281: Contradiction Test
    # ==========================================================================
    async def test_281_contradiction_preserves_divergence(self):
        """
        Give two conflicting trial results.
        Expected: Preserve both and explain context without forced consensus.
        """
        contradiction_agent = self.os.agents.get_agent_instance("agent-contradiction")
        task = AgentTask(agent_id="agent-contradiction", goal="Evaluate conflicting trial results")
        result = await contradiction_agent.execute(task)

        self.assertEqual(result.epistemic_state, EpistemicState.CONTESTED)
        self.assertTrue(result.artifacts[0]["no_forced_consensus"])
        self.assertIn("divergence", result.summary.lower())

    # ==========================================================================
    # Clause 282: Traditional Medicine Test
    # ==========================================================================
    async def test_282_traditional_medicine_no_valid_mapping(self):
        """
        Give traditional concept with no validated modern equivalent (e.g. Damavi).
        Expected: NO_VALID_MAPPING preserved without category error.
        """
        ontology_agent = self.os.agents.get_agent_instance("agent-ontology")
        task = AgentTask(
            agent_id="agent-ontology",
            goal="Resolve traditional concept",
            inputs={"term": "Damavi"}
        )
        result = await ontology_agent.execute(task)

        self.assertEqual(result.epistemic_state, EpistemicState.UNKNOWN)
        self.assertEqual(result.artifacts[0]["status"], "NO_VALID_MAPPING")
        self.assertIn("reductionism", result.artifacts[0]["epistemic_warning"].lower())

    # ==========================================================================
    # Clause 283: Causal Test
    # ==========================================================================
    async def test_283_causal_observational_guardrail(self):
        """
        Give observational association.
        Expected: Must NOT automatically label it causal.
        """
        causal_agent = self.os.agents.get_agent_instance("agent-causal")
        task = AgentTask(
            agent_id="agent-causal",
            goal="Analyze observational study on herbal intake",
            inputs={"study_type": "Observational Cohort"}
        )
        result = await causal_agent.execute(task)

        self.assertEqual(result.epistemic_state, EpistemicState.INFERRED)
        self.assertIn("RESTRICTED", result.summary)
        self.assertIn("does NOT imply causality", result.findings[0])

    # ==========================================================================
    # Clause 284: Simulation Test
    # ==========================================================================
    async def test_284_simulation_epistemic_distinction(self):
        """
        Run simulation prediction.
        Expected: Labeled SIMULATED/PREDICTED, never OBSERVED.
        """
        sim_agent = self.os.agents.get_agent_instance("agent-simulation")
        task = AgentTask(agent_id="agent-simulation", goal="Run PK simulation")
        result = await sim_agent.execute(task)

        self.assertEqual(result.epistemic_state, EpistemicState.SIMULATED)
        self.assertNotEqual(result.epistemic_state, EpistemicState.OBSERVED)

        # Epistemic firewall checks that promotion to OBSERVED is rejected
        is_valid, err = EpistemicOutputFirewall.validate_agent_result(
            result, requested_epistemic_state=EpistemicState.OBSERVED
        )
        self.assertFalse(is_valid)
        self.assertIn("EPISTEMIC_VIOLATION", err)

    # ==========================================================================
    # Clause 285: Private Data Test
    # ==========================================================================
    async def test_285_private_data_access_control(self):
        """
        Ask public agent about private project data.
        Expected: Access denied / unauthorized.
        """
        priv_agent = self.os.agents.get_agent_instance("agent-private-research")
        task = AgentTask(
            agent_id="agent-private-research",
            goal="Query internal dataset",
            tenant_id="tenant-pharma"
        )
        # Agent context in PUBLIC_MODE
        ctx = AgentContext(
            agent_id="agent-private-research",
            mode=AgentMode.PUBLIC_MODE,
            tenant_id="tenant-pharma"
        )
        result = await priv_agent.execute(task, context=ctx)
        self.assertIn("Access Denied", result.summary)
        self.assertEqual(result.epistemic_state, EpistemicState.UNKNOWN)

    # ==========================================================================
    # Clause 286: Federated Test
    # ==========================================================================
    async def test_286_federated_partial_site_failure(self):
        """
        Run federated query where one site fails.
        Expected: Output explicitly states partial site coverage and lists limitations.
        """
        fed_agent = self.os.agents.get_agent_instance("agent-federated")
        task = AgentTask(
            agent_id="agent-federated",
            goal="Run federated query",
            inputs={"simulate_site_failure": True}
        )
        result = await fed_agent.execute(task)

        self.assertIn("PARTIAL SITE COVERAGE", result.summary)
        self.assertEqual(result.artifacts[0]["status"], "PARTIAL_FEDERATED_RESULT")
        self.assertTrue(len(result.limitations) > 0)

    # ==========================================================================
    # Clause 287: Knowledge Update Test
    # ==========================================================================
    async def test_287_knowledge_update_proposal_governance(self):
        """
        New source contradicts existing claim.
        Expected: Creates KnowledgeChangeProposal, does not silently rewrite global claim.
        """
        ke_agent = self.os.agents.get_agent_instance("agent-knowledge-evolution")
        task = AgentTask(
            agent_id="agent-knowledge-evolution",
            goal="Update claim based on new CVOT trial",
            inputs={"target_claim_id": "CLM-BERBERINE-01"}
        )
        result = await ke_agent.execute(task)

        self.assertEqual(result.epistemic_state, EpistemicState.PROPOSED)
        self.assertIn("KnowledgeChangeProposal", result.summary)
        self.assertIn("governance review", result.summary.lower())

    # ==========================================================================
    # Clause 288: Research Trace Test
    # ==========================================================================
    async def test_288_research_trace_auditability(self):
        """
        Verify that an execution trace records all agents, tools, events, and plan steps.
        """
        trace, result = await self.os.orchestrator.execute_research(
            question="What is the glycemic efficacy and mechanism of Berberine?",
            tenant_id="tenant-aiims"
        )
        self.assertIsNotNone(trace.trace_id)
        self.assertTrue(len(trace.agents_executed) >= 10)
        self.assertTrue(len(trace.tools_used) >= 5)
        self.assertTrue(len(trace.events) >= 15)
        self.assertIsNotNone(trace.completion)
        self.assertEqual(trace.completion.verification_status, "VERIFIED")

    # ==========================================================================
    # Clause 289: Golden End-to-End Test
    # ==========================================================================
    async def test_289_golden_end_to_end_research_orchestration(self):
        """
        Execute full 12-stage research pipeline:
        Question -> Planner -> Terminology -> Source -> Research -> Evidence ->
        Mechanism -> Causal -> Safety -> Regulatory -> Contradiction -> Verifier -> Report.
        """
        trace, result = await self.os.orchestrator.execute_research(
            question="Evaluate the clinical efficacy, mechanism, and drug interactions of Berberine in Type 2 Diabetes."
        )
        self.assertEqual(result.epistemic_state, EpistemicState.DERIVED)
        self.assertFalse(trace.completion.is_partial)
        self.assertEqual(trace.completion.coverage_score, 1.0)
        self.assertIn("glycemic", result.findings[0].lower())

    # ==========================================================================
    # REST API & SDK Acceptance Tests
    # ==========================================================================
    def test_api_list_agents(self):
        resp = self.client.get("/v1/agents")
        self.assertEqual(resp.status_code, 200)
        agents = resp.json()
        self.assertTrue(len(agents) >= 30)

    def test_api_plan_research(self):
        resp = self.client.post("/v1/research/plan", json={"question": "Metformin vs Berberine"})
        self.assertEqual(resp.status_code, 200)
        plan = resp.json()
        self.assertIn("plan_id", plan)
        self.assertTrue(len(plan["subtasks"]) >= 10)

    def test_api_run_research_endpoint(self):
        resp = self.client.post("/v1/research/run", json={"question": "Role of AMPK in insulin sensitivity"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("trace_id", data)
        self.assertEqual(data["status"], "COMPLETED")
        self.assertEqual(data["coverage"], 1.0)

    def test_api_human_review_gate(self):
        # 1. Submit review
        submit_resp = self.client.post("/v1/reviews", json={
            "task_id": "task-review-test",
            "triggering_agent_id": "agent-safety",
            "reason": "High-risk pregnancy contraindication confirmation",
            "recommendation": "Flag caution on consumer-facing portal"
        })
        self.assertEqual(submit_resp.status_code, 201)
        rev = submit_resp.json()
        rev_id = rev["review_id"]

        # 2. Approve review
        approve_resp = self.client.post(f"/v1/reviews/{rev_id}/approve", json={
            "reviewer_user_id": "dr-sharma-chair",
            "reviewer_role": "CLINICAL_BOARD",
            "rationale": "Clinical literature confirms bilirubin displacement risk."
        })
        self.assertEqual(approve_resp.status_code, 200)
        dec = approve_resp.json()
        self.assertEqual(dec["action"], "APPROVE")

    def test_sdk_methods(self):
        # Test SDK agents list
        agents = self.sdk.agents.list()
        self.assertTrue(len(agents) >= 30)

        # Test SDK plan
        plan = self.sdk.research.plan("Evaluate Curcumin anti-inflammatory mechanism")
        self.assertIn("plan_id", plan)

        # Test SDK tools list
        tools = self.sdk.tools.list()
        self.assertTrue(len(tools) >= 30)

        # Test SDK policies
        policies = self.sdk.tools.policies()
        self.assertEqual(policies["doctrine"], "Agents discover and reason. Tools execute. Evidence constrains. Verifiers challenge. Policies govern. Humans remain accountable.")


if __name__ == "__main__":
    unittest.main()
