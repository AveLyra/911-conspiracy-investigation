#!/usr/bin/env python3
"""Fixed synthetic raster controls. No historical input or curve classifier."""
import argparse
import hashlib
from io import BytesIO
import itertools
import json
from pathlib import Path
import platform
import sys
import warnings

import PIL
from PIL import Image, features

HERE = Path(__file__).resolve().parent
PROTOCOL_SHA = '4adaa3b617a624de9353feda130c1778e0c60d00e133d88754f66baa3298b248'
WIDTH, HEIGHT = 160, 96
COLORS = {'black': (0, 0, 0), 'gold': (204, 153, 0), 'blue': (0, 0, 255),
          'red': (255, 0, 0), 'green': (0, 128, 0), 'cyan': (0, 180, 180),
          'purple': (128, 0, 128)}
CODECS = {'png': ('PNG', {'compress_level': 6}),
          'jpg95s0': ('JPEG', {'quality': 95, 'subsampling': 0, 'optimize': False, 'progressive': False}),
          'jpg75s0': ('JPEG', {'quality': 75, 'subsampling': 0, 'optimize': False, 'progressive': False}),
          'jpg75s2': ('JPEG', {'quality': 75, 'subsampling': 2, 'optimize': False, 'progressive': False}),
          'jpg50s2': ('JPEG', {'quality': 50, 'subsampling': 2, 'optimize': False, 'progressive': False})}
ALLOWANCES = (0, 1, 2, 4)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode()


def rgb(value, target=False):
    if (not isinstance(value, (list, tuple)) or len(value) != 3
            or any(type(c) is not int or not 0 <= c <= 255 for c in value)
            or (target and tuple(value) == (255, 255, 255))):
        raise ValueError('invalid_rgb_or_white_target')
    return tuple(value)


def params(color, w, m2, p2, style):
    if (color not in COLORS or type(w) is not int or w not in (1, 3)
            or type(m2) is not int or m2 not in (0, 1)
            or type(p2) is not int or p2 not in (0, 1)
            or style not in ('solid', 'dashed')):
        raise ValueError('invalid_fixture')
    return {'color': color, 'rgb': list(COLORS[color]), 'w': w, 'm2': m2, 'p2': p2, 'style': style}


def fixtures():
    for values in itertools.product(COLORS, (1, 3), (0, 1), (0, 1), ('solid', 'dashed')):
        p = params(*values)
        yield f'{p["color"]}-w{p["w"]}-m{p["m2"]}-p{p["p2"]}-{p["style"]}', p


def mixed_channel(channel, covered):
    if type(channel) is not int or not 0 <= channel <= 255 or type(covered) is not int or not 0 <= covered <= 16:
        raise ValueError('invalid_mixture')
    return (covered * channel + (16 - covered) * 255 + 8) // 16


def segment(label, m2, p2, w, start=16, end=144, dashed=False):
    # For these declared controls m2 may be -1 only in crossing scenes.
    return {'label': label, 'm2': m2, 'p2': p2, 'w': w,
            'start': start, 'end': end, 'dashed': dashed}


def validate_scene(scene):
    if not isinstance(scene, dict) or set(scene) != {'description', 'color', 'segments', 'white_masks'}:
        raise ValueError('invalid_scene')
    rgb(scene['color'], target=True)
    if not isinstance(scene['description'], str) or not isinstance(scene['segments'], list) or not isinstance(scene['white_masks'], list):
        raise ValueError('invalid_scene_fields')
    for s in scene['segments']:
        if (not isinstance(s, dict) or set(s) != {'label', 'm2', 'p2', 'w', 'start', 'end', 'dashed'}
                or not isinstance(s['label'], str) or not s['label']
                or type(s['m2']) is not int or s['m2'] not in (-1, 0, 1)
                or type(s['p2']) is not int or s['p2'] not in (0, 1)
                or type(s['w']) is not int or s['w'] not in (1, 3)
                or any(type(s[k]) is not int for k in ('start', 'end'))
                or not 0 <= s['start'] < s['end'] <= WIDTH or type(s['dashed']) is not bool):
            raise ValueError('invalid_segment')
    for box in scene['white_masks']:
        if (not isinstance(box, (list, tuple)) or len(box) != 4
                or any(type(v) is not int for v in box)
                or not 0 <= box[0] < box[2] <= WIDTH or not 0 <= box[1] < box[3] <= HEIGHT):
            raise ValueError('invalid_mask')


def in_segment(u16, v16, s):
    if not 16 * s['start'] <= u16 < 16 * s['end']:
        return False
    if s['dashed'] and ((u16 - 16 * 16) // (8 * 16)) % 2:
        return False
    center32 = 48 * 32 + s['m2'] * (u16 - 80 * 16) + 16 * s['p2']
    return center32 - 16 * s['w'] <= 2 * v16 < center32 + 16 * s['w']


def render_scene(scene):
    """Union same-color coverage, then opaque white masks, at 4x4 point samples."""
    validate_scene(scene)
    target = scene['color']
    output = bytearray(WIDTH * HEIGHT * 3)
    offset = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            count = 0
            for dy in (2, 6, 10, 14):
                for dx in (2, 6, 10, 14):
                    u, v = 16 * x + dx, 16 * y + dy
                    occupied = any(in_segment(u, v, s) for s in scene['segments'])
                    masked = any(16*a <= u < 16*c and 16*b <= v < 16*d
                                 for a, b, c, d in scene['white_masks'])
                    count += int(occupied and not masked)
            output[offset:offset+3] = bytes(mixed_channel(c, count) for c in target)
            offset += 3
    return Image.frombytes('RGB', (WIDTH, HEIGHT), bytes(output))


def fixture_scene(p):
    checked = params(p['color'], p['w'], p['m2'], p['p2'], p['style'])
    if p != checked:
        raise ValueError('fixture_schema_mismatch')
    return {'description': 'Single declared synthetic line; fixed 4x4 point sampling.',
            'color': p['rgb'], 'segments': [segment('A', p['m2'], p['p2'], p['w'], dashed=p['style'] == 'dashed')],
            'white_masks': []}


def candidate(pixel, target):
    pixel, target = rgb(pixel), rgb(target, target=True)
    q = [255-c for c in target]
    z = [255-c for c in pixel]
    Q = sum(v*v for v in q)
    A = sum(v*t for v, t in zip(z, q))
    return 5*A >= Q and all(abs(v*Q-A*t) <= 32*Q for v, t in zip(z, q))


def row_runs(rows):
    if (not isinstance(rows, (list, tuple)) or any(type(y) is not int or not 0 <= y < HEIGHT for y in rows)
            or list(rows) != sorted(set(rows))):
        raise ValueError('invalid_row_membership')
    runs = []
    for y in rows:
        if not runs or y != runs[-1][1]:
            runs.append([y, y+1])
        else:
            runs[-1][1] += 1
    return runs


def column_record(x, rows, p):
    params(p['color'], p['w'], p['m2'], p['p2'], p['style'])
    if type(x) is not int or not 16 <= x < 144:
        raise ValueError('invalid_column')
    runs = row_runs(rows)
    truth = p['style'] == 'solid' or ((x - 16) // 8) % 2 == 0
    truth_y2 = [96+p['m2']*(x-80)+p['p2'], 96+p['m2']*(x+1-80)+p['p2']] if truth else None
    status = 'missing' if not runs else ('single' if len(runs) == 1 else 'ambiguous')
    envelope = runs[0] if status == 'single' else None
    allowances = {}
    for allowance in ALLOWANCES:
        expanded = [envelope[0]-allowance, envelope[1]+allowance] if envelope else None
        allowances[str(allowance)] = {'envelope_y': expanded,
            'width': expanded[1]-expanded[0] if expanded else None,
            'covered': (2*expanded[0] <= truth_y2[0] and 2*expanded[1] >= truth_y2[1]) if expanded and truth else None}
    return {'x': x, 'truth_support': truth, 'truth_centerline_y2': truth_y2,
            'runs_y': runs, 'run_widths': [b-a for a, b in runs], 'status': status,
            'envelope_y': envelope, 'envelope_width': envelope[1]-envelope[0] if envelope else None,
            'allowances': allowances}


def analyze(image, p):
    fixture_scene(p)
    if image.mode != 'RGB' or image.size != (WIDTH, HEIGHT):
        raise ValueError('invalid_image_shape_or_mode')
    pixels = image.load()
    records = [column_record(x, [y for y in range(HEIGHT) if candidate(pixels[x, y], p['rgb'])], p)
               for x in range(16, 144)]
    true = [r for r in records if r['truth_support']]
    gaps = [r for r in records if not r['truth_support']]
    summary = {'true_columns': len(true), 'gap_columns': len(gaps),
               'true_status_columns': {s: [r['x'] for r in true if r['status'] == s]
                                       for s in ('missing', 'ambiguous', 'single')},
               'gap_candidate_columns': [r['x'] for r in gaps if r['runs_y']],
               'gap_status_columns': {s: [r['x'] for r in gaps if r['status'] == s]
                                      for s in ('missing', 'ambiguous', 'single')},
               'allowances': {}}
    for a in map(str, ALLOWANCES):
        summary['allowances'][a] = {
            'covered_columns': [r['x'] for r in true if r['allowances'][a]['covered'] is True],
            'single_enclosure_failures': [r['x'] for r in true if r['allowances'][a]['covered'] is False],
            'unassessed_missing_or_ambiguous': [r['x'] for r in true if r['allowances'][a]['covered'] is None]}
    return {'columns': records, 'summary': summary}


def encode_decode(image, codec):
    if codec not in CODECS or image.mode != 'RGB' or image.size != (WIDTH, HEIGHT):
        raise ValueError('invalid_codec_or_image')
    fmt, settings = CODECS[codec]
    buffer = BytesIO()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        image.save(buffer, format=fmt, **settings)
        data = buffer.getvalue()
        with Image.open(BytesIO(data)) as opened:
            opened.load()
            if opened.mode != 'RGB' or opened.size != (WIDTH, HEIGHT) or getattr(opened, 'n_frames', 1) != 1:
                raise ValueError('decoded_shape_mode_frame_mismatch')
            decoded = opened.copy()
    return data, decoded, [str(w.message) for w in caught]


def ambiguity_pairs():
    def scene(description, color, segments, masks=()):
        return {'description': description, 'color': list(color), 'segments': segments, 'white_masks': list(masks)}
    yield 'dash-mask', (
        scene('A is dashed; no occluder.', COLORS['red'], [segment('A', 1, 1, 1, dashed=True)]),
        scene('A is solid; white gap rectangles applied AFTER line coverage.', COLORS['red'], [segment('A', 1, 1, 1)],
              [[x, 0, x+8, HEIGHT] for x in range(24, 144, 16)]))
    yield 'cross-identity', (
        scene('A retains positive slope and B negative slope through crossing.', COLORS['blue'],
              [segment('A', 1, 0, 3), segment('B', -1, 0, 3)]),
        scene('After u=80, A takes negative-slope branch and B positive-slope branch; labels are latent, not painted.', COLORS['blue'],
              [segment('A', 1, 0, 3, end=80), segment('B', -1, 0, 3, end=80),
               segment('A', -1, 0, 3, start=80), segment('B', 1, 0, 3, start=80)]))
    yield 'full-occlusion', (
        scene('No latent line and no mask.', COLORS['purple'], []),
        scene('Latent positive-slope line completely covered by white AFTER line coverage.', COLORS['purple'],
              [segment('A', 1, 1, 3)], [[0, 0, WIDTH, HEIGHT]]))


def pin(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': sha(data)}


def input_pins():
    names = ['RASTER-UNCERTAINTY-STAGE.md', 'NUMERICAL-PROTOCOL.md', 'HUMAN-REVIEW-GATE.md',
             'REGISTRATION-STAGE.md', 'raster_uncertainty.py', 'test_raster_uncertainty.py']
    result = {name: pin(HERE/name) for name in names}
    if result['RASTER-UNCERTAINTY-STAGE.md']['sha256'] != PROTOCOL_SHA:
        raise ValueError('protocol_pin_mismatch')
    return result


def write_new(path, data):
    with path.open('xb') as stream:
        stream.write(data)


def run(name):
    if name not in ('synthetic-run01', 'synthetic-run02'):
        raise ValueError('output_name_not_allowed')
    before = input_pins()
    if sys.version_info[:3] != (3, 12, 14) or PIL.__version__ != '12.3.0':
        raise ValueError('runtime_version_mismatch')
    output = HERE/name
    output.mkdir(exist_ok=False)  # Including existing empty directories/symlinks.
    products = {}
    def save(relative, data):
        path = output/relative
        path.parent.mkdir(parents=True, exist_ok=True)
        write_new(path, data)
        products[relative] = {'bytes': len(data), 'sha256': sha(data)}
    try:
        runtime = {'python': platform.python_version(), 'pillow': PIL.__version__,
                   'jpeg_codec': features.version_codec('jpg'), 'libjpeg_turbo': features.version_feature('libjpeg_turbo'),
                   'executable': pin(Path(sys.executable)), 'pillow_entry': pin(Path(PIL.__file__)),
                   'imaging_binary': pin(Path(Image.core.__file__)),
                   'limit': 'Entry-point/binary hashes, not complete dependency closure.'}
        save('runtime.json', json_bytes(runtime))
        summaries = []
        for identifier, p in fixtures():
            base = render_scene(fixture_scene(p))
            for codec, (fmt, settings) in CODECS.items():
                encoded, decoded, diagnostics = encode_decode(base, codec)
                extension = 'png' if fmt == 'PNG' else 'jpg'
                image_path = f'cases/{identifier}/{codec}.{extension}'
                save(image_path, encoded)
                report = {'id': identifier, 'parameters': p, 'codec': codec, 'settings': settings,
                          'encoded': {'path': image_path, 'bytes': len(encoded), 'sha256': sha(encoded)},
                          'base_rgb_sha256': sha(base.tobytes()), 'decoded_rgb_sha256': sha(decoded.tobytes()),
                          'warnings': diagnostics, **analyze(decoded, p)}
                save(f'cases/{identifier}/{codec}.json', json_bytes(report))
                summaries.append({'id': identifier, 'codec': codec, 'warnings': diagnostics, **report['summary']})
        pairs = []
        for identifier, scenes in ambiguity_pairs():
            save(f'ambiguity/{identifier}/latent.json', json_bytes({'a': scenes[0], 'b': scenes[1]}))
            a, b = [render_scene(scene) for scene in scenes]
            pair = {'id': identifier, 'latent_descriptors_differ': scenes[0] != scenes[1],
                    'base_equal': a.tobytes() == b.tobytes(),
                    'base_a_sha256': sha(a.tobytes()), 'base_b_sha256': sha(b.tobytes()), 'codecs': {}}
            for codec, (fmt, _) in CODECS.items():
                left, dl, wl = encode_decode(a, codec)
                right, dr, wr = encode_decode(b, codec)
                for side, data in [('a', left), ('b', right)]:
                    save(f'ambiguity/{identifier}/{side}-{codec}.{"png" if fmt == "PNG" else "jpg"}', data)
                pair['codecs'][codec] = {'encoded_equal': left == right, 'decoded_equal': dl.tobytes() == dr.tobytes(),
                    'a_encoded_sha256': sha(left), 'b_encoded_sha256': sha(right),
                    'a_rgb_sha256': sha(dl.tobytes()), 'b_rgb_sha256': sha(dr.tobytes()), 'warnings': {'a': wl, 'b': wr}}
            save(f'ambiguity/{identifier}/results.json', json_bytes(pair))
            pairs.append(pair)
        after = input_pins()
        if before != after:
            raise ValueError('inputs_changed')
        save('summary.json', json_bytes({'base_fixtures': 112, 'encoded_cases': len(summaries),
                                       'case_summaries': summaries, 'ambiguity_pairs': pairs}))
        write_new(output/'manifest.json', json_bytes({'status': 'completed_not_scientifically_accepted',
            'input_pins_before': before, 'input_pins_after': after, 'products': products,
            'fixed_dimensions': [WIDTH, HEIGHT], 'fixed_allowances': ALLOWANCES, 'codec_settings': CODECS,
            'command_template': 'bundled-python -B raster_uncertainty.py --run synthetic-run01|synthetic-run02'}))
    except Exception as exc:
        write_new(output/'failure.json', json_bytes({'error_type': type(exc).__name__, 'message': str(exc),
                                                     'completed_products': products}))
        raise
    return {'run': name, 'cases': len(summaries), 'products': len(products), 'manifest': pin(output/'manifest.json')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True, choices=['synthetic-run01', 'synthetic-run02'])
    args = parser.parse_args()
    print(json.dumps(run(args.run), sort_keys=True))


if __name__ == '__main__':
    main()
