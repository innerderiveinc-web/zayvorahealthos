export interface SearchResultItem {
  id: string;
  title: string;
  resultType: string;
  source: string;
  date: string;
  evidenceGrade: string;
  snippet: string;
  whyRelevant: string;
  status: "Current" | "Superseded" | "Retracted" | "Conflicting" | "Limited Evidence";
  doiOrPmid?: string;
  system?: string;
}

export interface ClaimTraceData {
  claimId: string;
  claimText: string;
  normalizedClaim: {
    subject: string;
    predicate: string;
    object: string;
    population?: string;
    effect?: string;
  };
  evidenceLevel: string;
  sourceId: string;
  sourceTitle: string;
  passage: string;
  context: string;
  limitations: string[];
  verificationStatus: "SUPPORTED" | "PARTIALLY_SUPPORTED" | "CONTRADICTED" | "UNVERIFIED" | "BLOCKED";
}

export interface ContradictionRecord {
  topic: string;
  type: string;
  divergence: string;
  positionA: { claim: string; population?: string; grade: string };
  positionB: { claim: string; population?: string; grade: string };
  probableCause: string;
  resolution: string;
}

export interface ResearchPlanData {
  planId: string;
  title: string;
  primaryQuestion: string;
  subQuestions: string[];
  pico: {
    population: string;
    intervention: string;
    comparator?: string;
    outcomes: string[];
  };
  criteria: {
    inclusion: string[];
    exclusion: string[];
  };
}

export interface EvidenceTableItem {
  evidenceId: string;
  studyTitle: string;
  year: string;
  studyDesign: string;
  population: string;
  sampleSize: number;
  intervention: string;
  comparator?: string;
  outcome: string;
  findings: string;
  safety: string;
  evidenceGrade: string;
  source: string;
}

export interface AgentTaskStep {
  stepId: string;
  agentRole: string;
  action: string;
  status: "COMPLETED" | "RUNNING" | "PENDING" | "VERIFIED" | "VETOED";
  evidenceAttached?: string[];
  latencyMs: number;
}

export interface ResearchSnapshotItem {
  snapshotId: string;
  title: string;
  createdDate: string;
  sha256Hash: string;
  hmacSignature: string;
  studiesCount: number;
  claimsCount: number;
  reproducibilityStatus: "EXACT_MATCH" | "VERIFIED" | "DRIFT_DETECTED";
  isLocked: boolean;
}

export interface ComputationalJobItem {
  jobId: string;
  query: string;
  engine: "DuckDB" | "Parquet" | "Polars";
  recordsProcessed: number;
  seedLocked: number;
  certificateId: string;
  relativeDivergence: number;
  status: "FULLY_REPRODUCIBLE" | "COMPLETED";
}

export interface GRADEProfileItem {
  outcomeName: string;
  relativeEffect: string;
  absoluteRisk: string;
  participants: number;
  studiesCount: number;
  riskOfBias: "LOW" | "MODERATE" | "HIGH";
  inconsistency: "NONE" | "SERIOUS";
  indirectness: "NONE" | "SERIOUS";
  imprecision: "NONE" | "SERIOUS";
  certainty: "HIGH" | "MODERATE" | "LOW" | "VERY_LOW";
}
