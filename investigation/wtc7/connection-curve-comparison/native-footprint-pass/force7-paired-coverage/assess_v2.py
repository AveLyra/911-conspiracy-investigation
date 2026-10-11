"""Explicit additive reader binding for the unchanged conditional F7 test.

The pinned legacy module supplies pure validation/arithmetic helpers. Its build
function and hardcoded reader paths are not invoked or monkeypatched.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEGACY_SHA = 'e8a4af86fcaea4b34c8b86ea837fa6ec7d78455d6d576c89946818e5c0ca949a'
BINDINGS = {'primary': 'reader-primary.json', 'peer': 'reader-peer-v2.json'}
PRESERVED = {
    'COMPLETION-V2.md': '6d68e22e1410c76302e135a5b73adffde1374bcc51699225133400c9fc69ab4a',
    'peer-reread-2026-10-08.md': '39368d4316acf06f53a7dfd4ed96eaecf45667d858ea4327c6b64b58b33a08d2',
    'reader-peer.py': '3d4bf1e066755d0242f287ef02b48a40fc6f27a28941953471e089214c00d98b',
    'reader-primary.py': 'eb88429fabb627c72cdca859574daadd6f31d2fae68b44c3cd81961a6f65ca3b',
    'reader-primary.json': '4a3c323f83b25b93a88dd8db1b31fdcc77935e90b1494e3b3dc8f7eb40f8b734',
    'reader-primary-notes.md': '85e77c860c9fc701f76daa44d846ed7101f6b7ea0de5726bafa0540549963f28',
    'assess.py': LEGACY_SHA,
    'test_assess.py': 'a3945b67fd16e0f205360b0ac411a3dd086935a22a1bf73a52123c428528a36d',
    'independent_check.py': 'b95e64271eab6c2bb6c9f981ddbda39bfa8159204ddfd81304f828b231f54304',
    'test_independent_check.py': '4a644deada7fe66838757e319929e8711cab40b127f54ed5def18c891c0e8f18',
    'report.md': '6e8477bd2a5c270cdec40b2652bb55523f7c905418bd335401516e8334194d42',
    'validation.md': '930ebe0d208d19e6c1a544da9a764a748db7fc9a1d2c53456d444f931c8ff11b',
    'CONSUMER-COMPATIBILITY.md': '30dfd6b79e89358050fd9b60bc4e9a09bc302ba66aeb9bd8472ee9791180c12c',
}


def library():
    path = HERE / 'assess.py'
    if hashlib.sha256(path.read_bytes()).hexdigest() != LEGACY_SHA:
        raise ValueError('Changed legacy consumer')
    spec = importlib.util.spec_from_file_location('f7_preserved_consumer_v1', path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def validate_bindings(values):
    expected = {'primary': 'reader-primary.json', 'peer': 'reader-peer-v2.json'}
    if type(values) is not dict or values != expected:
        raise ValueError('Exact versioned reader binding required')
    return {role: HERE / name for role, name in values.items()}


def add_preserved(pins, a):
    for name, expected in PRESERVED.items():
        a.add(pins, HERE / name, expected)


def include_reader_inputs(pins, owner, data, a):
    """Expand declared JSON dependencies even when their bytes are already pinned."""
    pending = [(Path(owner) / name, expected) for name, expected in data['inputs'].items()]
    expanded = set()
    while pending:
        path, expected = pending.pop()
        path = path.resolve()
        a.add(pins, path, expected)
        if path in expanded or path.suffix != '.json':
            continue
        expanded.add(path)
        child = a.load(path)
        if 'inputs_after' in child:
            a.require(child['inputs'] == child['inputs_after'], 'Nested before/after pins differ')
        pending.extend((path.parent / name, value) for name, value in child.get('inputs', {}).items())
        if path.name.startswith('reader-') and 'script_pin' in child:
            a.add(pins, path.with_suffix('.py'), child['script_pin'])


def build(reader_pins):
    a = library()
    a.require(type(reader_pins) is dict and set(reader_pins) == set(a.ROLES),
              'Both explicit frozen reader hashes required')
    paths = validate_bindings(BINDINGS)
    pins = {}
    add_preserved(pins, a)
    for name, expected in {**a.FROZEN, **a.METHODS}.items():
        a.add(pins, HERE / name, expected)
    for name in ('assess_v2.py', 'test_assess_v2.py', 'reader-peer-v2-notes.md'):
        a.add(pins, HERE / name)
    prior = a.load(a.OLD / 'run01.json')
    a.require((a.OLD / 'run01.json').read_bytes() == (a.OLD / 'run02.json').read_bytes(), 'Old repeats')
    a.require(prior['inputs'] == prior['inputs_after'], 'Old before/after pins')
    for name, expected in prior['inputs'].items():
        a.add(pins, a.BASE / name, expected)
    prior_receipt = a.load(a.OLD / 'independent-check.json')
    a.require(prior_receipt['inputs'] == prior_receipt['inputs_after'], 'Prior independent receipt pins')
    for name, expected in prior_receipt['inputs'].items():
        a.add(pins, a.BASE / name, expected)
    old_cells = [c for c in prior['candidate_cells'] if c['pair'] == 'F7']
    old_states = next(p for p in prior['pairs'] if p['pair'] == 'F7')['scenarios']
    old_snapshot = a.encode(old_cells)
    a.require((HERE / 'context01.json').read_bytes() == (HERE / 'context02.json').read_bytes(), 'Context repeats')
    context = a.load(HERE / 'context01.json')
    a.require(context['target_boxes'] == {'F7': a.TARGET} and context['context_boxes'] == {'F7': a.CONTEXT}
              and context['sources'] == {'F7': 'Im2.jpg'} and context['source_size'] == [741, 88], 'Context identity')
    pixels = {(r['x'], r['y']): r['rgb'] for r in context['cells']['F7']}
    a.require(len(pixels) == len(context['cells']['F7']) == 10032 and
              set(pixels) == {(x, y) for x in range(218, 332) for y in range(88)}, 'Context coverage')
    for name, expected in context['inputs'].items():
        a.add(pins, HERE / name, expected, True)
    loaded = a.methods()
    geometry, calc, adapter, _, h, totals, _ = loaded
    a.require(a.encode(geometry.pairings('F7', old_cells, prior['axis_boxes'])) == a.encode(old_states), 'Old F7 replay')
    rep = json.loads((a.BASE / 'pypdf-representation01.json').read_text(), parse_float=a.F)
    invocation = next(r for r in rep['image_invocations'] if r['name'] == 'Im2')
    strip = calc.geometry.Strip('Im2', *invocation['native_dimensions'], invocation['ctm'])
    readings, added, roles, regions, white = {}, [], {}, {}, {}
    for role in a.ROLES:
        path = paths[role]
        a.add(pins, path, reader_pins[role], True)
        data = a.load(path)
        include_reader_inputs(pins, path.parent, data, a)
        required = {'PROTOCOL.md', 'READERS.md', 'context01.json', 'context02.json',
                    '../../native-strips01/Im2.jpg'}
        if role == 'peer':
            required |= {'COMPLETION-V2.md', 'reader-peer.py', 'peer-reread-2026-10-08.md'}
        a.require(required <= set(data['inputs']), 'Required versioned reader dependencies')
        script = path.with_suffix('.py')
        a.add(pins, script, data['script_pin'])
        a.require(a.encode(a.module(script, data['script_pin']['sha256']).build()) == a.encode(data), 'Literal build differs')
        a.validate(data, role, loaded)
        readings[role] = data
        rows = calc.process({r: [adapter.row_adapter(row, height=88) for row in data['routes'][r]]
                             for r in ('solid', 'dash')}, strip, a.TARGET, 'F')
        key = os.path.relpath(path, a.BASE)
        added.append({'pair': 'F7', 'source': 'Im2', 'reader_path': key, 'rows': rows,
                      'summary': {'records': len(rows), 'conditional_windows': sum(r['conditional_window'] for r in rows),
                                  'reasons_nonexclusive': dict(Counter(k for r in rows for k in r['reasons']))}})
        roles[key] = role
        regions[key] = {'pair': 'F7', 'source': 'Im2', 'target_box': a.TARGET}
        white[role] = [{'scope': scope, 'class': cls, 'x': row['x'], 'y': y}
                       for scope, rows0 in list(data['routes'].items()) + [('unassigned', data['unassigned_bands'])]
                       for row in rows0 for cls in ('core', 'fringe') for y in row[cls]
                       if pixels[row['x'], y] == [255, 255, 255]]
    comparison = a.compare_readers(readings, h)
    cells = geometry.make_cells(added, roles, regions)
    after_states = geometry.pairings('F7', old_cells + cells, prior['axis_boxes'])
    a.require(a.encode(old_cells) == old_snapshot, 'Old candidates mutated')
    after = {name: a.pin(HERE / name) for name in pins}
    a.require(after == pins, 'Input changed')
    return {'status': 'conditional_F7_coverage_followup_not_admitted_support',
            'region_id': a.REGION, 'target_box': a.TARGET, 'context_box': a.CONTEXT,
            'inputs': pins, 'inputs_after': after, 'originals': readings,
            'validation_alias': {'preserved': a.REGION, 'copy_only': a.VALIDATION_ALIAS,
                                 'purpose': 'Unchanged old validator two-token region parser; no source/target/role change'},
            'reader_comparison': comparison,
            'reader_difference_summary': {'routes': totals.totals(comparison['route_records']),
                                          'all_ink': totals.totals(comparison['all_ink_columns']),
                                          'status_different': sum(r['primary']['status'] != r['peer']['status'] for r in comparison['route_records'])},
            'selected_exact_white': white, 'new_readings': added, 'new_candidate_cells': cells,
            'preserved_old_F7_candidate_cells': old_cells, 'before_scenarios': old_states,
            'after_scenarios': after_states, 'axis_boxes': prior['axis_boxes'],
            'unchanged_other_pairs_reference': os.path.relpath(a.OLD / 'run01.json', HERE),
            'actual_D': None, 'human_accepted': False, 'model_discrepancies': None,
            'assumptions': ['Hidentity', 'Hsupport', 'Hink0'],
            'limits': ['Explicit v2 filename binding; old primary and old partial peer preserved.',
                       'New source and conditional coverage only; no seam trajectory join.',
                       'Four reader-role combinations are alternatives, not independent evidence.',
                       'Roles denote fixed annotation versions across regions, not necessarily the same agent/person; the four scenarios are not all possible annotation uncertainty.',
                       'Fixed old CE packet and its unavailable F7 slots unchanged.',
                       'No generating-curve containment, physical calibration or causal finding.']}


def save(path, raw):
    with Path(path).open('xb') as output:
        output.write(raw)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--primary-sha', required=True)
    parser.add_argument('--peer-sha', required=True)
    parser.add_argument('--run', required=True, choices=('01', '02'))
    args = parser.parse_args()
    result = build({'primary': args.primary_sha, 'peer': args.peer_sha})
    a = library()
    destination = HERE / f'run-v2-{args.run}.json'
    save(destination, a.encode(result))
    print(json.dumps({'output': a.pin(destination), 'new_records': sum(len(r['rows']) for r in result['new_readings']),
                      'new_candidates': len(result['new_candidate_cells']), 'pins': len(result['inputs'])}, sort_keys=True))
