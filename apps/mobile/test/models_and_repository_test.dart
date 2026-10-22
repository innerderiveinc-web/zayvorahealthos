import 'package:flutter_test/flutter_test.dart';
import 'package:zayvora_healthos_mobile/data/models/botanical_entry.dart';
import 'package:zayvora_healthos_mobile/data/models/interaction_result.dart';

void main() {
  group('BotanicalEntry Model Tests', () {
    test('parses json correctly and handles missing fields gracefully', () {
      final json = {
        'key': 'berberine',
        'botanical_name': 'Berberis aristata DC.',
        'family': 'Berberidaceae',
        'common_names': ['Tree Turmeric', 'Darhald'],
        'clinical_domain': 'Endocrinology & Metabolic',
        'active_phytochemicals': ['Berberine', 'Berbamine'],
        'modern_pharmacology': 'AMPK activator',
        'evidence_grade': 'Level 1a (Strong RCT Evidence)',
        'rct_count': 14,
        'unani': {
          'mizaj': 'Hot 2° / Dry 2°',
          'afaal': ['Musaffi-e-Dam', 'Daf-e-Taffun'],
        }
      };

      final entry = BotanicalEntry.fromJson(json);

      expect(entry.key, 'berberine');
      expect(entry.displayName, 'Tree Turmeric');
      expect(entry.botanicalName, 'Berberis aristata DC.');
      expect(entry.family, 'Berberidaceae');
      expect(entry.activePhytochemicals.length, 2);
      expect(entry.hasClinicalEvidence, isTrue);
      expect(entry.unaniMizaj, 'Hot 2° / Dry 2°');
      expect(entry.unaniAfaal.length, 2);
    });

    test('handles unverified entry with null clinical evidence', () {
      final json = {
        'key': 'unverified_herb',
        'botanical_name': 'Herba test',
        'common_names': ['Test Herb'],
      };

      final entry = BotanicalEntry.fromJson(json);

      expect(entry.key, 'unverified_herb');
      expect(entry.displayName, 'Test Herb');
      expect(entry.evidenceGrade, isNull);
      expect(entry.hasClinicalEvidence, isFalse);
    });
  });

  group('InteractionResult Model Tests', () {
    test('identifies critical hazard appropriately', () {
      final res = InteractionResult(
        hazardScore: 85,
        triageLevel: 'CRITICAL_LETHALITY_ALERT',
        detectedClashes: ['Warfarin CYP clash'],
        actionableDirectives: ['Mandatory INR monitoring'],
        cryptographicProvenance: 'sha256:abc',
        timestamp: '2026-10-22T00:00:00Z',
      );

      expect(res.isCritical, isTrue);
      expect(res.isSafe, isFalse);
      expect(res.detectedClashes.length, 1);
    });

    test('identifies safe interaction appropriately', () {
      final res = InteractionResult(
        hazardScore: 15,
        triageLevel: 'MONITORED_CO_PRESCRIPTION',
        detectedClashes: [],
        actionableDirectives: ['Standard observation'],
        cryptographicProvenance: 'local',
        timestamp: '2026-10-22T00:00:00Z',
      );

      expect(res.isSafe, isTrue);
      expect(res.isCritical, isFalse);
    });
  });
}
