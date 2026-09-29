# Method preflight — point-independent target correspondence

2026-09-24. Reviewer `/root/curve_method`, reused prior-informed AI. Earlier
Reader C, scene-locator author and provenance critical reviewer; not blinded,
a human expert or an independent historical witness. This is a separate
prospective method/code-reading pass, not implementation or result validation.
Only this working review is written. No new image viewing, pixel/video decoding,
historical scoring, source acquisition, engine acceptance or legal work occurred.

## Scope and controlling reads

Read current main AGENTS, WORKFLOW, START-HERE and the full investigation
CHARTER; current worktree STATUS top (lines1–145); the complete preceding
bright-point report/method review; and the complete new protocol. Main authority
and preserved sources remain read-only. Evidence-falsification-auditor,
source-of-truth-guardian and repo-orchestrator skills and relevant references
were read. Repository intake was run read-only in the worktree, reporting
branch `research/sherlock-wtc7-investigation`, HEAD `e8d83d7` and preserved WIP.
It is not a whole-repository content or privacy certification.

Read all of the existing `tilted-camera-source-join/compare_scenes.py`,
`scene-independent-check.py`, `PROTOCOL.md` and `SCENE-ADDENDUM.md`; no imports
or test/history entry points were executed. Read only the exact existing light
screen descriptions relevant to mask location after root requested that check.

| Read artifact | SHA-256 |
|---|---|
| New `PROTOCOL.md` | `e9345fd05579cfcc7f45b1fa850271eeea8f3f7abe23a80dfb70bc6063364503` |
| Main CHARTER, previously pinned controlling version | `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd` |
| Preceding bright-point `report.md` | `9f27ca9e41dbf05b136533781479e1c97f78a82d18f200d283f860698bc7e6c9` |
| Preceding bright-point `method-review.md` | `1da2fb3c28fd397af4eb12b7a72aef2cd2cc69a284468245dbc4ef1bb3270cc4` |
| Current STATUS snapshot | `60f0bd6f178e3932ca36bffbe475b8109173f7402f12fb58a1201ed67c355d1e` |
| Existing `compare_scenes.py` | `80f5e15b66940a3db3f9fc91e52e84a8c3d706f10c3b8cd756ec923884bd73a5` |
| Existing `scene-independent-check.py` | `4f2deeec53d768de631405f10b0d12abecde3011dc8b21785d8c93f7f0d953f4` |
| Existing join `PROTOCOL.md` | `0bec10bef245cf59d62800dce2c67913da62b90cbb8b42a42d9d9ce2555614e1` |

## Reuse and metric assessment

The old producer's lines33–41 define raw MAE and mean-centered correlation;
lines73–90 verify PNG/native-luma identity and width-only resize. These are
useful bounded components. Lines44–52 and97 force a deterministic minimum of
the old full-scene score; that is a ranking operation, not exposure acceptance.
The old full-scene mask includes foreground and must not silently remain the
new selection mask. Its eight-query/701-candidate orientation is different
from this six-query/all476-Tilted search.

The old separate checker's lines64–104 provide a scalar integer oracle and
integer absolute-difference/covariance arithmetic; lines107–117 preserve exact
ties and rank order. Reuse is appropriate, but code reused as the new producer
is no longer a separately authored verification of that producer. Preserve a
separate expected-value calculation and source admission.

For each fixed mask M, retain the integer sum
`S(i,j) = sum(abs(Camera2_i[p] - resized_Tilted_j[p]) for p in M)` and its
sample count, with MAE `S/len(M)`. Signed/int64 arithmetic avoids uint8 wrap.
Compare integer sums for exact rankings within a fixed mask, not rounded
displayed MAEs. Correlation remains diagnostic and null for constant vectors;
it must not rescue an unfavorable MAE ranking. The new protocol does this.

NEAREST/BILINEAR remain separate diagnostic raster branches, not physical
aspect calibration. Omitting the previously redundant BOX branch is declared
before target scores and does not itself create independence. No fitted
translation, contrast, warp, time offset or mask tuning is admitted.

## Mask-location concern and its disposition

The already-frozen text establishes a descriptive left-foreground location:
`camera2-light-screen/reader-c-observations.md` lines341 and346–354 describe
6925; `reader-b-observations.md` lines264 and464 describe 6925 and6970. The
supporting exact ranges read were C332–361, B257–278 and B457–477. They do not
establish pixel coordinate x<320 or coincident locations for both appearances.

The proposed fixed right-half, target-right and right-background masks are
suitable **conditionally**. The new protocol now requires both native frames'
own-receipt admission and coarse mask sanity checks before scoring. One frame
alone would have assumed common placement. An appearance not comfortably
excluded must stop this declaration rather than trigger score-informed repair.
This reviewer has not performed those views. The protocol's statement that
the boundary is far from the foreground remains a condition to verify, not
a fresh coordinate finding supplied by this review.

The implementation must explicitly define the native Tilted perturbation
region used for the exclusion control. An output-grid exclusion alone is
insufficient: BILINEAR may mix a source pixel across a nearby boundary. Test
the actual width-resize pipeline and kernel footprint, with a conservative
guard region, showing excluded-point-region changes cannot change any retained
sample. Do not claim that every source pixel in an entire left half is ignored
merely because all retained output x coordinates start at320. The coarse
historical sanity check and synthetic footprint check answer different questions.

## Alternatives and failure policy

Top five rank positions, **all** ties at the fifth score, and each retained
index's in-domain neighbors make a reproducible inspection shortlist. They are
not a calibrated confidence set or all physically plausible counterparts.
Keep all476 scores per query/branch/region. If ties make the shortlist include
the entire domain, preserve that result or stop; do not silently cap it.

Region/branch disagreement, endpoint minima, repeated winners and reversed
order remain findings about the diagnostic. Do not impose one-to-one,
consecutive or monotonic assignments to make the sequence look plausible.
The right-background region can be nearly unchanged across many frames; that
is not temporal corroboration. Overlapping masks and related encodings do not
supply independent votes. The protocol states these limits appropriately.

The strongest failure mode is a repeated, dropped, field-combined or blended
processed image whose best numerical candidate is not a corresponding original
exposure. Shared background and encoding differences can dominate even after
the foreground point is excluded. A narrow rank gap is not a probability; a
large gap cannot by itself authenticate exposure or processing ancestry.

## Minimum controls and remaining gates

The declared controls cover the relevant arithmetic categories. Before relying
on implementation, verify at least:

- Known copies, signed brightness shifts, localized changes, constant images
  and unsigned-subtraction hazards against hand/scalar expectations.
- Exact ties and cutoff-crossing ties, including all-equal candidates; keep
  every tied index and clip neighbor expansion only to0–475.
- Static agreement with changing-region disagreement; preserve the discrepancy.
- Repeated/ambiguous neighbors and representative blend/drop cases: no unique
  historical exposure assertion may emerge from a forced rank.
- Global-grid/half-open membership, actual width-resize behavior and excluded
  source-region perturbation invariance for both branches; perturbation just
  outside the exclusion should exercise retained content rather than a vacuous
  all-zero mask.
- Missing/duplicate/invalid inputs, changed pins, frame/clock mismatches,
  nonfinite or malformed arrays, fresh-output refusal and repeat determinism.
- Separately implemented material score/selection verification with source
  identities checked independently; no producer-import oracle.

None of these controls is represented as run or passed in this preflight.
Fresh all476-frame decode admission, synthetic tests, mask sanity checks,
implementation review and independent score reproduction remain pending here.

Human-gate ceiling: this declaration supports bounded candidate-generation
diagnostics, not accepted synchronization, point absence, intensity, duration
or causal measurements. It does not clear the CHARTER requirement for synthetic
ground-truth tests and actual-human spot checks before consequential automated
measurement. Calling a score provisional would not permit subsequently using
it as an accepted exposure join or light-absence result. No paired target-light
view is included; that requires its separately declared, reviewed scope.

## Preflight disposition and actual commands

**No material method objection remains to the stated candidate-shortlist
diagnostic, conditional on the outstanding checks above.** This is method
readiness, not executable-code approval, source admission or a passing result.
Root's forthcoming implementation/results require their own review.

Actual commands were read-only `cat`, bounded `sed -n`, `nl -ba`, `rg -n`,
`shasum -a 256`, and
`python3 /Users/admin/.codex/skills/repo-orchestrator/scripts/repo_intake.py`.
One combined instruction output truncated WORKFLOW/START-HERE/CHARTER;
separate complete reads recovered them. A broad location-term query printed
too much; the exact relevant ranges above were then read completely. Neither
truncation was treated as negative evidence. No matcher/control entry point,
media viewer or historical measurement command was run. Only this new review
was saved with `apply_patch`; all older records remain unchanged.

## Implementation review — initial development snapshot

At root's request, read complete new `match.py` (191 lines at the first count),
`test_match.py` (103 lines), this unit's protocol again and `mask-sanity.md`.
Read complete `extract.py` only to check the producer-to-matcher receipt
contract. Root expressly reported that schema adaptation was still in progress
and historical scoring had not run. This is not a review of frozen final code.
No test, matcher, decoder or image viewer was executed by this reviewer.

The mask-sanity record is root's two separately source-pinned, original-detail
views, not this reviewer's fresh observation. Its SHA-256 is
`10c475f0eb44a07d3625bcdd58999b4ba45198a0add8cb07cc81913b0e75bcdc`.
It describes both appearances as comfortably in the far-left foreground and
expressly limits the check to coarse exclusion. This satisfies the recorded
two-frame sanity step as an attributed AI observation, not actual-human review
or a quantitative location measurement.

The code implements signed integer differences and int64 sums, separately
retained region/branch results, complete score arrays, exact cutoff ties,
in-domain neighbor union and explicit repeated/reversed winners. No preferred
resampling branch, monotonic repair or forced one-to-one exposure join was
introduced. Correlation does not select candidates. The tests include the
all476-tie case and keep its entire shortlist rather than silently capping it.

Two concrete guard gaps were sent before freeze:

1. `rank_and_retain` applies `int()` to scores before validation. That silently
   truncates fractional values and converts booleans, rather than rejecting
   them as invalid integer absolute-difference sums. This is a function-input
   guard gap, not evidence that internally generated int64 historical sums
   would be wrong. Require integer type before conversion, permitting NumPy
   integer scalars but rejecting boolean/fractional/negative inputs, and test
   the refusal.
2. `read_native` tests grayscale mode, geometry and one frame, but the initial
   version does not test `image.format == 'PNG'` despite its error label and
   the fixed source contract. Add that format guard and a non-PNG grayscale
   synthetic refusal. File and luma pins already constrain normal inputs; this
   is a narrow contract-completeness repair, not an observed source substitution.

The existing exclusion control changes all native Tilted columns x<350 and
Camera2 columns x<300. Its preserved-sample equality is meaningfully tested
through both resize branches, with included-region positive controls. Report
these actual protected bounds, not all source pixels in an entire left half.
It does not test global encoding/auto-exposure influence or source authenticity.

The initial matcher expects `receipt['frames']` and per-row `sha256`, while
the extractor writes a pinned `frames.json` product and `png_identity`. Root
had already identified/advised that in-progress schema adaptation; no failed
run or newly discovered historical defect is asserted here. The final version
must verify the receipt-to-frames product identity and per-image pins, preserve
all476 baseline full-frame/luma/clock joins, and receive independent source
admission before scores are relied upon.

Disposition at this development stage: the metric and ambiguity policy are
implemented coherently by inspection; the two small guard repairs, final
receipt adaptation, actual controls and frozen-code/source reviews remain
pending. Final review will be appended without rewriting these initial concerns.

## Frozen matcher review and synthetic replay

Read the complete revised matcher and tests after root's freeze signal. Actual
`shasum -a 256` agrees with both declared pins:

- `match.py`:
  `c097560d6763ac09d1870ef572e65e9b12d70669e81d26712d94750596a710f9`.
- `test_match.py`:
  `6496581215bdf992334726db611a85b4400a76efb4e5a993f8dbb868c9797a95`.

Both guard concerns are resolved before this reviewer's control run.
`rank_and_retain` checks nonnegative Integral values before conversion and
explicitly rejects Python/NumPy booleans; tests refuse fractional, boolean,
negative and NaN scores. `read_native` explicitly requires PNG format, with a
grayscale TIFF stored under a `.png` name refused by the new control. The
initial concerns remain above; no failed historical score was asserted.

The receipt adaptation now checks the extraction receipt's `frames.json`
product hash, reads its complete0–475 domain, checks frame-count/geometry and
joins every per-PNG identity to the extraction receipt. For every native row it
compares index, PTS, exact time, full-frame hash and luma hash with the pinned
old map before matching actual PNG/luma bytes. The pinned upstream Camera2
selection still fixes all701 candidate rows and the six exact query basenames.
Before/after pins cover the consumed files. These are coherent matcher-side
checks by inspection; complete extraction diagnostics and provenance remain
the separate source-admission obligation, not something this synthetic replay
has newly established.

Actually executed, from this unit directory:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B test_match.py
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -c 'import platform, numpy, PIL; print({"python": platform.python_version(), "numpy": numpy.__version__, "pillow": PIL.__version__})'
```

Both exited0. The first reported **9 tests, OK**, in0.061s. Runtime: Python
3.12.14, NumPy2.3.5, Pillow12.3.0. It used synthetic arrays and temporary
synthetic PNG/TIFF fixtures; no historical matcher entry point was invoked and
no historical pixels or scores were read. This is a separate execution of the
author's tests, not independently authored full historical arithmetic or a
reconstruction of the historical exposure. The test's scalar expected SAD and
known sampling checks remain narrower controls, not source authentication.

Root separately reported11 extractor controls passing under author/root
execution and an initial sandbox output-creation denial followed by an
authorized same-code retry. Those reports were not rerun or converted into
source-admission findings by this reviewer. No native extraction output,
historical score or post-run verification has been assessed in this appendix.

**Final code-review disposition:** no remaining material defect was identified
in the frozen matcher for the declared candidate-shortlist diagnostic; both
requested narrow repairs are verified, and its nine synthetic controls pass in
this replay. This does not validate unrun/unreviewed scores. Independent native
source admission, actual complete score reproduction, retained disagreements,
and result-level critique remain necessary before relying on the shortlist.
The separate paired-view declaration and actual-human/consequential-measurement
gates remain unchanged. Only this review file was edited.
