"""
ZMIE Evaluation & Scientific Validation Lab REST API Router
Exposes endpoints for:
- Benchmarks and datasets
- Evaluation runs, results, metrics, and error cascades
- Scientific experiments and 6-layer ablations
- Model comparisons and release quality gates
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.models.evaluation import (
    Benchmark, BenchmarkDataset, EvaluationRun, CaseEvaluationResult,
    Experiment, ReleaseScorecard, MetricDefinition
)
from app.evaluation.registry import BenchmarkRegistry
from app.evaluation.runner import EvaluationRunner
from app.evaluation.experiments import ExperimentEngine
from app.evaluation.gate import ReleaseGateEngine

router = APIRouter(prefix="/evaluation", tags=["Evaluation & Scientific Validation Lab"])


# --- Benchmarks & Datasets ---

@router.get("/benchmarks", response_model=List[Benchmark])
def list_benchmarks():
    return BenchmarkRegistry.list_benchmarks()


@router.get("/benchmarks/{benchmark_id}", response_model=Benchmark)
def get_benchmark(benchmark_id: str):
    bmk = BenchmarkRegistry.get_benchmark(benchmark_id)
    if not bmk:
        raise HTTPException(status_code=404, detail="Benchmark not found.")
    return bmk


@router.get("/datasets", response_model=List[BenchmarkDataset])
def list_datasets():
    return BenchmarkRegistry.list_datasets()


@router.get("/datasets/{dataset_id}", response_model=BenchmarkDataset)
def get_dataset(dataset_id: str):
    ds = BenchmarkRegistry.get_dataset(dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    return ds


@router.get("/metrics", response_model=List[MetricDefinition])
def list_metrics():
    return BenchmarkRegistry.list_metrics()


# --- Evaluation Runs ---

class TriggerRunRequest(BaseModel):
    benchmark_id: str
    model_version: str = "claude-3-5-sonnet"
    knowledge_version: str = "2026.10"


@router.post("/runs", response_model=EvaluationRun)
def trigger_run(req: TriggerRunRequest):
    try:
        return EvaluationRunner.execute_benchmark(
            benchmark_id=req.benchmark_id,
            model_version=req.model_version,
            knowledge_version=req.knowledge_version
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/runs", response_model=List[EvaluationRun])
def list_runs():
    return EvaluationRunner.list_runs()


@router.get("/runs/{run_id}", response_model=EvaluationRun)
def get_run(run_id: str):
    run_obj = EvaluationRunner.get_run(run_id)
    if not run_obj:
        raise HTTPException(status_code=404, detail="Run not found.")
    return run_obj


@router.get("/runs/{run_id}/results", response_model=List[CaseEvaluationResult])
def get_run_results(run_id: str):
    run_obj = EvaluationRunner.get_run(run_id)
    if not run_obj:
        raise HTTPException(status_code=404, detail="Run not found.")
    return run_obj.case_results


@router.get("/runs/{run_id}/metrics")
def get_run_metrics(run_id: str):
    run_obj = EvaluationRunner.get_run(run_id)
    if not run_obj:
        raise HTTPException(status_code=404, detail="Run not found.")
    return {
        "run_id": run_id,
        "metrics": run_obj.aggregated_metrics,
        "dimension_scores": run_obj.dimension_scores
    }


@router.get("/runs/{run_id}/errors")
def get_run_errors(run_id: str):
    run_obj = EvaluationRunner.get_run(run_id)
    if not run_obj:
        raise HTTPException(status_code=404, detail="Run not found.")
    all_errors = []
    for cr in run_obj.case_results:
        if cr.errors_detected:
            all_errors.append({
                "case_id": cr.case_id,
                "errors": cr.errors_detected,
                "root_cause_stage": cr.root_cause_stage,
                "root_cause_description": cr.root_cause_description,
                "first_failure_detail": cr.first_failure_detail
            })
    return {"run_id": run_id, "errors_count": len(all_errors), "error_cascades": all_errors}


# --- Scientific Experiments & Ablations ---

@router.get("/experiments", response_model=List[Experiment])
def list_experiments():
    # Ensure all pre-registered critical experiments are populated
    ExperimentEngine.run_critical_experiment_1_six_layer_ablation()
    ExperimentEngine.run_critical_experiment_2_general_ai_comparison()
    ExperimentEngine.run_critical_experiment_3_version_progression()
    ExperimentEngine.run_critical_experiment_4_layer_degradation()
    ExperimentEngine.run_critical_experiment_5_source_governance()
    return ExperimentEngine.list_experiments()


@router.get("/experiments/{experiment_id}", response_model=Experiment)
def get_experiment(experiment_id: str):
    exp = ExperimentEngine.get_experiment(experiment_id)
    if not exp:
        # Check if critical experiment requested
        if experiment_id == "EXP-01-SIX-LAYER-ABLATION":
            return ExperimentEngine.run_critical_experiment_1_six_layer_ablation()
        if experiment_id == "EXP-02-GENERAL-AI-VS-ZMIE":
            return ExperimentEngine.run_critical_experiment_2_general_ai_comparison()
        raise HTTPException(status_code=404, detail="Experiment not found.")
    return exp


@router.post("/models/benchmark", response_model=Experiment)
def run_ablation_benchmark():
    """Runs Section 298 critical ablation study"""
    return ExperimentEngine.run_critical_experiment_1_six_layer_ablation()


@router.post("/models/compare", response_model=Experiment)
def run_model_comparison():
    """Runs Section 299 general AI vs ZMIE comparison"""
    return ExperimentEngine.run_critical_experiment_2_general_ai_comparison()


# --- Production Release Quality Gate ---

@router.get("/gate/status", response_model=ReleaseScorecard)
def get_release_gate_status(run_ids: Optional[str] = Query(None)):
    cand_ids = [rid.strip() for rid in run_ids.split(",")] if run_ids else []
    return ReleaseGateEngine.evaluate_release_candidate(cand_ids)
