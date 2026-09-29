"""Focused synthetic controls; no historical image access or full sweep."""
import copy
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
S = types.ModuleType('synthetic_raster_under_test')
S.__file__ = str(HERE/'raster_uncertainty.py')
exec(compile((HERE/'raster_uncertainty.py').read_bytes(), S.__file__, 'exec'), S.__dict__)


class RasterControls(unittest.TestCase):
    def test_full_cartesian_membership_without_running_sweep(self):
        rows = list(S.fixtures())
        self.assertEqual(len(rows), 112)
        self.assertEqual(len(set(k for k, _ in rows)), 112)
        self.assertEqual(len(S.CODECS)*len(rows), 560)
        self.assertEqual(set(p['color'] for _, p in rows), set(S.COLORS))
        self.assertEqual(S.ALLOWANCES, (0, 1, 2, 4))

    def test_half_up_rounding_and_endpoints(self):
        self.assertEqual(S.mixed_channel(0, 8), 128)
        self.assertEqual(S.mixed_channel(128, 8), 192)
        for c in range(256):
            self.assertEqual(S.mixed_channel(c, 0), 255)
            self.assertEqual(S.mixed_channel(c, 16), c)
        for c, n in [(True, 1), (0, True), (0, -1), (0, 17), (256, 1), (0, float('nan'))]:
            with self.assertRaises(ValueError): S.mixed_channel(c, n)

    def test_fixed_sample_counts_flat_halfphase_and_slope(self):
        # Explicit shared boundary expectations, not an unseen oracle.
        for m2, p2, x, expected in [(0, 0, 80, {47:8, 48:8}),
                                   (0, 1, 80, {48:16}), (1, 1, 16, {16:12, 17:4})]:
            image = S.render_scene(S.fixture_scene(S.params('black', 1, m2, p2, 'solid')))
            actual = {y: image.getpixel((x, y))[0] for y in range(S.HEIGHT) if image.getpixel((x, y)) != (255,255,255)}
            self.assertEqual(actual, {y:(255*(16-n)+8)//16 for y,n in expected.items()})

    def test_band_edges_domain_and_dash_edges(self):
        line = S.segment('A', 0, 0, 1, dashed=True)
        self.assertTrue(S.in_segment(16*16, 47*16+8, line))  # Lower edge included.
        self.assertFalse(S.in_segment(16*16, 48*16+8, line)) # Upper edge excluded.
        self.assertFalse(S.in_segment(16*16-1, 48*16, line))
        self.assertFalse(S.in_segment(144*16, 48*16, line))
        self.assertTrue(S.in_segment(24*16-1, 48*16, line))
        self.assertFalse(S.in_segment(24*16, 48*16, line))
        self.assertTrue(S.in_segment(32*16, 48*16, line))

    def test_exact_contrast_and_offcolor_thresholds(self):
        target = (255,0,0)
        self.assertFalse(S.candidate((255,205,205), target))
        self.assertTrue(S.candidate((255,204,204), target)) # 5A == Q.
        self.assertTrue(S.candidate((255,172,236), target)) # Per-channel residual == 32Q.
        self.assertFalse(S.candidate((255,171,237), target)) # Residual == 33Q.
        for color in S.COLORS.values():
            self.assertFalse(S.candidate((255,255,255), color))
            for n in range(17):
                pixel = tuple((n*c + (16-n)*255 + 8)//16 for c in color)
                self.assertEqual(S.candidate(pixel, color), n >= 4)

    def test_invalid_rgb_rejected_even_after_numerically_equal_valid_call(self):
        S.candidate((1,0,0), (0,0,0))
        for invalid in [(True,0,0), (1.0,0,0), (float('nan'),0,0), (256,0,0), (-1,0,0), (0,0), None]:
            with self.assertRaises(ValueError): S.candidate(invalid, (0,0,0))
            with self.assertRaises(ValueError): S.candidate((0,0,0), invalid)
        with self.assertRaises(ValueError): S.candidate((255,255,255), (255,255,255))

    def test_components_keep_disconnected_runs_and_cell_edges(self):
        self.assertEqual(S.row_runs([]), [])
        self.assertEqual(S.row_runs([1,2,4,7,8,9]), [[1,3],[4,5],[7,10]])
        for rows in [[1,1],[2,1],[-1],[96],[True],None]:
            with self.assertRaises(ValueError): S.row_runs(rows)

    def test_column_truth_and_all_allowances_without_nearest_run_selection(self):
        p = S.params('blue',1,1,1,'dashed')
        single = S.column_record(16,[16,17],p)
        self.assertEqual(single['truth_centerline_y2'],[33,34])
        self.assertEqual(single['envelope_y'],[16,18])
        for a in (0,1,2,4):
            self.assertEqual(single['allowances'][str(a)], {'envelope_y':[16-a,18+a],'width':2+2*a,'covered':True})
        ambiguous = S.column_record(16,[1,16,17],p)
        self.assertEqual(ambiguous['status'],'ambiguous')
        self.assertIsNone(ambiguous['envelope_y'])
        self.assertEqual(ambiguous['runs_y'],[[1,2],[16,18]])
        self.assertTrue(all(r['covered'] is None for r in ambiguous['allowances'].values()))
        self.assertEqual(S.column_record(16,[],p)['status'],'missing')
        gap = S.column_record(24,[16],p)
        self.assertFalse(gap['truth_support']); self.assertIsNone(gap['truth_centerline_y2'])
        self.assertIsNone(gap['allowances']['4']['covered'])
        fail = S.column_record(16,[14],p)
        self.assertFalse(fail['allowances']['0']['covered'])
        self.assertTrue(fail['allowances']['2']['covered'])

    def test_blank_and_gap_leakage_are_reported_not_bridged(self):
        p = S.params('red',1,0,0,'dashed')
        image = S.Image.new('RGB',(160,96),'white')
        result = S.analyze(image,p)
        self.assertEqual(len(result['columns']),128)
        self.assertEqual(len(result['summary']['true_status_columns']['missing']),64)
        self.assertEqual(result['summary']['gap_candidate_columns'],[])
        image.putpixel((24,48),(255,0,0))
        result = S.analyze(image,p)
        self.assertEqual(result['summary']['gap_candidate_columns'],[24])
        self.assertEqual(result['columns'][8]['runs_y'],[[48,49]])
        self.assertFalse(result['columns'][8]['truth_support'])

    def test_codecs_preserve_shape_and_png_is_lossless(self):
        base = S.render_scene(S.fixture_scene(S.params('cyan',3,0,1,'solid')))
        for codec in S.CODECS:
            data, decoded, diagnostics = S.encode_decode(base,codec)
            self.assertEqual(decoded.size,(160,96)); self.assertEqual(decoded.mode,'RGB')
            self.assertEqual(diagnostics,[])
            again, repeated, _ = S.encode_decode(base,codec)
            self.assertEqual(data,again); self.assertEqual(decoded.tobytes(),repeated.tobytes())
            if codec == 'png': self.assertEqual(base.tobytes(),decoded.tobytes())

    def test_three_distinct_latent_pairs_all_five_codecs(self):
        pairs = list(S.ambiguity_pairs()); self.assertEqual(len(pairs),3)
        for identifier,(a,b) in pairs:
            self.assertNotEqual(a,b)
            # Difference must involve actual geometry/style/masking, not prose alone.
            self.assertNotEqual((a['segments'],a['white_masks']),(b['segments'],b['white_masks']))
            left,right = S.render_scene(a),S.render_scene(b)
            self.assertEqual(left.tobytes(),right.tobytes(),identifier)
            for codec in S.CODECS:
                le,ld,lw = S.encode_decode(left,codec); re,rd,rw = S.encode_decode(right,codec)
                self.assertEqual(le,re); self.assertEqual(ld.tobytes(),rd.tobytes())
                self.assertEqual(lw+rw,[])

    def test_invalid_geometry_images_and_nonfinite_inputs(self):
        for vals in [('black',True,0,0,'solid'),('black',1,float('nan'),0,'solid'),('black',1,0,True,'solid'),('white',1,0,0,'solid'),('black',1,0,0,'unknown')]:
            with self.assertRaises(ValueError): S.params(*vals)
        base = S.fixture_scene(S.params('black',1,0,0,'solid'))
        for field,value in [('m2',True),('start',float('nan')),('end',16),('w',None),('dashed',1)]:
            scene = copy.deepcopy(base); scene['segments'][0][field]=value
            with self.assertRaises(ValueError): S.render_scene(scene)
        scene=copy.deepcopy(base);scene['white_masks']=[[0,0,True,96]]
        with self.assertRaises(ValueError): S.render_scene(scene)
        for image in [S.Image.new('L',(160,96)),S.Image.new('RGB',(159,96))]:
            with self.assertRaises(ValueError): S.analyze(image,S.params('black',1,0,0,'solid'))
            with self.assertRaises(ValueError): S.encode_decode(image,'png')
        with self.assertRaises(ValueError): S.column_record(True,[],S.params('black',1,0,0,'solid'))

    def test_no_arbitrary_output_name_and_exclusive_write(self):
        for name in ['../synthetic-run01','synthetic-run03','/tmp/other',None]:
            with self.assertRaises(ValueError): S.run(name)
        with tempfile.TemporaryDirectory(prefix='raster-controls-') as folder:
            path=Path(folder)/'existing';path.write_bytes(b'preserved')
            with self.assertRaises(FileExistsError): S.write_new(path,b'replacement')
            self.assertEqual(path.read_bytes(),b'preserved')
            (Path(folder)/'synthetic-run01').mkdir()
            with patch.object(S,'HERE',Path(folder)), patch.object(S,'input_pins',return_value={}):
                with self.assertRaises(FileExistsError): S.run('synthetic-run01')
            self.assertEqual(list((Path(folder)/'synthetic-run01').iterdir()),[])

    def test_protocol_mismatch_before_output_and_preserved_execution_failure(self):
        with patch.object(S,'PROTOCOL_SHA','0'*64):
            with self.assertRaisesRegex(ValueError,'protocol_pin_mismatch'): S.input_pins()
        with tempfile.TemporaryDirectory(prefix='raster-failure-control-') as folder:
            with patch.object(S,'HERE',Path(folder)), patch.object(S,'input_pins',return_value={}), patch.object(S,'fixtures',side_effect=RuntimeError('synthetic_control_failure')):
                with self.assertRaisesRegex(RuntimeError,'synthetic_control_failure'): S.run('synthetic-run01')
            result=json.loads((Path(folder)/'synthetic-run01/failure.json').read_text())
            self.assertEqual(result['error_type'],'RuntimeError')
            self.assertIn('runtime.json',result['completed_products'])
            self.assertFalse((Path(folder)/'synthetic-run01/manifest.json').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
