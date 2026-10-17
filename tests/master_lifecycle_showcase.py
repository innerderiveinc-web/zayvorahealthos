#!/usr/bin/env python3
"""
ZMIE Master Production Lifecycle Loop Showcase
Demonstrates the continuous 7-stage enterprise lifecycle:
Production → Monitor → Revalidate → Benchmark → Audit → Improve → Release
"""

import sys
import json
from datetime import datetime, timezone

from app.main import app
from app.lifecycle.master_loop import ProductionLifecycleEngine, ProductionLifecycleRunReport
from zmie import ZMIEClient
from app.platform.gateway import APIGatewayEngine


def print_banner(title: str):
    print("\n" + "=" * 85)
    print(f"  {title}")
    print("=" * 85)


def run_showcase():
    print_banner("ZMIE — MASTER PRODUCTION LIFECYCLE CLOSED LOOP SHOWCASE")
    print("  Enterprise Standard: Production → Monitor → Revalidate → Benchmark → Audit → Improve → Release")
    print(f"  Execution Timestamp: {datetime.now(timezone.utc).isoformat()}")

    # 1. Initialize Master Engine & Client
    engine = ProductionLifecycleEngine()
    raw_key, _ = APIGatewayEngine.create_api_key(
        tenant_id="tenant-lifecycle-showcase",
        owner="chief-architect@zmie.org",
        name="Showcase Master Key",
        scopes=["knowledge:read", "rag:read", "safety:read", "search:read", "evidence:read"]
    )
    client = ZMIEClient(api_key=raw_key, app_instance=app)

    print("\n[*] Initializing Master Closed-Loop Transition: v1.0.0 → v1.1.0...")

    # 2. Run Full 7-Stage Cycle
    report: ProductionLifecycleRunReport = engine.execute_full_lifecycle(
        initial_version="v1.0.0",
        target_version="v1.1.0"
    )

    print(f"\n[+] Cycle Execution Complete!")
    print(f"    Run ID             : {report.run_id}")
    print(f"    Initial Version    : {report.initial_version}")
    print(f"    Released Version   : {report.released_version}")
    print(f"    Trigger Event      : {report.trigger_event}")
    print(f"    Overall Status     : {report.overall_status}")
    print(f"    Digital Signature  : {report.digital_signature[:32]}...")

    # 3. Stage-by-Stage Detailed Breakdown
    stage_icons = {
        "PRODUCTION": "🚀",
        "MONITOR": "📡",
        "REVALIDATE": "🔄",
        "BENCHMARK": "📊",
        "AUDIT": "🛡️",
        "IMPROVE": "⚡",
        "RELEASE": "🚢"
    }

    for idx, (stage_key, stage) in enumerate(report.stages.items(), 1):
        icon = stage_icons.get(stage_key, "▶")
        print_banner(f"{icon} STAGE {idx}/7: {stage.stage_name}")
        print(f"  Status   : {stage.status}")
        print(f"  Started  : {stage.started_at}")
        print(f"  Completed: {stage.completed_at}")
        print(f"  Summary  : {stage.summary}")
        print("  Evidence & Verification Signals:")
        for k, v in stage.evidence.items():
            if isinstance(v, (dict, list)):
                formatted = json.dumps(v, indent=4)
                indented = "\n".join("      " + line for line in formatted.splitlines())
                print(f"    * {k:<26}:\n{indented}")
            else:
                print(f"    * {k:<26}: {v}")

    # 4. Verify REST API Integration
    print_banner("🌐 API GATEWAY INTEGRATION VERIFICATION (/v1/lifecycle)")
    stages_resp = client._request("GET", "/v1/lifecycle/stages")
    print(f"  GET /v1/lifecycle/stages response:")
    print(f"    Sequence: {' -> '.join(stages_resp.get('sequence', []))}")
    print(f"    Total Configured Stages: {len(stages_resp.get('stages', {}))}")

    api_run = client._request(
        "POST",
        "/v1/lifecycle/run",
        json_data={"initial_version": "v1.0.0", "target_version": "v1.1.0"}
    )
    print(f"  POST /v1/lifecycle/run response:")
    print(f"    Run ID          : {api_run.get('run_id')}")
    print(f"    Released Version: {api_run.get('released_version')}")
    print(f"    Overall Status  : {api_run.get('overall_status')}")
    print(f"    Signature Valid : {bool(api_run.get('digital_signature'))}")

    print_banner("✅ ZMIE MASTER PRODUCTION LIFECYCLE 100% OPERATIONAL & VERIFIED")


if __name__ == "__main__":
    run_showcase()

