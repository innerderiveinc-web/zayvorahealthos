import React from "react";
import { Compass, CheckCircle2, ChevronRight, FileText, Database } from "lucide-react";
import { ResearchPlanData } from "../lib/types";

export const ResearchWorkspace: React.FC<{ plan: ResearchPlanData; status: string }> = ({ plan, status }) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Compass className="h-4 w-4 text-teal-400" />
            <span className="text-xs font-mono uppercase tracking-wider text-teal-400">Research Workbench</span>
          </div>
          <h2 className="text-lg font-bold text-white">{plan.title}</h2>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">Execution Status:</span>
          <span className="px-2.5 py-1 rounded bg-teal-950/80 text-teal-300 border border-teal-800/80 text-xs font-mono font-semibold">
            {status}
          </span>
        </div>
      </div>

      {/* PICO Framework */}
      <div>
        <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2">PICO Deconstruction</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <span className="text-teal-400 font-bold block mb-1">P — Population</span>
            <span className="text-slate-300">{plan.pico.population}</span>
          </div>
          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <span className="text-teal-400 font-bold block mb-1">I — Intervention</span>
            <span className="text-slate-300">{plan.pico.intervention}</span>
          </div>
          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <span className="text-teal-400 font-bold block mb-1">C — Comparator</span>
            <span className="text-slate-300">{plan.pico.comparator || "Standard Care / Placebo"}</span>
          </div>
          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <span className="text-teal-400 font-bold block mb-1">O — Outcomes</span>
            <span className="text-slate-300">{plan.pico.outcomes.join(", ")}</span>
          </div>
        </div>
      </div>

      {/* Decomposed Sub-Questions */}
      <div>
        <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2">Decomposed Sub-Questions</h3>
        <div className="space-y-2">
          {plan.subQuestions.map((q, i) => (
            <div key={i} className="flex items-start gap-2.5 bg-slate-950/70 p-3 rounded-lg border border-slate-800 text-xs text-slate-200">
              <span className="text-teal-400 font-mono font-bold">0{i + 1}.</span>
              <span>{q}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Inclusion / Exclusion Criteria */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
          <span className="text-xs font-mono uppercase text-emerald-400 block mb-2 font-bold">Inclusion Criteria</span>
          <ul className="space-y-1.5 text-xs text-slate-300">
            {plan.criteria.inclusion.map((inc, i) => (
              <li key={i} className="flex items-start gap-2">
                <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500 mt-0.5 shrink-0" />
                <span>{inc}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
          <span className="text-xs font-mono uppercase text-rose-400 block mb-2 font-bold">Exclusion Criteria</span>
          <ul className="space-y-1.5 text-xs text-slate-300">
            {plan.criteria.exclusion.map((exc, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-rose-500 font-bold text-xs shrink-0">✕</span>
                <span>{exc}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
