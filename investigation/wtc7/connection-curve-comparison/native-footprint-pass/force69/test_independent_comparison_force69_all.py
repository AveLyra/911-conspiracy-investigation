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
SPEC = importlib.util.spec_from_file_location('force69_all_checker', HERE / 'independent-comparison-force69-all-check.py')
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

    def test_fragment_specific_route_reference_rejected_if_wrong_owner(self):
        data = fixture()
        band = data['unassigned_bands'][0]
        band.update(fragment_id=None, core=[20], fringe=[19, 21],
                    candidate_routes=['solid', 'dash'],
                    fragments=[{'fragment_id': 'a', 'core': [20], 'fringe': [19]},
                               {'fragment_id': 'b', 'core': [], 'fringe': [21]}],
                    possible_routes_by_fragment={'a': ['dash'], 'b': ['solid']})
        data['routes']['dash'][10]['band_refs'] = ['a']
        data['routes']['solid'][10] = row(215, status='identity_conflict', refs=['b'])
        C.validate('F6-Im2', 'primary', data)
        data['routes']['dash'][10]['band_refs'] = ['b']
        with self.assertRaisesRegex(AssertionError, 'that fragment candidate'):
            C.validate('F6-Im2', 'primary', data)

    def test_every_region_scoped_and_full_read_only_command(self):
        for regions in ([name] for name in C.BOXES):
            with self.subTest(regions=regions):
                self.assertEqual(C.replay_command(regions),
                                 [C.sys.executable, '-B', str(HERE / 'independent-comparison-force69-all-check.py'),
                                  '--region', regions[0]])
        all_regions = list(C.BOXES)
        command = C.replay_command(all_regions)
        self.assertEqual(command[3::2], ['--region'] * 6)
        self.assertEqual(command[4::2], all_regions)
        self.assertNotIn('--output', command)

    def test_duplicate_return_keys_are_not_silently_discarded(self):
        for source in ("def build():\n return {'x': 1, 'x': 2}",
                       "def build():\n return {1: 'x'}"):
            with self.subTest(source=source), self.assertRaises(AssertionError):
                C.return_fields(ast.parse(source))

    def test_literal_top_level_container_is_explicit(self):
        for runs in ({}, (), None, 'not a run list'):
            with self.subTest(runs=runs), self.assertRaises(AssertionError):
                C.expand_tables(runs, C.BOXES['F6-Im2'])

    def test_source_partitions_and_every_rgb_record_with_synthetic_pixels(self):
        seeds = {'Im0.jpg': 17, 'Im1.jpg': 79, 'Im2.jpg': 151}
        rgb = lambda name, x, y: [(x + seeds[name]) % 256, y, seeds[name]]
        context = {'target_boxes': C.BOXES, 'context_boxes': C.CONTEXTS,
                   'sources': C.SOURCES, 'pairs': C.PAIRS,
                   'source_dimensions': {name: [741, 88] for name in seeds},
                   'human_accepted': False, 'classification': None,
                   'cells': {region: [{'x': x, 'y': y, 'rgb': rgb(C.SOURCES[region], x, y)}
                                     for y in range(box[1], box[3]) for x in range(box[0], box[2])]
                             for region, box in C.CONTEXTS.items()}}
        class SyntheticImage:
            mode, size = 'RGB', (741, 88)
            def __init__(self, path):
                self.name = path.name
            def __enter__(self):
                return self
            def __exit__(self, *_):
                return False
            def load(self):
                pass
            def tobytes(self):
                return bytes(v for y in range(88) for x in range(741) for v in rgb(self.name, x, y))
        with patch.object(C.Image, 'open', side_effect=SyntheticImage):
            result = C.source_contexts(context)
            self.assertEqual(sum(map(len, result.values())), 62231)
            self.assertNotEqual(result['F7-Im1'][330, 50], result['F7-Im2'][330, 50])
            changes = [
                lambda d: d['cells'].pop('F9-Im0'),
                lambda d: d['cells'].update(extra=[]),
                lambda d: d['cells']['F9-Im0'].pop(),
                lambda d: d['cells']['F9-Im0'][0].update(x=219),
                lambda d: d['cells']['F9-Im0'][-1].update(rgb=[0, 0, 0]),
                lambda d: d['cells']['F9-Im0'][0].update(rgb=[True, 53, 17]),
                lambda d: d['source_dimensions'].update({'Im0.jpg': [740, 88]}),
                lambda d: d.update(human_accepted=True),
            ]
            for i, change in enumerate(changes):
                bad = copy.deepcopy(context)
                change(bad)
                with self.subTest(i=i), self.assertRaises(AssertionError):
                    C.source_contexts(bad)

    def test_peer_coverage_requires_union_not_total_count(self):
        region = 'F9-Im0'
        box = C.CONTEXTS[region]
        cells = [{'x': x, 'y': y, 'rgb': [1, 2, 3]}
                 for y in range(box[1], box[3]) for x in range(box[0], box[2])]
        blocks = [{'display_region': region, 'box': [218, 53, 270, 88], 'untruncated': True, 'receipt': 'synthetic-a'},
                  {'display_region': region, 'box': [270, 53, 327, 88], 'untruncated': True, 'receipt': 'synthetic-b'}]
        data = {'reader': 'peer', 'unassigned_bands': [], 'coverage': {
            'raw_blocks': blocks, 'raw_context_cells': 3815, 'full_native_strip_viewed': True,
            'full_composed_page_viewed': True, 'all_blocks_untruncated': True,
            'target_columns': 105, 'model_route_records': 210, 'unassigned_band_records': 0}}
        C.coverage(region, data, {'cells': {region: cells}})
        bad = copy.deepcopy(data)
        bad['coverage']['raw_blocks'][1]['box'] = [269, 53, 326, 88]
        with self.assertRaisesRegex(AssertionError, 'complete declared peer context coverage'):
            C.coverage(region, bad, {'cells': {region: cells}})

    def test_nonfrozen_scope_fails_before_reading_historical_artifacts(self):
        with patch.object(C, 'FROZEN', {}), patch.object(C, 'pin') as pin:
            with self.assertRaisesRegex(AssertionError, 'must be frozen before replay'):
                C.run(['F6-Im2'])
            pin.assert_not_called()

    def test_invalid_scope_fails_before_reading_historical_artifacts(self):
        for regions in ([], ['F9-Im0', 'F9-Im0'], ['missing'], 'F9-Im0'):
            with self.subTest(regions=regions), patch.object(C, 'pin') as pin:
                with self.assertRaisesRegex(AssertionError, 'explicit unique declared region scope'):
                    C.run(regions)
                pin.assert_not_called()

    def test_entire_comparison_arithmetic_records_and_metadata(self):
        region = 'F6-Im2'
        readers = {'primary': fixture(), 'peer': fixture()}
        readers['peer']['reader'] = 'peer'
        readers['peer']['unassigned_bands'][0].update(core=[22], fringe=[21, 23])
        bands = {role: C.validate(region, role, data) for role, data in readers.items()}
        empty = {key: {op: [] for op in C.OPS} for key in C.CLASSES}
        rows = [{'route': route, 'x': x,
                 'primary_original': readers['primary']['routes'][route][x - 205],
                 'peer_original': readers['peer']['routes'][route][x - 205],
                 'sets': copy.deepcopy(empty)}
                for route in C.ROUTES for x in range(205, 365)]
        ink = [{'x': x, 'primary_unassigned_original': bands['primary'].get(x),
                'peer_unassigned_original': bands['peer'].get(x), 'sets': copy.deepcopy(empty)}
               for x in range(205, 365)]
        ink[10]['sets'] = {
            'core': {'intersection': [], 'union': [20, 22], 'primary_only': [20],
                     'peer_only': [22], 'symmetric_difference': [20, 22]},
            'fringe': {'intersection': [21], 'union': [19, 21, 23], 'primary_only': [19],
                       'peer_only': [23], 'symmetric_difference': [19, 23]},
            'outer': {'intersection': [21], 'union': [19, 20, 21, 22, 23], 'primary_only': [19, 20],
                      'peer_only': [22, 23], 'symmetric_difference': [19, 20, 22, 23]}}
        fake_pin = {'bytes': 3, 'sha256': 'synthetic'}
        inputs = {name: fake_pin for name in ('reader-F6-Im2-primary.json', 'reader-F6-Im2-peer.json',
                  'compare_force69.py', 'test_compare_force69.py', '../force45/compare_force45.py')}
        names = ['reader-F6-Im2-primary.json', 'reader-F6-Im2-peer.json']
        whites = {'primary': [], 'peer': []}
        expected = {'input_pins': {name: inputs[name] for name in names}, 'dependencies': {},
                    'script_pin': fake_pin, 'test_pin': fake_pin, 'helper_pin': fake_pin,
                    'pair': 'F6', 'source_image': 'Im2.jpg', 'literal_readings': readers,
                    'route_comparisons': rows, 'visible_ink_comparisons': ink,
                    'summary': {'routes': {'entries': 320, 'outer_different': 0, 'class_different': 0},
                                'visible_ink': {'entries': 160, 'outer_different': 1, 'class_different': 1},
                                'route_status_different': 0, 'selected_exact_white_cells': whites},
                    'metadata_sentinel': {'original': True}}
        comparator = ast.parse('def run():\n return {' + ', '.join(
            repr(key) + ': ' + (repr(value) if key == 'metadata_sentinel' else 'unused')
            for key, value in expected.items()) + '}')
        result = C.check_comparison(region, readers, bands, expected, whites, {}, inputs, comparator)
        self.assertEqual(result['set_operations_checked'], 7200)
        self.assertEqual(result['reader_route_records'], 640)
        self.assertEqual(result['literal_replay_exclusions'], [])
        mutations = [
            lambda d: d['route_comparisons'][-1]['sets']['outer']['primary_only'].append(87),
            lambda d: d['visible_ink_comparisons'][10]['sets']['core'].update(intersection=[20]),
            lambda d: d['literal_readings']['peer'].update(source_image='Im1.jpg'),
            lambda d: d['route_comparisons'][0]['primary_original'].update(note='altered'),
            lambda d: d['summary']['routes'].update(entries=319),
            lambda d: d.pop('metadata_sentinel'),
            lambda d: d.update(extra='not part of saved format'),
        ]
        for i, change in enumerate(mutations):
            bad = copy.deepcopy(expected)
            change(bad)
            with self.subTest(i=i), self.assertRaises(AssertionError):
                C.check_comparison(region, readers, bands, bad, whites, {}, inputs, comparator)


if __name__ == '__main__':
    unittest.main(verbosity=2)
