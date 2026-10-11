# Independent scene observations for Clip 5

2026-10-03 local date; observation clocks are UTC on October 4. Frozen before
any Clip 6 image or exchange of stage3 candidate judgments. **No supported
scene/view counterpart to 5-141, 5-142 or 5-143 is recovered in these nine
samples.** Some architecture is compatible at a broad building level, but
the exposed corner ordering differs from the frozen reference views and
other diagnostic details are obscured or unexposed. This does not exclude a
shared building, location or unsampled scene.

## Continued reader scope and identities

I am the same `/root/stage2_visual` computational reader as in stage2.
[The earlier setup](../stage2/reader-setup.md), SHA-256
`25de136c23a31eeeea5efeb4825c02bedf8a9ec4d26518def0486504f939423a`,
continues to apply. I am not the original September 28 reference observer:
I use that observer's unchanged [textual reference freeze](../reader-references.md),
SHA-256 `4d8a6fdbab71439308db92a51e5d7123cc04f507a35e9c93b8a7c7b7642263eb`.
I reread that text and the complete protocol before this stage, without
reopening reference images or retuning landmarks. Main-control, charter,
protocol and reference hashes were rechecked unchanged at 01:23:09 UTC.
No root-stage3 observation or new judgment was read before this freeze.
Prior knowledge and earlier clip readings remain known; this is not blinded
or independent historical/camera evidence, expert review or human acceptance.

Root released run01 after reporting clean extraction and repeat checks. I
verified the selection/frame-manifest hashes and all nine run01 PNG hashes
before viewing, then checked source bytes/hash locally after viewing. I did
not independently rerun the decoder. Integrity of received bytes is not
historical authenticity.

| Artifact | Identity |
| --- | --- |
| Source | `raw/clip5-attempt1.avi`, 65881740 bytes; SHA-256 `8a7c04527e7807ec141c9da2af65d7a654493c462ecdff238764d3760196727f` |
| Selection | `preparation01/selection-targets.json`; SHA-256 `d2bbb409fc90d86e65b186dfaa06443f9c95bf72680adda61f8bb56b4409ea26` |
| Frame manifest | `run01/vince-clip5/frames.json`; SHA-256 `650859f6b7868ac5c43e993bd55d8dab4b23217a443f19d17b107db6fc5a6167` |
| Protocol | `../PROTOCOL.md`; SHA-256 `5dbaca2b2329db7bc85f67fc0995adf5fd15b8fe3fd0c4b0e50f445179dd35bc` |

The frame manifest preserves exact individual PNG/RGB hashes, PTS and native
metadata. Inventory: 529 frames, indices/PTS 0–528; time base
`333673/10000000` seconds per PTS unit. Native raster 720 by 480, SAR 8:9,
DV/yuv411p, interlaced with `top_field_first=0`. No aspect or field transform
was applied. Only descriptive adjacency/ordering is used, not metric slopes,
proportions or apparent motion. Encoded times are not historical event times.

## Complete display record

Pre-view clock **2026-10-04 01:33:14 UTC**; after-view clock
**2026-10-04 01:33:56 UTC**. Viewed the complete
`run01/vince-clip5/native/frame-000001.png` through `frame-000009.png`, exactly
once each and in that order, using original-detail `view_image`. All displays
succeeded. No repeat, crop, zoom, enhancement, reference reread, other frame,
Clip 6 image, audio or continuous playback was used.

| PNG suffix | Source index and PTS | Exact encoded seconds | Direct appearance observation |
| --- | ---: | --- | --- |
| 000001 | 0 | `0` | Street-level view with a person holding a microphone in the foreground, debris-like material across the ground, a vehicle and gridded facade behind. A large broadcast lower-third blocks the lower scene. The three frozen reference compositions are not exposed as complete views. |
| 000002 | 66 | `11011209/5000000` | Tight partial person/microphone view at right against a bright, veiled background. Local reference-facade geometry is not resolved. |
| 000003 | 132 | `11011209/2500000` | Wider street corridor: pale gridded building at left, different facade at right, bright veiling between them and a curved horizontal street fixture crossing above a large foreground debris-like pile. The pale left building's near corner leads into a narrower face to its right. |
| 000004 | 198 | `33033627/5000000` | Similar corridor with lower gridded sections of the left building, right-side facade, curved horizontal fixture and ground pile. Fine upper irregular-feature relationships are not jointly exposed. |
| 000005 | 264 | `11011209/1250000` | Upward view of a broad pale banded face to the left of a corner, with a dark adjoining region just right of it and bright veiling farther right. Two interrupted dark bands are visible in the lower part of the pale face; the news strip hides lower continuity. |
| 000006 | 330 | `11011209/1000000` | Same left-pale-face / corner / right-dark-region ordering. Paired dark bands and paler rows below remain visible; a separate facade is partly visible at the far right beyond veiling. |
| 000007 | 396 | `33033627/2500000` | Similar upward banded-facade scene; broad pale face remains left of the corner and veiled/dark adjoining region. No opposite-side sign stack or upper-right overhang relationship from 5-142 is exposed. |
| 000008 | 462 | `77078463/5000000` | Lower-framed portion of the same broad composition: dark upper bands toward the top-left, larger rectangular/grid-like subdivisions below, and a narrower right-hand side beside veiling. Broadcast strip obscures the lower connection among these features. |
| 000009 | 528 | `11011209/625000` | Person with microphone centered in front of street corridor, vehicle and ground debris-like material. The person and lower-third obscure much of the potential reference context. |

The microphone/channel markings and broadcast wording are recorded appearance,
not source authentication. A curved street fixture in indices 132/198 is
not, by itself, the distinctive sign assembly specified in the reference.
Describing a person with a microphone does not authenticate that person's
identity or the report's historical circumstances.

## Reference-specific tests

**5-141 — no supported same-view association; broad same-building possibility
remains unresolved.** The pair of interrupted dark strips above paler rows
in indices 264–396 resembles part of R141-A. But the exposed broad pale face
is left of its near corner, with a dark/veiled adjoining region to the right;
the frozen reference puts the broad pale face on the right and the veiled
side/other facade on the left. This is a real contrary cue to the specific
view, not merely an omitted cropped object. It can reflect another side,
corner or camera position; the screen cannot determine which. I do not
assume an undocumented mirror transform to force correspondence. The full
upper-pair / lower-interrupted-band / grid relation is also not jointly
established through the graphic. Generic paired bands are insufficient.

**5-142 — no supported reference-specific view; omitted features remain
unresolved.** The wider street samples show a curved fixture and architecture,
but not the frozen green direction-sign / BARCLAY / ONE WAY assembly left
of the target corner in combination with the upper-right projecting object.
Do not relabel the observed street fixture as that sign assembly without
the specific ordering. The upward samples have the opposite pale-face/corner
ordering just described; the person foreground samples are poor tests.
Missing signs through framing or obstruction are not whole-location
exclusions or proof that the signs are absent from the clip.

**5-143 — no supported local counterpart; fine context unresolved.** The
specific near-corner irregular upper group, adjoining pale patch/irregular
boundary, intervening pale interval and lower grid do not appear together
at discriminating detail. Some samples are too wide, some blocked by the
person or graphic. The pale-face side of the exposed upward corner also
differs from the frozen close reference. This weighs against identifying
those particular samples as that same view, but cannot exclude the same
building or an unviewed local neighborhood.

The strongest alternative to a true nonmatch is a different view or exposure
of a related building scene; that remains plausible and untested. A later
separately declared spatial/source test could resolve it. No new transform,
frame selection or criterion was introduced to make a match pass.

## Coverage and inference ceiling

Only indices **0, 66, 132, 198, 264, 330, 396, 462, 528** were viewed; **520**
inventory frames remain unviewed. Sampled non-recovery is not absence from
the full clip. The varied compositions are retained without inferring
continuous camera motion, shot boundaries or historical chronology from
sparse stills. Building identity, common recording and exact exposure remain
unestablished. No floor/pane state, fire area, temperature, duration, motion,
timing, support loss, cause ranking, human acceptance or legal promotion
follows from these observations.
