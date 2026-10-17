# ZMIE SOURCE CONNECTOR SPECIFICATION
## Pluggable Data Acquisition Contract & Operational Protocols

---

### 1. Abstract Connector Interface (`BaseSourceConnector`)

All ingestion adapters across biomedical literature, clinical registries, guideline bodies, and traditional codices inherit from the `BaseSourceConnector` contract in `app.ingestion.connectors.base`:

```python
class BaseSourceConnector(ABC):
    @abstractmethod
    async def discover(self, query: str, limit: int = 10, **kwargs) -> List[Dict[str, Any]]: ...

    @abstractmethod
    async def identify(self, identifier: str) -> Optional[Dict[str, Any]]: ...

    @abstractmethod
    async def fetch_metadata(self, identifier: str) -> Optional[Dict[str, Any]]: ...

    @abstractmethod
    async def fetch_document(self, identifier: str) -> Optional[Dict[str, Any]]: ...

    @abstractmethod
    async def fetch_updates(self, since: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]: ...

    def check_access(self, identifier: str) -> bool: ...

    def check_license(self, raw_license: Optional[str], is_oa: bool = False, full_text_contract: bool = False) -> LicenseClass: ...

    @abstractmethod
    def normalize(self, raw_record: Dict[str, Any]) -> Dict[str, Any]: ...

    def report_status(self) -> Dict[str, Any]: ...
```

---

### 2. Connector Implementations

#### A. OpenAlex Connector (`OpenAlexConnector`)
- **Source ID**: `SRC-OPENALEX-001`
- **Authority Tier**: `Tier D` (Scholarly Bibliographic Graph)
- **API Endpoint**: `https://api.openalex.org/works`
- **Capabilities**: Full-text inverted index reconstruction, citation count extraction, topic concept mapping, DOI resolution.
- **Licensing Handling**: Resolves `open_access.oa_status` and primary location license tags. Quarantines non-OA full-text into Class C.

#### B. Europe PMC Connector (`EuropePMCConnector`)
- **Source ID**: `SRC-EPMC-001`
- **Authority Tier**: `Tier B` (National / International Biomedical Archive)
- **API Endpoint**: `https://www.ebi.ac.uk/europepmc/webservices/rest`
- **Capabilities**: PMID/PMCID/DOI resolution, structured XML parsing, retraction status monitoring (`hasRetraction == 'Y'`), grant and funder tracking.

#### C. AYUSH Traditional Research Connector (`AYUSHResearchConnector`)
- **Source ID**: `SRC-AYUSH-IN-001`
- **Authority Tier**: `Tier A` / `Tier E` (Statutory Ayush Registry & Classical Codices)
- **Capabilities**: Structured codex monographs (Unani *Al-Qanun fi al-Tibb*, NFUM, Ayurveda *Charaka Samhita*, API), clinical research institute paper normalization (CCRIMH, CCRUM, CCRAS).

#### D. Clinical Trials Connector (`ClinicalTrialsConnector`)
- **Source ID**: `SRC-CLINICALTRIALS-US-001`
- **Authority Tier**: `Tier B` (US National Institutes of Health / NLM)
- **API Endpoint**: `https://clinicaltrials.gov/api/v2/studies`
- **Capabilities**: Interventional and observational trial protocols, recruitment status, Phase 1-4 classification, PICO intervention and primary outcome mapping.

---

### 3. Resilience, Rate Limiting & Circuit Breaking

1. **Exponential Backoff**:
   - Initial interval: 500ms
   - Factor: 2.0
   - Maximum retries: 3
   - Maximum interval: 10s
2. **Circuit Breaker**:
   - Threshold: 5 consecutive connection failures or 50% error rate over 60 seconds.
   - Action: Transitions connector status to `UNAVAILABLE`, switches discovery to local cached or sovereign replica mirrors, emits alert to telemetry bus.
3. **Graceful Offline Fallback**:
   - When running in an isolated or sandboxed network, connectors gracefully fallback to synthetic mock verification records without throwing unhandled fatal exceptions.
