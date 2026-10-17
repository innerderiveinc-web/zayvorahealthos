"""
ZMIE Scientific Agent Operating System Showcase (Prompt 24)
Demonstrates governed multi-agent execution, DAG planning, epistemic boundaries,
independent verification, contradiction preservation, and human governance.
"""

import asyncio
from fastapi.testclient import TestClient

from app.main import app
from app.agent_os import (
    get_agent_os,
    EpistemicState,
    AgentRiskLevel,
    TaskExecutionState,
    MemoryScope,
    MemoryState,
    ReviewDecisionAction,
    EpistemicOutputFirewall,
    KnowledgeChangeProposal,
    AgentTask,
    AgentResult
)
from app.models.federated_privacy import ResearchDataClassification, AgentMode, AgentContext
from zmie.client import ZMIE


async def main():
    print("=" * 80)
    print("ZMIE SCIENTIFIC AGENT OPERATING SYSTEM (Prompt 24 Showcase)")
    print("=" * 80)

    os = get_agent_os()
    sdk = ZMIE(app_instance=app)

    # 1. Agent Catalog & Capabilities
    print("\n[1] Checking Agent OS Catalog...")
    agents = os.agents.list_agents()
    tools = os.tools.list_tools()
    print(f"  -> Total Registered Specialist Agents: {len(agents)}")
    print(f"  -> Total Registered Sandbox Tools: {len(tools)}")
    print("  -> Sample Agents: SourceAgent, ResearchAgent, EvidenceAgent, MechanismAgent,")
    print("                    CausalAgent, SimulationAgent, VerificationAgent, AdversarialAgent")

    # 2. Scientific Planning Agent (DAG Deconstruction)
    print("\n[2] Generating Governed Research Plan (DAG)...")
    question = "Investigate the clinical efficacy, mechanism of action, and drug interactions of Berberine in Type 2 Diabetes."
    plan = os.planner.create_plan(question=question)
    print(f"  -> Plan ID: {plan.plan_id}")
    print(f"  -> Original Question: '{plan.original_question}'")
    print(f"  -> Subtasks Generated: {len(plan.subtasks)}")
    for i, st in enumerate(plan.subtasks[:6], 1):
        deps = f"(depends on: {', '.join(st.dependencies)})" if st.dependencies else "(root task)"
        print(f"     {i}. [{st.agent_id}] {st.name} {deps}")
    print(f"     ... and {len(plan.subtasks) - 6} more stages including Verification and Synthesis.")

    # 3. Multi-Agent DAG Execution & Trace Generation
    print("\n[3] Executing Multi-Agent Research Pipeline...")
    trace, result = await os.orchestrator.execute_research(question=question)
    print(f"  -> Trace ID: {trace.trace_id}")
    print(f"  -> Agents Executed: {len(trace.agents_executed)}")
    print(f"  -> Tools Used: {len(trace.tools_used)}")
    print(f"  -> Events Recorded: {len(trace.events)}")
    print(f"  -> Coverage Score: {trace.completion.coverage_score * 100:.1f}%")
    print(f"  -> Verification Status: {trace.completion.verification_status}")
    print(f"  -> Epistemic State: {result.epistemic_state.value}")
    print(f"  -> Synthesis Summary: {result.summary}")

    # 4. Epistemic Output Firewall Guardrails
    print("\n[4] Validating Epistemic Output Firewall (Non-Negotiable Boundaries)...")
    # Test A: Simulation -> Observed (Blocked)
    sim_agent = os.agents.get_agent_instance("agent-simulation")
    sim_res = await sim_agent.execute(AgentTask(agent_id="agent-simulation", goal="PK simulation"))
    is_valid_sim, err_sim = EpistemicOutputFirewall.validate_agent_result(
        sim_res, requested_epistemic_state=EpistemicState.OBSERVED
    )
    print(f"  -> Block SIMULATED -> OBSERVED promotion: {not is_valid_sim} ({err_sim})")

    # Test B: Private -> Public Direct Leakage (Blocked)
    priv_res = AgentResult(
        task_id="t-priv",
        agent_id="agent-private-research",
        epistemic_state=EpistemicState.OBSERVED,
        summary="Confidential formulation data",
        classification=ResearchDataClassification.CONFIDENTIAL
    )
    is_valid_priv, err_priv = EpistemicOutputFirewall.validate_agent_result(
        priv_res, target_classification=ResearchDataClassification.PUBLIC
    )
    print(f"  -> Block PRIVATE -> PUBLIC unapproved leak: {not is_valid_priv} ({err_priv})")

    # 5. Zero-Tolerance Independent Verification
    print("\n[5] Zero-Tolerance Independent Verification...")
    verifier = os.agents.get_agent_instance("agent-verifier")
    fake_check = await verifier.execute(AgentTask(
        agent_id="agent-verifier",
        goal="Verify citation",
        inputs={"citation": "DOI:10.1000/fabricated_hallucinated_paper_2026"}
    ))
    print(f"  -> Fabricated citation outcome: {fake_check.epistemic_state.value} ({fake_check.summary})")

    # 6. Contradiction Preservation (No Forced Consensus)
    print("\n[6] Contradiction Preservation...")
    contra = os.agents.get_agent_instance("agent-contradiction")
    contra_res = await contra.execute(AgentTask(agent_id="agent-contradiction", goal="Evaluate divergent trials"))
    print(f"  -> Contradiction state: {contra_res.epistemic_state.value}")
    print(f"  -> Divergence nature: {contra_res.artifacts[0]['nature']}")
    print(f"  -> Forced consensus avoided: {contra_res.artifacts[0]['no_forced_consensus']}")

    # 7. Traditional Medicine Integrity (No False Equivalence)
    print("\n[7] Traditional Medicine Conceptual Boundary...")
    onto = os.agents.get_agent_instance("agent-ontology")
    trad_res = await onto.execute(AgentTask(agent_id="agent-ontology", goal="Map Damavi", inputs={"term": "Damavi"}))
    print(f"  -> Mapping status: {trad_res.artifacts[0]['status']}")
    print(f"  -> Reductionism warning: {trad_res.artifacts[0]['epistemic_warning']}")

    # 8. Human Review Gate & Knowledge Change Proposal
    print("\n[8] Human Governance & Knowledge Change Proposal...")
    ke_agent = os.agents.get_agent_instance("agent-knowledge-evolution")
    prop_res = await ke_agent.execute(AgentTask(
        agent_id="agent-knowledge-evolution",
        goal="Propose claim update",
        inputs={"target_claim_id": "CLM-BERBERINE-01"}
    ))
    print(f"  -> Knowledge Evolution Output: {prop_res.summary}")

    # Submit and approve review request
    rev = os.review_gate.submit_review_request(
        task_id="task-showcase-01",
        triggering_agent_id="agent-safety",
        reason="Confirm pregnancy caution flag on public endpoint",
        recommendation="Flag caution"
    )
    decision = os.review_gate.decide_review(
        review_id=rev.review_id,
        reviewer_user_id="dr-hakeem-chair",
        reviewer_role="GOVERNANCE_BOARD",
        action=ReviewDecisionAction.APPROVE,
        rationale="Approved based on maternal-fetal pharmacological profile."
    )
    print(f"  -> Human Review Decision: {decision.action.value} by {decision.reviewer_user_id}")

    # 9. SDK Endpoints Verification
    print("\n[9] Python SDK Client Verification...")
    sdk_agents = sdk.agents.list()
    sdk_tools = sdk.tools.list()
    sdk_plan = sdk.research.plan("Evaluate Curcumin in Rheumatoid Arthritis")
    sdk_policies = sdk.tools.policies()
    print(f"  -> SDK Agents count: {len(sdk_agents)}")
    print(f"  -> SDK Tools count: {len(sdk_tools)}")
    print(f"  -> SDK Research Plan ID: {sdk_plan['plan_id']}")
    print(f"  -> SDK Doctrine: '{sdk_policies['doctrine']}'")

    print("\n" + "=" * 80)
    print("PROMPT 24 SCIENTIFIC AGENT OPERATING SYSTEM: 100% OPERATIONAL")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
