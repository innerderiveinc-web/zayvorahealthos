# ZMIE MULTILINGUAL & CROSS-LANGUAGE MODEL
## Polyglot Medical Acquisition, Script Normalization & Terminology Alignment

---

### 1. Supported Linguistic & Epistemic Traditions

ZMIE ingests medical knowledge natively across seven primary linguistic and scholarly traditions:

| Medical Tradition | Source Languages | Primary Scripts | Transliteration Standard | Canonical Corpus |
|---|---|---|---|---|
| **Modern Biomedicine** | English, Latin | Latin script | N/A | PubMed, Cochrane, FDA |
| **Unani Tibb** | Arabic, Persian, Urdu | Arabic / Nastaliq script | DIN 31635 / IJMES | *Al-Qanun fi al-Tibb*, NFUM, CCRUM |
| **Ayurveda** | Sanskrit, Hindi | Devanagari script | ISO 15919 / IAST | *Charaka Samhita*, *Sushruta*, API |
| **Siddha** | Tamil | Tamil script | ISO 15919 | *Agathiyar Gunavagadam*, Siddha Formulary |
| **TCM** | Classical & Modern Chinese | Simplified / Traditional Hanzi | Pinyin with tones | *Huangdi Neijing*, *Shennong Bencaojing* |
| **Sowa-Rigpa** | Classical Tibetan | Tibetan script | Wylie transliteration | *Gyushi (Four Tantras)* |

---

### 2. Script Normalization Standards

1. **Unicode Canonical Normalization**: All incoming text streams are converted to Unicode NFC (Normalization Form C) to resolve combining diacritics and composite characters.
2. **Arabic/Persian/Urdu Nastaliq Handling**:
   - Diacritics (*tashkeel/harakat*) are retained in canonical codex storage but stripped for lexical index searches.
   - Character normalization maps Persian/Urdu variants (e.g. `ک` $\leftrightarrow$ `ك`, `ی` $\leftrightarrow$ `ي`, `ہ` $\leftrightarrow$ `ه`) to canonical search equivalents.
3. **Indic / Devanagari / Tamil Handling**:
   - Virama and conjunct ligatures are normalized to standard Unicode sequences.
   - IAST (*International Alphabet of Sanskrit Transliteration*) is stored as a first-class synonym alongside original Devanagari text.

---

### 3. Cross-Language Entity Resolution

Medical entities maintain a multilingual descriptor record:

```json
{
  "concept_id": "MED-CONCEPT-BERBERIS",
  "latin_botanical": "Berberis aristata DC.",
  "modern_english": "Indian Barberry / Tree Turmeric",
  "unani_arabic_persian": {
    "original_script": "دار ہلد",
    "transliteration_ijmes": "Darhald",
    "canonical_part": "Zarishk (Berries), Rasaut (Extract)"
  },
  "ayurveda_sanskrit": {
    "original_script": "दारुहरिद्रा",
    "transliteration_iast": "Dāruharidrā",
    "guna_karma": ["Tikta", "Kashaya", "Ushna", "Kaphapittashamaka"]
  },
  "tcm_chinese": {
    "hanzi": "黄连 (analogue)",
    "pinyin": "Huánglián",
    "action": "Clear heat, dry dampness"
  }
}
```
*Notice: Different systems identify botanical and pharmacological identities without forcing their diagnostic frameworks into an artificial equivalence.*
