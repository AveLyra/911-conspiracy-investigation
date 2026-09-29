"""Exact, synthetic two-plane sensitivity checks; no historical measurements."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def dot(a, b):
    return sum((x*y for x, y in zip(a, b, strict=True)), F(0))


def inverse(normals):
    (a, b), (c, d) = normals
    det = a*d-b*c
    if det == 0:
        raise ValueError('Singular normals do not define a unique inverse')
    return ((d/det, -b/det), (-c/det, a/det))


def solve(normals, q, errors):
    if any(e < 0 for e in errors):
        raise ValueError('Residual error bounds must be nonnegative')
    inv = inverse(normals)
    center = tuple(dot(row, q) for row in inv)
    radius = tuple(dot(tuple(abs(x) for x in row), errors) for row in inv)
    intervals = tuple((c-r, c+r) for c, r in zip(center, radius, strict=True))
    return {
        'center': center, 'radius': radius, 'intervals': intervals,
        'zero_vector_feasible': all(abs(v) <= e for v, e in zip(q, errors, strict=True)),
        'zero_north_feasible': intervals[1][0] <= 0 <= intervals[1][1],
    }


def project(camera, right, forward, point):
    delta = tuple(p-c for p, c in zip(point, camera, strict=True))
    depth = dot(forward, delta)
    if depth <= 0:
        raise ValueError('Point is not in front of this ideal camera')
    return (dot(right, delta)/depth, delta[2]/depth), depth


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def calculate():
    directions = ((F(3, 5), F(4, 5)), (F(4, 5), F(3, 5)),
                  (F(12, 13), F(5, 13)), (F(99, 101), F(20, 101)),
                  (F(9999, 10001), F(200, 10001)))
    cases = []
    for i, n in enumerate(directions):
        assert dot(n, n) == 1
        cases.append((f'conditioning_{i+1}', (n, (F(1), F(0))),
                      (F(0), F(2)), (F(1, 5), F(1, 5))))
    cases.append(('general', ((F(3, 5), F(4, 5)), (F(-4, 5), F(3, 5))),
                  (F(2), F(-3)), (F(1, 5), F(1, 10))))
    results = []
    for name, normals, truth, errors in cases:
        q = tuple(dot(row, truth) for row in normals)
        answer = solve(normals, q, errors)
        assert answer['center'] == truth
        assert tuple(dot(n, answer['center']) for n in normals) == q
        exact = solve(normals, q, (F(0), F(0)))
        assert exact['intervals'] == tuple((v, v) for v in truth)
        results.append({'name': name, 'normals': normals, 'truth': truth,
                        'q': q, 'errors': errors, **answer})

    controls = {'all_six_exact_forward_inverse': True, 'all_six_zero_width': True}
    try:
        inverse(((F(1), F(0)), (F(1), F(0))))
    except ValueError:
        controls['singular_rejected'] = True
    else:
        raise AssertionError('Singular matrix admitted')
    try:
        solve(cases[0][1], (F(0), F(0)), (F(-1), F(0)))
    except ValueError:
        controls['negative_error_rejected'] = True
    else:
        raise AssertionError('Negative error admitted')

    cameras = (((F(-4), F(3), F(1)), (F(3, 5), F(4, 5), F(0)),
                (F(4, 5), F(-3, 5), F(0))),
               ((F(0), F(8), F(2)), (F(1), F(0), F(0)),
                (F(0), F(-1), F(0))))
    projections = []
    for j, (camera, right, forward) in enumerate(cameras, start=1):
        assert dot(right, right) == dot(forward, forward) == 1
        assert dot(right, forward) == 0
        for xy in ((F(0), F(0)), (F(0), F(2)), (F(1), F(-1))):
            horizontal_coordinates = []
            for z in (F(0), F(2), F(5)):
                point = (*xy, z)
                image, depth = project(camera, right, forward, point)
                signed_plane_distance = dot(right[:2], xy)
                assert image[0]*depth == signed_plane_distance
                if xy == (0, 0):
                    assert image[0] == 0
                horizontal_coordinates.append(image[0])
                projections.append({'camera': j, 'point': point, 'image': image,
                                    'depth': depth, 'q': signed_plane_distance})
            assert len(set(horizontal_coordinates)) == 1
    controls['all_eighteen_pinhole_identities'] = True
    controls['six_vertical_tracks_keep_image_horizontal_coordinate'] = True
    return {'scope': 'synthetic_only_not_wtc7_measurement',
            'length_unit': 'arbitrary synthetic u', 'cases': results,
            'projections': projections, 'controls': controls}


def main():
    output = HERE/'math01.json'
    if output.exists():
        raise FileExistsError('Refusing existing synthetic result')
    inputs = (Path(__file__), HERE/'MATH-PROTOCOL.md', Path(sys.executable))
    before = {str(p): identity(p) for p in inputs}
    result = calculate()
    after = {str(p): identity(p) for p in inputs}
    assert before == after
    result.update({'before': before, 'after': after, 'inputs_unchanged': True,
                   'python': sys.version})
    with output.open('x') as f:
        json.dump(encode(result), f, indent=2, sort_keys=True)
        f.write('\n')
    print(json.dumps({'cases': len(result['cases']),
                      'projections': len(result['projections']),
                      'controls': result['controls']}))


if __name__ == '__main__':
    main()
