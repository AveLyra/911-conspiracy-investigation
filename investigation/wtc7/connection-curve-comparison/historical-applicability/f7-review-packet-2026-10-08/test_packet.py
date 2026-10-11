import copy
from fractions import Fraction as F
from pathlib import Path
import tempfile
import unittest
import packet as p


def fixtures():
    def cell(id, pair='F7'):
        return {'id': id, 'pair': pair, 'role': 'primary', 'route': 'dash'}
    def rows(end=1):
        return [{'solid_reader': s, 'dash_reader': d, 'human_accepted': False, 'actual_D': None,
                 'segments': [{'render_x': [0, end], 'status': 'paired_local_candidate'}]}
                for s in p.old.ROLES for d in p.old.ROLES]
    common = {'human_accepted': False, 'actual_D': None, 'model_discrepancies': None,
              'assumptions': ['Hidentity', 'Hsupport', 'Hink0'], 'axis_boxes': {'toy': [0, 4]}}
    a = dict(copy.deepcopy(common), pairs=[{'pair': n, 'scenarios': rows()} for n in p.old.PAIRS],
             candidate_cells=[cell('old'), cell('other', 'F3')])
    f = dict(copy.deepcopy(common), before_scenarios=rows(), after_scenarios=rows(2),
             preserved_old_F7_candidate_cells=[cell('old')], new_candidate_cells=[cell('new')])
    return a, f


class Composition(unittest.TestCase):
    def test_exact_preservation_and_nonmutation(self):
        a, f = fixtures()
        original = copy.deepcopy((a, f))
        result = p.compose(a, f, 1)
        self.assertEqual(result['candidate_cells'], a['candidate_cells'] + f['new_candidate_cells'])
        self.assertEqual((a, f), original)
        self.assertEqual([v for v in result['pairs'] if v['pair'] != 'F7'],
                         [v for v in a['pairs'] if v['pair'] != 'F7'])
        self.assertEqual(next(v for v in result['pairs'] if v['pair'] == 'F7')['scenarios'],
                         f['after_scenarios'])

    def test_non_f7_addition_rejected(self):
        a, f = fixtures(); f['new_candidate_cells'][0]['pair'] = 'F8'
        with self.assertRaisesRegex(ValueError, 'outside F7'): p.compose(a, f, 1)

    def test_missing_addition_rejected(self):
        a, f = fixtures(); f['new_candidate_cells'] = []
        with self.assertRaisesRegex(ValueError, 'incomplete'): p.compose(a, f, 1)

    def test_duplicate_addition_rejected(self):
        a, f = fixtures(); f['new_candidate_cells'].append(copy.deepcopy(f['new_candidate_cells'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate'): p.compose(a, f, 2)

    def test_old_id_collision_rejected(self):
        a, f = fixtures(); f['new_candidate_cells'][0]['id'] = 'old'
        with self.assertRaisesRegex(ValueError, 'duplicate'): p.compose(a, f, 1)

    def test_changed_old_cells_rejected(self):
        a, f = fixtures(); f['preserved_old_F7_candidate_cells'][0]['id'] = 'changed'
        with self.assertRaisesRegex(ValueError, 'old F7 cells'): p.compose(a, f, 1)

    def test_changed_before_scenarios_rejected(self):
        a, f = fixtures(); f['before_scenarios'][0]['segments'][0]['render_x'] = [0, 2]
        with self.assertRaisesRegex(ValueError, 'old F7 scenarios'): p.compose(a, f, 1)

    def test_changed_axes_rejected(self):
        a, f = fixtures(); f['axis_boxes']['toy'][1] = 5
        with self.assertRaisesRegex(ValueError, 'axis boxes'): p.compose(a, f, 1)

    def test_acceptance_or_result_contamination_rejected(self):
        for key, value in [('human_accepted', True), ('actual_D', []), ('model_discrepancies', {})]:
            for index in (0, 1):
                with self.subTest(key=key, index=index):
                    pair = fixtures(); pair[index][key] = value
                    with self.assertRaisesRegex(ValueError, 'acceptance'): p.compose(*pair, 1)

    def test_scenario_acceptance_rejected(self):
        a, f = fixtures(); f['after_scenarios'][0]['human_accepted'] = True
        with self.assertRaisesRegex(ValueError, 'acceptance'): p.compose(a, f, 1)

    def test_missing_scenario_rejected(self):
        a, f = fixtures(); f['after_scenarios'].pop()
        with self.assertRaisesRegex(ValueError, 'four scenarios'): p.compose(a, f, 1)

    def test_duplicate_scenario_rejected(self):
        a, f = fixtures(); f['after_scenarios'][1] = copy.deepcopy(f['after_scenarios'][0])
        with self.assertRaisesRegex(ValueError, 'reader roster'): p.compose(a, f, 1)

    def test_empty_f7_remains_unavailable(self):
        a, f = fixtures()
        for row in f['after_scenarios']: row['segments'] = []
        result = p.compose(a, f, 1)
        target = next(v for v in result['pairs'] if v['pair'] == 'F7')['scenarios'][0]
        self.assertIsNone(p.old.quantile(p.old.intervals(target['segments']), F(1, 2))['page_x'])

    def test_boundary_tie_not_nudged(self):
        rows = [{'render_x': [0, 1], 'status': 'paired_local_candidate'},
                {'render_x': [2, 3], 'status': 'paired_local_candidate'}]
        result = p.old.quantile(p.old.intervals(rows), F(1, 2))
        self.assertEqual(result['page_x'], 1)
        self.assertTrue(result['cumulative_tie'])
        self.assertEqual(p.old.point_state({'segments': rows}, result['page_x'])['status'],
                         'boundary_unresolved')

    def test_overlapping_after_segments_rejected(self):
        a, f = fixtures(); f['after_scenarios'][0]['segments'].append(
            {'render_x': [1, 3], 'status': 'paired_local_candidate'})
        with self.assertRaisesRegex(ValueError, 'overlapping'): p.compose(a, f, 1)

    def test_slot_preservation_and_change_detection(self):
        old = [{'id': 'CE-' + n + 'Q' + str(i), 'pair': n, 'payload': None}
               for n in p.old.PAIRS for i in (1, 2, 3)]
        new = copy.deepcopy(old)
        for s in new:
            if s['pair'] == 'F7': s['payload'] = 'new'
        unchanged, changed = p.compare_slots(new, old)
        self.assertEqual(len(unchanged), 39)
        self.assertEqual(changed, ['CE-F7Q1', 'CE-F7Q2', 'CE-F7Q3'])
        new[0]['payload'] = 'contamination'
        with self.assertRaisesRegex(ValueError, 'non-F7'): p.compare_slots(new, old)

    def test_missing_or_reordered_slot_rejected(self):
        rows = [{'id': 'CE-' + n + 'Q' + str(i), 'pair': n} for n in p.old.PAIRS for i in (1, 2, 3)]
        with self.assertRaises(ValueError): p.compare_slots(rows[:-1], rows)
        with self.assertRaises(ValueError): p.compare_slots(rows[::-1], rows)

    def test_changed_helper_rejected_before_execution(self):
        with tempfile.TemporaryDirectory(prefix='f7-packet-test-') as name:
            file = Path(name) / 'helper.py'
            file.write_text("raise RuntimeError('must not execute')")
            with self.assertRaisesRegex(ValueError, 'changed original'): p.import_helper(file)

    def test_dependency_owner_resolution(self):
        with tempfile.TemporaryDirectory(prefix='f7-input-owner-') as name:
            directory = Path(name); nested = directory / 'nested'; nested.mkdir()
            source = directory / 'source.txt'; source.write_text('synthetic source')
            expected = p.pin(source)
            pins = {}
            root = {'inputs': {'source.txt': expected}, 'inputs_after': {'source.txt': expected}}
            child = {'inputs': {'../source.txt': expected}, 'inputs_after': {'../source.txt': expected}}
            p.include_declared(pins, root, directory)
            p.include_declared(pins, child, nested)
            self.assertEqual(len(pins), 1)
            self.assertEqual((p.BASE / next(iter(pins))).resolve(), source.resolve())

    def test_saved_dependency_drift_rejected(self):
        with self.assertRaisesRegex(ValueError, 'dependency drift'):
            p.include_declared({}, {'inputs': {'missing': {}}, 'inputs_after': {}}, p.HERE)


if __name__ == '__main__':
    unittest.main()
