# Independent scene observations for Clip 3

2026-10-03. Frozen before viewing any Clip 4 candidate and before exchanging
new judgments with root. The nine fixed samples support a provisional
scene/view counterpart to reference 5-143 under the frozen landmark rubric.
They do not establish common-recording or exact-exposure identity. No
glass-state or physical fire/collapse conclusion is made.

## Reader and evidence boundaries

I am the replacement computational reader identified in
[reader-setup.md](reader-setup.md), not the original author of the September 28
reference observations. This comparison reuses that author's complete
[unchanged reference record](../reader-references.md), SHA-256
`4d8a6fdbab71439308db92a51e5d7123cc04f507a35e9c93b8a7c7b7642263eb`.
I did not reopen the reference images, read root's stage2 observations, or
consult another reader's new judgments. Prior labels and project context are
known, so the reading is not blinded. It is not human or expert acceptance.

Root released admitted run01 products after reporting strict processing and
repeat checks. I separately read and verified the selection and frame-manifest
file hashes and all nine run01 PNG hashes before the first display. I also
checked the source byte count and SHA-256 locally after the nine views.
These integrity checks do not authenticate historical camera custody or
independently reproduce root's decoder audit.

| Artifact | Local identity |
| --- | --- |
| Source | `raw/clip3-attempt1.avi`, 23621148 bytes; SHA-256 `ced46b4c4318ef53c38eaf9485b76efa4d4d2c155b7194871a8479f0841a993d` |
| Selection | `preparation01/selection-targets.json`; SHA-256 `5ab837d58c8821f7f16117ec4ea2392f65411462273d3e2b868e1ddaf2e522b7` |
| Frame manifest | `run01/vince-clip3/frames.json`; SHA-256 `e854216730cab2613a15408742d840a2ceff0f71956362715d3d219e83f5129e` |
| Operative protocol | `../PROTOCOL.md`; SHA-256 `5dbaca2b2329db7bc85f67fc0995adf5fd15b8fe3fd0c4b0e50f445179dd35bc` |

The frame manifest pins each PNG and decoded RGB digest, exact PTS, source
index and geometry. Selection metadata reports 189 frames, indices 0 through
188, time base `333673/10000000` seconds per PTS unit, native raster 720 by
480, SAR 8:9, DV/yuv411p. All selected frames are interlaced with
`top_field_first=0`. No aspect correction or field separation was performed.
Use only robust ordering/adjacency; image slopes and proportions are not
decisive metrics. Encoded times below are not authenticated event times.

## Display record and sampled observations

Clock check before reading/displaying: **2026-10-03 22:47:43 UTC**. Viewed
`run01/vince-clip3/native/frame-000001.png` through `frame-000009.png`, exactly
once each, in that order, using `view_image` with original detail. All nine
displays succeeded. The after-view clock was **2026-10-03 22:48:08 UTC**.
No failed display, repeat, crop, zoom, transform, reference reread, extra
frame, other clip image or audio view occurred. The table follows the actual
view order, not an inferred historical sequence between different sources.

| PNG suffix | Source index and PTS | Exact encoded seconds | Direct appearance observation |
| --- | ---: | --- | --- |
| 000001 | 0 | `0` | Broad pale face at right, dark veiled area at left, irregular dark upper features and rectangular features lower down. A conspicuous sloping/roof-like outline and LIVE text appear in the upper area, alongside the facade appearance. The frame has a mixed/superposed-looking composition; whether that is an edit, another foreground/background object or other source artifact is unresolved. A large broadcast lower-third obscures much of the lower scene. Do not use the apparent roof-like outline as a decisive physical landmark. |
| 000002 | 24 | `1001019/1250000` | Close pale facade right of a corner; near-corner dark irregular upper region, adjoining pale strip/patch beneath an irregular dark boundary, another upper dark feature farther right. Large regular rectangular sections lie lower on the pale face. Orange/yellow luminosity and dark veiling are at left. Lower-third remains. |
| 000003 | 47 | `15682631/10000000` | Same ordered upper irregular group and lower regular rectangular features, with a more central near corner and broad luminous/veiled region at left. The pale facade interval separates the upper group from the lower rectangle. |
| 000004 | 71 | `23690783/10000000` | Tighter/different framing: much of the upper irregular group is cut by the top edge; one large lower rectangular area remains clearly on the pale-face side. A luminous region fills much of the left side. This sample alone provides a weaker test of the complete upper arrangement. |
| 000005 | 94 | `15682631/5000000` | Upper near-corner irregular dark group and adjoining pale patch/irregular boundary are again visible above a pale interval and broad regular rectangle. The rightmost upper feature is partly cut by the right edge. |
| 000006 | 118 | `19686707/5000000` | Same upper-group / pale-interval / lower-rectangle ordering relative to the corner. A pale small projecting-looking mark occurs at the lower margin of the upper near-corner region; no material identity is assigned. |
| 000007 | 141 | `47047893/10000000` | Near-corner upper dark region and pale-edged irregular feature remain above the regular rectangular section; another dark feature is cut at right. Left-side veiling/luminosity differs in appearance but is not used as an identifier. |
| 000008 | 165 | `11011209/2000000` | Upper irregular group remains adjacent to the same corner, above the pale interval and lower broad rectangular section. Broadcast strip continues to cover lower facade; a further rectangular part is visible below the strip at the bottom edge. |
| 000009 | 188 | `15682631/2500000` | Same local ordering with upper features lower in this framing; the broad lower rectangle is partly behind the lower-third. Another rectangular portion reaches the bottom edge. The complete wider street context is not exposed. |

The samples contain a lower-third reading, in substance, “World Trade Center
attacked and destroyed,” plus a channel mark. These are observations of
broadcast text, not independently adopted factual claims or source identity
proof. The first frame's appearance is retained as an ambiguity, not silently
excluded and not treated as a separate authenticated scene.

## Reference-specific assessment and countercues

### Reference 5-143

**Provisional supported scene/view counterpart**, chiefly indices 24, 47,
94, 118, 141, 165 and 188. Two distinct frozen relationships are supported:

1. **R143-A:** Immediately to the right of the corner, a broad irregular dark
   upper region is followed by a pale patch/strip beneath an irregular dark
   boundary within a more regular outer frame; another upper dark feature
   occurs farther right and is partly clipped. This is a specific ordered
   local arrangement, not merely dark windows or a pale building.
2. **R143-B:** That upper group is above an uninterrupted-looking pale facade
   interval, followed lower down by a broad regular rectangular grid-like
   section. A further rectangular portion is cut at the bottom in several
   samples. The lower-third hides part of that continuation, but the upper
   group, intervening interval and first lower rectangle are jointly exposed.

The corner has the pale facade/features to its right and veiling/luminosity
to its left, consistent with R143-C. That context reinforces the comparison
but is not counted as a second independent restatement of R143-A.

Contrary-cue check: I did not observe a reversal of the upper-group / interval
/ lower-rectangle order or a placement of those features on the opposing
side of the corner in the discriminating samples. The actual lower-third
and first-frame mixed appearance differ from the reference record; they
limit direct exposure comparison, not by themselves the local scene/view
association. Index 71 omits much of the upper group and is weaker evidence,
not a contradictory full-view test. Light, veiling, compression, interlacing,
native aspect and the use of a textual reference record limit fine-shape
certainty. No equality of small boundaries or pixels is asserted.

The strongest alternative is another exposure/view of the same local facade
arrangement. That alternative is fully compatible with this bounded result:
the test does not distinguish it from a common underlying recording. A
later separately declared exact frame/field/source-transform comparison
could test that stronger claim. This result would weaken if such a check
found that the apparently corresponding local arrangements occupy different
facade neighborhoods or that decisive shapes were compositing artifacts.

### Reference 5-141

**No supported 5-141 scene/view association in these nine samples; unresolved
as a source relationship.** The candidate is compatible at a broad
corner/pale-face level, but the reference's upper pair of separated irregular
horizontal strips, intervening pale bands and lower interrupted band are not
jointly displayed as that larger arrangement. The candidate close-up and
lower-third leave insufficient context to test those distinctive relations.
Missing cropped bands or the far-left facade sliver are not proof of a
nonmatch. The 5-143 association does not establish 5-141 exposure or identity.

### Reference 5-142

**No supported 5-142 scene/view association in these nine samples; unresolved
as a source relationship.** The distinctive foreground sign stack to the left
of the corner and projecting upper-right obstruction are not exposed. A
close facade composition cannot test their relative ordering or absence from
the larger street scene. Generic corner/rectangle compatibility and bright
color cannot meet the two-distinctive-relationship rule. The absence of
street furniture from this close crop is not a conclusive incompatibility.

## Coverage and permitted conclusion

Nine distinct samples cover only indices **0, 24, 47, 71, 94, 118, 141, 165,
188** out of 189 inventory frames. The other 180 frames and all intervening
content were not viewed. There was no continuous playback or shot detection.
This is a positive local scene/view lead for 5-143, not a full-clip source
audit or proof that the other references are absent from Clip 3.

Same-building compatibility is implicit in the local correspondence but is
not a newly authenticated building attribution. Common recording and exact
exposure remain unestablished. No event clock, window/glass classification,
temperature, fire area or duration, movement, acceleration, support-loss
mechanism, causal ranking, accepted finding or legal promotion follows.
