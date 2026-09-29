#!/usr/bin/env python3
"""Synthetic-only controls; no held media/probe/frame payload is read or decoded."""
import argparse
import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock
import warnings

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
M = None


class Controls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='wtc7-tilted-extract-controls-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.paths = {k: self.base/n for k, n in {
            'media': 'synthetic.mp4', 'decoder': 'synthetic-decoder', 'probe': 'probe.json',
            'selection': 'selection.json', 'frames': 'baseline.json',
            'source_receipt': 'source.json', 'views_receipt': 'views.json'}.items()}
        self.paths['media'].write_bytes(b'SYNTHETIC media identity only')
        self.paths['decoder'].write_bytes(b'NOT EXECUTABLE: fake runner only')
        self.probe = {'streams': [{'width': 4, 'height': 2, 'pix_fmt': 'yuv420p',
                                   'time_base': '1/30', 'sample_aspect_ratio': '1:1'}],
                      'frames': [{'width': 4, 'height': 2, 'pix_fmt': 'yuv420p',
                                  'pts': t, 'best_effort_timestamp': t} for t in (0, 2, 5, 9)]}
        self.rows = [{'index': i, 'pts': t, 'time_seconds_exact': str(Fraction(t, 30))}
                     for i, t in enumerate((0, 2, 5, 9))]
        self.parts = [bytes((i*37+j*13) % 256 for j in range(12)) for i in range(4)]
        self.raw = b''.join(self.parts)
        self.baseline = [{**r, 'decoded_sha256': M.sha(part), 'luma_sha256': M.sha(part[:8])}
                         for r, part in zip(self.rows, self.parts)]
        self.selection = {'n': 4, 'geometry': [4, 2], 'time_base': '1/30',
                          'indices': [0, 1, 2, 3], 'frames': self.rows}
        for key, data in [('probe', self.probe), ('selection', self.selection),
                          ('frames', self.baseline)]:
            self.save(key, data)
        self.save('source_receipt', {'media': M.pin(self.paths['media'])})
        self.save('views_receipt', {'media': M.pin(self.paths['media']),
            'probe': M.pin(self.paths['probe']), 'selection': M.pin(self.paths['selection']),
            'binary': M.pin(self.paths['decoder']),
            'execution': {'argv': M.decoder_argv(self.paths['decoder'], self.paths['media']),
                          'raw_sha256': M.sha(self.raw)}})
        self.expected = {p: M.pin(p)['sha256'] for p in self.paths.values()}
        self.output = self.base/'output'

    def save(self, key, value):
        self.paths[key].write_text(json.dumps(value))

    def result(self, raw=None, stderr=b'', code=0, failure=None):
        return {'stdout': self.raw if raw is None else raw, 'stderr': stderr,
                'returncode': code, 'failure': failure,
                'retained_streams_complete': failure is None}

    def run_fixture(self, output=None, runner=None):
        return M.extract_to(output or self.output, self.paths, self.expected,
                            shape=(4, 2), count=4, time_base='1/30', sar='1:1',
                            runner=runner or (lambda argv, bound: self.result()))

    def map_check(self, probe=None, selection=None, baseline=None):
        return M.validate_map(probe or self.probe, selection or self.selection,
                              self.baseline if baseline is None else baseline,
                              (4, 2), 4, '1/30', '1:1')

    def test_complete_native_pixels_clocks_products_and_repeat(self):
        self.assertEqual(self.run_fixture()['frames'], 4)
        frames = M.read_json(self.output/'frames.json')
        self.assertEqual([r['index'] for r in frames], list(range(4)))
        self.assertEqual([r['pts'] for r in frames], [0, 2, 5, 9])
        self.assertEqual([r['time_seconds_exact'] for r in frames], ['0', '1/15', '1/6', '3/10'])
        for i, row in enumerate(frames):
            with M.Image.open(self.output/row['png']) as im:
                self.assertEqual((im.mode, im.size, im.n_frames), ('L', (4, 2), 1))
                self.assertEqual(im.tobytes(), self.parts[i][:8])
            self.assertEqual(row['png_identity'], M.pin(self.output/row['png']))
        receipt = M.read_json(self.output/'receipt.json')
        self.assertEqual(receipt['inputs_before'], receipt['inputs_after'])
        self.assertEqual(len(receipt['products']), 10)
        for name, identity in receipt['products'].items():
            self.assertEqual(identity, M.pin(self.output/name))
        second = self.base/'repeat'
        self.run_fixture(output=second)
        self.assertEqual({p.name: p.read_bytes() for p in self.output.iterdir()},
                         {p.name: p.read_bytes() for p in second.iterdir()})

    def test_helper_pin_checked_before_execution(self):
        path = self.base/'untrusted.py'
        path.write_text("raise RuntimeError('must never execute')")
        with self.assertRaisesRegex(ValueError, 'BEFORE execution'):
            M.load_helper(path, '0'*64)

    def test_missing_duplicate_bool_reordered_and_bad_digest_rows(self):
        cases = [self.baseline[:-1], self.baseline+[self.baseline[-1]],
                 list(reversed(self.baseline))]
        for key, value in [('index', True), ('pts', True), ('index', 1),
                            ('decoded_sha256', 'bad'), ('luma_sha256', 'bad')]:
            case = copy.deepcopy(self.baseline); case[0][key] = value; cases.append(case)
        for case in cases:
            with self.subTest(case_kind=type(case).__name__), self.assertRaises(ValueError):
                self.map_check(baseline=case)

    def test_map_clock_geometry_format_and_selection_refusals(self):
        cases = []
        for mutate in [lambda p: p['frames'][1].update(pts=0, best_effort_timestamp=0),
                       lambda p: p['frames'][1].update(pts=3),
                       lambda p: p['frames'][1].update(width=6),
                       lambda p: p['streams'][0].update(width=6),
                       lambda p: p['streams'][0].update(pix_fmt='gray'),
                       lambda p: p['streams'][0].update(time_base='1/60'),
                       lambda p: p['streams'][0].update(sample_aspect_ratio='2:1')]:
            p=copy.deepcopy(self.probe); mutate(p); cases.append(p)
        for p in cases:
            with self.assertRaises(ValueError): self.map_check(probe=p)
        for mutate in [lambda s: s.update(n=True), lambda s: s.update(indices=[0,1,1,3]),
                       lambda s: s.update(frames=list(reversed(self.rows)))]:
            s=copy.deepcopy(self.selection); mutate(s)
            with self.assertRaises(ValueError): self.map_check(selection=s)

    def test_full_frame_luma_tamper_duplicate_and_count_refusals(self):
        for bad in [self.raw[:-1], self.raw+b'x', self.parts[0]*4,
                    bytes([self.raw[0]^1])+self.raw[1:],
                    self.raw[:8]+bytes([self.raw[8]^1])+self.raw[9:]]:
            with self.assertRaises(ValueError):
                M.validate_raw(bad, self.rows, self.baseline, (4,2))
        old=copy.deepcopy(self.baseline); old[0]['luma_sha256']='0'*64
        with self.assertRaises(ValueError): M.validate_raw(self.raw,self.rows,old,(4,2))

    def test_predecode_tampered_missing_pin_and_duplicate_json(self):
        self.paths['media'].write_bytes(b'changed')
        runner=mock.Mock()
        with self.assertRaises(ValueError): self.run_fixture(runner=runner)
        runner.assert_not_called(); self.assertFalse(self.output.exists())
        self.paths['media'].unlink()
        with self.assertRaises(FileNotFoundError): self.run_fixture(runner=runner)
        runner.assert_not_called()
        path=self.base/'duplicate.json'; path.write_text('{"a":1,"a":2}')
        with self.assertRaisesRegex(ValueError,'duplicate JSON'): M.read_json(path)

    def test_warning_error_timeout_and_overflow_retained_not_admitted(self):
        for i,result in enumerate([self.result(stderr=b'synthetic warning\n'),
                                   self.result(code=3,stderr=b'synthetic error\n'),
                                   self.result(raw=b'partial',failure='timeout'),
                                   self.result(raw=self.raw+b'x',failure='stdout_limit')]):
            out=self.base/('failure'+str(i))
            with self.assertRaises(ValueError):
                self.run_fixture(output=out,runner=lambda argv,bound,r=result:r)
            self.assertEqual((out/'decode.stderr').read_bytes(),result['stderr'])
            self.assertEqual(M.read_json(out/'execution.json')['stdout_bytes_retained'],len(result['stdout']))
            self.assertTrue((out/'failure.json').is_file())
            self.assertFalse((out/'receipt.json').exists())
            self.assertFalse(list(out.glob('frame-*.png')))

    def test_actual_bounded_runner_success_warning_overflow_and_timeout(self):
        def run(code,limit=16,timeout=2,stderr=16):
            return M.bounded_process([sys.executable,'-B','-c',code],limit,timeout,stderr)
        r=run("import os;os.write(1,b'abc');os.write(2,b'warn')")
        self.assertEqual((r['stdout'],r['stderr'],r['returncode'],r['failure']),(b'abc',b'warn',0,None))
        r=run("import os;os.write(1,b'x'*100)")
        self.assertEqual((r['failure'],len(r['stdout'])),('stdout_limit',17))
        r=run("import os;os.write(2,b'e'*100)")
        self.assertEqual((r['failure'],len(r['stderr'])),('stderr_limit',17))
        r=run("import time;time.sleep(1)",timeout=.03)
        self.assertEqual(r['failure'],'timeout');self.assertFalse(r['retained_streams_complete'])

    def test_output_and_dangling_symlink_refuse_without_decode(self):
        self.output.mkdir();(self.output/'sentinel').write_bytes(b'preserve')
        runner=mock.Mock()
        with self.assertRaises(ValueError): self.run_fixture(runner=runner)
        runner.assert_not_called();self.assertEqual((self.output/'sentinel').read_bytes(),b'preserve')
        out=self.base/'dangling';out.symlink_to(self.base/'missing')
        with self.assertRaises(ValueError): self.run_fixture(output=out,runner=runner)
        for name in ['../bad','/tmp/bad','a/b','a b','',True]:
            with self.assertRaises(ValueError): M.output_path(name)

    def test_changed_input_after_decode_and_python_warning_preserved(self):
        def mutate(argv,bound):
            self.paths['media'].write_bytes(b'changed during run')
            return self.result()
        with self.assertRaisesRegex(ValueError,'changed during run'): self.run_fixture(runner=mutate)
        self.assertTrue((self.output/'inputs-after.json').is_file())
        self.assertFalse((self.output/'receipt.json').exists())
        self.paths['media'].write_bytes(b'SYNTHETIC media identity only')
        original=M.Image.frombytes
        def warned(*args,**kwargs):
            warnings.warn('synthetic rendering warning',UserWarning)
            return original(*args,**kwargs)
        out=self.base/'warning'
        with mock.patch.object(M.Image,'frombytes',side_effect=warned), self.assertRaises(ValueError):
            self.run_fixture(output=out)
        self.assertTrue(M.read_json(out/'python-warnings.json'))
        self.assertFalse((out/'receipt.json').exists())

    def test_decoder_contract_and_reviewed_cli_gates(self):
        argv=M.decoder_argv(Path('/decoder'),Path('/media'))
        self.assertEqual(argv,['/decoder','-nostdin','-nostats','-hide_banner','-v','warning',
            '-copyts','-noautorotate','-i','/media','-map','0:v:0','-an','-noautoscale',
            '-pix_fmt','yuv420p','-fps_mode','passthrough','-enc_time_base:v','demux','-f','rawvideo','-'])
        with self.assertRaisesRegex(ValueError,'execution flag'):
            M.historical('unused','0'*64,'0'*64,False)
        with mock.patch.object(M,'HERE',self.base):
            (self.base/'PROTOCOL.md').write_text('synthetic protocol')
            with self.assertRaisesRegex(ValueError,'producer pin'):
                M.historical('unused','0'*64,M.pin(self.base/'PROTOCOL.md')['sha256'],True)
            with self.assertRaisesRegex(ValueError,'protocol pin'):
                M.historical('unused',M.pin(M.__file__)['sha256'],'0'*64,True)
        self.assertFalse((self.base/'unused').exists())


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expect-code-sha256',required=True)
    args=parser.parse_args()
    source=HERE/'extract.py';raw=source.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=args.expect_code_sha256:
        raise SystemExit('producer hash mismatch BEFORE test import')
    M=types.ModuleType('synthetic_test_subject');M.__file__=str(source)
    exec(compile(raw,str(source),'exec'),M.__dict__)
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    print(json.dumps({'synthetic_only':True,'tests':result.testsRun,'passed':result.wasSuccessful(),
        'producer_sha256':hashlib.sha256(raw).hexdigest(),
        'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'python':sys.version.split()[0],'pillow':M.PILLOW_VERSION}))
    raise SystemExit(not result.wasSuccessful())
