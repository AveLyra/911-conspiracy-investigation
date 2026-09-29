# Camera2: joining the paper to identifiable video features

2026-09-19. Research-only source/measurement-prerequisite report, not an expert
opinion, new acceleration estimate, legal fact or completed investigation.
Read with the [protocol](PROTOCOL.md), [declared extension and freeze deviation](ADDENDUM-01.md),
[independent visual review](independent-feature-review.md) and
[settings review](settings-review.md). Source evidence outranks these summaries.
The [result cross-review](result-review.md) independently checks the eight
comparison rows and the stated inference limits; [validation](validation.md)
records actual runs, review coverage, failures and the next bounded task.

## What changed

The paper's four labels can be tied to useful native-image neighborhoods, but
not to four authenticated, continuously trackable material points. In the two
fixed frames, the image-right outer corner and lower right roof-step foot have
identifiable candidates; the lower left step foot is identifiable only in the
later frame; the image-left corner remains smoke-obscured.

An important cross-unit distinction is now explicit: the earlier study's
**C2-T2 upper rooftop step corner is not the paper's WC lower roofline point**.
They must not be joined as the same target. This is not a newly discovered error
in the earlier trackability study: that study expressly defined the upper
endpoint, prohibited substitution of the lower endpoint, and did not claim it
was the paper's WC. The present source comparison prevents a future false join.

The paper's download ID matches the held Camera2 video. The initial settings
search did not identify its saved project, physical calibration or selected zero
frame. Two differently named public-kit projects were then selected for the
separate bounded alias inspection described below. Missing settings do not prove
the measurements wrong, and numerical table reproduction does not supply them.

## Source and observation coverage

Primary source: Chandler, Walter and Szamboti (2023), printed p. 13, Figure 4 of
the [held paper](../luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf).
PDF SHA-256: `cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394`.
The caption separately labels NE, EC, WC and NW, the north screen wall, and the
west penthouse. The preceding sentence says the east penthouse has already
collapsed in that image; Figure 4 therefore cannot by itself identify time zero.

Both reviewers viewed the complete page and both complete native 640 x 480
grayscale images: decoded index 6593 at `219767/999` seconds, and 6841 at
`684101/2997` seconds of the held file's encoded clock. The separate reviewer
also viewed the complete embedded Figure 4 raster, not an additional historical
image. No new video decode, enhancement, interpolation or registration was used.
These are two selected comparison frames, not an onset bracket or a frame-by-frame
motion record. Their hashes, luma hashes and exact PTS agree with the held
selection record in [verification run 01](verification01.json) and
[verification run 02](verification02.json).

## Feature correspondence and disagreement

Names in the first column are **the source's assignments**, not independent
authentication of compass direction, building member or physical attachment.

| Paper label | Candidate visible feature | f6593 | f6841 |
|---|---|---|---|
| NE, neon green | Image-left lower-roof corner neighborhood | Ambiguous region only | Ambiguous region only |
| EC, blue | Lower-left foot of surviving raised roof-outline step | Ambiguous region only | Projected-junction candidate near (352,151) |
| WC, orange | **Lower-right** foot of raised roof-outline step | Candidate near (424–425,154) | Candidate near (424–425,154) |
| NW, red | Outer image-right top/side outline corner | Candidate near (454–455,156) | Candidate near (454–455,156) |

Coordinates are native pixels, x right/y down. See the frozen
[root proposal](root-feature-proposal.json) and
[separate proposal](independent-feature-proposal.json) for subjective enclosing
boxes and reasons. Region midpoints are not substituted as measurements.

Both proposals classify the same five rows as candidate points and the same
three as regions; their detailed descriptive status strings differ. All eight
subjective boxes overlap.
For candidate pairs, reviewer minus root is (-1,0) pixels at NW, (+1,0) at WC,
and (0,0) at EC in f6841. These are descriptive comparisons, not accuracy scores,
confidence intervals, a consensus track or proof of no motion.

**Independence limitation:** the separate reviewer saved its proposal before
sending coordinates, without seeing root annotations or old numeric target
coordinates. Root had inspected the images and formed its estimates but had
not saved them when that message arrived. Thus the root freeze rule failed.
The agreement must not be counted as a blinded independent replication. The
unchanged files and [deviation record](ADDENDUM-01.md) preserve that failure;
automated validation cannot repair it. Neither reviewer is an independent
human or licensed structural/forensic expert.

### Join to the older two-target study

The [older frozen proposal](../camera2-target-trackability/targets-proposal.md)
defines T1 as the outer top/side corner at (454,156) and T2 as the **upper** step
endpoint at (424,144), explicitly not the lower junction. Figure 4's red NW
neighborhood is consistent with T1. Its orange WC is approximately ten image
pixels below T2 at this baseline; the separate light-blue west-penthouse marker
is on the upper step. This is a qualitative source-label comparison, not a
recovered original Tracker selection or authenticated structural identity.

Do not relabel old T2 coordinates as WC, carry its disappearance into WC's
coverage, or use the old two-target comparison as a four-roof-point reproduction.
The older uncertainty at f6946 and failure from f6961 onward remain preserved
in the [prior continuation report](../camera2-target-trackability/report.md).
Whether the lower junction itself stays usable later requires its own declared
continuity review; this two-frame study has not performed it.

## Clock, scale and alias coverage

The [settings review](settings-review.md) freshly checks the MOV hash, source
manifest, relevant saved settings and primary paper pages 10, 13, 15 and 50.
The paper's Camera2 public file ID matches the acquired MOV. Its 0.2-second
printed grid and east-penthouse zero do not give an exact source frame,
per-row PTS, Tracker timing method, metric scale or calibration endpoint pair.
The located Camera3 project's values cannot be transferred to Camera2.

The [bounded alias review](alias-review.md) then opened only the two preselected
public-kit TRZ members in memory. It found a saved Tracker project in each,
referencing `DistantViewWTC7.avi` and `TiltedCameraWTC7Clip.mp4` respectively.
Both saved clips use `stepsize=6`; they have distinct timing, origin, rotation,
scale and tape fields. The Tilted Camera project, for example, records
`video_framecount=476`, `stepcount=80`, `starttime=-2020.0`,
`delta_t=33.36666666666667`, equal `xscale/yscale=1.4841091539439202`, and an
assigned tape world length of `58.293` with `length_unit=m`. These are literal
saved fields, not newly validated physical values or an authenticated clock.
Their exact XML classes, other values, member hashes and search coverage are in
the [sanitized receipt](alias-receipt.json). Neither embedded media file has the
same bytes as the held Camera2 MOV; each archive also duplicates its own video
bytes under two member paths. Copies do not add corroboration.

After a prospectively declared extension, root viewed both complete saved
application thumbnails. The [thumbnail review](thumbnail-review.md) finds a
similar roof/foreground/background arrangement, making a related Camera2 clip
or processing history a plausible source lead, particularly for the Tilted
Camera project. It does **not** identify a common exposure, the paper's original
project or valid transferable settings. These 320 x 228 application screenshots
are not native frames; their tiny graph/table values were not read as data.
No embedded video was decoded and no source-coordinate mapping was recovered.

This changes the next step: test the held alternative clip/project before
concluding the desired settings are absent. The initial review's inventory-only
state remains frozen as dated search coverage, while this later review closes
only that limited archive-inspection gap.

## Evidentiary effect and next test

This advances feature identity and search coverage, not the mechanics of support
loss. The [published-table arithmetic](../multipoint-table-reproduction/report.md)
still supports gravity-scale motion in the source-assigned north-face data
under the declared fit choices. Its original positions, scale, time origin,
feature persistence and camera geometry have **not** thereby been independently
validated. This unit neither refutes that motion nor establishes it anew.

The strongest objection to overreading the present gap is straightforward:
the authors may have used usable features or valid calibration settings not
recovered in this search. Conversely, a colored ring on a blurred projected
junction is not sufficient to show that one material point was followed. Exact
saved Camera2 projects/point exports, source-frame associations and architectural
endpoint records would test those competing readings directly.

No causal-ranking change follows. The [integrated assessment](../causal-chain-synthesis/report.md)
remains conditional technical weight without an independently established
strict causal ordering, a demolition finding or equal odds. No original Luna
artifact is overwritten, no legal record is promoted, and no Sherlock/Faraday
case acceptance or activation occurs.

Next feasible WP2 work must retain separate tasks: (1) test the exact held Tilted
Camera clip/project against Camera2 under the source-identity protocol proposed
in the thumbnail review, including saved media/filter and point-export provenance;
(2) freeze a later-frame continuity protocol for the **lower** EC/WC
junctions and NE neighborhood rather than reuse T2; (3) establish a Camera2-only
metric calibration from identified same-plane endpoints and a dimensional source;
(4) bracket an explicitly defined east-penthouse appearance change in native
PTS, without choosing an offset to force agreement with the paper's onset labels.
None substitutes for the charter's human spot-check and consequential-measurement
review gates. The full investigation, including the late-fire lineage lane,
remains active and incomplete.
