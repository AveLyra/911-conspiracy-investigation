# Finite-interval net-force constraint

2026-09-24. Q04/Q06 method and conditional calculation under the main charter.
Root and `/root/motion_force_gap` independently identified the finite-interval
identity before exchanging numerical results. A bounded read of six current
reports and three linked methods found no existing implementation of this
force bound; earlier fit, clock, perspective and transition tests remain valid
within their scopes. This is not a new video measurement or new evidence about
the actual moving mass.

## Objective and acceptance before computation

Quantify the **minimum non-affine tracked-point/center-of-mass displacement**
needed to accommodate a proposed lower bound on net upward force during a
selected interval. Test this through a displacement identity without inferring
instantaneous force, failed-column count, or a mechanism from one roof point.
Deliver a derivation, exact input/value table, continuous threshold functions,
independent arithmetic and methodological review, and a readable conditional
interpretation. An inability to supply a historical COM bound remains material,
not an excuse to call either substantial support or zero support proved.

Source: already reconciled page47 positions in
`../multipoint-table-reproduction/transcription-root/table47.json`, SHA256
`a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc`.
Underlying held Chandler/Walter/Szamboti2023 PDF hash
`cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394`.
No fresh transcription or source authentication is claimed. Printed source y
is upward; negate it once for downward physical interpretation.

Use endpoints and midpoint of the **existing primary windows**, fixed before
this unit's calculation: NE at8.0,8.6,9.2s; EC/WC/NW at8.2,9.4,10.6s.
These windows have different lengths and must not be treated as simultaneous
whole-facade measurements. Use their actual three position entries, not fitted
coefficients. Preserve all12 inputs, exact tokens, row indices, and null failures.

Three clock scenarios from the prior clock audit: printed nominal clock,
uniform time multiplier1001/1000, and1000/999. The latter correspond to the
previously declared six-frames-per-sample interpretation at30000/1001fps and
2997/100fps. They are scenarios, not recovered original clocks. Length scale
is the source's assigned scale throughout; physical calibration remains open.
Use g=9.81m/s^2 as a reference convention, not a surveyed local measurement.

For each of four points and three clocks, calculate the centered second
difference A and its exact nearest-hundredth printing half-width0.02/h^2.
Printing uncertainty is not tracking, physical calibration, or COM uncertainty.
Provide the full continuous one-sided threshold

    B_min(rho) = max(0, [h^2 * (A_low - g + g*rho)] / 4)

for a proposed **at-least-rho** triangular-weighted net upward force fraction.
Retain the exact affine slope/intercept inside max; show values at rho=
0,0.1,0.25,0.5,0.75,1 as illustrative force scenarios, not probabilities or
historical proposals. Do not optimize windows or assume a physical B value.
There are12 clock/point cases and72 scenario evaluations. No interpolation,
smoothing, coefficient fitting or new raw-media decoding.

## Mechanical definition

Physical times are tc-h,tc,tc+h, downward displacement positive. A[p] is the
triangular-weighted acceleration, kernel(h-|t-tc|)/h^2 over this interval.
For a fixed set of material particles of constant total mass M with center
z and constant gravity, M*a_z=M*g+D-U. Define R=U-D as net upward external
non-gravity force. Internal forces cancel only within the defined material set;
mass accretion through a spatial boundary requires a different equation.

If p=z+r and at each sampled time |r-(alpha+beta*t)|<=B, then
|A[p]-A[z]|<=4B/h^2. The affine offset need not be known. This is a geometric
dependency, not permission to assume arbitrary deformation or a compensating
downward pull. Together with A[p] in[a_low,a_high], it bounds the triangular-
weighted R/(M*g) between1-(a_high+4B/h^2)/g and1-(a_low-4B/h^2)/g.
The bound concerns signed net force. It neither separates U and D nor bounds
every column, peak instantaneous force, restoring stiffness, or failure time.

## Verification and boundaries

Root uses exact Python Fraction arithmetic; a separate reviewer implements
and checks the cases independently without importing root code or results
before freezing its output. Require exact agreement on tokens, memberships,
clock factors, A/printing intervals, hinge coefficients and all72 evaluations.
Verify constant/linear/quadratic and higher-polynomial identities by analytic
integration; test affine-offset invariance and all eight signs of three-point
bounded errors to verify sharp extrema. Include malformed/null/missing-time
rejections. Independently derive the formula and ensure a bounded oscillatory
offset does not get interpreted as an instantaneous acceleration bound.
One same-code repeat confirms deterministic output; numerical agreement is
not historical physical validation.

Pin source table, PDF, protocol, code and runtime in generated receipts.
Use create-only output directories. New work is confined to this worktree;
main/raw/legal/accepted-engine state, prior measurements and source PDFs are
preserved. No new network, solver, costs, outreach, private transfer, commit,
or push. Necessary-displacement thresholds are a test requirement for later
geometry/COM work, not an actual historic force measurement or causal ranking.
