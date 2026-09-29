# Camera 3 tape endpoints and facade repetition

The saved calibration has **positive image support for its approximate scale,
but not two independently identified architectural endpoints**. Its upper
query is near a facade stripe transition below the large dark upper-facade
rectangle. Its lower query falls at the transition to a bright foreground
obstruction, where a clean background window/floor endpoint is not resolved.
Two separately frozen initial descriptions agree on this visibility problem;
they do not independently agree on an exact interval count.

A declared pixel-repetition test adds useful contrary evidence to dismissing
the calibration outright: the visible facade strip to the left of the
obstruction has a best integer repetition lag of **13 pixels** in every tested
frame/window/method. The tape's vertical separation is approximately 194.49
pixels, or about **14.96 such cycles**. That is consistent with the lab's
fifteen-regular-floor-interval calibration, but does not prove that each image
cycle is a storey, identify its endpoints or validate the original analysis.

This is research-only progress on Q03/Q04/Q05/Q10, not a new acceleration,
force, structural-model or cause result. The [protocol](PROTOCOL.md),
[profile declaration](PROFILE-DECLARATION.md), preserved observations and
[validation](validation.md) define the finite scope. The preceding
[metric-motion audit](../metric-motion-audit/report.md) remains unchanged.

## Direct image evidence

The source is the preserved public kit `Camera3.wmv`, SHA-256
`48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722`.
Its outer and nested copies are byte-identical. The sanitized project names
that basename and records 442 frames. This supports present-file
correspondence; it does not reproduce the historical Tracker decoder, raster
conventions, time table or original camera exposures.[^1]

The selected diagnostic indices were fixed before new images were viewed:
138, 141 and 168, at inherited encoded times 9.2, 9.4 and 11.2 seconds. A fresh
complete decode matched the prior 442-frame grayscale stream and every
per-frame hash. Only these three new native frames were visually inspected;
the other 439 frames were not newly viewed. The selection tests early
calibration context, not the earliest collapse onset or the whole event.

Frame 138, native grayscale, without analytical marks:

![Camera 3 diagnostic frame 138, unmarked native grayscale](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera3-calibration-endpoints/run01/frame-0138.png)

The saved queries are approximately `(414.3771,196.2404)` and
`(416.9570,390.7277)`. These decimal coordinates are saved settings, not newly
measured landmark positions. Both analysts inspected three complete native
frames and three unmarked 3x context crops before comparing their written
descriptions. Both later inspected the twelve endpoint-refinement displays.
Nearest-neighbor enlargement repeats pixels; it does not recover detail.[^2]

| Query | Separately recorded image observation | What remains unresolved |
|---|---|---|
| Upper | Repeated facade bands below the dark upper rectangle, not the parapet. Refinement places it near the pale-to-darker stripe transition. | Whether that phase represents a window top, window bottom, slab level or another facade component; absolute floor number. |
| Lower | At/near the left edge of a bright foreground structure, with background banding immediately to its left. Refinement preserves the occlusion-boundary association. | A clean second background-building marker; whether a visible row was extrapolated behind the obstruction; exact architectural phase and depth. |

The following separate display repeats the lower neighborhood of frame 138
at 12x and marks the **saved-coordinate query** with a red cross. The mark was
not present in the recording and is not a new feature localization. The
[unmarked patch](refinement01/lower-0138-unmarked.png) remains preserved.

![Diagnostic saved-query overlay at the lower endpoint, not historical image content](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera3-calibration-endpoints/refinement01/lower-0138-query-overlay.png)

The marker uses a declared integer-pixel-centre display convention. A
pixel-corner convention moves it by less than one native pixel. Blur and
mixed boundary pixels are additional limitations. It is defensible to call
this an occlusion-boundary neighborhood, but not to decide the exact physical
side from the cross's many decimal digits.

The separate observer initially reported a subjective **14–16-cycle** span,
with about fifteen plausible when following bands just to the left. Root's
initial note explicitly withheld a reliable endpoint-to-endpoint count.
Those positions are preserved in [root observations](root-observations.md)
and [independent observations](independent-observations.md). They must not be
reported as two independent confirmations of fifteen. The
[refinement review](refinement-review.md) records the later comparison.

## Pixel-repetition result

After those first-pass notes were frozen, the [exploratory declaration](PROFILE-DECLARATION.md)
fixed a strip at columns 402–411 and rows 202–384, to the left of the lower
obstruction and excluding both exact query locations. Its per-row mean uses
ten original grayscale pixels. No image was deblurred, retimed or filled in.

The calculation tests every integer lag 8–18 in the full 183-row profile and
its fixed 91-row/92-row parts, both with and without a linear trend removed.
All profiles, row sums and **198 lag correlations** are retained in
[profile01.json](profile01.json). Nine finite synthetic controls test known
periods and undefined constant/detrended-ramp cases before historical data.

| Frame | Full strip, raw / detrended | Upper part, raw / detrended | Lower part, raw / detrended |
|---|---|---|---|
| 138 | 13 / 13 pixels | 13 / 13 pixels | 13 / 13 pixels |
| 141 | 13 / 13 pixels | 13 / 13 pixels | 13 / 13 pixels |
| 168 | 13 / 13 pixels | 13 / 13 pixels | 13 / 13 pixels |

The correlations at those maxima range approximately 0.9280–0.9717. These
are correlation coefficients, **not probabilities, confidence levels or
eighteen independent measurements**. The windows and transforms reuse the
same pixels; the three frames share a source and almost the same facade.
An integer-lag maximum also does not measure subpixel period or establish a
historical projection-error interval. Equal maximizing lags in upper/lower
windows do not prove an affine camera model.

The approximately 194.49-pixel **vertical** query separation divided by 13
is approximately 14.96. This compares a fixed-column repetition with a
slightly slanted query-to-query span, not a direct count of identified
endpoint phases. The result supports the approximate fifteen-cycle reading
without resolving the occluded endpoint. It is stronger than scalar
floor-sheet agreement alone, but weaker than a physically validated scale.

## Dimensional alternatives and their consequences

The public lab procedure uses separated floors and supplied dimensions. The
prior primary-page audit found that 58.293 m = 191.25 ft = fifteen 12.75-ft
intervals; seven floor-level pairs share that separation. The floor sheet
also includes nonuniform storeys. None of the current images supplies a
verified floor-number/drawing join. See the complete
[calibration-source review](../metric-motion-audit/calibration-source-review.md)
for that source and its exact limits.[^3]

Two interpretations remain live:

1. **Corresponding repetitive features, about fifteen regular intervals
   apart.** The saved length, image repetition and approximate visual count
   are coherent with this account. The lower point might have been selected
   by extending a visible band into the obscured region. The present record
   does not document that selection procedure or establish equal endpoint
   offsets from actual floors.
2. **Unlike phases or a count/feature error.** The upper architectural phase
   is not identified and the lower query is not a clean target marker. An
   off-by-one assignment or inappropriate foreground reference is possible.
   Possibility is not proof that an error occurred. The strong near-13-pixel
   repetition is contrary evidence to treating the assigned scale as
   arbitrary or wholly unsupported.

For transparent sensitivity only, if the same pixel span represented 14,
15 or 16 **equal 12.75-ft physical intervals**, the assumed lengths would be:

| Assumed interval count | Assigned physical span | Scale relative to the saved 15-interval assignment |
|---|---|---|
| 14 | 54.4068 m | 14/15, approximately 0.9333 |
| 15 | 58.2930 m | 1 |
| 16 | 62.1792 m | 16/15, approximately 1.0667 |

With all other geometry, image curvature and clocks held fixed, a physical
acceleration estimate would scale by the same factors. This is **not** a
measured ±6.7% calibration uncertainty, a correction to any published result,
or evidence selecting 14 or 16 over 15. Neither the observer's coarse count
nor the integer-period diagnostic supplies that probability distribution.
Unmatched stripe phase and projective depth are separate uncertainties.

## Claim ledger and next physical test

Grades apply to the narrow proposition, not a complete collapse explanation.

| Claim | Layer / strength | Alternative and discriminator |
|---|---|---|
| These selected pixels reproduce the preserved diagnostic. | Derived integrity result; A for byte correspondence. | A different source, decoder result or selection breaks the join. Source authenticity and old runtime equivalence remain separate. |
| The lower saved query identifies an unoccluded target-floor endpoint. | Contradicted as a clean-visibility description in these frames; no physical endpoint identity established. | The intended feature may continue behind the foreground. A source-linked calibration annotation or clearer exact-source image could establish the intended construction. |
| The visible strip has an approximately 13-pixel repetition scale under the declared diagnostic. | Derived; A for the specified arrays/calculation, limited to integer lags and selected strip. | Changing phase, heterogeneous bands or a different strip may alter the diagnostic. All method/window outcomes are retained. |
| The tape spans fifteen physical floor intervals with a validated length. | C as a coherent conditional assignment; D as independently verified historical calibration. | Repetition need not establish floor identity, equal offsets or the hidden endpoint. A drawing/image crosswalk or independently identified visible reference pair is needed. |
| Foreground overlap proves the calibration was erroneous or contrived. | Unsupported. | Extrapolating a visible row is an ordinary alternative; the repetition/length agreement is affirmative contrary evidence. Evidence of the actual construction, not intention inferred from an anomaly, is needed. |
| This result establishes g, universal support loss or a cause. | Not established; no historical trajectory or force model fitted. | Those require separately specified physical calibration, timing, moving-system identification and mechanism-discriminating evidence. |

The next substantive task should **produce a conditional trajectory result**,
not another generic calibration checklist. Declare a reproducible export of
the public project's actual two marked-point arrays and their nominal saved
analysis clock, keeping raw private path fields excluded. Cross-check selected
points against the images; compare reasonable fit windows and a new visible-
reference calibration where feasible, retaining the original 15-interval
assignment and clearly labelled alternatives. Do not tune scale, onset or
time mapping to obtain g. Report what remains true across those assumptions
and what fails. Until the charter's human/physical-calibration gates are met,
this remains an exploratory, explicitly conditional reconstruction—not a
consequential finding about forces, cause or intent.

The exact higher-quality calibration image/drawing and original loaded
point/time export remain valuable discriminators, but imperfect provenance
does not prevent testing the stated public analysis conditionally. No new
production/held-packet content, structural model execution, legal-record
promotion, bridge, outreach or causal-ranking change occurs through this
image-source unit. The broader investigation remains active and incomplete.

## Sources

[^1]: Preserved public kit [Camera3.wmv](</Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/outer/The Kit/WTC7-Camera 3/videos/Camera3.wmv>), source hash stated above; prior [WMV diagnostic](/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-recording-comparison/wmv-diagnostic/report.md) and new [run01 receipt](run01/receipt.json). These are an access copy and its derivatives, not independent cameras or authenticated original exposures.

[^2]: [Sanitized public saved settings](/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/saved-tracker-settings.json), SHA-256 `ccfd9c4de098539680caf9f296eb5ea784ade27497d860a32284285e577cefeb`; selected native/query-display identities and coordinate conventions in [independent product review](independent-products.md). The original project XML and private author-machine path fields were not opened in this unit.

[^3]: David Chandler, [public lab instructions](/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/outer/Lab-Instructions.pdf), p. 3, and [Elevations of Floors of WTC 7](</Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/outer/The Kit/WTC7-Camera 3/WTC7 Floor Spacing.pdf>), one-page kit sheet. Their source hashes, prior complete-page viewing and seven-pair enumeration are recorded in the linked metric-unit calibration-source review. No new PDF-page viewing or independent architectural survey is claimed here.
