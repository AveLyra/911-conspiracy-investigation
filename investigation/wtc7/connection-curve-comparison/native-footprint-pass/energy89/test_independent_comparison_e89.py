"""Fault-injection controls for the independent checker, not its producers."""
import ast
import copy
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('e89_independent', HERE / 'independent-comparison-e89-check.py')
C = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(C)


def fixture():
    data = {'pair': 'E8', 'target_box': C.BOXES['E8'], 'context_box': C.CONTEXTS['E8'],
            'routes': {'solid': [], 'dash': []}, 'unassigned_bands': []}
    for route in data['routes']:
        data['routes'][route] = [C.row('E8', 'root', x, [], [], None, 'no_attributable_cells', 'Fixture.', []) for x in range(535, 690)]
    data['unassigned_bands'].append(C.row('E8', 'root', 537, [62], [61, 63], 'band', 'identity_conflict', 'Fixture.', []))
    data['routes']['solid'][2] = C.row('E8', 'root', 537, [], [], None, 'identity_conflict', 'Fixture.', ['band'])
    return data


class Controls(unittest.TestCase):
    def test_scalar_controls(self):
        self.assertTrue(all(C.controls().values()))

    def test_valid_missing_empty_and_coexistence(self):
        a = fixture()
        bands = C.validate('E8', a)
        self.assertIsNone(bands.get(538))
        self.assertEqual(C.visible('E8', a, bands, 537), {'core': [62], 'fringe': [61, 63]})
        a['routes']['solid'][2] = C.row('E8', 'root', 537, [70], [69, 71], 'solid', 'identified_local_fragment', 'Fixture.', ['band'])
        C.validate('E8', a)

    def test_fringe_only_boundary(self):
        a = fixture()
        a['routes']['dash'][0] = C.row('E8', 'root', 535, [], [62], 'dash', 'boundary_truncated', 'Fixture.', [])
        C.validate('E8', a)

    def test_reader_faults(self):
        faults = []
        a = fixture(); a['routes']['solid'][2]['band_refs'] = ['wrong']; faults.append(('wrong_id', a))
        a = fixture(); a['routes']['solid'][2]['band_refs'] = [{'band_id': 'band', 'x': 538}]; faults.append(('wrong_column', a))
        a = fixture(); a['routes']['solid'][2]['unassigned_band_refs'] = []; faults.append(('two_schemas', a))
        a = fixture(); a['routes']['solid'][2]['band_refs'] *= 2; faults.append(('duplicate_ref', a))
        a = fixture(); a['unassigned_bands'] *= 2; faults.append(('duplicate_band', a))
        a = fixture(); a['routes']['solid'].pop(); faults.append(('missing_column', a))
        a = fixture(); a['coverage'] = {'target_box': C.BOXES['E9']}; faults.append(('contradictory_box', a))
        a = fixture(); a['routes']['solid'][2] = C.row('E8', 'root', 537, [62], [], 'solid', 'identified_local_fragment', 'Fixture.', []); faults.append(('band_model_duplicate', a))
        a = fixture(); a['routes']['solid'][2]['boundary_flags'] = ['target_left']; faults.append(('transferred_flag', a))
        a = fixture(); a['routes']['solid'][3] = C.row('E8', 'root', 538, [70], [], 'solid', 'identified_local_fragment', 'Fixture.', [])
        a['routes']['dash'][3] = copy.deepcopy(a['routes']['solid'][3]); faults.append(('models_duplicate', a))
        for status in ('fringe_only', 'identified_local_fragment', 'boundary_truncated'):
            a = fixture(); a['routes']['dash'][3]['status'] = status; faults.append(('empty_' + status, a))
        a = fixture(); a['routes']['dash'][3]['core'] = [70]; faults.append(('selected_no_attribution', a))
        for name, data in faults:
            with self.subTest(name=name), self.assertRaises(AssertionError):
                C.validate('E8', data)

    def test_each_comparison_operation(self):
        left, right = {'core': [62], 'fringe': [61, 63]}, {'core': [63], 'fringe': [61, 62]}
        a, b = C.classes(left), C.classes(right)
        expected = {key: C.operations(a[key], b[key]) for key in a}
        self.assertEqual(C.verify_sets(expected, left, right), 15)
        for key in a:
            for op in C.OPS:
                corrupt = copy.deepcopy(expected); corrupt[key][op].append(80)
                with self.subTest(key=key, op=op), self.assertRaises(AssertionError):
                    C.verify_sets(corrupt, left, right)

    def test_manual_run_order_holes_identity_and_faults(self):
        self.assertEqual(C.expand_runs('E8', [[540, 540, [62], [], 'b'], [537, 538, [], [61], 'a']]),
                         {540: ([62], [], 'b'), 537: ([], [61], 'a'), 538: ([], [61], 'a')})
        for runs in [[[534, 535, [62], [], 'a']], [[540, 690, [62], [], 'a']], [[True, 538, [62], [], 'a']],
                     [[537, 540, [62], [], 'a'], [540, 541, [62], [], 'b']], [[540, 540, [62], []]]]:
            with self.subTest(runs=runs), self.assertRaises(AssertionError):
                C.expand_runs('E8', runs)

    def test_literal_refuses_execution(self):
        for expression in ['dangerous()', 'dict(**x)', '[v for v in x]', 'x.y', '1+2']:
            with self.subTest(expression=expression), self.assertRaises(AssertionError):
                C.literal(ast.parse(expression, mode='eval').body, {})

    def test_four_complete_literal_replays_and_coverage(self):
        for pair in ('E8', 'E9'):
            for who in ('root', 'independent'):
                name = 'reader-' + pair + '-' + who
                script = HERE / (name + '.py')
                self.assertEqual(C.pin(script)['sha256'], C.FROZEN[script.name])
                data = C.read(name + '.json')
                with self.subTest(pair=pair, who=who):
                    self.assertEqual(C.expand(pair, who, ast.parse(script.read_text())), data)
                    C.validate(pair, data)
                    C.coverage(pair, data)

    def test_selected_white_is_flagged_without_changing_selection(self):
        data = fixture(); original = copy.deepcopy(data)
        white, count = C.selected_cells(data, {(537, 61): [255, 255, 255], (537, 62): [1, 2, 3], (537, 63): [255, 254, 255]})
        self.assertEqual(white, [{'scope': 'unassigned', 'class': 'fringe', 'x': 537, 'y': 61}])
        self.assertEqual(count, 3)
        self.assertEqual(data, original)


if __name__ == '__main__':
    unittest.main(verbosity=2)
