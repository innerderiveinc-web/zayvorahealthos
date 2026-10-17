"""
ZMIE Controlled Launch & Continuous Monitoring FastAPI Router
PROMPT 35 Architecture Implementation
"""

from typing import List, Dict, Optional, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.controlled_launch.engine import ControlledLaunchEngine
from app.controlled_launch.models import (
    ControlledLaunchPlan,
    ContinuousMonitoringTelemetry,
    MonitoringDaemonStatus,
    TripwireCause,
    ControlledProductionLaunchReport,
    ProductionScopeCertificate,
    ProductionIncidentRecord,
)

router = APIRouter(prefix="/controlled-launch", tags=["Controlled Launch & Continuous Monitoring"])

# Global singleton
_launch_engine = ControlledLaunchEngine()


def get_launch_engine() -> ControlledLaunchEngine:
    return _launch_engine


class RollbackRequest(BaseModel):
    reason: str
    cause: TripwireCause = TripwireCause.MANUAL_OPERATOR_ABORT


class SimulateTripwireRequest(BaseModel):
    cause: TripwireCause = TripwireCause.CITATION_FABRICATION_DETECTED
    details: Dict[str, Any] = {}


@router.get("/plan", response_model=ControlledLaunchPlan)
def get_launch_plan(
    engine: ControlledLaunchEngine = Depends(get_launch_engine)
):
    """
    Returns current progressive ring-based rollout plan and canary telemetry.
    """
    return engine.get_launch_plan()


@router.post("/promote", response_model=ControlledLaunchPlan)
def promote_to_next_ring(
    engine: ControlledLaunchEngine = Depends(get_launch_engine)
):
    """
    Promotes rollout to next ring (Ring 0 -> Ring 1 -> Ring 2 -> Ring 3) after verifying canary criteria.
    """
    try:
        return engine.promote_to_next_ring()
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rollback", response_model=ControlledLaunchPlan)
def rollback(
    req: RollbackRequest,
    engine: ControlledLaunchEngine = Depends(get_launch_engine)
):
    """
    Executes emergency circuit-breaker rollback to Ring 0.
    """
    return engine.trigger_circuit_breaker_rollback(reason=req.reason, cause=req.cause)


@router.post("/simulate-tripwire", response_model=ControlledLaunchPlan)
def simulate_tripwire(
    req: SimulateTripwireRequest,
    engine: ControlledLaunchEngine = Depends(get_launch_engine)
):
    """
    Simulates an automated tripwire event and triggers immediate circuit breaker rollback.
    """
    return engine.simulate_tripwire(cause=req.cause, details=req.details)


@router.get("/telemetry", response_model=ContinuousMonitoringTelemetry)
def get_telemetry(
    engine: ControlledLaunchEngine = Depends(get_launch_engine)
):
    """
    Samples real-time 24/7 continuous health and revalidation telemetry.
    """
    return engine.sample_continuous_monitoring_telemetry()


@router.get("/daemons", response_model=List[MonitoringDaemonStatus])
def get_daemons(
    engine: ControlledLaunchEngine = Depends(get_launch_engine)
):
    """
    Returns operational status of all 5 autonomous monitoring daemons.
    """
    return engine.get_monitoring_daemons()


@router.get("/slos", response_model=Dict[str, Any])
def get_slos(
    engine: ControlledLaunchEngine = Depends(get_launch_engine)
):
    """
    Returns platform SLO targets, observed canary metrics, and remaining error budget.
    """
    return engine.get_slos()


@router.post("/launch-report", response_model=ControlledProductionLaunchReport)
@router.get("/launch-report", response_model=ControlledProductionLaunchReport)
def generate_launch_report(
    engine: ControlledLaunchEngine = Depends(get_launch_engine)
):
    """
    Clause 317: Produces the official ZMIE Controlled Production Launch Report with signed governance authorization.
    """
    return engine.generate_launch_report()


@router.post("/scope-certificate", response_model=ProductionScopeCertificate)
@router.get("/scope-certificate", response_model=ProductionScopeCertificate)
def issue_scope_certificate(
    engine: ControlledLaunchEngine = Depends(get_launch_engine)
):
    """
    Clause 297: Issues the official cryptographic ZMIE Production Scope Certificate.
    """
    return engine.issue_scope_certificate()


@router.post("/incidents", response_model=ControlledLaunchPlan)
def log_incident(
    incident: ProductionIncidentRecord,
    engine: ControlledLaunchEngine = Depends(get_launch_engine)
):
    """
    Clauses 137-148: Logs a production incident. If severity is P0, automatically triggers zero-second rollback.
    """
    return engine.log_incident(incident)

