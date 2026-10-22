import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;
import '../models/botanical_entry.dart';

class LocalCatalogService {
  List<BotanicalEntry>? _cachedEntries;

  Future<List<BotanicalEntry>> loadCatalog() async {
    if (_cachedEntries != null && _cachedEntries!.isNotEmpty) {
      return _cachedEntries!;
    }

    try {
      final jsonString = await rootBundle.loadString('assets/catalog_seed.json');
      final Map<String, dynamic> data = json.decode(jsonString);
      final List<dynamic> rawEntries = data['entries'] as List<dynamic>? ?? [];

      _cachedEntries = rawEntries
          .map((item) => BotanicalEntry.fromJson(item as Map<String, dynamic>))
          .toList();

      return _cachedEntries!;
    } catch (e) {
      // Graceful fallback if asset load fails
      return [];
    }
  }

  Future<List<BotanicalEntry>> search(String query) async {
    final all = await loadCatalog();
    if (query.trim().isEmpty) return all;

    final q = query.toLowerCase().trim();
    return all.where((entry) {
      if (entry.key.toLowerCase().contains(q)) return true;
      if (entry.botanicalName.toLowerCase().contains(q)) return true;
      if (entry.family.toLowerCase().contains(q)) return true;
      if (entry.clinicalDomain.toLowerCase().contains(q)) return true;
      for (final cn in entry.commonNames) {
        if (cn.toLowerCase().contains(q)) return true;
      }
      for (final syn in entry.languageSynonyms.values) {
        if (syn.toString().toLowerCase().contains(q)) return true;
      }
      return false;
    }).toList();
  }

  Future<BotanicalEntry?> getByKey(String key) async {
    final all = await loadCatalog();
    try {
      return all.firstWhere((e) => e.key.toLowerCase() == key.toLowerCase());
    } catch (_) {
      return null;
    }
  }
}
