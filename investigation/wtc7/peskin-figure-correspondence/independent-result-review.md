# Independent dense summary and regional arithmetic verification

2026-09-13. **PASS within the declared numeric scope.** The full accepted
summary and all 86 regional grayscale diagnostics agree with independent
recalculation. This is post-producer verification, not independent source
discovery, exposure identification, historical timing or physical validation.

## Declaration, independence and coverage

The controlling main AGENTS/WORKFLOW/START-HERE, investigation CHARTER and
unit PROTOCOL/METHOD were read. Development-verification, evidence-falsification-
auditor and source-of-truth safeguards governed new worktree-only artifacts.
Read complete `summarize_dense.py` (95 lines), `check_regions.py` (65 lines),
`CANDIDATE-REVIEW-01.md` (43 lines), `independent-target-review.md` (191 lines),
and `DENSE-CONTINUATION-02.md` (41 lines), plus the scoring/raster definitions.
Full code/declaration pins are recorded in the checker and result receipt.

The [independent checker](independent_result_check.py) was frozen at SHA256
`3f4a8d5547e387ec3dbfd72a8425a477269c2884195598ef0b3f6320eac93455`
before opening any historical dense result or candidate pixel. Its synthetic
control gate passed first. Root then expressly released the following exact
READY files; no failed `dense01` payload was admitted or inspected:

| Frozen producer input | SHA256 |
|---|---|
| [primary-summary.json](primary-summary.json) | `c34061bdc218dfd9c818766066ed5aecc636a39f815ef1340ca57dae769327b3` |
| [regions01.json](regions01.json) | `9e9639e15ea1385ae7aa09bfb206f6b333cb68939fa526bd04448a9682936868` |

This timing establishes controls/code-before-new-results, not a blind
independent discovery exercise: producer code, selected method, target-region
review and earlier screening context were known. No producer module/function
is imported. Ranking uses independently written ordering and connected-index
grouping, but its per-frame scores remain **supplied producer results**, not
fresh independent FFT surface measurements.

Regional coordinates/exclusions are read as literal data from the pinned
`check_regions.py`; they are attributed to the prior target-review transcription,
not independently rediscovered image regions. This arm reimplements exact
target-pixel-center masks and fixed-transform sampling, then computes Pearson
using explicit overlapping pairs, separate means and `math.fsum` centered sums.
Pillow grayscale/bilinear rasterization is shared with the producer; this is
not a second independent image-decoding/resampling library.

## Synthetic gate and actual execution

The [control receipt](fixtures/independent-result-controls01.json), SHA256
`583c6bbdfba52bdb5e277ac2ffe86e08f03c4695b5aa961e6f69e3fb6b6aec50`,
records **24/24 PASS**, exit 0 before historical input access. Coverage includes
all disconnected bands, reversed order, duplicates, empty targets/candidates,
tie ordering, absent dynamic values, nonfinite rejection, positive/negative
linear relationships, flat/empty/below-32-pixel rejection, exactly 32 pixels,
coverage below/at 85%, overlap-only means, nonbinary masks, outer-edge/half-open
mask boundaries, expanded exclusions, fixed-view identity/padding and changed
transform rejection. A grouped 40-seed-case integer-array comparison against
exact Fraction raw moments had maximum Pearson error
`5.551115123125783e-17`. The 24 tests are not 24 independent source validations.

Both commands used the bundled Python executable
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
in `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, with `-B`.
Full `argv`, Python and Pillow versions are retained in each receipt. Controls:

```text
research/sherlock-wtc7-investigation/peskin-figure-correspondence/independent_result_check.py controls --output research/sherlock-wtc7-investigation/peskin-figure-correspondence/fixtures/independent-result-controls01.json
```

Historical verification, after READY, reran the same controls before opening
the pinned historical inputs:

```text
research/sherlock-wtc7-investigation/peskin-figure-correspondence/independent_result_check.py verify --summary-sha256 c34061bdc218dfd9c818766066ed5aecc636a39f815ef1340ca57dae769327b3 --regions-sha256 9e9639e15ea1385ae7aa09bfb206f6b333cb68939fa526bd04448a9682936868 --output research/sherlock-wtc7-investigation/peskin-figure-correspondence/independent-result-check01.json
```

Both first executions passed; there is no failed run hidden by a corrected
receipt. Pillow 12.3.0 emitted a `getdata` deprecation warning, not a failed
measurement or decoder warning. No warning-driven implementation change was
made after seeing historical results. Every output was create-only.

## Actual agreement

The [numeric verification receipt](independent-result-check01.json), SHA256
`4969c34b87f50fd3c6d8915fb94407a4ba37a0b0edc2f4aaa6d9f4ace4e4a700`,
contains full reconstructed ranking/band structures, all regional outputs,
18 input pins and all 12 native-image byte/hash entries.

| Accepted run | Frames |
|---|---:|
| dense00 | 240 |
| dense11 | 240 |
| dense12 | 239 |
| dense13 | 240 |
| Total | 959 |

All **1,918 target-frame relations** were checked for complete target membership,
local frame index and PTS/timebase join. Stored independent-probe PTS lists
match the frame tables exactly within each declared half-open interval; global
PTS are unique/increasing. Receipt source/version/runtime identities and
frame/probe/anchor-count fields were checked. This rechecks saved metadata,
not the source video bytes or anchor pixels themselves; the video was not
opened or decoded by this arm.

All four target/metric rankings, their complete top-four rows/transforms and
every disconnected 0.005/0.01/0.02 score band match **exactly**, not merely the
best score or outer envelope. The failed partial run contributes zero accepted
rows. A 239-frame chunk is recorded as such, with matching stored probe coverage;
this check does not reinterpret it as a dropped original-camera frame.

Regional coverage is **12 candidate-target pairs**, seven for T148 and five
for T149, from 12 native images plus two target JPEGs. All candidate native and
target byte pins were verified before pixel reading. The source-selected
transform was fixed; no fitting or candidate selection was repeated on these
regions. All 86 selected-pixel and valid-pixel counts and nullness decisions
match exactly. There are zero null regional scores here. Maximum absolute
coverage difference is `0.0`; maximum absolute Pearson difference is
`1.4432899320127035e-15`, below the **pre-result absolute tolerance `1e-12`**.
These are numerical residuals, not confidence bounds or source uncertainty.

## Inference ceiling and preservation

Agreement verifies aggregation and fixed-raster regional arithmetic. It does
not authenticate clocks, recover source-generation history, establish a unique
original exposure, verify pure flame/smoke segmentation, provide thermometry,
or decide structural mechanism or intent. High correlation and a narrow score
band can coexist with repeated structure, dependent frame sequences and
unmodeled transforms. A second implementation does not make these frames an
independent camera or historical witness.

The checker did not re-decode media, create PNGs, rerun the FFT search, inspect
the failed `dense01` directory, or certify the still-separate same-code
reproductions. It did not visually inspect images; pixel processing is not a
human full-frame source review. No main/raw/status/legal file, producer or
earlier artifact was edited; no package install, web call or transmission.
