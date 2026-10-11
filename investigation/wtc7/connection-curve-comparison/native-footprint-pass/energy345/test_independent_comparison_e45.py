"""Fault-injection controls for the independently authored E4/E5 checker only."""
import ast
import copy
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('independent_e45', HERE / 'independent-comparison-e45-check.py')
C = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(C)


def fixture():
    data = {'pair': 'E4', 'target_box': C.BOXES['E4'], 'context_box': C.CONTEXTS['E4'],
            'routes': {'solid': [], 'dash': []}, 'unassigned_bands': []}
    for route in data['routes']:
        for x in range(440, 690):
            data['routes'][route].append(C.record('E4', 'root', x, [], [],
                'no_attributable_cells', None, 'Synthetic inspected empty attribution.', []))
    data['unassigned_bands'].append(C.record('E4', 'root', 442, [80], [79, 81],
        'identity_conflict', 'fixture-band', 'Synthetic shared band.', []))
    data['routes']['solid'][2] = C.record('E4', 'root', 442, [], [], 'identity_conflict',
        None, 'Synthetic reference.', ['fixture-band'])
    return data


class IndependentControls(unittest.TestCase):
    def test_scalar_controls(self):
        self.assertTrue(all(C.controls().values()))

    def test_valid_fixture_and_missing_is_not_empty(self):
        data = fixture()
        bands = C.validate_reader('E4', data)
        self.assertIsNone(bands.get(443))
        self.assertEqual(bands[442]['core'], [80])
        self.assertEqual(C.visible('E4', data, bands, 442), {'core': [80], 'fringe': [79, 81]})

    def test_different_visible_pieces_may_coexist(self):
        data = fixture()
        data['routes']['solid'][2] = C.record('E4', 'root', 442, [83], [82, 84],
            'identified_local_fragment', 'fixture-solid', 'Synthetic separate piece.', ['fixture-band'])
        C.validate_reader('E4', data)

    def test_fringe_only_boundary_permitted(self):
        data = fixture()
        data['routes']['dash'][0] = C.record('E4', 'root', 440, [], [80],
            'boundary_truncated', 'fixture-edge', 'Synthetic fringe edge.', [])
        C.validate_reader('E4', data)

    def test_reject_reader_faults(self):
        faults = []
        a = fixture(); a['routes']['solid'][2]['band_refs'] = ['wrong']; faults.append(('wrong_id', a))
        a = fixture(); a['routes']['solid'][2]['band_refs'] = [{'band_id': 'fixture-band', 'x': 443}]; faults.append(('wrong_column', a))
        a = fixture(); a['routes']['solid'][2]['unassigned_band_refs'] = []; faults.append(('two_reference_schemas', a))
        a = fixture(); a['routes']['solid'][2]['band_refs'] *= 2; faults.append(('duplicate_reference', a))
        a = fixture(); a['unassigned_bands'] *= 2; faults.append(('duplicate_band', a))
        a = fixture(); a['routes']['solid'].pop(); faults.append(('missing_column', a))
        a = fixture(); a['coverage'] = {'target_box': C.BOXES['E5']}; faults.append(('conflicting_box', a))
        a = fixture(); a['routes']['solid'][2]['core'] = [80]; faults.append(('model_band_duplicate', a))
        a = fixture(); a['routes']['solid'][2]['boundary_flags'] = ['target_bottom']; faults.append(('transferred_band_flag', a))
        a = fixture(); a['routes']['dash'][3] = C.record('E4', 'root', 443, [83], [], 'identified_local_fragment', 'dash', 'Fixture.', [])
        a['routes']['solid'][3] = copy.deepcopy(a['routes']['dash'][3]); faults.append(('models_duplicate', a))
        a = fixture(); a['routes']['dash'][3]['status'] = 'fringe_only'; faults.append(('empty_fringe_status', a))
        a = fixture(); a['routes']['dash'][3]['status'] = 'identified_local_fragment'; faults.append(('empty_identified_status', a))
        a = fixture(); a['routes']['dash'][3]['core'] = [83]; faults.append(('selected_absent_status', a))
        a = fixture(); a['routes']['dash'][3]['status'] = 'boundary_truncated'; faults.append(('empty_boundary_status', a))
        for label, data in faults:
            with self.subTest(label=label), self.assertRaises(AssertionError):
                C.validate_reader('E4', data)

    def test_each_operation_is_independently_checked(self):
        left, right = {'core': [80], 'fringe': [79, 81]}, {'core': [81], 'fringe': [79, 80]}
        a, b = C.classes(left), C.classes(right)
        expected = {kind: C.membership(a[kind], b[kind]) for kind in a}
        self.assertEqual(C.verify_sets(expected, left, right), 15)
        for kind in ('core', 'fringe', 'outer'):
            for operation in C.OPS:
                corrupted = copy.deepcopy(expected)
                corrupted[kind][operation].append(90)
                with self.subTest(kind=kind, operation=operation), self.assertRaises(AssertionError):
                    C.verify_sets(corrupted, left, right)

    def test_run_overlap_bounds_and_boolean_rejected(self):
        for runs in [[(440, 442), (442, 444)], [(439, 442)], [(440, 690)], [(442, 440)], [(True, 442)]]:
            with self.subTest(runs=runs), self.assertRaises(AssertionError):
                C.run_membership(runs, 'E4')

    def test_literal_metadata_does_not_execute_expressions(self):
        for expression in ['dangerous()', 'dict(**x)', '[v for v in x]', 'x.y', '1+2']:
            with self.subTest(expression=expression), self.assertRaises(AssertionError):
                C.literal(ast.parse(expression, mode='eval').body, {})

    def test_e4_all_literal_metadata_and_records(self):
        for who in ('root', 'independent'):
            script = HERE / ('reader-E4-' + who + '.py')
            tree = ast.parse(script.read_text())
            self.assertEqual(C.pin(script)['sha256'], C.FROZEN[script.name])
            self.assertEqual(C.expand_e4(who, tree, C.literal_constants(tree)), C.read('reader-E4-' + who + '.json'))

    def test_e5_all_literal_metadata_and_records(self):
        for who in ('root', 'independent'):
            script = HERE / ('reader-E5-' + who + '.py')
            tree = ast.parse(script.read_text())
            self.assertEqual(C.pin(script)['sha256'], C.FROZEN[script.name])
            self.assertEqual(C.expand_e5(who, tree, C.literal_constants(tree)), C.read('reader-E5-' + who + '.json'))

    def test_e5_literal_runs_preserve_holes_and_local_ids(self):
        actual = C.explicit_runs([[400, 401, [30], [29], 'a'], [403, 403, [], [31], 'b']])
        self.assertEqual(actual, {400: ([30], [29], 'a'), 401: ([30], [29], 'a'), 403: ([], [31], 'b')})
        for runs in [[[394, 394, [], [30], 'a']], [[400, 403, [30], [], 'a'], [403, 404, [], [29], 'b']],
                     [[400, 401, [30], []]], [[True, 401, [30], [], 'a']]]:
            with self.subTest(runs=runs), self.assertRaises(AssertionError):
                C.explicit_runs(runs)


if __name__ == '__main__':
    unittest.main(verbosity=2)
