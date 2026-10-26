import React from "react";
import { X, ShieldCheck, FileText, ExternalLink, AlertCircle } from "lucide-react";
import { ClaimTraceData } from "../lib/types";
import { StatusBadge } from "./StatusBadge";

interface ClaimTraceDrawerProps {
  data: ClaimTraceData | null;
  onClose: () => void;
}

export const ClaimTraceDrawer: React.FC<ClaimTraceDrawerProps> = ({ data, onClose }) => {
  if (!data) return null;

  return (
    <div className="fixed inset-y-0 right-0 w-full max-w-md bg-slate-900 border-l border-slate-800 shadow-2xl z-50 flex flex-col animate-slideLeft">
      <div className="p-5 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ShieldCheck className="h-4 w-4 text-teal-400" />
          <h3 className="font-semibold text-sm text-white">Claim Provenance Trace</h3>
        </div>
        <button onClick={onClose} className="text-slate-400 hover:text-white transition">
          <X className="h-4 w-4" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-5 space-y-6 text-sm">
        {/* Claim text */}
        <div>
          <span className="text-[11px] font-mono text-slate-500 uppercase tracking-wider block mb-1">Asserted Claim</span>
          <p className="text-slate-200 font-medium leading-relaxed bg-slate-950 p-3 rounded-lg border border-slate-800">
            "{data.claimText}"
          </p>
        </div>

        {/* Verification Status */}
        <div className="flex items-center justify-between bg-slate-950/60 p-3 rounded-lg border border-slate-800/80">
          <span className="text-xs text-slate-400">Firewall Verification:</span>
          <StatusBadge status={data.verificationStatus} />
        </div>

        {/* Normalized components */}
        <div>
          <span className="text-[11px] font-mono text-slate-500 uppercase tracking-wider block mb-2">Normalized Medical Components</span>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="bg-slate-950 p-2.5 rounded border border-slate-800">
              <span className="text-slate-500 block">Subject:</span>
              <span className="text-slate-300 font-mono">{data.normalizedClaim.subject}</span>
            </div>
            <div className="bg-slate-950 p-2.5 rounded border border-slate-800">
              <span className="text-slate-500 block">Predicate:</span>
              <span className="text-slate-300 font-mono">{data.normalizedClaim.predicate}</span>
            </div>
            <div className="bg-slate-950 p-2.5 rounded border border-slate-800">
              <span className="text-slate-500 block">Outcome / Target:</span>
              <span className="text-slate-300 font-mono">{data.normalizedClaim.object}</span>
            </div>
            <div className="bg-slate-950 p-2.5 rounded border border-slate-800">
              <span className="text-slate-500 block">Evidence Grade:</span>
              <span className="text-teal-400 font-mono">{data.evidenceLevel}</span>
            </div>
          </div>
        </div>

        {/* Cited Anchor Passage */}
        <div>
          <span className="text-[11px] font-mono text-slate-500 uppercase tracking-wider block mb-1">Direct Source Anchor Passage</span>
          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-xs text-slate-300 leading-relaxed font-serif italic">
            "{data.passage}"
          </div>
        </div>

        {/* Source metadata */}
        <div className="bg-slate-950 p-3.5 rounded-lg border border-slate-800 text-xs space-y-1.5">
          <div className="flex justify-between">
            <span className="text-slate-500">Source Document:</span>
            <span className="text-slate-300 font-medium truncate max-w-[200px]">{data.sourceTitle}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Source Identifier:</span>
            <span className="text-teal-400 font-mono">{data.sourceId}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Context Conditions:</span>
            <span className="text-slate-300">{data.context}</span>
          </div>
        </div>

        {/* Limitations */}
        {data.limitations && data.limitations.length > 0 && (
          <div>
            <span className="text-[11px] font-mono text-amber-500 uppercase tracking-wider flex items-center gap-1 mb-1.5">
              <AlertCircle className="h-3.5 w-3.5" /> What Remains Uncertain
            </span>
            <ul className="list-disc pl-4 space-y-1 text-xs text-slate-400">
              {data.limitations.map((lim, i) => (
                <li key={i}>{lim}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};
