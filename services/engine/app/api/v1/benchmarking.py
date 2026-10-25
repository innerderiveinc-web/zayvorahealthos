"""
ZMIE Scientific Benchmarking & Validation FastAPI Router
Scientific Benchmarking REST Gateway
"""

from typing import List, Dict, Optional, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.benchmarking.engine import ScientificBenchmarkingEngine
from app.benchmarking.models import (
    BenchmarkDatasetType,
    BenchmarkRunReport,
    ScientificValidationReport,
)

router = APIRouter(prefix="/benchmarking", tags=["Scientific Benchmarking & Validation"])

# Global singleton
_benchmarking_engine = ScientificBenchmarkingEngine()


def get_benchmarking_engine() -> ScientificBenchmarkingEngine:
    return _benchmarking_engine


class RunBenchmarkRequest(BaseModel):
    dataset: BenchmarkDatasetType = BenchmarkDatasetType.NEGATIVE_CONTROLS


@router.post("/run", response_model=BenchmarkRunReport)
def run_benchmark(
    req: RunBenchmarkRequest,
    engine: ScientificBenchmarkingEngine = Depends(get_benchmarking_engine)
):
    """
    Executes standardized scientific benchmark suite across golden test batteries.
    """
    return engine.run_benchmark_suite(dataset=req.dataset)


@router.get("/reports", response_model=List[BenchmarkRunReport])
def list_reports(
    engine: ScientificBenchmarkingEngine = Depends(get_benchmarking_engine)
):
    """
    Lists all executed scientific benchmark validation reports.
    """
    return engine.list_run_reports()


@router.get("/reports/{run_id}", response_model=BenchmarkRunReport)
def get_report(
    run_id: str,
    engine: ScientificBenchmarkingEngine = Depends(get_benchmarking_engine)
):
    """
    Retrieves specific benchmark run report by ID.
    """
    report = engine.get_run_report(run_id)
    if not report:
        raise HTTPException(status_code=404, detail="Benchmark run report not found")
    return report


@router.post("/validation-report", response_model=ScientificValidationReport)
def generate_validation_report(
    engine: ScientificBenchmarkingEngine = Depends(get_benchmarking_engine)
):
    """
    Generates comprehensive scientific validation report across all 24 dimensions,
    evaluating 12 golden batteries and producing a signed Go / No-Go matrix.
    """
    return engine.generate_scientific_validation_report()


@router.get("/validation-reports", response_model=List[ScientificValidationReport])
def list_validation_reports(
    engine: ScientificBenchmarkingEngine = Depends(get_benchmarking_engine)
):
    """
    Lists all comprehensive scientific validation reports.
    """
    return engine.list_validation_reports()


@router.get("/validation-reports/{report_id}", response_model=ScientificValidationReport)
def get_validation_report(
    report_id: str,
    engine: ScientificBenchmarkingEngine = Depends(get_benchmarking_engine)
):
    """
    Retrieves specific comprehensive scientific validation report by ID.
    """
    report = engine.get_validation_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Scientific validation report not found")
    return report


@router.get("/go-no-go-matrix", response_model=Dict[str, str])
def get_go_no_go_matrix(
    engine: ScientificBenchmarkingEngine = Depends(get_benchmarking_engine)
):
    """
    Returns the latest production Go / No-Go decision matrix.
    """
    reports = engine.list_validation_reports()
    if reports:
        return reports[-1].go_no_go_matrix
    # Generate on the fly if none exists
    new_report = engine.generate_scientific_validation_report()
    return new_report.go_no_go_matrix


@router.get("/datasets", response_model=List[str])
def list_datasets():
    """
    Lists all available golden benchmark datasets.
    """
    return [d.value for d in BenchmarkDatasetType]
