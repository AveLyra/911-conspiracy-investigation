# Stage C: capped lossless roof-detail sensitivity pass

Declared September 20, 2026 UTC, before making/viewing these display products.
Previous goal turn: **progress** (two saved annotations, exact checks, bounded
review and a specific visibility/identity limit). Current main controls and
full charter were rechecked; research worktree remains e8d83d7 with intentional
WIP. This is a post-outcome **display sensitivity test**, not blind replication,
new evidence, added resolution, an AI reconstruction or a cause classifier.

## Question and fixed scope

Can a lossless enlargement of the already-verified Camera 2 luminance pixels
clarify whether the last raised right-roof remnant belongs to the intended
west-penthouse outline, and whether that material can be traced behind the
contemporaneous moving local parapet? This directly tests both risks in Stage B:
over-conservative censoring and a shared wrong-component identification.

Use only run01/camera2/selection.json and its existing native PNGs. No new
decode, acquisition, source-clock correction, alternate camera, report-image
substitution, smoothing, contrast adjustment, deinterlacing, synthetic fill,
super-resolution, stabilization, pixel marking or metrical calibration.

The **71 distinct source indices** are fixed before rendering:

- Baseline/east context: 6593, 6689, 6701, 6707, 6714, 6717, 6724, 6736, 6784.
- Intermediate west context: 6881, 6904.
- Every stored index **6920–6978 inclusive** (59 consecutive images).
- Late context: 7013.

All are inside Stage B's fixed 6593–7013 interval. The east samples supply
context/component continuity only; they do **not** support narrowing the
Stage B onset brackets across unsampled gaps. No frame/crop/scale extension
is authorized within this pass, even if the endpoint remains inconvenient.

## Display transform and source preservation

For each 640×480 mode-L source image, take the same half-open rectangle
**(x0,y0,x1,y1) = (300,125,465,245)**: source columns300–464 and rows125–244,
165×120 native pixels. Save that native crop and a **4× integer nearest-
neighbor display**, 660×480 pixels. Each input pixel becomes one constant4×4
block. No other image transform or marking is allowed. Image titles/indices
belong outside the raster; complete source frames stay available untouched.
This rectangle is intended to retain the target roof and adjacent facade;
sufficient context is a condition to check, not an assumed outcome. If the
candidate or necessary occluder reference reaches/leaves the crop, or identity
requires omitted context, record unresolved. Crop-edge disappearance is not
a below-parapet observation. Cropping cannot recover obscured material.

Reuse only the read-and-pinned pure `crop` function and its five synthetic
controls from `../camera2-calibration-source/prepare_context.py`, SHA-256
`31c7ca05494fa3abb8ea4300077691c8aa79abd2e0238fad6b8c0317ba33be91`.
Do not run its historical CLI or edit that prior unit. A small Stage C driver
may import the pinned module without executing `main`, add scope/source/output
checks and preserve its code/dependency/version identities in new run receipts.
Use the existing Python3.13.7/Pillow12.0.0 environment; no new package install.

Pin selection JSON to
`e297292a04a093d757b7693b9914abe4b88db4e6b836461f49c8dee411e78b2d`.
Check canonical ordered unique indices, exact PTS/timebase identities, native
PNG/luminance bytes and source geometry for every chosen frame. Preserve the
four Stage B freeze hashes recorded in stage-b-validation.md and pin this
declaration. Verify input/code/dependency pins again after rendering.

## Implementation acceptance, distinct from visual acceptance

Before historical display generation, rerun the inherited five synthetic crop
tests and test the new driver's selection, exact-pixel mapping, bad input/pin/
geometry rejection, output collision/confinement, source-change rejection and
failure reporting. Keep test/failure outputs separate from historical displays.
The independent pixel oracle must use explicit integer index replication or
byte-row construction, not the producer crop/resize function. Verify every
native crop pixel and every4×4display block against the source rectangle.

Produce two fresh, separately named outputs, `stage-c-run01` and
`stage-c-run02`, without overwriting anything. Each must contain exactly71
native crops and71 enlarged PNGs plus explicit snapshots/receipt metadata.
All paired images must match; independently verify input/product hashes,
transform dimensions, pixel mapping, frame/PTS joins and unchanged freezes.
Retain warnings/errors/failures rather than blessing matching corrupted output.
A successful transform says nothing about whether a roof edge is identifiable.

## Visual acceptance and stopping rule

Root and a separate observer each view all71 complete enlarged images in index
order after product verification. Native crops need not be separately displayed:
the exact mapping is mechanically verified and prior complete-frame context is
disclosed. Record actual viewing and any failed displays; derivatives generated
are not derivatives viewed. Repeat display of these same images is permitted
and counted separately, but no alternate rendering or further selection.

Both know the Stage B results. Before exchange, save/hash separate Stage C
records. Do not send candidate frames, contour descriptions, endpoint results
or conclusions until root confirms both freezes. Procedural status is allowed.

At the existing context frames and through the continuous west run, distinguish
the **material candidate outline** from the **foreground parapet/occluder**.
Record source-coordinate segment/range descriptions where genuinely resolved;
record `unresolved` rather than interpolate a hidden edge. Grouped runs may
share an annotation if every intervening image was inspected and the state
remains the same. These are qualitative contour bounds, not calibrated point
tracks, subpixel coordinates or physical dimensions. An apparent local step
alone is insufficient to prove which component made it.

Retain Stage B's local event rule: positive visibility, ambiguous transition
and a first confidently below/behind-parapet state with its actual next two
stored-frame confirmations. A new first positive must be in the continuous
run and **at or before6976**. Sparse context or isolated7013 cannot supply
missing adjacent confirmations. A first crossing, persistent loss through
smoke, a moving outer corner, screenwall loss and physical roof sinking are
not equivalent.

Three confident post-state frames establish a **local qualifying transition**,
not necessarily final disappearance. Finality across the unviewed enlarged
6979–7012 gap remains conditional/unresolved;7013 cannot establish continuous
absence. A later positively visible remnant lower-bounds final disappearance,
but not an earlier first crossing followed by reappearance. Explicitly test
the continuity/reappearance alternative and the moving occluder before giving
either interpretation. Do not relabel a local crossing as the final endpoint.

Report whether the display (a) strengthens, weakens or leaves the6958component
association unchanged; (b) supports a new finite bound or preserves censoring;
and (c) changes the permitted conditional elapsed statement when combined with
the original east brackets. Any revised result is a **new sensitivity result**,
never a replacement of the frozen originals. If identity fails, withdraw the
corresponding inference in the synthesis rather than use an alternate bump.

**Hard stop:** one fixed transform, one fixed71-image set, two separate records
and post-freeze review. If the crossing stays unresolved, close this display
route with the exact source-quality/component/human-review requirement. Do not
repeat zoom/crop/threshold tuning or invent a finite interval. Next work then
moves to another material feasible charter lead or the specified source/review
prerequisite. No new cause ranking from display success alone.

## Authority boundary

All products and findings are research-only. Raw sources, prior code, all Stage
A/B freezes and accepted Sherlock/Faraday/legal records remain untouched.
No disclosure, external feedback send, paid work, solver, signature, filing,
publication, commit or push is included. Generic workflow lessons may extend
the existing locally pending SFB notes, without changing their archived-task
routing status or claiming a verified engine defect.
