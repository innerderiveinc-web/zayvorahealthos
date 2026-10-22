import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../view_models/safety_view_model.dart';
import '../../../core/app_colors.dart';

class SafetyScreen extends StatefulWidget {
  const SafetyScreen({super.key});

  @override
  State<SafetyScreen> createState() => _SafetyScreenState();
}

class _SafetyScreenState extends State<SafetyScreen> {
  final TextEditingController _drugInputCtrl = TextEditingController();
  final TextEditingController _herbInputCtrl = TextEditingController();

  final List<String> _quickDrugs = ['Warfarin', 'Metformin', 'Lisinopril', 'Digoxin', 'Atorvastatin', 'Aspirin'];
  final List<String> _quickHerbs = ['Berberine', "St. John's Wort", 'Ashwagandha', 'Ginkgo biloba', 'Licorice', 'Garlic'];

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<SafetyViewModel>().checkConnection();
    });
  }

  @override
  void dispose() {
    _drugInputCtrl.dispose();
    _herbInputCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<SafetyViewModel>();
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Herb-Drug Interaction Guard'),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16),
            child: Row(
              children: [
                Container(
                  width: 8,
                  height: 8,
                  decoration: BoxDecoration(
                    color: vm.isOnline ? AppColors.statusGreen : AppColors.statusOrange,
                    shape: BoxShape.circle,
                  ),
                ),
                const SizedBox(width: 6),
                Text(
                  vm.isOnline ? 'Online Engine' : 'Offline Mode',
                  style: const TextStyle(fontSize: 12),
                ),
              ],
            ),
          )
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Section 1: Allopathic Rx Drugs
            const Text(
              '1. Prescribed Allopathic Medications',
              style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                ...vm.selectedDrugs.map((d) {
                  return Chip(
                    label: Text(d),
                    deleteIcon: const Icon(Icons.close, size: 16),
                    onDeleted: () => vm.removeDrug(d),
                    backgroundColor: AppColors.primaryTeal.withOpacity(0.15),
                    labelStyle: const TextStyle(fontWeight: FontWeight.w600),
                  );
                }),
              ],
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _drugInputCtrl,
                    decoration: InputDecoration(
                      hintText: 'Add Rx drug (e.g. Warfarin)...',
                      isDense: true,
                      suffixIcon: IconButton(
                        icon: const Icon(Icons.add),
                        onPressed: () {
                          if (_drugInputCtrl.text.isNotEmpty) {
                            vm.addDrug(_drugInputCtrl.text);
                            _drugInputCtrl.clear();
                          }
                        },
                      ),
                    ),
                    onSubmitted: (val) {
                      if (val.isNotEmpty) {
                        vm.addDrug(val);
                        _drugInputCtrl.clear();
                      }
                    },
                  ),
                ),
              ],
            ),
            const SizedBox(height: 6),
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: _quickDrugs.map((q) {
                  return Padding(
                    padding: const EdgeInsets.only(right: 6),
                    child: ActionChip(
                      label: Text('+ $q', style: const TextStyle(fontSize: 11)),
                      onPressed: () => vm.addDrug(q),
                    ),
                  );
                }).toList(),
              ),
            ),

            const SizedBox(height: 20),

            // Section 2: Botanical Formulations
            const Text(
              '2. Botanical / Herbal Co-Prescriptions',
              style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                ...vm.selectedHerbs.map((h) {
                  return Chip(
                    label: Text(h),
                    deleteIcon: const Icon(Icons.close, size: 16),
                    onDeleted: () => vm.removeHerb(h),
                    backgroundColor: AppColors.accentGold.withOpacity(0.15),
                    labelStyle: const TextStyle(fontWeight: FontWeight.w600),
                  );
                }),
              ],
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _herbInputCtrl,
                    decoration: InputDecoration(
                      hintText: 'Add herb (e.g. Berberine)...',
                      isDense: true,
                      suffixIcon: IconButton(
                        icon: const Icon(Icons.add),
                        onPressed: () {
                          if (_herbInputCtrl.text.isNotEmpty) {
                            vm.addHerb(_herbInputCtrl.text);
                            _herbInputCtrl.clear();
                          }
                        },
                      ),
                    ),
                    onSubmitted: (val) {
                      if (val.isNotEmpty) {
                        vm.addHerb(val);
                        _herbInputCtrl.clear();
                      }
                    },
                  ),
                ),
              ],
            ),
            const SizedBox(height: 6),
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: _quickHerbs.map((q) {
                  return Padding(
                    padding: const EdgeInsets.only(right: 6),
                    child: ActionChip(
                      label: Text('+ $q', style: const TextStyle(fontSize: 11)),
                      onPressed: () => vm.addHerb(q),
                    ),
                  );
                }).toList(),
              ),
            ),

            const SizedBox(height: 20),

            // Section 3: Patient Demographics (Age / eGFR)
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      '3. Patient Physiological Factors',
                      style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Patient Age: ${vm.patientAge} years'),
                        Text(
                          vm.patientAge >= 65 ? 'Geriatric Risk Tier' : 'Adult Tier',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                            color: vm.patientAge >= 65 ? AppColors.statusOrange : AppColors.statusGreen,
                          ),
                        ),
                      ],
                    ),
                    Slider(
                      value: vm.patientAge.toDouble(),
                      min: 18,
                      max: 95,
                      divisions: 77,
                      activeColor: AppColors.primaryTeal,
                      onChanged: (val) => vm.updateAge(val.toInt()),
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Renal Function (eGFR): ${vm.patientEgfr} mL/min'),
                        Text(
                          vm.patientEgfr < 60 ? 'Renal Impairment' : 'Normal Renal',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                            color: vm.patientEgfr < 60 ? AppColors.statusRed : AppColors.statusGreen,
                          ),
                        ),
                      ],
                    ),
                    Slider(
                      value: vm.patientEgfr.toDouble(),
                      min: 15,
                      max: 120,
                      divisions: 105,
                      activeColor: AppColors.primaryTeal,
                      onChanged: (val) => vm.updateEgfr(val.toInt()),
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 20),

            // Run Simulation Button
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton.icon(
                icon: vm.isEvaluating
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                    : const Icon(Icons.shield_outlined),
                label: Text(
                  vm.isEvaluating ? 'Simulating Pharmacokinetics...' : 'Evaluate Herb-Drug Interaction Hazard',
                  style: const TextStyle(fontSize: 15),
                ),
                onPressed: vm.isEvaluating ? null : vm.evaluate,
              ),
            ),

            const SizedBox(height: 24),

            // Simulation Results
            if (vm.result != null) ...[
              _buildResultCard(context, vm.result!),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildResultCard(BuildContext context, dynamic res) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isCritical = res.isCritical;
    final isModerate = res.isModerate;

    final Color badgeColor = isCritical
        ? AppColors.statusRed
        : isModerate
            ? AppColors.statusOrange
            : AppColors.statusGreen;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: isDark ? AppColors.darkCard : AppColors.lightSurface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: badgeColor, width: 1.5),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: badgeColor.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  res.triageLevel,
                  style: TextStyle(
                    color: badgeColor,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              Text(
                'Hazard Score: ${res.hazardScore}/100',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  color: badgeColor,
                ),
              ),
            ],
          ),
          const Divider(height: 24),
          if (res.detectedClashes.isNotEmpty) ...[
            const Text(
              'Identified Pharmacokinetic / Pharmacodynamic Clashes:',
              style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 6),
            ...res.detectedClashes.map((c) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 2),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('• ', style: TextStyle(color: AppColors.statusRed, fontWeight: FontWeight.bold)),
                      Expanded(child: Text(c, style: const TextStyle(fontSize: 13))),
                    ],
                  ),
                )),
            const SizedBox(height: 12),
          ],
          if (res.actionableDirectives.isNotEmpty) ...[
            const Text(
              'Clinical Prescribing Directives & TDM Protocols:',
              style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 6),
            ...res.actionableDirectives.map((d) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 2),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('✓ ', style: TextStyle(color: AppColors.primaryTealLight, fontWeight: FontWeight.bold)),
                      Expanded(child: Text(d, style: const TextStyle(fontSize: 13))),
                    ],
                  ),
                )),
          ],
        ],
      ),
    );
  }
}
