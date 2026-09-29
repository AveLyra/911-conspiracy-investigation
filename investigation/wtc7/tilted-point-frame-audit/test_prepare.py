#!/usr/bin/env python3
"""Synthetic-only controls for the fixed presentation adapter; no media decode."""
import argparse
import copy
from fractions import Fraction
import io
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
import prepare as p
from PIL import Image, __version__ as pillow_version


def pattern():
    # Every location recoverable from channels; no historical pixels.
    return Image.frombytes('RGB', (720, 480), bytes(
        c for y in range(480) for x in range(720)
        for c in (x % 256, y % 256, x//256 + 4*(y//256))))


def point(track, x, y, index=0, key=False):
    return {'track_id': track, 'frame_index': index, 'key': key,
            'x': x, 'y': y, 'x_saved_text': repr(x), 'y_saved_text': repr(y)}


def project_fixture():
    tracks = []
    for name, indices in p.EXPECTED.items():
        keys = list(range(360, 403, 6)) if name == 'pointmass05' else indices
        rows = []
        for ordinal, index in enumerate(indices, 1):
            coords = {}
            for axis, value in [('x', 100.25), ('y', 200.5)]:
                text = repr(value)
                coords[axis] = {'status': 'present', 'occurrences': [{'value': value,
                    'saved_text': text, 'text_sha256': p.sha(text.encode()),
                    'status': 'valid_finite', 'xml_path': f'/synthetic/{name}/{index}/{axis}'}]}
            rows.append({'entry_ordinal_one_based': ordinal, 'index': index,
                         'status': 'saved_object', 'finite_complete': True,
                         'saved_keyFrame_member': index in keys,
                         'xml_path': f'/synthetic/{name}/{index}',
                         'objects': [{'status': 'expected_class', 'finite_complete': True,
                                      'coordinates': coords}]})
        tracks.append({'track_id': name, 'saved_indices': indices.copy(),
                       'framedata_array_count': 1, 'keyFrames_array_count': 1,
                       'keyFrames': [{'values': keys.copy()}], 'xml_path': '/synthetic/'+name,
                       'framedata': [{'duplicate_indices': [], 'rows': rows}]})
    return {'pointmass_tracks': tracks}


def probe_fixture():
    return {'streams': [{'width': 720, 'height': 480, 'pix_fmt': 'yuv420p',
                        'time_base': '1/60000', 'sample_aspect_ratio': '131:144'}],
            'frames': [{'width': 720, 'height': 480, 'pix_fmt': 'yuv420p',
                        'best_effort_timestamp': 2002*i, 'pts': 2002*i} for i in range(476)]}


class RepeatedRaw:
    """Memory-light synthetic constant-YUV stream for the 476-frame loop."""
    cell = bytes(518400)
    def __len__(self): return 518400*476
    def __getitem__(self, sl):
        assert sl.step is None and sl.stop-sl.start == 518400
        return self.cell


class Controls(unittest.TestCase):
    out = None

    @classmethod
    def setUpClass(cls):
        cls.native = pattern()

    def test_rounding_integer_fraction_ties_near_ties(self):
        for x, want in [(0,0), (1,1), (1.25,1), (1.5,2), (-0.5,0),
                        (-1.5,-1), (-1.6,-2), (-0.4,0), (719.8,720),
                        (math.nextafter(0.5, 0),0), (math.nextafter(0.5,1),1),
                        (math.nextafter(-0.5, -1),-1)]:
            with self.subTest(x=x): self.assertEqual(p.nearest(x), want)

    def test_nonfinite_bool_and_nonnumeric_refused(self):
        for x in [True, False, float('nan'), float('inf'), -float('inf'), None, '2']:
            with self.subTest(x=x), self.assertRaises(ValueError): p.geometry(x, 0)
            with self.subTest(y=x), self.assertRaises(ValueError): p.geometry(0, x)

    def test_boundary_memberships_separate(self):
        for xy, continuous, cell in [((-0.4,20),False,True), ((719.8,20),True,False),
                ((20,-0.4),False,True), ((20,479.8),True,False), ((0,0),True,True),
                ((720,480),False,False), ((-50,900),False,False)]:
            g = p.geometry(*xy)
            self.assertEqual(g['original_coordinate_inside'], continuous)
            self.assertEqual(g['rounded_cell_inside'], cell)

    def test_all_crop_pixels_mask_roundtrip_and_marker(self):
        fixture = [(360,240), (0,0), (719,0), (0,479), (719,479),
                   (-0.4,25.5), (719.8,479.8), (-100,-100), (1000,800), (2.5,-1.5)]
        for x, y in fixture:
            with self.subTest(x=x,y=y):
                plain, marked, mask, g = p.crop_pair(self.native, x, y)
                # Independent arithmetic oracle: int floor via //, no producer crop.
                r = (Fraction(x)+Fraction(1,2)) // 1
                s = (Fraction(y)+Fraction(1,2)) // 1
                mask_expected = []
                for v in range(60):
                    for u in range(60):
                        valid = 0 <= r-30+u < 720 and 0 <= s-30+v < 480
                        mask_expected.append(255 if valid else 0)
                self.assertEqual(mask.tobytes(), bytes(mask_expected))
                for v in range(180):
                    for u in range(180):
                        a, b = r-30+u//3, s-30+v//3
                        expected = (a%256,b%256,a//256+4*(b//256)) if 0 <= a < 720 and 0 <= b < 480 else (255,0,255)
                        self.assertEqual(plain.getpixel((u,v)), expected)
                        arm = (v == 91 and 6 <= abs(u-91) <= 15) or (u == 91 and 6 <= abs(v-91) <= 15)
                        self.assertEqual(marked.getpixel((u,v)), (0,255,255) if arm else expected)
                self.assertEqual(mask_expected.count(255),g['valid_source_pixels'])
                self.assertEqual(marked.getpixel((91,91)),plain.getpixel((91,91)))

    def test_full_native_and_missing_track_slots(self):
        f={'index':0,'pts':17,'time_base':'1/60000','time_seconds_exact':'17/60000'}
        image, crops, slots = p.panel(self.native, f, [point('pointmass05',360,240)], True)
        self.assertEqual(image.size,(1128,648))
        self.assertEqual(image.crop((12,72,732,552)).tobytes(), self.native.tobytes())
        self.assertEqual(set(crops), {'pointmass05'})
        self.assertEqual(slots['pointmass08'], {'status':'missing_saved_row'})
        for rect in [(744,420,924,600),(936,420,1116,600)]:
            self.assertEqual(image.crop(rect).tobytes(), bytes((24,24,24))*180*180)
        for kind,rect in [('plain',(744,140,924,320)),('marked',(936,140,1116,320))]:
            self.assertEqual(image.crop(rect).tobytes(),crops['pointmass05'][kind].tobytes())

    def test_geometry_and_panel_frame_slot_rejections(self):
        f={'index':0,'pts':0,'time_base':'1/60000','time_seconds_exact':'0'}
        for points in [[point('pointmass05',1,2,index=1)],
                       [point('pointmass05',1,2),point('pointmass05',3,4)],
                       [point('wrong',1,2)], [point('pointmass05',1,2,key=1)]]:
            with self.assertRaises(ValueError):p.panel(self.native,f,points,True)
        with self.assertRaises(ValueError):p.crop_pair(Image.new('RGB',(640,480)),0,0)

    def test_exact_83_source_rows_50_frames_and_keys(self):
        rows=p.source_rows(project_fixture())
        self.assertEqual(len(rows),83)
        self.assertEqual(sorted({r['frame_index'] for r in rows}),list(range(150,445,6)))
        self.assertEqual(sum(not r['key'] for r in rows),35)
        self.assertEqual(sum(r['key'] for r in rows if r['track_id']=='pointmass05'),8)
        self.assertEqual(sum(r['key'] for r in rows if r['track_id']=='pointmass08'),40)

    def test_source_missing_duplicate_wrong_index_key_text_refused(self):
        def row(d): return d['pointmass_tracks'][0]['framedata'][0]['rows'][0]
        mutations=[lambda d:d['pointmass_tracks'].pop(),
            lambda d:d['pointmass_tracks'].append(copy.deepcopy(d['pointmass_tracks'][0])),
            lambda d:row(d).update(index=151),
            lambda d:row(d).update(index=True),
            lambda d:row(d).update(saved_keyFrame_member=True),
            lambda d:d['pointmass_tracks'][0]['framedata'][0]['rows'].pop(),
            lambda d:row(d)['objects'][0]['coordinates']['x']['occurrences'][0].update(value=True),
            lambda d:row(d)['objects'][0]['coordinates']['x']['occurrences'][0].update(saved_text='2')]
        for change in mutations:
            d=project_fixture();change(d)
            with self.assertRaises(ValueError):p.source_rows(d)

    def test_476_native_map_and_hash_loop(self):
        probe=probe_fixture();_,rows=p.held.parse_map(probe)
        baseline=[{**r,'decoded_sha256':p.sha(RepeatedRaw.cell),
                   'luma_sha256':p.sha(bytes(345600))} for r in rows]
        self.assertEqual(p.validate_map(probe,baseline)[1],rows)
        self.assertEqual(p.validate_decoded(RepeatedRaw(),rows,baseline),baseline)
        for field,value in [('pts',123),('decoded_sha256','0'*64),('luma_sha256','0'*64),('index',1)]:
            bad=copy.deepcopy(baseline);bad[0][field]=value
            with self.assertRaises(ValueError):p.validate_decoded(RepeatedRaw(),rows,bad)
        with self.assertRaises(ValueError):p.validate_decoded(b'',rows,baseline)
        probe['frames'][1]['best_effort_timestamp']=0
        with self.assertRaises(ValueError):p.validate_map(probe,baseline)

    def test_wrong_source_pin_and_helper_before_execution(self):
        path=self.out/'bad-helper.py'
        with path.open('x') as f:f.write("raise RuntimeError('MUST NOT EXECUTE')\n")
        with self.assertRaisesRegex(ValueError,'BEFORE import'):p.load_helper(path,'0'*64)
        with self.assertRaisesRegex(ValueError,'input hash mismatch'):p.require_pins({path:'0'*64})

    def test_unsafe_existing_directory_and_symlink_refusal(self):
        with patch.object(p,'HERE',self.out):
            for value in ('../a','/tmp/a','a/b','A','',None):
                with self.assertRaises(ValueError):p.output_path(value)
            (self.out/'existing').mkdir()
            with self.assertRaises(ValueError):p.output_path('existing')
            (self.out/'dangling').symlink_to(self.out/'absent')
            with self.assertRaises(ValueError):p.output_path('dangling')
            with patch.object(p.subprocess,'run') as run:
                with self.assertRaises(ValueError):p.historical('existing','0'*64)
                run.assert_not_called()

    def test_success_warning_error_timeout_diagnostics(self):
        scenarios=[('ok',subprocess.CompletedProcess(['synthetic'],0,b'abc',b''),False),
                   ('warning',subprocess.CompletedProcess(['synthetic'],0,b'abc',b'warning\n'),True),
                   ('error',subprocess.CompletedProcess(['synthetic'],1,b'',b'failed\n'),True),
                   ('timeout',subprocess.TimeoutExpired(['synthetic'],60,output=b'x',stderr=b'timed\n'),True)]
        for stem,result,fails in scenarios:
            kwargs={'side_effect':result} if isinstance(result,Exception) else {'return_value':result}
            with patch.object(p.subprocess,'run',**kwargs):
                if fails:
                    with self.assertRaises(ValueError):p.run_process(['synthetic'],self.out,stem)
                else:self.assertEqual(p.run_process(['synthetic'],self.out,stem)[0],b'abc')
            saved=json.loads((self.out/(stem+'-execution.json')).read_text())
            data=(self.out/(stem+'.stderr')).read_bytes()
            self.assertEqual(saved['stderr_bytes'],len(data))
            self.assertEqual(saved['stderr_sha256'],p.sha(data))

    def test_png_no_clobber(self):
        path=self.out/'single-pixel.png'
        p.png_save(path,Image.new('RGB',(1,1),(11,22,33)))
        before=p.pin(path)
        with self.assertRaises(FileExistsError):p.png_save(path,Image.new('RGB',(1,1),(0,0,0)))
        self.assertEqual(p.pin(path),before)


def save_fixtures(out):
    native=pattern()
    products={'synthetic-native.png':p.png_save(out/'synthetic-native.png',native)}
    fixtures=[('central', [point('pointmass05',360.5,240.25),point('pointmass08',100.5,200.5,key=True)]),
              ('boundaries',[point('pointmass05',-0.4,0),point('pointmass08',719.8,479.8,key=True)]),
              ('missing',[point('pointmass08',-100.5,-100.5,key=True)])]
    records=[]
    for name,points in fixtures:
        frame={'index':0,'pts':17,'time_base':'1/60000','time_seconds_exact':'17/60000'}
        image,crops,slots=p.panel(native,frame,points,True)
        panel_name=name+'-panel.png'
        products[panel_name]=p.png_save(out/panel_name,image)
        for track,items in crops.items():
            for kind,crop in items.items():
                n=f'{name}-{track}-{kind}.png';products[n]=p.png_save(out/n,crop)
        records.append({'name':name,'frame':frame,'points':points,'slots':slots,'panel_png':panel_name})
    p.write_json(out/'fixtures.json',{'status':'synthetic_only','pattern':'RGB(x%256,y%256,x//256+4*(y//256))',
                 'layout':p.LAYOUT,'fixtures':records,'products':products})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',required=True)
    args=parser.parse_args();out=p.output_path(args.out)
    paths=[Path(__file__),Path(p.__file__),p.HELPER,p.HERE/'PROTOCOL.md',p.HERE/'method-review.md',
           Path(sys.executable),Path(Image.__file__),Path(Image.core.__file__)]
    before=p.snapshot(paths)
    out.mkdir();Controls.out=out
    p.write_json(out/'input-receipt.json',{'argv':sys.argv,'inputs_before':before,
                 'python':platform.python_version(),'pillow':pillow_version,'synthetic_only':True})
    log=io.StringIO()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
    result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    with (out/'tests.log').open('x') as f:f.write(log.getvalue())
    if result.wasSuccessful():save_fixtures(out)
    after=p.snapshot(paths)
    stable=before==after
    p.write_json(out/'receipt.json',{'tests_run':result.testsRun,'failures':len(result.failures),
                 'errors':len(result.errors),'successful':result.wasSuccessful() and stable,
                 'inputs_before':before,'inputs_after':after,'inputs_unchanged':stable,
                 'synthetic_only':True,'historical_decode_or_view':False,
                 'products':{str(f.relative_to(out)):p.pin(f) for f in sorted(out.rglob('*'))
                             if f.is_file() and not f.is_symlink()}})
    print(log.getvalue())
    print(json.dumps({'receipt':p.pin(out/'receipt.json'),'successful':result.wasSuccessful() and stable}))
    sys.exit(0 if result.wasSuccessful() and stable else 1)
