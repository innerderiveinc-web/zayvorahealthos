import 'package:flutter_test/flutter_test.dart';
import 'package:zayvora_healthos_mobile/data/models/research_result.dart';
import 'package:zayvora_healthos_mobile/data/repositories/research_repository.dart';
import 'package:zayvora_healthos_mobile/ui/features/research/view_models/research_view_model.dart';

class MockResearchRepository implements ResearchRepository {
  @override
  Future<ResearchResultModel> conductInvestigation(String question) async {
    return ResearchResultModel(
      jobId: 'job-mock-123',
      title: 'Mock Investigation: $question',
      question: question,
      executiveSummary: 'Controlled trial synthesis conducted under zero-fabrication invariants.',
      state: 'COMPLETED',
      gradeCertainty: 'HIGH',
      clinicalPosture: 'ENDORSED_MONITORED',
      debateConsensus: 'Robust consensus reached by Arbiter agent.',
      autoRepairedCount: 2,
      reactToolsInvoked: ['tool_pubmed_search', 'tool_codex_lookup'],
      assertions: [
        ResearchAssertionModel(
          assertionId: 'ast-1',
          statement: 'Active botanical constituents modulate target glycemic biomarkers.',
          epistemicStatus: 'CONFIRMED',
          citations: ['PMID:20010020'],
        )
      ],
      isOfflineGenerated: false,
    );
  }
}

void main() {
  group('ResearchViewModel Tests', () {
    test('Initial stage is idle with null result', () {
      final vm = ResearchViewModel(repository: MockResearchRepository());
      expect(vm.stage, ResearchPipelineStage.idle);
      expect(vm.result, isNull);
      expect(vm.isLoading, isFalse);
    });

    test('runInvestigation cycles through stages and completes', () async {
      final vm = ResearchViewModel(repository: MockResearchRepository());
      final future = vm.runInvestigation('Berberine in Type 2 Diabetes');

      await future;

      expect(vm.stage, ResearchPipelineStage.completed);
      expect(vm.result, isNotNull);
      expect(vm.result!.gradeCertainty, 'HIGH');
      expect(vm.result!.autoRepairedCount, 2);
      expect(vm.result!.assertions.length, 1);
      expect(vm.result!.assertions.first.epistemicStatus, 'CONFIRMED');
    });

    test('clear resets state to idle', () async {
      final vm = ResearchViewModel(repository: MockResearchRepository());
      await vm.runInvestigation('Test');
      expect(vm.result, isNotNull);

      vm.clear();
      expect(vm.stage, ResearchPipelineStage.idle);
      expect(vm.result, isNull);
    });
  });
}
