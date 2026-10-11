"""Synthetic-only controls for the frozen two-arm aspect sensitivity."""
import copy
from fractions import Fraction
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest import mock

import numpy as np
from PIL import Image

SUBJECT = PARENT = CORE = None


class AspectControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global SUBJECT, PARENT, CORE
        if SUBJECT is None:
            import aspect_screen as SUBJECT
            PARENT, CORE, _ = SUBJECT.dependencies()

    def setUp(self):
        self.a, self.parent, self.core = SUBJECT, PARENT, CORE
        self.config = self.parent.config_load()
        self.rng = np.random.default_rng(8102026)
        self.image = self.rng.integers(20, 235, (120, 180)).astype(float)
        self.regions = self.a.masks(self.parent, self.config)

    def row(self, i, score=.8, static=.6, dynamic=.7):
        ev = lambda x: {'score': x, 'coverage': 1., 'pixels': 100, 'missing_reason': None if x is not None else 'variance'}
        return {'source_index': i, 'transforms': [{'fit_score': score, 'fit_coverage': 1., 'fit_pixels': 100,
                'evaluations': {'static_evaluation': ev(static), 'dynamic': ev(dynamic)}}]}

    def maps(self):
        def row(i, base):
            return {'source_index': i, 'png': f'{i}.png', 'source_pts': i,
                    'source_time_base': str(base), 'source_seconds_exact': str(i*base)}
        early = [{**row(i, Fraction(1001, 30000)), 'quarter_bin': second}
                 for second, i in enumerate(self.a.EARLY_INDICES)]
        refs = [row(i, Fraction(1, 30)) for i in self.a.REFERENCE_INDICES]
        return early, refs

    def test_baseline_exact_all_scales(self):
        for scale in self.a.SCALES:
            a, v, t = self.a.canvas(self.parent, self.image, scale, Fraction(1))
            b, w, u = self.parent.canvas(self.image, scale)
            np.testing.assert_array_equal(a, b)
            np.testing.assert_array_equal(v, w)
            self.assertEqual({k: t[k] for k in u}, u)

    def test_rational_sizes_origins_and_native_mapping(self):
        factor = Fraction(133, 144)
        self.assertEqual(Fraction(950, 320) / Fraction(720, 224), factor)
        for scale, expected in [(.75, (135, 83, 47, 43)), (1., (180, 111, 25, 29)), (1.75, (315, 194, -43, -12))]:
            _, _, t = self.a.canvas(self.parent, self.image, scale, factor)
            self.assertEqual(tuple(t[k] for k in ('raster_width', 'raster_height', 'canvas_x', 'canvas_y')), expected)
        for scale in self.a.SCALES:
            _, _, t = self.a.canvas(self.parent, self.image, scale, factor)
            s, sw, sh = Fraction(str(scale)), t['raster_width'], t['raster_height']
            self.assertEqual(Fraction(t['unrounded_height']), 120*s*factor)
            self.assertEqual((sw, sh), (round(180*s), round(120*s*factor)))
            self.assertEqual(Fraction(t['native_magnification_x']), Fraction(950*sw, 180*320))
            self.assertEqual(Fraction(t['native_magnification_y']), Fraction(720*sh, 120*224))
            # Mapping slopes in native pixel-edge coordinates, not index centers.
            self.assertEqual(Fraction(950, 180)/Fraction(320, sw), Fraction(t['native_magnification_x']))
            self.assertEqual(Fraction(720, 120)/Fraction(224, sh), Fraction(t['native_magnification_y']))
        with self.assertRaises(ValueError): self.a.canvas(self.parent, self.image, 1., 133/144)
        with self.assertRaises(ValueError): self.a.canvas(self.parent, self.image, .9, Fraction(9, 10))

    def test_all_translation_corners_clipping_and_padding(self):
        target = self.rng.integers(20, 235, (120, 180)).astype(float)
        for factor in self.a.ARMS.values():
            for scale in (.75, 1., 1.75):
                a, v, t = self.a.canvas(self.parent, self.image, scale, factor)
                raster = np.asarray(Image.fromarray(self.image.astype(np.uint8)).resize(
                    (t['raster_width'], t['raster_height']), Image.Resampling.BILINEAR))
                yy, xx = np.indices(a.shape)
                sx, sy = xx-t['canvas_x'], yy-t['canvas_y']
                truth = (sx >= 0) & (sx < raster.shape[1]) & (sy >= 0) & (sy < raster.shape[0])
                np.testing.assert_array_equal(v, truth)
                np.testing.assert_array_equal(a[v], raster[sy[v], sx[v]])
                scores, cover = self.core.pearson_surface(a, target, self.regions['fit'], v)
                for top, left in ((0, 0), (0, 50), (50, 0), (50, 50), (25, 25)):
                    patch, pv = a[top:top+120, left:left+180], v[top:top+120, left:left+180]
                    direct = self.parent.dynamic_score(self.core, patch, target, self.regions['fit'], pv)
                    self.assertAlmostEqual(cover[top, left], direct['coverage'], delta=1e-12)
                    if direct['score'] is None: self.assertTrue(np.isnan(scores[top, left]))
                    else: self.assertAlmostEqual(scores[top, left], direct['score'], delta=1e-9)
                a[~v] = 123456
                again, _ = self.core.pearson_surface(a, target, self.regions['fit'], v)
                np.testing.assert_allclose(again, scores, atol=1e-10, rtol=0, equal_nan=True)

    def test_masks_fixed_disjoint_and_native_centers(self):
        self.assertEqual([int(m.sum()) for m in self.regions.values()], [4784, 1363, 1886])
        for a, b in (('fit', 'static_evaluation'), ('fit', 'dynamic'), ('static_evaluation', 'dynamic')):
            self.assertFalse((self.regions[a] & self.regions[b]).any())
        boxes = ([790, 80, 1060, 630], [190, 490, 440, 665], [475, 60, 695, 335])
        for box, mask in zip(boxes, self.regions.values()):
            direct = [[box[0] <= 165+Fraction((2*x+1)*950, 360) < box[2]
                       and box[1] <= Fraction((2*y+1)*720, 240) < box[3]
                       for x in range(180)] for y in range(120)]
            np.testing.assert_array_equal(mask, direct)

    def test_known_aspect_relationship(self):
        a, v, _ = self.a.canvas(self.parent, self.image, 1.75, Fraction(133, 144))
        target = a[25:145, 25:205].copy()
        self.assertTrue(v.all())
        best, _, _ = self.a.register(self.parent, self.core, self.image, target, self.regions, Fraction(133, 144), [1.75])
        baseline, _, _ = self.a.register(self.parent, self.core, self.image, target, self.regions, Fraction(1), [1.75])
        self.assertEqual((best[0]['top'], best[0]['left']), (25, 25))
        self.assertGreater(best[0]['fit_score'], 1-1e-10)
        self.assertLess(baseline[0]['fit_score'], .99)

    def test_evaluation_changes_do_not_refit(self):
        changed = self.image.copy()
        union = self.regions['static_evaluation'] | self.regions['dynamic']
        changed[union] = 255-changed[union]
        before, scores, coverage = self.a.register(self.parent, self.core, self.image, self.image, self.regions, Fraction(1), [1.])
        after, again, cover = self.a.register(self.parent, self.core, self.image, changed, self.regions, Fraction(1), [1.])
        np.testing.assert_array_equal(scores, again)
        np.testing.assert_array_equal(coverage, cover)
        self.assertEqual([(r['top'], r['left'], r['fit_score']) for r in before], [(r['top'], r['left'], r['fit_score']) for r in after])
        for name in self.a.METRICS[1:]:
            self.assertGreater(before[0]['evaluations'][name]['score'], 1-1e-10)
            self.assertLess(after[0]['evaluations'][name]['score'], -1+1e-10)

    def test_flat_repeated_detail_and_nulls(self):
        best, scores, _ = self.a.register(self.parent, self.core, np.zeros_like(self.image), self.image, self.regions, Fraction(1), [1.])
        self.assertEqual(best, [])
        self.assertFalse(np.isfinite(scores).any())
        tile = self.rng.uniform(0, 255, (8, 8))
        repeated = np.tile(tile, (3, 3))
        scores, _ = self.core.pearson_surface(repeated, tile, np.ones_like(tile), np.ones_like(repeated))
        self.assertGreaterEqual(int((abs(scores-1) < 1e-10).sum()), 9)
        self.assertEqual(self.parent.dynamic_score(self.core, self.image, self.image, self.regions['fit'], np.zeros_like(self.image, bool))['missing_reason'], 'coverage')
        self.assertEqual(self.parent.dynamic_score(self.core, self.image*0, self.image, self.regions['fit'], np.ones_like(self.image, bool))['missing_reason'], 'variance')
        small = np.zeros_like(self.image, bool); small.flat[:31] = True
        self.assertEqual(self.parent.dynamic_score(self.core, self.image, self.image, small, np.ones_like(small))['missing_reason'], 'pixel_count')

    def test_top_two_exact_ties_use_scale_top_left(self):
        core = mock.Mock(wraps=self.core)
        s = np.full((51, 51), np.nan); s[25, 25] = s[25, 26] = s[26, 25] = .8
        core.pearson_surface.return_value = (s, np.ones_like(s))
        best, _, _ = self.a.register(self.parent, core, self.image, self.image, self.regions, Fraction(1), [1.1, 1.])
        self.assertEqual([(t['requested_scale'], t['top'], t['left']) for t in best], [(1., 25, 25), (1., 25, 26)])

    def test_rankings_ties_nearbest_missing_and_endpoints(self):
        rows = [self.row(30), self.row(0), self.row(60, score=.79, dynamic=None), {'source_index': 90, 'transforms': []}]
        ranked = self.a.rank(rows)
        self.assertEqual(ranked, self.a.rank(rows[::-1]))
        self.assertEqual(ranked['fit']['top_two'], [0, 30])
        self.assertEqual(ranked['fit']['near_best']['0.005'], [0, 30])
        self.assertEqual(ranked['fit']['near_best']['0.02'], [0, 30, 60])
        self.assertEqual([r['source_index'] for r in ranked['dynamic']['unavailable']], [60, 90])
        self.assertTrue(ranked['fit']['ranking'][0]['sample_boundary'])
        self.assertEqual(self.a.rank([{'source_index': 0, 'transforms': []}])['shortlist_union'], [])

    def test_common_support_equal_counts_unequal_sets(self):
        mask = np.ones_like(self.image, bool)
        av, bv = mask.copy(), mask.copy()
        av[:, :9] = False; bv[:, -9:] = False
        target = 255-self.image
        result = self.a.common_support(self.parent, self.core, target, mask, [(self.image, av), (target, bv)])
        self.assertFalse(result['valid_sets_equal'])
        self.assertEqual(result['baseline_pixels'], result['alternative_pixels'])
        self.assertEqual(result['intersection_pixels'], 120*162)
        self.assertEqual(result['intersection_coverage'], .9)
        self.assertAlmostEqual(result['diagnostic']['score_delta'], 2., delta=1e-12)
        equal = self.a.common_support(self.parent, self.core, self.image, mask, [(self.image, av)]*2)
        self.assertTrue(equal['valid_sets_equal'])
        self.assertEqual(equal['diagnostic']['score_delta'], 0.)

    def test_common_support_full_mask_gate_and_missing_transform(self):
        mask = np.ones_like(self.image, bool)
        av, bv = mask.copy(), mask.copy(); av[:, :20] = False; bv[:, -20:] = False
        result = self.a.common_support(self.parent, self.core, self.image, mask, [(self.image, av), (self.image, bv)])
        self.assertLess(result['intersection_coverage'], .85)
        self.assertEqual(result['diagnostic']['availability'], 'neither')
        self.assertEqual(result['diagnostic']['baseline']['missing_reason'], 'coverage')
        self.assertIsNone(result['diagnostic']['score_delta'])
        absent = self.a.common_support(self.parent, self.core, self.image, mask, None)
        self.assertIsNone(absent['valid_sets_equal'])
        self.assertIsNone(absent['intersection_coverage'])

    def test_delta_all_availability_transitions(self):
        one = {'score': .8, 'coverage': .9, 'pixels': 90, 'missing_reason': None}
        two = {'score': .9, 'coverage': 1., 'pixels': 100, 'missing_reason': None}
        null = {'score': None, 'coverage': .7, 'pixels': 70, 'missing_reason': 'coverage'}
        for a, b, label in ((one, two, 'both'), (one, null, 'baseline_only'), (null, one, 'alternative_only'), (null, null, 'neither')):
            result = self.a.delta(a, b)
            self.assertEqual(result['availability'], label)
            self.assertEqual(result['score_delta'] is not None, label == 'both')
        self.assertAlmostEqual(self.a.delta(one, two)['score_delta'], .1)
        self.assertAlmostEqual(self.a.delta(one, two)['coverage_delta'], .1)

    def test_exact_228_pair_screen_coverage_synthetic_only(self):
        keys = self.a.pair_keys()
        self.assertEqual(len(keys), 228)
        self.assertEqual(len(set(keys)), 228)
        self.assertEqual({a: sum(k[0] == a for k in keys) for a in self.a.ARMS}, {'baseline': 114, 'native_relative_aspect': 114})
        early, refs = self.maps()
        record = {'early': early, 'references': refs, 'synthetic_only': True}
        loaded = (record, [self.image]*38, [self.image]*3)
        null = ([], np.full((21, 51, 51), np.nan), np.zeros((21, 51, 51)))
        with tempfile.TemporaryDirectory(prefix='aspect-grid-') as d:
            with mock.patch.object(self.a, 'inputs', return_value=loaded) as read, mock.patch.object(self.a, 'register', return_value=null) as fit:
                result = self.a.screen(Path(d), self.parent, self.core, self.config, time.monotonic())
            self.assertEqual(read.call_count, 2)
            self.assertEqual(fit.call_count, 228)
            self.assertEqual(result['pairs'], 228)
            rows = json.loads((Path(d)/'results.json').read_text())
            self.assertEqual([(r['arm'], r['reference_index'], r['source_index']) for r in rows], keys)
            self.assertEqual(len(json.loads((Path(d)/'paired-summary.json').read_text())), 114)
            self.assertEqual(len(list(Path(d).glob('surfaces-*.npz'))), 228)
            self.assertTrue(all(r['missing_reason'] == 'all_fit_transforms_invalid' for r in rows))

    def test_input_pin_failure_precedes_module_import(self):
        with tempfile.TemporaryDirectory(prefix='aspect-pin-') as d:
            p = Path(d)/'synthetic.json'; self.a.save(p, {'synthetic': True})
            self.a.require_pins({p: self.a.pin(p)['sha256']})
            with mock.patch.object(self.a, 'FROZEN', {p: '0'*64}), mock.patch.object(self.a, 'module') as load:
                with self.assertRaises(ValueError): self.a.dependencies()
                load.assert_not_called()

    def test_selection_pts_missing_duplicate_and_path_rejection(self):
        early, refs = self.maps()
        self.assertEqual(self.a.selection(self.parent, early, refs), (early, refs))
        cases = []
        wrong = copy.deepcopy(early); wrong[0]['source_seconds_exact'] = '1'; cases.append((wrong, refs))
        wrong = copy.deepcopy(early); wrong[1]['quarter_bin'] = 0; cases.append((wrong, refs))
        wrong = copy.deepcopy(refs); wrong[0]['source_pts'] += 1; cases.append((early, wrong))
        wrong = copy.deepcopy(refs); wrong[0]['png'] = '../escape.png'; cases.append((early, wrong))
        cases.extend([(early[:-1], refs), (early+early[:1], refs)])
        for e, r in cases:
            with self.assertRaises(ValueError): self.a.selection(self.parent, e, r)

    def test_fresh_controls_and_exact_method_freeze(self):
        with tempfile.TemporaryDirectory(prefix='aspect-gate-') as d:
            p = Path(d); (p/'inherited').mkdir()
            frozen = {'synthetic': True}
            self.a.save(p/'inherited/summary.json', {'pass': True})
            self.a.save(p/'controls.json', {'pass': True, 'inherited': {'controls': 11, 'pass': True},
                        'adapter': {'tests_run': 9, 'pass': True}, 'aspect': {'tests_run': 18, 'pass': True}})
            self.a.save(p/'receipt.json', {'mode': 'controls', 'status': 'complete', 'before': frozen, 'after': frozen,
                        'products': {s: self.a.pin(p/s) for s in ('controls.json', 'inherited/summary.json')}})
            control_pin = self.a.control_gate(p, frozen)
            with self.assertRaises(ValueError): self.a.control_gate(p, {'changed': True})
            self.a.save(p/'method-freeze.json', {'schema_version': 1, 'status': 'ready_for_historical',
                        'method_state': frozen, 'controls_receipt': control_pin})
            self.a.freeze_gate(p/'method-freeze.json', frozen, control_pin)
            with self.assertRaises(ValueError): self.a.freeze_gate(p/'method-freeze.json', frozen, {'sha256': '0'*64})
            # Only temporary synthetic fixtures are deliberately changed.
            (p/'controls.json').write_text('{}')
            with self.assertRaises(ValueError): self.a.control_gate(p, frozen)

    def test_exclusive_output_and_scoped_names(self):
        with tempfile.TemporaryDirectory(prefix='aspect-output-') as d, mock.patch.object(self.a, 'HERE', Path(d)):
            for mode, name in (('controls', 'controls01'), ('screen', 'aspect01'), ('screen', 'aspect02')):
                path = self.a.output_path(mode, name); path.mkdir()
                with self.assertRaises(FileExistsError): self.a.output_path(mode, name)
            for mode, name in (('controls', '../controls01'), ('screen', 'aspect03'), ('screen', 'controls01'), ('controls', '/tmp/x')):
                with self.assertRaises(ValueError): self.a.output_path(mode, name)
            p = Path(d)/'saved.json'; self.a.save(p, {'first': True})
            before = p.read_bytes()
            with self.assertRaises(FileExistsError): self.a.save(p, {'second': True})
            self.assertEqual(p.read_bytes(), before)

    def test_runtime_and_budget_guards(self):
        with mock.patch.object(self.a.platform, 'python_version', return_value='0.0'):
            with self.assertRaises(ValueError): self.a.state(self.config)
        with tempfile.TemporaryDirectory(prefix='aspect-budget-') as d:
            with self.assertRaises(RuntimeError): self.parent.budget(Path(d), time.monotonic()-601, self.config)
            self.a.save(Path(d)/'synthetic.json', {'synthetic': True})
            config = dict(self.config, max_bytes=1)
            with self.assertRaises(RuntimeError): self.parent.budget(Path(d), time.monotonic(), config)


if __name__ == '__main__':
    unittest.main(verbosity=2)
