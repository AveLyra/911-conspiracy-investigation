# What the published multipoint numbers reproduce

2026-09-19. WP2/Q03-Q05; research, not an expert opinion or litigation finding. [Protocol](PROTOCOL.md), [source/method review](method-review.md), [independent numerical review](independent-numeric-review.md), [verification](validation.md). The [charter](../CHARTER.md) controls the wider investigation.

**The printed tables support gravity-scale downward acceleration under the authors' assigned units, but do not uniquely reproduce four exact acceleration claims without selecting fitting windows.** All 98 declared fits have been independently reproduced arithmetically. Two source-motivated timing hypotheses make every tested derivative row rounding-compatible; the historical method remains unidentified. The small discrepancies should not be presented as unexplained evidence of manipulation. Neither result independently validates the original tracking/calibration or establishes instantaneous, whole-building free fall.

## Source and actual work

We used the [preserved 2023 Chandler/Walter/Szamboti paper](../luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf), not a summary of it. Pages43–46 label four north-face accelerations; page 47 prints positions/velocities. Page15 supplies nominal 0.2-second sampling and onset labels. The paper does not specify exact regression masks or derivative settings. Pages48–50 expressly use the western camera for onset rather than acceleration and align its clock through the Camera2 northwest corner. These are source statements, not independent historical findings.

Two separately frozen transcriptions agree on **791 numerical tokens and 229 blanks**: all 70 rows of the selected11 page 47 columns and all 25 rows/all 10 page 50 columns. Root and the transcription reviewer inspected the complete relevant pages; the broader source-method review inspected pages 10–16 and 37–50. No missing value became zero. [Exact reconciliation](reconciliation.json).

Root ran centered NumPy least squares; a separate reviewer implemented exact rational normal equations without seeing those results. Both ran twice to exclusive outputs. All 98 fits, memberships, residuals, weights and decision flags agree within the declared1e-8 numerical tolerance (largest acceleration difference about4.41e-13). This is independent arithmetic, not independent video evidence or independent engineering expertise.

## The four primary reconstructions

Downward accelerations below are in **assigned m/s²**, conditional on the printed coordinate scale and nominal clock. Primary windows were declared before calculating: NE8.0–9.2s; EC/WC/NW8.2–10.6s. The source's actual fit masks remain unidentified.

| Roofline point | Paper label | Our velocity-line fit | Our position-quadratic fit | Full fixed-grid velocity range |
|---|---:|---:|---:|---:|
| Northeast corner | 9.30 | 9.307 | 9.268 | 8.907–9.590 |
| East-center | 9.79 | 9.781 | 9.930 | 8.905–9.882 |
| West-center | 9.81 | 10.320 | 10.601 | 9.724–10.603 |
| Northwest corner | 9.92 | 9.957 | 9.957 | 9.317–10.094 |

The finite grid contains9 NE windows and 12 per other point; each has both fit families. Four additional whole-post-onset contrasts retain the later curvature, giving49 windows/98 fits in total. Every result and residual is retained in [run01](run01/results.json); [run02](run02/results.json) is byte-identical. The independent review gives the complete position-fit ranges and display-rounding bounds.

The NE/EC primary velocity differences are compatible with nearest-hundredth input/output display rounding; WC/NW primary differences are not. This does **not by itself falsify the reported labels**, because the original fitting membership and settings are unspecified. Across the fixed grid, five velocity windows are rounding-compatible with the four labels:

- NE:8.0–9.2 or8.2–9.2s.
- EC:8.2–10.6s.
- WC:8.2–11.0s.
- NW:8.0–10.6s.

These are all matches within the declared grid, not cherry-picked replacements or recovered historical masks. Most tested windows do not reproduce the corresponding exact label within printing bounds. The grid nevertheless retains gravity-scale acceleration across the sampled main-descent intervals: roughly 9–11 assigned m/s² here. That is favorable evidence for the numerical content of the rapid-descent claim **conditional on the supplied measurements**, not proof of a precise universal 9.81m/s² interval.

Position quadratics need not equal lines fitted to differentiated positions: they weight the data differently, and velocity stencils can use neighboring positions outside a selected fit window. The primary WC difference is much larger than printing precision. Including the full later printed sequence lowers fitted average acceleration further; that does not invalidate an earlier gravity-scale interval or identify why later apparent acceleration changes. No physical error distribution, force history or confidence interval is assigned.

## A small anomaly tested against an ordinary explanation

The original nominal-grid test compared each interior printed velocity with `(next position − previous position)/0.4s`. Of 161 supported rows,150 were compatible with nearest-hundredth rounding and 11 were not. The latter residuals were all positive0.035–0.045m/s during negative velocity. One initial NW velocity lacks a printed preceding position and remains untestable.

We preserved that result and declared a separate [post-result clock diagnostic](CLOCK-ADDENDUM.md) before testing alternatives. A fresh hash/probe confirms that the held Camera2 access copy reports `30000/1001` nominal fps and `2997/100` average fps. Its acquisition record's public file ID exactly matches the Camera2 link on paper page 50. This is a real source-download join, **not** a native-camera or table-to-frame authentication.

If nominal 0.2-second samples represent six frames, the centered span is slightly longer than 0.4s at either listed rate. Testing precisely those two alternatives, with their adjusted exact rounding bounds, makes **all 161 individual derivative rows compatible**; the nominal 30fps case retains11 failures. Both runs agree and independent exact arithmetic checks all 483 row-candidate comparisons. These two source-motivated timing hypotheses provide row-wise compatibility, not identification of the historical method. The six-frame assumption is unverified, the source presentation intervals are not perfectly uniform, and per-row compatibility is weaker than one jointly reconstructed hidden-precision series. The 98 original fits have not been rescaled or overwritten.

Accordingly, calling those11 discrepancies evidence of fabricated velocities would be unwarranted. Conversely, the compatibility result does not authenticate calibration, eliminate smoothing alternatives or prove instantaneous onset. [Clock results](clock-results01.json).

## Western view: transformation check, not an acceleration replication

All 75 raw-minus-reference comparisons are rounding-compatible. The adjusted center/SW columns admit constant offsets of 4.32–4.33 and 8.23–8.24 in the source's assigned position units. These are pairwise display-rounding feasibility intervals, not recovered hidden constants or measurement error bars.

After subtracting each point's own8.20s value, the largest absolute pairwise displacement difference is 0.28 at 8.60s, with signed center minus SW = −0.28. Unknown tracking, projection, pan/zoom and scale effects prevent interpreting that as physical deformation or a quantified rejection of rigidity. Additive common-height adjustment removes initial height differences by construction; it cannot establish common acceleration. The Camera2-derived timing anchor also limits independent cross-camera onset corroboration. No western acceleration or new onset was calculated here.

## Evidence-weight update

| Proposition | Type / status | What would change it |
|---|---|---|
| Selected published values are faithfully transcribed and the declared98 fits reproduce | Derived; directly established within this calculation's scope | A source-cell error, wrong membership, sign/weight error or failed independent reproduction |
| Printed north-face data have gravity-scale main-descent curvature | Conditional numerical support strengthened by direct table reproduction | Independently calibrated tracks/clock or source corrections inconsistent with it |
| The exact four labels identify one reproducible historical fit procedure | Not established; finite window sensitivity is material | Original fit masks, project/export settings and a successful source-linked reproduction |
| Eleven small derivative discrepancies require suspicious processing | Not supported; two source-motivated clock hypotheses account for each row | Exact historical settings excluding those explanations, followed by a failed full reconstruction |
| West table independently verifies acceleration or an absolute synchronized clock | Not established; the source expressly limits its method | Independent calibration/time alignment and uncertainty-qualified trajectory reconstruction |
| These results distinguish fire initiation from deliberate support removal | Underdetermined | Specified competing models making different verified predictions for the same observables, plus initiating-mechanism evidence |

The strongest objection to overinterpreting this unit is that it processes the authors' **already-derived** measurements. It neither supplies independently observed positions nor establishes which members carried load. The strongest result against dismissing the paper is that its rapid motion is numerically present and not erased by this finite sensitivity analysis. Both facts must survive the synthesis.

The [integrated causal assessment](../causal-chain-synthesis/report.md) is unchanged: conditional model/mechanical evidence, but no independently established strict comparative probability ordering. There is no demolition finding, restored fire-first finding, equal-odds finding or evidence of author/agency intent from this unit.

## Next discriminating work

Map the paper's four Figure4 feature identities, coordinate scale and table-time zero to the already-held Camera2 frames and any available saved analysis settings. Preserve exact PTS and prior reference/trackability failures. Then freeze independent multi-point placements and onset/fit choices before reconstructing historical motion. Do not skip that step because the paper's tables fit a plausible curve, and do not reacquire the already-held Camera2 download unnecessarily.

The late-fire-video lineage lane remains open. Originals, failed nominal-clock comparisons, alternative fits and the Luna audit remain preserved. No main/legal record, Faraday protocol, accepted Sherlock finding or external message was changed. The comprehensive investigation remains active and incomplete.
