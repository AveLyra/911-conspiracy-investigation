# Manual stroke envelopes pass the declared synthetic trial

October 7, 2026. Two separately frozen AI readings each supplied 140 local
pixel envelopes that contained the generating line over the complete queried
column, while withholding 28 locations. Neither falsely admitted a true dash
gap. This supports these frozen readings on these finite synthetic examples;
it does not establish historical graph accuracy, an engineering discrepancy
or a collapse cause.

The [completed fourteen-pair source inventory](../remaining-route-inventory/report.md)
remains the historical starting point. This trial answers its next method
question without enlarging a bound after seeing a failure or changing either
reader's response.

## Results and disagreement

| Declared check | Reader A | Reader B |
|---|---:|---:|
| Complete column annotations | 168 | 168 |
| Envelopes containing the full true line segment | 140 | 140 |
| Withheld locations | 28 | 28 |
| False admissions in generating gaps | 0 | 0 |
| Containment failures among admitted envelopes | 0 | 0 |
| Tiles with at least one correct interior envelope | 28 of 28 | 28 of 28 |
| Correctly unresolved latent-property questions | 4 of 4 | 4 of 4 |
| Admitted envelope widths in native pixels | 2–7 | 2–7 |

The originals are [Reader A](reader-a.json) and [Reader B](reader-b.json);
the complete scored entries are [A](score-a01.json) and [B](score-b01.json).
Both readers withheld the same locations, but their outer pixel sets differ
at 53 entries and their core/fringe classifications at 56. These differences
remain in the frozen responses. Matching pass/fail classifications do not
make the annotations identical; neither their intersection nor their union
is promoted into a calibrated source-error bound.

The four refusal questions concern a dashed line versus an occluded continuous
line, ambiguous identity through a same-color crossing, a fully hidden path
versus no path, and a crop edge versus a physical endpoint. They test whether
the reader avoids an unsupported inference. They do not recover any hidden
path or show that such an ambiguity occurs at a particular historical location.

## Method and reproducibility

The [protocol](PROTOCOL.md) was frozen before generating the packet. The
unchanged parent renderer supplied seven colors in four configurations each:
thin positive-slope, half-pixel-phase PNG solid/dashed lines, and thicker
negative-slope JPEG50/subsampling2 solid/dashed lines. Six fixed columns per
tile gave 168 entries per reader. No historical pixels or physical units
entered the trial. No color detector, fitted centerline, added radius or gap
bridge was used by the declared annotation method.

Readers viewed all seven contact sheets, all four separate refusal images,
and the complete unfiltered RGB records for all queried columns. Individual
T images were not separately opened. Native coordinates came from the raw
column records, not the 3x context image dimensions. Their new expected-row
contents and each other's responses were withheld until freezing. Prior
renderer/task familiarity and the allowed manifest's truth-related filenames
and hashes limit blinding; equal hashes can reveal raster equality. The
refusal questions themselves cue the ambiguity to consider. This is
same-source AI method testing, not actual
human sample acceptance or independent historical corroboration.

The scoring rule admits only a nonempty contiguous outer row set with an
identified local stroke. It compares the rectangle's edges against both
endpoint limits of the generating line over the entire column, accounting
for either slope. Ground-truth gap support is evaluated separately. Malformed
accepted sets raise an error rather than being silently repaired. No such
error occurred in the frozen readers.

Both generation runs reproduce all 74 products byte for byte. Each reader's
two scoring runs also match byte for byte. The [independent generation check](independent-check.json)
verified all 168 truth entries and 16,128 raw-column cells. A separate complete
[score check](score-independent-check.json) records the independent arithmetic
and disagreement audit. The [verification record](verification.json) retains
pins, actual commands, receipts and limits. Ten focused producer tests passed,
including negative slope, boundary equality, midpoint-only false containment,
false gap admission, malformed rows, all-withheld nonvacuity and refusal errors.

One minor reporting bug is preserved: generation's console `run` label says
`full-occlusion` because a loop shadows the requested name. The output paths
were fixed before that loop; both directories, manifests and all products
were checked. No images were misrouted or regenerated to conceal this issue.
Existing-directory and score-file overwrite refusals left all original bytes
unchanged. The code and output versions remain pinned as executed.

## Historical applicability and next decision

These are repeated straight-line geometries with colors varied, not 168
independent accuracy trials or a random sample of historical shapes. A pass
does not supply a confidence level, guarantee curvature/crossing performance,
validate strip joins, or distinguish hidden same-color contributions. Reader
agreement alone cannot supply those missing assumptions.
Width, slope, phase and encoding also change together between the two
conditions; this trial does not isolate their individual effects.
Manual fringe selection remains judgment-dependent. Passing these readings
does not establish a reproducible accuracy rule for new images. Geometric
containment and historical curve identity/support are separate requirements;
wider rectangles cannot repair an unknown identity or hidden continuation.

The [encoding comparison](source-applicability.json) finds that all twelve
historical strips share the trial JPEG's subsampling code, but none has the
same quantization tables. That is not evidence of worse quality, nor does it
require exact encoding equality for useful approximate measurements. It does
prevent treating this trial as an established reproduction of the historical
raster process. Original stroke geometry and earlier encoding history remain
unknown.

The next task is one bounded historical-applicability decision using the
existing registration, complete source-region inventory and frozen native
annotations. Deliver an applicability table for all fourteen pairs, naming
candidate regions, existing footprint evidence, tested-condition matches and
mismatches, explicit assumptions, and a disposition: conditional local estimate,
further specified recovery, or unresolved. State bounds assumptions separately
from identity/support assumptions. Where supported, prepare
the full all-pair support inventory and unchanged 42-slot human packet; label
conditional sensitivity estimates separately from accepted measurements.
Do not demand exact pre-raster recovery, treat unknown support as zero, or
repeat this synthetic trial as a substitute for that decision. If a specific
region cannot support a bounded measurement, record the needed array/source
detail and the resulting metric limitation instead of endlessly expanding its
pixel census.

The wider thermal-to-failure and collapse/arrest tests remain separate. No
cause ranking, human acceptance, engine finding, legal record or publication
changed. Research stays uncommitted in this investigation worktree; no push
or external disclosure occurred. The full charter remains active and incomplete.
