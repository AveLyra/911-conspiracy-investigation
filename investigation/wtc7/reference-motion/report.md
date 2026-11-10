> **Historical research:** This is a dated computational record, not a new analysis or instruction. Local paths are redacted and omitted dependencies marked; see the [publication note](README.md).

# Multi-reference image-motion constraints

This fixed-reference test supplies a limited Camera 4 image-registration result and exposes a failure in the Camera 2 reference selection. It does **not** supply a calibrated building trajectory, gravitational-acceleration estimate or collapse-cause discriminator. Both historical runs preserve the same results, including all rejected matches. Research-only under Q03–Q05/WP2 (historical local reference `../CHARTER.md`; not included here); no canonical fact or legal claim is promoted.

## Inputs and method

The [protocol](PROTOCOL.md) was declared before automatic matching, but after prior visual familiarity with the footage. Six candidate references per camera were selected by a separate computational annotator. These are not surveyed points or certified stationary objects. The recorded banner, repeated window/lens patterns and different-depth overlap corners carry explicit role uncertainty. Human and specialist review remain unfulfilled.

Inputs are the 71 Camera 2 and 63 Camera 4 event images already preserved in the preceding screening package (historical local reference `../multiview-onset-review/report.md`; not included here). Their source files, exact access-copy timestamps and PNG/luma hashes are pinned in [run01/input-pins.json](run01/input-pins.json). No new decode, retiming, missing-frame interpolation or source-image stabilization was performed. Integrity relative to captured bytes is not original-camera authentication.

Each feature is independently searched within 24 pixels of its frozen baseline position, using both 19×19 and 27×27 templates. Templates and centers do not update across time. The [implementation](measure.py) saves every normalized-correlation grid, undefined score, competitor, tie, boundary and quality flag. A best-scoring location is not automatically admitted as a match. All six references must pass before translation, orientation-preserving similarity or affine fitting; no outlier is discarded. Source code, parameters and protocol are copied into each run.

The two-pixel maximum training/leave-one-reference-out criteria are uncalibrated consistency screens. They are neither statistical confidence limits nor accuracy bounds at the building. In particular, translation leave-one-out error is exactly 6/5 of its corresponding in-sample error for six equally weighted points: it is a stricter rescaling, not an independent validation source. More flexible maps can be unstable when a geometrically important reference is omitted. Common correspondence errors can pass every internal residual check.

## Complete matching and fitting result

Each run contains **1,608 match rows and score grids**, and **804 model-status rows**, covering every declared image, reference, template size and model. Across matching rows, 1,189 candidates pass and 419 reject. Across model rows, 252 are computed and 552 fail reference admission; 227 of the computed fits pass the consistency screen. These repeated, overlapping measurements are not independent historical observations or scientific confidence scores. [Complete matches](run01/matches.json), [model results](run01/transforms.json), [descriptive summary](summary01.json).

| Camera / template | Passing patch candidates | All-six model fits per model | Translation passes | Similarity passes | Affine passes |
|---|---:|---:|---:|---:|---:|
| Camera 2 / 19×19 | 310 / 426 | 0 / 71 | 0 | 0 | 0 |
| Camera 2 / 27×27 | 355 / 426 | 0 / 71 | 0 | 0 | 0 |
| Camera 4 / 19×19 | 260 / 378 | 42 / 63 | 41 | 42 | 28 |
| Camera 4 / 27×27 | 264 / 378 | 42 / 63 | 41 | 42 | 33 |

### Camera 2: the six-reference procedure fails at its own seed

C2-R3, frozen at (288,400), has baseline template standard deviations **1.80645** and **1.81982** Y code values, below the declared minimum of 2. It rejects in all 71 images for each size, including the baseline. Thus the original all-six procedure produces **no Camera 2 transformation**, even though several other references produce stable-looking candidate coordinates. A baseline match to itself can have correlation approximately 1 and still fail texture suitability.

The other results must remain visible: C2-R1/R2/R4/R5 pass every selected image at both sizes. C2-R6 passes 26/71 at size 19, with 45 distant-competitor rejections, but 71/71 at size 27. Several candidate centers repeat exactly; others differ by one or two stored pixels. This shows template-context dependence and integer quantization, not certified zero camera motion.

Post-output visual inspection identified a description-to-coordinate mismatch, subsequently confirmed by the original annotator: the C2-R3 center is on a dark patch above/left of the small bright cap described in the annotation. This is a **reviewer coordinate-selection error**, not merely low resolution. The original record is preserved, and all five R3 manual evaluation rows (ten size-specific comparisons) lack the claimed feature-identity support. Neither low texture nor repeated nominal manual coordinates can repair that association. The source imagery itself has not failed this test; the **declared reference selection and gates** have failed to admit a fit.

### Camera 4: early consistency, model sensitivity and later loss

For both template sizes, all six references pass in the first **42 selected images**, indices 899–1199, approximately **29.996633–40.006633 seconds in this access copy**. These are sampled encoded frames, not proof of continuous track validity between them. Similarity fits pass all 42 screens. Translation passes 41, ending at index 1192 (39.773067s); at index 1199 its maximum residual is 2.006932 pixels, just above the two-pixel screen, while maximum leave-one-out error is 2.408319 pixels, about 20% above it. The threshold is not a sharp physical boundary.

At index1199, both sizes produce identical six candidate displacements relative to their original seeds: horizontal changes from −3 to 0 pixels and vertical changes from −20 to −18 pixels. The similarity fit accommodates the differences with maximum residual 0.661809 and maximum leave-one-out error 0.880441 pixels. This is a coherent **image-coordinate** change among the selected reference candidates, consistent with the already observed reframing. It does not identify a camera's physical translation/rotation, a focal-length history, a common depth plane or a correction valid at the building.

From index1207 (40.273567s) onward, the remaining **21 selected images** fail all-six admission for both sizes. Four references fail at the first such sample; isolated foreground references remain candidate matches longer, depending on size. No subset is used to extend the camera fit. In the fixed late manual samples (1259 and1350), the original sign, upper-left window and upper-right signal are out of view, while the other selected anchors are ambiguous. A red rejected maximum elsewhere in the frame is not a recovered reference.

Affine flexibility does not solve the problem. Its maximum leave-one-out error among computed fits reaches **4.433638 pixels** at size19 and **4.636515 pixels** at size27, compared with similarity maxima of **1.300983** and **1.964888**. Fewer affine fits pass. Lower least-squares training error does not guarantee better prediction of an omitted reference; these references' geometry, correspondence error and integer sampling matter. This is evidence against selecting a correction solely for its fit to the same points used to estimate it, not proof that similarity is the true camera model.

## Visual and independent checks

Root inspected all **24 analytical overlays**: baseline plus five fixed evaluation images for both cameras and both sizes. They preserve the native source-image dimensions and add colored candidate marks plus an external explanatory footer; they are labeled analytical derivatives, not historical originals. The late Camera 4 rejected boxes visibly fall on unrelated or uncertain content. Some edge labels clip; coordinates and rejection reasons remain in the complete machine records. Frozen manual annotations must not be edited to agree with these outputs.

The separate [computational review](independent-method.md) reproduces every complete score grid through a different arithmetic route, checks all 804 model-status rows and independently calculates all 252 admitted fits and 1,512 omitted-reference predictions. Its maximum score difference is 3.98015×10⁻¹⁴, and all compared match decisions agree. Root reran that verifier successfully. This establishes numerical reproduction within the stated tolerances, not physical validity.

The [frozen manual-comparison plan](independent-comparison.md) and [complete 120-row comparison](independent-comparison.json) preserve the distinction between coordinates and identity. At each template size, all 48 originally localized rows have finite automatic winners inside the subjective manual envelopes. But five of those rows are C2-R3's now-invalidated landmark association: numerical agreement with a misplaced manual anchor is **not correct feature identification**. Those rows remain explicitly flagged, not deleted to improve a score. The remaining rows also retain their original role/depth and subjective-localization limits.

Among the 30 Camera 2 evaluation comparisons per size, 23 pass automatic gates at size19 and 25 at size27; the others reject despite falling within the coarse manual envelopes. The extra size19 rejections are C2-R6 at indices6654 and6751. Camera 4 has 18 passing, coarsely localized comparisons per size and 12 rejected late comparisons, whose manual status remains six ambiguous and six unavailable. No accepted automatic candidate occurs in that late unresolved manual sample. This is a bounded sample result, not a calibrated false-positive rate or proof that all accepted candidates have the right identity.

The annotator also inspected all 24 overlays after scoring and rechecked the Camera 2 baseline/native grid after root raised the R3 issue. This confirmation was prompted and post-output, not a blind independent discovery. Original [annotations](independent-annotations.json), descriptions and coordinates remain unchanged. All 120 compared rows agree exactly between runs. Root read and reran the comparison script: all result fields agree except the recorded Python runtime (reviewer 3.14.0, root 3.13.7), so the comparison JSON outputs are not byte-identical. Rerunning arithmetic does not repeat or independently validate the visual attestation embedded in that result. The [comparison report](independent-comparison-results.md) preserves the original reviewer's exact coverage and correction history.

## Claim ledger and consequences

| Claim | Type / strength | Support and reproducibility | Assumptions, alternatives and weakening test |
|---|---|---|---|
| This exact six-reference Camera 2 configuration admits no transform. | Derived, A within the declared procedure. | Complete status rows; both runs byte-identical. | Threshold/selection failure is not absence of useful visual references. An explicitly versioned, baseline-screened configuration could change this result. |
| Camera 4's first 42 selected frames permit the declared all-six similarity consistency screen. | Derived, A for arithmetic; physical interpretation C. | Full reference/status/fit records and fixed two-size comparison. | Repeated-feature/common-mode errors, uncertain reference stationarity/depth and uncalibrated gates remain. Independent material-identity/calibration evidence could weaken the camera interpretation. |
| The later 21 selected Camera 4 frames cannot be corrected by this all-six method. | Derived, A for this method; general impossibility unsupported. | Recorded failures and late visual/manual limits. | Other retained references, an explicitly changed scale-aware method or original footage could enable another test; no extrapolation or replacement is made here. |
| A more flexible map is not necessarily better constrained away from its fitted references. | Derived/model-dependent, A for these computed leave-one-out results. | Saved per-reference predictions, two sizes and synthetic geometry controls. | A genuinely independent set of well-distributed, same-plane references could give a different result. |
| These results establish collapse acceleration, hidden support timing or a cause. | Unsupported, E. | No building trajectory, force model or physical calibration is computed. | Those require separate measured features, geometry/clocks/uncertainty and structural analysis; software or reference consistency alone cannot supply them. |

No collapse-explanation ranking changes. The new records reduce the risk of treating camera movement, an unsuitable annotation or a flexible fitted map as building physics. The highest-value next media step is to resolve the Camera 2 seed-description error and prospectively specify a replacement/baseline-quality screen, while retaining this unsuccessful configuration. That would be a new exploratory version, not a retroactive success. Camera 4's supported subset can inform a separately declared target-feature feasibility test, but human material-point checks and scale/perspective calibration still precede consequential kinematic inference. [One historical reference to separate agency material was omitted from this public derivative.]

## Sources and reproduction

- Preceding screen and original-source lineage (historical local reference `../multiview-onset-review/report.md`; not included here); this test uses its native `refine01` event images rather than acquiring new footage.
- [Protocol](PROTOCOL.md), [frozen feature configuration](features.json), [independent annotations](independent-annotations.md), [implementation](measure.py).
- [OpenCV template-matching definition](https://docs.opencv.org/4.13.0/de/da9/tutorial_template_matching.html) and [NumPy2.3 least-squares documentation](https://numpy.org/doc/2.3/reference/generated/numpy.linalg.lstsq.html): mathematical background only. The historical matcher is the local NumPy implementation, not an invocation or validation of OpenCV.
- [Validation record](validation.md), [run01 receipt](run01/receipt.json), [run02 receipt](run02/receipt.json), [root controls](controls02/receipt.json), and [independent synthetic checks rerun by root](independent-tests02.json).
