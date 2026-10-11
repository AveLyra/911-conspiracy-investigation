"""Inventory-qualification-only correction; frozen numerical results unchanged."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
V1_SHA = '79f63ff2618de2d53ad7467a19372b1f5ba97ff36677f6ca61d13d51ff8c6d8f'
METHOD_SHA = 'a085e680a4d3d6a892429e12adb30364d1858b7d0799054652afe9dfec53b5b6'
APPEND = {
    'F5': 'Older Im2/Im4 peer generic same-column band references can flag an unrelated route; those original references and conditional exclusions remain unchanged.',
    'F6': 'A repeated fragment ID across an unknown span does not establish continuity.'
}


def helpers():
    path = HERE/'extend.py'
    if hashlib.sha256(path.read_bytes()).hexdigest() != METHOD_SHA:
        raise ValueError('Frozen version-1 producer changed')
    spec = importlib.util.spec_from_file_location('frozen_force56_v1', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def amended(prior):
    if type(prior.get('version')) is not int or prior['version'] != 1 or prior.get('status') != 'conditional_force56_extension_not_accepted_measurement':
        raise ValueError('Exact version-1 input required')
    result = copy.deepcopy(prior)
    seen = set()
    for item in result['inventory']['pairs']:
        pair = item['pair']
        if pair in APPEND:
            if pair in seen or APPEND[pair] in item['identity_and_topology_limits']:
                raise ValueError('Duplicate correction or pair')
            seen.add(pair)
            item['identity_and_topology_limits'] += ' '+APPEND[pair]
    if seen != set(APPEND):
        raise ValueError('Missing corrected pair')
    return result


def build():
    e = helpers(); before = {}
    for name in ('run01.json', 'run02.json'):
        e.include(before, HERE/name, V1_SHA)
    e.require((HERE/'run01.json').read_bytes() == (HERE/'run02.json').read_bytes(), 'Version-1 copies differ')
    prior = json.loads((HERE/'run01.json').read_text())
    e.require(e.exact(prior['inputs'], prior['inputs_after']), 'Version-1 maps differ')
    for name, expected in prior['inputs'].items():
        e.include(before, BASE/name, expected)
    for name in ('PROTOCOL-V2.md', 'extend_v2.py', 'test_extend_v2.py'):
        e.include(before, HERE/name)
    result = amended(prior)
    # Invert the only substantive edit and compare the entire payload.
    unchanged = copy.deepcopy(result)
    for item in unchanged['inventory']['pairs']:
        if item['pair'] in APPEND:
            suffix = ' '+APPEND[item['pair']]
            item['identity_and_topology_limits'] = item['identity_and_topology_limits'][:-len(suffix)]
    e.require(e.exact(unchanged, prior), 'Unexpected version-2 substantive change')
    result['version'] = 2
    result['status'] = 'conditional_force56_extension_v2_not_accepted_measurement'
    result['correction_provenance'] = {
        'prior_outputs_preserved': [e.key(HERE/name) for name in ('run01.json','run02.json')],
        'reason': 'Version-1 current-inventory prose omitted older annotation-reference and continuity qualifications.',
        'appended_qualifications': APPEND.copy(), 'all_numerical_and_original_payload_unchanged': True}
    after = {name: e.pin(BASE/name) for name in before}
    e.require(e.exact(before, after), 'Inputs changed during correction')
    result['inputs'], result['inputs_after'] = before, after
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', choices=('01','02'))
    args = parser.parse_args()
    path = HERE/f'run-v2-{args.run}.json'
    if path.exists():
        raise FileExistsError('Existing version-2 output preserved')
    e = helpers(); result = build(); e.save(path, e.encode(result))
    print(json.dumps({'output': e.pin(path), 'pins': len(result['inputs']),
                      'windows': result['conditional_window_counts'], 'version': result['version']}))
