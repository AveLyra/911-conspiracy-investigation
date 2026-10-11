"""Synthetic-only adapter controls. No historical media is opened or decoded."""
from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import platform
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

import numpy as np
from PIL import Image

import pilot as p


def fixture(root, count=189):
    """Fake source bytes and invented PNGs; never a historical/video fixture."""
    stage = root/'stage2'
    directory = stage/'run01/vince-clip3'
    (directory/'native').mkdir(parents=True)
    (stage/'raw').mkdir()
    source = stage/'raw/clip3-attempt1.avi'
    source.write_bytes(b'synthetic bytes, not an AVI')
    indices = [(j*(count-1)+7)//8 for j in range(9)]
    rows = []
    for ordinal, index in enumerate(indices, 1):
        image = Image.new('RGB', (720, 480), (index % 256, ordinal, 23))
        path = directory/f'native/frame-{ordinal:06d}.png'
        image.save(path)
        rows.append(dict(file=f'native/frame-{ordinal:06d}.png', source_index=index, pts=index,
            time_base=p.TIME_BASE, pts_seconds_exact=str(index*Fraction(p.TIME_BASE)), width=720, height=480,
            sample_aspect_ratio='8:9', interlaced_frame=1, top_field_first=0,
            png_sha256=p.sha(path), rgb_sha256=hashlib.sha256(image.tobytes()).hexdigest()))
    src = dict(id='vince-clip3', path=str(source.resolve()), sha256=p.sha(source),
               bytes=source.stat().st_size, count=count, indices=indices)
    write_json(stage/'run01/manifest.input.json', dict(schema='late-fire-sequence-v1', sources=[src]))
    manifest_sha = p.sha(stage/'run01/manifest.input.json')
    identity = dict(bytes=src['bytes'], sha256=src['sha256'])
    receipt = dict(schema='late-fire-sequence-v1', source=src, reasons=[],
        pins=dict(manifest_sha256=manifest_sha, code_sha256=p.SAMPLER_SHA),
        source_identity=dict(before=identity, after=identity, status='matched_before_and_after'),
        structure='inventory_and_products_checked',
        admission='descriptive_candidate_pending_independent_and_human_review', scientific_or_human_acceptance=False,
        probe_diagnostics=dict(status='clean', rejected=[]), decode_diagnostics=dict(status='clean', rejected=[]))
    probe = dict(streams=[dict(time_base=p.TIME_BASE)], frames=[dict(pts=index, width=720, height=480,
        sample_aspect_ratio='8:9', interlaced_frame=1, top_field_first=0) for index in range(count)])
    for name, value in (('frames.json', rows), ('receipt.json', receipt), ('probe.stdout', probe)):
        write_json(directory/name, value)
    spec = dict(clip=3, stage=2, count=count, bytes=src['bytes'], source_sha256=src['sha256'],
        frames_sha256=p.sha(directory/'frames.json'), receipt_sha256=p.sha(directory/'receipt.json'),
        manifest_sha256=manifest_sha)
    return spec, directory


def write_json(path, value):
    # Generated synthetic fixture edits are confined to TemporaryDirectory.
    path.write_bytes(p.json_bytes(value))


class AdapterControls(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng(20261004)

    def test_native_dimension_masks(self):
        for size in ((705, 480), (706, 457)):
            box = [35, 40, 300, 350]
            actual = p.mask_for([box], size)
            direct = np.array([[box[0] <= (x+.5)*size[0]/180 < box[2] and
                                box[1] <= (y+.5)*size[1]/120 < box[3]
                                for x in range(180)] for y in range(120)])
            np.testing.assert_array_equal(actual, direct)
        self.assertFalse(np.array_equal(p.mask_for([[0, 0, 705, 160]], (705, 480)),
                                       p.mask_for([[0, 0, 705, 160]], (706, 457))))

    def test_invalid_masks(self):
        for boxes in ([], [[0, 0, 0, 3]], [[0, 0, 800, 10]], [[0, 0, 10.0, 10]]):
            with self.assertRaises(ValueError): p.mask_for(boxes, (705, 480))
        image = np.ones((120, 180))
        mask = np.ones_like(image, dtype=bool)
        with self.assertRaisesRegex(ValueError, 'overlapping'): p.register(image, image, mask, mask)

    def test_parity_measured_rows(self):
        raster = np.zeros((480, 720, 3), np.uint8)
        raster[::2] = 27
        raster[1::2] = 221
        arms = p.representations(Image.fromarray(raster))
        self.assertEqual(tuple(arms), p.ARMS)
        np.testing.assert_array_equal(arms['even'], np.full((120, 180), 27))
        np.testing.assert_array_equal(arms['odd'], np.full((120, 180), 221))
        for im in (Image.new('L', (720, 480)), Image.new('RGB', (720, 478))):
            with self.assertRaises(ValueError): p.representations(im)

    def test_excluded_bottom_invariance_all_39_scale_arms(self):
        raster = self.rng.integers(0, 256, (480, 720, 3), dtype=np.uint8)
        left, right = raster.copy(), raster.copy()
        left[360:] = 0
        right[360:] = 255
        a, b = p.representations(Image.fromarray(left)), p.representations(Image.fromarray(right))
        working_valid = p.working_validity()
        self.assertEqual(int(working_valid.sum()), 88*180)
        for arm in p.ARMS:
            np.testing.assert_array_equal(a[arm][working_valid], b[arm][working_valid])
            self.assertTrue(np.any(a[arm][~working_valid] != b[arm][~working_valid]))
            for scale in p.core.SCALES:
                ca, va, ta = p.guarded_canvas(a[arm], scale)
                cb, vb, tb = p.guarded_canvas(b[arm], scale)
                np.testing.assert_array_equal(va, vb)
                np.testing.assert_array_equal(ca[va], cb[vb])
                self.assertEqual(ta, tb)
                self.assertEqual(ta['raster_width'], round(180*scale))
                self.assertEqual(ta['raster_height'], round(120*scale))

    def test_guard_nearest_mask_and_two_boundary_rows(self):
        for scale in p.core.SCALES:
            _, valid, t = p.guarded_canvas(np.zeros((120, 180)), scale)
            sw, sh = t['raster_width'], t['raster_height']
            expected = np.array(Image.fromarray(p.working_validity()).resize((sw, sh), Image.Resampling.NEAREST))
            expected[np.flatnonzero(expected.any(axis=1))[-2:]] = False
            full = np.zeros((170, 230), bool)
            x, y = t['canvas_x'], t['canvas_y']
            full[y:y+sh, x:x+sw] = expected
            np.testing.assert_array_equal(valid, full)

    def test_flat_and_nonfinite(self):
        static = p.mask_for([[20, 20, 80, 70]], (180, 120))
        dynamic = p.mask_for([[100, 20, 160, 70]], (180, 120))
        flat = np.full((120, 180), 35.)
        best, scores, overlap = p.register(flat, flat, static, dynamic)
        self.assertEqual(best, [])
        self.assertEqual(scores.shape, (13, 51, 51))
        self.assertFalse(np.isfinite(scores).any())
        self.assertTrue(np.isfinite(overlap).all())
        for value in (np.nan, np.inf, -np.inf):
            bad = flat.copy(); bad[0, 0] = value
            with self.assertRaises(ValueError): p.register(bad, flat, static, dynamic)

    def test_count_and_strict_variance_boundary(self):
        vector = np.arange(32, dtype=float).reshape(4, 8)
        mask = np.ones_like(vector, bool)
        with patch.object(p.core.np, 'dot', return_value=32*1e-8):
            self.assertIsNone(p.core.scalar_pearson(vector, vector, mask))
        mask.flat[0] = False
        self.assertIsNone(p.core.scalar_pearson(vector, vector, mask))
        # Exact synthetic raw moments exercise the surface's strict > convention.
        moments = [np.array([[32.]]), np.array([[0.]]), np.array([[32*1e-8]]),
                   np.array([[0.]]), np.array([[32*1e-8]]), np.array([[32*1e-8]])]
        with patch.object(p.core, 'correlate_valid', side_effect=moments):
            score, _ = p.core.pearson_surface(vector, vector, np.ones_like(vector), np.ones_like(vector))
        self.assertTrue(np.isnan(score[0, 0]))

    def test_static_fit_does_not_refit_dynamic(self):
        scene = self.rng.integers(20, 230, (120, 180), dtype=np.uint8).astype(float)
        static = p.mask_for([[15, 15, 75, 65]], (180, 120))
        dynamic = p.mask_for([[100, 15, 160, 65]], (180, 120))
        changed = scene.copy(); changed[dynamic] = 255-scene[dynamic]
        same, s0, c0 = p.register(scene, scene, static, dynamic)
        different, s1, c1 = p.register(scene, changed, static, dynamic)
        np.testing.assert_array_equal(s0, s1)
        np.testing.assert_array_equal(c0, c1)
        self.assertEqual((same[0]['dx'], same[0]['dy'], same[0]['requested_scale']), (0, 0, 1.))
        self.assertAlmostEqual(same[0]['static_score'], 1, places=10)
        self.assertAlmostEqual(same[0]['dynamic_score'], 1, places=10)
        self.assertAlmostEqual(different[0]['dynamic_score'], -1, places=10)
        for a, b in zip(same, different):
            self.assertEqual({k: v for k, v in a.items() if k != 'dynamic_score'},
                             {k: v for k, v in b.items() if k != 'dynamic_score'})

    def test_repeated_geometry_multiple_aliases(self):
        tile = self.rng.integers(20, 230, (8, 8)).astype(float)
        repeated = np.tile(tile, (3, 3))
        score, _ = p.core.pearson_surface(repeated, tile, np.ones_like(tile), np.ones_like(repeated))
        self.assertGreaterEqual(int(np.sum(np.abs(score-1) < 1e-10)), 9)

    def test_exact_transform_ties(self):
        static = p.mask_for([[15, 15, 75, 65]], (180, 120))
        dynamic = p.mask_for([[100, 15, 160, 65]], (180, 120))
        scores = np.full((51, 51), np.nan); scores[4, 8] = scores[4, 7] = scores[5, 0] = .8
        with patch.object(p.core, 'pearson_surface', return_value=(scores, np.ones_like(scores))):
            best, _, _ = p.register(np.ones((120, 180)), np.ones((120, 180)), static, dynamic)
        self.assertEqual([(b['requested_scale'], b['top'], b['left']) for b in best], [(.85, 4, 7), (.85, 4, 8)])

    def test_summary_separate_groups_paired_shortlist_invalid_and_ties(self):
        rows = []
        for target in ('143', '142'):
            for clip in (3, 7):
                for arm in p.ARMS:
                    for index, static, dynamic in ((9, .9, .8), (1, .9, .798), (4, .887, .9)):
                        rows.append(dict(target=target, clip=clip, arm=arm,
                            paired=(target, clip) in (('143', 3), ('142', 7)), source_index=index,
                            best=[dict(static_score=static, dynamic_score=dynamic)]))
        # Unique cross-only leader may appear in sensitivity sets, never shortlist.
        rows.append(dict(target='143', clip=7, arm='full', paired=False, source_index=999,
                         best=[dict(static_score=1., dynamic_score=1.)]))
        for row in rows:
            if row['target'] == '142' and row['clip'] == 3 and row['arm'] == 'odd': row['best'] = []
        result = p.summarize(rows)
        self.assertEqual(len(result['groups']), 24)
        self.assertNotIn(dict(clip=7, source_index=999), result['shortlist'])
        group = next(g for g in result['groups'] if (g['target'], g['clip'], g['arm'], g['metric']) ==
                     ('143', 3, 'full', 'static_score'))
        self.assertEqual([r['source_index'] for r in group['ranked']], [1, 9, 4])
        self.assertEqual(group['epsilon_sets'], {'0.005': [1, 9], '0.01': [1, 9], '0.02': [1, 4, 9]})
        invalid = [g for g in result['groups'] if g['best_score'] is None]
        self.assertEqual(len(invalid), 2)
        self.assertTrue(all(g['reason'] and all(v == [] for v in g['epsilon_sets'].values()) for g in invalid))
        self.assertEqual(p.json_bytes(result), p.json_bytes(p.summarize(list(reversed(rows)))))

    def test_create_only_caps_and_deterministic_arrays(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            a, b = p.Output(root/'a'), p.Output(root/'b')
            for output in (a, b): output.npz('arrays.npz', x=np.arange(20), valid=p.working_validity())
            self.assertEqual((a.path/'arrays.npz').read_bytes(), (b.path/'arrays.npz').read_bytes())
            with self.assertRaises(FileExistsError): a.json('arrays.npz', {})
            with self.assertRaises(FileExistsError): p.Output(root/'a')
            tiny = p.Output(root/'tiny', byte_cap=1024**2+128)
            with self.assertRaisesRegex(ValueError, 'byte cap'): tiny.write('large', b'x'*129)
            tiny.json('failure.json', dict(status='failed'), terminal=True)
            with patch.object(p.time, 'monotonic', return_value=tiny.started+241):
                with self.assertRaisesRegex(ValueError, 'time cap'): tiny.check()

    def test_pipeline_108_comparisons_wiring_synthetic_mock_scores(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            spec, directory = fixture(root)
            frames = p.verify_clip(spec, root, {})
            frames += [dict(r, clip=7) for r in frames]
            targets = {t: dict(paired_clip=c, arrays=(None, None, None)) for t, c in (('143', 3), ('142', 7))}
            scores, coverage = np.full((13, 51, 51), np.nan), np.zeros((13, 51, 51))
            with patch.object(p, 'register', return_value=([], scores, coverage)) as register:
                results = p.comparisons(frames, targets, p.Output(root/'output'))
            self.assertEqual(register.call_count, 108)
            self.assertEqual(len({r['surfaces'] for r in results}), 108)
            self.assertEqual(sum(r['paired'] for r in results), 54)
            self.assertEqual(len(p.summarize(results)['groups']), 24)
            self.assertEqual(p.summarize(results)['shortlist'], [])


class IntegrityControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.spec, self.directory = fixture(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def verify(self):
        return p.verify_clip(self.spec, self.root, {})

    def change_frames(self, mutate):
        rows = p.load(self.directory/'frames.json')
        mutate(rows)
        write_json(self.directory/'frames.json', rows)
        self.spec['frames_sha256'] = p.sha(self.directory/'frames.json')

    def test_source_manifest_and_both_index_lists(self):
        rows = self.verify()
        self.assertEqual([r['source_index'] for r in rows], [0, 24, 47, 71, 94, 118, 141, 165, 188])
        with tempfile.TemporaryDirectory() as other:
            spec, _ = fixture(Path(other), 1128)
            rows = p.verify_clip(spec, Path(other), {})
        self.assertEqual([r['source_index'] for r in rows], [0, 141, 282, 423, 564, 705, 846, 987, 1127])
        self.assertEqual(rows[5]['source_index'], 705)  # ceil(704.375), not nearest rounding

    def test_source_hash_mismatch(self):
        (self.root/'stage2/raw/clip3-attempt1.avi').write_bytes(b'different synthetic source')
        with self.assertRaisesRegex(ValueError, 'hash mismatch'): self.verify()

    def test_frame_manifest_pin_mismatch(self):
        with (self.directory/'frames.json').open('ab') as stream: stream.write(b' ')
        with self.assertRaisesRegex(ValueError, 'hash mismatch'): self.verify()

    def test_missing_frame(self):
        self.change_frames(lambda rows: rows.pop())
        with self.assertRaisesRegex(ValueError, 'missing/duplicate'): self.verify()

    def test_duplicate_frame(self):
        self.change_frames(lambda rows: rows.__setitem__(1, rows[0]))
        with self.assertRaisesRegex(ValueError, 'missing/duplicate'): self.verify()

    def test_pts_join(self):
        self.change_frames(lambda rows: rows[1].update(pts=25))
        with self.assertRaisesRegex(ValueError, 'PTS join'): self.verify()

    def test_rgb_hash_join(self):
        self.change_frames(lambda rows: rows[0].update(rgb_sha256='0'*64))
        with self.assertRaisesRegex(ValueError, 'RGB hash'): self.verify()

    def test_png_hash_join(self):
        self.change_frames(lambda rows: rows[0].update(png_sha256='0'*64))
        with self.assertRaisesRegex(ValueError, 'hash mismatch'): self.verify()

    def test_reject_non_rgb_png(self):
        path = self.directory/'native/frame-000001.png'
        Image.new('L', (720, 480)).save(path)
        self.change_frames(lambda rows: rows[0].update(png_sha256=p.sha(path)))
        with self.assertRaisesRegex(ValueError, 'PNG format'): self.verify()

    def test_probe_pts_mismatch(self):
        path = self.directory/'probe.stdout'
        probe = p.load(path); probe['frames'][17]['pts'] = 16
        write_json(path, probe)
        with self.assertRaisesRegex(ValueError, 'probe frame identity'): self.verify()

    def test_manifest_source_mismatch(self):
        path = self.root/'stage2/run01/manifest.input.json'
        value = p.load(path); value['sources'][0]['bytes'] += 1
        write_json(path, value)
        self.spec['manifest_sha256'] = p.sha(path)
        with self.assertRaisesRegex(ValueError, 'source manifest join'): self.verify()

    def test_strict_json(self):
        path = self.root/'invalid.json'
        for text in ('{"a":1,"a":2}', '{"a":NaN}'):
            path.write_text(text)
            with self.assertRaises(ValueError): p.load(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, help='New synthetic-control directory; never overwrite')
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(exist_ok=False)
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    with (output/'tests.log').open('x') as stream: stream.write(log.getvalue())
    summary = dict(scope='Synthetic adapter controls only; historical media not opened, decoded or scored',
        argv=sys.argv, pilot_sha256=p.sha(p.__file__), tests_sha256=p.sha(__file__), core_sha256=p.CORE_SHA,
        python=platform.python_version(), numpy=np.__version__, pillow=Image.__version__,
        tests_run=result.testsRun, failures=[str(t) for t, _ in result.failures],
        errors=[str(t) for t, _ in result.errors], skipped=[str(t) for t, _ in result.skipped],
        status='passed' if result.wasSuccessful() and not result.skipped else 'failed',
        log_sha256=p.sha(output/'tests.log'))
    with (output/'summary.json').open('xb') as stream: stream.write(p.json_bytes(summary))
    print(log.getvalue(), end='')
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
