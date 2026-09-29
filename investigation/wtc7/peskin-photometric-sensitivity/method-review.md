# Pre-result photometric methods review

Research-only independent agent review, September 13, 2026. This is a review
of the method and code, not an independent source family, expert certification,
historical exposure identification or legal clearance.

## Reviewed state and actual independence

Read the current main-repository AGENTS, WORKFLOW and START-HERE instructions;
the full investigation charter; evidence-falsification, source-of-truth and
development-verification skills; the preceding correspondence report,
METHOD-01, CANDIDATE-REVIEW-01, check_regions.py and match_screen.py; and the
complete new protocol and calculation script. The prior report disclosed its
scores and qualitative findings. No source images, target images, new
historical arrays or historical photometric scores were viewed before this
review was saved. Familiarity is therefore documented rather than described
as a clean historical holdout.

Reviewed final pins:

- PROTOCOL.md: `edbc10c984c45e915d40853ea1ea0e9aa97f256af47643afa944dda278a8b7ed`
- measure.py: `eff2aa28a85d303ec6f17b47be312bfc13de35dbaa1c117a2d8ade5a7a03041a`
- Producer controls JSON: `18d01391dc41f7546f78c3d5a03aa3e1d96e610867af517d49775fcaed08b77b`

Root reports 28/28 synthetic controls passing; this review verified the file
pin and inspected the control implementation, but did not independently rerun
the producer's control function. A separate arithmetic checker is being
prepared and is not claimed complete by this pre-result review.

## Findings and corrections before calculation

1. **Material overlap found and corrected.** Figure 149's old foreground box
   `[5,95,265,435]` overlaps evaluation W1 `[164,125,580,173]`. The initial new
   script would have trained on those W1 pixels despite promising that W/D
   pixels never fit a curve. The final script removes the union of all W/D
   masks from the new photometric foreground, asserts disjointness, and tests
   both targets at both resolutions. The protocol records the correction.
   The previously selected geometry and preceding results remain unchanged;
   their old foreground support is not retroactively called disjoint.
2. **Comparable holdout baseline added.** Each fit row now retains the raw
   training and holdout errors on exactly its own selected support. A corrected
   holdout error can therefore be compared with its matching raw baseline.
3. **Control promise made explicit in code.** Recoverable gamma controls check
   normalized prediction error as well as coefficient error. The signed
   shift/padding control checks the sampling direction and validity mask.
   The protocol states that bias is source/prediction minus target.
4. **Version and execution gates checked.** Run names/modes are restricted;
   outputs are created in fresh directories; historical execution requires
   matching successful producer-control code/protocol pins and output hash.
   Prior dependency, native-image receipt and target pins are checked. The
   baseline branch must reconstruct the old sampled image and validity mask.

No unresolved critical issue in the reviewed final implementation prevents the
bounded historical calculation. This finding concerns the stated retrospective
sensitivity test only. Final evidentiary wording remains subject to complete
results, reproduction and independent arithmetic review.

## Interpretation constraints retained

OLS estimates a positive-slope affine transform of powered encoded gray values
before clipping, then evaluates clipped predictions. It is not the solution to
a clipped-loss fit or a recovered camera response. All seven gammas, both
foreground folds, four sampling branches and all twelve candidate/target pairs
remain visible; W/D errors do not select a winning curve.

The tiled holdout tests transfer within the already selected images. Its pixels
are spatially dependent, and old geometry and shortlist construction used these
scenes. It does not provide independent event-level validation. Foreground
intensity-range extrapolation and clipping diagnostics are essential because
bright features may lie outside the range that constrained a fit.

Rank and quantile-support diagnostics measure spatial ordering/support at the
declared sample grid. Strict monotone maps preserve ordering before clipping;
that invariance is not fresh corroboration from multiple gamma curves. Ties,
flat fields, missing coverage and empty threshold unions remain explicit.
Threshold support is not flame area; encoded endpoints are not authenticated
sensor saturation. Tiny bright-feature regions at the coarse grid remain
limited-resolution, correlated observations even when the sample gate passes.

Success would show compatibility with a tested global gray adjustment under a
fixed candidate/geometry/sampling choice. Failure would show remaining
discrepancy within that family. Neither result identifies exposure, historical
processing, selective falsification, interior fire history, steel temperature,
structural failure, an actor or intent. The meaningful added result is a
quantified sensitivity/transfer limit; causal rankings should not change from
this unit alone.

## Separate checker plan

The owned `independent_check.py` will use saved source/target/validity arrays,
with shared image decoding, resampling and prior geometry explicitly disclosed.
It will separately reconstruct masks and tile folds; solve OLS by a design-matrix
least-squares method; verify saved coefficients; and recompute error, rank,
threshold support, clipping and extrapolation diagnostics with independent
function implementations. Numerical comparisons will use declared tight
arithmetic tolerances, not historical equivalence cutoffs. Synthetic controls
will precede saved historical-array verification. Producer code will not be
imported by that checker.

Only this research working review and its scoped checker are owned by this
reviewer. Preserved sources, prior outputs, main/legal records, bridge state,
commits and transmissions are outside this work.

## Post-result arithmetic addendum

The preceding review was saved before root began run01. After that method
review, root ran the producer and made its saved arrays available. The separate
[checker](independent_check.py) passed [23/23 synthetic controls](independent-controls01.json)
before it read historical arrays. Its [run01 verification](independent-check01.json)
then passed: 48 branch rows, 672 fitted curves, 392 baseline/rank region rows,
6,832 fitted-region rows and 1,344 foreground-baseline rows, the last repeated
across gammas by the producer. These are computation-coverage counts, not
independent observations or historical validation successes.

All 454,236 compared scalar/null/string leaves matched. Count and null
comparisons were exact; coefficient tolerance was 1e-10 absolute and other
float tolerance 1e-9 absolute. The largest observed float difference was
`7.016609515630989e-14`. Independent rectangle masks, foreground/evaluation
disjointness, tile folds, source validity geometry and source/output hashes
also passed. The checker uses design-matrix `numpy.linalg.lstsq` for OLS and
separate rank, quantile, error, support, coverage and extrapolation functions.
After verifying coefficients, it uses the saved coefficients for predictions
so independent-solver roundoff does not masquerade as an exact threshold or
endpoint-count disagreement. This is an explicit limit of the reproduction.

Checker SHA256:
`029f3bdcd582c96ff0e2a440ae8c66c6133c8280bfe209e6da6843fdc63c1497`.
Control-output SHA256:
`130cbfb421eddefd099e3e67e5f19dea516d394a351f1daa48a071d1f8bc51c2`.
Run01 check-output SHA256:
`ee2251434e3ee274b21068749d6ceb47b34df1b4e9e5a1570a1e588c7032e3bd`.
Producer run01 results/arrays pins are recorded in that output. Shared runtime:
Python 3.12.14 and NumPy 2.3.5. The checker does not import producer code or
redecode historical images. Shared saved preprocessing remains a consequential
independence boundary, and no source or target image was viewed by this reviewer.

Operationally, default `python3` lacked NumPy; the declared bundled interpreter
was used. The first synthetic-control invocation reached output writing but was
denied by the filesystem sandbox, leaving no output file. The same invocation
then completed after scoped escalation for the designated research worktree.
This was an environment permission issue, not a failed arithmetic control.

Interpretation clarification: "foreground" is the existing mask's nominal
role, not a certified segmentation of a single physical plane. The discovered
T149 intersection establishes training/evaluation mask overlap; it does not
establish that W1 physically depicts foreground. Broad rectangles can contain
mixed foreground/background content. Removing their overlap makes the new
photometric training/evaluation supports disjoint without authenticating their
scene-plane labels. This caveat narrows wording; it changes no frozen code,
mask, parameter or result.

## Final closeout review — September 15, 2026

Re-read the current main-repository AGENTS.md, WORKFLOW.md and START-HERE.md
before this addendum. The changed case-management controls do not authorize
legal drafting, disclosure or research promotion here. Read the complete
`report.md`, `validation.md` and `summarize.py`, and checked the frozen protocol,
producer, results and independent-replay identities. No further historical
images, acquisition or image processing were used.

A separate read-only calculation from `run01/results.json`, without importing
the summary script, reproduced every region-range field and gamma-transfer
count in `summary01.json` exactly. The 344 W/D patch instances consist of
224 for Figure 148 and 120 for Figure 149. With two fitting folds, each gamma
has 448 and 240 comparisons respectively: 688 per gamma and 4,816 across seven
gammas. Every comparison has strictly lower MAE than its matching raw baseline;
every raw W/D mean bias is positive. These remain repeated computations on
correlated selected images, not 4,816 independent observations.

All six bright-region table rows round correctly from the full candidate,
sampling and fold ranges. Both examples match the previously selected leader
indices (93 and 185), and their source ticks agree with the reported seconds
under the prior 1/1000 timebase. The reported bias spans, Figure 148 D3
top-10%-support IoU range, and Figure 149 D1 training-range extrapolation span
also match. The 1st–99th-percentile extrapolation fields in the complete summary
were checked as well; no adverse summary field was omitted from this numeric
verification. Root's independent-check replay equals the earlier checker output
after removing only `argv` and `elapsed_seconds`.

The report's A rating is expressly bounded to the verified calculation, and its
B compatibility inference is confined to the tested gray-adjustment family.
The report preserves residual disagreement, tied/threshold support limits,
nominal mixed-plane masks, historical selection, shared preprocessing,
unidentified processing and the inability to recover flame area, interior
heating or a collapse mechanism. It does not use the result to dismiss separate
fire-input mismatches, establish intent, exclude intervention or change the
integrated causal ranking. No substantive numeric or inference correction is
required within those stated limits.

One documentation correction was requested: validation's sentence "The protocol
and independent method review were frozen before historical calculation" should
read "The protocol and the pre-result portion of the independent method review
were saved before historical calculation; subsequent review addenda are
explicitly labeled." The method-review file intentionally contains later
addenda, so the entire file should not be described as frozen before results.
This request changes no protocol, data or pre-result decision. Final scoped
closeout clearance is conditional only on that chronology clarification;
the requested literal edit does not require another scientific calculation.

Reviewed report SHA256:
`9d30600103d7be34263febebf6abcb968b8a00421b9c63275e8df8604c7d8fc6`.
Reviewed validation SHA256 before the requested wording correction:
`6154bffdcb9cff9746f9d51b9aadf867d8dd09caba501c0619dfe46d9ddf0a90`.
Summary-script SHA256:
`5c3cf6fa0a84064f4ed419c8834269739cd7c7702a950892b9f7ee9ab3e14b6e`.
Independently checked summary SHA256:
`024f7c989deda3663df78caaff82cafac98d5079ea084057019e15288353e17e`.
The frozen protocol, producer and run01 result hashes still match their earlier
pins. This reviewer appended only this dated addendum during closeout; root's
report, data and code were not edited.

Correction disposition, also September 15: root applied the requested chronology
wording, and this reviewer read back the exact corrected paragraph. Corrected
validation SHA256 is
`49234a7e835cadbce337c3a3b4f19bf886684e3d6dc110eeb1e2c259e05ba2b4`.
The sole closeout condition above is satisfied. Final scoped methods,
arithmetic-summary and report-claim review is complete with no unresolved
actionable correction. Authority, source independence and inference limits
remain as stated throughout this review.
