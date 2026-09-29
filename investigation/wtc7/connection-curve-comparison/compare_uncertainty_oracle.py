"""Post-freeze comparison adapter, not an independent general optimizer.

Root's analytical answers froze before producer code was read. This adapter
invokes that producer and preserves every comparison, dependency pin and output.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import platform
import re
import sys

HERE = Path(__file__).resolve().parent
EXPECTED = {
    'UNCERTAINTY-STAGE.md': '38d075e25e6c8352a4f3229736accdf12f40c09e54b6d833036052e92790e34a',
    'NUMERICAL-PROTOCOL.md': 'e03c47c1945b9eb9fd0a040d757d5f5f66bf76791ced8944323d3c92d1120df3',
    'HUMAN-REVIEW-GATE.md': '2e6f34d2e2d6d423c440c8a56b4a3c4796429d59f4d0baf0cf03609341a271ee',
    'curve_math.py': '7b5a1a3dc4cd822d0e948bdcb6ec5d2793a23bad0744f56dcfcc47980a1300e1',
    'curve_uncertainty.py': 'e8a01c17388ec62f7d2b71d7a94fda9f9fce7b2515c12344e180cc750c644042',
    'uncertainty_oracle.py': 'da9b90eef453975eeddb0c803e64ea9395813a1b54afe2102558b96af0b097b6',
}


def pins():
    names = tuple(EXPECTED) + ('test_curve_uncertainty.py', Path(__file__).name)
    return {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in names}


def evaluate_path(paths, x):
    """Separate slope/intercept evaluation solely to check returned witnesses."""
    values = []
    for path in paths:
        for (a, ya), (b, yb) in zip(path, path[1:]):
            if a <= x <= b:
                slope = Q(yb-ya) / Q(b-a)
                values.append(slope*x + Q(ya)-slope*a)
    if not values or len(set(values)) != 1:
        raise AssertionError('witness is unsupported or nonunique')
    return values[0]


def run():
    before = pins()
    if any(before[name] != wanted for name, wanted in EXPECTED.items()):
        raise ValueError('frozen input mismatch')
    import uncertainty_oracle as oracle
    import curve_uncertainty as producer

    def build(paths, label):
        if paths is None:
            return None
        return tuple(producer.SupportedBranch(f'{label}-{i}', producer.SUPPORT_TAG, path)
                     for i, path in enumerate(paths))

    comparisons = []
    for case in oracle.fixtures():
        if case['kind'] == 'local':
            actual = producer.local_envelope(build(case['curve'], 'local'), case['query'],
                                             y_radius=case['radius'])
        else:
            rr, rs, sr, ss = case['radii']
            axis = producer.SharedAxis('root-oracle-shared-axis', **case['axis'])
            actual = producer.compare_uncertain(build(case['reference'], 'reference'),
                build(case['candidate'], 'candidate'), case['query'], axis=axis,
                reference_x_radius=rr, candidate_x_radius=rs,
                reference_y_radius=sr, candidate_y_radius=ss)
            if actual['sign'] != case['expected_sign']:
                raise AssertionError(f"sign mismatch: {case['name']}")
            # Verify the shared-axis/radius metadata, not only its final interval.
            assert actual['axis']['calibration_id'] == 'root-oracle-shared-axis'
            for key, default in (('x_scale', (1, 1)), ('x_offset', (0, 0)),
                                 ('y_scale', (1, 1)), ('y_offset', (0, 0))):
                assert actual['axis'][key] == case['axis'].get(key, default)
            for key, radius in zip(('reference_x_radius', 'candidate_x_radius',
                                    'reference_y_radius', 'candidate_y_radius'), case['radii']):
                assert actual[key] == radius
            a = case['axis'].get('x_scale', (1, 1))
            b = case['axis'].get('x_offset', (0, 0))
            candidates = [Q(s)*x for s in a for x in case['query']]
            t = (min(candidates)+b[0], max(candidates)+b[1])
            assert actual['reachable_t'] == t
            assert actual['reference_demand'] == (t[0]-rr, t[1]+rr)
            assert actual['candidate_demand'] == (t[0]-rs, t[1]+rs)
            if case['expected_bounds'] is not None:
                for label, index in (('minimum', 0), ('maximum', 1)):
                    w = actual['centerline_extremizers'][label]
                    assert t[0] <= w['t'] <= t[1]
                    assert abs(w['u']-w['t']) <= rr and abs(w['v']-w['t']) <= rs
                    value = evaluate_path(case['candidate'], w['v'])-evaluate_path(case['reference'], w['u'])
                    assert value == actual['centerline_bounds'][index]
            else:
                assert actual['centerline_extremizers'] is None
        if actual['bounds'] != case['expected_bounds']:
            raise AssertionError(f"bounds mismatch: {case['name']}")
        assert actual['query'] == case['query']
        assert actual['status'] == ('unresolved' if case['expected_bounds'] is None else 'resolved')
        comparisons.append({'case': case, 'actual': actual, 'matches': True})
    after = pins()
    assert before == after
    return oracle.jsonable(dict(status='all-fixed-analytical-expectations-match',
        python=platform.python_version(), executable=sys.executable,
        input_pins_before=before, input_pins_after=after,
        local_cases=12, pair_cases=20, expected_unresolved=7,
        comparisons=comparisons,
        scope='synthetic analytical examples; not a second general optimizer or historical measurement'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', help='new local JSON basename; existing outputs are refused')
    args = parser.parse_args()
    if args.out is not None and re.fullmatch(r'[a-z0-9-]+\.json', args.out) is None:
        raise ValueError('output must be a plain lowercase local JSON basename')
    payload = json.dumps(run(), sort_keys=True, indent=2) + '\n'
    if args.out is None:
        print(payload, end='')
    else:
        with (HERE/args.out).open('x', encoding='utf-8') as f:
            f.write(payload)
        print(json.dumps({'created': args.out, 'cases': 32, 'sha256': hashlib.sha256(payload.encode()).hexdigest()}))


if __name__ == '__main__':
    main()
