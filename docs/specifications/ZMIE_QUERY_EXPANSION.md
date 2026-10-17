# ZMIE CONTROLLED QUERY EXPANSION SPECIFICATION
## Synonyms, Multilingual Transliterations & Traditional Epistemic Boundaries

---

### 1. Controlled Expansion Principles (Section 9)

Query expansion in ZMIE is strictly governed by ontological dictionaries to prevent semantic drift:
- Expands exact scientific synonyms, abbreviations, and international nonproprietary names (INN).
- Does not expand unrelated concepts merely because they co-occur or appear semantically close.

---

### 2. Traditional Medicine Expansions (Section 10)

Traditional terms are expanded across classical transliterations and historical orthographies while strictly preserving their epistemic system boundaries:

```text
┌─────────────────┬──────────────────────────────────────────────────────┐
│ Concept Term    │ Expanded Canonical Forms                             │
├─────────────────┼──────────────────────────────────────────────────────┤
│ Mizaj           │ Mizaj, Mizāj, مزاج, Mijaz, Temperament, Damwi,       │
│                 │ Safrawi, Balghami, Sawdawi                           │
├─────────────────┼──────────────────────────────────────────────────────┤
│ Darhald         │ Darhald, Daruharidra, Berberis aristata, Rasaut,     │
│                 │ Indian Barberry                                      │
├─────────────────┼──────────────────────────────────────────────────────┤
│ Jatharagni      │ Jatharagni, Agni, Mandagni, Pachaka Pitta, Digestive │
│                 │ Fire, Ama                                            │
├─────────────────┼──────────────────────────────────────────────────────┤
│ Pi Qi Xu        │ Pi Qi Xu, 脾气虚, Spleen Qi Deficiency, Spleen-      │
│                 │ Stomach Rotting and Ripening                         │
└─────────────────┴──────────────────────────────────────────────────────┘
```
- Boundaries: Expanding *Mizaj* includes Unani humoral subclasses, but does not conflate it with Ayurvedic *Tridosha* unless an explicit cross-system comparison query is invoked.
