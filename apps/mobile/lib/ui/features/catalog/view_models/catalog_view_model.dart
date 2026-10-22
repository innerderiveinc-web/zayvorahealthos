import 'package:flutter/foundation.dart';
import '../../../../data/models/botanical_entry.dart';
import '../../../../data/repositories/botanical_repository.dart';

class CatalogViewModel extends ChangeNotifier {
  final BotanicalRepository _repository;

  CatalogViewModel({BotanicalRepository? repository})
      : _repository = repository ?? BotanicalRepository();

  List<BotanicalEntry> _entries = [];
  List<BotanicalEntry> get entries => _entries;

  List<String> _domains = [];
  List<String> get domains => _domains;

  String _searchQuery = '';
  String get searchQuery => _searchQuery;

  String? _selectedDomain;
  String? get selectedDomain => _selectedDomain;

  bool _isLoading = true;
  bool get isLoading => _isLoading;

  Future<void> init() async {
    _isLoading = true;
    notifyListeners();

    try {
      _entries = await _repository.getAllEntries();
      _domains = await _repository.getClinicalDomains();
    } catch (_) {
      _entries = [];
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> onSearchChanged(String query) async {
    _searchQuery = query;
    _applyFilters();
  }

  void onDomainSelected(String? domain) {
    if (_selectedDomain == domain) {
      _selectedDomain = null;
    } else {
      _selectedDomain = domain;
    }
    _applyFilters();
  }

  Future<void> _applyFilters() async {
    _isLoading = true;
    notifyListeners();

    try {
      final results = await _repository.searchEntries(_searchQuery);
      if (_selectedDomain != null && _selectedDomain!.isNotEmpty) {
        _entries = results.where((e) => e.clinicalDomain == _selectedDomain).toList();
      } else {
        _entries = results;
      }
    } catch (_) {
      _entries = [];
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}
