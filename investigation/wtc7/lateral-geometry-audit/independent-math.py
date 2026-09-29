"""Exact four-vertex synthetic oracle; no producer or historical-data imports."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / 'MATH-PROTOCOL.md'
OUTPUT = HERE / 'independent-math01.json'


def pin(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def dot(a, b):
    if len(a) != len(b):
        raise ValueError('dimension mismatch')
    return sum((x * y for x, y in zip(a, b)), F(0))


def solve(rows, q):
    """Two-pivot Gauss-Jordan elimination, not an interval-radius formula."""
    a = [[F(x) for x in row] + [F(value)] for row, value in zip(rows, q)]
    if len(a) != 2 or any(len(row) != 3 for row in a):
        raise ValueError('expected two-dimensional system')
    for column in range(2):
        pivot = next((i for i in range(column, 2) if a[i][column]), None)
        if pivot is None:
            raise ValueError('singular: unique inversion unavailable')
        a[column], a[pivot] = a[pivot], a[column]
        divisor = a[column][column]
        a[column] = [value / divisor for value in a[column]]
        for i in range(2):
            if i != column:
                multiplier = a[i][column]
                a[i] = [x - multiplier * y for x, y in zip(a[i], a[column])]
    answer = (a[0][2], a[1][2])
    assert tuple(dot(row, answer) for row in rows) == tuple(q)
    return answer


def corners(rows, q, error):
    if len(error) != 2 or any(value < 0 for value in error):
        raise ValueError('negative or malformed error bound')
    residual_bounds = [(value - width, value + width)
                       for value, width in zip(q, error)]
    vertices = []
    for signs in product((-1, 1), repeat=2):
        residual = tuple(q[i] + signs[i] * error[i] for i in range(2))
        vertices.append({'signs': signs, 'q': residual,
                         'd': solve(rows, residual)})
    intervals = tuple((min(v['d'][i] for v in vertices),
                       max(v['d'][i] for v in vertices)) for i in range(2))
    origin_feasible = all(lo <= 0 <= hi for lo, hi in residual_bounds)
    north_zero = intervals[1][0] <= 0 <= intervals[1][1]
    witness = None
    if north_zero:
        low = min(vertices, key=lambda v: v['d'][1])['d']
        high = max(vertices, key=lambda v: v['d'][1])['d']
        if low[1] == high[1]:
            witness = low
        else:
            t = -low[1] / (high[1] - low[1])
            assert 0 <= t <= 1
            witness = tuple((1 - t) * x + t * y for x, y in zip(low, high))
        assert witness[1] == 0
        assert all(lo <= dot(row, witness) <= hi
                   for row, (lo, hi) in zip(rows, residual_bounds))
    return {'q_bounds': residual_bounds, 'vertices': vertices,
            'x_interval': intervals[0], 'y_interval': intervals[1],
            'zero_horizontal_vector_feasible': origin_feasible,
            'zero_north_component_feasible': north_zero,
            'zero_north_witness': witness}


def projection(center, right, forward, point):
    relative = tuple(p - c for p, c in zip(point, center))
    depth = dot(forward, relative)
    if depth <= 0:
        raise ValueError('point not in front of camera')
    return depth, dot(right, relative) / depth, relative[2] / depth


def serialize(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: serialize(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [serialize(v) for v in value]
    return value


def calculate():
    fixed_normals = ((F(3, 5), F(4, 5)), (F(4, 5), F(3, 5)),
                     (F(12, 13), F(5, 13)), (F(99, 101), F(20, 101)),
                     (F(9999, 10001), F(200, 10001)))
    fixtures = [((normal, (F(1), F(0))), (F(0), F(2)),
                 (F(1, 5), F(1, 5))) for normal in fixed_normals]
    fixtures.append((((F(3, 5), F(4, 5)), (F(-4, 5), F(3, 5))),
                     (F(2), F(-3)), (F(1, 5), F(1, 10))))
    results = []
    zero_width_checks = []
    for index, (normals, truth, error) in enumerate(fixtures, 1):
        assert all(dot(row, row) == 1 for row in normals)
        q = tuple(dot(row, truth) for row in normals)
        recovered = solve(normals, q)
        assert recovered == truth
        result = corners(normals, q, error)
        assert result['x_interval'][0] <= truth[0] <= result['x_interval'][1]
        assert result['y_interval'][0] <= truth[1] <= result['y_interval'][1]
        results.append({'case': index, 'normals': normals, 'truth': truth,
                        'errors': error, 'q_center': q, 'center_recovered': recovered,
                        **result})
        zero = corners(normals, q, (F(0), F(0)))
        assert all(v['d'] == truth for v in zero['vertices'])
        assert zero['x_interval'] == (truth[0], truth[0])
        assert zero['y_interval'] == (truth[1], truth[1])
        zero_width_checks.append({'case': index, 'recovered': truth, 'passed': True})
    singular_rejected = False
    try:
        solve(((F(1), F(0)), (F(1), F(0))), (F(0), F(0)))
    except ValueError:
        singular_rejected = True
    assert singular_rejected
    negative_error_rejected = False
    try:
        normals, truth, _ = fixtures[0]
        q = tuple(dot(row, truth) for row in normals)
        corners(normals, q, (F(-1, 5), F(1, 5)))
    except ValueError:
        negative_error_rejected = True
    assert negative_error_rejected

    cameras = (
        {'id': 'C1', 'center': (F(-4), F(3), F(1)),
         'right': (F(3, 5), F(4, 5), F(0)),
         'forward': (F(4, 5), F(-3, 5), F(0))},
        {'id': 'C2', 'center': (F(0), F(8), F(2)),
         'right': (F(1), F(0), F(0)),
         'forward': (F(0), F(-1), F(0))})
    for camera in cameras:
        assert dot(camera['right'], camera['right']) == 1
        assert dot(camera['forward'], camera['forward']) == 1
        assert dot(camera['right'], camera['forward']) == 0
        assert dot(camera['right'], camera['center']) == 0
    projected = []
    for x, y in ((F(0), F(0)), (F(0), F(2)), (F(1), F(-1))):
        per_camera = {camera['id']: [] for camera in cameras}
        for z in (F(0), F(2), F(5)):
            point = (x, y, z)
            recovered_residuals = []
            for camera in cameras:
                depth, u, v = projection(camera['center'], camera['right'],
                                          camera['forward'], point)
                expected_q = dot(camera['right'][:2], (x, y))
                recovered_q = u * depth
                assert recovered_q == expected_q
                if x == 0 and y == 0:
                    assert u == 0
                per_camera[camera['id']].append((depth, u))
                recovered_residuals.append(recovered_q)
                projected.append({'camera': camera['id'], 'point': point,
                                  'depth': depth, 'image_horizontal': u,
                                  'image_vertical': v, 'plane_distance': expected_q,
                                  'recovered_plane_distance': recovered_q})
            assert solve(tuple(camera['right'][:2] for camera in cameras),
                         tuple(recovered_residuals)) == (x, y)
        assert all(len(set(values)) == 1 for values in per_camera.values())
    assert len(results) == 6 and len(projected) == 18
    return {'inverse_cases': results, 'cameras': cameras,
            'pinhole_projections': projected,
            'controls': {'singular_rejected': singular_rejected,
                         'negative_error_rejected': negative_error_rejected,
                         'zero_width_same_fixtures': zero_width_checks,
                         'horizontal_invariance_groups_passed': 6,
                         'original_edge_zero_projections_passed': 6,
                         'plane_distance_recoveries_passed': 18,
                         'paired_inverse_recoveries_passed': 9}}


def main():
    if OUTPUT.exists():
        raise FileExistsError('Refusing to overwrite frozen independent oracle')
    paths = (PROTOCOL, Path(__file__).resolve())
    before = {p.name: pin(p) for p in paths}
    result = calculate()
    after = {p.name: pin(p) for p in paths}
    assert before == after
    receipt = {'scope': 'synthetic algebra only; no historical calibration or cause',
               'method': 'exact Gauss-Jordan inversion at four residual-box vertices',
               'python': sys.version, 'input_pins_before': before,
               'input_pins_after': after, 'results': serialize(result)}
    with OUTPUT.open('x') as handle:
        json.dump(receipt, handle, indent=2, sort_keys=True)
        handle.write('\n')
    print(json.dumps({'inverse_cases': 6, 'vertices': 24,
                      'pinhole_projections': 18, 'controls_passed': True,
                      'output_sha256': pin(OUTPUT)['sha256']}))


if __name__ == '__main__':
    main()
