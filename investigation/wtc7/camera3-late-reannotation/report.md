# Dense Camera 3 roofline re-annotation

Fresh image annotations preserve the earlier evidence for rapid, curved
descent at the right-hand roof corner. They do **not** establish that the
two previously tracked locations had different physical accelerations.
The second location lacks a reliably identified material marker. Beyond
separate-window uncertainty, a stronger joint test constructs a constant
image-y separation that satisfies both observers' placement ranges at every
mutually localized sample. This is a conditional mathematical alternative,
not proof of equal physical acceleration or a statistical tie.

The foreground-reference diagnostic also supplies useful positive evidence:
none of its integer matches shifted vertically in the selected frames.
Ordinary common vertical image translation is therefore not supported as
the explanation for the large descent. Exact camera stationarity, physical
calibration and the cause of support loss remain unestablished.[^1]

## New image evidence

Each of two computational observers viewed all 22 complete native images
and all 22 enlarged target crops: frame 258, then every saved mark from 288
through 348 in steps of three. This covers the entire nominal 10–14 s late
interval at its saved 0.2 s sampling, not every intervening video exposure.
The analysis clock remains conditional and its zero is not collapse onset.
All 442 decoded grayscale-frame hashes match the prior diagnostic map.
Hash agreement does not authenticate original exposure timing or remove
the source's previously documented decoding/cadence qualifications.[^2]

Root knew the preceding coarse screen and fitted summaries. The separate
observer had the new feature definitions but did not read the old points,
fits, root annotations or prior reports before freezing its own table.
This is independent annotation of the same access-copy images, not
independent source evidence, a blind historical holdout or human review.

**A, the right upper corner:** both observers could localize it in all 22
images, including the small final lip above foreground obstruction. Every
saved A y coordinate lies inside each observer's corresponding subjective
y envelope. All 22 pairs of new y envelopes overlap. This supports the
original corner association and its broad trajectory; it does not certify
subpixel precision or an unchanged three-dimensional material point.

**B, the upper rim at fixed image column 322:** this new operational sample
is deliberately a silhouette coordinate, not a presumed material track.
Neither observer identified a distinctive persistent material marker there.
Root supplied tentative placements at 342/345 and rejected 348; the separate
observer rejected all three. The 19 mutually localized y envelopes overlap.
Root's bounds contain 16 of 21 comparable saved y values; the separate
observer's contain 19 of 19. Root's five exclusions are frames 300, 309, 312, 315, 318.
The original track also varies in x, so these are proximity checks rather
than measurements of exactly the same point.[^3]

Smoke progressively obscures the left rim. Changing roof steps, a flatter
left outline and the increasingly small visible facade limit any assumption
of rigid motion. These appearances alone do not separate deformation,
perspective and recording effects. No ground impact, debris footprint,
internal column or support-failure time is visible in this selection.

![Final selected native frame: the right corner remains visible while the left rim is smoke-softened and foreground-obstructed](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera3-late-reannotation/views01/frame-0348.png)

## Position fits and placement sensitivity

Every declared 9-, 13- and 21-point late window is retained: 23 windows per
series, three series (A, B, A−B), and three datasets (two fresh observers plus
the saved points). Of 207 window records, 187 contain linear/quadratic fits
and 20 remain uncomputed because a fresh B localization is missing. No
missing point was filled, and no original point or fit was changed.

The quadratic acceleration is a linear weighted sum of the y placements.
For each observer's inclusive per-image interval, the calculation retains
the exact linear interval extrema, treating allowed placements as a
Cartesian product. These are **subjective placement envelopes**, not
confidence intervals, calibrated measurement errors or full physical
uncertainty. They exclude clock, scale, depth, feature-identity and model
errors. Saved points have no assigned error interval, not a zero-error one.

The following comparison uses the previously discussed 303–339 window
(nominal 11.0–13.4 s), not a newly selected best-gravity window. All 23 alternatives
remain in the machine-readable results.[^4]

| Dataset | A coefficient | B coefficient | A−B coefficient and placement envelope |
|---|---:|---:|---:|
| Fresh root | 32.018 | 29.296 | 2.722 [−12.962,18.407] |
| Fresh separate observer | 33.117 | 29.271 | 3.846 [−13.437,21.129] |
| Original saved positions | 32.906 | 28.550 | 4.356; uncertainty not assigned |

Units are native downward pixels per nominal second squared. Rounded
table limits are not outward-rounded strict bounds; use full retained
weights/intervals for exact computation. B and A−B here involve a sampled
outline, not two validated material accelerations.

All 20 computed root A−B envelopes and all 16 computed separate-observer
A−B envelopes contain zero, across the complete declared window set.
Neither observer has a complete 21-point B or A−B fit: root's three and
the separate observer's seven differential windows with missing placements
remain uncomputed. This is not a full late-interval differential measurement.
Thus the fresh placements do not establish a nonzero acceleration difference
under these envelopes. That does not establish equality, erase the original
numerical difference, or show that the subjective envelopes have complete
physical coverage. Windows overlap and do not multiply independent evidence.
Separate zero inclusion also does not, by itself, establish one jointly
feasible point sequence giving zero curvature in every overlapping window.

### Joint feasibility addresses the review's stronger question

A separately declared [post-result addendum](JOINT-ENVELOPE-ADDENDUM.md)
tests whether **one constant A−B image-y separation** can satisfy every
usable placement range simultaneously. This is stronger than inspecting
window-wise intervals. At each sample its permissible separation is
[A_low−B_high, A_high−B_low]; the intersection across samples determines
feasibility. An empty intersection would reject this countermodel within
the supplied boxes. No central annotation was changed.

All six declared scenarios are feasible:

| Placement constraints / coverage | Included paired samples | Feasible constant A−B interval, px |
|---|---:|---:|
| Root, all selected / late only | 21 / 20 | [−31,−30] / [−32,−30] |
| Separate observer, all selected / late only | 19 / 18 | [−32,−30] / [−33,−30] |
| Both observers simultaneously, all selected / late only | 19 / 18 | [−31,−30] / [−33,−30] |

For example, a constant −30.5 px separation has an explicit constructed
sequence inside **both** observers' original y boxes at all 19 mutually
localized samples, including 258. Each A placement and B placement in that
witness meets its corresponding bounds simultaneously. Root omits 348;
the separate and combined scenarios omit 342/345/348. No witness or measured
constraint is supplied at an omitted frame. The combined late interval is
wider than root's because it omits two additional frames; these are different
coverage sets, not evidence that intersecting the same boxes widens them.[^7]

This demonstrates that these placement envelopes can accommodate common
vertical displacement of the two defined image features on the covered
samples. It does not establish rigid physical motion, material identity,
continuous motion between samples, gravity, a probability, or that placement
error actually caused the old numerical difference. The witness is a
calculated countermodel, not a new set of observations. It imposes only
the declared y-box constraints and adds no physical dynamics.

For A alone in 303–339, line-versus-quadratic position RMSE is 7.978 versus
0.708 px for root and 8.231 versus 0.445 px for the separate observer. The marked
curvature survives re-annotation. Using only the earlier assigned scalar
scale, with **no axis rotation**, the A coefficients become 9.596 and 9.925
assigned m/s²; the equivalent saved y-only coefficient is 9.862. The fresh
placement envelopes become approximately 7.500–11.692 and 7.829–12.021.
These are positive conditional gravity-scale results, not newly calibrated
physical accelerations. They should not be compared as identical calculations
to the preceding saved-angle 9.874 value.[^5]

## Foreground references and common motion

Three preselected foreground texture neighborhoods were tested with 21- and
31-pixel patches over a fixed ±6-pixel search. All 132 numerical rows passed
the frozen contrast, correlation, competing-peak, uniqueness and boundary
screens. Complete 22,308 correlation scores remain available.

Every winning vertical offset was zero. The sole nonzero horizontal offset
was +1 px for the small streetlamp patch at 336; its larger-patch alternative
was zero. Thus 43 of 44 all-three reference groups have zero mean and residual
translation; the remaining group has mean (+1/3, 0) px. These are integer
texture-match results, not a subpixel camera-error bound.[^6]

Visual preflight disagreement remains material: root accepted the small
right-neighbor patch for scoring with a low-contrast warning; the separate
observer rejected its indistinct visual identity. Passing its numerical
screen does not override that rejection. The 31-pixel alternative was
provisionally accepted by both and independently yields zero offsets.

A purely common vertical shift cancels algebraically from same-frame A−B.
This is distinct from claiming that arbitrary camera motion cancels: B is
sampled at a fixed image column, so horizontal translation can select a
different location on a sloping rim. Rotation, perspective/depth, deformation
and changing silhouette identity are not removed by this subtraction.

## Interpretation and next discriminator

| Claim | Evidence layer / strength | Limitation or falsifier |
|---|---|---|
| The recognizable corner has pronounced late downward curvature in these images. | Observation plus calculation; B for shared-image trajectory support. | Incorrect corner correspondence, source transformation or materially different calibrated annotations. |
| Its late acceleration is gravity-scale under the saved scalar scale/nominal clock. | Conditional calculation; C for historical physical interpretation. | Independent clock/geometry calibration or defensible tracking changes. |
| The two locations had different physical accelerations. | D/underdetermined. | Fresh A−B placement envelopes contain zero; B material identity is unresolved. Better material tracks could resolve the issue. |
| Common integer vertical image translation explains the large descent. | Disfavored within this finite diagnostic. | Incorrect reference associations, untested camera transformations or source processing. Zero integer optima do not prove exact stationarity. |
| This establishes uniform whole-building free fall or the collapse mechanism. | E if asserted from this unit alone. | Neither the moving mass system, three-dimensional geometry nor the initiating causal chain was measured. |

The next motion discriminator is a separately declared **distinctive facade
feature** that remains visible with A, rather than another forced extension
of B through smoke. A dark upper-facade rectangular opening/band supplies a
candidate corner for a baseline identity check; it is a lead, not an already
accepted material marker. Its correspondence, visible interval, geometry and
source clock must be tested before using it as a second physical trajectory.
No new architectural or metric calibration was established in this unit.

The broader investigation remains active. These observations refine what
the terminal-motion evidence can support, but do not distinguish fire-based
initiation from deliberate removal or identify intent. Structural inputs,
other camera views and the other charter workstreams remain separate tests.

## Reproduction and source record

Root independently reproduced all 22,308 real reference scores and 2,366
synthetic scores with raw-moment arithmetic, rather than importing the
centered-product producer. Maximum correlation error was 4.45 × 10⁻16; all
reference gates and 44 translation groups agree. Fourteen full synthetic
reference fixtures include translations, intensity changes, flat/repeated
textures and boundary rejection. The preparation review independently
verified all 51 image file pins and all 28 enlarged crop interiors.

The [independent exact-rational verifier](verify_fits.py) and root's complete
[rerun](independent-fit-root01.json) reproduce all 207 record dispositions,
935 fitted coefficients, 4,070 residuals, 2,035 quadratic weights and 236
interval endpoints, plus all point comparisons and the retained positive
control calculations. Maximum acceleration difference is 3.26 × 10⁻12 px/s².
The [separate interpretation review](interpretation-review.md) required the
missing-full-window and joint-feasibility qualifications above; arithmetic
agreement does not validate the physical interpretation.
The joint addendum separately passes five full synthetic control groups
(seven control solutions). Root's different integer-inequality checker
verifies all six scenarios, 115 witness rows and 304 original-box membership
checks exactly. Overlapping scenarios reuse the same observations and do
not supply 115 independent samples.

Known limitations remain preserved: the factor 8 reference ruler ticks are
half a display pixel from replicated-block geometric centers; the factor 3
target rulers are exact. Some exceptional preparation failures lack durable
receipts, although this actual preparation completed with a valid receipt.
Two negative fit-control records retain reason labels rather than their
attempted numeric arrays. These are scoped method/provenance limitations,
not invented failures or grounds to rewrite frozen outputs.

[^1]: [Declared protocol](PROTOCOL.md), [reference preflight](reference-preflight.md), [reference results](reference01/scores.json) and [root's independent arithmetic](root-reference-verification01.json).

[^2]: [Image receipt](views01/receipt.json); preserved public [Camera3 WMV](</Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/outer/The Kit/WTC7-Camera 3/videos/Camera3.wmv>), SHA-256 48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722. [Earlier diagnostic map](/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-recording-comparison/wmv-diagnostic/run02/default-frames.json). No new acquisition or historical-clock authentication.

[^3]: Frozen [root observations](root-observations.md) and [numeric table](root-observations.json); frozen [separate observations](independent-observations.md) and [numeric table](independent-observations.json); [complete per-point comparison](analysis01/comparison.json).

[^4]: [All fits, residuals, weights and failed windows](analysis01/fits.json), [controls](analysis01/controls.json), [execution receipt](analysis01/receipt.json). Original [numeric-only point export](../camera3-conditional-trajectories/extraction01/points.json), SHA-256 f85e6f0ddbb55e3ef142a62e774237c69a59b9bbcbc31a92f93a37b9a9099df3; original private-path-bearing project was not reopened.

[^5]: Prior [conditional trajectory report](../camera3-conditional-trajectories/report.md) and [endpoint/calibration study](../camera3-calibration-endpoints/report.md). Assigned scalar scale 3.3366687576783383 px/m; neither it nor the nominal clock is independently recalibrated here.

[^6]: [Reference-method review](reference-method-review.md), [complete synthetic controls](reference01/controls.json), [run receipt](reference01/receipt.json). A computational review is not expert validation or human approval.

[^7]: [Joint exact-rational results and constructed witnesses](joint01/result.json), [controls](joint01/controls.json), [run receipt](joint01/receipt.json), [producer review](joint-review.md) and [root's independent original-box verification](joint-root-verification01.json). Combined constraints intersect both observers' boxes; they do not average or replace the frozen annotations.
