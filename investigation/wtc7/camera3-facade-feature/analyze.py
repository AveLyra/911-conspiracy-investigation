"""Declared exploratory image geometry; no causal or physical calibration inference."""
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'camera3-late-reannotation'
FRAMES = [258, *range(288, 349, 3)]
PINS = {
    HERE / 'PROTOCOL.md': 'd8adc5afa2e8f9b5d986b0d3042f8b420509478fc84dd5dfd7ea26016415c27e',
    HERE / 'root-observations.json': 'b0c8fa4339ab36188c20779ec8414d211e1be6ecb39a7597c2a9c90fd5f64838',
    HERE / 'independent-observations.json': '8ee9e5c5884dbcc9645958e96c9c7fa8561953cbb71820d0f699b72874f2c47a',
    OLD / 'root-observations.json': '20b873f21704b3ccb8ceb75cba3eb09a84ab3431223a0c3f68ef7ce54efa397a',
    OLD / 'independent-observations.json': '529db0a68030a3ef26eef26723f0ab8c635fe47d6a743b780014d375ab95808f',
    OLD / 'views01/receipt.json': '8bf54e80ccb0eb823cd9a09fc45e285fa4a649c166aaf2b26d551c13782c3161',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fit(frames, values, bounds):
    missing = [f for f, v in zip(frames, values) if v is None]
    if missing:
        return {'status': 'missing', 'missing_frames': missing}
    t = (np.asarray(frames, dtype=float) - 138) / 15
    y = np.asarray(values, dtype=float)
    boxes = np.asarray(bounds, dtype=float)
    if not np.isfinite(y).all() or not np.isfinite(boxes).all():
        raise ValueError('nonfinite input')
    if np.any(boxes[:, 0] > y) or np.any(y > boxes[:, 1]):
        raise ValueError('central placement outside bounds')
    if len(set(frames)) != len(frames) or np.any(np.diff(t) <= 0):
        raise ValueError('nonincreasing time')
    center = float((t[0] + t[-1]) / 2)
    halfspan = float((t[-1] - t[0]) / 2)
    z = (t - center) / halfspan
    result = {'status': 'computed', 't': t.tolist(), 'values': values,
              'bounds': bounds, 'center': center, 'halfspan': halfspan}
    for degree, name in [(1, 'linear'), (2, 'quadratic')]:
        design = np.column_stack([z ** k for k in range(degree + 1)])
        inv = np.linalg.pinv(design)
        coefficients = inv @ y
        residuals = y - design @ coefficients
        result[name] = {'coefficients': coefficients.tolist(),
                        'residuals': residuals.tolist(),
                        'sse': float(residuals @ residuals),
                        'rmse': float(np.sqrt(np.mean(residuals ** 2)))}
        if degree == 2:
            weights = 2 * inv[2] / halfspan ** 2
            limits = [float(np.sum(np.where(weights >= 0, weights * boxes[:, 0], weights * boxes[:, 1]))),
                      float(np.sum(np.where(weights >= 0, weights * boxes[:, 1], weights * boxes[:, 0])))]
            result.update(acceleration=float(weights @ y), weights=weights.tolist(),
                          acceleration_bounds=limits)
    return result


def joint(rows):
    """Rows retain original boxes per observer; no averaging or overwritten data."""
    if not rows:
        return {'status': 'no_data'}
    axes = {}
    for axis in ['x', 'y']:
        per = []
        for row in rows:
            a = [max(o['A'][axis][0] for o in row['observers']),
                 min(o['A'][axis][1] for o in row['observers'])]
            c = [max(o['C'][axis][0] for o in row['observers']),
                 min(o['C'][axis][1] for o in row['observers'])]
            per.append({'frame': row['frame'], 'A': a, 'C': c,
                        'separation': [a[0] - c[1], a[1] - c[0]]})
        lower = max(r['separation'][0] for r in per)
        upper = min(r['separation'][1] for r in per)
        local_gap = max(max(r['A'][0] - r['A'][1], r['C'][0] - r['C'][1]) for r in per)
        delta = max(0, local_gap / 2, (lower - upper) / 4)
        axes[axis] = {'per_frame': per, 'intersection': [lower, upper],
                      'max_lower_frames': [r['frame'] for r in per if r['separation'][0] == lower],
                      'min_upper_frames': [r['frame'] for r in per if r['separation'][1] == upper],
                      'local_max_gap': local_gap, 'minimum_delta': delta,
                      'feasible_original': local_gap <= 0 and lower <= upper}
    vector_delta = max(a['minimum_delta'] for a in axes.values())
    witness = []
    vector = {axis: sum(a['intersection']) / 2 for axis, a in axes.items()}
    for i, row in enumerate(rows):
        w = {'frame': row['frame']}
        for axis, a in axes.items():
            p = a['per_frame'][i]
            ab = [p['A'][0] - vector_delta, p['A'][1] + vector_delta]
            cb = [p['C'][0] - vector_delta, p['C'][1] + vector_delta]
            lo = max(ab[0], vector[axis] + cb[0])
            hi = min(ab[1], vector[axis] + cb[1])
            assert lo <= hi
            aw = (lo + hi) / 2
            cw = aw - vector[axis]
            for observer in row['observers']:
                assert observer['A'][axis][0] - vector_delta <= aw <= observer['A'][axis][1] + vector_delta
                assert observer['C'][axis][0] - vector_delta <= cw <= observer['C'][axis][1] + vector_delta
            w[axis] = {'A': aw, 'C': cw}
        witness.append(w)
    return {'status': 'computed', 'axes': axes, 'minimum_uniform_delta': vector_delta,
            'feasible_original': vector_delta == 0, 'witness_separation': vector,
            'witness_delta': vector_delta, 'witness': witness,
            'witness_is_observation': False}


def controls():
    frames = list(range(288, 315, 3))
    t = (np.array(frames) - 138) / 15
    fits = []
    for name, y, expected in [('constant', np.full(9, 7.), 0),
                              ('linear', 3 + 2*t, 0),
                              ('curved', 3 + 2*t + 4*t*t, 8),
                              ('translated_pair_difference', np.full(9, 10.), 0)]:
        values = y.tolist()
        bounds = [[v-1, v+1] for v in values]
        r = fit(frames, values, bounds)
        assert abs(r['acceleration'] - expected) < 1e-8
        fits.append({'name': name, 'frames': frames, 'expected_acceleration': expected, 'result': r})
    values = [0] * 8 + [None]
    missing = fit(frames, values, [[-1, 1]] * 8 + [None])
    assert missing == {'status': 'missing', 'missing_frames': [312]}
    joint_controls = []
    def obs(a, c):
        return {'A': {'x': a, 'y': a}, 'C': {'x': c, 'y': c}}
    fixtures = [
        ('constant', [{'frame': 0, 'observers': [obs([9,11],[1,3])]},
                      {'frame': 1, 'observers': [obs([19,21],[11,13])]}], 0),
        ('global_conflict', [{'frame': 0, 'observers': [obs([0,0],[0,0])]},
                            {'frame': 1, 'observers': [obs([4,4],[0,0])]}], 1),
        ('local_conflict', [{'frame': 0, 'observers': [obs([0,0],[0,0]),obs([4,4],[4,4])]}], 2),
        ('touching', [{'frame': 0, 'observers': [obs([0,1],[0,1])]},
                     {'frame': 1, 'observers': [obs([2,3],[0,1])]}], 0),
    ]
    for name, rows, expected in fixtures:
        r = joint(rows)
        assert r['minimum_uniform_delta'] == expected
        joint_controls.append({'name': name, 'rows': rows, 'expected_delta': expected, 'result': r})
    assert joint([]) == {'status': 'no_data'}
    return {'fits': fits, 'missing': {'frames': frames, 'values': values, 'result': missing},
            'joint': joint_controls, 'empty': {'rows': [], 'result': joint([])}}


def main():
    out = Path(sys.argv[1]).resolve()
    if out.exists():
        raise SystemExit('refusing existing output directory')
    check = controls()  # synthetic tests precede historical calculation
    before = {str(p): digest(p) for p in PINS}
    assert before == {str(p): h for p, h in PINS.items()}, 'input pin mismatch'
    data = {}
    for who in ['root', 'independent']:
        aa = {r['frame']: r['A'] for r in json.loads((OLD / f'{who}-observations.json').read_text())['rows']}
        cc = {r['frame']: r for r in json.loads((HERE / f'{who}-observations.json').read_text())['frames']}
        assert sorted(aa) == FRAMES and sorted(cc) == FRAMES
        data[who] = {'A': aa, 'C': cc}
    comparisons = []
    for frame in FRAMES:
        row = {'frame': frame, 'observers': {}}
        for who, d in data.items():
            a, c = d['A'][frame], d['C'][frame]
            value = {'C_localized': c['x'] is not None}
            if value['C_localized']:
                for axis in ['x', 'y']:
                    lo, hi = c[axis + '_bounds']
                    assert lo <= c[axis] <= hi
                    value[axis] = {'C': c[axis], 'C_bounds': [lo, hi], 'A': a[axis],
                                   'A_bounds': [a[axis+'min'], a[axis+'max']],
                                   'A_minus_C': a[axis] - c[axis],
                                   'separation_bounds': [a[axis+'min'] - hi, a[axis+'max'] - lo]}
            row['observers'][who] = value
        if all(o['C_localized'] for o in row['observers'].values()):
            row['C_overlap'] = {axis: [max(o[axis]['C_bounds'][0] for o in row['observers'].values()),
                                      min(o[axis]['C_bounds'][1] for o in row['observers'].values())]
                                for axis in ['x', 'y']}
        comparisons.append(row)
    scenarios = []
    for who in ['root', 'independent', 'combined']:
        for coverage, frames in [('all', FRAMES), ('late', FRAMES[1:])]:
            rows, omitted = [], []
            observers = ['root','independent'] if who == 'combined' else [who]
            for frame in frames:
                if any(data[o]['C'][frame]['x'] is None for o in observers):
                    omitted.append(frame)
                    continue
                values = []
                for o in observers:
                    a, c = data[o]['A'][frame], data[o]['C'][frame]
                    values.append({'observer': o,
                                   'A': {q: [a[q+'min'],a[q+'max']] for q in ['x','y']},
                                   'C': {q: c[q+'_bounds'] for q in ['x','y']}})
                rows.append({'frame': frame, 'observers': values})
            scenarios.append({'observer': who, 'coverage': coverage, 'selected_frames': frames,
                              'omitted': omitted, 'rows': rows, 'result': joint(rows)})
    fits = []
    for who, d in data.items():
        for series in ['C', 'A-C']:
            for length in [9, 13, 21]:
                for start in range(22 - length):
                    frames = FRAMES[1:][start:start+length]
                    values, bounds = [], []
                    for frame in frames:
                        a, c = d['A'][frame], d['C'][frame]
                        if c['y'] is None:
                            values.append(None)
                            bounds.append(None)
                        elif series == 'C':
                            values.append(c['y'])
                            bounds.append(c['y_bounds'])
                        else:
                            values.append(a['y']-c['y'])
                            bounds.append([a['ymin']-c['y_bounds'][1], a['ymax']-c['y_bounds'][0]])
                    fits.append({'observer': who, 'series': series, 'frames': frames,
                                 'fit': fit(frames, values, bounds)})
    assert before == {str(p): digest(p) for p in PINS}
    out.mkdir(parents=True, exist_ok=False)
    for name, obj in [('controls.json',check),('results.json',{'comparison':comparisons,'joint':scenarios,'fits':fits})]:
        with (out/name).open('x') as stream:
            json.dump(obj, stream, indent=2, allow_nan=False)
            stream.write('\n')
    receipt = {'python':platform.python_version(),'numpy':np.__version__,'command':sys.argv,
               'source_code_sha256':digest(Path(__file__)), 'inputs_before_and_after': before,
               'outputs': {name:digest(out/name) for name in ['controls.json','results.json']},
               'status':'completed', 'scope':'conditional image coordinates; no historical physical validation'}
    with (out/'receipt.json').open('x') as stream:
        json.dump(receipt,stream,indent=2)
        stream.write('\n')
    print(json.dumps({'status':'completed','fits':len(fits),'computed':sum(r['fit']['status']=='computed' for r in fits),
                      'scenarios':len(scenarios),'output':str(out)}))


if __name__ == '__main__':
    main()
