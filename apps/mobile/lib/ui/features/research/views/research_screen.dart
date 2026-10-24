import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../core/app_colors.dart';
import '../view_models/research_view_model.dart';
import '../../../../data/models/research_result.dart';

class ResearchScreen extends StatefulWidget {
  const ResearchScreen({super.key});

  @override
  State<ResearchScreen> createState() => _ResearchScreenState();
}

class _ResearchScreenState extends State<ResearchScreen> {
  final TextEditingController _controller = TextEditingController();

  final List<String> _presets = [
    'Berberine in Type 2 Diabetes Glycemic Control',
    'Ashwagandha in Anxiety & Cortisol Modulation',
    'Majun Dabeed-ul-Ward Polyherbal Safety',
    'Curcumin & Piperine Anti-Inflammatory Synergy'
  ];

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _submit(String q) {
    if (q.trim().isEmpty) return;
    _controller.text = q;
    FocusScope.of(context).unfocus();
    context.read<ResearchViewModel>().runInvestigation(q);
  }

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<ResearchViewModel>();
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Row(
          children: [
            Icon(Icons.biotech, color: AppColors.primaryTealLight),
            SizedBox(width: 8),
            Text('Agentic Research Studio'),
          ],
        ),
        actions: [
          if (vm.result != null)
            IconButton(
              icon: const Icon(Icons.refresh),
              tooltip: 'Reset',
              onPressed: () {
                _controller.clear();
                vm.clear();
              },
            ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Search Input Card
            Card(
              color: isDark ? AppColors.darkCard : AppColors.lightCard,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                side: BorderSide(color: isDark ? AppColors.darkBorder : AppColors.lightBorder),
              ),
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                child: Row(
                  children: [
                    const Icon(Icons.psychology, color: AppColors.primaryTealLight),
                    const SizedBox(width: 8),
                    Expanded(
                      child: TextField(
                        controller: _controller,
                        decoration: const InputDecoration(
                          hintText: 'Enter clinical or polyherbal PICO topic...',
                          border: InputBorder.none,
                        ),
                        onSubmitted: _submit,
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.send, color: AppColors.primaryTealLight),
                      onPressed: () => _submit(_controller.text),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 10),

            // Presets
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: _presets.map((p) {
                return ActionChip(
                  label: Text(p, style: const TextStyle(fontSize: 11)),
                  backgroundColor: isDark ? AppColors.darkSurface : AppColors.lightSurface,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                  onPressed: () => _submit(p),
                );
              }).toList(),
            ),
            const SizedBox(height: 20),

            // Pipeline Progress Section
            if (vm.isLoading) ...[
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: isDark ? AppColors.darkSurface : AppColors.lightSurface,
                  borderRadius: BorderRadius.circular(12),
                  border: BorderSide(color: AppColors.primaryTeal.withOpacity(0.4)),
                ),
                child: Column(
                  children: [
                    const LinearProgressIndicator(color: AppColors.primaryTealLight),
                    const SizedBox(height: 12),
                    Text(
                      vm.stageLabel,
                      style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.primaryTealLight),
                    ),
                    const SizedBox(height: 6),
                    const Text(
                      'Zero-Fabrication Critic & ReAct Multi-Hop Loop Active',
                      style: TextStyle(fontSize: 12, color: AppColors.textDarkSecondary),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),
            ],

            // Error display
            if (vm.errorMessage != null) ...[
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppColors.statusRed.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(8),
                  border: BorderSide(color: AppColors.statusRed),
                ),
                child: Text('Error: ${vm.errorMessage}', style: const TextStyle(color: AppColors.statusRed)),
              ),
              const SizedBox(height: 20),
            ],

            // Completed Result
            if (vm.result != null) ...[
              _buildResultCard(vm.result!, isDark),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildResultCard(ResearchResultModel res, bool isDark) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Header & GRADE Badge
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            color: isDark ? AppColors.darkCard : AppColors.lightCard,
            borderRadius: BorderRadius.circular(12),
            border: BorderSide(color: isDark ? AppColors.darkBorder : AppColors.lightBorder),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Chip(
                    label: Text(
                      'GRADE: ${res.gradeCertainty}',
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: Colors.white),
                    ),
                    backgroundColor: _gradeColor(res.gradeCertainty),
                  ),
                  Chip(
                    label: Text(
                      res.clinicalPosture,
                      style: const TextStyle(fontSize: 11, color: Colors.white),
                    ),
                    backgroundColor: AppColors.primaryTealDark,
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Text(
                res.title,
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
              ),
              const SizedBox(height: 6),
              Text(
                res.executiveSummary,
                style: TextStyle(
                  fontSize: 13,
                  color: isDark ? AppColors.textDarkSecondary : AppColors.textLightSecondary,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 14),

        // Adversarial Debate Card
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            color: isDark ? AppColors.darkSurface : AppColors.lightSurface,
            borderRadius: BorderRadius.circular(12),
            border: BorderSide(color: AppColors.accentGold.withOpacity(0.5)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Row(
                children: [
                  Icon(Icons.gavel, color: AppColors.accentGold, size: 18),
                  SizedBox(width: 6),
                  Text(
                    'Adversarial Consensus (Advocate vs. Skeptic)',
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: AppColors.accentGold),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Text(
                res.debateConsensus,
                style: const TextStyle(fontSize: 12),
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  Icon(Icons.auto_fix_high, size: 14, color: AppColors.primaryTealLight),
                  const SizedBox(width: 4),
                  Text(
                    'Critic Auto-Repaired Assertions: ${res.autoRepairedCount}',
                    style: const TextStyle(fontSize: 11, color: AppColors.primaryTealLight),
                  ),
                  const Spacer(),
                  Text(
                    'ReAct Tools: ${res.reactToolsInvoked.length}',
                    style: const TextStyle(fontSize: 11, color: AppColors.textDarkSecondary),
                  ),
                ],
              ),
            ],
          ),
        ),
        const SizedBox(height: 14),

        // Grounded Assertions
        const Text(
          'Grounded Medical Assertions:',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
        ),
        const SizedBox(height: 8),

        ...res.assertions.map((ast) {
          return Card(
            margin: const EdgeInsets.only(bottom: 8),
            color: isDark ? AppColors.darkCard : AppColors.lightCard,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
              side: BorderSide(color: isDark ? AppColors.darkBorder : AppColors.lightBorder),
            ),
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(
                          color: ast.epistemicStatus == 'CONFIRMED'
                              ? AppColors.statusGreen.withOpacity(0.2)
                              : AppColors.statusOrange.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(
                          ast.epistemicStatus,
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            color: ast.epistemicStatus == 'CONFIRMED'
                                ? AppColors.statusGreen
                                : AppColors.statusOrange,
                          ),
                        ),
                      ),
                      const Spacer(),
                      Text(
                        ast.citations.join(', '),
                        style: const TextStyle(fontSize: 10, color: AppColors.textDarkSecondary),
                      ),
                    ],
                  ),
                  const SizedBox(height: 6),
                  Text(
                    ast.statement,
                    style: const TextStyle(fontSize: 13),
                  ),
                ],
              ),
            ),
          );
        }).toList(),
      ],
    );
  }

  Color _gradeColor(String grade) {
    switch (grade.toUpperCase()) {
      case 'HIGH':
        return AppColors.statusGreen;
      case 'MODERATE':
        return AppColors.primaryTeal;
      case 'LOW':
        return AppColors.statusOrange;
      default:
        return AppColors.statusRed;
    }
  }
}
