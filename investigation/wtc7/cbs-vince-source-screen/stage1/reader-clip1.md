# Independent Clip 1 scene screen - first freeze

2026-09-28. Provisional source identification only. Saved before opening any
Clip 2 candidate image and before receiving root's new candidate judgments.
No reference image was reopened for this stage; the one frozen reference
record controls all eight candidates. Prior familiarity is disclosed; this
is not a blinded or independently sourced historical validation.

## Input and execution boundary

Read the complete [protocol](../PROTOCOL.md) and my complete
[frozen reference descriptions](../reader-references.md), exit 0,
chunk `8ac8ab`. Their checked SHA-256 pins are respectively
`5dbaca2b2329db7bc85f67fc0995adf5fd15b8fe3fd0c4b0e50f445179dd35bc`
and `4d8a6fdbab71439308db92a51e5d7123cc04f507a35e9c93b8a7c7b7642263eb`.
Only `run01/vince-clip1/native/frame-000001.png` through `frame-000009.png`
were displayed. The [frame map](run01/vince-clip1/frames.json) is 4,141 bytes,
SHA-256 `d45c1642468dd498ae9a5f8a97643ee88bf0c991a1c85bfe306d69edf459b31c`.

Before views, a read-only standard-library check confirmed the nine exact
PNG names in ascending map order and their complete byte SHA-256 values
against that map, plus the frozen protocol/reference pins; exit 0,
chunk `d222f5`. Map metadata reports 720 x 480, SAR 8:9, interlaced frame
and bottom-field-first for every selected frame, time base 41709/1250000.
These are encoded relative presentation times, not authenticated event times.

Root reported completed strict preparation and two extraction runs, including
matching frame/PNG/RGB/PTS checks, and a separate artifact audit underway.
This reader did not rerun those pipelines, rehash the entire source AVI,
independently check the quantile selection against its complete frame
inventory or validate historical custody. Own narrow checks establish which
held PNGs were read, not the entire upstream source/admission chain.

Viewed all nine complete images once with original-detail `view_image`, in
ascending ordinal order, in batches 1-3, 4-6, 7-9. All displays succeeded;
no repeat, crop, enhancement, aspect correction or deinterlacing occurred.
SAR/interlace and visible texture limit metric comparisons; none were made.

## Frame identities and complete sample observations

Codes below are reference-specific scene dispositions, not physical-state
labels. **I** means the positively visible composition is incompatible with
the named reference's scene/view at this inspected sample. It does not mean
that the entire clip excludes that scene. **U** means mixed/obstructed detail
leaves correspondence unresolved. No frame in this screen reaches the
two-distinctive-relationships threshold for a supported association.

All files are under `run01/vince-clip1/native/`. Source index and PTS are
identical here as reported by the map; exact seconds are retained without
conversion to a wall clock.

| Ordinal | Source index / PTS | Exact seconds | Visible scene and decisive qualification | 5-141 | 5-142 | 5-143 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | Distant rectangular tower with its roof and a projecting mast/antenna visible, smoke-like plume to the left, open sky around its upper part, and a large broadcast lower-third obscuring the bottom. This is not the references' close near-corner/lower-facade composition. | I | I | I |
| 2 | 53 | 2210577/1250000 | Same clearly exposed tower-top/mast relationship and sky/plume composition. No recovered near-corner band/grid grouping or street-level foreground relationship from the references. Broadcast banner is not evidence of a source match. | I | I | I |
| 3 | 105 | 875889/250000 | Tower top and mast remain the dominant positive geometry; plume texture differs but is not a matching criterion. The distant roof-bearing view is incompatible with the specified close facade scenes. | I | I | I |
| 4 | 157 | 6548313/1250000 | The roof/mast above the long rectangular tower and broad sky remain visible. No reference-specific corner/upper-band/lower-grid ordering is resolved in this composition. | I | I | I |
| 5 | 209 | 8717181/1250000 | Continued distant tower-top composition with the same large lower-third foreground overlay. Cloud texture and network graphics do not supply either required spatial relation. | I | I | I |
| 6 | 261 | 10886049/1250000 | Same tower/mast and open-sky ordering; no counterpart to the reference 142 sign/corner/foreground assembly or reference 143 close upper-feature/lower-grid grouping. | I | I | I |
| 7 | 313 | 13054917/1250000 | Distant tower top remains positively identifiable as a scene element; left plume and broadcast banner persist. Differences in plume shape are not a scene association. | I | I | I |
| 8 | 365 | 3044757/250000 | The tower, roof/mast and sky geometry still dominate. The reference facades' local corner neighborhoods are not the visible subject. No supported scene association. | I | I | I |
| 9 | 417 | 17392653/1250000 | The tower layer remains visible, with additional faint/overlapping building-like forms across it. This looks transition/superposition-like, but the single selected raster cannot establish the mechanism or fully identify an additional scene. The tower component remains incompatible; the added/mixed component is unresolved, not confidently excluded. | U | U | U |

The frame 9 qualification is not erased to obtain a uniformly negative result.
It does not affirm a reference match: neither required pair of distinctive
relations can be recovered from its mixed appearance. It also does not prove
a cut, dissolve, physical event or recording chronology. No intervening frames
were opened to settle that ambiguity.

## Reference-specific assessment and strongest alternative

- **5-141:** The inspected tower-top views do not reproduce R141-A/B's
  near-corner ordered band groups and lower grid structure. The visible
  roof/mast/sky composition is affirmative different-scene evidence, not
  merely absence of a small cropped landmark. Frame 9 has an unresolved
  additional appearance layer. No same-building claim is independently
  established from this comparison.
- **5-142:** None of the selected frames supports the combined R142-A/B
  street-sign assembly, near corner and opposing foreground obstruction.
  Their absence alone would not suffice, but the positively visible distant
  tower-top view is not the reference composition. The lower-third covers
  part of the candidate scene, so no claim is made about hidden detail.
- **5-143:** The distinctive upper irregular-feature / pale interval /
  lower-grid arrangement beside the close corner is not recovered. The
  exposed tower-top geometry in samples 1-8 is an incompatible view rather
  than a small brightness or aspect-ratio difference. The mixed last sample
  is unresolved at finer scene identification.

The strongest remaining possibility is a reference-related scene in an
uninspected interval, or an unresolved component of the mixed last sample.
Nine spaced images do not examine every shot or prove whole-clip absence.
All open intervals between the listed encoded sample times remain visually
uninspected in this lane. This screen cannot rule out other material within
those intervals or identify its source chronology.

CBS-like branding and a news lower-third are visible content, not proof of
camera provenance, common original footage or the catalogue attribution.
No historical building/event identification is needed to reach the narrower
sampled-scene result and none is newly authenticated here.

## Checked PNG identity ledger

| Ordinal | Bytes | PNG SHA-256 |
| --- | --- | --- |
| 1 | 592225 | `45fde6114f4da275dc88c4343f4037886d4221bf4cafc623e0ac795a821f48f9` |
| 2 | 586650 | `f65ce0e43b2dbbaa73cf75b640883a7e6adf4c81921bd6ed1f8ce9c95160bda4` |
| 3 | 585557 | `6e27df079fe6046826ee3ef52e8f6cffe692ae26cd118338d07d198d8bdad89b` |
| 4 | 585481 | `388c3bcf0a5c65770e4f5f32f7db1759315606530d3498eb591a84ca59c05608` |
| 5 | 579904 | `3f6adcf28e32b0db03046ef0ad2e9d3a2cbe5351a56078992047706af582c7ca` |
| 6 | 586882 | `ec22fd8c45d9c84f4d22bc1b0958eda8fca3e0d06efffdf3adf032af6293c3b8` |
| 7 | 582796 | `f2149c343ed73b1d236553699a228bc9f33b66d85e6579eef612a3d7b6693861` |
| 8 | 583181 | `295ec6bd70c57ea0c67b5516546d54dcc864a04d969a9777f96c092ecacadb94` |
| 9 | 608656 | `9f070089cc0b8409d0738589ab823404ce2501f489713152355fd8f1525545d6` |

## First-freeze boundary

Nine inspected samples, nine successful displays, no failures or repeats.
No candidate association established within these selected frames; the
last-frame additional/mixed scene remains unresolved. This is finite sampled
non-recovery, not full-clip nonexistence, proof of the wrong catalogue family
or completion of the eight-candidate study. Stage 1 still requires Clip 2
and independent comparison after both readers freeze.

No audio, extra frame, video playback, crop, metric match score, glass-state
classification, physical measurement, source/exposure identity, event-clock
claim, cause ranking or human acceptance follows. Only this new reader note
was written; original sources, extracted frames and the reference freeze
remain unchanged. No peer candidate judgment was read before saving this
complete Clip 1 record.
