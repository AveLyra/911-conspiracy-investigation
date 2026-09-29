# Joint printed-table consistency test

September20,2026 UTC; declared before any joint historical calculation.
The prior row-wise clock test is complete and remains unchanged. This is an
explicit follow-up to its untested joint-consistency condition, not a new
independent video measurement or retrospective claim of blind preregistration.

Question: can one hidden-precision position per printed sample simultaneously
satisfy every supported centered-difference velocity in the published four-point
Camera2 table under each of the three already fixed clock hypotheses?

Use only the two frozen page47 transcriptions in
`../multipoint-table-reproduction/transcription-root/table47.json` and
`../multipoint-table-reproduction/transcription-independent/table47.json`.
Verify identical selected rows/tokens and the preserved source-PDF hash. No
PDF re-transcription, new frames, fit-window selection, smoothing, dropped
rows, invented endpoints, arbitrary clock tuning or rescaling of prior fits.
Read the earlier report, PROTOCOL and CLOCK-ADDENDUM. Main controls and full
CHARTER govern; all outputs remain working research in this worktree. No
main/legal/accepted-engine/solver state, installation, outreach or disclosure.

Fixed assumptions: every printed position and velocity is within a **closed**
plus/minus0.005 interval around its decimal value; this is a generous
nearest-hundredth display envelope, not a specified tie-breaking rule or
physical measurement uncertainty. Times label the nominal0.2-second sample
grid. Centered spans are exactly12/30,12/(30000/1001),12/(2997/100) seconds.
Six-frame spacing remains a hypothesis. Preserve every blank and the already
unsupported first northwest velocity; do not invent its missing neighbor.

For each of NE/EC/WC/NW and each clock (12 cases), introduce one shared
position variable for every present y cell. Bound each by its display interval.
For each supported velocity, constrain the difference between its following
and preceding position to `span * [v-0.005, v+0.005]`. Reuse the same variables
across overlapping rows. The printed center position need not enter that
row's centered derivative. All supported rows are simultaneous constraints.

Root will implement exact rational difference constraints with a feasibility
witness or negative-cycle certificate; no floating tolerance or external
optimization/structural solver. A separate reviewer uses an independently
implemented interval-chain calculation and independently transcribed inputs,
without reading root results first. Both freeze full results before comparison.
Witnesses must pass every original interval/derivative constraint. An
infeasibility certificate must name valid input-derived inequalities whose
sum is impossible. Retain boundary-only feasibility explicitly if detected;
closed-envelope feasibility does not identify a rounding tie policy.

Synthetic controls: feasible constant/linear sequences, translation invariance,
exact endpoint feasibility, a known beyond-bound failure, individually feasible
rows that are jointly impossible, disconnected/missing-velocity chains and
malformed duplicate/unsorted/non-grid rows. Run twice to fresh create-only
outputs, compare deterministic results and pin code/protocol/input/source bytes.
No historical run before these controls pass. Preserve failures without tuning
data, clock hypotheses or acceptance.

Acceptance: all12 cases independently agree on feasibility, with a checked
full witness or explicit contradiction; all constraint and unsupported-row
counts reconcile with the existing row-wise study. A discrepant reviewer
result stays unresolved. This tests whether clock plus display rounding is
a mathematically sufficient explanation of the table's derivative relation,
not whether authors used it. Infeasibility implies another data/processing
assumption is needed; it does not establish fabrication. Feasibility is not
calibration, actual frame timing, instantaneous support loss or a WTC7 cause.
No new ranking follows from this limited method test alone.
