"""Read-only saved-product verification; never decodes or displays historical media.

The only CLI write is a fresh JSON result inside this unit. No producer module
is imported. A pass verifies recorded products and their consistency, not a
fresh source-YUV-to-PNG linkage, historical clock, endpoint, or mechanism.
"""
import argparse
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

import PIL
from PIL import Image, ImageDraw

UNIT = Path(__file__).resolve().parent
MAIN = Path('/Users/admin/docs/911')
BASE = MAIN / 'research/sherlock-wtc7-investigation'
OLD = BASE / 'multiview-onset-review'
TIMING = BASE / 'timing-audit/run-2026-09-08-v1.1/VID-WTC7-001'
SOURCE = MAIN / 'research/wtc7-video-comparison/media/analysis-source/NIST Camera 2_CBS-Net Dub6 48 (Converted).mov'
SOURCE_ID = 'VID-WTC7-001'
SOURCE_BYTES = 208810910
RAW_SHA = '1490b125faceae77a19edbda835682da3876f503c766af04be6cf6e93751b4dc'
INPUT_SHA = {
    SOURCE: '84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730',
    TIMING / 'frame-map.csv': 'ccc78c7ff933710f8e8e767dce5e05855fefb05bb75241d2bec01b4739c3b812',
    TIMING / 'frames.json': '424a2c27064548797ca9f4f0855781af490e4c912c7ccd5bc5340ee9a20524f0',
    TIMING / 'source-identity.json': '632c27b1ad4d04bddd991568a7c30206841ae3af5606fac801e61ffff561ca38',
}
DEPENDENCY_SHA = {
    OLD / 'extract.py': 'df245c5fcf2790a45643c1fddf481bd38c63aed3592a4b0c9ad32819c23dc64c',
    OLD / 'PROTOCOL.md': '1dfdabe397ff64fba08b712f2999242380aa1cd5733f74152392064aec8794a5',
    UNIT / 'STAGE-B.md': '24738fd6c695f450972b663cb55836b3d935b8c91487630c1aeca763d21d3da3',
    Path('/opt/homebrew/bin/ffmpeg'): '7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569',
    Path('/opt/homebrew/bin/ffprobe'): 'fd670257233c93c88608a62ed8b5ddeeb812bd341dfb39bbe0e1c654b91672ad',
    Path('/Users/admin/.pyenv/versions/3.13.7/bin/python3.13'): '7d29600aa971dfd764a15b113d5964b1e74a18176a6b70cb31646d45e9e5018e',
}
CSV_KEYS = {'frame_index_zero_based', 'source_pts', 'source_time_base',
            'source_time_seconds_exact', 'best_effort_timestamp', 'decoded_sha256',
            'identical_to_previous_decoded_frame'}
DIAGNOSTIC = rb'\[aist#0:[0-9]+/pcm_s16le @ 0x[0-9a-f]+\] Guessed Channel Layout: stereo'
KIND = 'historical-extraction'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fingerprint(path):
    with Path(path).open('rb') as stream:
        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': Path(path).stat().st_size, 'sha256': sha}


def strict_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate-json-key')
        result[key] = value
    return result


def read_json(path):
    def noninteger(value):
        raise ValueError('noninteger-json-number: ' + value)
    return json.loads(Path(path).read_text(), object_pairs_hook=strict_pairs,
                      parse_float=noninteger, parse_constant=noninteger)


def integer(value):
    require(type(value) is str and re.fullmatch(r'0|-?[1-9][0-9]*', value), 'integer-text')
    return int(value)


def rational(value):
    require(type(value) is str, 'rational-text')
    result = Fraction(value)
    require(str(result) == value, 'rational-not-canonical')
    return result


def validate_rows(rows, metadata):
    require(bool(rows) and len(rows) == len(metadata), 'map-metadata-count')
    times = []
    last_hash = None
    tb = None
    for i, (row, frame) in enumerate(zip(rows, metadata)):
        require(set(row) == CSV_KEYS, 'map-columns')
        require(integer(row['frame_index_zero_based']) == i, 'map-index-order')
        pts = integer(row['source_pts'])
        require(integer(row['best_effort_timestamp']) == pts, 'map-best-effort')
        current_tb = rational(row['source_time_base'])
        require(current_tb > 0 and (tb is None or current_tb == tb), 'map-timebase')
        tb = current_tb
        time = rational(row['source_time_seconds_exact'])
        require(time == pts * tb and (not times or time > times[-1]), 'map-time-order')
        times.append(time)
        digest = row['decoded_sha256']
        require(type(digest) is str and re.fullmatch(r'[0-9a-f]{64}', digest), 'map-hash')
        require(row['identical_to_previous_decoded_frame'] == str(digest == last_hash), 'duplicate-flag')
        last_hash = digest
        for key in ('pts', 'pkt_dts', 'best_effort_timestamp'):
            require(type(frame[key]) is int and frame[key] == pts, 'metadata-' + key)
        require(type(frame['duration']) is int and frame['duration'] > 0, 'metadata-duration')
        require(type(frame['width']) is int and type(frame['height']) is int, 'metadata-dimension-type')
        require((frame['width'], frame['height'], frame['pix_fmt']) == (640, 480, 'yuv420p'), 'metadata-format')
        for key in ('interlaced_frame', 'top_field_first', 'repeat_pict'):
            require(type(frame[key]) is int and frame[key] == 0, 'metadata-' + key)
    return times


def derive_selection(times, low=Fraction(220), high=Fraction(234)):
    """Linear threshold walk, independent of the producer's membership selector."""
    require(type(low) is Fraction and type(high) is Fraction and low <= high, 'selection-range')
    require(all(type(t) is Fraction for t in times), 'selection-time-type')
    require(all(b > a for a, b in zip(times, times[1:])), 'selection-order')
    left = 0
    while left < len(times) and times[left] < low:
        left += 1
    right = left
    while right < len(times) and times[right] <= high:
        right += 1
    require(left < right, 'selection-empty')
    require(left > 0 and right < len(times), 'selection-missing-bound')
    indices = list(range(left - 1, right + 1))
    reasons = {i: ['closed-interval-interior'] for i in indices}
    reasons[left - 1] = ['immediately-preceding-bound']
    reasons[right] = ['immediately-following-bound']
    return indices, reasons


def pinned_inputs():
    pins = {}
    for path, expected in INPUT_SHA.items():
        fp = fingerprint(path)
        require(fp['sha256'] == expected, 'input-sha: ' + path.name)
        pins[str(path.relative_to(MAIN))] = fp
    require(pins[str(SOURCE.relative_to(MAIN))]['bytes'] == SOURCE_BYTES, 'source-bytes')
    with (TIMING / 'frame-map.csv').open(newline='') as stream:
        reader = csv.DictReader(stream)
        require(len(reader.fieldnames) == len(CSV_KEYS) and set(reader.fieldnames) == CSV_KEYS, 'csv-header')
        rows = list(reader)
    metadata = read_json(TIMING / 'frames.json')['frames']
    require(len(rows) == len(metadata) == 8042, 'input-count')
    times = validate_rows(rows, metadata)
    require(rows[0]['source_time_base'] == '1/2997', 'source-timebase')
    identity = read_json(TIMING / 'source-identity.json')
    require(identity['record_id'] == SOURCE_ID and identity['source_integrity'] ==
            pins[str(SOURCE.relative_to(MAIN))], 'source-identity')
    require(identity['media_relative_path'] == 'analysis-source/' + SOURCE.name, 'source-relative-name')
    indices, reasons = derive_selection(times)
    require(indices == list(range(6593, 7014)), 'fixed-selection')
    require([times[i] for i in (6593, 6594, 7012, 7013)] ==
            [Fraction(219767, 999), Fraction(219800, 999), Fraction(701204, 2997), Fraction(701303, 2997)], 'fixed-bound-times')
    return rows, metadata, pins, indices, reasons


def safe_child(root, name):
    require(type(name) is str and '\\' not in name, 'product-name')
    relative = PurePosixPath(name)
    require(not relative.is_absolute() and relative.parts and
            all(part not in ('.', '..') for part in relative.parts) and str(relative) == name, 'product-path')
    path = root / relative
    require(path.resolve().is_relative_to(root.resolve()), 'product-escape')
    require(not any(p.is_symlink() for p in (path, *path.parents) if p != root.parent), 'product-symlink')
    return path


def check_inventory(root, receipt):
    require(receipt['status'] == 'complete' and receipt['execution_kind'] == KIND, 'receipt-state')
    products = receipt['products']
    require(type(products) is dict and bool(products), 'empty-products')
    actual = set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'inventory-symlink')
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    require(actual == set(products) | {'receipt.json'} and 'receipt.json' not in products, 'inventory-set')
    for name, identity in products.items():
        require(type(identity) is dict and set(identity) == {'bytes', 'sha256'} and
                type(identity['bytes']) is int and identity['bytes'] >= 0, 'inventory-identity')
        require(fingerprint(safe_child(root, name)) == identity, 'inventory-pin: ' + name)
    return products


def check_diagnostic(data):
    lines = data.splitlines()
    require(len(lines) == 1 and re.fullmatch(DIAGNOSTIC, lines[0]), 'diagnostic-exactly-one')
    # Normalize only the admitted process address, preserving newline and stream ID.
    return re.sub(rb' @ 0x[0-9a-f]+\]', b' @ ADDRESS]', data)


def half_pixels(data, width, height):
    """Independent integer equivalent of separable 2x BOX, not Image.resize."""
    require(width > 0 and height > 0 and width % 2 == height % 2 == 0 and
            len(data) == width * height, 'half-size-geometry')
    out = bytearray()
    for y in range(0, height, 2):
        for x in range(0, width, 2):
            p = y * width + x
            top = (data[p] + data[p + 1] + 1) // 2
            bottom = (data[p + width] + data[p + width + 1] + 1) // 2
            out.append((top + bottom + 1) // 2)
    return bytes(out)


def check_images(destination, images, rows, metadata, indices, reasons, geometry=(640, 480)):
    require(type(images) is list and len(images) == len(indices), 'image-count')
    extra = {'selection_reasons', 'png', 'png_identity', 'luma_sha256',
             'source_duration_ticks', 'source_duration_seconds_exact'}
    pixels = []
    for entry, index in zip(images, indices):
        row = rows[index]
        require(set(entry) == set(row) | extra and {key: entry[key] for key in row} == row, 'selected-row')
        require(entry['selection_reasons'] == reasons[index], 'selected-reason')
        require(entry['png'] == f'f{index:06d}.png', 'selected-png-name')
        duration = metadata[index]['duration']
        require(type(entry['source_duration_ticks']) is int and entry['source_duration_ticks'] == duration and
                entry['source_duration_seconds_exact'] == str(duration * rational(row['source_time_base'])), 'selected-duration')
        path = safe_child(destination, entry['png'])
        require(fingerprint(path) == entry['png_identity'], 'png-file-pin')
        with Image.open(path) as image:
            require(image.format == 'PNG' and image.mode == 'L' and image.size == geometry, 'png-format')
            require(getattr(image, 'n_frames', 1) == 1, 'png-animation')
            raw = image.tobytes()
        require(hashlib.sha256(raw).hexdigest() == entry['luma_sha256'], 'png-luma-pin')
        pixels.append(raw)
    return pixels


def check_sheets(destination, names, images, pixels, geometry=(640, 480)):
    expected_names = [f'overview-{i:02d}.png' for i in range((len(images) + 15) // 16)]
    require(names == expected_names, 'sheet-names')
    width, height = geometry
    tw, th = width // 2, height // 2
    for page, name in enumerate(names):
        expected = Image.new('L', (tw * 4, (th + 26) * 4), 255)
        draw = ImageDraw.Draw(expected)
        for cell, (entry, raw) in enumerate(zip(images[page * 16:(page + 1) * 16], pixels[page * 16:(page + 1) * 16])):
            x, y = (cell % 4) * tw, (cell // 4) * (th + 26)
            expected.paste(Image.frombytes('L', (tw, th), half_pixels(raw, width, height)), (x, y))
            text = f"frame {entry['frame_index_zero_based']} | {float(rational(entry['source_time_seconds_exact'])):.6f} s"
            draw.text((x + 3, y + th + 2), text, fill=0)
        with Image.open(safe_child(destination, name)) as sheet:
            require(sheet.format == 'PNG' and sheet.mode == 'L' and sheet.size == expected.size and
                    getattr(sheet, 'n_frames', 1) == 1, 'sheet-format')
            require(sheet.tobytes() == expected.tobytes(), 'sheet-pixels-labels')


def check_initial(root, driver_sha):
    require(type(driver_sha) is str and re.fullmatch(r'[0-9a-f]{64}', driver_sha), 'driver-sha-argument')
    expected = dict(DEPENDENCY_SHA)
    expected[UNIT / 'stage_b_extract.py'] = driver_sha
    initial = read_json(root / 'initial.json')
    require(initial['kind'] == KIND, 'initial-kind')
    require(set(initial['pins']) == {str(p) for p in expected}, 'initial-pin-set')
    for path, sha in expected.items():
        current = fingerprint(path)
        require(current['sha256'] == sha and initial['pins'][str(path)] == current, 'initial-pin: ' + path.name)
    require(initial['executable'] == '/Users/admin/.pyenv/versions/3.13.7/bin/python3.13' and
            initial['python'].startswith('3.13.7 ') and initial['pillow'] == '12.0.0' == PIL.__version__, 'initial-runtime')
    require(initial['ffmpeg_version'].startswith('ffmpeg version 7.1.1 ') and
            initial['ffprobe_version'].startswith('ffprobe version 7.1.1 '), 'initial-tool-version')
    snapshots = {'driver-snapshot.py': UNIT / 'stage_b_extract.py',
                 'stage-b-snapshot.md': UNIT / 'STAGE-B.md',
                 'inherited-extract-snapshot.py': OLD / 'extract.py',
                 'inherited-protocol-snapshot.md': OLD / 'PROTOCOL.md'}
    for name, original in snapshots.items():
        require(fingerprint(root / name) == initial['pins'][str(original)], 'snapshot-pin: ' + name)
    return initial


def expected_command():
    return ['/opt/homebrew/bin/ffmpeg', '-nostdin', '-nostats', '-hide_banner', '-v', 'warning',
            '-copyts', '-noautorotate', '-i', str(SOURCE), '-map', '0:v:0', '-an',
            '-noautoscale', '-pix_fmt', 'yuv420p', '-fps_mode', 'passthrough',
            '-enc_time_base:v', 'demux', '-f', 'rawvideo', '-']


def check_run(root, inputs, driver_sha):
    rows, metadata, pins, indices, reasons = inputs
    receipt = read_json(root / 'receipt.json')
    products = check_inventory(root, receipt)
    require(receipt['cameras'] == {'camera2': {'checked_frames': 8042, 'selected': 421}}, 'receipt-cameras')
    initial = check_initial(root, driver_sha)
    require(receipt['runtime_pins_before'] == initial['pins'] == receipt['runtime_pins_after'], 'runtime-pin-records')
    require(read_json(root / 'source-pins-before.json') == pins ==
            read_json(root / 'source-pins-after.json'), 'source-pin-files')
    plan = read_json(root / 'selection-plan.json')
    require(plan == {'start_seconds_exact': '220', 'end_seconds_exact': '234', 'closed': True,
                     'interior_count': 419, 'selected_count': 421, 'indices': indices,
                     'source_time_base': '1/2997'} and type(plan['closed']) is bool and
            all(type(i) is int for i in plan['indices']), 'selection-plan')
    destination = root / 'camera2'
    selected = read_json(destination / 'selection.json')
    require(selected['source_id'] == SOURCE_ID and selected['execution_kind'] == KIND, 'selection-source-kind')
    require(type(selected['checked_frames']) is int and selected['checked_frames'] == 8042 and
            selected['geometry'] == [640, 480], 'selection-count-geometry')
    require(type(selected['exit_code']) is int and selected['exit_code'] == 0, 'decoder-exit')
    require(selected['command'] == expected_command(), 'decoder-command')
    require(selected['raw_stream_sha256'] == RAW_SHA, 'full-raw-digest')
    require(selected['diagnostics'] == {'audio_layout_guess_stereo_lines': 1, 'unclassified_lines': 0,
                                      'raw_local_log': 'decoder.local-only.log'}, 'diagnostic-record')
    require(all(type(selected['diagnostics'][key]) is int for key in
                ('audio_layout_guess_stereo_lines', 'unclassified_lines')), 'diagnostic-count-type')
    diagnostic = check_diagnostic((destination / 'decoder.local-only.log').read_bytes())
    for key in ('input_pins', 'input_pins_before', 'input_pins_after'):
        require(selected[key] == pins, 'source-pin-record: ' + key)
    pixels = check_images(destination, selected['images'], rows, metadata, indices, reasons)
    check_sheets(destination, selected['overview_sheets'], selected['images'], pixels)
    expected_files = {'initial.json', 'selection-plan.json', 'source-pins-before.json', 'source-pins-after.json',
                      'driver-snapshot.py', 'stage-b-snapshot.md',
                      'inherited-extract-snapshot.py', 'inherited-protocol-snapshot.md',
                      'camera2/selection.json', 'camera2/decoder.local-only.log'}
    expected_files.update('camera2/' + e['png'] for e in selected['images'])
    expected_files.update('camera2/' + name for name in selected['overview_sheets'])
    require(set(products) == expected_files, 'contract-product-set')
    return {'products': products, 'diagnostic_normalized': diagnostic, 'initial': initial,
            'receipt_pin': fingerprint(root / 'receipt.json')}


def compare_runs(first, second):
    require(set(first['products']) == set(second['products']), 'repeat-inventory')
    for name in first['products']:
        if name != 'camera2/decoder.local-only.log':
            require(first['products'][name] == second['products'][name], 'repeat-product: ' + name)
    require(first['diagnostic_normalized'] == second['diagnostic_normalized'], 'repeat-diagnostic')


def unit_path(path, fresh=False):
    path = Path(path).absolute()
    require(path != UNIT and path.is_relative_to(UNIT) and path.resolve().is_relative_to(UNIT), 'scope-path')
    require(not any(p.is_symlink() for p in (path, *path.parents) if p != UNIT.parent), 'scope-symlink')
    if fresh:
        require(not path.exists() and path.parent.is_dir(), 'output-not-fresh-or-parent-missing')
    else:
        require(path.is_dir(), 'run-directory')
    return path


def verify_pair(run01, run02, driver_sha):
    require(run01.resolve() != run02.resolve(), 'distinct-runs-required')
    inputs = pinned_inputs()
    first = check_run(run01, inputs, driver_sha)
    second = check_run(run02, inputs, driver_sha)
    compare_runs(first, second)
    require(pinned_inputs() == inputs, 'verification-inputs-changed')
    # Check files again to reject a concurrent mutation during the product pass.
    for root, checked in ((run01, first), (run02, second)):
        require(fingerprint(root / 'receipt.json') == checked['receipt_pin'], 'receipt-changed')
        require(check_inventory(root, read_json(root / 'receipt.json')) == checked['products'], 'products-changed')
    return {'status': 'passed', 'scope': 'saved-product verification, no historical decode or image display',
            'runs': {str(run01): first['receipt_pin'], str(run02): second['receipt_pin']},
            'input_pins': inputs[2], 'all_map_metadata_rows': 8042, 'per_run_selected': 421,
            'per_run_overviews': 27, 'per_run_product_count': len(first['products']),
            'selection_first_last': [6593, 7013], 'interior_count': 419,
            'limits': ['Source-to-selected-Y-plane linkage relies on pinned producer execution; not independently redecoded.',
                       'Rawvideo carries no PTS; source-time join relies on recorded full ordered YUV hash checks.',
                       'Shared Pillow label raster and source inventory are dependencies, not independent historical evidence.',
                       'No endpoint, original-clock, camera-authentication, human-acceptance or causal finding.']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run01', required=True, type=Path)
    parser.add_argument('--run02', required=True, type=Path)
    parser.add_argument('--driver-sha', required=True)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args(argv)
    out = unit_path(args.out, fresh=True)
    runs = [unit_path(args.run01), unit_path(args.run02)]
    require(not any(out.is_relative_to(run) for run in runs), 'output-inside-run')
    try:
        result = verify_pair(*runs, args.driver_sha)
    except Exception as error:
        result = {'status': 'failed', 'error_type': type(error).__name__, 'error': str(error),
                  'scope': 'saved-product verification; no historical decode or image display'}
    result.update(checker=fingerprint(Path(__file__)), python=sys.version, pillow=PIL.__version__, argv=sys.argv[1:] if argv is None else argv)
    with out.open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'status': result['status'], 'output': str(out)}))
    return 0 if result['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
