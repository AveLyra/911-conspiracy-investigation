#!/usr/bin/env python3
"""Finite manual-envelope controls; no historical inputs or pixel detector."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys

import PIL
from PIL import Image, ImageDraw, features

HERE = Path(__file__).resolve().parent
PROTOCOL_SHA = '11e1d727b2de69c50ed6c343f59b101a4ec3f3b8c2ad724bff5557da1b0318ad'
RENDERER_SHA = '878872fcde4316e2655e156221de970a41f5186351a9525159c7eb7520e8760f'
COLUMNS = [20, 23, 24, 28, 32, 36]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def packed(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode()


def pin(path):
    data = path.read_bytes()
    return {'sha256': digest(data), 'bytes': len(data)}


def column_runs(image, x):
    runs = []
    for y in range(image.height):
        value = list(image.getpixel((x, y)))
        if runs and runs[-1][2] == value:
            runs[-1][1] = y + 1
        else:
            runs.append([y, y + 1, value])
    return runs


def generate(name):
    inputs = {p.name: pin(p) for p in [HERE/'PROTOCOL.md', HERE/'trial.py', HERE.parent/'raster_uncertainty.py']}
    assert inputs['PROTOCOL.md']['sha256'] == PROTOCOL_SHA
    assert inputs['raster_uncertainty.py']['sha256'] == RENDERER_SHA
    spec = importlib.util.spec_from_file_location('frozen_renderer', HERE.parent/'raster_uncertainty.py')
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    out = HERE/name
    out.mkdir(exist_ok=False)
    products = {}
    def save(relative, data):
        target = out/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as f:
            f.write(data)
        products[relative] = {'sha256': digest(data), 'bytes': len(data)}
    def png(image):
        from io import BytesIO
        buffer = BytesIO()
        image.save(buffer, format='PNG', compress_level=6)
        return buffer.getvalue()
    public, truths, pictures = [], [], []
    for color in renderer.COLORS:
        for condition, width, slope2, phase2, codec in [('A', 1, 1, 1, 'png'), ('B', 3, -1, 0, 'jpg50s2')]:
            for style in ['solid', 'dashed']:
                identifier = f'T{len(truths)+1:02d}'
                scene = {'description': 'Declared isolated synthetic stroke.', 'color': list(renderer.COLORS[color]),
                         'segments': [renderer.segment('A', slope2, phase2, width, dashed=style=='dashed')], 'white_masks': []}
                encoded, decoded, warnings = renderer.encode_decode(renderer.render_scene(scene), codec)
                ext = 'png' if codec == 'png' else 'jpg'
                save(f'packet/{identifier}.{ext}', encoded)
                rows = {str(x): column_runs(decoded, x) for x in COLUMNS}
                save(f'packet/{identifier}-columns.json', packed({'id': identifier, 'size': list(decoded.size), 'columns_rle': rows,
                    'convention': '[first row,end row exclusive,unfiltered RGB], exhaustive native column'}))
                public.append({'id': identifier, 'image': f'{identifier}.{ext}', 'columns': COLUMNS, 'raw': f'{identifier}-columns.json'})
                truths.append({'id': identifier, 'condition': condition, 'color': color, 'style': style, 'scene': scene,
                               'codec': codec, 'warnings': warnings,
                               'columns': [{'x': x, 'support': style=='solid' or ((x-16)//8)%2==0,
                                            'endpoint_y2': [96+slope2*(x-80)+phase2, 96+slope2*(x+1-80)+phase2]} for x in COLUMNS]})
                pictures.append((identifier, decoded))
    for first in range(0, 28, 4):
        canvas = Image.new('RGB', (960, 624), 'white')
        draw = ImageDraw.Draw(canvas)
        for j, (identifier, decoded) in enumerate(pictures[first:first+4]):
            left, top = (j%2)*480, (j//2)*312
            draw.text((left+8, top+5), identifier, fill='black')
            canvas.paste(decoded.resize((480, 288), Image.Resampling.NEAREST), (left, top+24))
        save(f'packet/contact-{first//4+1:02d}.png', png(canvas))
    questions = [
        'Do visible interruptions alone establish a dashed generating path rather than an occluded continuous path?',
        'Do pixels alone establish which same-color identity continues through the crossing?',
        'Does the blank picture establish absence of a hidden path?']
    refusals = []
    for i, (name, scenes) in enumerate(renderer.ambiguity_pairs(), 1):
        identifier = f'R{i:02d}'
        a, b = [renderer.render_scene(s) for s in scenes]
        ea, _, _ = renderer.encode_decode(a, 'png')
        eb, _, _ = renderer.encode_decode(b, 'png')
        save(f'packet/{identifier}.png', ea)
        save(f'truth/{identifier}-alternative.png', eb)
        refusals.append({'id': identifier, 'kind': name, 'scenes': list(scenes), 'encoded_equal': ea==eb, 'rgb_equal': a.tobytes()==b.tobytes()})
        public.append({'id': identifier, 'image': f'{identifier}.png', 'question': questions[i-1]})
    scene = {'description': 'Solid path continuing beyond a later crop.', 'color': list(renderer.COLORS['black']),
             'segments': [renderer.segment('A', 0, 0, 3)], 'white_masks': []}
    full = renderer.render_scene(scene)
    cropped = full.crop((16, 0, 64, 96))
    save('packet/R04.png', png(cropped))
    refusals.append({'id': 'R04', 'kind': 'crop-not-endpoint', 'scene': scene, 'crop': [16, 0, 64, 96], 'continues_beyond_crop': True})
    public.append({'id': 'R04', 'image': 'R04.png', 'question': 'Does the line reaching the right picture edge establish its physical endpoint?'})
    save('packet/index.json', packed(public))
    save('truth.json', packed({'tiles': truths, 'refusals': refusals}))
    save('runtime.json', packed({'python': platform.python_version(), 'pillow': PIL.__version__, 'jpeg': features.version_codec('jpg'),
        'executable': pin(Path(sys.executable)), 'imaging_binary': pin(Path(Image.core.__file__))}))
    after = {p.name: pin(p) for p in [HERE/'PROTOCOL.md', HERE/'trial.py', HERE.parent/'raster_uncertainty.py']}
    assert after == inputs
    save('manifest.json', packed({'inputs': inputs, 'products': products.copy(), 'scope': 'synthetic generation only, no annotation scoring'}))
    print(json.dumps({'run': name, 'products': len(products), 'manifest': pin(out/'manifest.json')}))


def envelope(entry):
    if set(entry) != {'x', 'core', 'fringe', 'status', 'cue'} or type(entry['x']) is not int or entry['x'] not in COLUMNS:
        raise ValueError('invalid_entry')
    for key in ('core', 'fringe'):
        values = entry[key]
        if not isinstance(values, list) or any(type(v) is not int or not 0 <= v < 96 for v in values) or values != sorted(set(values)):
            raise ValueError('invalid_rows')
    if set(entry['core']) & set(entry['fringe']):
        raise ValueError('overlapping_core_fringe')
    if entry['status'] not in ('identified', 'unresolved') or not isinstance(entry['cue'], str) or not entry['cue'].strip():
        raise ValueError('invalid_status_or_cue')
    outer = sorted(entry['core'] + entry['fringe'])
    if entry['status'] == 'unresolved':
        return None
    if not outer or outer != list(range(outer[0], outer[-1]+1)):
        raise ValueError('identified_empty_or_disconnected')
    return [outer[0], outer[-1]+1]


def score(reader, truth):
    if set(reader['tiles']) != {t['id'] for t in truth['tiles']}:
        raise ValueError('tile_coverage')
    if set(reader['refusals']) != {r['id'] for r in truth['refusals']}:
        raise ValueError('refusal_coverage')
    results, nonvacuity = [], {}
    for tile in truth['tiles']:
        entries = reader['tiles'][tile['id']]
        if [e['x'] for e in entries] != COLUMNS:
            raise ValueError('column_coverage')
        correct = 0
        for entry, expected in zip(entries, tile['columns']):
            bounds = envelope(entry)
            y2 = expected['endpoint_y2']
            outcome = 'withheld' if bounds is None else ('false_admission' if not expected['support'] else
                       'contained' if 2*bounds[0] <= min(y2) and max(y2) <= 2*bounds[1] else 'containment_failure')
            # 20 and 36 are strictly interior in every declared isolated line.
            correct += int(outcome == 'contained' and entry['x'] in (20, 36))
            results.append({'id': tile['id'], 'x': entry['x'], 'bounds': bounds, 'width': bounds[1]-bounds[0] if bounds else None,
                            'truth_support': expected['support'], 'truth_endpoint_y2': y2, 'outcome': outcome})
        nonvacuity[tile['id']] = correct > 0
    refusal_results = {}
    for key, answer in reader['refusals'].items():
        if set(answer) != {'answer', 'reason'} or answer['answer'] not in ('unresolved', 'established') or not isinstance(answer['reason'], str) or not answer['reason'].strip():
            raise ValueError('invalid_refusal')
        refusal_results[key] = answer['answer'] == 'unresolved'
    counts = {o: sum(r['outcome']==o for r in results) for o in ['contained', 'withheld', 'false_admission', 'containment_failure']}
    return {'entries': results, 'counts': counts, 'nonvacuity': nonvacuity, 'refusals_correct': refusal_results,
            'method_passes_this_reader': not counts['false_admission'] and not counts['containment_failure'] and all(nonvacuity.values()) and all(refusal_results.values())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', choices=['run01', 'run02'])
    parser.add_argument('--score', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.generate and not args.score and not args.output:
        generate(args.generate)
    elif args.score and args.output and not args.generate:
        result = score(json.loads(args.score.read_text()), json.loads((HERE/'run01/truth.json').read_text()))
        payload = {'reader': pin(args.score), 'truth': pin(HERE/'run01/truth.json'), 'code': pin(HERE/'trial.py'), 'result': result}
        with args.output.open('xb') as f:
            f.write(packed(payload))
        print(json.dumps({'result': pin(args.output), 'counts': result['counts'], 'method_passes_this_reader': result['method_passes_this_reader']}))
    else:
        parser.error('choose generation or reader score with new output')


if __name__ == '__main__':
    main()
