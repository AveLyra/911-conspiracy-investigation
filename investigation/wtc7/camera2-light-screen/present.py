#!/usr/bin/env python3
"""Fixed native contact-page presentation; no video decode or light detection."""
import argparse
import csv
from fractions import Fraction
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import re
import sys
import warnings

import PIL
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin, _imaging, _imagingft

UNIT = Path(__file__).resolve().parent
MAIN = Path('/Users/admin/docs/911')
SOURCE = UNIT.parent / 'camera2-penthouse-event/run01/camera2'
DECLARATION_SHA = '8f715d88286e404fd2e20209e216a98e559860086f55161d722fe56916c6ef25'
TIMING = 'research/sherlock-wtc7-investigation/timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/'
VIDEO = 'research/wtc7-video-comparison/media/analysis-source/NIST Camera 2_CBS-Net Dub6 48 (Converted).mov'
UPSTREAM = {
    TIMING + 'frame-map.csv': {'bytes': 867161, 'sha256': 'ccc78c7ff933710f8e8e767dce5e05855fefb05bb75241d2bec01b4739c3b812'},
    TIMING + 'frames.json': {'bytes': 3389769, 'sha256': '424a2c27064548797ca9f4f0855781af490e4c912c7ccd5bc5340ee9a20524f0'},
    TIMING + 'source-identity.json': {'bytes': 449, 'sha256': '632c27b1ad4d04bddd991568a7c30206841ae3af5606fac801e61ffff561ca38'},
    VIDEO: {'bytes': 208810910, 'sha256': '84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730'},
}
SELECTION_PIN = {'bytes': 330219, 'sha256': 'e297292a04a093d757b7693b9914abe4b88db4e6b836461f49c8dee411e78b2d'}
RECEIPT_PIN = {'bytes': 68222, 'sha256': 'a5c72edd8f7714c0916c7b66f39f745c2cd7d73c99510f6c8a4be87ed751a114'}
CHARTER_SHA = '54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd'
INDICES = tuple(range(6593, 7014))
SIZE = (640, 480)
PAGE_SIZE = (1280, 1512)
SOURCE_DIAGNOSTICS = {'audio_layout_guess_stereo_lines': 1,
                      'raw_local_log': 'decoder.local-only.log', 'unclassified_lines': 0}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def fingerprint(path):
    path = Path(path)
    require(not path.is_symlink(), 'input-symlink: ' + path.name)
    with path.open('rb') as stream:
        before = os.fstat(stream.fileno())
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        after = os.fstat(stream.fileno())
    require((before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns), 'changed-during-hash')
    return {'bytes': after.st_size, 'sha256': digest}


def integer(value):
    require(type(value) is str and re.fullmatch(r'0|[1-9][0-9]*', value), 'canonical-integer')
    return int(value)


def rational(value):
    require(type(value) is str, 'fraction-type')
    result = Fraction(value)
    require(str(result) == value, 'canonical-fraction')
    return result


def pages():
    return [list(range(6593 + 5*p, 6599 + 5*p)) for p in range(84)]


def select_rows(document, timing_rows, receipt):
    require(document['geometry'] == [640, 480] and document['source_id'] == 'VID-WTC7-001', 'selection-source')
    require(document['checked_frames'] == 8042 and document['exit_code'] == 0, 'selection-extraction')
    require(document['diagnostics'] == SOURCE_DIAGNOSTICS, 'source-warning-state')
    for key in ('input_pins', 'input_pins_before', 'input_pins_after'):
        require(document[key] == UPSTREAM, 'upstream-pin-declaration')
    require(receipt['status'] == 'complete' and receipt['cameras']['camera2'] ==
            {'checked_frames': 8042, 'selected': 421}, 'source-receipt-state')
    require(len(timing_rows) == 8042, 'timing-count')
    require([integer(row['frame_index_zero_based']) for row in timing_rows] == list(range(8042)), 'timing-index-order')
    rows = document['images']
    require([integer(row['frame_index_zero_based']) for row in rows] == list(INDICES), 'selection-order-membership')
    previous_time = None
    for row, index in zip(rows, INDICES):
        pts = integer(row['source_pts'])
        require(integer(row['best_effort_timestamp']) == pts, 'best-effort-pts')
        tb = rational(row['source_time_base'])
        time = rational(row['source_time_seconds_exact'])
        require(tb == Fraction(1, 2997) and time == pts*tb, 'exact-clock-join')
        require(previous_time is None or time > previous_time, 'clock-order')
        previous_time = time
        ticks = row['source_duration_ticks']
        require(type(ticks) is int and ticks > 0 and
                rational(row['source_duration_seconds_exact']) == ticks*tb, 'duration-join')
        require(row['png'] == f'f{index:06d}.png', 'source-basename')
        pin = row['png_identity']
        require(type(pin['bytes']) is int and pin['bytes'] > 0, 'source-byte-count')
        for digest in (pin['sha256'], row['luma_sha256'], row['decoded_sha256']):
            require(type(digest) is str and re.fullmatch('[0-9a-f]{64}', digest), 'digest-format')
        require(receipt['products']['camera2/' + row['png']] == pin, 'source-receipt-product')
        for key, value in timing_rows[index].items():
            require(row[key] == value, 'timing-map-row-mismatch')
    return rows


def read_source(row):
    path = SOURCE / row['png']
    require(not SOURCE.is_symlink() and not path.is_symlink() and
            path.resolve().parent == SOURCE.resolve(), 'source-path-confinement')
    data = path.read_bytes()
    require(identity(data) == row['png_identity'], 'source-png-pin')
    with Image.open(io.BytesIO(data)) as image:
        require(image.format == 'PNG' and image.mode == 'L' and image.size == SIZE, 'source-image-contract')
        require(getattr(image, 'n_frames', 1) == 1, 'source-not-single-frame')
        require(not set(image.info) & {'transparency', 'gamma', 'srgb', 'icc_profile'}, 'source-photometric-metadata')
        require(hashlib.sha256(image.tobytes()).hexdigest() == row['luma_sha256'], 'source-luma-pin')
        return image.copy()


def compose_page(rows, load=read_source):
    require(len(rows) == 6, 'six-rows-required')
    indices = [integer(row['frame_index_zero_based']) for row in rows]
    require(indices == list(range(indices[0], indices[0]+6)), 'page-order')
    result = Image.new('L', PAGE_SIZE, 24)
    font = ImageFont.load_default(size=14)
    cells = []
    for slot, row in enumerate(rows):
        x, y = (slot % 2)*640, (slot // 2)*504
        image = load(row)
        require(image.mode == 'L' and image.size == SIZE, 'native-cell-contract')
        label = f"source {indices[slot]} | PTS {row['source_pts']} | t={row['source_time_seconds_exact']} s"
        strip = Image.new('L', (640, 24), 24)
        draw = ImageDraw.Draw(strip)
        box = draw.textbbox((6, 3), label, font=font)
        require(box[0] >= 0 and box[1] >= 0 and box[2] <= 640 and box[3] <= 24, 'label-fit')
        draw.text((6, 3), label, font=font, fill=240)
        result.paste(strip, (x, y))
        result.paste(image, (x, y+24))
        cells.append({'slot_zero_based': slot, 'source_index': indices[slot],
            'source_png': row['png'], 'source_png_identity': row['png_identity'],
            'source_luma_sha256': row['luma_sha256'],
            'source_pts': row['source_pts'], 'source_time_base': row['source_time_base'],
            'source_time_seconds_exact': row['source_time_seconds_exact'],
            'label': label, 'label_rectangle_half_open': [x, y, x+640, y+24],
            'source_rectangle_half_open': [x, y+24, x+640, y+504]})
    return result, cells


def fresh_output(name):
    require(type(name) is str and name in ('run01', 'run02'), 'output-scope')
    out = UNIT / name
    require(not out.is_symlink() and not out.exists(), 'output-already-exists')
    require(out.resolve().parent == UNIT.resolve(), 'output-confinement')
    return out


def write_json(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')


def runtime_pins():
    require(platform.python_version() == '3.12.14' and PIL.__version__ == '12.3.0', 'reviewed-runtime-version')
    paths = [Path(__file__), UNIT/'test_present.py', Path(sys.executable).resolve(),
             *[Path(module.__file__) for module in (PIL, Image, ImageDraw, ImageFont, PngImagePlugin, _imaging, _imagingft)]]
    return {str(path): fingerprint(path) for path in paths}


def input_pins():
    expected = {MAIN/key: value for key, value in UPSTREAM.items()}
    expected[SOURCE/'selection.json'] = SELECTION_PIN
    expected[SOURCE.parent/'receipt.json'] = RECEIPT_PIN
    actual = {str(path): fingerprint(path) for path in expected}
    for path, pin in expected.items():
        require(actual[str(path)] == pin, 'input-pin: ' + path.name)
    charter = MAIN/'research/sherlock-wtc7-investigation/CHARTER.md'
    actual[str(charter)] = fingerprint(charter)
    require(actual[str(charter)]['sha256'] == CHARTER_SHA, 'charter-pin')
    return actual


def products(out):
    return {path.name: fingerprint(path) for path in sorted(out.iterdir()) if path.is_file()}


def run(name, expected_code, expected_protocol):
    out = fresh_output(name)
    require(fingerprint(Path(__file__))['sha256'] == expected_code, 'reviewed-code-pin')
    require(expected_protocol == DECLARATION_SHA and
            fingerprint(UNIT/'PROTOCOL.md')['sha256'] == expected_protocol, 'reviewed-protocol-pin')
    out.mkdir(exist_ok=False)
    phase, before, after, runtime_before, runtime_after = 'inputs', {}, {}, {}, {}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        try:
            before = input_pins()
            before[str(UNIT/'PROTOCOL.md')] = fingerprint(UNIT/'PROTOCOL.md')
            runtime_before = runtime_pins()
            selection_data = (SOURCE/'selection.json').read_bytes()
            receipt_data = (SOURCE.parent/'receipt.json').read_bytes()
            require(identity(selection_data) == SELECTION_PIN and identity(receipt_data) == RECEIPT_PIN, 'metadata-changed')
            selection, receipt = json.loads(selection_data), json.loads(receipt_data)
            timing_data = (MAIN/(TIMING+'frame-map.csv')).read_bytes()
            require(identity(timing_data) == UPSTREAM[TIMING+'frame-map.csv'], 'timing-changed')
            timing_rows = list(csv.DictReader(io.StringIO(timing_data.decode('utf-8'))))
            rows = select_rows(selection, timing_rows, receipt)
            source_identity = json.loads((MAIN/(TIMING+'source-identity.json')).read_bytes())
            require(source_identity['record_id'] == 'VID-WTC7-001' and
                    source_identity['source_integrity'] == UPSTREAM[VIDEO], 'video-identity-join')
            require(receipt['products']['camera2/selection.json'] == SELECTION_PIN, 'selection-receipt-pin')
            log = SOURCE/'decoder.local-only.log'
            before[str(log)] = fingerprint(log)
            require(before[str(log)] == receipt['products']['camera2/decoder.local-only.log'], 'source-diagnostic-log-pin')
            phase = 'all-native-inputs'
            for row in rows:
                before[str(SOURCE/row['png'])] = fingerprint(SOURCE/row['png'])
                require(before[str(SOURCE/row['png'])] == row['png_identity'], 'native-pin')
                read_source(row).close()
            write_json(out/'input-pins-before.json', before)
            write_json(out/'runtime-pins-before.json', runtime_before)
            for source, name in [(Path(__file__), 'producer-snapshot.py'),
                    (UNIT/'test_present.py', 'test-snapshot.py'), (UNIT/'PROTOCOL.md', 'protocol-snapshot.md'),
                    (SOURCE/'selection.json', 'selection-snapshot.json')]:
                data = source.read_bytes()
                require(identity(data) == before.get(str(source), runtime_before.get(str(source))), 'snapshot-changed')
                with (out/name).open('xb') as stream:
                    stream.write(data)
            phase = 'presentation'
            rendered = []
            for page_number, indices in enumerate(pages()):
                chosen = [rows[index-INDICES[0]] for index in indices]
                panel, cells = compose_page(chosen)
                name = f'page-{page_number:02d}.png'
                with (out/name).open('xb') as stream:
                    panel.save(stream, format='PNG')
                with Image.open(out/name) as saved:
                    require(saved.mode == 'L' and saved.size == PAGE_SIZE and saved.n_frames == 1 and not saved.info, 'saved-page-contract')
                    require(saved.tobytes() == panel.tobytes(), 'saved-page-pixels')
                rendered.append({'page_zero_based': page_number, 'png': name,
                    'png_identity': fingerprint(out/name), 'luma_sha256': hashlib.sha256(panel.tobytes()).hexdigest(),
                    'size': list(PAGE_SIZE), 'mode': 'L', 'cells': cells})
            write_json(out/'manifest.json', {'status': 'presentation-only', 'pages': rendered,
                'source_indices': list(INDICES), 'source_geometry': list(SIZE), 'source_mode': 'L',
                'page_geometry': list(PAGE_SIZE), 'external_label_height': 24,
                'source_generation_diagnostics': selection['diagnostics'],
                'limitations': 'Unchanged native luma presentation; no color, photometric calibration, detector, human acceptance or event finding.'})
            phase = 'post-pins'
            after = {path: fingerprint(path) for path in before}
            runtime_after = runtime_pins()
            write_json(out/'input-pins-after.json', after)
            write_json(out/'runtime-pins-after.json', runtime_after)
            require(after == before and runtime_after == runtime_before, 'input-or-runtime-changed')
            require(not caught, 'unexpected-presentation-warning')
            require({path.name for path in out.glob('*.png')} == {f'page-{p:02d}.png' for p in range(84)}, 'page-membership')
            result = {'status': 'complete-presentation-only', 'pages': 84, 'unique_source_frames': 421,
                'display_slots': 504, 'python': platform.python_version(), 'pillow': PIL.__version__,
                'command': sys.argv, 'warnings': [], 'source_generation_diagnostics': selection['diagnostics'],
                'input_pins_before': before, 'input_pins_after': after,
                'runtime_pins_before': runtime_before, 'runtime_pins_after': runtime_after,
                'products': products(out)}
            write_json(out/'receipt.json', result)
            return result
        except Exception as error:
            write_json(out/'failure.json', {'status': 'failed', 'phase': phase,
                'error_type': type(error).__name__, 'error': str(error),
                'warnings': [{'category': w.category.__name__, 'message': str(w.message)} for w in caught],
                'input_pins_before': before, 'input_pins_after': after,
                'runtime_pins_before': runtime_before, 'runtime_pins_after': runtime_after,
                'partial_products': products(out)})
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, choices=('run01', 'run02'))
    parser.add_argument('--expect-code-sha256', required=True)
    parser.add_argument('--expect-protocol-sha256', required=True)
    args = parser.parse_args()
    result = run(args.out, args.expect_code_sha256, args.expect_protocol_sha256)
    print(json.dumps({key: result[key] for key in ('status', 'pages', 'unique_source_frames', 'display_slots')}))


if __name__ == '__main__':
    main()
