# Exact-arithmetic diagnostic follow-up

September 13, 2026. Prospective for this follow-up, AFTER both floating-point
implementations froze. Their results, code, comparisons and disagreements
remain preserved. This is not a retrospective claim that the original
floating classification reproduced. No physical input or gate is tuned.

## Trigger and unchanged question

The root implementation retained 325 small inverted distance enclosures,
maximum 2.7755575615628914e-17 versus its declared numerical buffer 9.4869e-9.
Its entire class2 population comes from these inversions, including rows
otherwise outside the distance gate. A separately written triangle routine
has different class counts. Consequently neither class2 counts nor apparent
changes in class2/3 membership may be interpreted as physical thickness or
extension sensitivity. An arithmetic resolution is needed before a reliable
candidate-to-deletion-list join. Failed replication is evidence about these
calculations, not the source model or collapse.

Keep the original population, ordered master records, parsed coordinates,
supplied thickness scenarios, settings 1/1.006/1.025, both triangulations,
bilinear bound and classification margins. Replace approximate evaluation
of these geometric definitions with rational arithmetic and outward square-
root intervals. This is not a new contact algorithm or effective solver rule.

## Rational inputs and intervals

Interpret each frozen IEEE-754 coordinate, supplied thickness and numerical
constant (including the three e values, 0.6, 0.05 and saved epsilon) as its
EXACT binary rational using as_integer_ratio. This certifies a calculation
on parsed values, not unrounded source decimals or physical dimensions.
Compute extended Q corners rationally from original frozen coordinates;
do not use rounded extended corners from either floating output as inputs.

For each triangle compute its squared closed-set point distance exactly:
the minimum of three closed-edge squared distances and squared perpendicular
plane distance if the projected point is inside by exact oriented-cross
signs. Zero-area triangles use edges/vertices. All dot/cross products,
projection signs, clamping, squared distances and comparisons are rational.
Use the minimum squared distance for each two-triangle union. Signed plane
distances remain undefined for a degenerate plane; exact flags use -1/0/1.

For nonnegative rational x=a/b, outward square-root bounds at precision k:

    n = isqrt(floor(a * 2^(2k) / b))
    lower = n / 2^k
    upper = lower if n^2*b == a*2^(2k), else (n+1)/2^k.

This integer construction encloses the exact nonnegative root. Use fixed
k=80 and k=120 in separate full runs; do not adapt precision or thresholds
to obtain a preferred classification. The half-length mixed-difference
expression is still w=norm(R0-R1+R2-R3)/4 (equivalently square root of its
squared norm divided by16). Preserve both source constants and all formulas.

Combine interval endpoints outward. For the patch distance, retain

    L_lower = max(0, dA_lower-w_upper, dB_lower-w_upper)
    U_upper = min(dA_upper+w_upper, dB_upper+w_upper).

These outer endpoints contain the exact enclosure from the mathematical
review. Threshold intervals use exact thickness sums and outward shorter-
original-diagonal roots. Certify class3 only if U_upper < delta_low_lower
- epsilon; certify class1 only if L_lower > delta_high_upper + epsilon;
otherwise retain class2. Unknown thickness stays class0. No small-inversion
repair is needed: require L_lower <= U_upper exactly. This is an arithmetic
certificate within the declared geometric surrogate, never physical accuracy.

## Complete, conservative broad phase

Do not assume that either floating admission mask is complete. For each CID
and master, bound delta_high for every known node by using the population's
maximum supplied slave thickness and the master maximum. Obtain an outward
rational upper bound G using the same root intervals. Every potentially
qualifying point must lie in each exact axis slab [min(Q)-G, max(Q)+G].

Use sorted source float coordinates to find slab candidates efficiently.
Before searching, convert each exact rational slab endpoint to a float and
adjust outward with nextafter until its exact binary-rational value is on
the conservative side. All source floats represent the original rational
coordinate ordering exactly. Intersect the three index selections; this
cannot exclude a point in the exact slab. Unknown-thickness nodes are always
retained independently of location.

For the slab candidates, compute point-to-AABB squared distance exactly and
admit if it is <= (the node's delta_high upper bound)^2. Preserve any
interval-straddling box comparison as an admitted uncertainty, not exclusion.
Record every complete-population mask, slab and exact-box counts, including
all zeros and unknowns. Compare masks with both frozen floating runs, but
do not force agreement. The outward broad phase may retain additional
boundary cases while certifying that no qualifying known-thickness point was
lost under THIS domain and these thresholds.

## Output and verification

Preserve exact identity/classification/projection arrays, packed masks and
source/geometry pins. Retain rational numerator/denominator endpoints for
each admitted row's patch and threshold enclosure in a separate JSON proof
record; ordinary displayed floats are only views. Keep the complete source
arrays as dependencies, not new raw-source reconstructions. Reproducible
derived part joins remain numeric and source-pinned.

Before historical evaluation test perfect/inexact rational square roots,
outward conversion, interior/edge/vertex projection, reversed winding,
degenerate triangles, known warped patch points, extended-domain-only
admission, whole-population broad-phase conservatism on synthetic geometry,
unknown priority, interval-threshold overlap and create-only/pin guards.
Use 80/120-bit runs to compare exact classifications/membership and enclosure
nesting; report any failure without tuning. Independent review must inspect
the arithmetic, method and receipts, and reproduce the material results or
state its exact coverage limitation. Retain the original failed floating
comparison as such even if this follow-up succeeds.

No solver, raw edit, source acquisition, historical pairing, force/capacity,
floor identity, cause ranking, legal promotion, transmission or bridge use.

## Pre-evaluation correction: preserve the existing numerical buffer

Two independent reviewers identified an omitted epsilon in the broad-phase
description above before either exact implementation evaluated historical
geometry. For this follow-up, G is the global delta_high upper bound PLUS
the unchanged saved epsilon, and each exact AABB admission compares squared
distance with (the node's delta_high upper bound PLUS epsilon)^2. These rules
supersede the two unbuffered expressions above. They retain the original
floating protocol's buffer rather than silently dropping its boundary band.
Unknown-thickness class0 always takes precedence, including any diagnostic
inversion flag. The word "half-length" above is a wording error: w remains
the explicit norm/4 formula. No results were used to choose this correction.
