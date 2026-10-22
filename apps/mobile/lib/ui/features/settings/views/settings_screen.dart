import 'package:flutter/material.dart';
import '../../../../data/services/zmie_api_service.dart';
import '../../../core/app_colors.dart';

class SettingsScreen extends StatefulWidget {
  final VoidCallback onThemeChanged;
  final bool isDarkMode;

  const SettingsScreen({
    super.key,
    required this.onThemeChanged,
    required this.isDarkMode,
  });

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final ZmieApiService _apiService = ZmieApiService();
  final TextEditingController _urlCtrl = TextEditingController();
  final TextEditingController _keyCtrl = TextEditingController();

  bool _isChecking = false;
  bool? _healthResult;

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final url = await _apiService.getBaseUrl();
    final key = await _apiService.getApiKey();
    setState(() {
      _urlCtrl.text = url;
      _keyCtrl.text = key;
    });
  }

  Future<void> _saveSettings() async {
    await _apiService.saveSettings(
      baseUrl: _urlCtrl.text,
      apiKey: _keyCtrl.text,
    );
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Settings saved successfully.')),
      );
    }
  }

  Future<void> _testConnection() async {
    setState(() {
      _isChecking = true;
      _healthResult = null;
    });
    await _saveSettings();
    final ok = await _apiService.checkHealth();
    setState(() {
      _isChecking = false;
      _healthResult = ok;
    });
  }

  @override
  void dispose() {
    _urlCtrl.dispose();
    _keyCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('System Settings & Connectivity'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Section: Engine Connectivity
          _buildCard(
            context,
            title: 'ZMIE Engine Backend API Gateway',
            icon: Icons.cloud_outlined,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Base API URL:',
                  style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600),
                ),
                const SizedBox(height: 6),
                TextField(
                  controller: _urlCtrl,
                  decoration: const InputDecoration(
                    hintText: 'e.g. http://127.0.0.1:8000',
                  ),
                ),
                const SizedBox(height: 12),
                const Text(
                  'API Access Key (Bearer / Header):',
                  style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600),
                ),
                const SizedBox(height: 6),
                TextField(
                  controller: _keyCtrl,
                  obscureText: true,
                  decoration: const InputDecoration(
                    hintText: 'e.g. zmie-res-key-9921',
                  ),
                ),
                const SizedBox(height: 14),
                Row(
                  children: [
                    Expanded(
                      child: ElevatedButton.icon(
                        icon: _isChecking
                            ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                            : const Icon(Icons.network_check, size: 18),
                        label: const Text('Test Connection'),
                        onPressed: _isChecking ? null : _testConnection,
                      ),
                    ),
                    const SizedBox(width: 10),
                    OutlinedButton(
                      onPressed: _saveSettings,
                      child: const Text('Save'),
                    ),
                  ],
                ),
                if (_healthResult != null) ...[
                  const SizedBox(height: 12),
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: _healthResult!
                          ? AppColors.statusGreen.withOpacity(0.12)
                          : AppColors.statusRed.withOpacity(0.12),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Row(
                      children: [
                        Icon(
                          _healthResult! ? Icons.check_circle : Icons.error_outline,
                          color: _healthResult! ? AppColors.statusGreen : AppColors.statusRed,
                          size: 18,
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            _healthResult!
                                ? 'Connected to ZMIE API Gateway (HTTP 200)'
                                : 'Connection failed. Working in local offline codex mode.',
                            style: TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              color: _healthResult! ? AppColors.statusGreen : AppColors.statusRed,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ]
              ],
            ),
          ),

          const SizedBox(height: 16),

          // Section: Appearance
          _buildCard(
            context,
            title: 'Display & Appearance',
            icon: Icons.palette_outlined,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Dark Theme Mode'),
                Switch(
                  value: widget.isDarkMode,
                  activeColor: AppColors.primaryTeal,
                  onChanged: (_) => widget.onThemeChanged(),
                ),
              ],
            ),
          ),

          const SizedBox(height: 16),

          // Section: Offline Storage
          _buildCard(
            context,
            title: 'Offline Scientific Codex',
            icon: Icons.offline_pin_outlined,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildInfoRow('Bundled Botanical Codex', '657 Monographs (Local JSON)'),
                _buildInfoRow('Pharmacopoeias', 'UPI / API / Canonical treatises'),
                _buildInfoRow('Zero Fabrication Policy', 'Strictly Enforced'),
              ],
            ),
          ),

          const SizedBox(height: 16),

          // Section: About
          _buildCard(
            context,
            title: 'About ZAYVORA HealthOS',
            icon: Icons.info_outline,
            child: const Text(
              'TriMedSearch™ (ZMIE) Mobile Edition v1.0.0\n'
              'Unified Tri-Paradigm Medical Intelligence Platform connecting Modern Biomedicine, Unani-Tibb, and Ayurveda with zero evidence fabrication and cryptographic audit trails.',
              style: TextStyle(fontSize: 12, height: 1.5, color: Colors.grey),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCard(
    BuildContext context, {
    required String title,
    required IconData icon,
    required Widget child,
  }) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isDark ? AppColors.darkCard : AppColors.lightSurface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: isDark ? AppColors.darkBorder : AppColors.lightBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, size: 18, color: AppColors.primaryTealLight),
              const SizedBox(width: 8),
              Text(
                title,
                style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
              ),
            ],
          ),
          const Divider(height: 20),
          child,
        ],
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 13, color: Colors.grey)),
          Text(value, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
