import '../models/interaction_result.dart';
import '../services/zmie_api_service.dart';

class SafetyRepository {
  final ZmieApiService _apiService;

  SafetyRepository({ZmieApiService? apiService})
      : _apiService = apiService ?? ZmieApiService();

  Future<InteractionResult> evaluateInteractions({
    required List<String> drugs,
    required List<String> herbs,
    int age = 65,
    int egfr = 60,
  }) async {
    return _apiService.simulateSafety(
      drugs: drugs,
      herbs: herbs,
      age: age,
      egfr: egfr,
    );
  }

  Future<bool> isBackendConnected() async {
    return _apiService.checkHealth();
  }
}
