#!/usr/bin/env python3
"""Ordinal visual screen: missing source timestamps stay missing."""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
FIRST = HERE / 'prepare.py'
FIRST_SHA = 'f3a3be5e9335cdf50b336fe29acd7d5d92b6e6b3f7b726a1427796e365241a93'
ADDENDUM_SHA = '930123e028a5c0feadf58b6967cf1d789f5bc8a5e0d6fc12e582c527b3dfd293'
if hashlib.sha256(FIRST.read_bytes()).hexdigest() != FIRST_SHA:
    raise ValueError('first adapter changed')
spec = importlib.util.spec_from_file_location('first_media_adapter', FIRST)
first = importlib.util.module_from_spec(spec)
spec.loader.exec_module(first)
base = first.base


def timestamp(frame, key):
    value = frame.get(key)
    base.require(value is None or type(value) is int, 'timestamp must be integer or missing')
    return value


def parse_map(data):
    base.require(len(data.get('streams', [])) == 1, 'one video stream')
    stream = data['streams'][0]
    w, h = stream['width'], stream['height']
    base.require(type(w) is int and type(h) is int and 0 < w <= 2000 and 0 < h <= 2000,
                 'bounded native geometry')
    base.require(w % 2 == h % 2 == 0 and stream['pix_fmt'] == 'yuv420p', 'native format')
    tick = Fraction(stream['time_base'])
    base.require(tick > 0, 'positive time base')
    frames = data.get('frames', [])
    base.require(8 <= len(frames) <= 10000, 'exact eight selection requires at least eight frames')
    rows = []
    for index, frame in enumerate(frames):
        base.require((frame['width'], frame['height'], frame['pix_fmt']) == (w, h, 'yuv420p'),
                     'frame geometry/format changed')
        p = timestamp(frame, 'pts')
        b = timestamp(frame, 'best_effort_timestamp')
        base.require(p is None or b is None or p == b, 'present timestamps disagree')
        rows.append({'index': index, 'stored_pts': p, 'best_effort_timestamp': b,
                     'stored_pts_seconds_exact': None if p is None else str(p * tick),
                     'best_effort_seconds_exact': None if b is None else str(b * tick)})
    for key in ('stored_pts', 'best_effort_timestamp'):
        known = [r[key] for r in rows if r[key] is not None]
        base.require(all(b > a for a, b in zip(known, known[1:])), 'known timestamps not increasing')
    return stream, rows


def diagnostic_runner(directory):
    def run(argv, **kwargs):
        directory.mkdir()
        try:
            result = subprocess.run(argv, **kwargs)
        except subprocess.TimeoutExpired as exc:
            err = exc.stderr or b''
            (directory / 'stderr.bin').write_bytes(err[:1048576])
            base.write_json(directory / 'execution.json', {
                'argv': argv, 'status': 'timeout', 'timeout_seconds': exc.timeout,
                'stderr_bytes': len(err), 'stderr_sha256': base.sha(err),
                'stderr_truncated': len(err) > 1048576,
            })
            raise
        err = result.stderr
        (directory / 'stderr.bin').write_bytes(err[:1048576])
        receipt = {'argv': argv, 'status': 'returned', 'returncode': result.returncode,
                   'stderr_bytes': len(err), 'stderr_sha256': base.sha(err),
                   'stderr_truncated': len(err) > 1048576,
                   'stdout_bytes': len(result.stdout), 'stdout_sha256': base.sha(result.stdout)}
        if Path(argv[0]) == base.PROBE:
            base.require(len(result.stdout) <= 16777216, 'probe output bound')
            (directory / 'probe-stdout.json').write_bytes(result.stdout)
        base.write_json(directory / 'execution.json', receipt)
        return result
    return run


class Controls(unittest.TestCase):
    def fixture(self):
        return {'streams': [{'width': 4, 'height': 2, 'pix_fmt': 'yuv420p', 'time_base': '1/30'}],
                'frames': [{'width': 4, 'height': 2, 'pix_fmt': 'yuv420p', 'pts': i,
                            'best_effort_timestamp': i} for i in range(9)]}

    def test_missing_is_not_filled(self):
        d = self.fixture()
        del d['frames'][0]['pts']
        del d['frames'][8]['pts']
        del d['frames'][8]['best_effort_timestamp']
        rows = parse_map(d)[1]
        self.assertIsNone(rows[0]['stored_pts'])
        self.assertEqual(rows[0]['best_effort_timestamp'], 0)
        self.assertIsNone(rows[8]['stored_pts_seconds_exact'])
        self.assertIsNone(rows[8]['best_effort_seconds_exact'])

    def test_zero_and_exact_seconds(self):
        rows = parse_map(self.fixture())[1]
        self.assertEqual(rows[0]['stored_pts'], 0)
        self.assertEqual(rows[1]['stored_pts_seconds_exact'], '1/30')

    def test_disagreement(self):
        d = self.fixture(); d['frames'][2]['pts'] = 3
        with self.assertRaises(ValueError): parse_map(d)

    def test_nonmonotone(self):
        d = self.fixture(); d['frames'][2].update(pts=0, best_effort_timestamp=0)
        with self.assertRaises(ValueError): parse_map(d)

    def test_short(self):
        d = self.fixture(); d['frames'] = d['frames'][:7]
        with self.assertRaises(ValueError): parse_map(d)

    def test_format(self):
        d = self.fixture(); d['streams'][0]['pix_fmt'] = 'gray'
        with self.assertRaises(ValueError): parse_map(d)

    def test_geometry(self):
        d = self.fixture(); d['frames'][3]['width'] = 2
        with self.assertRaises(ValueError): parse_map(d)

    def test_timestamp_type(self):
        d = self.fixture(); d['frames'][2]['pts'] = True
        with self.assertRaises(ValueError): parse_map(d)

    def test_selection(self):
        self.assertEqual(base.selected_indices(962), [0,137,274,411,549,686,823,961])

    def test_path(self):
        with self.assertRaises(ValueError): base.safe_output('../escape')

    def test_failed_probe_diagnostics_retained(self):
        with tempfile.TemporaryDirectory(prefix='distant-view-test-') as temp:
            target = Path(temp)/'diagnostics'
            result = SimpleNamespace(returncode=1, stdout=b'{bad-json', stderr=b'probe warning')
            with mock.patch.object(subprocess, 'run', return_value=result):
                diagnostic_runner(target)([str(base.PROBE)], capture_output=True)
            self.assertEqual((target/'probe-stdout.json').read_bytes(), result.stdout)
            self.assertEqual((target/'stderr.bin').read_bytes(), result.stderr)
            self.assertEqual(json.loads((target/'execution.json').read_text())['returncode'], 1)

    def test_timeout_diagnostics_retained(self):
        with tempfile.TemporaryDirectory(prefix='distant-view-test-') as temp:
            target = Path(temp)/'diagnostics'
            error = subprocess.TimeoutExpired('fixture', 1, stderr=b'late warning')
            with mock.patch.object(subprocess, 'run', side_effect=error):
                with self.assertRaises(subprocess.TimeoutExpired):
                    diagnostic_runner(target)(['fixture'], timeout=1)
            self.assertEqual((target/'stderr.bin').read_bytes(), b'late warning')
            self.assertEqual(json.loads((target/'execution.json').read_text())['status'], 'timeout')

    def test_diagnostics_exclusive(self):
        with tempfile.TemporaryDirectory(prefix='distant-view-test-') as temp:
            with self.assertRaises(FileExistsError):
                diagnostic_runner(Path(temp))(['fixture'])


def main():
    p = argparse.ArgumentParser()
    p.add_argument('stage', choices=['test', 'probe', 'decode'])
    p.add_argument('--out'); p.add_argument('--probe')
    args = p.parse_args()
    base.require(base.pin(HERE/'PROTOCOL.md')['sha256'] == first.PROTOCOL_SHA, 'protocol changed')
    base.require(base.pin(HERE/'ORDINAL-ADDENDUM.md')['sha256'] == ADDENDUM_SHA, 'addendum changed')
    if args.stage == 'test':
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
        raise SystemExit(not result.wasSuccessful())
    output = base.safe_output(args.out)
    diag = base.safe_output(args.out + '-diagnostics')
    base.parse_map = parse_map
    base.subprocess = SimpleNamespace(run=diagnostic_runner(diag))
    if args.stage == 'probe':
        base.stage_probe(args.out)
    else:
        base.stage_decode(args.probe, args.out)
    base.write_json(output/'ordinal-adapter-receipt.json', {
        'adapter': base.pin(__file__), 'first_adapter': base.pin(FIRST),
        'base_producer': base.pin(first.BASE), 'protocol': base.pin(HERE/'PROTOCOL.md'),
        'addendum': base.pin(HERE/'ORDINAL-ADDENDUM.md'),
        'source_receipt': base.pin(HERE/'source'/'receipt.json'),
        'diagnostics': base.pin(diag/'execution.json'),
        'scope': 'ordinal screen only; missing timestamps remain missing',
    })


if __name__ == '__main__':
    main()
