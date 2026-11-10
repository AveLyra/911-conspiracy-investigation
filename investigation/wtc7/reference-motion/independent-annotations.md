> **Historical research:** This is a dated computational record, not a new analysis or instruction. Local paths are redacted and omitted dependencies marked; see the [publication note](README.md).

# Independent stationary-reference candidate annotations

2026-09-11. Working research under the investigation charter; computational AI visual annotation, not human or professional forensic review. Baseline candidates were sent to the root investigator before scoring, and before this annotation pass inspected its fixed evaluation frames. Prior case knowledge and prior Camera 2/4 screening are acknowledged; this is not a pristine holdout. No current tracking output was viewed.

## Baseline declaration

The [machine-readable annotation record](independent-annotations.json) contains the fixed candidate IDs, integer native-pixel centers, descriptions and subjective localization envelopes. Coordinates have origin at the upper-left native pixel, x rightward and y downward. Both 19×19 and 27×27 centered patches fit every declared baseline location. The centers will not be moved to improve subsequent algorithm scores.

Camera 2 uses native `refine01/camera2/f006593.png` (640×480); Camera 4 uses `refine01/camera4/f000899.png` (480×360), under the existing multiview-onset review. Six features per view were chosen as apparent neighboring-building or street-fixture references. Building names, depth and actual material-point identities are unverified. Camera 2's high left area is smoky, so its references favor the right skyline and lower foreground. Camera 4 offers few strong isolated features away from the distant building; its candidates include explicitly uncertain roles rather than treating all six as proven static points.

In particular, the Camera 4 hanging banner might move independently; an overlap corner may join structures at different depths; signal illumination can vary; repeated windows, steps and signal lenses may be confused. These are declared reference-quality risks. Membership in this candidate list does not prove suitability for stabilization or a single common camera transform.

Native originals were viewed first. Separately labeled `independent-grids/camera2-baseline-grid.png` and `camera4-baseline-grid.png` assist coordinate reading: each original was copied to RGB solely for colored lines at 20-pixel spacing and coordinate labels. No resampling, source-pixel modification or historical decoding was performed; originals remain untouched. Grid content is an annotation derivative and is not historical image evidence.

The existing motion-pilot protocol and limits were read for methodological lessons: two patch sizes are sensitivity checks, correlation does not establish material identity, translation does not solve zoom/parallax, rejected tracking is a procedure limit, and subjective AI coordinate envelopes are not physical or statistical accuracy bounds. Its numerical tracks and results are not reused here.

## Completed evaluation coverage

All ten fixed evaluation images were opened at native stored resolution, followed by their separate 20-pixel grid derivatives. Camera 2: f6654, f6751, f6931, f7013, f7104. Camera 4: f960, f1042, f1162, f1259, f1350. Together with the baselines, this pass viewed **12 native images and 12 separate grids**. Native image hashes and exact source PTS are recorded in the JSON. The grids use the same no-resampling overlay procedure described above and live only in `independent-grids/`.

There are 60 feature/frame rows: **48 localized, six ambiguous, six unavailable**. All six Camera 2 candidates remain recognizable across its five fixed evaluation frames. The assigned nominal centers do not resolve a shift larger than their coarse subjective localization envelopes. Identical rounded coordinates do not establish zero motion, validate one-pixel residuals, or imply subpixel accuracy. The smallest caps and soft/repeated architectural features receive wider envelopes. These points span different, uncalibrated depths and do not establish a common geometric plane.

Camera 4 supplies 18 coarse localizations in its first three evaluation frames. At f1259 and f1350, the original sign arrow, small upper-left window and upper-right signal lens are outside the retained view. The banner and two selected foreground overlap/roof anchors cannot be securely transferred under the strong reframing and scale change: their six late rows are marked ambiguous, with no guessed coordinate. Related foreground structures remain visible; failure to assign their original anchors is a limitation of this particular reference selection and annotation pass, not a claim that all possible references are unavailable.

Coordinates represent fixed patch-center anchors located by the descriptions, not an assertion that every baseline center is an exact mathematical corner or surveyed material point. A later use must preserve that convention. The subjective rectangular envelopes cover localization uncertainty in this visual pass; they are not statistical confidence intervals, physical displacement errors, or evidence that the candidate is stationary. Role uncertainty—especially banner motion and different-depth overlap intersections—remains separate from coordinate uncertainty.

No algorithm output was viewed before these annotations were completed. The root investigator confirmed that automatic historical scoring had not yet run. Baseline centers remain unchanged. Automatic comparison is pending; if future matching finds a high-score location for an unavailable/ambiguous row, the score alone cannot establish that the original reference was recovered. The preserved full candidate set permits declared exclusion/sensitivity tests, but post-result replacement must be a new exploratory configuration.

No acceleration, physical calibration, common support-failure timing, synchronization or causal inference follows. Only these annotation records and their separately labeled grids were created in this pass; no source media, frozen derivative, algorithm, case record or bridge state was changed. No supplementary-production content was accessed.
