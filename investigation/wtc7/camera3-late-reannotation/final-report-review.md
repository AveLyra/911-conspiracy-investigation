# Final report numerical and interpretation review

2026-09-12. Independent computational review of the complete report at
SHA-256 **af93973ab00ed333efafbbc4ecb3389522252b317f72880f7423b213a0c6bf61**.
No material numerical or interpretation error requiring correction was found
within the reviewed scope. This is a report-to-evidence check, not another
image annotation, physical validation, or independent replication of the
joint-feasibility calculation.

## Read and checked

I read the complete report, JOINT-ENVELOPE-ADDENDUM.md and joint-review.md,
and the complete root joint-verification receipt. I parsed joint01/result.json,
examined all six scenario definitions, coverage/omissions/constants and the
19-row combined selected witness, and checked its displayed counts against
the root verification receipt. I checked report values against the frozen
fit/comparison outputs and my earlier independent fit receipt, compared the
root fit rerun to that receipt, and reviewed reference-result summaries and
the relevant preparation-review coverage/limitations. No fit, correlation
search, video decode or joint witness generator was rerun in this review.

The evidence-falsification-auditor and source-of-truth-guardian safeguards
keep these statements attached to the particular input/report versions.
The existing independent fit implementation and reviews remain unchanged.

Principal checked pins:

| Artifact | SHA-256 |
|---|---|
| report.md | af93973ab00ed333efafbbc4ecb3389522252b317f72880f7423b213a0c6bf61 |
| joint01/result.json | 7e9b4466a1ccbefad226086efd9d66cfaa34d94378100581efb6dd05ad128668 |
| joint-root-verification01.json | 36b608c28b4bc2389d799983c52c1d5b48f0311984ff9cd28602a5d27d6309c4 |
| independent-fit-root01.json | b2c26b2a1371dba526cf1d72f5c94a48eeae70e40df6daa13a975fe7496f26c0 |
| independent-fit-verification01.json | b833d877d87eabc302122e7fd8f0b8018fc9d6517fc8bdddcabe459648d72ae6 |

The root fit rerun and my independent receipt are equal after excluding the
command field, which necessarily records the different output argument.
This confirms the stated rerun relationship, not a new independent source.

## Fit, annotation and scalar-conversion summaries

All reported fit counts agree: 207 dispositions, 187 computed and 20
uncomputed; 935 coefficients, 4,070 residuals, 2,035 weights and 236 placement
interval endpoints. Root A−B has 20 computed/3 uncomputed windows; the
separate observer has 16 computed/7 uncomputed. Every computed fresh A−B
interval contains zero. Neither fresh B track supports a complete 21-point
late fit.

The A denominators are 22/22 localized per observer, with 22 overlapping
new y-envelope pairs and each saved A y contained in both corresponding
observer envelopes. B has 21 localized root samples and 19 separate
samples, of which 19 are mutually localized. Their 19 y-envelope pairs
overlap. Root contains 16/21 comparable saved B y values; the separate
observer contains 19/19. Root exclusions are exactly 300,309,312,315,318.
These denominators include 258 and must not be confused with late-only
coverage.

The 303–339 displayed native-coordinate table matches the retained fits
at the stated three-decimal rounding. Its warning that rounded limits are
not outward-rounded strict bounds is appropriate.

Direct division by the stated scalar 3.3366687576783383 px/assigned-m gives:

| 303–339 A series | Assigned m/s², unrotated | Assigned placement envelope |
|---|---:|---|
| Root | 9.5957927931 | [7.4999878149,11.6915977713] |
| Separate observer | 9.9251335754 | [7.8293285972,12.0209385536] |
| Saved y only | 9.8620204460 | Unknown |

These agree with the report's 9.596/9.925/9.862 and rounded envelopes.
Root A linear/quadratic RMSE 7.9780976596/0.7076228086 and separate A
8.2314367604/0.4450950266 also agree with the displayed values.
The report correctly separates these unrotated scalar conversions from the
earlier saved-angle result and labels them conditional, not a new calibration.

## Joint countermodel summaries

Every reported scenario matches the exact retained result:

| Scenario | Included / declared | Omitted | Feasible constant interval | Witness constant |
|---|---:|---|---|---|
| Root selected | 21 / 22 | 348 | [−31,−30] | −30.5 |
| Root late | 20 / 21 | 348 | [−32,−30] | −31 |
| Separate selected | 19 / 22 | 342,345,348 | [−32,−30] | −31 |
| Separate late | 18 / 21 | 342,345,348 | [−33,−30] | −31.5 |
| Combined selected | 19 / 22 | 342,345,348 | [−31,−30] | −30.5 |
| Combined late | 18 / 21 | 342,345,348 | [−33,−30] | −31.5 |

All 19 combined-selected witness rows, including 258, retain c=−61/2.
The root checker reports exact satisfaction of the applicable original
boxes, not merely satisfaction of independently summarized intervals.
There are 115 witness rows across the six alternative scenarios.
Original-box membership counts are 42+40+38+36+76+72=304: two y-feature
boxes per observer per witness. These are reused observations, not 115
independent samples or 304 independent constraints on historical physics.
The root receipt records five synthetic groups comprising seven solutions.

The wider combined-late interval is correctly explained by omission of
342/345, where root alone supplied B labels. Comparing [−33,−30] with
root's [−32,−30] is not an intersection-of-identical-coverage comparison.
The report does not smuggle root's two extra labels into the combined
19/18-sample claims, and it explicitly supplies no measured constraint or
witness at omitted frames.

## Reference and reproduction summaries

The retained reference summaries and root receipt support the reported
132 passing numeric rows, 22,308 real scores, 2,366 synthetic scores,
14 synthetic fixtures and 44 translation groups. The retained translation
array has 43 groups with exactly zero mean and residual vectors and one
side21 group at336 with mean (+1/3,0), R1 residual (+2/3,0) and R2/R3
residuals (−1/3,0). The side31 alternative at336 is zero. The root receipt's
maximum correlation discrepancy 4.4408920985e−16 supports the rounded
upper description 4.45e−16.

The preparation review supports the stated 51 file pins and 28 enlarged
crop interiors, and documents the half-display-pixel factor8 tick placement.
This reviewer did not independently re-render or inspect those images.
The report preserves the small R3-patch visual-preflight rejection by the
separate observer; numerical matching does not overrule it.

## Interpretation clearance and remaining ceiling

The report addresses the earlier logical gap: separate window intervals
containing zero alone do not establish one simultaneous sequence. The
newly declared joint test supplies an explicit constant **image-y**
separation countermodel within the subjective boxes on included samples.
It properly does not call that construction new observations, a probability,
calibrated uncertainty, a full 21-late-sample history or proof of physical
rigidity/equal acceleration.

B's fixed-column silhouette definition remains prominent. The report
correctly distinguishes algebraic cancellation of a purely common vertical
shift from horizontal resampling of a sloping rim, rotation, depth and
changing silhouette identity. The positive corner curvature is not
dismissed, but no inference to a moving mass system, force, whole-building
free fall, support-failure timing, cause or intent is claimed.

The previous fit review's minor omitted-x/dx supplement for unlocalizable
B comparisons and its two incompletely retained rejection fixtures remain
valid and preserved in independent-fit-review.md. They do not change any
displayed fit or joint-feasibility result. The report's reference
qualifications prevent a numerical match from becoming a stationarity or
subpixel-error certificate.

The broad cause ranking is not identified by this unit. The final report
states that limit without converting absence of a discriminating result
into evidence for either fire or deliberate removal. No material unresolved
report correction was found; the physical/source limitations remain open
investigation constraints, not closed by this review.

Only this review was written in this follow-up. Source media, annotations,
earlier reviews/receipts, main, case records and canonical registries were
unchanged. No external transfer, accepted finding or publication occurred.
