"""Synthetic-only controls for the independently authored checker.

Historical replay is a separate command, not concealed in a unit-test total.
"""
import ast
import copy
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('force45_checker', HERE / 'independent-comparison-force45-check.py')
C = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(C)


def row(x, core=None, fringe=None, fid=None, status='no_attributable_cells', refs=None):
    core, fringe = core or [], fringe or []
    return {'x': x, 'core': core, 'fringe': fringe, 'fragment_id': fid, 'status': status,
            'boundary_flags': C.flags(C.BOXES['F4-Im4'], x, core + fringe), 'band_refs': refs or [], 'note': 'Synthetic fixture.'}


def fixture():
    data = {'pair': 'F4', 'region_id': 'F4-Im4', 'reader': 'primary', 'source_image': 'Im4.jpg',
            'target_box': C.BOXES['F4-Im4'], 'context_box': C.CONTEXTS['F4-Im4'],
            'human_accepted': False, 'physical_support': None,
            'routes': {route: [row(x) for x in range(330, 425)] for route in C.ROUTES},
            'unassigned_bands': [row(340, [20], [19, 21], 'band', 'identity_conflict')]}
    data['routes']['dash'][10] = row(340, [], [], None, 'identity_conflict', ['band'])
    return data


class SyntheticControls(unittest.TestCase):
    def test_explicit_arithmetic_and_holes(self):
        self.assertEqual(C.operations([2, 4], [4, 7]), {'intersection': [4], 'union': [2, 4, 7],
                         'primary_only': [2], 'peer_only': [7], 'symmetric_difference': [2, 7]})
        self.assertEqual(C.operations([], []), {key: [] for key in C.OPS})
        self.assertEqual(C.operations([], [2, 4])['peer_only'], [2, 4])

    def test_all_fifteen_operations_are_checked(self):
        left, right = {'core': [2], 'fringe': [1, 3]}, {'core': [3], 'fringe': [1, 2]}
        a, b = C.classes(left), C.classes(right)
        correct = {key: C.operations(a[key], b[key]) for key in C.CLASSES}
        self.assertEqual(C.verify_sets(correct, left, right), 15)
        for key in C.CLASSES:
            for op in C.OPS:
                bad = copy.deepcopy(correct)
                bad[key][op].append(80)
                with self.subTest(key=key, op=op), self.assertRaises(AssertionError):
                    C.verify_sets(bad, left, right)

    def test_direction_not_dictionary_order(self):
        values = {'peer': [4, 7], 'primary': [2, 4]}
        self.assertEqual(C.operations(values['primary'], values['peer'])['primary_only'], [2])
        self.assertEqual(C.operations(values['peer'], values['primary'])['primary_only'], [7])

    def test_literal_nonexecution(self):
        for expression in ['dangerous()', 'dict(**x)', '[v for v in x]', 'x.y', '__import__("os")', 'len(dangerous())']:
            with self.subTest(expression=expression), self.assertRaises(AssertionError):
                C.literal(ast.parse(expression, mode='eval').body, {})
        self.assertEqual(C.literal(ast.parse("{'v': cfg['x'], 'n': 2*(x1-x0), 'length': len(rows)}", mode='eval').body,
                                  {'cfg': {'x': 3}, 'x0': 2, 'x1': 5, 'rows': [7]}), {'v': 3, 'n': 6, 'length': 1})

    def test_manual_membership_multiple_holes_and_order(self):
        runs = [[340, 340, [4], [3], 'a'], [337, 338, [], [5], 'b'], [340, 340, [8], [], 'c']]
        actual = C.expand_tables(runs, C.BOXES['F4-Im4'], 'prefix-')
        self.assertEqual(list(actual), [340, 337, 338])
        self.assertNotIn(339, actual)
        self.assertEqual(actual[340], [{'fragment_id': 'prefix-a', 'core': [4], 'fringe': [3]},
                                      {'fragment_id': 'prefix-c', 'core': [8], 'fringe': []}])
        self.assertEqual(C.union_rows(actual[340], 'core'), [4, 8])

    def test_invalid_literal_memberships(self):
        variants = [
            [[True, 340, [4], [], 'a']], [[329, 340, [4], [], 'a']],
            [[340, 425, [4], [], 'a']], [[340, 340, [88], [], 'a']],
            [[340, 340, [4], [4], 'a']], [[340, 340, [4, 4], [], 'a']],
            [[340, 340, [4], [], 'a'], [340, 340, [4], [], 'b']],
            [[340, 340, [4], [], 'a'], [340, 340, [8], [], 'a']],
            [[340, 340, [], [], 'a']], [[340, 340, [True], [], 'a']],
        ]
        for runs in variants:
            with self.subTest(runs=runs), self.assertRaises(AssertionError):
                C.expand_tables(runs, C.BOXES['F4-Im4'])

    def test_boundaries_and_fringe_only(self):
        self.assertEqual(C.flags(C.BOXES['F4-Im4'], 330, []), [])
        self.assertEqual(C.flags(C.BOXES['F4-Im4'], 424, [0, 87]), ['target_right', 'target_top', 'target_bottom'])
        data = fixture()
        data['routes']['solid'][0] = row(330, [], [0], 'a', 'boundary_truncated')
        C.validate('F4-Im4', 'primary', data)

    def test_missing_empty_and_band_id_are_distinct(self):
        data = fixture()
        bands = C.validate('F4-Im4', 'primary', data)
        self.assertIsNone(bands.get(341))
        data['unassigned_bands'].append(row(341))
        bands = C.validate('F4-Im4', 'primary', data)
        self.assertEqual(bands[341]['core'], [])
        data['unassigned_bands'][0]['band_id'] = 'aggregate'
        data['routes']['dash'][10]['band_refs'] = [{'band_id': 'aggregate', 'x': 340}]
        C.validate('F4-Im4', 'primary', data)

    def test_fragment_memberships_and_multi_band_member_refs(self):
        data = fixture()
        data['unassigned_bands'][0] = dict(row(340, [20], [19, 21], None, 'identity_conflict'), fragments=[
            {'fragment_id': 'a', 'core': [20], 'fringe': [19]}, {'fragment_id': 'b', 'core': [], 'fringe': [21]}])
        data['routes']['dash'][10]['band_refs'] = ['a', 'b']
        C.validate('F4-Im4', 'primary', data)
        bad = copy.deepcopy(data)
        bad['unassigned_bands'][0]['fragments'][0]['fringe'] = [19, 21]
        with self.assertRaises(AssertionError):
            C.validate('F4-Im4', 'primary', bad)

    def test_reader_faults(self):
        faults = []
        def bad(label, mutate):
            value = fixture(); mutate(value); faults.append((label, value))
        bad('wrong_ref', lambda d: d['routes']['dash'][10].update(band_refs=['wrong']))
        bad('wrong_ref_column', lambda d: d['routes']['dash'][10].update(band_refs=[{'x': 341, 'band_id': 'band'}]))
        bad('duplicate_ref', lambda d: d['routes']['dash'][10].update(band_refs=['band', 'band']))
        bad('two_ref_schemas', lambda d: d['routes']['dash'][10].update(unassigned_band_refs=[]))
        bad('missing_column', lambda d: d['routes']['solid'].pop())
        bad('duplicate_band', lambda d: d['unassigned_bands'].append(copy.deepcopy(d['unassigned_bands'][0])))
        bad('empty_reason', lambda d: d['routes']['solid'][10].update(note=' '))
        bad('band_model_overlap', lambda d: d['routes']['solid'].__setitem__(10, row(340, [20], [], 's', 'identified_local_fragment')))
        bad('flag_transfer', lambda d: d['routes']['solid'][10].update(boundary_flags=['target_left']))
        bad('boolean_x', lambda d: d['routes']['solid'][0].update(x=True))
        bad('boolean_y', lambda d: d['routes']['solid'][0].update(core=[True]))
        bad('row_order', lambda d: d['routes']['solid'][0].update(fringe=[2, 1]))
        bad('wrong_region_same_pair', lambda d: d.update(region_id='F5-Im4', pair='F5'))
        bad('wrong_source', lambda d: d.update(source_image='Im2.jpg'))
        bad('human_accepted', lambda d: d.update(human_accepted=True))
        for status in ('identified_local_fragment', 'fringe_only', 'boundary_truncated'):
            bad('empty_' + status, lambda d, status=status: d['routes']['solid'][20].update(status=status))
        for label, value in faults:
            with self.subTest(label=label), self.assertRaises(AssertionError):
                C.validate('F4-Im4', 'primary', value)

    def test_ref_to_empty_band_rejected(self):
        data = fixture()
        data['unassigned_bands'][0] = dict(row(340), band_id='empty-band')
        data['routes']['dash'][10]['band_refs'] = [{'x': 340, 'band_id': 'empty-band'}]
        with self.assertRaises(AssertionError):
            C.validate('F4-Im4', 'primary', data)

    def test_exact_white_diagnostic_not_automatic_repair(self):
        data = fixture(); original = copy.deepcopy(data)
        count, white = C.selected_white(data, {(340, 19): [255, 255, 255], (340, 20): [1, 2, 3], (340, 21): [255, 254, 255]})
        self.assertEqual(count, 3)
        self.assertEqual(white, [{'scope': 'unassigned', 'class': 'fringe', 'x': 340, 'y': 19}])
        self.assertEqual(data, original)


if __name__ == '__main__':
    unittest.main(verbosity=2)
