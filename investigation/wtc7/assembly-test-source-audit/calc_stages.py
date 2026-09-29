#!/usr/bin/env python3
"""Native-unit sensitivity to reported failure stage; no TN conversion."""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
import json
from pathlib import Path
import platform
from calc_assembly import encoded, sha

ROOT_SHA = '3265861472770daee4fe35df339d91a419c175a9bb793c73f225a5cd3adb07ac'
PROTOCOL_SHA = '7f1c6ddb2425891869c369e115c8f66eb77836cfdd2bcddbb034bc4ddfee46c4'


def select(record, rule):
    if rule not in ('initial', 'maximum_reported_stage'):
        raise ValueError('unknown selection')
    stage = 'initial'
    second = record.get('secondary')
    if rule == 'maximum_reported_stage' and second is not None:
        if F(second['shear']) > F(record['initial']['shear']):
            stage = 'secondary'
    return stage, record[stage]


def stats(values):
    values = list(map(F, values))
    if len(values) < 2:
        raise ValueError('variance requires at least two values')
    mean = sum(values, F(0)) / len(values)
    if mean <= 0:
        raise ValueError('COV requires positive mean')
    ss = sum(((v - mean) ** 2 for v in values), F(0))
    out = {'n': len(values), 'mean': encoded(mean)}
    with localcontext() as ctx:
        ctx.prec = 40
        mean_d = Decimal(mean.numerator) / Decimal(mean.denominator)
        for label, denominator in [('sample', len(values)-1), ('population', len(values))]:
            variance = ss / denominator
            sd = (Decimal(variance.numerator) / Decimal(variance.denominator)).sqrt()
            out[label] = {'variance': encoded(variance), 'sd': str(sd),
                          'cov_percent': str(100 * sd / mean_d)}
    return out


def controls():
    checks = {}
    r = {'initial': {'shear':'2', 'rotation':'9'},
         'secondary': {'shear':'3', 'rotation':'4'}}
    checks['initial_rule'] = select(r, 'initial')[0] == 'initial'
    checks['secondary_larger'] = select(r, 'maximum_reported_stage')[0] == 'secondary'
    checks['associated_rotation'] = select(r, 'maximum_reported_stage')[1]['rotation'] == '4'
    r['secondary']['shear'] = '2'
    checks['tie_initial'] = select(r, 'maximum_reported_stage')[0] == 'initial'
    r['secondary']['shear'] = '1'
    checks['initial_larger'] = select(r, 'maximum_reported_stage')[0] == 'initial'
    r['secondary'] = None
    checks['null_initial'] = select(r, 'maximum_reported_stage')[0] == 'initial'
    s = stats(['1','2','3'])
    checks['mean'] = s['mean']['fraction'] == '2'
    checks['sample_variance'] = s['sample']['variance']['fraction'] == '1'
    checks['population_variance'] = s['population']['variance']['fraction'] == '2/3'
    checks['sample_sd'] = F(s['sample']['sd']) == 1
    checks['sample_cov'] = F(s['sample']['cov_percent']) == 50
    checks['constant_variance'] = stats(['2','2'])['sample']['variance']['fraction'] == '0'
    checks['exact_decimal_mean'] = stats(['0.1','0.2'])['mean']['fraction'] == '3/20'
    for name, function in [
        ('singleton_rejected', lambda: stats(['1'])),
        ('zero_mean_rejected', lambda: stats(['-1','1'])),
        ('empty_rejected', lambda: stats([])),
        ('unknown_rule_rejected', lambda: select(r, 'peak')),
    ]:
        try:
            function()
            checks[name] = False
        except ValueError:
            checks[name] = True
    assert all(checks.values()), checks
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('refuse overwrite')
    base = Path(__file__).resolve().parent
    source_json = base / 'thompson-stages-root.json'
    protocol = base / 'STAGE-DIAGNOSTIC-PROTOCOL.md'
    assert sha(source_json) == ROOT_SHA
    assert sha(protocol) == PROTOCOL_SHA
    data = json.loads(source_json.read_text())
    source = base / data['source']
    assert sha(source) == data['source_sha256']
    records = data['records']
    assert len(records) == 9
    assert {r['test'] for r in records} == {f'{b}ST{n}' for b in (3,4,5) for n in (1,2,3)}
    groups = []
    for cohort in ('all_reported', 'figure_subset_without_5ST1'):
        for bolts in (3,4,5):
            selected_records = [r for r in records if r['test'].startswith(str(bolts))
                                and not (cohort != 'all_reported' and r['test'] == '5ST1')]
            for rule in ('initial','maximum_reported_stage'):
                selected = []
                for record in selected_records:
                    stage, values = select(record, rule)
                    selected.append({'test': record['test'], 'stage': stage,
                                     'shear': values['shear'], 'rotation': values['rotation'],
                                     'secondary_available': record['secondary'] is not None,
                                     'secondary_footnote': record['secondary_footnote']})
                groups.append({'cohort':cohort, 'bolts':bolts, 'rule':rule,
                               'selected':selected, 'shear_kip':stats([r['shear'] for r in selected]),
                               'rotation_rad':stats([r['rotation'] for r in selected])})
    contrasts = []
    for record in records:
        second = record['secondary']
        if second is None:
            contrasts.append({'test':record['test'], 'secondary_minus_initial':None,
                              'secondary_footnote':record['secondary_footnote']})
        else:
            first = record['initial']
            delta = F(second['shear']) - F(first['shear'])
            contrasts.append({'test':record['test'], 'secondary_minus_initial':encoded({
                'shear_kip':delta, 'shear_percent_of_initial':100*delta/F(first['shear']),
                'rotation_rad':F(second['rotation'])-F(first['rotation'])})})
    result = {'scope':'Native printed-stage sensitivity; not global peaks or a NIST-series reconstruction.',
              'python':platform.python_version(), 'controls':controls(), 'groups':groups,
              'contrasts':contrasts, 'pins':{'input':sha(source_json), 'source':sha(source),
              'protocol':sha(protocol), 'code':sha(Path(__file__)),
              'helper':sha(base/'calc_assembly.py')}}
    assert sha(source_json) == ROOT_SHA and sha(protocol) == PROTOCOL_SHA
    assert sha(source) == data['source_sha256']
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'groups':len(groups), 'contrast_records':len(contrasts),
                      'controls':len(result['controls']), 'output_sha256':sha(args.output)}))


if __name__ == '__main__':
    main()
