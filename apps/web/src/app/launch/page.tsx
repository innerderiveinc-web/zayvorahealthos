"use client";

import React, { useState, useEffect } from "react";
import { 
  Rocket, 
  CheckCircle2, 
  AlertTriangle, 
  ShieldAlert, 
  RotateCcw, 
  ArrowRight, 
  Activity, 
  Radar, 
  Radio, 
  Server, 
  Lock,
  Play,
  FileCheck,
  FileText,
  Shield,
  Layers,
  HelpCircle,
  Eye,
  PlusCircle,
  X,
  ExternalLink
} from "lucide-react";
import { NavigationHeader } from "../../components/NavigationHeader";

export default function ControlledLaunchPage() {
  const [currentRing, setCurrentRing] = useState<number>(0);
  const [isProcessing, setIsProcessing] = useState(false);
  const [circuitBreakerTripped, setCircuitBreakerTripped] = useState(false);
  const [tripwireMessage, setTripwireMessage] = useState("");
  const [activeTab, setActiveTab] = useState<"RINGS" | "FEATURES" | "DAEMONS" | "GOVERNANCE" | "INCIDENTS">("RINGS");

  // Modals
  const [showReportModal, setShowReportModal] = useState(false);
  const [showScopeCertModal, setShowScopeCertModal] = useState(false);
  const [showIncidentModal, setShowIncidentModal] = useState(false);
  const [showTripwireModal, setShowTripwireModal] = useState(false);

  // New incident form state
  const [newIncidentSeverity, setNewIncidentSeverity] = useState<"P0" | "P1" | "P2" | "P3">("P0");
  const [newIncidentTitle, setNewIncidentTitle] = useState("Synthetic Citation Fabrication Injection");
  const [newIncidentScope, setNewIncidentScope] = useState("KNOWLEDGE_FIREWALL");

  const rings = [
    { 
      id: "RING_0_INTERNAL", 
      name: "Ring 0: Internal Science Board", 
      traffic: "100%", 
      tenants: ["tenant-internal-science-board"], 
      p99: "18.4ms",
      sloLatency: "<= 30ms",
      sloErrorRate: "< 0.01%",
      capabilities: "Internal science review, golden battery calibration, diagnostics",
      desc: "Isolated calibration ring with 100% internal staff traffic."
    },
    { 
      id: "RING_1_PILOT_ACADEMIC", 
      name: "Ring 1: Pilot Academic Centers", 
      traffic: "25%", 
      tenants: ["Harvard Med", "Oxford Trials", "Charité Berlin"], 
      p99: "24.1ms",
      sloLatency: "<= 40ms",
      sloErrorRate: "< 0.05%",
      capabilities: "Public Search, PRISMA Systematic Reviews, Deterministic Compute",
      desc: "Selected university research cohorts running non-clinical reviews."
    },
    { 
      id: "RING_2_CLINICAL_NETWORK", 
      name: "Ring 2: Clinical Research Network", 
      traffic: "50%", 
      tenants: ["Mayo Clinic", "Hopkins Research", "AIIMS Delhi"], 
      p99: "31.0ms",
      sloLatency: "<= 45ms",
      sloErrorRate: "< 0.05%",
      capabilities: "Clinical Decision Support (HITL mandatory), Regulatory Intelligence",
      desc: "Licensed clinical research cohorts with strict physician oversight required."
    },
    { 
      id: "RING_3_GLOBAL_PRODUCTION", 
      name: "Ring 3: Global Production", 
      traffic: "100%", 
      tenants: ["Global Enterprise Federation", "Public Search Portal"], 
      p99: "42.5ms",
      sloLatency: "<= 50ms",
      sloErrorRate: "< 0.10%",
      capabilities: "All approved production scopes under Clause 8",
      desc: "Full general availability rollout across all participating enterprise tenants."
    },
  ];

  const [features, setFeatures] = useState([
    {
      name: "PublicMedicalSearch",
      version: "1.0.0",
      scope: "PUBLIC_SEARCH",
      status: "ENABLED",
      owner: "Search Lead",
      risk: "LOW",
      strategy: "Disable via FeatureFlag or route to cached index"
    },
    {
      name: "PRISMADeepResearch",
      version: "1.0.0",
      scope: "PROFESSIONAL_RESEARCH",
      status: "ENABLED",
      owner: "Scientific Integrity Lead",
      risk: "LOW",
      strategy: "Pause background research queues"
    },
    {
      name: "DeterministicScientificCompute",
      version: "1.0.0",
      scope: "SCIENTIFIC_COMPUTE",
      status: "ENABLED",
      owner: "SRE Lead",
      risk: "LOW",
      strategy: "Fallback to Python float library"
    },
    {
      name: "ClinicalDecisionSupport",
      version: "1.0.0",
      scope: "CLINICAL_DECISION_SUPPORT",
      status: "RESTRICTED",
      owner: "Clinical Safety Lead",
      risk: "ACCEPTABLE_WITH_CONTROLS",
      strategy: "Instantly revert to informational disclaimer mode"
    },
    {
      name: "AutonomousDiagnosticPrescription",
      version: "1.0.0",
      scope: "CLINICAL_DECISION_SUPPORT",
      status: "BLOCKED",
      owner: "Chief Medical Officer",
      risk: "CRITICAL",
      strategy: "Strict compile-time & runtime block enforced (INV-01)"
    },
    {
      name: "RegulatoryJurisdictionEngine",
      version: "1.0.0",
      scope: "REGULATORY_INTELLIGENCE",
      status: "ENABLED",
      owner: "Regulatory Affairs Lead",
      risk: "LOW",
      strategy: "Display jurisdiction unknown notice"
    },
    {
      name: "GovernedAgentOS",
      version: "1.0.0",
      scope: "AGENTIC_RESEARCH",
      status: "PILOT_ONLY",
      owner: "AI Operations Lead",
      risk: "ACCEPTABLE_WITH_CONTROLS",
      strategy: "Revoke agent tool execution permissions"
    },
    {
      name: "FederatedInstitutionalIntelligence",
      version: "1.0.0",
      scope: "FEDERATED_INTELLIGENCE",
      status: "PILOT_ONLY",
      owner: "Privacy Lead",
      risk: "ACCEPTABLE_WITH_CONTROLS",
      strategy: "Disconnect external federated sockets"
    },
  ]);

  const daemons = [
    { name: "CanonicalRegistrySyncDaemon", status: "HEALTHY", items: "8,420 / hr", desc: "Crossref, PubMed & DataCite live sync", latency: "12.4ms" },
    { name: "RetractionRadarWatcher", status: "ACTIVE", items: "1,250 / hr", desc: "Automated literature retraction & expression of concern scanner", latency: "18.2ms" },
    { name: "EpistemicDriftDetector", status: "ACTIVE", items: "415 / hr", desc: "Epistemic distance: 0.80 (target >= 0.70)", latency: "22.5ms" },
    { name: "HMACChainIntegrityScanner", status: "ACTIVE", items: "24,000 / hr", desc: "Audit block SHA-256 HMAC verification & anti-tamper checking", latency: "8.1ms" },
    { name: "TenantIsolationGuard", status: "ENFORCED", items: "1,580 / hr", desc: "Cross-tenant RLS barrier verification & canary queries", latency: "14.6ms" },
  ];

  const [incidents, setIncidents] = useState([
    {
      id: "INC-202610-001",
      severity: "P2",
      title: "Crossref Synchronization Latency Fluctuation",
      affectedScope: "SOURCE_REGISTRY",
      status: "RESOLVED",
      action: "P99 latency spiked to 48ms, auto-routed to secondary mirror.",
      detectedAt: "2026-10-04T02:15:00Z"
    },
  ]);

  const handlePromote = async () => {
    if (currentRing < rings.length - 1) {
      setIsProcessing(true);
      try {
        const res = await fetch("http://localhost:8000/v1/controlled-launch/promote", { method: "POST" });
        if (res.ok) {
          const data = await res.json();
          // Match ring string to index
          const ringKey = data.current_ring;
          const idx = rings.findIndex(r => r.id === ringKey);
          setCurrentRing(idx !== -1 ? idx : currentRing + 1);
        } else {
          setCurrentRing(prev => prev + 1);
        }
      } catch {
        setCurrentRing(prev => prev + 1);
      } finally {
        setIsProcessing(false);
        setCircuitBreakerTripped(false);
      }
    }
  };

  const executeCircuitBreakerRollback = async (reason: string, cause: string) => {
    setIsProcessing(true);
    try {
      await fetch("http://localhost:8000/v1/controlled-launch/rollback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reason, cause })
      });
    } catch {
      // fallback
    } finally {
      setCurrentRing(0);
      setCircuitBreakerTripped(true);
      setTripwireMessage(reason);
      setIsProcessing(false);
      setShowTripwireModal(false);
    }
  };

  const handleCreateIncident = async () => {
    const newInc = {
      incident_id: `INC-${Date.now().toString().slice(-4)}`,
      severity: newIncidentSeverity,
      title: newIncidentTitle,
      description: "Incident reported from Launch Operations console.",
      affected_scope: newIncidentScope,
      status: "OPEN",
      action_taken: newIncidentSeverity === "P0" ? "Automatic zero-second circuit breaker rollback executed" : "Dispatched to on-call engineer"
    };

    setIncidents(prev => [
      {
        id: newInc.incident_id,
        severity: newInc.severity,
        title: newInc.title,
        affectedScope: newInc.affected_scope,
        status: newInc.severity === "P0" ? "CONTAINED" : "OPEN",
        action: newInc.action_taken,
        detectedAt: new Date().toISOString()
      },
      ...prev
    ]);

    if (newIncidentSeverity === "P0") {
      executeCircuitBreakerRollback(`CRITICAL P0 INCIDENT: ${newIncidentTitle}`, "INVARIANT_VIOLATION");
    }

    setShowIncidentModal(false);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <NavigationHeader activeTab="launch" />

      <main className="flex-1 max-w-7xl w-full mx-auto p-6 md:p-8 space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
          <div>
            <div className="flex items-center gap-3">
              <div className="h-9 w-9 rounded-lg bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-400">
                <Rocket className="h-5 w-5" />
              </div>
              <h1 className="text-xl font-bold tracking-tight text-white">Controlled Production Launch & Continuous Surveillance</h1>
              <span className="px-2 py-0.5 rounded text-[11px] font-mono bg-teal-500/10 text-teal-400 border border-teal-500/30 font-semibold">
                PRODUCTION ACTIVE
              </span>
            </div>
            <p className="text-sm text-slate-400 mt-1">
              Progressive canary rings (Rings 0–3), automated tripwire circuit breakers, and 24/7 background surveillance daemons.
            </p>
          </div>

          <div className="flex items-center gap-2 flex-wrap">
            <button
              onClick={() => setShowScopeCertModal(true)}
              className="px-3 py-2 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 font-mono text-xs rounded-lg flex items-center gap-1.5 transition"
            >
              <FileCheck className="h-3.5 w-3.5 text-teal-400" />
              Scope Certificate
            </button>
            <button
              onClick={() => setShowReportModal(true)}
              className="px-3 py-2 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 font-mono text-xs rounded-lg flex items-center gap-1.5 transition"
            >
              <FileText className="h-3.5 w-3.5 text-teal-400" />
              Signed Launch Report
            </button>
            <button
              onClick={handlePromote}
              disabled={isProcessing || currentRing >= rings.length - 1}
              className="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-slate-950 font-bold rounded-lg text-xs flex items-center gap-2 transition disabled:opacity-50"
            >
              <Play className="h-3.5 w-3.5 fill-current" />
              {isProcessing ? "Promoting..." : `Promote to Ring ${currentRing + 1}`}
            </button>
            <button
              onClick={() => setShowTripwireModal(true)}
              disabled={isProcessing}
              className="px-3 py-2 bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 border border-rose-500/40 font-semibold rounded-lg text-xs flex items-center gap-1.5 transition"
            >
              <RotateCcw className="h-3.5 w-3.5" />
              Simulate Tripwire
            </button>
          </div>
        </div>

        {/* Circuit Breaker Status Banner */}
        {circuitBreakerTripped && (
          <div className="bg-rose-950/40 border border-rose-500/40 rounded-xl p-4 flex items-center justify-between text-xs text-rose-200 animate-in fade-in duration-200">
            <div className="flex items-center gap-3">
              <ShieldAlert className="h-5 w-5 text-rose-400 flex-shrink-0" />
              <div>
                <span className="font-bold text-rose-300 block">AUTOMATED CIRCUIT BREAKER TRIPPED: Zero-Second Rollback Executed</span>
                <span>{tripwireMessage || "Invariant tripwire activated. System immediately reverted all outer traffic back to Ring 0 (Internal Science Board)."}</span>
              </div>
            </div>
            <button
              onClick={() => setCircuitBreakerTripped(false)}
              className="px-2.5 py-1 rounded font-mono bg-rose-500/20 text-rose-300 font-bold border border-rose-500/30 hover:bg-rose-500/30 transition"
            >
              DISMISS
            </button>
          </div>
        )}

        {/* Tab Controls */}
        <div className="flex border-b border-slate-800 space-x-6">
          <button
            onClick={() => setActiveTab("RINGS")}
            className={`pb-3 text-xs font-semibold tracking-wider transition ${
              activeTab === "RINGS"
                ? "text-teal-400 border-b-2 border-teal-500"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            CANARY RINGS & SLOS
          </button>
          <button
            onClick={() => setActiveTab("FEATURES")}
            className={`pb-3 text-xs font-semibold tracking-wider transition ${
              activeTab === "FEATURES"
                ? "text-teal-400 border-b-2 border-teal-500"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            FEATURE REGISTRY (CLAUSE 10)
          </button>
          <button
            onClick={() => setActiveTab("DAEMONS")}
            className={`pb-3 text-xs font-semibold tracking-wider transition ${
              activeTab === "DAEMONS"
                ? "text-teal-400 border-b-2 border-teal-500"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            SURVEILLANCE DAEMONS (5)
          </button>
          <button
            onClick={() => setActiveTab("INCIDENTS")}
            className={`pb-3 text-xs font-semibold tracking-wider transition flex items-center gap-1.5 ${
              activeTab === "INCIDENTS"
                ? "text-teal-400 border-b-2 border-teal-500"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            INCIDENT CENTER
            <span className="px-1.5 py-0.2 rounded-full text-[10px] bg-slate-800 text-slate-300">
              {incidents.length}
            </span>
          </button>
        </div>

        {/* TAB 1: RINGS & CANARIES */}
        {activeTab === "RINGS" && (
          <div className="space-y-6">
            {/* Progressive Delivery Rings Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {rings.map((r, idx) => {
                const isCurrent = idx === currentRing;
                const isCompleted = idx < currentRing;
                return (
                  <div
                    key={r.id}
                    className={`p-5 rounded-xl border transition flex flex-col justify-between ${
                      isCurrent
                        ? "bg-slate-900 border-teal-500/60 shadow-lg shadow-teal-950/40"
                        : isCompleted
                        ? "bg-slate-900/40 border-slate-800"
                        : "bg-slate-950 border-slate-900 opacity-60"
                    }`}
                  >
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-[11px] font-mono text-slate-400 font-semibold">{r.id}</span>
                        {isCurrent ? (
                          <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-teal-500/10 text-teal-400 border border-teal-500/30 font-bold animate-pulse">
                            ACTIVE RING
                          </span>
                        ) : isCompleted ? (
                          <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                            COMPLETED
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-400">
                            PLANNED
                          </span>
                        )}
                      </div>
                      <h3 className="font-semibold text-white text-sm mb-1">{r.name}</h3>
                      <p className="text-[11px] text-slate-400 mb-3">{r.desc}</p>
                      <div className="space-y-1 text-xs text-slate-400 font-mono">
                        <div className="flex justify-between">
                          <span>Traffic:</span>
                          <span className="text-slate-200">{r.traffic}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Latency p99:</span>
                          <span className="text-teal-400">{r.p99}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>SLO Limit:</span>
                          <span className="text-slate-400">{r.sloLatency}</span>
                        </div>
                      </div>
                    </div>

                    <div className="mt-4 pt-3 border-t border-slate-800/80 text-[11px] text-slate-500 font-mono">
                      <span>Tenants: {r.tenants.length} enrolled</span>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Live Canary Telemetry KPIs */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
                <span className="text-xs font-mono text-slate-400 uppercase block">Active Delivery Ring</span>
                <span className="text-xl font-bold font-mono text-teal-400 mt-1 block">RING {currentRing}</span>
                <span className="text-[11px] text-slate-500 mt-0.5 block">{rings[currentRing].name}</span>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
                <span className="text-xs font-mono text-slate-400 uppercase block">Invariant Violations</span>
                <span className="text-2xl font-bold font-mono text-emerald-400 mt-1 block">0</span>
                <span className="text-[11px] text-slate-500 mt-0.5 block">10/10 invariants intact</span>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
                <span className="text-xs font-mono text-slate-400 uppercase block">Canary Hallucination</span>
                <span className="text-2xl font-bold font-mono text-teal-400 mt-1 block">0.0%</span>
                <span className="text-[11px] text-slate-500 mt-0.5 block">12,500 queries verified</span>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
                <span className="text-xs font-mono text-slate-400 uppercase block">Circuit Breaker</span>
                <span className="text-xl font-bold font-mono text-emerald-400 mt-1 block">ARMED</span>
                <span className="text-[11px] text-slate-500 mt-0.5 block">Zero-second rollback</span>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
                <span className="text-xs font-mono text-slate-400 uppercase block">System Health</span>
                <span className="text-xl font-bold font-mono text-emerald-400 mt-1 block">OPERATIONAL</span>
                <span className="text-[11px] text-slate-500 mt-0.5 block">5 daemons reporting</span>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: FEATURE REGISTRY */}
        {activeTab === "FEATURES" && (
          <div className="bg-slate-900/40 border border-slate-800 rounded-xl overflow-hidden">
            <div className="p-4 bg-slate-900/80 border-b border-slate-800 flex items-center justify-between text-xs">
              <span className="font-semibold text-white">Clause 10 — Production Feature Registry</span>
              <span className="text-slate-400 font-mono">
                {features.filter(f => f.status === "ENABLED").length} ENABLED | 
                {" "}{features.filter(f => f.status === "RESTRICTED" || f.status === "PILOT_ONLY").length} RESTRICTED / PILOT | 
                {" "}{features.filter(f => f.status === "BLOCKED").length} BLOCKED
              </span>
            </div>
            <div className="divide-y divide-slate-800/60">
              {features.map((feat, idx) => (
                <div key={idx} className="p-4 flex flex-col md:flex-row md:items-center justify-between gap-3 hover:bg-slate-900/30 transition text-xs">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-slate-100 font-bold">{feat.name}</span>
                      <span className="text-[10px] font-mono text-slate-500">v{feat.version}</span>
                      <span className="text-[10px] font-mono text-slate-400 bg-slate-800/80 px-1.5 py-0.5 rounded">
                        {feat.scope}
                      </span>
                    </div>
                    <div className="text-[11px] text-slate-400 mt-1 flex flex-wrap gap-x-4">
                      <span>Owner: <strong className="text-slate-300">{feat.owner}</strong></span>
                      <span>Risk: <strong className="text-slate-300">{feat.risk}</strong></span>
                      <span>Rollback: <em className="text-slate-400">{feat.strategy}</em></span>
                    </div>
                  </div>
                  <div>
                    <span className={`px-2.5 py-1 rounded text-xs font-bold font-mono ${
                      feat.status === "ENABLED"
                        ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30"
                        : feat.status === "BLOCKED"
                        ? "bg-rose-500/10 text-rose-400 border border-rose-500/30"
                        : "bg-amber-500/10 text-amber-400 border border-amber-500/30"
                    }`}>
                      {feat.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 3: DAEMONS */}
        {activeTab === "DAEMONS" && (
          <div className="bg-slate-900/40 border border-slate-800 rounded-xl overflow-hidden">
            <div className="p-4 bg-slate-900/80 border-b border-slate-800 flex items-center justify-between text-xs">
              <span className="font-semibold text-white flex items-center gap-2">
                <Radio className="h-4 w-4 text-teal-400 animate-pulse" />
                24/7 Autonomous Surveillance Daemons (Background Workers)
              </span>
              <span className="text-slate-400 font-mono">5 / 5 Daemons Healthy</span>
            </div>
            <div className="divide-y divide-slate-800/60">
              {daemons.map((d, idx) => (
                <div key={idx} className="p-4 flex items-center justify-between hover:bg-slate-900/30 transition text-xs">
                  <div className="flex items-center gap-3">
                    <CheckCircle2 className="h-4 w-4 text-emerald-400 flex-shrink-0" />
                    <div>
                      <span className="font-mono text-slate-200 font-medium block">{d.name}</span>
                      <span className="text-[11px] text-slate-500">{d.desc}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-4 font-mono text-xs">
                    <span className="text-slate-400">Latency: {d.latency}</span>
                    <span className="text-slate-400">{d.items}</span>
                    <span className="px-2.5 py-0.5 rounded text-[11px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                      {d.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 4: INCIDENT MANAGEMENT */}
        {activeTab === "INCIDENTS" && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <p className="text-xs text-slate-400">
                P0 incidents instantly execute zero-second circuit breaker rollback to Ring 0. P1-P3 alerts maintain safe ring routing.
              </p>
              <button
                onClick={() => setShowIncidentModal(true)}
                className="px-3 py-1.5 bg-teal-600 hover:bg-teal-500 text-slate-950 font-bold rounded-lg text-xs flex items-center gap-1.5 transition"
              >
                <PlusCircle className="h-3.5 w-3.5" />
                Report Incident
              </button>
            </div>

            <div className="bg-slate-900/40 border border-slate-800 rounded-xl overflow-hidden divide-y divide-slate-800/60">
              {incidents.map((inc) => (
                <div key={inc.id} className="p-4 flex items-start justify-between gap-4 text-xs">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                        inc.severity === "P0"
                          ? "bg-rose-500/20 text-rose-300 border border-rose-500/30"
                          : inc.severity === "P1"
                          ? "bg-amber-500/20 text-amber-300 border border-amber-500/30"
                          : "bg-slate-800 text-slate-300 border border-slate-700"
                      }`}>
                        {inc.severity}
                      </span>
                      <span className="font-mono text-slate-200 font-bold">{inc.title}</span>
                      <span className="text-[10px] font-mono text-slate-500">[{inc.id}]</span>
                    </div>
                    <p className="text-[11px] text-slate-400 mt-1">Action: {inc.action}</p>
                    <span className="text-[10px] font-mono text-slate-500 block mt-1">Scope: {inc.affectedScope} | Detected: {inc.detectedAt}</span>
                  </div>
                  <div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-300 border border-slate-700">
                      {inc.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* MODAL 1: Launch Report Modal */}
        {showReportModal && (
          <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full p-6 space-y-4 max-h-[85vh] overflow-y-auto">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <FileCheck className="h-5 w-5 text-teal-400" />
                  <h3 className="font-bold text-white text-base">Controlled Production Launch Report</h3>
                </div>
                <button onClick={() => setShowReportModal(false)} className="text-slate-400 hover:text-white">
                  <X className="h-5 w-5" />
                </button>
              </div>

              <div className="space-y-3 text-xs font-mono text-slate-300">
                <div className="bg-slate-950 p-4 rounded-xl space-y-2 border border-slate-800">
                  <div className="flex justify-between">
                    <span className="text-slate-500">REPORT ID:</span>
                    <span className="text-teal-400">launch-rep-202610-prod</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">RELEASE ID:</span>
                    <span className="text-white">REL-ZMIE-2026.10-GA-1</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">FINAL DECISION:</span>
                    <span className="text-emerald-400 font-bold">GO_LIVE_APPROVED</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">CURRENT STAGE:</span>
                    <span className="text-teal-400">{rings[currentRing].id}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">AUTHENTICITY SIGNATURE:</span>
                    <span className="text-slate-400 truncate max-w-xs">9a8f27bd91...38d21c (HMAC-SHA256)</span>
                  </div>
                </div>

                <div className="space-y-1">
                  <span className="text-slate-400 font-bold block">Approved Production Scopes:</span>
                  <p className="text-slate-300 text-[11px]">
                    PublicMedicalSearch, PRISMADeepResearch, DeterministicScientificCompute, RegulatoryJurisdictionEngine
                  </p>
                </div>

                <div className="space-y-1">
                  <span className="text-rose-400 font-bold block">Strictly Blocked Scopes (INV-01):</span>
                  <p className="text-slate-300 text-[11px]">
                    AutonomousDiagnosticPrescription (prohibited compile-time & runtime)
                  </p>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800 flex justify-end">
                <button
                  onClick={() => setShowReportModal(false)}
                  className="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-slate-950 font-bold text-xs rounded-lg transition"
                >
                  Close Report
                </button>
              </div>
            </div>
          </div>
        )}

        {/* MODAL 2: Scope Certificate Modal */}
        {showScopeCertModal && (
          <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full p-6 space-y-4 max-h-[85vh] overflow-y-auto">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <Shield className="h-5 w-5 text-teal-400" />
                  <h3 className="font-bold text-white text-base">Production Scope Certificate (Clause 297)</h3>
                </div>
                <button onClick={() => setShowScopeCertModal(false)} className="text-slate-400 hover:text-white">
                  <X className="h-5 w-5" />
                </button>
              </div>

              <div className="space-y-3 text-xs font-mono text-slate-300">
                <div className="bg-slate-950 p-4 rounded-xl space-y-2 border border-slate-800">
                  <div className="flex justify-between">
                    <span className="text-slate-500">CERTIFICATE ID:</span>
                    <span className="text-teal-400">scope-cert-202610-001</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">AUTHORITY:</span>
                    <span className="text-white">Chief Launch Officer & Release Governance Authority</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">RELEASE ID:</span>
                    <span className="text-white">REL-ZMIE-2026.10-GA-1</span>
                  </div>
                </div>

                <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
                  <span className="text-slate-400 font-bold block uppercase text-[10px]">Certified Limitations & Invariants</span>
                  <ul className="list-disc list-inside text-[11px] text-slate-300 space-y-1">
                    <li>Autonomous Diagnostic Prescription strictly prohibited (INV-01 / Safety Gate)</li>
                    <li>Clinical Decision Support requires human licensed physician review</li>
                    <li>Traditional Medicine mappings maintain epistemic distance and do not imply 1:1 biomedical equivalence</li>
                  </ul>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800 flex justify-end">
                <button
                  onClick={() => setShowScopeCertModal(false)}
                  className="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-slate-950 font-bold text-xs rounded-lg transition"
                >
                  Acknowledge Certificate
                </button>
              </div>
            </div>
          </div>
        )}

        {/* MODAL 3: Tripwire Simulation Modal */}
        {showTripwireModal && (
          <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <ShieldAlert className="h-5 w-5 text-rose-400" />
                  <h3 className="font-bold text-white text-base">Simulate Automated Tripwire</h3>
                </div>
                <button onClick={() => setShowTripwireModal(false)} className="text-slate-400 hover:text-white">
                  <X className="h-5 w-5" />
                </button>
              </div>

              <p className="text-xs text-slate-400">
                Select an automated tripwire condition to verify instant zero-second rollback to Ring 0 (Internal Science Board):
              </p>

              <div className="space-y-2">
                {[
                  { id: "CITATION_FABRICATION_DETECTED", label: "Citation Fabrication Detected", desc: "Generated DOI fails registry lookup" },
                  { id: "CROSS_TENANT_LEAKAGE", label: "Cross-Tenant Leakage Attempt", desc: "Unauthorized inter-tenant data query" },
                  { id: "INVARIANT_VIOLATION", label: "Invariant Safety Violation", desc: "Attempted autonomous prescription trigger" },
                  { id: "SAFETY_FIREWALL_BREACH", label: "CYP450 Safety Firewall Breach", desc: "Bypassed drug-herb contraindication rule" },
                  { id: "SLO_LATENCY_BREACH", label: "SLO Latency Breach (p99 > 100ms)", desc: "Sustained p99 latency degradation" }
                ].map(tw => (
                  <button
                    key={tw.id}
                    onClick={() => executeCircuitBreakerRollback(`Simulated tripwire: ${tw.label}`, tw.id)}
                    className="w-full text-left p-3 rounded-xl bg-slate-950 hover:bg-rose-950/30 border border-slate-800 hover:border-rose-500/40 transition group"
                  >
                    <span className="font-semibold text-xs text-slate-200 group-hover:text-rose-300 block">{tw.label}</span>
                    <span className="text-[11px] text-slate-500 block">{tw.desc}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* MODAL 4: Report Incident Modal */}
        {showIncidentModal && (
          <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-amber-400" />
                  <h3 className="font-bold text-white text-base">Report Production Incident</h3>
                </div>
                <button onClick={() => setShowIncidentModal(false)} className="text-slate-400 hover:text-white">
                  <X className="h-5 w-5" />
                </button>
              </div>

              <div className="space-y-3 text-xs">
                <div>
                  <label className="text-slate-400 block mb-1">Severity Level</label>
                  <select
                    value={newIncidentSeverity}
                    onChange={(e) => setNewIncidentSeverity(e.target.value as any)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-white"
                  >
                    <option value="P0">P0 - Critical (Triggers Immediate Rollback)</option>
                    <option value="P1">P1 - High (Major Degradation)</option>
                    <option value="P2">P2 - Moderate (Minor Anomaly)</option>
                    <option value="P3">P3 - Low (Informational)</option>
                  </select>
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Incident Title</label>
                  <input
                    type="text"
                    value={newIncidentTitle}
                    onChange={(e) => setNewIncidentTitle(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-white"
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Affected Scope</label>
                  <input
                    type="text"
                    value={newIncidentScope}
                    onChange={(e) => setNewIncidentScope(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-white"
                  />
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800 flex justify-end gap-2">
                <button
                  onClick={() => setShowIncidentModal(false)}
                  className="px-3 py-1.5 text-xs text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreateIncident}
                  className="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-slate-950 font-bold text-xs rounded-lg transition"
                >
                  Log & Dispatch
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
