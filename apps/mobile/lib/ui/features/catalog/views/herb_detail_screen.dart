import 'package:flutter/material.dart';
import '../../../../data/models/botanical_entry.dart';
import '../../../core/app_colors.dart';

class HerbDetailScreen extends StatelessWidget {
  final BotanicalEntry entry;

  const HerbDetailScreen({super.key, required this.entry});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: Text(entry.displayName),
        actions: [
          IconButton(
            icon: const Icon(Icons.bookmark_border),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('${entry.displayName} saved to favorites')),
              );
            },
          )
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header Card
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: isDark
                      ? [AppColors.darkSurface, AppColors.darkCard]
                      : [AppColors.primaryTeal.withOpacity(0.08), Colors.white],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: isDark ? AppColors.darkBorder : AppColors.lightBorder,
                ),
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
                          color: AppColors.primaryTeal.withOpacity(0.15),
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: AppColors.primaryTeal.withOpacity(0.4)),
                        ),
                        child: Text(
                          entry.clinicalDomain,
                          style: const TextStyle(
                            color: AppColors.primaryTealLight,
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: entry.hasClinicalEvidence
                              ? AppColors.statusGreen.withOpacity(0.15)
                              : Colors.grey.withOpacity(0.15),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          entry.evidenceGrade ?? 'UNVERIFIED',
                          style: TextStyle(
                            color: entry.hasClinicalEvidence
                                ? AppColors.statusGreen
                                : Colors.grey,
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Text(
                    entry.displayName,
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 0.3,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    entry.botanicalName,
                    style: const TextStyle(
                      fontSize: 14,
                      fontStyle: FontStyle.italic,
                      color: AppColors.primaryTealLight,
                    ),
                  ),
                  if (entry.family.isNotEmpty) ...[
                    const SizedBox(height: 2),
                    Text(
                      'Family: ${entry.family}',
                      style: TextStyle(
                        fontSize: 12,
                        color: isDark ? AppColors.textDarkSecondary : AppColors.textLightSecondary,
                      ),
                    ),
                  ]
                ],
              ),
            ),

            const SizedBox(height: 20),

            // Classical Unani Mizaj & Actions
            _buildSectionCard(
              context,
              title: 'Classical Unani Framework (Mizaj & Afaal)',
              icon: Icons.auto_awesome,
              iconColor: AppColors.accentGold,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildPropertyRow('Mizaj (Temperament)', entry.unaniMizaj),
                  if (entry.unani['darja'] != null)
                    _buildPropertyRow('Darja (Intensity)', entry.unani['darja'].toString()),
                  if (entry.unaniAfaal.isNotEmpty) ...[
                    const SizedBox(height: 8),
                    const Text(
                      'Canonical Actions (Af\'aal):',
                      style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600),
                    ),
                    const SizedBox(height: 6),
                    Wrap(
                      spacing: 6,
                      runSpacing: 6,
                      children: entry.unaniAfaal.map((af) {
                        return Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: isDark ? AppColors.darkSurface : AppColors.lightCard,
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: isDark ? AppColors.darkBorder : AppColors.lightBorder),
                          ),
                          child: Text(af, style: const TextStyle(fontSize: 12)),
                        );
                      }).toList(),
                    )
                  ],
                  const SizedBox(height: 8),
                  _buildPropertyRow('Canonical Codex', entry.canonicalCodex),
                ],
              ),
            ),

            const SizedBox(height: 16),

            // Modern Pharmacological Data
            _buildSectionCard(
              context,
              title: 'Modern Pharmacology & Phytochemistry',
              icon: Icons.science_outlined,
              iconColor: AppColors.primaryTealLight,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (entry.activePhytochemicals.isNotEmpty) ...[
                    const Text(
                      'Key Phytochemical Constituents:',
                      style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600),
                    ),
                    const SizedBox(height: 6),
                    Wrap(
                      spacing: 6,
                      runSpacing: 6,
                      children: entry.activePhytochemicals.map((pc) {
                        return Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: AppColors.primaryTeal.withOpacity(0.12),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(
                            pc,
                            style: const TextStyle(
                              fontSize: 12,
                              color: AppColors.primaryTealLight,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        );
                      }).toList(),
                    ),
                    const SizedBox(height: 12),
                  ],
                  if (entry.modernPharmacology.isNotEmpty)
                    Text(
                      entry.modernPharmacology,
                      style: const TextStyle(fontSize: 13, height: 1.4),
                    ),
                  if (entry.rctCount != null && entry.rctCount! > 0) ...[
                    const SizedBox(height: 8),
                    _buildPropertyRow('Evaluated Human RCTs', '${entry.rctCount} Trials'),
                  ]
                ],
              ),
            ),

            const SizedBox(height: 16),

            // Quality & Statutory Standards
            _buildSectionCard(
              context,
              title: 'Statutory Standards & Posology',
              icon: Icons.verified_outlined,
              iconColor: AppColors.statusGreen,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (entry.partUsed.isNotEmpty)
                    _buildPropertyRow('Part Used', entry.partUsed),
                  if (entry.badraqah.isNotEmpty)
                    _buildPropertyRow('Badraqah (Anupana)', entry.badraqah),
                  if (entry.muddatTaseer.isNotEmpty)
                    _buildPropertyRow('Potency Duration', entry.muddatTaseer),
                  const SizedBox(height: 8),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: isDark ? AppColors.darkSurface : AppColors.lightCard,
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: isDark ? AppColors.darkBorder : AppColors.lightBorder),
                    ),
                    child: const Text(
                      'Clinical Note: Dosage and therapeutic regimen must be prescribed by licensed clinician in accordance with official UPI / API statutory compendia.',
                      style: TextStyle(fontSize: 12, fontStyle: FontStyle.italic),
                    ),
                  )
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionCard(
    BuildContext context, {
    required String title,
    required IconData icon,
    required Color iconColor,
    required Widget child,
  }) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Container(
      width: double.infinity,
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
              Icon(icon, size: 18, color: iconColor),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  title,
                  style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                ),
              ),
            ],
          ),
          const Divider(height: 20, thickness: 0.8),
          child,
        ],
      ),
    );
  }

  Widget _buildPropertyRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 140,
            child: Text(
              label,
              style: const TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w500,
                color: Colors.grey,
              ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600),
            ),
          ),
        ],
      ),
    );
  }
}
