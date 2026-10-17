"use client";

import React, { useState } from "react";
import { Bot, Play, CheckCircle2, ShieldAlert, Cpu, Network, ArrowRight, Activity, Clock, ShieldCheck } from "lucide-react";
import { NavigationHeader } from "../../components/NavigationHeader";
import { AgentTaskStep } from "../../lib/types";

export default function AgentOSPage() {
  const [taskQuery, setTaskQuery] = useState("Evaluate Berberine vs Metformin in Type 2 Diabetes with full mechanistic & safety trace");
  const [isRunning, setIsRunning] = useState(false);

  const steps: AgentTaskStep[] = [
    {
      stepId: "step-01",
      agentRole: "SCIENTIFIC_PLANNER",
      action: "Decomposed research query into PICO dimensions & sub-hypotheses",
      status: "COMPLETED",
      latencyMs: 38
    },
    {
      stepId: "step-02",
      agentRole: "DISCOVERY_SPECIALIST",
      action: "Queried PubMed, ClinicalTrials.gov, and AYUSH TKDL registries (42 studies identified)",
      status: "COMPLETED",
      latencyMs: 84
    },
    {
      stepId: "step-03",
      agentRole: "SCREENING_SPECIALIST",
      action: "PRISMA 2020 inclusion filter applied (18 high-quality RCTs & compendial records retained)",
      status: "COMPLETED",
      latencyMs: 52
    },
    {
      stepId: "step-04",
      agentRole: "EVIDENCE_VERIFIER",
      action: "Verified atomic claim grounding against raw PMIDs; zero hallucination invariant certified",
      status: "VERIFIED",
      latencyMs: 44
    },
    {
      stepId: "step-05",
      agentRole: "CONTRADICTION_DETECTOR",
      action: "Detected LDL-C lowering divergence across East Asian vs Caucasian cohorts; attributed to dietary fat & PCSK9",
      status: "COMPLETED",
      latencyMs: 61
    },
    {
      stepId: "step-06",
      agentRole: "SAFETY_FIREWALL_AGENT",
      action: "Deterministic safety evaluation: CYP3A4 inhibition flagged; pregnancy Kernicterus contraindication enforced",
      status: "VERIFIED",
      latencyMs: 29
    },
    {
      stepId: "step-07",
      agentRole: "GOVERNANCE_GATE",
      action: "Validated all 10 Invariants (INV-01 to INV-10); approved for executive synthesis",
      status: "VERIFIED",
      latencyMs: 18
    },
    {
      stepId: "step-08",
      agentRole: "SYNTHESIS_AGENT",
      action: "Generated publication-grade living evidence monograph with full cryptographic provenance",
      status: "COMPLETED",
      latencyMs: 72
    }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <NavigationHeader activeTab="agent-os" />

      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-8 space-y-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 text-teal-400 font-mono text-xs uppercase tracking-wider mb-1">
              <Bot className="h-4 w-4" /> Governed Scientific Agent Operating System (Prompt 24 & 28)
            </div>
            <h1 className="text-2xl font-bold text-white">Multi-Agent Scientific Execution & Governance Engine</h1>
            <p className="text-slate-400 text-xs mt-1">
              Deterministic planner-orchestrator coordinating specialized agents under strict epistemic & safety firewalls.
            </p>
          </div>
          <div className="flex items-center gap-2 font-mono text-xs">
            <span className="px-3 py-1.5 rounded-lg bg-teal-950/60 border border-teal-800 text-teal-300 flex items-center gap-1.5">
              <Activity className="h-3.5 w-3.5 text-teal-400" /> Pipeline: GOVERNED
            </span>
          </div>
        </div>

        {/* Query Input */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
          <label className="text-xs font-mono uppercase text-slate-400 font-bold block">
            Governed Agent Task Submission
          </label>
          <div className="flex gap-3">
            <input
              type="text"
              value={taskQuery}
              onChange={(e) => setTaskQuery(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-700/80 rounded-lg px-4 py-2.5 text-xs text-white focus:outline-none focus:border-teal-500"
            />
            <button
              onClick={() => setIsRunning(!isRunning)}
              className="bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold px-5 py-2.5 rounded-lg text-xs uppercase tracking-wider transition flex items-center gap-1.5"
            >
              <Play className="h-3.5 w-3.5" /> {isRunning ? "Running..." : "Dispatch Pipeline"}
            </button>
          </div>
        </div>

        {/* Execution Flow Trace */}
        <div className="space-y-4">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Cpu className="h-4 w-4 text-teal-400" /> Governed Multi-Agent Execution Trace
          </h2>

          <div className="space-y-3">
            {steps.map((st, i) => (
              <div
                key={st.stepId}
                className="bg-slate-900 border border-slate-800/80 rounded-xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs"
              >
                <div className="flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-slate-950 border border-slate-700 flex items-center justify-center font-mono text-[11px] text-teal-400 shrink-0 mt-0.5">
                    0{i + 1}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-white uppercase text-[11px]">{st.agentRole}</span>
                      <span className={`px-2 py-0.2 rounded text-[10px] font-mono ${
                        st.status === "VERIFIED" 
                          ? "bg-emerald-950 text-emerald-300 border border-emerald-800" 
                          : "bg-blue-950 text-blue-300 border border-blue-800"
                      }`}>
                        {st.status}
                      </span>
                    </div>
                    <p className="text-slate-300 mt-1 leading-relaxed">{st.action}</p>
                  </div>
                </div>

                <div className="flex items-center gap-4 text-slate-400 font-mono text-[11px] shrink-0 self-end md:self-center">
                  <span className="flex items-center gap-1">
                    <Clock className="h-3 w-3" /> {st.latencyMs} ms
                  </span>
                  <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Governance & Veto Rules */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <ShieldCheck className="h-4 w-4 text-teal-400" /> Active Safety & Governance Gates
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
              <span className="text-teal-400 font-bold block mb-1 font-mono uppercase">Zero Fabrication Gate</span>
              <p className="text-slate-400">Claims without grounded passage citations are purged. LLMs cannot invent DOIs or synthetic trial findings.</p>
            </div>
            <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
              <span className="text-amber-400 font-bold block mb-1 font-mono uppercase">Epistemic Equivalence Gate</span>
              <p className="text-slate-400">Traditional concepts (Mizaj, Doshas) cannot be reduced to 1:1 biomedical terms. Preserves conceptual distance.</p>
            </div>
            <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
              <span className="text-rose-400 font-bold block mb-1 font-mono uppercase">Deterministic Safety Gate</span>
              <p className="text-slate-400">Contraindications and CYP450 enzyme interactions calculated deterministically outside model context.</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
