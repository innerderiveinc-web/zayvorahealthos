# ZAYVORA HealthOS — Mobile Edition (Flutter)

A clean, offline-first cross-platform mobile application (iOS & Android) for **ZAYVORA HealthOS & ZMIE Tri-Paradigm Medical Intelligence**.

---

## Key Capabilities

1. **Complete 657-Entry Botanical Codex (Offline-First)**:
   - Instant 0ms search across English common names, Latin binomials, botanical families, and Urdu/Arabic/Persian synonyms.
   - Comprehensive monograph views: Classical Unani Mizaj (Temperament), Canonical Actions (*Af'aal*), statutory pharmacopoeial standards (UPI / API), parts used, active phytochemicals, and modern pharmacology.
   - Strictly enforces the **Zero Evidence Fabrication** policy: entries without modern controlled trial data are honestly marked `UNVERIFIED`.

2. **Herb-Drug Interaction & Lethality Guard**:
   - Interactive safety triage simulator for polypharmacy regimens.
   - Combines allopathic prescriptions (e.g., Warfarin, Digoxin, Metformin, Lisinopril) with botanical formulations (e.g., Berberine, St. John's Wort, Ashwagandha, Ginkgo, Licorice).
   - Real-time patient demographic adjustment: Geriatric age modeling and renal clearance ($eGFR$).
   - Detects CYP450 enzyme clashes, P-glycoprotein induction, and outputs actionable clinical directives with Therapeutic Drug Monitoring (TDM) protocols.

3. **Hybrid Engine Connectivity & Settings**:
   - Directly interfaces with the ZMIE FastAPI backend (`/health`, `/v1/safety/simulate`, `/v1/search`, `/v1/research/jobs`).
   - Configurable API Gateway URL and authenticated `X-API-Key` with real-time ping diagnostics.
   - Seamless offline fallback: operates with full local safety intelligence when external internet or backend server is unreachable.
   - Native Material 3 Dark & Light themes with clinical teal/emerald design palette.

---

## Architectural Structure

Follows the official Flutter Layered MVVM Architecture:

```text
apps/mobile/
├── assets/
│   └── catalog_seed.json             # Bundled 657-botanical local codex
├── lib/
│   ├── main.dart                     # App entrypoint & MultiProvider setup
│   ├── data/
│   │   ├── models/                   # BotanicalEntry, InteractionResult
│   │   ├── services/                 # LocalCatalogService, ZmieApiService
│   │   └── repositories/             # BotanicalRepository, SafetyRepository
│   └── ui/
│       ├── core/                     # AppColors, AppTheme (Material 3 Dark/Light)
│       └── features/
│           ├── home/views/           # HomeScreen with bottom navigation bar
│           ├── catalog/              # CatalogScreen, HerbDetailScreen, CatalogViewModel
│           ├── safety/               # SafetyScreen, SafetyViewModel
│           └── settings/             # SettingsScreen (API & connectivity config)
└── test/                             # Unit tests for models, repositories & viewmodels
```

---

## Prerequisites & Launching

### Run with Flutter
```bash
cd apps/mobile

# Install dependencies
flutter pub get

# Run on connected iOS device or simulator
flutter run -d ios

# Run on connected Android device or emulator
flutter run -d android

# Run on Web (Chrome)
flutter run -d chrome
```

### Run Automated Tests
```bash
cd apps/mobile
flutter test
```
