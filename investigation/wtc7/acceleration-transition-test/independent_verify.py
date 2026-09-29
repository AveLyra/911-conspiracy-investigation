"""Exact certificate checking only: no optimizer, producer import, or media."""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
T0 = F(32, 5)
TIMES = tuple(T0 + F(i, 5) for i in range(16))
DURATIONS = (F(0), F(1, 5), F(2, 5), F(4, 5))
ONSETS = tuple(T0 + F(k, 20) for k in range(41))
FACTORS = (F(1), F(1001, 1000), F(1000, 999))
EPS = F(1, 200)
THRESHOLDS = {F(1, 10**7), F(1, 10**6), F(1, 10**5)}
FIELDS = {'ne': 'ne_corner_y', 'ec': 'ec_roofline_y',
          'wc': 'wc_roofline_y', 'nw': 'nw_corner_y'}
SOURCE = HERE.parent / 'multipoint-table-reproduction'
SOURCE_PINS = {
    SOURCE / 'transcription-independent/table47.json':
        'fe5e566dff8cbff6aa80a00656820504b2542bc5468eef96eb9911d5e4aea2f8',
    SOURCE / 'transcription-root/table47.json':
        'a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc',
    HERE.parent / 'luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf':
        'cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fraction(value):
    require(isinstance(value, str), 'fraction fields must be strings')
    return F(value)


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def pin(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}


def g(s, duration):
    require(duration >= 0, 'negative duration')
    if s <= 0:
        return F(0)
    if duration == 0:
        return s * s / 2
    if s < duration:
        return s**3 / (6 * duration)
    return s*s/2 - duration*s/2 + duration*duration/6


def valid_times(times):
    require(len(times) >= 4, 'inadequate observations')
    require(all(isinstance(t, F) for t in times), 'missing/nonrational time')
    require(all(a < b for a, b in zip(times, times[1:])),
            'duplicate or non-increasing times')


def phases(times, tau, duration):
    require(duration >= 0, 'negative duration')
    result = {
        'before': sum(t < tau for t in times),
        'at_start': sum(t == tau for t in times),
        'inside': sum(tau < t < tau + duration for t in times),
        'at_end': sum(t == tau + duration for t in times) if duration else 0,
        'after': sum(t > tau + duration for t in times),
    }
    require(sum(result.values()) == len(times), 'phase partition failure')
    return result


def constraints(times, values, tau, duration):
    valid_times(times)
    require(len(values) == len(times), 'value/time length mismatch')
    require(duration >= 0, 'negative duration')
    B, h = [], []
    for t, y in zip(times, values):
        x, basis = t - T0, g(t - tau, duration)
        B.extend(((F(1), x, basis, F(-1)), (F(-1), -x, -basis, F(-1))))
        h.extend((y, -y))
    B.extend(((F(0), F(0), F(1), F(0)), (F(0), F(0), F(0), F(-1))))
    h.extend((F(0), F(0)))
    return B, h


def dot(a, b):
    require(len(a) == len(b), 'dot dimension mismatch')
    return sum((x*y for x, y in zip(a, b)), F(0))


def certificate(times, values, tau, duration, beta, dual):
    require(len(beta) == 4, 'primal must have four entries')
    B, h = constraints(times, values, tau, duration)
    require(len(dual) == len(B), 'dual length mismatch')
    require(all(v >= 0 for v in dual), 'negative dual multiplier')
    require(all(dot(row, beta) <= bound for row, bound in zip(B, h)),
            'primal inequality failure')
    columns = tuple(sum((dual[i]*B[i][j] for i in range(len(B))), F(0))
                    for j in range(4))
    require(columns == (0, 0, 0, -1), 'dual column identity failure')
    lower_bound = -dot(h, dual)
    require(beta[3] == lower_bound, 'primal/dual objective gap')
    residuals = tuple(beta[0] + beta[1]*(t-T0) + beta[2]*g(t-tau, duration)-y
                      for t, y in zip(times, values))
    require(max(abs(r) for r in residuals) <= beta[3], 'residual bound failure')
    return residuals


def clock_checks(times, values, tau, duration, beta, dual, residuals):
    transformed = []
    for alpha in FACTORS:
        mapped_times = tuple(T0 + alpha*(t-T0) for t in times)
        mapped_tau, mapped_D = T0 + alpha*(tau-T0), alpha*duration
        mapped_beta = (beta[0], beta[1]/alpha, beta[2]/alpha**2, beta[3])
        mapped_dual = list(dual)
        mapped_dual[-2] *= alpha**2
        require(all(g(alpha*(t-tau), mapped_D) == alpha**2*g(t-tau, duration)
                    for t in times), 'basis clock covariance failure')
        check = certificate(mapped_times, values, mapped_tau, mapped_D,
                            mapped_beta, tuple(mapped_dual))
        require(check == residuals, 'clock changed position residuals')
        require(phases(mapped_times, mapped_tau, mapped_D) == phases(times, tau, duration),
                'clock changed phase membership')
        transformed.append({'alpha': alpha, 'tau': mapped_tau, 'D': mapped_D,
                            'beta': mapped_beta,
                            'extra': max(F(0), mapped_beta[3]-EPS)})
    return transformed


def synthetic(tau, duration, acceleration=F(-8)):
    return tuple(F(100) + (t-T0)/4 + acceleration*g(t-tau, duration) for t in TIMES)


def expected_controls():
    specs = {}
    for duration in DURATIONS:
        specs[('known', F(38, 5), duration)] = synthetic(F(38, 5), duration)
        specs[('line', F(38, 5), duration)] = synthetic(F(38, 5), duration, F(0))
        specs[('all_post', F(4), duration)] = synthetic(F(4), F(0))
    altered = list(synthetic(F(38, 5), F(0)))
    altered[3] += 1
    specs[('outlier', F(38, 5), F(0))] = tuple(altered)
    specs[('upward', F(38, 5), F(0))] = synthetic(F(38, 5), F(0), F(8))
    offgrid = synthetic(F(61, 8), F(0))
    for duration in DURATIONS:
        for tau in ONSETS:
            specs[('offgrid_step', tau, duration)] = offgrid
    require(len(specs) == 178, 'synthetic specification count')
    return specs


def read_source():
    for path, expected in SOURCE_PINS.items():
        require(pin(path)['sha256'] == expected, 'source pin mismatch: '+path.name)
    independent = json.loads((SOURCE/'transcription-independent/table47.json').read_text())
    root = json.loads((SOURCE/'transcription-root/table47.json').read_text())
    require(len(independent['rows']) == len(root['rows']) == 70, 'source row count')
    root_by_id = {r['row']: r for r in root['rows']}
    require(len(root_by_id) == 70, 'duplicate root source rows')
    selected = [r for r in independent['rows'] if all(r[key] is not None for key in FIELDS.values())]
    require(tuple(fraction(r['time_s']) for r in selected) == TIMES,
            'full common position intersection differs')
    require([r['source_row'] for r in selected] == list(range(38, 54)), 'source membership')
    for row in selected:
        other = root_by_id[row['source_row']]
        require(row['time_s'] == other['time_s'], 'literal time transcription mismatch')
        for target, field in FIELDS.items():
            require(row[field] == other[target+'_y'], 'literal position transcription mismatch')
    return {target: tuple(fraction(row[field]) for row in selected)
            for target, field in FIELDS.items()}, [r['source_row'] for r in selected]


def verify_fit(fit, expected_values):
    tau, duration = fraction(fit['tau']), fraction(fit['D'])
    times = tuple(map(fraction, fit['times']))
    values = tuple(map(fraction, fit['y']))
    require(times == TIMES, 'fit changed full common time membership')
    require(values == expected_values, 'fit values differ from declared inputs')
    beta = tuple(map(fraction, fit['beta']))
    dual = tuple(map(fraction, fit['dual']))
    residuals = certificate(times, values, tau, duration, beta, dual)
    require(tuple(map(fraction, fit['residuals'])) == residuals, 'saved residual mismatch')
    require(fraction(fit['extra']) == max(F(0), beta[3]-EPS), 'extra allowance mismatch')
    require(fit['phase_counts'] == phases(times, tau, duration), 'saved phase counts mismatch')
    require(F(str(fit['activity_threshold'])) in THRESHOLDS, 'undeclared activity threshold')
    clocks = clock_checks(times, values, tau, duration, beta, dual, residuals)
    return {'label': fit['label'], 'tau': tau, 'D': duration, 'beta': beta,
            'R': beta[3], 'extra': max(F(0), beta[3]-EPS),
            'printing_compatible': beta[3] <= EPS,
            'phase_counts': phases(times, tau, duration), 'clocks': clocks}


def summarize(checked):
    groups = {}
    for result in checked:
        groups.setdefault((result['label'], result['D']), []).append(result)
    summaries = []
    for (label, duration), group in sorted(groups.items()):
        best = min(row['R'] for row in group)
        winners = sorted((r for r in group if r['R'] == best), key=lambda r:r['tau'])
        summaries.append({'label': label, 'D': duration, 'R': best,
                          'extra': max(F(0), best-EPS), 'printing_compatible': best <= EPS,
                          'onsets': [r['tau'] for r in winners],
                          'grid_boundary': any(r['tau'] in (ONSETS[0], ONSETS[-1]) for r in winners),
                          'zero_acceleration_winner': any(r['beta'][2] == 0 for r in winners),
                          'winners': winners})
    for item in summaries:
        step = next((s for s in summaries if s['label'] == item['label'] and s['D'] == 0), None)
        if step is not None:
            delta = item['R']-step['R']
            item['delta_R_from_step'] = delta
            item['residual_order_vs_step'] = 'lower' if delta < 0 else 'higher' if delta > 0 else 'equal'
            item['both_printing_compatible_with_step'] = item['printing_compatible'] and step['printing_compatible']
    return summaries


def compare_summaries(saved, computed):
    core = ('label','D','R','extra','printing_compatible','onsets','grid_boundary','zero_acceleration_winner')
    normalized = []
    for row in saved:
        normalized.append({key: row[key] for key in core})
    expected = [{key: encode(row[key]) for key in core} for row in computed]
    require(sorted(normalized,key=lambda r:(r['label'],F(r['D']))) ==
            sorted(expected,key=lambda r:(r['label'],F(r['D']))), 'saved minima/ties summary mismatch')


def verify_controls(record):
    specs = expected_controls()
    fits = record['fits']
    require(len(fits) == 178, 'all 178 synthetic fits required')
    seen, checked = set(), []
    for fit in fits:
        key = (fit['label'], fraction(fit['tau']), fraction(fit['D']))
        require(key in specs and key not in seen, 'missing/duplicate/unknown synthetic membership')
        seen.add(key)
        result = verify_fit(fit, specs[key])
        label, _, duration = key
        b,v,a,R = result['beta']
        if label == 'known':
            require((b,v,a,R) == (100,F(1,4),-8,0), 'known-parameter control failure')
        elif label == 'line':
            require((b,v,a,R) == (100,F(1,4),0,0), 'line/unidentified control failure')
        elif label == 'all_post':
            expected_b = F(100)-8*(duration*(T0-4)/2-duration**2/6)
            require((b,v,a,R) == (expected_b,F(1,4)-4*duration,-8,0), 'all-post nuisance control failure')
        elif label == 'outlier':
            require(R > EPS, 'outlier must exceed printing tolerance')
        elif label == 'upward':
            require(a == 0, 'upward constrained-boundary control failure')
        checked.append(result)
    require(seen == set(specs), 'incomplete synthetic coverage')
    summaries = summarize(checked)
    compare_summaries(record['summary'], summaries)
    return {'fits_verified': len(checked), 'clock_certificates_verified': 3*len(checked),
            'summaries': summaries}


def verify_history(record, values):
    expected = [(label,tau,duration) for label in FIELDS for duration in DURATIONS for tau in ONSETS]
    fits = record['fits'];require(len(fits) == 656, 'all 656 historical cases required')
    keys = [(r['label'],fraction(r['tau']),fraction(r['D'])) for r in fits]
    require(keys == expected, 'historical grid order/membership changed')
    checked = []
    for fit in fits:
        require(fit['target'] == fit['label'], 'target/label disagreement')
        checked.append(verify_fit(fit, values[fit['label']]))
    summaries = summarize(checked)
    compare_summaries(record['summary'], summaries)
    return {'fits_verified': len(checked), 'clock_certificates_verified': 3*len(checked),
            'summaries': summaries}


def expect_rejection(call):
    try:
        call()
    except (ValueError, TypeError, KeyError, ZeroDivisionError):
        return
    raise ValueError('negative control was accepted')


def nonsingular_basis(rows):
    require(len(rows) == 4 and all(len(r) == 4 for r in rows), 'basis dimensions')
    a = [list(row) for row in rows]
    for col in range(4):
        pivot = next((i for i in range(col,4) if a[i][col]), None)
        require(pivot is not None, 'singular exact basis')
        a[col],a[pivot] = a[pivot],a[col]
        divisor = a[col][col];a[col] = [x/divisor for x in a[col]]
        for i in range(col+1,4):
            factor = a[i][col];a[i] = [x-factor*y for x,y in zip(a[i],a[col])]


def self_tests():
    for duration in DURATIONS[1:]:
        require(g(F(0),duration) == 0 and g(duration,duration) == duration**2/6,
                'integrated-basis boundary continuity')
        require(g(duration/2,duration) == duration**2/48, 'integrated ramp interior')
        require(g(2*duration,duration) == 7*duration**2/6, 'post-ramp basis')
    require(g(F(-1),F(0)) == g(F(0),F(0)) == 0 and g(F(2),F(0)) == 2, 'step basis')
    expect_rejection(lambda:g(F(0),F(-1)))
    expect_rejection(lambda:valid_times((F(0),F(1),F(1),F(2))))
    expect_rejection(lambda:valid_times((F(0),F(2),F(1),F(3))))
    expect_rejection(lambda:valid_times((F(0),None,F(2),F(3))))
    expect_rejection(lambda:valid_times((F(0),F(1),F(2))))
    line = synthetic(F(38,5),F(0),F(0));beta=(F(100),F(1,4),F(0),F(0))
    dual = (F(0),)*33+(F(1),)
    residuals=certificate(TIMES,line,F(38,5),F(0),beta,dual)
    clock_checks(TIMES,line,F(38,5),F(0),beta,dual,residuals)
    expect_rejection(lambda:certificate(TIMES,line,F(38,5),F(0),(F(101),*beta[1:]),dual))
    expect_rejection(lambda:certificate(TIMES,line,F(38,5),F(0),beta,(F(0),)*34))
    B,_=constraints(TIMES,line,F(38,5),F(0))
    expect_rejection(lambda:nonsingular_basis([B[0]]*4))
    # An analytic certificate for the already-declared upward synthetic case.
    # Its nonzero a-bound multiplier exercises the nontrivial clock transform.
    upward=synthetic(F(38,5),F(0),F(8))
    beta_up=(F(12104,125),F(457,100),F(0),F(396,125))
    lam=[F(0)]*34;lam[1]=F(1,5);lam[18]=F(1,2);lam[31]=F(3,10);lam[32]=F(99,250)
    residuals=certificate(TIMES,upward,F(38,5),F(0),beta_up,tuple(lam))
    clock_checks(TIMES,upward,F(38,5),F(0),beta_up,tuple(lam),residuals)
    return {'piecewise_basis_controls': 'passed', 'input_rejection_controls': 'passed',
            'mutated_primal_dual_rejected': True, 'singular_basis_rejected': True,
            'analytic_line_and_upward_certificates': 'passed',
            'clock_nonzero_acceleration_bound_multiplier': 'passed'}


def local_input(name):
    path=Path(name)
    if not path.is_absolute():path=HERE/path
    require(path.parent.resolve() == HERE.resolve() and not path.is_symlink(),
            'result input must be a nonsymlink file in this unit')
    return path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--controls')
    parser.add_argument('--historical')
    parser.add_argument('--output')
    args=parser.parse_args()
    output=None
    if args.output:
        output=local_input(args.output)
        require(output.name == 'verification01.json', 'only designated verification output allowed')
        if output.exists():raise FileExistsError('Refusing existing verification output')
    if args.self_test:
        require(not(args.controls or args.historical or output), 'self-test is read-only')
        print(json.dumps(self_tests(),sort_keys=True));return
    require(args.controls is not None, 'synthetic controls required before historical verification')
    paths=[HERE/'PROTOCOL.md',Path(__file__).resolve(),*SOURCE_PINS,local_input(args.controls)]
    if args.historical:paths.append(local_input(args.historical))
    before={str(p):pin(p) for p in paths}
    result={'scope':'certificate verification; not physical validation','self_tests':self_tests()}
    values,ids=read_source();result['source_rows']=ids
    result['controls']=verify_controls(json.loads(local_input(args.controls).read_text()))
    if args.historical:
        result['historical']=verify_history(json.loads(local_input(args.historical).read_text()),values)
    after={str(p):pin(p) for p in paths};require(before == after,'input changed during verification')
    result.update(input_pins_before=before,input_pins_after=after,python=sys.version)
    if output:
        with output.open('x') as handle:
            json.dump(encode(result),handle,indent=2,sort_keys=True);handle.write('\n')
    print(json.dumps({'controls_verified':result['controls']['fits_verified'],
                      'historical_verified':result.get('historical',{}).get('fits_verified',0),
                      'output_sha256':pin(output)['sha256'] if output else None}))


if __name__ == '__main__':
    main()
