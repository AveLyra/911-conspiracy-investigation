# Synthetic raster uncertainty and identifiability stage

2026-09-27. Declared before new fixture generation or outcomes. Prior-informed
method development, not blind historical validation. The previous goal turn
completed the OP-01/IX-01 source review. This stage advances the existing
connection-graph unit; it does not change its seven-pair scope or human gate.

## Authority, scope and acceptance

Main CHARTER, PROTOCOL, NUMERICAL-PROTOCOL, HUMAN-REVIEW-GATE and
REGISTRATION-STAGE remain controlling. Original source files, annotations,
registration, graph arithmetic and viewer are read-only. No historical image
input, ordinate extraction, solver, drawing access, new acquisition, matrix
save, legal promotion, external transfer or accepted-engine mutation.

Implement a small synthetic fixture generator and local color-support probe
in this directory, plus tests, reproducible outputs and independent review.
Acceptance requires all declared fixture combinations, all missed/spurious/
ambiguous results retained, code/input/runtime pins, two deterministic runs,
independent recomputation of a fixed sample and the analytic ambiguity tests.
It does not require every proposed allowance to cover every fixture. A failed
coverage bound is a result; do not tune thresholds or remove cases to pass.
No synthetic outcome calibrates historical uncertainty or clears human review.

## Fixed fixtures and transformations

Use a160x96 white RGB raster, with upper-left edge coordinates u,v. A line is
defined on16 <= u <144 by v =48 + m*(u-80) + p and vertical thickness w
(not perpendicular stroke width), with the lower band edge included and upper
edge excluded. Coverage is estimated using a4x4 grid of subpixel centers
(i+1/2)/4 on each axis, i=0..3, per cell, not exact analytic area coverage.
The sampled colors are
mixed with white by half-up integer rounding: (channel_sum+8)//16. Do not use
a plotting library's unrecorded stroke conventions.

Full Cartesian product: seven fixture colors; w in{1,3}; m in{0,1/2};
p in{0,1/2}; solid or dashed. Dashed support is8 source units on,8 off,
starting at u=16. Colors RGB: black(0,0,0), gold(204,153,0), blue(0,0,255),
red(255,0,0), green(0,128,0), cyan(0,180,180), purple(128,0,128).
These are invented stress-test colors, not measured historical ink values.
Exactly112 base fixtures; no physical load, displacement or energy labels.

Each is encoded losslessly as PNG and as JPEG at quality95/subsampling0,
75/0,75/2 and50/2:560 encoded/decoded cases. Record Pillow and JPEG library
versions, actual image settings and hashes. JPEG quality/subsampling settings
are stress conditions, not an estimate of the source's compression history.
Use JPEG optimize=False/progressive=False and PNG compress_level=6. No resize,
sharpening, fitted denoising or repeated recompression.

## Fixed local probe and reporting

For target color c, let q=255-c and for decoded RGB pixel let z=255-pixel.
With Q=sum(q_i^2), A=sum(z_i*q_i), admit a candidate pixel only if
5*A >= Q and every abs(z_i*Q-A*q_i) <=32*Q. This is a fixed20-percent
contrast threshold plus off-color tolerance, not a trained color classifier.
Use exact integer comparisons. The supplied target color is known only in
the synthetic fixture; this does not authenticate a historical curve identity.

Scan all rows for columns16..143. Retain every contiguous candidate row run.
No candidates = missing; multiple runs = ambiguous; exactly one run gives
the full native cell-edge y envelope [first,last+1]. Do not select the run
nearest ground truth, choose a centroid or silently span disconnected runs.
Expand that envelope by each fixed allowance{0,1,2,4} native pixels and test
coverage of the true centerline range over the complete column footprint
[x,x+1], using the infimum/supremum over the half-open visible column.
Report all four, without selecting a best allowance afterward.
Truth support is computed from the geometric fixture, not the extracted mask.

Separate columns with true visible line from dash gaps. For true-support
columns report missing/ambiguous/single-run and enclosure failures, retaining
the exact columns and bounds. For gap columns report every candidate,
including JPEG leakage; none establishes curve support. Store per-column
results and complete per-fixture summaries, not only averages. Include
envelope widths so larger bounds do not appear to improve precision.
No gap bridging, interpolation, style identification or cross-curve continuation
is admitted. Do not turn coverage fractions on this selected grid into
statistical confidence or a historical detection rate.

## Constructive non-identifiability controls

Construct three explicit pairs of different latent scenes with identical
visible base RGB arrays, then check equality after every declared codec:

1. Dashed line versus solid line hidden by white rectangles at the dash gaps.
2. Two same-color crossing lines with unchanged labels versus their identity
   assignments swapped after the crossing. Visible union is unchanged.
3. An absent line versus an arbitrary line completely covered by opaque white.

Specify separate latent scene descriptors, masking/draw order and resulting
visible bytes; independently render both, rather than comparing the same
named array to itself. Compare base RGB, encoded bytes and decoded RGB for
every codec. Codec equality preserves the constructed ambiguity; it is not
five independent ambiguity findings. Independent analytic
review must confirm that the constructions actually establish the claimed
limited ambiguity. These counterexamples show why local pixels alone cannot
universally identify dashes, continuation or absence. They do not assert
that any specific ambiguity occurs in the historical plot.

## Verification, review and remaining work

Controls cover specified subpixel sampling and rounding, blank background rejection,
color threshold boundaries, row components, empty/ambiguous support, full
cell envelopes, codec dimensions, no gap bridging, invalid inputs and
exclusive-create outputs. Missing or nonfinite input must fail, not clamp.
Reject a white target (Q=0), boolean/noninteger/out-of-range RGB channels and
malformed geometry. This isolated-line test does not test rejection of grid
lines, text or a mixed-color historical plot; no such classifier is claimed.
Actual structural comparison continues to use the already tested arithmetic;
this stage does not create a parallel scientific engine.

Root owns this declaration and final synthesis/navigation. A bounded producer
owns raster_uncertainty.py, test_raster_uncertainty.py and synthetic-run01/02.
A separate critic reviews method/code and checks fixed cases without importing
the producer's pixel predicate/component/envelope functions. Review all three
ambiguity pairs and all seven colors for w1,m1/2,p1/2,dashed, across five codecs.
Root reads the implementation and replays the tests and a complete output
comparison. Preserve failures and code corrections with their timing; no
post-result threshold changes. No historical pixels or new browser flow are
in scope, so visual QA concerns selected synthetic fixtures only.

Deliver a concise report of what these finite controls establish, which
claims they fail to establish, and the next exact historical measurement
prerequisites. Actual human axis/label and selected-curve spot-checks, native
linewidth/color characterization and explicit visible-support declarations
remain necessary. Synthetic success alone is not permission to trace.
