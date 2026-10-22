import 'package:flutter/foundation.dart';
import '../../../../data/models/interaction_result.dart';
import '../../../../data/repositories/safety_repository.dart';

class SafetyViewModel extends ChangeNotifier {
  final SafetyRepository _repository;

  SafetyViewModel({SafetyRepository? repository})
      : _repository = repository ?? SafetyRepository();

  final List<String> _selectedDrugs = ['Warfarin'];
  List<String> get selectedDrugs => List.unmodifiable(_selectedDrugs);

  final List<String> _selectedHerbs = ['Berberine'];
  List<String> get selectedHerbs => List.unmodifiable(_selectedHerbs);

  int _patientAge = 68;
  int get patientAge => _patientAge;

  int _patientEgfr = 55;
  int get patientEgfr => _patientEgfr;

  InteractionResult? _result;
  InteractionResult? get result => _result;

  bool _isEvaluating = false;
  bool get isEvaluating => _isEvaluating;

  bool _isOnline = false;
  bool get isOnline => _isOnline;

  Future<void> checkConnection() async {
    _isOnline = await _repository.isBackendConnected();
    notifyListeners();
  }

  void addDrug(String drug) {
    final d = drug.trim();
    if (d.isNotEmpty && !_selectedDrugs.contains(d)) {
      _selectedDrugs.add(d);
      notifyListeners();
    }
  }

  void removeDrug(String drug) {
    _selectedDrugs.remove(drug);
    notifyListeners();
  }

  void addHerb(String herb) {
    final h = herb.trim();
    if (h.isNotEmpty && !_selectedHerbs.contains(h)) {
      _selectedHerbs.add(h);
      notifyListeners();
    }
  }

  void removeHerb(String herb) {
    _selectedHerbs.remove(herb);
    notifyListeners();
  }

  void updateAge(int age) {
    _patientAge = age;
    notifyListeners();
  }

  void updateEgfr(int egfr) {
    _patientEgfr = egfr;
    notifyListeners();
  }

  Future<void> evaluate() async {
    if (_selectedDrugs.isEmpty && _selectedHerbs.isEmpty) return;

    _isEvaluating = true;
    notifyListeners();

    try {
      _result = await _repository.evaluateInteractions(
        drugs: _selectedDrugs,
        herbs: _selectedHerbs,
        age: _patientAge,
        egfr: _patientEgfr,
      );
    } catch (_) {
      _result = null;
    } finally {
      _isEvaluating = false;
      notifyListeners();
    }
  }
}
