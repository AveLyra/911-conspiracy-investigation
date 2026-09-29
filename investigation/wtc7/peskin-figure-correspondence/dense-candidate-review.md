# Dense shortlist: bounded visual and method review

2026-09-13. **Disposition: strong multi-feature scene/composition correspondence,
but not a unique access-copy frame or original-exposure identification.** All
12 global shortlisted native images and both complete targets were inspected.
Several neighboring candidates remain visually similar at the available
detail. No new numerical scoring, decoding, imagery or source acquisition was
performed by this arm. This note does not identify a historical clock, exposure
separation, original cadence, fire temperature or collapse mechanism.

## Actual independence and inspection sequence

The shortlist was producer-selected from the declared global top four per
target per metric, not independently sampled. The prior target-only and
one-second reviews were already known. Those notes remain unchanged:

- [Independent target review](independent-target-review.md), SHA256
  `ceee2c6607f33a16225fb8c01aa876f076a382f3ce54d7b0776d266ca7ab6b9f`.
- [Initial candidate review](initial-candidate-review.md), SHA256
  `38c01ff83a4e1879510a67092604a8965ff90b1051689ac00799c3bbe3537327`.

Before image inspection, the following projection extracted only identities
from the hash-checked primary summary. It discarded metric names, score
values, ranking order and fitted transforms, and sorted the union by PTS:

```jq
[.results | to_entries[] | .key as $target | .value[] | .top_four[] |
 {target:$target,source_pts,run,frame_index,native_png}]
| unique_by([.target,.source_pts]) | sort_by(.source_pts,.target)
```

Both complete targets were viewed first, followed by native indices 77, 91,
93, 95 and 96. **Before any qualitative file checkpoint was frozen**, root's
message identifying indices 93 and 185 as its leading images and describing
its strong composition/fire-feature agreement arrived. The remaining indices
97, 101, 178, 179, 185, 186 and 187 were then fully viewed with that context
known. This was disclosed to root immediately. Accordingly, the final note
is **not wholly rank-blind**, and the first five image views are not a separately
frozen interpretation. No clean holdout or fully independent interpretation is
claimed. Numerical dense score values and regional diagnostic results were
not read at any point before this note was frozen.

Earlier code review read DENSE-01's initial-screen leader labels only after
the earlier ten-frame qualitative note had already been frozen. That fact
does not restore blindness to the present dense review. Parent reported
959 frames / 1918 comparisons and subsequently successful reproductions;
these are producer/reproduction claims, not this arm's independent numerical
coverage result. This arm verified the 12-image union and its saved identities,
not every dense frame or score surface.

## Controls and source pins

Current main AGENTS/WORKFLOW/START-HERE and the full CHARTER were read in the
preceding bounded work. The full candidate declaration, prior target/initial
reviews and applicable evidence/source/development safeguards were read for
this review sequence; the continuation declaration was fully read before
these new images. No legal or source authority boundary was changed.

| Dependency | SHA256 / role |
|---|---|
| `primary-summary.json` | `c34061bdc218dfd9c818766066ed5aecc636a39f815ef1340ca57dae769327b3`; identities/receipt pins only read, not score values |
| `CANDIDATE-REVIEW-01.md` | `860b87a847365de05ed3dc0cedccd788f55a9230da9bdc7a10e110c1bb881784` |
| `DENSE-CONTINUATION-02.md` | `f532f8376db02f01f5943ea7f1df99719a016a57eecaee2185db079b320f5156` |
| `METHOD-01.md` | `412c7aae4da6010d4323d900182c8419dc314fd64953ed9c2c3878b3bd335e6c` |
| `DENSE-01.md` | `8a7ac08aa7901c0de5956b617950f9fda35a786b7a9b58a26c7ba54c785413f8` |
| `DENSE-GATES-01.md` | `8d0c5bae4654c99813d0d896989963c2b557e80e87a160cbedc5edcebce3ebda` |
| `dense12/receipt.json` | `9d149ffecb76137c9581017671eabf6b930bbdbd4da99e8a52c4c032186536ef`; completed status and selected native pins read, SHA agrees with summary |

Only the accepted production set dense00/dense11/dense12/dense13 is referenced
by the supplied summary. The continuation declaration preserves the failed
partial dense01 separately and explains the decoder read-allowance change;
this arm did not inspect or count that failed partial output as accepted data.
It did not independently diagnose the decoder or reperform its coverage tests.
Every globally selected image happens to be in dense12; that is a shortlist
property, not a reason to omit the other chunks from root's numeric coverage.

Targets are the same 720 x 478 main-repository JPEGs already source-reviewed:

- `fire-annotation/assets/run-01/images/A-370a6ef2789a.jpg` (T148), SHA256
  `8afb62b6dce6e4618075c66576ef9fdf88295d636427893dc36064afb37a1253`.
- `fire-annotation/assets/run-01/images/A-e43e4088a4a2.jpg` (T149), SHA256
  `6129afd898a56282579832595715ef2e1093b55d299b693810ac05c72af53469`.

Both targets and all 12 native PNG hashes were checked before and after
viewing and remained unchanged. All 12 PNG byte sizes matched the completed
receipt. The PNGs are 1620 x 1080 RGB, 8-bit, non-interlaced containers; that
does not establish the historical source's acquisition/interlace mode.
All image views used full original-detail files, without generated crops,
aspect correction, overlays or enhancement. No full PDF page was newly viewed
in this dense arm; the preceding complete-page review remains the placement
and caption dependency. No new video-byte or decoded-pixel equivalence test
was performed here. Matching preserved file hashes is not historical
authentication or an independent reproduction of frame extraction.

## Exact inspected native-image coverage

All paths below are relative to this unit's `dense12/`. Source PTS is the
summary's identity field in the declared time base 1/1000, not a historical
clock. A = viewed before root's leading-image message; B = viewed afterward.
Seven target-148 and five target-149 rows are 12 unique full native images.

| Target | Native file | PTS | Phase | Bytes | SHA256 |
|---|---|---:|---|---:|---|
| T148 | `native-0077.png` | 2520599 | A | 532823 | `663567d6be6d063dea603539dc9c28b9f587d0d9b8f45c83b2b6e88d63cc02a0` |
| T148 | `native-0091.png` | 2521066 | A | 516289 | `fb2fddaf374e08d42404aa1bebdcd47d64304df26804b98869649c95298e5878` |
| T148 | `native-0093.png` | 2521133 | A | 527145 | `3bb0cdc2b0cd5b9e85f94c1c7bf8674232edfd192cd7276ebfcfa00b9a686f3c` |
| T148 | `native-0095.png` | 2521200 | A | 567930 | `4127eb851a81a9b8724161ff9bf31f529c05c0bbb06de116b25e9abd1b9a6e03` |
| T148 | `native-0096.png` | 2521233 | A | 543928 | `cfaeac16be09e7dce63e60ad03861c1b984292f98da15fc7c1f55205f98e90a4` |
| T148 | `native-0097.png` | 2521266 | B | 541631 | `a9431f6a7c0b69f84018735a70c71385b405a8ba6ffd5c2b8284f1ab51a98fad` |
| T148 | `native-0101.png` | 2521400 | B | 535894 | `3391d7cc51d57e8e847c0ad4b4df2a212d74d8b4afb94276534a244a5f750d7b` |
| T149 | `native-0178.png` | 2523969 | B | 511162 | `113a05aff65030ae7cf259e2188a50eb174c57f1f621bc5513fc63ded44b1256` |
| T149 | `native-0179.png` | 2524002 | B | 504053 | `733060fcc49d94d794b7b23a050725a58236bc0b23af7a7ada610f5f22232d93` |
| T149 | `native-0185.png` | 2524203 | B | 525179 | `7d7af8f0ba19221420bbaf5dfa9f57812b8931c19c5cc1f235debcdab400297a` |
| T149 | `native-0186.png` | 2524236 | B | 514184 | `6029f9d5d7abfadd32f57470897a565e0842a49aee6529353b9c830afb8f8a17` |
| T149 | `native-0187.png` | 2524269 | B | 508098 | `0766e250bdc7c581215f64af89d7c2011a12cfe537c4d6b62172030f61809ff5` |

## Qualitative comparison, including contrary details

The report's numerical floor/column labels and copyright are excluded from
correspondence evidence. "Upper" and "lower" refer to visible scene regions;
no independent floor attribution is newly made. Differences described below
are visual observations, not fitted residuals or quantified flame areas.

| Native index | Foreground composition | WTC 7 plane and dynamic content | Contrary evidence / resolution limit |
|---|---|---|---|
| 77 | Recognizable left banded facade, diagonal lower setback and right brick/ledge edge, but markedly different vertical framing from T148. | Isolated small warm patch and lower window-row warm points recur; the strong upper-fire row is also visible along the image top. | The lower row sits appreciably lower than in the target full composition, and the upper strong row is not present in T148's full composition. Fine warm-point shapes do not establish identity. A possible crop/translation is not ruled out by this full-frame mismatch alone. |
| 91 | Strong T148 coarse layout: left diagonal setback level and both foreground edges resemble the target arrangement. | Lower window band, pale haze above it, small left warm cluster, fainter separated patches and isolated upper warm feature all agree at scene level. | The isolated feature is visibly lobed and soft, whereas the target's feature is a smaller compact point. Fine lower-cluster identity and exact background alignment remain unresolved. |
| 93 | Same close lower framing, with a small apparent horizontal shift relative to 91. | A short group of bright lower points, fainter central/right content, haze and isolated upper patch reproduce the target's separated feature arrangement. | This is a strong candidate, but not visually distinguishable from all neighboring samples at exposure precision. Target contrast/grain differs; no matched mullion residual or fine-shape equality was measured. |
| 95 | Foreground bands and lower setback retain the close T148 arrangement; tiny upper-edge bright content is visible. | Isolated upper patch and lower row's several bright points recur with pale intervening haze. | Fine intensity/lobe changes are small and not an exposure identifier; the faint right-side glow is not demonstrably identical to T148. |
| 96 | Nearly the same apparent framing as 95. | Nearly the same coarse separated warm features and lower haze/window structure. | This review cannot reliably discriminate 95 from 96 at fine visual precision. That is not a decoded-pixel-duplicate assertion. |
| 97 | The same lower-scene foreground layout persists. | Upper warm feature, lower short bright cluster and faint right patch remain visible. | Neighboring-frame similarity limits a unique choice; subtle shape/position changes are not quantified or used to force a match. |
| 101 | The lower framing remains close, without a new distinctive foreground landmark. | The upper warm feature looks more bent/compact and the lower cluster has relatively separated bright ends. | Those visible differences may reflect flame change or image-generation/detail limits; neither an exact match nor exclusion of a related exposure follows. |
| 178 | Upper-scene left setback and projecting ledge, with right brick edge, are close to T149's arrangement but laterally shifted in the full composition. | Two background window bands over the fire row, a clipped left flame, central group and separated right group agree at scene level. | The central right bright lobe appears broader and the rightmost separate form more conspicuous than the target. Intensity adjustment and encoding can alter these appearances. |
| 179 | Very similar arrangement to 178; this PTS was already represented in the one-second review, so it is not a new independent observation. | The same three spatially separated bright regions and upper window bands remain apparent. | Fine dynamic detail is not demonstrably identical, and this arm did not equate the differently encoded PNGs across runs by file hash or re-test their decoded pixels. |
| 185 | Particularly close T149 composition: upper left setback and projecting ledge levels, left facade termination and right brick edge fit the target's scene arrangement well. | Two background window bands and all three separated bright regions agree strongly in placement: left occlusion-edge flame, central multiple bright bases/tongues, right group across a dark separation. | Despite strong agreement, the access copy has broader, brighter and softer lobes than the target in places. Background haze/contrast differs. No unique fine-shape equality or exclusion of 186/187 is demonstrated. Root's favorable leader interpretation was known before this image was viewed. |
| 186 | Upper-scene composition is very similar to 185, with a slight apparent foreground shift. | The same upper rows and three bright groups recur, with a rounded dominant right-hand bright form and central low bright bases. | Similarity to 185 and the target is substantial but not uniquely discriminating; clipping and blur remain. Root context was already known. |
| 187 | Same overall upper layout with another small apparent foreground displacement. | The separated flame groups and upper window rows persist, with small variations in the central and outer-right forms. | This visual review cannot select one original exposure among 185/186/187. Apparent fine differences are not thermometric or a quantitative identity test. |

The strength is **not merely repeated foreground windows**: the small upper
patch plus lower opening row/haze in T148, and two background rows plus three
separated bright regions in T149, supply scene-specific agreement beyond one
grid cell. Nonetheless, foreground agreement does not certify WTC 7 plane
registration. Smoke can contaminate nominal structural regions, the repeated
window grid remains ambiguous, and no independent background transform was
fitted here. No target mask, transform family or threshold was tuned from these
images. The twelve producer-selected views are correlated same-source evidence,
not twelve independent witnesses.

The observed broader/brighter access-copy flame forms are **not evidence that
the report exaggerated fire**. The targets have documented intensity adjustment
and different encoding/generation, and an exact exposure has not been fixed.
Neither apparent color nor these cross-generation brightness differences
measure interior heat, fuel, duration, steel temperature or structural effect.

## Pre-result implementation review and correction record

Before dense result access, the complete initial `check_regions.py` and
`summarize_dense.py` were read against the declarations and target note.
Relevant core definitions were read, not executed. This is an implementation
review, **not this arm's numerical reproduction**.

- `check_regions.py`, SHA256
  `6990064d77887e245b6843c0580679c5e5c9b5e5a262e1f5e8287fb7411a196b`,
  faithfully transcribes all 14 W/D rectangles and all 21 exclusions (9 T148;
  12 T149 including the two extra non-scene exclusions). Four-native-pixel
  expansion, outer-three-pixel exclusion, center-based mask selection,
  fixed best-foreground transform, valid-overlap 85% gate and core minimum
  32-pixel/strict population-variance greater-than-1e-8 gates agree with the
  declared regional method. It retains every declared region, including null
  correlations, and does not refit geometry on flame or background regions.
- Initial `summarize_dense.py`, SHA256
  `f4d37cfd8b5a0b4bc893f5ea57d7fa0c8dcec1a961b006f3db056538ca87f7d4`,
  implements global top-four selection per target/metric with PTS tie breaks,
  and islands by consecutive combined frame index, including chunk boundaries.
  These islands are groups of selected decoded-frame indices, not independently
  authenticated intervals of historical continuity or statistical confidence.
- A concrete robustness defect was reported before results: `ranked[0]` and
  the printed best-PTS expression fail when a metric has no eligible rows.
  The later complete script, SHA256
  `c53783179e50851616a35d12c4f5f05403ea2cb54112df961c439ecce29297d9`,
  was read after image coverage. It handles empty metrics with empty top-four
  and band lists and null best score/PTS. It also uses the declared continuation
  run names and permits the explicitly different first runner while checking
  shared method identity. No empty-metric or continuation test was run by
  this arm, and no actual historical empty-metric failure is alleged.
- Core dependency inspected for the preceding checks:
  `match_screen.py`, SHA256
  `06a400fbb378dfa710dd86799792f8f615a40eea19e82c23b9f3e0592a3b64a8`.
  Review covered its target definitions, save, mask, working-image, canvas,
  scalar-Pearson and registration code, not a full fresh solver/matcher audit.

## Permissible conclusion and stopping boundary

The selected images support a credible visual association of each report
figure with these portions of the admitted access-copy scene. That qualified
positive finding should not be erased merely because perfect reproduction is
unavailable. Equally, this review does not independently certify the numeric
winner, eliminate the neighboring frames, or turn the selected PTS span into
an exhaustive identity interval. All source-relative interval calculations,
full score coverage and reproduction receipts belong to root's separately
reported work and were not recomputed here.

Strong scene agreement can coexist with unresolved frame/exposure identity.
The report's caption clocks and the compilation's original/edit history remain
separate source questions. Failure of an exact match in this transform family
would not prove an invented fire, incorrect figure, timing error, deliberate
alteration or collapse cause. This note stops at the declared 12-image coverage;
no further images or numerical analysis were added. Only this new research
note was created; all prior notes, code, results, sources and main/legal records
were preserved without transmission, source execution or bridge action.
