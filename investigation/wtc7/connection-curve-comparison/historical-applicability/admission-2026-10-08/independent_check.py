"""Independent candidate-geometry audit; no producer imports or pixel reading.

The protocol and producer schema were inspected. New source-row decisions use
the separately implemented, hash-pinned earlier independent checker. Candidate
partitions use midpoint membership, not the producer's event sweep. Output is
conditional bookkeeping, not support, human acceptance or model discrepancy.
"""
import argparse
from collections import Counter
import copy
from fractions import Fraction as Q
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
OLD = 'historical-applicability/force56-extension-2026-10-08/'
NEW = 'native-footprint-pass/force6-im3/'
INDEPENDENT = 'historical-applicability/conditional-envelopes-2026-10-08/independent_check.py'
PROTOCOL_SHA = '166558c3c50e061a8854dd60ec2e2cac5ce05389f674be8e55cf793c1aabfc7d'
HELPER_SHA = '8f83a8b591de73aef342ecb6d01830cd012eb0593e43731236ba73f553ad69f0'
PAIRS = tuple(panel+str(n) for panel in ('F', 'E') for n in range(3, 10))
ROLES = ('primary', 'peer')
STATES = ('gap', 'solid_only', 'dash_only', 'overlapping_candidate_coverage',
          'shared_ink_ownership_conflict', 'paired_local_candidate')
FIXED = {
    OLD+'run-v2-01.json': '3b9e96e03a0daa37a0c30e8b9e4eb540b0b350a1b3ae832eeb3acc161815dd07',
    OLD+'run-v2-02.json': '3b9e96e03a0daa37a0c30e8b9e4eb540b0b350a1b3ae832eeb3acc161815dd07',
    OLD+'independent-check.json': '89b2948f2233fe0ae1883245fbe5166a84de586d707b510ae195578b8216081b',
    NEW+'independent-check.json': '22491e6a1e4459941dff884dab4b8d54e389c3731847c5fd1ae8849ca4d8b591',
    NEW+'reader-primary.json': 'd53723cc3d1b86bdbaf5cbed2dec5690e18ddf67efad2dae323bc7905690a3e9',
    NEW+'reader-peer.json': 'ab84ccc41a395414982489c8ef4e9d874908a4e79c6b08a84a6d3c651ba32f42',
    NEW+'compare.py': '63dae6eb1e69ac974f4a065650440ac13f5fbb5f4cbfdd41b7bddad8f2076ce7',
    'historical-applicability/conditional-envelopes-2026-10-08/calculate.py':
        '9d3f00efca8cb858b80a2b34c11f8253d2de59c66b46257df9dfc715d73ee89a',
    'historical-applicability/approach34-extension-2026-10-08/extend.py':
        '18f5862d014c5e9848cd6332da3929437c7ff93031e3ca255730d1f9e0dfc3f0',
    'pypdf-representation01.json': '1cbb52b2e12a3d2b13d1a2ac008aab091bf64dc57deaf5b646fd6098521992e5',
}


def demand(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    demand(type(value) in (int, str, Q), 'exact rational required')
    return Q(value)


def normalize(value):
    if type(value) is Q:
        return str(value)
    if type(value) is dict:
        return {key: normalize(item) for key, item in value.items()}
    if type(value) in (list, tuple):
        return [normalize(item) for item in value]
    return value


def encoded(value):
    return (json.dumps(normalize(value), sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()


def pin(path):
    raw = Path(path).read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def load(path):
    return json.loads(Path(path).read_text(), parse_float=Q)


def require_pin_shape(value):
    demand(type(value) is dict and set(value) == {'bytes', 'sha256'}, 'invalid pin fields')
    demand(type(value['bytes']) is int and value['bytes'] >= 0, 'invalid pin byte count')
    digest = value['sha256']
    demand(type(digest) is str and len(digest) == 64 and
           all(c in '0123456789abcdef' for c in digest), 'invalid pin digest')


def add_pin(result, path, expected=None):
    path = Path(path).resolve()
    key = os.path.relpath(path, BASE)
    observed = pin(path)
    if type(expected) is str:
        demand(observed['sha256'] == expected, 'changed fixed input: '+key)
    elif expected is not None:
        require_pin_shape(expected)
        demand(observed == expected, 'changed pinned input: '+key)
    demand(key not in result or result[key] == observed, 'conflicting normalized pin: '+key)
    result[key] = observed
    return key


def include_map(result, mapping, owner):
    demand(type(mapping) is dict, 'pin map required')
    for key, expected in mapping.items():
        demand(type(key) is str and key, 'invalid pin path')
        add_pin(result, Path(owner)/key, expected)


def check_required_pins(found, required):
    demand(type(found) is dict, 'producer pin map required')
    for key, expected in required.items():
        demand(key in found and found[key] == expected, 'required pin omitted or changed: '+key)
    for value in found.values():
        require_pin_shape(value)


def prior_helper():
    demand(pin(BASE/INDEPENDENT)['sha256'] == HELPER_SHA, 'independent helper changed')
    spec = importlib.util.spec_from_file_location('admission_prior_independent', BASE/INDEPENDENT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_source(original):
    """Declare the new list-membership spelling without a producer adapter."""
    source = copy.deepcopy(original)
    demand(set(source['routes']) == {'solid', 'dash'}, 'new source route roster')
    for route in ('solid', 'dash'):
        for row in source['routes'][route]:
            demand(not set(row) & {'column', 'core_rows', 'fringe_rows', 'fragments', 'band_refs'},
                   'ambiguous new source aliases')
            members = row.pop('fragment_membership')
            demand(type(members) is list, 'new source membership must be a list')
            row['fragments'] = members
            seen = set()
            for member in members:
                selected = set(member['core']) | set(member['fringe'])
                demand(not seen & selected, 'overlapping fragment members')
                seen |= selected
    return source


def bounds_by_vertices(length, axes):
    size = rational(length)
    demand(size >= 0, 'negative candidate length')
    left, right = ([rational(x) for x in axes[key]] for key in ('L', 'R'))
    demand(len(left) == len(right) == 2 and left[0] <= left[1] and right[0] <= right[1],
           'invalid endpoint intervals')
    results = []
    for a, b in itertools.product(left, right):
        demand(b > a, 'nonpositive shared-axis span')
        results.append(Q(8, 5)*size/(b-a))
    return [min(results), max(results)]


def cells_valid(cells):
    ids = set()
    for cell in cells:
        demand(type(cell['id']) is str and cell['id'] and cell['id'] not in ids, 'duplicate/invalid candidate ID')
        ids.add(cell['id'])
        demand(cell['route'] in ('solid', 'dash'), 'unknown candidate route')
        demand(len(cell['render_x']) == 2 and rational(cell['render_x'][0]) < rational(cell['render_x'][1]),
               'empty/reversed source-x interval')
        rectangle = cell['native_rectangle']
        demand(type(rectangle) is list and len(rectangle) == 4 and
               all(type(n) is int for n in rectangle) and
               rectangle[0] < rectangle[2] and rectangle[1] < rectangle[3], 'invalid native rectangle')
        demand(type(cell['source']) is str and cell['source'], 'missing source')
        demand(type(cell['body']) is list and len(cell['body']) == 3 and
               all(type(n) is str and n for n in cell['body']), 'invalid body provenance')


def native_intersection(first, second):
    if first['source'] != second['source']:
        return False
    a, b = first['native_rectangle'], second['native_rectangle']
    # Literal native cells; selected rectangles are contiguous by prior screening.
    return bool(set(range(a[0], a[2])) & set(range(b[0], b[2]))) and \
           bool(set(range(a[1], a[3])) & set(range(b[1], b[3])))


def midpoint_partition(cells):
    """Enumerate membership independently on every exact elementary interval."""
    cells_valid(cells)
    ids = {cell['id']: cell for cell in cells}
    edges = sorted({rational(x) for cell in cells for x in cell['render_x']})
    pieces = []
    for lo, hi in zip(edges, edges[1:]):
        midpoint = (lo+hi)/2
        active = {route: sorted(cell['id'] for cell in cells if cell['route'] == route and
                               rational(cell['render_x'][0]) < midpoint < rational(cell['render_x'][1]))
                  for route in ('solid', 'dash')}
        s, d = active['solid'], active['dash']
        shared = [[a, b] for a in s for b in d if native_intersection(ids[a], ids[b])]
        overlap = [route for route in ('solid', 'dash') if len(active[route]) > 1]
        # Protocol priority preserves one-style-only with a separate overlap flag.
        if not s and not d:
            status = 'gap'
        elif not s:
            status = 'dash_only'
        elif not d:
            status = 'solid_only'
        elif overlap:
            status = 'overlapping_candidate_coverage'
        elif shared:
            status = 'shared_ink_ownership_conflict'
        else:
            status = 'paired_local_candidate'
        pieces.append({'render_x': [lo, hi], 'solid_refs': s, 'dash_refs': d,
                       'shared_ink_conflicts': shared, 'status': status, 'overlapping_routes': overlap})
    groups = []
    start = 0
    while start < len(pieces):
        piece = pieces[start]
        if piece['status'] != 'paired_local_candidate':
            start += 1
            continue
        identity = [ids[piece[route+'_refs'][0]]['body'] for route in ('solid', 'dash')]
        stop = start+1
        while stop < len(pieces):
            nxt = pieces[stop]
            if nxt['status'] != 'paired_local_candidate' or nxt['render_x'][0] != pieces[stop-1]['render_x'][1]:
                break
            if [ids[nxt[route+'_refs'][0]]['body'] for route in ('solid', 'dash')] != identity:
                break
            stop += 1
        groups.append({'render_x': [piece['render_x'][0], pieces[stop-1]['render_x'][1]],
                       'body_pair': identity, 'segment_indices': list(range(start, stop))})
        start = stop
    totals = dict.fromkeys(STATES, Q(0))
    own = {'solid': Q(0), 'dash': Q(0)}
    common = Q(0)
    for piece in pieces:
        width = piece['render_x'][1]-piece['render_x'][0]
        totals[piece['status']] += width
        for route in own:
            if piece[route+'_refs']:
                own[route] += width
        if piece['solid_refs'] and piece['dash_refs']:
            common += width
    return {'segments': pieces, 'paired_runs': groups, 'render_lengths': totals,
            'own_candidate_render_lengths': own, 'any_paired_render_length': common,
            'paired_segment_count': sum(piece['status'] == 'paired_local_candidate' for piece in pieces)}


def expected_cells(readings, roles, regions):
    result = []
    for reading in readings:
        path = reading['reader_path']
        demand(path in regions and path in roles, 'reading not in frozen roster')
        region = regions[path]
        demand((reading['pair'], reading['source']) == (region['pair'], region['source']), 'reading region mismatch')
        for row in reading['rows']:
            demand(type(row['conditional_window']) is bool and row['curve_support_established'] is False,
                   'source acceptance/status changed')
            if row['conditional_window']:
                demand(row['reasons'] == [] and row['fragment_id'], 'conditional row with missing identity or exclusions')
                rect = row['render_rectangle']
                demand(len(rect) == 4 and rational(rect[0]) < rational(rect[2]) and
                       rational(rect[1]) < rational(rect[3]), 'invalid candidate rectangle')
                result.append({'id': path+':'+row['route']+':'+str(row['column']),
                    'pair': reading['pair'], 'role': roles[path], 'reader_path': path,
                    'source': reading['source'], 'target_box': region['target_box'],
                    'route': row['route'], 'column': row['column'], 'fragment_id': row['fragment_id'],
                    'native_rectangle': row['native_rectangle'], 'render_rectangle': rect,
                    'render_x': [rational(rect[0]), rational(rect[2])],
                    'body': [path, reading['source'], row['fragment_id']]})
    cells_valid(result)
    return result


def acceptance_guards(actual):
    demand(actual['status'] == 'conditional_candidate_geometry_not_admitted_support' and
           type(actual['version']) is int and actual['version'] == 1, 'incorrect version/status')
    demand(actual['human_accepted'] is False and actual['shared_axis_parameters'] is True,
           'acceptance or axis correlation changed')
    demand(actual['assumptions'] == ['Hidentity', 'Hsupport', 'Hink0'], 'assumptions changed')
    demand(all(actual[key] is None for key in ('actual_D', 'quantile_targets', 'model_discrepancies')),
           'unpermitted support/sample/discrepancy result')


def scenario_check(actual, chosen, pair, solid_role, dash_role, axes):
    expected = midpoint_partition(chosen)
    expected.update(solid_reader=solid_role, dash_reader=dash_role,
        conditional_candidate_length_m={key: bounds_by_vertices(expected['render_lengths']['paired_local_candidate'], box)
            for key, box in axes.items() if key.startswith(pair[0]+'-')},
        actual_D=None, candidate_set='C_H', human_accepted=False)
    demand(actual == normalize(expected), 'candidate partition/provenance/length mismatch: '+pair+'/'+solid_role+'/'+dash_role)
    return expected


def required_closure(old, old_receipt, new_receipt):
    required = {}
    for key, digest in FIXED.items():
        add_pin(required, BASE/key, digest)
    demand(old['inputs'] == old['inputs_after'] and len(old['inputs']) == 173, 'old 173-input closure changed')
    demand(old_receipt['required_total_pin_count'] == 173 and
           old_receipt['required_input_map_sha256'] == hashlib.sha256(
               json.dumps(old['inputs'], sort_keys=True, allow_nan=False).encode()).hexdigest(),
           'old receipt input-map summary differs')
    include_map(required, old['inputs'], BASE)
    include_map(required, old_receipt['fixed_reference_pins'], BASE)
    include_map(required, old_receipt['run_pins'], BASE/OLD)
    add_pin(required, BASE/OLD/'independent_check.py', old_receipt['checker_pin'])
    demand(new_receipt['inputs'] == new_receipt['inputs_after'] and len(new_receipt['inputs']) == 55,
           'new 55-input receipt closure differs')
    include_map(required, new_receipt['inputs'], BASE/NEW)
    for key in ('NUMERICAL-PROTOCOL.md', 'HUMAN-SAMPLE-SELECTION.md', 'HUMAN-REVIEW-GATE.md',
                NEW+'report.md', NEW+'reader-primary-notes.md', NEW+'reader-peer-notes.md'):
        add_pin(required, BASE/key)
    for key in ('PROTOCOL.md', 'assess.py', 'test_assess.py'):
        add_pin(required, HERE/key, PROTOCOL_SHA if key == 'PROTOCOL.md' else None)
    return required


def verify(run1, run2, expected_sha):
    demand(type(expected_sha) is str and len(expected_sha) == 64, 'explicit frozen output SHA required')
    runs = [Path(run1).resolve(), Path(run2).resolve()]
    demand(runs[0] != runs[1], 'two distinct result paths required')
    run_pins = {os.path.relpath(path, HERE): pin(path) for path in runs}
    demand(all(item['sha256'] == expected_sha for item in run_pins.values()) and
           runs[0].read_bytes() == runs[1].read_bytes(), 'frozen runs differ')
    actual = load(runs[0])
    old = load(BASE/(OLD+'run-v2-01.json'))
    old_receipt = load(BASE/(OLD+'independent-check.json'))
    new_receipt = load(BASE/(NEW+'independent-check.json'))
    required = required_closure(old, old_receipt, new_receipt)
    demand(actual['inputs'] == actual['inputs_after'], 'producer before/after map differs')
    check_required_pins(actual['inputs'], required)
    before = {}
    include_map(before, actual['inputs'], BASE)
    for path in runs:
        add_pin(before, path, expected_sha)
    add_pin(before, BASE/INDEPENDENT, HELPER_SHA)
    for key in ('independent_check.py', 'test_independent_check.py'):
        add_pin(before, HERE/key)
    helper = prior_helper()
    acceptance_guards(actual)
    demand(tuple(p['pair'] for p in old['inventory']['pairs']) == PAIRS and len(old['readings']) == 42 and
           sum(len(r['rows']) for r in old['readings']) == old['records'] == 13240, 'old scope differs')
    demand(actual['prior_conditional_result'] == OLD+'run-v2-01.json' and
           actual['old_reading_objects_unchanged'] is True and actual['old_reading_count'] == 42 and
           actual['old_record_count'] == 13240 and actual['all_record_count'] == 14420, 'old reference/count mismatch')
    roles, regions = {}, {}
    for pair in old['inventory']['pairs']:
        for region in pair['completed_footprints']:
            demand(len(region['readers']) == 2, 'old role-pair count')
            for index, reader in enumerate(region['readers']):
                path = reader['path']
                demand(path not in roles, 'duplicated prior reader')
                roles[path] = ROLES[index]
                regions[path] = {'pair': pair['pair'], 'source': region['source'], 'target_box': region['target_box']}
    demand(set(roles) == {r['reader_path'] for r in old['readings']}, 'prior reading roster differs')
    representation = load(BASE/'pypdf-representation01.json')
    invocations = representation['image_invocations']
    demand(len(invocations) == 12 and len({v['name'] for v in invocations}) == 12, 'strip CTM roster differs')
    invocation = next(v for v in invocations if v['name'] == 'Im3')
    demand(invocation['native_dimensions'] == [741, 88], 'new native dimensions differ')
    new_readings, originals = [], {}
    counts = Counter()
    for role in ROLES:
        path = NEW+'reader-'+role+'.json'
        source = load(BASE/path)
        snapshot = encoded(source)
        demand(source['pair'] == 'F6' and source['source'] == 'Im3.jpg' and source['reader'] == role and
               source['target_box'] == [145, 0, 440, 88], 'new source identity differs')
        region = {'pair': 'F6', 'source': 'Im3', 'target_box': [145, 0, 440, 88]}
        rows = helper.expected_rows(copy_source(source), region, 'F', invocation)
        demand(len(rows) == 590 and encoded(source) == snapshot, 'new source coverage or preservation differs')
        counts['new_route_decisions'] += len(rows)
        counts['new_rectangle_conversions'] += sum(row['native_rectangle'] is not None for row in rows)
        counts['new_conditional_windows'] += sum(row['conditional_window'] for row in rows)
        counts['new_axis_hulls'] += sum(len(row['physical_windows'] or []) for row in rows)
        new_readings.append({'pair': 'F6', 'source': 'Im3', 'reader_path': path, 'rows': rows,
            'summary': {'records': len(rows), 'conditional_windows': sum(row['conditional_window'] for row in rows),
                        'reasons_nonexclusive': dict(Counter(reason for row in rows for reason in row['reasons']))}})
        originals[path] = source
        roles[path], regions[path] = role, region
    demand(actual['new_readings'] == normalize(new_readings), 'new decisions/mappings/summaries differ')
    demand(actual['new_source_originals'] == originals, 'new original objects changed')
    demand(actual['roles'] == roles and actual['regions'] == regions, 'role/region roster differs')
    axes = {panel+'-'+reader: helper.axis_intervals(panel, reader)
            for panel in ('F', 'E') for reader in ('root', 'independent')}
    demand(actual['axis_boxes'] == old['axis_boxes'] == normalize(axes), 'fixed shared-axis boxes differ')
    cells = expected_cells(old['readings']+normalize(new_readings), roles, regions)
    demand(actual['candidate_cells'] == normalize(cells), 'candidate cells or provenance differ')
    demand(tuple(pair['pair'] for pair in actual['pairs']) == PAIRS, 'all fourteen pairs/order required')
    pair_coverage = {}
    for pair in actual['pairs']:
        name = pair['pair']
        demand(set(pair) == {'pair', 'scenarios'} and len(pair['scenarios']) == 4, 'four scenarios required')
        pair_coverage[name] = []
        for index, (solid, dash) in enumerate(itertools.product(ROLES, repeat=2)):
            chosen = [c for c in cells if c['pair'] == name and
                      ((c['route'] == 'solid' and c['role'] == solid) or
                       (c['route'] == 'dash' and c['role'] == dash))]
            checked = scenario_check(pair['scenarios'][index], chosen, name, solid, dash, axes)
            counts['scenarios'] += 1
            counts['elementary_segments'] += len(checked['segments'])
            counts['paired_runs'] += len(checked['paired_runs'])
            counts['conditional_length_extrema'] += 4
            pair_coverage[name].append({'solid_reader': solid, 'dash_reader': dash,
                'candidate_cells': len(chosen), 'segments': len(checked['segments']),
                'paired_segments': checked['paired_segment_count'], 'paired_runs': len(checked['paired_runs'])})
    counts.update(candidate_cells=len(cells), pairs=14, old_readings_by_frozen_reference=42,
                  old_records_by_frozen_reference=13240, new_readings=2)
    demand(counts['new_route_decisions'] == 1180 and counts['scenarios'] == 56, 'historical verification scope differs')
    omission_controls = []
    for key in required:
        altered = dict(actual['inputs'])
        del altered[key]
        try:
            check_required_pins(altered, required)
        except ValueError:
            omission_controls.append(key)
        else:
            raise ValueError('missing required pin accepted: '+key)
    after = {name: pin(BASE/name) for name in before}
    demand(before == after, 'inputs changed during independent check')
    return {'status': 'pass_conditional_candidate_geometry_only',
        'coverage': dict(counts), 'pairs': pair_coverage,
        'producer_run_pins': run_pins, 'required_producer_pin_count': len(required),
        'producer_pin_count': len(actual['inputs']), 'inputs': before, 'inputs_after': after,
        'required_pin_omission_checks': sorted(omission_controls),
        'old_closure_count': 173, 'new_source_receipt_closure_count': 55,
        'independence': 'Pinned prior independent raw-row/CTM checker only; no assess, producer calculator, adapter, classifier, partition or length imports. Midpoint-active partition and vertex length extrema separately implemented; schema and protocol inspected.',
        'limits': 'All new decisions and all candidate geometry checked. Old 42 reading objects preserved by frozen reference, not independently recalculated here. No pixel rereading, semantic ownership verification, established support, quantile, model discrepancy, human acceptance or physical/causal inference.'}


def save_exclusive(path, value):
    with Path(path).open('xb') as stream:
        stream.write(encoded(value))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run1', type=Path, default=HERE/'run01.json')
    parser.add_argument('--run2', type=Path, default=HERE/'run02.json')
    parser.add_argument('--expected-sha', required=True)
    parser.add_argument('--save-receipt', action='store_true')
    args = parser.parse_args()
    try:
        receipt = verify(args.run1, args.run2, args.expected_sha)
        if args.save_receipt:
            target = HERE/'independent-check.json'
            save_exclusive(target, receipt)
            print(json.dumps({'status': receipt['status'], 'receipt_pin': pin(target),
                              'coverage': receipt['coverage']}, sort_keys=True))
        else:
            print(json.dumps(receipt, sort_keys=True, indent=2))
        return 0
    except (KeyError, TypeError, ValueError, OSError, ZeroDivisionError) as error:
        print(json.dumps({'status': 'fail', 'error_type': type(error).__name__, 'error': str(error)}, sort_keys=True))
        return 1


if __name__ == '__main__':
    sys.exit(main())
