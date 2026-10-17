# ZMIE SOURCE SECURITY & ACCESS CONTROL SPECIFICATION
## Zero-Trust Connector Security, Secret Management & Multi-Tenant Isolation

---

### 1. Zero-Trust Network & API Security

1. **Connector Isolation**:
   - Ingestion workers run within isolated network zones.
   - External provider traffic is restricted to HTTPS (TLS 1.3) egress through monitored egress gateways.
2. **Secret Management**:
   - Provider API keys (e.g. OpenAlex mailto tokens, PubMed E-utilities keys, institutional publisher bearer tokens) are managed via encrypted environment variables or HashiCorp Vault.
   - Keys are rotated on a 90-day cycle and never logged to stdout or transcript files.
3. **SSRF Prevention**:
   - Outward DOI / URL resolvers strictly validate destination IP addresses, blocking loopback (`127.0.0.1`), private RFC 1918 subnets (`10.0.0.0/8`, `192.168.0.0/16`, `172.16.0.0/12`), and link-local addresses.

---

### 2. Multi-Tenant Cryptographic Isolation

ZMIE serves hospitals, academic institutions, and sovereign ministries under strict multi-tenant boundaries:
- **Tenant Scope Enforcement**: Every internal query, index partition, and retrieval operation is tagged with `tenant_id`.
- **Zero Cross-Tenant Leakage**:
  - Proprietary institutional documents (e.g. private clinical trial data under Class A contracts) are encrypted using tenant-specific KMS keys.
  - Public biomedical graphs are read-only and shared across tenants, but private annotations, custom taxonomies, and research projects are strictly segregated.
  - Acceptance tests actively verify that cross-tenant queries return zero records (`assert len(tenant_b_records) == 0`).

---

### 3. Immutable Security Audit Trails

All acquisition activities generate structured audit logs stored in the PostgreSQL `audit_events` ledger:
```json
{
  "event_id": "AUD-2026-X091",
  "timestamp": "2026-10-03T18:30:00Z",
  "actor": "IngestionWorker-04",
  "action": "DOCUMENT_ACQUIRED",
  "source_id": "SRC-EPMC-001",
  "document_id": "PMID:38291040",
  "sha256": "8a7f1...e99",
  "license_class": "CLASS_B",
  "quarantine_enforced": false
}
```
Logs are append-only and cryptographically chained to prevent retroactive tampering.
