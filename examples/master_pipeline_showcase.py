#!/usr/bin/env python3
"""
ZMIE Master Knowledge Evolution Pipeline Showcase
Demonstrating the complete unbroken continuum:
Source -> Research -> Data -> Mechanism/Causality -> Living Evidence -> Knowledge Evolution.
"""

import sys
import json
from app.research.master_pipeline import MasterKnowledgeEvolutionPipeline


def run_master_pipeline_showcase():
    print("=" * 85)
    print("  ZMIE — MASTER KNOWLEDGE EVOLUTION PIPELINE")
    print("  Source -> Research -> Data -> Mechanism/Causality -> Living Evidence -> Knowledge Evolution")
    print("=" * 85)

    pipeline = MasterKnowledgeEvolutionPipeline()
    result = pipeline.run_pipeline("SGLT2_HEART_FAILURE")

    print(f"\nRun ID       : {result['pipeline_run_id']}")
    print(f"Topic        : {result['topic']}")
    print(f"Executed At  : {result['executed_at']}")
    print(f"Completed At : {result['completed_at']}\n")

    for stage_data in result["unbroken_chain"]:
        stage_name = stage_data["stage"]
        status = stage_data["status"]
        print("-" * 85)
        print(f"[{stage_name}] Status: {status}")
        print("-" * 85)
        for k, v in stage_data.items():
            if k in ["stage", "status"]:
                continue
            if isinstance(v, dict):
                print(f"  {k}:")
                for sub_k, sub_v in v.items():
                    print(f"    * {sub_k:<28}: {sub_v}")
            elif isinstance(v, list):
                print(f"  {k}:")
                for item in v:
                    print(f"    * {item}")
            else:
                print(f"  {k:<30}: {v}")
        print()

    print("=" * 85)
    print(f"  MASTER PIPELINE VERDICT:")
    print(f"  {result['master_verdict']}")
    print("=" * 85)


if __name__ == "__main__":
    run_master_pipeline_showcase()
