import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/interaction_result.dart';

class ZmieApiService {
  static const String defaultBaseUrl = 'http://127.0.0.1:8000';
  static const String defaultApiKey = 'zmie-res-key-9921';

  Future<String> getBaseUrl() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('zmie_api_base_url') ?? defaultBaseUrl;
  }

  Future<String> getApiKey() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('zmie_api_key') ?? defaultApiKey;
  }

  Future<void> saveSettings({required String baseUrl, required String apiKey}) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('zmie_api_base_url', baseUrl.trim().replaceAll(RegExp(r'/+$'), ''));
    await prefs.setString('zmie_api_key', apiKey.trim());
  }

  Map<String, String> _buildHeaders(String apiKey) {
    return {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-API-Key': apiKey,
    };
  }

  Future<bool> checkHealth() async {
    try {
      final baseUrl = await getBaseUrl();
      final uri = Uri.parse('$baseUrl/health');
      final res = await http.get(uri).timeout(const Duration(seconds: 4));
      return res.statusCode == 200;
    } catch (_) {
      return false;
    }
  }

  Future<InteractionResult> simulateSafety({
    required List<String> drugs,
    required List<String> herbs,
    int age = 65,
    int egfr = 60,
  }) async {
    final baseUrl = await getBaseUrl();
    final apiKey = await getApiKey();
    final uri = Uri.parse('$baseUrl/v1/safety/simulate');

    final payload = {
      'drugs': drugs,
      'herbs': herbs,
      'patient_factors': {
        'age': age,
        'eGFR': egfr,
      }
    };

    try {
      final res = await http.post(
        uri,
        headers: _buildHeaders(apiKey),
        body: json.encode(payload),
      ).timeout(const Duration(seconds: 8));

      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        return InteractionResult.fromJson(data);
      } else {
        throw Exception('API returned status code ${res.statusCode}: ${res.body}');
      }
    } catch (e) {
      // Offline fallback safety assessment
      return _generateOfflineSafetySimulation(drugs, herbs);
    }
  }

  InteractionResult _generateOfflineSafetySimulation(List<String> drugs, List<String> herbs) {
    final hasWarfarin = drugs.any((d) => d.toLowerCase().contains('warfarin'));
    final hasStJohns = herbs.any((h) => h.toLowerCase().contains('st. john') || h.toLowerCase().contains('hypericum'));
    final hasBerberine = herbs.any((h) => h.toLowerCase().contains('berberine'));
    final hasDigoxin = drugs.any((d) => d.toLowerCase().contains('digoxin'));

    int score = 20;
    String triage = 'MONITORED_CO_PRESCRIPTION';
    List<String> clashes = [];
    List<String> directives = [];

    if (hasWarfarin && (hasStJohns || hasBerberine)) {
      score = 85;
      triage = 'CRITICAL_LETHALITY_ALERT';
      clashes.add('CYP3A4 / CYP2C9 Competitive Inhibition & Warfarin Clearance Reduction');
      directives.add('Mandatory serial INR monitoring. High pharmacokinetic bleed hazard.');
    } else if (hasDigoxin && hasStJohns) {
      score = 75;
      triage = 'HIGH_PHARMACOKINETIC_HAZARD';
      clashes.add('P-glycoprotein (ABCB1) Induction reducing cardiac glycoside bioavailability');
      directives.add('Monitor serum digoxin concentrations closely.');
    } else {
      directives.add('Standard clinical surveillance. Screen baseline renal/hepatic biomarkers.');
    }

    return InteractionResult(
      hazardScore: score,
      triageLevel: triage,
      detectedClashes: clashes,
      actionableDirectives: directives,
      cryptographicProvenance: 'offline-local-engine',
      timestamp: DateTime.now().toIso8601String(),
    );
  }
}
