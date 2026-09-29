"""Read-only Stage C pixel oracle; no producer import, crop or resize call."""
import argparse
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image, __version__ as pillow_version

UNIT = Path(__file__).resolve().parent
INDICES = sorted({6593, 6689, 6701, 6707, 6714, 6717, 6724, 6736,
                  6784, 6881, 6904, 7013} | set(range(6920, 6979)))
BOX = (300, 125, 465, 245)
SELECTION_SHA = 'e297292a04a093d757b7693b9914abe4b88db4e6b836461f49c8dee411e78b2d'
FREEZES = {
    'root-stage-b.md': 'c01c9fe3628fae76417d11c166f5981706162c93362984c6114157a6a70e2bbf',
    'root-stage-b-scope.md': '3135cf7600ab4b9cef7a60adef238cf653ce38a71fe7af64f54b98b3254124c3',
    'observer-stage-b.md': 'cea1a9c0db50d0ece47ceb19a877f97977d8348e47c61a84fc630ce5c54a6da5',
    'observer-stage-b-scope.md': '9794d0e106f87bdb0a8783c559992ec62757c9088ba993dd8d5a6da48e13809d',
    'STAGE-C.md': '7a1bf712a8d1b5dc629395e2c704afda1cce93068db386f0125e460663b2554d',
}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def oracle(raw, width, height, box, scale):
    require(type(raw) is bytes, 'bytes')
    require(type(width) is int and type(height) is int and width > 0 and height > 0, 'geometry')
    require(len(raw) == width * height, 'length')
    require(len(box) == 4 and all(type(n) is int for n in box), 'box-type')
    x0, y0, x1, y1 = box
    require(0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height, 'box-bounds')
    require(type(scale) is int and scale > 0, 'scale')
    rows = [raw[y * width + x0:y * width + x1] for y in range(y0, y1)]
    native = b''.join(rows)
    enlarged_rows = [b''.join(bytes([v]) * scale for v in row) for row in rows]
    return native, b''.join(row * scale for row in enlarged_rows)


def read_luma(encoded, size):
    with Image.open(io.BytesIO(encoded)) as image:
        require(image.format == 'PNG' and image.mode == 'L' and image.size == size, 'png-format')
        require(getattr(image, 'n_frames', 1) == 1, 'png-multiple-frames')
        require(not set(image.info) & {'transparency', 'gamma', 'srgb', 'icc_profile', 'chromaticity'}, 'png-rendering-metadata')
        return image.tobytes()


def check_image(path, metadata, expected, size):
    encoded = path.read_bytes()
    require(metadata['png'] == path.name, 'image-name')
    require(metadata['png_identity'] == {'bytes': len(encoded), 'sha256': digest(encoded)}, 'png-pin')
    require(metadata['size'] == list(size) and metadata['mode'] == 'L', 'image-description')
    raw = read_luma(encoded, size)
    require(raw == expected, 'pixel-mapping')
    require(metadata['luma_sha256'] == digest(raw), 'luma-pin')
    return encoded


def verify(first, second):
    require(first.resolve() != second.resolve(), 'distinct-runs-required')
    selection = UNIT / 'run01/camera2/selection.json'
    selection_bytes = selection.read_bytes()
    require(digest(selection_bytes) == SELECTION_SHA, 'selection-pin')
    source = json.loads(selection_bytes)['images']
    require([r['frame_index_zero_based'] for r in source] == [str(n) for n in range(6593, 7014)], 'source-order')
    lookup = {int(r['frame_index_zero_based']): r for r in source}
    for name, pin in FREEZES.items():
        require(digest((UNIT / name).read_bytes()) == pin, 'freeze-pin:' + name)
    require(len(INDICES) == 71, 'index-count')
    receipt_bytes = [(d / 'receipt.json').read_bytes() for d in (first, second)]
    receipts = [json.loads(data) for data in receipt_bytes]
    checked_files = {d / 'receipt.json': digest(data) for d, data in zip((first, second), receipt_bytes)}
    wanted = {f'f{n:06d}-{kind}.png' for n in INDICES for kind in ('native', '4x')}
    for d, r in zip((first, second), receipts):
        require(not (d / 'failure.json').exists(), 'failed-run')
        require(r['status'] == 'complete' and r['execution_kind'] == 'stage-c-historical-display', 'receipt-status')
        require(all(type(n) is int for n in r['indices']), 'index-types')
        require(r['indices'] == INDICES and r['rectangle_half_open'] == list(BOX), 'plan')
        require(type(r['scale']) is int and r['scale'] == 4 and r['resampling'] == 'NEAREST', 'transform')
        require(r['source_geometry'] == [640, 480] and r['source_mode'] == 'L', 'source-description')
        require([v['frame_index_zero_based'] for v in r['rows']] == INDICES, 'row-order')
        require(all(type(v['frame_index_zero_based']) is int for v in r['rows']), 'row-index-types')
        require({f.name for f in d.glob('*.png')} == wanted, 'png-file-set')
    for position, n in enumerate(INDICES):
        src = lookup[n]
        require(src['png'] == f'f{n:06d}.png', 'source-name')
        path = selection.parent / src['png']
        data = path.read_bytes()
        require(src['png_identity'] == {'bytes': len(data), 'sha256': digest(data)}, 'source-file-pin')
        checked_files[path] = digest(data)
        raw = read_luma(data, (640, 480))
        require(digest(raw) == src['luma_sha256'], 'source-luma-pin')
        require(Fraction(src['source_pts']) * Fraction(src['source_time_base']) == Fraction(src['source_time_seconds_exact']), 'source-time')
        expected = oracle(raw, 640, 480, BOX, 4)
        pairs = [[], []]
        for run, (directory, receipt) in enumerate(zip((first, second), receipts)):
            row = receipt['rows'][position]
            require(row['source'] == src, 'row-source-join')
            require(set(row['outputs']) == {'native', '4x'}, 'row-output-set')
            for kind, pixels, size in zip(('native', '4x'), expected, ((165, 120), (660, 480))):
                image_path = directory / f'f{n:06d}-{kind}.png'
                checked = check_image(image_path, row['outputs'][kind], pixels, size)
                checked_files[image_path] = digest(checked)
                pairs[run].append(checked)
        require(pairs[0] == pairs[1], 'paired-image-byte-equality')
    for name, pin in FREEZES.items():
        require(digest((UNIT / name).read_bytes()) == pin, 'freeze-changed:' + name)
    require(digest(selection.read_bytes()) == SELECTION_SHA, 'selection-changed')
    for path, pin in checked_files.items():
        require(digest(path.read_bytes()) == pin, 'checked-file-changed:' + path.name)
    return {'status': 'pass-pixels-metadata-only', 'source_frames': 71,
            'image_instances_verified': 284, 'paired_images': 142,
            'source_selection_sha256': SELECTION_SHA, 'declaration_and_freezes': FREEZES,
            'receipt_sha256': [digest(data) for data in receipt_bytes],
            'checker_sha256': digest(Path(__file__).read_bytes()), 'pillow': pillow_version,
            'oracle': 'integer byte slices and value/row repetition; no producer import/crop/resize',
            'limits': 'Shared PNG decoder; checks transformed bytes, not source authenticity or component identity; producer snapshot/runtime inventory checked separately.'}


class Controls(unittest.TestCase):
    def fixture_image(self, directory, pixels, mode='L'):
        p = Path(directory) / 'synthetic.png'
        Image.frombytes(mode, (2, 2), pixels).save(p)
        encoded = p.read_bytes()
        return p, {'png': p.name, 'png_identity': {'bytes': len(encoded), 'sha256': digest(encoded)},
                   'luma_sha256': digest(pixels), 'size': [2, 2], 'mode': mode}

    def test_good_image(self):
        with tempfile.TemporaryDirectory(prefix='stage-c-check-') as directory:
            p, meta = self.fixture_image(directory, bytes([1, 2, 3, 4]))
            self.assertEqual(check_image(p, meta, bytes([1, 2, 3, 4]), (2, 2)), p.read_bytes())

    def test_rehashed_wrong_pixel_rejects(self):
        with tempfile.TemporaryDirectory(prefix='stage-c-check-') as directory:
            p, meta = self.fixture_image(directory, bytes([1, 2, 3, 5]))
            with self.assertRaisesRegex(ValueError, 'pixel-mapping'):
                check_image(p, meta, bytes([1, 2, 3, 4]), (2, 2))

    def test_wrong_mode_and_pin_reject(self):
        with tempfile.TemporaryDirectory(prefix='stage-c-check-') as directory:
            p, meta = self.fixture_image(directory, bytes(12), mode='RGB')
            meta['mode'] = 'L'
            with self.assertRaisesRegex(ValueError, 'png-format'):
                check_image(p, meta, bytes(4), (2, 2))
            meta['png_identity']['sha256'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'png-pin'):
                check_image(p, meta, bytes(4), (2, 2))

    def test_duplicate_run_rejects_before_inputs(self):
        with self.assertRaisesRegex(ValueError, 'distinct-runs-required'):
            verify(Path('/private/tmp/stage-c-same'), Path('/private/tmp/stage-c-same'))

    def test_animated_png_rejects(self):
        buffer = io.BytesIO()
        first = Image.new('L', (2, 2), 20)
        first.save(buffer, format='PNG', save_all=True, append_images=[Image.new('L', (2, 2), 100)], duration=100)
        with self.assertRaisesRegex(ValueError, 'png-multiple-frames'):
            read_luma(buffer.getvalue(), (2, 2))

    def test_transparent_png_rejects(self):
        buffer = io.BytesIO()
        Image.new('L', (2, 2), 20).save(buffer, format='PNG', transparency=20)
        with self.assertRaisesRegex(ValueError, 'png-rendering-metadata'):
            read_luma(buffer.getvalue(), (2, 2))

    def test_known_small_mapping(self):
        a, b = oracle(bytes(range(12)), 4, 3, (1, 1, 4, 3), 2)
        self.assertEqual(a, bytes([5, 6, 7, 9, 10, 11]))
        self.assertEqual(b, bytes([5, 5, 6, 6, 7, 7] * 2 + [9, 9, 10, 10, 11, 11] * 2))

    def test_identity(self):
        self.assertEqual(oracle(b'\x01\x02\x03\x04', 2, 2, (0, 0, 2, 2), 1), (b'\x01\x02\x03\x04',) * 2)

    def test_bounds(self):
        for box in [(-1, 0, 1, 1), (0, 0, 3, 1), (0, 1, 1, 1), (0, 0, 1, 3)]:
            with self.assertRaises(ValueError):
                oracle(bytes(4), 2, 2, box, 4)

    def test_strict_types(self):
        for scale in [True, 1.0, 0, -1]:
            with self.assertRaises(ValueError):
                oracle(bytes(4), 2, 2, (0, 0, 1, 1), scale)
        with self.assertRaises(ValueError):
            oracle(bytes(4), 2, 2, (0.0, 0, 1, 1), 4)

    def test_source_length(self):
        with self.assertRaises(ValueError):
            oracle(bytes(3), 2, 2, (0, 0, 1, 1), 4)

    def test_exact_plan(self):
        self.assertEqual(len(INDICES), 71)
        self.assertEqual(INDICES[11:70], list(range(6920, 6979)))
        self.assertEqual(INDICES[-1], 7013)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()
    if args.test:
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
        raise SystemExit(not result.wasSuccessful())
    print(json.dumps(verify(UNIT / 'stage-c-run01', UNIT / 'stage-c-run02'), indent=2, sort_keys=True))
