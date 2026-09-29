"""Synthetic Stage C controls; never render or display historical pixels."""
import argparse
from contextlib import ExitStack, redirect_stderr, redirect_stdout
import copy
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import sys
import unittest
from unittest.mock import patch
import warnings

sys.dont_write_bytecode = True
from PIL import Image
import stage_c_display as sc

CONTROL = None
BASE = None


def json_replace(path, value):
    # Only called for this suite's deliberately mutable synthetic fixtures.
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def synthetic_selection():
    rows = []
    for index in range(6593, 7014):
        pts = index * 100 + index % 3
        rows.append({'frame_index_zero_based': str(index), 'source_pts': str(pts),
            'best_effort_timestamp': str(pts), 'source_time_base': '1/2997',
            'source_time_seconds_exact': str(Fraction(pts, 2997)),
            'source_duration_ticks': 100, 'source_duration_seconds_exact': '100/2997',
            'png': f'f{index:06d}.png', 'png_identity': {'bytes': 1, 'sha256': '0' * 64},
            'luma_sha256': '0' * 64})
    return {'source_id': 'VID-WTC7-001', 'checked_frames': 8042, 'exit_code': 0,
            'geometry': [640, 480], 'images': rows}


def oracle(source_bytes):
    """Independent byte-row oracle: no PIL crop/resize and no producer helper."""
    native_rows = [source_bytes[y * 640 + 300:y * 640 + 465] for y in range(125, 245)]
    native = b''.join(native_rows)
    enlarged = b''.join(b''.join(bytes((value,)) * 4 for value in row) * 4 for row in native_rows)
    return native, enlarged


def prepare_base():
    root = CONTROL / 'synthetic-base'
    unit = root / 'unit'
    source = unit / 'run01/camera2'
    source.mkdir(parents=True)
    for path in sc.PINS:
        if path == sc.CROP_MODULE or path == sc.SOURCE / 'selection.json':
            continue
        destination = root / 'CHARTER.md' if path.name == 'CHARTER.md' else unit / path.name
        shutil.copyfile(path, destination)
    shutil.copyfile(sc.UNIT / 'test_stage_c_display.py', unit / 'test_stage_c_display.py')
    document = synthetic_selection()
    pattern = bytes((17 * x + 29 * y + (x * y) % 251) % 256 for y in range(480) for x in range(640))
    for row in document['images']:
        index = int(row['frame_index_zero_based'])
        if index in sc.INDICES:
            plane = pattern.translate(bytes((value + index) % 256 for value in range(256)))
            with (source / row['png']).open('xb') as stream:
                Image.frombytes('L', (640, 480), plane).save(stream, format='PNG')
            row['png_identity'] = sc.fingerprint(source / row['png'])
            row['luma_sha256'] = hashlib.sha256(plane).hexdigest()
    sc.write_json(source / 'selection.json', document)
    return root


class Controls(unittest.TestCase):
    def setUp(self):
        case = CONTROL / self._testMethodName
        shutil.copytree(BASE, case)
        self.unit = case / 'unit'
        self.source = self.unit / 'run01/camera2'
        self.out = self.unit / 'stage-c-run01'
        self.selection = self.source / 'selection.json'
        pins = {path if path == sc.CROP_MODULE else
                (case / 'CHARTER.md' if path.name == 'CHARTER.md' else
                 self.selection if path == sc.SOURCE / 'selection.json' else self.unit / path.name): digest
                for path, digest in sc.PINS.items()}
        pins[self.selection] = sc.fingerprint(self.selection)['sha256']
        stack = self.enterContext(ExitStack())
        for name, value in [('UNIT', self.unit), ('SOURCE', self.source), ('PINS', pins),
                            ('EXECUTION_KIND', 'stage-c-synthetic-control')]:
            stack.enter_context(patch.object(sc, name, value))

    def change_selection(self, edit):
        document = json.loads(self.selection.read_text())
        edit(document)
        json_replace(self.selection, document)
        sc.PINS[self.selection] = sc.fingerprint(self.selection)['sha256']

    def replace_first_image(self, image):
        row = json.loads(self.selection.read_text())['images'][0]
        path = self.source / row['png']
        image.save(path, format='PNG')
        self.change_selection(lambda document: document['images'][0].update(
            png_identity=sc.fingerprint(path), luma_sha256=hashlib.sha256(image.tobytes()).hexdigest()))

    def failed(self, phase):
        receipt = json.loads((self.out / 'failure.json').read_text())
        self.assertEqual(receipt['status'], 'failed')
        self.assertEqual(receipt['execution_kind'], 'stage-c-synthetic-control')
        self.assertEqual(receipt['phase'], phase)
        self.assertFalse((self.out / 'receipt.json').exists())
        return receipt

    def test_fixed_selection_exact_pts_and_order(self):
        selected = sc.select_rows(synthetic_selection())
        expected = [6593, 6689, 6701, 6707, 6714, 6717, 6724, 6736, 6784, 6881, 6904,
                    *range(6920, 6979), 7013]
        self.assertEqual([int(row['frame_index_zero_based']) for row in selected], expected)
        self.assertEqual(len(selected), 71)
        for row in selected:
            self.assertEqual(Fraction(row['source_time_seconds_exact']),
                             int(row['source_pts']) * Fraction(row['source_time_base']))

    def test_selection_rejects_order_duplicate_missing_and_noncanonical(self):
        for edit in [lambda rows: rows.reverse(), lambda rows: rows.append(copy.deepcopy(rows[0])),
                     lambda rows: rows.pop(1), lambda rows: rows[0].update(frame_index_zero_based='06593'),
                     lambda rows: rows[0].update(frame_index_zero_based=6593),
                     lambda rows: rows[0].update(png='../f006593.png')]:
            document = synthetic_selection()
            edit(document['images'])
            with self.subTest(edit=edit), self.assertRaises(ValueError):
                sc.select_rows(document)

    def test_selection_rejects_bad_time_identity_and_duration(self):
        for update in [{'source_pts': '659300.0'}, {'best_effort_timestamp': '1'},
                       {'source_time_base': '2/5994'}, {'source_time_base': '1/3000'},
                       {'source_time_seconds_exact': '220'}, {'source_duration_ticks': True},
                       {'source_duration_ticks': 0}, {'source_duration_seconds_exact': '1'}]:
            document = synthetic_selection()
            document['images'][0].update(update)
            with self.subTest(update=update), self.assertRaises(ValueError):
                sc.select_rows(document)

    def test_selection_failure_receipt(self):
        self.change_selection(lambda document: document['images'][0].update(source_pts='1'))
        with self.assertRaisesRegex(ValueError, 'pts-best-effort'):
            sc.run(self.out)
        self.failed('selection')

    def test_bad_pin_precedes_import_or_image_read(self):
        sc.PINS[self.selection] = '0' * 64
        with patch.object(sc, 'load_crop') as load, patch.object(sc, 'read_source') as read:
            with self.assertRaisesRegex(ValueError, 'input-pin'):
                sc.run(self.out)
        load.assert_not_called()
        read.assert_not_called()
        self.failed('input-pins')

    def test_pinned_crop_rejected_without_running_main(self):
        with patch.object(sc, 'CROP_SHA', '0' * 64):
            with self.assertRaisesRegex(ValueError, 'crop-code-pin'):
                sc.run(self.out)
        self.failed('input-pins')

    def test_runtime_version_and_fixed_geometry_guards(self):
        with patch.object(sc.platform, 'python_version', return_value='0.0.0'):
            with self.assertRaisesRegex(ValueError, 'python-version'):
                sc.runtime_inputs()
        with patch.object(sc.PIL, '__version__', '0.0.0'):
            with self.assertRaisesRegex(ValueError, 'pillow-version'):
                sc.runtime_inputs()
        with patch.object(sc, 'RECTANGLE', (301, 125, 466, 245)):
            with self.assertRaisesRegex(ValueError, 'fixed-transform'):
                sc.run(self.out)
        self.failed('input-pins')

    def test_wrong_source_dimensions(self):
        self.replace_first_image(Image.new('L', (639, 480)))
        with self.assertRaisesRegex(ValueError, 'source-image-geometry'):
            sc.run(self.out)
        self.failed('render')

    def test_wrong_source_mode(self):
        self.replace_first_image(Image.new('RGB', (640, 480)))
        with self.assertRaisesRegex(ValueError, 'source-image-geometry'):
            sc.run(self.out)
        self.failed('render')

    def test_consistent_hash_multiframe_source_rejected(self):
        path = self.source / 'f006593.png'
        image = Image.new('L', (640, 480), 17)
        image.save(path, format='PNG', save_all=True,
                   append_images=[Image.new('L', (640, 480), 61)], duration=[100, 100], loop=0)
        self.change_selection(lambda document: document['images'][0].update(
            png_identity=sc.fingerprint(path), luma_sha256=hashlib.sha256(image.tobytes()).hexdigest()))
        with self.assertRaisesRegex(ValueError, 'source-image-frames'):
            sc.run(self.out)
        self.failed('render')

    def test_render_affecting_metadata_rejected(self):
        path = self.source / 'f006593.png'
        image = Image.new('L', (640, 480), 17)
        image.save(path, format='PNG', transparency=17)
        self.change_selection(lambda document: document['images'][0].update(
            png_identity=sc.fingerprint(path), luma_sha256=hashlib.sha256(image.tobytes()).hexdigest()))
        with self.assertRaisesRegex(ValueError, 'source-render-metadata'):
            sc.run(self.out)
        self.failed('render')

    def test_wrong_luma_hash(self):
        self.change_selection(lambda document: document['images'][0].update(luma_sha256='0' * 64))
        with self.assertRaisesRegex(ValueError, 'source-luma-pin'):
            sc.run(self.out)
        self.failed('render')

    def test_wrong_png_hash_before_render(self):
        path = self.source / 'f006593.png'
        with path.open('ab') as stream:
            stream.write(b'synthetic corruption')
        with patch.object(sc, 'read_source') as read:
            with self.assertRaisesRegex(ValueError, 'source-png-pin'):
                sc.run(self.out)
        read.assert_not_called()
        self.failed('selection')

    def test_collision_preserves_existing_and_refuses_unscoped_paths(self):
        self.out.mkdir()
        sentinel = self.out / 'sentinel'
        sentinel.write_bytes(b'preserve this synthetic existing artifact')
        with self.assertRaisesRegex(ValueError, 'output-already-exists'):
            sc.run(self.out)
        self.assertEqual(list(self.out.iterdir()), [sentinel])
        self.assertEqual(sentinel.read_bytes(), b'preserve this synthetic existing artifact')
        for path in [self.unit, self.unit.parent / 'stage-c-run01', self.unit / 'other',
                     self.unit / 'nested/stage-c-run01', self.unit / 'stage-c-run01/../stage-c-run02']:
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'output-scope'):
                sc.fresh_output(path)

    def test_output_and_source_symlinks_rejected(self):
        self.out.symlink_to(self.unit / 'absent', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'output-symlink'):
            sc.run(self.out)
        self.assertTrue(self.out.is_symlink())
        self.assertFalse((self.unit / 'absent').exists())
        path = self.source / 'f006593.png'
        sibling = self.source / 'synthetic-identical-copy.png'
        path.rename(sibling)
        path.symlink_to(sibling)
        with self.assertRaisesRegex(ValueError, 'source-symlink'):
            sc.run(self.unit / 'stage-c-run02')
        self.out = self.unit / 'stage-c-run02'
        self.failed('selection')

    def test_source_mutation_after_render_rejected(self):
        inherited = sc.load_crop()
        original = inherited.crop
        changed = False

        def mutate(image, rectangle, scale):
            nonlocal changed
            result = original(image, rectangle, scale)
            if not changed:
                with (self.source / 'f006593.png').open('ab') as stream:
                    stream.write(b'synthetic post-read source mutation')
                changed = True
            return result

        with patch.object(inherited, 'crop', mutate), patch.object(sc, 'load_crop', return_value=inherited):
            with self.assertRaisesRegex(ValueError, 'source-or-dependency-changed'):
                sc.run(self.out)
        failure = self.failed('post-input-pins')
        self.assertNotEqual(failure['input_pins_before'], failure['input_pins_after'])
        self.assertEqual(len(list(self.out.glob('*.png'))), 142)

    def test_frozen_input_mutation_rejected(self):
        inherited = sc.load_crop()
        original = inherited.crop

        def mutate(image, rectangle, scale):
            (self.unit / 'root-stage-b.md').write_bytes(b'synthetic changed frozen input')
            return original(image, rectangle, scale)

        with patch.object(inherited, 'crop', mutate), patch.object(sc, 'load_crop', return_value=inherited):
            with self.assertRaisesRegex(ValueError, 'source-or-dependency-changed'):
                sc.run(self.out)
        self.failed('post-input-pins')

    def test_runtime_code_mutation_rejected(self):
        inherited = sc.load_crop()
        original = inherited.crop

        def mutate(image, rectangle, scale):
            (self.unit / 'test_stage_c_display.py').write_bytes(b'# synthetic changed code fixture\n')
            return original(image, rectangle, scale)

        with patch.object(inherited, 'crop', mutate), patch.object(sc, 'load_crop', return_value=inherited):
            with self.assertRaisesRegex(ValueError, 'runtime-or-code-changed'):
                sc.run(self.out)
        failure = self.failed('post-runtime-pins')
        self.assertNotEqual(failure['runtime_pins_before'], failure['runtime_pins_after'])

    def test_warning_retained_and_rejected(self):
        inherited = sc.load_crop()
        original = inherited.crop
        warned = False

        def warn(image, rectangle, scale):
            nonlocal warned
            if not warned:
                warnings.warn('synthetic test warning', UserWarning)
                warned = True
            return original(image, rectangle, scale)

        with patch.object(inherited, 'crop', warn), patch.object(sc, 'load_crop', return_value=inherited):
            with self.assertRaisesRegex(ValueError, 'unexpected-warning'):
                sc.run(self.out)
        self.assertEqual(self.failed('post-runtime-pins')['warnings'],
                         [{'category': 'UserWarning', 'message': 'synthetic test warning'}])

    def test_output_write_error_retained(self):
        with patch.object(Image.Image, 'save', side_effect=OSError('synthetic write failure')):
            with self.assertRaisesRegex(OSError, 'synthetic write failure'):
                sc.run(self.out)
        failure = self.failed('render')
        self.assertEqual(failure['error_type'], 'OSError')
        self.assertIn('f006593-native.png', failure['partial_products'])

    def test_complete_fixture_two_runs_and_independent_pixels(self):
        first = sc.run(self.out)
        second_path = self.unit / 'stage-c-run02'
        second = sc.run(second_path)
        self.assertEqual(first['status'], 'complete')
        self.assertEqual(first['execution_kind'], 'stage-c-synthetic-control')
        self.assertEqual(len(first['rows']), 71)
        self.assertEqual(first['input_pins_before'], first['input_pins_after'])
        self.assertEqual(first['runtime_pins_before'], first['runtime_pins_after'])
        self.assertEqual(first['rows'], second['rows'])
        expected_names = {f'f{index:06d}-{kind}.png' for index in sc.INDICES for kind in ('native', '4x')}
        self.assertEqual({p.name for p in self.out.glob('*.png')}, expected_names)
        for row in first['rows']:
            with Image.open(self.source / row['source']['png']) as image:
                expected = oracle(image.tobytes())
            self.assertEqual(row['frame_index_zero_based'], int(row['source']['frame_index_zero_based']))
            for (kind, dimensions), pixels in zip([('native', (165, 120)), ('4x', (660, 480))], expected):
                product = row['outputs'][kind]
                path = self.out / product['png']
                self.assertEqual(path.read_bytes(), (second_path / product['png']).read_bytes())
                self.assertEqual(sc.fingerprint(path), product['png_identity'])
                self.assertEqual(hashlib.sha256(pixels).hexdigest(), product['luma_sha256'])
                with Image.open(path) as image:
                    self.assertEqual((image.mode, image.size), ('L', dimensions))
                    self.assertEqual(getattr(image, 'n_frames', 1), 1)
                    self.assertEqual(image.info, {})
                    self.assertEqual(image.tobytes(), pixels)
        for name, identity in first['products'].items():
            self.assertEqual(sc.fingerprint(self.out / name), identity)
        self.assertEqual((self.out / 'stage-c-snapshot.md').read_bytes(), (self.unit / 'STAGE-C.md').read_bytes())
        self.assertFalse((self.out / 'failure.json').exists())

    def test_oracle_detects_single_bad_pixel_and_block_mapping(self):
        image = Image.frombytes('L', (640, 480), bytes(index % 251 for index in range(640 * 480)))
        native, enlarged = sc.load_crop().crop(image, sc.RECTANGLE, sc.SCALE)
        expected_native, expected_enlarged = oracle(image.tobytes())
        self.assertEqual(native.tobytes(), expected_native)
        self.assertEqual(enlarged.tobytes(), expected_enlarged)
        enlarged.putpixel((659, 479), (enlarged.getpixel((659, 479)) + 1) % 256)
        self.assertNotEqual(enlarged.tobytes(), expected_enlarged)
        native.putpixel((0, 0), (native.getpixel((0, 0)) + 1) % 256)
        self.assertNotEqual(native.tobytes(), expected_native)

    def test_cli_dispatch_and_no_input_or_transform_overrides(self):
        with patch.object(sc, 'run', return_value={'status': 'complete', 'rows': [None] * 71}) as execute:
            with redirect_stdout(io.StringIO()):
                sc.main(['--out', 'stage-c-run01'])
        execute.assert_called_once_with('stage-c-run01')
        for extra in [['--source', 'elsewhere'], ['--scale', '5'], ['--camera', 'camera4']]:
            with patch.object(sc, 'run') as execute, redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    sc.main(['--out', 'stage-c-run01', *extra])
            self.assertEqual(caught.exception.code, 2)
            execute.assert_not_called()


def fresh_control_root(value):
    path = Path(value)
    if not path.is_absolute():
        path = sc.UNIT / path
    require_relative = path.relative_to(sc.UNIT)
    parts = require_relative.parts
    sc.require(1 <= len(parts) <= 2 and re.fullmatch(r'stage-c-driver-controls(?:-root)?[0-9]{2}', parts[0]),
               'control-output-scope')
    sc.require(len(parts) == 1 or re.fullmatch(r'attempt[0-9]{2}', parts[1]), 'control-attempt-scope')
    sc.require(all(not part.is_symlink() for part in (path, path.parent)), 'control-output-symlink')
    sc.require(not path.exists() and path.resolve().is_relative_to(sc.UNIT), 'control-output-collision')
    return path


def protected_pins():
    pins = sc.pinned_inputs()
    pins.update(sc.runtime_inputs())
    document = json.loads((sc.SOURCE / 'selection.json').read_text())
    for row in sc.select_rows(document):
        path = sc.SOURCE / row['png']
        identity = sc.fingerprint(path)
        sc.require(identity == row['png_identity'], 'historical-png-preservation-pin')
        pins[str(path)] = identity
    return pins


def main():
    global CONTROL, BASE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    CONTROL = fresh_control_root(args.out)
    CONTROL.mkdir(parents=True, exist_ok=False)
    before = protected_pins()
    sc.write_json(CONTROL / 'protected-pins-before.json', before)
    for path, name in [(Path(sc.__file__), 'driver-snapshot.py'), (Path(__file__), 'test-snapshot.py'),
                       (sc.CROP_MODULE, 'inherited-crop-snapshot.py'), (sc.UNIT / 'STAGE-C.md', 'stage-c-snapshot.md')]:
        with (CONTROL / name).open('xb') as stream:
            stream.write(path.read_bytes())
    BASE = prepare_base()
    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(sc.load_crop().Controls),
                               unittest.defaultTestLoader.loadTestsFromTestCase(Controls)])
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    after = protected_pins()
    sc.write_json(CONTROL / 'protected-pins-after.json', after)
    with (CONTROL / 'tests.log').open('x') as stream:
        stream.write(log.getvalue())
    print(log.getvalue(), end='')
    preserved = before == after
    sc.write_json(CONTROL / 'receipt.json', {'status': 'pass' if result.wasSuccessful() and preserved else 'fail',
        'execution_kind': 'synthetic-controls-no-historical-render-or-view', 'command': sys.argv,
        'tests': result.testsRun, 'inherited_tests': 5, 'failures': len(result.failures), 'errors': len(result.errors),
        'protected_unchanged': preserved, 'python': sys.version, 'pillow': sc.PIL.__version__,
        'code': sc.fingerprint(Path(sc.__file__)), 'tests_code': sc.fingerprint(Path(__file__)),
        'products': {str(path.relative_to(CONTROL)): sc.fingerprint(path)
                     for path in sorted(CONTROL.rglob('*')) if path.is_file() and not path.is_symlink()},
        'symlinks': {str(path.relative_to(CONTROL)): str(path.readlink())
                     for path in sorted(CONTROL.rglob('*')) if path.is_symlink()}})
    raise SystemExit(0 if result.wasSuccessful() and preserved else 1)


if __name__ == '__main__':
    main()
