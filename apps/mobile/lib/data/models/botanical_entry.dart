class BotanicalEntry {
  final String key;
  final String botanicalName;
  final String family;
  final List<String> commonNames;
  final String clinicalDomain;
  final List<String> activePhytochemicals;
  final String modernPharmacology;
  final String? evidenceGrade;
  final int? rctCount;
  final String partUsed;
  final Map<String, dynamic> unani;
  final Map<String, dynamic> ayurveda;
  final Map<String, dynamic> languageSynonyms;
  final String mahiyat;
  final String badraqah;
  final String muddatTaseer;

  BotanicalEntry({
    required this.key,
    required this.botanicalName,
    required this.family,
    required this.commonNames,
    required this.clinicalDomain,
    required this.activePhytochemicals,
    required this.modernPharmacology,
    this.evidenceGrade,
    this.rctCount,
    required this.partUsed,
    required this.unani,
    required this.ayurveda,
    required this.languageSynonyms,
    required this.mahiyat,
    required this.badraqah,
    required this.muddatTaseer,
  });

  factory BotanicalEntry.fromJson(Map<String, dynamic> json) {
    List<String> parseStringList(dynamic val) {
      if (val is List) {
        return val.map((e) => e.toString()).toList();
      } else if (val is String && val.isNotEmpty) {
        return [val];
      }
      return [];
    }

    return BotanicalEntry(
      key: json['key']?.toString() ?? '',
      botanicalName: json['botanical_name']?.toString() ?? 'Botanical Specimen',
      family: json['family']?.toString() ?? '',
      commonNames: parseStringList(json['common_names']),
      clinicalDomain: json['clinical_domain']?.toString() ?? 'General Pharmacopoeia',
      activePhytochemicals: parseStringList(json['active_phytochemicals']),
      modernPharmacology: json['modern_pharmacology']?.toString() ?? '',
      evidenceGrade: json['evidence_grade']?.toString(),
      rctCount: json['rct_count'] is int ? json['rct_count'] as int : null,
      partUsed: json['part_used']?.toString() ?? '',
      unani: json['unani'] is Map<String, dynamic> ? json['unani'] as Map<String, dynamic> : {},
      ayurveda: json['ayurveda'] is Map<String, dynamic> ? json['ayurveda'] as Map<String, dynamic> : {},
      languageSynonyms: json['language_synonyms'] is Map<String, dynamic> ? json['language_synonyms'] as Map<String, dynamic> : {},
      mahiyat: json['mahiyat']?.toString() ?? '',
      badraqah: json['badraqah']?.toString() ?? '',
      muddatTaseer: json['muddat_taseer']?.toString() ?? '',
    );
  }

  String get displayName {
    if (commonNames.isNotEmpty) return commonNames.first;
    if (key.isNotEmpty) return key[0].toUpperCase() + key.substring(1);
    return botanicalName;
  }

  String get unaniMizaj {
    return unani['mizaj']?.toString() ?? 'Not specified in codex';
  }

  String get canonicalCodex {
    return unani['canonical_codex']?.toString() ?? 'Statutory Ayurvedic / Unani Pharmacopoeia (API/UPI)';
  }

  List<String> get unaniAfaal {
    final af = unani['afaal'];
    if (af is List) return af.map((e) => e.toString()).toList();
    return [];
  }

  bool get hasClinicalEvidence => evidenceGrade != null && evidenceGrade!.isNotEmpty;
}
