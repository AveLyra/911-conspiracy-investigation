"""Synthetic-only controls: never reads/decodes historical media."""
import tempfile
from pathlib import Path
import unittest
from contextlib import ExitStack, redirect_stdout
import io
import json
import subprocess
from types import SimpleNamespace
from unittest.mock import patch

from PIL import Image
import prepare


class SelectionControls(unittest.TestCase):
    def test_exact_selection_and_order(self):
        raw = b''.join(bytes([i]) * 12 for i in range(8))
        self.assertEqual(prepare.selected_planes(raw, 4, 3, 8, (7, 0, 3)),
                         [(7, bytes([7]) * 12), (0, bytes(12)), (3, bytes([3]) * 12)])

    def test_historical_sized_index_labels_are_synthetic(self):
        raw = bytes(i % 251 for i in range(442))
        self.assertEqual(prepare.selected_planes(raw, 1, 1, 442, prepare.INDICES),
                         [(i, bytes([i % 251])) for i in range(255, 262)])

    def test_wrong_length(self):
        for raw in (b'', bytes(3), bytes(5)):
            with self.subTest(length=len(raw)), self.assertRaises(ValueError):
                prepare.selected_planes(raw, 2, 2, 1, (0,))

    def test_invalid_dimensions(self):
        for dims in ((0, 2, 1), (2, -1, 1), (2, 2, False), (2.0, 2, 1)):
            with self.subTest(dims=dims), self.assertRaises(ValueError):
                prepare.selected_planes(bytes(4), *dims, (0,))

    def test_invalid_selection(self):
        for indices in ((), (0, 0), (-1,), (1,), (False,), (0.0,)):
            with self.subTest(indices=indices), self.assertRaises(ValueError):
                prepare.selected_planes(bytes(4), 2, 2, 1, indices)

    def test_png_roundtrip_and_rejections(self):
        pixels = bytes((0, 30, 90, 255))
        with tempfile.TemporaryDirectory(prefix='camera3-spot-control-') as temp:
            path = Path(temp) / 'synthetic.png'
            Image.frombytes('L', (2, 2), pixels).save(path)
            prepare.check_png(path, pixels, 2, 2)
            with self.assertRaises(ValueError):
                prepare.check_png(path, bytes(4), 2, 2)
            with self.assertRaises(ValueError):
                prepare.check_png(path, pixels, 1, 4)
            Image.new('RGB', (2, 2)).save(path)
            with self.assertRaises(ValueError):
                prepare.check_png(path, bytes(12), 2, 2)

    def test_output_rejection_and_no_clobber(self):
        with tempfile.TemporaryDirectory(prefix='camera3-spot-control-') as temp:
            with patch.object(prepare, 'HERE', Path(temp)):
                self.assertEqual(prepare.output_path('run01'), Path(temp) / 'run01')
                (Path(temp) / 'run01').mkdir()
                for name in ('run01', '../escape', '/tmp/escape', 'a/b', ''):
                    with self.subTest(name=name), self.assertRaises(ValueError):
                        prepare.output_path(name)


class SyntheticPipelineControls(unittest.TestCase):
    def exercise(self, mode):
        """Mock decoder and source tree; no historical source or pipeline is read."""
        with tempfile.TemporaryDirectory(prefix='camera3-spot-pipeline-') as temp:
            root = Path(temp)
            unit = root / 'unit'
            unit.mkdir()
            prior = root / 'prior'
            (prior / 'views01').mkdir(parents=True)
            old = root / 'old'
            old.mkdir()
            source, binary = root / 'synthetic.wmv', root / 'synthetic-ffmpeg'
            source.write_bytes(b'explicit synthetic source, never decoded')
            binary.write_bytes(b'mocked decoder, never executed')
            basecode = prior / 'prepare.py'
            basecode.write_text('# synthetic placeholder, never executed\n')
            (root / 'CHARTER.md').write_text('synthetic charter\n')
            for name in ('PROTOCOL.md', 'test_prepare.py'):
                (unit / name).write_text('synthetic fixture\n')
            raw = b''.join(bytes([i % 251]) * 4 for i in range(442))
            records = [{'index': i, 'pts': 0, 'time_base': '1/1000'} for i in range(442)]
            for index, pts in zip(prepare.INDICES, prepare.PTS):
                records[index]['pts'] = pts
            mapping = {'raw_frame_count': 442, 'records': records,
                       'pixel_hashes': [prepare.sha(raw[i * 4:(i + 1) * 4]) for i in range(442)],
                       'raw_sha256': prepare.sha(raw)}
            map_path = old / 'default-frames.json'
            map_path.write_text(json.dumps(mapping))
            def pin(path):
                data = path.read_bytes()
                return {'bytes': len(data), 'sha256': prepare.sha(data)}
            argv = [str(binary), '-nostdin', '-nostats', '-hide_banner', '-loglevel',
                    'repeat+level+info', '-debug_ts', '-copyts', '-noautorotate',
                    '-i', str(source), '-map', '0:v:0', '-an', '-noautoscale',
                    '-pix_fmt', 'gray', '-fps_mode', 'passthrough', '-enc_time_base:v',
                    'demux', '-f', 'rawvideo', '-']
            (old / 'receipt.json').write_text(json.dumps({
                'binaries': {str(binary): pin(binary)},
                'commands': [{'label': 'default', 'argv': argv}]}))
            anchor = raw[258 * 4:259 * 4] if mode != 'anchor' else bytes(4)
            Image.frombytes('L', (2, 2), anchor).save(prior / 'views01' / 'frame-0258.png')
            base = SimpleNamespace(SOURCE=source, BIN=binary, OLD=old, PUBLIC=root, pin=pin)
            stderr = b'corrupt decoded frame\n' * 3
            def fake_run(actual, **kwargs):
                self.assertEqual(actual, argv)
                self.assertEqual(kwargs['timeout'], 60)
                if mode == 'timeout':
                    raise subprocess.TimeoutExpired(argv, 60, output=b'partial', stderr=stderr)
                if mode == 'changed':
                    (unit / 'PROTOCOL.md').write_text('changed synthetic fixture\n')
                return SimpleNamespace(returncode=9 if mode == 'short' else 0,
                                       stdout=b'partial' if mode == 'short' else raw,
                                       stderr=stderr)
            with ExitStack() as stack:
                for attr, value in {'HERE': unit, 'BASE': basecode, 'WIDTH': 2, 'HEIGHT': 2,
                                    'SOURCE_SHA': pin(source)['sha256'],
                                    'MAP_SHA': pin(map_path)['sha256']}.items():
                    stack.enter_context(patch.object(prepare, attr, value))
                stack.enter_context(patch.object(prepare, 'load_base', return_value=base))
                runner = stack.enter_context(patch.object(prepare.subprocess, 'run', side_effect=fake_run))
                stack.enter_context(patch.object(prepare.sys, 'argv', ['synthetic-test', '--out', 'run01']))
                stack.enter_context(redirect_stdout(io.StringIO()))
                if mode == 'success':
                    prepare.main()
                else:
                    with self.assertRaises((ValueError, subprocess.TimeoutExpired)):
                        prepare.main()
                self.assertEqual(runner.call_count, 1)
            out = unit / 'run01'
            if mode == 'success':
                result = json.loads((out / 'receipt.json').read_text())
                self.assertEqual(result['status'], 'pass_diagnostic_only')
                self.assertEqual([r['index'] for r in result['frames']], list(range(255, 262)))
                self.assertEqual(len(list(out.glob('*.png'))), 7)
                self.assertEqual(result['inputs_before'], result['inputs_after'])
                self.assertFalse((out / 'failure.json').exists())
            else:
                self.assertFalse((out / 'receipt.json').exists())
                result = json.loads((out / 'failure.json').read_text())
                self.assertEqual(result['status'], 'failed_no_images_admitted')
                self.assertEqual((out / 'decode.stderr.local.txt').read_bytes(), stderr)
                self.assertEqual(result['decode']['corrupt_mentions'], 3)
                if mode in ('short', 'timeout'):
                    self.assertEqual(result['decode']['raw_bytes'], 7)
                    self.assertEqual(result['decode']['raw_sha256'], prepare.sha(b'partial'))
                    self.assertIsNone(result['decode']['all_frame_hashes_match'])
                    self.assertEqual(len(list(out.glob('*.png'))), 0)
                if mode == 'short':
                    self.assertEqual(result['decode']['returncode'], 9)
                if mode == 'timeout':
                    self.assertTrue(result['decode']['timed_out'])
                if mode == 'anchor':
                    self.assertIn('png_pixels', result['exception'])
                if mode == 'changed':
                    self.assertIn('input_changed_during_run', result['exception'])

    def test_seven_image_success(self):
        self.exercise('success')

    def test_short_nonzero_preserves_failure_metadata(self):
        self.exercise('short')

    def test_timeout_preserves_partial_metadata(self):
        self.exercise('timeout')

    def test_changed_input_refuses_acceptance(self):
        self.exercise('changed')

    def test_anchor_mismatch_refuses_acceptance(self):
        self.exercise('anchor')


if __name__ == '__main__':
    unittest.main(verbosity=2)
