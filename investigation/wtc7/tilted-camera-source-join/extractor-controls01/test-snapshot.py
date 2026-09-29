"""Synthetic controls only; no historical source decoding in these tests."""
import argparse
import csv
from fractions import Fraction
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import extract as ex

CONTROL = None


def rows_for(payloads, ticks=(5000, 5040, 5120, 5200)):
    return [dict(frame_index_zero_based=str(i), source_pts=str(pts), source_time_base='1/1000',
        source_time_seconds_exact=str(Fraction(pts, 1000)), best_effort_timestamp=str(pts),
        decoded_sha256=ex.digest(payload), identical_to_previous_decoded_frame='False')
        for i, (payload, pts) in enumerate(zip(payloads, ticks))]


def csv_text(rows):
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w, cls.h = 16, 12
        cls.payloads = [bytes((k * 37 + i) % 256 for i in range(192)) + bytes([20+k])*48 + bytes([220-k])*48 for k in range(4)]
        cls.rows = rows_for(cls.payloads)

    def destination(self):
        return Path(tempfile.mkdtemp(prefix=self._testMethodName+'-', dir=CONTROL))

    def test_lossless_pattern_irregular_offset_clock(self):
        dest = self.destination()
        video = dest/'known-pattern.mkv'
        cmd = [str(ex.FFMPEG), '-nostdin', '-hide_banner', '-v', 'warning', '-f', 'rawvideo',
            '-pixel_format', 'yuv420p', '-video_size', '16x12', '-framerate', '25', '-i', '-',
            '-vf', r'settb=1/1000,setpts=if(eq(N\,0)\,5000\,if(eq(N\,1)\,5040\,if(eq(N\,2)\,5120\,5200)))',
            '-c:v', 'ffv1', '-pix_fmt', 'yuv420p', '-enc_time_base:v', '1/1000',
            '-fps_mode', 'passthrough', str(video)]
        proc = subprocess.run(cmd, input=b''.join(self.payloads), capture_output=True, timeout=20)
        self.assertEqual((proc.returncode, proc.stderr), (0, b''))
        probe_cmd = ['/opt/homebrew/bin/ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_frames', '-show_entries', 'frame=pts,width,height,pix_fmt', '-of', 'json', str(video)]
        probe = subprocess.run(probe_cmd, capture_output=True, timeout=20)
        self.assertEqual((probe.returncode, probe.stderr), (0, b''))
        metadata = json.loads(probe.stdout)
        self.assertEqual([r['pts'] for r in metadata['frames']], [5000,5040,5120,5200])
        selected = {i:['synthetic-all'] for i in range(4)}
        result = ex.decode(video, self.rows, 16, 12, selected, dest)
        self.assertEqual(result['raw_stream_sha256'], ex.digest(b''.join(self.payloads)))
        for i, row in enumerate(result['images']):
            with ex.Image.open(dest/row['png']) as image:
                self.assertEqual(image.tobytes(), self.payloads[i][:192])
        ex.write_json(dest/'synthetic-receipt.json', dict(encode_command=cmd, probe_command=probe_cmd,
                      source=ex.fingerprint(video), metadata=metadata, decode=result))

    def test_rational_selection_and_coalescing(self):
        rows = rows_for(self.payloads, (0, 999, 1001, 2000))
        self.assertEqual(ex.selection(rows), {0:['first-at-or-after-0s'], 2:['first-at-or-after-1s'],
            3:['first-at-or-after-2s', 'last-frame']})
        self.assertEqual(ex.read_map(csv_text(rows), '1/1000'), rows)

    def test_map_corruptions(self):
        mutations = [('source_pts','5.0'), ('frame_index_zero_based','99'), ('source_time_base','1/20'),
                     ('best_effort_timestamp','4999'), ('source_time_seconds_exact','1'), ('decoded_sha256','z'*64)]
        for key, value in mutations:
            rows = [dict(r) for r in self.rows]
            rows[0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                ex.read_map(csv_text(rows), '1/1000')
        for ticks in [(0,0,1,2), (0,-1,1,2)]:
            with self.assertRaises(ValueError):
                ex.read_map(csv_text(rows_for(self.payloads, ticks)), '1/1000')

    def test_wrong_hash(self):
        rows = [dict(r) for r in self.rows]
        rows[2]['decoded_sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'raw-frame-hash'):
            ex.consume(io.BytesIO(b''.join(self.payloads)), rows, 16, 12, {}, self.destination())

    def test_diagnostic_classifier(self):
        self.assertEqual(ex.classify_diagnostics(b'')['audio_layout_guess_stereo_lines'], 0)
        self.assertEqual(ex.classify_diagnostics(b'[aist#0:1/pcm_s16le @ 0xabc] Guessed Channel Layout: stereo\n')['audio_layout_guess_stereo_lines'], 1)
        for data in [b'corrupt frame', b'[aist#0:1/pcm_s16le @ 0xabc] Guessed Channel Layout: stereo\nerror', b'Guessed Channel Layout: stereo']:
            with self.assertRaisesRegex(ValueError, 'decoder-diagnostics'):
                ex.classify_diagnostics(data)

    def test_short_and_extra_stream(self):
        for payload in [b''.join(self.payloads)[:-1], b''.join(self.payloads)+b'x']:
            with self.assertRaises(ValueError):
                ex.consume(io.BytesIO(payload), self.rows, 16, 12, {}, self.destination())

    def test_geometry_and_selection_guard(self):
        for width, chosen in [(15, {}), (16, {4:['invalid']}), (16, {True:['invalid']})]:
            with self.assertRaises(ValueError):
                ex.consume(io.BytesIO(b''.join(self.payloads)), self.rows, width, 12, chosen, self.destination())

    def test_overwrite_guard(self):
        dest = self.destination()
        sentinel = dest/'sentinel'
        sentinel.write_bytes(b'preserve')
        with self.assertRaises(FileExistsError):
            ex.run(dest)
        self.assertEqual(list(dest.iterdir()), [sentinel])
        self.assertEqual(sentinel.read_bytes(), b'preserve')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    CONTROL = args.out
    CONTROL.mkdir(parents=True, exist_ok=False)
    (CONTROL/'extract-snapshot.py').write_bytes(Path(ex.__file__).read_bytes())
    (CONTROL/'test-snapshot.py').write_bytes(Path(__file__).read_bytes())
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    ex.write_json(CONTROL/'receipt.json', dict(status='pass' if result.wasSuccessful() else 'fail',
        tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
        code=ex.fingerprint(Path(ex.__file__)), tests_code=ex.fingerprint(Path(__file__)),
        products={str(p.relative_to(CONTROL)):ex.fingerprint(p) for p in CONTROL.rglob('*') if p.is_file()}))
    raise SystemExit(0 if result.wasSuccessful() else 1)
