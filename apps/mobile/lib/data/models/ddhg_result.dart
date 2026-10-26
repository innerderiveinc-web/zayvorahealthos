class DDHGAlertMobile {
  final String alertId;
  final String severity;
  final String interactionType;
  final List<String> participatingAgents;
  final String mechanism;
  final String clinicalRisk;
  final String actionableDirective;
  final String? fdaBoxedWarning;

  DDHGAlertMobile({
    required this.alertId,
    required this.severity,
    required this.interactionType,
    required this.participatingAgents,
    required this.mechanism,
    required this.clinicalRisk,
    required this.actionableDirective,
    this.fdaBoxedWarning,
  });

  factory DDHGAlertMobile.fromJson(Map<String, dynamic> json) {
    final rawAgents = (json['participating_agents'] as List<dynamic>?) ?? [];
    return DDHGAlertMobile(
      alertId: json['alert_id'] ?? '',
      severity: json['severity'] ?? 'MODERATE_MONITOR',
      interactionType: json['interaction_type'] ?? 'DRUG_HERB',
      participatingAgents: rawAgents.map((e) => e.toString()).toList(),
      mechanism: json['biochemical_mechanism'] ?? '',
      clinicalRisk: json['clinical_risk'] ?? '',
      actionableDirective: json['actionable_directive'] ?? '',
      fdaBoxedWarning: json['fda_boxed_warning_reference'],
    );
  }
}

class DDHGMobileResult {
  final String overallStatus;
  final int criticalCount;
  final int majorCount;
  final int moderateCount;
  final List<DDHGAlertMobile> alerts;
  final String physicianSummary;

  DDHGMobileResult({
    required this.overallStatus,
    required this.criticalCount,
    required this.majorCount,
    required this.moderateCount,
    required this.alerts,
    required this.physicianSummary,
  });

  factory DDHGMobileResult.fromJson(Map<String, dynamic> json) {
    final rawAlerts = (json['alerts'] as List<dynamic>?) ?? [];
    return DDHGMobileResult(
      overallStatus: json['overall_status'] ?? 'CLEAR_TO_PROCEED',
      criticalCount: json['critical_alerts_count'] ?? 0,
      majorCount: json['major_alerts_count'] ?? 0,
      moderateCount: json['moderate_alerts_count'] ?? 0,
      alerts: rawAlerts
          .map((a) => DDHGAlertMobile.fromJson(a as Map<String, dynamic>))
          .toList(),
      physicianSummary: json['physician_summary'] ?? '',
    );
  }

  factory DDHGMobileResult.offlineFallback() {
    return DDHGMobileResult(
      overallStatus: 'BLOCKED_CONTRAINDICATION',
      criticalCount: 1,
      majorCount: 1,
      moderateCount: 0,
      alerts: [
        DDHGAlertMobile(
          alertId: 'ALERT-DG-CYP2C19-CLOPIDOGREL',
          severity: 'CRITICAL_CONTRAINDICATION',
          interactionType: 'DRUG_GENE',
          participatingAgents: ['CYP2C19 (*2/*2)', 'Clopidogrel'],
          mechanism: 'Impaired prodrug bioactivation via CYP2C19 loss of function.',
          clinicalRisk: 'Lack of antiplatelet protection and high arterial thrombosis risk.',
          actionableDirective: 'Switch to Prasugrel or Ticagrelor.',
          fdaBoxedWarning: 'FDA Black Box Warning on CYP2C19 Poor Metabolizers.',
        )
      ],
      physicianSummary: 'Critical pharmacogenomic contraindication identified.',
    );
  }
}
