"""Pure exact arithmetic for the prospective conditional graphical estimand.

Inputs are declared envelopes on open page-x cells, NOT recovered curves.
Interpretation for original curves requires Hidentity, Hsupport and Hink0;
this module neither tests those assumptions nor records human acceptance.
No I/O, historical data, interpolation, gap filling or cross-panel equality.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
from collections.abc import Mapping


def _q(value):
    if type(value) not in (int, Q):
        raise ValueError("coordinates must be exact int or Fraction, never bool/float")
    return Q(value)


def _name(value):
    if type(value) is not str or not value.strip():
        raise ValueError("a nonempty explicit identity is required")


@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q

    def __post_init__(self):
        object.__setattr__(self, "lo", _q(self.lo))
        object.__setattr__(self, "hi", _q(self.hi))
        if self.lo > self.hi:
            raise ValueError("reversed interval")


def _interval(value):
    if type(value) is not Interval:
        raise ValueError("explicit Interval required")
    return Interval(value.lo, value.hi)


@dataclass(frozen=True)
class Cell:
    """An open x interior and closed rendered-y enclosures for both models."""
    x: Interval
    spring_y: Interval
    shell_y: Interval

    def __post_init__(self):
        for name in ("x", "spring_y", "shell_y"):
            _interval(getattr(self, name))
        if self.x.lo == self.x.hi:
            raise ValueError("zero-length cell")


@dataclass(frozen=True)
class Scenario:
    pair_id: str
    panel: str
    frame: str
    cells: tuple

    def __post_init__(self):
        _name(self.pair_id)
        _name(self.frame)
        if self.panel not in ("force", "energy") or type(self.panel) is not str:
            raise ValueError("panel must be force (N) or energy (N-m)")
        if type(self.cells) is not tuple:
            raise ValueError("cells must be an explicit ordered tuple")
        previous = None
        for cell in self.cells:
            if type(cell) is not Cell:
                raise ValueError("Cell required")
            Cell(cell.x, cell.spring_y, cell.shell_y)
            if previous is not None and cell.x.lo < previous:
                raise ValueError("overlapping or backtracking cells; no automatic sorting")
            previous = cell.x.hi


@dataclass(frozen=True)
class AxisBox:
    """One rectangular L/R/T/B uncertainty box shared by every cell and model.

    All vertices must have positive width and height. A correlated non-box
    admissible set needs a different declared method; this API cannot encode it.
    """
    frame: str
    left: Interval
    right: Interval
    top: Interval
    bottom: Interval

    def __post_init__(self):
        _name(self.frame)
        for name in ("left", "right", "top", "bottom"):
            _interval(getattr(self, name))
        if self.left.hi >= self.right.lo or self.top.hi >= self.bottom.lo:
            raise ValueError("every axis state must have strictly positive spans")

    def states(self):
        return tuple(product(*(tuple(sorted({v.lo, v.hi})) for v in
                               (self.left, self.right, self.top, self.bottom))))


def _scenario(value):
    if type(value) is not Scenario:
        raise ValueError("Scenario required; unknown identity is not an envelope")
    return Scenario(value.pair_id, value.panel, value.frame, value.cells)


def _axis(value):
    if type(value) is not AxisBox:
        raise ValueError("AxisBox required")
    return AxisBox(value.frame, value.left, value.right, value.top, value.bottom)


def difference_page(cell):
    """Shell minus spring BEFORE positive scale; rendered y points downward.

    The shared physical-y offset cancels algebraically before any hull.
    """
    if type(cell) is not Cell:
        raise ValueError("Cell required")
    Cell(cell.x, cell.spring_y, cell.shell_y)
    return Interval(cell.spring_y.lo - cell.shell_y.hi,
                    cell.spring_y.hi - cell.shell_y.lo)


def _absolute(bounds):
    lower = (Q(0) if bounds.lo <= 0 <= bounds.hi
             else min(abs(bounds.lo), abs(bounds.hi)))
    return Interval(lower, max(abs(bounds.lo), abs(bounds.hi)))


def compare_envelopes(scenario, axis):
    """Conservative exact integral/mean hulls over this scenario's finite cells.

    Aggregate in page units, then evaluate each COMPLETE shared axis state.
    Fixed spans are 8/5 m and 1,000,000 N or 800,000 N-m. Endpoints and
    maxima are unspecified. Means use the same domain length; kx cancels.
    Hull endpoints need not be jointly attainable. No confidence level exists.
    """
    scenario, axis = _scenario(scenario), _axis(axis)
    if scenario.frame != axis.frame:
        raise ValueError("axis and cells use different coordinate frames")
    force = scenario.panel == "force"
    ymax = Q(1_000_000 if force else 800_000)
    unit = "N" if force else "N-m"
    units = {"integrals": {"signed": "N-m" if force else "N-m^2",
                           "absolute": "N-m" if force else "N-m^2",
                           "squared": "N^2-m" if force else "N^2-m^3"},
             "means": {"signed": unit, "absolute": unit,
                       "squared": "N^2" if force else "N^2-m^2"},
             "length": "m"}
    states = axis.states()
    length = sum((c.x.hi - c.x.lo for c in scenario.cells), Q(0))
    result = {"status": "unavailable-empty-domain", "pair_id": scenario.pair_id,
              "panel": scenario.panel, "frame": scenario.frame,
              "domain_page": tuple(c.x for c in scenario.cells),
              "page_length": length, "domain_length": Interval(0, 0),
              "integrals": None, "means": None, "units": units,
              "axis_vertices_evaluated": len(states),
              "estimand": "conditional-graphical-envelope; not original-curve bounds",
              "assumptions_unvalidated": ("Hidentity", "Hsupport", "Hink0"),
              "human_accepted": False}
    if not length:
        return result
    totals = {kind: [Q(0), Q(0)] for kind in ("signed", "absolute", "squared")}
    for cell in scenario.cells:
        signed = difference_page(cell)
        absolute = _absolute(signed)
        bounds = {"signed": signed, "absolute": absolute,
                  "squared": Interval(absolute.lo ** 2, absolute.hi ** 2)}
        width = cell.x.hi - cell.x.lo
        for kind, bound in bounds.items():
            totals[kind][0] += width * bound.lo
            totals[kind][1] += width * bound.hi
    samples = {group: {kind: [] for kind in totals} for group in ("integrals", "means")}
    lengths = []
    for left, right, top, bottom in states:
        kx, ky = Q(8, 5) / (right - left), ymax / (bottom - top)
        lengths.append(length * kx)
        for kind, (lo, hi) in totals.items():
            scale = ky ** (2 if kind == "squared" else 1)
            samples["integrals"][kind].extend((lo * kx * scale, hi * kx * scale))
            samples["means"][kind].extend((lo * scale / length, hi * scale / length))
    result.update(status="conditional-envelope-bounds",
                  domain_length=Interval(min(lengths), max(lengths)))
    for group, kinds in samples.items():
        result[group] = {kind: Interval(min(values), max(values))
                         for kind, values in kinds.items()}
    return result


def _alternatives(alternatives):
    if not isinstance(alternatives, Mapping) or not alternatives:
        raise ValueError("nonempty named alternatives required")
    present = []
    for name, scenario in alternatives.items():
        _name(name)
        if scenario is not None:
            present.append(_scenario(scenario))
    if len({(s.pair_id, s.panel, s.frame) for s in present}) > 1:
        raise ValueError("alternatives must name the same pair, units and page frame")
    return present


def require_same_domain(alternatives):
    """Require identical open comparison domains before comparing aggregates.

    Adjacent open cells retain their missing internal boundary. This strict
    check does not relabel domains differing by finite points as identical.
    Missing or empty alternatives are unavailable, never agreeing results.
    """
    present = _alternatives(alternatives)
    if len(present) != len(alternatives) or not all(s.cells for s in present):
        raise ValueError("missing or empty alternative")
    domains = {tuple(c.x for c in s.cells) for s in present}
    if len(domains) != 1:
        raise ValueError("changed comparison domain; different estimands")
    return next(iter(domains))


def reader_robust_sign(alternatives, page_x):
    """Strict sign at one common source position, conditional on all assumptions.

    Every named alternative must contain that position in an open cell.
    Positive calibration leaves the sign unchanged. No interval-wide claim
    or endpoint value follows from this point query.
    """
    _alternatives(alternatives)  # Validate all supplied data before missingness.
    page_x = _q(page_x)
    observations = {}
    for name, scenario in alternatives.items():
        state, bounds = "alternative-unavailable", None
        if scenario is not None:
            state = "outside-coverage"
            if any(page_x in (c.x.lo, c.x.hi) for c in scenario.cells):
                state = "boundary-unresolved"
            else:
                for cell in scenario.cells:
                    if cell.x.lo < page_x < cell.x.hi:
                        bounds = difference_page(cell)
                        state = ("positive" if bounds.lo > 0 else
                                 "negative" if bounds.hi < 0 else "zero-not-excluded")
                        break
        observations[name] = {"status": state, "difference_page": bounds}
    signs = {entry["status"] for entry in observations.values()}
    sign = next(iter(signs)) if len(signs) == 1 and signs <= {"positive", "negative"} else None
    return {"page_x": page_x, "sign": sign, "alternatives": observations,
            "status": "conditional-robust-sign" if sign else "unresolved",
            "human_accepted": False}
