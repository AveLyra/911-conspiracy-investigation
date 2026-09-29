#!/usr/bin/env python3
"""Exact arithmetic on frozen printed values; no solver or inferred properties."""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf')
SOURCE_SHA = '30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f'
DATA_SHA = '476051df3c2c58689b8dccc20a8a6a6f3ba9d246cca1445ca1d0a40596eebcf4'
PROTOCOL_SHA = '32b68c94b0a5c60edcc4e3689f1b742aca1666d086b3bffdad3fff5384524e3b'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def half_unit(s):
    if not isinstance(s, str) or not re.fullmatch(r'\d+(?:\.\d+)?', s):
        raise ValueError('Not an unsigned displayed decimal')
    places = len(s.split('.')[1]) if '.' in s else 0
    return F(1, 2 * 10**places)


def fmt(value):
    with localcontext() as ctx:
        ctx.prec = 40
        dec = Decimal(value.numerator) / Decimal(value.denominator)
        return {'fraction': str(value), 'decimal_16dp': format(dec, '.16f')}


def span(s):
    q, h = F(s), half_unit(s)
    return q - h, q + h


def quotient_span(f, d):
    fl, fh = span(f)
    dl, dh = span(d)
    if fl <= 0 or dl <= 0:
        raise ValueError('Positive interval inputs required')
    return fl / dh, fh / dl


def overlap(a, b):
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    return {'possible': lo <= hi, 'endpoint_only': lo == hi,
            'intersection_low': fmt(lo) if lo <= hi else None,
            'intersection_high': fmt(hi) if lo <= hi else None}


def controls():
    checks = [
        half_unit('10') == F(1, 2),
        half_unit('10.0') == F(1, 20),
        half_unit('0.001') == F(1, 2000),
        span('2.3') == (F(9, 4), F(47, 20)),
        quotient_span('2', '1') == (F(1), F(5)),
        overlap((F(0), F(1)), (F(1), F(2)))['endpoint_only'],
        not overlap((F(0), F(1)), (F(2), F(3)))['possible'],
        overlap((F(0), F(2)), (F(1), F(3)))['possible'],
        not overlap((F(0), F(2)), (F(1), F(3)))['endpoint_only'],
        fmt(F(1, 8))['decimal_16dp'] == '0.1250000000000000',
        F('0.601') * 75 == F(1803, 40),
    ]
    for fn, args in [(half_unit, ('NaN',)), (half_unit, ('-1',)),
                     (quotient_span, ('2', '0'))]:
        try:
            fn(*args)
        except ValueError:
            checks.append(True)
        else:
            checks.append(False)
    if not all(checks):
        raise AssertionError('Synthetic control failed')
    return len(checks)


def table_result(table):
    values, qs, ps = [], [], []
    for row in table['rows']:
        idx, page, location, member, connection, fs, ds, rs = row
        q, r = F(fs) / F(ds), F(rs)
        qspan, rspan = quotient_span(fs, ds), span(rs)
        qs.append(q)
        ps.append(r)
        values.append({
            'row': idx, 'pdf_page': page, 'location_alias': location,
            'member': member, 'connection': connection,
            'displayed': [fs, ds, rs],
            'display_half_units': [str(half_unit(s)) for s in (fs, ds, rs)],
            'quotient': fmt(q), 'quotient_minus_printed': fmt(q-r),
            'printed_ratio_interval': [fmt(x) for x in rspan],
            'input_rounding_quotient_interval': [fmt(x) for x in qspan],
            'exact_quotient_within_printed_ratio_interval': rspan[0] <= q <= rspan[1],
            'rounding_possibility': overlap(qspan, rspan),
        })
    summary = {}
    for label, series in [('printed_ratios', ps), ('quotients', qs)]:
        v = {'mean': sum(series)/len(series), 'minimum': min(series),
             'maximum': max(series)}
        summary[label] = {key: {**fmt(val), 'within_printed_summary_rounding_interval':
            span(table['printed_summary'][key])[0] <= val <=
            span(table['printed_summary'][key])[1]} for key, val in v.items()}
    return {'count': len(values), 'rows': values,
            'summary': summary, 'source_summary': table['printed_summary'],
            'direct_outside_rows': [v['row'] for v in values if not
                v['exact_quotient_within_printed_ratio_interval']],
            'rounding_disjoint_rows': [v['row'] for v in values if not
                v['rounding_possibility']['possible']],
            'rounding_endpoint_only_rows': [v['row'] for v in values if
                v['rounding_possibility']['endpoint_only']]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    ncontrols = controls()
    if args.output.exists():
        parser.error('Refusing to overwrite output')
    inputs = {'source': (SOURCE, SOURCE_SHA),
              'transcription': (BASE/'capacity-root.json', DATA_SHA),
              'protocol': (BASE/'ARITHMETIC-PROTOCOL.md', PROTOCOL_SHA)}
    for key, (path, expected) in inputs.items():
        if sha(path) != expected:
            raise ValueError('Pin mismatch: ' + key)
    data = json.loads(inputs['transcription'][0].read_text())
    assert data['schema'] == 'printed-capacity-root/v1'
    assert set(data['tables']) == {'11-2', '11-3', '11-4'}
    for t, count in [('11-2', 22), ('11-3', 13), ('11-4', 20)]:
        rows = data['tables'][t]['rows']
        assert len(rows) == count and [r[0] for r in rows] == list(range(1, count+1))
        assert all(len(r) == 8 for r in rows)
    formulas = [
        ('A325 stress', '60/0.8', F(60)/F('.8'), '75', 531, 'ksi'),
        ('A490 stress', '75/0.8', F(75)/F('.8'), '93.75', 531, 'ksi'),
        ('A325 shear', '0.601*75', F('.601')*75, '45', 531, 'kip'),
        ('Stud strength', '0.68*1*1*0.44*65', F('.68')*F('.44')*65, '19.5', 534, 'kip'),
        ('Stud position mean', '(21.5+17.2)/2', (F('21.5')+F('17.2'))/2, '19.4', 535, 'kip'),
    ]
    output = {'schema': 'printed-capacity-calculation/v1',
              'pins': {key: expected for key, (_, expected) in inputs.items()},
              'code_sha256': sha(Path(__file__).resolve()),
              'runtime': {'python': sys.version, 'executable': sys.executable},
              'controls_passed': ncontrols,
              'tables': {t: table_result(x) for t,x in data['tables'].items()},
              'formulas': [{'label': name, 'expression': expr, 'value': fmt(v),
                  'source_printed': p, 'pdf_page': pg, 'units': units,
                  'difference_from_printed': fmt(v-F(p)),
                  'within_printed_rounding_interval': span(p)[0] <= v <= span(p)[1]}
                  for name, expr, v, p, pg, units in formulas],
              'limitations': [
                  'Closed rounding intervals test possibility, not the actual rounding rule.',
                  'No unrounded worksheet values, physical tests or model execution.',
                  'Means are unweighted diagnostics, not an inferred NIST weighting rule.',
                  'Root location aliases in Table11-4 do not reclassify core floor girders as beams.',
              ]}
    with args.output.open('x') as handle:
        json.dump(output, handle, indent=2, sort_keys=True)
        handle.write('\n')
    print(json.dumps({'status': 'passed', 'controls': ncontrols,
        'rows': sum(t['count'] for t in output['tables'].values()),
        'outside_point_ratio_interval': {t:x['direct_outside_rows'] for t,x in output['tables'].items()},
        'rounding_disjoint': {t:x['rounding_disjoint_rows'] for t,x in output['tables'].items()},
        'output_sha256': sha(args.output)}))


if __name__ == '__main__':
    main()
