"""Descriptive summary of the frozen repair; never fits or changes a track."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def pin(path):
    with path.open('rb') as stream:
        return {'bytes': path.stat().st_size,
                'sha256': hashlib.file_digest(stream, 'sha256').hexdigest()}


def read(path):
    return json.loads(path.read_text())


def ranges(values):
    return [[min(v[j] for v in values), max(v[j] for v in values)]
            for j in (0, 1)] if values else None


def main():
    out = Path(sys.argv[1])
    if out.exists():
        raise FileExistsError('preserve previous summary')
    scopes = [HERE/'run01', HERE/'run02']
    pins = {str(p.relative_to(HERE)): pin(p)
            for scope in scopes for p in sorted(scope.iterdir())}
    names = sorted(p.name for p in scopes[0].iterdir())
    assert names == sorted(p.name for p in scopes[1].iterdir())
    assert all(pin(scopes[0]/n) == pin(scopes[1]/n) for n in names)
    for scope in scopes:
        receipt = read(scope/'receipt.json')
        assert receipt['status'] == 'complete' and receipt['stage'] == 'run'
        assert set(names) == set(receipt['products']) | {'receipt.json'}
        assert all(pin(scope/n) == identity for n, identity in receipt['products'].items())
    matches = read(scopes[0]/'matches.json')
    fits = read(scopes[0]/'transforms.json')
    assert len(matches) == 852 and len(fits) == 426
    result = {'scope': 'Descriptive image-coordinate results, not physical calibration or cause.',
              'summarizer': pin(Path(__file__)), 'inputs': pins,
              'byte_identical_files_in_each_run': len(names), 'groups': [],
              'size_candidate_disagreements': [], 'computed_boundary_rows': []}
    for half in (9, 13):
        rows = [r for r in matches if r['half'] == half]
        group = {'side': half*2+1, 'match_statuses': dict(Counter(r['status'] for r in rows)),
                 'references': [], 'models': []}
        for ref in sorted({r['reference'] for r in rows}):
            selected = [r for r in rows if r['reference'] == ref]
            accepted = [r for r in selected if r['status'] == 'candidate']
            group['references'].append({
                'reference': ref, 'statuses': dict(Counter(r['status'] for r in selected)),
                'flags': dict(Counter(f for r in selected for f in r['flags'])),
                'rejected_indices': [r['index'] for r in selected if r['status'] != 'candidate'],
                'accepted_shift_ranges_xy': ranges([[r['candidate_xy'][j]-r['baseline_xy'][j]
                                                     for j in (0, 1)] for r in accepted])})
        for model in ('translation', 'similarity', 'affine'):
            selected = [r for r in fits if r['half'] == half and r['model'] == model]
            computed = [r for r in selected if r['status'] == 'computed']
            group['models'].append({
                'model': model, 'statuses': dict(Counter(r['status'] for r in selected)),
                'passing_indices': [r['index'] for r in selected if r['passes_consistency_screen']],
                'computed_failed_indices': [r['index'] for r in computed if not r['passes_consistency_screen']],
                'maximum_training_residual': max((r['max_residual'] for r in computed), default=None),
                'maximum_LOO_error': max((r['max_loo_error'] for r in computed), default=None),
                'computed_offset_ranges_xy': ranges([r['offset'] for r in computed])})
            for row in computed:
                if min(abs(row['max_residual']-2), abs(row['max_loo_error']-2)) <= 1e-8:
                    result['computed_boundary_rows'].append(row)
        result['groups'].append(group)
    lookup = {(r['index'], r['half'], r['reference']): r for r in matches}
    for small in matches:
        if small['half'] != 9:
            continue
        large = lookup[(small['index'], 13, small['reference'])]
        if small['candidate_xy'] != large['candidate_xy'] or small['status'] != large['status']:
            result['size_candidate_disagreements'].append({
                'index': small['index'], 'reference': small['reference'],
                'seconds_exact': small['seconds_exact'],
                'side19_xy': small['candidate_xy'], 'side27_xy': large['candidate_xy'],
                'side19_status': small['status'], 'side27_status': large['status']})
    assert all(pin(HERE/name) == identity for name, identity in pins.items())
    with out.open('x') as stream:
        stream.write(json.dumps(result, indent=2, sort_keys=True, allow_nan=False)+'\n')
    print(json.dumps({'status': 'complete', 'equal_files': len(names),
                      'size_disagreements': len(result['size_candidate_disagreements']),
                      'near_boundary_models': len(result['computed_boundary_rows'])}))


if __name__ == '__main__':
    main()
