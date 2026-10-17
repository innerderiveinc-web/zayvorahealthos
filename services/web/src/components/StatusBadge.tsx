import React from "react";
import clsx from "clsx";

export type BadgeStatus =
  | "Current"
  | "Superseded"
  | "Retracted"
  | "Conflicting"
  | "Limited Evidence"
  | "SUPPORTED"
  | "PARTIALLY_SUPPORTED"
  | "UNVERIFIED"
  | "BLOCKED"
  | "Pass"
  | "Modify"
  | "Block";

interface StatusBadgeProps {
  status: BadgeStatus | string;
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, className }) => {
  const sLower = status.toLowerCase();

  let colorClasses = "bg-slate-800 text-slate-300 border-slate-700";

  if (sLower === "current" || sLower === "supported" || sLower === "pass") {
    colorClasses = "bg-emerald-950/70 text-emerald-300 border-emerald-800/60";
  } else if (sLower === "partially_supported" || sLower === "limited evidence" || sLower === "modify") {
    colorClasses = "bg-amber-950/70 text-amber-300 border-amber-800/60";
  } else if (sLower === "conflicting") {
    colorClasses = "bg-indigo-950/70 text-indigo-300 border-indigo-800/60";
  } else if (sLower === "retracted" || sLower === "blocked" || sLower === "block") {
    colorClasses = "bg-rose-950/70 text-rose-300 border-rose-800/60";
  } else if (sLower === "superseded" || sLower === "unverified") {
    colorClasses = "bg-slate-900 text-slate-400 border-slate-800";
  }

  return (
    <span
      className={clsx(
        "inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border tracking-wide uppercase",
        colorClasses,
        className
      )}
    >
      {status}
    </span>
  );
};
