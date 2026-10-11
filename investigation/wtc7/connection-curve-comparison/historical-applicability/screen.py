"""Classify frozen F3 annotation geometry; no pixels, physical units or curve fit."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import platform

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'f3-descending-corridor'
EXPECTED = {
    'reader-root.json': '50059b664dc330543d6c6c174bc6ea87968d1fe631c8f8879de9cef4683cdd2c',
    'reader-independent.json': '40c763898afa44619aaf0dfb9a198b44d7c51aff0ed15b4f51e303192d39e6c6',
    'reconcile.py': '0b0c0aaa58afbf780e377d67b0d371fed0d07169c0100e132401b588fdec2f39',
}


def pin(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def validator():
    path = OLD / 'reconcile.py'
    if pin(path)['sha256'] != EXPECTED[path.name]:
        raise ValueError('Changed frozen validator')
    spec = importlib.util.spec_from_file_location('frozen_corridor_validator', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate


def classify(entry):
    """Input must first pass the pinned complete-reader validator."""
    core, fringe = set(entry['core_rows']), set(entry['fringe_rows'])
    outer = sorted(core | fringe)
    fragment = entry.get('fragment_id')
    explicit = isinstance(fragment, str) and bool(fragment.strip())
    members = entry.get('fragment_membership')
    reasons = []
    if entry['status'] != 'identified_local_fragment':
        reasons.append('nonidentified_status')
    if not core:
        reasons.append('empty_core')
    if not outer:
        reasons.append('empty_outer')
    if outer and outer != list(range(outer[0], outer[-1] + 1)):
        reasons.append('disconnected_outer')
    if entry['boundary_flags']:
        reasons.append('boundary')
    if not explicit:
        reasons.append('missing_identifier')
    if members is not None:
        if len(members) > 1:
            reasons.append('multiple_fragment_members')
        elif len(members) == 1:
            matching = explicit and list(members) == [fragment]
            if matching:
                matching = all(members[fragment][k] == entry[k]
                               for k in ('core_rows', 'fringe_rows'))
            if not matching:
                reasons.append('inconsistent_single_fragment_identity')
        elif outer or explicit:
            reasons.append('inconsistent_single_fragment_identity')
    eligible = not reasons
    rect = [entry['column'], outer[0], entry['column'] + 1, outer[-1] + 1] if eligible else None
    return {'source_record': entry, 'eligible': eligible, 'reasons': reasons,
            'native_cell_rectangle': rect}


def summarize(rows):
    result = {}
    for route in ('all', 'solid', 'dash'):
        subset = [r for r in rows if route == 'all' or r['source_record']['route'] == route]
        eligible = sum(r['eligible'] for r in subset)
        result[route] = {'entries': len(subset), 'eligible': eligible,
                         'excluded': len(subset) - eligible,
                         'reason_counts_nonexclusive': dict(Counter(reason for r in subset for reason in r['reasons']))}
    return result


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')


def run(target):
    if target.exists():
        raise FileExistsError('Existing output preserved')
    paths = [OLD / name for name in EXPECTED]
    paths += [HERE / name for name in ('PROTOCOL.md', 'screen.py', 'test_screen.py')]
    before = {str(p.relative_to(HERE.parent)): pin(p) for p in paths}
    for name, expected in EXPECTED.items():
        if pin(OLD / name)['sha256'] != expected:
            raise ValueError('Changed frozen input: ' + name)
    validate = validator()
    results = {}
    for name in ('root', 'independent'):
        source = json.loads((OLD / ('reader-' + name + '.json')).read_text())
        rows = [classify(e) for e in validate(source)]
        results[name] = {'reader': source['reader'], 'rows': rows, 'summary': summarize(rows)}
    after = {str(p.relative_to(HERE.parent)): pin(p) for p in paths}
    if before != after:
        raise ValueError('Input changed during screen')
    output = {'status': 'complete', 'python': platform.python_version(),
              'inputs': before, 'inputs_after': after, 'readers': results,
              'human_accepted': False,
              'limits': 'Annotation geometry only. Rectangles enclose selected cells, not validated historical curves. No physical ordinates, support union, model discrepancy or source re-reading.'}
    save(target, output)
    return {name: result['summary'] for name, result in results.items()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', choices=('run01', 'run02'))
    args = parser.parse_args()
    print(json.dumps(run(HERE / (args.run + '.json')), sort_keys=True))
