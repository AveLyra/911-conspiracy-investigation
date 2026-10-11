"""Independent packet controls and synthetic scalar-assignment arithmetic oracle."""
import copy
from fractions import Fraction as Q
import importlib.util
import itertools
from pathlib import Path
import struct
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('independent_envelope_packet_check', HERE/'independent_check.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
MATH_BEFORE = c.pin(HERE/'envelope_math.py')
if MATH_BEFORE['sha256'] != '7d1b5bc8acaa36e9d78ade1715c42c4a672c30a12c18510b1da7b37446ec7b0e':
    raise ValueError('reviewed arithmetic module changed before synthetic oracle')
spec = importlib.util.spec_from_file_location('envelope_math_under_test', HERE/'envelope_math.py')
math = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = math
spec.loader.exec_module(math)


def segment(lo, hi, state='paired_local_candidate'):
    return {'render_x': [lo, hi], 'status': state}


def source_cell():
    return {'id': 'toy-row', 'reader_path': 'toy-reader', 'role': 'primary', 'route': 'solid',
            'source': 'Im0', 'fragment_id': 'toy-body', 'native_rectangle': [10, 20, 11, 23],
            'render_rectangle': [10, 20, 11, 23], 'render_x': [10, 11]}


def identity_invocation():
    return {'ctm': [36, 0, 0, 36, 0, 756], 'native_dimensions': [100, 100]}


class SelectionControls(unittest.TestCase):
    def test_full_domain_exact_quantiles(self):
        values = [c.select_from_segments([segment(0, Q(8, 5))], q)[0]['page_x']
                  for q in (Q(1, 4), Q(1, 2), Q(3, 4))]
        self.assertEqual(values, [Q(2, 5), Q(4, 5), Q(6, 5)])

    def test_gap_tie_uses_preceding_endpoint(self):
        segments = [segment(0, Q(1, 5)), segment(Q(1, 5), Q(4, 5), 'gap'), segment(Q(4, 5), 1)]
        targets = [c.select_from_segments(segments, f)[0] for f in (Q(1, 4), Q(1, 2), Q(3, 4))]
        self.assertEqual([r['page_x'] for r in targets], [Q(1, 10), Q(1, 5), Q(9, 10)])
        self.assertTrue(targets[1]['cumulative_tie'])
        self.assertEqual(targets[1]['component'], 0)

    def test_bookkeeping_merge_does_not_hide_internal_boundary(self):
        segments = [segment(0, 1), segment(1, 2)]
        target, components = c.select_from_segments(segments, Q(1, 2))
        self.assertEqual(components, [[0, 2]])
        self.assertEqual(target['page_x'], 1)
        self.assertFalse(target['cumulative_tie'])
        self.assertEqual(c.scenario_position(segments, 1), {'status': 'boundary_unresolved', 'segment_indices': [0, 1]})

    def test_empty_primary_never_uses_peer(self):
        target, components = c.select_from_segments([segment(0, 1, 'dash_only')], Q(1, 2))
        self.assertEqual(components, [])
        self.assertIsNone(target['page_x'])
        self.assertEqual(c.scenario_position([segment(0, 2)], None)['status'], 'no_primary_target')

    def test_same_position_alternative_states_are_distinct(self):
        for segments, x, state in [([segment(0, 1)], 2, 'outside_candidate_extent'),
                                  ([segment(0, 1)], 0, 'boundary_unresolved'),
                                  ([segment(0, 1, 'gap')], Q(1, 2), 'gap'),
                                  ([segment(0, 1, 'shared_ink_ownership_conflict')], Q(1, 2), 'shared_ink_ownership_conflict'),
                                  ([segment(0, 1, 'overlapping_candidate_coverage')], Q(1, 2), 'overlapping_candidate_coverage')]:
            with self.subTest(state=state):
                self.assertEqual(c.scenario_position(segments, x)['status'], state)

    def test_invalid_source_domains_are_errors(self):
        for segments in ([segment(1, 1)], [segment(1, 0)], [segment(False, 1)],
                         [segment(0.0, 1)], [segment(0, 2), segment(1, 3)],
                         [segment(2, 3), segment(0, 1)], [segment(0, 1, 'invented')]):
            with self.subTest(segments=segments), self.assertRaises(ValueError):
                c.select_from_segments(segments, Q(1, 2))
        for fraction in (0, 1, False, .5):
            with self.assertRaises(ValueError):
                c.select_from_segments([segment(0, 1)], fraction)

    def test_malformed_alternative_not_hidden_by_missing_target(self):
        with self.assertRaises(ValueError):
            c.scenario_position([segment(0, 0)], None)

    def test_affine_quantiles_map_to_same_source_location(self):
        original = [segment(1, 2), segment(4, 7)]
        for scale, shift in ((Q(2), Q(-3)), (Q(1, 7), Q(4, 3))):
            transformed = [segment(scale*q(r['render_x'][0])+shift, scale*q(r['render_x'][1])+shift) for r in original]
            for fraction in (Q(1, 4), Q(1, 2), Q(3, 4)):
                source = c.select_from_segments(original, fraction)[0]['page_x']
                target = c.select_from_segments(transformed, fraction)[0]['page_x']
                self.assertEqual((target-shift)/scale, source)


def q(value):
    return Q(value)


class MappingControls(unittest.TestCase):
    def test_inverse_endpoint_interpolation(self):
        result = c.source_mapping(source_cell(), Q(21, 2), identity_invocation())
        self.assertEqual(result['native_x'], Q(21, 2))
        self.assertEqual(result['render_rectangle'], [10, 20, 11, 23])
        self.assertFalse(result['boundary_touch'])
        self.assertTrue(c.source_mapping(source_cell(), 11, identity_invocation())['boundary_touch'])

    def test_distinct_nonuniform_strip_scale(self):
        invocation = {'native_dimensions': [20, 10], 'ctm': [18, 0, 0, 9, 36, 756]}
        # x render = 100 + 2.5u; y render = 75 + 2.5v.
        cell = dict(source_cell(), native_rectangle=[4, 2, 5, 4], render_rectangle=[110, 80, Q(225, 2), 85], render_x=[110, Q(225, 2)])
        result = c.source_mapping(cell, Q(445, 4), invocation)
        self.assertEqual(result['native_x'], Q(9, 2))
        self.assertEqual(result['render_rectangle'], [110, 80, Q(225, 2), 85])

    def test_invalid_mapping_rejected(self):
        for changed, x in ((dict(source_cell(), render_rectangle=[10, 20, 12, 23]), Q(21, 2)),
                           (dict(source_cell(), render_x=[10, 12]), Q(21, 2)),
                           (dict(source_cell(), native_rectangle=[10, 20, True, 23]), Q(21, 2)),
                           (source_cell(), 12)):
            with self.assertRaises(ValueError):
                c.source_mapping(changed, x, identity_invocation())

    def test_axis_displacement_exact_and_invalid(self):
        self.assertEqual(c.displacement_hull(5, {'L': [0, 1], 'R': [9, 10]}), [Q(32, 45), Q(8, 9)])
        self.assertIsNone(c.displacement_hull(None, {'L': [0, 1], 'R': [9, 10]}))
        for axis in ({'L': [0, 2], 'R': [1, 3]}, {'L': [True, 2], 'R': [9, 10]}):
            with self.assertRaises(ValueError):
                c.displacement_hull(5, axis)

    def test_duplicates_use_footprints_not_coordinates_or_row_ids(self):
        def slot(number, change_shell=False, empty=False):
            entries = []
            for model in ('spring', 'shell'):
                rectangle = [1, 2, 2, 3] if model == 'spring' or not change_shell else [2, 2, 3, 3]
                mapping = [] if empty else [{'source': 'Im0', 'native_rectangle': rectangle, 'cell_id': str(number)}]
                entries.append({'id': f'CE-F3Q{number}-{model}', 'model': model,
                    'mappings': {role: copy.deepcopy(mapping) for role in c.ROLES},
                    'duplicate_entries': {role: [] for role in c.ROLES}})
            return {'id': f'CE-F3Q{number}', 'pair': 'F3', 'entries': entries, 'duplicate_paired_slots': []}
        slots = [slot(1), slot(2), slot(3, True), slot(4, empty=True)]
        c.mark_duplicates(slots)
        self.assertEqual(slots[0]['duplicate_paired_slots'], ['CE-F3Q2'])
        self.assertEqual(slots[2]['duplicate_paired_slots'], [])
        self.assertEqual(slots[3]['duplicate_paired_slots'], [])
        self.assertEqual(slots[0]['entries'][0]['duplicate_entries']['peer'], ['CE-F3Q2-spring', 'CE-F3Q3-spring'])

    def test_pin_omission_and_bad_types(self):
        expected = {name: {'bytes': 1, 'sha256': 'a'*64} for name in ('one', 'two')}
        c.require_closure(expected, expected)
        for key in expected:
            missing = dict(expected)
            del missing[key]
            with self.assertRaises(ValueError): c.require_closure(missing, expected)
        with self.assertRaises(ValueError): c.pin_shape({'bytes': True, 'sha256': 'a'*64})

    def test_exclusive_save(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'receipt.json'
            c.save_exclusive(path, {'synthetic': True})
            initial = path.read_bytes()
            with self.assertRaises(FileExistsError): c.save_exclusive(path, {})
            self.assertEqual(path.read_bytes(), initial)


def scalar_oracle(cells, axis, panel):
    """Enumerate scalar assignments, including equality for convex minima.

    Expected values use direct physical ordinates and coordinate differences;
    no interval arithmetic or scale/difference helpers from the tested module.
    These finite cases attain all extrema of the relaxed synthetic envelopes.
    """
    ymax = Q(1000000 if panel == 'force' else 800000)
    choices = []
    for _, spring, shell in cells:
        r, s = set(map(Q, spring)), set(map(Q, shell))
        overlap_lo, overlap_hi = max(spring[0], shell[0]), min(spring[1], shell[1])
        if overlap_lo <= overlap_hi:
            r.add(Q(overlap_lo)); s.add(Q(overlap_lo))
        choices.append(tuple(itertools.product(r, s)))
    observed = {group: {kind: [] for kind in ('signed', 'absolute', 'squared')} for group in ('integrals', 'means')}
    lengths = []
    for left, right, top, bottom in itertools.product(*(sorted(set(pair)) for pair in axis)):
        lengths_m = [Q(8, 5)*(Q(x[1])-left)/(right-left)-Q(8, 5)*(Q(x[0])-left)/(right-left)
                     for x, _, _ in cells]
        length = sum(lengths_m, Q(0)); lengths.append(length)
        for assignment in itertools.product(*choices):
            delta = [ymax*(bottom-shell)/(bottom-top)-ymax*(bottom-spring)/(bottom-top)
                     for spring, shell in assignment]
            values = {'signed': sum((w*d for w, d in zip(lengths_m, delta)), Q(0)),
                      'absolute': sum((w*abs(d) for w, d in zip(lengths_m, delta)), Q(0)),
                      'squared': sum((w*d*d for w, d in zip(lengths_m, delta)), Q(0))}
            for kind, value in values.items():
                observed['integrals'][kind].append(value)
                observed['means'][kind].append(value/length)
    return {group: {kind: (min(values), max(values)) for kind, values in kinds.items()}
            for group, kinds in observed.items()}, (min(lengths), max(lengths))


class SyntheticArithmeticOracle(unittest.TestCase):
    def test_scalar_assignment_oracle_over_both_units_and_shared_axes(self):
        cases = [(((0, 1), (2, 4), (1, 3)),),
                 (((0, 2), (7, 8), (0, 1)), ((3, 4), (0, 2), (4, 5))),
                 (((Q(1, 3), Q(2, 3)), (1, 1), (3, 3)), ((2, 3), (4, 4), (2, 2))),
                 (((0, 1), (0, 2), (1, 4)), ((2, 3), (2, 5), (3, 4)))]
        axes = [((Q(0), Q(0)), (Q(8, 5), Q(8, 5)), (Q(0), Q(0)), (Q(1000000), Q(1000000))),
                ((Q(-2), Q(1)), (Q(8), Q(10)), (Q(-3), Q(2)), (Q(9), Q(12)))]
        for panel, raw, axis in itertools.product(('force', 'energy'), cases, axes):
            with self.subTest(panel=panel, cells=raw, axis=axis):
                expected, length = scalar_oracle(raw, axis, panel)
                cells = tuple(math.Cell(math.Interval(*x), math.Interval(*r), math.Interval(*s)) for x, r, s in raw)
                scenario = math.Scenario('synthetic', panel, 'toy-page', cells)
                box = math.AxisBox('toy-page', *(math.Interval(*pair) for pair in axis))
                actual = math.compare_envelopes(scenario, box)
                for group, kinds in expected.items():
                    for kind, bounds in kinds.items():
                        self.assertEqual((actual[group][kind].lo, actual[group][kind].hi), bounds)
                self.assertEqual((actual['domain_length'].lo, actual['domain_length'].hi), length)
                self.assertFalse(actual['human_accepted'])

    def test_robust_sign_and_missing_alternative_are_explicit(self):
        cell = math.Cell(math.Interval(0, 1), math.Interval(3, 4), math.Interval(0, 1))
        scenario = math.Scenario('toy', 'force', 'page', (cell,))
        self.assertEqual(math.reader_robust_sign({'one': scenario, 'two': scenario}, Q(1, 2))['sign'], 'positive')
        self.assertIsNone(math.reader_robust_sign({'one': scenario, 'two': None}, Q(1, 2))['sign'])
        self.assertIsNone(math.reader_robust_sign({'one': scenario}, 1)['sign'])

    def test_different_domains_not_interchangeable(self):
        def scenario(hi):
            return math.Scenario('toy', 'energy', 'page', (math.Cell(math.Interval(0, hi), math.Interval(3, 4), math.Interval(0, 1)),))
        with self.assertRaises(ValueError): math.require_same_domain({'one': scenario(1), 'two': scenario(2)})
        self.assertEqual(math.require_same_domain({'one': scenario(1), 'two': scenario(1)}), (math.Interval(0, 1),))


def tearDownModule():
    if c.pin(HERE/'envelope_math.py') != MATH_BEFORE:
        raise ValueError('arithmetic module changed during synthetic oracle')


if __name__ == '__main__':
    unittest.main()
