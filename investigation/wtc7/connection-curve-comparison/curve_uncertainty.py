"""Exact synthetic local envelopes under a named, shared calibration box.

No historical inputs, inferred allowances, uncertain knots, integral-error
estimator, probability model or acceptance decision. Outputs are conditional
uniform hulls over the entire query, not a separate band at each x.
"""
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import itertools
from pathlib import Path
import sys
import types


CORE_SHA256 = '7b5a1a3dc4cd822d0e948bdcb6ec5d2793a23bad0744f56dcfcc47980a1300e1'
_core_path = Path(__file__).resolve().with_name('curve_math.py')
_core_bytes = _core_path.read_bytes()
if hashlib.sha256(_core_bytes).hexdigest() != CORE_SHA256:
    raise ValueError('frozen curve_math source pin mismatch')
if 'curve_math' in sys.modules:
    _core = sys.modules['curve_math']
    if Path(_core.__file__).resolve() != _core_path:
        raise ValueError('curve_math was imported from another path')
else:
    # Execute precisely the checked bytes, without a source/bytecode-cache race.
    # Register under the existing name so all users share SupportedBranch identity.
    _core = types.ModuleType('curve_math')
    _core.__file__ = str(_core_path)
    sys.modules['curve_math'] = _core
    exec(compile(_core_bytes, str(_core_path), 'exec'), _core.__dict__)

SupportedBranch = _core.SupportedBranch
SUPPORT_TAG = _core.SUPPORT_TAG


def _interval(value, *, positive=False):
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        raise ValueError('explicit closed (low, high) interval required')
    low, high = map(_core._q, value)
    if low > high or (positive and low <= 0):
        raise ValueError('ordered interval required; scales must be strictly positive')
    return low, high


def _radius(value):
    value = _core._q(value)
    if value < 0:
        raise ValueError('radius must be nonnegative')
    return value


def _curve(value):
    if value is None:
        return None
    branches = _core._branches(value)
    # Revalidate fields too; a frozen dataclass is not a security boundary.
    for b in branches:
        SupportedBranch(b.name, b.support_tag, b.points)
    return branches


@dataclass(frozen=True)
class SharedAxis:
    calibration_id: str
    x_scale: tuple = (1, 1)
    x_offset: tuple = (0, 0)
    y_scale: tuple = (1, 1)
    y_offset: tuple = (0, 0)

    def __post_init__(self):
        if type(self.calibration_id) is not str or not self.calibration_id.strip():
            raise ValueError('named shared calibration required')
        for field in ('x_scale', 'x_offset', 'y_scale', 'y_offset'):
            object.__setattr__(self, field, _interval(getattr(self, field), positive=field.endswith('scale')))


def _axis_record(axis):
    if type(axis) is not SharedAxis:
        raise ValueError('explicit SharedAxis object required')
    validated = SharedAxis(axis.calibration_id, axis.x_scale, axis.x_offset, axis.y_scale, axis.y_offset)
    return {field: getattr(validated, field) for field in
            ('calibration_id', 'x_scale', 'x_offset', 'y_scale', 'y_offset')}


def _supported_branch(curve, query):
    if curve is None:
        return None
    for branch in curve:
        if branch.points[0][0] <= query[0] <= query[1] <= branch.points[-1][0]:
            return branch
    return None


def local_envelope(curve, query, *, y_radius=0):
    """Exact extrema of one fully supported closed query, expanded in y."""
    query, y_radius, curve = _interval(query), _radius(y_radius), _curve(curve)
    result = {'query': query, 'y_radius': y_radius, 'bounds': None,
              'status': 'unresolved', 'reason': None, 'branch_name': None,
              'support': None if curve is None else tuple((b.points[0][0], b.points[-1][0]) for b in curve),
              'branch_names': None if curve is None else tuple(b.name for b in curve),
              'evaluated_x': ()}
    if curve is None:
        result['reason'] = 'unknown-identity-or-support'
        return result
    branch = _supported_branch(curve, query)
    if branch is None:
        result['reason'] = 'query-not-fully-supported'
        return result
    xs = sorted({query[0], query[1]} | {x for x, _ in branch.points if query[0] < x < query[1]})
    values = [_core._value(branch, x) for x in xs]
    result.update(bounds=(min(values)-y_radius, max(values)+y_radius),
                  status='resolved', branch_name=branch.name, evaluated_x=tuple(xs))
    return result


def _product(a, b):
    values = [x*y for x in a for y in b]
    return min(values), max(values)


def _vertices(u, v, distance):
    """Vertices of rectangle intersected with |u-v|<=distance, including degeneracy.

    Enumerating intersections of all nonparallel boundary pairs avoids losing
    a line/point polygon to a positive-area clipping convention. Bounded feasible
    polyhedra here always have a vertex; every vertex satisfies all halfplanes.
    """
    constraints = ((-1, 0, -u[0]), (1, 0, u[1]), (0, -1, -v[0]), (0, 1, v[1]),
                   (1, -1, distance), (-1, 1, distance))
    points = set()
    for (a, b, c), (d, e, f) in itertools.combinations(constraints, 2):
        determinant = a*e-b*d
        if determinant == 0:
            continue
        x = Fraction(c*e-b*f, determinant)
        y = Fraction(a*f-c*d, determinant)
        if all(h*x+k*y <= bound for h, k, bound in constraints):
            points.add((x, y))
    return tuple(sorted(points))


def compare_uncertain(reference, candidate, query, *, axis,
                      reference_x_radius=0, candidate_x_radius=0,
                      reference_y_radius=0, candidate_y_radius=0):
    """Uniform candidate-minus-reference hull; errors are sets, not probabilities.

    Shared A/B affect both curves through one t, G scales their difference,
    and truly shared H cancels. Local radii remain separate even for identical
    centerlines. A missing curve/support never substitutes a numerical zero.
    """
    # Validate EVERY supplied input before returning scientific missingness.
    query = _interval(query)
    calibration = _axis_record(axis)
    rr, rs = _radius(reference_x_radius), _radius(candidate_x_radius)
    sr, ss = _radius(reference_y_radius), _radius(candidate_y_radius)
    reference, candidate = _curve(reference), _curve(candidate)
    transformed = _product(calibration['x_scale'], query)
    t = (transformed[0]+calibration['x_offset'][0], transformed[1]+calibration['x_offset'][1])
    demanded_r, demanded_s = (t[0]-rr, t[1]+rr), (t[0]-rs, t[1]+rs)
    checks = {'reference': local_envelope(reference, demanded_r),
              'candidate': local_envelope(candidate, demanded_s)}
    failures = tuple({'curve': name, 'query': check['query'], 'reason': check['reason']}
                     for name, check in checks.items() if check['status'] != 'resolved')
    result = {'query': query, 'axis': calibration, 'reachable_t': t,
              'reference_x_radius': rr, 'candidate_x_radius': rs,
              'reference_y_radius': sr, 'candidate_y_radius': ss,
              'reference_demand': demanded_r, 'candidate_demand': demanded_s,
              'support_checks': checks, 'failures': failures,
              'status': 'unresolved', 'bounds': None, 'sign': None,
              'centerline_bounds': None, 'ordinate_expanded_bounds': None,
              'centerline_extremizers': None, 'evaluated_vertices': 0,
              'difference': 'candidate-minus-reference', 'shared_y_offset_cancels': True,
              'scope': 'uniform-hull-over-query-and-rectangular-parameter-box; not an integral bound'}
    if failures:
        return result
    ref = _supported_branch(reference, demanded_r)
    cand = _supported_branch(candidate, demanded_s)
    extrema = []
    for (r0, _), (r1, _) in zip(ref.points, ref.points[1:]):
        u = (max(r0, demanded_r[0]), min(r1, demanded_r[1]))
        if u[0] > u[1]:
            continue
        for (s0, _), (s1, _) in zip(cand.points, cand.points[1:]):
            v = (max(s0, demanded_s[0]), min(s1, demanded_s[1]))
            if v[0] > v[1]:
                continue
            for up, vp in _vertices(u, v, rr+rs):
                witness_t = max(t[0], up-rr, vp-rs)
                if witness_t > min(t[1], up+rr, vp+rs):
                    raise ArithmeticError('vertex lacks required shared-t witness')
                value = _core._value(cand, vp)-_core._value(ref, up)
                extrema.append((value, up, vp, witness_t))
    if not extrema:
        raise ArithmeticError('fully supported shared-t domain unexpectedly empty')
    low, high = min(extrema), max(extrema)
    centerline = (low[0], high[0])
    expanded = (low[0]-sr-ss, high[0]+sr+ss)
    bounds = _product(calibration['y_scale'], expanded)
    result.update(status='resolved', bounds=bounds,
                  sign='positive' if bounds[0] > 0 else ('negative' if bounds[1] < 0 else 'unresolved'),
                  centerline_bounds=centerline, ordinate_expanded_bounds=expanded,
                  centerline_extremizers={label: {'u': value[1], 'v': value[2], 't': value[3]}
                                         for label, value in (('minimum', low), ('maximum', high))},
                  evaluated_vertices=len(extrema))
    return result
