# R7 annotation comparison and post-output overlay review

## Comparison criteria declared before opening the new outputs

2026-09-11. Compare the five frozen R7 annotation rows at both 19×19 and 27×27 template sizes: ten expected keys `(camera2, frame, C2-R7, size)`. The annotation JSON is frozen at SHA-256 `4ef189587f0039a01b7968e83784779196008d541fa357aeec97dba159af67d6`; do not revise its coordinates, envelopes or status after seeing matching outputs.

Join exact frame/reference/size identities, native PNG hashes and rational source PTS. Duplicate keys, mismatched identities or changed frozen inputs are contract failures, not numerical agreement. Keep a missing automatic row explicit. Preserve all supplied scores, competitors, acceptance/rejection statuses and reasons. For a finite native integer candidate at a localized manual row, compute automatic-minus-manual `(dx,dy)` and classify inside only when both absolute differences are no greater than the corresponding subjective envelope halfwidth. Rejected finite winners remain eligible for that coordinate comparison but do not become accepted matches. Ambiguous/unavailable manual rows would retain their status and have no guessed coordinate comparison.

Run01 supplies the automatic candidates. Check the same ten run02 records for exact equality as a bounded repeat check, not a new independent observation. Review all twelve run01 overlays: baseline f6593 plus f6654, f6751, f6931, f7013 and f7104, each at halfwidth 9 and 13. Record actual post-output visual coverage and any wrong-feature, rejection, label/occlusion or identity limitations; do not re-annotate the other five references or amend the pre-output record. A helper re-execution reproduces comparison arithmetic, not the visual review.

This is computational AI review on familiar retrospective images, not human review, clean-holdout validation, calibrated accuracy, physical stationarity, camera calibration, target motion or cause. No raw decoding, new source, held/agency-production contents, bridge, network or shared procedure/configuration edits are part of this comparison.

## Results

The [ten-record comparison](comparison.json) is complete. Each template size has five accepted R7 candidates, all five inside the frozen subjective manual envelopes; there are no missing, rejected, outside-envelope or no-coordinate R7 results in this fixed sample. All ten compared run02 records exactly equal run01. Two template sizes and two executions of the same retained inputs are not independent historical corroboration.

| Frame | Automatic center, both sizes | Frozen manual center | Automatic minus manual, both sizes | Frozen envelope | Gates, both sizes |
|---|---|---|---|---|---|
| 6654 | (333,413) | (334,412) | (−1,+1) | ±3 px in each axis | Pass, no flags |
| 6751 | (333,413) | (334,412) | (−1,+1) | ±3 px in each axis | Pass, no flags |
| 6931 | (333,413) | (334,412) | (−1,+1) | ±3 px in each axis | Pass, no flags |
| 7013 | (333,413) | (334,412) | (−1,+1) | ±3 px in each axis | Pass, no flags |
| 7104 | (333,413) | (334,411) | (−1,+2) | ±4 px in each axis | Pass, no flags |

The automatic method selects an integer template center; the independent annotation estimated the visual center of a blurred bright patch. Those are not exact mathematical material-point definitions. The stated differences remain visible rather than being zeroed or corrected after output. The unchanged automatic center does not establish zero/subpixel camera motion, and the manual center variation does not establish physical motion. A matching gate pass is not a probability of correct identity.

The helper verified the ten exact frame/reference/size keys and rational PTS, six native PNG byte identities and grayscale headers (baseline plus evaluation frames), declared annotation/candidate/preflight hashes, consumed product hashes against both completed receipts, copied code/configuration/protocol lineage, and the final run-pin union. This is a bounded artifact check, not a reproduction of every historical score grid, fit or source acquisition. Full numerical and regression verification remain the separate reviewer's scope.

### Actual post-output visual coverage

Displayed and inspected **all twelve distinct run01 overlays** at original stored resolution: frames 6593, 6654, 6751, 6931, 7013 and 7104, each at halfwidths 9 and 13. The [JSON inventory](comparison.json) lists every exact overlay filename and receipt-checked SHA-256. No run02 overlay was visually inspected, and no additional historical native frame was visually reopened during this post-output pass. The earlier five native images and five labeled crops used for annotation remain separately documented in [evaluation-annotations.md](evaluation-annotations.md).

R7's marker remains associated with the intended bright roof-edge patch in every reviewed overlay, not the former R3 dark-area anchor. No R7-specific gross feature swap, disappearance or new marker-placement error was identified in this sample. This is appearance-level computational review only. Colored squares and adjacent text cover some underlying pixels, so the overlays cannot themselves validate exact center position; the pre-output native/crop review supplies the separate coarse localization.

The 19×19 overlays at f6654 and f6751 retain red R6 markers while R7 is green. The saved R6 records report `ambiguous_competitor`; R6 passes at 27×27 in these frames. This independent limitation survives the R3 replacement and must not be obscured by R7's success. These four R6 automatic records are included only as overlay context, not new manual annotations or additions to the ten-record R7 denominator. The other five reference observations were neither changed nor revalidated here.

All labels in this twelve-overlay sample remain readable; no consequential new label clipping was identified. The footer explicitly identifies an analytical derivative and disclaims physical tracks. Different depth planes, repeated patterns, overlap geometry, blur/compression and brightness/highlight changes remain limits on material-point identity and stationarity. These five evaluation frames do not establish continuous correspondence across intervening frames or a calibrated camera map transferable to WTC7.

### Reproduction, runtime and preserved failure

The standalone [comparison helper](compare_r7.py) uses Python's standard library and does not import the matcher or fit transforms. It preserves the report's original criteria prefix, SHA-256 `40a98f6bb2ca25c1cc2ea0e5a724bdfacf2da6720b060914553c379c816463fb`, while allowing this results section to be additive. All frozen annotation and selection hashes were unchanged before and after the successful comparison.

An initial helper execution **failed before producing any comparison JSON** because I incorrectly required the procedure-only `initial.json` pin dictionary to equal the final receipt dictionary. Inspection of the wrapper showed that it deliberately adds `input-pins.json` and the two preflight dependencies after initialization; shared initial pin values were unchanged. The corrected helper verifies the exact normalized union of those three sources against the final receipt, with conflict checks, rather than accepting an arbitrary subset. This was a comparator schema-assumption error, not a demonstrated historical-data change or a relaxation of the frame/identity/envelope criteria. The [failed helper snapshot](compare_r7-failed01.py), SHA-256 `64786d97fae2ba829df992e3e3160da8030a491bca81ff95a4e34dc5de73955a`, and [execution history](comparison-execution-history.json) preserve the failure.

The successful helper and its retained [repeat output](comparison-repeat01.json) both record **Python 3.13.7**, invoked explicitly as `/Users/admin/.pyenv/versions/3.13.7/bin/python3`. Their JSON bytes are identical, checked with `cmp`; both hashes are `02525db6ef42ba96f4e4e4cbe810b5b85a60c113b21f5dfe11a68abbf025b67e`. The successful helper source is SHA-256 `1ac67a947388f7088c2c34ee1c633d384e2c28f31116a8d8f1d13d9ea2c9c350`. These runtime statements come from the actual output artifacts, not an assumed shell default or the historical matcher environment.

Focused helper self-tests passed for inclusive/outside envelope boundaries, rejected finite winners, malformed/missing coordinates, ambiguous/unavailable identities, duplicate-key rejection and exact rational PTS. Repeated execution reproduces this arithmetic and artifact checking; it does **not** repeat the visual inspection. Accordingly the JSON contains an overlay artifact inventory, not a machine-generated assertion that the helper has viewed images. The development-verification skill guided these focused checks; no browser was needed for this local file comparison.

The bounded review is complete with no annotation adjustment required. The outcome supports only that the replacement R7 candidate and the independent coarse appearance annotations agree in this fixed sample under the unchanged gates. It does not erase v1's reference-selection failure, cure R6's separate size sensitivity, establish physical stationarity, certify the full camera-model result, or change any acceleration/causal conclusion.
