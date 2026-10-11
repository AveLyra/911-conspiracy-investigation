#!/usr/bin/env python3
"""Seven pinned diagnostic images; no brightness or historical event scoring."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import re
import subprocess
import sys

from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'camera3-late-reannotation' / 'prepare.py'
BASE_SHA = '0b7baeb81236a7ab8fdb5435ed7d86e10c754e22fd35f94051d96538ae29d139'
SOURCE_SHA = '48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722'
MAP_SHA = '8afdf759ecc45215b9212699ef2adb72de553c52667d82b39c9382df8e6b36c2'
INDICES = tuple(range(255, 262))
WIDTH, HEIGHT, COUNT = 720, 480, 442
PTS = (17000, 17066, 17133, 17200, 17266, 17333, 17400)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def selected_planes(raw, width, height, count, indices):
    if any(type(n) is not int or n <= 0 for n in (width, height, count)):
        raise ValueError('invalid_dimensions')
    size = width * height
    if len(raw) != count * size:
        raise ValueError('raw_length')
    if not indices or len(set(indices)) != len(indices):
        raise ValueError('empty_or_duplicate_indices')
    if any(type(i) is not int or not 0 <= i < count for i in indices):
        raise ValueError('index_range')
    return [(i, raw[i * size:(i + 1) * size]) for i in indices]


def output_path(name):
    if not re.fullmatch(r'[a-z0-9_-]+', name):
        raise ValueError('invalid_output_name')
    out = HERE / name
    if out.exists():
        raise ValueError('output_exists')
    return out


def check_png(path, pixels, width, height):
    with Image.open(path) as image:
        image.load()
        if image.mode != 'L' or image.size != (width, height):
            raise ValueError('png_format')
        if image.tobytes() != pixels:
            raise ValueError('png_pixels')


def load_base():
    if sha(BASE.read_bytes()) != BASE_SHA:
        raise ValueError('base_code_changed')
    spec = importlib.util.spec_from_file_location('pinned_camera3_prepare', BASE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # Reviewed definitions; its main is not called.
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    out = output_path(args.out)
    base = load_base()
    paths = {
        'source': base.SOURCE, 'binary': base.BIN,
        'map': base.OLD / 'default-frames.json',
        'old_receipt': base.OLD / 'receipt.json',
        'base_code': BASE, 'code': Path(__file__),
        'tests': HERE / 'test_prepare.py', 'protocol': HERE / 'PROTOCOL.md',
        'old_png258': BASE.parent / 'views01' / 'frame-0258.png',
        'charter': base.PUBLIC / 'CHARTER.md',
        'python_executable': Path(sys.executable),
    }
    before = {key: base.pin(path) for key, path in paths.items()}
    if before['source']['sha256'] != SOURCE_SHA:
        raise ValueError('source_changed')
    if before['map']['sha256'] != MAP_SHA:
        raise ValueError('map_changed')
    old = json.loads(paths['old_receipt'].read_text())
    mapping = json.loads(paths['map'].read_text())
    if before['binary'] != old['binaries'][str(base.BIN)]:
        raise ValueError('binary_changed')
    if (mapping['raw_frame_count'] != COUNT or
            len(mapping['records']) != COUNT or len(mapping['pixel_hashes']) != COUNT):
        raise ValueError('map_count')
    for index, pts in zip(INDICES, PTS):
        row = mapping['records'][index]
        if row['index'] != index or row['pts'] != pts or row['time_base'] != '1/1000':
            raise ValueError('map_clock')
    argv = [str(base.BIN), '-nostdin', '-nostats', '-hide_banner',
            '-loglevel', 'repeat+level+info', '-debug_ts', '-copyts',
            '-noautorotate', '-i', str(base.SOURCE), '-map', '0:v:0', '-an',
            '-noautoscale', '-pix_fmt', 'gray', '-fps_mode', 'passthrough',
            '-enc_time_base:v', 'demux', '-f', 'rawvideo', '-']
    original = [c['argv'] for c in old['commands'] if c['label'] == 'default']
    if original != [argv]:
        raise ValueError('recipe_changed')
    out.mkdir()
    receipt = {'status': 'started', 'python': platform.python_version(),
               'pillow': pillow_version, 'inputs': {k: str(v) for k, v in paths.items()},
               'inputs_before': before, 'argv': argv, 'indices': list(INDICES)}
    (out / 'start.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    try:
        proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        (out / 'decode.stderr.local.txt').write_bytes(proc.stderr)
        raw = proc.stdout
        receipt['decode'] = {'returncode': proc.returncode, 'raw_bytes': len(raw),
                             'raw_sha256': sha(raw), 'all_frame_hashes_match': None,
                             'corrupt_mentions': proc.stderr.count(b'corrupt decoded frame'),
                             'stderr_sha256': sha(proc.stderr)}
        planes = selected_planes(raw, WIDTH, HEIGHT, COUNT, INDICES)
        all_hashes = [sha(raw[i * WIDTH * HEIGHT:(i + 1) * WIDTH * HEIGHT])
                      for i in range(COUNT)]
        receipt['decode']['all_frame_hashes_match'] = all_hashes == mapping['pixel_hashes']
        if (proc.returncode or sha(raw) != mapping['raw_sha256'] or
                all_hashes != mapping['pixel_hashes'] or
                receipt['decode']['corrupt_mentions'] != 3):
            raise ValueError('decode_identity_or_warning_failure')
        receipt['frames'] = []
        for index, pixels in planes:
            name = f'frame-{index:04d}.png'
            path = out / name
            Image.frombytes('L', (WIDTH, HEIGHT), pixels).save(path)
            check_png(path, pixels, WIDTH, HEIGHT)
            if index == 258:
                check_png(paths['old_png258'], pixels, WIDTH, HEIGHT)
            receipt['frames'].append({'index': index, 'name': name,
                                      'clock': mapping['records'][index],
                                      'pixel_sha256': sha(pixels), **base.pin(path)})
        after = {key: base.pin(path) for key, path in paths.items()}
        receipt['inputs_after'] = after
        if after != before:
            raise ValueError('input_changed_during_run')
        receipt['status'] = 'pass_diagnostic_only'
    except Exception as exc:
        receipt['status'] = 'failed_no_images_admitted'
        receipt['exception'] = type(exc).__name__ + ': ' + str(exc)
        if isinstance(exc, subprocess.TimeoutExpired):
            (out / 'decode.stderr.local.txt').write_bytes(exc.stderr or b'')
            receipt['decode'] = {'returncode': None, 'timed_out': True,
                                 'raw_bytes': len(exc.output or b''),
                                 'raw_sha256': sha(exc.output or b''),
                                 'all_frame_hashes_match': None,
                                 'stderr_sha256': sha(exc.stderr or b''),
                                 'corrupt_mentions': (exc.stderr or b'').count(b'corrupt decoded frame')}
        (out / 'failure.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
        raise
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': receipt['status'], 'frames': len(receipt['frames']),
                      'all_442_hashes_match': True, 'warnings_retained': 3}))


if __name__ == '__main__':
    main()
