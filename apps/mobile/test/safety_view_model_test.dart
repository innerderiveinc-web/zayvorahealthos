import 'package:flutter_test/flutter_test.dart';
import 'package:zayvora_healthos_mobile/ui/features/safety/view_models/safety_view_model.dart';

void main() {
  group('SafetyViewModel State Management Tests', () {
    test('initializes with default safety parameters', () {
      final vm = SafetyViewModel();

      expect(vm.selectedDrugs, contains('Warfarin'));
      expect(vm.selectedHerbs, contains('Berberine'));
      expect(vm.patientAge, 68);
      expect(vm.patientEgfr, 55);
      expect(vm.result, isNull);
      expect(vm.isEvaluating, isFalse);
    });

    test('adds and removes drugs accurately', () {
      final vm = SafetyViewModel();

      vm.addDrug('Metformin');
      expect(vm.selectedDrugs, contains('Metformin'));

      // Duplicate prevention
      vm.addDrug('Metformin');
      expect(vm.selectedDrugs.where((d) => d == 'Metformin').length, 1);

      vm.removeDrug('Metformin');
      expect(vm.selectedDrugs, isNot(contains('Metformin')));
    });

    test('adds and removes herbs accurately', () {
      final vm = SafetyViewModel();

      vm.addHerb('Ashwagandha');
      expect(vm.selectedHerbs, contains('Ashwagandha'));

      vm.removeHerb('Ashwagandha');
      expect(vm.selectedHerbs, isNot(contains('Ashwagandha')));
    });

    test('updates age and eGFR demographics', () {
      final vm = SafetyViewModel();

      vm.updateAge(75);
      expect(vm.patientAge, 75);

      vm.updateEgfr(40);
      expect(vm.patientEgfr, 40);
    });
  });
}
