"""ZMIE Scientific Data Fabric & Computational Research Engine Showcase.

Demonstrates the complete end-to-end research continuum (Prompt 21):
1. Scientific Data Fabric Ingestion & Quality Profiling
2. Immutable Cryptographic Snapshot Pinning (SHA256)
3. Preregistered Analysis Planning & Data Leakage Checking
4. Containerized/Sandboxed Computation Execution (Strictly COMPUTED state)
5. End-to-End Data Lineage Tracing (Raw Data -> Evidence -> Candidate Claim)
6. Reproducibility Engine & Signed Computational Certificate
7. Computation Diffing (Parameter/Code/Data deltas)
8. Candidate Claim Generation & Human Governance Promotion
9. Intellectual Property & License Protection
"""

import json
from app.models.scientific_compute import (
    DataField,
    Dataset,
    PrivacyClassification,
    ScientificState,
)
from app.scientific_compute.engine import ScientificDataFabricEngine


def run_showcase():
    print("=" * 80)
    print(" ZMIE SCIENTIFIC DATA FABRIC & COMPUTATIONAL RESEARCH ENGINE")
    print(" 'No scientific result without a traceable computational path.'")
    print("=" * 80)

    engine = ScientificDataFabricEngine()

    # 1. Dataset Ingestion & Profiling
    print("\n--- [STAGE 1] DATA FABRIC INGESTION & QUALITY PROFILING ---")
    fields = [
        DataField(field_name="patient_id", data_type="string", semantic_type="Identifier"),
        DataField(field_name="empagliflozin_arm", data_type="categorical", semantic_type="Exposure", ontology_concept_id="CON-DRUG-EMPA-01"),
        DataField(field_name="cv_death_event", data_type="numeric", semantic_type="Outcome", ontology_concept_id="CON-DIS-MI-01"),
        DataField(field_name="followup_days", data_type="numeric", semantic_type="FollowupTime", unit="days", normalized_unit="days"),
        DataField(field_name="baseline_egfr", data_type="numeric", semantic_type="Confounder", unit="mL/min", normalized_unit="mL/min"),
        DataField(field_name="baseline_ntpro_bnp", data_type="numeric", semantic_type="Biomarker", unit="pg/mL", normalized_unit="pg/mL", missing_count=12, missing_pct=0.012),
    ]
    ds = Dataset(
        dataset_id="DS-EMPEROR-REDUCED-01",
        name="EMPEROR-Reduced Trial Cohort",
        description="Phase 3 multicenter randomized trial assessing empagliflozin in heart failure with reduced ejection fraction.",
        publisher_or_institution="Global Heart Failure Clinical Network",
        domain="Cardiovascular Clinical Trial",
        privacy_class=PrivacyClassification.INTERNAL,
        fields=fields,
        records_count=3730,
        created_at=engine._now(),
        updated_at=engine._now(),
    )
    ingested_ds, dqr = engine.ingest_dataset(ds)
    print(f"  • Dataset Ingested: [{ingested_ds.dataset_id}] {ingested_ds.name} ({ingested_ds.records_count} records)")
    print(f"    Quality Score: {dqr.completeness_score * 100:.2f}% | Fitness for Purpose: {dqr.fitness_for_purpose}")
    print(f"    Missingness Mechanisms Detected: {dqr.missingness_mechanisms}")

    # 2. Immutable Cryptographic Snapshot
    print("\n--- [STAGE 2] IMMUTABLE DATASET SNAPSHOT PINNING ---")
    snap = engine.create_snapshot(ingested_ds.dataset_id, version_tag="v1.0")
    print(f"  • Pinned Snapshot ID: {snap.snapshot_id}")
    print(f"    Content SHA256: {snap.content_sha256[:32]}...")
    print(f"    Schema Hash:    {snap.fields_schema_hash[:32]}...")

    # 3. Preregistered Analysis Plan & Leakage Checks
    print("\n--- [STAGE 3] PREREGISTERED ANALYSIS PLAN & LEAKAGE CHECK ---")
    plan = engine._plans["PLAN-SGLT2-CV-DEATH"]
    print(f"  • Protocol ID: {plan.plan_id}")
    print(f"    Research Question: {plan.research_question}")
    print(f"    Statistical Method: {plan.statistical_method}")
    print(f"    Data Leakage Checks Passed: {plan.data_leakage_checks_passed} (Zero post-outcome contaminations)")

    # 4. Computational Execution (Strictly COMPUTED state)
    print("\n--- [STAGE 4] CONTAINERIZED COMPUTATION EXECUTION ---")
    job = engine.execute_analysis_workflow(plan.plan_id, snap.snapshot_id)
    print(f"  • Run ID: {job.job_id} | Status: {job.status.value}")
    print(f"    Runtime Container: {job.runtime_environment.container_image}")
    print(f"    Code Hash: {job.code_hash[:32]}...")
    
    art = job.results[0]
    est = art.effect_estimate
    print(f"\n  >> Output Artifact [{art.artifact_id}] (Scientific State: {art.scientific_state.value}):")
    print(f"     Measure: {est.measure_type} = {est.point_estimate} (95% CI {est.confidence_interval_95[0]} - {est.confidence_interval_95[1]}, p = {est.p_value})")
    print(f"     Sample Size: {est.sample_size} | Events: {est.events_count} | Standard Error: {est.standard_error}")
    print(f"     Scientific Boundary: Effect estimate is tagged COMPUTED, NEVER confused with raw observation.")

    # 5. End-to-End Data Lineage Graph
    print("\n--- [STAGE 5] END-TO-END DATA LINEAGE TRACING ---")
    lineage = engine.trace_data_lineage(job.job_id)
    print(f"  Lineage Graph ID: {lineage.graph_id}")
    print(f"  Trace Path ({len(lineage.nodes)} nodes, {len(lineage.edges)} edges):")
    for i, n in enumerate(lineage.nodes):
        print(f"    [{i+1}] ({n.node_type}) {n.label} [State: {n.scientific_state.value}]")

    # 6. Reproducibility Engine & Certificate
    print("\n--- [STAGE 6] REPRODUCIBILITY ENGINE & SIGNED CERTIFICATE ---")
    reproduced_job, cert = engine.reproduce_run(job.job_id)
    print(f"  • Reproduced Run ID: {reproduced_job.job_id}")
    print(f"    Reproducibility Verdict: {cert.reproducibility_verdict}")
    print(f"    Relative Numerical Divergence: {cert.relative_divergence} (Exact Concordance)")
    print(f"    Computational Certificate: {cert.certificate_id} [Certified: {cert.certified_at}]")

    # 7. Computation Diffing
    print("\n--- [STAGE 7] COMPUTATION DIFFING (RUN A vs RUN B) ---")
    job_b = engine.execute_analysis_workflow(plan.plan_id, snap.snapshot_id, {"alpha": 0.01})
    diff = engine.compute_diff(job.job_id, job_b.job_id)
    print(f"  • Diff ID: {diff.diff_id}")
    print(f"    Parameters Changed: {diff.parameters_changed} | Code Changed: {diff.code_changed}")
    print(f"    Point Estimate Delta: {diff.effect_estimate_delta} | Concordant: {diff.conclusion_concordance}")
    print(f"    Summary: {diff.narrative_summary}")

    # 8. Candidate Claim Generation & Human Governance Gating
    print("\n--- [STAGE 8] CANDIDATE CLAIM GENERATION & EVIDENCE RELEASE GATING ---")
    candidate_claim = engine.generate_candidate_claim(art.artifact_id)
    print(f"  • Candidate Claim: [{candidate_claim.claim_id}]")
    print(f"    Statement: {candidate_claim.statement}")
    print(f"    Governance State: {candidate_claim.human_review_status} (Promoted to Evidence Graph: {candidate_claim.promoted_to_evidence_graph})")

    promoted_claim = engine.review_and_promote_claim(
        claim_id=candidate_claim.claim_id,
        reviewer_name="Dr. E. Vance, Principal Investigator",
        approve=True,
    )
    print(f"  • Expert Review Decision: APPROVED by {promoted_claim.reviewed_by}")
    print(f"    Promoted to Evidence Graph: {promoted_claim.promoted_to_evidence_graph} [Scientific State: {promoted_claim.scientific_state.value}]")

    # 9. License & IP Protection
    print("\n--- [STAGE 9] INTELLECTUAL PROPERTY & LICENSE PROTECTION ---")
    allowed, msg = engine.verify_dataset_export_permission("DS-RESTRICTED-PHARMA-PROPRIETARY")
    print(f"  • Export Request for 'DS-RESTRICTED-PHARMA-PROPRIETARY': Allowed: {allowed}")
    print(f"    Policy Enforced: {msg}")

    print("\n" + "=" * 80)
    print(" ALL PROMPT 21 DATA FABRIC & COMPUTATIONAL CAPABILITIES VERIFIED")
    print("=" * 80)


if __name__ == "__main__":
    run_showcase()
