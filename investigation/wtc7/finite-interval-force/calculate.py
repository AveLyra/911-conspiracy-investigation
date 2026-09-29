"""Exact conditional finite-interval calculation; no new media measurements."""
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
TABLE = HERE.parent / 'multipoint-table-reproduction/transcription-root/table47.json'
PDF = HERE.parent / 'luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf'
TABLE_SHA = 'a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc'
PDF_SHA = 'cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394'
WINDOWS = {'ne': ('8.0', '8.6', '9.2'),
           'ec': ('8.2', '9.4', '10.6'),
           'wc': ('8.2', '9.4', '10.6'),
           'nw': ('8.2', '9.4', '10.6')}
CLOCKS = {'nominal': F(1), 'six_frames_30000_1001': F(1001, 1000),
          'six_frames_2997_100': F(1000, 999)}
RHO = tuple(map(F, ('0', '0.1', '0.25', '0.5', '0.75', '1')))
G, PRINT_ERROR = F('9.81'), F('0.005')


def pin(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def pack(x):
    return {'exact': str(x), 'decimal': float(x)}


def second_difference(values, halfspan):
    if halfspan <= 0 or len(values) != 3:
        raise ValueError('Three values and positive halfspan required')
    return (values[0] - 2 * values[1] + values[2]) / halfspan**2


def select(table, point, times):
    rows = table['rows']
    chosen = []
    for t in times:
        matches = [r for r in rows if F(r['time_s']) == F(t)]
        if len(matches) != 1:
            raise ValueError('Missing or duplicate time')
        row = matches[0]
        value = row.get(point + '_y')
        if not isinstance(value, str):
            raise ValueError('Missing/nontext position')
        F(value)  # Reject malformed decimal tokens.
        chosen.append(row)
    if F(times[1]) - F(times[0]) != F(times[2]) - F(times[1]):
        raise ValueError('Times must be equally spaced')
    return chosen


def controls():
    # Analytic integral of p'' against normalized triangular kernel.
    polynomial_checks = 0
    for coeff in ((F(4),), (F(4), F(-7)), (F(0), F(0), G / 2),
                  (F(2), F(3), F(-5), F(7)),
                  (F(-2), F(1), F(3), F(-4), F(5), F(6))):
        for h in (F('0.6'), F('1.2'), F('2.3')):
            values = [sum(c * t**n for n, c in enumerate(coeff))
                      for t in (-h, F(0), h)]
            integral = F(0)
            for n in range(2, len(coeff)):
                k = n - 2
                if k % 2 == 0:
                    moment = 2 * h**k / ((k + 1) * (k + 2))
                    integral += coeff[n] * n * (n - 1) * moment
            assert second_difference(values, h) == integral
            affine = [v + F(103) - 17*t for v, t in zip(values, (-h, 0, h))]
            assert second_difference(affine, h) == integral
            polynomial_checks += 1
    sharpness = []
    for h in (F('0.6'), F('1.2')):
        b = F('0.17')
        corners = [second_difference([s*b for s in signs], h)
                   for signs in itertools.product((-1, 1), repeat=3)]
        assert min(corners) == -4*b/h**2 and max(corners) == 4*b/h**2
        sharpness.append({'h': str(h), 'corner_cases': len(corners),
                          'minimum': str(min(corners)), 'maximum': str(max(corners))})
    good = {'rows': [{'time_s': str(t), 'row': i, 'ne_y': '0.00'}
                     for i, t in enumerate((F(0), F(1), F(2)))]}
    bad = [({'rows': []}, ('0', '1', '2')),
           ({'rows': good['rows'] + good['rows'][:1]}, ('0', '1', '2')),
           ({'rows': [dict(r, ne_y=None) for r in good['rows']]}, ('0', '1', '2')),
           ({'rows': [dict(r, ne_y='bad') for r in good['rows']]}, ('0', '1', '2')),
           (good, ('0', '1', '1'))]
    rejected = 0
    for table, times in bad:
        try:
            select(table, 'ne', times)
        except (ValueError, ZeroDivisionError):
            rejected += 1
    assert rejected == len(bad)
    return {'polynomial_and_affine_checks': polynomial_checks,
            'corner_sharpness': sharpness, 'invalid_inputs_rejected': rejected}


def calculate(table):
    results = []
    for point, times in WINDOWS.items():
        chosen = select(table, point, times)
        positions = [-F(r[point + '_y']) for r in chosen]
        for clock, factor in CLOCKS.items():
            h = (F(times[1]) - F(times[0])) * factor
            a = second_difference(positions, h)
            error = 4 * PRINT_ERROR / h**2
            lo, hi = a - error, a + error
            intercept, slope = h**2 * (lo - G) / 4, h**2 * G / 4
            values = [{'rho_at_least': str(r),
                       'minimum_B': pack(max(F(0), intercept + slope * r))}
                      for r in RHO]
            # Every corner of the three rounded positions must attain or lie
            # inside the claimed acceleration bounds.
            extrema = [second_difference([p + s*PRINT_ERROR for p, s in zip(positions, signs)], h)
                       for signs in itertools.product((-1, 1), repeat=3)]
            assert min(extrema) == lo and max(extrema) == hi
            # A sharp witness at a_low and e=(B,-B,B) attains each positive
            # necessary threshold. It is mathematical, not a WTC7 model.
            for item in values:
                rho = F(item['rho_at_least'])
                b = F(item['minimum_B']['exact'])
                a_com = lo - 4*b/h**2
                net_fraction = 1 - a_com/G
                assert net_fraction >= rho
                if b > 0:
                    assert net_fraction == rho
            results.append({'point': point, 'clock': clock,
                            'clock_multiplier': str(factor), 'halfspan_s': str(h),
                            'source_time_tokens': list(times),
                            'source_rows': [r['row'] for r in chosen],
                            'source_y_tokens_upward': [r[point + '_y'] for r in chosen],
                            'downward_second_difference': pack(a),
                            'printing_only_interval': [pack(lo), pack(hi)],
                            'B_hinge_intercept': pack(intercept),
                            'B_hinge_slope': pack(slope), 'scenarios': values})
    assert len(results) == 12 and sum(len(x['scenarios']) for x in results) == 72
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, choices=('run01', 'run02'))
    args = parser.parse_args()
    out = HERE / args.out
    if out.exists():
        raise FileExistsError('Refusing existing output')
    inputs = [TABLE, PDF, HERE/'PROTOCOL.md', Path(__file__), Path(sys.executable)]
    before = {str(p): pin(p) for p in inputs}
    assert before[str(TABLE)]['sha256'] == TABLE_SHA
    assert before[str(PDF)]['sha256'] == PDF_SHA
    table = json.loads(TABLE.read_text())
    assert table['source_sha256'] == PDF_SHA and table['physical_and_printed_page'] == 47
    result = {'scope': 'conditional assigned-coordinate constraint; not historical force',
              'gravity_reference': str(G), 'printing_error_per_position': str(PRINT_ERROR),
              'controls': controls(), 'cases': calculate(table)}
    after = {str(p): pin(p) for p in inputs}
    if before != after:
        raise RuntimeError('Inputs changed')
    out.mkdir()
    with (out/'results.json').open('x') as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write('\n')
    with (out/'receipt.json').open('x') as f:
        json.dump({'before': before, 'after': after, 'inputs_unchanged': True,
                   'python': sys.version, 'results': pin(out/'results.json')}, f, indent=2)
        f.write('\n')
    print(json.dumps({'cases': 12, 'threshold_evaluations': 72,
                      'controls': result['controls'], 'results': pin(out/'results.json')}))


if __name__ == '__main__':
    main()
