# Local curve-uncertainty adapter: prospective synthetic contract

2026-09-27. Research only. Extends the missing local-envelope calculation in
NUMERICAL-PROTOCOL.md without changing its seven-pair historical scope or
HUMAN-REVIEW-GATE.md. The preceding user-response turn rechecked an existing
R1 result and added no new goal evidence. No historical coordinates, new
source views, raster traces, solver or accepted engine state enter this stage.

## Question and fixed domain

Can exact arithmetic carry both horizontal and vertical coordinate allowances
through an explicitly supported piecewise-linear curve comparison, preserve
shared calibration dependence, and refuse an answer when an allowance reaches
a gap or unknown identity? This is a conditional calculation, not an estimator
of the allowances themselves or a calibration of the historical images.

Reuse `curve_math.SupportedBranch` and its exact integer/Fraction validation,
strictly increasing x and disjoint ordered closed-support rules. Do not change
that frozen implementation. Inputs describe exact toy centerline functions;
allowances describe separate sets around them. No float, bool, nonfinite,
backtracking, vertical-function segment or unrecognized identity is admitted.
`None` as a curve explicitly means unresolved identity/support, not zero force.

First provide a raw local envelope over a closed query interval [l,h], allowing
l=h. If the entire query fits one supported branch, use both query endpoints
and every intervening knot to get exact ordinate extrema, then expand by the
declared nonnegative vertical radius. If any query point falls outside support
or in a gap, return unresolved and no numeric envelope. Do not clip the query
to the visible portion, bridge a dash, extrapolate or omit a troublesome point.

## Shared-calibration pair model

Declare a named shared-axis object with four closed rational intervals:
horizontal scale A>0, horizontal offset B, vertical scale G>0 and vertical
offset H. All combinations within this rectangular parameter box are allowed
in this synthetic model. A real anchor-fit feasible set need not be rectangular;
an enclosing box may be conservative, but is not automatically source-valid.
Do not infer the box or fit it to a desired difference.

For query x in a closed interval X, let t=A*x+B. The continuous reachable t
set is the interval T obtained by exact product and sum extrema, retaining
the same t for both curves. Allow independent set-valued local displacements
u=t+eR and v=t+eS, with |eR|<=rR and |eS|<=rS. These are nonnegative horizontal
radii in the centerline's coordinate system, after the shared transform.
Local ordinate allowances are |dR|<=sR and |dS|<=sS, before shared vertical
scaling. They are sets, not independent random variables. A maps query-x
units to centerline-x units; B and rR/rS have centerline-x units. G maps
centerline-ordinate units to output units; H has output-ordinate units.
Positive G assumes the centerline ordinate already increases with the plotted
physical quantity; native raster y increasing downward needs a prior declared
inversion. No historical conversion is supplied here. This model has exact
knot positions and uncertain query locations, not general uncertain knots.

The difference is explicitly

`D = G * (S(v) + dS - R(u) - dR)`.

The genuinely shared H cancels algebraically; unknown separate vertical
offsets must not be represented as H. Common horizontal error does not in
general cancel because the slopes/shapes may differ. R and S remain separate
measurements even when their toy centerlines coincide; local errors are not
silently equated. Retain the named calibration and all input allowances in
the output so marginal results cannot masquerade as independent observations.

Require R support over all [T.low-rR,T.high+rR] and S support over all
[T.low-rS,T.high+rS]. Any gap, missing tail or unknown identity produces an
unresolved pair with bounds and sign unset, while identifying the failing
curve/query. Malformed inputs are errors, not scientific missingness.

For fully supported input, get the exact minimum/maximum of S(v)-R(u) over
this shared-t model, then expand by sR+sS and multiply by positive G using
both ends as appropriate for signed intervals. A constructive implementation
may clip each pair of linear-segment rectangles in (u,v) by

`|u-v| <= rR+rS`,

along with the respective demanded u/v bounds. These conditions are necessary
and sufficient for a shared t in T: the three one-dimensional intervals
T, [u-rR,u+rR], [v-rS,v+rS] intersect iff they intersect pairwise. Optimize the
affine segment difference at every feasible polygon vertex. Preserve degenerate
line/point intersections (including both radii zero); no fixed sampling grid
or parameter-corner-only shortcut may miss an interior knot extremum.

Return positive only if the lower bound is strictly >0, negative only if the
upper bound is strictly <0; otherwise sign is unresolved, not proof of equality.
Bounds enclose every x in the declared query interval and every admitted
parameter/local-error assignment. Thus a strict sign is uniform over that
query. For nonzero-width X this is one uniform hull, not a separate band at
each x. The bounds are marginal extrema, not a joint distribution,
not necessarily jointly attainable at several x, and not uncertainty bounds
for the integral/peak-location metrics in `curve_math.compare_curves`.

## Fixed verification and acceptance before outcomes

Root owns this declaration and a separately frozen exact analytical oracle;
a producer owns the new adapter and focused tests. The root oracle must freeze
before reading the new producer implementation or results. A separate method
critic reviews the contract and implementation. Shared existing contracts and
method discussion are disclosed; this is not a blind historical study.

Controls must include flat and sloped envelopes; a narrow interior peak missed
by endpoint-only evaluation; point queries; negative coordinates/ordinates;
support-edge contact; queries touching and crossing a gap; missing tails and
unknown identity; positive/negative/zero-touching differences; unequal per-curve
local x/y radii (not one-sided errors); common offset cancellation; different slopes under shared
x error; identical slopes with shared versus independent local x error; sign
changes under uncertainty; positive scale intervals with negative differences;
exact rational values; and rejection of malformed/type-confusable inputs.

Run every declared control, retaining failures and corrections. Compare all
independently expected oracle results. Execute the deterministic oracle/adapter
comparison twice without overwriting earlier artifacts and compare complete
outputs. Root reads final code/tests and replays them after any fix. Record
input/code hashes, runtime, actual commands and scope of independent coverage.
No statistical coverage, human approval or historical validation is implied.

Deliver `curve_uncertainty.py`, focused tests, independent analytical controls
and a review/validation note within this existing unit. Update report/status
navigation. No new framework, historical extraction, accepted bridge transfer,
case promotion, publication, fee, outreach, commit or push. The separate
matrix-save and archived-feedback-routing boundaries remain unchanged.
