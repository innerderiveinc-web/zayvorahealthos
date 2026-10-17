"use client";

import React, { useState } from "react";
import { 
  GitBranch, 
  Activity, 
  AlertTriangle, 
  CheckCircle2, 
  Clock, 
  RefreshCw, 
  ArrowRight, 
  FileText, 
  Layers, 
  ShieldAlert,
  Zap,
  TrendingDown,
  UserCheck
} from "lucide-react";
import { NavigationHeader } from "../../components/NavigationHeader";

export default function RevalidationPage() {
  const [activeTab, setActiveTab] = useState<"GRAPH" | "RADAR" | "DELTAS">("GRAPH");
  const [retractingStudy, setRetractingStudy] = useState("study-101");
  const [retractionReason, setRetractionReason] = useState("Fabricated multicenter observational dataset discovered by institutional audit");
  const [isProcessing, setIsProcessing] = useState(false);
  const [deltaOutput, setDeltaOutput] = useState<any | null>(null);

  const initialNodes = [
    { id: "study-101", type: "PRIMARY_STUDY", label: "Multicenter RCT of Hydroxychloroquine (s-101)", status: "ACTIVE", effect: "-0.42" },
    { id: "study-102", type: "PRIMARY_STUDY", label: "Randomized Antiviral Trial (s-102)", status: "ACTIVE", effect: "+0.05" },
    { id: "meta-covid-01", type: "META_ANALYSIS", label: "Living Systematic Review Meta-Analysis", status: "ACTIVE", effect: "-0.1145" },
    { id: "grade-covid-01", type: "GRADE_PROFILE", label: "Certainty of Evidence: MODERATE", status: "ACTIVE", grade: "MODERATE" },
    { id: "rec-who-covid-14", type: "CLINICAL_RECOMMENDATION", label: "WHO Inpatient Therapeutics Section 14", status: "ACTIVE", action: "Weak recommendation" },
    { id: "snap-2026-covid-v1", type: "RESEARCH_SNAPSHOT", label: "Frozen Research Consensus Snapshot v1.0", status: "FROZEN", version: "1.0.0" },
  ];

  const [nodes, setNodes] = useState(initialNodes);

  const handleTriggerRetraction = () => {
    setIsProcessing(true);
    setTimeout(() => {
      // Simulate cascade invalidation
      setNodes((prev) =>
        prev.map((n) => {
          if (n.id === retractingStudy) return { ...n, status: "RETRACTED" };
          if (n.id === "meta-covid-01") return { ...n, status: "RECALCULATED", effect: "+0.05" };
          if (n.id === "grade-covid-01") return { ...n, status: "DOWNGRADED", grade: "VERY_LOW" };
          if (n.id === "rec-who-covid-14") return { ...n, status: "SUSPENDED" };
          if (n.id === "snap-2026-covid-v1") return { ...n, status: "DEPRECATED" };
          return n;
        })
      );

      setDeltaOutput({
        delta_id: "delta-8f92b410",
        study_id: retractingStudy,
        reason: retractionReason,
        affected_nodes_count: 4,
        previous_effect: -0.1145,
        new_effect: 0.05,
        previous_grade: "MODERATE",
        new_grade: "VERY_LOW",
        shift_magnitude: 0.1645,
        affected_guidelines: ["rec-who-covid-14"],
        affected_snapshots: ["snap-2026-covid-v1"],
        requires_human_review: true,
        status: "PENDING_CLINICAL_BOARD_REVIEW"
      });

      setIsProcessing(false);
    }, 500);
  };

  const handleResetGraph = () => {
    setNodes(initialNodes);
    setDeltaOutput(null);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <NavigationHeader />

      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-8">
        {/* Banner */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              <div className="p-2 bg-indigo-500/10 border border-indigo-500/30 rounded-lg text-indigo-400">
                <RefreshCw className="w-7 h-7" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white tracking-tight">Continuous Evidence & Knowledge Revalidation</h1>
                <p className="text-sm text-slate-400">Prompt 31 Implementation — Dynamic claim dependency graph, retraction surveillance & cascade invalidation</p>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="px-3 py-1 bg-indigo-950/80 text-indigo-400 border border-indigo-800/80 rounded-full text-xs font-semibold uppercase tracking-wider flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></span>
              SURVEILLANCE RADAR LIVE
            </span>
          </div>
        </div>

        {/* Tab Selection */}
        <div className="flex border-b border-slate-800 mb-8 space-x-6 text-sm font-medium">
          <button
            onClick={() => setActiveTab("GRAPH")}
            className={`pb-3 transition-colors border-b-2 ${activeTab === "GRAPH" ? "border-indigo-400 text-indigo-400" : "border-transparent text-slate-400 hover:text-slate-200"}`}
          >
            Dynamic Evidence Dependency Graph
          </button>
          <button
            onClick={() => setActiveTab("RADAR")}
            className={`pb-3 transition-colors border-b-2 ${activeTab === "RADAR" ? "border-indigo-400 text-indigo-400" : "border-transparent text-slate-400 hover:text-slate-200"}`}
          >
            Surveillance Ingestion & Revalidation Trigger
          </button>
          <button
            onClick={() => setActiveTab("DELTAS")}
            className={`pb-3 transition-colors border-b-2 ${activeTab === "DELTAS" ? "border-indigo-400 text-indigo-400" : "border-transparent text-slate-400 hover:text-slate-200"}`}
          >
            Living Evidence Delta Log
          </button>
        </div>

        {/* Tab 1: Graph */}
        {activeTab === "GRAPH" && (
          <div className="space-y-6">
            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-lg font-semibold text-slate-100">Living Evidence Dependency Chain</h2>
                  <p className="text-sm text-slate-400">Notice how a primary study flows through meta-analysis, GRADE profile, clinical guidelines, and research snapshots.</p>
                </div>
                {deltaOutput && (
                  <button
                    onClick={handleResetGraph}
                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-medium transition"
                  >
                    Reset Simulation
                  </button>
                )}
              </div>

              {/* Graphical Nodes Flow */}
              <div className="grid grid-cols-1 md:grid-cols-5 gap-4 my-6">
                {/* Primary Studies */}
                <div className="space-y-3">
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">1. Primary Studies</div>
                  {nodes.filter(n => n.type === "PRIMARY_STUDY").map(n => (
                    <div key={n.id} className={`p-3.5 rounded-lg border text-xs transition-all ${
                      n.status === "RETRACTED" ? "bg-rose-950/40 border-rose-800 text-rose-300" : "bg-slate-950 border-slate-800 text-slate-200"
                    }`}>
                      <div className="font-semibold mb-1">{n.label}</div>
                      <div className="flex justify-between text-[11px] text-slate-400">
                        <span>Status: <strong className={n.status === "RETRACTED" ? "text-rose-400" : "text-emerald-400"}>{n.status}</strong></span>
                        <span>Effect: {n.effect}</span>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Meta-Analysis */}
                <div className="space-y-3">
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">2. Meta-Analysis</div>
                  {nodes.filter(n => n.type === "META_ANALYSIS").map(n => (
                    <div key={n.id} className={`p-3.5 rounded-lg border text-xs transition-all ${
                      n.status === "RECALCULATED" ? "bg-amber-950/40 border-amber-800 text-amber-300" : "bg-slate-950 border-slate-800 text-slate-200"
                    }`}>
                      <div className="font-semibold mb-1">{n.label}</div>
                      <div className="text-[11px] text-slate-400 mt-2">
                        Pooled Effect: <strong className="text-slate-100 font-mono">{n.effect}</strong>
                      </div>
                      <div className="text-[10px] text-slate-400 mt-1">Status: {n.status}</div>
                    </div>
                  ))}
                </div>

                {/* GRADE Profile */}
                <div className="space-y-3">
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">3. GRADE Profile</div>
                  {nodes.filter(n => n.type === "GRADE_PROFILE").map(n => (
                    <div key={n.id} className={`p-3.5 rounded-lg border text-xs transition-all ${
                      n.grade === "VERY_LOW" ? "bg-rose-950/40 border-rose-800 text-rose-300" : "bg-slate-950 border-slate-800 text-slate-200"
                    }`}>
                      <div className="font-semibold mb-1">Certainty Profile</div>
                      <div className="mt-2">
                        Certainty: <span className={`px-2 py-0.5 rounded font-bold text-[10px] ${
                          n.grade === "VERY_LOW" ? "bg-rose-900 text-rose-200" : "bg-teal-900 text-teal-200"
                        }`}>{n.grade}</span>
                      </div>
                      <div className="text-[10px] text-slate-400 mt-1.5">Status: {n.status}</div>
                    </div>
                  ))}
                </div>

                {/* Clinical Guideline */}
                <div className="space-y-3">
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">4. Clinical Guideline</div>
                  {nodes.filter(n => n.type === "CLINICAL_RECOMMENDATION").map(n => (
                    <div key={n.id} className={`p-3.5 rounded-lg border text-xs transition-all ${
                      n.status === "SUSPENDED" ? "bg-rose-950/40 border-rose-800 text-rose-300 animate-pulse" : "bg-slate-950 border-slate-800 text-slate-200"
                    }`}>
                      <div className="font-semibold mb-1">{n.label}</div>
                      <div className="text-[10px] text-slate-400 mt-2">
                        Status: <strong className={n.status === "SUSPENDED" ? "text-rose-400" : "text-emerald-400"}>{n.status}</strong>
                      </div>
                      {n.status === "SUSPENDED" && (
                        <div className="text-[10px] text-rose-300 mt-1 font-semibold flex items-center gap-1">
                          <AlertTriangle className="w-3 h-3" /> Safety Review Locked
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                {/* Research Snapshot */}
                <div className="space-y-3">
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">5. Research Snapshot</div>
                  {nodes.filter(n => n.type === "RESEARCH_SNAPSHOT").map(n => (
                    <div key={n.id} className={`p-3.5 rounded-lg border text-xs transition-all ${
                      n.status === "DEPRECATED" ? "bg-slate-900/60 border-slate-800 text-slate-400 line-through" : "bg-slate-950 border-slate-800 text-slate-200"
                    }`}>
                      <div className="font-semibold mb-1">{n.label}</div>
                      <div className="text-[10px] mt-2">Status: {n.status}</div>
                      <div className="text-[10px] text-slate-400 mt-0.5">Version: {n.version}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Delta Details Card if calculated */}
            {deltaOutput && (
              <div className="bg-indigo-950/30 border border-indigo-800/80 rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2 text-indigo-300 font-semibold">
                    <Zap className="w-5 h-5 text-indigo-400" />
                    <span>Living Evidence Delta Computed: {deltaOutput.delta_id}</span>
                  </div>
                  <span className="px-3 py-1 bg-amber-950 border border-amber-800 text-amber-300 text-xs font-bold rounded-full">
                    {deltaOutput.status}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm mt-4">
                  <div className="p-3.5 bg-slate-950 rounded-lg border border-slate-800">
                    <span className="text-xs text-slate-400 block mb-1">Effect Size Shift</span>
                    <div className="font-mono text-base font-bold text-slate-200">
                      {deltaOutput.previous_effect} ➔ <span className="text-amber-400">{deltaOutput.new_effect}</span>
                    </div>
                  </div>
                  <div className="p-3.5 bg-slate-950 rounded-lg border border-slate-800">
                    <span className="text-xs text-slate-400 block mb-1">GRADE Certainty Downgrade</span>
                    <div className="font-mono text-base font-bold text-rose-400">
                      {deltaOutput.previous_grade} ➔ {deltaOutput.new_grade}
                    </div>
                  </div>
                  <div className="p-3.5 bg-slate-950 rounded-lg border border-slate-800">
                    <span className="text-xs text-slate-400 block mb-1">Affected Guidelines</span>
                    <div className="font-mono text-sm font-semibold text-rose-300">
                      {deltaOutput.affected_guidelines.join(", ")}
                    </div>
                  </div>
                  <div className="p-3.5 bg-slate-950 rounded-lg border border-slate-800">
                    <span className="text-xs text-slate-400 block mb-1">Human Review Gate</span>
                    <div className="font-semibold text-emerald-400 flex items-center gap-1.5">
                      <UserCheck className="w-4 h-4" /> Required (Locked)
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab 2: Radar */}
        {activeTab === "RADAR" && (
          <div className="space-y-6">
            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold text-slate-100 mb-2">Simulate Surveillance Event Ingestion</h2>
              <p className="text-sm text-slate-400 mb-4">Ingest a study retraction or challenge event to trigger downstream ripple revalidation.</p>

              <div className="space-y-4 max-w-2xl">
                <div>
                  <label className="text-xs font-medium text-slate-300 mb-1 block">Target Primary Study</label>
                  <select
                    value={retractingStudy}
                    onChange={(e) => setRetractingStudy(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                  >
                    <option value="study-101">study-101: Multicenter RCT Hydroxychloroquine (s-101)</option>
                    <option value="study-102">study-102: Randomized Antiviral Trial (s-102)</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs font-medium text-slate-300 mb-1 block">Retraction / Surveillance Reason</label>
                  <input
                    type="text"
                    value={retractionReason}
                    onChange={(e) => setRetractionReason(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                  />
                </div>

                <button
                  onClick={() => {
                    handleTriggerRetraction();
                    setActiveTab("GRAPH");
                  }}
                  disabled={isProcessing}
                  className="px-5 py-2.5 bg-rose-600 hover:bg-rose-500 text-white rounded-lg font-medium text-sm flex items-center gap-2 transition-all disabled:opacity-50"
                >
                  {isProcessing ? <RefreshCw className="w-4 h-4 animate-spin" /> : <ShieldAlert className="w-4 h-4" />}
                  Ingest Retraction & Execute Cascade Invalidation
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: Deltas */}
        {activeTab === "DELTAS" && (
          <div className="space-y-6">
            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold text-slate-100 mb-2">Living Evidence Delta Reports</h2>
              <p className="text-sm text-slate-400 mb-6">Historical register of computed delta adjustments from living revalidation surveillance.</p>

              {deltaOutput ? (
                <div className="p-4 bg-slate-950 rounded-lg border border-slate-800 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-mono text-xs font-bold text-indigo-400">{deltaOutput.delta_id}</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-950 text-amber-300 border border-amber-800">
                      {deltaOutput.status}
                    </span>
                  </div>
                  <p className="text-sm text-slate-200">Trigger: {deltaOutput.reason}</p>
                  <p className="text-xs text-slate-400">Target Study: {deltaOutput.study_id} | Epistemic Shift Magnitude: {deltaOutput.shift_magnitude}</p>
                </div>
              ) : (
                <div className="p-8 text-center text-slate-500 text-sm">
                  No active delta reports yet. Trigger a surveillance event in the &quot;Surveillance Ingestion&quot; tab.
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
