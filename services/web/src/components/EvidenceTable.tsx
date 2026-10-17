import React from "react";
import { EvidenceTableItem } from "../lib/types";

export const EvidenceTable: React.FC<{ items: EvidenceTableItem[] }> = ({ items }) => {
  return (
    <div className="overflow-x-auto border border-slate-800 rounded-xl bg-slate-900/60 shadow-lg">
      <table className="w-full text-left text-xs border-collapse">
        <thead>
          <tr className="border-b border-slate-800 bg-slate-950/80 text-[11px] font-mono uppercase tracking-wider text-slate-400">
            <th className="py-3 px-4">Study</th>
            <th className="py-3 px-3">Design</th>
            <th className="py-3 px-3">Population</th>
            <th className="py-3 px-2 text-center">N</th>
            <th className="py-3 px-3">Intervention</th>
            <th className="py-3 px-4">Key Findings</th>
            <th className="py-3 px-3">Grade</th>
            <th className="py-3 px-3">Safety / Adverse</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800/60 text-slate-300">
          {items.map((row) => (
            <tr key={row.evidenceId} className="hover:bg-slate-800/30 transition">
              <td className="py-3 px-4 font-medium text-slate-100 max-w-[200px]">
                <div className="truncate">{row.studyTitle}</div>
                <span className="text-[10px] text-teal-400 font-mono block mt-0.5">{row.source} ({row.year})</span>
              </td>
              <td className="py-3 px-3 text-slate-400 font-mono text-[11px]">{row.studyDesign}</td>
              <td className="py-3 px-3 max-w-[150px] truncate">{row.population}</td>
              <td className="py-3 px-2 text-center font-mono text-slate-400">{row.sampleSize}</td>
              <td className="py-3 px-3 max-w-[140px] truncate text-slate-200">{row.intervention}</td>
              <td className="py-3 px-4 max-w-[260px] leading-relaxed text-slate-200">{row.findings}</td>
              <td className="py-3 px-3">
                <span className="px-2 py-0.5 rounded bg-teal-950/80 text-teal-300 border border-teal-800/70 text-[10px] font-mono">
                  {row.evidenceGrade}
                </span>
              </td>
              <td className="py-3 px-3 text-slate-400 text-[11px] max-w-[140px] truncate">{row.safety}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
