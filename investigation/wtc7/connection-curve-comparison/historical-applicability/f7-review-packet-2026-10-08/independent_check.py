"""Independent composition and full reconstruction of the versioned F7 packet.

Only the SHA-pinned prior independent selection/mapping/header code is imported.
This author also authored the F7 primary annotation and v2 arithmetic checker:
shared-source/method lineage, not blind reading or historical corroboration.
"""
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
OLD_PACKET = BASE / 'historical-applicability/envelope-packet-2026-10-08'
F7 = BASE / 'native-footprint-pass/force7-paired-coverage'
ADMISSION_REF = 'historical-applicability/admission-2026-10-08/run01.json'
OLD_PACKET_REF = 'historical-applicability/envelope-packet-2026-10-08/packet01.json'
F7_REF = 'native-footprint-pass/force7-paired-coverage/run-v2-01.json'
PACKET_ID = 'conditional-envelope-f7-v2-2026-10-08'
HELPER_SHA = '16e5e348f5cbd14d4b6a8b37c9067da052be927c347a9763a2c96cd498f9ab68'
PROTOCOL_SHA = 'c3081a9ca870d0b67ddee5cec2d7dc4d346db137711baf1dbdc39af3bc362651'
FROZEN = {
    ADMISSION_REF: '4aeca445bc71d4495dd578df6a4de96e3bf2d54004b6afb0b1efcf7bb631930e',
    ADMISSION_REF.replace('run01', 'run02'): '4aeca445bc71d4495dd578df6a4de96e3bf2d54004b6afb0b1efcf7bb631930e',
    OLD_PACKET_REF: 'cb0f9da2f36e384eeeb046528696bba4f379fc8419f393a18ae2f809b05829cc',
    OLD_PACKET_REF.replace('packet01', 'packet02'): 'cb0f9da2f36e384eeeb046528696bba4f379fc8419f393a18ae2f809b05829cc',
    'historical-applicability/envelope-packet-2026-10-08/independent-check.json':
        'cc822cf3cb0214f9e3901a0d554af922363383518a18418b034bcde132d0760d',
    'historical-applicability/envelope-packet-2026-10-08/independent_check.py': HELPER_SHA,
    F7_REF: 'ade1b08251bd68ed71ec535e263389725e193b81e6aa4959e8a891fcb1505aeb',
    F7_REF.replace('01.json', '02.json'): 'ade1b08251bd68ed71ec535e263389725e193b81e6aa4959e8a891fcb1505aeb',
    'native-footprint-pass/force7-paired-coverage/independent-check-v2.json':
        'd48538e8048dfce4bf68741f24075f496d4a0bf996435bc5a8f392f4f7623c57',
    'historical-applicability/f7-review-packet-2026-10-08/PROTOCOL.md': PROTOCOL_SHA,
}
# Set only to separately supplied reviewed producer freezes, never current-file discovery.
PRODUCER_PINS = {
    'packet.py': '48015d31f451d838ec4b3438e329edd3938a81507c25d537d9c877a88b3f23fe',
    'test_packet.py': 'fbb3fe8ae0ac106fc201aef15a2d1bf468c7d692ccf11e3bf864a5d8c6f89be7',
}


def import_helper(path):
    path = Path(path)
    if not path.is_file() or path.is_symlink():
        raise ValueError('plain independent helper required')
    if hashlib.sha256(path.read_bytes()).hexdigest() != HELPER_SHA:
        raise ValueError('independent reconstruction helper changed')
    spec = importlib.util.spec_from_file_location('f7_packet_pinned_independent', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


old = import_helper(OLD_PACKET / 'independent_check.py')
demand, encoded, canonical, pin, load = old.demand, old.encoded, old.canonical, old.pin, old.load
PAIRS, ROLES = old.PAIRS, old.ROLES


def exact(a, b):
    return encoded(a) == encoded(b)


def digest(value):
    demand(type(value) is str and len(value) == 64 and
           all(c in '0123456789abcdef' for c in value), 'explicit frozen SHA256 required')


def require_unaccepted(value):
    demand(value.get('human_accepted') is False and value.get('actual_D') is None and
           value.get('model_discrepancies') is None, 'acceptance/result contamination')


def scenarios(value):
    demand(type(value) is list and len(value) == 4 and
           [(s['solid_reader'], s['dash_reader']) for s in value] ==
           list(itertools.product(ROLES, repeat=2)), 'four ordered fixed role scenarios')
    for s in value:
        demand(s.get('human_accepted') is False and s.get('actual_D') is None,
               'scenario acceptance contamination')
        old.elementary(s['segments'])


def compose(admission, f7, counts=(4779, 75, 264)):
    """Independent additive composition; counts may be reduced only in synthetic calls."""
    require_unaccepted(admission)
    require_unaccepted(f7)
    demand(f7.get('status') == 'conditional_F7_coverage_followup_not_admitted_support' and
           f7.get('region_id') == 'F7-Im2-early', 'F7 result identity')
    demand(tuple(p['pair'] for p in admission['pairs']) == PAIRS, 'old pair roster/order')
    old_cells, new_cells = admission['candidate_cells'], f7['new_candidate_cells']
    demand(type(old_cells) is list and type(new_cells) is list and
           len(old_cells) == counts[0] and len(new_cells) == counts[1], 'candidate count scope')
    selected_old = [c for c in old_cells if c['pair'] == 'F7']
    demand(len(selected_old) == counts[2] and
           exact(selected_old, f7['preserved_old_F7_candidate_cells']), 'old F7 cells changed')
    demand(all(c['pair'] == 'F7' for c in new_cells), 'non-F7 addition')
    ids = [c['id'] for c in old_cells + new_cells]
    demand(all(type(i) is str and i for i in ids) and len(set(ids)) == len(ids),
           'missing/duplicate candidate identity')
    prior_pair = next(p for p in admission['pairs'] if p['pair'] == 'F7')
    demand(exact(prior_pair['scenarios'], f7['before_scenarios']), 'old F7 scenarios changed')
    demand(exact(admission['axis_boxes'], f7['axis_boxes']), 'shared axes changed')
    for pair in admission['pairs']:
        scenarios(pair['scenarios'])
    scenarios(f7['after_scenarios'])
    result = copy.deepcopy(admission)
    result['candidate_cells'].extend(copy.deepcopy(new_cells))
    next(p for p in result['pairs'] if p['pair'] == 'F7')['scenarios'] = copy.deepcopy(f7['after_scenarios'])
    demand(exact(result['candidate_cells'][:len(old_cells)], old_cells), 'old candidate prefix changed')
    demand(exact([p for p in result['pairs'] if p['pair'] != 'F7'],
                 [p for p in admission['pairs'] if p['pair'] != 'F7']), 'other thirteen pairs changed')
    return result


def compose_metadata(admission, f7, previous_slots, slots):
    demand(len(previous_slots) == len(slots) == 42 and
           [s['id'] for s in previous_slots] == [s['id'] for s in slots], 'stable 42-slot roster')
    unchanged = [s['id'] for s in slots if s['pair'] != 'F7']
    demand(len(unchanged) == 39, '39 non-F7 slots required')
    for before, after in zip(previous_slots, slots):
        if before['pair'] != 'F7':
            demand(exact(before, after), 'non-F7 slot changed ' + before['id'])
    return {'old_candidate_cell_count': len(admission['candidate_cells']),
        'added_F7_candidate_cell_count': len(f7['new_candidate_cells']),
        'composed_candidate_cell_count': len(admission['candidate_cells']) + len(f7['new_candidate_cells']),
        'preserved_old_F7_candidate_cell_count': len(f7['preserved_old_F7_candidate_cells']),
        'unchanged_pairs': [p for p in PAIRS if p != 'F7'], 'unchanged_slot_ids': unchanged,
        'changed_slot_ids': [after['id'] for before, after in zip(previous_slots, slots)
                             if not exact(before, after)],
        'inventory_reference_base': 'connection-curve-comparison'}


def normalize_inventory(inventory):
    result = copy.deepcopy(inventory)
    demand(tuple(r['pair'] for r in result) == PAIRS, 'inventory pair roster')
    for row in result:
        demand(row['all_scenarios_preserved_in'] == 'admission-2026-10-08/run01.json',
               'unexpected independent helper reference')
        row['all_scenarios_preserved_in'] = F7_REF if row['pair'] == 'F7' else ADMISSION_REF
    return result


def check_packet(actual, previous, slots, inventory, assets, composition):
    require_unaccepted(previous)
    demand(previous.get('version') == 1 and type(previous.get('version')) is int and
           previous.get('status') == 'conditional_mapping_packet_pending_human',
           'prior packet identity')
    demand(type(actual.get('version')) is int and actual.get('version') == 2 and
           actual.get('packet_id') == PACKET_ID, 'versioned packet identity')
    expected = copy.deepcopy(previous)
    expected.update(version=2, packet_id=PACKET_ID, parent_packet=OLD_PACKET_REF,
                    f7_result=F7_REF, composition=composition, slots=slots,
                    inventory=inventory, assets=assets,
                    summary=dict(Counter(s['selection_status'] for s in slots)),
                    inputs=actual['inputs'], inputs_after=actual['inputs_after'])
    demand(exact(actual, expected), 'packet metadata/slots/inventory/pending states differ')
    require_unaccepted(actual)
    demand(actual.get('original_actual_D_sampling_fulfilled') is False,
           'original actual-D sampling not fulfilled')
    demand(actual.get('domain_kind') == 'C_H_primary_primary_not_actual_D' and
           actual.get('parent_result') == ADMISSION_REF and
           actual.get('assumptions') == ['Hidentity', 'Hsupport', 'Hink0'],
           'domain/reference/assumptions changed')
    for slot in slots:
        demand(slot['human_accepted'] is False, 'slot acceptance')
        for entry in slot['entries']:
            demand(entry['human_response'] is None and entry['human_status'] == 'uninspected',
                   'entry response contamination')


def include_declared(required, record, owner):
    demand(type(record.get('inputs')) is dict and
           exact(record['inputs'], record['inputs_after']), 'declared before/after closure differs')
    for name, expected in record['inputs'].items():
        demand(type(name) is str and bool(name), 'declared input path')
        old.add_pin(required, Path(owner) / name, expected)


def frozen_inputs():
    required = {}
    for name, sha in PRODUCER_PINS.items():
        digest(sha)
        old.add_pin(required, HERE / name, sha)
    for name, sha in FROZEN.items():
        old.add_pin(required, BASE / name, sha)
    previous = load(BASE / OLD_PACKET_REF)
    old_receipt = load(OLD_PACKET / 'independent-check.json')
    f7_receipt = load(F7 / 'independent-check-v2.json')
    demand(old_receipt['status'] == 'pass_conditional_packet_bookkeeping_only' and
           f7_receipt['status'] == 'pass_F7_source_bookkeeping_and_conditional_arithmetic_only',
           'prior receipt status')
    # These formats have DIFFERENT path owners. Never resolve receipt inputs at BASE.
    include_declared(required, previous, BASE)
    include_declared(required, old_receipt, BASE)
    include_declared(required, f7_receipt, F7)
    for name, expected in old_receipt['packet_pins'].items():
        old.add_pin(required, OLD_PACKET / name, expected)
    for name, expected in f7_receipt['producer_run_pins'].items():
        old.add_pin(required, F7 / name, expected)
    inherited, invocations, assets = old.required_inputs()
    for name, expected in inherited.items():
        old.add_pin(required, BASE / name, expected)
    return required, previous, invocations, assets


def matching_packets(run1, run2, expected_sha):
    digest(expected_sha)
    paths = [Path(run1), Path(run2)]
    demand(all(p.is_file() and not p.is_symlink() for p in paths), 'plain packet files required')
    demand(not os.path.samefile(*paths), 'two distinct packet files required')
    demand(paths[0].read_bytes() == paths[1].read_bytes() and
           pin(paths[0])['sha256'] == expected_sha, 'frozen packet bytes/hash differ')
    return [p.resolve() for p in paths]


def verify(run1, run2, expected_sha):
    paths = matching_packets(run1, run2, expected_sha)
    required, previous, invocations, assets = frozen_inputs()
    actual = load(paths[0])
    demand(exact(actual['inputs'], actual['inputs_after']), 'packet before/after differs')
    old.require_closure(actual['inputs'], required)
    before = {}
    for name, expected in actual['inputs'].items():
        old.add_pin(before, BASE / name, expected)
    for path in paths:
        old.add_pin(before, path, expected_sha)
    for name in ('independent_check.py', 'test_independent_check.py'):
        old.add_pin(before, HERE / name)
    admission, f7 = load(BASE / ADMISSION_REF), load(BASE / F7_REF)
    admission_before, f7_before = encoded(admission), encoded(f7)
    composed = compose(admission, f7)
    demand(encoded(admission) == admission_before and encoded(f7) == f7_before,
           'composition mutated originals')
    previous_slots, previous_inventory = old.reconstruct(admission, invocations)
    demand(exact(previous['slots'], previous_slots) and
           exact(previous['inventory'], previous_inventory), 'frozen old packet reconstruction differs')
    slots, raw_inventory = old.reconstruct(composed, invocations)
    demand(len(slots) == 42 and sum(len(s['entries']) for s in slots) == 84, '42/84 roster')
    composition = compose_metadata(admission, f7, previous['slots'], slots)
    inventory = normalize_inventory(raw_inventory)
    check_packet(actual, previous, slots, inventory, assets, composition)
    demand(actual['source_pdf'] == {'path': os.path.relpath(old.PDF, BASE),
           'sha256': old.PDF_SHA, 'physical_page': 76, 'printed_page': 25}, 'source PDF locator')
    omissions = []
    for name in required:
        damaged = dict(actual['inputs'])
        del damaged[name]
        try:
            old.require_closure(damaged, required)
        except ValueError:
            omissions.append(name)
        else:
            raise ValueError('required pin omission accepted ' + name)
    after = {name: pin(BASE / name) for name in before}
    demand(before == after, 'inputs changed during independent check')
    entries = [e for s in slots for e in s['entries']]
    mappings = [m for e in entries for role in ROLES for m in e['mappings'][role]]
    return {'status': 'pass_versioned_conditional_packet_bookkeeping_only',
        'packet_id': PACKET_ID, 'packet_pins': {os.path.relpath(p, HERE): pin(p) for p in paths},
        'composition': composition,
        'coverage': {'preserved_old_candidate_cells': 4779, 'added_F7_candidate_cells': 75,
            'composed_candidate_cells': 4854, 'preserved_old_F7_cells': 264,
            'pairs': 14, 'unchanged_other_pairs': 13, 'paired_slots': 42, 'model_entries': 84,
            'unchanged_non_F7_slots': 39, 'scenario_position_states': 168,
            'model_reader_alternative_lists': 168, 'native_coordinate_mappings': len(mappings),
            'image_headers': 13,
            'displacement_hulls': sum(v is not None for s in slots for v in s['displacement_m'].values()),
            'duplicate_model_role_flags': sum(bool(e['duplicate_entries'][r]) for e in entries for r in ROLES),
            'duplicate_paired_slot_flags': sum(bool(s['duplicate_paired_slots']) for s in slots)},
        'selection_summary': dict(Counter(s['selection_status'] for s in slots)),
        'required_producer_pin_count': len(required), 'producer_pin_count': len(actual['inputs']),
        'required_pin_omission_checks': sorted(omissions), 'inputs': before, 'inputs_after': after,
        'independence': 'Only SHA-pinned old independent reconstruction/header helpers imported; no producer composition, selection, mapping, annotation or comparison imports. Composition independently authored; prior method shared. Author also made F7 primary annotation and F7 v2 arithmetic checker. Not blind or independent historical corroboration.',
        'limits': 'Conditional packet bookkeeping/native mapping only. Source image headers, not pixels, checked. Old and new candidate geometry/eligibility retained through frozen admission and F7 arithmetic receipt, not newly reclassified. No source ownership, generating-curve enclosure, actual D, human response, physical metric or cause accepted.'}


def save_receipt(value, directory=HERE):
    path = Path(directory) / 'independent-check.json'
    old.save_exclusive(path, value)
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run1', type=Path, default=HERE / 'packet01.json')
    parser.add_argument('--run2', type=Path, default=HERE / 'packet02.json')
    parser.add_argument('--expected-sha', required=True)
    parser.add_argument('--save-receipt', action='store_true')
    args = parser.parse_args(argv)
    receipt = verify(args.run1, args.run2, args.expected_sha)
    if args.save_receipt:
        path = save_receipt(receipt)
        print(json.dumps({'status': receipt['status'], 'coverage': receipt['coverage'],
                          'pin': pin(path)}, sort_keys=True))
    else:
        print(encoded(receipt).decode(), end='')


if __name__ == '__main__':
    main()
