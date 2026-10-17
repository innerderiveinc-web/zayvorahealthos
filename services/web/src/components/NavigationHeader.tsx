import React from "react";
import Link from "next/link";
import { 
  Search, 
  Compass, 
  BookOpen, 
  Network, 
  FileText, 
  Database, 
  ShieldCheck, 
  Bot, 
  History, 
  Cpu, 
  RefreshCw,
  BarChart3,
  Rocket,
  Lock
} from "lucide-react";

export const NavigationHeader: React.FC<{ activeTab?: string }> = ({ activeTab = "search" }) => {
  const tabs = [
    { id: "search", label: "SEARCH", href: "/", icon: Search },
    { id: "medicine", label: "MEDICINE", href: "/medicine", icon: BookOpen },
    { id: "research", label: "RESEARCH", href: "/research", icon: Compass },
    { id: "evidence", label: "EVIDENCE", href: "/evidence", icon: ShieldCheck },
    { id: "compare", label: "COMPARE", href: "/compare", icon: FileText },
    { id: "graph", label: "GRAPH", href: "/graph", icon: Network },
    { id: "agent-os", label: "AGENT OS", href: "/agent-os", icon: Bot },
    { id: "audit", label: "AUDIT", href: "/audit", icon: History },
    { id: "credibility", label: "CREDIBILITY", href: "/credibility", icon: ShieldCheck },
    { id: "trust-firewall", label: "TRUST FIREWALL", href: "/trust-firewall", icon: ShieldCheck },
    { id: "revalidation", label: "REVALIDATION", href: "/revalidation", icon: RefreshCw },
    { id: "security", label: "SECURITY", href: "/security", icon: Lock },
    { id: "benchmarking", label: "BENCHMARKING", href: "/benchmarking", icon: BarChart3 },
    { id: "readiness", label: "READINESS", href: "/readiness", icon: ShieldCheck },
    { id: "launch", label: "LAUNCH", href: "/launch", icon: Rocket },
    { id: "lifecycle", label: "LIFECYCLE", href: "/lifecycle", icon: RefreshCw },
    { id: "compute", label: "COMPUTE", href: "/compute", icon: Cpu },
    { id: "sources", label: "SOURCES", href: "/sources", icon: Database },
  ];

  return (
    <header className="border-b border-slate-800 bg-slate-950/90 backdrop-blur sticky top-0 z-50 px-6 py-3 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <Link href="/" className="flex items-center space-x-3 group">
          <div className="h-8 w-8 rounded-lg bg-teal-500 flex items-center justify-center font-bold text-slate-950 group-hover:bg-teal-400 transition">
            Z
          </div>
          <div>
            <span className="font-bold text-base tracking-wide text-white block">ZMIE</span>
            <span className="text-[10px] text-teal-400 font-mono tracking-wider -mt-1 block uppercase">Medical Intelligence</span>
          </div>
        </Link>
      </div>

      <nav className="flex space-x-1 overflow-x-auto max-w-4xl py-1">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          const Icon = tab.icon;
          return (
            <Link
              key={tab.id}
              href={tab.href}
              className={`px-2.5 py-1.5 rounded-md text-[11px] font-semibold tracking-wider flex items-center gap-1.5 whitespace-nowrap transition ${
                isActive
                  ? "bg-teal-500/10 text-teal-400 border border-teal-500/30"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
              }`}
            >
              <Icon className="h-3.5 w-3.5" />
              {tab.label}
            </Link>
          );
        })}
      </nav>

      <div className="flex items-center space-x-3 flex-shrink-0">
        <span className="text-[11px] font-mono text-slate-400 border border-slate-800 bg-slate-900 px-2 py-1 rounded">
          KNOWLEDGE: 2026.10
        </span>
      </div>
    </header>
  );
};
