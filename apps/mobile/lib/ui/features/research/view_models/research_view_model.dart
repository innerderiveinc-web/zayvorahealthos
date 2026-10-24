import 'package:flutter/foundation.dart';
import '../../../../data/models/research_result.dart';
import '../../../../data/repositories/research_repository.dart';

enum ResearchPipelineStage {
  idle,
  decomposingPico,
  searchingCorpora,
  reactMultiHop,
  criticReflection,
  adversarialDebate,
  completed,
  error
}

class ResearchViewModel extends ChangeNotifier {
  final ResearchRepository _repository;

  ResearchViewModel({ResearchRepository? repository})
      : _repository = repository ?? ResearchRepository();

  ResearchPipelineStage _stage = ResearchPipelineStage.idle;
  bool _isLoading = false;
  ResearchResultModel? _result;
  String? _errorMessage;

  ResearchPipelineStage get stage => _stage;
  bool get isLoading => _isLoading;
  ResearchResultModel? get result => _result;
  String? get errorMessage => _errorMessage;

  String get stageLabel {
    switch (_stage) {
      case ResearchPipelineStage.idle:
        return 'Ready for PICO topic';
      case ResearchPipelineStage.decomposingPico:
        return 'Step 1/5: PICO Framework Decomposition...';
      case ResearchPipelineStage.searchingCorpora:
        return 'Step 2/5: Cross-Corpus Retrieval & Screening...';
      case ResearchPipelineStage.reactMultiHop:
        return 'Step 3/5: ReAct Multi-Hop Clue Discovery...';
      case ResearchPipelineStage.criticReflection:
        return 'Step 4/5: Critic Closed-Loop Self-Correction...';
      case ResearchPipelineStage.adversarialDebate:
        return 'Step 5/5: Adversarial Debate Consensus...';
      case ResearchPipelineStage.completed:
        return 'Synthesis Complete & Grounded';
      case ResearchPipelineStage.error:
        return 'Investigation Error';
    }
  }

  Future<void> runInvestigation(String question) async {
    final clean = question.trim();
    if (clean.isEmpty) return;

    _isLoading = true;
    _errorMessage = null;
    _stage = ResearchPipelineStage.decomposingPico;
    notifyListeners();

    try {
      // Simulate realistic stage progressions for UX responsiveness
      await Future.delayed(const Duration(milliseconds: 300));
      _stage = ResearchPipelineStage.searchingCorpora;
      notifyListeners();

      await Future.delayed(const Duration(milliseconds: 300));
      _stage = ResearchPipelineStage.reactMultiHop;
      notifyListeners();

      await Future.delayed(const Duration(milliseconds: 300));
      _stage = ResearchPipelineStage.criticReflection;
      notifyListeners();

      await Future.delayed(const Duration(milliseconds: 300));
      _stage = ResearchPipelineStage.adversarialDebate;
      notifyListeners();

      final res = await _repository.conductInvestigation(clean);
      _result = res;
      _stage = ResearchPipelineStage.completed;
    } catch (e) {
      _errorMessage = e.toString();
      _stage = ResearchPipelineStage.error;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void clear() {
    _stage = ResearchPipelineStage.idle;
    _result = null;
    _errorMessage = null;
    _isLoading = false;
    notifyListeners();
  }
}
