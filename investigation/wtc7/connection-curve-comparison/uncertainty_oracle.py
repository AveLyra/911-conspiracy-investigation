"""Root's fixed analytical expectations, frozen before new producer-code reading.

No producer imports, optimization, graph reading, random sampling or historical
data. Fractions encode hand-derived examples of UNCERTAINTY-STAGE's model.
Shared method discussion and existing curve_math knowledge are disclosed.
"""
from fractions import Fraction as Q
import json


def branches(*paths):
    return tuple(tuple(tuple(point) for point in path) for path in paths)


def line(m, b, lo=-10, hi=10):
    return branches(((lo, m * lo + b), (hi, m * hi + b)))


def local(name, curve, query, expected, radius=0):
    return dict(name=name, kind="local", curve=curve, query=query,
                radius=radius, expected_bounds=expected)


def pair(name, ref, cand, query, expected, *, axis=None, radii=(0, 0, 0, 0)):
    return dict(name=name, kind="pair", reference=ref, candidate=cand,
                query=query, axis=axis or {}, radii=radii,
                expected_bounds=expected,
                expected_sign=(None if expected is None else
                               "positive" if expected[0] > 0 else
                               "negative" if expected[1] < 0 else "unresolved"))


def fixtures():
    tent = branches(((0, 0), (Q(49, 100), 0), (Q(1, 2), 7),
                     (Q(51, 100), 0), (1, 0)))
    gaps = branches(((0, 0), (1, 0)), ((2, 3), (3, 3)))
    triangle = branches(((0, 0), (1, 1), (2, 0)))
    # Local extrema: affine endpoints or all enclosed PL vertices, then +/-y.
    result = [
        local("flat_y_radius", line(0, 3, 0, 4), (1, 2), (Q(5, 2), Q(7, 2)), Q(1, 2)),
        local("signed_affine_endpoints", line(2, 1, -2, 2),
              (-Q(1, 2), Q(3, 2)), (-Q(1, 4), Q(17, 4)), Q(1, 4)),
        local("narrow_interior_peak", tent, (Q(1, 4), Q(3, 4)), (0, 7)),
        local("point_at_peak", tent, (Q(1, 2), Q(1, 2)), (7, 7)),
        local("support_edge_with_y", tent, (0, 0), (-1, 1), 1),
        local("crosses_gap", gaps, (Q(1, 2), Q(5, 2)), None),
        local("closed_support_contact", gaps, (1, 1), (0, 0)),
        local("gap_between_valid_endpoints", gaps, (1, 2), None),
        local("outside_tail", tent, (-1, 1), None),
        local("unknown_identity", None, (0, 1), None),
        local("negative_ordinates", line(1, -2, -2, 2), (-1, 0), (-3, -2)),
        local("full_closed_support", line(0, 3, 0, 4), (0, 4), (3, 3)),
    ]
    # Each pair is solvable by a stated affine expression or visible tent extrema.
    result.extend([
        pair("constant_positive", line(0, 3), line(0, 4), (0, 1), (1, 1)),
        pair("common_vertical_offset_cancels", line(0, 3), line(0, 4),
             (0, 1), (1, 1), axis={"y_offset": (-100, 100)}),
        # 1 +/- (1+2).
        pair("unequal_local_y", line(0, 3), line(0, 4), (0, 1),
             (-2, 4), radii=(0, 0, 1, 2)),
        # -3 times [1,2].
        pair("negative_shared_gain", line(0, 4), line(0, 1), (0, 1),
             (-6, -3), axis={"y_scale": (1, 2)}),
        pair("zero_contact_is_not_positive", line(0, 3), line(0, 4),
             (0, 1), (0, 2), radii=(0, 0, 1, 0)),
        # (t+1)-t = 1 for all common t, even with shared origin uncertainty.
        pair("equal_slopes_shared_horizontal", line(1, 0), line(1, 1),
             (1, 3), (1, 1), axis={"x_offset": (-2, 2)}),
        # 1+eS-eR with |eS|<=2, |eR|<=1.
        pair("equal_slopes_independent_local", line(1, 0), line(1, 1),
             (0, 1), (-2, 4), radii=(1, 2, 0, 0)),
        # t+1+3eS-2eR, t in [1,2], errors contribute +/-2.
        pair("different_slopes_unequal_radii", line(2, 0), line(3, 1),
             (1, 2), (0, 5), radii=(Q(1, 4), Q(1, 2), 0, 0)),
        # [1,2]*[-2,-1]+[1,2] = [-3,1].
        pair("signed_query_scale_offset", line(0, 0), line(1, 0),
             (-2, -1), (-3, 1), axis={"x_scale": (1, 2), "x_offset": (1, 2)}),
        # 2t-t=t, t in [0,3].
        pair("horizontal_error_different_slopes", line(1, 0), line(2, 0),
             (1, 2), (0, 3), axis={"x_offset": (-1, 1)}),
        pair("pair_narrow_interior_peak", line(0, 0), tent,
             (Q(1, 4), Q(3, 4)), (0, 7)),
        pair("point_query_local_radius_spans_peak", line(0, 0), tent,
             (Q(1, 2), Q(1, 2)), (0, 7), radii=(0, Q(1, 100), 0, 0)),
        pair("identical_tent_common_location", tent, tent, (0, 1), (0, 0)),
        # Unit-Lipschitz triangle: difference <= |u-v|<=1/5; attained at .8,1.
        pair("triangle_local_dependence", triangle, triangle,
             (Q(9, 10), Q(11, 10)), (-Q(1, 5), Q(1, 5)),
             radii=(Q(1, 10), Q(1, 10), 0, 0)),
        # (-2 +/- 3/4) * [1/2,3/2].
        pair("negative_gain_and_local_y", line(0, 3), line(0, 1),
             (0, 1), (-Q(33, 8), -Q(5, 8)),
             axis={"y_scale": (Q(1, 2), Q(3, 2))},
             radii=(0, 0, Q(1, 4), Q(1, 2))),
        pair("degenerate_joint_support_point", line(1, 0, 0, 1),
             line(2, 0, 1, 2), (1, 1), (1, 1)),
        pair("pair_crosses_gap", gaps, line(0, 0), (0, 3), None),
        pair("radius_reaches_missing_tail", line(0, 0, 0, 1),
             line(0, 1, 0, 2), (Q(1, 2), Q(3, 4)), None,
             radii=(Q(1, 2), 0, 0, 0)),
        pair("candidate_identity_unknown", line(0, 0), None, (0, 1), None),
        # t - 2(t+eR) = -t-2eR, t in [0,1].
        pair("one_zero_horizontal_radius", line(2, 0), line(1, 0),
             (0, 1), (-3, 2), radii=(1, 0, 0, 0)),
    ])
    assert len(result) == 32
    assert len({r["name"] for r in result}) == len(result)
    return result


def jsonable(value):
    if type(value) is Q:
        return str(value)
    if type(value) is dict:
        return {k: jsonable(v) for k, v in value.items()}
    if type(value) in (tuple, list):
        return [jsonable(v) for v in value]
    return value


if __name__ == "__main__":
    print(json.dumps(jsonable(fixtures()), sort_keys=True, indent=2))
