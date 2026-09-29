"""Fixed-grid kinematic minimax fits with exact optimality certificates."""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from pathlib import Path
import sys
import traceback
import warnings

import numpy as np
import scipy
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent/'multipoint-table-reproduction'
ROOT = PARENT/'transcription-root/table47.json'
OTHER = PARENT/'transcription-independent/table47.json'
PINS = {ROOT: 'a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc',
        OTHER: 'fe5e566dff8cbff6aa80a00656820504b2542bc5468eef96eb9911d5e4aea2f8'}
T0 = F('6.4')
TIMES = tuple(T0+F(i, 5) for i in range(16))
TAUS = tuple(T0+F(i, 20) for i in range(41))
DURATIONS = (F(0), F(1, 5), F(2, 5), F(4, 5))
CLOCKS = (F(1), F(1001, 1000), F(1000, 999))


def identity(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def encode(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [encode(v) for v in x]
    return x


def dot(a, b):
    return sum((x*y for x, y in zip(a, b, strict=True)), F(0))


def solve(a, b):
    n = len(b)
    rows = [[F(x) for x in row]+[F(value)] for row, value in zip(a, b, strict=True)]
    if any(len(r) != n+1 for r in rows): raise ValueError('Non-square basis')
    for j in range(n):
        pivot = next((k for k in range(j, n) if rows[k][j]), None)
        if pivot is None: raise ValueError('Singular basis')
        rows[j], rows[pivot] = rows[pivot], rows[j]
        divisor = rows[j][j]
        rows[j] = [v/divisor for v in rows[j]]
        for k in range(n):
            if k != j:
                c = rows[k][j]
                rows[k] = [x-c*y for x, y in zip(rows[k], rows[j], strict=True)]
    return tuple(r[-1] for r in rows)


def g(s, duration):
    if duration < 0: raise ValueError('Negative duration')
    positive = max(s, F(0))
    if duration == 0: return positive**2/2
    return (positive**3-max(s-duration, F(0))**3)/(6*duration)


def validate_series(times, y):
    if len(times) != len(y) or len(times) < 4: raise ValueError('Insufficient/misaligned observations')
    if any(v is None for v in (*times, *y)): raise ValueError('Missing observation')
    if any(b <= a for a, b in zip(times, times[1:])): raise ValueError('Non-increasing times')


def constraints(times, y, tau, duration, alpha=F(1)):
    validate_series(times, y)
    rows, rhs = [], []
    for t, observed in zip(times, y, strict=True):
        x, shape = alpha*(t-T0), g(alpha*(t-tau), alpha*duration)
        rows.extend([(F(1), x, shape, F(-1)), (F(-1), -x, -shape, F(-1))])
        rhs.extend([observed, -observed])
    rows.extend([(F(0), F(0), F(1), F(0)), (F(0), F(0), F(0), F(-1))])
    rhs.extend([F(0), F(0)])
    return rows, rhs


def certificate(rows, rhs, beta, dual):
    return (len(rows) == len(dual) and all(w >= 0 for w in dual)
            and all(dot(row, beta) <= h for row, h in zip(rows, rhs, strict=True))
            and all(sum((row[j]*w for row, w in zip(rows, dual, strict=True)), F(0))
                    == (F(-1) if j == 3 else F(0)) for j in range(4))
            and beta[3] == -dot(rhs, dual))


def phase_counts(times, tau, duration):
    return {'before': sum(t < tau for t in times),
            'at_start': sum(t == tau for t in times),
            'inside': sum(tau < t < tau+duration for t in times),
            'at_end': sum(t == tau+duration for t in times) if duration else 0,
            'after': sum(t > tau+duration for t in times)}


def fit(times, y, tau, duration, label):
    rows, rhs = constraints(times, y, tau, duration)
    with warnings.catch_warnings(record=True) as diagnostic:
        warnings.simplefilter('always')
        result = linprog([0., 0., 0., 1.],
                         A_ub=np.array(rows, dtype=float), b_ub=np.array(rhs, dtype=float),
                         bounds=[(None, None)]*4, method='highs-ds')
    if diagnostic: raise RuntimeError('Optimizer warnings: '+str([str(w.message) for w in diagnostic]))
    if not result.success: raise RuntimeError('Optimizer failure: '+result.message)
    support = tuple(i for i, v in enumerate(result.ineqlin.marginals) if v < -1e-9)
    for threshold in (1e-7, 1e-6, 1e-5):
        active = [i for i, v in enumerate(result.ineqlin.residual) if abs(v) <= threshold]
        if not set(support).issubset(active) or len(support) > 4: continue
        # Bounds first improve degenerate zero-error basis selection, not acceptance.
        rest = sorted((i for i in active if i not in support), key=lambda i: (i < len(rows)-2, i))
        for extra in combinations(rest, 4-len(support)):
            basis = (*support, *extra)
            try:
                beta = solve([rows[i] for i in basis], [rhs[i] for i in basis])
                w = solve(list(zip(*(rows[i] for i in basis))), (F(0), F(0), F(0), F(-1)))
            except ValueError:
                continue
            dual = [F(0)]*len(rows)
            for i, weight in zip(basis, w, strict=True): dual[i] = weight
            if not certificate(rows, rhs, beta, dual): continue
            residuals = tuple(beta[0]+beta[1]*(t-T0)+beta[2]*g(t-tau, duration)-v
                              for t, v in zip(times, y, strict=True))
            assert max(abs(r) for r in residuals) == beta[3]
            for alpha in CLOCKS:
                mapped = (beta[0], beta[1]/alpha, beta[2]/alpha**2, beta[3])
                mapped_dual = list(dual)
                mapped_dual[-2] *= alpha**2
                b2, h2 = constraints(times, y, tau, duration, alpha)
                assert certificate(b2, h2, mapped, mapped_dual)
            return {'label': label, 'tau': tau, 'D': duration, 'times': times, 'y': y,
                    'beta': beta, 'dual': dual, 'residuals': residuals,
                    'extra': max(F(0), beta[3]-F(1, 200)),
                    'phase_counts': phase_counts(times, tau, duration),
                    'activity_threshold': threshold, 'basis_indices': basis,
                    'float_iterations': int(result.nit), 'clock_certificates': len(CLOCKS)}
    raise RuntimeError(f'No exact certificate for {label}, tau={tau}, D={duration}; float={result.x.tolist()}')


def summary(fits):
    groups = {}
    for r in fits:
        groups.setdefault((r['label'], r['D']), []).append(r)
    out = []
    for (label, duration), group in groups.items():
        minimum = min(r['beta'][3] for r in group)
        winners = [r for r in group if r['beta'][3] == minimum]
        out.append({'label': label, 'D': duration, 'R': minimum,
                    'extra': max(F(0), minimum-F(1, 200)),
                    'printing_compatible': minimum <= F(1, 200),
                    'onsets': [r['tau'] for r in winners],
                    'grid_boundary': any(r['tau'] in (TAUS[0], TAUS[-1]) for r in winners),
                    'zero_acceleration_winner': any(r['beta'][2] == 0 for r in winners)})
    return out


def generated(tau, duration, a=F(-8)):
    return tuple(F(100)+(t-T0)/4+a*g(t-tau, duration) for t in TIMES)


def controls(fits):
    for d in DURATIONS:
        for s in (F(-1), F(0), d/2, d, d+F(1)):
            piece = F(0) if s <= 0 else (s*s/2 if d == 0 else
                     s**3/(6*d) if s < d else s*s/2-d*s/2+d*d/6)
            assert g(s, d) == piece
        if d:
            assert d**3/(6*d) == d*d/2-d*d/2+d*d/6
            assert F(0)**2/(2*d) == 0 and d**2/(2*d) == d-d/2
            assert F(0)/d == 0 and d/d == 1
        r = fit(TIMES, generated(F('7.6'), d), F('7.6'), d, 'known')
        assert r['beta'] == (F(100), F(1, 4), F(-8), F(0)); fits.append(r)
        r = fit(TIMES, tuple(F(100)+(t-T0)/4 for t in TIMES), F('7.6'), d, 'line')
        assert r['beta'][2:] == (F(0), F(0)); fits.append(r)
        r = fit(TIMES, generated(F(4), F(0)), F(4), d, 'all_post')
        assert r['beta'][3] == 0; fits.append(r)
    noisy = list(generated(F('7.6'), F(0))); noisy[3] += 1
    r = fit(TIMES, tuple(noisy), F('7.6'), F(0), 'outlier')
    assert r['beta'][3] > F(1, 200); fits.append(r)
    r = fit(TIMES, generated(F('7.6'), F(0), F(8)), F('7.6'), F(0), 'upward')
    assert r['beta'][2] == 0 and r['beta'][3] > 0; fits.append(r)
    for d in DURATIONS:
        for tau in TAUS:
            fits.append(fit(TIMES, generated(F('7.625'), F(0)), tau, d, 'offgrid_step'))
    assert len(fits) == 178
    bad_calls = [lambda: g(F(1), F(-1)), lambda: validate_series((F(1),), (F(1),)),
                 lambda: validate_series((F(1),)*4, (F(1),)*4),
                 lambda: validate_series(TIMES, (*generated(F(4), F(0))[:-1], None)),
                 lambda: solve([[F(0)]*4]*4, [F(0)]*4)]
    for call in bad_calls:
        try: call()
        except ValueError: pass
        else: raise AssertionError('Invalid input admitted')
    r = fits[0]; rows, rhs = constraints(r['times'], r['y'], r['tau'], r['D'])
    beta = list(r['beta']); beta[0] += 1
    dual = list(r['dual']); dual[0] = -1
    assert not certificate(rows, rhs, beta, r['dual'])
    assert not certificate(rows, rhs, r['beta'], dual)
    return {'synthetic_fits': 178, 'invalid_input_rejections': 5,
            'mutated_certificates_rejected': 2, 'piecewise_basis_checks': 20,
            'boundary_position_checks': 3, 'boundary_velocity_acceleration_checks': 12,
            'all_clock_certificates': 534}


def load_history():
    for path, expected in PINS.items():
        assert identity(path)['sha256'] == expected
    root, other = json.loads(ROOT.read_text()), json.loads(OTHER.read_text())
    rr = {F(r['time_s']): r for r in root['rows']}
    oo = {F(r['time_s']): r for r in other['rows']}
    assert len(rr) == len(root['rows']) == len(oo) == len(other['rows']) == 70
    targets = [('ne', 'ne_y', 'ne_corner_y'), ('ec', 'ec_y', 'ec_roofline_y'),
               ('wc', 'wc_y', 'wc_roofline_y'), ('nw', 'nw_y', 'nw_corner_y')]
    common = sorted(t for t in rr if all(rr[t][key] is not None for _, key, _ in targets))
    assert common == list(TIMES)
    data = {}
    for target, rkey, okey in targets:
        assert all(rr[t][rkey] == oo[t][okey] for t in TIMES)
        data[target] = {'y': tuple(F(rr[t][rkey]) for t in TIMES),
                        'source_rows': [rr[t]['row'] for t in TIMES],
                        'literal_values': [rr[t][rkey] for t in TIMES]}
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['controls', 'historical'])
    parser.add_argument('output')
    parser.add_argument('--controls')
    args = parser.parse_args()
    output = HERE/args.output
    if output.parent != HERE or output.exists(): raise FileExistsError('Unsafe or existing output')
    paths = [Path(__file__).resolve(), HERE/'PROTOCOL.md', Path(sys.executable)]
    if args.mode == 'historical':
        if not args.controls: raise ValueError('Passing controls required')
        control_path = HERE/args.controls
        prior = json.loads(control_path.read_text())
        assert prior['status'] == 'passed' and prior['control_results']['synthetic_fits'] == 178
        assert prior['pins_before'][str(Path(__file__).resolve())] == identity(Path(__file__).resolve())
        paths.extend([ROOT, OTHER, control_path])
    before = {str(p): identity(p) for p in paths}
    fits = []
    result = {'schema': 'acceleration-transition-v1', 'mode': args.mode, 'status': 'incomplete',
              'runtime': {'python': sys.version, 'numpy': np.__version__, 'scipy': scipy.__version__,
                          'optimizer': 'scipy.optimize.linprog highs-ds'},
              'pins_before': before, 'clock_factors': CLOCKS, 'fits': fits}
    try:
        if args.mode == 'controls': result['control_results'] = controls(fits)
        else:
            data = load_history(); result['source_data'] = data
            for target, source in data.items():
                for d in DURATIONS:
                    for tau in TAUS:
                        r = fit(TIMES, source['y'], tau, d, target)
                        r['target'] = target; fits.append(r)
            assert len(fits) == 656
        result['summary'] = summary(fits)
        result['status'] = 'passed'
    except Exception as error:
        result['error'] = type(error).__name__+': '+str(error)
        result['traceback'] = traceback.format_exc()
        raise
    finally:
        result['pins_after'] = {str(p): identity(p) for p in paths}
        result['inputs_unchanged'] = result['pins_after'] == before
        with output.open('x') as f:
            json.dump(encode(result), f, indent=2, sort_keys=True); f.write('\n')
    assert result['inputs_unchanged']
    print(json.dumps({'status': result['status'], 'mode': args.mode, 'fits': len(fits),
                      'clock_certificates': len(fits)*len(CLOCKS), 'output': output.name}))


if __name__ == '__main__': main()
