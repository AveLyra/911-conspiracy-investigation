"""Harmless exact controls, executed before loading historical table bytes."""
from fractions import Fraction as F
from pathlib import Path
import json
import tempfile
import chain_oracle as q


def edge(a, lo, hi):
    return {'left': a, 'right': a+2, 'center': a+1, 'lo': F(lo), 'hi': F(hi)}


def synthetic_rows(n=10, slope=0):
    rows = []
    for i in range(n):
        row = {'source_row': i+1, 'time_s': f'{i/5:.1f}'}
        for prefix in q.POINTS.values():
            row[prefix+'_y'] = f'{4+slope*i/5:.2f}'
            row[prefix+'_v'] = f'{slope:.2f}' if 0 < i < n-1 else None
        rows.append(row)
    return rows


def refusal(call):
    try:
        call()
    except (ValueError, FileExistsError):
        return
    raise AssertionError('Expected explicit refusal')


def run_controls():
    passed = []
    for slope in (0, 2, -3):
        rows = synthetic_rows(slope=slope)
        q.validate_rows(rows)
        bounds, links, unsupported = q.problem(rows, 'ne_corner', F(2, 5))
        result = q.solve(bounds, links)
        assert result['feasible'] and not result['boundary_only'] and not unsupported
        assert len(result['chains']) == 2 and len(links) == 8
        q.validate_witness(bounds, links, result['witness'])
        passed.append('constant_or_linear_'+str(slope))

    bounds = {0: (F(0), F(1)), 2: (F(1), F(2)), 4: (F(2), F(3))}
    links = [edge(0, F(3, 4), F(5, 4)), edge(2, F(3, 4), F(5, 4))]
    base = q.solve(bounds, links)
    shift = F(137, 19)
    translated = q.solve({i: (lo+shift, hi+shift) for i, (lo, hi) in bounds.items()}, links)
    assert translated['witness'] == {i: value+shift for i, value in base['witness'].items()}
    passed.append('translation_invariance')

    bounds = {0: (F(0), F(1)), 2: (F(3), F(4))}
    links = [edge(0, 1, 2)]
    result = q.solve(bounds, links)
    assert result['feasible'] and result['boundary_only']
    assert result['witness'] == {0: F(1), 2: F(3)}
    passed.append('closed_endpoint_only_feasible')
    bounds[2] = (F(301, 100), F(4))
    result = q.solve(bounds, links)
    assert not result['feasible']
    q.validate_certificate(bounds, links, result['chains'][0]['contradiction']['certificate'])
    passed.append('beyond_endpoint_infeasible')

    bounds = {i: (F(0), F(1)) for i in (0, 2, 4)}
    links = [edge(0, F(3, 4), 1), edge(2, F(3, 4), 1)]
    assert all(q.solve({i: bounds[i] for i in (e['left'], e['right'])}, [e])['feasible'] for e in links)
    result = q.solve(bounds, links)
    assert not result['feasible']
    cert = result['chains'][0]['contradiction']['certificate']
    q.validate_certificate(bounds, links, cert)
    assert cert['sum_rhs'] == F(-1, 2)
    passed.append('rowwise_feasible_jointly_impossible')
    refusal(lambda: q.validate_certificate(bounds, links, {**cert, 'sum_rhs': F(0)}))
    refusal(lambda: q.validate_certificate(bounds, links, {**cert, 'atoms': ['not-an-input']}))
    passed.append('two_corrupt_certificates_refused')

    disconnected = q.solve(bounds, links[:1])
    assert disconnected['feasible'] and len(disconnected['chains']) == 2
    q.validate_witness(bounds, links[:1], disconnected['witness'])
    passed.append('disconnected_missing_velocity_chain')
    refusal(lambda: q.validate_witness(bounds, links[:1], {0: 0, 2: 1}))
    refusal(lambda: q.validate_witness(bounds, links[:1], {0: 0, 2: 2, 4: 0}))
    refusal(lambda: q.validate_witness(bounds, links[:1], {0: 1, 2: 0, 4: 0}))
    passed.append('three_corrupt_witnesses_refused')

    rows = synthetic_rows()
    rows[4]['ne_corner_y'] = None
    bounds, links, unsupported = q.problem(rows, 'ne_corner', F(2, 5))
    assert 4 not in bounds and any(e['center'] == 4 for e in links)
    assert [u['source_row'] for u in unsupported] == [4, 6]
    assert q.solve(bounds, links)['feasible']
    passed.append('center_position_not_required_missing_neighbors_retained')
    rows = synthetic_rows()
    rows[0]['nw_corner_v'] = '0.00'
    _, links, unsupported = q.problem(rows, 'nw_corner', F(2, 5))
    assert len(links) == 8 and [u['source_row'] for u in unsupported] == [1]
    passed.append('unsupported_first_velocity_not_invented')

    for kind in ('duplicate', 'unsorted', 'non_grid', 'bad_decimal'):
        rows = synthetic_rows()
        if kind == 'duplicate':
            rows[3]['source_row'] = rows[2]['source_row']
        elif kind == 'unsorted':
            rows[2], rows[3] = rows[3], rows[2]
        elif kind == 'non_grid':
            rows[3]['time_s'] = '0.61'
        else:
            rows[3]['ne_corner_y'] = 4.0
        refusal(lambda: q.validate_rows(rows))
        passed.append('malformed_'+kind+'_refused')
    refusal(lambda: q.solve({0: (F(0), F(1)), 2: (F(0), F(1))}, [edge(0, 0, 1)]*2))
    passed.append('duplicate_constraint_refused')
    with tempfile.TemporaryDirectory(prefix='synthetic-create-only-', dir=q.HERE) as temporary:
        directory = Path(temporary)
        before = list(directory.iterdir())
        refusal(lambda: q.create_output(directory))
        assert list(directory.iterdir()) == before
    passed.append('existing_output_refused_unchanged')
    return passed


if __name__ == '__main__':
    tests = run_controls()
    print(json.dumps({'status': 'PASS', 'control_groups': len(tests), 'controls': tests}, indent=2))
