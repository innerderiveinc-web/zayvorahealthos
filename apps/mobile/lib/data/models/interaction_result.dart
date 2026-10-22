class InteractionResult {
  final int hazardScore;
  final String triageLevel;
  final List<String> detectedClashes;
  final List<String> actionableDirectives;
  final String cryptographicProvenance;
  final String timestamp;

  InteractionResult({
    required this.hazardScore,
    required this.triageLevel,
    required this.detectedClashes,
    required this.actionableDirectives,
    required this.cryptographicProvenance,
    required this.timestamp,
  });

  factory InteractionResult.fromJson(Map<String, dynamic> json) {
    List<String> parseList(dynamic val) {
      if (val is List) return val.map((e) => e.toString()).toList();
      return [];
    }

    return InteractionResult(
      hazardScore: json['hazard_score'] is int ? json['hazard_score'] as int : 0,
      triageLevel: json['triage_level']?.toString() ?? 'MONITORED_CO_PRESCRIPTION',
      detectedClashes: parseList(json['detected_clashes']),
      actionableDirectives: parseList(json['actionable_directives']),
      cryptographicProvenance: json['cryptographic_provenance']?.toString() ?? '',
      timestamp: json['timestamp']?.toString() ?? DateTime.now().toIso8601String(),
    );
  }

  bool get isCritical => triageLevel.contains('CRITICAL') || hazardScore >= 70;
  bool get isModerate => triageLevel.contains('MODERATE') || (hazardScore >= 40 && hazardScore < 70);
  bool get isSafe => hazardScore < 40;
}
