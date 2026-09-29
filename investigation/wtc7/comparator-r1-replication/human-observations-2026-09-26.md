# R1 comparator: user-reported native-coordinate observations

Intake: 2026-09-26 America/New_York (2026-09-27 UTC). Working research.
These are the user's reported observations, transcribed from two consecutive
replies in this task after the local viewer restart. They are not AI image
annotations, a new camera source, or independent evidence of the historical
cause. The second reply repeats the same coordinates and adds a placement
tolerance. No new image was displayed by the agent during this intake.

## User input and explicit interpretation

The user described each point as `LOCKED` with native-pixel x and y. In the
second reply the user stated:

> Honestly, we can narrow the confidence interval to 1 pixel from what I defined

For this y-based study, conservatively interpret that as an inclusive
**assessed placement range [y − 1, y + 1] native pixels**, not a one-pixel
total width. The radius-one convention is the agent's disclosed interpretation,
not a verbatim definition supplied by the user. It is not a statistical
confidence interval, calibrated error bound, or demonstrated repeatability.
No radial or two-dimensional uncertainty model is assigned. The x coordinates
are retained as reported point selections, not given an invented x-error model.

The first points on frames 443 and 444 were not explicitly labeled R1 in either
reply. They are attributed to R1 by their ordering and surrounding B1/B2 labels;
this is an explicit, correctable interpretation. No other coordinate is changed.
No feature-identity ambiguity was reported; this records the user's intended
R1/B1/B2 mappings, not expert certification of physical material continuity.

## Complete reported point table

Native origin is upper-left; x increases rightward and y downward. The review
assets are 1280 × 720. The viewer's locked native-coordinate readout is the
reported method; exact zoom, click-versus-keyboard adjustments and repetitions
were not specified and are not invented here.

| Source frame | R1 x | R1 y | B1 x | B1 y | B2 x | B2 y |
|---|---:|---:|---:|---:|---:|---:|
| 239 | 585 | 136 | 339 | 497 | 1116 | 562 |
| 434 | 586 | 147 | 339 | 497 | 1116 | 562 |
| 441 | 586 | 155 | 339 | 497 | 1116 | 562 |
| 442 | 586 | 155 | 339 | 497 | 1116 | 562 |
| 443 | 585 | 157 | 339 | 497 | 1116 | 562 |
| 444 | 585 | 159 | 339 | 497 | 1116 | 562 |

The corresponding R1 y-ranges are [135,137], [146,148], [154,156],
[154,156], [156,158], [158,160], in that order. B1's assessed y-range is
[496,498] and B2's is [561,563] in every reported frame. Repeated reference
coordinates do not establish physical stationarity or zero measurement error.

## Scope of human-check acceptance

The [frozen protocol](PROTOCOL.md) requires actual human feature/coordinate/
envelope checking before the historical numerical replication. The user's
named point placements followed by an explicit one-pixel tolerance provide
that substantive input. A read-only check parsed both original AI tables and
confirmed that every assessed human y-range is wholly contained in each
reader's original y-band: **18 placements × 2 readers = 36 containment checks**.
This is stronger than the earlier central-point-only check. No x-envelope
agreement is claimed because the original AI records provide no x-envelopes.

The human mapping prerequisite is therefore satisfied for these six frames
and these three intended features, under the disclosed y-radius convention.
A separate AI method reviewer checked the gate interpretation against the
protocol and review instructions; that review is not another human observation.
It did not perform the containment calculation. Root performed those checks.

This clears only that prerequisite. Source-clock authentication, reference
stationarity, complete physical uncertainty, numerical verification and
collapse-cause conclusions do not follow from it. A systematic feature-selection
error could survive precise clicks; the present acceptance is the specified
human mapping check, not proof that every possible image/geometry error is absent.

## Preserve the original experiment

The original two-reader reproduction must use the original frozen AI bands.
Do not replace or tighten them using this human record, average the readers,
or choose the more favorable annotation after computing a result. The narrower
human ranges are a separate attributable observation version. Any numerical
human-annotation comparison must be declared separately before its results,
and must not be presented as the original two-reader replication.

No historical displacement interval, detection, old-table comparison or
reproduction verdict was computed during this intake. The original protocol,
annotations and source images remain unchanged.

## Actual verification and source identity

Read-only checks used Python 3.12.14 with pathlib, re, hashlib and struct,
through a stdout-only script. Both annotation tables had exactly the six
declared sections and all three feature entries. All 36 full-y-envelope
containment checks passed. All reported points and their radius-one y-ranges
are within the native raster; checking bounds does not calibrate accuracy.

The six viewer PNG byte hashes and 1280 × 720 headers also matched the existing
fixed-asset identities. This was a byte/header check, not image decoding,
display, original-exposure authentication or a rerun of the source-clock audit.
Source frame 239 maps to output ordinal 0001; 434 to 0196; 441–444 to 0203–0206,
respectively, under the existing [source check](source-check.md).

Unchanged input SHA-256 values:

- Protocol: `2bbc5777dd39dde42a2945d1d049a1a46f8c4b61678308e328e803f0ffa2331a`.
- Root annotations: `d8d9bfb77b51780e1cef47e7a41577509d37bbfbd7189667e2eb69693fb51352`.
- Second annotations: `240a1849e927bebb38803037cc28253132186ddb5049577bab467d7e1769846d`.

The current user instruction supports recording this new human observation and
its range assessment. It is not approval of the separately pending combined
NIST/UAF observation matrix, any disclosure, legal promotion, commit or push.
