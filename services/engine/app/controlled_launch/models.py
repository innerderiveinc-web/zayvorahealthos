"""
ZMIE Controlled Launch & Continuous Monitoring Models
PROMPT 35 Architecture Implementation
Progressive Rings, Feature Registry, Incident Management & Scope Certificates
"""

from __future__ import annotations
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DeploymentRing(str, Enum):
    """The 4 Progressive Deployment Rings (Prompt 35)."""
    RING_0_INTERNAL = "RING_0_INTERNAL"
    RING_1_PILOT_ACADEMIC = "RING_1_PILOT_ACADEMIC"
    RING_2_CLINICAL_NETWORK = "RING_2_CLINICAL_NETWORK"
    RING_3_GLOBAL_PRODUCTION = "RING_3_GLOBAL_PRODUCTION"


class RolloutStatus(str, Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ROLLED_BACK = "ROLLED_BACK"
    COMPLETED = "COMPLETED"


class LaunchMode(str, Enum):
    """The 6 Production Launch Modes (Clause 8)."""
    INTERNAL = "INTERNAL"
    PRIVATE_PILOT = "PRIVATE_PILOT"
    ENTERPRISE_PILOT = "ENTERPRISE_PILOT"
    LIMITED_PRODUCTION = "LIMITED_PRODUCTION"
    PUBLIC_BETA = "PUBLIC_BETA"
    GENERAL_AVAILABILITY = "GENERAL_AVAILABILITY"


class ProductionFeatureState(str, Enum):
    """Production Feature Lifecycle States (Clause 9)."""
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    INTERNAL_ONLY = "INTERNAL_ONLY"
    PILOT_ONLY = "PILOT_ONLY"
    RESTRICTED = "RESTRICTED"
    BLOCKED = "BLOCKED"
    DEGRADED = "DEGRADED"
    PAUSED = "PAUSED"


class TripwireCause(str, Enum):
    """Automated Circuit-Breaker Tripwire Causes."""
    CITATION_FABRICATION_DETECTED = "CITATION_FABRICATION_DETECTED"
    CROSS_TENANT_LEAKAGE = "CROSS_TENANT_LEAKAGE"
    INVARIANT_VIOLATION = "INVARIANT_VIOLATION"
    SAFETY_FIREWALL_BREACH = "SAFETY_FIREWALL_BREACH"
    SLO_LATENCY_BREACH = "SLO_LATENCY_BREACH"
    MANUAL_OPERATOR_ABORT = "MANUAL_OPERATOR_ABORT"


class IncidentSeverity(str, Enum):
    """Production Incident Severity Taxonomy (Clause 138)."""
    P0 = "P0"  # Cross-tenant data leakage, critical security breach, critical scientific integrity failure
    P1 = "P1"  # Severe degradation, key service unavailable
    P2 = "P2"  # Non-critical functionality degraded
    P3 = "P3"  # Minor informational issue


class CanaryTelemetryMetrics(BaseModel):
    traffic_percentage: float
    requests_evaluated: int
    error_rate: float
    p99_latency_ms: float
    invariant_violations: int = 0
    hallucination_rate: float = 0.0
    calculation_errors: int = 0
    citation_fidelity: float = 1.0
    tenant_boundary_breaches: int = 0
    epistemic_drift_alerts: int = 0
    error_budget_remaining: float = 1.0
    is_healthy: bool = True


class ReleaseRingState(BaseModel):
    ring: DeploymentRing
    status: RolloutStatus
    traffic_percentage: float
    tenants_enrolled: List[str]
    canary_metrics: CanaryTelemetryMetrics
    slo_targets: Dict[str, float] = Field(default_factory=dict)
    allowed_capabilities: List[str] = Field(default_factory=list)
    promoted_at: Optional[str] = None


class TripwireEvent(BaseModel):
    tripwire_id: str
    cause: TripwireCause
    ring_tripped: DeploymentRing
    details: Dict[str, Any] = Field(default_factory=dict)
    rollback_target: DeploymentRing = DeploymentRing.RING_0_INTERNAL
    tripped_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class MonitoringDaemonStatus(BaseModel):
    daemon_name: str
    status: str  # "ACTIVE", "HEALTHY", "DEGRADED"
    last_heartbeat: str
    items_scanned_last_hour: int
    anomalies_detected: int = 0
    details: Dict[str, Any] = Field(default_factory=dict)


class ProductionFeatureItem(BaseModel):
    """Production Feature Registry Entry (Clause 10)."""
    feature_name: str
    version: str
    scope: str
    status: ProductionFeatureState
    dependencies: List[str] = Field(default_factory=list)
    owner: str
    risk: str
    rollback_strategy: str


class ProductionIncidentRecord(BaseModel):
    """Production Incident Log Entry (Clauses 137-148)."""
    incident_id: str
    severity: IncidentSeverity
    title: str
    description: str
    affected_scope: str
    status: str  # "OPEN", "CONTAINED", "RESOLVED", "CLOSED"
    action_taken: str
    detected_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    resolved_at: Optional[str] = None


class ControlledLaunchPlan(BaseModel):
    plan_id: str
    target_version: str
    release_id: str = "REL-ZMIE-2026.10-GA-1"
    current_ring: DeploymentRing
    launch_mode: LaunchMode = LaunchMode.INTERNAL
    rings: Dict[str, ReleaseRingState]
    circuit_breaker_armed: bool = True
    recent_tripwires: List[TripwireEvent] = Field(default_factory=list)
    feature_registry: List[ProductionFeatureItem] = Field(default_factory=list)
    incident_log: List[ProductionIncidentRecord] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class ContinuousMonitoringTelemetry(BaseModel):
    telemetry_id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    registry_sync_status: str = "HEALTHY"
    retraction_radar_status: str = "ACTIVE"
    living_graph_nodes_monitored: int
    active_invariants_count: int = 10
    audit_chain_hmac_verified: bool = True
    epistemic_drift_score: float = 0.80
    tenant_isolation_status: str = "ENFORCED"
    active_daemons: List[MonitoringDaemonStatus] = Field(default_factory=list)
    system_health_verdict: str = "OPERATIONAL"


class ControlledProductionLaunchReport(BaseModel):
    """Clause 317: Final Controlled Production Launch Report."""
    report_id: str
    release_id: str
    deployment_mode: LaunchMode
    launch_scope: Dict[str, Any]
    current_stage: DeploymentRing
    features_enabled: List[str]
    features_blocked: List[str]
    features_restricted: List[str]
    canary_metrics: CanaryTelemetryMetrics
    security_status: str = "HARDENED"
    privacy_status: str = "ISOLATED"
    scientific_integrity_status: str = "VERIFIED"
    trust_status: str = "FIREWALL_ACTIVE"
    monitoring_status: str = "ACTIVE_5_DAEMONS"
    rollback_status: str = "ARMED_AND_READY"
    active_incidents: List[ProductionIncidentRecord] = Field(default_factory=list)
    open_risks: List[str] = Field(default_factory=list)
    final_decision: str = "GO_LIVE_APPROVED"
    digital_signature: str
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class ProductionScopeCertificate(BaseModel):
    """Clause 297: Production Scope Certificate."""
    certificate_id: str
    release_id: str
    validated_scopes: List[str]
    restricted_scopes: List[str]
    known_limitations: List[str]
    authority: str = "Chief Launch Officer & Release Governance Authority"
    digital_signature: str
    certified_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
