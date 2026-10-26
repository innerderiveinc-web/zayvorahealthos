import 'package:flutter_test/flutter_test.dart';
import 'package:zayvora_healthos_mobile/data/models/meta_synthesis_result.dart';
import 'package:zayvora_healthos_mobile/data/models/ddhg_result.dart';
import 'package:zayvora_healthos_mobile/data/models/hybrid_search_result.dart';
import 'package:zayvora_healthos_mobile/data/models/prisma_result.dart';

void main() {
  group('MetaSynthesisMobileResult Model Tests', () {
    test('parses meta synthesis JSON correctly', () {
      final json = {
        'query': 'Berberine for Glycemic Control',
        'meta_summary': {
          'num_studies': 4,
          'total_participants': 312,
          'pooled_effect': -0.73,
          'ci_lower': -0.92,
          'ci_upper': -0.54,
          'i_squared_pct': 16.4,
          'cochran_q': 3.59,
          'grade_certainty': 'HIGH (⊕⊕⊕⊕)',
          'forest_plot_svg': '<svg viewBox="0 0 760 280"></svg>',
        },
        'clinical_interpretation': 'Significant HbA1c reduction demonstrated.',
      };

      final model = MetaSynthesisMobileResult.fromJson(json);

      expect(model.query, 'Berberine for Glycemic Control');
      expect(model.numStudies, 4);
      expect(model.totalParticipants, 312);
      expect(model.pooledEffect, -0.73);
      expect(model.ciLower, -0.92);
      expect(model.ciUpper, -0.54);
      expect(model.iSquaredPct, 16.4);
      expect(model.gradeCertainty, 'HIGH (⊕⊕⊕⊕)');
      expect(model.forestPlotSvg, contains('<svg'));
    });

    test('offline fallback constructs valid clinical values', () {
      final fallback = MetaSynthesisMobileResult.offlineFallback('Curcumin arthritis');

      expect(fallback.query, 'Curcumin arthritis');
      expect(fallback.numStudies, greaterThan(0));
      expect(fallback.totalParticipants, greaterThan(0));
      expect(fallback.gradeCertainty, isNotEmpty);
    });
  });

  group('DDHGMobileResult Model Tests', () {
    test('parses critical DDHG triad alerts from JSON correctly', () {
      final json = {
        'overall_status': 'BLOCKED_CONTRAINDICATION',
        'critical_alerts_count': 1,
        'major_alerts_count': 1,
        'moderate_alerts_count': 0,
        'alerts': [
          {
            'alert_id': 'ALERT-TRIAD-WARFARIN-STJOHNS-CYP2C9',
            'severity': 'CRITICAL_CONTRAINDICATION',
            'interaction_type': 'DRUG_HERB_GENE_TRIAD',
            'participating_agents': ['Warfarin', 'St. John\'s Wort', 'CYP2C9 (*3/*3)'],
            'biochemical_mechanism': 'Catastrophic dual-vector kinetic clash.',
            'clinical_risk': 'Severe therapeutic failure or fatal hemorrhage.',
            'actionable_directive': 'Avoid concurrent St. John\'s Wort.',
            'fda_boxed_warning_reference': 'FDA Boxed Warning: Bleeding Hazard.',
          }
        ],
        'physician_summary': 'Pharmacogenomic and botanical contraindication identified.',
      };

      final result = DDHGMobileResult.fromJson(json);

      expect(result.overallStatus, 'BLOCKED_CONTRAINDICATION');
      expect(result.criticalCount, 1);
      expect(result.alerts.length, 1);

      final alert = result.alerts.first;
      expect(alert.alertId, 'ALERT-TRIAD-WARFARIN-STJOHNS-CYP2C9');
      expect(alert.severity, 'CRITICAL_CONTRAINDICATION');
      expect(alert.participatingAgents.length, 3);
      expect(alert.fdaBoxedWarning, contains('FDA Boxed Warning'));
    });

    test('offline fallback creates valid default safety object', () {
      final fallback = DDHGMobileResult.offlineFallback();

      expect(fallback.overallStatus, 'BLOCKED_CONTRAINDICATION');
      expect(fallback.criticalCount, 1);
      expect(fallback.alerts.first.interactionType, 'DRUG_GENE');
    });
  });

  group('HybridSearchResultMobile Model Tests', () {
    test('parses 3-tier hybrid search response with RRF scores', () {
      final json = {
        'query': 'berberine insulin resistance',
        'fusion_algorithm': 'Weighted Reciprocal Rank Fusion (k=60)',
        'total_results': 1,
        'results': [
          {
            'document_id': 'PMID:18442638',
            'title': 'Efficacy of Berberine in Type 2 Diabetes',
            'snippet': 'Randomized trial of berberine...',
            'source_organization': 'PubMed',
            'authority_tier': 'Tier B',
            'evidence_level': 'E6_controlled_clinical_evidence',
            'study_type': 'RCT',
            'final_composite_score': 0.94,
            'channel_scores': {
              'bm25': 3.5,
              'neural_vector': 0.88,
              'causal_graph': 1.0,
              'rrf_fusion': 0.045,
            },
            'mesh_terms': ['Berberine', 'Diabetes Mellitus, Type 2'],
            'causal_paths': ['Berberine -> AMPK -> Glucose'],
            'why_this_result': 'Strong multi-channel consensus',
          }
        ],
        'mesh_expansion': {
          'expanded_terms': ['berberine', 'daruharidra', 't2dm'],
        }
      };

      final result = HybridSearchResultMobile.fromJson(json);

      expect(result.query, 'berberine insulin resistance');
      expect(result.totalResults, 1);
      expect(result.results.length, 1);

      final item = result.results.first;
      expect(item.documentId, 'PMID:18442638');
      expect(item.bm25Score, 3.5);
      expect(item.vectorScore, 0.88);
      expect(item.graphScore, 1.0);
      expect(item.rrfScore, 0.045);
      expect(result.expandedMeSHTerms, contains('daruharidra'));
    });
  });

  group('PRISMAReviewMobileResult Model Tests', () {
    test('parses PRISMA 2020 review model correctly', () {
      final json = {
        'review_id': 'PRISMA-TEST-001',
        'review_report': {
          'title': 'Systematic Review of Botanical Interventions',
          'research_question': 'Is Berberine effective for T2DM?',
          'flow_counts': {
            'records_identified': 120,
            'duplicates_removed': 20,
            'records_screened': 100,
            'records_excluded': 70,
            'reports_sought_retrieval': 30,
            'reports_not_retrieved': 10,
            'studies_included_in_synthesis': 8,
          },
          'checklist': List.filled(27, {'item': '1a', 'status': 'REPORTED'}),
        },
        'flow_diagram_svg': '<svg viewBox="0 0 760 480"></svg>',
        'bibtex_export': '@article{test_review,\n  title={Test}\n}',
      };

      final model = PRISMAReviewMobileResult.fromJson(json);

      expect(model.reviewId, 'PRISMA-TEST-001');
      expect(model.recordsIdentified, 120);
      expect(model.duplicatesRemoved, 20);
      expect(model.recordsScreened, 100);
      expect(model.recordsExcluded, 70);
      expect(model.reportsAssessed, 30);
      expect(model.reportsExcluded, 10);
      expect(model.studiesIncluded, 8);
      expect(model.checklistItemsCount, 27);
      expect(model.bibtexContent, contains('@article'));
    });
  });
}
