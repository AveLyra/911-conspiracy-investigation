# Lateral roof-corner geometry: what is and is not reproduced

2026-09-20 UTC. Research-only continuation of the independent investigation and
Luna-summary reevaluation. [Source protocol](PROTOCOL.md), [root reading](root-reading.md),
[separate reading](independent-reading.md), [prospective arithmetic](MATH-PROTOCOL.md).
No historical pixel measurements, source acquisition or cause ranking added.

## Result

**The published images and construction have positive, conditional evidentiary
weight for lateral deformation. We have not independently reproduced the
reported 11 m +/- 3 m magnitude or its uncertainty from these eight pages.**
The report combines that estimate with a second camera to infer motion
primarily northward; it does not give a separately calibrated exact north
component. Failure to reproduce the interval is neither a zero-displacement
finding nor evidence that NIST fabricated it.

The geometric principle is sound for ideal central projection, with lens
distortion corrected or bounded: with the same identifiable corner and a
fixed or correctly registered camera, a point descending purely vertically
stays on the projected line of its original vertical edge. A genuine departure
from that line requires lateral displacement. This does not require the whole
facade to remain rigid. But establishing a genuine departure, its world
direction and its metric size requires feature identity, camera correction,
calibration and time correspondence that have not been independently measured
here. Reading NIST's annotated derivatives is not an independent raw-video test.

## Source and input audit

Primary source: held [NCSTAR 1-9](/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf),
SHA256 `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.
Both prior-informed AI readers viewed all eight complete pages separately and
froze notes before exchanging interpretations. They share the same source and
are not independent historical witnesses, blinded readers or engineering experts.

| Physical / printed pages | What is actually supplied | What this audit cannot substitute |
|---|---|---|
|53 /9|Approximate trapezoidal dimensions and building context.|A surveyed corner-coordinate model, plan skew and dimensional uncertainty.|
|307–308 /263–264|Camera-location map, scale bar and contextual views.|Numerical camera poses, elevations, calibration and error bounds; distant Cameras 1/2 are not Cameras 3/4.|
|320–321 /276–277|Camera 4 hand movement/zoom and registration using two foreground buildings; original/current edge near-coincidence in five displayed views; differing NE/NW edge behavior.|Transformation matrices, point placements, residuals and a rigid-facade assumption. Foreground registration can leave depth-dependent errors if camera position changes.|
|322 /278|Camera 4 panels at 6.7, 7.7, 8.8, 9.7, 10.1, 10.6, 10.9, 11.4 seconds; reported westward tilt by 10.6.|An exact Camera 4 observation at the Camera 3 construction's 10.3 seconds, or a justified interpolation/error bound.|
|323–324 /279–280|Camera 3 difference images and the heavily processed 10.3-second construction; stated use of line angle, building dimensions, camera distance and corner viewing angles; 11 m +/- 3 m estimate.|The original equation/worksheet, numerical camera distance and viewing angles, complete annotation definitions and propagated uncertainty.|

Figure 5-206 contains the labels `60` and `91, -54 degrees`; these pages do not
fully define their units/endpoints or roles. Guessing their meanings to obtain
11 m would be fitting the answer. The prose's line-angle referent needs
clarification, not an accusation that parallel lines make the method impossible.

Two bounded correspondence issues remain. The illustrated Camera 4 series
brackets 10.3 seconds with a near-aligned 10.1-second view and a tilted
10.6-second view. This does not prove intervening video was unavailable to
NIST; it means the exact-time join is not published in this page set. Also,
roughly ten stories of descent in the earlier discussion and roughly seven
in the target construction require feature/time clarification before becoming
metric constraints. Approximate prose alone does not establish a contradiction.

## Independently checked mathematics

For a vertical edge at horizontal position H0 and camera center C, the original
edge's image line corresponds to the vertical world plane through C and H0.
Its horizontal unit normal n gives a signed distance q for a displaced point:

```text
n . d = q,                 d = (east displacement, north displacement)
N d = (q1,q2),             N has the two camera-plane normals as rows
d = inverse(N) q,          when det(N) is nonzero
```

**q is a physical plane distance, not a pixel offset.** Perspective depth and
camera calibration are needed to convert image data to it. The ideal central-
projection equation is `p ~ A K R (P-C)`, with compatible projective coordinate
mapping A, camera intrinsics K and pose R; nonlinear lens distortion must be
corrected or bounded separately. In the ideal exact Camera 4 coincidence case, a calibrated Camera 3
ray can instead be intersected with Camera 4's vertical reference plane, as
derived in the separate reading. Neither form recovers missing historical inputs.

For fixed known N and independently bounded residual errors e1,e2, the exact
coordinate half-width is `sum(abs(inverse(N)[i,j]) * ej)`. Once historically
justified inputs are supplied, the published estimate and zero must be tested
against the same feasible set. Zero **horizontal vector** is
feasible iff both residual intervals contain zero. Zero **north component**
only requires that the north-coordinate interval include zero; east-west
movement may still be required. These questions must not be conflated.

The [synthetic calculation](math01.json) deliberately uses arbitrary length
units u, **not WTC 7 metres**. It fixes true d=(0,2), n2=(1,0), and residual
errors of 1/5 u in both views, varying only the declared n1 direction:

| Synthetic n1 | Exact north interval (u) | Zero north feasible? | Zero horizontal vector feasible? |
|---|---|---|---|
|(3/5,4/5)|[1.6,2.4]|No|No|
|(4/5,3/5)|[1.4,2.6]|No|No|
|(12/13,5/13)|[1,3]|No|No|
|(99/101,20/101)|[0,4]|Yes|No|
|(9999/10001,200/10001)|[-18,22]|Yes|Yes|

This demonstrates the possible sensitivity to viewing geometry, not that the
real cameras were nearly parallel or had these errors. A sixth general matrix
case, exact zero-width intervals, singular/invalid-input controls and 18
synthetic pinhole projections test the algebra. The projections retain a
vertical-only point on its original edge and recover q through projective
depth; they are not a test of historical registration quality. The separately
frozen four-vertex oracle and root's read-only replay agree exactly on all six
intervals/zero tests and all 18 projections. [Validation](validation.md) records
the checks and limits.

## Identifiability and evidentiary consequence

The reduced qualitative constraints admit different positive lateral amounts:
motion along Camera 4's horizontal sightline stays on its reference image
line, while producing a Camera 3 departure when the views are independent.
Those qualitative statements alone do not select 11 m. Adding calibrated
ray positions/reference geometry could select a value; the missing step is
not forbidden by physics. We have not shown every such hypothetical amount
fits the full original images or the actual building dimensions.

The historical feasible set requires justified bounds for camera pose,
registration, corner/reference placements, geometric dimensions and the
same-time join. These pages do not supply that complete numerical set.
Therefore this audit neither reproduces [8,14] m as a supported interval nor
demonstrates whether zero northward displacement belongs to the same justified
set. Missing bounds are not unlimited bounds and do not make zero automatically
admissible. The source's positive directional evidence remains.

This qualifies earlier reliance on the figure against a literal, perfectly
vertical corner trajectory: cite it as **NIST's attributed geometric estimate**,
not a newly independently verified 11 m displacement. A roof-corner displacement
during descent is not a final debris map, the translation of the entire
structure, the timing of all hidden support failures, or a discriminator of
fire versus deliberate initiation by itself. No causal ordering changes.

The strongest objection is that NIST identifies a method and provides images;
failure to publish all intermediate numbers on these pages is not evidence
the estimate is wrong. That objection is valid. Conversely, citing the report
again cannot establish independent reproduction or validate its uncertainty.

## Next input that could change this result

The original Figure 5-206 worksheet or equivalent input table—exact reference
geometry, camera calibration, annotated source frames and transformations,
same-time Camera 4 constraint, and the meaning/derivation of +/- 3 m—would
permit a direct check. Independently calibrating native frames is an alternative
new measurement, not completed by this audit. A shared-input north-positive
interval would strengthen the result; a same-input feasible zero or a documented
geometry/timing error would weaken it. No new request or transmission is made.

This bounded audit addresses an earlier quoted premise, not all Luna-authored
work or the full charter. The [twelve-artifact Luna audit](../luna-reevaluation-2026-09-19/report.md)
and [causal-chain assessment](../causal-chain-synthesis/report.md) retain their
limits. All outputs stay in the investigation worktree; no legal or accepted
Sherlock/Faraday state, source, commit or remote is changed.
