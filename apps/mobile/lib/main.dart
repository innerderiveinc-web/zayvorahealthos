import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'ui/core/app_theme.dart';
import 'ui/features/catalog/view_models/catalog_view_model.dart';
import 'ui/features/safety/view_models/safety_view_model.dart';
import 'ui/features/research/view_models/research_view_model.dart';
import 'ui/features/home/views/home_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const ZayvoraHealthOsApp());
}

class ZayvoraHealthOsApp extends StatefulWidget {
  const ZayvoraHealthOsApp({super.key});

  @override
  State<ZayvoraHealthOsApp> createState() => _ZayvoraHealthOsAppState();
}

class _ZayvoraHealthOsAppState extends State<ZayvoraHealthOsApp> {
  bool _isDarkMode = true;

  void _toggleTheme() {
    setState(() {
      _isDarkMode = !_isDarkMode;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => CatalogViewModel()),
        ChangeNotifierProvider(create: (_) => SafetyViewModel()),
        ChangeNotifierProvider(create: (_) => ResearchViewModel()),
      ],
      child: MaterialApp(
        title: 'ZAYVORA HealthOS',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        themeMode: _isDarkMode ? ThemeMode.dark : ThemeMode.light,
        home: HomeScreen(
          onThemeChanged: _toggleTheme,
          isDarkMode: _isDarkMode,
        ),
      ),
    );
  }
}
