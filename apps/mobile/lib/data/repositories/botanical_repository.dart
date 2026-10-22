import '../models/botanical_entry.dart';
import '../services/local_catalog_service.dart';

class BotanicalRepository {
  final LocalCatalogService _catalogService;

  BotanicalRepository({LocalCatalogService? catalogService})
      : _catalogService = catalogService ?? LocalCatalogService();

  Future<List<BotanicalEntry>> getAllEntries() async {
    return _catalogService.loadCatalog();
  }

  Future<List<BotanicalEntry>> searchEntries(String query) async {
    return _catalogService.search(query);
  }

  Future<BotanicalEntry?> getEntryByKey(String key) async {
    return _catalogService.getByKey(key);
  }

  Future<List<String>> getClinicalDomains() async {
    final entries = await getAllEntries();
    final domains = entries
        .map((e) => e.clinicalDomain)
        .where((d) => d.isNotEmpty)
        .toSet()
        .toList();
    domains.sort();
    return domains;
  }
}
