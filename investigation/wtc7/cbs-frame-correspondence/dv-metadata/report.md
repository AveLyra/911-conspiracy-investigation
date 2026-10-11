# DV stream metadata: timecode present, recording-date/time packs absent

2026-10-04. Research-only. This is a bounded metadata result, not a collapse
mechanism finding or an authenticated account of the camera's history.

## Answer

Across all eight held CBS/Vince access-copy AVIs, the scan recovered **timecode-type
packs in every encoded frame, but no recording-date/time pack identifiers in
any of the inspected subcode, video-auxiliary or audio-auxiliary slots**. The
population is all 5,567 frames and 3,674,220 five-byte slots, not a sample.

This does **not** supply an independently authenticated filming clock for
Figures 5-141–143. It also does not prove the published chronology wrong.
The earlier tape-label ordering conflict remains conditional on the source
associations and on whether those labels preserve original recording order.
The new per-frame timecode material is a concrete continuity/mapping lead,
not yet a verified calendar, elapsed-time sequence or camera-clock reading.

The [raw summary](v2/inventory-summary.json) and eight complete result manifests
under `v2/results/` preserve the counts and uninterpreted five-byte candidates.
The [execution record](execution.md) records both refused version 1 attempts,
the explicitly increased storage capacity, the frozen version 2 method and
actual verification. A separately implemented direct-byte audit reproduced all
frame locations, retained bytes, per-frame identifier counts and raw target
variants; root's [complete rerun](root-independent-audit.json) also passed.
This is computational reproduction of the same sources, not independent
historical corroboration or user/expert acceptance.

## Observations, without semantic clock conversion

Every frame has the same identifier counts:

| Area | Identifiers and counts per frame | Slots per frame |
| --- | --- | ---: |
| Subcode | `13`: 40; `ff`: 80 | 120 |
| Audio auxiliary | `50`: 10; `51`: 10; `ff`: 70 | 90 |
| Video auxiliary | `60`: 10; `61`: 10; `ff`: 430 | 450 |

The pinned primary definitions identify `13` as timecode, `52`/`53` as audio
recording date/time and `62`/`63` as video recording date/time. None of the four
recording-date/time identifiers appears. We report `ff` as the observed raw
identifier, not as proof that every remaining byte in those slots is empty.
Within each frame, all 40 `13` packs agree byte-for-byte. Each frame's five-byte
value is unique within its clip. Neither property by itself establishes valid
BCD digits, a continuous counter, correct drop-frame handling or camera origin.

| Clip | Frames | Compressed artifacts | First raw `13` pack | Last raw `13` pack |
| --- | ---: | ---: | --- | --- |
| 1 | 418 | 5 | `13d78580c0` | `13d49980c0` |
| 2 | 809 | 9 | `13d4b380c0` | `13d48081c0` |
| 3 | 189 | 2 | `13e88081c0` | `13c68781c0` |
| 4 | 206 | 3 | `13c98781c0` | `13c49481c0` |
| 5 | 529 | 6 | `13e2d481c0` | `13d29282c0` |
| 6 | 197 | 2 | `13c6c782c0` | `13e2d382c0` |
| 7 | 1,128 | 12 | `13e69283c0` | `13d3d083c0` |
| 8 | 2,091 | 21 | `13d3b588c0` | `13c5c589c0` |

The retained control/header population totals 53,276,190 raw bytes, stored
losslessly in 60 artifacts totaling 19,906,399 compressed bytes. All eight held
source files still match their acquisition pins. The collection checked frame
extents and the fixed DIF layout; this is not complete DV codec-conformance
certification. No image
or sound was decoded or viewed in this unit.

## Why the result does not settle chronology

The strongest alternative to an erroneous publication order remains a copy or
edit timeline whose labels are not original camera chronology. The format can
carry copied or generated timing fields. The pinned FFmpeg muxer source shows
that software can write timecode and recording-date/time fields; that is a
demonstration of a technical possibility, **not** a finding that FFmpeg or any
particular editing workflow produced these historical files. See
[primary definitions and copy/edit limits](references.md).

Conversely, clean-looking, internally consistent timecode could preserve real
recording continuity. A checked interpretation might identify counter breaks,
agreement with the AVI tags or a useful disagreement. That is still worth
testing, but agreement between two fields copied from one timeline would not
make them independent clocks. A counter without authenticated date, origin and
edit mapping does not independently establish the claimed local filming times.

Absence here is limited to the declared DV slots in these eight exact access
copies. It is not absence from original tapes, every possible metadata channel,
unexamined files, the agency archive or a source custodian's records. It does
not establish who removed anything, whether removal occurred, or intent.

## Next discriminator and unchanged inference limits

Predeclare a semantic timecode test over the retained bytes: validate digit and
flag meanings against primary definitions; preserve invalid and contradictory
values; check every adjacent frame transition; and compare the eight starts
with their exact AVI labels under explicit rate/drop-frame interpretations.
Do not silently substitute nominal DV rates for the saved AVI rates. Synthetic
boundary and malformed-value controls and a separate method review must precede
historical interpretation. The original-camera/edit/still export mapping remains
a separate documentary lead even if all internal counters prove consistent.

This unit does not change a ranking of collapse causes, measure temperature or
fire severity, validate NIST's structural model, prove deliberate support
removal, or establish concealment. A valid chronology would help test specific
time-dependent fire/window claims; its present absence is not a universal gate
on qualified spatial observations or the other charter workstreams.

The user's locked comparator coordinates and user-assessed ±1 native-y-pixel
placement ranges remain unchanged, not statistical confidence intervals.
Human 142-N12 and model/window joins remain unresolved. No human acceptance,
engine activation, legal/main promotion, external disclosure, commit or push.
The comprehensive investigation remains active and incomplete.
