# Independent Camera 2 reference-repair review

Declared 2026-09-11 18:56:40 UTC, before this reviewer inspects replacement-reference historical scores. Research-only under the [charter](../CHARTER.md), following the unsuccessful Camera 2 configuration preserved in the [v1 report](../reference-motion/report.md). The evidence-auditing and development-verification skills guide the distinction between reproducible arithmetic, correct artifact lineage, and unvalidated physical correspondence.

## Declared bounded review

Only the invalid C2-R3 reference may change, under a new reference ID and an explicitly saved description/coordinate association. C2-R1, R2, R4, R5 and R6; the 71 preserved Camera 2 event PNGs and exact PTS; template sides 19 and 27; radius 24; fixed-baseline matching; all-six admission; all three mapping models; and leave-one-reference-out rules remain unchanged. The original algorithm must retain SHA-256 `adb48c18a928ab44bba0f30cc8b6cdffbdd3a60918464600a568249b7822640e`. The unsuccessful v1 outputs remain preserved.

The review will check the replacement's baseline-only preflight, both-template acceptance by the old gates, preflight/declaration/configuration hashes, recorded selection/review scope and their ordering relative to later-frame scoring. Root and annotator acceptance are computational review, not actual human or expert certification. Familiarity with prior event results prevents treating this exploratory repair as an unused event-level holdout.

Each completed run must contain exactly 852 match/score-grid rows and 426 model rows. For the five retained references, all 710 rows and corresponding grids must be exactly equal to the matching v1 records, including rejected outcomes. All 142 replacement-reference rows must be present. Complete input identities, per-frame metadata, score grids/undefined masks, match gates, six-reference admission, every admitted model and each LOO fold will be independently checked. Two fresh runs must reproduce all deterministic products, with receipt counts distinguished from receipt-listed products.

Numerical verification will reuse the previously checked independent FFT/integral-image NCC and mean/complex-plane/QR mapping oracles in the frozen [v1 verifier](../reference-motion/verify.py), without invoking the production historical-run entry point. Grid finite-value comparisons use absolute `1e-8`; shapes and undefined masks are exact. Fit arithmetic uses absolute `1e-8` and relative `1e-10`. Stored-grid decisions are audited at their exact declared thresholds, separately from numerical agreement; independently recomputed grid decisions and threshold proximity remain visible.

Only new wrapper/preflight contracts need additional focused testing. The already-passing full v1 matcher and transform suite is not rerun merely because a reference ID changes. Wrapper failures, invalid configurations, mismatched preflight pins, changed retained references/parameters, and overwrite attempts must fail closed or remain explicitly untested. No original source image, old run, algorithm, threshold or declaration is edited by this reviewer.

## Interpretation boundary

A better-admitted v2 reference set would show that this configuration passes more of the fixed method's checks. It would not repair the old identity error retroactively, authenticate a physical landmark, establish stationary camera geometry, or permit acceleration/cause claims. Unchanged-reference equality tests scope preservation and determinism; common correspondence errors can remain unchanged too. Any residual reference, size, model, visibility or geometry failure must remain in the report.

## Status at declaration

Replacement choice, baseline preflight, wrapper inspection and released historical paths are pending. This reviewer has not opened replacement-reference historical outputs. Results will be appended with exact reviewed code/configuration and report hashes.

## Preflight and wrapper review — 2026-09-11 19:09:59 UTC

Before legitimate historical scoring, review found two contract weaknesses in the initial wrapper: a self-consistently rehashed preflight could change the replacement object without exact candidate/first-qualified validation, and retained-baseline failure could occur before computed rejection records were saved. Root corrected both before the completed preflight. The reviewed driver SHA-256 is `092ca6057a5f3ecbfa96bd4968bee9f1e681fb8e7b50c66ff724f65139d33b18`; root wrapper tests are `149534a21922ab4a185f482dbfd6b0675e446a0b4613924235513d171ede06e3`. Code inspection now confirms exact current preflight procedure/runtime/source pins, baseline-score recalculation, first-qualified selection, exact approved candidate/retained-reference objects and fixed parameters. Baseline scores and grids precede retained-reference rejection. No remaining blocking run-contract defect was found in that bounded review.

Root's four passing controls include six pure-function selection mutations; despite the broad test name, those are not six actual rewritten-file entry tests. The separate [verification-preflight01.json](verification-preflight01.json) adds one real file-level negative test. It copies the completed preflight into `preflight-tamper01`, changes R7 from `[333,413]` to `[334,413]`, and updates the copied receipt's selection hash so all copied product hashes remain internally consistent. Calling the actual `execute('run',...)` entry rejects with `exact-approved-reference-set`. A sentinel on `frame_analysis` records zero calls and forbids later-frame scoring. The preserved [failure record](verification-failure01/failure.json), initial state and snapshots remain in `verification-failure01`; no accepted receipt, match/model/grid output or historical overlay was produced. This tests one altered-coordinate file-level rejection, not every possible tampering or failure path. The legitimate preflight and source code remained unchanged.

The released `preflight01` receipt is `8fea3c45f64ecf96aefa2c329d0f322a20d03ec42daea80bef9fad49706318b6`; the selected configuration is `1615cf412019ea9e15d116e20007966890238c3beb68e54abfa5a08666db8fae`. It contains 11 receipt-listed products, 12 files including its receipt. The sole proposed candidate C2-R7 is the first jointly qualified candidate; no other proposed or rejected candidate is concealed. Its complete object replaces R3 and the other five objects are unchanged. All 12 baseline grids (five retained references plus R7, two sizes each) agree with the independent FFT calculation to maximum absolute difference `1.4432899320127035e-14`, with no winner/competitor/tie/flag/status decision differences. R7's baseline template standard deviations are 14.6417510878 and 12.2221598701 for sides 19 and 27; both return their seed with no rejection flags. These are construction-image suitability results, not independent stationarity or later correspondence evidence.

Command actually run:

```text
/Users/admin/.pyenv/versions/3.13.7/bin/python3 research/sherlock-wtc7-investigation/camera2-reference-repair/verify_repair.py --preflight preflight01 --tamper-contract preflight-tamper01 verification-failure01 --out research/sherlock-wtc7-investigation/camera2-reference-repair/verification-preflight01.json
```

That passing receipt pins verifier `78091e1d2dfc6e717d3f376d3ff07fe91216aa0a954ac13d0afc6353aad8df04`, before additive declared-baseline metadata, exact output-name/runtime checks and overlay-pixel reconstruction were added for the historical review. The numerical oracles and production code were not changed. All 33 receipt-listed original v1 products were rehashed successfully. Replacement-reference historical outputs were not read in this preflight/control review.

Selection limitations remain material: the template is constructed from its own baseline and the two sizes overlap; neither self-match nor agreement between sizes supplies independent physical evidence. Final hashes establish identity, not chronology alone. Root's preserved preflight completion/release and this pre-output review establish the recorded local ordering, while prior event familiarity prevents a clean holdout claim. Joint transforms and LOO predictions may legitimately change after replacing one point even though the other five unconditional match records stay identical.

## Completed historical product review — 2026-09-11 19:17:17 UTC

Root released `run01` and `run02` after observing their complete artifact receipts. The original launching shell exit statuses/session IDs were not recovered after a context transition; this review does **not** certify those unrecovered statuses. The completed receipts, full inventories, input/procedure snapshots, post-computation producer checks and independent product review are the available execution evidence. No replacement historical output was opened by this reviewer before that release, and no historical analysis was restarted.

The final [verification03.json](verification03.json) passes with verifier SHA-256 `c035c33f16404a459e712b83221201cffc822495ce13a23e28dbc9197c1f9315`; its receipt SHA-256 is `b3e7a57c35a2da1bee7c9fe393e3da4a20b3ba4f2bed3c140298f6ab4e34a9ea`. The reused fit-oracle dependency is additionally pinned before import and after checking to `e2bb15bb6dfc9317b51db40602e53191570c888205cf26640c0b40197340c912`, matching its original v1 verification record. Python is 3.13.7, NumPy 2.3.4 and Pillow 12.0.0; executable and producer runtime identities are checked against both runs. This verifies the recorded local runtime, not cross-platform numerical invariance.

Command actually run, with shell exit 0 recovered for this verification command:

```text
/Users/admin/.pyenv/versions/3.13.7/bin/python3 research/sherlock-wtc7-investigation/camera2-reference-repair/verify_repair.py --preflight preflight01 --runs run01 run02 --out research/sherlock-wtc7-investigation/camera2-reference-repair/verification03.json
```

Both producer receipts have SHA-256 `d2b8ae21b6fe3b0190538142b1db37be9f5a31b80d581d5ac6c39e90a952f320`. Each run has exactly **25 receipt-listed products, 26 files including the receipt**; all 26 file contents are identical across the two distinct, non-aliased run directories. All declared native input identities, exact PTS, original source/map and procedure hashes are checked. The first identical copy supplies the numerical audit, not a second independent historical observation.

- All **852 match rows**, **852 named grids** and **426 model-status rows** have exact declared coverage and frame-major order.
- The **710 retained-reference records and grids** are exactly equal to v1, including every rejection and all grid bytes; no wrapper metadata exception was needed.
- All **142 R7 grids**, containing **340,942 score values**, were independently recomputed. Maximum absolute NCC difference is `9.424752644981993e-15`; masks, support, native template coordinates, metadata and stored-grid decisions agree. No independently recomputed winner/competitor/tie/flag/status decision differs.
- All **291 admitted model fits** and **1,746 LOO folds** agree with the independent mean/complex/QR oracles within the declared tolerances. The **135 reference-quality-failure model rows** correctly remain uncomputed; no point was dropped to obtain a fit.
- All **12 overlay PNGs** were reconstructed pixel-for-pixel from the frozen native frame, stored marker/label rows and analytical footer. This checks rendering lineage, not visual landmark identity. Root and annotator own the separate visual interpretation.

The numerical admission result retains important failures:

| Template | Each model computed | Translation screens | Similarity screens | Affine screens |
|---|---:|---:|---:|---:|
| 19×19 | 26/71 | 26/71 | 26/71 | 25/71 |
| 27×27 | 71/71 | 71/71 | 71/71 | 71/71 |

R7 passes both sizes in all 71 frames. The remaining **45** match rejections are unchanged C2-R6 19×19 `ambiguous_competitor` outcomes; they prevent all three models from being admitted on those frames. Across sizes there are **61 coordinate-or-status disagreements**: 8 for R1 and 53 for R6, including 16 where both sizes accept. A separate read-only rebuild of the entire disagreement list exactly matches `summary01.json`; summary01 and summary02 are byte-identical with SHA-256 `f4a26efc136cd4241b1774a3721109ffc84d7d7cf73d155aec8a070e7b752bd8`. Totals independently agree: 807 candidate matches, 45 rejected matches, 291 computed models, 135 uncomputed quality failures, 290 exact stored screen passes. Larger-template agreement is a sensitivity result, not automatic evidence of greater physical accuracy.

### Exact cutoff and floating arithmetic

All three near-threshold rows occur at f7021, 19×19. Five matched coordinates equal their baseline coordinates; R6 alone changes from `[557,319]` to `[555,319]`. Leaving R6 out gives five identity point pairs. Three retained source points have nonzero integer twice-area `-9285`, so the affine identity map is uniquely identified; translation and proper-similarity identity maps are likewise unique. The exact omitted R6 error is therefore `[-2,0]`, squared norm 4, norm exactly **2 pixels**.

The stored LOO maxima are 2.0 (translation), 1.9999999999997726 (similarity) and 2.000000000000796 (affine). The independent affine calculation gives 1.9999999999998863, reversing only the floating binary screen at that boundary; its other LOO errors are below 2. The producer's original affine `false` remains preserved and correctly reported under its exact `<=2` implementation. The exact identity-fold result explains why this one nominal model-screen difference is numerical cutoff sensitivity, **not demonstrated physical inconsistency**. No tolerance or threshold was changed post hoc, and no hypothetical corrected pass count replaces the published count.

### Preserved review failures and fixes

- A second static reviewer found that the initial verifier allowed the same directory twice and omitted a direct pin for the imported fit-oracle dependency. Both guards were tightened before full historical verification. [verification-duplicate-rejection01.json](verification-duplicate-rejection01.json) preserves the expected exit-1 rejection `two distinct historical run directories required`, exercised with the preflight directory supplied twice; it did not inspect historical results as two runs.
- [verification01.json](verification01.json) is the initial failed historical review, not a failed producer run. Its exact `complete stage input/procedure lineage` rejection came from the reviewer's assumption that the two preflight-parent keys would be absolute. The producer stored their repository-relative command spelling. A read-only comparison found exactly those two spelling differences and no hash-value mismatch. The verifier now permits only the exact absolute or exact repo-relative form of each known parent file, exactly once, and records the original spelling. No source, selection, producer or historical product was corrected.
- [verification02.json](verification02.json) then passed full coverage. The final verification03 adds only the explicit independent and analytic cutoff annotation above. Both prior full-review receipts, the two passing preflight receipts, the actual tamper fixture and its failure record remain preserved. The final verifier is frozen for root's independent rerun.

This review supports a bounded derived claim: replacing the confirmed erroneous selection allows the unchanged numerical method to admit this Camera 2 configuration on the reported frames, with strong size dependence and the exact cutoff effect retained. It does not establish material-point stationarity, a unique camera plane/model, subpixel accuracy, target motion, gravity compatibility or cause. Shared apparent-position errors can fit all three mappings; neither repetition, FFT agreement nor LOO removes that limitation. No v1 invalid-reference finding is retroactively upgraded.

## Root rerun and bounded report disposition

[verification-root01.json](verification-root01.json), SHA-256 `461ac50a0e92ce3dd2a0a12f1361ef44025e53cb30b7635696af0a8c566e291c`, is a passing root rerun of the frozen verifier. This reviewer compared its complete JSON with verification03: only `command` differs. It is independent execution of the same audit program, not an independently designed second oracle.

The [report](report.md) was read in full at SHA-256 `bd571c775f7be0c451ba07fbdb534ec2a91449686a65ed7edb006208acb8b384`. No substantive numerical or causal overstatement was found within this review's scope. A further read-only check confirms all 142 R7 outputs are accepted at `[333,413]`; for side27 the other four non-R1 references and R7 remain at baseline, while R1's only displacements are `[0,-1]` and `[0,0]`, supporting the stated translation range. The report appropriately limits these integer image-space outputs, preserves the 45 smaller-template rejections and exact-cutoff flag, discloses unavailable launcher exit statuses, and does not upgrade them to physical calibration or causal evidence.

Two minor qualifications were returned to root: describe `<=2` as the **unchanged exact** gate rather than a mathematically “strict” inequality; and keep the ten annotation-comparison paragraph provisional until its actual final artifacts are reviewed. The annotation arithmetic/visual review belongs to the separately identified reviewer; this report disposition does not certify an unfinished comparison. A later report revision needs its own bounded changed-text hash disposition, not silent inheritance of this one.

### Final changed-text disposition

The final report at SHA-256 `45661aa0dd763d0c26c6e2b8fc77b171f123ea40d1c7220d56cc131742e3e8ad` resolves both qualifications. This additive check was limited to the amended cutoff/comparison statements and their finalized comparison evidence; no new numerical or visual analysis was run, and the frozen verifier and historical outputs were not changed.

The cutoff is now accurately described as the **unchanged exact `<=2` gate**. The finalized [comparison report](comparison-report.md), SHA-256 `1d78127e8a09bca98a46c8583dd0729030aab2a8e626ef0c89aa2d33d2a73ea6`, and all ten saved JSON rows support the newly stated outcome: both sizes accept each of the five fixed R7 candidates; all lie inside the unchanged subjective envelopes; automatic-minus-manual differences are `[-1,+1]` in the first four frames and `[-1,+2]` in the last. Every row records run02 equality, consistent with the prior full-run byte comparison. Runtime fields state Python 3.13.7. The three comparison outputs (`comparison.json`, `comparison-repeat01.json`, `comparison-root01.json`) have the same SHA-256 `02525db6ef42ba96f4e4e4cbe810b5b85a60c113b21f5dfe11a68abbf025b67e`.

The final comparison report retains the initial helper failure and limits the outcome to coarse appearance-envelope agreement; it does not convert ten comparisons into ten independent observations, physical identity, stationarity, calibrated accuracy or cause. Actual visual coverage remains the annotator/root's separately recorded work, not a claim that the comparison helper or this changed-text check viewed imagery. The validation text also now accurately identifies the duplicate-directory control as the preflight directory supplied twice, before historical inventory inspection. No remaining issue was found in the amended statements within this bounded review.
