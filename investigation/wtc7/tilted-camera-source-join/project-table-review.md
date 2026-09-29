# Frozen all-row project / printed-table comparison

2026-09-19. Research derivative under `TABLE-ADDENDUM.md`, declared before
conversion. This tests saved numerical correspondence with the paper's printed
Camera2 table; it is not a new measurement, physical calibration, reconstruction
of editing history, source-identification certificate or causal finding.

## Result

**Five of 48 predeclared pairings agree throughout their available displacement
rows within the ±0.010 printed subtraction enclosure. No pairing agrees
throughout in absolute position within ±0.005. No shared finite row passes the
separate printed-time rounding test of ±0.005 seconds under the assigned U
clock.** The displacement results therefore concern the nominal 0.2-second row
join, not exact printed timing or equal absolute coordinates.

All eight tracks, all **334** saved rows and all **48** prescribed X-or-Y column
pairings were calculated. All results—including incompatible and unavailable
pairings—are in `table01/comparison.json` and its byte-identical fresh repeat
`table02/comparison.json`. The complete per-pair counts, baselines, residual
ranges and maxima are also in each run's `summary.json`. Source labels were
not reassigned to table columns.

| Numerically compatible displacement pairing | Shared finite rows | Original saved-minus-printed baseline offset | Largest absolute displacement residual |
|---|---:|---:|---:|
| pointmass01 Y / `nw_y` | 70 | +1.665216128 | 0.007706381 |
| pointmass02 X / `ref_x` | 70 | +20.467218527 | 0.009277063 |
| pointmass02 Y / `ref_y` | 70 | +1.664764841 | 0.008062614 |
| pointmass06 Y / `ne_y` | 16 | +1.665972074 | 0.006701733 |
| pointmass08 Y / `wc_y` | 40 | +1.667643992 | 0.004908741 |

Positions are in the saved **assigned units**. The numerical table does not
independently validate the metre label. The raw offsets remain in the output
and were not subtracted in the absolute-position test. The displacement test
subtracts each series' own value at its **same first shared finite row**, exactly
as preregistered. That baseline's zero displacement residual is automatic,
not additional evidence. Pairings with no shared finite rows have no baseline.

The compatible source labels among these results are source-assigned `NW
Corner` (PM01) and `NE Corner` (PM06). PM02 and PM08 remain ordinal IDs with
withheld/name-hashed source labels. Numerical closeness does not rename them.

## Retained mismatch and missing-data findings

The conspicuous partial correspondence is **pointmass05 Y / `ec_y`**:
32/43 shared rows pass the displacement enclosure, but the largest absolute
displacement residual is **0.230451834**. The first shared-row original offset
is +1.666542649 assigned units. Eight of eight saved key-frame rows pass, while
24/35 nonkey rows pass. The 11 failing nonkey frame indices are
252, 258, 270, 276, 282, 288, 294, 300, 306, 312 and 318. All 43 rows remain in
both runs. The key/nonkey subgroup display uses a saved provenance flag; it does
not change the predeclared all-row result or identify the nonkey rows' origin.

PM03 Y against `ne_y`, `ec_y` and `wc_y` has **zero** shared finite values and
no baseline. These are unavailable comparisons, not passing or failing position
fits. The other 40 pairings with shared finite rows do not pass every
displacement enclosure. Only one individual absolute-position comparison passes
anywhere among the 48 pairings (PM06 Y / `nw_y`); an isolated crossing is not a
series correspondence.

Across all pairings, the output retains:

- 1,512 shared finite nominal-time comparisons;
- 390 saved rows at published times whose selected paper cell is blank;
- 1,458 published rows with no saved counterpart in that track;
- 102 saved-row comparisons outside the publication's time range.

These counts repeat the same source rows across multiple pairings and are not
independent observations. Each pairing contains its union of saved-grid and
published times, including absent states. Every original saved row carries its
frame, selected step, key-frame flag, original coordinate text and XML locators.
Every printed comparison carries PDF hash, physical/printed page 47, row,
column, printed time text and coordinate text. No missing value was filled or
treated as zero.

## Clock and transform actually applied

The exact source-reviewed inverse was used once:

```text
u = x - 470.25; v = y - 349.0
A = -2.5913472025433153 degrees
sx = sy = 1.4841091539439202
X = cos(A)*u/sx - sin(A)*v/sy
Y = -sin(A)*u/sx - cos(A)*v/sy
```

No scale, angle, coordinate origin, source label or time offset was optimized.
No saved filter was inverted. Units and the original calibration remain
conditional on the saved assignment and image space.

Clock **U** uses the exact rational representation of the saved decimal:
`t_s = (-2020 + n*33.36666666666667)/1000`, at selected frames `n=6*k`.
The nominal grid rounds to the nearest multiple of 0.2 seconds with exact
half-grid ties away from zero. Only existing printed rows are joined. Both
the original time and residual are retained.

For shared finite rows, U-minus-printed time ranges from approximately
**−0.0190 to −0.0052 seconds**, outside the separately enforced ±0.005-second
printed rounding enclosure. Thus all 1,512 shared finite comparisons fail
strict time compatibility, even when position change is compatible. This is
not repaired by silently rounding the selected spacing to 0.2 seconds.

This zero-pass statement applies **only to rows joined to the printed table**.
Five later PM02 source rows—frames 450, 456, 462, 468 and 474—are within ±0.005
seconds of their nominal grid values 13.0, 13.2, 13.4, 13.6 and 13.8. Those grid
values are outside the printed table, which ends at 12.8 seconds, and remain
unjoined. It would be incorrect to report that none of all 334 converted source
rows meets the nominal-grid enclosure.

The current clip has uniform PTS spacing of 2002 ticks on a 1/60000-second time
base. Applying the inspected controller's endpoint stretch using loaded
frames **0 and 474** makes the current-PTS conditional clock equal U at all 80
selected frames, with **exact rational difference zero**. Frame 475 was not
used as the loaded endpoint. The selected end's U time is approximately
13.7958 seconds; its underlying current PTS is 948948 ticks, or 15.8158 seconds
before assigned origin/stretch. Current FFprobe PTS identity with a historical
Xuggle frame-time array is not established by this equality.

The absolute position enclosure is ±0.005 assigned units; the displacement
enclosure is ±0.010. A separate arithmetic tolerance of **1e-9** is reported
beside the print-only decision. The above complete-pair outcomes are unchanged
by adding that tolerance. No acceleration or velocity was computed.

## Verification and provenance

The paper source is the held Chandler/Walter/Szamboti 2023 PDF, SHA-256
`cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394`.
The selected page-47 transcription hash is
`a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc`.
Its existing independent reconciliation reports exact agreement for 70 rows
and 11 columns; the current source/transcription/reconciliation pins were
rechecked before use. This lane did not newly view the PDF page or treat a
repeated table as another independent physical observation.

The project export hash is
`4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8`.
All source/project/probe/addendum/semantics pins are retained in each run's
receipt and comparison. All were unchanged after calculation. The original
TRK's source/export preservation and direct-XML checks remain in the earlier
`project-export-review.md`; none of those files was changed for this calculation.

The **13 synthetic tests passed before historical computation**, and passed
again automatically before each output run. They cover degrees/radians,
vertical sign, unequal scales using a separate forward matrix, uniform and
irregular clocks, loaded versus full-video endpoints, negative-time and
half-grid rounding, both printed enclosure boundaries and separate tolerance,
sparse/null rows, no-overlap/no-baseline behavior, first-shared-finite baselines,
strict timing independent from nominal-grid position compatibility, ambiguous
grid rejection and key-frame flags surviving conversion. No browser test
applies to this non-UI calculation.

Commands actually run from the dedicated investigation worktree:

```sh
python3 research/sherlock-wtc7-investigation/tilted-camera-source-join/project-table-controls.py
python3 research/sherlock-wtc7-investigation/tilted-camera-source-join/compare_project_table.py --out table01
python3 research/sherlock-wtc7-investigation/tilted-camera-source-join/compare_project_table.py --out table02
```

Python 3.12.14. Both runs used narrow permission for new output directories in
the worktree. Every output file was exclusively created; existing outputs were
not overwritten. Byte comparison of all four output products passed:

| Product, identical in table01/table02 | Bytes | SHA-256 |
|---|---:|---|
| comparison.json | 5228329 | `ee49c2628398d5b1009df9c8ef12dc51aa1ec74a4c4a697d894bad38dda3bf19` |
| summary.json | 87607 | `a6ac614ca2d6cdfe3e5e4aef9991e9bb8fe6c7e973ab0a9b548f47123bbc06c5` |
| controls.json | 135 | `5edc437e15c4e3ab4acf65416ad289c5dc745df06bd2bd12d3d51d45c2465b77` |
| receipt.json | 2110 | `639b2f310e91966c320a2d88170c8852c957e7495018e75cc2c5a3971411c011` |

A final read-only invariant check also passed: 334 converted rows, 48 pairs,
each pair's complete saved-row count, all 70 printed rows represented per pair,
and exact agreement between row statuses and summary counts. Adding the
separate arithmetic tolerance changes no absolute or displacement pass count.
The 13 controls passed again after those checks. No producer or result file was
edited after either calculation.

Producer `compare_project_table.py`: 19,405 bytes, SHA-256
`1455defb2a41a14226cb7657ed4f6dcb517e7e3d7893fb3e791a357d3d0b25f5`.
Tests `project-table-controls.py`: 7,793 bytes, SHA-256
`28c19f12ae294ce572dbce04032c366934c3aa2735340aaf7bc54edbdac52e13`.
The controlling addendum hash before computation was
`f5597785cac2a11a7680bd9f051df8455a5f190387544ac6ef675ee907a108e1`.

The separate computational [independent arithmetic
review](table-independent-review.md) is now complete. That reviewer froze two
byte-identical outputs before reading this lane's results, using a generic
determinant inverse and exact rational printed/clock arithmetic. Its later
cross-output check found **zero disagreements** across all 668 X/Y values,
1,512 absolute residuals, 1,512 displacement residuals, 3,462 normalized
row/pair states, 48 summaries, source memberships/locators, key-frame flags,
baseline choices and exact clock/grid fields. All match decisions agree.
Maximum numerical differences were 5.684341886080802e-14 for coordinates,
6.128431095930864e-14 for absolute residuals and 8.185119249048967e-14 for
displacement residuals, below the declared 1e-9 bound.

Both independent outputs (`table-independent01.json` and
`table-independent02.json`) are 3,748,451 bytes with SHA-256
`61f2b977e3ceae5c8987744357b6d9a41039d6de5a315272145cb708414f839d`.
The completed independent review is 12,058 bytes, SHA-256
`0892372a2f1a701e8103c61cdc263eba3c16a91e7ae48c5ea53d2d61c5d71d12`.
The final checker with its appended cross-output verifier has SHA-256
`47accb7302a060bcc839c5baaf97ae2fcf2f8c32e3b5a7063f0484be670b4f1d`;
it byte-recovers and verifies the independent producer originally frozen at
SHA-256 `b28a84ca109c41e40dac7bda89338169b8fb0c4e868a759a5d95e6347e54ec3f`.
This lane read that final review and independently reran the read-only command
below, which passed and rechecked all eight source pins. No external human or
specialist review is claimed.

```sh
python3 research/sherlock-wtc7-investigation/tilted-camera-source-join/table-independent-check.py --compare-existing
```

No historical calculation or synthetic-control run failed in this lane.
A preparatory inventory query referred to an absent `media01/receipt.json`;
the actual preserved source/probe paths were then identified and pinned before
calculation. It produced no comparison or altered data. Earlier export failures
are retained in the separate export review.

## Interpretation and disconfirming evidence

The complete displacement correspondences support a narrow **numerical
relationship** between several saved trajectories and printed series under
the declared coarse time join. A different coordinate origin or a related
saved version is consistent with the common approximately +1.67 Y offsets,
but no origin-change mechanism was fit or established. Shared underlying
processing can produce matching position changes without independently accurate
measurement.

The strongest contrary evidence to an exact saved-project/publication join is
the **absolute-position mismatch, strict timing mismatch and the retained PM05
all-row failure**. The 35 nonkey PM05 rows cannot be declared independent manual
measurements or confirmed interpolations from this arithmetic. Passing its
eight surviving keys does not erase its other saved values.

These are reproducible conditional calculations, not historical method
certification. Establishing the paper's exact inputs would require a pinned
historical project/export/media/engine lineage and an explanation of the
saved-versus-printed offsets, clock choice and PM05 discrepancies. Physical
accuracy separately requires source-raster point/calibration evidence and
uncertainty. No causal ranking, legal fact, accepted Sherlock result or
publication status was changed.

## Review revision record

The pre-independent-check version of this review, after its local invariant
check, had SHA-256
`0adbee529dc090ddb37dc8d732631a1a8c6addc6fa9114ccefc988e13f4fa7f9`.
It stated: "That independent result is pending in this version of the note;
deterministic repeats and the synthetic tests alone do not establish it."
That was the verification state then. The current review replaces that pending
assessment with the saved independent result, source pins and successful replay
above, and explicitly distinguishes the five late PM02 rows from actual
publication joins. These are review/clarification changes; **neither producer,
either run's comparison/summary/control/receipt files, the addendum nor any
source was modified**.

An initial text-update attempt for this final review failed because an
irrelevant trailing context line did not match. No edit was applied. The
narrowed update succeeded; it changed no calculation or acceptance criterion.
