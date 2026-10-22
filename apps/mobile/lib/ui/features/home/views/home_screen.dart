import 'package:flutter/material.dart';
import '../../catalog/views/catalog_screen.dart';
import '../../safety/views/safety_screen.dart';
import '../../settings/views/settings_screen.dart';
import '../../../core/app_colors.dart';

class HomeScreen extends StatefulWidget {
  final VoidCallback onThemeChanged;
  final bool isDarkMode;

  const HomeScreen({
    super.key,
    required this.onThemeChanged,
    required this.isDarkMode,
  });

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _currentIndex = 0;

  @override
  Widget build(BuildContext context) {
    final List<Widget> screens = [
      const CatalogScreen(),
      const SafetyScreen(),
      SettingsScreen(
        onThemeChanged: widget.onThemeChanged,
        isDarkMode: widget.isDarkMode,
      ),
    ];

    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: screens,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (idx) {
          setState(() {
            _currentIndex = idx;
          });
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.eco_outlined),
            selectedIcon: Icon(Icons.eco, color: AppColors.primaryTealLight),
            label: 'Codex (657)',
          ),
          NavigationDestination(
            icon: Icon(Icons.shield_outlined),
            selectedIcon: Icon(Icons.shield, color: AppColors.primaryTealLight),
            label: 'Safety Guard',
          ),
          NavigationDestination(
            icon: Icon(Icons.tune_outlined),
            selectedIcon: Icon(Icons.tune, color: AppColors.primaryTealLight),
            label: 'Settings',
          ),
        ],
      ),
    );
  }
}
