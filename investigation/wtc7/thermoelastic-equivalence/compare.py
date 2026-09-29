#!/usr/bin/env python3
"""Post-freeze exact crosscheck and replay; never an independent observation."""
from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import platform

BASE = Path(__file__).resolve().parent
PINS = {
    'PROTOCOL.md': 'd9df71946dd097a4b6154d07fb07c8e0dff8206a91c1393f8251ceac9b817bc0',
    'calculate.py': '635b5a6b091e529e25c6c804b60fb18c46ba82705863615633890712a7131681',
    'oracle.py': '3cea4c4b1a4d9cd2efdeaeec121ff897013b1a708ff5a4fba01c822f391ab282',
    'run01.json': '4df08eff5cea878172efa4e2b6d5cf8d91b8310e4e4bbb92953e809c3761d5f3',
    'run02.json': '4df08eff5cea878172efa4e2b6d5cf8d91b8310e4e4bbb92953e809c3761d5f3',
    'oracle-run01.json': '349a15b2bfa9682f263c51610de4aefa22dd058b4d51d3b8c748c9f67d035e73',
    'oracle-run02.json': '349a15b2bfa9682f263c51610de4aefa22dd058b4d51d3b8c748c9f67d035e73',
}


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, BASE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition, label):
    if not condition:
        raise ValueError(label)


def equal_number(a, b, label):
    require(isinstance(a, str) and isinstance(b, str), label + ': fraction string required')
    require(Q(a) == Q(b), label)


def main():
    for name, expected in PINS.items():
        require(hashlib.sha256((BASE / name).read_bytes()).hexdigest() == expected, 'pin: ' + name)
    root = json.loads((BASE / 'run01.json').read_text())
    independent = json.loads((BASE / 'oracle-run01.json').read_text())
    rmodule, omodule = load_module('root_replay', 'calculate.py'), load_module('oracle_replay', 'oracle.py')
    require(rmodule.result() == root, 'complete root result replay')
    replay = omodule.encode(omodule.run())
    require(replay == {key: independent[key] for key in replay}, 'complete oracle run replay')
    require(len(replay['states']) == 9, 'all nine oracle states retained')
    require(len(replay['checks']) == 125 and replay['failed_checks'] == 0, 'oracle check coverage')
    counts = Counter()
    aliases = {'cold': 'cold', 'uniform': 'variable_modulus_uniform',
               'variable': 'variable_modulus_nonuniform',
               'constant_uniform': 'constant_modulus_uniform',
               'constant_variable': 'constant_modulus_nonuniform'}
    require(set(root['cases']) == set(aliases), 'root fixture set')
    for name, independent_name in aliases.items():
        a, b = root['cases'][name], independent['states'][independent_name]
        pairs = [(a['free_thermal_extension'], b['thermal_extension_H']),
                 (a['axial_compliance'], b['axial_compliance_C']),
                 (a['beta'], b['input']['beta'])]
        require(len(a['theta']) == len(b['input']['theta']) == 3, 'temperature lengths')
        pairs.extend(zip(a['theta'], b['input']['theta']))
        require(len(a['probe_loads']) == 3 and set(b['load_probes']) == {'zero', 'p', 'p2'}, 'probe set')
        for ra, label in zip(a['probe_loads'], ('zero', 'p', 'p2')):
            rb = b['load_probes'][label]
            for ka, kb in [('load', 'force'), ('total_extension', 'total_extension'),
                           ('increment_from_own_cold_load', 'increment_from_cold_at_same_probe_load'),
                           ('increment_from_reference_preload', 'increment_from_common_cold_preload_p')]:
                pairs.append((ra[ka], rb[kb]))
        pairs.extend([(a['stress_free_clamp_total_force'], b['clamps']['cold_stress_free']['total_force']),
                      (a['preloaded_clamp_total_force'], b['clamps']['cold_preloaded']['total_force']),
                      (a['preloaded_clamp_force_increment'], b['clamps']['cold_preloaded']['force_change_from_initial'])])
        for key, idx in [('identified_at_zero_and_p', 0), ('identified_at_p_and_p2', 1)]:
            require(len(a[key]) == len(b['two_load_identifications'][idx]['H_C']) == 2, 'inverse pair lengths')
            pairs.extend(zip(a[key], b['two_load_identifications'][idx]['H_C']))
        for index, (x, y) in enumerate(pairs):
            equal_number(x, y, f'{name}:{index}')
            counts[name] += 1
    # Adapter controls: equivalent notation accepted; unequal or non-rational
    # content cannot turn into a passing scientific comparison.
    equal_number('2', '2/1', 'equivalent representations')
    for a, b in [('1/1000', '1/999'), ('not-a-fraction', '1'), (True, '1')]:
        try:
            equal_number(a, b, 'deliberate adapter mismatch')
        except (ValueError, TypeError):
            pass
        else:
            raise ValueError('adapter accepted a deliberate mismatch')
    print(json.dumps({'status': 'PASS', 'python': platform.python_version(),
        'pinned_files': len(PINS), 'root_complete_replay': True,
        'oracle_complete_run_replay': True, 'oracle_states': 9,
        'oracle_checks': 125, 'oracle_check_kinds': dict(Counter(c['kind'] for c in replay['checks'])),
        'common_case_exact_scalars': dict(counts), 'total_exact_scalar_comparisons': sum(counts.values()),
        'adapter_controls': {'equivalent_notation': 1, 'expected_rejections': 3},
        'limits': 'Same synthetic inputs, no new empirical evidence or historical validity.'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
