# Independent synthetic raster method and implementation review

2026-09-27. Working research only. This is a prior-informed computational
review, not a blind study, human source spot-check, historical uncertainty
calibration, expert certification, or permission to trace a historical plot.

## Scope and method decisions before producer outcomes

Read the current main CHARTER and this unit's PROTOCOL,
NUMERICAL-PROTOCOL, HUMAN-REVIEW-GATE, REGISTRATION-STAGE and
RASTER-UNCERTAINTY-STAGE. Reviewed the producer's complete renderer/probe/report
implementation and focused tests. No historical pixels, source drawings,
solver, matrix, original annotations or external sources were opened.

The fixed product is 7 colors x 2 widths x 2 slopes x 2 phases x 2 styles:
112 bases, each with five codecs, hence 560 cases. Before results, this
review requested explicit half-up rounding, subpixel centers, line-edge
inclusion, half-open support endpoint bounds, and independently rendered
latent ambiguity scenes. The declaration now specifies these conventions and
calls its 4x4 operation point sampling rather than exact analytic area coverage.
It also explicitly limits the probe to known-color isolated synthetic lines,
not rejection of text, grids, mixed-color traces or historical style identity.

Final declaration SHA-256:
`4adaa3b617a624de9353feda130c1778e0c60d00e133d88754f66baa3298b248`.
No threshold or fixture membership was changed in response to outcomes.

## Separate implementation and actual verification

[raster_independent_check.py](raster_independent_check.py) imports no producer
predicate, component, envelope or renderer. Its color decision uses exact
rational projection and residuals; consecutive row runs use a separate
grouping implementation. It regenerates the seven selected base RGB arrays
with integer-scaled sample coordinates. It independently renders six ambiguity
scenes using rational sample-point/band tests, then uses the declared codecs.
Decoded pixels are evaluated before the corresponding producer result is read
for comparison. Every selected column field, expanded envelope, width,
coverage decision and summary list is compared exactly.

This is implementation independence within a shared specification, not
historical independence. Root and reviewer exchanged method feedback before
the runs; root separately checked exact mixtures and sample geometry before
outcomes. The checker was written with access to producer code/schema. Both
implementations use Pillow and the same JPEG library for codecs; no independent
codec was implemented.

The producer's two runs were confirmed complete before this checker read run01.
The reviewer did not poll partially written images or receipts. The fixed
sample is all seven colors at w=1, m=1/2, p=1/2, dashed, across five codecs.

Commands actually executed, using the bundled Python executable at
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`:

```text
python3 -B raster_independent_check.py --self-test
python3 -B raster_independent_check.py --run synthetic-run01
```

Both exited 0. The run command prints JSON and writes no files; its exact
stdout was saved with apply_patch as
[raster-independent-check01.json](raster-independent-check01.json).

- 35 selected cases; 4,480 complete column records compared, including all
  four allowance results per column, with zero mismatches.
- Seven independently regenerated base RGB arrays matched the producer pins
  and the lossless PNG pixels.
- Three ambiguity pairs: six separate latent scenes independently rendered;
  all three base equalities and all 15 codec pair equalities reproduced.
  All 30 independently re-encoded side images matched the saved encoded bytes.
- 31 independent-checker boundary controls passed. These include exact contrast
  and off-color boundaries, blank input, half-up rounding, row/cell boundaries,
  disconnected support, all four allowances, and malformed RGB rejection.
  They test this checker; they are not additional independent executions of
  the producer's boundary API. The producer's focused test source was read;
  root owns its reported focused-test replay.
- 107 consumed run files were pinned and unchanged during the audit. Current
  producer/control input pins matched its before/after manifest pins.

Runtime: Python 3.12.14; Pillow 12.3.0; JPEG codec 6.2;
libjpeg-turbo 3.1.4.1. Checker SHA-256:
`6013e91b8f2ffa31daf8cd216d868575407df62a4c627e021b0fa79f575dd559`.
Producer SHA-256:
`878872fcde4316e2655e156221de970a41f5186351a9525159c7eb7520e8760f`.

## Retained checker defect and correction

Before producer outcomes, root found a defect in initial checker SHA-256
`a6d73136743bc7c35b577dd14571ba9593e1492469bf38fd6b584cd23960be27`:
the cache decorator ran before RGB validation. After a valid integer-pixel
call warmed the cache, equal-valued boolean or float tuples could reuse that
result without validation. Root demonstrated the problem in a stdout-only
check; the initial 18 self-controls had missed it.

Validation was moved to an uncached public wrapper. Added warmed-cache tests
reject both invalid pixel tuples and invalid target tuples. Added blank,
ambiguity, full-cell and gap-boundary controls brought the final total to 31.
All passed before the independent comparison. The correction changes malformed
input handling, not the valid-pixel predicate, thresholds or selected fixtures.
Initial self-controls also ran under Python 3.13.7/Pillow 12.0.0; the saved full
audit and final self-controls used the bundled runtime identified above.

An initial attempt to read the producer test file occurred while that file was
still being authored and returned missing-file status. It was subsequently
read in full after it had been written, before either full-run dataset was
examined; no absence or verification claim was based on the initial attempt.

## Selected-sample results and limits

Each codec row below covers 448 true-support columns and 448 true gap columns.
These are repeated pixel-column observations from seven deliberately selected
fixtures, not independent statistical trials or a sample of historical graphs.

| Codec | Missing | Ambiguous | Single run | Zero-allowance enclosed | Zero-allowance enclosure failure |
|---|---:|---:|---:|---:|---:|
| PNG | 0 | 0 | 448 | 448 | 0 |
| JPEG 95, 4:4:4 | 0 | 0 | 448 | 448 | 0 |
| JPEG 75, 4:4:4 | 8 | 0 | 440 | 424 | 16 |
| JPEG 75, 4:2:0 | 56 | 0 | 392 | 64 | 328 |
| JPEG 50, 4:2:0 | 96 | 4 | 348 | 84 | 264 |

Across this sample, 160 true columns were missing and four were ambiguous;
2,076 were single runs. The zero allowance enclosed 1,468 and failed enclosure
for 608, leaving 164 unassessed. Allowances 1, 2 and 4 enclosed all 2,076 single
runs in this finite sample, while the same 164 columns remained unassessed.
This does not select one pixel as a calibrated uncertainty allowance: wider
intervals necessarily sacrifice precision, and numerical expansion does not
recover missing identity or support. All allowance widths remain in the pinned
producer column records. No candidate appeared in the 2,240 selected gap
columns; that is not a claim about all 560 cases or historical dash gaps.

The three constructive controls establish limited ambiguities in the stated
latent scene class:

1. A dashed red line and a solid red line hidden at the same gap rectangles
   yield identical sampled pixels. This does not classify a historical gap.
2. Two same-color crossing lines preserve the visible union when their labels
   swap branches at the crossing. Additional source labels or justified
   continuity constraints could distinguish hypotheses; pixels alone do not.
3. An absent line and a line hidden completely by opaque white yield identical
   observations. This concerns possible occlusion, not proof of hidden content.

Independent encoded and decoded equality across five codecs verifies that
these transformations preserve each constructed ambiguity. It is not five
independent identifiability findings or evidence that these scenes occur in
the historical source.

## Disposition

No unresolved producer/checker discrepancy was found in the fixed sample or
the three constructions. This review does not reproduce every case in the
560-case sweep; root owns the complete-run replay and output comparison.
It also does not test arbitrary scenes, mixed-color contamination, every
subpixel phase, real JPEG history, curve continuation, interpolation or the
historical coordinate mapping.

The next historical prerequisites remain actual human axis/legend and selected
source-to-coordinate spot-checks; native linewidth/color and image-transform
characterization; explicit visible-support declarations; and a separately
declared, tested rule before any dash-gap bridging. Neither the synthetic
controls nor this review clears HUMAN-REVIEW-GATE or changes a cause ranking.
