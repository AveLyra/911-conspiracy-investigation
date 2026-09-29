# Stage B: fixed-interval conditional visible-event timing

Declared September 20, 2026 UTC, after Stage A's partial identity pass and
before new extraction or endpoint annotation. Published event values, source
figures and previous Camera 2 work are known. This is prior-informed testing,
not a blind benchmark or a new source-independent camera authentication.
The main controls and full charter continue to govern.

## Scope and acceptance

Use only the held Camera 2 MOV pinned in PROTOCOL.md. Select every stored frame
whose **exact rational PTS time** lies in the closed interval [220,234] encoded
seconds, plus the immediately preceding and following frames. Read-only
selection from the held map establishes 419 interior +2 bounding =421 frames,
indices 6593–7013 inclusive. Verify this independently in the new driver; do
not extend the interval because a result is inconvenient. No metrical scale,
audio, new camera, new acquisition or solver is included.

Acceptance has separate levels: (1) verified extraction; (2) explicit actual
visual coverage and independently frozen annotation; (3) correctly calculated
bounded interval or declared non-identifiability; (4) limited comparison with
published quantities. A passing extractor does not imply levels 2–4. Human/
specialist acceptance, original clock and causation remain outside these
automatic levels. An inconclusive endpoint is an allowed scientific result.

## Extraction and method controls

Use a thin Camera 2-only driver reusing the existing pinned extractor's
`inputs`, `read_map`, `decode` and `sheets` functions. The old two-camera CLI
and fixed-output verifier must not be run unchanged. Do not change main's
historical code, protocol, verifier or outputs. Pin the new driver, this
declaration and imported code; snapshot actual runtime dependencies and the
old method separately as inherited implementation context.

Decode from the source beginning without seeking or retiming; verify all 8,042
decoded YUV420P frame hashes against the held inventory, not merely the 421
selected frames. Save native 640×480 luminance PNGs with no enhancement,
interpolation, stabilization or overlays. Preserve exact index, PTS, duration
and timebase. Use inherited whole-image overview sheets only for navigation;
their reduced raster cannot certify a fine outline boundary. Native frames
must be inspected for asserted endpoint brackets and ambiguous alternatives.
Any later crop/overlay display pass must have its own prospective bounds and
lossless transform declaration; none is authorized silently by a contact sheet.

Keep the inherited watchdog and strict diagnostic classification. Separately
retain the known unmapped PCM stereo-layout guess and every raw diagnostic.
Unexpected lines, extra warnings, timing/hash/geometry mismatch or partial
decoding fail admission; matching repeated pixels cannot cure a failure.
The inherited grammar accepts repeated matching lines, so the new driver must
require **exactly one** known layout-guess line for this source, matching the
historical clean video-only executions. Zero or multiple lines need a separately
declared diagnostic review, not silent acceptance. No audio inference follows.

Rerun the inherited eight synthetic controls using a fresh new-unit output
directory. Add driver tests before historical extraction: exact rational closed
interval selection, predecessor/successor coverage, monotone and strict integer
index validation, missing bounds, wrong dependency pins, output collision,
failure receipt and one-camera-only behavior. Synthetic driver tests should
inject a fake decoding adapter, not use historical pixels. Preserve failures.
Run historical extraction twice into previously absent run01/run02. Compare
all deterministic PNGs, selection rows and complete raw-stream digests. Pin
address-bearing diagnostic files separately; do not demand their byte equality.
Record commands, terminal statuses and actual test counts.

## Visual and event definitions frozen before endpoint inspection

Initial candidate areas are broad, overlapping *search regions*, not exact
component polygons: east-penthouse area in the left portion of the target
roof, screenwall in the middle, west-penthouse area/upper right step to the
right, with the lower north facade/parapet in front. Stage A's source geometry
and baseline, not the desired event time, supply those identities. Do not
substitute the screenwall, smoke edge or outer parapet corner for a penthouse.

Two AI observers should each inspect the complete selected-frame overviews,
then declare candidate native-frame runs before opening them. Native follow-up
may inspect any/all of the fixed 421 frames, never outside this interval. Keep
an explicit viewed-index list: extraction is not viewing, thumbnail viewing
is not native inspection. Do not exchange endpoint candidates or findings
until both standalone records are saved. Source/implementation discussion is
permitted; all accidental endpoint disclosures must be recorded. Existing
context exposure and published-time knowledge remain disclosed.

For **east onset**, identify downward change in a defensibly continuous
east-penthouse-associated material outline relative to local facade/parapet
context. Brightness/smoke change alone is not positive; whole-camera movement
is an alternative unless relative geometry distinguishes it. Record last
confident unchanged and first confident downward-change frames, with all
intervening ambiguous frames retained. A first positive needs persistence or
consistent further change in at least the following two stored frames; retain
the original first frame, not the third, as the positive edge. No claim of
subpixel physical stillness or earliest infinitesimal motion is made.

For **west disappearance**, identify the remaining west-penthouse-associated
outline above the **contemporaneous moving local north parapet**. Record last
confident visible and first confident below/behind-parapet frames. Trace the
material outline through native adjacent frames; require the first post-event
state to persist for two following frames within scope. Simple nondetection
through smoke/dust, an unresolved crossing or lost feature identity is
**ambiguous/censored**, not a confident post-event frame. Keep screenwall loss
and the physical roof plane distinct from this projected visibility threshold.

If either event lacks a confident bound within scope, report the actual
one-sided bound or non-identifiability. Do not select a convenient substitute,
fill an obscured run, alter opacity/contrast, or extend the interval to produce
a precise discrepancy. Persisting camera ambiguity also censors the result.
After both freezes, compare disagreements explicitly, preserving originals.

## Arithmetic and limited model comparison

For observer-specific encoded-time event brackets E=[eL,eU] and W=[wL,wU],
report elapsed-time enclosure [wL−eU,wU−eL] using exact rational PTS. This is
an observational bracket, not a statistical confidence interval. Give each
observer's result and the union envelope, not a fabricated average or error
probability. No constant offset is fitted to the published value; an absolute
origin shift cancels in the interval. Missing source-clock/conversion fidelity
remains a separate systematic uncertainty, not invented numeric padding.

Compare only after freezing observations, retaining the published roughly
9.3-second distant-view prose and both Case B model pairs (6.9/7.3 with damage,
10.6/10.9 without). Their different virtual viewpoints remain a comparability
limit. Do not import the street-view 8.0±0.1 threshold or the neighboring
10.0±0.1 figure's uncertainty. Bracketing by two damage cases is not a
probabilistic ensemble or unique causal validation. Any discrepancy addresses
a particular visible-event correspondence, not guilt, intent or mechanism
identification. Report strongest counterinterpretation and remaining next test.

No accepted Sherlock/Faraday transition, legal promotion, human-gate bypass,
outreach, publication, fee, commit or push is authorized here.
