"""Independent E8/E9 context/RGB/display check; no producer module imports.

Producer show is exercised as a pinned read-only black box. Parsing, geometry,
RGB offsets and fixture expectations are separately implemented here. This is
not visual classification, historical authentication or a second codec family.
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
TARGETS = {'E8': [535, 54, 690, 86], 'E9': [530, 30, 690, 56]}
CONTEXTS = {'E8': [533, 52, 692, 88], 'E9': [528, 28, 692, 58]}
SOURCES = {'E8': 'Im7.jpg', 'E9': 'Im7.jpg'}
EXPECTED = {
    '../read_context.py': 'da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json': 'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    'PROTOCOL.md': '98edc562841efdbc3ffb7f25c813b507cf553142a972f5558680e7218f7e6e25',
    '../../native-strips01/Im7.jpg': '3509c0fb002d47d1cc9d1ae624377534c8b31bd9fea7fdadd380a7b5f4d4a09d',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    'read_context.py': '377d4f41b990502ca87fc7d1b4b9b069eede0aa71f281c68cb5ae879d7196a2c',
    'context01.json': '0f7528e58a57f7244673a79d4fbfd77bdb9c8c6f277cb57b3686cb8bcff818c7',
    'context02.json': '0f7528e58a57f7244673a79d4fbfd77bdb9c8c6f277cb57b3686cb8bcff818c7',
}


def require(ok, label):
    if not ok:
        raise AssertionError(label)


def pin(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def clipped_context(box, width, height):
    require(type(box) is list and len(box) == 4 and all(type(n) is int for n in box), 'integer box')
    x0, y0, x1, y1 = box
    require(0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height, 'target bounds')
    return [max(0, x0 - 2), max(0, y0 - 2), min(width, x1 + 2), min(height, y1 + 2)]


def source_cells(rows, box, rgb, width, height):
    require(len(rgb) == width * height * 3, 'RGB byte length')
    x0, y0, x1, y1 = box
    require(0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height, 'context bounds')
    require(type(rows) is list and len(rows) == (x1 - x0) * (y1 - y0), 'all context records')
    values = {}
    for i, row in enumerate(rows):
        x, y = x0 + i % (x1 - x0), y0 + i // (x1 - x0)
        require(type(row) is dict and sorted(row) == ['rgb', 'x', 'y'], 'context record fields')
        require(type(row['x']) is int and type(row['y']) is int and row['x'] == x and row['y'] == y,
                'unique row-major context coordinates')
        value = row['rgb']
        require(type(value) is list and len(value) == 3 and all(type(v) is int and 0 <= v <= 255 for v in value),
                'integer RGB triplet')
        offset = 3 * (y * width + x)
        require(tuple(value) == tuple(rgb[offset:offset + 3]), 'fresh RGB offset equality')
        values[x, y] = tuple(value)
    return values


def parse_display(lines, box):
    x0, y0, x1, y1 = box
    require(len(lines) == x1 - x0, 'every display column')
    values = {}
    for i, line in enumerate(lines):
        require(':' in line, 'display column separator')
        lead, body = line.split(':', 1)
        x = x0 + i
        require(lead == str(x), 'canonical ordered display column')
        previous = y0 - 1
        for token in body.split():
            require(token.count(':') == 1, 'display row separator')
            row_text, channels_text = token.split(':')
            require(re.fullmatch(r'0|[1-9][0-9]*', row_text) is not None, 'canonical row integer')
            y = int(row_text)
            require(y0 <= y < y1 and y > previous, 'bounded ordered unique display rows')
            previous = y
            channels = channels_text.split(',')
            require(len(channels) == 3 and all(re.fullmatch(r'0|[1-9][0-9]*', v) for v in channels),
                    'canonical RGB channel integers')
            value = tuple(int(v) for v in channels)
            require(all(0 <= v <= 255 for v in value), 'display channel bounds')
            require(value != (255, 255, 255), 'exact-white only omitted not explicit')
            values[x, y] = value
    return values


def display_roundtrip(values, sparse):
    require(all(xy in values for xy in sparse), 'no added display position')
    for xy, value in values.items():
        require(sparse.get(xy, (255, 255, 255)) == value, 'every display cell matches source')
    require(len(sparse) == sum(v != (255, 255, 255) for v in values.values()), 'only exact-white omitted')


def controls():
    results = {}
    rgb = bytes([9, 9, 9, 255, 255, 255, 0, 4, 7, 8, 8, 8, 255, 254, 255, 255, 255, 255])
    rows = [{'x': 1, 'y': 0, 'rgb': [255, 255, 255]}, {'x': 2, 'y': 0, 'rgb': [0, 4, 7]},
            {'x': 1, 'y': 1, 'rgb': [255, 254, 255]}, {'x': 2, 'y': 1, 'rgb': [255, 255, 255]}]
    box = [1, 0, 3, 2]
    values = source_cells(rows, box, rgb, 3, 2)
    sparse = parse_display(['1: 1:255,254,255', '2: 0:0,4,7'], box)
    display_roundtrip(values, sparse)
    results['explicit_RGB_offsets_and_full_roundtrip'] = values == {
        (1, 0): (255, 255, 255), (2, 0): (0, 4, 7), (1, 1): (255, 254, 255), (2, 1): (255, 255, 255)}
    results['near_white_preserved'] = sparse[1, 1] == (255, 254, 255)
    results['omitted_white_recovered'] = sparse.get((1, 0), (255, 255, 255)) == (255, 255, 255)
    results['clipped_two_cell_context'] = clipped_context([1, 1, 4, 3], 5, 4) == [0, 0, 5, 4]
    bad_displays = [
        ('duplicate_column', ['1:', '1:']), ('missing_column', ['1:']),
        ('extra_column', ['1:', '2:', '3:']), ('column_leading_zero', ['01:', '2:']),
        ('unordered_rows', ['1: 1:1,2,3 0:1,2,3', '2:']),
        ('duplicate_rows', ['1: 0:1,2,3 0:4,5,6', '2:']),
        ('outside_row', ['1: 2:1,2,3', '2:']), ('negative_row', ['1: -1:1,2,3', '2:']),
        ('row_leading_zero', ['1: 00:1,2,3', '2:']), ('explicit_white', ['1: 0:255,255,255', '2:']),
        ('outside_channel', ['1: 0:256,1,2', '2:']), ('negative_channel', ['1: 0:-1,1,2', '2:']),
        ('boolean_channel', ['1: 0:True,1,2', '2:']), ('missing_channel', ['1: 0:1,2', '2:']),
    ]
    for label, lines in bad_displays:
        try:
            parse_display(lines, box)
        except AssertionError:
            results['reject_display_' + label] = True
        else:
            results['reject_display_' + label] = False
    bad_rows = []
    a = copy.deepcopy(rows); a[1]['x'] = 1; bad_rows.append(('duplicate_coordinate', a))
    a = copy.deepcopy(rows); a[0]['x'] = True; bad_rows.append(('boolean_coordinate', a))
    a = copy.deepcopy(rows); a[0]['rgb'][0] = True; bad_rows.append(('boolean_channel', a))
    a = copy.deepcopy(rows); a[0]['rgb'][0] = 256; bad_rows.append(('channel_bounds', a))
    a = copy.deepcopy(rows); a[0]['rgb'][0] = 254; bad_rows.append(('single_wrong_byte', a))
    a = copy.deepcopy(rows); a.reverse(); bad_rows.append(('wrong_order', a))
    bad_rows.append(('missing_record', rows[:-1]))
    for label, corrupt in bad_rows:
        try:
            source_cells(corrupt, box, rgb, 3, 2)
        except AssertionError:
            results['reject_context_' + label] = True
        else:
            results['reject_context_' + label] = False
    for label, corrupt in [('near_white_omitted', {(2, 0): (0, 4, 7)}),
                           ('wrong_visible_cell', {(1, 1): (255, 254, 254), (2, 0): (0, 4, 7)}),
                           ('added_position', dict(sparse, **{}))]:
        if label == 'added_position':
            corrupt[3, 0] = (1, 2, 3)
        try:
            display_roundtrip(values, corrupt)
        except AssertionError:
            results['reject_roundtrip_' + label] = True
        else:
            results['reject_roundtrip_' + label] = False
    require(all(results.values()), 'all independent synthetic controls')
    return results


def run():
    tested = controls()
    before = {name: pin(HERE / name) for name in EXPECTED}
    for name, sha in EXPECTED.items():
        require(before[name]['sha256'] == sha, 'frozen pin ' + name)
    before['context-independent-check.py'] = pin(Path(__file__))
    first, second = (HERE / 'context01.json').read_bytes(), (HERE / 'context02.json').read_bytes()
    require(first == second, 'context repeat exact bytes')
    context = json.loads(first)
    require(context == json.loads(second), 'context repeat structure')
    require(sorted(context) == sorted(['cells', 'classification', 'context_boxes', 'human_accepted', 'inputs',
                                       'pillow', 'python', 'sources', 'target_boxes']), 'exact context metadata keys')
    require(context['target_boxes'] == TARGETS and context['context_boxes'] == CONTEXTS, 'fixed rectangles')
    require(context['sources'] == SOURCES and sorted(context['cells']) == ['E8', 'E9'], 'fixed sources/pairs')
    require(context['human_accepted'] is False and context['classification'] is None, 'unclassified unaccepted')
    require(context['python'] == '3.13.7' and context['pillow'] == '12.0.0', 'recorded producer runtime')
    expected_inputs = {name: value for name, value in before.items()
                       if name not in ('context01.json', 'context02.json', 'context-independent-check.py')}
    require(context['inputs'] == expected_inputs, 'all metadata dependency pins exact')
    roster = json.loads((HERE / '../REGIONS.json').read_text())
    for pair, box in TARGETS.items():
        entries = [entry for entry in roster['pairs'] if entry['id'] == pair]
        require(len(entries) == 1 and entries[0]['new_regions'] == [['Im7'] + box], 'parent fixed region ' + pair)
    with Image.open(HERE / '../../native-strips01/Im7.jpg') as source:
        require(source.mode == 'RGB' and source.size == (745, 92), 'source RGB representation')
        source.load()
        rgb = source.tobytes()
    details, commands = {}, []
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for pair, target in TARGETS.items():
        box = clipped_context(target, 745, 92)
        require(box == CONTEXTS[pair], 'independently derived clipped context')
        values = source_cells(context['cells'][pair], box, rgb, 745, 92)
        x0, _, x1, _ = box
        command = [sys.executable, '-B', str(HERE / 'read_context.py'), 'show', '--pair', pair,
                   '--first', str(x0), '--last', str(x1 - 1)]
        shown = subprocess.run(command, capture_output=True, text=True, env=env, check=False)
        require(shown.returncode == 0 and not shown.stderr, 'read-only producer display successful')
        lines = shown.stdout.splitlines()
        require(lines and lines[0] == 'Native ' + pair + '; exact RGB, only exact (255,255,255) omitted; all other context cells shown.',
                'exact display convention header')
        sparse = parse_display(lines[1:], box)
        display_roundtrip(values, sparse)
        commands.append(command)
        details[pair] = {'target_box': target, 'context_box': box, 'checked_cells': len(values),
                         'display_columns': x1 - x0, 'nonwhite_shown': len(sparse),
                         'exact_white_omitted': len(values) - len(sparse),
                         'near_white_nonwhite_retained': sum(v != (255, 255, 255) and min(v) >= 254 for v in values.values()),
                         'source_representation': 'RGB 745x92', 'display_exit_code': shown.returncode,
                         'display_stdout_bytes': len(shown.stdout.encode()),
                         'display_stdout_sha256': hashlib.sha256(shown.stdout.encode()).hexdigest(),
                         'ordering': 'all unique row-major context cells; ascending display columns/rows',
                         'pixel_comparison': 'all match fresh RGB byte offsets',
                         'display_roundtrip': 'every source cell recovered with exact-white default only'}
    after = {name: pin(HERE / name) for name in before}
    require(after == before, 'all context/source/code/protocol inputs preserved')
    total = sum(row['checked_cells'] for row in details.values())
    require(total == 10644, 'complete declared E8/E9 contexts')
    return {'status': 'passed', 'checker_role': 'same-source nonblind AI computational check; no visual classification or annotation reading',
            'independent_controls': tested, 'independent_control_count': len(tested),
            'inputs': before, 'inputs_after': after, 'pair_results': details,
            'total_checked_cells': total, 'repeat_bytes_equal': True, 'repeat_structure_equal': True,
            'declared_pin_count': len(expected_inputs),
            'runtime': {'python': platform.python_version(), 'pillow': pillow_version},
            'saved_producer_runtime': {'python': context['python'], 'pillow': context['pillow']},
            'command': [sys.executable, '-B', str(Path(__file__).resolve())],
            'read_only_display_commands': commands,
            'limits': [
                'No producer module imported by this checker. Pinned producer show is executed as a read-only black box and imports its own pinned helper internally.',
                'The checker uses a different Python/Pillow environment from saved production, but both use the Pillow decoder family; no independent codec validation.',
                'No annotation files opened, images visually viewed, model identity classified, containment calibrated, physical support admitted or human acceptance supplied.',
                'The composed page is integrity-checked only; its rendering and visual correspondence are not evaluated.',
                '10644 counts context records across both pairs; overlapping source positions are checked in each context and are not independent historical evidence.',
                'The display reader may omit only exact white. Successful faithful display does not certify that selected nonwhite cells are curve ink.',
            ], 'human_accepted': False, 'physical_support': None}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--output', choices=['context-independent-check.json', 'context-independent-check-repeat.json'])
    args = parser.parse_args()
    result = {'status': 'passed', 'controls': controls()} if args.controls else run()
    raw = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n'
    if args.output:
        target = HERE / args.output
        with target.open('x') as output:
            output.write(raw)
        print(json.dumps({'output': target.name, 'pin': pin(target), 'status': result['status']}))
    else:
        print(raw, end='')
