# What rapid descent constrains over a measured interval

2026-09-24. Research-only Q04/Q06. This extends the existing motion/force
boundary with a finite-interval calculation and a testable geometric dependency.
It does not measure WTC7's actual resistance or supply an independently
calibrated center-of-mass trajectory.

The new result is a **necessary displacement threshold**: if the printed
roof-point coordinates and times represent physical vertical motion, how much
changing separation between that point and a defined body's center of mass
would be needed to accommodate a proposed amount of net upward resistance?
The point-versus-COM caveat can thereby be tested quantitatively rather than
used as an unlimited explanation for a gravity-scale descent.

## Input and prospective choices

[Protocol](PROTOCOL.md) fixes the endpoint/midpoint triples of the already-used
primary windows before this calculation. No fit window was optimized for a
force result. Input is the previously independently reconciled page47 position
table from the held2023 Chandler/Walter/Szamboti paper; provenance and physical
calibration limits remain those of the
[table reproduction](../multipoint-table-reproduction/report.md).
Source y is positive upward and is negated once. Only twelve position slots
enter; no velocities, smooth fit coefficients or inferred hidden positions.

| Feature | Printed times (s) | Printed upward-y tokens | Source rows |
|---|---|---|---|
| NE | 8.0, 8.6, 9.2 | 127.98, 125.51, 119.77 | 46,49,52 |
| EC | 8.2, 9.4, 10.6 | 127.25, 117.06, 92.59 | 47,53,59 |
| WC | 8.2, 9.4, 10.6 | 128.40, 119.66, 95.47 | 47,53,59 |
| NW | 8.2, 9.4, 10.6 | 129.68, 120.61, 96.85 | 47,53,59 |

Positions have assigned metre units. Nominal times and two previously declared
uniform clock multipliers1001/1000 and1000/999 give12 cases. Neither those
clocks nor the scale has been authenticated as the historical physical
measurement. The reference g=9.81m/s^2 is a convention, not measured local g.
NE's1.2s interval is shorter than the other three2.4s intervals. They are not
simultaneous full-facade samples; no different windows are silently pooled.

## Derivation and the body boundary

Let physical downward position be p(t), sampled at tc-h,tc,tc+h. Define

    A[p] = (p(tc-h) - 2*p(tc) + p(tc+h)) / h^2.

For a trajectory with absolutely continuous velocity (in particular, a twice
continuously differentiable trajectory), integrating twice and eliminating
position/initial velocity gives exactly

    A[p] = integral[-h,h] ((h - |s|)/h^2) * p''(tc+s) ds.

The triangular kernel is nonnegative and integrates to1. Thus A is a weighted
interval mean, not a fitted instantaneous derivative or a claim of constant
acceleration. Derivation does not require a from-rest initial condition.

Choose a **fixed material set** with constant total mass M and COM z(t).
With constant gravity, external downward force D and upward force U,

    M*z'' = M*g + D - U,
    R = U - D,
    weighted_mean(R)/(M*g) = 1 - A[z]/g.

R is signed net external non-gravity force. Internal forces cancel only for
the specified set. A geographic envelope that collects newly falling material
is a different system with momentum flux. No WTC7 material set, mass fraction,
or historically correct external-force inventory has been identified here.

If the tracked physical point is p=z+r and some affine function alpha+beta*t
satisfies |r(ti)-(alpha+beta*ti)|<=B at all three sampled times, then

    |A[p] - A[z]| <= 4*B/h^2.

The affine term cancels. B is a bound on **non-affine relative displacement**,
not absolute separation, the point's net descent, or deformation at only the
middle frame. The bound follows from coefficient magnitudes1,2,1 and is sharp:
sample residuals(B,-B,B) attain the upper limit. No particular deformation is
assumed to have happened. Rotation and relative motion of hidden mass must be
accounted for before a physical B bound can be supplied. Constant separation
between two visible roof points does not bound either point relative to the
hidden COM.

If the physical A[p] is bounded by[a_low,a_high], then

    1 - (a_high + 4*B/h^2)/g
        <= weighted_mean(R)/(M*g)
        <= 1 - (a_low - 4*B/h^2)/g.

For a proposed **lower bound rho** on that force fraction, a necessary condition
is

    B >= B_min(rho) = max(0, h^2*(a_low - g + g*rho)/4).

This follows because weighted_mean(R)/(Mg)>=rho requires A[z]<=g*(1-rho).
At the three-sample mathematical level the positive threshold can be attained
with the stated extremal residuals and A[p]=a_low. That existence witness is
not a mechanically valid building reconstruction; the geometry, mass and other
observed points may impose additional constraints. rho=0 means **nonnegative
net upward force**, not an equality R=0. rho=1 means a mean net upward force at
least equal to this body's weight; it does not name every intact support.

## Conditional values and their limits

For this illustration a_low/a_high include **printing rounding only**:
independent nearest0.01 position tokens give0.005 per coordinate and
half-width0.02/h^2 for A. These are not physical measurement error bars.
Scale, time, projection, annotation and material-point uncertainties have not
been folded into these small intervals. If those errors are supplied, the
force bounds must be recalculated; wider acceleration bounds can reduce the
necessary B thresholds.

Nominal-clock results; A in assigned m/s^2, B in assigned metres under the
conditional physical interpretation:

| Feature | A | Printing-only A interval | B_min(0.25) | B_min(0.50) |
|---|---:|---|---:|---:|
| NE | 9.08333 | 9.02778 to9.13889 | 0.150325 | 0.371050 |
| EC | 9.91667 | 9.90278 to9.93056 | 0.916300 | 1.799200 |
| WC | 10.72917 | 10.71528 to10.74306 | 1.208800 | 2.091700 |
| NW | 10.20139 | 10.18750 to10.21528 | 1.018800 | 1.901700 |

Example: given the NW nominal coordinates and only their printing allowance,
net upward resistance with a triangular-weighted average at least one quarter of a **defined body's**
weight would require a non-affine point/COM displacement allowance of at least
1.0188 assigned metres across the three samples. If an independently justified
bound were smaller, that particular force hypothesis would be excluded under
the other assumptions. No such physical bound is presently supplied. Conversely,
an allowance large enough to pass is only a necessary geometric condition;
it does not show that a building can realize the required force/motion history.

The complete continuous functions are max(0,intercept+slope*rho). For the
nominal clock their(intercept,slope) pairs are NE(-0.0704,0.8829),
EC(0.0334,3.5316), WC(0.3259,3.5316), NW(0.1359,3.5316). All12 clock/point
functions and all72 predeclared evaluations are in [results](run01/results.json).
Positive B_min(0) in some assigned-coordinate cases must not be presented as
historical faster-than-gravity motion or actual downward pulling. It tests
a conjunction of unvalidated scale/time/point/COM/force assumptions.

These second differences intentionally differ from the earlier all-sample
quadratic/velocity regressions. They use different linear weights, and three
samples discard intervening information. The protocol supplies a transparent
interval constraint, not a claim that three points are the most informative
estimator or that the source's labels are falsified by a different statistic.
No sample set was selected after seeing these values.

## What this changes and what would falsify it

The mathematical and assigned-coordinate computations strengthen the method
for testing the user’s objection: sustained gravity-scale COM acceleration
would tightly constrain **net** upward resistance. It cannot coexist with a
large uncompensated upward force on that same body over the same weighted
interval. A proposed downward pull must come from a physically justified force
history, not an unexplained cancellation introduced to rescue a favored model.

However, bounded position offsets do not bound instantaneous accelerations:
r(t)=B*cos(omega*t) stays bounded for every omega while |r''| can grow without
limit. The actual three-point bound therefore concerns weighted interval force;
it establishes neither peak resistance, all-column failure simultaneity,
absence of stiffness, initiation by fire, nor deliberate removal.

| Claim | Evidence layer / present strength | What would change it |
|---|---|---|
| Finite difference equals triangular-weighted acceleration and yields the stated COM-force bound. | Derived; exact under the declared mechanics/regularity conditions. | Algebra, sign, normalization, body-boundary or independent arithmetic failure. |
| The selected printed samples give the reported12 conditional functions. | Derived from previously checked published tokens; two independently implemented calculations agree exactly on all12 cases and72 thresholds. | Changed/mistranscribed source values, wrong windows/clock factors or comparison mismatch. |
| Actual WTC7 net resistance had one of these values. | Underdetermined; no historical B, COM/material set or physical uncertainty envelope supplied. | Independently calibrated physical tracks and source-grounded relative-motion/COM bounds for the same body and interval. |
| Every support suddenly disappeared, or a particular mechanism did it. | Unsupported by this calculation alone. | A specified and validated force/load-path/failure chronology with independent mechanism evidence. |

## Verification and next dependency

Root's exact-fraction implementation produced12 cases/72 thresholds and an
identical same-code repeat. It checked15 analytic polynomial/affine identities,
two sets of eight error-corner extrema, source-rounding extrema and threshold
witnesses in every case, and five malformed/missing-input rejections.
The separate implementation froze its output before seeing root code/results;
the exact comparison and methodological review are recorded in
[independent-review.md](independent-review.md) and [validation.md](validation.md).
Numerical verification and synthetic sharpness do not authenticate the source
measurements or establish a physically realizable structure.

The next material step is to bound the changing point/COM displacement for a
specified moving material set using actual visible geometry plus a documented
mass model, or demonstrate why available footage cannot do so. Several visible
roof points moving together do not constrain hidden internal mass without
additional assumptions. A proposed alternative is to use the visible facade
as the material set, but its mass, attachments, 3D deformation, detachment and
external forces must then be audited explicitly. If no body boundary can be
identified from accessible records, retain this as a conditional force test
and name that limit; do not accumulate more fit variants as a substitute.
