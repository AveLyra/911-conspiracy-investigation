"""Synthetic-only controls for the independently authored checker.

Historical replay is a separate command, not concealed in a unit-test total.
"""
import ast
import copy
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('force69_checker', HERE / 'independent-comparison-force69-check.py')
C = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(C)


def row(x, core=None, fringe=None, fid=None, status='no_attributable_cells', refs=None):
    core, fringe = core or [], fringe or []
    return {'x': x, 'core': core, 'fringe': fringe, 'fragment_id': fid, 'status': status,
            'boundary_flags': C.flags(C.BOXES['F6-Im2'], x, core + fringe), 'band_refs': refs or [], 'note': 'Synthetic fixture.'}


def fixture():
    data = {'pair': 'F6', 'region_id': 'F6-Im2', 'reader': 'primary', 'source_image': 'Im2.jpg',
            'target_box': C.BOXES['F6-Im2'], 'context_box': C.CONTEXTS['F6-Im2'],
            'human_accepted': False, 'physical_support': None,
            'routes': {route: [row(x) for x in range(205, 365)] for route in C.ROUTES},
            'unassigned_bands': [row(215, [20], [19, 21], 'band', 'identity_conflict')]}
    data['unassigned_bands'][0]['candidate_routes'] = ['dash']
    data['routes']['dash'][10] = row(215, [], [], None, 'identity_conflict', ['band'])
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
        runs = [[215, 215, [4], [3], 'a'], [212, 213, [], [5], 'b'], [215, 215, [8], [], 'c']]
        actual = C.expand_tables(runs, C.BOXES['F6-Im2'], 'prefix-')
        self.assertEqual(list(actual), [215, 212, 213])
        self.assertNotIn(214, actual)
        self.assertEqual(actual[215], [{'fragment_id': 'prefix-a', 'core': [4], 'fringe': [3]},
                                      {'fragment_id': 'prefix-c', 'core': [8], 'fringe': []}])
        self.assertEqual(C.union_rows(actual[215], 'core'), [4, 8])

    def test_invalid_literal_memberships(self):
        variants = [
            [[True, 215, [4], [], 'a']], [[204, 215, [4], [], 'a']],
            [[215, 365, [4], [], 'a']], [[215, 215, [88], [], 'a']],
            [[215, 215, [4], [4], 'a']], [[215, 215, [4, 4], [], 'a']],
            [[215, 215, [4], [], 'a'], [215, 215, [4], [], 'b']],
            [[215, 215, [4], [], 'a'], [215, 215, [8], [], 'a']],
            [[215, 215, [], [], 'a']], [[215, 215, [True], [], 'a']],
        ]
        for runs in variants:
            with self.subTest(runs=runs), self.assertRaises(AssertionError):
                C.expand_tables(runs, C.BOXES['F6-Im2'])

    def test_boundaries_and_fringe_only(self):
        self.assertEqual(C.flags(C.BOXES['F6-Im2'], 205, []), [])
        self.assertEqual(C.flags(C.BOXES['F6-Im2'], 364, [0, 87]), ['target_right', 'target_top', 'target_bottom'])
        data = fixture()
        data['routes']['solid'][0] = row(205, [], [0], 'a', 'boundary_truncated')
        C.validate('F6-Im2', 'primary', data)

    def test_missing_empty_and_band_id_are_distinct(self):
        data = fixture()
        bands = C.validate('F6-Im2', 'primary', data)
        self.assertIsNone(bands.get(216))
        data['unassigned_bands'].append(dict(row(216), candidate_routes=[]))
        bands = C.validate('F6-Im2', 'primary', data)
        self.assertEqual(bands[216]['core'], [])
        data['unassigned_bands'][0]['band_id'] = 'aggregate'
        data['routes']['dash'][10]['band_refs'] = [{'band_id': 'aggregate', 'x': 215}]
        C.validate('F6-Im2', 'primary', data)

    def test_fragment_memberships_and_multi_band_member_refs(self):
        data = fixture()
        data['unassigned_bands'][0] = dict(row(215, [20], [19, 21], None, 'identity_conflict'), candidate_routes=['dash'], fragments=[
            {'fragment_id': 'a', 'core': [20], 'fringe': [19]}, {'fragment_id': 'b', 'core': [], 'fringe': [21]}])
        data['routes']['dash'][10]['band_refs'] = ['a', 'b']
        C.validate('F6-Im2', 'primary', data)
        bad = copy.deepcopy(data)
        bad['unassigned_bands'][0]['fragments'][0]['fringe'] = [19, 21]
        with self.assertRaises(AssertionError):
            C.validate('F6-Im2', 'primary', bad)

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
        bad('band_model_overlap', lambda d: d['routes']['solid'].__setitem__(10, row(215, [20], [], 's', 'identified_local_fragment')))
        bad('flag_transfer', lambda d: d['routes']['solid'][10].update(boundary_flags=['target_left']))
        bad('boolean_x', lambda d: d['routes']['solid'][0].update(x=True))
        bad('boolean_y', lambda d: d['routes']['solid'][0].update(core=[True]))
        bad('row_order', lambda d: d['routes']['solid'][0].update(fringe=[2, 1]))
        bad('wrong_region_same_pair', lambda d: d.update(region_id='F7-Im1', pair='F7'))
        bad('wrong_source', lambda d: d.update(source_image='Im0.jpg'))
        bad('human_accepted', lambda d: d.update(human_accepted=True))
        for status in ('identified_local_fragment', 'fringe_only', 'boundary_truncated'):
            bad('empty_' + status, lambda d, status=status: d['routes']['solid'][20].update(status=status))
        for label, value in faults:
            with self.subTest(label=label), self.assertRaises(AssertionError):
                C.validate('F6-Im2', 'primary', value)

    def test_ref_to_empty_band_rejected(self):
        data = fixture()
        data['unassigned_bands'][0] = dict(row(215), band_id='empty-band', candidate_routes=[])
        data['routes']['dash'][10]['band_refs'] = [{'x': 215, 'band_id': 'empty-band'}]
        with self.assertRaises(AssertionError):
            C.validate('F6-Im2', 'primary', data)

    def test_exact_white_diagnostic_not_automatic_repair(self):
        data = fixture(); original = copy.deepcopy(data)
        count, white = C.selected_white(data, {(215, 19): [255, 255, 255], (215, 20): [1, 2, 3], (215, 21): [255, 254, 255]})
        self.assertEqual(count, 3)
        self.assertEqual(white, [{'scope': 'unassigned', 'class': 'fringe', 'x': 215, 'y': 19}])
        self.assertEqual(data, original)


    def test_candidate_ownership_not_missing_or_inferred(self):
        data = fixture()
        C.validate('F6-Im2', 'primary', data)
        mutations = [
            lambda d: d['unassigned_bands'][0].pop('candidate_routes'),
            lambda d: d['unassigned_bands'][0].update(candidate_routes='dash'),
            lambda d: d['unassigned_bands'][0].update(candidate_routes=['dash', 'dash']),
            lambda d: d['unassigned_bands'][0].update(candidate_routes=['bad']),
            lambda d: d['unassigned_bands'][0].update(candidate_routes=['solid']),
            lambda d: d['routes']['dash'][10].update(status='no_attributable_cells', band_refs=[]),
            lambda d: d['routes']['solid'][10].update(status='identity_conflict'),
        ]
        for mutate in mutations:
            changed = copy.deepcopy(data)
            mutate(changed)
            with self.assertRaises(AssertionError):
                C.validate('F6-Im2', 'primary', changed)
        empty = fixture()
        empty['unassigned_bands'][0] = dict(row(215), candidate_routes=[])
        empty['routes']['dash'][10] = row(215)
        C.validate('F6-Im2', 'primary', empty)
        empty['unassigned_bands'][0]['status'] = 'identity_conflict'
        with self.assertRaises(AssertionError):
            C.validate('F6-Im2', 'primary', empty)

    def test_fragment_candidate_union_checked(self):
        data = fixture()
        data['unassigned_bands'][0].update(
            fragments=[{'fragment_id': 'band', 'core': [20], 'fringe': [19, 21]}],
            possible_routes_by_fragment={'band': ['dash']})
        C.validate('F6-Im2', 'primary', data)
        for value in ({}, {'wrong': ['dash']}, {'band': ['solid']}, {'band': ['dash', 'dash']}):
            bad = copy.deepcopy(data)
            bad['unassigned_bands'][0]['possible_routes_by_fragment'] = value
            with self.assertRaises(AssertionError):
                C.validate('F6-Im2', 'primary', bad)

    def test_ignored_outside_runs_and_empty_ids_rejected(self):
        for run in ([100, 101, [2], [], 'a'], [205, 366, [2], [], 'a'],
                    [210, 211, [2], [], ''], [210, 211, [2], [], None]):
            with self.subTest(run=run), self.assertRaises(AssertionError):
                C.expand_tables([run], C.BOXES['F6-Im2'])

    def test_primary_owner_expansion_and_metadata_nonexecution(self):
        text = """EXPECTED = {}
BAND_NOTE = 'Manually retained unresolved material; synthetic.'
ROUTE_NOTE = 'Manual source-native local-style attribution. Synthetic.'
def build(spec, script):
    return {'pair': 'F6', 'region_id': rid, 'source_image': raw['sources'][rid],
            'target_box': box, 'context_box': raw['context_boxes'][rid],
            'inputs': before, 'script_pin': pin(script), 'literal_instructions': runs,
            'unassigned_possible_routes': ownership, 'coverage': spec['coverage'],
            'identity_basis': spec['identity_basis'], 'routes': routes,
            'unassigned_bands': bands, 'retained_note': 'metadata sentinel'}
"""
        helper = ast.parse(text)
        spec = {'region': 'F6-Im2', 'literal': {'solid': [[210, 210, [10], [], 's']],
                'dash': [], 'unassigned': [[210, 210, [20], [19, 21], 'u']]},
                'ownership': {'u': ['dash']}, 'coverage': {'synthetic': True}, 'identity_basis': 'synthetic'}
        tree = ast.parse('SPEC = ' + repr(spec))
        fake_pin = {'bytes': 3, 'sha256': 'synthetic'}
        context = {'sources': C.SOURCES, 'context_boxes': C.CONTEXTS}
        with patch.object(C, 'pin', return_value=fake_pin):
            result = C.expand('F6-Im2', 'primary', tree, {}, helper, context)
        self.assertEqual(result['retained_note'], 'metadata sentinel')
        self.assertEqual(result['literal_instructions'], spec['literal'])
        self.assertEqual(result['unassigned_bands'][5]['candidate_routes'], ['dash'])
        self.assertEqual(result['routes']['solid'][5]['band_refs'], [])
        self.assertEqual(result['routes']['dash'][5]['band_refs'], ['unassigned-210'])
        self.assertEqual(result['routes']['dash'][5]['status'], 'identity_conflict')
        self.assertEqual(result['unassigned_bands'][5]['possible_routes_by_fragment'], {'u': ['dash']})
        broken = copy.deepcopy(spec)
        broken['ownership']['extra'] = ['solid']
        with self.assertRaises(AssertionError):
            C.expand_primary('F6-Im2', broken, helper)

    def test_peer_candidate_expansion_preserves_both_members_and_holes(self):
        helper = ast.parse("EMPTY = 'Inspected column; synthetic.'\nINK = 'Local visible style attribution; synthetic.'\nNONE = 'No model cells selected after actual inspection; synthetic.'")
        cfg = {'pair': 'F6', 'region_id': 'F6-Im2', 'source_image': 'Im2.jpg',
               'target': C.BOXES['F6-Im2'], 'context': C.CONTEXTS['F6-Im2'],
               'solid': [[210, 210, [10], [], 's']], 'dash': [],
               'unassigned': [[210, 210, [20], [], 'u1'], [210, 210, [], [22], 'u2']],
               'unassigned_candidates': {210: ['dash']}, 'unassigned_reasons': {210: 'Synthetic ownership.'}}
        routes, bands = C.expand_peer('F6-Im2', cfg, helper)
        self.assertEqual(bands[5]['core'], [20])
        self.assertEqual(bands[5]['fringe'], [22])
        self.assertEqual([p['fragment_id'] for p in bands[5]['fragments']], ['F6-Im2-peer-u1', 'F6-Im2-peer-u2'])
        self.assertEqual(routes['solid'][5]['unassigned_band_refs'], [])
        self.assertEqual(routes['dash'][5]['unassigned_band_refs'], [{'band_id': 'F6-Im2-peer-unassigned-210', 'x': 210}])
        self.assertEqual(bands[6]['candidate_routes'], [])
        self.assertEqual(bands[6]['status'], 'no_attributable_cells')
        for changed in ({}, {210: ['bad']}, {210: ['dash', 'dash']}, {210: ['solid', 'dash']}):
            bad = copy.deepcopy(cfg)
            bad['unassigned_candidates'] = changed
            with self.assertRaises(AssertionError):
                C.expand_peer('F6-Im2', bad, helper)

    def test_primary_declared_coverage_counts_are_not_enough(self):
        data = fixture()
        data['coverage'] = {'context_blocks_inclusive': [[203, 366]], 'context_rows_inclusive': [0, 87],
                            'context_cells': 14432, 'all_target_columns_read': True, 'native_strip_viewed': True,
                            'complete_composed_page_viewed': True, 'model_route_records': 320,
                            'unassigned_band_records': 1}
        C.coverage('F6-Im2', data, {})
        for blocks in ([[204, 366]], [[203, 250], [250, 366]], [[203, 367]], [[True, 366]]):
            bad = copy.deepcopy(data)
            bad['coverage']['context_blocks_inclusive'] = blocks
            with self.assertRaises(AssertionError):
                C.coverage('F6-Im2', bad, {})
        bad = copy.deepcopy(data)
        bad['coverage']['context_rows_inclusive'] = [1, 87]
        with self.assertRaises(AssertionError):
            C.coverage('F6-Im2', bad, {})

    def test_peer_same_source_coverage_union_and_exact_rgb(self):
        region, other = 'F7-Im1', 'F8-Im1'
        target = C.CONTEXTS[region]
        cells = lambda box: [{'x': x, 'y': y, 'rgb': [1, 2, 3]}
                             for y in range(box[1], box[3]) for x in range(box[0], box[2])]
        context = {'cells': {region: cells(target), other: cells(C.CONTEXTS[other])}}
        block = {'display_region': other, 'box': list(target), 'untruncated': True, 'receipt': 'synthetic'}
        data = {'reader': 'peer', 'unassigned_bands': [None] * 115, 'coverage': {
            'raw_blocks': [block], 'raw_context_cells': 4760, 'full_native_strip_viewed': True,
            'full_composed_page_viewed': True, 'all_blocks_untruncated': True,
            'target_columns': 115, 'model_route_records': 230, 'unassigned_band_records': 115}}
        C.coverage(region, data, context)
        for key, value in [('display_region', 'F7-Im2'), ('untruncated', False), ('receipt', ''),
                           ('box', [219, 48, 337, 88]), ('box', [218, 49, 337, 88])]:
            bad = copy.deepcopy(data)
            bad['coverage']['raw_blocks'][0][key] = value
            with self.assertRaises(AssertionError):
                C.coverage(region, bad, context)
        bad_context = copy.deepcopy(context)
        for r in bad_context['cells'][other]:
            if (r['x'], r['y']) == (218, 48):
                r['rgb'] = [1, 2, 4]
        with self.assertRaises(AssertionError):
            C.coverage(region, data, bad_context)

    def test_complete_metadata_equality_is_type_strict(self):
        a = {'coverage': {'count': 1}, 'note': 'original', 'candidate_routes': []}
        self.assertTrue(C.equal(a, copy.deepcopy(a)))
        for bad in ({'coverage': {'count': True}, 'note': 'original', 'candidate_routes': []},
                    {'coverage': {'count': 1}, 'note': 'changed', 'candidate_routes': []},
                    {'coverage': {'count': 1}, 'note': 'original'}):
            self.assertFalse(C.equal(a, bad))


if __name__ == '__main__':
    unittest.main(verbosity=2)
