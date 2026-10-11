"""Versioned dependency closure repair; frozen version-1 arithmetic reused."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
V1_SCRIPT_SHA = '18f5862d014c5e9848cd6332da3929437c7ff93031e3ca255730d1f9e0dfc3f0'
V1_RESULT_SHA = 'eba3bb5fd8913751052c68b71d0efad3f8fd0da12977a579a85fd793c7406ce7'


def producer():
    import hashlib
    path = HERE/'extend.py'
    if hashlib.sha256(path.read_bytes()).hexdigest() != V1_SCRIPT_SHA:
        raise ValueError('Frozen version-1 producer changed')
    spec = importlib.util.spec_from_file_location('approach_extension_v1', path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def merge(pins, root, parent, values, pin):
    if type(values) is not dict:
        raise ValueError('Dependency map required')
    for name, expected in values.items():
        if not isinstance(name, str) or type(expected) is not dict or set(expected) != {'sha256','bytes'}:
            raise ValueError('Unsupported dependency-map entry')
        path = (parent/name).resolve()
        key = str(path.relative_to(root))
        if key in pins and pins[key] != expected:
            raise ValueError('Conflicting declared pins: '+key)
        actual = pin(path)
        if actual != expected:
            raise ValueError('Changed declared dependency: '+key)
        pins[key] = actual


def build():
    e = producer()
    prior = json.loads((HERE/'run01.json').read_text())
    before = {}
    for name in ('run01.json','run02.json'):
        value = e.pin(HERE/name)
        e.require(value['sha256'] == V1_RESULT_SHA, 'Frozen version-1 result changed')
        before[str((HERE/name).relative_to(BASE))] = value
    e.require(prior['inputs'] == prior['inputs_after'], 'Version-1 receipt mismatch')
    merge(before, BASE, BASE, prior['inputs'], e.pin)
    app = BASE/e.APP
    roots = [(app/f'reader-{pair}-{role}.json', ('inputs',))
             for pair in ('E3','E4') for role in ('primary','peer')]
    roots += [(app/name, ('inputs',)) for name in ('context01.json','context02.json')]
    roots += [(app/'independent-check.json', ('inputs','inputs_after'))]
    roots += [(app/f'comparison-{pair}-{run}.json', ('input_pins','dependencies'))
              for pair in ('E3','E4') for run in ('01','02')]
    roots += [(app/'../energy345/context01.json', ('inputs',))]
    declarations = []
    for path, fields in roots:
        path = path.resolve()
        key = str(path.relative_to(BASE))
        e.require(key in before, 'Unpinned dependency-map owner: '+key)
        e.require(e.pin(path) == before[key], 'Changed dependency-map owner: '+key)
        data = json.loads(path.read_text())
        for field in fields:
            merge(before, BASE, path.parent, data[field], e.pin)
            declarations.append({'path':key, 'field':field, 'relative_to':str(path.parent.relative_to(BASE))})
        if path.name.startswith('reader-'):
            merge(before, BASE, path.parent, {path.with_suffix('.py').name:data['script_pin']}, e.pin)
            declarations.append({'path':key, 'field':'script_pin', 'relative_to':str(path.parent.relative_to(BASE))})
    for name in ('PROTOCOL-V2.md','extend_v2.py','test_extend_v2.py'):
        before[str((HERE/name).relative_to(BASE))] = e.pin(HERE/name)
    result = e.build()
    e.require(e.encode(result) == (HERE/'run01.json').read_bytes(), 'Version-1 replay differs')
    # Exact prior-result replay above precedes the only permitted wrapper changes.
    result = copy.deepcopy(result)
    result['status'] = 'conditional_preparation_extension_v2_not_accepted_measurement'
    result['version'] = 2
    result['repair_provenance'] = {
        'prior_outputs_preserved': [str((HERE/name).relative_to(BASE)) for name in ('run01.json','run02.json')],
        'prior_verification_limit': 'Version 1 omitted three declared upstream pins; it was not fully protocol-verified.',
        'dependency_map_roots': declarations,
        'substantive_payload_identical_to_v1': True,
        'new_scientific_result': False}
    after = {name:e.pin(BASE/name) for name in before}
    e.require(before == after, 'Input changed during repaired extension')
    result['inputs'], result['inputs_after'] = before, after
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', choices=('01','02'))
    args = parser.parse_args()
    target = HERE/f'run-v2-{args.run}.json'
    if target.exists():
        raise FileExistsError('Existing version-2 output preserved')
    e = producer()
    result = build()
    e.save(target, e.encode(result))
    print(json.dumps({'output':e.pin(target),'pins':len(result['inputs']),
                      'windows':result['conditional_window_counts'],'version':result['version']}))
