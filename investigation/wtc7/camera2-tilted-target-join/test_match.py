import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from PIL import Image

spec = importlib.util.spec_from_file_location('target_match', Path(__file__).with_name('match.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class Controls(unittest.TestCase):
    def test_scalar_sad_signed_brightness(self):
        q = np.array([0, 20, 80, 255], dtype=np.uint8)
        c = np.array([q, [255, 0, 30, 0]], dtype=np.uint8)
        self.assertEqual(m.absolute_sums(c, q).tolist(), [0, sum(abs(int(a)-int(b)) for a,b in zip(c[1], q))])
        metrics = m.inherited_metrics()
        for offset in (-5, 5):
            a, r = metrics([[30+offset, 50+offset, 80+offset]], [30, 50, 80])
            self.assertEqual(a.tolist(), [5.0]); self.assertAlmostEqual(r[0], 1)

    def test_local_change_constant_and_blend(self):
        metrics = m.inherited_metrics()
        a, r = metrics([[10, 20, 30, 80]], [10, 20, 30, 40])
        self.assertEqual(a.tolist(), [10]); self.assertLess(r[0], 1)
        _, r = metrics([[1, 1], [0, 2]], [1, 1]); self.assertTrue(np.isnan(r).all())
        # Averaged query between adjacent recordings has equal scores: no unique exposure.
        sad = m.absolute_sums(np.array([[0, 20], [20, 40]], dtype=np.uint8), np.array([10, 30], dtype=np.uint8))
        self.assertEqual(m.rank_and_retain(sad, [12, 13])['minimum_ties'], [12, 13])

    def test_rank_cut_ties_and_neighbors(self):
        r = m.rank_and_retain([0, 1, 2, 3, 4, 4, 8, 9], list(range(8)))
        self.assertEqual(r['rank5_with_ties'], list(range(6)))
        self.assertEqual(r['shortlist_with_neighbors'], list(range(7)))
        self.assertTrue(r['boundary_minimum'])
        r = m.rank_and_retain([0]*476, list(range(476)))
        self.assertEqual(r['minimum_ties'], list(range(476)))
        self.assertEqual(r['shortlist_with_neighbors'], list(range(476)))

    def test_ordering_no_repair(self):
        self.assertEqual(m.ordering_flags([4, 4, 3]), {'repeated_pairs': [[4, 4]], 'reversed_pairs': [[4, 3]]})

    def test_masks_and_excluded_perturbation(self):
        source = np.zeros((480, 720), dtype=np.uint8)
        changed = source.copy(); changed[:, :350] = 255
        query = np.zeros((480, 640), dtype=np.uint8)
        altered_query = query.copy(); altered_query[:, :300] = 255
        expected = {'right_half': 8736, 'target_right': 2560, 'right_background': 1320}
        for branch in m.BRANCHES:
            a, b = m.sampled(source, branch), m.sampled(changed, branch)
            for name, rect in m.REGIONS.items():
                mask = m.mask(rect)
                self.assertEqual(int(mask.sum()), expected[name])
                np.testing.assert_array_equal(a[mask], b[mask])
                np.testing.assert_array_equal(query[::4, ::4][mask], altered_query[::4, ::4][mask])
                self.assertEqual(m.absolute_sums(b[mask][None, :], query[::4, ::4][mask]).tolist(), [0])
            included = source.copy(); included[:, 560:710] = 255
            for rect in m.REGIONS.values():
                mask = m.mask(rect)
                if rect != m.REGIONS['target_right']:
                    self.assertGreater(int(m.absolute_sums(m.sampled(included, branch)[mask][None, :], query[::4, ::4][mask])[0]), 0)

    def test_width_grid_known_lookup(self):
        native = np.tile((np.arange(720)%256).astype(np.uint8), (480, 1))
        got = m.sampled(native, 'nearest')
        xs = np.floor((np.arange(0, 640, 4)+0.5)*720/640).astype(int)
        np.testing.assert_array_equal(got[0], native[0, xs])
        rows = np.tile((np.arange(480)%256).astype(np.uint8)[:, None], (1, 720))
        for branch in m.BRANCHES:
            np.testing.assert_array_equal(m.sampled(rows, branch)[:, 0], rows[::4, 0])

    def test_static_region_conflict_retained(self):
        a = m.rank_and_retain([0, 0, 0, 0, 0, 0], list(range(6)))
        b = m.rank_and_retain([5, 4, 3, 2, 1, 0], list(range(6)))
        self.assertEqual(a['minimum_ties'], list(range(6)))
        self.assertNotEqual(a['minimum'], b['minimum'])

    def test_bad_inputs(self):
        for c,q in [([[1]], [1]), (np.array([[1]], dtype=np.uint8), np.array([], dtype=np.uint8))]:
            with self.assertRaises(ValueError): m.absolute_sums(c, q)
        for sums, ids in [([0,1],[1,1]), ([0],[1]), ([0,1],[1,2,3])]:
            with self.assertRaises(ValueError): m.rank_and_retain(sums, ids)
        for scores in ([0.5, 1], [False, 1], [np.bool_(False), 1], [-1, 1], [float('nan'), 1]):
            with self.assertRaises(ValueError): m.rank_and_retain(scores, [0, 1])
        with self.assertRaises(ValueError): m.sampled(np.zeros((480,640), dtype=np.uint8), 'nearest')

    def test_file_guards(self):
        with tempfile.TemporaryDirectory(prefix='target-join-test-') as tmp:
            tmp = Path(tmp)
            with patch.object(m, 'HERE', tmp):
                for name in ('../bad', '/tmp/escape', 'two words'):
                    with self.assertRaises(ValueError): m.safe_dir(name)
                (tmp/'exists').mkdir()
                with self.assertRaises(ValueError): m.safe_dir('exists')
                with self.assertRaises(ValueError): m.safe_dir('missing', True)
            png = tmp/'small.png'; Image.fromarray(np.zeros((2,2), dtype=np.uint8)).save(png)
            with self.assertRaises(ValueError): m.read_native(png, '0'*64, '0'*64, (2,2))
            with self.assertRaises(ValueError): m.read_native(png, m.sha(png), '0'*64, (3,3))
            with self.assertRaises(ValueError): m.read_native(png, m.sha(png), '0'*64, (2,2))
            tiff = tmp/'other.png'; Image.fromarray(np.zeros((2,2), dtype=np.uint8)).save(tiff, format='TIFF')
            with self.assertRaises(ValueError): m.read_native(tiff, m.sha(tiff), m.hashlib.sha256(bytes(4)).hexdigest(), (2,2))


if __name__ == '__main__':
    unittest.main(verbosity=2)
