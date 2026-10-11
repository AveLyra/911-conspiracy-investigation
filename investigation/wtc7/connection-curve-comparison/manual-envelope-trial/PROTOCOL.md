# Manual stroke envelope admissibility trial

October 7, 2026. Prospective for this finite trial; prior-informed method
development. This tests whether manual native stroke annotations support a
particular graphical bound. It does not assume that they do. The parent
protocol, numerical contract, all fourteen pairs and 42 human-review slots
remain unchanged. No historical ordinate or comparison is admitted here.

## Fixed controls and reader task

Reuse only the renderer, codec and ambiguity-scene functions in the unchanged
parent `raster_uncertainty.py`, not its candidate detector or analysis. Make
28 isolated-line controls: seven existing colors, solid/dashed, and two
conditions. Condition A has vertical stroke width 1, slope +1/2, phase +1/2,
PNG. Condition B has width 3, slope -1/2, phase 0, JPEG quality 50 with
subsampling 2. The existing 160 by 96 raster, 4 by 4 subpixel coverage, white
background and encoded settings control; these are not historical compression
estimates. Query native columns 20, 23, 24, 28, 32 and 36 in every tile:
168 entries per reader. They span interiors and boundaries but the response
must come from the raster, not the generating formula.

Add four refusal controls: the existing dashed-versus-white-masked pair,
same-color crossing identity pair and full-occlusion pair, plus a cropped
solid line whose last visible column cannot identify a physical endpoint.
Use PNG for these. Preserve both latent descriptors for each paired control;
readers see one representative raster per pair. Questions ask whether pixels
alone establish the gap's origin, the through-crossing identity, absence of a
hidden path, or a physical endpoint, respectively. Correctly refuse each.

Two separate AI readers receive the packet rasters, full unfiltered RGB
columns and task instructions, but must not inspect the new truth manifest,
generator code, scorer, each other's annotations or scores until freezing.
Existing renderer familiarity is disclosed; this is truth-withheld review,
not a claim of complete blinding or independent historical evidence. Each
reader sees all 32 controls and supplies every required entry. Root creates
and scores the packet, and cannot act as a truth-withheld reader.

## Proposed envelope and falsification

For each column retain sorted native core and fringe row sets, an identity
disposition, and a brief visual/RGB cue. Core means visibly attributed local
stroke; fringe means plausible uncertain edge ink. Inspect context and every
raw cell; do not introduce an intensity/color cutoff or use ground truth to
choose rows. No fitted centerline, added radius, interpolation or dash-gap
bridging. Empty, disconnected, competing or unassignable sets are unresolved.

Only an explicitly identified fragment with one contiguous nonempty outer
set (core union fringe) supplies a proposed envelope: [x,x+1] horizontally
and [first row,last row+1] vertically. This geometric rectangle is a candidate
bound, not yet a calibrated uncertainty interval. The scorer checks both
endpoint limits of the exact generating line over the complete pixel column,
using minimum and maximum for either slope. Compare against truth support,
not extracted ink. A numeric envelope in a genuine dash gap is false admission.
An identified but disconnected set remains a recorded method/input failure;
it is not silently filled to make an envelope.

Report every containment failure, false gap admission, withheld entry and
envelope width separately for both readers. Require at least one correct
interior envelope in each isolated tile; refusing everything cannot pass.
Every refusal control must remain unresolved on the queried latent property.
Any false enclosure, false admission, malformed acceptance or incorrect
refusal answer fails this proposed method on its declared domain. No repair
of bounds or re-annotation after scoring. Original disagreements remain.

## Verification and finite endpoint

Freeze and hash this declaration before generation. Generate the packet twice
with exclusive-create output, pin renderer/protocol/runtime and all products,
and compare every byte product. Verify known-path truth and scoring separately
without importing the producer's envelope or support logic. Retain synthetic
scorer controls for downward slope, boundary equality, gaps, disjoint rows,
empty sets, core/fringe overlap, duplicate/type-invalid cells, full-column
not midpoint-only coverage and refusal errors. Actual commands/results and
critic coverage must be saved; no count represents scientific confidence.

A finite pass would justify only the tested conditions, not unknown historical
rasterization, line thickness, compression or model identity. A failure closes
this zero-added-radius manual-envelope method for the tested domain, not all
graphical methods. The practical next decision must identify the failed
condition and needed evidence without an indefinite annotation expansion.
No new expert gate, historical simulation, accepted engine state, legal
promotion, disclosure, outreach, commit or push. Work stays in this investigation
checkout. The full charter remains active and incomplete.
