"""
==============================================================================
ZMIE Local Persistent Storage Engine (SQLite Fallback Engine)
==============================================================================
Provides zero-dependency, crash-resilient persistence across server restarts
when external PostgreSQL / Neo4j Docker containers are offline.
Stores:
- Audit Event Chains (HMAC Merkle proofs)
- Research Jobs & Plans (PICO, search matrices, reports)
- Verified Source Ledger entries
==============================================================================
"""

import os
import sqlite3
import json
from typing import Dict, Any, List, Optional
from datetime import datetime


class LocalPersistentStore:
    _instance: Optional["LocalPersistentStore"] = None

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            data_dir = os.path.join(base_dir, "data")
            os.makedirs(data_dir, exist_ok=True)
            self.db_path = os.path.join(data_dir, "zmie_local.db")
        else:
            self.db_path = db_path

        self._init_tables()

    @classmethod
    def get_instance(cls) -> "LocalPersistentStore":
        if cls._instance is None:
            cls._instance = LocalPersistentStore()
        return cls._instance

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_tables(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # 1. Audit Chain
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_chain (
                    event_id TEXT PRIMARY KEY,
                    actor TEXT,
                    tenant_id TEXT,
                    object_type TEXT,
                    object_id TEXT,
                    action TEXT,
                    block_hash TEXT,
                    prev_hash TEXT,
                    signature TEXT,
                    timestamp TEXT,
                    payload_json TEXT
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_tenant ON audit_chain(tenant_id)")

            # 2. Research Jobs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS research_jobs (
                    job_id TEXT PRIMARY KEY,
                    primary_question TEXT,
                    state TEXT,
                    pico_json TEXT,
                    plan_json TEXT,
                    report_json TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)

            # 3. Source Ledger
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS source_ledger (
                    identifier TEXT PRIMARY KEY,
                    registry TEXT,
                    title TEXT,
                    canonical_hash TEXT,
                    trust_tier TEXT,
                    is_authentic INTEGER,
                    payload_json TEXT,
                    last_synced_at TEXT
                )
            """)
            conn.commit()

    # --- Audit Operations ---
    def save_audit_event(self, event_dict: Dict[str, Any]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO audit_chain 
                (event_id, actor, tenant_id, object_type, object_id, action, block_hash, prev_hash, signature, timestamp, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event_dict.get("event_id"),
                event_dict.get("actor"),
                event_dict.get("tenant_id"),
                event_dict.get("object_type"),
                event_dict.get("object_id"),
                event_dict.get("action"),
                event_dict.get("block_hash"),
                event_dict.get("prev_hash"),
                event_dict.get("signature"),
                str(event_dict.get("timestamp")),
                json.dumps(event_dict, default=str)
            ))
            conn.commit()

    def load_audit_chain(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT payload_json FROM audit_chain ORDER BY rowid ASC")
            rows = cursor.fetchall()
            return [json.loads(r["payload_json"]) for r in rows]

    # --- Research Job Operations ---
    def save_research_job(self, job_id: str, question: str, state: str, job_dict: Dict[str, Any]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.utcnow().isoformat() + "Z"
            cursor.execute("""
                INSERT OR REPLACE INTO research_jobs
                (job_id, primary_question, state, plan_json, report_json, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                job_id,
                question,
                state,
                json.dumps(job_dict.get("plan", {}), default=str),
                json.dumps(job_dict.get("report", {}), default=str) if job_dict.get("report") else None,
                now
            ))
            conn.commit()

    def load_all_research_jobs(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT job_id, primary_question, state, plan_json, report_json FROM research_jobs")
            rows = cursor.fetchall()
            results = []
            for r in rows:
                results.append({
                    "job_id": r["job_id"],
                    "question": r["primary_question"],
                    "state": r["state"],
                    "plan": json.loads(r["plan_json"]) if r["plan_json"] else {},
                    "report": json.loads(r["report_json"]) if r["report_json"] else None
                })
            return results
