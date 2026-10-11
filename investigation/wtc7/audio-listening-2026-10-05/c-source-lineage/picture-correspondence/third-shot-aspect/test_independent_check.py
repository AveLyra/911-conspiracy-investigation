"""Synthetic controls only: no historical frames, scores or output traversal."""
import copy
from fractions import Fraction
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('aspect_separate_checker', HERE / 'independent_check.py')
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)


def metric(score, coverage=1., count=100, reason=None):
    return {'score': score, 'coverage': coverage, 'pixels': count, 'missing_reason': reason}


def row(index, fit=.8, evaluation=.5, dynamic=.2):
    transforms = [] if fit is None else [{'fit_score': fit, 'fit_coverage': 1., 'fit_pixels': 100,
        'evaluations': {'static_evaluation': metric(evaluation, reason='variance' if evaluation is None else None),
                        'dynamic': metric(dynamic, reason='variance' if dynamic is None else None)}}]
    return {'source_index': index, 'transforms': transforms}


class IndependentControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.helper = C.load_helper()
        cls.image = (np.arange(21600).reshape(120, 180) % 251).astype(float)
        cls.full = np.ones((120, 180), bool)

    def test_exact_factor_derivation(self):
        self.assertEqual(Fraction(950, 320) / Fraction(720, 224), Fraction(133, 144))
        self.assertEqual(Fraction(720, 224) / Fraction(950, 320), Fraction(144, 133))

    def test_all_grid_sizes_independent_rational_round(self):
        for arm in C.ARMS:
            factor = Fraction(1) if arm == 'baseline' else Fraction(133, 144)
            for index in range(21):
                t = C.geometry(arm, index)
                scale = Fraction(index + 15, 20)
                # Integer nearest-height oracle is safe here: no half tie on this fixed grid.
                unrounded = 120 * scale * factor
                self.assertNotEqual(unrounded - unrounded.numerator // unrounded.denominator, Fraction(1, 2))
                self.assertEqual(t['raster_width'], round(180 * scale))
                self.assertEqual(t['raster_height'], round(120 * scale * factor))
                self.assertEqual(Fraction(t['native_magnification_x']), Fraction(950 * t['raster_width'], 57600))
                self.assertEqual(Fraction(t['native_magnification_y']), Fraction(3 * t['raster_height'], 112))

    def test_known_sizes_and_floor_origins(self):
        for index, expected in [(0, (135, 83, 47, 43)), (5, (180, 111, 25, 29)), (20, (315, 194, -43, -12))]:
            t = C.geometry('native_relative_aspect', index)
            self.assertEqual(tuple(t[k] for k in ('raster_width', 'raster_height', 'canvas_x', 'canvas_y')), expected)
        self.assertEqual(C.geometry('baseline', 20)['canvas_y'], -20)

    def test_f1_exact_parent_independent_canvas_equivalence(self):
        for index, scale in enumerate(C.SCALES):
            a, av, _ = C.make_canvas(self.image, 'baseline', index)
            b, bv, _ = self.helper.canvas(self.image, scale)
            np.testing.assert_array_equal(a, b)
            np.testing.assert_array_equal(av, bv)

    def test_clipped_canvas_all_translation_corners(self):
        for arm in C.ARMS:
            for index in range(21):
                a, valid, t = C.make_canvas(self.image, arm, index)
                xx, yy = np.meshgrid(np.arange(230), np.arange(170))
                expected = ((xx >= t['canvas_x']) & (xx < t['canvas_x'] + t['raster_width'])
                            & (yy >= t['canvas_y']) & (yy < t['canvas_y'] + t['raster_height']))
                np.testing.assert_array_equal(valid, expected)
                self.assertTrue((a[~valid] == 0).all())
                for top, left in [(0, 0), (0, 50), (50, 0), (50, 50)]:
                    self.assertEqual(a[top:top+120, left:left+180].shape, (120, 180))
                    np.testing.assert_array_equal(valid[top:top+120, left:left+180], expected[top:top+120, left:left+180])

    def test_native_pixel_center_oracle(self):
        t = C.geometry('native_relative_aspect', 5)
        p = C.native_coordinates(0, 0, 25, 29, t)
        self.assertEqual(p, {'reference_x': Fraction(6035, 36), 'reference_y': Fraction(3),
                             'early_x': Fraction(8, 9), 'early_y': Fraction(112, 111)})
        q = C.native_coordinates(1, 1, 25, 29, t)
        self.assertEqual((q['reference_x']-p['reference_x']) / (q['early_x']-p['early_x']), Fraction(t['native_magnification_x']))
        self.assertEqual((q['reference_y']-p['reference_y']) / (q['early_y']-p['early_y']), Fraction(t['native_magnification_y']))

    def test_geometry_refuses_unplanned_family(self):
        for arm, index in [('third', 0), ('baseline', -1), ('baseline', 21), ('baseline', True)]:
            with self.assertRaises(AssertionError):
                C.geometry(arm, index)

    def test_working_array_rejects_bad_geometry_range(self):
        for a in [np.zeros((119, 180)), np.full((120, 180), np.nan), np.full((120, 180), -1), np.full((120, 180), 256)]:
            with self.assertRaises(AssertionError):
                C.make_canvas(a, 'baseline', 5)

    def test_mask_centers_counts_and_separation(self):
        regions = {k: self.helper.mask([rectangle], C.CROP) for k, rectangle in C.RECTANGLES.items()}
        self.assertEqual([int(regions[k].sum()) for k in C.METRICS], [4784, 1363, 1886])
        for k, ranges in {'fit': (13, 105, 118, 170), 'static_evaluation': (82, 111, 5, 52), 'dynamic': (10, 56, 59, 100)}.items():
            expected = np.zeros((120, 180), bool)
            y0, y1, x0, x1 = ranges
            expected[y0:y1, x0:x1] = True
            np.testing.assert_array_equal(regions[k], expected)
        self.assertTrue(all(not (regions[a] & regions[b]).any() for i, a in enumerate(C.METRICS) for b in C.METRICS[i+1:]))

    def test_direct_known_gain_inverse_and_flat(self):
        self.assertAlmostEqual(C.direct_record(self.helper, self.image, self.image * 3 + 2, self.full, self.full)['score'], 1)
        self.assertAlmostEqual(C.direct_record(self.helper, self.image, -self.image, self.full, self.full)['score'], -1)
        self.assertEqual(C.direct_record(self.helper, self.image * 0, self.image, self.full, self.full)['missing_reason'], 'variance')

    def test_gate_boundary_fullmask_denominator(self):
        a = np.arange(100, dtype=float).reshape(10, 10)
        full = np.ones(a.shape, bool)
        valid = full.copy(); valid.flat[85:] = False
        result = C.direct_record(self.helper, a, a, full, valid)
        self.assertEqual((result['score'], result['coverage'], result['pixels']), (1., .85, 85))
        valid.flat[84] = False
        self.assertEqual(C.direct_record(self.helper, a, a, full, valid)['missing_reason'], 'coverage')

    def test_pixel_and_variance_gates(self):
        a = np.arange(31, dtype=float)[None, :]
        full = np.ones(a.shape, bool)
        self.assertEqual(C.direct_record(self.helper, a, a, full, full)['missing_reason'], 'pixel_count')
        a = np.tile([-1e-5, 1e-5], 20)[None, :]
        full = np.ones(a.shape, bool)
        self.assertEqual(C.direct_record(self.helper, a, a, full, full)['missing_reason'], 'variance')

    def test_surface_global_top_two_ties_and_null(self):
        scores = np.full((21, 51, 51), np.nan)
        coverage = np.ones(scores.shape)
        scores[20, 0, 0] = .9; scores[0, 50, 50] = .9; scores[0, 0, 1] = .9
        self.assertEqual(C.top_two(scores, coverage), [(0, 0, 1), (0, 50, 50)])
        scores[:] = np.nan
        self.assertEqual(C.top_two(scores, coverage), [])

    def test_surface_rejects_invalid_arrays(self):
        s = np.full((21, 51, 51), np.nan); c = np.ones(s.shape)
        for scores, coverage in [(s[:20], c[:20]), (np.full(s.shape, np.inf), c), (s, c * 1.01), (s, c * np.nan), (c * 1.01, c)]:
            with self.assertRaises(AssertionError):
                C.top_two(scores, coverage)

    def test_common_same_count_different_positions(self):
        a = np.arange(100, dtype=float).reshape(10, 10)
        full = np.ones(a.shape, bool)
        av, bv = full.copy(), full.copy()
        av.flat[:10] = False; bv.flat[-10:] = False
        r = C.common_diagnostic(self.helper, a, full, [(a, av), (a, bv)])
        self.assertFalse(r['valid_sets_equal'])
        self.assertEqual((r['baseline_pixels'], r['alternative_pixels'], r['intersection_pixels'], r['intersection_coverage']), (90, 90, 80, .8))
        self.assertEqual(r['diagnostic']['availability'], 'neither')
        self.assertEqual(r['diagnostic']['baseline']['missing_reason'], 'coverage')

    def test_common_scores_use_same_positions_without_refit(self):
        a = np.arange(100, dtype=float).reshape(10, 10)
        full = np.ones(a.shape, bool)
        av, bv = full.copy(), full.copy()
        av.flat[:5] = False; bv.flat[-5:] = False
        b = a.copy(); b[~bv] = 1e8
        r = C.common_diagnostic(self.helper, a, full, [(a, av), (b, bv)])
        self.assertEqual(r['intersection_coverage'], .9)
        self.assertEqual(r['diagnostic']['availability'], 'both')
        self.assertEqual(r['diagnostic']['score_delta'], 0.)
        self.assertEqual(r['diagnostic']['baseline']['score'], 1.)

    def test_common_missing_transform_explicit_null(self):
        r = C.common_diagnostic(self.helper, self.image, self.full, None)
        self.assertIsNone(r['diagnostic'])
        self.assertIsNone(r['valid_sets_equal'])
        self.assertEqual(r['missing_reason'], 'one_or_both_primary_fit_transforms_missing')

    def test_availability_all_four_states(self):
        for a, b, expected in [(None, None, 'neither'), (None, .4, 'alternative_only'), (.5, None, 'baseline_only'), (.5, .4, 'both')]:
            r = C.comparison(metric(a), metric(b))
            self.assertEqual(r['availability'], expected)
            self.assertEqual(r['coverage_delta'], 0.)
            if a is None or b is None:
                self.assertIsNone(r['score_delta'])
            else:
                self.assertAlmostEqual(r['score_delta'], -.1)

    def test_rankings_ties_unavailable_near_sets_and_union(self):
        rows = [row(60, .8, .4, None), row(0, .8, .7, .9), row(30, .795, .8, .1), row(90, None)]
        r = C.expected_ranking(rows)
        self.assertEqual(r['fit']['top_two'], [0, 60])
        self.assertEqual(r['static_evaluation']['top_two'], [30, 0])
        self.assertEqual(r['dynamic']['top_two'], [0, 30])
        self.assertEqual([x['source_index'] for x in r['dynamic']['unavailable']], [60, 90])
        self.assertEqual(r['shortlist_union'], [0, 30, 60])
        self.assertTrue(r['fit']['ranking'][0]['sample_boundary'])
        self.assertEqual(r['fit']['near_best']['0.01'], [0, 60, 30])

    def test_evaluation_never_chooses_second_transform(self):
        r = row(0, evaluation=.1)
        r['transforms'].append(copy.deepcopy(r['transforms'][0]))
        r['transforms'][1]['evaluations']['static_evaluation']['score'] = 1.
        self.assertEqual(C.expected_ranking([r])['static_evaluation']['ranking'][0]['score'], .1)

    def test_exact_pair_roster_and_surface_binding(self):
        rows = []
        for arm, ref, source in C.expected_keys():
            rows.append({'arm': arm, 'reference_index': ref, 'source_index': source,
                         'source_pts': 0, 'source_time_base': '1', 'reference_pts': 0, 'reference_time_base': '1',
                         'sample_boundary': source in (C.EARLY[0], C.EARLY[-1]),
                         'surface_file': f'surfaces-{arm}-C{ref}-E{source}.npz', 'transforms': [], 'missing_reason': 'all_fit_transforms_invalid'})
        self.assertEqual(len(rows), 228)
        C.check_rows(rows)
        for mutation in [rows[:-1], rows + [rows[-1]], list(reversed(rows))]:
            with self.assertRaises(AssertionError):
                C.check_rows(mutation)
        wrong = copy.deepcopy(rows); wrong[0]['surface_file'] = wrong[1]['surface_file']
        with self.assertRaises(AssertionError):
            C.check_rows(wrong)

    def test_equality_rejects_missing_key_and_null_zero(self):
        for actual, expected in [({'x': 1}, {'x': 1, 'y': 0}), ({'score': 0.}, {'score': None}), ({'x': True}, {'x': 1})]:
            with self.assertRaises(AssertionError):
                C.same(actual, expected)
        C.same({'score': .5 + 5e-10, 'coverage': .5 + 5e-13}, {'score': .5, 'coverage': .5})
        with self.assertRaises(AssertionError):
            C.same({'coverage': .5 + 5e-11}, {'coverage': .5})

    def test_missing_dependency_cannot_pass_self_report(self):
        config = {k: {'path': '/synthetic/' + k, 'sha256': 'dummy'} for k in ('early_video', 'c_video', 'early_map', 'c_map')}
        state = {'schema_version': 1, 'python': '3.13.7', 'numpy': '2.3.4', 'pillow': '12.0.0',
                 'source_specs': config, 'pins': {p: {'sha256': C.FIXED.get(Path(p), 'dummy')} for p in C.required_method_paths()}}
        with patch.object(C, 'check_pin'):
            C.check_state(state, config)
            for path in C.required_method_paths():
                missing = copy.deepcopy(state); del missing['pins'][path]
                with self.assertRaises(AssertionError):
                    C.check_state(missing, config)

    def test_changed_fixed_hash_and_source_spec_rejected(self):
        config = {k: {'path': '/synthetic/' + k, 'sha256': 'dummy'} for k in ('early_video', 'c_video', 'early_map', 'c_map')}
        state = {'schema_version': 1, 'python': '3.13.7', 'numpy': '2.3.4', 'pillow': '12.0.0',
                 'source_specs': config, 'pins': {p: {'sha256': C.FIXED.get(Path(p), 'dummy')} for p in C.required_method_paths()}}
        bad = copy.deepcopy(state); bad['pins'][str(C.HERE / 'PROTOCOL.md')]['sha256'] = 'wrong'
        with patch.object(C, 'check_pin'), self.assertRaises(AssertionError):
            C.check_state(bad, config)
        bad = copy.deepcopy(state); bad['source_specs']['early_map']['sha256'] = 'wrong'
        with patch.object(C, 'check_pin'), self.assertRaises(AssertionError):
            C.check_state(bad, config)

    def test_product_inventory_rejects_omitted_or_extra_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / 'one').write_bytes(b'one')
            pins = {'one': C.pin(d / 'one')}
            C.check_products(d, pins, {'one'})
            for declared, required in [({}, set()), (pins, {'one', 'two'})]:
                with self.assertRaises(AssertionError):
                    C.check_products(d, declared, required)
            (d / 'one').write_bytes(b'changed')
            with self.assertRaises(AssertionError):
                C.check_products(d, pins, {'one'})

    def test_path_escape_and_helper_hash_rejected(self):
        for p in ['../escape', '/absolute', 'inner/../../escape']:
            with self.assertRaises(AssertionError):
                C.safe_product(Path('/tmp/synthetic'), p)
        with patch.object(C, 'HELPER_SHA', '0' * 64), self.assertRaises(AssertionError):
            C.load_helper()


if __name__ == '__main__':
    unittest.main(verbosity=2)
