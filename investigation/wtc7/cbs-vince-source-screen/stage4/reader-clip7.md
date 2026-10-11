# Independent scene observations for Clip 7

2026-10-04 UTC, October 3 locally. Frozen before any Clip 8 image and before
exchanging stage4 judgments. **The fixed samples support a bounded scene/view
counterpart to Figure 5-142, principally at index 564.** They do not establish
a common original recording or exact exposure. The 5-141 and 5-143 comparisons
remain unresolved. No physical glazing or fire conclusion is made.

## Reader scope and evidence pins

The same replacement reader `/root/stage2_visual` continues under the
[stage2 setup](../stage2/reader-setup.md), SHA-256
`25de136c23a31eeeea5efeb4825c02bedf8a9ec4d26518def0486504f939423a`.
I use the original observer's unchanged textual
[reference freeze](../reader-references.md), SHA-256
`4d8a6fdbab71439308db92a51e5d7123cc04f507a35e9c93b8a7c7b7642263eb`.
At 02:00:46 UTC I rechecked the main/control, charter, protocol/reference
and setup hashes and reread the complete protocol, reference descriptions
and completed stage3 report. No reference image was reopened or landmark
retuned. Prior labels, source knowledge and earlier outcomes are known;
this is not blinding, an independent camera or actual-human/expert review.
Textual-reference dependence is not a new reference-pixel inspection.

Root released run01 after reporting clean diagnostics and repeat checks.
Before viewing, I verified selection/sampling/frame-manifest hashes and
all nine Clip 7 run01 PNG hashes. After viewing I checked source bytes/hash.
These are local integrity checks, not original-camera authentication or an
independent rerun of root's decoder audit. No root-stage4 observations or
new judgments were read before this file froze.

| Artifact | Identity |
| --- | --- |
| Source | `raw/clip7-attempt1.avi`, 140334936 bytes; SHA-256 `a2aefd37d58a7f2e7cea73c8d06114ec941e2178d1a4ddc9419649dd9936487b` |
| Selection | `preparation01/selection-targets.json`; SHA-256 `9d676f014c4b866129eeb77df2a6be519326dd8dbe08a54ac8026864514f4e72` |
| Sampling manifest | `preparation01/sampling-manifest.json`; SHA-256 `8cfc8ac6ce67b0c1ca15c874b3663a638585798bb3aba8461bfe2b5c4fbc4fd6` |
| Frame manifest | `run01/vince-clip7/frames.json`; SHA-256 `15a0d0ae2b7d0f650688abf90bd474f7f1dafdb8f6a595a3ad9e046b980d9e0f` |
| Protocol | `../PROTOCOL.md`; SHA-256 `5dbaca2b2329db7bc85f67fc0995adf5fd15b8fe3fd0c4b0e50f445179dd35bc` |

The frame manifest pins each PNG/RGB hash, source index, PTS and native
metadata. Inventory: 1128 frames, indices/PTS 0–1127, time base
`333673/10000000` seconds per PTS unit. Stored raster 720 by 480, SAR 8:9,
interlaced with `top_field_first=0`; no aspect correction or field transform.
Encoded time is not authenticated historical time. Ordering and occlusion
are compared, not metric shape, proportions or apparent movement.

## Complete display record

Pre-view clock: **2026-10-04 02:07:29 UTC**. Viewed complete
`run01/vince-clip7/native/frame-000001.png` through `frame-000009.png`, exactly
once each in order, using original-detail `view_image`. All nine displayed
successfully. After-view clock: **2026-10-04 02:08:01 UTC**. No repeat, crop,
zoom, enhancement, extra frame, Clip 8 image, reference reread, audio or
continuous playback occurred.

| PNG suffix | Source index and PTS | Exact encoded seconds | Direct appearance observation |
| --- | ---: | --- | --- |
| 000001 | 0 | `0` | Soft/horizontally lined street-level image with a low angular vehicle-like form and scattered material before a pale lower facade. The broadcast lower-third masks much of the lower scene. No reference-specific upper arrangement is resolved. |
| 000002 | 141 | `47047893/10000000` | Person and microphone-like object at right, vehicles and facade base behind, with a traffic-signal housing on a pole at left and a veiled/luminous gap between buildings. The foreground person masks part of the relevant architecture. |
| 000003 | 282 | `47047893/5000000` | Tight bright yellow/veiled region beside a dark architectural area, with a cropped sign at upper right. Too little stable target geometry is exposed for a complete scene comparison. |
| 000004 | 423 | `141143679/10000000` | Street-sign assembly at upper left: BARCLAY-looking street panel above a right-pointing ONE WAY panel; a signal housing is lower on the pole. Pale facade at right contains large rectangular grid-like areas; a dark vertical corner/gap and veiling separate it from the left foreground/neighbor. Higher direction sign and upper-right overhang are not jointly exposed in this crop. |
| 000005 | 564 | `47047893/2500000` | Wide upward scene: green direction-sign panel at left above street-name panel and a partly visible lower arrow sign, with smaller upper sign/support objects and another facade farther left. Main pale facade is right of a veiled corner/gap. A dark projecting object overlaps from the upper right. An irregular dark horizontal strip lies above smaller stacked near-corner rectangles and wider grid-like sections farther right. Banner masks some lowest detail. |
| 000006 | 705 | `47047893/2000000` | Person with light face covering and microphone centered against street/base facade, vehicles and pole. Most diagnostic upper facade/sign-overhang arrangement is out of frame; lower-third persists. |
| 000007 | 846 | `141143679/5000000` | Wider person/street view with pole left, vehicle right, facade base and scattered ground material. It does not jointly expose the reference's distinctive upper scene relationships. |
| 000008 | 987 | `329335251/10000000` | Closer foreground person/microphone view. Signal housing and bright gap behind, vehicle/base facade at right; person and banner obscure target context. |
| 000009 | 1127 | `376049471/10000000` | Mixed-looking composition: foreground person coexists with a red emergency-vehicle-like form and another street/building image, with LIVE text at upper left. Fine geometry is not reliable for a new match. A transition or source artifact is possible, but its cause is not established. |

Sign words are supplementary scene context, not the sole basis of the
association. No person's identity is authenticated from source labels or
appearance. Broadcast text/channel marks, bright color and veiling are not
camera, time or physical-fire authentication. Ground material is not assigned
to a particular historical event or mechanism.

## Reference-specific result and contrary tests

**5-142 — supported bounded scene/view association, strongest at index 564.**
At least two distinctive frozen relationships are jointly exposed there:

1. **R142-B:** The sign-support/left-facade foreground occupies the left side,
   while a separate dark projecting object overlaps the pale building from
   the upper right. The main near corner and veiled gap lie between these
   opposed foreground constraints. This is more specific than a generic
   pale facade or single sign.
2. **R142-C:** On the pale face right of that corner, the irregular horizontal
   strip lies above the larger grid-like regions, with smaller stacked
   rectangles nearest the corner and wider gridded sections farther right.
   Its placement relative to the street foreground supplies a second
   architectural relationship, not a paraphrase of the first.

R142-A is also supported in part: the green panel is above the street-name
panel on the left support, with the lower arrow sign partly clipped/covered.
Index 423 exposes the street-name / ONE WAY ordering more clearly but omits
the higher panel/overhang; it is contextual support, not an assertion that
the full sign stack is equally legible in one exact exposure. Small upper
support/sign objects before the left background facade are compatible with
R142-D. The B/C pair, not text recognition or plume color, carries the match.

Contrary-cue check: in index 564 the sign assembly, corner/gap and right-hand
projecting object are not reversed or placed in incompatible foreground
order. The irregular-strip / lower-grid ordering is also compatible where
visible. The broadcast strip hides lowest features; interlacing, native
aspect and report processing limit fine geometry. The late mixed-looking
frame is not used to strengthen the match. A different exposure or camera
from a similar street position remains an alternative. A separately declared
exact-frame/field/source-transform test could distinguish that from a common
underlying recording; this screen cannot. A demonstrated incompatible
foreground overlap or different facade neighborhood would weaken the lead.

**5-141 — partial broad compatibility, unresolved association.** Index 564
has compatible pale-right / veiled-left / separate-left-building ordering
and a lower irregular strip/grid neighborhood, but the complete paired
upper strips and intervening/lower grouping are not securely exposed at
the top of this sample. Other samples mostly show lower street context.
Do not fill clipped upper geometry from the 5-142 association or from earlier
clips. No whole-building or whole-clip nonmatch is claimed.

**5-143 — compatible local neighborhood at coarse scale, unresolved fine
association.** Index 564 shows a near-corner irregular strip above rectangles,
but the distinctive pale patch/irregular-boundary arrangement within the
upper local group is too small/soft to confirm R143-A. The broader street
view cannot automatically establish the close reference's exact local
relations or exposure. Other samples omit, obscure or impair that detail.
No absence claim is made about the actual building or unviewed intervals.

## Coverage and conclusion ceiling

Viewed only **0, 141, 282, 423, 564, 705, 846, 987, 1127** of 1128 frames;
**1119 remain unviewed**. No continuous playback, shot detection or extra
selection followed the positive sample. The changing sparse compositions
do not independently establish camera movement, edit timing or historical
chronology. The positive 5-142 result remains a scene/view inference, not
exact exposure, common recording, custody or an independent new building
identification. No floor/glass state, temperature, fire extent/duration,
kinematics, support loss, cause, accepted finding or legal promotion follows.
