#!/usr/bin/env python3
"""Verify the full-C packet without importing the extraction implementation."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def identity(path):
    with path.open('rb') as stream:
        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'sha256': sha, 'bytes': path.stat().st_size}


def read(path):
    return json.loads(path.read_text())


def tree(directory):
    return {str(p.relative_to(directory)): identity(p) for p in sorted(directory.rglob('*')) if p.is_file()}


def main():
    target = HERE / 'verification.json'
    if target.exists():
        raise FileExistsError('Refusing existing verification result')
    checks = {}

    def check(name, truth):
        checks[name] = bool(truth)
        if not truth:
            raise AssertionError(name)

    receipts = []
    for name in ('run01', 'run02'):
        directory = HERE / name
        receipt = read(directory / 'receipt.json')
        receipts.append(receipt)
        check(name + ':complete', receipt['status'] == 'complete')
        check(name + ':source_preserved', receipt['source_before'] == receipt['source_after'] == identity(Path(receipt['source'])))
        check(name + ':inputs_preserved', receipt['inputs_before'] == receipt['inputs_after'])
        check(name + ':binaries_preserved', receipt['binary_pins'] == receipt['binary_pins_after'])
        for path, pin in receipt['inputs_before'].items():
            check(name + ':input:' + path, identity(Path(path)) == pin)
        for path, pin in receipt['products'].items():
            check(name + ':product:' + path, identity(directory / path) == pin)
        check(name + ':commands_succeeded', all(row['exit'] == 0 for row in receipt['commands']))
        synthetic = read(directory / 'synthetic-checks.json')
        check(name + ':synthetic_six', len(synthetic) == 6 and all(synthetic.values()))
        rows = read(directory / 'compilation-selected.json')
        check(name + ':indices', [r['source_index'] for r in rows] == list(range(12900,13650)))
        check(name + ':exact_times', all(Fraction(r['source_seconds_exact']) == Fraction(r['source_index'],30) == r['source_pts'] * Fraction(r['source_time_base']) for r in rows))
        fixed = read(directory / 'fixed-native-selection.json')
        check(name + ':fixed_native', [r['source_index'] for r in fixed] == list(range(12900,13650,30)))
        check(name + ':sheets', len(list((directory / 'compilation-overview').glob('*.png'))) == 25)
        old_root = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/acoustic-audit/av-correspondence/run01')
        old = {r['source_index']:r for r in read(old_root / 'compilation-selected.json') if 13020 <= r['source_index'] < 13290}
        new = {r['source_index']:r for r in rows}
        check(name + ':old_count', len(old) == 270)
        check(name + ':old_overlap', all(identity(old_root / r['png']) == identity(directory / new[i]['png']) for i,r in old.items()))
    first, second = receipts
    check('same_product_names', first['products'].keys() == second['products'].keys())
    differences = [p for p in first['products'] if first['products'][p] != second['products'][p]]
    check('only_synthetic_container_differences', set(differences) <= {'synthetic-0.mkv','synthetic-5.mkv'})
    before = tree(HERE / 'run01')
    guard = subprocess.run([sys.executable, '-B', str(HERE / 'extract_full_c.py'), 'run01'], capture_output=True)
    check('existing_output_refused', guard.returncode != 0 and b'FileExistsError' in guard.stderr and b'Refusing existing output' in guard.stderr)
    check('guard_preserves_all_run01_files', before == tree(HERE / 'run01'))
    result = {
        'status': 'passed', 'checks': checks, 'check_count': len(checks),
        'pair_product_count': len(first['products']), 'pair_differences': differences,
        'verification_script': identity(Path(__file__)),
        'limits': 'Software and captured-byte integrity checks, not historical authentication, independent decoder implementation, sound identification, human visual acceptance or causal validation.'
    }
    with target.open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({key:result[key] for key in ('status','check_count','pair_product_count','pair_differences')}))


if __name__ == '__main__':
    main()
