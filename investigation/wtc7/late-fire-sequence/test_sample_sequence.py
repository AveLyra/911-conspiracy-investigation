"""Finite synthetic/saved-log controls; never decodes historical footage."""
import argparse
import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from PIL import Image
import sample_sequence as m

OLD = Path(__file__).resolve().parent.parent / 'late-fire-catalog-join'
ARTIFACTS = None
CONTROL = OLD / 'control01/synthetic.avi'
CONTROL_SHA = '03faf8b842dbec9ea7358b91f3cb0097a40a1b0719696b698025a4b79599b8c6'
DOC = json.loads((OLD / 'control01/guess-off/probe.stdout').read_bytes())


def item():
    return {'id': 'synthetic', 'path': str(CONTROL), 'sha256': CONTROL_SHA,
            'bytes': 881930, 'count': 125, 'indices': [0, 60, 120, 124]}


def log_for(dest):
    raw = (OLD / 'control01/guess-off/decode.stderr').read_text()
    old = OLD / 'control01/guess-off/native/frame-%06d.png'
    return raw.replace(str(old), str(dest / 'native/frame-%06d.png')).encode()


class Controls(unittest.TestCase):
    def destination(self, suffix=''):
        return ARTIFACTS / (self._testMethodName + suffix)

    def test_manifest_and_explicit_indices(self):
        m.validate_manifest({'schema': m.SCHEMA, 'sources': [item()]})
        for indices in [[], [0, 0], [60, 0], [-1], [125], [True], [1.0]]:
            value = item(); value['indices'] = indices
            with self.subTest(indices=indices), self.assertRaises(m.Refusal):
                m.validate_source(value)
        value = item(); value['path'] = 'relative.avi'
        with self.assertRaises(m.Refusal):m.validate_source(value)
        with self.assertRaises(m.Refusal):m.validate_manifest({'schema': m.SCHEMA, 'sources': [item(), item()]})

    def test_inventory_negatives(self):
        m.inventory(DOC, 125)
        with self.assertRaises(m.Refusal):m.inventory(DOC, 124)
        for field, value in [('pts', None), ('pts', True), ('pts', 0), ('width', 97)]:
            bad = copy.deepcopy(DOC);bad['frames'][1][field] = value
            with self.subTest(field=field,value=value), self.assertRaises(m.Refusal):m.inventory(bad,125)
        bad=copy.deepcopy(DOC);del bad['frames'][0]['pts']
        with self.assertRaises(m.Refusal):m.inventory(bad,125)
        bad=copy.deepcopy(DOC);bad['streams'][0]['time_base']='0/30'
        with self.assertRaises(m.Refusal):m.inventory(bad,125)

    def test_saved_clean_and_refused_logs(self):
        for rel in ['control01/guess-off', 'run01/cbs-net-dub5-15']:
            d=OLD/rel; r=json.loads((d/'receipt.json').read_bytes())
            result=m.decode_diagnostics((d/'decode.stderr').read_bytes(), r['source'], d/'native/frame-%06d.png')
            self.assertEqual(result['status'],'clean',result)
        d=OLD/'run01/cbs-net-dub6-44';r=json.loads((d/'receipt.json').read_bytes())
        self.assertEqual(m.probe_diagnostics((d/'probe.stderr').read_bytes())['status'],'refused')
        self.assertEqual(m.decode_diagnostics((d/'decode.stderr').read_bytes(),r['source'],d/'native/frame-%06d.png')['status'],'refused')

    def test_decode_grammar_injections(self):
        dest=self.destination();raw=log_for(dest)
        injections=[b'[warning] warning',b'[error] error',b'[fatal] fatal',b'[panic] panic',
            b'untagged diagnostic',b'[info] ERROR: corrupt',b'[info]     unknown : warning',
            b'[info]     encoder : Lavf61.7.100 extra',b'[info] [info] duplicated',
            b'[unknown @ 0x123] [info] config out time_base: 0/0, frame_rate: 0/0',
            b'   ',b'\r',b'\x00',b'\t',b'\x7f']
        for extra in injections:
            with self.subTest(extra=extra):
                self.assertEqual(m.decode_diagnostics(raw+extra+b'\n',CONTROL,dest/'native/frame-%06d.png')['status'],'refused')
        with self.assertRaises(UnicodeDecodeError):m.decode_diagnostics(raw+b'\xff',CONTROL,dest/'native/frame-%06d.png')
        self.assertEqual(m.probe_diagnostics(b'\n')['status'],'refused')

    def test_showinfo_and_cardinality(self):
        dest=self.destination();raw=log_for(dest);frames,stream,tb=m.inventory(DOC,125)
        m.check_showinfo(raw,frames,[0,60,120,124],tb)
        final=b'[info] frame=    4 fps=0.0 q=-0.0 Lsize=N/A time=00:00:00.00 bitrate=N/A speed=   0x    \n'
        self.assertEqual(m.decode_diagnostics(raw+final,CONTROL,dest/'native/frame-%06d.png')['status'],'refused')
        self.assertEqual(m.decode_diagnostics(raw.replace(b'config out time_base: 0/0',b'config out time_base: 1/30'),CONTROL,dest/'native/frame-%06d.png')['status'],'refused')
        self.assertEqual(m.decode_diagnostics(raw,CONTROL,dest/'wrong-output.png')['status'],'refused')
        for wrong in [raw.replace(b'frame=    4',b'frame=    5'),raw.replace(b's:96x64',b's:97x64'),
                      raw.replace(b'sar:4/3',b'sar:1/1'),raw.replace(b'fmt:bgr0',b'fmt:yuv411p'),
                      raw.replace(b'i:P',b'i:B')]:
            with self.assertRaises(m.Refusal):m.check_showinfo(wrong,frames,[0,60,120,124],tb)

    def test_synthetic_pixels_pts_sar_repeat(self):
        pair=[]
        for suffix in ['-01','-02']:
            d=self.destination(suffix);r=m.sample_source(item(),d,{'kind':'synthetic control'})
            self.assertNotEqual(r['admission'],'refused',r)
            self.assertEqual(r['source_identity']['status'],'matched_before_and_after')
            rows=json.loads((d/'frames.json').read_bytes());self.assertEqual([x['source_index'] for x in rows],[0,60,120,124])
            for row,color in zip(rows,[(255,0,0),(0,255,0),(0,0,255),(0,0,255)]):
                with Image.open(d/row['file']) as im:
                    self.assertEqual(im.size,(96,64));self.assertEqual(im.mode,'RGB')
                    self.assertEqual(im.tobytes(),bytes(color)*(96*64))
                    self.assertEqual(hashlib.sha256(im.tobytes()).hexdigest(),row['rgb_sha256'])
                self.assertEqual(m.sha(d/row['file']),row['png_sha256'])
                self.assertEqual(Fraction(row['pts_seconds_exact']),Fraction(row['source_index'],30))
                self.assertEqual(row['sample_aspect_ratio'],'4:3')
            pair.append(rows)
        self.assertEqual(*pair)

    def test_wrong_hash_preserves_identity(self):
        bad=item();bad['sha256']='0'*64
        with patch.object(m.subprocess,'run') as mocked:
            r=m.sample_source(bad,self.destination(),{})
            mocked.assert_not_called()
        self.assertEqual(r['admission'],'refused')
        self.assertEqual(r['source_identity']['before'],r['source_identity']['after'])

    def test_wrong_count_retained(self):
        bad=item();bad['count']=126
        fake=SimpleNamespace(returncode=0,stdout=json.dumps(DOC).encode(),stderr=b'')
        with patch.object(m.subprocess,'run',return_value=fake) as mocked:
            r=m.sample_source(bad,self.destination(),{})
            self.assertEqual(mocked.call_count,1)
        self.assertEqual(r['admission'],'refused');self.assertIn('frame count',r['reasons'][0])

    def test_probe_only_diagnostic(self):
        fake=SimpleNamespace(returncode=0,stdout=json.dumps(DOC).encode(),stderr=b'probe-only warning\n')
        with patch.object(m.subprocess,'run',return_value=fake) as mocked:
            r=m.sample_source(item(),self.destination(),{})
            self.assertEqual(mocked.call_count,1)
        self.assertEqual(r['admission'],'refused');self.assertEqual(r['probe_diagnostics']['status'],'refused')
        self.assertEqual(r['decode_diagnostics']['status'],'not_attempted')
        self.assertEqual(r['source_identity']['status'],'matched_before_and_after')

    def test_decode_severity_refusals(self):
        for level in ['warning','error','fatal','panic']:
            dest=self.destination('-'+level)
            outputs=[SimpleNamespace(returncode=0,stdout=json.dumps(DOC).encode(),stderr=b''),
                     SimpleNamespace(returncode=0,stdout=b'',stderr=log_for(dest)+f'[{level}] injected\n'.encode())]
            with patch.object(m.subprocess,'run',side_effect=outputs):r=m.sample_source(item(),dest,{})
            self.assertEqual(r['admission'],'refused');self.assertEqual(r['decode_diagnostics']['status'],'refused')
            self.assertEqual(r['source_identity']['status'],'matched_before_and_after')
            self.assertFalse((dest/'frames.json').exists())

    def test_existing_destination(self):
        dest=self.destination();dest.mkdir();(dest/'sentinel').write_text('preserve')
        with self.assertRaises(FileExistsError):m.sample_source(item(),dest,{})
        self.assertEqual(list(dest.iterdir()),[dest/'sentinel'])
        self.assertEqual((dest/'sentinel').read_text(),'preserve')

    def test_process_nonzero_status_retained(self):
        dest=self.destination();dest.mkdir()
        stdout,stderr,status=m.run_command([sys.executable,'-B','-c','import sys;print("out");sys.stderr.write("err\\n");sys.exit(7)'],dest,'nonzero')
        self.assertEqual(status['returncode'],7);self.assertEqual(stdout,b'out\n');self.assertEqual(stderr,b'err\n')
        self.assertEqual(json.loads((dest/'nonzero.status.json').read_bytes())['returncode'],7)
        source_dest=self.destination('-source')
        with patch.object(m.subprocess,'run',return_value=SimpleNamespace(returncode=7,stdout=b'',stderr=b'failed\n')):
            r=m.sample_source(item(),source_dest,{})
        self.assertEqual(r['admission'],'refused')
        self.assertEqual(json.loads((source_dest/'probe.status.json').read_bytes())['returncode'],7)
        self.assertIn('after',r['source_identity'])
        dest2=self.destination('-decode')
        outputs=[SimpleNamespace(returncode=0,stdout=json.dumps(DOC).encode(),stderr=b''),
                 SimpleNamespace(returncode=7,stdout=b'',stderr=log_for(dest2))]
        with patch.object(m.subprocess,'run',side_effect=outputs):r=m.sample_source(item(),dest2,{})
        self.assertEqual(r['admission'],'refused')
        self.assertEqual(json.loads((dest2/'decode.status.json').read_bytes())['returncode'],7)
        self.assertIn('after',r['source_identity'])

    def test_optimized_checks_still_refuse(self):
        dest=self.destination();dest.mkdir()
        command=[sys.executable,'-O','-B','-c',
            'import sample_sequence as m; '+
            'm.validate_source({"id":"x","path":"/tmp/x","sha256":"0"*64,"bytes":1,"count":2,"indices":[0,0]})']
        _,stderr,status=m.run_command(command,dest,'optimized-negative')
        self.assertNotEqual(status['returncode'],0);self.assertIn(b'Refusal',stderr)

    def test_manifest_plan_pin_and_run_output(self):
        d=self.destination();d.mkdir();plan=d/'plan.txt';plan.write_text('Synthetic fixture only.\n')
        manifest=d/'selection.json';m.save(manifest,{'schema':m.SCHEMA,'sources':[item()]})
        r=m.execute(manifest,m.sha(manifest),plan,m.sha(plan),d/'run')
        self.assertEqual(r['status'],'descriptive_candidates_only',r)
        bad=m.execute(manifest,m.sha(manifest),plan,'0'*64,d/'wrong-plan')
        self.assertEqual(bad['status'],'refused');self.assertTrue((d/'wrong-plan/run-receipt.json').exists())


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True,type=Path);args=parser.parse_args()
    ARTIFACTS=m.absolute(str(args.out));ARTIFACTS.mkdir()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    m.save(ARTIFACTS/'test-results.json',{'tests_run':result.testsRun,'failures':len(result.failures),
        'errors':len(result.errors),'successful':result.wasSuccessful(),
        'helper_sha256':m.sha(Path(m.__file__)),'tests_sha256':m.sha(Path(__file__)),
        'synthetic_source_sha256':m.sha(CONTROL)})
    sys.exit(0 if result.wasSuccessful() else 1)
