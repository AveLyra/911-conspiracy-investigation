"""Fixed-binding F7 v2 orchestration using only pinned independent components.

No producer, adapter, annotation or selection implementation is imported.
Historical verification fails closed until the coordinator freezes producer pins.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEGACY_SHA = 'b95e64271eab6c2bb6c9f981ddbda39bfa8159204ddfd81304f828b231f54304'
COMPLETION_SHA = '6d68e22e1410c76302e135a5b73adffde1374bcc51699225133400c9fc69ab4a'
READER_FILES = {'primary': 'reader-primary.json', 'peer': 'reader-peer-v2.json'}
PRESERVED = {
    'reader-primary.py': 'eb88429fabb627c72cdca859574daadd6f31d2fae68b44c3cd81961a6f65ca3b',
    'reader-primary.json': '4a3c323f83b25b93a88dd8db1b31fdcc77935e90b1494e3b3dc8f7eb40f8b734',
    'reader-primary-notes.md': '85e77c860c9fc701f76daa44d846ed7101f6b7ea0de5726bafa0540549963f28',
    'reader-peer.py': '3d4bf1e066755d0242f287ef02b48a40fc6f27a28941953471e089214c00d98b',
    'assess.py': 'e8a4af86fcaea4b34c8b86ea837fa6ec7d78455d6d576c89946818e5c0ca949a',
    'test_assess.py': 'a3945b67fd16e0f205360b0ac411a3dd086935a22a1bf73a52123c428528a36d',
    'independent_check.py': LEGACY_SHA,
    'test_independent_check.py': '4a644deada7fe66838757e319929e8711cab40b127f54ed5def18c891c0e8f18',
    'report.md': '6e8477bd2a5c270cdec40b2652bb55523f7c905418bd335401516e8334194d42',
    'validation.md': '930ebe0d208d19e6c1a544da9a764a748db7fc9a1d2c53456d444f931c8ff11b',
    'peer-reread-2026-10-08.md': '39368d4316acf06f53a7dfd4ed96eaecf45667d858ea4327c6b64b58b33a08d2',
    'COMPLETION-V2.md': COMPLETION_SHA,
}
# Coordinator-supplied hashes only; do not silently hash current draft code.
PRODUCER_PINS = {
    'assess_v2.py': 'ff75e080274c814f40816425d562ebf27b3fb71b514b7566506d688ce6000840',
    'test_assess_v2.py': '058e6bbc3b99d38fd68aa6b30a9c6650602a0e462f02c3172b6b99f9ccf865b3',
}


def import_legacy(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ValueError('plain pinned independent checker required')
    if hashlib.sha256(path.read_bytes()).hexdigest() != LEGACY_SHA:
        raise ValueError('prior independent checker changed')
    spec = importlib.util.spec_from_file_location('f7_v2_pinned_independent', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


old = import_legacy(HERE / 'independent_check.py')
require, exact, encoded = old.require, old.exact, old.encoded
pin, load, add_pin = old.pin, old.load, old.add_pin
BASE, OLD, ROLES = old.BASE, old.OLD, old.ROLES


def digest(value):
    require(type(value) is str and len(value) == 64 and
            all(c in '0123456789abcdef' for c in value), 'explicit frozen SHA256 required')


def fixed_inputs(directory, expected):
    """Check explicit caller-supplied freezes, never learn them from disk."""
    result = {}
    for name, sha in expected.items():
        digest(sha)
        path = Path(directory) / name
        require(path.is_file() and not path.is_symlink(), 'plain fixed file required ' + name)
        add_pin(result, path, sha)
    return result


def bound_readers(reader_shas, before, directory=HERE):
    """Only these two filenames are valid; source identity is not version-renamed."""
    require(type(reader_shas) is dict and set(reader_shas) == set(ROLES),
            'two explicit frozen reader hashes')
    readers, paths = {}, {}
    for role in ROLES:
        digest(reader_shas[role])
        path = Path(directory) / READER_FILES[role]
        for file in (path, path.with_suffix('.py')):
            require(file.is_file() and not file.is_symlink(),
                    'plain fixed reader path required ' + file.name)
        add_pin(before, path, reader_shas[role])
        data = load(path)
        require(type(data) is dict and data.get('reader') == role and
                data.get('region_id') == old.REGION and data.get('pair') == 'F7' and
                data.get('source') == 'Im2.jpg', 'bound reader identity/role')
        old.pin_shape(data['script_pin'])
        add_pin(before, path.with_suffix('.py'), data['script_pin'])
        readers[role], paths[role] = data, path
    return readers, paths


def required_inputs(prior, old_receipt, readers, paths, frozen):
    result = dict(frozen)
    for name, sha in {**old.FIXED, **old.METHOD_PINS}.items():
        add_pin(result, HERE / name, sha)
    add_pin(result, HERE / 'CONSUMER-COMPATIBILITY.md', old.COMPATIBILITY_SHA)
    require(prior['inputs'] == prior['inputs_after'] and len(prior['inputs']) == 205,
            'old 205-input closure')
    old.include_map(result, prior['inputs'], BASE)
    require(old_receipt['inputs'] == old_receipt['inputs_after'] and
            len(old_receipt['inputs']) == 209, 'old independent 209-input closure')
    require(old_receipt['required_producer_pin_count'] == 205 and
            old_receipt['producer_pin_count'] == 205, 'old receipt producer scope')
    old.include_map(result, old_receipt['inputs'], BASE)
    old.include_map(result, old_receipt['producer_run_pins'], OLD)
    context = load(HERE / 'context01.json')
    require(len(context['inputs']) == 9, 'context nine-input map')
    old.closure(result, [HERE / 'context01.json', HERE / 'context02.json'])
    for role in ROLES:
        data = readers[role]
        required_reader = {name: pin(HERE / name) for name in
                           ('PROTOCOL.md', 'READERS.md', 'context01.json', 'context02.json')}
        required_reader.update(context['inputs'])
        # The unchanged primary predates v2; only the additive peer owes these pins.
        if role == 'peer':
            for name in ('COMPLETION-V2.md', 'reader-peer.py', 'peer-reread-2026-10-08.md'):
                required_reader[name] = frozen[name]
        old.require_map(data['inputs'], required_reader)
        old.closure(result, [paths[role]])
    return result


def old_state(actual, prior):
    cells = [c for c in prior['candidate_cells'] if c['pair'] == 'F7']
    scenarios = next(p['scenarios'] for p in prior['pairs'] if p['pair'] == 'F7')
    require(exact(actual['preserved_old_F7_candidate_cells'], cells) and
            exact(actual['before_scenarios'], scenarios), 'old F7 objects not preserved')
    require(actual['unchanged_other_pairs_reference'] ==
            os.path.relpath(OLD / 'run01.json', HERE), 'old other-pair reference')
    return cells, scenarios


def reader_paths(readings, paths):
    require(type(readings) is list and len(readings) == 2 and
            [r.get('reader_path') for r in readings] ==
            [os.path.relpath(paths[role], BASE) for role in ROLES],
            'explicit ordered v2 reader provenance')


def identical_runs(run1, run2, expected_sha):
    digest(expected_sha)
    run1, run2 = Path(run1), Path(run2)
    require(all(p.is_file() and not p.is_symlink() for p in (run1, run2)),
            'plain producer run files required')
    require(not os.path.samefile(run1, run2) and run1.read_bytes() == run2.read_bytes(),
            'distinct identical output copies')
    require(pin(run1)['sha256'] == expected_sha, 'frozen result hash')
    return run1.resolve(), run2.resolve()


def verify(run1, run2, expected_sha, reader_shas):
    # Must finish all fixed guards before opening any new reader or result JSON.
    frozen = fixed_inputs(HERE, {**PRESERVED, **PRODUCER_PINS})
    require(reader_shas.get('primary') == PRESERVED['reader-primary.json'],
            'unchanged primary hash required')
    run1, run2 = identical_runs(run1, run2, expected_sha)
    actual = load(run1)
    old.acceptance(actual)
    before = dict(frozen)
    readers, paths = bound_readers(reader_shas, before)
    reader_paths(actual['new_readings'], paths)
    prior, old_receipt = load(OLD / 'run01.json'), load(OLD / 'independent-check.json')
    required = required_inputs(prior, old_receipt, readers, paths, frozen)
    require(actual['inputs'] == actual['inputs_after'], 'current producer before/after')
    old.require_map(actual['inputs'], required)
    old.include_map(before, actual['inputs'], HERE)
    for path in (run1, run2):
        add_pin(before, path, expected_sha)
    for path, sha in old.HELPERS.values():
        add_pin(before, HERE / path, sha)
    for name in ('independent_check_v2.py', 'test_independent_check_v2.py'):
        add_pin(before, HERE / name)
    add_pin(before, HERE / 'context-check.json', old.CONTEXT_RECEIPT_SHA)
    context_receipt = load(HERE / 'context-check.json')
    require(context_receipt['pins_before'] == context_receipt['pins_after'] and
            context_receipt['distinct_cells'] == 10032 and
            context_receipt['source_records_checked'] == 20064, 'context receipt scope/pins')
    old.include_map(before, context_receipt['pins_before'], HERE)
    require((HERE / 'context01.json').read_bytes() == (HERE / 'context02.json').read_bytes(),
            'context copies')
    context = load(HERE / 'context01.json')
    pixels = {(r['x'], r['y']): r['rgb'] for r in context['cells']['F7']}
    require(len(pixels) == 10032, 'pinned context scope')
    geometry, row_helper, book = old.helper('geometry'), old.helper('rows'), old.helper('bookkeeping')
    representation = load(BASE / 'pypdf-representation01.json')
    invocation = next(v for v in representation['image_invocations'] if v['name'] == 'Im2')
    require(invocation['native_dimensions'] == [741, 88], 'new strip dimensions')
    axes = {panel + '-' + reader: row_helper.axis_intervals(panel, reader)
            for panel in ('F', 'E') for reader in ('root', 'independent')}
    require(exact(actual['axis_boxes'], axes) and exact(prior['axis_boxes'], axes),
            'fixed axis alternatives')
    readings, roles, regions, white = [], {}, {}, {}
    counts = Counter()
    for role in ROLES:
        data = readers[role]
        snapshot = encoded(data)
        bands = old.annotation(data, role, book)
        path = os.path.relpath(paths[role], BASE)
        region = {'pair': 'F7', 'source': 'Im2', 'target_box': old.TARGET}
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
    comparison, summary = old.comparisons(readers, book)
    require(exact(actual['reader_comparison'], comparison) and
            exact(actual['reader_difference_summary'], summary), 'reader set arithmetic/summary')
    require(exact(actual['selected_exact_white'], white), 'selected-white diagnostics')
    old_cells, old_scenarios = old_state(actual, prior)
    coverage = []
    for phase, cells, scenarios in [
            ('before', old_cells, old_scenarios),
            ('after', old_cells + new_cells, actual['after_scenarios'])]:
        require(type(scenarios) is list and len(scenarios) == 4, 'four fixed role scenarios')
        for index, (solid, dash) in enumerate(itertools.product(ROLES, repeat=2)):
            chosen = [c for c in cells if (c['route'] == 'solid' and c['role'] == solid) or
                      (c['route'] == 'dash' and c['role'] == dash)]
            expected = geometry.scenario_check(scenarios[index], chosen, 'F7', solid, dash, axes)
            counts[phase + '_scenarios'] += 1
            counts[phase + '_elementary_segments'] += len(expected['segments'])
            counts[phase + '_paired_runs'] += len(expected['paired_runs'])
            counts[phase + '_length_extrema'] += 4
            coverage.append({'phase': phase, 'solid_reader': solid, 'dash_reader': dash,
                'segments': len(expected['segments']), 'paired_segments': expected['paired_segment_count'],
                'paired_runs': len(expected['paired_runs'])})
    omissions = []
    for name in required:
        altered = dict(actual['inputs'])
        del altered[name]
        try:
            old.require_map(altered, required)
        except ValueError:
            omissions.append(name)
        else:
            raise ValueError('omitted required pin accepted ' + name)
    after = {name: pin(HERE / name) for name in before}
    require(before == after, 'inputs changed during independent check')
    counts.update(new_candidate_cells=len(new_cells), preserved_old_F7_cells=len(old_cells),
                  reader_comparison_arrays=(220 + 110) * 3 * 5, old_readings_by_reference=44,
                  old_source_records_by_reference=14420)
    return {'status': 'pass_F7_source_bookkeeping_and_conditional_arithmetic_only',
        'coverage': dict(counts), 'scenarios': coverage,
        'reader_comparison_summary': summary, 'selected_exact_white': white,
        'required_producer_pin_count': len(required), 'producer_pin_count': len(actual['inputs']),
        'required_pin_omission_checks': sorted(omissions), 'inputs': before, 'inputs_after': after,
        'producer_run_pins': {os.path.relpath(p, HERE): pin(p) for p in (run1, run2)},
        'reader_original_pins': {role: pin(paths[role]) for role in ROLES},
        'independence': 'Versioned orchestration reuses the SHA-pinned prior independent checker and its raw-row/CTM, midpoint-partition and integer-mask/truth-table components. No producer, annotation, selection, adapter, calculator or event-sweep imports. This wrapper author also authored the frozen primary source reading; this is arithmetic independence, not source-reader independence.',
        'limits': 'All new rows and material F7 geometry/arithmetic checked; old 14420 rows retained by frozen reference, not reclassified. Four role combinations are version-role scenarios, not necessarily the same agent across regions. Literal-script expansion is parent replay, not executed here. Coverage/view receipts are attestations, not proof of perception. Context fidelity inherited from the pinned full-cell check. No source ownership, H hypothesis, generating-curve containment, physical support, human acceptance or cause result.'}


def save_receipt(receipt, directory=HERE):
    path = Path(directory) / 'independent-check-v2.json'
    with path.open('xb') as output:
        output.write(encoded(receipt))
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run1', type=Path, default=HERE / 'run-v2-01.json')
    parser.add_argument('--run2', type=Path, default=HERE / 'run-v2-02.json')
    parser.add_argument('--expected-sha', required=True)
    parser.add_argument('--primary-sha', required=True)
    parser.add_argument('--peer-sha', required=True)
    parser.add_argument('--save-receipt', action='store_true')
    args = parser.parse_args(argv)
    receipt = verify(args.run1, args.run2, args.expected_sha,
                     {'primary': args.primary_sha, 'peer': args.peer_sha})
    if args.save_receipt:
        path = save_receipt(receipt)
        print(json.dumps({'output': pin(path), 'coverage': receipt['coverage']}, sort_keys=True))
    else:
        print(encoded(receipt).decode(), end='')


if __name__ == '__main__':
    main()
