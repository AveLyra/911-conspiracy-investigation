"""Finite F7 reading comparison and inherited conditional-coverage test."""
import argparse
from collections import Counter
import copy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
REGION = 'F7-Im2-early'
VALIDATION_ALIAS = 'F7-Im2'
TARGET = [220, 0, 330, 88]
CONTEXT = [218, 0, 332, 88]
ROLES = ('primary', 'peer')
OLD = BASE/'historical-applicability/admission-2026-10-08'
METHODS = {
    '../../historical-applicability/admission-2026-10-08/assess.py': 'bf0ad1c87374adda3e2751461b33aec678b780f438b74d32ac75767f8f5de1e4',
    '../../historical-applicability/conditional-envelopes-2026-10-08/calculate.py': '9d3f00efca8cb858b80a2b34c11f8253d2de59c66b46257df9dfc715d73ee89a',
    '../../historical-applicability/approach34-extension-2026-10-08/extend.py': '18f5862d014c5e9848cd6332da3929437c7ff93031e3ca255730d1f9e0dfc3f0',
    '../force56-remainder/compare.py': '81dc892b21e891a9c11d2bc7697d1b936a497a91950584659e04fc718776313a',
    '../force45/compare_force45.py': '932792f49797c4034beb1124d8174a56c911319e17fa536e199f0709950557be',
    '../force69/compare_force69.py': 'f332359911f4d7bf5e768bf9e36b37ddb6995e857f6cf7ae5fa5456bb6dd4a6e',
    '../approach34/compare.py': 'cb4a2da60959a4b0a40ddb4a072c1cbedf4624da63daf1a50b37db0eb2dd5bac',
    '../../historical-applicability/screen.py': 'eab1bc47664a9e4a9176f0f1c79b20c0c3b223e03f64b983c982d74a67433b82',
    '../../registration_controls.py': '98873f48740f69499f509e1e1db5c425586d25811e83ae9c88c862db7e54bc54',
}
FROZEN = {
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
FIELDS = {'x', 'core', 'fringe', 'fragment_id', 'fragment_membership', 'status',
          'reason', 'boundary_flags', 'unassigned_band_refs'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pin(path):
    raw = Path(path).read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def encode(obj):
    def exact(value):
        if type(value) is F:
            return str(value)
        raise TypeError('Only exact Fraction extensions permitted')
    return (json.dumps(obj, default=exact, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()


def load(path):
    return json.loads(Path(path).read_text())


def add(pins, path, expected=None, recurse=False):
    path = Path(path).resolve()
    name = os.path.relpath(path, HERE)
    actual = pin(path)
    if type(expected) is str:
        require(actual['sha256'] == expected, 'Changed fixed input '+name)
    elif expected is not None:
        require(type(expected) is dict and set(expected) == {'bytes', 'sha256'}
                and type(expected['bytes']) is int and actual == expected, 'Changed/invalid pin '+name)
    if name in pins:
        require(pins[name] == actual, 'Conflicting dependency '+name)
        return
    pins[name] = actual
    if recurse and path.suffix == '.json':
        data = load(path)
        for child, value in data.get('inputs', {}).items():
            add(pins, path.parent/child, value, True)


def module(path, expected=None):
    path = Path(path).resolve()
    if expected:
        require(pin(path)['sha256'] == expected, 'Changed import '+str(path))
    spec = importlib.util.spec_from_file_location('f7_'+path.parent.name+'_'+path.stem, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = result
    spec.loader.exec_module(result)
    return result


def methods():
    for name, expected in METHODS.items():
        require(pin(HERE/name)['sha256'] == expected, 'Changed helper '+name)
    geometry, calc, adapter, validator = [module(HERE/name, METHODS[name]) for name in list(METHODS)[:4]]
    validator.TARGETS = {VALIDATION_ALIAS: TARGET}
    validator.CONTEXTS = {VALIDATION_ALIAS: CONTEXT}
    h, comparison, a = validator.helpers()
    return geometry, calc, adapter, validator, h, comparison, a


def validation_copy(data, role):
    """Explicit compatibility alias on a copy; original ID is never rewritten."""
    require(role in ROLES and data['reader'] == role, 'Exact role')
    require(data['region_id'] == REGION and data['pair'] == 'F7'
            and data['source'] == 'Im2.jpg', 'Exact new region/source')
    for key, expected in [('target_box', TARGET), ('context_box', CONTEXT)]:
        require(type(data[key]) is list and all(type(n) is int for n in data[key])
                and data[key] == expected, 'Exact integer '+key)
    require(set(data['routes']) == {'solid', 'dash'}, 'Both and only both routes')
    for rows in data['routes'].values():
        require(all(set(row) == FIELDS for row in rows), 'Exact route fields')
    for row in data['unassigned_bands']:
        require(set(row) == FIELDS | {'band_id', 'candidate_routes'}, 'Exact band fields')
        require(row['unassigned_band_refs'] == [], 'No band-to-band refs')
    cv = data['coverage']
    require({'full_context_inspected', 'raw_context_cells', 'raw_blocks', 'actual_views',
             'prior_knowledge', 'rows', 'uncompleted_context'} <= set(cv), 'Coverage schema')
    require(type(cv['rows']) is list and all(type(n) is int for n in cv['rows'])
            and cv['rows'] == [0, 87], 'Explicit row coverage')
    views = cv['actual_views']
    require(type(views) is list and views and all(type(v) is dict and
            isinstance(v.get('path'), str) and v['path'].strip() and
            isinstance(v.get('receipt'), str) and v['receipt'].strip() for v in views),
            'Actual view paths and receipts')
    required_views = {(HERE/'../../native-strips01/Im2.jpg').resolve(),
                      (HERE/'../../render01/page-076.png').resolve()}
    require(required_views <= {(HERE/v['path']).resolve() for v in views}, 'Missing source/page view')
    require(isinstance(cv['prior_knowledge'], str) and cv['prior_knowledge'].strip(), 'Prior disclosure')
    require(type(cv['raw_blocks']) is list and all(type(b) is dict and
            ('truncated' not in b or b['truncated'] is False) for b in cv['raw_blocks']),
            'Explicitly truncated block is not complete coverage')
    require('counterpart_new_annotations_read' not in cv or cv['counterpart_new_annotations_read'] is False,
            'Counterpart access contradicts separate freeze')
    copied = copy.deepcopy(data)
    copied['region_id'] = VALIDATION_ALIAS
    return copied


def validate(data, role, loaded):
    snapshot = encode(data)
    copied = validation_copy(data, role)
    _, _, _, validator, h, _, a = loaded
    validator.validate(copied, VALIDATION_ALIAS, role, h, a)
    require(encode(data) == snapshot, 'Preserved original mutated')


def compare_readers(readings, h):
    routes, ink = [], []
    for route in ('solid', 'dash'):
        for first, second in zip(readings['primary']['routes'][route], readings['peer']['routes'][route]):
            routes.append({'route': route, 'x': first['x'], 'primary': first, 'peer': second,
                           'sets': h.comparison(first, second)})
    for x in range(TARGET[0], TARGET[2]):
        chosen = []
        for role in ROLES:
            data = readings[role]
            rows = [data['routes'][r][x-TARGET[0]] for r in ('solid', 'dash')]
            rows += [row for row in data['unassigned_bands'] if row['x'] == x]
            chosen.append({cls: sorted({y for row in rows for y in row[cls]}) for cls in ('core', 'fringe')})
        ink.append({'x': x, 'sets': h.comparison(*chosen)})
    return {'route_records': routes, 'all_ink_columns': ink}


def build(reader_pins):
    require(set(reader_pins) == set(ROLES), 'Both explicit frozen reader hashes required')
    pins = {}
    for name, expected in {**FROZEN, **METHODS}.items():
        add(pins, HERE/name, expected)
    for name in ('assess.py', 'test_assess.py', 'CONSUMER-COMPATIBILITY.md'):
        add(pins, HERE/name)
    prior = load(OLD/'run01.json')
    require((OLD/'run01.json').read_bytes() == (OLD/'run02.json').read_bytes(), 'Old repeats')
    require(prior['inputs'] == prior['inputs_after'], 'Old before/after pins')
    for name, expected in prior['inputs'].items():
        add(pins, BASE/name, expected)
    prior_receipt = load(OLD/'independent-check.json')
    require(prior_receipt['inputs'] == prior_receipt['inputs_after'], 'Prior independent receipt pins')
    for name, expected in prior_receipt['inputs'].items():
        add(pins, BASE/name, expected)
    old_cells = [c for c in prior['candidate_cells'] if c['pair'] == 'F7']
    old_states = next(p for p in prior['pairs'] if p['pair'] == 'F7')['scenarios']
    old_snapshot = encode(old_cells)
    raw_context = (HERE/'context01.json').read_bytes()
    require(raw_context == (HERE/'context02.json').read_bytes(), 'Context repeats')
    context = load(HERE/'context01.json')
    require(context['target_boxes'] == {'F7': TARGET} and context['context_boxes'] == {'F7': CONTEXT}
            and context['sources'] == {'F7': 'Im2.jpg'} and context['source_size'] == [741, 88], 'Context identity')
    pixels = {(r['x'], r['y']): r['rgb'] for r in context['cells']['F7']}
    require(len(pixels) == len(context['cells']['F7']) == 10032 and
            set(pixels) == {(x,y) for x in range(218,332) for y in range(88)}, 'Context coverage')
    add(pins, HERE/'context01.json', recurse=True)
    # The fixed pin above already visited the file; explicitly include its inputs.
    for name, expected in context['inputs'].items():
        add(pins, HERE/name, expected, True)
    loaded = methods()
    geometry, calc, adapter, _, h, totals, _ = loaded
    require(encode(geometry.pairings('F7', old_cells, prior['axis_boxes'])) == encode(old_states), 'Old F7 replay')
    rep = json.loads((BASE/'pypdf-representation01.json').read_text(), parse_float=F)
    invocation = next(r for r in rep['image_invocations'] if r['name'] == 'Im2')
    strip = calc.geometry.Strip('Im2', *invocation['native_dimensions'], invocation['ctm'])
    readings, added, roles, regions, white = {}, [], {}, {}, {}
    for role in ROLES:
        path = HERE/f'reader-{role}.json'
        add(pins, path, reader_pins[role], True)
        data = load(path)
        require({'PROTOCOL.md', 'READERS.md', 'context01.json', 'context02.json',
                 '../../native-strips01/Im2.jpg'} <= set(data['inputs']), 'Required reader dependencies')
        script = path.with_suffix('.py')
        add(pins, script, data['script_pin'])
        require(encode(module(script, data['script_pin']['sha256']).build()) == encode(data), 'Literal build differs')
        validate(data, role, loaded)
        readings[role] = data
        rows = calc.process({r: [adapter.row_adapter(row, height=88) for row in data['routes'][r]]
                             for r in ('solid', 'dash')}, strip, TARGET, 'F')
        key = os.path.relpath(path, BASE)
        added.append({'pair': 'F7', 'source': 'Im2', 'reader_path': key, 'rows': rows,
                      'summary': {'records': len(rows), 'conditional_windows': sum(r['conditional_window'] for r in rows),
                                  'reasons_nonexclusive': dict(Counter(k for r in rows for k in r['reasons']))}})
        roles[key] = role
        regions[key] = {'pair': 'F7', 'source': 'Im2', 'target_box': TARGET}
        white[role] = [{'scope': scope, 'class': cls, 'x': row['x'], 'y': y}
                       for scope, rows0 in list(data['routes'].items())+[('unassigned', data['unassigned_bands'])]
                       for row in rows0 for cls in ('core', 'fringe') for y in row[cls]
                       if pixels[row['x'], y] == [255, 255, 255]]
    comparison = compare_readers(readings, h)
    cells = geometry.make_cells(added, roles, regions)
    after_states = geometry.pairings('F7', old_cells+cells, prior['axis_boxes'])
    require(encode(old_cells) == old_snapshot, 'Old candidates mutated')
    after = {name: pin(HERE/name) for name in pins}
    require(after == pins, 'Input changed')
    return {'status': 'conditional_F7_coverage_followup_not_admitted_support',
            'region_id': REGION, 'target_box': TARGET, 'context_box': CONTEXT,
            'inputs': pins, 'inputs_after': after, 'originals': readings,
            'validation_alias': {'preserved': REGION, 'copy_only': VALIDATION_ALIAS,
                                 'purpose': 'Unchanged old validator two-token region parser; no source/target/role change'},
            'reader_comparison': comparison,
            'reader_difference_summary': {'routes': totals.totals(comparison['route_records']),
                                          'all_ink': totals.totals(comparison['all_ink_columns']),
                                          'status_different': sum(r['primary']['status'] != r['peer']['status'] for r in comparison['route_records'])},
            'selected_exact_white': white, 'new_readings': added, 'new_candidate_cells': cells,
            'preserved_old_F7_candidate_cells': old_cells, 'before_scenarios': old_states,
            'after_scenarios': after_states, 'axis_boxes': prior['axis_boxes'],
            'unchanged_other_pairs_reference': os.path.relpath(OLD/'run01.json', HERE),
            'actual_D': None, 'human_accepted': False, 'model_discrepancies': None,
            'assumptions': ['Hidentity', 'Hsupport', 'Hink0'],
            'limits': ['New source and conditional coverage only; no seam trajectory join.',
                       'Four reader-role combinations are alternatives, not independent evidence.',
                       'Roles denote fixed annotation versions across regions, not necessarily the same agent/person; the four scenarios are not all possible annotation uncertainty.',
                       'Fixed old CE packet and its unavailable F7 slots unchanged.',
                       'No generating-curve containment, physical calibration or causal finding.']}


def save(path, raw):
    with Path(path).open('xb') as stream:
        stream.write(raw)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--primary-sha', required=True)
    p.add_argument('--peer-sha', required=True)
    p.add_argument('--run', required=True, choices=('01', '02'))
    args = p.parse_args()
    result = build({'primary': args.primary_sha, 'peer': args.peer_sha})
    destination = HERE/f'run{args.run}.json'
    save(destination, encode(result))
    print(json.dumps({'output': pin(destination), 'new_records': sum(len(r['rows']) for r in result['new_readings']),
                      'new_candidates': len(result['new_candidate_cells']), 'pins': len(result['inputs'])}, sort_keys=True))
