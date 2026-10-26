// ZMIE Public Knowledge REST API Client SDK (TypeScript / JavaScript)
// For web applications, node services, and clinical workflows.

export interface SearchResponse {
  query: string;
  summary: string;
  what_medicine_knows: string[];
  evidence_breakdown: {
    human_rcts: number;
    meta_analyses: number;
    overall_grade: string;
  };
  cross_system_perspectives: Record<string, any>;
  contradictions: Record<string, any>;
  citations: Array<{
    citation_id: string;
    title: string;
    year: number;
    authority_tier: string;
  }>;
  coverage_score: number;
}

export interface ClaimPassport {
  claim_id: string;
  statement: string;
  source: {
    source_id: string;
    organization: string;
    authority_tier: string;
  };
  evidence_context: Record<string, any>;
  entailment_audit: {
    verdict: string;
    confidence: number;
  };
}

export class ZMIEClient {
  private baseUrl: string;
  private apiKey?: string;

  constructor(config?: { baseUrl?: string; apiKey?: string }) {
    this.baseUrl = (config?.baseUrl || "http://localhost:8000").replace(/\/$/, "");
    this.apiKey = config?.apiKey;
  }

  private async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const headers: Record<string, string> = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    };

    if (this.apiKey) {
      headers["Authorization"] = `Bearer ${this.apiKey}`;
    }

    const response = await fetch(`${this.baseUrl}${path}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`ZMIE API Error: ${response.status} ${response.statusText}`);
    }

    return response.json() as Promise<T>;
  }

  async search(query: string, mode: "public" | "evidence_only" | "researcher_deep" = "public"): Promise<SearchResponse> {
    const params = new URLSearchParams({ q: query, mode });
    return this.request<SearchResponse>(`/v1/search?${params.toString()}`);
  }

  async auditClaim(claimId: string): Promise<ClaimPassport> {
    return this.request<ClaimPassport>(`/v1/search/why-this/${encodeURIComponent(claimId)}`);
  }

  async compareSystems(topic: string): Promise<any> {
    const params = new URLSearchParams({ topic });
    return this.request<any>(`/v1/ontology/compare?${params.toString()}`);
  }

  async evaluateSafety(payload: { substance: string; medications?: string[]; symptoms?: string[] }): Promise<any> {
    return this.request<any>("/v1/safety/evaluate", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }
}
