> **Historical research:** This is a dated computational record, not a new analysis or instruction. Local paths are redacted and omitted dependencies marked; see the [publication note](README.md).

# Independent reference-motion method review

Test plan recorded 2026-09-11 18:17:54 UTC, after reading [PROTOCOL.md](PROTOCOL.md) and before reading the implementation or its historical match outputs. Research-only under the charter (historical local reference `../CHARTER.md`; not included here). This computational reviewer owns neither the reference-seed annotations nor their evaluation-coordinate envelopes. No visual or physical-motion finding is made here.

The evidence-auditing skill shapes this review by separating successful arithmetic, reproducible image matching, reference-consistency screening, and historically correct correspondence. The development-verification skill shapes the finite synthetic checks and independent recalculation. Neither skill turns an automated result into human or expert certification.

## Declared numerical checks

The implementation will be exercised with deterministic synthetic images and analytic point mappings. Tests will use the public matcher/fit entry points where possible, while expected coefficients, residuals, and score values are constructed independently. Historical rechecking will not use the implementation's transform-fit helper. Matching thresholds and historical seeds will not be changed in response to these tests.

| Control | Expected result or diagnostic limit |
|---|---|
| Unique textured patch at a known integer translation inside the search | Correct center and NCC approximately 1; all screening gates pass if the competitor margin is sufficient. |
| Positive contrast and additive brightness change without clipping | Zero-mean NCC remains approximately 1 at the true center. Negative contrast is not positive correlation. |
| Identical patches at distinct centers more than 3 pixels apart | Equal best scores; margin approximately zero and rejection. |
| Equal nearby best peaks inside the competitor exclusion | Deterministic coordinate choice does not remove ambiguity. Tie behavior must be explicitly recorded and reconciled with acceptance. |
| Constant template or candidate window | Undefined NCC or texture rejection; never silently perfect. NaN/Inf or malformed inputs must not become accepted coordinates or fits. |
| True winner at a search boundary | Explicit boundary rejection, including the effective valid support near an image edge. |
| Same 19-pixel core with distinguishing context only in the 27-pixel outer area | The smaller template is ambiguous while the larger template may distinguish it. A size disagreement must remain visible. |
| Integer matcher applied to fractional shifts or smooth/periodic texture | No calibrated subpixel localization follows; a failed or quantized match is an expected limitation. |
| Six exact translated references | Translation is the mean displacement; all residuals and leave-one-out errors are zero within floating-point tolerance. |
| Exact orientation-preserving similarity | Closed-form complex-plane similarity reproduces scale/rotation/translation and predicts all references. Reflection is not part of this model. |
| Exact general affine map | Independently solved affine coefficients predict all references; translation/similarity need not fit. Signed determinant remains a descriptive diagnostic. |
| Five stationary references and one displacement vector d | Translation residual magnitudes are |d|/6 for five references and 5|d|/6 for the displaced one. Euclidean RMS is sqrt(5)|d|/6. Leave-one-out errors are |d|/5 for the five and |d| for the displaced one. No reference may disappear from the fit. |
| Coincident or collinear reference geometry | Coincident points do not identify similarity; collinear points do not identify a general affine map. Noncoincident collinear points can identify the specified orientation-preserving similarity. |
| Five collinear references plus one off the line | Full affine rank can pass while leaving out the sole off-line point fails rank. The invalid held-out result must remain explicit. |
| Nearly collinear or badly spread reference geometry | Enforce the stated normalized design condition threshold; report instability rather than silently accepting a visually small residual. |
| Common displacement of all reference matches | A perfect fit cannot distinguish true common image motion from common correspondence error. |

## Preregistration pitfalls sent to the implementer

Before historical outputs, the reviewer requested explicit integer-center convention, standard-deviation/NCC definition, deterministic tie handling, full score-grid and valid-window support, Euclidean error definitions, normalized design scaling, conditioning threshold, similarity reflection policy, and signed affine determinant diagnostics.

The initial protocol says ties remain ambiguous but excludes competitors within Chebyshev radius 3 when calculating its margin. Two equally good nearby locations could therefore have a large distant-competitor margin. The final implementation/protocol must either reject or explicitly retain that local ambiguity; a deterministic row-major choice alone is not evidence of a uniquely localized feature.

Only the six-point candidate screen authorizes a fit. A failed individual match cannot be filled from neighboring times, a favored template size, a different reference, or a lower-residual model. A successful full fit does not authorize hiding a failed leave-one-out rank/conditioning check. All fit comparisons use the same retained reference set and the same target-image sample.

## Inference boundary

NCC measures normalized patch similarity, not a probability of correct identity. The declared variance, correlation, margin, boundary, and two-pixel gates are screening choices with uncalibrated false-match and false-rejection rates. Exact synthetic controls establish behavior on their construction, not on every compressed historical image. Scene texture, compression, parallax, projective changes, occlusion and common-mode correspondence errors can remain even when all six candidates pass.

An affine model has more degrees of freedom than a translation or similarity model. Its lower training residual is expected from model flexibility and does not identify camera mechanics. Leave-one-reference-out errors test the retained references' mutual predictability; they do not establish accuracy at a target on another image plane or outside their spatial support. Baseline matching uses construction data and is not an independent validation sample. Temporal repetition from the same source does not create independent event-level evidence.

## Execution record

Pending implementation and finite test execution. Results and any implementation revisions will be appended without rewriting this declared test plan. No historical scores or transform results have been inspected at this declaration stage.

### Synthetic execution completed; historical work paused

The finite synthetic run [independent-tests01.json](independent-tests01.json) passed **22 checks, with zero failures** using [independent_tests.py](independent_tests.py). The subject was `measure.py`, SHA-256 `adb48c18a928ab44bba0f30cc8b6cdffbdd3a60918464600a568249b7822640e`; it remained unchanged during the run. The tested protocol SHA-256 was `ba1750a2f84af2301da525199314f9e136e21769413d4f8455df856357fce09b`. Python was 3.13.7 and NumPy 2.3.4. Exact reviewer-code identity, input constructions, command and per-test diagnostics are preserved in the receipt and test source.

The root investigation paused historical registration following notice of newly received agency material. This reviewer did not open that material, call the historical `run()` entry point, inspect historical automatic matches, or calculate historical transforms. Reproduction of historical outputs and comparison with the annotator's evaluation envelopes therefore remain pending. This receipt is not completion of the protocol's complete historical acceptance gates.

| Observed synthetic result | Scope of what it establishes |
|---|---|
| All 81 windows of a deterministic score grid agree with a direct, independently written zero-mean NCC calculation; maximum difference `3.712308238590367e-16`. | Arithmetic agreement for this construction, supplementing the specific matching controls. The independent oracle explicitly subtracts both patch means. |
| Known integer shifts pass at sizes 19 and 27; positive contrast/brightness change preserves the true match. Negative contrast rejects. | The stated integer matcher and normalization behave correctly on the tested textures. |
| A same-core distractor rejects at size 19 but distinguishing outer context passes at size 27. | Template-size dependence is demonstrated and cannot be treated as a reason to silently favor the passing historical size. |
| Two equal adjacent maxima have a distant-competitor margin about `0.1997`, yet reject with `tied_best`. | The preregistration tie concern is resolved by the added full-grid tie count; exclusion-radius margin alone would not have rejected this case. |
| Constant-template and constant-candidate grids are entirely undefined and reject. Nominal-radius and image-clipped boundary winners also reject. | Tested undefined-score masks and effective-boundary handling fail closed. |
| The deterministic half-pixel horizontal blend gives best NCC about `0.7151` and rejects. A textured smooth ramp also rejects as nonunique. | A valid synthetic shift can fail the screening gate; lack of a passing match is not lack of motion. No subpixel accuracy is established. |
| Exact translation, proper similarity and affine mappings agree with independent calculations and leave-one-out predictions. | Numerical fit behavior on known maps. Translation uses a direct mean, similarity a complex-plane closed form, and affine a direct QR solve in the independent oracle. |
| For displacement `d=(9,12)` of one of six references, fitted translation is `(1.5,2)`, Euclidean RMS is `5.590169943749475`, and LOO errors are `(3,3,3,3,3,15)`. | All six references remain in the calculation; the inconsistency is retained and the screen rejects. |
| Noncoincident collinear geometry passes proper similarity and rejects affine. Five collinear plus one off-line can fit affine exactly, but holding out the off-line point fails rank and prevents consistency acceptance. | Model-specific identifiability and the separation of full-fit success from failed LOO geometry are correctly implemented in these controls. |
| Near-collinear affine design is rank 3 but has normalized condition about `1,358,263.42`; it rejects. Coincident, reflected and collapsed-map controls also produce the declared rejection/invalid-mapping flags. | Passing rank alone is insufficient; conditioning and positive nonsingular mapping checks have tested consequences. |
| Invalid dtype, shape, center, radius, model and nonfinite point contracts reject. | These finite malformed-input cases fail closed; arbitrary malformed configurations are not exhaustively tested. |

No blocking numerical defect was found by these tests. Minor floating-point score overshoot above 1 at machine precision is retained in raw arithmetic; assertions use a declared `1e-11` score tolerance and do not interpret scores as probabilities. No production code or historical thresholds were changed by this reviewer.

An additional read-only analytic reviewer independently confirmed the outlier formula and geometry distinction without seeing code, images or annotations. For six equally weighted translated points, the LOO residual is exactly `6/5` of the corresponding in-sample residual. Translation LOO therefore supplies a stricter rescaling of the same inconsistency, not an independent source of validation evidence. More generally, common displacement added to every matched point leaves both in-sample and LOO errors unchanged. A coherent correspondence error can pass both gates with zero residual.

The tests exercised `match`, `fit_points`, and `fit_with_loo`. They did **not** execute the historical run wrapper, file/config ingestion, product inventories, synthetic-to-historical integration, complete historical score grids, two historical repetitions, or independent-coordinate comparisons. The all-six-candidate restriction in the run wrapper was inspected in code but was not tested by launching that wrapper. Those are material remaining checks if this version resumes historical scoring.

Reproduce only these synthetic checks with a new, non-existing receipt filename:

```sh
[local-path-sha256:d253ac5ca405bea7268a7b6981029e99142dfed700872fc3eedd9ef53be5b71e] research/sherlock-wtc7-investigation/reference-motion/independent_tests.py --out research/sherlock-wtc7-investigation/reference-motion/independent-tests02.json
```

The test runner preserves prior receipts by refusing to overwrite them. It disables Python bytecode-cache writing before importing the computational subject and does not invoke its historical entry point. No browser, network request, source-video decode, canonical-record modification or external transmission was used for this review.

### Resumed historical verification plan

On resumption, the root investigator authorized a separate verifier and will provide explicit completed-run paths. Before inspecting those outputs, this reviewer declares complete coverage of 1,608 match rows/score grids and 804 model rows per run: 71 + 63 event images, six configured references, two template sizes, and three candidate mapping models. Prior input identities, saved PNG/luma bytes, configuration, procedure snapshots, complete product inventories, and two-run byte identity will be checked. Expensive numerical checks may run once on the first copy when every corresponding product in the second copy is independently verified byte-identical.

Full NCC grids will be independently recomputed using zero-padded FFT cross-correlation and integral-image window sums/variance, without importing the historical matcher. This route differs from the implementation's sliding-window/einsum arithmetic. Grid shape and finite/undefined masks must agree exactly; finite scores must agree within absolute `1e-8`. Fixed synthetic score-grid controls will first check the independent FFT routine against direct mean-subtracted patch correlations. Saved winners, competitors, tie counts, exact gate decisions, row coverage and all-six admission will be independently derived from the stored grid values without applying the numerical comparison tolerance to screening thresholds.

The `1e-8` grid comparison tolerance is looser than the declared `1e-12` tie rule. Numerical grid agreement and correct screening bookkeeping are therefore separate findings. The verifier will also report any winner/gate differences obtained from independently recomputed grids, plus threshold proximity; a passing bookkeeping audit must not be described as proving numerically invariant localization.

Every admitted transform and each leave-one-out fold will be independently recalculated using a direct mean for translation, complex-plane similarity, and direct QR affine least squares. Coefficients, residuals and held-out errors use absolute `1e-8` and relative `1e-10` comparison tolerances; reference membership, rank/conditioning disposition and recorded screening decisions are checked separately. The same scientific limits from the synthetic review continue to apply. No historical output has been inspected at this resumption-plan stage.

### Completed historical numerical and product verification

After the root investigator explicitly released terminally completed `run01` and `run02`, [verify.py](verify.py) completed the declared checks successfully. [verification01.json](verification01.json) is the full independent receipt. The preceding FFT-only self-check, which read no historical outputs, is preserved separately as [verification-selfcheck01.json](verification-selfcheck01.json). There was no failed historical verification attempt or change to the verifier between those two checks. The verifier remains frozen at SHA-256 `b19d4692706e47f29ce9356342c12dcd6821c21dd7124de58d6570f38cc1ed0f`.

The count scope is explicit: **33 receipt-listed products** are byte-identical between the two historical runs. The receipt itself is also independently byte-identical, with SHA-256 `3e84b93f588ba329a122ee6ac8ef0ac7daf67a9ba6451503c75ff968682eaf17`, giving **34 files per run including the receipt**. Every listed product, snapshot, runtime/procedure pin, and exact input-pin set was checked. All 134 input native PNGs were checked for byte identity, luma identity, mode, dimensions and exact increasing source PTS; original source/map bytes were also rehashed before and after numerical review. These are the preserved event inputs, not a new video decode.

The FFT routine first agreed with direct patch correlations on all 226 finite synthetic-control windows, with maximum difference `3.885780586188048e-16`, and correctly retained an entirely undefined constant-window mask. It then independently recomputed **all 1,608 historical score grids**, containing **3,836,112 grid values**. Shapes and undefined masks match exactly. The maximum finite NCC difference was **`3.980149543281186e-14`**, below the declared `1e-8` comparison tolerance. All compared winners, competitors, tie counts, flags and statuses also agree when derived from the independently recomputed grids. No row was within the declared review proximity of the NCC, competitor-margin or two-pixel consistency thresholds. This observed numerical agreement does not calibrate the screening thresholds or guarantee invariance under other decoders, libraries or image preprocessing.

All **1,608 match rows** and **804 model rows** have the exact declared coverage, order, source timestamp, reference identity and template size. Every six-reference admission or rejection is correct under the stored-grid gates. All **252 admitted model fits** and **1,512 leave-one-reference-out folds** were recalculated independently. The other **552 model rows** correctly remain reference-quality failures. All **24 overlays** were reconstructed pixel-for-pixel, including original image pixels, candidate positions, colors and labels; this checks rendering, not the visual correctness of a material-point identity. Numerical checks performed on `run01` transfer to the independently verified byte-identical product copies in `run02`.

| View / template | Passing individual candidates | Images admitted to each model | Translation / similarity / affine consistency passes |
|---|---:|---:|---:|
| Camera 2 / 19 | 310 of 426 | 0 of 71 | 0 / 0 / 0 |
| Camera 2 / 27 | 355 of 426 | 0 of 71 | 0 / 0 / 0 |
| Camera 4 / 19 | 260 of 378 | 42 of 63 | 41 / 42 / 28 |
| Camera 4 / 27 | 264 of 378 | 42 of 63 | 41 / 42 / 33 |

Camera 2's frozen C2-R3 center is `(288,400)` in the native pixel convention. Its baseline standard deviations are `1.806446781685411` at side 19 and `1.8198184565228372` at side 27, below the gate of 2; this persists in every frame because the baseline template is fixed. The root investigator subsequently relayed the independent annotator's confirmation that the bright-cap description had been associated with the wrong coordinate. This is an **annotation description-to-coordinate error**, not merely a low-texture-footage result. This numerical reviewer did not make a new visual identification. The original coordinates, descriptions and all outputs must remain preserved with the post-output correction explicitly labeled; no reference was dropped or replaced to obtain a passing Camera 2 fit in this version.

Camera 4's admitted index sets are identical across template sizes: the first 42 selected images, indices 899 through 1199, with exact endpoint PTS `899899/30000` and `1200199/30000` seconds. Every remaining selected image fails all-six admission. At index 1199, translation's maximum residual is `2.0069324297987152` pixels and its maximum LOO error is `2.4083189157584686`; both sizes reject that translation screen. Similarity's corresponding values are `0.6618093033103456` and `0.8804412476786075`. These are image-coordinate consistency calculations and do not establish physical camera movement, stationarity, scale, depth or a valid correction at the building.

The affine comparison has been checked at the appropriate metric. On the same admitted references, affine RMS never exceeds similarity RMS within `1e-10`, but its **maximum** point residual is greater in seven side-19 frames and two side-27 frames. Its maximum LOO errors are `4.433638186176743` and `4.636514503384739`, versus similarity maxima `1.3009825515712259` and `1.964888372358922`. The permissible claim is about least-squares flexibility and observed omitted-reference prediction, not universally lower maximum training residual or a physically true similarity camera model.

The review read the root [report](report.md) at SHA-256 **`56b2d8774808fcdd8e502d80972c8c67f6c51222927c338673a47e65a1f0995f`**. Its arithmetic counts, reported extrema, least-squares-versus-maximum distinction, and stated physical limits agree with the verified records. Two requested wording updates were sent to the root: replace the then-possible/unresolved C2-R3 mismatch with the annotator-confirmed error, and restrict “narrowly” to the `2.006932` in-sample residual rather than the `2.408319` LOO error, which is about 20% above 2. That reviewed hash predates replacement of the draft's pending-review paragraphs; later report text is not silently covered by this hash-specific review.

**Conclusion within scope:** no blocking numerical or product-integrity defect was found in these two completed historical runs. The unsuccessful Camera 2 configuration, later Camera 4 rejection, model/size sensitivity, and remaining material-point uncertainty are substantive limits to preserve. These checks establish reproducible calculations and artifacts, not human/expert validation, historical camera authenticity, calibrated motion, or a collapse-cause conclusion. Independent visual comparison and its post-output annotation correction remain a separate review record; neither this reviewer nor the verifier substitutes for that record.

Reproduce the historical numerical check with a new receipt filename:

```sh
[local-path-sha256:d253ac5ca405bea7268a7b6981029e99142dfed700872fc3eedd9ef53be5b71e] research/sherlock-wtc7-investigation/reference-motion/verify.py --runs run01 run02 --out research/sherlock-wtc7-investigation/reference-motion/verification02.json
```

This reads only the released local run products and their explicitly pinned public-footage inputs, preserves prior verification receipts, and does not import `measure.py` or call its historical entry point. The verifier shares NumPy/Pillow with the implementation; full numerical-library independence and physical correspondence validation are not claimed.

### Bounded follow-up on report wording and verifier reproduction

The root investigator independently reran the frozen verifier. [verification02.json](verification02.json) reports `pass`, `passed_declared_checks`, and `all_compared_decisions_agree` using the same verifier SHA-256. This is a repeat execution of the independent verifier, not another independent event sample.

The changed report paragraphs were reviewed at SHA-256 **`4744aba276193c9def91415adbb0212dd4ca2cb9a4565d6c7cacc9e5ab45cf78`**. They now explicitly identify the annotator-confirmed coordinate-selection error, preserve the invalidated R3 feature-identity association, and distinguish the slightly exceeding in-sample residual from the LOO error about 20% above threshold. Those requested wording corrections are resolved. The report's still-pending manual-comparison integration remains outside this completed numerical review; later additions should retain their own actual coverage and unresolved feature-identity qualifications. No further numerical tests were necessary after the complete checks and repeat execution passed.
