# Independent localized-change and roof-feature observations

September 20, 2026 UTC. Research-only, prior-informed AI visual reading, saved
before reading root's new selection or observation files or receiving its
candidate findings. Not blind review, an independent camera, a human
spot-check, or a licensed forensic/engineering opinion.

## Authority, input and actual coverage

Read main controls, the complete charter, current status/limits, the main
comparator protocol/report and the earlier A/V protocol/refinement/report.
The present [protocol](PROTOCOL.md) has SHA-256
`1d1d1993a6d9a27f66037d5abef449ffe685e7238c20a81a9b85f97ae240883c`;
the frozen [feature/display rules](FEATURES.md) have SHA-256
`bfee24a125a8358d076ef0cd78f23958764385762e8802ae8be1ec77c88289d7`.
My pre-refinement [selection](independent-selection.md) was frozen at
`0e514e82ff744c504cb96d3ac71512b8e7b16f895fa12f4053db5cb305f9c501`.
These three hashes were rechecked unchanged after viewing.

Historical input is the admitted VID-DEM-001 uploaded access copy, source
SHA-256 `8560cd686a18c8fcc16fe802691e0f17f117c713b4cd1862017af24d391ce5a2`.
I viewed only supplied `run02` native PNGs and `display01` overview sheets.
The selected map SHA-256 is
`14c72246559d79812c1eef4b42d977c64d1f28bc97d0f034a945cddb8db5561a`.
All frame pins below use zero-based source indices, not PNG ordinal numbers;
the PNG ordinal is source index minus 238. This map preserves encoded PTS,
not authenticated original exposure times or real-time speed.

Actual display record:

- Nine overview sheets, suffixes 0000, 0030, 0060, 0090, 0120, 0150, 0180,
  0210 and 0240, each once in ascending order: all 242 thumbnails, indices
  239-480. Thumbnail screening is not native-size examination.
- Native grid: 239, 254, 269, 284, 299, 314, 329, 344, 359, 374, 389, 404,
  419, 434, 449, 464, 479, 480. Index 239 was the earlier baseline admission
  display and was not reopened. The other 17 were displayed once in order.
- Frozen native refinements: every index 359-376, then every index 434-466,
  once each in ascending order. Overlapping R1/R2 category coverage was
  combined, not displayed twice. These are 51 refinement presentations.
- Total: **69 native presentations of 64 distinct indices**, five planned
  repeats (359, 374, 434, 449, 464), plus nine overview-sheet displays.
  **No failed, truncated or reopened display occurred for this reader.** All
  native images were displayed at original detail, at most three per call.
  No crop, zoom derivative, stabilization, enhancement or extra interval.

Read-only checks matched all 18 grid and 51 refinement map entries, filename
joins and PNG hashes. Set arithmetic reproduces the 64/69 counts and five
repeated anchors. Exact-fraction checks below used each selected row's PTS
and 1/30000 timebase. No source acquisition, historical decoder or tracking
algorithm was run by me. Root's extraction/pixel verification and assessment
of the 13 conversion-fallback warnings per run are admission information,
not checks performed by this reader or a colorimetric/authenticity validation.

## Observations, not physical initiation times

| Category | Native evidence and my observation | Permitted result and uncertainty |
|---|---|---|
| L | Across 359-376, a dark narrow protrusion becomes distinctly recognizable outside the left facade edge near x574-584/y397-403 at 368; it remains recognizable at 369 and 370 and thereafter in this refinement. Earlier frames contain small edge/surface differences that I cannot consistently separate from existing openings, shimmer and small changes. | A localized appearance change is positive by 368, with three-frame confirmation through 370. Index367 is ambiguous, not a certified unchanged predecessor. This is not an adjacent-frame physical-onset bracket or the first event anywhere on the facade. |
| R1 | The left roof/wall vertex and adjacent mullions remain identifiable through the chosen 434-451 interval while the left face changes shape. Its downward image displacement relative to each reference passes my frozen interval rule at 442-444, as calculated below. | Positive-by442, confirmed through444, conditional on these subjective placements/reference identities. Earlier ambiguity extends before the selected interval; no stationary last-before anchor or finite first-physical-motion bracket is established. |
| R2 | The central top corner changes configuration across449-466. A dark projecting strip, bent top rows and the changing roof/facade junction make it unclear which late edge preserves the original exact material vertex. | Apparent deformation/motion is visible, but no qualifying three-frame, two-reference R2 detection is established. Do not substitute the antenna base, uppermost surviving outline or a nearby new kink for R2. |
| R3 | The upper-right corner remains recognizable in the native grid, including479/480, without a resolved downward transition meeting my rule. | Detection unresolved/right-censored within the fixed coverage, not proof of zero displacement or a lower bound on physical initiation. No additional R3 interval was selected or inspected as a separate refinement. |

The positive L description is deliberately neutral: dark outward edge change,
not an observed explosive charge, column cut or support-removal instant. The
later coarse-grid frames show several larger facade outgrowths and substantial
changing geometry. Those do not make the first small change unambiguous or
authenticate a causal sequence.

The older A/V report recognized changes in earlier sparse samples, including
the neighborhood of index360. My more conservative recognition of this
particular protrusion at368 does not erase that record or establish that
360-367 were unchanged. The present category/coverage and uncertainty must
remain visible rather than silently declaring a new universal first event.

## Subjective placements and exact interval calculation

Inclusive y-envelopes are integer native-pixel visual placement ranges, **not
statistical confidence intervals**, subpixel measurements or calibrated
physical-coordinate errors. Positive y is downward. B1's stepped/curved trim
and the small partially screened B2 corner limit precision; I retained broad
envelopes rather than using their approximate feature-map coordinates as exact.

At baseline239: R1 [134,139], R2 [110,115], R3 [113,119], B1 [493,502],
B2 [562,574]. These were recorded in my frozen selection before refinement.

For intervals R_i=[r_lo,r_hi], B_i=[b_lo,b_hi], baseline R_0 and B_0,
the exact enclosure used is:

`Delta(R-B) = [r_lo - b_hi - r0_hi + b0_lo, r_hi - b_lo - r0_lo + b0_hi]`.

| R1 index | R1 y-envelope | B1 y-envelope | B2 y-envelope | Delta versus B1 | Delta versus B2 | Classification |
|---|---|---|---|---|---|---|
| 239 | [134,139] | [493,502] | [562,574] | Baseline | Baseline | Reference placement, not proof of rest |
| 434 | [143,154] | [493,502] | [562,574] | [-5,29] | [-8,32] | Ambiguous |
| 441 | [150,162] | [493,502] | [562,574] | [2,37] | [-1,40] | One reference passes; joint rule fails |
| 442 | [152,163] | [493,502] | [562,574] | [4,38] | [1,41] | Positive |
| 443 | [153,164] | [493,502] | [562,574] | [5,39] | [2,42] | Positive |
| 444 | [154,165] | [493,502] | [562,574] | [6,40] | [3,43] | Positive, third consecutive |

Every displayed B1/B2 instance used in this table remains within the stated
envelope; equal envelopes mean no more precise displacement was resolved,
not exact measured stationarity. The 434 and441 positive upper limits forbid
treating either as a stationary last-before anchor. The three positive rows
establish a finite-resolution R1 detection only; they do not turn441-442
into a physical-onset interval. Earlier coarse observations likewise do not
exclude a small pre-existing motion.

For R2 at449 I can provisionally place the original corner within [112,123],
with B1 [493,502] and B2 [562,574]; this plainly does not pass the two-reference
rule against baseline. Through the later selected interval, increasing
configuration/identity uncertainty cannot be repaired by choosing the highest
visible pixel. I cannot localize an authenticated continuation at464-466
well enough to admit three R2 coordinates. No interpolated values are supplied.

For R3 at479 and480 my visual envelope is [111,122] with the same broad B1/B2
envelopes. It overlaps baseline and permits both positive and negative relative
changes; two late frames would not by themselves satisfy persistence anyway.
This is a nondetection with limited opportunity to resolve small motion, not
a measurement that the right corner remained physically stationary.

## Encoded-time pins and ordering ceiling

| Role | Index | Exact encoded seconds | Decimal navigation only |
|---|---:|---|---:|
| Baseline | 239 | 239239/30000 | 7.974633333 |
| L ambiguous predecessor | 367 | 367367/30000 | 12.245566667 |
| L first recognized positive of the selected protrusion | 368 | 23023/1875 | 12.278933333 |
| L second confirmation | 369 | 123123/10000 | 12.312300000 |
| L third confirmation | 370 | 37037/3000 | 12.345666667 |
| R1 earlier selected anchor | 434 | 217217/15000 | 14.481133333 |
| R1 joint-rule ambiguity | 441 | 147147/10000 | 14.714700000 |
| R1 positive-by coordinate | 442 | 221221/15000 | 14.748066667 |
| R1 second confirmation | 443 | 443443/30000 | 14.781433333 |
| R1 third confirmation | 444 | 37037/2500 | 14.814800000 |
| R2 last allowed refinement frame | 466 | 233233/15000 | 15.548866667 |
| Final admitted bounding frame | 480 | 2002/125 | 16.016000000 |

These positive witness coordinates are ordered within the encoded copy. They
do **not** establish strict first-onset ordering: both have earlier unresolved
regions, and R1's possible small-motion region is not bounded after L. No
numeric physical delay is computed from the two detection coordinates. With
R2 and R3 unresolved under the declared rule, no onset of distributed motion
at all three roof features is established in this pass.

## Alternatives, claim strength and stop

Simple common vertical image translation is insufficient for the accepted
R1 displacement under the two-reference envelope assumptions. That is not
full camera calibration: rotation, zoom, parallax, lens/exposure/edit history,
reference stationarity and subjective placement errors remain unmeasured.
B3 supplied only coarse context. The upper facade's clearly changing shape
also defeats an assumption that one roof point traces a rigid building or
the original building's mass center.

The strongest objection is that my broad manually assigned envelopes and
point-identity judgments are not calibrated annotation errors. A better
source or qualified independent marker review could reveal earlier motion,
resolve R2, or contradict a borderline positive placement. Accordingly, the
local visual-change and gross R1-motion descriptions are B within this access
copy and the stated coverage; exact physical initiation, distributed roof
onset, source authenticity, rigid motion and causal identification remain D.
The integer interval/PTS arithmetic is directly reproducible from these
annotations but does not validate them physically.

The frozen display route is exhausted. No interval extension, crop/zoom,
threshold adjustment, new retrieval or source substitution is proposed here.
A stronger result requires feature-resolving original/camera records and
qualified placement/reference review, not another unreported screen of the
same access copy. No WTC7 causal ranking, legal promotion, accepted engine
state, outreach, fee, commit or push changes. Only my selection and this
independent observation note were written in this unit.
