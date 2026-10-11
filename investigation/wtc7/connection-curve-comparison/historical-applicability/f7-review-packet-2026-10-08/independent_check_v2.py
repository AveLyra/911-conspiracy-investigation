"""Independent dependency-only repair gate; preserves the failed first checker.

Reuses only frozen independent-checker code, never the packet producers.
The author's prior F7 annotation/checker lineage remains explicitly disclosed.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREFIX = 'historical-applicability/f7-review-packet-2026-10-08/'
PRIOR_PREFIX = 'historical-applicability/envelope-packet-2026-10-08/'
CHECKER_SHA = 'b7d1c58ecac301a008a5d521b18a93292ec9b79aa8cc8fab78a15b4cf4c689a7'
CHECKER_TEST_SHA = '455cc0fa4193c0c1196c830b07a3381d5cf77edc6bbc978f08b0d44d6f7eadfc'
CANDIDATE_SHA = 'ceadeebf040913d5654c20bce5d55dca5ae2b7e4d6612821818f67af6024fb1c'
REPAIR_SHA = '0f60d4b0592840fcdce8f40cebb5e94b9fab8d76c73fb1683c9a9260a0af4770'
REPAIR_PINS = {
    'DEPENDENCY-REPAIR.md': REPAIR_SHA,
    'packet_v2.py': '92d52738b35072912bc6d9a00f3d97f52922e3f00d87bf691d1d1ee49ea61bb1',
    'test_packet_v2.py': 'd05dede03d4feafcfac4167becd47383b57992d7695611bdbc64f93d551fa7c4',
    'packet01.json': CANDIDATE_SHA,
    'packet02.json': CANDIDATE_SHA,
}
MISSING_PRIOR = sorted(PRIOR_PREFIX + name for name in (
    'independent_check.py', 'test_independent_check.py',
    'envelope_math.py', 'test_envelope_math.py'))


def import_previous(directory):
    directory = Path(directory)
    for name, expected in (('independent_check.py', CHECKER_SHA),
                           ('test_independent_check.py', CHECKER_TEST_SHA)):
        path = directory / name
        if not path.is_file() or path.is_symlink():
            raise ValueError('plain frozen checker files required')
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('frozen independent checker/test changed: ' + name)
    spec = importlib.util.spec_from_file_location('f7_packet_independent_before_repair',
                                                 directory / 'independent_check.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


previous = import_previous(HERE)
old = previous.old
demand, encoded, exact, pin, load = (previous.demand, previous.encoded,
                                    previous.exact, previous.pin, previous.load)
BASE = previous.BASE


def required_inputs():
    required, _, _, _ = previous.frozen_inputs()
    demand(len(required) == 264, 'original required closure must retain 264 pins')
    original_required = copy.deepcopy(required)
    for name, sha in REPAIR_PINS.items():
        old.add_pin(required, HERE / name, sha)
    demand(len(required) == 269, 'repaired required closure must contain 269 pins')
    return required, original_required


def require_rejected_omissions(candidate, original_required):
    demand(type(candidate.get('inputs')) is dict and
           exact(candidate['inputs'], candidate.get('inputs_after')),
           'rejected candidate before/after differs')
    missing = sorted(name for name in original_required if name not in candidate['inputs'])
    demand(missing == MISSING_PRIOR, 'original four-pin failure not preserved')
    present = {name: value for name, value in original_required.items() if name not in missing}
    demand(exact(candidate['inputs'], present), 'rejected candidate listed pins differ')
    return missing


def require_dependency_only(actual, candidate, required):
    demand(type(actual.get('inputs')) is dict and
           exact(actual['inputs'], actual.get('inputs_after')),
           'repair before/after differs')
    old.require_closure(actual['inputs'], required)
    demand(exact(actual['inputs'], required), 'repair must have exactly the required pin map')
    without_inputs = lambda record: {key: value for key, value in record.items()
                                     if key not in ('inputs', 'inputs_after')}
    demand(exact(without_inputs(actual), without_inputs(candidate)),
           'dependency repair changed a non-input field')


def verify(run1, run2, expected_sha):
    paths = previous.matching_packets(run1, run2, expected_sha)
    rejected_paths = previous.matching_packets(HERE / 'packet01.json',
                                               HERE / 'packet02.json', CANDIDATE_SHA)
    demand(not any(os.path.samefile(a, b) for a in paths for b in rejected_paths),
           'repaired outputs may not alias rejected candidates')
    required, original_required = required_inputs()
    actual = load(paths[0])
    for path in rejected_paths:
        candidate = load(path)
        missing = require_rejected_omissions(candidate, original_required)
        require_dependency_only(actual, candidate, required)
    before = copy.deepcopy(required)
    for path in paths:
        old.add_pin(before, path, expected_sha)
    for name, sha in (('independent_check.py', CHECKER_SHA),
                      ('test_independent_check.py', CHECKER_TEST_SHA),
                      ('independent_check_v2.py', None),
                      ('test_independent_check_v2.py', None)):
        old.add_pin(before, HERE / name, sha)
    # Full unchanged independent composition, 42-slot reconstruction, mappings,
    # headers, pending states and original 264 omission probes execute here.
    receipt = previous.verify(paths[0], paths[1], expected_sha)
    demand(receipt['producer_pin_count'] == 269, 'repaired producer pin count')
    demand(all(before.get(name) == value for name, value in receipt['inputs'].items()),
           'inherited checker saw different inputs')
    omissions = []
    for name in required:
        damaged = copy.deepcopy(actual)
        del damaged['inputs'][name]
        damaged['inputs_after'] = copy.deepcopy(damaged['inputs'])
        try:
            require_dependency_only(damaged, candidate, required)
        except ValueError:
            omissions.append(name)
        else:
            raise ValueError('repaired required pin omission accepted ' + name)
    after = {name: pin(BASE / name) for name in before}
    demand(before == after, 'inputs changed during repaired independent check')
    receipt.update(required_producer_pin_count=len(required),
                   required_pin_omission_checks=sorted(omissions),
                   inputs=before, inputs_after=after)
    receipt['dependency_repair'] = {
        'declaration': PREFIX + 'DEPENDENCY-REPAIR.md', 'declaration_sha256': REPAIR_SHA,
        'rejected_candidate_pins': {os.path.relpath(p, HERE): pin(p) for p in rejected_paths},
        'rejected_candidate_status': 'dependency_closure_failed_not_released',
        'original_missing_required_pins': missing,
        'non_input_fields_exactly_equal_rejected_candidates': True,
        'original_required_pin_count': len(original_required),
        'original_candidate_pin_count': len(candidate['inputs']),
    }
    receipt['independence'] += (' Dependency-only repair wrapper imports the SHA-pinned '
        'unchanged independent checker, not either producer. It retains and rechecks '
        'the original closure failure and compares every non-input field to both candidates.')
    return receipt


def save_receipt(value, directory=HERE):
    path = Path(directory) / 'independent-check-v2.json'
    old.save_exclusive(path, value)
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run1', type=Path, default=HERE / 'packet-v2-01.json')
    parser.add_argument('--run2', type=Path, default=HERE / 'packet-v2-02.json')
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
