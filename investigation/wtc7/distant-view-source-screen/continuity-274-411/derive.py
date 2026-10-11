#!/usr/bin/env python3
"""Fixed ordinal derivation and categorical-roster checks; never judges a frame.

Use --self-test for synthetic fixtures only.  Historical processing is the
separate, explicit `run --out run01` command.  Its outputs remain unaccepted
derivatives until the independent pixel checker and actual readers review them.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import selectors
import subprocess
import sys
import tempfile
import time
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
FIRST, LAST, COUNT = 274, 411, 962
WIDTH, HEIGHT = 704, 480
BOX = (350, 90, 630, 380)
CROP_SIZE = (280, 290)
COLS, ROWS, GUTTER, LABEL = 4, 3, 12, 22
PAGE_SIZE = (COLS * 280 + (COLS + 1) * GUTTER,
             ROWS * (290 + LABEL) + (ROWS + 1) * GUTTER)
FRAME_BYTES = WIDTH * HEIGHT * 3 // 2
RAW_BYTES = FRAME_BYTES * COUNT
DIAGNOSTIC_BYTES = 1024 * 1024
DECODER = Path('/opt/homebrew/bin/ffmpeg')
MEDIA = PARENT / 'source/DistantViewWTC7.avi'
TIMESTAMP_KEYS = ('index', 'stored_pts', 'best_effort_timestamp',
                  'stored_pts_seconds_exact', 'best_effort_seconds_exact')
INPUT_HASHES = {
    HERE / 'PROTOCOL.md': '230777a8aff939d2fcc76386fcdc18e26449305c8ba1da34874cdf387af9b970',
    MEDIA: 'a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e',
    DECODER: '7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569',
    PARENT / 'probe02/selection.json': '4b5110f731a6f3b13b2ab324571c0687e2c6304d1755f40441259c0bc35fead3',
    PARENT / 'probe02/probe.json': '30ffecbe23b289c8069dff8d174e19d0fac3af4c6f4fab0c90c6bf8d2a04d467',
    PARENT / 'views01/frames.json': '047cb354cfabe633f92ed4c10ecb283fde955d3787198477f50710d4eef812ce',
    PARENT / 'views01/receipt.json': '7a35a72597746c9b48e6ccc537ea58e8c9b4c45deb42eec065a3e3da2f7108ff',
    PARENT / 'source/receipt.json': '47f642341459f9857a84cdf4e6804cd954786272513bf7c34fcbd74a7ecddf3f',
    PARENT / 'independent-verification.json': '72eefba7acb6fbd2970d6aaef6ae8b274056170a805b467f1ad178a723c772c4',
    PARENT / 'ordinal_screen.py': '1c1a91e26062155c842908dd29f631f0da0868a34f6cf1eee4c3c3b7aa412b59',
    PARENT / 'prepare.py': 'f3a3be5e9335cdf50b336fe29acd7d5d92b6e6b3f7b726a1427796e365241a93',
    PARENT / 'PROTOCOL.md': '47cd92e19bc8d2796e66efaf3e828ba9589d3d254da920de3a6802e7727c0daf',
    PARENT / 'ORDINAL-ADDENDUM.md': '930123e028a5c0feadf58b6967cf1d789f5bc8a5e0d6fc12e582c527b3dfd293',
    PARENT.parent / 'tilted-camera-source-join/prepare_media.py':
        'b8d2010b99001dba79d10b887571ffdfa53b13d8b6800f26a1ed4442c11ba0d5',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    with Path(path).open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': Path(path).stat().st_size, 'sha256': digest}


def write_json(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write('\n')


def write_bytes(path, value):
    with Path(path).open('xb') as stream:
        stream.write(value)


def safe_output(name):
    require(isinstance(name, str) and re.fullmatch(r'[a-z][a-z0-9_-]*', name),
            'unsafe output name')
    out = HERE / name
    require(not out.exists() and not out.is_symlink(), 'output already exists')
    return out


def input_snapshot():
    result = {}
    for path, expected in INPUT_HASHES.items():
        actual = pin(path)
        require(actual['sha256'] == expected, 'input hash mismatch: ' + str(path))
        result[str(path)] = actual
    result[str(Path(__file__).resolve())] = pin(__file__)
    require(result[str(MEDIA)]['bytes'] == 4749520, 'source size mismatch')
    return result


def load_helpers():
    """Reuse the pinned nullable parser, not its earlier diagnostic wrapper."""
    for name in ('ordinal_screen.py', 'prepare.py'):
        require(pin(PARENT / name)['sha256'] == INPUT_HASHES[PARENT / name],
                'helper hash mismatch')
    spec = importlib.util.spec_from_file_location('frozen_ordinal_screen', PARENT / 'ordinal_screen.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decoder_command():
    return [str(DECODER), '-nostdin', '-nostats', '-hide_banner', '-v', 'warning',
            '-copyts', '-noautorotate', '-i', str(MEDIA), '-map', '0:v:0', '-an',
            '-noautoscale', '-pix_fmt', 'yuv420p', '-fps_mode', 'passthrough',
            '-enc_time_base:v', 'demux', '-f', 'rawvideo', '-']


def bounded_capture(argv, directory, stdout_limit, timeout=60, diagnostic_limit=DIAGNOSTIC_BYTES):
    """Read bounded pipes; persist partial evidence before rejecting any failure.

    Hashes/counts describe bytes actually captured, not unobserved output after
    termination. Only bounded prefixes are persisted; raw stdout is kept in
    memory up to stdout_limit+1. No retry or warning waiver is performed.
    """
    directory.mkdir()
    started = time.monotonic()
    buffers = {'stdout': bytearray(), 'stderr': bytearray()}
    status, returncode, error = 'returned', None, None
    process = None
    with selectors.DefaultSelector() as selector:
        try:
            process = subprocess.Popen(argv, stdin=subprocess.DEVNULL,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for name in buffers:
                pipe = getattr(process, name)
                os.set_blocking(pipe.fileno(), False)
                selector.register(pipe, selectors.EVENT_READ, name)
            while selector.get_map():
                remaining = timeout - (time.monotonic() - started)
                if remaining <= 0:
                    status = 'timeout'
                    break
                for key, _ in selector.select(min(remaining, 0.1)):
                    name = key.data
                    limit = stdout_limit if name == 'stdout' else diagnostic_limit
                    chunk = os.read(key.fileobj.fileno(), min(65536, limit + 1 - len(buffers[name])))
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    buffers[name].extend(chunk)
                    if len(buffers[name]) > limit:
                        status = name + '_oversize'
                        break
                if status != 'returned':
                    break
            if status == 'returned':
                remaining = max(0.001, timeout - (time.monotonic() - started))
                try:
                    returncode = process.wait(timeout=remaining)
                except subprocess.TimeoutExpired:
                    status = 'timeout'
        except OSError as exc:
            status, error = 'launch_or_pipe_error', str(exc)
        finally:
            if process is not None:
                if process.poll() is None:
                    process.kill()
                returncode = process.wait()
                process.stdout.close()
                process.stderr.close()
    receipt = {'argv': argv, 'status': status, 'returncode': returncode,
               'timeout_seconds': timeout, 'elapsed_seconds': time.monotonic() - started,
               'stdout_limit': stdout_limit, 'diagnostic_prefix_limit': diagnostic_limit,
               'capture_complete': status == 'returned', 'error': error}
    for name, data in buffers.items():
        prefix = data[:diagnostic_limit]
        filename = name + '-prefix.bin'
        write_bytes(directory / filename, prefix)
        receipt[name] = {'captured_bytes': len(data), 'captured_sha256': sha(data),
                         'saved_prefix': filename, 'saved_bytes': len(prefix),
                         'saved_sha256': sha(prefix), 'saved_prefix_truncated': len(prefix) < len(data)}
    write_json(directory / 'execution.json', receipt)
    require(status == 'returned', 'decoder capture stopped: ' + status)
    require(returncode == 0, 'decoder returned nonzero')
    require(not buffers['stderr'], 'decoder warning/error requires review')
    return buffers['stdout'], receipt


def validate_metadata(selection, frames, parsed_rows, geometry):
    require(selection['n'] == COUNT and selection['geometry'] == [WIDTH, HEIGHT],
            'fixed source count/geometry changed')
    require(tuple(geometry) == (WIDTH, HEIGHT), 'probe geometry changed')
    require(selection['frames'] == parsed_rows and len(parsed_rows) == COUNT,
            'nullable timestamp map changed')
    require(len(frames) == COUNT, 'hash roster count changed')
    for index, (row, hashed) in enumerate(zip(parsed_rows, frames)):
        require(row['index'] == index and hashed['index'] == index, 'ordinal gap/duplicate')
        require({key: hashed[key] for key in TIMESTAMP_KEYS} == row, 'timestamp/hash map mismatch')
        for field in ('decoded_sha256', 'luma_sha256'):
            require(isinstance(hashed[field], str) and re.fullmatch(r'[0-9a-f]{64}', hashed[field]),
                    'invalid expected digest')


def verify_decoded(raw, expected, width=WIDTH, height=HEIGHT):
    frame_bytes = width * height * 3 // 2
    require(len(raw) == len(expected) * frame_bytes, 'decoded byte/count mismatch')
    view = memoryview(raw)
    checked = []
    for index, row in enumerate(expected):
        require(row['index'] == index, 'expected hash ordinal gap/duplicate')
        frame = view[index * frame_bytes:(index + 1) * frame_bytes]
        decoded, luma = sha(frame), sha(frame[:width * height])
        require(decoded == row['decoded_sha256'], 'decoded hash mismatch at ' + str(index))
        require(luma == row['luma_sha256'], 'luma hash mismatch at ' + str(index))
        checked.append({**row, 'decoded_sha256': decoded, 'luma_sha256': luma})
    return checked


def crop_pixels(data, width=WIDTH, height=HEIGHT, box=BOX):
    require(len(data) == width * height, 'luma length mismatch')
    require(len(box) == 4 and all(type(v) is int for v in box), 'invalid crop rectangle')
    x0, y0, x1, y1 = box
    require(0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height, 'crop outside source')
    return b''.join(bytes(data[y * width + x0:y * width + x1]) for y in range(y0, y1))


def page_layout():
    pages = []
    for page in range(12):
        cells = []
        for slot in range(12):
            ordinal = FIRST + page * 12 + slot
            row, col = divmod(slot, COLS)
            x = GUTTER + col * (CROP_SIZE[0] + GUTTER)
            y = GUTTER + row * (CROP_SIZE[1] + LABEL + GUTTER)
            cells.append({'slot': slot, 'row': row, 'column': col,
                          'index': ordinal if ordinal <= LAST else None,
                          'blank': ordinal > LAST,
                          'label': 'BLANK - no frame' if ordinal > LAST else 'frame ' + str(ordinal),
                          'label_origin': [x, y],
                          'page_box': [x, y + LABEL, x + CROP_SIZE[0], y + LABEL + CROP_SIZE[1]],
                          'source_box': list(BOX) if ordinal <= LAST else None})
        pages.append({'page': page + 1, 'size': list(PAGE_SIZE), 'cells': cells})
    return pages


def make_page(layout, crops):
    from PIL import Image, ImageDraw, ImageFont
    page = Image.new('L', PAGE_SIZE, 255)
    draw = ImageDraw.Draw(page)
    font = ImageFont.load_default(size=12)
    for cell in layout['cells']:
        x, y = cell['label_origin']
        bounds = draw.textbbox((x, y), cell['label'], font=font)
        require(bounds[0] >= x and bounds[1] >= y and bounds[2] <= x + CROP_SIZE[0]
                and bounds[3] <= y + LABEL, 'label would overlap crop/gutter')
        draw.text((x, y), cell['label'], fill=0, font=font)
        if not cell['blank']:
            pixels = crops[cell['index']]
            require(len(pixels) == CROP_SIZE[0] * CROP_SIZE[1], 'crop pixel count')
            page.paste(Image.frombytes('L', CROP_SIZE, pixels), tuple(cell['page_box'][:2]))
        actual = page.crop(tuple(cell['page_box'])).tobytes()
        expected = b'\xff' * (CROP_SIZE[0] * CROP_SIZE[1]) if cell['blank'] else crops[cell['index']]
        require(actual == expected, 'page cell pixel mismatch')
    return page


def save_png(path, image, expected_pixels):
    from PIL import Image
    with path.open('xb') as stream:
        image.save(stream, format='PNG')
    with Image.open(path) as readback:
        require(readback.mode == 'L' and readback.size == image.size
                and readback.tobytes() == expected_pixels, 'PNG pixel mismatch')
    return {'path': path.name, **pin(path), 'pixel_sha256': sha(expected_pixels),
            'mode': 'L', 'size': list(image.size)}


def expand_ranges(records, kind):
    """Expand only explicit observed ranges; never fill missing judgments.

    Both kinds use {first,last,status,reason}; endpoints are inclusive.
    For links first/last are left-frame ordinals, each denoting (n,n+1).
    """
    require(kind in ('frames', 'links') and isinstance(records, list), 'invalid range kind/list')
    end = LAST if kind == 'frames' else LAST - 1
    allowed = ('V', 'A', 'O', 'X') if kind == 'frames' else ('supported', 'uncertain', 'broken')
    expanded, seen = [], set()
    for record in records:
        require(isinstance(record, dict) and set(record) == {'first', 'last', 'status', 'reason'},
                'range needs exactly first,last,status,reason; no defaults/fill')
        first, last = record['first'], record['last']
        require(type(first) is int and type(last) is int and FIRST <= first <= last <= end,
                'range bounds invalid')
        require(record['status'] in allowed and isinstance(record['reason'], str)
                and record['reason'].strip(), 'explicit single judgment and reason required')
        for index in range(first, last + 1):
            require(index not in seen, 'duplicate range coverage')
            seen.add(index)
            identity = {'ordinal': index} if kind == 'frames' else {'from': index, 'to': index + 1}
            expanded.append({**identity, 'status': record['status'], 'reason': record['reason']})
    require(seen == set(range(FIRST, end + 1)), 'range coverage gap')
    return sorted(expanded, key=lambda row: row['ordinal'] if kind == 'frames' else row['from'])


def validate_roster(frames, links):
    require(isinstance(frames, list) and isinstance(links, list), 'rosters must be explicit lists')
    require(len(frames) == 138 and len(links) == 137, '138 frames and 137 links required')
    for index, row in zip(range(FIRST, LAST + 1), frames):
        require(isinstance(row, dict) and set(row) == {'ordinal', 'status', 'reason'}, 'invalid frame fields')
        require(type(row['ordinal']) is int and row['ordinal'] == index, 'frame duplicate/gap/order')
        require(row['status'] in ('V', 'A', 'O', 'X') and isinstance(row['reason'], str)
                and row['reason'].strip(), 'explicit frame status/reason required')
    runs, start = [], None
    for offset, row in enumerate(links):
        left = FIRST + offset
        require(isinstance(row, dict) and set(row) == {'from', 'to', 'status', 'reason'}, 'invalid link fields')
        require(type(row['from']) is int and type(row['to']) is int
                and (row['from'], row['to']) == (left, left + 1), 'link duplicate/gap/order')
        require(row['status'] in ('supported', 'uncertain', 'broken')
                and isinstance(row['reason'], str) and row['reason'].strip(), 'explicit link judgment required')
        if row['status'] == 'supported':
            require(frames[offset]['status'] == frames[offset + 1]['status'] == 'V',
                    'supported link touches non-V frame')
            if start is None:
                start = left
        elif start is not None:
            runs.append([start, left])
            start = None
    if start is not None:
        runs.append([start, LAST])
    return {'frames': 138, 'links': 137, 'supported_runs_inclusive': runs,
            'uninterrupted_observational_candidate':
                all(row['status'] == 'V' for row in frames)
                and all(row['status'] == 'supported' for row in links),
            'semantic_or_human_acceptance_implied': False}


def run(out_name):
    from PIL import Image, __version__ as pillow_version
    output = safe_output(out_name)
    before = input_snapshot()
    output.mkdir()
    write_json(output / 'inputs-before.json', before)
    try:
        helper = load_helpers()
        selection = json.loads((PARENT / 'probe02/selection.json').read_text())
        prior = json.loads((PARENT / 'views01/frames.json').read_text())
        source_receipt = json.loads((PARENT / 'views01/receipt.json').read_text())
        probe = json.loads((PARENT / 'probe02/probe.json').read_text())
        stream, rows = helper.parse_map(probe)
        validate_metadata(selection, prior, rows, (stream['width'], stream['height']))
        argv = decoder_command()
        require(argv == source_receipt['execution']['argv'], 'decoder command changed')
        require(source_receipt['binary'] == before[str(DECODER)], 'decoder receipt mismatch')
        raw, execution = bounded_capture(argv, output / 'diagnostics', RAW_BYTES)
        checked = verify_decoded(raw, prior)
        require(sha(raw) == source_receipt['execution']['raw_sha256'], 'aggregate raw hash mismatch')
        require(input_snapshot() == before, 'input changed before image derivation')
        write_json(output / 'decoded-checks.json', {'frames_checked': COUNT, 'all_hashes_match': True,
                   'raw_bytes': len(raw), 'raw_sha256': sha(raw), 'frames': checked})
        for name in ('native', 'crops', 'pages'):
            (output / name).mkdir()
        crops, frame_records = {}, []
        view = memoryview(raw)
        for index in range(FIRST, LAST + 1):
            pixels = bytes(view[index * FRAME_BYTES:index * FRAME_BYTES + WIDTH * HEIGHT])
            crop = crop_pixels(pixels)
            crops[index] = crop
            native = save_png(output / 'native' / f'frame-{index:04d}.png',
                              Image.frombytes('L', (WIDTH, HEIGHT), pixels), pixels)
            cropped = save_png(output / 'crops' / f'crop-{index:04d}.png',
                               Image.frombytes('L', CROP_SIZE, crop), crop)
            native['path'] = 'native/' + native['path']
            cropped['path'] = 'crops/' + cropped['path']
            frame_records.append({**rows[index], 'decoded_sha256': prior[index]['decoded_sha256'],
                                  'luma_sha256': prior[index]['luma_sha256'], 'source_box': list(BOX),
                                  'native': native, 'crop': cropped})
        del view, raw
        page_records = []
        for layout in page_layout():
            page = make_page(layout, crops)
            saved = save_png(output / 'pages' / f'page-{layout["page"]:02d}.png', page, page.tobytes())
            saved['path'] = 'pages/' + saved['path']
            for cell in layout['cells']:
                cell['crop_pixel_sha256'] = None if cell['blank'] else sha(crops[cell['index']])
                cell['crop_path'] = None if cell['blank'] else f'crops/crop-{cell["index"]:04d}.png'
                cell['mapping'] = None if cell['blank'] else {
                    'source_to_crop_translation': [-BOX[0], -BOX[1]],
                    'crop_to_page_translation': cell['page_box'][:2], 'scale': [1, 1]}
            page_records.append({**layout, 'png': saved})
        write_json(output / 'frames.json', frame_records)
        write_json(output / 'pages.json', page_records)
        after = input_snapshot()
        write_json(output / 'inputs-after.json', after)
        require(after == before, 'input changed during derivation')
        write_json(output / 'receipt.json', {
            'status': 'derived_only_not_visually_reviewed', 'producer': pin(__file__),
            'python': platform.python_version(), 'python_executable': sys.executable,
            'pillow': pillow_version, 'inputs_unchanged': True, 'decoded_frames_checked': COUNT,
            'selected_interval_inclusive': [FIRST, LAST], 'native_frames': 138, 'crops': 138,
            'pages': 12, 'blank_cells': 6, 'source_box': list(BOX), 'page_size': list(PAGE_SIZE),
            'context_ordinals': [274, 342, 411], 'timestamps': 'nullable fields copied exactly; ordinal only',
            'pixel_mapping': 'source (x,y) -> crop (x-350,y-90) -> page plus recorded cell origin',
            'execution': pin(output / 'diagnostics/execution.json'),
            'decoded_checks': pin(output / 'decoded-checks.json'),
            'frames': pin(output / 'frames.json'), 'page_mapping': pin(output / 'pages.json'),
            'no_classifications_generated': True, 'no_source_acceptance_implied': True,
            'image_byte_repeatability': 'PNG file hashes recorded; decoded pixel hashes are the source checks',
        })
    except Exception as exc:
        # Leave all failed/partial products in their exclusive directory.
        failure = {'status': 'failed_incomplete_not_admitted', 'type': type(exc).__name__, 'message': str(exc)}
        try:
            after = input_snapshot()
            failure['inputs_unchanged'] = after == before
            if not (output / 'inputs-after.json').exists():
                write_json(output / 'inputs-after.json', after)
        except Exception as after_exc:
            failure['input_after_check_error'] = str(after_exc)
        write_json(output / 'failure.json', failure)
        raise
    return output


class Controls(unittest.TestCase):
    def roster(self):
        frames = expand_ranges([{'first': FIRST, 'last': LAST, 'status': 'V', 'reason': 'synthetic fixture'}], 'frames')
        links = expand_ranges([{'first': FIRST, 'last': LAST - 1, 'status': 'supported', 'reason': 'synthetic fixture'}], 'links')
        return frames, links

    def test_crop_boundaries_and_pixels(self):
        pixels = bytes((x + 3 * y) % 256 for y in range(HEIGHT) for x in range(WIDTH))
        crop = crop_pixels(pixels)
        self.assertEqual(len(crop), 280 * 290)
        for cy in range(290):
            self.assertEqual(crop[cy * 280:(cy + 1) * 280],
                             pixels[(90 + cy) * WIDTH + 350:(90 + cy) * WIDTH + 630])
        for box in ((-1, 0, 1, 1), (0, 0, 705, 2), (0, 0, 1, 481), (3, 2, 2, 4)):
            with self.assertRaises(ValueError): crop_pixels(pixels, box=box)

    def test_page_order_pixels_and_six_blank_cells(self):
        crops = {index: bytes([index % 255]) * (280 * 290) for index in range(FIRST, LAST + 1)}
        seen, blanks = [], 0
        for layout in page_layout():
            page = make_page(layout, crops)
            self.assertEqual(page.size, PAGE_SIZE)
            for cell in layout['cells']:
                actual = page.crop(tuple(cell['page_box'])).tobytes()
                if cell['blank']:
                    blanks += 1
                    self.assertIsNone(cell['source_box'])
                    self.assertEqual(actual, b'\xff' * (280 * 290))
                else:
                    seen.append(cell['index'])
                    self.assertEqual(actual, crops[cell['index']])
        self.assertEqual(seen, list(range(FIRST, LAST + 1)))
        self.assertEqual(blanks, 6)
        self.assertTrue(all(cell['blank'] for cell in page_layout()[-1]['cells'][6:]))

    def test_png_roundtrip_exclusive(self):
        from PIL import Image
        with tempfile.TemporaryDirectory(prefix='continuity-synthetic-') as temp:
            path = Path(temp) / 'fixture.png'
            pixels = bytes(range(64))
            receipt = save_png(path, Image.frombytes('L', (8, 8), pixels), pixels)
            self.assertEqual(receipt['pixel_sha256'], sha(pixels))
            with self.assertRaises(FileExistsError):
                save_png(path, Image.frombytes('L', (8, 8), pixels), pixels)

    def test_decoded_and_luma_hash_rejection(self):
        raw = bytes(range(12))
        expected = [{'index': 0, 'decoded_sha256': sha(raw), 'luma_sha256': sha(raw[:8])}]
        self.assertEqual(verify_decoded(raw, expected, 4, 2), expected)
        for field in ('decoded_sha256', 'luma_sha256'):
            bad = copy.deepcopy(expected); bad[0][field] = '0' * 64
            with self.assertRaises(ValueError): verify_decoded(raw, bad, 4, 2)
        with self.assertRaises(ValueError): verify_decoded(raw[:-1], expected, 4, 2)

    def test_full_roster(self):
        result = validate_roster(*self.roster())
        self.assertEqual(result['supported_runs_inclusive'], [[FIRST, LAST]])
        self.assertTrue(result['uninterrupted_observational_candidate'])
        self.assertFalse(result['semantic_or_human_acceptance_implied'])

    def test_no_link_inference_or_bridging(self):
        frames, links = self.roster()
        links[5]['status'] = 'uncertain'
        result = validate_roster(frames, links)
        self.assertFalse(result['uninterrupted_observational_candidate'])
        self.assertEqual(result['supported_runs_inclusive'], [[274, 279], [280, 411]])

    def test_supported_link_touching_non_v_rejected(self):
        for status in ('A', 'O', 'X'):
            frames, links = self.roster(); frames[10]['status'] = status
            with self.assertRaises(ValueError): validate_roster(frames, links)
            links[9]['status'], links[10]['status'] = 'uncertain', 'broken'
            self.assertFalse(validate_roster(frames, links)['uninterrupted_observational_candidate'])

    def test_missing_duplicate_unknown_and_fill_rejected(self):
        frames, links = self.roster()
        for frame_rows, link_rows in ((frames[:-1], links), (frames, links[:-1]),
                                      (frames + frames[-1:], links), (frames, links + links[-1:])):
            with self.assertRaises(ValueError): validate_roster(frame_rows, link_rows)
        for field, bad in (('status', ''), ('status', 'V/A'), ('reason', ''), ('ordinal', True)):
            changed = copy.deepcopy(frames); changed[3][field] = bad
            with self.assertRaises(ValueError): validate_roster(changed, links)
        changed = copy.deepcopy(frames); changed[3] = copy.deepcopy(changed[2])
        with self.assertRaises(ValueError): validate_roster(changed, links)
        changed = copy.deepcopy(links); changed[3]['to'] += 1
        with self.assertRaises(ValueError): validate_roster(frames, changed)
        changed = copy.deepcopy(frames); changed[3]['fill'] = 'V'
        with self.assertRaises(ValueError): validate_roster(changed, links)

    def test_range_gap_duplicate_and_defaults_rejected(self):
        item = {'first': FIRST, 'last': LAST, 'status': 'V', 'reason': 'synthetic'}
        with self.assertRaises(ValueError): expand_ranges([item, item], 'frames')
        bad = dict(item, last=LAST - 1)
        with self.assertRaises(ValueError): expand_ranges([bad], 'frames')
        for key in ('status', 'reason'):
            bad = dict(item); del bad[key]
            with self.assertRaises(ValueError): expand_ranges([bad], 'frames')

    def test_nullable_timestamp_parser(self):
        helper = load_helpers()
        fixture = {'streams': [{'width': 4, 'height': 2, 'pix_fmt': 'yuv420p', 'time_base': '1/30'}],
                   'frames': [{'width': 4, 'height': 2, 'pix_fmt': 'yuv420p',
                               'pts': index, 'best_effort_timestamp': index} for index in range(8)]}
        del fixture['frames'][0]['pts']
        del fixture['frames'][-1]['pts']; del fixture['frames'][-1]['best_effort_timestamp']
        rows = helper.parse_map(fixture)[1]
        self.assertIsNone(rows[0]['stored_pts'])
        self.assertEqual(rows[0]['best_effort_timestamp'], 0)
        self.assertIsNone(rows[-1]['best_effort_seconds_exact'])
        self.assertEqual(rows[1]['stored_pts_seconds_exact'], '1/30')

    def capture_fixture(self, code, limit=64, timeout=2, diag=64):
        with tempfile.TemporaryDirectory(prefix='continuity-synthetic-') as temp:
            directory = Path(temp) / 'capture'
            error = None
            try:
                bounded_capture([sys.executable, '-B', '-c', code], directory, limit, timeout, diag)
            except ValueError as exc:
                error = exc
            receipt = json.loads((directory / 'execution.json').read_text())
            return error, receipt, (directory / 'stdout-prefix.bin').read_bytes(), (directory / 'stderr-prefix.bin').read_bytes()

    def test_capture_success(self):
        error, receipt, out, err = self.capture_fixture('import os; os.write(1,b"abc")')
        self.assertIsNone(error)
        self.assertEqual((out, err), (b'abc', b''))
        self.assertTrue(receipt['capture_complete'])

    def test_capture_nonzero_and_warning_retained(self):
        for exit_code in (0, 3):
            error, receipt, out, err = self.capture_fixture(
                f'import os; os.write(1,b"partial"); os.write(2,b"warning"); raise SystemExit({exit_code})')
            self.assertIsNotNone(error)
            self.assertEqual((out, err), (b'partial', b'warning'))
            self.assertEqual(receipt['returncode'], exit_code)

    def test_capture_timeout_partial_outputs(self):
        error, receipt, out, err = self.capture_fixture(
            'import os,time; os.write(1,b"partial"); os.write(2,b"late"); time.sleep(2)', timeout=0.2)
        self.assertIsNotNone(error)
        self.assertEqual(receipt['status'], 'timeout')
        self.assertFalse(receipt['capture_complete'])
        self.assertEqual((out, err), (b'partial', b'late'))

    def test_capture_oversize_preserved_before_reject(self):
        error, receipt, out, _ = self.capture_fixture('import os; os.write(1,b"abcdefghij")', limit=4, diag=3)
        self.assertIsNotNone(error)
        self.assertEqual(receipt['status'], 'stdout_oversize')
        self.assertEqual(out, b'abc')
        self.assertEqual(receipt['stdout']['captured_bytes'], 5)
        self.assertTrue(receipt['stdout']['saved_prefix_truncated'])

    def test_capture_launch_error_and_exclusive(self):
        with tempfile.TemporaryDirectory(prefix='continuity-synthetic-') as temp:
            directory = Path(temp) / 'capture'
            with self.assertRaises(ValueError): bounded_capture(['/nonexistent-continuity-fixture'], directory, 64)
            receipt = json.loads((directory / 'execution.json').read_text())
            self.assertEqual(receipt['status'], 'launch_or_pipe_error')
            with self.assertRaises(FileExistsError): bounded_capture(['unused'], directory, 64)

    def test_safe_output(self):
        for name in ('../bad', '/tmp/bad', 'a/b', '', 'run 01', None):
            with self.assertRaises(ValueError): safe_output(name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('action', nargs='?', choices=['run'])
    parser.add_argument('--out')
    args = parser.parse_args()
    if args.self_test:
        require(args.action is None and args.out is None, 'self-test cannot request historical run')
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        raise SystemExit(not result.wasSuccessful())
    require(args.action == 'run' and args.out is not None, 'explicit run --out required')
    output = run(args.out)
    print(json.dumps({'status': 'derived_only_not_reviewed', 'output': str(output)}))


if __name__ == '__main__':
    main()
