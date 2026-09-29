# Two remaining fire images: first-look result

2026-09-24. Research only, single prior-informed AI reader, not paired annotation,
source authentication, a thermal measurement or a structural conclusion.
Selection and allowable inferences were fixed in [FIRE-FIRST-ACTION](FIRE-FIRST-ACTION.md).

## Actual inspection and result

Root inspected both complete native JPEGs before the four newly rendered complete
pages. Source captions and the older source-map lead were already known; this
was not blind. Then root visually read all physical PDF pages 274-277, including
captions and the surrounding timing discussion. The four pages are legible and
complete in their 935×1210 display derivatives. The extra Figure 5-147 on page277
is context, not a newly selected exposure or independent observation family.

| Native asset / visual page association | Pixel observation | Limits |
|---|---|---|
| A-79c9dd7424ec, 695×476; visually associated with Figure5-145 on physical275/printed231 | Gray/dark veiling over much of the target facade; separated reddish/pale luminous features near the row labeled9, including a group roughly x330–550/y90–120, and a small bright patch roughly x279–302/y142–159 near the row labeled8. Most features do not resolve sufficiently detailed flame tongues for a confident morphology distinction from glow in this still. | Heavy haze, small features, labels, poles, trees and foreground buildings/vehicles obscure parts of the view. Floor/column numbers are report overlays, not independently surveyed coordinates. Bounding ranges are rough locators, not emitting areas. Lower or darker regions cannot be scored as interior fire absence. |
| A-0ca71594109e, 328×311; visually associated with Figure5-146 on physical276/printed232 | A broad dark plume/veil crosses the central/lower facade. Several separated orange luminous patches align across a lower horizontal band, clearest roughly x115–136/y249–266, with additional smaller patches to its right. Some upper facade bands are visible without comparable resolved luminous features. | Native resolution is especially limited. The bright patches are consistent with fire but do not, alone, resolve emitting gas, window identities or continuous burning between them. Foreground buildings, lamps and trees occlude lower/frontage portions. Unseen interiors and the other faces remain unobserved. |

These native stills support bounded luminous-feature and obscuration observations.
They do not independently verify every flame/window or continuity claim made
in the report's discussion of its fuller video material. That is a resolution
and source-scope limit, **not evidence that those fuller claims are false**.
Conversely, assigning a categorical low heat release from the small projected
patches would also exceed the pixels. Neither report-image brightness nor the
absence of resolved tongues is a temperature measurement.

## Primary-source timing and processing check

The directly inspected source is main `authority/nist/wtc7/ncstar-1-9.pdf`,
SHA-256 `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.
The following are NIST's attributed reasoning/labels, not independently
authenticated clocks, camera positions or historical facts:

- Physical274/printed230 estimates Figure5-145's time using apparent fire
  distribution relative to Figure5-144, an assumed typical intense-burning
  duration and an assumed15-minute separation. It assigns roughly4:10p.m.
  with at least5minutes uncertainty. The caption shows ±5min; the prose's
  "at least" matters and is not reduced to a hard symmetric error bound here.
- Physical275/printed231 estimates about10minutes of development between
  Figures5-145/146 to place the latter around4:20p.m. The next caption calls
  that a rough estimate. These are not two independent clock readings.
- Physical277/printed233 compares the latter photograph to later Peskin frames
  and invokes typical intense-burning duration to argue a latest possible
  time of4:28p.m. That bound depends on the fire-duration/decline assumptions;
  this first look does not independently derive or endorse it as a hard limit.
- Both selected captions disclose intensity adjustments and added labels;
  Figure5-145 also discloses a blurred face, and Figure5-146 is a crop. No new
  enhancement, crop or recompression was applied in this unit. The extracted
  images retain the report's processing, which is not original camera data.

**Consequence:** these pictures can constrain visible spatial patterns, but
their assigned times cannot independently validate the fire-development
assumptions used to date them. This directly verifies an already identified
timing-dependency concern; it is not a newly discovered admission, evidence
of fabrication or proof that NIST's chronology is wrong. An independent
clock/source-sequence anchor could strengthen, revise or contradict it.

## Reproduction and remaining test

The fixed coverage join found34 candidate figures in the older source map:
8 already in the25-photo paired set and26 lacking coverage in this declared
union. The two selected figures are among those26. This first look adds two
single-reader records; it does **not** convert their state to paired or
reduce the26 lacking-paired-record count. The other24 remain outside this
new visual pass. The independent reviewer caught an initially over-specific
page assignment for145/146; [correction](FIRE-JOIN-CORRECTION.md) preserves it.
Corrected source-map grouped page locators remain grouped, not guessed unique
figure/page assignments. See [coverage result](fire-coverage02.json).

The pinned reused extractor produced4 pages and3 native image objects with
zero recorded warnings, verified the source before/after, and saved commands,
runtime, dimensions, hashes and placement records. A later separate
[technical check](fire-extraction-independent-check.md) independently parsed
the four pages with pdfminer/pdfplumber: all three objects' dimensions,
decrypted encoded JPEG bytes and placements agree, and31 products/key match
their pins. That reviewer did not view pixels or certify figure associations.
The historical extractor receipt names its original
entry point; `wrapper-receipt.json` records the actual wrapper and page/output
overrides. No historical extraction was overwritten and no source changed.

Next bounded measurement: preserve this prior exposure, obtain a separate
native-image observation record for both figures under the batch2 vocabulary,
then retain disagreements before source/model comparison. Independently
review the verified extraction and page placement; join any richer source clip/clock only
if actually located and authorized. A same-region/time model contradiction
requires that additional join. No causal ranking, heat estimate, whole-floor
absence finding, engine acceptance or legal fact results from this first look.
