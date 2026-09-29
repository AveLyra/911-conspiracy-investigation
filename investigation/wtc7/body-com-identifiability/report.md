# What would connect the visible descent to a force measurement?

2026-09-24. Research-only Q04/Q05/Q06/Q10. The present records support rapid
descent and approximately common apparent motion in a selected facade region.
They do **not yet supply a defensible historical bound on that region's
roof-point/center-of-mass motion**. This unit explains precisely which missing
information matters, tests that conclusion mathematically, and avoids demanding
information that is not actually necessary.

The [source review](source-review.md) finds extensive released model geometry
and concrete mass-card locations—not an absence of structural information.
It also finds that the stronger two-feature Camera3 observations cannot be
silently joined to the Camera2 samples used in the preceding force calculation.
No historical force, new acceleration or cause ranking is computed here.

## What the observations do and do not identify

The [Camera3 A/C result](../camera3-facade-feature/report.md) allows a single
constant image separation within both observers' original boxes at20/22
selected samples. It supplies affirmative evidence for approximately common
apparent motion, not proof of a known rigid material body. The louver-corner
architectural association is useful; exact attachment, depth, full assembly
membership and physical pose remain unidentified. The different Camera2 four-
point correspondence has its own smoke, feature-continuity and clock/scale
limits. These limitations must not erase the positive gravity-scale curvature
in the published data or be presented as measured large errors.

Three candidate systems have different meanings:

| Material system | What its force would describe | Current missing information |
|---|---|---|
| All original building material, including fragments | Net external force on that entire fixed set | Motion/enclosure of hidden and dispersed material, not just roof motion |
| A region fixed by original story/member membership | Net force on that particular material region | Exact membership and its phase-resolved position/deformation bounds |
| A specified facade assembly | Forces on that assembly, including attachments and contact with other structure | Material/geometry join, sufficiently constrained pose/deformation, and a COM bound |

An attached facade is a valid fixed material set; it need not first detach.
Its attachment forces are external to that set. Fragmentation likewise does
not invalidate a fixed set if its original particles are retained in the
accounting. A spatial volume that gains/loses material requires momentum-flux
terms instead. Absolute total mass cancels from the force-to-weight ratio;
a numerical tonnage estimate is not a prerequisite once the COM motion is known.

## Exact finite-interval question

Downward is positive. At physical times tc-h,tc,tc+h, write

    A[x] = (x_- - 2*x_0 + x_+) / h^2.

This is the triangular-weighted mean acceleration under the regularity
conditions in the [prior derivation](../finite-interval-force/report.md).
For fixed mass M, COM z, downward non-gravity force D and upward force U,

    weighted_mean(U-D)/(M*g) = 1 - A[z]/g.

Let a tracked physical point be p and r=p-z. The exact smallest maximum
three-sample residual after removing an arbitrary affine trend from r is

    B* = |r_- - 2*r_0 + r_+| / 4.

The lower bound follows from coefficient magnitudes1,2,1. For signed
d=(r_--2*r0+r_+)/4, residuals(d,-d,d) attain it; subtracting them from r
leaves an affine triple. Thus B* is not directly a peak-to-peak change or
the point's total descent. In a symmetric extremal example, peak-to-peak
residual is2B*. No bound on between-sample or instantaneous motion follows.

The prior B_min(rho) is a **necessary lower threshold** for accommodating
at least a proposed weighted net upward force. A useful geometry test would
supply an independent **upper bound** on B*. If that upper bound is below
the necessary threshold, that force proposal is excluded under the other
assumptions. Without such a bound, this calculation alone does not decide it.

## Two explicit missing-information examples

These constructions are exact kinematics for reduced observation sets, **not
demonstrations of mechanically feasible WTC7 histories**. Their purpose is to identify what an
additional measurement must constrain, not to grant a favored mechanism
arbitrary hidden movement or unexplained downward forces.

**Hidden material.** Let a visible group's COM be p+c, where c is constant;
a hidden group's fixed mass fraction is eta, and its COM is p+c+s. Then
the combined COM is z=p+c+eta*s. Changing only the unobserved relative
motion s changes the total COM while leaving all selected visible motion
unchanged. Specifically, relative to affine s0, set

    s(t) = s0(t) - (B/eta)*(2*((t-tc)/h)^2 - 1).

Then A[z] decreases by4B/h^2 while the visible history is identical.
The departure from the affine baseline s0 is bounded by B/eta throughout the interval. A known
clearance bound, mass fraction or actual observation of the hidden group
would limit or reject this example. It is not evidence that such excursion
occurred, had adequate clearance, or could satisfy the building's force and
energy requirements. Same visible points do not imply same full images.

**Rigid panel with only its top line observed.** Put markers along local
(x,0,0), COM at(0,0,L), translate by p(t) in downward z, and rotate about
the marker line by theta(t). Every top-line marker remains at(x,0,p(t)),
even with perfectly measured3D coordinates, but COM height becomes

    z(t) = p(t) + L*cos(theta(t)).

Identity orientation and a varying orientation therefore need not have the
same COM curvature. If the middle orientation is zero and both endpoint
cosines equal c, the correction is

    A[z] - A[p] = -2*L*(1-c)/h^2,
    B* = L*(1-c)/2.

An off-line same-body marker changes position in this construction. A complete
calibrated facade view could rule it out. We have **not** shown that the four
historical roof labels are exact collinear material markers, that the actual
facade rotated this way, or that the construction fits the actual videos.
It demonstrates why a roofline-only reduced constraint is insufficient, not
why all image evidence must be ignored. Even rigidity alone is not enough
unless orientation is also fixed or constrained.

## Sufficient bounds: what would make the test work

1. **Full-body vertical envelope without known mass distribution.** Suppose
   every particle in the selected fixed set has offset from p in[L_j,U_j] at
   each sample. Positive-mass convexity puts COM in the same interval. Therefore

       (L_- - 2*U_0 + L_+)/h^2 <= A[z]-A[p]
                                <= (U_- - 2*L_0 + U_+)/h^2.

   This is a conservative box bound; it does not assert all extrema are
   structurally attainable or independent in a real body. It needs the entire
   selected material set, not merely the visible silhouette. Known sub-body
   mass fractions can tighten the intervals. A static model-coordinate box
   is not a measured changing historical envelope.

2. **Bounded hidden/visible relative motion.** If the visible point/visible-COM
   affine residual is bounded by BV, hidden/visible-COM affine residual by BH,
   and the hidden mass fraction eta is fixed and at most eta_max, then

       B* <= BV + eta_max*BH.

   Actual bounds on those quantities, not an invented allowance, would connect
   the observation to the force test.

3. **Rigid pose with known or bounded COM location.** For a body-fixed marker a,
   body-fixed COM c, translation T and proper rotation R, p=T+R*a and z=T+R*c.
   Their vertical second-difference correction is

       A[p_z]-A[z_z] = e_z^T*(R_- - 2*R_0 + R_+)*(a-c)/h^2.

   A known constant3D orientation makes this zero, regardless of absolute
   total mass or exact c. If |a-c|<=L, the magnitude is at most
   L*||(R_--2*R0+R_+)^T e_z||/h^2. A known convex COM region gives tighter
   extrema of this linear functional. Three known noncollinear same-body3D
   markers determine a proper rigid pose; projected2D points still require
   calibrated geometry/pose and ambiguity analysis. A stable marker triangle
   does not establish rigidity of the unobserved remainder without justification.

## Synthetic verification and claim strength

The [prospective fixtures](PROTOCOL.md) use arbitrary units and no WTC7
measurements: eight hidden-mass cases, eight rigid-rotation cases, two envelope
cases, affine-removal controls and invalid-input checks. The loose envelope
does not exclude a net upward fraction of at least1/4; the tight envelope excludes it.
This checks that the method can discriminate when information is supplied;
it does not estimate a historical uncertainty or favor a mechanism.

The centered toy trajectory p=5t^2 is a curvature normalization, not an
asserted reversal or start-from-rest during the collapse. Adding a common
affine translation leaves every relative offset and second difference unchanged;
choosing its downward velocity greater than10h makes that visible trajectory
monotonically downward throughout the example interval. This removes a
superficial kinematic objection, not the unresolved structural-feasibility test.

[Producer results](run01/results.json) preserve all sixteen example histories,
rotations, COMs and affine witnesses, plus both envelope results. Producer
controls recover24 proper poses and check144 pair distances. A separately
implemented oracle froze results before comparison. See the
[independent review](independent-review.md) and [validation](validation.md)
for actual agreement, repeats, scope and any outstanding critique.

| Claim | Type / strength | Strongest objection or falsifier |
|---|---|---|
| Selected visible point histories alone can leave COM curvature unidentified. | Derived; directly established for the stated reduced observation models. | Additional full-image, rigid-pose, mass or envelope constraints can exclude the constructed alternatives; this is not nonidentifiability under every available observation. |
| The reviewed holdings now provide a defensible historical B upper bound. | Not established within this bounded source join. | A source-linked body definition and same-time3D/deformation/envelope measurements could supply one; located but unjoined records remain leads. |
| A full mass model and prior detachment are mandatory before any force/weight inference. | Overstatement, corrected here. | Fixed-set Newtonian mechanics, convexity and verified constant orientation supply counterexamples to those supposed prerequisites. |
| Some unspecified hidden motion proves substantial support could coexist with the historical roof motion. | Unsupported as a building-specific conclusion. | Actual geometry, force/energy/contact histories and matching image predictions are required. |
| Rapid observed descent can be dismissed because the COM is not perfectly known. | Unsupported. | Positive curvature/common-motion evidence remains; quantify uncertainties and test specified mechanisms rather than discard it. |

## What changes and the next discriminating record

The earlier practical dependency is now sharper: **identify the body and bound
its relative geometry**, not necessarily weigh the whole building. The original
north-elevation/lower-west-louver detail and same-time, calibrated material-point
correspondence are the most direct route for the facade candidate. Their presence
elsewhere in local holdings has not been excluded by this audit. A bounded
drawing/attachment locator is preferable to inventing a numerical B or running
more fits on the same unjoined roof-point table.

If the needed geometry cannot be recovered, preserve the conditional force
constraint and the positive rapid-motion observations separately. Neither this
limitation nor the synthetic alternatives validate NIST's initiating sequence,
establish deliberate removal, or answer how actual connections failed. Those
claims still require the building-specific propagation and mechanism evidence.
This closes a measurement-dependency audit, not the full investigation. No main,
raw, canonical legal, accepted Sherlock/Faraday or external state is changed.
