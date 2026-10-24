import '../models/research_result.dart';
import '../services/zmie_api_service.dart';

class ResearchRepository {
  final ZmieApiService _apiService;

  ResearchRepository({ZmieApiService? apiService})
      : _apiService = apiService ?? ZmieApiService();

  Future<ResearchResultModel> conductInvestigation(String question) async {
    return await _apiService.executeResearchJob(question);
  }
}
