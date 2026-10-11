# Independent scene observations for Clip 4

2026-10-03. Frozen before exchanging new judgments with root. The fixed
samples provide a compatible, plausible scene/view lead for reference 5-141,
but this reader leaves the two-distinctive-relationship threshold unresolved:
the broadcast strip obscures a consequential lower-facade relationship.
References 5-142 and 5-143 are likewise not established from these samples.
This is not a whole-clip nonmatch or a finding about physical window state.

## Reader independence and pins

The replacement-reader limitations and immutable reference record are given
in [reader-setup.md](reader-setup.md). I used the original reader's frozen
descriptions, SHA-256
`4d8a6fdbab71439308db92a51e5d7123cc04f507a35e9c93b8a7c7b7642263eb`,
without reopening the reference images or altering those descriptions.
No root-stage2 observation or new root judgment was read. This is an
unblinded computational reading, not independent camera evidence, human
acceptance or specialist certification.

[My complete Clip 3 record](reader-clip3.md) was saved and hashed **before**
any Clip 4 view. Its frozen SHA-256 is
`7ced0d4337547dcd413d55a881f033c1e98d65ad767717cd9ea4382b8c581877`.
I checked the Clip 4 manifest and all nine PNG hashes before viewing them,
and checked the source byte count and SHA-256 after the views. Root had
reported strict extraction and repeat checks; I did not independently
rerun its decoder audit. Integrity relative to held bytes does not establish
original-camera custody.

| Artifact | Local identity |
| --- | --- |
| Source | `raw/clip4-attempt1.avi`, 25734188 bytes; SHA-256 `a4eb4934882428b15a156d2a7bfe1755e3dc00b37667f08a59c365645b3e07e8` |
| Selection | `preparation01/selection-targets.json`; SHA-256 `5ab837d58c8821f7f16117ec4ea2392f65411462273d3e2b868e1ddaf2e522b7` |
| Frame manifest | `run01/vince-clip4/frames.json`; SHA-256 `2d765327c06af5f2b5464e31ecacba356e1fa529d95c15b8e762e6bc856bc2c5` |
| Operative protocol | `../PROTOCOL.md`; SHA-256 `5dbaca2b2329db7bc85f67fc0995adf5fd15b8fe3fd0c4b0e50f445179dd35bc` |

The manifest preserves per-frame PNG/RGB hashes, source indices, PTS and
geometry. Selection metadata reports 206 frames, indices 0 through 205,
time base `166837/5000000` seconds per PTS unit, 720 by 480 native raster,
SAR 8:9 and DV/yuv411p. Selected frames are interlaced with
`top_field_first=0`. Native aspect and field-instant limitations prohibit
using apparent slopes, proportions or motion as decisive measurements.
Encoded times below are not authenticated event times.

## Display record and direct observations

After the Clip 3 freeze and before any Clip 4 image, the clock check was
**2026-10-03 22:49:15 UTC**. Viewed
`run01/vince-clip4/native/frame-000001.png` through `frame-000009.png`, exactly
once each, in ascending order, using original-detail `view_image`. All
displays succeeded. After-view clock: **2026-10-03 22:49:39 UTC**. The final
image has marked visual artifacts but it displayed successfully; it was
not retried or discarded. No crop, zoom, new transform, extra image, audio,
reference reread or continuous playback occurred. Combined stage2 count is
18 distinct candidate images, nine from each clip.

| PNG suffix | Source index and PTS | Exact encoded seconds | Direct appearance observation |
| --- | ---: | --- | --- |
| 000001 | 0 | `0` | Broad pale facade at right; near corner separates it from a dark, heavily veiled region at left. A separate light facade forms the far-left edge. Two dark, interrupted horizontal strips cross the right facade below a broad pale upper region; several lighter regular bands lie below. A large broadcast lower-third hides the next lower-facade neighborhood; a thin bottom strip shows larger dark/light rectangular portions. |
| 000002 | 26 | `2168881/2500000` | Same paired dark-strip / lower pale-band ordering. Far-left light facade and veiled adjoining region remain left of the target corner. The upper strip has an irregular-looking boundary; no material state is assigned. Lower-third still obscures the lower arrangement. |
| 000003 | 52 | `2168881/1250000` | Same wider upward facade composition, with two interrupted strips starting near the corner and extending right. Near-corner stacked pale rectangles and wider regular bands farther right are partly visible below them. Lower relation remains cut by the graphic. |
| 000004 | 77 | `12846449/5000000` | Paired upper dark strips, paler bands below and separate left facade are jointly visible. Dark lower rectangular portions can be seen below the lower-third near the bottom; continuity through the obscured area is not observable. |
| 000005 | 103 | `17184211/5000000` | Similar composition with less of the far-left facade exposed. Dense veiling occupies the left region; pair of interrupted strips and regular lower bands remain on the right-hand pale face. |
| 000006 | 129 | `21521973/5000000` | Far-left facade sliver is visible again. The ordering from left facade, through veiled adjoining region, to target corner and broad pale right face persists. No street-sign stack or upper-right projecting foreground object is exposed. |
| 000007 | 154 | `12846449/2500000` | Same pair of dark strips above lighter rows; lower-third masks the lower facade. Small bottom portions suggest larger rectangular subdivisions, but cannot establish the obscured intervening strip or its exact relation to them. |
| 000008 | 180 | `1501533/250000` | Same main ordered features and occlusion. No reversal of corner/face/left-facade ordering is apparent. Fine detail in veiling and bands is limited by low resolution and source artifacts. |
| 000009 | 205 | `6840317/1000000` | Severe horizontal multicolored lines, high-contrast banding, a displaced-looking top area and distorted lower-third obscure the frame. The underlying broad facade arrangement is still partly recognizable, but this sample cannot provide reliable additional fine-landmark discrimination. No diagnosis of the artifact's cause is made. |

Broadcast text and channel mark resemble the lower-third in Clip 3. That is
not evidence of a common camera, common exposure, event clock or original
custody. It also physically obscures the area needed for part of the fixed
comparison. The final frame's visual defect is preserved even though the
processing pipeline admitted it without a fatal diagnostic; successful
decoding does not mean clean historical image content.

## Reference-specific comparison and contrary tests

### Reference 5-141

**Compatible, plausible scene/view lead; threshold unresolved for this
reader.** R141-A is supported at descriptive resolution in indices 0 through
180: two separated interrupted/dark strips extend rightward from the same
near-corner neighborhood, above lighter regular bands. R141-C is also
compatible: the broad pale face is right of a veiled adjoining region, with
another light facade farther left. This ordering has more value in
combination than color or a channel label alone.

The limitation is discrimination, not an observed contradiction. The frozen
record cautions that the partly exposed separate left facade alone is weak.
Here the broadcast strip hides the lower interrupted band and much of the
large lower grid arrangement required by R141-B. Although bottom fragments
are compatible with larger rectangles, I cannot verify their uninterrupted
ordering through the graphic. Thus I do not treat the broad three-part city
view plus R141-A as a securely demonstrated pair of distinctive matches.
This is a conservative unresolved threshold judgment, not a finding that
the described relationships are absent or incompatible.

Contrary cues were tested where exposed: I did not see the pale face moved
to the opposite side of the actual near corner, a reversed left-facade
occlusion relation, or a reversal of the two-strip / pale-row ordering. But
those broad compatibilities cannot resolve the hidden lower neighborhood.
The source's blue cast and graphic differ from the report description;
neither is a geometric disproof. Index 205 is too artifact-degraded to close
the gap. No metric shape or slope comparison is made.

The strongest alternative is a similar upward view of the same banded
building, perhaps showing a different facade neighborhood or exposure.
A separately declared exact source/frame comparison or a genuinely exposed
lower arrangement would distinguish the stronger match claim. The
unresolved rating should not be rewritten as negative source evidence.

### Reference 5-142

**Unresolved; no supported reference-specific scene/view association.** The
candidate shows a broad pale face, left-side veiling and another facade, but
not the distinctive foreground sign assembly or upper-right projecting
obstruction. Their absence from the crop supplies no test of their true
street-scene ordering. The generic shared elements and possible larger
lower rectangles are insufficient. No whole-scene incompatibility is
claimed because the required foreground context is not exposed.

### Reference 5-143

**Unresolved as a source relationship; no supported local counterpart from
these nine samples.** The wider shot does not expose the reference's local
near-corner irregular upper feature/pale patch together with the immediately
lower regular grid at sufficient discriminating detail. The lower-third
hides much of the potentially relevant lower neighborhood. There is no
observed contradictory local ordering because the target local arrangement
is not jointly available to test. Clip 3's separate positive lead does not
transfer an exposure or local match to Clip 4.

## Coverage and conclusion ceiling

Viewed indices **0, 26, 52, 77, 103, 129, 154, 180, 205** only. The other
197 inventory frames and all intervening content remain unviewed in this
pass. No unsampled scene is declared absent. No additional frames were
selected after seeing the source content or its final visual artifacts.

Same-building compatibility is a lead, not newly authenticated attribution.
The compatible 5-141 view deserves later testing, but common underlying
recording and exact exposure are unestablished for all three references.
No glazing classification, fire area/temperature/duration, event timing,
motion, structural conclusion, causal ranking, human acceptance, expert
finding or legal-record promotion follows.
