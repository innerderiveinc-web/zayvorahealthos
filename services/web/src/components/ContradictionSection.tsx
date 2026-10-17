import React from "react";
import { AlertCircle, Scale, ArrowRight } from "lucide-react";
import { ContradictionRecord } from "../lib/types";

export const ContradictionSection: React.FC<{ records: ContradictionRecord[] }> = ({ records }) => {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <Scale className="h-5 w-5 text-indigo-400" />
        <h3 className="text-base font-semibold text-white">Where Evidence Differs</h3>
      </div>
      <p className="text-xs text-slate-400">
        ZMIE rejects forced artificial consensus. When clinical trials conflict, divergent perspectives and root causes are surfaced.
      </p>

      <div className="grid grid-cols-1 gap-4 mt-3">
        {records.map((rec, i) => (
          <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-md">
            <div className="flex items-center justify-between mb-3">
              <span className="font-semibold text-sm text-slate-200">{rec.topic}</span>
              <span className="text-[10px] font-mono uppercase bg-indigo-950/80 text-indigo-300 border border-indigo-800/80 px-2 py-0.5 rounded">
                {rec.type}
              </span>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed mb-4 bg-slate-950/60 p-3 rounded-lg border border-slate-800/80">
              {rec.divergence}
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800/80">
                <span className="text-[10px] font-mono text-emerald-400 uppercase tracking-wider block mb-1">Position A</span>
                <p className="text-xs text-slate-300 leading-relaxed font-medium mb-1">"{rec.positionA.claim}"</p>
                {rec.positionA.population && (
                  <span className="text-[11px] text-slate-500 block">Cohort: {rec.positionA.population}</span>
                )}
              </div>
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800/80">
                <span className="text-[10px] font-mono text-amber-400 uppercase tracking-wider block mb-1">Position B</span>
                <p className="text-xs text-slate-300 leading-relaxed font-medium mb-1">"{rec.positionB.claim}"</p>
                {rec.positionB.population && (
                  <span className="text-[11px] text-slate-500 block">Cohort: {rec.positionB.population}</span>
                )}
              </div>
            </div>

            <div className="pt-3 border-t border-slate-800/70 text-xs space-y-1">
              <div>
                <span className="text-slate-500">Probable Root Cause: </span>
                <span className="text-slate-300">{rec.probableCause}</span>
              </div>
              <div>
                <span className="text-slate-500">Proposed Resolution Pathway: </span>
                <span className="text-teal-400">{rec.resolution}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
