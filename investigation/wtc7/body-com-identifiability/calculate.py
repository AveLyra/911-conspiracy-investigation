"""Exact synthetic identification controls, not a historical collapse model."""
import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
G = Q(10)


def pin(path):
    data = path.read_bytes()
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}


def serial(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {k: serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def curvature(values, h):
    if len(values) != 3 or h <= 0:
        raise ValueError('Three values and a positive halfspan required')
    return (values[0] - 2*values[1] + values[2]) / h**2


def affine_residual(values, h):
    delta = curvature(values, h) * h**2 / 4
    residual = [delta, -delta, delta]
    trend = [v-e for v, e in zip(values, residual)]
    assert curvature(trend, h) == 0
    assert max(map(abs, residual)) == abs(delta)
    return {'minimum_B': abs(delta), 'affine_trend': trend, 'residual': residual}


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q(0))


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0]]


def minus(a, b):
    return [x-y for x, y in zip(a, b)]


def mapped(matrix, point, translation):
    return [dot(row, point)+v for row, v in zip(matrix, translation)]


def proper(matrix):
    columns = list(zip(*matrix))
    return (all(dot(a, b) == Q(i == j)
                for i, a in enumerate(columns) for j, b in enumerate(columns))
            and dot(columns[0], cross(columns[1], columns[2])) == 1)


def recover_unit_pose(origin, x_marker, z_marker):
    # Known local points 0, e_x, e_z: recover columns of the proper rotation.
    x = minus(x_marker, origin)
    z = minus(z_marker, origin)
    y = cross(z, x)
    matrix = [list(row) for row in zip(x, y, z)]
    if not proper(matrix):
        raise ValueError('Known noncollinear unit geometry not reproduced')
    return matrix, origin


def envelope_bounds(intervals, h):
    if len(intervals) != 3 or h <= 0 or any(lo > hi for lo, hi in intervals):
        raise ValueError('Ordered intervals at three times and positive h required')
    lower = (intervals[0][0] - 2*intervals[1][1] + intervals[2][0]) / h**2
    upper = (intervals[0][1] - 2*intervals[1][0] + intervals[2][1]) / h**2
    return lower, upper


def build():
    hidden = []
    for eta, h, b in itertools.product((Q(1, 4), Q(1, 2)), (Q(1), Q(2)),
                                        (Q(1, 10), Q(1, 2))):
        times = [-h, Q(0), h]
        visible = [5*t*t for t in times]
        baseline_hidden = [v+4 for v in visible]
        changed_hidden = [v+4-(b/eta)*(2*(t/h)**2-1)
                          for v, t in zip(visible, times)]
        baseline_com = [(1-eta)*v+eta*w for v, w in zip(visible, baseline_hidden)]
        changed_com = [(1-eta)*v+eta*w for v, w in zip(visible, changed_hidden)]
        relative = minus(visible, changed_com)
        residual = affine_residual(relative, h)
        assert curvature(visible, h) == curvature(baseline_com, h) == G
        assert curvature(changed_com, h) == G-4*b/h**2
        assert residual['minimum_B'] == b
        assert max(abs(a-c) for a, c in zip(changed_hidden, baseline_hidden)) == b/eta
        hidden.append({'eta': eta, 'h': h, 'B': b, 'times': times,
                       'visible_both_histories': visible,
                       'baseline_hidden': baseline_hidden, 'alternative_hidden': changed_hidden,
                       'baseline_COM': baseline_com, 'alternative_COM': changed_com,
                       'A_point': G, 'A_COM': curvature(changed_com, h),
                       'net_upward_fraction': 1-curvature(changed_com, h)/G,
                       'hidden_excursion': b/eta, 'relative_affine_fit': residual})

    rigid = []
    local_markers = [[Q(-1), Q(0), Q(0)], [Q(0)]*3,
                     [Q(1), Q(0), Q(0)], [Q(0), Q(0), Q(1)]]
    pose_checks = 0
    distance_checks = 0
    for h, length, (cosine, sine) in itertools.product(
            (Q(1), Q(2)), (Q(1), Q(3)),
            ((Q(4, 5), Q(3, 5)), (Q(3, 5), Q(4, 5)))):
        times = [-h, Q(0), h]
        visible = [5*t*t for t in times]
        rotations = []
        all_markers = []
        centers = []
        baseline = [v+length for v in visible]
        for i, v in enumerate(visible):
            c, s = (Q(1), Q(0)) if i == 1 else (cosine, sine)
            matrix = [[Q(1), Q(0), Q(0)], [Q(0), c, -s], [Q(0), s, c]]
            assert proper(matrix)
            translation = [Q(0), Q(0), v]
            markers = [mapped(matrix, p, translation) for p in local_markers]
            for actual, p in zip(markers[:3], local_markers[:3]):
                assert actual == [p[0], Q(0), v]
            for j, k in itertools.combinations(range(4), 2):
                expected = minus(local_markers[j], local_markers[k])
                actual = minus(markers[j], markers[k])
                assert dot(actual, actual) == dot(expected, expected)
                distance_checks += 1
            recovered, shift = recover_unit_pose(markers[1], markers[2], markers[3])
            assert recovered == matrix and shift == translation
            pose_checks += 1
            rotations.append(matrix)
            all_markers.append(markers)
            centers.append(mapped(matrix, [Q(0), Q(0), length], translation)[2])
        residual = affine_residual(minus(visible, centers), h)
        expected_correction = -2*length*(1-cosine)/h**2
        assert curvature(centers, h)-G == expected_correction
        assert residual['minimum_B'] == length*(1-cosine)/2
        assert all_markers[0][3] != [Q(0), Q(0), visible[0]+1]
        rigid.append({'h': h, 'L': length, 'cos': cosine, 'sin': sine,
                      'times': times, 'roof_reference_both_histories': visible,
                      'rotations': rotations, 'markers': all_markers,
                      'baseline_COM': baseline, 'alternative_COM': centers,
                      'A_point': G, 'A_COM': curvature(centers, h),
                      'net_upward_fraction': 1-curvature(centers, h)/G,
                      'relative_affine_fit': residual})

    envelopes = []
    for name, lo, hi in [('loose', Q(0), Q(2)), ('tight', Q(9, 10), Q(11, 10))]:
        intervals = [(lo, hi)]*3
        lower, upper = envelope_bounds(intervals, Q(1))
        corners = [curvature(c, Q(1)) for c in itertools.product((lo, hi), repeat=3)]
        assert (min(corners), max(corners)) == (lower, upper)
        # All three-time corner histories for two fixed masses, not new bodies each time.
        mixtures = []
        for values in itertools.product((lo, hi), repeat=6):
            combined = [values[i]/3+2*values[i+3]/3 for i in range(3)]
            assert all(lo <= x <= hi for x in combined)
            mixtures.append(curvature(combined, Q(1)))
        assert (min(mixtures), max(mixtures)) == (lower, upper)
        force_interval = [-upper/G, -lower/G]
        envelopes.append({'name': name, 'h': Q(1), 'relative_intervals': intervals,
                          'COM_minus_point_A_interval': [lower, upper],
                          'net_upward_fraction_interval': force_interval,
                          'quarter_weight_not_excluded': force_interval[1] >= Q(1, 4),
                          'corner_cases': len(corners), 'fixed_mass_mixture_cases': len(mixtures)})

    affine_controls = []
    for values, h in itertools.product(([Q(0)]*3, [Q(-1), Q(0), Q(1)],
                                         [Q(1), Q(0), Q(1)]), (Q(1), Q(2))):
        fit = affine_residual(values, h)
        shifted = [v+7-3*t for v, t in zip(values, (-h, 0, h))]
        assert affine_residual(shifted, h)['minimum_B'] == fit['minimum_B']
        affine_controls.append({'values': values, 'h': h, 'fit': fit})
    invalid = [lambda: curvature([Q(0)]*3, Q(0)),
               lambda: curvature([Q(0)]*3, Q(-1)),
               lambda: envelope_bounds([(Q(1), Q(0))]*3, Q(1)),
               lambda: envelope_bounds([(Q(0), Q(1))]*2, Q(1)),
               lambda: recover_unit_pose([Q(0)]*3, [Q(1), Q(0), Q(0)],
                                          [Q(-1), Q(0), Q(0)])]
    rejections = 0
    for check in invalid:
        try:
            check()
        except ValueError:
            rejections += 1
    assert rejections == len(invalid)
    return {'scope': 'synthetic kinematic identification tests; not historical motion or structural feasibility',
            'g_reference_arbitrary_units': G, 'hidden_cases': hidden, 'rigid_cases': rigid,
            'envelope_cases': envelopes, 'affine_controls': affine_controls,
            'controls': {'pose_recoveries': pose_checks, 'distance_preservation_checks': distance_checks,
                         'invalid_inputs_rejected': rejections, 'all_assertions_passed': True}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, choices=('run01', 'run02'))
    args = parser.parse_args()
    out = HERE/args.out
    if out.exists():
        raise FileExistsError('Output already exists; preserving prior run')
    inputs = [HERE/'PROTOCOL.md', Path(__file__), Path(sys.executable),
              HERE.parent/'finite-interval-force/report.md']
    before = {str(p): pin(p) for p in inputs}
    result = serial(build())
    after = {str(p): pin(p) for p in inputs}
    if before != after:
        raise RuntimeError('Dependencies changed')
    out.mkdir()
    with (out/'results.json').open('x') as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write('\n')
    with (out/'receipt.json').open('x') as f:
        json.dump({'before': before, 'after': after, 'python': sys.version,
                   'inputs_unchanged': True, 'results': pin(out/'results.json')}, f, indent=2)
        f.write('\n')
    print(json.dumps({'hidden_cases': 8, 'rigid_cases': 8, 'envelopes': 2,
                      'controls': result['controls'], 'results': pin(out/'results.json')}))


if __name__ == '__main__':
    main()
