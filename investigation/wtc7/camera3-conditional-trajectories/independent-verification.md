# Independent extraction, product and conditional-fit verification

## Disposition

**PASS for the declared numeric extraction, selected-image integrity and
conditional fit arithmetic.** No source-field, dependency, image-product,
window-coverage or numerical discrepancy was found. This is not a finding
that the saved points retain one physical feature, that the clock measures
historical exposures, that the assigned metre scale is physically validated,
or that any fitted coefficient establishes gravity, forces or cause.

The reviewer read the current charter, new `PROTOCOL.md`, parent
`metric-motion-audit/clock-source-review.md`, extraction producer and view
producer completely. The declared PointMass Java ranges 2840–2865,
2900–2932 and 3350–3400 and ImageCoordSystem 1128–1148 were read at the
pinned public source paths. They support the saved-field interpretation,
not the historical application's actual runtime. The fit producer was read
fully before historical fit values were examined.

The independent implementation never imports either producer. No Tracker
application, second 442-frame decode, image interpretation, new production,
held packet, external transfer or canonical promotion occurred. Only new
research verification artifacts in the dedicated investigation worktree were
written. Existing source, protocol, observations and producer outputs remain
unchanged. No reported reviewer or producer failure was suppressed.

## Subjects, receipts and execution

| Artifact | SHA-256 |
|---|---|
| Protocol | `d7fd79c3269155a06225346273aab4a6352c14c233beda4fa88989d244d3ec01` |
| Public original TRK | `955d1c2d00d7c287f4f235063eb603a0080cf0941595a5419aa7c94726c1a41c` |
| Sanitized settings | `ccfd9c4de098539680caf9f296eb5ea784ade27497d860a32284285e577cefeb` |
| `extract_points.py` | `08a851c45103516015b07c291ff06ca8e4596c7d9b7b60831515becdb9ea4c2f` |
| `extraction01/points.json` | `f85e6f0ddbb55e3ef142a62e774237c69a59b9bbcbc31a92f93a37b9a9099df3` |
| `extraction01/receipt.json` | `599911e494dc79f0cec5770a6caed44ddee1d9acb3fa64554db0e371bf86a16c` |
| `prepare_views.py` | `ea8f3d1b156db207c4e8d9ff9eb96ed27511792d6f2e739b80f7edc976ef13e4` |
| `fit_trajectories.py` | `dd8bbcb594d71f8d5085b7322e8292035127b4860112595c850fe0c41a2f32b4` |
| `fit01/fits.json` | `253bc0c3b3edc72f5bb261e49d6a87d8e1406ee5d33f832ed9bb7908ed7350a0` |
| Independent `verify_trajectories.py` | `710d196aba2600d102c7cb92d532d6a6e85aed6af633be8bcc199539e7b6efd0` |
| `independent-source-products01.json` | `e262101c0d4aa0246ad67ecf51c47a2919a1c88bf982a5aaca3f9397a4a9e813` |
| `independent-receipt01.json` | `4d1ec768f50a46da08cd5768c90b4fa4b25cfba1d0e33cdf749fe0cbc82f86e7` |

Both commands were run in the dedicated investigation worktree with Python
3.13.7 and Pillow 12.0.0. Each independently observed completion returned
**exit 0** and a `pass` receipt:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera3-conditional-trajectories/verify_trajectories.py --out independent-source-products01.json
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera3-conditional-trajectories/verify_trajectories.py --fit-run fit01 --out independent-receipt01.json
```

An earlier source/product-only invocation also exited 0 before the fit
extension, with its coverage reported to root; it did not write a receipt.
The two preserved receipts above use the same final verifier bytes. The
verifier AST parsed successfully. The independent implementation uses no
NumPy fitting, pseudoinverse, SVD or drawing operation.

The source/product stage checks **30** consumed file/runtime pins before
and after its work. The fit stage checks **11** before and after, joining its
points/protocol/extraction receipt to the preceding source check. Every
producer-declared input/output hash and expected product inventory matches.
These are stage-specific integrity checks, not historical authenticity or a
guarantee against arbitrary concurrent modification outside their intervals.

## Original numeric extraction and clock coverage

The preserved original project was checked as bounded inert XML only after
its expected SHA-256 matched. DTD and entity declarations are rejected
before parsing. The independent parser traverses the direct track collection
and selects the two PointMass objects in sibling order, independently of the
producer's XPath selection. It permits only the expected frame indices,
finite numeric x/y texts and the eleven explicitly approved configuration
properties. Arbitrary source names, author-machine paths, comments and
surrounding XML values are neither emitted nor written to a receipt.

Actual comparison coverage:

- Both 71-point arrays: **142 point pairs and 284 exact numeric coordinate
  texts**, with corresponding finite parsed values. The index sequence is
  exactly 138, 141, …, 348 for each ordinal; no duplicate, missing or reordered
  row was found. Ordinal labels are not physical feature identities.
- **Eleven configuration fields**, each joined original XML → existing
  sanitized derivative → new numeric extraction, including exact text and
  parsed value. Origins, angle, equal scales, duration and selection settings
  are saved assignments, not newly measured physical quantities.
- **304 current diagnostic clock records**, indices 138–441, compared
  field-for-field to the old map. Every PTS × time-base equals its recorded
  rational seconds value.
- **71 distinct saved-mark times** (used by both tracks, hence 142 track/time
  rows) have exactly equal nominal `(frame-138)/15` and current diagnostic PTS
  minus PTS[138]. Both complete 71-entry exported fit-clock arrays match.

The match supports use of these two explicitly named clock scenarios. It
does not independently recover the historical Xuggle time array, exposure
cadence or an error bound; the equal scenarios are not independent clocks.
Assigned time zero is not physical collapse onset.

## Selected-image and overlay checks

All **eight native PNGs** are grayscale `L`, 720×480. All **eight overlays**
are RGB, 720×480. The selected indices are exactly 138, 168, 198, 228, 258,
288, 318 and 348. Native file hashes, decoded pixel hashes and all product
metadata match the new receipt and old diagnostic frame map.

The preserved WMV hash is
`48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722`;
the old diagnostic map is
`8afdf759ecc45215b9212699ef2adb72de553c52667d82b39c9382df8e6b36c2`.
The new producer receipt's command matches the old default command exactly,
and its recorded whole-stream byte count/hash/all-frame equality agree with
the old map. This reviewer independently checks the eight retained native
frames, **not a second full 442-frame decode**. The producer's full-stream
check remains attributed to its code and receipt. The diagnostic warnings
are not silently upgraded to a clean historical-media certification.

For every overlay, independent integer pixel-set construction starts from
the native grayscale bytes, applies the source-point nearest-integer
rounding and the declared cyan/yellow cross arms, and compares **all
2,764,800 output pixels** across eight images. Each has 72 analytical mark
pixels in the union of both crosses. Colors, clipping, raster centers,
in-bounds flags and mark metadata agree. This is a check of the declared
new pixel-centre query display, not original Tracker raster conventions,
subpixel localization accuracy or architectural interpretation. Analytical
marks remain distinct from recording content.

## Independent fit oracle and prospective tolerance

Before opening historical fit values, the reviewer adopted and communicated
the protocol's **absolute 1e-9** comparison tolerance for coefficients and
derivatives and **absolute 1e-8** for SSE. Exact source-field, index, clock
text, window and method identity was required. The 1e-9 check is also used
for residual, RMSE, condition-number and sensitivity comparisons. No
tolerance or window was changed after looking at results.

The oracle represents the exported finite binary64 coordinates and nominal
clock values as exact rational numbers, forms centered half-span-normalized
polynomial normal equations, and solves them by exact Gauss–Jordan
elimination. It independently evaluates predictions, every residual and
SSE. This removes numerical normal-equation conditioning error from the
oracle; it does not assert that saved point digits are accurate observations.

Quadratic response weights follow from solving the dual normal system for
the acceleration functional `2*c2/halfspan²`; applying them to all input
coordinates reproduces the exact rational coefficient. Their maximum
absolute value and L1 sum are recomputed independently. Condition numbers
are checked by independent Jacobi diagonalization of the normalized Gram
matrix, not by reusing the producer's singular values. The largest checked
design condition number is approximately **7.981632**.

Geometry checks use independently evaluated high-precision Taylor sine and
cosine, the two declared angles and exactly the factors 14/15, 1 and 16/15.
The transform is `X=(cos(theta)*x-sin(theta)*y)/s` and downward
`D=(sin(theta)*x+cos(theta)*y)/s`, with the length factor applied separately.
Every position displacement and quadratic velocity/acceleration is checked
against that declared transform. No assumed gravity value determines scale,
clock, fit window or geometry.

Nine preliminary exact-control groups check polynomial degrees 0–3,
irregular quadratic timing, duplicate-time rejection, translation invariance,
one-point response and linear-length/inverse-square-clock scaling. Twelve
independently reconstructed analytic control cases also cover the producer's
declared cases, including insufficient sample/rank domain, zero/90-degree
coordinate signs and the continuous piecewise-motion witness. The latter's
straddling-window acceleration is exactly 1 in the independent calculation
although the prescribed sides have accelerations 0 and 2. The producer's
control file stores mostly flags, not every intermediate array: this review
checks those flags' names/shape plus independent analytic counterparts, not
unsaved producer intermediates.

## All-window results and error magnitudes

| Checked quantity | Actual coverage |
|---|---|
| Declared windows | 241 per track/clock: 67 five-point, 63 nine-point, 59 thirteen-point, 51 twenty-one-point and one full-span window |
| Track/clock window records | **964**, exact identity and ordering; zero failed windows |
| Axis/polynomial fit cases | **5,784**, both x/y and degrees 1/2/3 |
| Polynomial coefficients | **17,352** scalars |
| Position residuals | **67,464** scalars; none omitted |
| Quadratic response weights | **11,244**, plus every maximum/L1 summary |
| Quadratic geometry cases | **5,784**, each with both velocity and acceleration components |
| Complete transformed trajectories | **12** geometry arrays, each 71 two-component positions |
| Summary groups | All ten min/max groups reproduced from independent window calculations |

Largest absolute discrepancies were approximately:

| Comparison | Maximum absolute difference | Fixed tolerance |
|---|---:|---:|
| Polynomial coefficients | 1.121e-12 | 1e-9 |
| Image acceleration | 3.492e-12 | 1e-9 |
| Assigned-unit acceleration | 1.019e-12 | 1e-9 |
| Residuals | 1.078e-12 | 1e-9 |
| SSE | 1.216e-11 | 1e-8 |
| Quadratic response weights | 6.957e-14 | 1e-9 |
| Condition number | 1.688e-14 | 1e-9 |

The receipt retains comparison counts and maximum errors for every checked
numeric family, a complete discrepancy list (empty), and one independent
record for every window, including independently calculated acceleration,
SSEs by degree and condition numbers. Original points, all producer fit
coefficients/residuals, every sensitivity weight and all geometry scenarios
remain in their frozen producer artifacts. No best-g subset replaces them.

## Scientific ceiling and next use

The strongest verified claim is that these particular saved arrays give
these conditional polynomial and assigned-unit results under the named
clock and affine geometry scenarios. Numerical failure in another
implementation, a source/hash mismatch or changed window definition would
falsify that computational claim. None was found in this review.

For equally spaced saved marks, the 5/9/13/21/71-point windows span
0.8/1.6/2.4/4/14 assigned seconds. Windows overlap; the two clock scenarios
coincide here. These calculations do not create independent observations.
A fitted quadratic's constant acceleration describes its whole fitting
window, not necessarily an instantaneous acceleration. Cubic residual
improvement can indicate model-form sensitivity, not a new validated
physical mechanism. Residual size and unit-coordinate sensitivity are not
complete annotation, projection or clock uncertainty and are not confidence
intervals.

Physical feature continuity and sampled visibility boundaries require the
separate observations and report; this reviewer did not inspect or infer
them from the numerical outcome. Those limitations should tag the affected
windows, not erase their calculations. The illustrative 14/15/16 scale
choices are not measured uncertainty bounds. The conventional 9.80665 m/s²
constant was verified as a comparison reference only; no gravity-equivalence
threshold or causal ranking follows from its presence.

Root's bounded report and independent full-code rerun can now use these
verified conditional results while retaining those limits. Neither an
internally successful reconstruction nor an ambiguous landmark is proof of
historical physical validity or contrivance.
