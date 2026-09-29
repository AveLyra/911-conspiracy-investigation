"""Exact arithmetic for source-independent, explicitly supported toy curves.

No PDF/image parser, source acquisition, historical data, statistical error
model, uncertainty estimator or physical acceptance decision is implemented.
Fractions and integers only: floats (even finite ones), strings and booleans
are rejected rather than silently rounded or interpreted as measurements.
"""

from dataclasses import dataclass
from fractions import Fraction


SUPPORT_TAG = "explicit-supported-monotone"
ORDER_TAG = "explicit-path-order"
PURE_DISSIPATION_IDENTITY = "same-conjugate-path-units-baseline-pure-dissipation"


def _q(value):
    if type(value) not in (int, Fraction):
        raise ValueError("exact finite int/Fraction required; no bool/float/string")
    return Fraction(value)


def _points(points):
    if not isinstance(points, (tuple, list)) or len(points) < 2:
        raise ValueError("at least two explicit points required")
    result = []
    for point in points:
        if not isinstance(point, (tuple, list)) or len(point) != 2:
            raise ValueError("each point must be an explicit (x, y) pair")
        result.append((_q(point[0]), _q(point[1])))
    return tuple(result)


@dataclass(frozen=True)
class SupportedBranch:
    """A declared closed support interval; declaration is not authentication."""

    name: str
    support_tag: str
    points: tuple

    def __post_init__(self):
        if type(self.name) is not str or not self.name.strip():
            raise ValueError("branch name required")
        if type(self.support_tag) is not str or self.support_tag != SUPPORT_TAG:
            raise ValueError("unknown/ambiguous support")
        points = _points(self.points)
        if any(b[0] <= a[0] for a, b in zip(points, points[1:])):
            raise ValueError("function branch must have strictly increasing x")
        object.__setattr__(self, "points", points)


def _branches(branches):
    if not isinstance(branches, (tuple, list)) or not branches:
        raise ValueError("one or more explicitly supported branches required")
    if any(type(branch) is not SupportedBranch for branch in branches):
        raise ValueError("only SupportedBranch objects accepted")
    if len({branch.name for branch in branches}) != len(branches):
        raise ValueError("branch names must be unique within each curve")
    for left, right in zip(branches, branches[1:]):
        if right.points[0][0] <= left.points[-1][0]:
            raise ValueError("branches must be ordered with strictly disjoint support")
    return tuple(branches)


def _axis(axis):
    if not isinstance(axis, (tuple, list)) or len(axis) != 2:
        raise ValueError("axis must be an explicit (minimum, maximum)")
    lo, hi = map(_q, axis)
    if hi <= lo:
        raise ValueError("axis range must be strictly positive")
    return lo, hi


def _value(branch, x):
    for (x0, y0), (x1, y1) in zip(branch.points, branch.points[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    raise ValueError("extrapolation outside declared support is forbidden")


def _merge_locations(locations):
    merged = []
    for lo, hi in sorted(set(locations)):
        if merged and lo <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(hi, merged[-1][1]))
        else:
            merged.append((lo, hi))
    return tuple(merged)


def _peak(pieces, index, absolute=False):
    # piece = (x0, x1, ref0, ref1, candidate0, candidate1).
    def endpoints(piece):
        if index == "difference":
            return piece[4] - piece[2], piece[5] - piece[3]
        return piece[index], piece[index + 1]

    transform = abs if absolute else lambda value: value
    maximum = max(transform(y) for piece in pieces for y in endpoints(piece))
    locations = []
    for piece in pieces:
        a, b = endpoints(piece)
        if a == b and transform(a) == maximum:
            locations.append((piece[0], piece[1]))
        else:
            if transform(a) == maximum:
                locations.append((piece[0], piece[0]))
            if transform(b) == maximum:
                locations.append((piece[1], piece[1]))
    return {"value": maximum, "locations": _merge_locations(locations)}


def _own_peak(branches):
    pieces = tuple((x0, x1, y0, y1, y0, y1)
                   for branch in branches
                   for (x0, y0), (x1, y1) in zip(branch.points, branch.points[1:]))
    return _peak(pieces, 2)


def compare_curves(reference, candidate, *, x_axis, y_axis):
    """Compare exact toy piecewise-linear functions on joint support only.

    Differences are candidate minus reference. Normalization uses the declared
    positive y-axis range, never the ordinate/reference force. `mean_squared`
    and its normalized form are RMS squared; no inexact square root is taken.
    Areas across gaps are partial-domain sums, not a continuous work history.
    """
    reference, candidate = _branches(reference), _branches(candidate)
    xlo, xhi = _axis(x_axis)
    ylo, yhi = _axis(y_axis)
    for branch in reference + candidate:
        for x, y in branch.points:
            if not (xlo <= x <= xhi and ylo <= y <= yhi):
                raise ValueError("points outside declared axes are not unclipped support")

    intervals, pieces, crossings = [], [], []
    for ref in reference:
        for cand in candidate:
            lo = max(ref.points[0][0], cand.points[0][0])
            hi = min(ref.points[-1][0], cand.points[-1][0])
            if hi <= lo:
                continue
            intervals.append((lo, hi))
            knots = sorted({lo, hi} | {
                x for branch in (ref, cand) for x, _ in branch.points if lo < x < hi
            })
            for x0, x1 in zip(knots, knots[1:]):
                d0 = _value(cand, x0) - _value(ref, x0)
                d1 = _value(cand, x1) - _value(ref, x1)
                cuts = [x0, x1]
                if d0 * d1 < 0:
                    cross = x0 - d0 * (x1 - x0) / (d1 - d0)
                    crossings.append(cross)
                    cuts.insert(1, cross)
                for a, b in zip(cuts, cuts[1:]):
                    pieces.append((a, b, _value(ref, a), _value(ref, b),
                                   _value(cand, a), _value(cand, b)))
    if not pieces:
        raise ValueError("no positive-length common supported domain")
    pieces.sort(key=lambda piece: piece[0])
    intervals.sort()
    length = sum((hi - lo for lo, hi in intervals), Fraction(0))
    nominal_lo = max(reference[0].points[0][0], candidate[0].points[0][0])
    nominal_hi = min(reference[-1].points[-1][0], candidate[-1].points[-1][0])
    nominal_length = nominal_hi - nominal_lo
    # Every valid interval is contained in this envelope; no gap is filled.
    if not (0 < length <= nominal_length):
        raise ValueError("invalid common-domain accounting")

    ref_area = cand_area = signed = absolute = squared = Fraction(0)
    for x0, x1, r0, r1, c0, c1 in pieces:
        h, d0, d1 = x1 - x0, c0 - r0, c1 - r1
        if d0 * d1 < 0:
            raise ArithmeticError("difference crossing was not split")
        ref_area += h * (r0 + r1) / 2
        cand_area += h * (c0 + c1) / 2
        signed += h * (d0 + d1) / 2
        absolute += h * (abs(d0) + abs(d1)) / 2
        squared += h * (d0 * d0 + d0 * d1 + d1 * d1) / 3
    scale = yhi - ylo
    max_difference = _peak(pieces, "difference", absolute=True)
    return {
        "difference_sign": "candidate-minus-reference",
        "area_scope": "joint-supported-domain-only",
        "x_axis": (xlo, xhi), "y_axis": (ylo, yhi), "y_scale": scale,
        "reference_support": tuple((b.points[0][0], b.points[-1][0]) for b in reference),
        "candidate_support": tuple((b.points[0][0], b.points[-1][0]) for b in candidate),
        "common_intervals": tuple(intervals), "common_length": length,
        "nominal_overlap": (nominal_lo, nominal_hi),
        "nominal_overlap_length": nominal_length,
        "coverage_nominal": length / nominal_length,
        "coverage_axis": length / (xhi - xlo),
        "pieces": tuple(pieces), "interior_zero_crossings": tuple(sorted(set(crossings))),
        "reference_area": ref_area, "candidate_area": cand_area,
        "signed_difference_area": signed, "absolute_difference_area": absolute,
        "squared_difference_integral": squared,
        "signed_mean": signed / length, "mean_absolute": absolute / length,
        "mean_squared": squared / length,
        "normalized_signed_mean": signed / (length * scale),
        "normalized_mean_absolute": absolute / (length * scale),
        "normalized_mean_squared": squared / (length * scale * scale),
        "reference_peak_own": _own_peak(reference),
        "candidate_peak_own": _own_peak(candidate),
        "reference_peak_common": _peak(pieces, 2),
        "candidate_peak_common": _peak(pieces, 4),
        "reference_terminal_supported": reference[-1].points[-1],
        "candidate_terminal_supported": candidate[-1].points[-1],
        "common_terminal_supported": (pieces[-1][1], pieces[-1][3], pieces[-1][5]),
        "maximum_absolute_difference": max_difference,
        "normalized_maximum_absolute_difference": max_difference["value"] / scale,
    }


def ordered_area(points, *, order_tag):
    """Signed geometric line integral, conditional on a declared path order.

    Backtracking is retained. A purely vertical path has zero area; it is not a
    positive-length function domain and cannot be used by compare_curves.
    Nothing here verifies that drawing order was physical loading order.
    """
    if type(order_tag) is not str or order_tag != ORDER_TAG:
        raise ValueError("path order is unknown")
    points = _points(points)
    return sum(((y0 + y1) * (x1 - x0) / 2
                for (x0, y0), (x1, y1) in zip(points, points[1:])), Fraction(0))


def mn_m_to_nm(area):
    """Unit conversion only, not identification of work with dissipation."""
    return _q(area) * 1_000_000


def conditional_pure_dissipation_residual(work_nm, dissipated_nm, *, identity):
    """Toy diagnostic E-W under an explicitly stipulated identity only.

    This token does not verify actual source definitions, human review, energy
    balance or physical validity. Unknown/alternative identities are refused.
    """
    if type(identity) is not str or identity != PURE_DISSIPATION_IDENTITY:
        raise ValueError("energy identity is unknown or not pure dissipation")
    return _q(dissipated_nm) - _q(work_nm)
