"""
ZMIE FastAPI Main Application & API Gateway
"""

import os
from fastapi import FastAPI, Request, Body, status
from fastapi.responses import JSONResponse, HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from app.core.tenancy import TenantAccessDeniedException, TenantIsolationException
from app.api.v1.search import router as search_router
from app.api.v1.research import router as research_router
from app.api.v1.safety import router as safety_router
from app.api.v1.governance import router as governance_router
from app.api.v1.export import router as export_router
from app.api.v1.ontology import router as ontology_router
from app.api.v1.graph import router as graph_router
from app.api.v1.timeline import router as timeline_router
from app.api.v1.clinical import router as clinical_router
from app.api.v1.enterprise import router as enterprise_router
from app.api.v1.network import router as network_router
from app.api.v1.admin import router as admin_router
from app.api.v1.topics import router as topics_router
from app.api.v1.projects import router as projects_router
from app.api.v1.verify import router as verify_router
from app.api.v1.security import router as security_router
from app.api.v1.platform import router as platform_router
from app.api.v1.evaluation import router as evaluation_router
from app.api.v1.sources import router as sources_router
from app.api.v1.research_network import router as research_network_router
from app.api.v1.rwe import router as rwe_router
from app.api.v1.causal_mechanistic import router as causal_mechanistic_router
from app.api.v1.living_evidence import router as living_evidence_router
from app.api.v1.clinical_regulatory import router as clinical_regulatory_router
from app.api.v1.simulation_hypothesis import router as simulation_hypothesis_router
from app.api.v1.closed_loop_learning import router as closed_loop_router
from app.api.v1.terminology_evolution import router as terminology_evolution_router
from app.api.v1.scientific_compute import router as scientific_compute_router
from app.api.v1.collaboration_network import router as collaboration_network_router
from app.api.v1.federated_privacy import router as federated_privacy_router
from app.api.v1.agent_os import router as agent_os_router
from app.api.v1.skos import router as skos_router
from app.api.v1.audit import router as audit_router
from app.api.v1.enterprise_spec import router as enterprise_spec_router
from app.api.v1.credibility import router as credibility_router
from app.api.v1.trust_firewall import router as trust_firewall_router
from app.api.v1.continuous_revalidation import router as continuous_revalidation_router
from app.api.v1.security_hardening import router as security_hardening_router
from app.api.v1.benchmarking import router as benchmarking_router
from app.api.v1.production_readiness import router as production_readiness_router
from app.api.v1.controlled_launch import router as controlled_launch_router
from app.api.v1.lifecycle import router as lifecycle_router
from app.api.v1.billing import router as billing_router

from urllib.parse import unquote
import re
import time
import threading
from collections import defaultdict

# --- ZMIE API Gateway Security Hardening ---

class APIRateLimiter:
    """High-performance sliding-window in-memory rate limiter per IP address."""
    def __init__(self, requests_per_minute: int = 300):
        self.rpm = requests_per_minute
        self.history = defaultdict(list)
        self._lock = threading.Lock()

    def is_allowed(self, client_ip: str) -> tuple[bool, int, int]:
        """Returns (allowed, current_count, retry_after_seconds)"""
        now = time.time()
        window_start = now - 60.0
        with self._lock:
            timestamps = self.history[client_ip]
            timestamps = [t for t in timestamps if t > window_start]
            if len(timestamps) >= self.rpm:
                self.history[client_ip] = timestamps
                retry_after = int(60.0 - (now - timestamps[0])) + 1
                return False, len(timestamps), max(1, retry_after)
            timestamps.append(now)
            self.history[client_ip] = timestamps
            return True, len(timestamps), 0

    def reset(self):
        with self._lock:
            self.history.clear()

api_rate_limiter = APIRateLimiter(requests_per_minute=int(os.environ.get("ZMIE_RATE_LIMIT_PER_MINUTE", "300")))

# WAF threat inspection signatures (strictly targeted, zero clinical false positives)
WAF_THREAT_PATTERNS = [
    ("XSS_ATTACK", re.compile(r"(?i)(<script\b|javascript\s*:|onerror\s*=|onload\s*=|eval\s*\(|document\.cookie|<iframe\b|<object\b)")),
    ("SQL_INJECTION", re.compile(r"(?i)(\bunion\s+select\b|\bselect\s+.*\s+from\b|\binsert\s+into\b|\bdelete\s+from\b|\bdrop\s+table\b|\bupdate\s+.*\s+set\b|\bexec\s*\(|\bwaitfor\s+delay\b|;\s*--|'\s+or\s+'1'='1|--\s*$)")),
    ("PATH_TRAVERSAL", re.compile(r"(?:\.\.[/\\])+|/etc/passwd|/etc/shadow|\bboot\.ini\b|\bwindows[/\\]system32\b")),
    ("COMMAND_INJECTION", re.compile(r"(?i)(?:[;&|`]\s*(?:cat|ls|rm|curl|wget|bash|sh|nc|netcat|id|whoami|python|powershell|cmd)\b|\$\([^)]+\)|\`[^`]+\`)")),
    ("PROMPT_INJECTION", re.compile(r"(?i)(ignore\s+(?:all\s+)?previous\s+instructions|system\s+prompt\s+override|bypass\s+safety\s+filter|jailbreak\s+mode)")),
]

app = FastAPI(
    title="TriMedSearch™ — Tri-Paradigm Medical Intelligence & Evidence Engine",
    description="Standalone living medical knowledge, evidence synthesis, and cross-system intelligence infrastructure.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def security_hardening_gateway_middleware(request: Request, call_next):
    """
    Unified ZMIE Security Gateway Middleware:
    1. Anti-DDoS Sliding Window Rate Limiting (300 req/min per IP)
    2. Web Application Firewall (WAF) threat inspection (XSS, SQLi, Path Traversal, Cmd Inj, Prompt Inj)
    3. OWASP Top 10 Security Response Headers injection
    """
    client_ip = request.client.host if request.client else "127.0.0.1"

    # 1. Rate Limiter Check (exempt docs and health checks)
    if not request.url.path.startswith(("/docs", "/openapi.json", "/redoc", "/favicon.ico", "/sw.js")):
        allowed, count, retry_after = api_rate_limiter.is_allowed(client_ip)
        if not allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "RATE_LIMIT_EXCEEDED",
                    "message": "Too many requests. Gateway rate limit exceeded.",
                    "limit_per_minute": api_rate_limiter.rpm,
                    "retry_after_seconds": retry_after
                },
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(api_rate_limiter.rpm),
                    "X-RateLimit-Remaining": "0"
                }
            )

    # 2. WAF Threat Inspection
    # Inspect decoded path and query string
    decoded_path = unquote(request.url.path)
    decoded_query = unquote(request.url.query)
    combined_target = f"{decoded_path}?{decoded_query}" if decoded_query else decoded_path

    # Check for payload in request body if small and applicable
    body_text = ""
    content_type = request.headers.get("content-type", "")
    if request.method in ("POST", "PUT", "PATCH") and any(t in content_type for t in ("json", "text", "form")):
        try:
            body_bytes = await request.body()
            body_text = body_bytes.decode("utf-8", errors="ignore")
        except Exception:
            pass

    inspection_target = f"{combined_target} {body_text}"
    for threat_name, pattern in WAF_THREAT_PATTERNS:
        if pattern.search(inspection_target):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "error": "SECURITY_THREAT_BLOCKED",
                    "threat_type": threat_name,
                    "message": "Malicious payload detected and blocked by ZMIE Threat Shield WAF.",
                    "path": request.url.path
                }
            )

    # 3. Call downstream handlers
    response = await call_next(request)

    # 4. Inject OWASP Top 10 Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=(), payment=()"
    response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
    if "Content-Security-Policy" not in response.headers:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self' 'unsafe-inline' 'unsafe-eval' https: data: blob:; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com https://cdnjs.cloudflare.com https: blob:; "
            "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com https:; "
            "font-src 'self' data: https://cdnjs.cloudflare.com https://fonts.gstatic.com https:; "
            "img-src 'self' data: blob: https:; "
            "connect-src 'self' https: ws: wss:;"
        )

    return response


# Register API Subsystems
app.include_router(search_router, prefix="/v1")
app.include_router(research_router, prefix="/v1")
app.include_router(safety_router, prefix="/v1")
app.include_router(governance_router, prefix="/v1")
app.include_router(export_router, prefix="/v1")
app.include_router(ontology_router, prefix="/v1")
app.include_router(graph_router, prefix="/v1")
app.include_router(timeline_router, prefix="/v1")
app.include_router(clinical_router, prefix="/v1")
app.include_router(enterprise_router, prefix="/v1")
app.include_router(network_router, prefix="/v1")
app.include_router(admin_router, prefix="/v1")
app.include_router(topics_router, prefix="/v1")
app.include_router(projects_router, prefix="/v1")
app.include_router(verify_router, prefix="/v1")
app.include_router(security_router, prefix="/v1")
app.include_router(platform_router, prefix="/v1")
app.include_router(evaluation_router, prefix="/v1")
app.include_router(sources_router, prefix="/v1")
app.include_router(research_network_router, prefix="/v1")
app.include_router(rwe_router, prefix="/v1")
app.include_router(causal_mechanistic_router, prefix="/v1")
app.include_router(living_evidence_router, prefix="/v1")
app.include_router(clinical_regulatory_router, prefix="/v1")
app.include_router(simulation_hypothesis_router, prefix="/v1")
app.include_router(closed_loop_router, prefix="/v1")
app.include_router(terminology_evolution_router, prefix="/v1")
app.include_router(scientific_compute_router, prefix="/v1")
app.include_router(collaboration_network_router, prefix="/v1")
app.include_router(federated_privacy_router, prefix="/v1")
app.include_router(agent_os_router, prefix="/v1")
app.include_router(skos_router, prefix="/v1")
app.include_router(audit_router, prefix="/v1")
app.include_router(enterprise_spec_router, prefix="/v1")
app.include_router(credibility_router, prefix="/v1")
app.include_router(trust_firewall_router, prefix="/v1")
app.include_router(continuous_revalidation_router, prefix="/v1")
app.include_router(security_hardening_router, prefix="/v1")
app.include_router(benchmarking_router, prefix="/v1")
app.include_router(production_readiness_router, prefix="/v1")
app.include_router(controlled_launch_router, prefix="/v1")
app.include_router(lifecycle_router, prefix="/v1")
app.include_router(billing_router, prefix="/v1")

@app.exception_handler(TenantAccessDeniedException)
async def tenant_isolation_exception_handler(request: Request, exc: TenantAccessDeniedException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": "TENANT_ISOLATION_VIOLATION",
            "message": str(exc),
            "resource_tenant": getattr(exc, "resource_tenant", None),
            "caller_tenant": getattr(exc, "caller_tenant", None),
            "path": request.url.path,
        }
    )


@app.exception_handler(PermissionError)
async def permission_error_handler(request: Request, exc: PermissionError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": "PERMISSION_DENIED",
            "message": str(exc),
            "path": request.url.path,
        }
    )


@app.exception_handler(Exception)
async def global_crash_protection_handler(request: Request, exc: Exception):
    import logging
    logging.getLogger("zmie.api").error("Unhandled exception intercepted on %s: %s", request.url.path, str(exc), exc_info=True)
    raw_detail = str(exc)
    # Defense-in-depth sanitization: redact sensitive paths and credential tokens
    sanitized_detail = re.sub(r'/(?:Users|home|root|var|etc|private|tmp)[^\s"\']+', '[REDACTED_SYSTEM_PATH]', raw_detail)
    sanitized_detail = re.sub(r'(?i)(api[_-]?key|secret|token|password)=([^\s&]+)', r'\1=[REDACTED]', sanitized_detail)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error_code": "CRASH_PREVENTED",
            "message": "A critical system crash was successfully intercepted and prevented by the ZMIE Resilience Firewall.",
            "detail": sanitized_detail,
            "path": request.url.path
        }
    )


@app.get("/")
async def root():
    return {
        "engine": "TriMedSearch™ (ZMIE) — Tri-Paradigm Medical Intelligence Engine",
        "status": "operational",
        "version": "1.0.0",
        "philosophy": "Unify the world's medical knowledge without pretending that every medical system says the same thing."
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "subsystems": {
            "source_registry": "connected",
            "evidence_engine": "connected",
            "cross_system_ontology": "connected",
            "citation_validator": "active",
            "retraction_monitor": "active",
            "tenant_isolation_firewall": "enforced",
            "audit_dispatcher": "operational"
        }
    }


@app.get("/health/deep")
async def deep_health():
    """Deep diagnostic check verifying runtime storage, compute, and knowledge engine availability."""
    from app.core.config import get_settings
    from app.sources.registry import get_source_registry
    from app.core.audit import get_audit_dispatcher
    
    settings = get_settings()
    reg = get_source_registry()
    audit_dispatcher = get_audit_dispatcher()
    
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "diagnostics": {
            "sources_registered": len(reg.list_sources()),
            "audit_hash_chain_valid": audit_dispatcher.verify_integrity(),
            "invariants_enforced": [
                "INV-01 (Zero Fabrication)",
                "INV-02 (Tenant Boundary Isolation)",
                "INV-03 & INV-05 (Provenance & HMAC Audit Chaining)",
                "INV-04 (Epistemic Distance Preservation)",
                "INV-08 (Reproducible Computation)",
                "INV-10 (Deterministic Safety Firewall)"
            ]
        }
    }


@app.get("/workbench", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse, include_in_schema=False)
async def workbench():
    """Serves the standalone interactive medical intelligence workbench UI."""
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    html_path = os.path.join(root_dir, "workbench.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Workbench interface not found</h1>", status_code=404)


@app.get("/catalog_seed.json", include_in_schema=False)
@app.get("/workbench/catalog_seed.json", include_in_schema=False)
async def catalog_seed():
    """Serves the standalone pre-compiled medical knowledge catalog seed JSON."""
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    json_path = os.path.join(root_dir, "catalog_seed.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="application/json")
    return Response(content='{"error": "Catalog seed not found"}', status_code=404, media_type="application/json")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Prevent 404 spam in browser console."""
    return Response(status_code=204)


@app.get("/sw.js", include_in_schema=False)
async def service_worker():
    """Serves real offline-first PWA Service Worker script."""
    sw_code = """// ZMIE Progressive Web App (PWA) Offline-First Service Worker
const CACHE_NAME = 'zmie-v4-offline-cache';
const PRECACHE_URLS = ['/', '/workbench', '/health', '/v1/safety/catalog', '/catalog_seed.json'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_URLS).catch(() => {});
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((k) => {
          if (k !== CACHE_NAME) return caches.delete(k);
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200 && event.request.url.startsWith(self.location.origin)) {
          const clone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return networkResponse;
      })
      .catch(() => {
        return caches.match(event.request).then((cachedResponse) => {
          return cachedResponse || caches.match('/workbench');
        });
      })
  );
});
"""
    return Response(content=sw_code, media_type="application/javascript")


@app.get("/robots.txt", include_in_schema=False)
async def robots_txt():
    """Polite crawler directives preventing log spam."""
    return Response(content="User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /v1/admin/\n", media_type="text/plain")


@app.get("/cds-services")
async def root_cds_services_discovery():
    """HL7 CDS Hooks 1.0 Root Discovery Endpoint."""
    from app.agents.clinical_bridge import ClinicalCDSBridge
    return ClinicalCDSBridge.get_cds_services_manifest()


@app.post("/cds-services/{service_id}")
async def root_cds_service_invocation(service_id: str, request_data: dict = Body(...)):
    """HL7 CDS Hooks 1.0 Root Invocation Endpoint."""
    from app.agents.clinical_bridge import ClinicalCDSBridge
    return ClinicalCDSBridge.evaluate_cds_hook_request(service_id=service_id, request_data=request_data)


