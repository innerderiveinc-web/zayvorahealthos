# ZMIE GRAPH SECURITY & TENANT ISOLATION SPECIFICATION
## Graph Permissions, Private Research Layers & Safety Firewalls

---

### 1. Multi-Tenant Graph Layering (Sections 60, 61)

The ZMIE graph enforces strict hierarchical isolation across four visibility tiers:

```text
┌────────────────────────────────────────────────────────┐
│ 1. GLOBAL CANONICAL GRAPH (Public, Governed, Sovereign)│
├────────────────────────────────────────────────────────┤
│ 2. INSTITUTIONAL GRAPH (Hospital/Enterprise Licensed)  │
├────────────────────────────────────────────────────────┤
│ 3. PROJECT RESEARCH GRAPH (Collaborative Team Space)   │
├────────────────────────────────────────────────────────┤
│ 4. PERSONAL RESEARCH NOTES (Private to Single User)    │
└────────────────────────────────────────────────────────┘
```

---

### 2. Zero Cross-Tenant Traversal Leakage

1. **Partition Filtering**:
   - Every Cypher / SQL graph query automatically injects tenant constraints:
     $$\text{WHERE } (\text{node.tenant\_id} = \text{session.tenant\_id} \lor \text{node.is\_public} = \text{true})$$
2. **AI Synthesis Quarantine**:
   - Private institutional clinical trial data is strictly prohibited from entering shared global LLM caches or public search indexes.
3. **RBAC Permission Matrix**:
   - Capabilities (`view`, `traverse`, `export`, `annotate`, `create_mapping`, `approve_mapping`, `publish`, `delete`) are enforced at the API gateway layer via cryptographically signed JWT scopes.

---

### 3. Graph Safety Firewall (Section 90)

Before exposing graph relations to automated clinical decision support or AI synthesizers, the `GraphSafetyFirewall`:
- Intercepts and blocks relations marked as `RETRACTED`.
- Enforces warning headers on high-consequence edges (`CONTRAINDICATED_IN`, `INTERACTS_WITH`).
- Rejects unverified computational inferences from being reported as clinical facts.
