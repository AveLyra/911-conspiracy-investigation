# Bounded report and saved-result critique

2026-09-24. Reviewer `/root/curve_method`, reused prior-informed AI, author of
this unit's preflight/code review and earlier Reader C/provenance reviews.
This is a separate critical pass and saved-array cross-check, **not wholly
independent authorship, blinded review, a human expert or another historical
witness**. Only this new review is written; the frozen method review remains
unchanged. No historical image viewing, image/video decoding, new pixel scoring,
timing estimate, physical inference, acquisition or main/raw/engine edit occurs.

## Initial assembly read and pins

Read the complete report, validation, input review and saved summary, plus the
actual full score/receipt structures through a read-only check. The previously
fully read frozen matcher/tests were rehashed unchanged. Main controls and
the CHARTER remain controlling; the evidence/source-truth review standards
and declared method/actual-human boundaries are not replaced by this check.

| Artifact | Read snapshot SHA-256 |
|---|---|
| report.md | `b4ba9bc16fc0f9c9a26a8f37c6d82b28c1f05938ad4d6f2200ee903fb7c388d4` |
| validation.md | `6a2f74e59c4b197fda5c740f5678d3ea35996b79adc54566ab90340c5016c843` |
| input-review.md | `5e4b1632344e7a3f33b00c33130b24a16b8d08485a8fed503ca7e58378f33460` |
| match.py | `c097560d6763ac09d1870ef572e65e9b12d70669e81d26712d94750596a710f9` |
| test_match.py | `6496581215bdf992334726db611a85b4400a76efb4e5a993f8dbb868c9797a95` |
| method-review.md | `86bedf752a1cef45f46e385e16fc33e37d6c3a2b248d870d9a672d32de3518c7` |
| scores01/scores.json | `0b2fb440b95c86024ded4435fdf740f7b2805730d15399fc8efd906bbdf4fa9d` |
| scores01/summary.json | `14252698ebbabd8fbc7cd6ae8c5f1ffe18848263ac09dabf4ae3bd7a62a537cf` |
| scores01/receipt.json | `d411c4e6d81ed42c8a5d4cc5aea94908c16f8e563f25b3c646c8926153c0de3b` |

At this read the separate complete pixel-to-score checker was still underway.
The report and validation accurately label its completion as pending. A
filename-only `rg --files` check for check/verification/verify names returned1
with no matches after successful file reads/hashes; that is not a source
failure, nor proof that the separate check cannot succeed. Its actual result
will be read before final closeout, not presumed from same-program repeats.

## Independent saved-array check actually executed

Ran a stdout-only script with
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B - <<'PY'`
from this unit directory. It used only pathlib, itertools, hashlib, json, math
and platform; it did not import the matcher, extractor, Pillow or a scoring
implementation. Its independent expectations were the protocol's six query
IDs, two branches, three literal rectangles and candidate indices0–475.

The script checked every saved SAD/MAE/correlation-array length, nonnegative
integer SADs, MAE=`SAD/sample_count` within1e-12, finite/null correlation shape
and bounds, and exact region counts from a separate nested grid enumeration.
It independently sorted every SAD array, rebuilt minima/ties/runner-up gaps,
all fifth-rank cutoff ties, neighbor expansions and complete ranks, then
compared those against every saved ranking and summary field. No minimum was
accepted merely because the summary supplied it.

It also rebuilt each branch/region's winner/repetition/reversal series, all
six per-query unions and the full union. It rehashed all492 named matcher
inputs (first requiring their paths to remain within this unit or the prior
Tilted unit), both saved output hashes, and byte-compared all three products
between scores01 and scores02. All assertions passed; exit0, Python3.12.14:

`PASS_SAVED_SCORE_ARRAYS_RANKS_SHORTLISTS_SUMMARY_AND_RECEIPT_PINS`.

This establishes **saved-array arithmetic/summary consistency and current
file integrity**, not that each SAD/correlation was originally computed from
the correct native pixels. That latter link remains the separate complete
arithmetic check. Bounds checks on correlation do not verify its formula.

## Exact checked results and report-table disposition

There are36 unique query/branch/region rows, each containing476 candidate
scores: **17,136 scored pairs**. The exact region sample counts are8736,
2560 and1320 for right_half, target_right and right_background respectively.
Every declared combination is present exactly once. All report table minima
and shortlist counts agree with the independent saved-array reconstruction.

| Query | right_half / target_right, both branches | Background nearest / bilinear | Complete per-query shortlist |
|---:|---:|---:|---|
| 6924 | 311 | 311 / 311 | 306–314 (9) |
| 6925 | 312 | 312 / 312 | 306–318 (13) |
| 6926 | 313 | 312 / 313 | 308–316 and318–321 (13) |
| 6969 | 356 | 356 / 356 | 352–358 (7) |
| 6970 | 357 | 356 / 356 | 352–360 (9) |
| 6971 | 358 | 357 / 357 | 355–361 (7) |

The26-frame union is exactly306–321 and352–361. Index317 is absent from
6926's own shortlist but belongs to the union through another query; the
report explicitly preserves that distinction. The union is not a gap-filled
replacement for the per-query sets or an exhaustive exposure-confidence set.

No exact minimum tie contains0 or475. None of the six branch/region series
reverses. Background NEAREST repeats312 across6925/6926 and356 across6969/6970;
BILINEAR repeats356 across6969/6970. These disagreements remain in the report
and underlying results, not repaired into a one-to-one relationship. The two
right-side-region series select the same indices, but overlap and shared bytes
make them dependent observations, not independent camera corroboration.

## Concrete wording recommendations

No material table, count or shortlist error was found. Two narrow terminology
recommendations were sent before closeout:

1. Replace **“The two primary-region series”** with **“The right-half and
   target-right series.”** Only right_half was the declared primary scene
   diagnostic; target_right was a sensitivity region. Agreement does not
   retroactively make both primary tests.
2. Replace **“raw mean absolute luminance difference”** with **“raw mean absolute
   stored Y/luma-code difference.”** The metric uses encoded grayscale/Y
   values, not photometrically calibrated luminance. Other report limits
   already reject calibrated brightness or intensity conclusions.

These are scope/terminology refinements, not evidence the saved computation
was wrong. Their disposition will be recorded below without erasing the
initial wording or stage history.

## Claim ceilings and strongest objection

The report correctly separates minima from authenticated exposure joins,
repeat-run equality from independent history, point-excluded scene scoring
from testing the points themselves, and a finite shortlist from all possible
counterparts. It gives background disagreement rather than only favorable
right-side minima. It neither claims a Tilted point observation nor converts
an unviewed or inferior counterpart into a negative light finding.

The complete input review supplies an attributed metadata/byte-admission pass,
with actual commands and source pins, not a decode or fresh all-PNG admission.
Its two-tick duration/endpoint distinction and Camera2 diagnostic qualification
remain in the report. The validation distinguishes the sandbox refusal from a
source failure and records repaired guards before historical scoring. Root's
extraction11-test/product checks remain root/author-attributed; this reviewer
has not independently rerun extraction or decoded its outputs.

Strongest remaining objection: a unique numerical minimum can select a related
processed image without identifying a unique original exposure. Shared ancestry,
field blending, frame duplication and temporal or spatial resampling survive
the exclusion mask. Even later cross-copy point agreement would not by itself
authenticate an emitter or exclude a common upstream artifact. No numerical
rank gap is a calibrated probability.

The proposed26-frame paired review is a useful finite next step, **not an
already performed or quantitatively accepted test**. It must retain all
per-query associations, native source identity and alternative-frame visibility
limits. The actual-human and consequential-measurement boundaries remain open.

Current disposition: report content and saved-array accounting are supported
within this review's scope, with the two narrow wording refinements requested.
Complete pixel-to-score reproduction and assembled final-status review remain
pending. No all-Luna clearance, causal ranking, source authentication or
investigation completion follows.

## Wording resolution and completed arithmetic-check read

Read the corrected report completely. Snapshot SHA-256
`5053db7981ca7b8544333c1a47fc3c59b9e59da01844ddb47117e7ad2dbe83b6`
uses **“The right-half and target-right series”** and **“stored Y/luma-code
difference.”** Both requested terminology refinements are resolved; the
original concerns and assembly-stage pins remain above.

The separate pixel-to-score result is now available and was checked, not
assumed. Read the complete415-line `check_scores.py`, SHA-256
`8fd81da7b5d18967e3c954d26815c22c03bb0795c06b4d1962fd67a60abc740a`.
Read the execution metadata and programmatically parsed every recomputed row
in `independent-check01.json`, SHA-256
`a81fa35c35c6e1786ffe5b2711641419b1023a694b70f121b8c10bd2926a6c65`.
An initial direct print of this large JSON was truncated; it was not treated
as a complete manual read. The subsequent bounded structured read checked
all36 rows and emitted only execution/result metadata.

The checker independently enumerates sample coordinates, reconstructs all482
native PNGs under own byte/luma/format checks, and uses integer SAD and
integer-moment covariance, rather than importing the producer/helper. It
validates the complete extraction product/map/source contract and checks
all517 tracked input identities before/after. It shares the same native source
bytes, Pillow PNG/resize implementation and NumPy runtime; the author is a
prior-informed reused AI. This is separate numerical implementation and
execution, not separate historical evidence or a blind/expert review.

This reviewer **did not execute that checker or repeat its pixel computation**.
Instead, a second stdout-only standard-library script parsed its pinned result
and compared all saved recomputed rows with `scores01/scores.json`, including
every SAD, MAE, exact ranking and complete summary. It reproduced the saved
maximum differences from the two existing result arrays. Exit0:

`PASS_CHECKER_RECEIPT_AND_ALL_SAVED_RECOMPUTED_ROWS`.

Recorded checker execution: Python3.12.14, NumPy2.3.5, Pillow12.3.0;
482 native PNGs and17,136 score pairs. All SADs, MAEs, ranks, cutoff ties,
neighbors, per-query shortlists and the complete summary agree exactly.
The maximum correlation difference is `1.2312373343092986e-13`, below the
predeclared absolute tolerance `1e-12`; maximum MAE difference is0.0. Root
reports separately reading the full checker and passing its23 synthetic
self-checks. That root replay is not claimed as this reviewer's execution.

This complete independent arithmetic result resolves the pending
pixel-to-score reproduction dependency for the **declared diagnostic**. It
does not resolve the physical/provenance objections above. A forthcoming
status-header update may describe this bounded verification as complete; it
must not imply actual-human acceptance, an authenticated exposure, point
presence/absence, original camera fidelity or causal validation.

**Final bounded disposition:** the report's numeric table, candidate counts,
26-frame next-review union and inference limits are supported by the inspected
records and completed scoped checks. Both identified wording issues are
resolved. No remaining material report/method overclaim was identified within
this review's scope. The source-authentication problem and proposed paired
qualitative observations remain uncompleted; the full investigation and broader
Luna reevaluation remain open. No historical images were viewed and no new
pixel scores or physical measurements were generated by this reviewer. Frozen
method, source and result records were not changed.

### Arithmetic-complete assembled-text check

Finally read the full updated report
(`5b5e509580301fe920b5d29a74c0b4f5f03213c4184fe7ff1ea13765cde1020a`)
and validation
(`8e5007e61e5d79d9cf4e69706797a5aa1d4dc4b30887b377e27e182e37340ab4`).
Their new independent-check status, exact-versus-tolerance distinction, recorded
execution attribution and shared-library limits agree with the inspected
checker/result. Grade A is confined to what the fixed algorithm calculates,
not historical exposure identification. Root's additional517-input rehash is
properly distinguished from a third scoring implementation. No further material
correction was identified. The remaining pending critical-header wording can
now be closed by reference to this completed review; the next paired image
review remains a proposal, not a completed result or human approval.
