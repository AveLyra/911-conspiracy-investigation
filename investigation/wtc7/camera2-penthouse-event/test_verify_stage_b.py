"""Synthetic-only controls for the independent saved-product checker."""
import argparse
import copy
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from PIL import Image, ImageDraw

import verify_stage_b as verify

OUT = None


def write_json(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, sort_keys=True)
        stream.write('\n')


def rows_fixture():
    rows, metadata = [], []
    for index, pts in enumerate((219, 220, 221, 234, 235)):
        rows.append({'frame_index_zero_based': str(index), 'source_pts': str(pts),
                     'source_time_base': '1', 'source_time_seconds_exact': str(pts),
                     'best_effort_timestamp': str(pts), 'decoded_sha256': hashlib.sha256(bytes([index])).hexdigest(),
                     'identical_to_previous_decoded_frame': 'False'})
        metadata.append({'pts': pts, 'pkt_dts': pts, 'best_effort_timestamp': pts,
                         'duration': 1, 'width': 640, 'height': 480, 'pix_fmt': 'yuv420p',
                         'interlaced_frame': 0, 'top_field_first': 0, 'repeat_pict': 0})
    return rows, metadata


class Controls(unittest.TestCase):
    def setUp(self):
        self.directory = OUT / self._testMethodName
        self.directory.mkdir()

    def fixture(self):
        rows, metadata = rows_fixture()
        indices, reasons = verify.derive_selection([Fraction(r['source_pts']) for r in rows])
        images, pixels = [], []
        geometry = (64, 48)
        for i in indices:
            raw = bytes((i * 41 + j * 13) % 256 for j in range(geometry[0] * geometry[1]))
            name = f'f{i:06d}.png'
            Image.frombytes('L', geometry, raw).save(self.directory / name)
            images.append(dict(rows[i], selection_reasons=reasons[i], png=name,
                               png_identity=verify.fingerprint(self.directory / name),
                               luma_sha256=hashlib.sha256(raw).hexdigest(),
                               source_duration_ticks=1, source_duration_seconds_exact='1'))
            pixels.append(raw)
        # Fixture uses Pillow BOX, while the checker computes reduction with integers.
        sheet = Image.new('L', (128, 200), 255)
        draw = ImageDraw.Draw(sheet)
        for j, entry in enumerate(images):
            x, y = j % 4 * 32, j // 4 * 50
            with Image.open(self.directory / entry['png']) as source:
                sheet.paste(source.resize((32, 24), Image.Resampling.BOX), (x, y))
            draw.text((x + 3, y + 26), f"frame {entry['frame_index_zero_based']} | {float(Fraction(entry['source_time_seconds_exact'])):.6f} s", fill=0)
        sheet.save(self.directory / 'overview-00.png')
        return rows, metadata, indices, reasons, images, pixels, geometry

    def test_closed_interval_and_immediate_bounds(self):
        rows, metadata = rows_fixture()
        times = verify.validate_rows(rows, metadata)
        indices, reasons = verify.derive_selection(times)
        self.assertEqual(indices, [0, 1, 2, 3, 4])
        self.assertEqual(reasons[0], ['immediately-preceding-bound'])
        self.assertEqual(reasons[4], ['immediately-following-bound'])
        self.assertEqual(reasons[1], ['closed-interval-interior'])
        self.assertEqual(reasons[3], ['closed-interval-interior'])

    def test_rational_not_float_boundary(self):
        epsilon = Fraction(1, 10 ** 30)
        times = [Fraction(220) - epsilon, Fraction(220), Fraction(234), Fraction(234) + epsilon]
        self.assertEqual(verify.derive_selection(times)[0], [0, 1, 2, 3])
        self.assertEqual(verify.derive_selection(times)[1][0], ['immediately-preceding-bound'])

    def test_empty_missing_bounds_and_order_fail(self):
        cases = [[], [Fraction(220), Fraction(234), Fraction(235)],
                 [Fraction(219), Fraction(220), Fraction(234)],
                 [Fraction(218), Fraction(219), Fraction(235)],
                 [Fraction(219), Fraction(220), Fraction(220), Fraction(235)],
                 [Fraction(219), Fraction(234), Fraction(220), Fraction(235)], [219, 220, 235]]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                verify.derive_selection(case)

    def test_strict_map_indices_times_and_hash_flags(self):
        rows, metadata = rows_fixture()
        cases = [('frame_index_zero_based', True), ('frame_index_zero_based', '01'),
                 ('frame_index_zero_based', '0'), ('source_pts', '220.0'),
                 ('best_effort_timestamp', '222'), ('source_time_base', '0'),
                 ('source_time_seconds_exact', '221'), ('source_time_seconds_exact', '220.0'),
                 ('decoded_sha256', 'bad'), ('identical_to_previous_decoded_frame', 'True')]
        for field, value in cases:
            changed = copy.deepcopy(rows)
            changed[1][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                verify.validate_rows(changed, metadata)

    def test_metadata_duration_geometry_and_pts_fail(self):
        rows, metadata = rows_fixture()
        for field, value in [('pts', True), ('pkt_dts', 0), ('best_effort_timestamp', 0),
                             ('duration', True), ('duration', 0), ('width', 320),
                             ('pix_fmt', 'rgb24'), ('interlaced_frame', 1),
                             ('top_field_first', 1), ('repeat_pict', 1)]:
            changed = copy.deepcopy(metadata)
            changed[1][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify.validate_rows(rows, changed)

    def test_diagnostic_exact_one_and_address_only_repeat(self):
        one = b'[aist#0:1/pcm_s16le @ 0xabc] Guessed Channel Layout: stereo\n'
        other = one.replace(b'0xabc', b'0x12d')
        self.assertEqual(verify.check_diagnostic(one), verify.check_diagnostic(other))
        for data in [b'', one + one, one + b'warning\n', one.replace(b'stereo', b'mono'), b'\n' + one]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                verify.check_diagnostic(data)
        self.assertNotEqual(verify.check_diagnostic(one), verify.check_diagnostic(one.replace(b'#0:1', b'#0:2')))
        self.assertNotEqual(verify.check_diagnostic(one), verify.check_diagnostic(one.rstrip(b'\n')))

    def test_half_pixels_rounding(self):
        for raw, expected in [(b'\0\0\0\1', b'\1'), (b'\0\0\0\3', b'\1'),
                              (b'\0\1\1\0', b'\1'), (bytes([0, 255, 0, 255]), b'\x80')]:
            self.assertEqual(verify.half_pixels(raw, 2, 2), expected)
        with self.assertRaises(ValueError):
            verify.half_pixels(b'123', 2, 2)

    def test_native_pixels_and_independent_sheets_pass(self):
        rows, metadata, indices, reasons, images, pixels, geometry = self.fixture()
        actual = verify.check_images(self.directory, images, rows, metadata, indices, reasons, geometry)
        self.assertEqual(actual, pixels)
        verify.check_sheets(self.directory, ['overview-00.png'], images, actual, geometry)

    def test_selected_row_reason_duration_hash_rejections(self):
        rows, metadata, indices, reasons, images, pixels, geometry = self.fixture()
        for field, value in [('source_pts', '0'), ('selection_reasons', ['wrong']),
                             ('source_duration_ticks', True), ('source_duration_seconds_exact', '2'),
                             ('png', '../f000000.png'), ('luma_sha256', '0' * 64),
                             ('png_identity', {'bytes': 1, 'sha256': '0' * 64})]:
            altered = copy.deepcopy(images)
            altered[0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify.check_images(self.directory, altered, rows, metadata, indices, reasons, geometry)
        with self.assertRaises(ValueError):
            verify.check_images(self.directory, images[::-1], rows, metadata, indices, reasons, geometry)

    def test_wrong_pixel_even_with_file_pin_updated_fails(self):
        rows, metadata, indices, reasons, images, pixels, geometry = self.fixture()
        path = self.directory / images[0]['png']
        Image.new('L', geometry, 0).save(path)
        images[0]['png_identity'] = verify.fingerprint(path)
        with self.assertRaisesRegex(ValueError, 'png-luma-pin'):
            verify.check_images(self.directory, images, rows, metadata, indices, reasons, geometry)

    def test_wrong_mode_with_file_pin_updated_fails(self):
        rows, metadata, indices, reasons, images, pixels, geometry = self.fixture()
        path = self.directory / images[0]['png']
        Image.new('RGB', geometry, 0).save(path)
        images[0]['png_identity'] = verify.fingerprint(path)
        with self.assertRaisesRegex(ValueError, 'png-format'):
            verify.check_images(self.directory, images, rows, metadata, indices, reasons, geometry)

    def test_wrong_sheet_pixel_or_name_fails(self):
        rows, metadata, indices, reasons, images, pixels, geometry = self.fixture()
        with self.assertRaisesRegex(ValueError, 'sheet-names'):
            verify.check_sheets(self.directory, ['overview-01.png'], images, pixels, geometry)
        path = self.directory / 'overview-00.png'
        with Image.open(path) as source:
            changed = source.copy()
        changed.putpixel((127, 199), 0)
        changed.save(path)
        with self.assertRaisesRegex(ValueError, 'sheet-pixels-labels'):
            verify.check_sheets(self.directory, ['overview-00.png'], images, pixels, geometry)

    def test_inventory_and_failure_state_fail_closed(self):
        write_json(self.directory / 'a.json', {'fixture': True})
        receipt = {'status': 'complete', 'execution_kind': verify.KIND,
                   'products': {'a.json': verify.fingerprint(self.directory / 'a.json')}}
        write_json(self.directory / 'receipt.json', receipt)
        self.assertEqual(verify.check_inventory(self.directory, receipt), receipt['products'])
        failed = dict(receipt, status='failed')
        with self.assertRaises(ValueError):
            verify.check_inventory(self.directory, failed)
        synthetic = dict(receipt, execution_kind='synthetic-adapter-control')
        with self.assertRaises(ValueError):
            verify.check_inventory(self.directory, synthetic)
        altered = copy.deepcopy(receipt)
        altered['products']['a.json']['sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            verify.check_inventory(self.directory, altered)
        write_json(self.directory / 'extra.json', {})
        with self.assertRaises(ValueError):
            verify.check_inventory(self.directory, receipt)

    def test_missing_inventory_file_fails(self):
        receipt = {'status': 'complete', 'execution_kind': verify.KIND,
                   'products': {'missing.json': {'bytes': 0, 'sha256': '0' * 64}}}
        write_json(self.directory / 'receipt.json', receipt)
        with self.assertRaises(ValueError):
            verify.check_inventory(self.directory, receipt)

    def test_duplicate_json_rejected(self):
        with (self.directory / 'duplicate.json').open('x') as stream:
            stream.write('{"status":"failed","status":"complete"}')
        with self.assertRaisesRegex(ValueError, 'duplicate-json-key'):
            verify.read_json(self.directory / 'duplicate.json')

    def test_float_and_nonfinite_json_numbers_rejected(self):
        for index, number in enumerate(('1.0', 'NaN', 'Infinity')):
            path = self.directory / f'number-{index}.json'
            with path.open('x') as stream:
                stream.write('{"count":' + number + '}')
            with self.subTest(number=number), self.assertRaisesRegex(ValueError, 'noninteger-json-number'):
                verify.read_json(path)

    def test_unsafe_paths_and_symlinks_rejected(self):
        for name in ['/tmp/a', '../a', 'a/../b', './a', 'a//b', 'a\\b', '']:
            with self.subTest(name=name), self.assertRaises(ValueError):
                verify.safe_child(self.directory, name)
        (self.directory / 'link').symlink_to(verify.UNIT / 'STAGE-B.md')
        with self.assertRaises(ValueError):
            verify.safe_child(self.directory, 'link')

    def test_repeat_only_process_address_may_differ(self):
        first = {'products': {'a.png': {'bytes': 2, 'sha256': 'a' * 64},
                              'camera2/decoder.local-only.log': {'bytes': 2, 'sha256': 'b' * 64}},
                 'diagnostic_normalized': b'known'}
        second = copy.deepcopy(first)
        second['products']['camera2/decoder.local-only.log']['sha256'] = 'c' * 64
        verify.compare_runs(first, second)
        second['products']['a.png']['sha256'] = 'c' * 64
        with self.assertRaises(ValueError):
            verify.compare_runs(first, second)
        second = copy.deepcopy(first)
        second['diagnostic_normalized'] = b'changed'
        with self.assertRaises(ValueError):
            verify.compare_runs(first, second)

    def test_initial_runtime_and_snapshot_pins(self):
        files = {'driver-snapshot.py': verify.UNIT / 'stage_b_extract.py',
                 'stage-b-snapshot.md': verify.UNIT / 'STAGE-B.md',
                 'inherited-extract-snapshot.py': verify.OLD / 'extract.py',
                 'inherited-protocol-snapshot.md': verify.OLD / 'PROTOCOL.md'}
        pins = {str(p): verify.fingerprint(p) for p in verify.DEPENDENCY_SHA}
        pins[str(verify.UNIT / 'stage_b_extract.py')] = verify.fingerprint(verify.UNIT / 'stage_b_extract.py')
        initial = {'kind': verify.KIND, 'pins': pins,
                   'executable': '/Users/admin/.pyenv/versions/3.13.7/bin/python3.13',
                   'python': '3.13.7 synthetic version record', 'pillow': '12.0.0',
                   'ffmpeg_version': 'ffmpeg version 7.1.1 synthetic', 'ffprobe_version': 'ffprobe version 7.1.1 synthetic'}
        for name, source in files.items():
            with (self.directory / name).open('xb') as stream:
                stream.write(source.read_bytes())
        write_json(self.directory / 'initial.json', initial)
        driver_sha = pins[str(verify.UNIT / 'stage_b_extract.py')]['sha256']
        verify.check_initial(self.directory, driver_sha)
        with self.assertRaises(ValueError):
            verify.check_initial(self.directory, '0' * 64)
        with (self.directory / 'driver-snapshot.py').open('ab') as stream:
            stream.write(b'\n# synthetic tamper\n')
        with self.assertRaises(ValueError):
            verify.check_initial(self.directory, driver_sha)

    def test_cli_fresh_result_failure_and_no_overwrite(self):
        one, two = self.directory / 'run01', self.directory / 'run02'
        one.mkdir()
        two.mkdir()
        out = self.directory / 'result.json'
        args = ['--run01', str(one), '--run02', str(two), '--driver-sha', '0' * 64, '--out', str(out)]
        with patch.object(verify, 'verify_pair', side_effect=ValueError('synthetic-failure')):
            self.assertEqual(verify.main(args), 1)
        before = out.read_bytes()
        self.assertEqual(verify.read_json(out)['status'], 'failed')
        with self.assertRaises(ValueError):
            verify.main(args)
        self.assertEqual(out.read_bytes(), before)

    def test_cli_outside_unit_and_within_run_rejected(self):
        with self.assertRaises(ValueError):
            verify.unit_path(verify.MAIN / 'verification.json', fresh=True)
        with self.assertRaises(ValueError):
            verify.unit_path(verify.UNIT, fresh=True)
        run = self.directory / 'run'
        run.mkdir()
        out = run / 'bad-result.json'
        args = ['--run01', str(run), '--run02', str(self.directory), '--driver-sha', '0' * 64, '--out', str(out)]
        with patch.object(verify, 'verify_pair') as called, self.assertRaises(ValueError):
            verify.main(args)
        called.assert_not_called()
        self.assertFalse(out.exists())


def main():
    global OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    OUT = verify.unit_path(args.out, fresh=True)
    OUT.mkdir()
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    with (OUT / 'tests.log').open('x') as stream:
        stream.write(log.getvalue())
    receipt = {'status': 'passed' if result.wasSuccessful() else 'failed', 'execution_kind': 'synthetic-checker-controls',
               'tests': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
               'checker': verify.fingerprint(Path(verify.__file__)), 'test': verify.fingerprint(Path(__file__)),
               'python': sys.version, 'pillow': verify.PIL.__version__, 'argv': sys.argv[1:],
               'scope': 'generated patterns and synthetic metadata only; no historical decode or image display',
               'products': {str(p.relative_to(OUT)): verify.fingerprint(p) for p in sorted(OUT.rglob('*')) if p.is_file()}}
    write_json(OUT / 'receipt.json', receipt)
    print(log.getvalue(), end='')
    print(json.dumps({key: receipt[key] for key in ('status', 'tests', 'failures', 'errors')}))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
