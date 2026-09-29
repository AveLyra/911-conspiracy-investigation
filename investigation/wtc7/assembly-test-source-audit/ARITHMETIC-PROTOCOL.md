# Assembly comparison arithmetic protocol

Frozen before new calculation, after inspecting TN1749 Table3-3/3-4 fields.
This is a retrospective source audit, not preregistration of the historical
experiments. No discrepancy threshold is selected from computed outcomes.

## TN1749 table arithmetic

Include all six connection-size rows and both models (12 comparisons) on
physical PDF46 / printed28. Preserve load values (one decimal kN), rotation
values (three decimals rad), signed deviations and COV (one decimal percent).
Retain source test executions, figure histories and table membership as separate
fields: the tables do not themselves state n or the SD convention.

For each pair calculate exactly100*(model-experiment_mean)/experiment_mean.
Record signed error versus printed deviation. Test an explicit display-rounding
possibility: each displayed model and mean has half a last-place unit of
possible variation; each deviation has0.05percentage-point halfwidth. Positive
mean bounds give percentage extrema100*(model_low/mean_high-1) and
100*(model_high/mean_low-1). Retain disjoint and endpoint-only intersections.
These are printing hypotheses, not measurement error or authenticated inputs.
Do not turn table COV into a confidence interval or its unknown n into3 by fiat.

## Original-study crosswalk, if individual measurements are supplied

Freeze independently sourced original values/testIDs/page/units/precision and
their exact peak/initial-failure conventions before calculating. Include every
matching three-, four- and five-bolt record; preserve missing fields. Never
infer raw data by digitizing figures or rearranging a reported summary.

Compute group arithmetic means, both sample(n-1) and population(n) standard
deviations and COVs from the printed individual measurements, where supplied.
Use exact rational mean/variance and high-precision square roots, with declared
rounding for presentation. Show both whole reported groups and separately the
figure-displayed subset when the original supplies an omitted test; label these
candidate membership tests, not discovered NIST selection. If a test lacks a
quantity, do not impute it or use different counts without disclosure.

Compare original summary values against recomputation and TN1749. Keep original
rotation values, displacement, lengths and geometric convention distinct. Where
both sources give the required lengths and a formula, calculate the explicitly
stated original-to-retrospective conversion as a separate diagnostic; retain
unconverted results. No nominal-length ratio is automatically an exact angular
conversion. Every proposed convention or exclusion must be named before its
calculation; additional fields require an additive protocol.

Agreement of rounded summaries cannot identify unrounded histories or certify
the selected model. Preserve failures/nonmatches. Root and independent numeric
implementations freeze before cross-access; later schema comparison is labeled
post-freeze. Run root twice, rerun independent calculation as consumer and retain
source/code/protocol/runtime/output hashes. Synthetic controls must include
sign, zero-error, rounding-only overlap, genuine nonoverlap, endpoint tie,
nonpositive-denominator rejection and sample/population distinction where used.
