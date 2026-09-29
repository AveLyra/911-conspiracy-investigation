#!/usr/bin/env python3
"""Root exact-rational TN1749 displayed-table audit; no original-stage stats."""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def half_unit(text):
    exponent = Decimal(text).as_tuple().exponent
    return F(10) ** exponent / 2


def percent(model, mean):
    if mean <= 0:
        raise ValueError('nonpositive denominator')
    return 100 * (model / mean - 1)


def calculate(model_s, mean_s, printed_s):
    model, mean, printed = map(F, (model_s, mean_s, printed_s))
    dm, de, dp = map(half_unit, (model_s, mean_s, printed_s))
    if mean - de <= 0:
        raise ValueError('nonpositive denominator interval')
    if model - dm < 0:
        raise ValueError('negative model interval outside protocol')
    point = percent(model, mean)
    lo, hi = percent(model - dm, mean + de), percent(model + dm, mean - de)
    pl, ph = printed - dp, printed + dp
    il, ih = max(lo, pl), min(hi, ph)
    relation = 'disjoint' if il > ih else ('endpoint_only' if il == ih else 'overlap')
    return {
        'point_percent': point, 'point_minus_printed_pp': point - printed,
        'computed_interval': [lo, hi], 'printed_interval': [pl, ph],
        'intersection': None if il > ih else [il, ih],
        'relation': relation, 'point_within_printed_interval': pl <= point <= ph,
    }


def encoded(value):
    if isinstance(value, F):
        with localcontext() as ctx:
            ctx.prec = 40
            decimal = str(Decimal(value.numerator) / Decimal(value.denominator))
        return {'fraction': str(value), 'decimal': decimal}
    if isinstance(value, list):
        return [encoded(v) for v in value]
    if isinstance(value, dict):
        return {k: encoded(v) for k, v in value.items()}
    return value


def controls():
    checks = {}
    checks['zero'] = percent(F(1), F(1)) == 0
    checks['positive_sign'] = percent(F(2), F(1)) == 100
    checks['negative_sign'] = percent(F(1), F(2)) == -50
    checks['decimal_precision'] = half_unit('0.120') == F(1, 2000)
    checks['trailing_zero_precision'] = half_unit('1.00') == F(1, 200)
    checks['rounding_overlap'] = calculate('1.0', '3.0', '-65.0')['relation'] == 'overlap'
    checks['nonoverlap'] = calculate('1.00', '1.00', '20.0')['relation'] == 'disjoint'
    endpoint = calculate('1.50', '1.00', '50.5')
    # A separately explicit interval fixture tests equality without float tolerance.
    def overlap(a, b):
        lo, hi = max(a[0], b[0]), min(a[1], b[1])
        return 'disjoint' if lo > hi else ('endpoint_only' if lo == hi else 'overlap')
    checks['endpoint_only'] = overlap([F(0), F(1)], [F(1), F(2)]) == 'endpoint_only'
    checks['fractional_fixture'] = endpoint['point_percent'] == 50
    for name, fn in [
        ('zero_denominator', lambda: percent(F(1), F(0))),
        ('negative_denominator', lambda: percent(F(1), F(-1))),
        ('interval_denominator', lambda: calculate('1.0', '0.0', '0.0')),
        ('negative_model_interval', lambda: calculate('0.0', '1.0', '0.0')),
    ]:
        try:
            fn()
            checks[name] = False
        except ValueError:
            checks[name] = True
    checks['fraction_encoding'] = encoded(F(1, 3))['fraction'] == '1/3'
    assert all(checks.values()), checks
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--input-sha', required=True)
    parser.add_argument('--protocol-sha', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('refuse overwrite')
    base = args.input.parent
    protocol = base / 'ARITHMETIC-PROTOCOL.md'
    assert sha(args.input) == args.input_sha, 'input pin changed'
    assert sha(protocol) == args.protocol_sha, 'protocol pin changed'
    data = json.loads(args.input.read_text())
    source = (base / data['source']).resolve()
    assert sha(source) == data['source_sha256'], 'source pin changed'
    assert {(r['table'], r['bolts']) for r in data['rows']} == {
        (t, b) for t in ('3-3', '3-4') for b in (3, 4, 5)
    }
    assert len(data['rows']) == 6
    results = []
    for r in data['rows']:
        for model in ('detailed', 'reduced'):
            results.append({
                'table': r['table'], 'bolts': r['bolts'], 'model': model,
                'unit': r['unit'], 'mean': r['mean'], 'cov': r['cov'], 'n': r['n'],
                'value': r[model]['value'], 'printed_deviation': r[model]['deviation'],
                **encoded(calculate(r[model]['value'], r['mean'], r[model]['deviation']))
            })
    result = {
        'schema': 'root-tn1749-v1', 'python': platform.python_version(),
        'pins': {'input': sha(args.input), 'protocol': sha(protocol),
                 'source': sha(source), 'code': sha(Path(__file__))},
        'controls': controls(), 'comparisons': results,
        'scope': 'Displayed summary arithmetic only; no original-stage statistics or historical model validation.'
    }
    assert sha(args.input) == args.input_sha
    assert sha(protocol) == args.protocol_sha
    assert sha(source) == data['source_sha256']
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'rows': len(results), 'controls': len(result['controls']),
                      'relations': [r['relation'] for r in results],
                      'output_sha256': sha(args.output)}))


if __name__ == '__main__':
    main()
