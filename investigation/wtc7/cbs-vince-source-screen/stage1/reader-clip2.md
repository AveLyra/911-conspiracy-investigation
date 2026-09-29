# Independent Clip 2 scene screen - first freeze

2026-09-28. Provisional source matching only. [Clip 1](reader-clip1.md)
was saved before the first Clip 2 view: 9,216 bytes, SHA-256
`0eb7a642c38ca58dbcb7de2599a7f49dcf213d80b4f5ee24f53304697f5ce2cc`.
No peer candidate judgments were read. The unchanged [protocol](../PROTOCOL.md)
and [reference freeze](../reader-references.md) govern this record; no
reference image was reopened or cue retuned.

## Actual coverage and checks

Before views, checked the nine exact ascending PNG paths and full file hashes
against [frames.json](run01/vince-clip2/frames.json), exit 0, chunk `d57d02`.
The frame map is 4,175 bytes, SHA-256
`055b45aabca64b9ba784b44b0b2cf724e55041fdf9f2dd00bab6155d389bc651`.
Its records report 720 x 480, SAR 8:9, interlaced/bottom-field-first throughout,
time base 333673/10000000. Own checks did not rerun the complete source AVI,
selection inventory or root's two-run extraction/artifact audit.

Viewed only `run01/vince-clip2/native/frame-000001.png` through
`frame-000009.png`, once each, in ascending batches 1-3, 4-6, 7-9 using full
original-detail `view_image`. Nine successful displays, no failure or repeat.
No crop, deinterlace, resize, audio, metric comparison or extra frame.

## Nine-frame record

**I** below means an incompatible positively visible composition with the
specific reference view, not a whole-clip exclusion or proof of a different
recording. These samples do not reveal the references' required combinations
of local facade and foreground relations; hidden lower-facade detail remains
unresolved. Relative timestamps are encoded PTS values, not a historical clock.

| Ordinal | Source index / PTS | Exact seconds | Observed scene and specific cue/countercue | 5-141 | 5-142 | 5-143 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | Street/reporting view: foreground person with microphone, emergency vehicle on the left, low foreground buildings and a banded high-rise/roof behind. This positively different foreground/background arrangement does not reproduce any reference's near-corner composition. | I | I | I |
| 2 | 101 | 33700973/10000000 | Foreground person's head occupies the lower center; roof-bearing high-rise behind low rooflines, with another tall background form to the right. This is not the reference 142 sign/corner/canopy combination or the other references' close facade view. | I | I | I |
| 3 | 202 | 33700973/5000000 | Upper high-rise facade and roof structures dominate; broad dark banded face is left of a narrow lighter right-hand face. Foreground roof and lower-third cover the lower scene. This is a different exposed corner/top-of-building composition, not the references' local lower-facade relationships. | I | I | I |
| 4 | 303 | 101102919/10000000 | Same roof structures above the broad banded face, with narrow right face and foreground roof below/left. No two reference-specific landmark relations recovered. | I | I | I |
| 5 | 404 | 33700973/2500000 | Roof/banded upper-facade view persists. The foreground roof and banner still prevent reading the relevant lower neighborhood; that obstruction is not evidence about hidden landmarks. | I | I | I |
| 6 | 505 | 33700973/2000000 | Broad left face and lighter right side meet at the visible right-hand corner; upper rooftop features remain in frame. This topology is unlike the references' broad right face adjoining an obscured left side. No mirror/aspect correction is assumed. | I | I | I |
| 7 | 606 | 101102919/5000000 | Same upper-building and foreground-roof arrangement, with broadcast banner across the lower image. Generic horizontal bands alone do not identify a reference counterpart. | I | I | I |
| 8 | 707 | 235906811/10000000 | Upper banded facade/roof remains the visible subject; the reference-specific interrupted strips, lower grid neighborhood and street assembly are not jointly available. No positive scene association. | I | I | I |
| 9 | 808 | 33700973/1250000 | Continued roof/upper-facade view with the same opposing-face and foreground order. No supported reference match; no additional source scene inferred beyond the selected last frame. | I | I | I |

## Reference-specific disposition and strongest limitation

- **5-141:** The selected upper-building view does not supply R141-A/B's
  ordered local strip/intervening-band/lower-grid neighborhood beside the
  reference corner. A possible same-building resemblance from general bands
  is not enough for this scene/view criterion. No independent building
  identity or directional survey was established from the roof in this pass.
- **5-142:** The foreground person/emergency-vehicle/low-roof scene and then
  upper-building framing are positively different from the reference's
  sign-stack/corner/upper-right-obstruction scene. Missing signs alone are
  not the reasoning, and absence from cropped/obstructed areas is not scored
  as an independent countercue.
- **5-143:** The close irregular-upper-feature / pale interval / lower-grid
  arrangement is not recovered. Roof-level banding cannot replace that
  distinctive local geometry. The unexposed lower area remains untested,
  not classified incompatible pane by pane.

The strongest remaining alternative is a matching view in an uninspected
interval or another part of the source recording. All intervals between the
nine listed sample times remain visually uninspected. A different observed
view does not disprove common-recording membership, and a same-building view
would not prove it. Broadcast credit/name/lower-third text, smoke and generic
bands cannot bridge those distinctions. SAR/interlace limits preclude metric
slope, proportion or movement conclusions; only visible ordering/context was
used.

## Checked PNG pins

Ordinal 1-9 SHA-256 values respectively:

1. `9a90703406d26a44a02c62b9bfdedfee820c16d0f351a5fefcf03c6aa8a64e32`
2. `4ee8f467790f9ec11f11cd2c34dcb06a10312dd56f8a4585054c371e6a7b84df`
3. `3022e5664cae0b6c6a71ac48f1ca8746782d5d354c8383e41cca4b61e01355e2`
4. `5e893517c7397f82215ce7902abc58c6cfdf73cb9d207a05905a03c0adb6c733`
5. `1dd205c3a2dc82b51b073a1ab4b3a37109e5b52ba1474f51ce47d7431f4ee9f6`
6. `4677db3e677cb410f697bb86c251dc4635f71209bc2adf44d4e095eaf3955645`
7. `6f3b132a7ce52bad28b832bfaa54159d4ad6497fbc1889a804a0781ad1e52745`
8. `ef716082450ec45ce22a9c2a7bac69b2a2b0c68979d1f01c9a1f8d8c6c22ce5b`
9. `0179d7c2a5467ef7314cf8bf6fbf19819f438e7b217a4df2be08da7ff4019642`

## First-freeze boundary

All nine fixed images received a record. No supported scene/view association
to the three references was recovered within this coarse selection. This is
not exhaustive clip review or a finding that no such view exists. Clip 1's
original record is unchanged; no root/peer findings have been used to revise
either. The other six candidates remain outside this stage's coverage.
No glass-state claim, physical measurement, source/exposure identity, event
time, causal assessment, new human acceptance or canonical promotion follows.
