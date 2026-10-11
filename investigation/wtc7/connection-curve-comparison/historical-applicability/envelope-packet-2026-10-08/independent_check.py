"""Read-only independent audit of the conditional mapping packet.

No packet, admission, selection, mapping or historical envelope-arithmetic
imports. Targets are reconstructed from original elementary segment lengths;
inverse coordinates are reconstructed by affine native-endpoint interpolation.
Protocol/schema were inspected: this is not a blind source reading.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import itertools
import json
import os
from pathlib import Path
import struct
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
PARENT = BASE/'historical-applicability/admission-2026-10-08'
PARENT_SHA = '4aeca445bc71d4495dd578df6a4de96e3bf2d54004b6afb0b1efcf7bb631930e'
RECEIPT_SHA = '9d05f112c632af128ae2d37f18a0fcab0ebabb78cc76f0d5bc453493feb88afd'
PROTOCOL_SHA = 'ffa2fc84231d2b19dedfc6be7272460f05a980cdf6c5c6d8f15c36a66e8baaa9'
REP_SHA = '1cbb52b2e12a3d2b13d1a2ac008aab091bf64dc57deaf5b646fd6098521992e5'
PAGE_SHA = '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6'
PDF = Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf')
PDF_SHA = 'cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4'
PAIRS = tuple(panel+str(n) for panel in ('F', 'E') for n in range(3, 10))
ROLES = ('primary', 'peer')
STATES = {'gap', 'solid_only', 'dash_only', 'overlapping_candidate_coverage',
          'shared_ink_ownership_conflict', 'paired_local_candidate'}


def demand(condition, message):
    if not condition:
        raise ValueError(message)


def q(value):
    demand(type(value) in (str, int, Q), 'exact rational required')
    return Q(value)


def canonical(value):
    if type(value) is Q:
        return str(value)
    if type(value) is dict:
        return {key: canonical(item) for key, item in value.items()}
    if type(value) in (list, tuple):
        return [canonical(item) for item in value]
    return value


def encoded(value):
    return (json.dumps(canonical(value), sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()


def pin(path):
    raw = Path(path).read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def load(path):
    return json.loads(Path(path).read_text(), parse_float=Q)


def pin_shape(value):
    demand(type(value) is dict and set(value) == {'bytes', 'sha256'}, 'invalid pin fields')
    demand(type(value['bytes']) is int and value['bytes'] >= 0, 'invalid pin byte count')
    digest = value['sha256']
    demand(type(digest) is str and len(digest) == 64 and
           all(char in '0123456789abcdef' for char in digest), 'invalid pin digest')


def add_pin(result, path, expected=None):
    path = Path(path).resolve()
    key = os.path.relpath(path, BASE)
    observed = pin(path)
    if type(expected) is str:
        demand(observed['sha256'] == expected, 'changed fixed input: '+key)
    elif expected is not None:
        pin_shape(expected)
        demand(observed == expected, 'changed pinned input: '+key)
    demand(key not in result or result[key] == observed, 'conflicting pin: '+key)
    result[key] = observed
    return key


def require_closure(found, required):
    demand(type(found) is dict, 'input map required')
    for key, value in required.items():
        demand(found.get(key) == value, 'required dependency missing/changed: '+key)
    for value in found.values():
        pin_shape(value)


def elementary(segments):
    parsed = []
    for segment in segments:
        demand(type(segment['render_x']) is list and len(segment['render_x']) == 2, 'segment endpoints required')
        a, b = map(q, segment['render_x'])
        demand(a < b and (not parsed or a >= parsed[-1][1]), 'overlapping/reversed segment domain')
        demand(segment['status'] in STATES, 'unknown segment state')
        parsed.append((a, b, segment['status']))
    return parsed


def select_from_segments(segments, fraction):
    """Locate qL in original positive-length paired segments, never a hull."""
    fraction = q(fraction)
    demand(0 < fraction < 1, 'interior fraction required')
    selected = [(a, b) for a, b, state in elementary(segments) if state == 'paired_local_candidate']
    total = sum((b-a for a, b in selected), Q(0))
    # Independent connected-component construction: retain endpoints but do
    # not treat bookkeeping components as support at their internal cuts.
    starts = [i for i, interval in enumerate(selected) if i == 0 or interval[0] != selected[i-1][1]]
    ends = starts[1:]+[len(selected)]
    components = [[selected[start][0], selected[end-1][1]] for start, end in zip(starts, ends)]
    if not selected:
        return {'page_x': None, 'total_length': Q(0), 'component': None, 'cumulative_tie': False}, components
    target = fraction*total
    cumulative = list(itertools.accumulate(b-a for a, b in selected))
    chosen = next(i for i, end in enumerate(cumulative) if target <= end)
    before = cumulative[chosen-1] if chosen else Q(0)
    x = selected[chosen][0]+target-before
    component = next(i for i, (a, b) in enumerate(components) if a <= x <= b)
    component_end = sum((b-a for a, b in components[:component+1]), Q(0))
    return {'page_x': x, 'total_length': total, 'component': component,
            'cumulative_tie': target == component_end}, components


def scenario_position(segments, x):
    parsed = elementary(segments)
    if x is None:
        return {'status': 'no_primary_target', 'segment_indices': []}
    x = q(x)
    boundaries = [i for i, (a, b, _) in enumerate(parsed) if x == a or x == b]
    occupied = [i for i, (a, b, _) in enumerate(parsed) if a < x < b]
    demand(len(occupied) <= 1, 'multiple elementary interiors')
    if boundaries:
        return {'status': 'boundary_unresolved', 'segment_indices': boundaries}
    if occupied:
        return {'status': parsed[occupied[0]][2], 'segment_indices': occupied}
    return {'status': 'outside_candidate_extent', 'segment_indices': []}


def source_mapping(cell, page_x, invocation):
    page_x = q(page_x)
    width, height = invocation['native_dimensions']
    demand(type(width) is int and type(height) is int and min(width, height) > 0, 'invalid native dimensions')
    a, b, c, d, e, f = map(q, invocation['ctm'])
    demand(a > 0 and d > 0 and b == c == 0, 'unsupported CTM')
    native = cell['native_rectangle']
    demand(type(native) is list and len(native) == 4 and all(type(n) is int for n in native), 'native rectangle types')
    x0, y0, x1, y1 = native
    demand(0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height, 'native rectangle outside image')
    corners = []
    for u, v in itertools.product((x0, x1), (y0, y1)):
        pdf_x = e+a*Q(u, width)
        pdf_y = f+d*Q(height-v, height)
        corners.append((pdf_x*Q(25, 9), (792-pdf_y)*Q(25, 9)))
    rect = [min(p[0] for p in corners), min(p[1] for p in corners),
            max(p[0] for p in corners), max(p[1] for p in corners)]
    demand(rect == list(map(q, cell['render_rectangle'])) and
           [rect[0], rect[2]] == list(map(q, cell['render_x'])), 'frozen candidate mapping inconsistent')
    demand(rect[0] <= page_x <= rect[2], 'source target not in candidate footprint')
    # Invert by proportional position between independently transformed native
    # endpoints, not the producer's global inverse-CTM formula.
    native_x = x0+(page_x-rect[0])*(x1-x0)/(rect[2]-rect[0])
    demand(x0 <= native_x <= x1, 'inverse target outside native footprint')
    return {'cell_id': cell['id'], 'reader_path': cell['reader_path'], 'role': cell['role'],
        'route': cell['route'], 'source': cell['source'], 'fragment_id': cell['fragment_id'],
        'native_rectangle': native, 'render_rectangle': rect, 'native_x': native_x,
        'boundary_touch': page_x == rect[0] or page_x == rect[2],
        'asset_url': '/source/'+cell['source']+'.jpg'}


def displacement_hull(x, axis):
    if x is None:
        return None
    x = q(x)
    left, right = [q(v) for v in axis['L']], [q(v) for v in axis['R']]
    demand(len(left) == len(right) == 2 and left[0] <= left[1] < right[0] <= right[1], 'invalid horizontal axis')
    samples = []
    for l in left:
        for r in right:
            samples.append(Q(8, 5)*(x-l)/(r-l))
    return [min(samples), max(samples)]


def footprint(entry, role):
    return tuple(sorted((m['source'], tuple(m['native_rectangle'])) for m in entry['mappings'][role]))


def mark_duplicates(slots):
    """Pairwise footprint comparison, independent of producer grouping."""
    for slot in slots:
        for entry in slot['entries']:
            for role in ROLES:
                signature = footprint(entry, role)
                entry['duplicate_entries'][role] = [other['id'] for other_slot in slots
                    if other_slot['pair'] == slot['pair'] for other in other_slot['entries']
                    if other['id'] != entry['id'] and other['model'] == entry['model'] and
                    signature and footprint(other, role) == signature]
        signatures = [footprint(entry, 'primary') for entry in slot['entries']]
        slot['duplicate_paired_slots'] = [other['id'] for other in slots if other['pair'] == slot['pair'] and
            other['id'] != slot['id'] and all(signatures) and
            [footprint(entry, 'primary') for entry in other['entries']] == signatures]


def reconstruct(admission, invocations):
    demand(tuple(p['pair'] for p in admission['pairs']) == PAIRS, 'fourteen pair roster/order changed')
    slots, inventory = [], []
    for pair in admission['pairs']:
        name = pair['pair']
        scenarios = {(r['solid_reader'], r['dash_reader']): r for r in pair['scenarios']}
        demand(len(pair['scenarios']) == 4 and set(scenarios) == set(itertools.product(ROLES, repeat=2)),
               'four distinct scenarios required')
        primary = scenarios[('primary', 'primary')]
        component_reference = None
        for number, fraction in enumerate((Q(1, 4), Q(1, 2), Q(3, 4)), 1):
            target, components = select_from_segments(primary['segments'], fraction)
            component_reference = components
            x = target['page_x']
            states = {solid+'-'+dash: scenario_position(scenarios[(solid, dash)]['segments'], x)
                      for solid, dash in itertools.product(ROLES, repeat=2)}
            status = 'unavailable_empty_primary_domain' if x is None else states['primary-primary']['status']
            demand(x is None or status in ('paired_local_candidate', 'boundary_unresolved'), 'selected noncandidate position')
            slot = {'id': 'CE-'+name+'Q'+str(number), 'pair': name, 'quantile': fraction, **target,
                'selection_status': status, 'scenario_states': states,
                'displacement_m': {key: displacement_hull(x, box) for key, box in admission['axis_boxes'].items()
                                   if key.startswith(name[0]+'-')},
                'duplicate_paired_slots': [], 'entries': [], 'human_accepted': False}
            for model, route in (('spring', 'solid'), ('shell', 'dash')):
                mapping = {role: [] for role in ROLES}
                if x is not None:
                    for cell in admission['candidate_cells']:
                        if (cell['pair'] == name and cell['route'] == route and
                                q(cell['render_x'][0]) <= x <= q(cell['render_x'][1])):
                            demand(cell['role'] in ROLES and cell['source'] in invocations, 'unrostered source alternative')
                            mapping[cell['role']].append(source_mapping(cell, x, invocations[cell['source']]))
                reason = ('No primary paired coverage; do not invent a coordinate.' if x is None else
                          'Boundary locator only; point support unresolved.' if status == 'boundary_unresolved' else
                          'Conditional local mapping proposed; not accepted curve support.')
                slot['entries'].append({'id': slot['id']+'-'+model, 'model': model, 'style': route,
                    'mappings': mapping, 'duplicate_entries': {role: [] for role in ROLES},
                    'human_response': None, 'human_status': 'uninspected', 'reason': reason})
            slots.append(slot)
        inventory.append({'pair': name, 'primary_length_bookkeeping': component_reference,
            'own_candidate_render_lengths': primary['own_candidate_render_lengths'],
            'all_scenarios_preserved_in': 'admission-2026-10-08/run01.json'})
    mark_duplicates(slots)
    return slots, inventory


def image_header(path):
    """Inspect dimensions/8-bit three-channel encoding without a pixel decoder."""
    raw = Path(path).read_bytes()
    if raw.startswith(b'\x89PNG\r\n\x1a\n'):
        demand(raw[12:16] == b'IHDR' and len(raw) >= 29, 'invalid PNG header')
        width, height, depth, color = struct.unpack('>IIBB', raw[16:26])
        demand(depth == 8 and color == 2, 'PNG must be 8-bit RGB')
        return width, height
    demand(raw[:2] == b'\xff\xd8', 'expected JPEG or PNG')
    index = 2
    frames = set(range(0xc0, 0xd0)) - {0xc4, 0xc8, 0xcc}
    while index < len(raw):
        demand(raw[index] == 0xff, 'invalid JPEG marker')
        while index < len(raw) and raw[index] == 0xff:
            index += 1
        demand(index < len(raw), 'truncated JPEG marker')
        marker = raw[index]
        index += 1
        demand(marker not in (0xda, 0xd9), 'JPEG frame absent before scan/end')
        demand(index+2 <= len(raw), 'truncated JPEG length')
        length = int.from_bytes(raw[index:index+2], 'big')
        demand(length >= 2 and index+length <= len(raw), 'invalid JPEG segment length')
        if marker in frames:
            demand(length >= 8, 'invalid JPEG frame')
            depth, height, width, channels = struct.unpack('>BHHB', raw[index+2:index+8])
            demand(depth == 8 and channels == 3, 'JPEG must be 8-bit three-channel')
            return width, height
        index += length
    raise ValueError('JPEG frame absent')


def required_inputs():
    required = {}
    for name in ('run01.json', 'run02.json'):
        add_pin(required, PARENT/name, PARENT_SHA)
    add_pin(required, PARENT/'independent-check.json', RECEIPT_SHA)
    prior = load(PARENT/'independent-check.json')
    demand(prior['inputs'] == prior['inputs_after'], 'parent receipt changed during its check')
    for name, expected in prior['inputs'].items():
        add_pin(required, BASE/name, expected)
    add_pin(required, BASE/'pypdf-representation01.json', REP_SHA)
    add_pin(required, PDF, PDF_SHA)
    representation = load(BASE/'pypdf-representation01.json')
    demand(representation['source_sha256'] == PDF_SHA, 'PDF representation source differs')
    invocations = representation['image_invocations']
    demand(len(invocations) == 12 and {r['name'] for r in invocations} == {f'Im{i}' for i in range(12)},
           'twelve source-strip invocations required')
    assets = {}
    for invocation in invocations:
        name = invocation['name']
        path = BASE/'native-strips01'/(name+'.jpg')
        key = add_pin(required, path, invocation['encoded_jpeg_sha256'])
        demand(required[key]['bytes'] == invocation['encoded_jpeg_bytes'], 'JPEG byte count differs')
        width, height = image_header(path)
        demand([width, height] == invocation['native_dimensions'], 'JPEG/CTM dimensions differ')
        assets[name] = {'path': key, **required[key], 'width': width, 'height': height,
                        'ctm': invocation['ctm'], 'url': '/source/'+name+'.jpg'}
    page = BASE/'render01/page-076.png'
    key = add_pin(required, page, PAGE_SHA)
    demand(image_header(page) == (1700, 2200), 'full-page dimensions differ')
    assets['page'] = {'path': key, **required[key], 'width': 1700, 'height': 2200, 'url': '/page.png'}
    for name in ('PROTOCOL.md', 'packet.py', 'test_packet.py'):
        add_pin(required, HERE/name, PROTOCOL_SHA if name == 'PROTOCOL.md' else None)
    return required, {r['name']: r for r in invocations}, assets


def verify(run1, run2, expected_sha):
    demand(type(expected_sha) is str and len(expected_sha) == 64, 'explicit frozen packet SHA required')
    paths = [Path(run1).resolve(), Path(run2).resolve()]
    demand(paths[0] != paths[1], 'two distinct packet files required')
    runs = {os.path.relpath(path, HERE): pin(path) for path in paths}
    demand(all(p['sha256'] == expected_sha for p in runs.values()) and paths[0].read_bytes() == paths[1].read_bytes(),
           'frozen packets differ')
    required, invocations, assets = required_inputs()
    actual = load(paths[0])
    demand(actual['inputs'] == actual['inputs_after'], 'packet before/after differs')
    require_closure(actual['inputs'], required)
    before = {}
    for name, expected in actual['inputs'].items():
        add_pin(before, BASE/name, expected)
    for path in paths:
        add_pin(before, path, expected_sha)
    for name in ('independent_check.py', 'test_independent_check.py', 'envelope_math.py', 'test_envelope_math.py'):
        add_pin(before, HERE/name)
    admission = load(PARENT/'run01.json')
    demand(admission['human_accepted'] is False and admission['actual_D'] is None and
           admission['model_discrepancies'] is None and len(admission['candidate_cells']) == 4779,
           'prior scope or acceptance changed')
    slots, inventory = reconstruct(admission, invocations)
    demand(len(slots) == 42 and sum(len(slot['entries']) for slot in slots) == 84, '42/84 roster differs')
    demand(actual['slots'] == canonical(slots), 'slot selection, alternatives, mapping, flags or pending states differ')
    demand(actual['inventory'] == canonical(inventory), 'primary bookkeeping inventory differs')
    demand(actual['assets'] == canonical(assets), 'source assets differ')
    demand(actual['source_pdf'] == {'path': os.path.relpath(PDF, BASE), 'sha256': PDF_SHA,
                                   'physical_page': 76, 'printed_page': 25}, 'PDF locator differs')
    demand(actual['status'] == 'conditional_mapping_packet_pending_human' and type(actual['version']) is int and
           actual['version'] == 1 and actual['domain_kind'] == 'C_H_primary_primary_not_actual_D', 'packet identity differs')
    demand(actual['parent_result'] == 'historical-applicability/admission-2026-10-08/run01.json' and
           actual['assumptions'] == ['Hidentity', 'Hsupport', 'Hink0'], 'prior reference or hypotheses changed')
    demand(actual['actual_D'] is None and actual['model_discrepancies'] is None and
           actual['original_actual_D_sampling_fulfilled'] is False and actual['human_accepted'] is False,
           'unpermitted result or acceptance')
    summary = dict(Counter(slot['selection_status'] for slot in slots))
    demand(actual['summary'] == summary, 'packet summary differs')
    omissions = []
    for name in required:
        damaged = dict(actual['inputs'])
        del damaged[name]
        try:
            require_closure(damaged, required)
        except ValueError:
            omissions.append(name)
        else:
            raise ValueError('missing input accepted: '+name)
    after = {name: pin(BASE/name) for name in before}
    demand(before == after, 'inputs changed during independent verification')
    entries = [entry for slot in slots for entry in slot['entries']]
    mappings = [m for entry in entries for role in ROLES for m in entry['mappings'][role]]
    return {'status': 'pass_conditional_packet_bookkeeping_only', 'packet_pins': runs,
        'coverage': {'pairs': 14, 'paired_slots': 42, 'model_entries': 84,
            'scenario_position_states': 168, 'model_reader_alternative_lists': 168,
            'native_coordinate_mappings': len(mappings), 'image_headers': 13,
            'displacement_hulls': sum(v is not None for slot in slots for v in slot['displacement_m'].values()),
            'duplicate_model_role_flags': sum(bool(entry['duplicate_entries'][role]) for entry in entries for role in ROLES),
            'duplicate_paired_slot_flags': sum(bool(slot['duplicate_paired_slots']) for slot in slots)},
        'selection_summary': summary, 'required_producer_pin_count': len(required),
        'producer_pin_count': len(actual['inputs']), 'required_pin_omission_checks': sorted(omissions),
        'inputs': before, 'inputs_after': after,
        'independence': 'No producer/helper imports. Original-segment cumulative selection, same-position scenario inspection, direct four-corner CTMs, endpoint interpolation inverse, pairwise duplicate comparison and native image-header parsing. Output schema/protocol inspected; not blind.',
        'limits': 'No source reannotation, independent pixel decoder, human responses, accepted support, historical discrepancy or original-curve enclosure verification. Prior candidate geometry is protected by frozen input, not reclassified in this unit. Arithmetic oracle tests are synthetic and separately reported.'}


def save_exclusive(path, value):
    with Path(path).open('xb') as stream:
        stream.write(encoded(value))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run1', type=Path, default=HERE/'packet01.json')
    parser.add_argument('--run2', type=Path, default=HERE/'packet02.json')
    parser.add_argument('--expected-sha', required=True)
    parser.add_argument('--save-receipt', action='store_true')
    args = parser.parse_args()
    try:
        receipt = verify(args.run1, args.run2, args.expected_sha)
        if args.save_receipt:
            target = HERE/'independent-check.json'
            save_exclusive(target, receipt)
            print(json.dumps({'status': receipt['status'], 'coverage': receipt['coverage'], 'pin': pin(target)}, sort_keys=True))
        else:
            print(json.dumps(receipt, sort_keys=True, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError, ZeroDivisionError, struct.error) as error:
        print(json.dumps({'status': 'fail', 'error_type': type(error).__name__, 'error': str(error)}, sort_keys=True))
        return 1


if __name__ == '__main__':
    sys.exit(main())
