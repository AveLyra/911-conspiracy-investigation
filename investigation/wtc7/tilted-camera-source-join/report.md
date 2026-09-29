# Tilted Camera footage, saved tracks and published positions

2026-09-19. Research-only follow-through to the [Luna reevaluation](../luna-reevaluation-2026-09-19/report.md)
and [Camera2 source-feature audit](../camera2-paper-frame-join/report.md).
The main-repository investigation charter controls; no legal record, accepted
Sherlock/Faraday finding or causal ranking is changed.

## Result

The archived Tilted Camera clip has strong image-content correspondence with
the held Camera2 recording. Its saved project contains **334 coordinate rows
across eight tracks**. Under the literal saved transform and a declared nominal
time join, **five of 48 tested series pairings pass every shared finite
position-change comparison within printing limits**. This is substantially more evidence
of a numerical/source relationship than a similar filename or thumbnail.

It is **not an exact reconstruction of the published measurement history**:
no pairing reproduces every absolute position; none of the shared finite
publication rows has compatible printed time under the saved assigned clock;
and the potential east-center series retains 11 displacement discrepancies.
Several passing series cover only part of the printed table. No positions,
times, scales, labels or selection windows were adjusted to improve agreement.

The strongest objection to treating the matches as independent physical
validation is shared ancestry: an edited derivative and related saved project
can reproduce published movements while inheriting the same marking, scale,
projection or clock errors. Conversely, the retained differences do not prove
fabrication or that the measured movements are physically wrong.

## Source and coverage

The preserved public `WTC-911-Motion-Lab.zip` contains the exact named
`The Kit/WTC7-Tilted Camera/WTC7TiltedCamera.trz`. Its two embedded copies of
`TiltedCameraWTC7Clip.mp4` are byte-identical. One was preserved to a fixed safe
name; the TRK was parsed only as inert XML. Author paths and arbitrary strings
were not exported, and Tracker was not launched.

| Source layer | SHA-256 |
|---|---|
| Parent ZIP | `c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189` |
| Named TRZ | `7eee39a3f9c802343204d7f3f595478ab4c5a7c6c54ca8e2928c46c7ed8b7552` |
| Embedded MP4 | `393d76f986d0771c5ec38352bf29470a81a3c685bb8a1c7ea565ceefa334843f` |
| Nested TRK, zero-based entry 4 | `babf332bd340c1e902870f14d4370eab4f3a54de388ce06c1ca85ae222b1b5da` |
| Held Camera2 MOV | `84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730` |
| Printed-table transcription | `a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc` |

The [protocol](PROTOCOL.md), [scene declaration](SCENE-ADDENDUM.md),
[table declaration](TABLE-ADDENDUM.md) and [actual visual coverage](visual-review.md)
separate planned tests, inspected images, arithmetic and interpretation.
Sources remain read-only in main; new research remains in the isolated
investigation worktree. No private-packet inspection, new production intake,
external retrieval, outreach, disclosure, source promotion, commit or push
was performed by this unit. The previously incorporated supplementary
production and the prior twelve-artifact Luna audit remain distinct work.

## Footage correspondence, not recovered exposure timing

The embedded clip decodes to **476 frames, 720×480**, YUV420P, with sample
aspect **131:144** and a 1/60000-second time base. Its PTS spacing is uniformly
2002 ticks. The held Camera2 file is **640×480**, 8,042 frames, with its own
irregular stored timestamps. These are current encoded-media properties, not
authenticated historical acquisition or analysis-engine clocks.

All 8,042 decoded Camera2 frame hashes were checked against the existing map;
the declared candidate interval is frames 6500–7200 inclusive. Root viewed
eight evenly indexed, complete native Tilted images and then exactly the nine
Camera2 frames selected by the declared scoring. It did not visually inspect
every candidate or annotate a new trajectory.

The calculation tested eight queries against all 701 candidates, using three
fixed width-only resampling branches and four predefined regions: **67,296
MAE/correlation pairs**. No rotation, translation, time shift, tone fit or
physical calibration was optimized. The shared scene and smoke/roof sequence
are directly recognizable in the displayed samples.

| Tilted frame | Camera2, NEAREST / BOX | Camera2, BILINEAR |
|---:|---:|---:|
| 0 | 6613 | 6613 |
| 67 | 6681 | 6681 |
| 135 | 6749 | 6748 |
| 203 | 6817 | 6817 |
| 271 | 6884 | 6884 |
| 339 | 6952 | 6952 |
| 407 | 7020 | 7020 |
| 475 | 7088 | 7088 |

Every full-scene minimum is interior to the candidate range and has one exact
minimum, but every runner-up is adjacent. The smallest score gap is only
0.0130 native luma units; it is not a confidence interval. The query-135
one-frame branch disagreement and region-specific alternatives remain
preserved. There is no single recovered, globally exact frame offset.

**Redundant-branch limitation:** NEAREST and BOX produce different full resized
images but identical retained scores on the every-fourth-pixel grid. A separate
synthetic diagnostic reproduces this loss of filter differences. They cannot
count as two independent robustness checks. All three branches also share
Pillow, the same input sources and the selected grid.

The [independent scene review](scene-independent-review.md) reproduces every
MAE exactly and every correlation within 4.60×10⁻¹³, all 96 complete rank arrays
and all 24 full-scene selections/runner-up/tie/boundary records. That is
independent arithmetic, not independent visual authentication or a recovered
editing/exposure history. Full same-code repeats are separately recorded in
[validation](validation.md).

## Literal project semantics

The [complete numeric export](project-export-review.md) retains all rows,
missing positions, original frame indices, field locators and key-frame flags.
The [tagged-source review](source-semantics-review.md) supplies the exact
conditional coordinate inverse, degree/radian convention, selected-frame
domain and clock behavior. Its historical runtime call chain and media-engine
identity are not completely reproduced.

The project assigns origin `(470.25,349)`, angle −2.5913472025433153 **degrees**
and equal scales 1.4841091539439202 pixels per assigned unit; its length label
is `m`. It declares fixed origin/angle/scale and no saved video filters. No
saved filter does not mean no baked-in crop, resize or other earlier processing.
The coordinate-axis angle is not an instruction to rotate the image again.

The selected frames are **0,6,…,474**: 80 steps, not all 476 video frames.
The saved playhead at 258 is not the time origin. The uniform-engine hypothesis
U uses `(-2020+n*33.36666666666667)/1000` seconds. The inspected controller's
endpoint stretch, applied to the **current** uniform PTS at loaded endpoints
0 and 474, equals U exactly. This does not authenticate the historical Xuggle
engine array or the paper's exported clock.

One track, PM05, contains 43 saved coordinate rows but only eight surviving
keys. Its **35 nonkey rows all precede the first surviving key**. They cannot
be explained as interpolation *between those surviving keys alone*. Import,
earlier marking/editing or other history remains unresolved. Key membership
itself can denote manual or automated marking, not independent human evidence.

## Published-table comparison: successes and retained failures

The table source is physical/printed page47 of the held Chandler/Walter/Szamboti
2023 PDF, already independently transcribed and reconciled in the preceding
unit. The present comparison retains all 334 saved rows and all **48** specified
X/Y-to-column pairings, including blanks and absent counterparts. It creates
no new velocity or acceleration fit.

For the declared **nearest 0.2-second nominal-grid join**, absolute positions
use ±0.005 assigned units. Changes from each pair's first shared finite row
use ±0.010, accounting for subtraction of two printed positions. A separate
1e−9 arithmetic tolerance changes no complete-pair decision. The baseline
row's zero change residual is automatic, not an extra validating observation.

| Pair with every available displacement row compatible | Rows | Original saved−printed baseline offset | Maximum change residual |
|---|---:|---:|---:|
| PM01 Y → `nw_y` | 70 | +1.665216 | 0.007706 |
| PM02 X → `ref_x` | 70 | +20.467219 | 0.009277 |
| PM02 Y → `ref_y` | 70 | +1.664765 | 0.008063 |
| PM06 Y → `ne_y` | 16 | +1.665972 | 0.006702 |
| PM08 Y → `wc_y` | 40 | +1.667644 | 0.004909 |

These are assigned units, not independently validated metres. PM01 and PM06
carry source labels NW Corner and NE Corner; other IDs are not renamed based
on closeness. None of the 48 pairings passes every **absolute** position test.
Three pairings have no shared finite values and no baseline; they are
unavailable comparisons, not passes. The remaining 40 do not pass every
displacement enclosure.

**PM05 Y → `ec_y` fails the all-row displacement test:** 32/43 rows are within
the enclosure, but the largest residual is **0.230452 assigned units**. All
eight surviving key rows pass; 11 of the 35 nonkey rows fail. Their frame
indices are 252,258,270,276,282,288,294,300,306,312,318. Keeping only the keys
would conceal the declared all-row failure; this study does not do so.

**Strict time fails independently of position agreement.** Among 1,512 shared
finite comparisons across the 48 pairings, U-minus-printed time spans about
−0.0190 to −0.0052 seconds; zero passes the printed ±0.005-second enclosure.
Those counts reuse source rows across pairings. Five later PM02 source rows
do fit their own nearest nominal times, but those times are outside this
publication table; therefore “none of all 334 rows fits its nominal time”
would be false. The reported correspondence concerns the coarse nominal join,
not simultaneous agreement of position and printed time.

The [all-row review](project-table-review.md) and
[independent computation](table-independent-review.md) retain complete outputs,
original offsets, missing states and precise clock residuals. A separate
determinant-inverse/rational-arithmetic implementation agrees numerically on all
668 coordinates, 1,512 absolute residuals, 1,512 displacement residuals and the
48 pair summaries within the declared 1e−9 bound. All 3,462 normalized row
states, memberships and rounding decisions agree exactly; tolerance is not
used to excuse categorical disagreements.
The largest reported displacement-residual difference is 8.19×10⁻¹⁴. Shared
source/export/calibration dependencies remain shared despite distinct code.

## What this changes—and does not

The earlier “project-to-footage/table relationship unverified” status is now
narrowed: common footage is strongly supported, and several saved trajectories
have a reproducible numerical relationship to the publication. The exact
saved version/offset/clock/edit-history join remains unresolved. Prior dated
negative-coverage statements and the earlier root annotation-freeze failure
remain preserved; they are not retrospectively rewritten as stronger checks.

This is evidence **about the measurement's source and processing chain**, not
new evidence identifying the initiating collapse mechanism. It strengthens
traceability of several published displacements, while exposing exact-input
and nonkey-history limitations. It neither establishes nor refutes NIST's
specific failure sequence, another fire pathway or deliberate support removal.
The current integrated assessment still establishes no strict probability
ordering; this unit does not allocate equal odds or infer intent from missing
provenance. The user-requested Luna reevaluation remains an evidence-based
review of located work, not a conclusion based on model identity.

## Next independent task and release boundaries

For further reconstruction of the published analysis, resolve the saved-versus-
published input relationship as far as held records allow: identify an original point/time
export or a specifically linked alternative project/version; preserve its
exact provenance and compare all rows under a new declaration without fitting
away offsets or discarding nonkeys. An unchanged or discrepant version is a
valid outcome. A source-cited explanation of a coordinate-origin change would
not by itself explain the clock or PM05 differences.

New independent measurements need not await a complete reconstruction of the
paper's editing history. Their physical validation separately needs source-raster endpoint/feature identity,
an independent dimensional reference, aspect/projection handling, uncertainty
and the charter's human/specialist review. The remaining fire-lineage and
structural workstreams are still open. Do not rerun this finished arithmetic
as a substitute for those dependencies, or claim the full goal is complete.

The evidence-audit and source-of-truth skills shaped the all-row tests, shared-
dependency qualifications and preservation of failed/missing states. Generic
software lessons are queued locally under existing Sherlock feedback IDs;
the archived destination remains unresolved. No new message or bridge transfer
was sent, and no local calculations were promoted to accepted scientific or
legal findings.
