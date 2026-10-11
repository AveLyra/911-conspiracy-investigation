"""Versioned complete mapping regeneration after the finite F7 source recovery."""
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
OLD = HERE.parent / 'envelope-packet-2026-10-08'
F7 = BASE / 'native-footprint-pass/force7-paired-coverage'
PARENT = 'historical-applicability/admission-2026-10-08/run01.json'
PRIOR_PACKET = 'historical-applicability/envelope-packet-2026-10-08/packet01.json'
F7_RESULT = 'native-footprint-pass/force7-paired-coverage/run-v2-01.json'
PACKET_ID = 'conditional-envelope-f7-v2-2026-10-08'
HELPER_SHA = 'e17e1ab93d43238bd09b5071d45dee174fdc22dd721c00fac83df5739ef6cac7'
OLD_SHA = 'cb0f9da2f36e384eeeb046528696bba4f379fc8419f393a18ae2f809b05829cc'
F7_SHA = 'ade1b08251bd68ed71ec535e263389725e193b81e6aa4959e8a891fcb1505aeb'
FIXED = {
    PARENT: '4aeca445bc71d4495dd578df6a4de96e3bf2d54004b6afb0b1efcf7bb631930e',
    PRIOR_PACKET: OLD_SHA,
    'historical-applicability/envelope-packet-2026-10-08/packet02.json': OLD_SHA,
    'historical-applicability/envelope-packet-2026-10-08/independent-check.json':
        'cc822cf3cb0214f9e3901a0d554af922363383518a18418b034bcde132d0760d',
    F7_RESULT: F7_SHA,
    'native-footprint-pass/force7-paired-coverage/run-v2-02.json': F7_SHA,
    'native-footprint-pass/force7-paired-coverage/independent-check-v2.json':
        'd48538e8048dfce4bf68741f24075f496d4a0bf996435bc5a8f392f4f7623c57',
}


def import_helper(path):
    path = Path(path)
    if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != HELPER_SHA:
        raise ValueError('changed original mapping helper')
    spec = importlib.util.spec_from_file_location('fixed_original_packet', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


old = import_helper(OLD / 'packet.py')
require, encode, load, pin, include = old.require, old.encode, old.load, old.pin, old.include


def unaccepted(data):
    require(data['human_accepted'] is False and data['actual_D'] is None and
            data['model_discrepancies'] is None, 'unexpected acceptance or discrepancy')
    require(data['assumptions'] == ['Hidentity', 'Hsupport', 'Hink0'], 'changed assumptions')


def scenarios(rows):
    require(len(rows) == 4, 'four scenarios required')
    roster = {(r['solid_reader'], r['dash_reader']) for r in rows}
    require(roster == {(s, d) for s in old.ROLES for d in old.ROLES}, 'reader roster changed')
    for row in rows:
        require(row['human_accepted'] is False and row['actual_D'] is None,
                'scenario acceptance contamination')
        old.intervals(row['segments'])


def compose(admission, supplement, expected_additions):
    """Copy, never mutate, frozen inputs; no selection takes place here."""
    unaccepted(admission)
    unaccepted(supplement)
    require(tuple(p['pair'] for p in admission['pairs']) == old.PAIRS, 'pair roster changed')
    require(admission['axis_boxes'] == supplement['axis_boxes'], 'axis boxes changed')
    original = next(p for p in admission['pairs'] if p['pair'] == 'F7')
    require(original['scenarios'] == supplement['before_scenarios'], 'old F7 scenarios changed')
    old_cells = admission['candidate_cells']
    old_f7 = [c for c in old_cells if c['pair'] == 'F7']
    require(old_f7 == supplement['preserved_old_F7_candidate_cells'], 'old F7 cells changed')
    additions = supplement['new_candidate_cells']
    require(type(expected_additions) is int and expected_additions >= 0 and
            len(additions) == expected_additions, 'added-cell roster incomplete')
    require(all(c['pair'] == 'F7' and c['role'] in old.ROLES and
                c['route'] in ('solid', 'dash') for c in additions), 'addition outside F7 roster')
    ids = [c['id'] for c in old_cells + additions]
    require(len(set(ids)) == len(ids), 'duplicate candidate ID')
    for rows in (original['scenarios'], supplement['after_scenarios']):
        scenarios(rows)
    combined = copy.deepcopy(admission)
    combined['candidate_cells'].extend(copy.deepcopy(additions))
    next(p for p in combined['pairs'] if p['pair'] == 'F7')['scenarios'] = copy.deepcopy(
        supplement['after_scenarios'])
    require([p for p in combined['pairs'] if p['pair'] != 'F7'] ==
            [p for p in admission['pairs'] if p['pair'] != 'F7'], 'non-F7 pair changed')
    require(combined['candidate_cells'][:len(old_cells)] == old_cells, 'old cell prefix changed')
    return combined


def compare_slots(slots, previous):
    require(len(slots) == len(previous) == 42, 'complete 42-slot roster required')
    require([s['id'] for s in slots] == [s['id'] for s in previous], 'slot identity/order changed')
    unchanged, changed = [], []
    for current, prior in zip(slots, previous):
        if current['pair'] != 'F7':
            require(current == prior, 'non-F7 slot changed ' + current['id'])
            unchanged.append(current['id'])
        if current != prior:
            changed.append(current['id'])
    require(len(unchanged) == 39, '39 unchanged non-F7 slots required')
    return unchanged, changed


def include_declared(pins, record, owner):
    """Resolve each frozen map at its declared owner, then normalize to BASE."""
    require(record['inputs'] == record['inputs_after'], 'saved dependency drift')
    for name, expected in record['inputs'].items():
        include(pins, Path(owner) / name, expected)


def inputs():
    pins = {}
    for name, sha in FIXED.items():
        include(pins, BASE / name, sha)
    include(pins, OLD / 'packet.py', HELPER_SHA)
    prior = load(BASE / PRIOR_PACKET)
    receipt = load(F7 / 'independent-check-v2.json')
    include_declared(pins, prior, BASE)
    include_declared(pins, receipt, F7)
    for name in ('PROTOCOL.md', 'packet.py', 'test_packet.py'):
        include(pins, HERE / name)
    return pins, prior


def build():
    before, prior = inputs()
    unaccepted(prior)
    require(prior['version'] == 1 and prior['original_actual_D_sampling_fulfilled'] is False,
            'unexpected old packet version or support acceptance')
    require(all(s['human_accepted'] is False and all(e['human_response'] is None and
                e['human_status'] == 'uninspected' for e in s['entries']) for s in prior['slots']),
            'prior response must not be silently carried forward')
    admission, supplement = load(BASE / PARENT), load(BASE / F7_RESULT)
    require(len(admission['candidate_cells']) == 4779 and
            len(supplement['preserved_old_F7_candidate_cells']) == 264, 'fixed source cell counts')
    combined = compose(admission, supplement, 75)
    representation = load(BASE / 'pypdf-representation01.json')
    invocations = {i['name']: i for i in representation['image_invocations']}
    slots, inventory = old.make_slots(combined, invocations)
    # Correct the old helper's fixed provenance string explicitly, not its globals.
    for row in inventory:
        row['all_scenarios_preserved_in'] = F7_RESULT if row['pair'] == 'F7' else PARENT
    unchanged, changed = compare_slots(json.loads(encode(slots)), prior['slots'])
    result = copy.deepcopy(prior)
    result.update(version=2, packet_id=PACKET_ID, slots=slots, inventory=inventory,
                  parent_packet=PRIOR_PACKET, f7_result=F7_RESULT,
                  summary=dict(Counter(s['selection_status'] for s in slots)),
                  composition={
                      'old_candidate_cell_count': len(admission['candidate_cells']),
                      'added_F7_candidate_cell_count': len(supplement['new_candidate_cells']),
                      'composed_candidate_cell_count': len(combined['candidate_cells']),
                      'preserved_old_F7_candidate_cell_count': 264,
                      'unchanged_pairs': [p for p in old.PAIRS if p != 'F7'],
                      'unchanged_slot_ids': unchanged, 'changed_slot_ids': changed,
                      'inventory_reference_base': 'connection-curve-comparison'})
    after = {name: pin(BASE / name) for name in before}
    require(before == after, 'inputs changed during regeneration')
    result['inputs'], result['inputs_after'] = before, after
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', choices=('01', '02'))
    args = parser.parse_args()
    result = build()
    path = HERE / ('packet' + args.run + '.json')
    old.save(path, encode(result))
    print(json.dumps({'file': path.name, 'pin': pin(path), 'summary': result['summary'],
                      'composition': result['composition'], 'input_pins': len(result['inputs'])},
                     sort_keys=True))
