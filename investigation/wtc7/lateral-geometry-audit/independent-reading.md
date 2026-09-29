# Independent reading: northeast roof-corner lateral geometry

2026-09-20. Research-only, prior-informed computational reader. This note is
frozen before reading root's observations or exchanging interpretations.
It distinguishes NIST's reported measurements and calculation from my reading
of its pages. No new historical-frame measurement or numerical fit is made.

## Coverage, pins and visual acceptance

Main AGENTS.md, WORKFLOW.md, START-HERE.md and the complete CHARTER.md were read
in the immediately preceding task; their hashes were freshly rechecked unchanged
here. The entire new PROTOCOL.md and the source-of-truth-guardian,
evidence-falsification-auditor and PDF skills were read. These require preserving
raw sources, inspecting complete pages, and separating a stated estimate from
an independently reproduced interval. Only this exploratory note is written.

Source: `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf`, SHA-256
`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.
Protocol SHA-256:
`7f38d2e4f7b6295b238772aa91d53ad21c4afc3f7cfd7d8f2c1c95844f180417`.
`render01/receipt.json` SHA-256:
`d63eed304ab1cb1acf5bde5d50db57e2ac3e276e36090f6506522207ab2f365e`.

I waited for root's terminal admission. I then viewed each of the following
complete 150-dpi PNGs at original detail once, in four two-page calls. All eight
saved text extractions were read afterward as assistance, not as substitutes
for full-page viewing.

| Physical / printed page | Image | Complete-page result |
|---|---|---|
| 53 / 9 | `render01/p53.png` | Readable Chapter 2 / §2.1, complete text and footer. |
| 307 / 263 | `render01/p307.png` | Readable §5.7.2 and entire Fig. 5-183 camera map, labels, scale bar and caption. |
| 308 / 264 | `render01/p308.png` | Complete Figs. 5-184/185/186, three camera illustrations and captions. |
| 320 / 276 | `render01/p320.png` | Complete Fig. 5-202, caption and prose continuing onto p. 277. |
| 321 / 277 | `render01/p321.png` | Readable continuation, Fig. 5-203 and Camera 3 difference-image explanation. |
| 322 / 278 | `render01/p322.png` | Complete landscape Fig. 5-204: eight Camera 4 panels, annotation lines, times, caption and sideways footer/header. |
| 323 / 279 | `render01/p323.png` | Complete Fig. 5-205: nine Camera 3 difference panels, annotated edges, time labels and caption. |
| 324 / 280 | `render01/p324.png` | Complete construction paragraph and Fig. 5-206, red labels/lines, time label and caption. |

Coverage: eight unique pages, eight actual full-page image displays, no repeats,
no failed/truncated displays, no extra pages or extracted/enlarged figures.
No observed clipped prose, missing glyphs or missing figure/panel. Small source
annotations and blurred/compressed source imagery are not precise measurement
data merely because their page renders are complete. No coordinates were read
off pixels, no angles were measured, and no plan-map distance was extracted.

The receipt reports PyMuPDF rendering with zero saved warnings on all eight
pages, unchanged pinned inputs and completed rendering. Seven images are
1275 x 1650; the landscape p. 322 image is 1650 x 1275. These receipt claims
are distinguished from my visual acceptance. This uses the admitted MuPDF
route; it does not mean the prior Poppler environment was repaired.

Actual read-only checks: `cat` on the protocol, receipt and all eight text files;
`shasum -a 256` on main controls/charter, source PDF, protocol, receipt and all
eight PNGs. All commands returned 0; the source/protocol and PNG hashes matched
the declared receipt. I did not rerun rendering or validate its code independently.
No historical-media decode, listening, new source acquisition, source edit,
solver, numerical sweep, geometric fitting or acceptance-state change occurred.

Both readers share these published figures and prior task familiarity. Separate
notes are not blinded expertise, independent camera acquisition, or independent
source-family corroboration.

## What the source supplies

References below are printed pages, with physical-page mapping above. Values
are transcribed source values, not newly measured or converted quantities.

| Input / constraint | Supplied material | Important limit or missing component |
|---|---|---|
| World context and dimensions | P. 9: 47 stories; trapezoidal plan, approximately 329 ft longer side, 247 ft shorter side, 140 ft width, 610 ft height; adjacent street names. | Approximate overall dimensions, not surveyed roof-corner coordinates or their uncertainties. These four dimensions alone do not specify the trapezoid's offset/skew or camera-relative pose. Do not silently assume an isosceles plan or rigid rectangular facade. |
| Camera placement overview | Fig. 5-183, p. 263: Camera 3 marked on West Street; Camera 4 marked near West Broadway/Leonard; other camera locations and WTC 7 footprint shown. Map scale is 305 m (1000 ft). | Schematic map with no numerical Camera 3/4 coordinates, elevations, bearings, lens calibration or placement uncertainty supplied in these pages. Digitizing its scale would be a new measurement requiring a declared method. |
| Distant cameras | Same caption places Cameras 1 and 2 approximately 5-7 km away and uses arrows for their directions. | This is not the distance of Cameras 3 or 4 and must not be substituted for it. |
| Reference illustrations | P. 264, Figs. 5-184/185/186: pre-penthouse-descent Camera 1/2/3 views. Camera 2/3 intensities adjusted; Camera 3 floor labels added. | Views are published derivatives, not native camera files with a calibration or transformation record here. |
| Timing and early descent | Figs. 5-202 and 5-203, pp. 276-277: 8.1 s +/- 0.1 s and 9.0 s +/- 0.1 s after initial east-penthouse downward motion. At the latter time NIST reports nearly two stories of descent in 2.1 s after global-collapse start. | Those stated timing uncertainties belong to those figures. They are not automatically the error bounds of every later Camera 3/4 panel. Source timestamps, frame identifiers and cross-camera alignment residuals are not supplied here. |
| Deformation | P. 276 describes increasing east-edge rotation and a kink near Column 47. P. 277 describes differing northeast/northwest edge behavior. | A reported local corner displacement need not be whole-building translation or a rigid-body facade motion. Reference geometry must distinguish undeformed, initial and moving edges. |
| Camera 4 correction | Pp. 276-277: handheld camera moved and zoomed; two fixed foreground buildings were used to carry the original vertical edge line and a horizontal line into later frames. | No actual registration transforms, reference-point coordinates, zoom history, distortion model, residuals or parallax error bound is given. Fixed foreground buildings supply references, not automatic proof of exact distant-edge correction. |
| Camera 4 near-coincidence | P. 277: original and evolving northeast edge coincide within image resolution in the first five Fig. 5-204 panels, permitting vertical or camera-directed/receding motion rather than transverse motion. | Image-resolution tolerance is not quantified in pixels, angle or meters. A line-of-sight ambiguity is explicitly retained; coincidence is not zero total horizontal motion. |
| Camera 4 displayed sequence | Fig. 5-204, p. 278: 6.7, 7.7, 8.8, 9.7, 10.1, 10.6, 10.9, 11.4 s. Small white numbers in the first panel read 249 and 235. P. 277 identifies westward tilt in the next frame at 10.6 s. | The small numbers have no stated units or role in the construction in these pages; I do not adopt them as calibrated distances. The first-five coincidence statement reaches the 10.1 s panel, not an expressly displayed 10.3 s Camera 4 panel. |
| Camera 3 geometry and processing | P. 277: full building width, more oblique angle; earlier image-differencing technique applied; original and displaced edges marked with white lines. | The referenced differencing procedure is not fully specified in this page set. Input frames, registration, scaling, intensity operations and annotation errors are not supplied as executable data here. |
| Camera 3 direction interpretation | P. 277 reports both edges initially tilting north, continuing northeast-edge tilt, and northwest edge returning nearly to its original line. | This is positive reported directional evidence, not a newly reconstructed three-dimensional track. The report itself retains vertical/toward/away ambiguity for the northwest edge. |
| Camera 3 displayed sequence | Fig. 5-205, p. 279: 7.3, 7.8, 8.3, 8.8, 9.3, 9.8, 10.3, 10.8, 11.3 s, all referred to east-penthouse descent. | No uncertainty is printed for these individual times in the figure caption; no continuous-time trajectory is given. |
| Target frame and feature | P. 280, Fig. 5-206: heavily processed Camera 3 difference frame at 10.3 s; target is the top of the northeast corner of the descending roofline; descent described as about seven stories. | Not the penthouse tip, whole roof centroid, building center of mass, base trajectory or final debris boundary. Physical tracking/annotation identity must be checked in original data before a new measurement. |
| Reference-line construction | P. 280: two right-hand red lines trace west roofline and southwest edge; left red line is parallel to west-roofline annotation and passes through the descending northeast corner. | The named construction is useful but the line endpoints, coordinate system, selected original-versus-current reference geometry and full formula are not given. Parallel lines in an image are not by themselves a guarantee of parallel world lines under perspective. |
| Figure labels | Fig. 5-206 visibly labels the right annotation `91, -54 degrees` and the left `60`. | These literal marks are not accompanied by a complete legend giving the meaning, units and uncertainty of every number. Do not silently treat 60 as degrees, 91 as a length, or any of them as calibrated world viewing angles. |
| Stated calculation dependencies | P. 280 names an angle between lines, building dimensions, camera-building distance, and viewing angles of northeast/southwest corners. | Numerical Camera 3 distance, corner viewing angles, their definitions, equation and intermediate results are not supplied. The phrase about the angle is not an unambiguous executable specification of every annotation. |
| Published result and direction | P. 280: estimated displacement 11 m +/- 3 m from the original footprint; combining with Fig. 5-204 yields motion primarily due north. | Magnitude and direction come from a calculation plus a second-view interpretation. No uncertainty budget, confidence/coverage meaning, distribution, covariance or rounding rationale for +/- 3 m appears here. The magnitude is not stated as an independently measured exact north component. |

Two correspondence issues deserve preservation rather than quiet correction:

1. The target Camera 3 image is at 10.3 s; the shown Camera 4 sequence brackets
   that time with 10.1 s near-coincidence and 10.6 s westward tilt. Applying
   the former constraint exactly at 10.3 s requires a stated interpolation,
   uncertainty or same-time observation; it is not supplied by an identical
   printed time label. This does not show NIST lacked other intervening video
   frames, only that these selected pages do not publish that exact-time join.
2. P. 277 describes about ten stories of descent during the first-five-panel
   discussion; p. 280 describes about seven stories in the target construction.
   Both are approximate, and the feature/camera/timing basis needs clarification
   before using either as a metric height constraint. I do not resolve the
   difference by inventing floor heights or call it proof of a wrong estimate.

## Symbolic reconstruction: explicit assumptions, no numerical substitution

The pages do not publish NIST's equation. The following is an independently
written way to state the inverse-geometry problem, **not** a recovered NIST
algorithm or a validated fit. Let world coordinates be east, north, up. Let
`P(t)` be the target roof corner, `N0` a point on its original vertical edge,
and `Cj(t)` camera j's optical center. Camera orientation `Rj(t)`, intrinsic
matrix `Kj(t)` and any derivative-image mapping `Aj(t)` are parameters:

```text
homogeneous image point pj(t) ~ Aj(t) Kj(t) Rj(t) [P(t) - Cj(t)].

dNorth(t) = north_unit_vector . [P(t) - N0].
```

This ideal central-projection equation assumes lens distortion has been modeled
or bounded. Cropping, rescaling, roll/pan/zoom and registrations must be included
in the mappings or their uncertainty, not assumed absent. Image differencing
does not automatically supply geometric calibration. Corner and reference-edge
motion need not be governed by a single rigid facade model.

For a useful special case, suppose Camera 4's current image registration is
valid, its reference line is the projection of the original **world vertical**
northeast edge, and target coincidence holds at the same target time. Let
`q4` be a unit horizontal vector along the original camera-to-edge bearing,
and `n4` a horizontal normal to the vertical plane containing `C4` and that
original edge. Exact image-line coincidence implies:

```text
n4 . [P(t) - N0] = 0,
P_horizontal(t) = N0_horizontal + a q4.
```

It allows every along-plane amount `a`, including zero, before using Camera 3;
it does not alone establish zero northward motion. It also does not prove that
all such amounts fit Camera 3. For a calibrated Camera 3 target ray `v3`:

```text
P(t) = C3 + lambda v3,
lambda = n4 . (N0 - C3) / [n4 . v3],  provided n4 . v3 != 0.
```

This ray-plane intersection illustrates how a second, oblique view can recover
a point if the actual camera poses, reference plane, target ray and time join
are known. A small denominator creates sensitivity; no numerical conditioning
claim is made here. If Camera 4 only bounds coincidence, replace the exact
plane condition with a tolerance propagated from image-line residuals and pose
uncertainty. If coincidence no longer holds at the target time, a different
same-time bearing/point constraint is needed.

For an image line `ell4 = (a4,b4,c4)` and homogeneous pixel point `p4`, its
image-distance residual can be written:

```text
abs(ell4 . p4) / sqrt(a4^2 + b4^2) <= epsilon4.
```

Here `epsilon4` is an unknown required image tolerance, not a supplied number.
The line equation must use the same registered image coordinates as the point.
Equivalent line/point constraints could express Fig. 5-206's construction, but
its precise annotation semantics and camera parameters must first be supplied.
A weak-perspective/orthographic simplification could be investigated only with
a stated error justification; it is not silently substituted here.

## Same-standard test of the estimate and of zero

Let `Theta` contain all admissible camera, reference-geometry, annotation,
deformation and synchronization parameters, with their justified bounds.
The feasible displacement set is the set of `dNorth(P)` obtained from points
and parameters satisfying **both** views' constraints and the stated reference
geometry. The published estimate and `dNorth = 0` must be tested against that
same set, not one using fixed convenient parameters and the other using
unlimited uncertainty.

The pages name important dependencies but do not specify `Theta`, the measured
image constraints or their quantitative tolerances. Consequently I cannot
reproduce a conditional numerical interval or decide quantitatively whether
zero is excluded by those measurements. This is a constructive statement of
the missing inverse-problem inputs, not a constructed zero-motion history.
The Camera 4 constraint alone permits zero; the Camera 3 interpretation adds
positive directional evidence that must not be discarded when combining them.
An arbitrary zero-motion counterexample with unconstrained camera distortion
or facade behavior would not satisfy the task's equal-constraint requirement.

At face value NIST's stated estimate has a positive lower side, but adopting
its +/- 3 m as an independently verified total uncertainty would assume what
this task is testing. Conversely, inability to reconstruct it does not prove
that the quoted estimate is false, that zero fits the original images, or that
the corner fell exactly vertically. No new numerical range or probability is
assigned and no mathematical operations on plotted pixels were performed.

## Assessment and smallest decisive next input

Documentary grade A: NIST describes a two-view geometric argument, identifies
a target frame/construction and reports a local displacement with uncertainty.
The figures and prose contain positive directional evidence rather than a
bare unsupported number. This is not grade A physical validation by us.

Magnitude/uncertainty reproduction remains grade D in this page scope; the
reported direction retains conditional evidentiary support, not an independently
calibrated three-dimensional vector. Missing inputs here do not establish that
the investigation never possessed or used them. The result cannot be promoted
to whole-building translation, final footprint/debris containment, initiation,
intent or a causal ranking.

The most direct reproducibility input would be the original geometric worksheet
or equivalent equation/input table behind Fig. 5-206: exact reference-corner
coordinates, Camera 3/4 positions and orientation/calibration, annotated source
frame coordinates, derivative transformations, the same-time Camera 4 constraint,
and the derivation/meaning of +/- 3 m. These would permit an independent
conditional calculation with a declared sensitivity domain. A later remeasurement
from native frames is a different prospective task, not accomplished by this
page reading.

Evidence that the estimate remains north-positive across justified shared input
bounds would strengthen exclusion of zero. A same-input solution including zero,
or a documented error in a reference, timing join, projection or uncertainty
calculation, would weaken that exclusion. Neither result is supplied here.
Stop at the eight-page ledger and symbolic equations; no extra pages, geometry
extraction or numerical sensitivity sweep is authorized by this note.
