# Saved-position / printed-table comparison declaration

2026-09-19, after complete project schema/index export and source-semantics
review, before any saved-coordinate conversion or project-to-table numerical
comparison. Root has seen schema, safe labels, source indices/settings and scene
scores, not transformed project values. The numerical comparison is retrospective
source correspondence, not independent measurement validation.

## Inputs and fixed transform

Use all eight tracks and all 334 finite x/y rows from `project01.json`, SHA-256
`4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8`.
Use the independently reconciled printed Camera2 table at
`../multipoint-table-reproduction/transcription-root/table47.json`; require its
unchanged hash from that unit's reconciliation/source pins before use. Keep the
exact PDF source identity and printed physical page47/row/column locators.

Use only the literal Tilted image origin, degree angle, x/y scales and assigned
time fields. Follow `source-semantics-review.md`'s explicit inverse formula.
No coordinate offset, scale, angle, time origin or track label is optimized.
Convert every finite saved row, retaining original frame, selected step,
keyFrame membership and the original numeric field locators. Do not interpolate,
fill missing coordinates or discard the 35 nonkey PM05 rows. Keep their provenance
flag beside every derived/comparison row.

Clock hypothesis U is the **uniform historical engine clock** with the literal
assigned duration: `t_ms=-2020+n*33.36666666666667`, `t_s=t_ms/1000`, selected
frame `n=6*k`. This is a declared conditional calculation, not authentication
of the historical engine. Also compare the nominal clock with the current
probed PTS under source-reviewed endpoint stretch (expected endpoints0 and474),
without treating current PTS as the original engine data.

## Fixed row join and reporting precision

The publication reports a nominal 0.2-second grid. For each saved row, map its
calculated U time to the **nearest 0.2-second grid value** (ties away from zero),
then join only an existing published row at that grid value. Preserve the actual
time residual; do not describe this coarser nominal-grid join as exact timing.
Independently flag whether the calculated time is compatible with the printed
time rounded to 0.01 s (absolute residual <=0.005 s). No alternate offset/lag
search is part of this test. Missing/outside-grid rows stay explicitly unjoined.

For each of eight tracks, compare derived X with `ref_x`, and derived Y with
each of `ref_y,ne_y,ec_y,wc_y,nw_y`: **48 series comparisons**, including all
available and unavailable pairings. Source labels NW/NE remain source-assigned;
other candidate matches must not be chosen silently by their numeric closeness.

Two predeclared position diagnostics, reported separately:

1. Absolute saved-world versus printed position, with printed rounding enclosure
   +/-0.005 assigned units and only a separate <=1e-9 arithmetic tolerance.
2. Position change from that pair's first shared finite row, using the same
   baseline for both series. Its printed subtraction enclosure is +/-0.010
   assigned units, arithmetic tolerance <=1e-9. Report the baseline, actual
   original offset and all residuals; this diagnostic is explicitly offset-
   insensitive and cannot prove equal coordinates or a historical source join.

Summarize counts, complete-row compatibility, maximum absolute residual and
signed residual ranges for every pair. Keep every row and missing comparison,
not only the best pair. Do not infer match significance or a causal probability
from the number of passing rows. Dependent/shared inputs remain one source
family, not independent corroboration.

## Verification and scope limits

Before historical computation, synthetic tests must cover degrees versus
radians, sign and unequal scales, uniform versus irregular clock, source endpoints,
negative-time grid rounding, exact half-grid ties, print enclosure boundaries,
missing/sparse rows, no baseline when there is no overlap, and keyFrame flags
surviving conversion. Independently reproduce material output with a distinct
formula/code route or explicitly state the unverified part. Freeze source hashes
and repeat outputs without overwriting originals.

No velocity/acceleration fitting, physical scale validation, exposure-clock
authentication, new annotation, historical editing-history finding, paper-input
certification, causal ranking or legal promotion follows automatically. A
mismatch can reflect another project/version or different saved settings; a
match can reflect shared processing rather than independent accuracy. This
comparison tests those concrete numerical relationships, not intent.
