#!/usr/bin/env python3
"""Fresh integrity/reproduction and non-overwrite checks, not forensic validation."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def pin(path):
    sha = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            sha.update(chunk)
    return {"sha256": sha.hexdigest(), "bytes": path.stat().st_size}


def main():
    dest = HERE / 'verification.json'
    if dest.exists():
        raise FileExistsError('Refusing existing verification')
    checks, receipts, hashes = {}, {}, {}
    for run in ('run01', 'run02', 'refine01', 'refine02'):
        p = HERE / run / 'receipt.json'
        r = json.loads(p.read_text())
        receipts[run] = r
        hashes[run] = pin(p)
        checks[run + ':complete'] = r['status'] == 'complete'
        checks[run + ':sources_stable'] = r['sources_before'] == r['sources_after']
        checks[run + ':all_commands_zero'] = all(c['exit'] == 0 for c in r['commands'])
        for name, expected in r['products'].items():
            checks[run + ':product:' + name] = pin(HERE / run / name) == expected
    comparisons = {}
    for a, b in [('run01', 'run02'), ('refine01', 'refine02')]:
        left, right = receipts[a]['products'], receipts[b]['products']
        checks[a + ':same_product_names'] = left.keys() == right.keys()
        different = [k for k in left if left[k] != right[k]]
        # Preserve observed container-byte nonreproduction; decoded fixtures,
        # historical PNGs, overview sheets and timing maps must still match.
        allowed = ['synthetic-0.mkv', 'synthetic-5.mkv'] if a == 'run01' else []
        checks[a + ':no_other_product_difference'] = all(k in allowed for k in different)
        comparisons[a + ':' + b] = {'product_pairs': len(left), 'identical_pairs': len(left) - len(different),
                                    'different': different}
    coverage = {}
    for label in ('compilation', 'comparator'):
        initial = json.loads((HERE / 'run01' / (label + '-selected.json')).read_text())
        refined = json.loads((HERE / 'refine01' / (label + '-selected.json')).read_text())
        initial_by_index = {r['source_index']: r for r in initial}
        duplicates = [r for r in refined if r['source_index'] in initial_by_index]
        for r in duplicates:
            checks[label + ':overlap_pixels_pts:' + str(r['source_index'])] = all(
                r[k] == initial_by_index[r['source_index']][k] for k in ('sha256', 'bytes', 'source_pts', 'source_time_base'))
        coverage[label] = {'initial': len(initial), 'refined': len(refined), 'overlap': len(duplicates),
                           'unique_source_indexes': len(initial) + len(refined) - len(duplicates)}
    audio_a, audio_b = [HERE / run / 'measurements.json' for run in ('audio01', 'audio02')]
    checks['audio:byte_identical'] = pin(audio_a) == pin(audio_b)
    audio = json.loads(audio_a.read_text())
    checks['audio:synthetic_tests'] = all(audio['synthetic_checks'].values())
    for label in ('edited', 'msnbc'):
        checks['audio:source:' + label] = pin(HERE.parent / 'run01' / (label + '-stereo.wav')) == audio['sources'][label]
    guard_results = {}
    for script, run in [('extract_frames.py', 'run01'), ('refine_frames.py', 'refine01'), ('audio_crosswalk.py', 'audio01')]:
        directory = HERE / run
        before = {str(p.relative_to(directory)): pin(p) for p in directory.rglob('*') if p.is_file()}
        result = subprocess.run([sys.executable, str(HERE / script), run], capture_output=True, timeout=60)
        after = {str(p.relative_to(directory)): pin(p) for p in directory.rglob('*') if p.is_file()}
        checks['guard:' + script] = result.returncode != 0 and b'FileExistsError' in result.stderr and before == after
        guard_results[script] = {'exit': result.returncode, 'unchanged_files': len(before),
                                  'stderr_sha256': hashlib.sha256(result.stderr).hexdigest()}
    saved = {'status': 'pass' if all(checks.values()) else 'fail', 'checks': checks,
             'comparisons': comparisons, 'coverage': coverage, 'receipt_pins': hashes,
             'audio_measurements': pin(audio_a), 'guard_checks': guard_results,
             'code': pin(Path(__file__)),
             'limits': 'Integrity and same-code reproduction only. Two synthetic container bytes differ; no historical authenticity, sound attribution, original A/V sync or causal validation.'}
    with dest.open('x') as file:
        json.dump(saved, file, indent=2, sort_keys=True)
        file.write('\n')
    print(json.dumps({'status': saved['status'], 'checks': len(checks), 'comparisons': comparisons, 'coverage': coverage}))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
