"""Bounded synthetic controls. Never decode or view historical media."""
import argparse
from contextlib import redirect_stdout, redirect_stderr
import copy
import csv
from fractions import Fraction
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image
import stage_b_extract as sb

CONTROL = None
KNOWN = b'[aist#0:1/pcm_s16le @ 0xabc] Guessed Channel Layout: stereo\n'


def rows_at(ticks, tb='1/2997'):
    return [dict(frame_index_zero_based=str(i), source_pts=str(tick), source_time_base=tb,
                 source_time_seconds_exact=str(tick * Fraction(tb)), best_effort_timestamp=str(tick),
                 decoded_sha256='a' * 64, identical_to_previous_decoded_frame='False')
            for i, tick in enumerate(ticks)]


class FakeAdapter:
    """Synthetic map and flat synthetic luma only, not camera pixels."""
    def __init__(self, *, warning=KNOWN, reported_count=1, source_error=False,
                 metadata_error=False, post_change=False, result_error=None):
        self.rows = rows_at([i * 100 for i in range(8042)])
        self.metadata = [dict(pts=i * 100, duration=100, width=640, height=480, pix_fmt='yuv420p')
                         for i in range(8042)]
        if metadata_error:
            self.metadata[6600]['duration'] = True
        self.warning = warning
        self.reported_count = reported_count
        self.source_error = source_error
        self.post_change = post_change
        self.result_error = result_error
        self.calls = []

    def inputs(self):
        self.calls.append('inputs')
        if self.source_error:
            raise ValueError('synthetic-source-pin-failure')
        counter = self.calls.count('inputs')
        pins = {'synthetic-only-not-a-source-file': {'bytes': 0, 'sha256': 'b' * 64}}
        if self.post_change and counter > 1:
            pins['synthetic-only-not-a-source-file']['bytes'] = 1
        return copy.deepcopy(self.rows), copy.deepcopy(self.metadata), pins

    def decode(self, rows, chosen, destination):
        self.calls.append('decode')
        with (destination / 'decoder.local-only.log').open('xb') as stream:
            stream.write(self.warning)
        images = []
        result = {'checked_frames': 8042, 'geometry': [640, 480], 'exit_code': 0,
                  'diagnostics': {'audio_layout_guess_stereo_lines': self.reported_count,
                      'unclassified_lines': 0, 'raw_local_log': 'decoder.local-only.log'},
                  'raw_stream_sha256': 'c' * 64, 'images': images,
                  'command': ['synthetic-adapter-no-media-decoding']}
        if self.result_error == 'count':
            result['checked_frames'] = 8041
        if self.warning != KNOWN or self.reported_count != 1 or self.result_error:
            return result
        encoded = io.BytesIO()
        plane = bytes(640 * 480)
        Image.frombytes('L', (640, 480), plane).save(encoded, format='PNG')
        for index, reasons in chosen.items():
            name = f'f{index:06d}.png'
            with (destination / name).open('xb') as stream:
                stream.write(encoded.getvalue())
            images.append(dict(rows[index], selection_reasons=reasons, png=name,
                               png_identity=sb.fingerprint(destination / name),
                               luma_sha256=hashlib.sha256(plane).hexdigest()))
        return result

    def sheets(self, result, destination):
        self.calls.append('sheets')
        # Reuses only the inherited sheet function on synthetic PNGs; no decode.
        return sb.HistoricalAdapter().sheets(result, destination)


class Controls(unittest.TestCase):
    def output(self, label='run'):
        parent = Path(tempfile.mkdtemp(prefix=self._testMethodName + '-', dir=CONTROL))
        return parent / label

    def assert_failed(self, out, phase):
        record = json.loads((out / 'failure.json').read_text())
        self.assertEqual(record['status'], 'failed')
        self.assertEqual(record['execution_kind'], 'synthetic-adapter-control')
        self.assertEqual(record['phase'], phase)
        self.assertFalse((out / 'receipt.json').exists())

    def test_closed_exact_edges_and_bounds(self):
        rows = rows_at([219, 220, 233, 234, 235], '1')
        chosen, plan = sb.select_frames(rows)
        self.assertEqual(list(chosen), [0, 1, 2, 3, 4])
        self.assertEqual(plan['interior_count'], 3)
        self.assertEqual(chosen[0], ['immediately-preceding-bound'])
        self.assertEqual(chosen[4], ['immediately-following-bound'])

    def test_fractional_boundary_no_float_rounding(self):
        rows = rows_at([659339, 659340, 701298, 701299], '1/2997')
        chosen, plan = sb.select_frames(rows)
        self.assertEqual(list(chosen), [0, 1, 2, 3])
        self.assertEqual(plan['interior_count'], 2)

    def test_missing_bounds_empty_interval_and_invalid_bounds(self):
        cases = [rows_at([220, 221, 235], '1'), rows_at([219, 220, 234], '1'),
                 rows_at([218, 219, 235], '1'), []]
        for rows in cases:
            with self.subTest(rows=len(rows)), self.assertRaises(ValueError):
                sb.select_frames(rows)
        rows = rows_at([219, 220, 234, 235], '1')
        for start, end in [(220, Fraction(234)), (Fraction(234), Fraction(220))]:
            with self.assertRaises(ValueError):
                sb.select_frames(rows, start, end)

    def test_strict_index_and_clock_rejection(self):
        base = rows_at([219, 220, 234, 235], '1')
        changes = [('frame_index_zero_based', True), ('frame_index_zero_based', 1),
                   ('frame_index_zero_based', '01'), ('frame_index_zero_based', '0'),
                   ('source_pts', '220.0'), ('best_effort_timestamp', '221'),
                   ('source_time_base', '-1'), ('source_time_seconds_exact', '220.01')]
        for key, value in changes:
            rows = copy.deepcopy(base)
            rows[1][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                sb.select_frames(rows)
        for ticks in ([219, 219, 234, 235], [219, 218, 234, 235]):
            with self.assertRaisesRegex(ValueError, 'nonmonotone'):
                sb.select_frames(rows_at(ticks, '1'))

    def test_fixed_map_selection_without_media(self):
        path = sb.OLD.parent / 'timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/frame-map.csv'
        self.assertEqual(sb.fingerprint(path)['sha256'],
                         'ccc78c7ff933710f8e8e767dce5e05855fefb05bb75241d2bec01b4739c3b812')
        with path.open() as stream:
            rows = list(csv.DictReader(stream))
        chosen, plan = sb.select_frames(rows)
        self.assertEqual(list(chosen), list(range(6593, 7014)))
        self.assertEqual((plan['interior_count'], plan['selected_count']), (419, 421))

    def test_outside_and_existing_output_guards(self):
        for out in [sb.UNIT, sb.OLD / 'new-forbidden-output', Path('/private/tmp/forbidden-stage-b-output')]:
            with self.subTest(out=str(out)), self.assertRaises(ValueError):
                sb.fresh_output(out)
        out = self.output()
        out.mkdir()
        sentinel = out / 'sentinel'
        sentinel.write_text('preserve')
        with self.assertRaisesRegex(ValueError, 'already-exists'):
            sb.run(out, FakeAdapter())
        self.assertEqual(sentinel.read_text(), 'preserve')
        self.assertEqual([p.name for p in out.iterdir()], ['sentinel'])

    def test_symlink_output_guard(self):
        out = self.output()
        link = out.parent / 'symlink'
        link.symlink_to(sb.UNIT.parent, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            sb.fresh_output(link / 'forbidden-run')
        self.assertFalse((sb.UNIT.parent / 'forbidden-run').exists())

    def test_dependency_guard_precedes_source_or_decode(self):
        out, fake = self.output(), FakeAdapter()
        with patch.dict(sb.DEPENDENCIES, {sb.OLD / 'extract.py': '0' * 64}):
            with self.assertRaisesRegex(ValueError, 'dependency-pin'):
                sb.run(out, fake)
        self.assertEqual(fake.calls, [])
        self.assert_failed(out, 'dependency-pins')

    def test_source_guard_precedes_decode(self):
        out, fake = self.output(), FakeAdapter(source_error=True)
        with self.assertRaisesRegex(ValueError, 'source-pin'):
            sb.run(out, fake)
        self.assertEqual(fake.calls, ['inputs'])
        self.assert_failed(out, 'source-inputs')

    def test_metadata_duration_guard_precedes_decode(self):
        out, fake = self.output(), FakeAdapter(metadata_error=True)
        with self.assertRaisesRegex(ValueError, 'metadata-duration'):
            sb.run(out, fake)
        self.assertEqual(fake.calls, ['inputs'])
        self.assert_failed(out, 'source-inputs')

    def test_complete_synthetic_camera2_only_and_duration_join(self):
        out, fake = self.output(), FakeAdapter()
        result = sb.run(out, fake)
        self.assertEqual(fake.calls, ['inputs', 'decode', 'sheets', 'inputs'])
        receipt = json.loads((out / 'receipt.json').read_text())
        self.assertEqual(receipt['execution_kind'], 'synthetic-adapter-control')
        self.assertEqual(receipt['cameras'], {'camera2': {'checked_frames': 8042, 'selected': 421}})
        self.assertFalse((out / 'camera4').exists())
        self.assertFalse((out / 'failure.json').exists())
        self.assertEqual(len(result['images']), 421)
        self.assertEqual(len(result['overview_sheets']), 27)
        for item in result['images']:
            self.assertEqual(item['source_duration_ticks'], 100)
            self.assertEqual(item['source_duration_seconds_exact'], '100/2997')
        self.assertEqual((out / 'source-pins-before.json').read_bytes(),
                         (out / 'source-pins-after.json').read_bytes())
        self.assertEqual((out / 'stage-b-snapshot.md').read_bytes(), (sb.UNIT / 'STAGE-B.md').read_bytes())
        for name, identity in receipt['products'].items():
            self.assertEqual(sb.fingerprint(out / name), identity)

    def test_warning_count_and_raw_grammar_fail_closed(self):
        for warning, count in [(b'', 0), (KNOWN * 2, 2), (b'unknown warning\n', 1)]:
            out, fake = self.output(), FakeAdapter(warning=warning, reported_count=count)
            with self.subTest(count=count), self.assertRaises(ValueError):
                sb.run(out, fake)
            self.assertEqual(fake.calls, ['inputs', 'decode'])
            self.assert_failed(out, 'result-admission')
            self.assertEqual((out / 'camera2/decoder.local-only.log').read_bytes(), warning)

    def test_decoded_count_rejection(self):
        out, fake = self.output(), FakeAdapter(result_error='count')
        with self.assertRaisesRegex(ValueError, 'decoded-count'):
            sb.run(out, fake)
        self.assert_failed(out, 'result-admission')

    def test_post_source_change_preserves_failed_scope(self):
        out, fake = self.output(), FakeAdapter(post_change=True)
        with self.assertRaisesRegex(ValueError, 'post-input-pin'):
            sb.run(out, fake)
        self.assertEqual(fake.calls, ['inputs', 'decode', 'sheets', 'inputs'])
        self.assert_failed(out, 'post-input-pins')
        self.assertTrue((out / 'camera2/f006593.png').is_file())

    def test_cli_help_and_outside_output_no_decode(self):
        command = [sys.executable, str(sb.UNIT / 'stage_b_extract.py')]
        environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        help_run = subprocess.run(command + ['--help'], capture_output=True, text=True,
                                  timeout=20, env=environment)
        self.assertEqual(help_run.returncode, 0)
        self.assertIn('--out', help_run.stdout)
        bad_run = subprocess.run(command + ['--out', str(sb.OLD / 'forbidden-cli-run')],
                                 capture_output=True, text=True, timeout=20, env=environment)
        self.assertNotEqual(bad_run.returncode, 0)
        self.assertIn('output-outside-unit', bad_run.stderr)
        self.assertFalse((sb.OLD / 'forbidden-cli-run').exists())

    def test_cli_dispatch_and_unknown_argument(self):
        out = self.output()
        with patch.object(sb, 'run') as execute, redirect_stdout(io.StringIO()):
            sb.main(['--out', str(out)])
        execute.assert_called_once_with(out)
        with patch.object(sb, 'run') as execute, redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            sb.main(['--out', str(out), '--camera', 'camera4'])
        self.assertEqual(raised.exception.code, 2)
        execute.assert_not_called()


def main():
    global CONTROL
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    CONTROL = sb.fresh_output(args.out)
    CONTROL.mkdir(parents=True, exist_ok=False)
    for source, name in [(Path(sb.__file__), 'driver-snapshot.py'), (Path(__file__), 'test-snapshot.py'),
                         (sb.UNIT / 'STAGE-B.md', 'stage-b-snapshot.md')]:
        with (CONTROL / name).open('xb') as stream:
            stream.write(source.read_bytes())
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    with (CONTROL / 'tests.log').open('x') as stream:
        stream.write(log.getvalue())
    print(log.getvalue(), end='')
    sb.write_json(CONTROL / 'receipt.json', {'status': 'pass' if result.wasSuccessful() else 'fail',
        'execution_kind': 'synthetic-controls-no-historical-decode', 'tests': result.testsRun,
        'failures': len(result.failures), 'errors': len(result.errors),
        'python': sys.version, 'pillow': sb.PIL.__version__,
        'code': sb.fingerprint(Path(sb.__file__)), 'tests_code': sb.fingerprint(Path(__file__)),
        'products': {str(p.relative_to(CONTROL)): sb.fingerprint(p)
                     for p in sorted(CONTROL.rglob('*')) if p.is_file() and not p.is_symlink()},
        'symlinks': {str(p.relative_to(CONTROL)): str(p.readlink())
                     for p in sorted(CONTROL.rglob('*')) if p.is_symlink()}})
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
