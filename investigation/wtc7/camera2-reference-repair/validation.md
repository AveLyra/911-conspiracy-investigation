# Camera 2 repair: execution and verification

This is an exploratory follow-up under [PROTOCOL.md](PROTOCOL.md), not a replacement of the failed v1 record or physical camera calibration. The full investigation remains active. Numerical and visual acceptance below are computational checks, not human or professional engineering approval.

## Pre-scoring chronology and preserved versions

1. The protocol specified one-reference replacement, at most three ordered baseline-only candidates and unchanged numerical gates before new candidate scoring. The annotator proposed only C2-R7 at (333,413), preserving [candidate-seeds.json](candidate-seeds.json) and [selection-review.md](selection-review.md). No fallback is proposed and no later frame was inspected for this selection. Prior visual familiarity and v1 results remain disclosed.
2. Root's initial wrapper controls completed in [controls01](controls01/receipt.json): three cases passed. The pure selection checks exercised ordered choice, both-size and visual acceptance, no-qualified-candidate and missing-size behavior; synthetic frames checked actual matching/all-six admission; preservation checks exercised exclusive output creation. This did not exhaustively validate preflight-file mutation handling.
3. [baseline01](baseline01/receipt.json) completed without scoring new candidates: it saved a labeled full-baseline marker, exact native template crops and 10× nearest-neighbor displays. Root viewed the original native f6593, the full marker and both enlarged template displays. [visual-review.json](visual-review.json), recorded at 2026-09-11 19:01:56 UTC, accepts the source-pixel association within the visible bright patch, explicitly not a surveyed corner or measured brightness centroid. It predates new numerical preflight and replacement-reference historical scores.
4. Independent code review identified a run-stage contract gap: the original wrapper checked artifact hashes and retained references but did not fully bind the replacement object, selection order, settings and procedure/input identities to the approved preflight. Root strengthened those checks **before historical scoring**. Preflight now also saves finite score/grid outputs before a retained-reference failure, so a possible rejection is not reduced to an exception alone. The earlier code/test snapshots remain in controls01/baseline01. No v1 numeric function, old image or annotation was edited.
5. [controls02](controls02/receipt.json) passes four cases, adding six mutations of the **pure selection-contract function**: replacement coordinates/ID, later choice instead of the first, radius, template sizes and retained-reference coordinates. The test's name mentions internally rehashed mutations, but it does not itself create/re-hash preflight files; do not represent that label as full file-level mutation coverage. Separate wrapper-entry review is recorded below when completed.
6. [preflight01](preflight01/receipt.json) then completed successfully. All five retained baseline references and R7 pass both sizes. R7 standard deviations are 14.641751 and12.222160 Y code values; NCC is approximately1 for each self-match, with distant-competitor margins0.476175 and0.542073. These describe baseline matchability, not historical stationarity or tracking precision. Only one candidate was tested and none rejected. The selected configuration was frozen and supplied to the annotator before it reviewed the five fixed evaluation frames and before legitimate later-frame scoring.

Preflight `selection.json` SHA-256 is `1615cf412019ea9e15d116e20007966890238c3beb68e54abfa5a08666db8fae`; receipt SHA-256 is `8fea3c45f64ecf96aefa2c329d0f322a20d03ec42daea80bef9fad49706318b6`. Candidate JSON is `b093c5041ca34b5e1e27b617cc681f46cbd0327c6c525bec89faf43f7991078e`. These hashes pin bytes; the recorded execution and review sequence, rather than a hash alone, supports the preflight-before-scoring chronology.

Root freshly checked all receipt-listed products in baseline01 (12), preflight01 (11), controls01 (11) and controls02 (11): all45 hash/size pairs match. Existing directories were not overwritten. The inherited numerical module retains SHA-256 `adb48c18a928ab44bba0f30cc8b6cdffbdd3a60918464600a568249b7822640e`; the new wrapper and tests retain their own versioned snapshots and runtime pins.

## Historical execution and independent checks

Both legitimate runs have complete receipts and all declared products. Their launching command response was truncated across context recovery, so its exact terminal shell statuses/session IDs were not recovered. A read-only process-list attempt was denied by the environment; no duplicate run was launched. Completion is established by the producer's receipt-writing order, both completed receipts, exact inventories and independent verification of every product. Do not upgrade this into a claim of observed exit codes.

The actual commands launched were:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera2-reference-repair/repair.py run --preflight research/sherlock-wtc7-investigation/camera2-reference-repair/preflight01 --out research/sherlock-wtc7-investigation/camera2-reference-repair/run01
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera2-reference-repair/repair.py run --preflight research/sherlock-wtc7-investigation/camera2-reference-repair/preflight01 --out research/sherlock-wtc7-investigation/camera2-reference-repair/run02
```

Each run contains 852 match rows and complete grids, 426 model-status rows, 12 overlays and preserved preflight/procedure snapshots: 25 receipt-listed products, 26 files including the receipt. All 26 pairs are byte-identical. Runtime pins resolve to Python 3.13.7, NumPy 2.3.4 and Pillow 12.0.0. The frozen repair driver is `092ca6057a5f3ecbfa96bd4968bee9f1e681fb8e7b50c66ff724f65139d33b18`. No source, selection, producer, numerical gate or accepted run product changed after preflight.

## Independent verification, including failed attempts

The [independent review](independent-review.md) records the actual file-level altered-coordinate/rehashed-preflight test in [verification-preflight01.json](verification-preflight01.json). The real run entry rejects the copied altered selection; a sentinel records zero later-frame-analysis calls. [verification-failure01](verification-failure01/failure.json) and its snapshots preserve that intentional failure. This is one file-level mutation test, not exhaustive adversarial validation. The separate preflight02 verification adds baseline declaration, bounds and inventory/runtime checks.

The initial historical [verification01.json](verification01.json) failed because the independent checker assumed absolute parent-preflight pin keys, whereas the producer recorded the legitimate repo-relative command spelling. Exactly those two keys differed, not their file identities. The checker now accepts only one of the two explicit equivalent spellings per parent and retains the raw spelling. Producer/run files were not changed. A separate [duplicate-directory rejection](verification-duplicate-rejection01.json) preserves the expected failure when the same directory is supplied twice (the test used the preflight directory twice, before historical inventory inspection); duplicate inputs cannot masquerade as two independent executions.

[verification02.json](verification02.json) passes full coverage. The final [verification03.json](verification03.json) adds an arithmetic explanation of the three near-cutoff model rows, without changing a stored decision. Final verifier SHA-256: `c035c33f16404a459e712b83221201cffc822495ce13a23e28dbc9197c1f9315`. Root read the complete verifier and its changes, then ran:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera2-reference-repair/verify_repair.py --preflight preflight01 --runs run01 run02 --out research/sherlock-wtc7-investigation/camera2-reference-repair/verification-root01.json
```

That call was polled to terminal exit0. [Root's receipt](verification-root01.json) equals verification03 in every field except the recorded command/output path. Complete coverage is:

- All 710 unchanged-reference records and complete grids exactly equal their v1 counterparts, including rejections.
- All 142 new R7 grids, 340,942 values: maximum independent FFT difference `9.424752644981993e-15` under the declared `1e-8` tolerance; exact masks and no winner/competitor/tie/flag/status disagreements.
- All 426 model rows, 291 admitted fits and 1,746 LOO folds checked through independent mean/complex/QR calculations. The other 135 rows retain all-six reference failure.
- Both source/input/product inventories and every native PNG/luma/PTS pin checked; all 12 overlays reconstructed pixel-for-pixel. Shared Pillow rendering is a lineage check, not independent material-point recognition.
- At f7021/side19, independent arithmetic and the exact identity-map omitted fold explain the affine false flag as rounding at the unchanged two-pixel cutoff. The stored maximum `2.000000000000796` and independent `1.9999999999998863` straddle exactly 2. Neither the original flag nor any threshold is rewritten.

The frozen v1 numerical controls/oracles are reused, not rerun in full merely because the reference ID changed. Root's four wrapper controls, the exact-input regressions, new-grid and all-fit checks are the proportional new checks; no cumulative test count is a scientific-confidence estimate.

## Descriptive and visual review

Root's [summarizer](summarize.py) only counts/compares preserved products. Two fresh executions completed with exit0; [summary01](summary01.json) and [summary02](summary02.json) are byte-identical. The helper checks both full inventories and input preservation. It reports 807 admitted/45 rejected matches, 291 computed/135 uncomputed model rows, 290 stored screen passes, and 61 cross-size coordinate-or-status differences. Independent review rebuilt the complete difference list: eight R1 and 53 R6 pairs, including 16 pairs admitted at both sizes. No third historical fit was performed.

The annotator froze [evaluation-annotations.json](evaluation-annotations.json), SHA-256 `4ef189587f0039a01b7968e83784779196008d541fa357aeec97dba159af67d6`, before the new automatic outputs were released. It viewed five native evaluation images and five labeled crops; all five R7 appearances were localized at subjective ±3 or ±4 pixel envelopes. Prior event familiarity remains disclosed. The original annotations and selection were not revised after output access.

Root actually viewed all 12 `run01/overlay-{6593,6654,6751,6931,7013,7104}-{9,13}.png` overlays, not just their file inventory: six source frames at native geometry, two sizes each. R7's marker stays associated with the intended bright lower-central foreground patch. The smaller-patch R6 is visibly marked red at f6654/f6751 while the larger one is green. Root did not measure a new center from these post-output overlays, and did not inspect every image anew. The annotator's separately documented all-12 visual review and ten new coordinate comparisons are in [comparison-report.md](comparison-report.md); their exact run/failure/validation scope is recorded there. No computational visual review is described as human or professional acceptance.

### Final coordinate-comparison check

All ten new R7 comparison rows are accepted and inside their frozen subjective envelopes, with automatic-minus-manual differences (−1,+1) for the first four evaluation frames and (−1,+2) for f7104, in both sizes. All ten run02 rows equal run01. The comparison report preserves its initial helper failure: a reviewer incorrectly equated initial procedure pins with the final dependency union. The corrected helper checks the exact union of initial, input and preflight pins; source/run/annotation files were not modified. The failed helper snapshot and execution history remain linked in that report.

Root read the complete final helper and report, then independently executed:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera2-reference-repair/compare_r7.py --output research/sherlock-wtc7-investigation/camera2-reference-repair/comparison-root01.json
```

It completed with observed exit0. [Root's comparison](comparison-root01.json), [the original](comparison.json) and [the annotator's repeat](comparison-repeat01.json) are byte-identical, SHA-256 `02525db6ef42ba96f4e4e4cbe810b5b85a60c113b21f5dfe11a68abbf025b67e`. Actual runtime is Python 3.13.7. The helper includes focused coordinate/envelope/status/key/PTS controls; it does not repeat visual inspection, independently authenticate a landmark or quantify calibrated accuracy. The original annotations remain frozen.

No new agency-production payload or held packet content has been inspected. No source decode, source modification, bridge invocation, outside transfer, canonical promotion, filing, commit or push was performed. The bounded diagnostic's interpretation is in [report.md](report.md); the comprehensive goal remains active and incomplete.

## Repository closeout

Root's closeout freshly rehashed all 95 receipt-listed products across baseline01, preflight01, controls01/02 and run01/02; every byte size/hash matched. Five current Python helpers parsed successfully. At that check, ten local Markdown/navigation files had 177 resolvable local links and no unexpected trailing whitespace. Scoped Git whitespace checks and the repository's strict record validator passed. These are artifact/record-hygiene checks, not scientific validation. Current work remains uncommitted on `main` at `54c21d3`; unrelated changes are preserved.

The original producer launcher exit statuses remain unavailable as disclosed above; completed product receipts are not relabeled as terminal-output observations. Both root verification/comparison reruns and descriptive summaries have observed exit0. No new decode or replacement historical run is awaiting a poll. The next task is the production crosswalk after approval or the separately declared target-feature trackability study, not another rerun of this completed prerequisite.
