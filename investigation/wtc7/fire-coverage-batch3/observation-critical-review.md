# Batch 3 observation critical review

2026-09-24. Post-freeze review by the context-limited AI observer
`/root/fire3_observer`. Research only; qualitative image interpretation, not
optical-accuracy calibration, historical authentication, qualified forensic
review, or an accepted building-specific finding.

The fixed record supports visible flame-like activity in several report
representations and substantial limits on what exterior photographs reveal.
It does not establish mild interior heating, severe structural heating, a
whole-building fire extent, or the adequacy of either a fire or intervention
mechanism. The most useful new constraint is a source-qualified collection of
local appearances, including disagreements. It is not a calibrated spread
history.

## Scope, independence and verification

I inspected all 25 complete selected native JPEGs at original dimensions
before reading root labels or source captions. The first two asset rows were
separately frozen and copied unchanged into the full record. General prior
knowledge and source-added image markings limit blindness. Both annotators
are AI readers; their shared model and instructions are potential common
error sources. The disclosed text controls test rule comprehension, not
optical performance.

After both full freezes, I read both complete records, the complete
source-attribution JSON, the source review, and the existing FA-C01-07 audit.
I independently recomputed the five coarse per-image comparison fields in
JavaScript directly from the two JSON records, without calling the comparison
adapter. I also inspected these **complete source-page renders after freeze**:
physical 252, 258, 259, 261, 268, 272, 274, 275, 276, 281, 282, 283, 284 and 286
(printed page = physical page minus 44). These are context checks, not new
anonymous observations. I did not repeat the source reviewer's all-36-page
inspection or read Chapter 9 anew. Chapter 9 propositions below remain the
already source-pinned FA audit's report attributions, not an independent new
verification of those pages.

The 26th fixed target, figure 5-121, is visible on source page 252 but remains
unscored because the declared 17-strip common-scale gate failed. This review
does not cure that failure with a full-page render or a changed tolerance.
The 25-image result is a completed observation sub-study, not satisfaction of
the original full-26 native-representation acceptance gate.

Verified pins using `shasum -a 256`:

| Record | SHA-256 |
| --- | --- |
| `root.json` | `e8e7b7d23e993c68ecc0ee0df16a39a9204d4b0665f9734e08096e21925044c5` |
| `observer.json` | `6c4021bd658cc7f7b64af061c320809cdec1cbe923803a690a12e13d0015e1ac` |
| `source-attributions.json` | `c79c043fd6c0e87505481df94080f6d3a325c74f90e27f870a49f0b69a0cd20d` |
| Main `fire-annotation/source-comparison.md` | `e76e107caefc689435f2fa506f19495ce6a5f462c7543b2d8da9893cb6c2940e` |

Before this review, the observer's `jq`/`cmp` checks confirmed exact 25-ID
manifest order and unchanged pair rows; `shasum -a 256 -c -` verified all 25
selected JPEGs against their key hashes. The observer's construction check
tested every locator for finite numeric coordinates, positive extent and
native bounds. These checks do not measure annotation accuracy. Frozen labels
have not been edited after source or cross-observer review.

## Agreement and disagreements that must survive the summary

Independent recomputation gives nine differences among the 125 coarse fields:
four smoke-status, three flame-like-presence and two bounded-nondetection
presence differences. Target-evaluability and ambiguous-glow-presence match
for every asset. Root has a flame-like entry in nine images; observer in
twelve; nine overlap. These are counts of recorded judgments, not accuracy,
fire prevalence, event independence or matched-feature agreement.

Both readers identify flame-like morphology in figures 5-122, 5-123, 5-134,
5-136, 5-138, 5-140, 5-142, 5-143 and 5-152. Some forms are small or their
facade relation remains uncertain. Agreement is strongest as a claim about
the saved image judgments; the physical interpretation remains conditional
on processing, depth and source attribution.

All coarse-field differences are retained here:

| Asset / figure | Root versus observer | Consequence and competing reading |
| --- | --- | --- |
| A-79c9dd7424ec / 5-145 | Smoke uncertain versus visible. Both use ambiguous glow, limited detail and qualified nondetection. | Root distinguishes smoke from haze/exposure less confidently. Observer identifies an uneven veil. Neither assigns its source. Root's nondetection is upper frontage; observer's is a lower dark patch, so identical presence does not mean the same observation opportunity. |
| A-088afe86559c / 5-144 | No nondetection region versus an upper-band nondetection. | The observer accepts a bounded visible upper patch; root does not. This cannot become an extinction inference. Root also records an upper faint glow at `[214,181,275,209]` that the observer did not identify. Source page 274 explicitly retains reflection as an alternative for the proposed floor-9 reddish appearance. |
| A-7a19d98a72c7 / 5-122 | Smoke not identified versus uncertain. | Both identify flame-like forms at approximately `[155,90,396,176]`. The smoke difference supplies no smoke-origin or ventilation finding. |
| A-c3409ebb7a81 / 5-154 | Smoke uncertain versus visible. | Both identify only ambiguous glows. Page 282 discusses a separate street vehicle fire and derives smoke origin/motion from video. The still and the observer's visible-smoke label cannot establish that origin. The clipped low bright point remains target-relation uncertain. |
| A-c9a2677a3838 / 5-130 | Root ambiguous glow only/smoke uncertain; observer also flame-like/smoke visible. | The disputed middle band overlaps root `[89,211,277,240]` and observer `[89,208,257,244]`. Grain and source intensity adjustment plausibly explain the disagreement. Root's stricter morphology judgment is a substantive counterargument to the observer label, not evidence of a false source caption. Observer also lists two low glows with uncertain depth that root omitted. |
| A-d966352be998 / 5-133 | Root ambiguous glow only plus opaque-surface nondetection; observer additionally flame-like at `[296,194,408,318]` and no nondetection. | Root notes that bright contours often follow material edges; observer identifies local tapered forms. Saturation and illuminated hanging material are a strong alternative to interpreting all bright contours as flame. Neither record supports assigning the whole saturated region to emitting gas. |
| A-e9627d66e7e4 / 5-128 | Root ambiguous glow only; observer flame-like forms in the upper-right and lower bands. | The readers localize much the same bright bands but apply the resolved-morphology threshold differently. Neither is an independently calibrated detector. Preserve the disagreement rather than upgrading the source's fire-intensity prose into a deciding label. |

Coarse agreement conceals several consequential differences:

- **Same glowing patch, different facade confidence:** A-0ca71594109e / 5-146
  has facade-associated glows in root's record and uncertain relations in the
  observer record because of foreground lamps/depth. A-5e0bc6509e6c / 5-156
  similarly has root uncertain and observer facade-associated. Source captions
  are attribution evidence; they do not turn these optical judgments into
  independently established emitting windows.
- **Corner forms:** A-60c26b7f3416 / 5-143 and A-7c7cc22dc34c / 5-142 have
  largely overlapping flame-like locators, but root keeps the emitting plane
  uncertain while the observer uses `on_candidate_facade`. The image evidence
  supports a form near the apparent corner more strongly than an exact emitting
  face, opening, or depth. Page 272 separately leaves the lower plume's
  fire-versus-transported-smoke origin unresolved.
- **Broad boxes conceal mixed morphology:** A-aa662f5d0d91 / 5-140 has the
  observer's broad flame-like box `[161,221,655,313]`; root separates a clearer
  left portion `[165,267,339,312]` from an ambiguous right portion
  `[342,228,666,287]`. A-5394db776a29 / 5-136 likewise has observer's broad
  flame-like band beginning at x=95 while root separately labels the far-left
  band ambiguous. No conclusion that every bright point or the full rectangle
  is flame follows from the shared per-image presence flag.
- **Morphology scope is not identical even in a close-up:** A-36ed8ce42d01 /
  5-138 has root's lower flame-like locator `[213,288,437,393]` and two narrower
  observer lower locators. Both separately retain broad smooth orange glow.
  The source labels the view floor 8; it is not a floor-12 or floor-13 thermal
  close-up. The source's video-based smoke-flow and interior-pathway statements
  go beyond this still.

## Source joins and misleading denominators

No figure-to-asset mismatch was found in the 14 source pages I directly
rechecked. In particular, physical 258 has 5-128/A-e9627d66e7e4 above and
5-129/A-134e75612bed below; physical 261 has 5-132/A-287293e9806e above and
5-133/A-d966352be998 below. On physical 252 the 17-strip upper figure is 5-121
and the separate lower JPEG A-7a19d98a72c7 is 5-122. This limited result is not
a claim that I independently repeated all source-review associations.

The source join correctly preserves several material qualifications:

1. **Same exposure, different visible detail:** Page 259 explicitly identifies
   5-130 as an intensity-adjusted enlargement of 5-129. Neither reader identifies
   luminosity in the small complete 5-129 asset; both identify warm features in
   5-130, while morphology differs. The pair demonstrates representation-limited
   observation opportunity. It is not two independent corroborating photographs,
   a calibrated detection experiment, or proof that any image processing is
   deceptive.
2. **Floor list is not a burning-floor list:** `report_attributed_floors` lists
   discussed/visible floor locations. It must not become a count of burning
   floors. This is especially important for 5-152 (labels 12-17), 5-142
   (the ambiguous lower plume near 5/6), and the expressly conditional
   floor-14 placement for 5-153 on page 281.
3. **The pair's clocks are model-relevant assumptions:** Page 274 derives the
   approximate 5-145 time from a proposed 15-minute difference and a typical
   roughly 20-minute intense-burning duration. Page 275 assumes ten minutes
   from 5-145 to 5-146. The 5-145 caption's +/-5 minutes must retain the prose's
   at-least-five-minute qualification. This pair cannot independently validate
   the burning duration used to assign its times. Conversely, that dependence
   does not establish that the estimated times are false.
4. **Late sequence does not supply a complete extinction clock:** Page 283's
   qualified interpretation of no major fire over the visible width in 5-155
   does not assert all rooms were cold. Both readers retain no luminous entry
   in this small, partially obscured view. The 5-156 caption's +/-120-second
   interval extends past the source's collapse reference and remains an
   attributed estimate. The tighter 5-159 +/-15-second interval is not an
   independently checked synchronization in this batch.
5. **Source-family dependence survives differing credits:** Many CBS and
   Rabanne representations come from related sequences. The source attribution
   keeps Unknown for 5-152 and must not import Fox credit from context imagery.
   Neither 25 filenames nor the remaining unique representations establishes
   25 independent exposures, independent clocks, or independent fire events.

## Implications for the seven source-input questions

The controlling question definitions and Chapter 9 pins are in main
`research/sherlock-wtc7-investigation/fire-annotation/source-comparison.md`.
This batch adds appearances and attribution dependencies; it does not execute
the missing native-input comparisons.

| Question | What this batch can change | What remains untested |
| --- | --- | --- |
| FA-C01: prescribed/interpolated ventilation | New window/frontage views offer additional candidates for a source-to-window observation table. The clock audit makes dependent interpolation validation a concrete risk. | Whether each input breakage time matches independently timed observed window state; exact missing/hidden glass, interpolation bounds, and thermal consequences. A luminous feature is not itself a window-state measurement. |
| FA-C02: uncertain initial ignition and chosen initialization | Later appearances constrain whether proposed simulations reach the observed local frontages under supported times. | South-face noon ignition location/power, hidden early development, and the chosen second floor-8 ignition. Later flames neither demonstrate nor refute the specified initiating fire. |
| FA-C03: overlong modeled floor-12 north burning | Early/middle floor-12 attributions, including 5-122/123, improve the list of comparison targets; late limited views preserve local nondetections and ambiguous glows. | Independently measured duration mismatch, continuous extinction, core-versus-curtain-wall heat and any numerical temperature correction. New earlier fire evidence does not erase the separate acknowledged later-duration mismatch. |
| FA-C04: shifted floor-12 histories used for floors 11/13 | 5-134 and 5-152, plus 5-153/154/156/159's qualified placements, offer floor-specific appearance/time targets. Their dependencies and uncertainty must carry into the comparison. | Validity of one-hour/half-hour shifts, true floor layouts/fuel, integrated heating, connection response or the report's mild-heating-error judgment. A close view attributed to floor 8 cannot validate floor 13. |
| FA-C05: unconfirmed south-side spread | No resolving south-face exposure has been added by these selected north/corner/limited west views. | Whether unobserved simulated south burning occurred and its thermal consequence. The coverage gap is not evidence of absence or affirmative confirmation. |
| FA-C06: existing sensitivity checks versus coupled uncertainty | The new source-qualified observations clarify which quantities a future sensitivity comparison must reproduce. | This image review adds no fuel, ventilation, partition or heat-transfer sensitivity run. It neither supports a claim that no tests existed nor independently validates a spread-rate result's downstream structural implications. |
| FA-C07: fire-to-thermal transfer and gas/steel distinction | The evidence reinforces the need to keep photograph appearance separate from computed heat and member temperatures. | Exact heat-flux histories, FDS-to-thermal/member mapping, insulation effects, steel temperatures, structural capacity and collapse initiation. Neither flame hue nor an empty luminous list measures them. |

## The strongest defensible response to a mild, localized-fire premise

The premise needs two separate quantities. If **mild** means low heat release
or insufficient member heating, these images do not establish it. If it means
only tiny or inconsequential-looking visible activity everywhere, several
views with resolved extended luminous forms are direct counterexamples within
their pictured regions: 5-122, 5-138 and the 5-143 corner view are particularly
clear examples, with 5-134/136/140 supplying broader frontage context. Their
brightness still does not measure thermal severity.

If **localized** means spatially restricted at a particular instant, these
images contain localized bright bands and large unobserved regions, but no
calibrated denominator for the whole building. Selected views at different
and sometimes inferred times cannot be pooled into one simultaneous burning
area or a count of burning rooms. A close-up can look dramatic while covering
little of a floor; a distant dark photograph can hide active fire. The
5-129/130 same-exposure relationship provides a concrete warning against
inferring severity from whichever representation looks calmer or brighter.

The strongest objection to an overly fire-favorable reading is therefore
specific: visible fire does not demonstrate the relevant member temperatures,
that floor-12 substitutions faithfully reproduce floor 13, or that the
initiating connection sequence occurred. The strongest objection to an
overly fire-minimizing reading is also specific: weak or absent exterior
luminosity in a small obscured still is not evidence of weak interior heating,
and several selected local views plainly support flame-like activity.

The current bounded statement is: **the record contains substantial visible
fire activity in particular pictured regions, but this qualitative batch
does not measure interior severity or establish the proposed causal chain.**
Here substantial is a description of resolved visible forms, not a quantified
heat, area, duration or structural-capacity judgment. Where that adjective
would be mistaken for a measurement, use the exact asset-level descriptions
instead.

Confidence is high in the preserved comparison and documented attribution
dependencies, conditional on the verified source bytes. Confidence in any
individual borderline morphology or exact facade relation is lower and
explicitly disputed. Authenticated original/adjacent frames, independent
clock and geometry anchors, qualified review, and source-matched native
fire/thermal histories could change those conclusions. No cause odds,
intent finding, legal conclusion, model certification or goal completion is
supported by this review.

## Checks for the forthcoming report

Keep the 25-of-26 coverage limitation explicit; distinguish nine shared
flame-like-presence judgments from matched physical features; retain the
three morphology disagreements and important relation/scope disagreements;
keep same-exposure and clock dependencies visible; retain both the reported
model mismatches and the existence of sensitivity work; and do not convert
the phrase mild localized fire into an observed thermal quantity. Do not
change frozen labels to resolve these concerns. The source-of-truth and
evidence-audit skills keep this review a working research derivative.
