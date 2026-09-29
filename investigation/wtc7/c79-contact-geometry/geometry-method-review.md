# Independent mathematical review of the geometry diagnostic

September 13, 2026. Research-only conceptual/mathematical review. The complete
`GEOMETRIC-METHOD.md` reviewed had SHA-256
`73ec992e3c22d981f5cc367a8799635897903aba1b709941ec1ad2aa20c17d9e`.
The current main controls, investigation charter, unit protocol and source-of-
truth/evidence-audit skills control. This review owns only this working note.
No root numerical output, implementation, source geometry or new primary/manual
documentation was inspected. No source acquisition, solver, transmission,
canonical/legal edit or causal ranking occurred.

## Disposition

**The bilinear/triangle-union error bound, interval intersection, parameter-box
extension and AABB broad phase are valid in exact arithmetic under the stated
geometric definitions.** They remain geometric diagnostics, not a reconstruction
of LS-DYNA pair selection, effective thickness, initialization or surviving
restraint. The saved method appropriately distinguishes its numerical buffer
from a certified floating-point error bound and its thickness scenarios from
bounds on effective solver thickness.

Two precise safeguards should be explicit in the implementation and method:

1. If computed `L > U`, do not silently clamp, sort or treat the interval as an
   exact enclosure. A small inversion `0 < L-U <= epsilon` must be class 2
   (ambiguous), irrespective of the usual threshold tests; `L-U > epsilon`
   must fail. The root reviewer confirmed this intended policy in the task
   message, but the reviewed file only said to preserve small inversions.
2. For zero-area triangles, signed plane distance, the plane-projection-inside
   test and a normalized normal are undefined. Store null/undefined status,
   not invented zero distances or ordinary false flags. Distance to the closed
   edges/vertices is still defined. A raw zero cross-product is valid geometry
   data but is not a unit normal.

Finite real coordinates/thicknesses and correctly computed primitive distances
are preconditions of the theorem. Nonfinite intermediate values, overflow,
failed projection evaluation or invalid range ordering must be explicit
computational failures/unknowns, never silent outside classifications or
broad-phase exclusions. This note does not certify an implementation of those
safeguards; the independent numerical arm must check the actual products.

## Independent derivation

Write

    a = P1-P0,  b = P3-P0,  D = P0-P1+P2-P3,
    Q(u,v) = P0 + u*a + v*b + u*v*D,  0 <= u,v <= 1.

Let `TA` be the continuous piecewise-affine parameterization using diagonal
02, and `TB` the one using diagonal 13. Each maps its two closed parameter
triangles onto the corresponding two physical triangles, even if those physical
triangles degenerate or overlap. Direct subtraction gives:

| Parameter region | `Q-TA` | `Q-TB` |
|---|---|---|
| `v <= u` | `-v*(1-u)*D` | Use the sum-based regions below |
| `u <= v` | `-u*(1-v)*D` | Use the sum-based regions below |
| `u+v <= 1` | Use the ordering-based regions above | `u*v*D` |
| `u+v >= 1` | Use the ordering-based regions above | `(1-u)*(1-v)*D` |

Every scalar magnitude is at most `1/4`. For example, on `v <= u`,
`v*(1-u) <= u*(1-u) <= 1/4`; on `u+v <= 1`,
`u*v <= ((u+v)/2)^2 <= 1/4`. The remaining two cases follow by symmetry.

Every patch point therefore has a corresponding triangle-union point within
`w = ||D||/4`, and every triangle-union point has a parameter preimage and a
patch point within the same bound. Both directed distances are bounded, so
the **symmetric Hausdorff distance** between the patch image and each triangle
union is at most `w`. Injectivity, nonzero area, convexity and a unique normal
are not needed for this point-set statement.

For any point `x`, compact sets within Hausdorff distance `w` obey
`|distance(x,S)-distance(x,T)| <= w`: choose a nearest point in either set and
use the triangle inequality plus its corresponding point in the other set.
Consequently both intervals contain the same exact patch distance, and their
intersection is

    L = max(0, dA-w, dB-w),
    U = min(dA+w, dB+w).

In exact arithmetic the intersection is nonempty. The two approximations are
not independent observations or statistical replicates; intersecting their
valid deterministic bounds is simply a tighter enclosure. A planar face need
not have `D=0`, so this bound can be loose even when the two triangle unions
describe the same planar region. Conversely, `D=0` makes the bilinear map
affine and both triangle parameterizations exact as point sets.

## Extension and broad phase

For `e > 0`, set `alpha = -(e-1)/2` and reparameterize

    u = alpha + e*s,  v = alpha + e*t,  0 <= s,t <= 1.

The extended patch remains bilinear. Evaluating its corners in order gives
`R0,R1,R2,R3`, and direct expansion yields

    R0-R1+R2-R3 = e^2 * D.

Thus the same proof applies with `w_e = e^2*||D||/4`; computing the mixed
difference directly from the evaluated corners is mathematically equivalent.
The proposed settings `1.000`, `1.006` and `1.025` all satisfy the required
positive scale. This conclusion does not identify an effective solver MAXPAR.

In the new `(s,t)` coordinates all four bilinear weights are nonnegative and
sum to one. The entire selected patch lies within the convex hull of its four
evaluated corners, hence within their AABB. This holds even though the original
`(u,v)` weights can be negative on an expanded domain. An AABB of the ORIGINAL
corners alone would not have that guarantee for the expanded patch.

The point-to-AABB distance is therefore a valid lower bound on point-to-patch
distance. With known nonnegative scenario threshold `delta_high`, rejection
above `delta_high + epsilon` is conservative for this declared geometric gate
in exact arithmetic. Admitting unknown-thickness nodes unconditionally avoids
claiming an exclusion from an undefined threshold. Floating-point broad-phase
conservatism remains an implementation question because the epsilon policy is
not a proved rounding-error budget.

## Threshold and classification interpretation

The method explicitly defines both delta scenarios as the maximum of the
supplied thickness sum term and `0.05 * Dshort`, retaining the original diagonal
and supplied thickness ranges at every extension setting. For valid finite
nonnegative values with minimum no greater than maximum, monotonicity gives
`0 <= delta_low <= delta_high`.

Those inequalities compare two declared scenarios. They do not prove that
actual interpolated, extrapolated, offset, defaulted or solver-adjusted shell
thickness lies between the scenarios. The method correctly does not extrapolate
thickness merely because it extrapolates the geometry. Its master-alias and
incident-shell extrema are sensitivity inputs, not a recovered field law.

When the exact enclosure is valid, `U < delta_low-epsilon` places the exact
distance strictly below the low scenario gate; `L > delta_high+epsilon` places
it above the high scenario gate. Equality, the intervening thickness range,
numerical boundary proximity and unknown thickness remain unresolved. Calling
these “inside/outside the diagnostic gate” is accurate; calling them actual
ties, engaged contact or surviving restraints would not be.

`epsilon = 1e-10 * max(1, maxabs(selected coordinates))` is a reproducibility/
boundary policy in the unchanged coordinate units. It is not source precision,
measurement uncertainty, statistical confidence or a certified arithmetic
bound. It also depends on coordinate origin and unit scaling, especially through
the floor value 1. Independent agreement at that tolerance checks agreement
between implementations, not physical accuracy or solver fidelity. No tuning
after observing disagreements is licensed by this review.

## Degeneracy, orientation and physical limits

Exact zero-area triangles reduce to their closed edges, and zero-length edges
to points. Near-degenerate triangles require retained conditioning flags and
checked finite arithmetic; mathematical existence of distance does not make a
particular plane-projection calculation numerically stable. The proposed area
flag is a numerical convention, not a physical minimum-area criterion.

For the bilinear map the tangent vectors are `a+v*D` and `b+u*D`; their cross
product is the parametric normal before normalization. It can vanish or reverse.
Corner/center checks and triangle-normal dot products are useful warnings but
must retain undefined/zero cases and must not be represented as an exhaustive
self-intersection, injectivity or solver-surface-validity test. The method
already states the latter limitation appropriately.

The Hausdorff bound still holds for self-crossing/folded or repeated-corner
images. That does not supply a unique side, normal, physical shell interior,
contact projection, signed gap or acceptable contact surface. Euclidean
closeness without one-sided rejection is deliberately a wider diagnostic than
a solver-specific oriented projection or contact admissibility rule.

Likewise, same-node/same-part cases, duplicate master records and multiple
nearby masters must remain visible. Distance zero or multiple admitted rows
does not establish a tie; solver exclusions, offsets, search/order rules,
deformation, normals, initialization and contact/constraint mechanics can
distinguish them. No restraint stiffness, force, load path adequacy, instability
or historical cause follows from this diagnostic alone.

## Actual review coverage and remaining checks

This review independently derived the exact formulas above and read the whole
pinned prospective method. It did not rerun or inspect root calculations,
source/control/manual findings, extracted arrays or either implementation.
It offers **mathematical clearance with the stated safeguards**, not numerical
reproducibility or primary-source applicability certification.

The declared synthetic tests are appropriate. Add explicit tests for the small-
inversion ambiguity gate, excessive inversion failure and undefined plane
quantities if not already included. Test nonfinite intermediate handling and
near-degenerate projections without converting warning flags into ordinary
finite zeros. Compare unpruned and AABB-pruned synthetic results at all declared
extension settings. Preserve failures and any independently reproduced
disagreements; passing tests establish their tested scope only.

### Final pre-evaluation clarification disposition

The complete `GEOMETRIC-IMPLEMENTATION-ADDENDUM.md` was then read and its
SHA-256 independently checked as
`ada9f0cdfcb7d7dd3fd79d3c8cd6daf9f0a3f0937c6e7420f7c23dbd34fba9bd`.
It explicitly resolves both requested rules: small inversions retain their
values and become class 2; larger inversions fail; undefined plane quantities
use schema-defined NaN and projection flag -1, separately from raw zero cross
products and ordinary 0/1 projection flags. These intentional undefined-plane
markers must remain distinct from unexpected nonfinite distances, bounds or
thresholds. The original method hash remains unchanged.

**Bounded mathematical/conceptual clearance with those saved clarifications.**
No unresolved proof error was identified. Actual implementation, numerical
tests/results, source/manual applicability and physical/solver conclusions
remain outside this clearance. This disposition does not certify completion
merely because anticipated code or output filenames exist.
