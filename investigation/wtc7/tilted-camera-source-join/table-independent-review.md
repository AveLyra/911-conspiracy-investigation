# Independent saved-project / printed-table arithmetic review

Method frozen 2026-09-19 after reading [TABLE-ADDENDUM.md](TABLE-ADDENDUM.md) entirely and inspecting input schemas/hashes only, before historical point conversion or inspection of another comparison implementation/results. Research-only continuation of the source-method lane. The earlier source-semantics review is preserved unchanged.

## Independent method commitment

[table-independent-check.py](table-independent-check.py) uses the generic determinant inverse of the literal world-to-image matrix, not the explicit inverse expression used by the source review. Python `Fraction` preserves the exact saved-decimal clock, current PTS, 0.2-second grid, tie-away-from-zero rounding, printed decimals and enclosure boundaries. Trigonometric coordinates use finite binary floats; residuals retain exact rational representations of those floats, with a separately reported 1e-9 arithmetic tolerance.

Every one of the 334 finite saved rows will retain its original frame, selected step, keyframe flag, source field locators, absolute X/Y, actual assigned time, nominal-grid time, time residual and current-PTS stretched-clock comparison. Every one of 48 predetermined series pairs will retain all 70 publication row slots with explicit compared, missing-source, missing-published-value or missing-both status, plus every source row outside the publication grid. A displacement baseline is the pair's first shared finite row; no overlap means no baseline. All nonkey PM05 rows remain present with unresolved-history flags. Source-assigned labels remain source metadata; no label is selected by numerical closeness.

Synthetic controls execute before any historical input loading. They cover degrees, unequal scales, y sign, uniform/irregular clocks, loaded endpoint selection, negative and exact-half grid rounding, both print enclosures and the separate arithmetic tolerance, sparse/missing/no-overlap cases, fixed-baseline offsets and preserved keyframe flags. The program pins its input hashes before/after, creates outputs exclusively, and supports a separate repeat artifact.

At method freeze, no other comparison code or output had been inspected. Numerical findings and cross-implementation validation will be appended after this method is saved and the controls pass. A numerical relationship will remain conditional source correspondence, not physical or historical input validation.

## Completed result

Independent arithmetic reproduced all 334 saved coordinate pairs and all 48 prescribed series comparisons. The two separately created independent outputs are byte-identical. The later fieldwise check against `table01/comparison.json` and `table02/comparison.json` found **zero disagreements** in source membership, missing-data states, exact clock/grid fields, printed/source locators, keyframe flags, baseline choices, rounding decisions or pair summaries. Numerical differences from the distinct arithmetic routes are below the predeclared 1e-9 tolerance.

No pair has every shared absolute position compatible with the printed +/-0.005 enclosure. There is one individually compatible absolute cell across the 1,512 shared finite comparisons; it does not make a complete series match. The following five predeclared pairs have all shared **position changes** compatible with the +/-0.010 subtraction enclosure:

| Source ordinal / compared component | Printed column | Shared finite rows | Original saved-minus-printed offset at baseline | Maximum displacement residual |
|---|---|---:|---:|---:|
| PM01 Y | `nw_y` | 70 | +1.665216128 | 0.007706381 |
| PM02 X | `ref_x` | 70 | +20.467218527 | 0.009277063 |
| PM02 Y | `ref_y` | 70 | +1.664764841 | 0.008062614 |
| PM06 Y | `ne_y` | 16 | +1.665972074 | 0.006701733 |
| PM08 Y | `wc_y` | 40 | +1.667643992 | 0.004908741 |

Values are in the project's assigned world units. These are numeric pair outcomes, not newly assigned feature identities. Subtracting a common first-row baseline intentionally removes a constant offset; the retained original offsets show why a displacement pass does not establish identical absolute coordinates. The complete output retains all other pairings and rows, not only this passing subset.

PM05 Y versus `ec_y` is a material non-pass: 32 of 43 displacement rows are compatible and the largest residual is 0.230451834 assigned units. All 35 nonkey PM05 source rows remain present and flagged; their keyframe-history uncertainty is not resolved by this calculation. PM03 versus `ne_y`, `ec_y` and `wc_y` has no shared finite row and therefore no displacement baseline. Those cases remain unavailable comparisons rather than failed measured agreements.

## Time agreement is qualified by the join

The declared uniform-clock times agree **exactly as rational numbers** with current MP4 PTS after the source-reviewed stretch using loaded endpoints 0 and 474. This is equality under the current PTS scenario, not authentication of the original Xuggle engine array or exposure timing.

There are **zero strict printed-time passes among all 1,512 shared finite comparison rows**, and zero joint position-and-strict-time passes. Assigned times on the publication's joined grid differ from their printed times by approximately -0.0190 to -0.0052 seconds, outside the declared +/-0.005-second compatibility boundary. Their joins therefore remain nearest-0.2-second-grid correspondences.

Five converted PM02 rows, frames 450, 456, 462, 468 and 474, do lie within +/-0.005 seconds of their nearest grid values, 13.0 through 13.8 seconds. Those grid values are **outside** the printed table's -1.0 through 12.8-second range. Calling all 334 converted rows strict-time failures would be false; the zero-pass finding applies to actual publication joins.

## Complete coverage and reproducibility receipt

The complete comparison consists of 3,360 publication row slots (48 pairs x 70 rows) plus 102 source-row/pair entries outside the publication grid. Normalized states agree across the implementations:

| Row state | Count across the 48 comparisons |
|---|---:|
| Shared finite comparison | 1512 |
| Missing source, finite printed value | 960 |
| Source present, printed value missing | 390 |
| Both source and printed value missing | 498 |
| Source row outside publication grid | 102 |

These counts repeat shared source records across candidate pairs; they are not independent observations. The peer output uses different status names for some missing cases. The verifier compares underlying source/printed presence and locators before normalizing those names; no data-presence disagreement was hidden by a label substitution.

| Verified quantity | Coverage | Largest numerical difference |
|---|---:|---:|
| X and Y values | 668 values from all 334 source rows | 5.684341886080802e-14 |
| Absolute residuals | 1512 | 6.128431095930864e-14 |
| Displacement residuals | 1512 | 8.185119249048967e-14 |
| Original baseline offsets | 45 nonempty pairings | 4.085620730620576e-14 |
| Pair residual summaries | All 48 pairs, including unavailable cases | 5.911937606128959e-14 |

All strict-enclosure and tolerance-inclusive decisions agree exactly. All 3,462 row/pair memberships and missing states agree. Missing selected frames and missing full-video frames agree for all eight tracks; source coordinate literals, XML locators, assigned names, frame/step and key flags agree. Exact assigned time, grid, time residual and current-PTS stretched time agree on all 334 rows, covering all 80 selected frame times. The eight source pins in the peer receipt were independently rehashed and matched, including the primary PDF and reconciliation record. No PDF page or new image was viewed for this arithmetic follow-up.

| Preserved artifact | Bytes | SHA-256 |
|---|---:|---|
| [table-independent01.json](table-independent01.json) | 3748451 | `61f2b977e3ceae5c8987744357b6d9a41039d6de5a315272145cb708414f839d` |
| [table-independent02.json](table-independent02.json) | 3748451 | `61f2b977e3ceae5c8987744357b6d9a41039d6de5a315272145cb708414f839d` |
| Peer `table01/comparison.json` | 5228329 | `ee49c2628398d5b1009df9c8ef12dc51aa1ec74a4c4a697d894bad38dda3bf19` |
| Peer `table02/comparison.json` | 5228329 | `ee49c2628398d5b1009df9c8ef12dc51aa1ec74a4c4a697d894bad38dda3bf19` |

The printed input is physical/printed page 47 of the preserved paper, SHA-256 `cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394`; the reconciled table input hash is `a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc`. The project export hash is `4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8`. These source identities and the exact original cell/field locators remain in the outputs.

## Independence, actual commands and retained failures

1. Read the full frozen addendum and inspected schemas/hashes, without point conversion. Saved this method note and the independent producer before calculation. Initial producer: 19,591 bytes, SHA-256 `b28a84ca109c41e40dac7bda89338169b8fb0c4e868a759a5d95e6347e54ec3f`.
2. Ran `python3 table-independent-check.py --controls-only`: all 12 named synthetic control groups passed using Python 3.13.7. The historical command repeats those controls before loading its inputs.
3. Ran `python3 table-independent-check.py --out table-independent01.json`. The first attempt completed calculation in memory but failed at exclusive output creation with `PermissionError` because the worktree lies outside the default writable roots. No partial result file was accepted. The same command under scoped elevated execution succeeded; this was a filesystem authorization retry, not an automatic-approval rejection or a changed scientific method.
4. Ran `python3 table-independent-check.py --out table-independent02.json` under the same scoped write authorization. It succeeded and produced byte-identical output. Both historical outputs were preserved before inspecting peer results.
5. Read the peer output schemas and records only after those results were frozen. No peer producer implementation was read or executed. Appended the `--compare-existing` verifier to the independent script; the original producer body and original dispatch remain exactly recoverable. The verifier byte-reconstructs that initial script and checks it against the initial hash before comparison, so the later audit code is distinguishable from the frozen independent method.
6. Ran `python3 table-independent-check.py --compare-existing`: pass, zero disagreements across 62,910 field/decision checks, including the quantities listed above. The final script including the appended verifier is 30,849 bytes, SHA-256 `47accb7302a060bcc839c5baaf97ae2fcf2f8c32e3b5a7063f0484be670b4f1d`. The command rechecks both repeat identities, all peer source pins, both formulas' outputs and the full 48-pair row/summary comparison. It writes no result or source file.

The command paths above are relative to this investigation unit; the complete script path is `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/tilted-camera-source-join/table-independent-check.py`. An initial broad schema display was truncated; exact needed structures and the full data were subsequently processed by bounded inspection and the complete verifier. No truncated display was counted as complete visual/data review.

The strongest supported conclusion is that specific saved trajectories and printed position changes have the declared numerical correspondence despite absolute-coordinate and strict-time mismatches. A different saved project version or settings can explain disagreement; shared processing can explain agreement. Neither alternative is uniquely selected here. This work adds no velocity/acceleration fit, physical calibration, historical editing attribution, source-input certification, cause ranking, expert endorsement, legal promotion or acceptance. The earlier source review remains the record of what that lane knew before seeing numerical points.
