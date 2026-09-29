#!/usr/bin/env python3
"""Synthetic-only controls for native contact pages; never loads historical PNGs."""
import argparse
from collections import Counter
import copy
import csv
from fractions import Fraction
import io
import json
from pathlib import Path
import platform
import re
import sys
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
import present as p
from PIL import Image


def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)
    return p.identity(data)


def json_bytes(value):
    return (json.dumps(value, sort_keys=True) + '\n').encode()


class Controls(unittest.TestCase):
    output = None

    @classmethod
    def setUpClass(cls):
        cls.root = cls.output/'fixture'
        cls.unit = cls.root/'unit'
        cls.source = cls.root/'source/camera2'
        cls.main = cls.root/'main'
        cls.unit.mkdir(parents=True)
        cls.source.mkdir(parents=True)
        cls.base = Image.frombytes('L', (640, 480), bytes((x+7*y) % 256 for y in range(480) for x in range(640)))
        cls.timing = []
        for index in range(8042):
            cls.timing.append({'frame_index_zero_based': str(index), 'source_pts': str(index*100),
                'source_time_base': '1/2997', 'source_time_seconds_exact': str(Fraction(index*100, 2997)),
                'best_effort_timestamp': str(index*100), 'decoded_sha256': 'a'*64,
                'identical_to_previous_decoded_frame': 'False'})
        cls.rows = []
        product_pins = {}
        for index in p.INDICES:
            image = cls.base.point([(value+index) % 256 for value in range(256)])
            memory = io.BytesIO()
            image.save(memory, format='PNG')
            name = f'f{index:06d}.png'
            pin = put(cls.source/name, memory.getvalue())
            row = {**cls.timing[index], 'png': name, 'png_identity': pin,
                'luma_sha256': p.identity(image.tobytes())['sha256'],
                'source_duration_ticks': 100, 'source_duration_seconds_exact': str(Fraction(100, 2997))}
            cls.rows.append(row)
            product_pins['camera2/'+name] = pin
        timing_text = io.StringIO()
        writer = csv.DictWriter(timing_text, fieldnames=list(cls.timing[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(cls.timing)
        video_pin = put(cls.main/p.VIDEO, b'SYNTHETIC NONVIDEO BYTES\n')
        cls.upstream = {
            p.TIMING+'frame-map.csv': put(cls.main/(p.TIMING+'frame-map.csv'), timing_text.getvalue().encode()),
            p.TIMING+'frames.json': put(cls.main/(p.TIMING+'frames.json'), b'{"synthetic":true}\n'),
            p.TIMING+'source-identity.json': put(cls.main/(p.TIMING+'source-identity.json'),
                json_bytes({'record_id': 'VID-WTC7-001', 'source_integrity': video_pin})),
            p.VIDEO: video_pin}
        cls.selection = {'geometry': [640, 480], 'source_id': 'VID-WTC7-001',
            'checked_frames': 8042, 'exit_code': 0, 'diagnostics': p.SOURCE_DIAGNOSTICS.copy(),
            'images': cls.rows, **{key: cls.upstream for key in ('input_pins', 'input_pins_before', 'input_pins_after')}}
        cls.selection_pin = put(cls.source/'selection.json', json_bytes(cls.selection))
        product_pins['camera2/selection.json'] = cls.selection_pin
        product_pins['camera2/decoder.local-only.log'] = put(cls.source/'decoder.local-only.log', b'SYNTHETIC diagnostic fixture\n')
        cls.receipt = {'status': 'complete', 'cameras': {'camera2': {'checked_frames': 8042, 'selected': 421}}, 'products': product_pins}
        cls.receipt_pin = put(cls.source.parent/'receipt.json', json_bytes(cls.receipt))
        cls.protocol_pin = put(cls.unit/'PROTOCOL.md', b'SYNTHETIC TEST PROTOCOL; NOT HISTORICAL AUTHORITY\n')['sha256']
        cls.charter_pin = put(cls.main/'research/sherlock-wtc7-investigation/CHARTER.md', b'SYNTHETIC CHARTER\n')['sha256']
        put(cls.unit/'test_present.py', Path(__file__).read_bytes())

    def setUp(self):
        self.patches = patch.multiple(p, UNIT=self.unit, SOURCE=self.source, MAIN=self.main,
            UPSTREAM=self.upstream, SELECTION_PIN=self.selection_pin, RECEIPT_PIN=self.receipt_pin,
            DECLARATION_SHA=self.protocol_pin, CHARTER_SHA=self.charter_pin)
        self.patches.start()
        self.addCleanup(self.patches.stop)

    def test_fixed_84_pages_full_coverage_order_pairs_overlap(self):
        schedule = p.pages()
        self.assertEqual(len(schedule), 84)
        self.assertEqual(schedule[0], list(range(6593, 6599)))
        self.assertEqual(schedule[-1], list(range(7008, 7014)))
        self.assertEqual({i for page in schedule for i in page}, set(range(6593, 7014)))
        self.assertEqual(sum(map(len, schedule)), 504)
        for number, page in enumerate(schedule):
            self.assertEqual(page, list(range(6593+5*number, 6599+5*number)))
        for left, right in zip(schedule, schedule[1:]):
            self.assertEqual(set(left) & set(right), {left[-1]})
            self.assertEqual(left[-1], right[0])
        pairs = {(a, b) for page in schedule for a, b in zip(page, page[1:])}
        self.assertEqual(pairs, {(i, i+1) for i in range(6593, 7013)})
        counts = Counter(i for page in schedule for i in page)
        self.assertEqual(counts[6593], 1)
        self.assertEqual(counts[7013], 1)
        self.assertEqual(sum(count == 2 for count in counts.values()), 83)

    def test_selection_exact_clock_receipt_and_upstream(self):
        self.assertEqual(p.select_rows(self.selection, self.timing, self.receipt), self.rows)
        for field, value in [('source_pts', '1'), ('source_time_seconds_exact', '2'),
                ('source_time_base', '1/30'), ('source_duration_ticks', True),
                ('source_duration_seconds_exact', '1'), ('png', '../escape.png'),
                ('best_effort_timestamp', '0'), ('frame_index_zero_based', True)]:
            altered = copy.deepcopy(self.selection)
            altered['images'][0][field] = value
            with self.subTest(field=field), self.assertRaises((ValueError, KeyError)):
                p.select_rows(altered, self.timing, self.receipt)

    def test_missing_duplicate_reordered_rows_and_warning_state_refused(self):
        changes = [lambda d: d['images'].pop(), lambda d: d['images'].append(d['images'][0]),
            lambda d: d['images'].reverse(), lambda d: d['diagnostics'].update(unclassified_lines=1),
            lambda d: d.update(input_pins={})]
        for change in changes:
            altered = copy.deepcopy(self.selection)
            change(altered)
            with self.assertRaises(ValueError): p.select_rows(altered, self.timing, self.receipt)
        bad_receipt = copy.deepcopy(self.receipt)
        bad_receipt['products'].pop('camera2/f006593.png')
        with self.assertRaises(KeyError): p.select_rows(self.selection, self.timing, bad_receipt)
        bad_timing = copy.deepcopy(self.timing)
        bad_timing[6593]['decoded_sha256'] = 'b'*64
        with self.assertRaises(ValueError): p.select_rows(self.selection, bad_timing, self.receipt)

    def test_every_source_pixel_and_slot_rectangle_preserved(self):
        for number in (0, 41, 83):
            rows = self.rows[5*number:5*number+6]
            panel, cells = p.compose_page(rows)
            self.assertEqual((panel.mode, panel.size), ('L', (1280, 1512)))
            self.assertEqual([cell['source_index'] for cell in cells], list(range(6593+5*number, 6599+5*number)))
            for slot, cell in enumerate(cells):
                x, y = (slot % 2)*640, (slot // 2)*504
                expected_rect = [x, y+24, x+640, y+504]
                self.assertEqual(cell['source_rectangle_half_open'], expected_rect)
                self.assertEqual(cell['label_rectangle_half_open'], [x, y, x+640, y+24])
                index = 6593+5*number+slot
                expected = self.base.point([(v+index) % 256 for v in range(256)]).tobytes()
                self.assertEqual(panel.crop(expected_rect).tobytes(), expected)
                self.assertEqual(cell['source_luma_sha256'], p.identity(expected)['sha256'])
                self.assertEqual(cell['label'], f'source {index} | PTS {index*100} | t={Fraction(index*100,2997)} s')
                self.assertNotEqual(set(panel.crop(cell['label_rectangle_half_open']).tobytes()), {24})
            if number == 0:
                with (self.output/'synthetic-page-00.png').open('xb') as stream:
                    panel.save(stream, format='PNG')

    def test_page_row_count_order_mode_and_label_fit_refused(self):
        with self.assertRaises(ValueError): p.compose_page(self.rows[:5])
        with self.assertRaises(ValueError): p.compose_page(list(reversed(self.rows[:6])))
        with self.assertRaises(ValueError): p.compose_page(self.rows[:6], lambda _: Image.new('RGB', (640,480)))
        with self.assertRaises(ValueError): p.compose_page(self.rows[:6], lambda _: Image.new('L', (639,480)))
        rows = copy.deepcopy(self.rows[:6])
        rows[0]['source_time_seconds_exact'] = '1'*1000
        with self.assertRaisesRegex(ValueError, 'label-fit'): p.compose_page(rows)

    def test_missing_tampered_hash_and_luma_inputs_refused(self):
        row = copy.deepcopy(self.rows[0])
        row['png'] = 'missing.png'
        with self.assertRaises(FileNotFoundError): p.read_source(row)
        row = copy.deepcopy(self.rows[0])
        row['png_identity']['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'source-png-pin'): p.read_source(row)
        row = copy.deepcopy(self.rows[0])
        row['luma_sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'source-luma-pin'): p.read_source(row)
        row['png'] = '../escape.png'
        with self.assertRaisesRegex(ValueError, 'confinement'): p.read_source(row)

    def test_wrong_image_geometry_mode_and_multiframe_refused(self):
        directory = self.output/'bad-image-fixtures'
        directory.mkdir()
        for name, image in [('wrong-size.png', Image.new('L', (640,479))),
                            ('wrong-mode.png', Image.new('RGB', (640,480)))]:
            memory = io.BytesIO(); image.save(memory, format='PNG')
            row = {**self.rows[0], 'png': name, 'png_identity': put(directory/name, memory.getvalue())}
            with patch.object(p, 'SOURCE', directory), self.assertRaisesRegex(ValueError, 'source-image-contract'):
                p.read_source(row)
        memory = io.BytesIO()
        Image.new('L', (640,480), 1).save(memory, format='PNG', save_all=True,
                                       append_images=[Image.new('L', (640,480), 2)])
        row = {**self.rows[0], 'png': 'animated.png', 'png_identity': put(directory/'animated.png', memory.getvalue())}
        with patch.object(p, 'SOURCE', directory), self.assertRaisesRegex(ValueError, 'single-frame'):
            p.read_source(row)

    def test_existing_output_and_symlink_refused_before_any_change(self):
        directory = self.output/'refusal-unit'; directory.mkdir()
        existing = directory/'run01'; existing.mkdir()
        pin = put(existing/'sentinel.txt', b'SYNTHETIC PRESERVE\n')
        (directory/'run02').symlink_to(existing, target_is_directory=True)
        with patch.object(p, 'UNIT', directory):
            for value in ('run01', 'run02', '../run01', '/tmp/run01', 'run03', None):
                with self.subTest(value=value), self.assertRaises(ValueError): p.run(value, '0'*64, '0'*64)
        self.assertEqual(p.fingerprint(existing/'sentinel.txt'), pin)
        self.assertEqual([path.name for path in existing.iterdir()], ['sentinel.txt'])

    def test_wrong_producer_protocol_and_input_pins_refused(self):
        unit = self.output/'wrong-pin-unit'; unit.mkdir()
        put(unit/'PROTOCOL.md', (self.unit/'PROTOCOL.md').read_bytes())
        with patch.object(p, 'UNIT', unit):
            with self.assertRaisesRegex(ValueError, 'reviewed-code-pin'): p.run('run01', '0'*64, self.protocol_pin)
            code = p.fingerprint(Path(p.__file__))['sha256']
            with self.assertRaisesRegex(ValueError, 'reviewed-protocol-pin'): p.run('run01', code, '0'*64)
            self.assertFalse((unit/'run01').exists())
        with patch.object(p, 'SELECTION_PIN', {'bytes': 1, 'sha256': '0'*64}):
            with self.assertRaisesRegex(ValueError, 'input-pin'): p.input_pins()

    def test_two_complete_synthetic_runs_and_product_identity(self):
        code = p.fingerprint(Path(p.__file__))['sha256']
        one = p.run('run01', code, self.protocol_pin)
        two = p.run('run02', code, self.protocol_pin)
        for result in (one, two):
            self.assertEqual(result['status'], 'complete-presentation-only')
            self.assertEqual(result['input_pins_before'], result['input_pins_after'])
            self.assertEqual(result['runtime_pins_before'], result['runtime_pins_after'])
            self.assertEqual(result['source_generation_diagnostics'], p.SOURCE_DIAGNOSTICS)
            self.assertEqual(result['warnings'], [])
        for name in ['manifest.json', *[f'page-{number:02d}.png' for number in range(84)]]:
            self.assertEqual(one['products'][name], two['products'][name])
        manifest = json.loads((self.unit/'run01/manifest.json').read_bytes())
        self.assertEqual(len(manifest['pages']), 84)
        self.assertEqual(manifest['source_indices'], list(range(6593,7014)))

    def test_render_failure_retains_warning_and_no_complete_receipt(self):
        original = p.compose_page
        def warn(*args, **kwargs):
            import warnings
            warnings.warn('SYNTHETIC PRESENTATION WARNING', UserWarning)
            return original(*args, **kwargs)
        # A narrow early injected failure exercises retained diagnostics, not history.
        unit = self.output/'warning-unit'; unit.mkdir()
        put(unit/'PROTOCOL.md', (self.unit/'PROTOCOL.md').read_bytes())
        put(unit/'test_present.py', Path(__file__).read_bytes())
        def fail(*args, **kwargs):
            warn(*args, **kwargs)
            raise ValueError('synthetic-render-failure')
        with patch.object(p, 'UNIT', unit), patch.object(p, 'compose_page', fail):
            with self.assertRaisesRegex(ValueError, 'synthetic-render-failure'):
                p.run('run01', p.fingerprint(Path(p.__file__))['sha256'], self.protocol_pin)
        failure = json.loads((unit/'run01/failure.json').read_bytes())
        self.assertEqual(failure['phase'], 'presentation')
        self.assertEqual(failure['warnings'], [{'category': 'UserWarning', 'message': 'SYNTHETIC PRESENTATION WARNING'}])
        self.assertFalse((unit/'run01/receipt.json').exists())

    def test_post_runtime_change_refuses_admission(self):
        unit = self.output/'postchange-unit'; unit.mkdir()
        put(unit/'PROTOCOL.md', (self.unit/'PROTOCOL.md').read_bytes())
        put(unit/'test_present.py', Path(__file__).read_bytes())
        original = p.runtime_pins
        calls = 0
        def changed():
            nonlocal calls
            calls += 1
            pins = original()
            if calls == 2:
                pins[str(Path(p.__file__))] = {'bytes': 1, 'sha256': '0'*64}
            return pins
        # One synthetic page suffices to reach the unchanged post-pin gate.
        with patch.object(p, 'UNIT', unit), patch.object(p, 'runtime_pins', changed), \
                patch.object(p, 'pages', lambda: [list(range(6593,6599))]):
            with self.assertRaisesRegex(ValueError, 'input-or-runtime-changed'):
                p.run('run01', p.fingerprint(Path(p.__file__))['sha256'], self.protocol_pin)
        failure = json.loads((unit/'run01/failure.json').read_bytes())
        self.assertEqual(failure['phase'], 'post-pins')
        self.assertNotEqual(failure['runtime_pins_before'], failure['runtime_pins_after'])
        self.assertFalse((unit/'run01/receipt.json').exists())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'controls[0-9]{2}', args.out): raise ValueError('controls-output-scope')
    output = Path(__file__).resolve().parent/args.out
    if output.exists() or output.is_symlink(): raise ValueError('controls-output-exists')
    output.mkdir(exist_ok=False)
    Controls.output = output
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    put(output/'tests.txt', stream.getvalue().encode())
    p.write_json(output/'receipt.json', {'status': 'passed' if result.wasSuccessful() else 'failed',
        'execution_kind': 'synthetic-controls-only', 'tests_run': result.testsRun,
        'failures': len(result.failures), 'errors': len(result.errors), 'python': platform.python_version(),
        'pillow': p.PIL.__version__, 'command': sys.argv,
        'producer': p.fingerprint(Path(p.__file__)), 'tests': p.fingerprint(Path(__file__)),
        'test_output': p.fingerprint(output/'tests.txt')})
    print(stream.getvalue(), end='')
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__': main()
