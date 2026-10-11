# Dense first-shot picture refinement

October 7, 2026. Prospective for this dense scoring stage, not a blind
preregistration or independent holdout. The parent picture pilot has already
identified a first-shot lead around earlier-copy seconds 12–16. This is a
conditional refinement of that lead with two seconds of padding, not a
source-wide search or a new independent item of corroboration.

## Fixed scope and dependencies

Use every presented frame in earlier-copy PTS [10,18): expected source indices
300 through 539 inclusive, 240 frames. Use the unchanged C first-shot references
at local seconds 0, 2 and 4, compilation indices 12900, 12960 and 13020.
The earlier video, C video, C extraction map, parent configuration, numerical
core and parent adapter retain the pins in the parent packet. The new driver
must verify those pins before imports/use and preserve them afterward.

Extract twice using the unchanged, pinned native-frame extraction helper,
full-input decoding and exact rational PTS, into new extract01/extract02
directories. Run its existing zero/nonzero-origin synthetic controls each
time. Verify 240 selected indices, dimensions 320×224, time base 1/30000 and
nominal rate 30000/1001. Compare the eight overlapping coarse samples at
integer seconds 10 through 17 exactly. A separate sequential decode of all
1130 presented frames must compare all 240 selected raster pixels from both
runs, without using the producer's selection helper. Preserve stderr, command
receipts, code/runtime pins, generated maps and eight overview sheets per run.
Unique decoded PNGs do not establish unique original-camera exposures.

## Inherited scoring; no retuning

Retain exactly the parent's first-shot crop [120,0,1170,720), static rectangles
[750,330,1140,680) and [170,490,380,640), and dynamic rectangle
[260,20,680,315). Use all parent scales, translation grid, working dimensions,
Pillow grayscale/bilinear transformations, coverage/count/variance gates,
static-selected two transforms, tie rules, and descriptive near-best sets.
The new thin driver imports the parent's verified functions; it must not
monkeypatch the parent configuration or rewrite the prior packet. The parent
protocol remains the full numerical method specification. Its first masks
contain 4786 static and 3528 dynamic pixels, with no overlap.

Compute all 720 pairs, preserving the complete 21×51×51 static-score and
coverage surfaces, both retained transforms, and dynamic scores evaluated
only at static-selected transforms. The primary dynamic ranking uses the
best-static transform. Save full rankings and near-best sets within 0.005,
0.01 and 0.02 of each best score. These sets are not confidence intervals or
independent observations: adjacent compressed video frames are correlated.
Report their contiguous source-index bands, ties and endpoint leaders without
changing selection rules. Do not select the result that best fits a timing
expectation. No threshold converts a correlation into proof of identity.

Use the same pinned Python 3.13.7 / NumPy 2.3.4 / Pillow 12.0.0 runtime in both
new runs. Each extraction and scoring run has a 600-second wall-time cap and
384-MiB output cap (not an RSS-memory claim). Preserve incomplete failures;
do not silently raise caps. Native synthetic containers may differ in metadata;
historical PNGs/maps/sheets and all score products must reproduce exactly.
Map both score runs to extract01's verified immutable map so incidental
directory names cannot create apparent scientific differences.

## Tests and independent checks

Before historical scoring: separate protocol critique; fresh 11 inherited
core controls and all nine parent adapter tests, including the unchanged-
scenery/changing-image sequence control; new dense wrapper tests for source
indices, PTS endpoints, duplicate/missing/malformed input rejection, exact
3×240 Cartesian coverage, and stale controls/output refusal. Use synthetic
test data, not historical scores. Record any repair and rerun relevant tests.
Duplicate rejection concerns source indices/map entries, not equal raster
content: genuine repeated pictures remain valid inputs and are reported.
Controls must bind to current driver/test/protocol/config/dependency/runtime
pins. Verify source and selected-frame hashes before and after execution.

Independently recompute all selected static/dynamic scores by direct summation,
without importing the scoring producer or its numerical core. Tolerances stay
1e-9 absolute score error and 1e-12 coverage error. Check all 720 pair memberships,
complete saved-surface top-two selections, all rankings/near-best sets and both
run product equality. This checks selected arithmetic, not an independent
recomputation of every FFT search cell. A separate checker may reuse its own
already reviewed arithmetic functions; shared Pillow resampling is explicit.

For each reference, inspect the union of the top two static and top two dynamic
candidate frames, at most 12 unique source frames, alongside the three native
C references. Root and a separate computational reader retain their first
observations separately: stationary detail, distinctive changing cloud
outlines, contradictory contours, crop limitations, movement and ambiguity.
Neither reader is blind or a qualified human acceptance authority. A numerical
leader that disagrees outside the mask remains a disagreement, not a license
to select another frame for a preferred timing fit.
Top-two choices may cluster in one near-identical band. Other near-best bands
not included by this fixed shortlist remain visually uninspected alternatives;
the bounded review cannot establish uniqueness against them.

## Permitted result and stopping point

The deliverable is a source-pinned report of whether dense sampling strengthens,
weakens or leaves unresolved the shared-picture-material lead, with all close
alternatives and limitations. Exact exposure or sequence identity remains
unresolved unless distinctive changing details actually discriminate it.
Identical/near-identical exposures, interpolation, common processing, nearby
camera/time and selection bias remain alternatives. No image-based rate fit,
time map, original clock, audio processing/matching, sound classification,
source authentication, acoustic silence, cause ranking, Sherlock/Faraday
acceptance, legal promotion, external disclosure or commit/push is authorized
by this stage. In particular, C's approximate bang at local 13 seconds is in
a different shot and cannot inherit a first-shot picture match.

The full investigation charter remains active and incomplete. Stop this stage
after two runs, independent verification and bounded visual review; any wider
search, changed masks or audio-rate analysis needs a separately declared test.
