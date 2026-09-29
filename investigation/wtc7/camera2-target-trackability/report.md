# Camera 2: which visible corners remain trackable?

Research-only image observations and conditional calculations, September 12,
2026. This is not a physical trajectory, expert finding or cause determination.
The [charter](../CHARTER.md) remains controlling and incomplete.

## Result

The outer upper-right corner, **T1**, is consistently identifiable in both
annotation records through selected frame 7051. Its recorded displacement from
the baseline is **138 native pixels downward and 9 pixels image-left**, with
subjective displacement enclosures of **[131,145]** vertically and **[-16,-2]**
horizontally. Both analysts then lose it behind foreground/smoke overlap.
These image coordinates do not establish physical height, lateral drift, tilt,
acceleration or the force causing movement. In particular, an image-left
component can arise in the projection of a physical vertical line; it is not
itself evidence of building tilt.

The smaller raised-outline upper endpoint, **T2**, becomes ambiguous much
earlier. Its apparent earlier motion **is not a robustly reproduced ordering
result in this test**: the analysts' close coordinates give different answers
to the declared displacement criterion, and they disagree about whether one
late corner still continues T2's definition. None of the **15 eligible
between-target vertical-displacement enclosures excludes zero**. The record
therefore does not establish different displacement of the two targets under
these envelopes, much less their order of physical support failure.

This package does not test mechanism-discriminating predictions. It neither
validates nor falsifies NIST's specific sequence, and neither establishes nor
excludes deliberate support removal; no causal ranking changes. It limits how
strongly these particular sampled corners can be used to argue either
explanation. It does not negate other visible events, unsampled images or
measurements with different, independently justified observables.

## What was actually examined

The [frozen protocol](PROTOCOL.md), [accepted definitions](selection.json),
[root annotations](root-annotations.json) and
[separate annotations](annotator-annotations.json) preserve the choices before
comparison. Both computational analysts viewed **17 full native 640×480
grayscale images and 17 fixed coordinate panels each**. The panels are
nearest-neighbor viewing aids, not additional images or independent evidence.
No images were added for this calculation or post-release comparison.

The source is the preserved converted CBS/DV access copy, SHA-256
`84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730`.
The original recording/exposure clock and forensic chain are not authenticated
by this file hash. Each selected frame keeps its actual encoded PTS and
rational time; nominal frame rate is not substituted for those timestamps.

The fixed schedule is:

`6593, 6654, 6751, 6841, 6886, 6916, 6931, 6946, 6961, 6976, 6991, 7006, 7021, 7036, 7051, 7081, 7104`.

T1 is the outer top/side outline corner; T2 is the **upper**, not lower,
endpoint of the short raised-outline step. Their initial proposed coordinates
are only 30 pixels apart horizontally and 12 vertically. No third target was
forced from a poorly defined region. They do not sample the whole roof,
façade or building. No structural member, material point or cardinal direction
is authenticated merely by these appearance definitions.

The baselines were re-localized, but both analysts already knew the shared
proposal and earlier event imagery. This is separately frozen computational
annotation, **not human review, a clean holdout or independent source
corroboration**. The [release record](annotation-release.json) preserves the
two sets before comparison; neither was revised to force agreement.

## Agreement, disagreement and missing observations

All **34 matched localization labels** agree: 23 localized, one ambiguous and
ten unavailable per analyst. Of the 23 co-localized centers, 12 match exactly
and 11 differ by one pixel on one axis. All recorded rectangles overlap and
mutually contain the other analyst's center. These are comparisons of recorded
judgments, not an accuracy rate; shared image/definition errors can agree.

At **T2 frame 6946**, both centers are **(420,160)**, yet root regards the short
step as appearance-consistent and the separate analyst regards correspondence
as uncertain because it nearly merges with the lower outline. A broader
localization rectangle does not settle that identity question. Root's
displacement remains eligible in its own record; the separate coordinate is
retained but excluded from same-feature displacement.

Both analysts mark T2 frame 6961 ambiguous and the later selected T2 samples
unavailable. Both mark T1 frames 7081 and 7104 unavailable. Full native images
were checked, not just the crops. No nearby roofline, foreground corner or
smoke boundary was substituted. Unavailability is not proof of physical
destruction. Full per-row reasoning and a separate all-pair critique are in
the [annotation comparison review](annotation-comparison-review.md).

## What the displacement criterion does—and does not—say

The conservative y enclosure is
`[(y-h)-(y0+h0), (y+h)-(y0-h0)]`, using each analyst's own baseline.
A strictly positive lower bound meets the declared sampled-downward criterion;
contact with zero does not. Envelopes are subjective center-location bounds,
not confidence intervals. Comparing the very same baseline observation with
itself gives exactly zero, not an independently broadened error interval.

| Observable and analyst | First eligible selected downward interval | Important limit |
|---|---|---|
| T1, both | Frame 6946; [2,14] pixels | Preceding selected frame 6931 is [-4,8]. Neither result identifies first physical motion. |
| T2, root | Frame 6931; [1,15] pixels | Depends on root's baseline, center and envelope. |
| T2, separate | None | Frame 6931 is [0,12]; frame 6946 correspondence is uncertain; subsequent samples are unresolved. This is not evidence of no motion. |

Frame 6931 has source time **231034/999 seconds** and frame 6946
**694600/2997 seconds**. Their separation, **1498/2997 seconds**, describes two
selected file samples—not a measured physical lag or onset bracket.

At frame 6931, nominal T2-minus-T1 vertical displacement is 6 pixels for root
and 4 for the separate analyst. The corresponding enclosures are **[-7,19]**
and **[-8,16]**. Every eligible between-target enclosure includes zero, so a
positive interval for one target and a zero-containing interval for another
cannot be substituted for a positive *difference* between them. There are
15 computed target-pair rows and 19 explicitly not-both-eligible rows. Two of
the 15 are necessarily zero baseline comparisons; **13 concern later samples**.
Zero-containing enclosures do not establish equal displacement or symmetry.

## Conditional reference-map sensitivity

The [completed reference repair](../camera2-reference-repair/report.md) supplies
six frozen size/model alternatives per observation: 19- and 27-pixel reference
patches, each with translation, similarity and affine maps. No reference was
re-fitted or selected using these target results. The map convention is
`q=A p+b`; current centers and all four envelope corners are mapped by
`A^-1(q-b)`, separately at baseline and current time.

All **408 attempts** are retained: **229 computed conditional maps**, **41
stored-map rejections among eligible observations**, and **138 attempts with
ineligible annotation endpoints**. These categories are not percentages of
correct historical measurements. Source-fit flags remain visible even when
the annotation exclusion takes precedence. The known frame-7021 small-patch
affine cutoff-rounding rejection is preserved, not repaired after seeing
target motion.

Among the 229 computed attempts, mapped-minus-raw center displacement ranges
approximately **[-0.0913,+0.4321] pixels in x** and **[-0.1187,+0.2048] in y**;
the largest inverse matrix condition is about **1.00336**. Those are sensitivity
ranges among the selected maps, not bounds on true camera error. Every mapped
baseline target lies outside the convex hull of the reference points; 177
current centers also lie outside, while 52 lie inside. Spatial/depth transfer
and the source geometry therefore remain unvalidated.

The maps do **not** resolve the T2 disagreement: all six give root a first
selected positive interval at 6931, while none gives the separate analyst one.
For T1, all three 27-pixel alternatives first qualify at 6946, whereas the
19-pixel alternatives first qualify at 6961 because their maps are not admitted
at 6946. That shift is an **availability effect**, not measured later movement.
Missing map outputs are never replaced with an identity correction.

Mapped rectangles propagate the supplied localization bounds under a fixed
map. They omit reference-fit, feature-identity, optical, temporal and physical
calibration uncertainty. Small corrections and well-conditioned matrices do
not eliminate these omissions.

## Claim audit and next discriminating test

| Claim | Layer / strength within this package | What limits or would weaken it |
|---|---|---|
| Both records show substantial late downward T1 appearance displacement. | Observation plus calculation; A for the stored native-coordinate result. | Depends on appearance continuity, not authenticated material identity or metric geometry. A demonstrated point substitution would invalidate that trajectory interpretation. |
| Both independently establish earlier T2 motion. | Not established. | Baseline/envelope sensitivity, one correspondence disagreement and zero-containing differential enclosures. |
| Reference adjustment establishes a physical camera correction. | Unsupported here. | Extrapolation, unvalidated depth/optics, and omitted fit uncertainty. |
| These coordinates establish near-g acceleration, whole-building symmetry or a collapse cause. | Unsupported here. | Sparse two-point coverage, missing late observations, uncalibrated scale/projection/clock and no tested force model. |

The direct next discrimination is a **separately declared human or qualified
image/structural specialist review** of the original target definition and the
6931/6946/6961 transition, allowing “not identifiable” and preserving both
original records. No outreach is authorized or claimed. More automated
agreement checks cannot supply that independent judgment.

Before consequential acceleration or force claims, source-time provenance and
metric projection/scale must be justified independently of the desired motion
curve. A bounded audit of the existing source/geometry dependencies can proceed
without new acquisition; an arbitrary smooth fit or denser selection alone
cannot meet those requirements. The broader fire, mechanism, comparator and
documentary workstreams remain open. Current repository navigation records a
separate supplementary-production content audit and discrepancy investigation;
this video pass has not inspected those payloads or that audit and does not
extend their inspection clearance. Do not repeat a blanket assertion that the
files remain unavailable or unreviewed. Their completeness and scientific
validity require the separate source/dependency review.

## Reproduction and review status

Two historical executions, [run01](run01/receipt.json) and
[run02](run02/receipt.json), completed with observed exit 0 after fresh
worktree-bound [calculation controls](calc-controls03/receipt.json) and an
independent current-code synthetic pass. The producer and frozen annotations
were unchanged. The result contains 68 observation/displacement rows,
34 cross-analyst comparisons, 34 between-target rows, 408 map attempts and
four raw first-selected-sample summaries.

The calculation source is [analyze.py](analyze.py), SHA-256
`ac495eecb98845cf5a11cd6d27161cd051ea367cc7cb6a9e186b57329ef10ed6`.
The [independent historical verification](verification-historical02.json)
checks every result row against a separate exact-rational/closed-form oracle,
without importing the producer. Both runs have **12 listed products plus a
receipt: 13 byte-identical files each**. Their common result SHA-256 is
`96165709df9e6c876631c518e10844297f24d1356fbcee60b4566c30ce59ffaa`.
Independent review is computational, not a separate historical source or
qualified human assessment. [Validation](validation.md) records the exact
execution/review coverage and retained failures; [worktree continuation](WORKTREE-CONTINUATION.md)
records relocation and read-only source dependencies.
