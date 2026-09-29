# Final bounded numerical/report review

**Disposition: PASS within the numeric and interpretive scope below.** No
displayed-value, plotted-series, window-selection or material inferential
discrepancy was found. This review does not newly inspect images, original
XML, source documents, keyframe semantics or feature identities.

## Reviewed subjects

The report and plot producer were read completely. Checked SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| `report.md` | `2f367faac6acc5fb695144d6d7dcb1b74d52fa1bcfa3ada87681f329728e8af3` |
| `plot_results.py` | `e3c737ebe8dbb514832d7a62182c68d2ba638d0fc242fa18a95d1a442db7221d` |
| `figure01/plotted-series.json` | `8b54ff0468acb7a685ad18fc00af7f68a0b5857e8761fb63fd694e1a694b7cb9` |
| `figure01/receipt.json` | `2cde4a570533aaca80cafa7b074d98a587d8671114ef074d8db4d10f6435f204` |
| Figure PNG, integrity check only | `67bcb76378289bb7360f51eb325aeab2f2fb5c68253f7bbeb467696bcc4807dc` |
| Root numerical rerun receipt | `30e78ffd3df7e6a624fd490fd6834fcfd3ed684ac45c6b8cd642a1ffd59ba9f4` |
| New `report-numeric-receipt01.json` | `145fbca36cf3c2fcfff357a5f3e0bb89f31fcbd51c6ca648741e0352ab12ae89` |

The original independent verifier and earlier receipts remain frozen.
Whole-JSON comparison independently confirms that root's rerun receipt
differs from `independent-receipt01.json` only in `command`. No rerun was
launched by this final-review pass.

The new read-only numeric cross-check ran with Python 3.13.7 through the
explicit pyenv interpreter, with bytecode disabled, and returned **exit 0**.
It imported no producer, decoded no video, performed no new trajectory fit
and used no image-display tool. The small receipt preserves all checked
table results and twelve input pins, identical before and after the check.
Only this review and its generated receipt were authored.

## Table and scalar checks

The six displayed window rows were independently joined by track, frame
endpoints, point count and nominal clock to the already independently
calculated window records. All twelve downward coefficients reproduce the
displayed three-decimal values. Their 21-point/13-point spans are exactly
4.0/2.4 assigned seconds; the nominal times and frame labels match.

The 11.0–13.4-second example's native-y RMSEs were recomputed as
`sqrt(independent_SSE/13)` for each polynomial degree, giving the displayed
8.175/0.352/0.188 pixels for track01 and 7.099/0.431/0.157 for track02.

For the scale table, the independently retained saved15 coefficients were
multiplied by exactly 14/15, 1 and 16/15. All six displayed accelerations
match rounding. Independent dimensional arithmetic gives exactly
54.4068/58.2930/62.1792 metres for 14/15/16 equal 12.75-foot intervals.
The zero-angle example is independently reproduced by dividing each
native-y quadratic acceleration by the saved pixel-per-assigned-metre
scale: 9.862 and 8.556 assigned m/s² after displayed rounding.

The final assigned downward displacements, 58.313 and 56.802 m, were checked
directly from first/last numeric coordinates and the declared rotation and
scale. Full-span coefficients 1.028/1.038 and the reported 5-point and
13-point maxima also match independently retained results.

All four unit-y-response rows were independently derived without the
producer's pseudoinverse. For each equally spaced, symmetric window,
let `v_i=t_i²-mean(t²)`. Its quadratic acceleration weights are exactly
`w_i=2*v_i/sum(v²)`. Multiply their maximum absolute value and absolute sum
by `cos(theta)/s` for the baseline downward response to y-only perturbations.
Every stored weight in every corresponding fit also agrees with this
closed-form result within the already fixed 1e-9 absolute tolerance.

| Points | Independently computed one-point maximum | Independently computed simultaneous bound |
|---|---:|---:|
| 5 | 2.140544142648204 | 8.562176570592815 |
| 9 | 0.454054818137498 | 2.270274090687489 |
| 13 | 0.164657241742170 | 1.047818811086533 |
| 21 | 0.042303243925854 | 0.393642817162682 |

All displayed response values are correct three-decimal rounding. They are
rounded summaries, not outward-rounded strict numerical bounds; use the
retained full-precision weights for a strict inequality. This ordinary
display qualification does not change the operator-sensitivity finding.

The 241 windows per track/clock, 964 window records and 5,784 scalar
polynomial fits agree with the prior independent coverage. The report does
not count overlapping windows or the coinciding clocks as independent data.

## All plot series and selection

The JSON series were reconstructed directly from the pinned fit,
trajectory and clock products. **Every field of all ten series matches
exactly**, including order, labels, time coordinates and values:

- Two 71-sample assigned-displacement series: 142 samples.
- Four sliding-window series per track with 67, 63, 59 and 51 samples:
  480 samples across both tracks.
- Total: **622 samples**. Every declared sliding-window start/stop pair is
  present exactly once per nominal-clock track/length series.

The plot producer selects only the declared nominal clock, saved angle and
15-interval scale, and plots all passing windows of the four declared
lengths. All those windows actually pass; therefore its status filter omits
none in this run. The two nominal-clock full-span fits are intentionally
excluded from the figure and retained in the source arrays, as disclosed.
No nearest-gravity or residual-quality filter is present. The figure's
reference line is the declared conventional 9.80665 value, not a fitted
parameter. All plotted time values lie within the code's 0–14-second axis.

Producer input pins, output pins and receipt counts match the independently
verified source artifacts. This checks series lineage and code selection,
plus the saved PNG's hash. It is **not** a new pixel-level plot rendering or
visual-layout review; those remain separate.

## Inferential assessment

The report fairly describes positive **conditional** gravity-scale
curvature in a late track01 window. It neither erases that evidence because
calibration is imperfect nor converts a coefficient near the reference into
a measured equality. The displayed decimals are explicitly distinguished
from physical accuracy or confidence intervals. The illustrative length
alternatives are not called a measured uncertainty range or given equal
probabilities. Axis-angle sensitivity is not represented as a perspective
bound, and the `1/r²` clock-rate law is conditional, not an asserted timing
correction.

The quadratic/cubic comparison properly concerns in-sample model form.
The report does not identify a window's constant coefficient as an
instantaneous acceleration, turn above-reference short-window estimates
into proof of extra force, or identify a roofline marker with the building's
center of mass. It correctly separates a real difference between saved
numeric tracks from the unresolved physical explanation of that difference.

Complete-array retention, complete sliding-window plotting and the explicit
post-run example-selection disclosure are important qualifications. These
are not a preregistered gravity-equivalence test. No test here independently
establishes whole-building free fall, simultaneous support disappearance,
mechanism or intent. Feature/source interpretation is assigned separate
review; this pass does not adopt those judgments as independently inspected
facts. No blocking numerical or report-interpretation correction is needed
within this scope.

## Final report ledger update

The final report SHA-256 is
`fcad554e3dedf1dc2cf1eb55a47223980ef0d8357630bf0b0587208cd5624df7`.
This reviewer read the five revised claim-ledger assessment cells. Reversing
exactly those five replacements in memory reproduces the initial fully
reviewed report hash
`2f367faac6acc5fb695144d6d7dcb1b74d52fa1bcfa3ada87681f329728e8af3`.
The check exited 0. Thus the numerical prose, tables, figure references and
all other report bytes are unchanged; the earlier numeric receipt remains
unaltered and applicable to them.

The revised grades remain appropriately proposition-specific: A for the
verified computation, C for a materially conditional historical
gravity-scale interpretation, D for unresolved physical equivalence or
mechanism, and E for deriving universal support disappearance from these
point histories alone. These are epistemic assessments, not probabilities
or evidence that a cause is impossible. The completed root rerun statement
is consistent with the separately compared receipt. **Final disposition
remains PASS in the bounded scope above.** No new source or fit inspection
was added by this five-cell confirmation.

### Rounding-language confirmation

Final report SHA-256:
`c2e66e0bf2b9f43d71fced142445d2f65097ce06ea49059a53fe5114be49fb2d`.
The sensitivity introduction now calls the displayed values
"maximum-response magnitudes" and explicitly directs readers to the retained
full-precision weights for a strict numerical bound. Reversing only this
paragraph replacement in memory reproduces the prior `fcad554e…` report
hash above; the check exited 0. No numerical values or other report text
changed. This resolves the rounding qualification explicitly in the report.
PASS remains unchanged; prior report hashes and receipts are preserved.
No calculation rerun or source check was performed for this confirmation.
