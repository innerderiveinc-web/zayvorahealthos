"""
ZMIE Infrastructure Layer: Database, Cryptographic Ledger, and Operational Telemetry
"""
from app.db.sqlite import SQLiteDatabase
from app.core.audit import AuditTrailDispatcher, get_audit_dispatcher
