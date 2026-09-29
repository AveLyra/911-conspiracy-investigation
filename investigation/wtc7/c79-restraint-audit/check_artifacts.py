#!/usr/bin/env python3
"""Local artifact integrity checks only; no source-deck execution or physics test."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parent


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def check():
    errors, counts, pins = [], {'python': 0, 'json': 0, 'markdown': 0,
                              'local_links': 0, 'table_pins': 0}, {}
    docs = []
    for path in sorted(BASE.iterdir()):
        if not path.is_file() or path.name.startswith('closeout'):
            continue
        pins[path.name] = sha(path)
        if path.suffix == '.py':
            ast.parse(path.read_text(), filename=path.name)
            counts['python'] += 1
        elif path.suffix == '.json':
            json.loads(path.read_text())
            counts['json'] += 1
        elif path.suffix == '.md':
            docs.append(path)
    for path in docs:
        text = path.read_text()
        counts['markdown'] += 1
        for i, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line or re.match(r'^(<<<<<<<|=======|>>>>>>>)', line):
                errors.append({'file': path.name, 'line': i, 'error': 'whitespace_or_conflict'})
        for raw in re.findall(r'\[[^\]\n]*\]\((<[^>]*>|[^)\n]*)\)', text):
            target = raw[1:-1] if raw.startswith('<') else raw
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                continue
            target = re.sub(r':\d+$', '', target.split('#', 1)[0])
            if not target:
                continue
            resolved = Path(target) if target.startswith('/') else path.parent / target
            counts['local_links'] += 1
            if not resolved.exists():
                errors.append({'file': path.name, 'error': 'missing_local_target', 'target': target})
    validation = (BASE / 'validation.md').read_text()
    for filename, expected in re.findall(r'^\| ([\w.-]+\.(?:py|json|md)) \| ([0-9a-f]{64}) \|$', validation, re.M):
        counts['table_pins'] += 1
        if not (BASE / filename).is_file() or sha(BASE / filename) != expected:
            errors.append({'file': filename, 'error': 'table_pin_mismatch'})
    pairs = [
        ('root01.json', 'root02.json', {'elapsed_seconds'}),
        ('contacts-root01.json', 'contacts-root02.json', {'elapsed_seconds'}),
        ('comparison01.json', 'comparison-root01.json', {'command', 'elapsed_seconds'}),
        ('contact-comparison01.json', 'contact-comparison-root01.json', {'command', 'elapsed_seconds'}),
        ('candidate-join01.json', 'candidate-join-root01.json', {'command', 'elapsed_seconds', 'peak_rss_bytes'}),
    ]
    comparisons = []
    for left, right, excluded in pairs:
        a = json.loads((BASE / left).read_text())
        b = json.loads((BASE / right).read_text())
        ok = ({k: v for k, v in a.items() if k not in excluded}
              == {k: v for k, v in b.items() if k not in excluded})
        expected_status = 'complete' if left in {'root01.json', 'contacts-root01.json'} else 'PASS'
        ok = ok and a['status'] == b['status'] == expected_status
        comparisons.append({'left': left, 'right': right, 'excluded_keys': sorted(excluded), 'equal': ok})
        if not ok:
            errors.append({'file': left, 'error': 'pair_status_or_equality'})
    return {'status': 'PASS' if not errors else 'FAIL', 'errors': errors,
            'scope': 'unit syntax, JSON, local links, explicit hash tables and frozen pair agreement only',
            'counts': counts, 'pins': pins, 'comparisons': comparisons,
            'python': sys.version.split()[0]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if Path(args.output).name != args.output or not re.fullmatch(r'closeout\d+\.json', args.output):
        parser.error('choose a fresh closeoutNN.json basename')
    output = BASE / args.output
    if output.exists():
        parser.error('output exists; preserve it and use a fresh name')
    result = check()
    with output.open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')
    print(json.dumps({'status': result['status'], 'counts': result['counts'],
                      'errors': result['errors'], 'sha256': sha(output)}))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
