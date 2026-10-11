"""Independent finite F7 eligibility, bookkeeping and geometry audit.

Imports only three hash-pinned prior INDEPENDENT checkers, never producer,
annotation, calculator, compatibility adapter or event-sweep implementations.
Schema and protocol were inspected; this is neither blind source reading nor
independent authorship from this agent's earlier midpoint/conditional checker.
"""
import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction as Q
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
OLD = BASE / 'historical-applicability/admission-2026-10-08'
REGION = 'F7-Im2-early'
TARGET = [220, 0, 330, 88]
CONTEXT = [218, 0, 332, 88]
ROLES = ('primary', 'peer')
HELPERS = {
    'geometry': ('../../historical-applicability/admission-2026-10-08/independent_check.py',
                 'a1e573d47ba05948e4db7ba637380267d732dd6fa4d180f491375175ebe9871d'),
    'rows': ('../../historical-applicability/conditional-envelopes-2026-10-08/independent_check.py',
             '8f83a8b591de73aef342ecb6d01830cd012eb0593e43731236ba73f553ad69f0'),
    'bookkeeping': ('../force6-im3/independent_check.py',
                    'd0eb3c11e38c135a51e6012d1ab549287ee9a9c245cd186cf8478e3eb5a2571b'),
}
METHOD_PINS = {
    '../../historical-applicability/admission-2026-10-08/assess.py': 'bf0ad1c87374adda3e2751461b33aec678b780f438b74d32ac75767f8f5de1e4',
    '../../historical-applicability/conditional-envelopes-2026-10-08/calculate.py': '9d3f00efca8cb858b80a2b34c11f8253d2de59c66b46257df9dfc715d73ee89a',
    '../../historical-applicability/approach34-extension-2026-10-08/extend.py': '18f5862d014c5e9848cd6332da3929437c7ff93031e3ca255730d1f9e0dfc3f0',
    '../force56-remainder/compare.py': '81dc892b21e891a9c11d2bc7697d1b936a497a91950584659e04fc718776313a',
    '../force45/compare_force45.py': '932792f49797c4034beb1124d8174a56c911319e17fa536e199f0709950557be',
    '../force69/compare_force69.py': 'f332359911f4d7bf5e768bf9e36b37ddb6995e857f6cf7ae5fa5456bb6dd4a6e',
    '../approach34/compare.py': 'cb4a2da60959a4b0a40ddb4a072c1cbedf4624da63daf1a50b37db0eb2dd5bac',
}
FIXED = {
    'PROTOCOL.md': 'aae8d37e8f0cda59f4c226e05c386f0dd73ace7b6954c7cd7ea81142f252ab19',
    'READERS.md': 'd62c0390fbb19bc507cb49a8da3d04802f1ad39e39784eb88ae27cc909424417',
    'context01.json': 'ff9f1f0e47b443994c6ba5325a1f2347c2522f48f2a79012b3c6d285bcb6874f',
    'context02.json': 'ff9f1f0e47b443994c6ba5325a1f2347c2522f48f2a79012b3c6d285bcb6874f',
    '../../historical-applicability/admission-2026-10-08/run01.json': '4aeca445bc71d4495dd578df6a4de96e3bf2d54004b6afb0b1efcf7bb631930e',
    '../../historical-applicability/admission-2026-10-08/run02.json': '4aeca445bc71d4495dd578df6a4de96e3bf2d54004b6afb0b1efcf7bb631930e',
    '../../historical-applicability/admission-2026-10-08/independent-check.json': '9d05f112c632af128ae2d37f18a0fcab0ebabb78cc76f0d5bc453493feb88afd',
    '../../historical-applicability/envelope-packet-2026-10-08/packet01.json': 'cb0f9da2f36e384eeeb046528696bba4f379fc8419f393a18ae2f809b05829cc',
    '../../pypdf-representation01.json': '1cbb52b2e12a3d2b13d1a2ac008aab091bf64dc57deaf5b646fd6098521992e5',
}
CONTEXT_RECEIPT_SHA = '85445cc886a9e4e1bf9d6019d454a5b7c8450d56b182b84124fa16af411d70ad'
COMPATIBILITY_SHA = '30dfd6b79e89358050fd9b60bc4e9a09bc302ba66aeb9bd8472ee9791180c12c'
OUTPUT_FIELDS = {'status', 'region_id', 'target_box', 'context_box', 'inputs', 'inputs_after',
    'originals', 'validation_alias', 'reader_comparison', 'reader_difference_summary',
    'selected_exact_white', 'new_readings', 'new_candidate_cells', 'preserved_old_F7_candidate_cells',
    'before_scenarios', 'after_scenarios', 'axis_boxes', 'unchanged_other_pairs_reference',
    'actual_D', 'human_accepted', 'model_discrepancies', 'assumptions', 'limits'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def normalized(value):
    if type(value) is Q:
        return str(value)
    if type(value) is dict:
        return {k: normalized(v) for k, v in value.items()}
    if type(value) in (list, tuple):
        return [normalized(v) for v in value]
    return value


def encoded(value):
    return (json.dumps(normalized(value), sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()


def exact(a, b):
    return encoded(a) == encoded(b)


def load(path):
    return json.loads(Path(path).read_text(), parse_float=Q)


def pin(path):
    raw = Path(path).read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def pin_shape(value):
    require(type(value) is dict and set(value) == {'bytes', 'sha256'} and
            type(value['bytes']) is int and value['bytes'] >= 0, 'pin shape/byte count')
    digest = value['sha256']
    require(type(digest) is str and len(digest) == 64 and all(c in '0123456789abcdef' for c in digest), 'pin digest')


def add_pin(pins, path, expected=None):
    path = Path(path).resolve()
    name = os.path.relpath(path, HERE)
    observed = pin(path)
    if type(expected) is str:
        require(observed['sha256'] == expected, 'changed fixed input '+name)
    elif expected is not None:
        pin_shape(expected)
        require(observed == expected, 'changed input '+name)
    require(name not in pins or pins[name] == observed, 'conflicting alias '+name)
    pins[name] = observed
    return name


def include_map(pins, declared, owner):
    require(type(declared) is dict, 'input map required')
    for name, expected in declared.items():
        require(type(name) is str and name, 'input path string')
        add_pin(pins, Path(owner)/name, expected)


def closure(pins, roots):
    pending = [Path(path).resolve() for path in roots]
    visited = set()
    while pending:
        path = pending.pop()
        add_pin(pins, path)
        if path in visited or path.suffix != '.json':
            continue
        visited.add(path)
        data = load(path)
        if 'inputs_after' in data:
            require(exact(data['inputs'], data['inputs_after']), 'nested before/after mismatch')
        if 'inputs' in data:
            include_map(pins, data['inputs'], path.parent)
            pending.extend((path.parent/name).resolve() for name in data['inputs'])
        if path.name.startswith('reader-') and 'script_pin' in data:
            add_pin(pins, path.with_suffix('.py'), data['script_pin'])


def require_map(found, required):
    require(type(found) is dict, 'required producer map')
    for name, value in required.items():
        require(name in found and exact(found[name], value), 'required pin omitted or changed '+name)
    for value in found.values():
        pin_shape(value)


def helper(name):
    path, sha = HELPERS[name]
    require(pin(HERE/path)['sha256'] == sha, 'independent helper changed '+name)
    spec = importlib.util.spec_from_file_location('f7_independent_'+name, HERE/path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def annotation(data, role, book, attest=True):
    require(role in ROLES and data['reader'] == role and data['region_id'] == REGION and
            data['pair'] == 'F7' and data['source'] == 'Im2.jpg', 'exact original identity')
    for key, value in (('target_box', TARGET), ('context_box', CONTEXT)):
        require(type(data[key]) is list and all(type(n) is int for n in data[key]) and data[key] == value, 'original '+key)
    require(data['human_accepted'] is False and data['physical_support'] is None, 'source acceptance')
    require(set(data['routes']) == {'solid', 'dash'}, 'both source routes')
    if attest:
        cv = data['coverage']
        require(cv['full_context_inspected'] is True and cv['uncompleted_context'] == [], 'incomplete attestation')
        require(type(cv['raw_context_cells']) is int and cv['raw_context_cells'] == 10032, 'context count attestation')
        require(type(cv['rows']) is list and all(type(n) is int for n in cv['rows']) and cv['rows'] == [0, 87], 'row attestation')
        require(type(cv['prior_knowledge']) is str and cv['prior_knowledge'].strip(), 'prior disclosure')
        for flag in ('counterpart_new_annotations_read', 'counterpart_new_annotation_read'):
            require(cv.get(flag, False) is False, 'counterpart exposure declared')
        columns = []
        require(type(cv['raw_blocks']) is list, 'raw blocks')
        for block in cv['raw_blocks']:
            a, b = block['columns']
            require(type(a) is int and type(b) is int and a <= b and
                    type(block['receipt']) is str and block['receipt'].strip() and
                    block.get('truncated', False) is False, 'block attestation')
            columns.extend(range(a, b+1))
        require(columns == list(range(218, 332)), 'exact-once context columns')
        views = cv['actual_views']
        require(type(views) is list and bool(views), 'view list')
        paths = set()
        for view in views:
            require(type(view) is dict and type(view.get('path')) is str and view['path'].strip() and
                    type(view.get('receipt')) is str and view['receipt'].strip(), 'view path/receipt')
            paths.add((HERE/view['path']).resolve())
        require({(BASE/'native-strips01/Im2.jpg').resolve(), (BASE/'render01/page-076.png').resolve()} <= paths, 'source/page view records')
    occupied, bands, by_column = defaultdict(int), {}, defaultdict(list)
    require(type(data['unassigned_bands']) is list, 'band list')
    for band in data['unassigned_bands']:
        c, f = book.validate_entry(band, TARGET, band=True)
        key = band['x'], band['band_id']
        require(type(key[1]) is str and key[1].strip() and key not in bands, 'unique band identity')
        candidates = band['candidate_routes']
        require(type(candidates) is list and len(candidates) == len(set(candidates)) and
                all(route in ('solid', 'dash') for route in candidates), 'band candidate routes')
        require(bool(c | f) == bool(candidates), 'band material/candidates')
        require(band['status'] != 'identity_conflict' or bool(c | f), 'empty conflict band')
        require(not occupied[key[0]] & (c | f), 'duplicate band ink')
        occupied[key[0]] |= c | f
        bands[key] = band
        by_column[key[0]].append(band)
    routes = {}
    for route in ('solid', 'dash'):
        records = data['routes'][route]
        require(type(records) is list and [r['x'] for r in records] == list(range(220, 330)), 'ordered route coverage')
        for row in records:
            c, f = book.validate_entry(row, TARGET)
            require(not occupied[row['x']] & (c | f), 'duplicate route/band ink')
            occupied[row['x']] |= c | f
            routes[route, row['x']] = row
            refs = row['unassigned_band_refs']
            for ref in refs:
                require((row['x'], ref) in bands and route in bands[row['x'], ref]['candidate_routes'], 'real route-specific reference')
            require(row['status'] != 'identity_conflict' or bool(refs), 'conflict without reference')
            require(bool(c | f) or not refs or row['status'] == 'identity_conflict', 'empty conflict status')
    for (x, name), band in bands.items():
        require(all(name in routes[route, x]['unassigned_band_refs'] for route in band['candidate_routes']), 'reciprocal band reference')
    return by_column


def comparisons(readers, book):
    routes = [{'route': route, 'x': a['x'], 'primary': a, 'peer': b, 'sets': book.compare_classes(a, b)}
              for route in ('solid', 'dash')
              for a, b in zip(readers['primary']['routes'][route], readers['peer']['routes'][route])]
    ink = []
    for index, x in enumerate(range(220, 330)):
        chosen = []
        for role in ROLES:
            data = readers[role]
            entries = [data['routes'][route][index] for route in ('solid', 'dash')]
            entries += [band for band in data['unassigned_bands'] if band['x'] == x]
            chosen.append(book.visible(entries))
        ink.append({'x': x, 'sets': book.compare_classes(*chosen)})
    return {'route_records': routes, 'all_ink_columns': ink}, {
        'routes': book.totals(routes), 'all_ink': book.totals(ink),
        'status_different': sum(row['primary']['status'] != row['peer']['status'] for row in routes)}


def required_inputs(prior, old_receipt, readers):
    result = {}
    for name, sha in {**FIXED, **METHOD_PINS}.items():
        add_pin(result, HERE/name, sha)
    add_pin(result, HERE/'CONSUMER-COMPATIBILITY.md', COMPATIBILITY_SHA)
    for name in ('assess.py', 'test_assess.py'):
        add_pin(result, HERE/name)
    require(prior['inputs'] == prior['inputs_after'] and len(prior['inputs']) == 205, 'old 205-input closure')
    include_map(result, prior['inputs'], BASE)
    require(old_receipt['inputs'] == old_receipt['inputs_after'] and len(old_receipt['inputs']) == 209,
            'old independent 209-input closure')
    require(old_receipt['required_producer_pin_count'] == 205 and old_receipt['producer_pin_count'] == 205,
            'old receipt producer scope')
    include_map(result, old_receipt['inputs'], BASE)
    include_map(result, old_receipt['producer_run_pins'], OLD)
    context = load(HERE/'context01.json')
    require(len(context['inputs']) == 9, 'context nine-input map')
    closure(result, [HERE/'context01.json', HERE/'context02.json'])
    for role, data in readers.items():
        required_reader = {name: pin(HERE/name) for name in ('PROTOCOL.md', 'READERS.md', 'context01.json', 'context02.json')}
        required_reader.update(context['inputs'])
        require_map(data['inputs'], required_reader)
        closure(result, [HERE/f'reader-{role}.json'])
    return result


def acceptance(output):
    require(set(output) == OUTPUT_FIELDS, 'result field scope')
    require(output['status'] == 'conditional_F7_coverage_followup_not_admitted_support' and
            output['region_id'] == REGION and exact(output['target_box'], TARGET) and
            exact(output['context_box'], CONTEXT), 'result identity/status')
    require(output['human_accepted'] is False and output['actual_D'] is None and
            output['model_discrepancies'] is None and output['assumptions'] == ['Hidentity', 'Hsupport', 'Hink0'], 'conditional boundary')
    require(output['validation_alias'] == {'preserved': REGION, 'copy_only': 'F7-Im2',
        'purpose': 'Unchanged old validator two-token region parser; no source/target/role change'}, 'validation alias scope')


def verify(run1, run2, expected_sha, reader_shas):
    require(set(reader_shas) == set(ROLES), 'two explicit frozen reader hashes')
    run1, run2 = Path(run1).resolve(), Path(run2).resolve()
    require(run1 != run2 and run1.read_bytes() == run2.read_bytes(), 'distinct identical output copies')
    require(pin(run1)['sha256'] == expected_sha, 'frozen result hash')
    actual, prior, old_receipt = load(run1), load(OLD/'run01.json'), load(OLD/'independent-check.json')
    acceptance(actual)
    readers = {}
    before = {}
    for role in ROLES:
        path = HERE/f'reader-{role}.json'
        add_pin(before, path, reader_shas[role])
        readers[role] = load(path)
    required = required_inputs(prior, old_receipt, readers)
    require(actual['inputs'] == actual['inputs_after'], 'current producer before/after')
    require_map(actual['inputs'], required)
    include_map(before, actual['inputs'], HERE)
    for path in (run1, run2):
        add_pin(before, path, expected_sha)
    for path, sha in HELPERS.values():
        add_pin(before, HERE/path, sha)
    for name in ('independent_check.py', 'test_independent_check.py'):
        add_pin(before, HERE/name)
    add_pin(before, HERE/'context-check.json', CONTEXT_RECEIPT_SHA)
    context_receipt = load(HERE/'context-check.json')
    require(context_receipt['pins_before'] == context_receipt['pins_after'] and
            context_receipt['distinct_cells'] == 10032 and context_receipt['source_records_checked'] == 20064,
            'context receipt scope/pins')
    include_map(before, context_receipt['pins_before'], HERE)
    require((HERE/'context01.json').read_bytes() == (HERE/'context02.json').read_bytes(), 'context copies')
    context = load(HERE/'context01.json')
    pixels = {(r['x'], r['y']): r['rgb'] for r in context['cells']['F7']}
    require(len(pixels) == 10032, 'pinned context scope')
    geometry, row_helper, book = helper('geometry'), helper('rows'), helper('bookkeeping')
    representation = load(BASE/'pypdf-representation01.json')
    invocation = next(v for v in representation['image_invocations'] if v['name'] == 'Im2')
    require(invocation['native_dimensions'] == [741, 88], 'new strip dimensions')
    axes = {panel+'-'+reader: row_helper.axis_intervals(panel, reader)
            for panel in ('F', 'E') for reader in ('root', 'independent')}
    require(exact(actual['axis_boxes'], axes) and exact(prior['axis_boxes'], axes), 'fixed axis alternatives')
    readings, roles, regions, white = [], {}, {}, {}
    counts = Counter()
    for role in ROLES:
        data = readers[role]
        snapshot = encoded(data)
        bands = annotation(data, role, book)
        path = os.path.relpath(HERE/f'reader-{role}.json', BASE)
        region = {'pair': 'F7', 'source': 'Im2', 'target_box': TARGET}
        rows = row_helper.expected_rows(geometry.copy_source(data), region, 'F', invocation)
        require(len(rows) == 220 and encoded(data) == snapshot, 'original preservation/row count')
        counts['source_route_records'] += 220
        counts['source_bands'] += sum(map(len, bands.values()))
        counts['new_decisions'] += len(rows)
        counts['new_rectangle_conversions'] += sum(r['native_rectangle'] is not None for r in rows)
        counts['new_conditional_windows'] += sum(r['conditional_window'] for r in rows)
        counts['new_axis_hulls'] += sum(len(r['physical_windows'] or []) for r in rows)
        readings.append({'pair': 'F7', 'source': 'Im2', 'reader_path': path, 'rows': rows,
            'summary': {'records': len(rows), 'conditional_windows': sum(r['conditional_window'] for r in rows),
                        'reasons_nonexclusive': dict(Counter(reason for r in rows for reason in r['reasons']))}})
        roles[path], regions[path] = role, region
        white[role] = [{'scope': scope, 'class': cls, 'x': row['x'], 'y': y}
            for scope in ('solid', 'dash', 'unassigned')
            for row in (data['unassigned_bands'] if scope == 'unassigned' else data['routes'][scope])
            for cls in ('core', 'fringe') for y in row[cls] if pixels[row['x'], y] == [255, 255, 255]]
    require(exact(actual['originals'], readers), 'embedded originals differ')
    require(exact(actual['new_readings'], readings), 'new decisions/CTM/axes/summaries differ')
    new_cells = geometry.expected_cells(readings, roles, regions)
    require(exact(actual['new_candidate_cells'], new_cells), 'new candidate provenance/geometry')
    comparison, summary = comparisons(readers, book)
    require(exact(actual['reader_comparison'], comparison) and exact(actual['reader_difference_summary'], summary), 'reader set arithmetic/summary')
    require(exact(actual['selected_exact_white'], white), 'selected-white diagnostics')
    old_cells = [c for c in prior['candidate_cells'] if c['pair'] == 'F7']
    old_scenarios = next(p['scenarios'] for p in prior['pairs'] if p['pair'] == 'F7')
    require(exact(actual['preserved_old_F7_candidate_cells'], old_cells) and
            exact(actual['before_scenarios'], old_scenarios), 'old F7 objects not preserved')
    require(actual['unchanged_other_pairs_reference'] == os.path.relpath(OLD/'run01.json', HERE), 'old other-pair reference')
    coverage = []
    for phase, cells, scenarios in [('before', old_cells, old_scenarios), ('after', old_cells+new_cells, actual['after_scenarios'])]:
        require(type(scenarios) is list and len(scenarios) == 4, 'four fixed role scenarios')
        for index, (solid, dash) in enumerate(itertools.product(ROLES, repeat=2)):
            chosen = [c for c in cells if (c['route'] == 'solid' and c['role'] == solid) or
                      (c['route'] == 'dash' and c['role'] == dash)]
            expected = geometry.scenario_check(scenarios[index], chosen, 'F7', solid, dash, axes)
            counts[phase+'_scenarios'] += 1
            counts[phase+'_elementary_segments'] += len(expected['segments'])
            counts[phase+'_paired_runs'] += len(expected['paired_runs'])
            counts[phase+'_length_extrema'] += 4
            coverage.append({'phase': phase, 'solid_reader': solid, 'dash_reader': dash,
                'segments': len(expected['segments']), 'paired_segments': expected['paired_segment_count'],
                'paired_runs': len(expected['paired_runs'])})
    omissions = []
    for name in required:
        altered = dict(actual['inputs'])
        del altered[name]
        try:
            require_map(altered, required)
        except ValueError:
            omissions.append(name)
        else:
            raise ValueError('omitted required pin accepted '+name)
    after = {name: pin(HERE/name) for name in before}
    require(before == after, 'inputs changed during independent check')
    counts.update(new_candidate_cells=len(new_cells), preserved_old_F7_cells=len(old_cells),
                  reader_comparison_arrays=(220+110)*3*5, old_readings_by_reference=44,
                  old_source_records_by_reference=14420)
    return {'status': 'pass_F7_source_bookkeeping_and_conditional_arithmetic_only',
        'coverage': dict(counts), 'scenarios': coverage,
        'reader_comparison_summary': summary, 'selected_exact_white': white,
        'required_producer_pin_count': len(required), 'producer_pin_count': len(actual['inputs']),
        'required_pin_omission_checks': sorted(omissions),
        'inputs': before, 'inputs_after': after,
        'producer_run_pins': {os.path.relpath(p, HERE): pin(p) for p in (run1, run2)},
        'reader_original_pins': {role: pin(HERE/f'reader-{role}.json') for role in ROLES},
        'independence': 'Hash-pinned independent raw-row/CTM, midpoint-partition and integer-mask/truth-table components reused. No producer, annotation, selection, adapter, calculator or event-sweep imports. Protocol/schema inspected; same checker author as earlier method work.',
        'limits': 'All new rows and material F7 geometry/arithmetic checked; old 14420 rows retained by frozen reference, not reclassified. P/P and other combinations are fixed version-role scenarios across regions, not necessarily the same person/agent across old and new readings. Literal-script byte expansion is parent replay, not independently executed here. Coverage/view receipts are attestations, not proof of perception. Context fidelity inherited from separately pinned full-cell check. No source ownership, H hypothesis, generating-curve containment, physical support, human acceptance or cause result.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run1', type=Path, default=HERE/'run01.json')
    parser.add_argument('--run2', type=Path, default=HERE/'run02.json')
    parser.add_argument('--expected-sha', required=True)
    parser.add_argument('--primary-sha', required=True)
    parser.add_argument('--peer-sha', required=True)
    parser.add_argument('--save-receipt', action='store_true')
    args = parser.parse_args()
    receipt = verify(args.run1, args.run2, args.expected_sha, {'primary': args.primary_sha, 'peer': args.peer_sha})
    if args.save_receipt:
        with (HERE/'independent-check.json').open('xb') as output:
            output.write(encoded(receipt))
        print(json.dumps({'output': pin(HERE/'independent-check.json'), 'coverage': receipt['coverage']}, sort_keys=True))
    else:
        print(encoded(receipt).decode(), end='')
