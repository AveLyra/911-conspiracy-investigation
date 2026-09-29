#!/usr/bin/env python3
"""Scoped artifact/replay/guard audit; not an independent mechanics calculation."""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote

BASE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def read(path):
    def reject(value):
        raise ValueError('nonfinite_json_' + value)
    return json.loads(path.read_text(), parse_constant=reject)


def differences(a, b, path=''):
    if type(a) is not type(b):
        return [path + ':type']
    if isinstance(a, dict):
        if a.keys() != b.keys():
            return [path + ':keys']
        return sum((differences(a[k], b[k], path + '/' + str(k)) for k in a), [])
    if isinstance(a, list):
        if len(a) != len(b):
            return [path + ':length']
        return sum((differences(x, y, path + '/' + str(i)) for i, (x, y) in enumerate(zip(a, b))), [])
    return [] if a == b else [path]


def replay_check(first, second, allowed):
    found = differences(read(BASE/first), read(BASE/second))
    require(set(found) <= set(allowed), 'unexpected_replay_difference_' + first)
    return {'first': first, 'second': second, 'excluded_difference_paths': found,
            'all_other_fields_equal': True}


def check_guards():
    spec = importlib.util.spec_from_file_location('contact_join_guard_subject', BASE/'contact_damage_join.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(prefix='contact-join-guard-', dir='/private/tmp') as directory:
        fixture = Path(directory)/'synthetic.txt'
        fixture.write_text('synthetic dependency\n')
        expected = sha(fixture)
        module.FILES = {'synthetic': (fixture, expected)}
        require(module.pins() == {'synthetic': expected}, 'positive_production_pin')
        fixture.write_text('changed synthetic dependency\n')
        try:
            module.pins()
        except ValueError as exc:
            require(str(exc) == 'dependency_pin', 'wrong_pin_refusal')
        else:
            raise ValueError('changed_dependency_accepted')
    requests = [
        (['--output', 'contact-damage999999.json', '--verification', 'independent-exact-reference80-root01.json',
          '--verification-sha', '0'*64], 'verification_pin', 'contact-damage999999.json'),
        (['--output', 'contact-damage01.json'], 'output_exists', 'contact-damage01.json'),
    ]
    records = []
    for arguments, reason, filename in requests:
        output = BASE/filename
        before = sha(output) if output.exists() else None
        require(filename != 'contact-damage999999.json' or before is None, 'negative_target_already_exists')
        run = subprocess.run([sys.executable, '-B', str(BASE/'contact_damage_join.py'), *arguments],
                             capture_output=True, text=True, check=False, timeout=30)
        after = sha(output) if output.exists() else None
        require(run.returncode != 0 and run.stderr.rstrip().endswith('ValueError: ' + reason), 'guard_reason_' + reason)
        require(before == after, 'guard_output_changed')
        records.append({'refusal': reason, 'returncode': run.returncode,
                        'stdout_empty': not run.stdout, 'output_unchanged': True})
    return {'changed_dependency_through_production_pins': 'PASS', 'actual_entrypoint_refusals': records,
            'scope': 'Synthetic dependency pin function plus actual verification-pin and create-only entrypoint refusals; not every failure path.'}


def audit():
    files = sorted(p for p in BASE.iterdir() if p.is_file() and not re.fullmatch(r'artifact-check[0-9]+\.json', p.name))
    inventory = {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in files}
    counts = {'python_AST': 0, 'JSON_parsed': 0, 'Markdown_local_links': 0, 'text_whitespace': 0}
    for path in files:
        if path.suffix == '.py':
            ast.parse(path.read_text(), filename=path.name)
            counts['python_AST'] += 1
        if path.suffix == '.json':
            read(path)
            counts['JSON_parsed'] += 1
        if path.suffix in ('.py', '.md'):
            body = path.read_text()
            require(not any(line.rstrip(' \t') != line for line in body.splitlines()), 'trailing_whitespace_' + path.name)
            require(not body or body.endswith('\n'), 'missing_final_newline_' + path.name)
            counts['text_whitespace'] += 1
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                target = target.strip().strip('<>')
                if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                    continue
                target = unquote(target.split('#', 1)[0])
                target = re.sub(r':\d+$', '', target)
                if target:
                    require((path.parent/target).exists(), 'missing_link_' + path.name + '_' + target)
                    counts['Markdown_local_links'] += 1
    expected = {
        'proximity-comparison01.json': 'FAIL_EXACT_REPRODUCTION',
        'proximity-comparison-root01.json': 'FAIL_EXACT_REPRODUCTION',
        'independent-exact80-01-failed.json': 'FAIL',
        'independent-exact-preflight01.json': 'REJECTED_BEFORE_CONTROLS_OR_EVALUATION',
        'exact-proximity80.json': 'passed', 'exact-proximity120.json': 'passed',
        'exact-proximity80-root01.json': 'passed',
        'independent-exact-reference80-root01.json': 'PASS',
        'independent-exact-reference120-root01.json': 'PASS',
        'independent-exact-precision-root01.json': 'PASS',
        'contact-damage01.json': 'PASS', 'contact-damage02.json': 'PASS',
        'independent-contact-damage-comparison-root01.json': 'PASS',
        'exact-parts01.json': 'passed', 'exact-parts-root01.json': 'passed',
    }
    for name, status in expected.items():
        require(read(BASE/name)['status'] == status, 'unexpected_status_' + name)
    replays = [
        replay_check('contact-damage01.json', 'contact-damage02.json', ['/command/2', '/elapsed_seconds']),
        replay_check('independent-exact-reference120-01.json', 'independent-exact-reference120-root01.json',
                     ['/command/0', '/command/4', '/elapsed_seconds', '/peak_bytes']),
        replay_check('independent-exact-precision01.json', 'independent-exact-precision-root01.json',
                     ['/command/0', '/command/2', '/seconds', '/peak_bytes']),
        replay_check('proximity-comparison01.json', 'proximity-comparison-root01.json',
                     ['/command/0', '/command/2', '/seconds', '/peak_bytes', '/producer_control_consumers/1/stderr_sha256']),
        replay_check('exact-parts01.json', 'exact-parts-root01.json', ['/command/4', '/elapsed_seconds']),
        replay_check('independent-contact-damage-comparison01.json', 'independent-contact-damage-comparison-root01.json',
                     ['/command/0', '/command/2', '/elapsed_seconds', '/peak_bytes',
                      '/result/producer_control_reruns/verify_contact_damage.py/stderr_sha256',
                      '/result/producer_control_reruns/contact_damage_join.py/stderr_sha256']),
    ]
    guards = check_guards()
    require(all(sha(BASE/name) == item['sha256'] for name, item in inventory.items()), 'artifact_changed_during_check')
    return {'status': 'PASS', 'counts': counts, 'inventory': inventory, 'expected_statuses': expected,
            'replay_comparisons': replays, 'guard_checks': guards,
            'scope': 'Integrity, parse/link/text hygiene, retained status, receipt replay equality and scoped guards. Not independent science, source authenticity or physical validation.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    require(re.fullmatch(r'artifact-check[0-9]+\.json', args.output) is not None, 'output_scope')
    target = BASE/args.output
    require(not target.exists(), 'output_exists')
    record = audit()
    record['command'] = sys.argv
    with target.open('x') as handle:
        json.dump(record, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write('\n')
    print(json.dumps({'status': record['status'], 'output': target.name, 'sha256': sha(target), 'counts': record['counts']}))
