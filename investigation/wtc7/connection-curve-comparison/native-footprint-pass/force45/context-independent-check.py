"""Independent F4/F5 raw-context and exact-white display verification.

No producer module or annotation file is imported or read. The pinned producer
display is a read-only subprocess; its output is parsed and compared against
a separately decoded RGB byte array. This is not an independent codec family,
source authentication, curve classification, or human acceptance.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

from PIL import Image, __version__ as pillow_version


HERE = Path(__file__).resolve().parent
PRODUCER_PYTHON = '/Users/admin/.pyenv/versions/3.13.7/bin/python3'
TARGETS = {'F4-Im4': [330, 0, 425, 88], 'F5-Im4': [375, 0, 475, 88],
           'F5-Im2': [225, 50, 350, 88]}
CONTEXTS = {'F4-Im4': [328, 0, 427, 88], 'F5-Im4': [373, 0, 477, 88],
            'F5-Im2': [223, 48, 352, 88]}
SOURCES = {'F4-Im4': 'Im4.jpg', 'F5-Im4': 'Im4.jpg', 'F5-Im2': 'Im2.jpg'}
PAIRS = {'F4-Im4': 'F4', 'F5-Im4': 'F5', 'F5-Im2': 'F5'}
DIMENSIONS = {'Im4.jpg': [741, 88], 'Im2.jpg': [741, 88]}
EXPECTED = {
    '../read_context.py': 'da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json': 'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    'PROTOCOL.md': '4df4510ba5664888124512ab052cfe535fce23dba482e5021cc69d4d0c47f285',
    '../../native-strips01/Im4.jpg': '53804060d00794d59628d6406337a6db5568bf30df63913ff4888b63082913fd',
    '../../native-strips01/Im2.jpg': '9f527c50ac92ef12454c550c66699773465cdc9aecfea55ca4130403166ae8e9',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    'read_context.py': 'cfce638b10df652fd8a8273603e9dee12c71952f567d4c1f534d6cd12e2b05ab',
    'context01.json': '161dfadf26fb6d7db86e83b025b208747a931bc83e4696830d1193dabd372fa4',
    'context02.json': '161dfadf26fb6d7db86e83b025b208747a931bc83e4696830d1193dabd372fa4',
    '../energy89/verification.json': '2b61e05714e2d7669052f0dfc467f24e591fb0528a92995c2a6247f6f3611b25',
}
WHITE = (255, 255, 255)


def demand(condition, reason):
    if not condition:
        raise AssertionError(reason)


def identical(actual, expected):
    """Unlike Python equality, reject booleans in place of integers."""
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(identical(actual[k], v) for k, v in expected.items())
    if isinstance(expected, (list, tuple)):
        return len(actual) == len(expected) and all(identical(a, b) for a, b in zip(actual, expected))
    return actual == expected


def file_pin(path):
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def context_box(target, size):
    demand(type(target) is list and len(target) == 4, 'four-edge target')
    demand(type(size) is list and len(size) == 2, 'two source dimensions')
    demand(all(type(n) is int for n in target + size), 'integer geometry, not booleans')
    x0, y0, x1, y1 = target
    width, height = size
    demand(0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height, 'bounded nonempty target')
    return [max(0, x0 - 2), max(0, y0 - 2), min(width, x1 + 2), min(height, y1 + 2)]


def metadata(data, targets, sources, pairs, dimensions, inputs, runtime):
    expected = {'target_boxes': targets, 'context_boxes': {
        name: context_box(box, dimensions[sources[name]]) for name, box in targets.items()},
        'sources': sources, 'pairs': pairs, 'source_dimensions': dimensions,
        'inputs': inputs, 'python': runtime[0], 'pillow': runtime[1],
        'classification': None, 'human_accepted': False}
    demand(type(data) is dict and set(data) == set(expected) | {'cells'}, 'complete exact metadata keys')
    for key, value in expected.items():
        demand(identical(data[key], value), 'metadata equality: ' + key)
    demand(type(data['cells']) is dict and set(data['cells']) == set(targets), 'distinct region cell keys')
    return expected['context_boxes']


def compare_cells(records, box, source_rgb, size):
    width, height = size
    demand(type(source_rgb) is bytes and len(source_rgb) == width * height * 3, 'decoded RGB byte count')
    x0, y0, x1, y1 = box
    demand(0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height, 'context is inside source')
    demand(type(records) is list and len(records) == (x1 - x0) * (y1 - y0), 'complete context record count')
    found = {}
    index = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            record = records[index]
            index += 1
            demand(type(record) is dict and set(record) == {'x', 'y', 'rgb'}, 'exact cell keys')
            demand(identical(record['x'], x) and identical(record['y'], y), 'row-major unique integer coordinates')
            rgb = record['rgb']
            demand(type(rgb) is list and len(rgb) == 3 and all(type(v) is int and 0 <= v <= 255 for v in rgb),
                   'RGB triplet of bounded integers')
            offset = (y * width + x) * 3
            actual = tuple(source_rgb[offset:offset + 3])
            demand(tuple(rgb) == actual, 'every source RGB byte equals saved RGB')
            found[x, y] = actual
    return found


def read_sparse(text, box):
    x0, y0, x1, y1 = box
    lines = text.splitlines()
    demand(len(lines) == x1 - x0, 'one sparse line per context column')
    found = {}
    for x, line in zip(range(x0, x1), lines):
        demand(line.startswith(str(x) + ':'), 'canonical ordered column label')
        prior_y = y0 - 1
        for token in line[len(str(x)) + 1:].split():
            demand(re.fullmatch(r'(0|[1-9][0-9]*):(0|[1-9][0-9]*),(0|[1-9][0-9]*),(0|[1-9][0-9]*)', token),
                   'canonical row and RGB token')
            y_text, rgb_text = token.split(':')
            y, rgb = int(y_text), tuple(map(int, rgb_text.split(',')))
            demand(y0 <= y < y1 and y > prior_y, 'sorted unique in-range sparse rows')
            demand(all(v <= 255 for v in rgb) and rgb != WHITE, 'nonwhite bounded channels')
            prior_y = y
            found[x, y] = rgb
    return found


def exact_white_roundtrip(all_cells, shown):
    demand(set(shown) <= set(all_cells), 'display adds no coordinate')
    demand(all(shown.get(where, WHITE) == value for where, value in all_cells.items()),
           'roundtrip every cell with exact-white default')
    demand(len(shown) == sum(value != WHITE for value in all_cells.values()), 'only exact white omitted')


def controls():
    """Independent nonhistorical fixtures; no image or repository source reads."""
    checks = {}

    def must_fail(label, action):
        try:
            action()
        except AssertionError:
            checks[label] = True
        else:
            checks[label] = False

    checks['clip_full_height'] = context_box([3, 0, 7, 8], [10, 8]) == [1, 0, 9, 8]
    checks['clip_all_edges'] = context_box([0, 0, 4, 2], [4, 2]) == [0, 0, 4, 2]
    checks['clip_interior'] = context_box([3, 3, 4, 4], [8, 8]) == [1, 1, 6, 6]
    for label, target, size in [
        ('target_boolean', [True, 0, 2, 2], [4, 2]),
        ('dimension_boolean', [0, 0, 1, 1], [4, True]),
        ('outside_target', [0, 0, 5, 2], [4, 2]),
        ('empty_target', [2, 0, 2, 2], [4, 2]),
    ]:
        must_fail('reject_' + label, lambda target=target, size=size: context_box(target, size))

    rgb = bytes([7, 8, 9, 255, 255, 255, 0, 4, 7,
                 4, 5, 6, 255, 254, 255, 255, 255, 255])
    rows = [{'x': 1, 'y': 0, 'rgb': [255, 255, 255]}, {'x': 2, 'y': 0, 'rgb': [0, 4, 7]},
            {'x': 1, 'y': 1, 'rgb': [255, 254, 255]}, {'x': 2, 'y': 1, 'rgb': [255, 255, 255]}]
    box = [1, 0, 3, 2]
    full = compare_cells(rows, box, rgb, [3, 2])
    sparse = read_sparse('1: 1:255,254,255\n2: 0:0,4,7\n', box)
    exact_white_roundtrip(full, sparse)
    checks['explicit_rgb_offsets'] = full == {
        (1, 0): WHITE, (2, 0): (0, 4, 7), (1, 1): (255, 254, 255), (2, 1): WHITE}
    checks['near_white_preserved'] = sparse[1, 1] == (255, 254, 255)
    checks['exact_white_roundtrip'] = len(sparse) == 2
    for label, mutate in [
        ('duplicate_coordinate', lambda a: a[1].update(x=1)),
        ('boolean_coordinate', lambda a: a[0].update(x=True)),
        ('boolean_channel', lambda a: a[0]['rgb'].__setitem__(0, True)),
        ('wrong_rgb_byte', lambda a: a[0]['rgb'].__setitem__(0, 254)),
        ('unordered_records', lambda a: a.reverse()),
        ('missing_record', lambda a: a.pop()),
        ('extra_record', lambda a: a.append(copy.deepcopy(a[-1]))),
        ('unexpected_key', lambda a: a[0].update(extra=None)),
    ]:
        bad = copy.deepcopy(rows)
        mutate(bad)
        must_fail('reject_cell_' + label, lambda bad=bad: compare_cells(bad, box, rgb, [3, 2]))
    for label, value in [
        ('duplicate_column', '1:\n1:\n'), ('missing_column', '1:\n'),
        ('extra_column', '1:\n2:\n3:\n'), ('column_leading_zero', '01:\n2:\n'),
        ('duplicate_row', '1: 0:1,2,3 0:4,5,6\n2:\n'),
        ('unordered_rows', '1: 1:1,2,3 0:4,5,6\n2:\n'),
        ('outside_row', '1: 2:1,2,3\n2:\n'), ('negative_row', '1: -1:1,2,3\n2:\n'),
        ('leading_zero_row', '1: 00:1,2,3\n2:\n'), ('explicit_white', '1: 0:255,255,255\n2:\n'),
        ('outside_channel', '1: 0:256,1,2\n2:\n'), ('negative_channel', '1: 0:-1,1,2\n2:\n'),
        ('boolean_channel', '1: 0:True,1,2\n2:\n'), ('missing_channel', '1: 0:1,2\n2:\n'),
    ]:
        must_fail('reject_display_' + label, lambda value=value: read_sparse(value, box))
    for label, value in [
        ('near_white_omitted', {(2, 0): (0, 4, 7)}),
        ('wrong_rgb', {(1, 1): (255, 253, 255), (2, 0): (0, 4, 7)}),
        ('extra_position', {**sparse, (3, 0): (1, 2, 3)}),
    ]:
        must_fail('reject_roundtrip_' + label, lambda value=value: exact_white_roundtrip(full, value))

    targets = {'P-a': [0, 0, 1, 1], 'P-b': [0, 0, 1, 1]}
    sources, pairs, dimensions = {'P-a': 'a', 'P-b': 'b'}, {'P-a': 'P', 'P-b': 'P'}, {'a': [1, 1], 'b': [1, 1]}
    payload = {'target_boxes': targets, 'context_boxes': copy.deepcopy(targets),
               'sources': sources, 'pairs': pairs, 'source_dimensions': dimensions,
               'inputs': {'f': {'sha256': 'synthetic', 'bytes': 1}},
               'python': 'synthetic', 'pillow': 'synthetic', 'classification': None, 'human_accepted': False,
               'cells': {'P-a': [{'x': 0, 'y': 0, 'rgb': [1, 2, 3]}],
                         'P-b': [{'x': 0, 'y': 0, 'rgb': [4, 5, 6]}]}}
    args = (targets, sources, pairs, dimensions, payload['inputs'], ('synthetic', 'synthetic'))
    metadata(payload, *args)
    a = compare_cells(payload['cells']['P-a'], targets['P-a'], bytes([1, 2, 3]), [1, 1])
    b = compare_cells(payload['cells']['P-b'], targets['P-b'], bytes([4, 5, 6]), [1, 1])
    checks['same_pair_native_coordinate_retains_source_identity'] = a[0, 0] != b[0, 0]
    must_fail('reject_swapped_source_rgb', lambda: compare_cells(payload['cells']['P-a'], targets['P-a'], bytes([4, 5, 6]), [1, 1]))
    for label, mutate in [
        ('source_reassignment', lambda d: d['sources'].update({'P-a': 'b'})),
        ('pair_reassignment', lambda d: d['pairs'].update({'P-a': 'Q'})),
        ('collapsed_region_keys', lambda d: d['cells'].pop('P-b')),
        ('target_boolean', lambda d: d['target_boxes']['P-a'].__setitem__(0, False)),
        ('dimension_boolean', lambda d: d['source_dimensions']['a'].__setitem__(0, True)),
        ('changed_pin', lambda d: d['inputs']['f'].update(sha256='wrong')),
        ('changed_runtime', lambda d: d.update(python='wrong')),
        ('human_acceptance', lambda d: d.update(human_accepted=True)),
        ('classification', lambda d: d.update(classification='curve')),
        ('extra_metadata', lambda d: d.update(extra=None)),
    ]:
        bad = copy.deepcopy(payload)
        mutate(bad)
        must_fail('reject_metadata_' + label, lambda bad=bad: metadata(bad, *args))
    demand(all(checks.values()), 'all synthetic controls pass')
    return checks


def run():
    checked_controls = controls()
    before = {name: file_pin(HERE / name) for name in EXPECTED}
    for name, expected in EXPECTED.items():
        demand(before[name]['sha256'] == expected, 'frozen pin: ' + name)
    before['context-independent-check.py'] = file_pin(Path(__file__))
    raw01, raw02 = (HERE / 'context01.json').read_bytes(), (HERE / 'context02.json').read_bytes()
    demand(raw01 == raw02 and len(raw01) == 2830264, 'both complete context saves byte-identical')
    data = json.loads(raw01)
    inputs = {name: pin for name, pin in before.items()
              if name not in ('context01.json', 'context02.json', '../energy89/verification.json', 'context-independent-check.py')}
    boxes = metadata(data, TARGETS, SOURCES, PAIRS, DIMENSIONS, inputs, ('3.13.7', '12.0.0'))
    demand(identical(boxes, CONTEXTS), 'all independently clipped contexts match fixed protocol')
    roster = json.loads((HERE / '../REGIONS.json').read_text())
    for pair in ('F4', 'F5'):
        selected = [entry for entry in roster['pairs'] if entry['id'] == pair]
        expected = [[SOURCES[r].removesuffix('.jpg'), *TARGETS[r]] for r in TARGETS if PAIRS[r] == pair]
        demand(len(selected) == 1 and identical(selected[0]['new_regions'], expected), 'parent fixed roster: ' + pair)

    prior_root = HERE / '../energy89'
    prior_manifest = json.loads((prior_root / 'verification.json').read_text())
    prior_before = {name: file_pin(prior_root / name) for name in prior_manifest['pins']}
    demand(identical(prior_before, prior_manifest['pins']), 'all older energy89 pins preserved')

    decoded = {}
    for source_name, size in DIMENSIONS.items():
        with Image.open(HERE / '../../native-strips01' / source_name) as image:
            demand(image.mode == 'RGB' and list(image.size) == size, 'unchanged source RGB representation')
            image.load()
            decoded[source_name] = image.tobytes()
    results, commands = {}, []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for region in TARGETS:
        source_name = SOURCES[region]
        box = boxes[region]
        all_cells = compare_cells(data['cells'][region], box, decoded[source_name], DIMENSIONS[source_name])
        command = [PRODUCER_PYTHON, '-B', str(HERE / 'read_context.py'), 'show', '--region', region,
                   '--first', str(box[0]), '--last', str(box[2] - 1)]
        process = subprocess.run(command, capture_output=True, check=False, env=env)
        demand(process.returncode == 0 and process.stderr == b'', 'producer read-only display succeeds')
        display = process.stdout.decode('utf-8')
        header, body = display.split('\n', 1)
        demand(header == f'Native {region}; exact RGB, only exact (255,255,255) omitted; all other context cells shown.',
               'explicit exact-white display header')
        shown = read_sparse(body, box)
        exact_white_roundtrip(all_cells, shown)
        commands.append(command)
        results[region] = {'pair': PAIRS[region], 'source': source_name, 'source_dimensions': DIMENSIONS[source_name],
                           'target_box': TARGETS[region], 'context_box': box,
                           'records_checked': len(all_cells), 'display_columns': box[2] - box[0],
                           'nonwhite_shown': len(shown), 'exact_white_omitted': len(all_cells) - len(shown),
                           'near_white_retained': sum(value != WHITE and min(value) >= 254 for value in all_cells.values()),
                           'all_rgb_equal': True, 'display_roundtrip_equal': True,
                           'display_stdout_bytes': len(process.stdout),
                           'display_stdout_sha256': hashlib.sha256(process.stdout).hexdigest(),
                           'display_exit_code': process.returncode}
    after = {name: file_pin(HERE / name) for name in before}
    prior_after = {name: file_pin(prior_root / name) for name in prior_before}
    demand(before == after and prior_before == prior_after, 'new and prior inputs unchanged during verification')
    total = sum(result['records_checked'] for result in results.values())
    demand(total == 23024, 'all three declared raw contexts checked')
    return {'status': 'passed', 'role': 'independent computational check; no visual or annotation interpretation',
            'controls': checked_controls, 'control_count': len(checked_controls),
            'inputs_before': before, 'inputs_after': after,
            'producer_dependency_count': len(inputs), 'regions': results, 'total_records_checked': total,
            'prior_energy89_manifest_pin': before['../energy89/verification.json'],
            'prior_energy89_artifact_pins_before': prior_before, 'prior_energy89_artifact_pins_after': prior_after,
            'prior_energy89_artifact_pin_count': len(prior_before), 'repeat_bytes_equal': True,
            'runtime': {'python': platform.python_version(), 'pillow': pillow_version},
            'saved_producer_runtime': {'python': data['python'], 'pillow': data['pillow']},
            'command': [sys.executable, '-B', str(Path(__file__).resolve())],
            'read_only_display_commands': commands,
            'limits': [
                'No producer helper imported; the pinned producer display runs only as a read-only subprocess.',
                'Checker uses bundled Python/Pillow, but shares the Pillow decoder family with production.',
                'Context record count includes overlap; it is not a count of independent historical observations.',
                'No annotation files read and no visible ink classification, curve fit, ordinate, seam join, or model comparison.',
                'Composed-page bytes are pinned only; rendering or correspondence is not independently checked here.',
                'Faithful raw RGB and display reproduction does not authenticate historical source content or establish physical support.',
            ], 'human_accepted': False, 'physical_support': None}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--output', choices=['context-independent-check.json', 'context-independent-check-repeat.json'])
    args = parser.parse_args()
    value = {'status': 'passed', 'controls': controls()} if args.controls else run()
    raw = json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n'
    if args.output:
        with (HERE / args.output).open('x') as destination:
            destination.write(raw)
        print(json.dumps({'status': value['status'], 'output': args.output, 'pin': file_pin(HERE / args.output)}))
    else:
        print(raw, end='')
