# Foreground reference diagnostic — implementation and preparation review

Research-only, 2026-09-12. This is the reference producer's method review,
not the separate numeric reproduction or a human/expert approval. Read the
final run receipt before accepting any generated summary. No saved target
tracks or new target-annotation files were read for this work.

## Authority and execution

The frozen `PROTOCOL.md` SHA-256
`7b13e006ab382121452f6e7c59f37d7f586b57f297a7e1c7154b86b2aae06c2f`
and `reference-preflight.md` SHA-256
`7417b2600ec7ca6f4a1464a7ee918bceb23962d09d3ea8708b8565b49cf73015`
control centers, patch sizes, search limits and gates. All three preflight
acceptances were preserved, including the low-contrast and uniqueness warnings.
Neither centers nor thresholds changed. Repository WORKFLOW/START-HERE and the
evidence-falsification, source-of-truth and development-verification skills
kept this as a non-canonical local computation with explicit limits.

Executed from the isolated investigation worktree using:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera3-late-reannotation/reference_diagnostic.py --out reference01
```

The run exited 0. Python 3.13.7, NumPy 2.3.4 and Pillow 12.0.0 are recorded
in the receipt. All 27 input pins (protocol, preflight, preparation code,
views receipt, diagnostic code and 22 native PNGs) were unchanged before/after.
Every native PNG's file bytes/hash and decoded 720×480 L pixel hash matched
the pinned preparation receipt. This reuses, and does not independently
recertify, the preceding complete WMV decode and its three corruption-warning
mentions. The source remains diagnostic, not a clean historical decode claim.

The script refuses an existing output path. A second invocation against
`reference01` exited 2 with `refused_existing_output`; no rerun or overwrite
was performed. Recognized computational/input errors after creating a new
output directory retain a failure receipt with stage, exception type, pins
and partial-product inventory, not raw exception text. A deliberately injected
failure path was not executed. File-system failure that prevents receipt
creation itself is not claimed to be recoverable by this script.

## Scoring definition and retained coverage

NCC subtracts each patch's own mean, takes the sum of pairwise centered
products, and divides by the product of centered Euclidean norms. Population
standard deviations divide summed squared deviations by side². A zero-energy
template or candidate produces JSON null for that score, not zero correlation.
Rows enumerate dy then dx from −6 through +6; all 169 scores and candidate
standard deviations remain available. The representative winner is the first
exact floating-point maximum in that order. Other maxima within 1e−12 remain
listed and fail uniqueness; a representative in a failed row is not accepted.

The distant alternative is the greatest finite score at Chebyshev distance
at least 3 from that representative winner. All equally best distant
alternatives within 1e−12 are saved. Every declared gate is evaluated without
discarding low-texture rows; a row must pass all five gates. No statistical
confidence, covariance or physical error bound is assigned to those gates.

Fourteen synthetic cases (seven cases at each patch size) ran before real
scoring. Full 65×65 baseline/current numeric inputs, complete result grids and
expected/observed checks are retained. Cases cover identity, known (−3,+2)
translation, the same translation plus brightness offset, positive gain plus
offset without clipping, flat-template rejection, repeating-texture tie/margin
rejection, and a known (+6,0) boundary winner rejected by the boundary gate.
All 14 passed their stated checks. Synthetic randomness is not an unspecified
dependency: the seed and all realized input arrays are saved. The controls
test these implemented operations, not real-reference physical stationarity.

Real coverage is 22 frames × 3 references × 2 patch sizes = 132 rows and
22,308 candidate NCC scores. All 132 passed every declared diagnostic gate.
Consequently all 44 frame/size groups have a mean translation and all three
residual vectors. Nothing was removed or reweighted after scoring.

| Reference | Side | Baseline population SD | Minimum winning NCC | Minimum distant margin |
|---|---:|---:|---:|---:|
| R1 | 21 | 48.453027 | 0.930198 | 0.189732 |
| R1 | 31 | 65.082187 | 0.970612 | 0.267541 |
| R2 | 21 | 27.542582 | 0.982500 | 0.336169 |
| R2 | 31 | 39.130036 | 0.992562 | 0.254197 |
| R3 | 21 | 11.328419 | 0.939808 | 0.229201 |
| R3 | 31 | 16.288345 | 0.967052 | 0.253304 |

Table values are rounded summaries, not outward-rounded bounds. R3's smaller
patch cleared the predeclared SD10 screen despite the preflight warning;
that is a result, not a reason to reinterpret the warning as a guaranteed
failure. Complete numeric values remain in the generated outputs.

Every winning dy is zero. All winning dx are zero except R1/side21 at frame336,
whose winning dx is +1. That group's mean is (+1/3,0), with R1 residual
(+2/3,0) and R2/R3 residuals (−1/3,0). The side31 alternative at frame336 is
zero for all references. All other group means/residuals are zero. These are
integer grid optima; no subpixel refinement was attempted.

## Preparation and display review

Read the complete frozen `prepare.py`. After scoring, this observer also
viewed the full reference-box overlay and all six reference patch displays.
Those displays support the preflight's descriptions of texture neighborhoods,
not a named fixed material point or shared target-plane depth.

A separate read-only numerical check (not importing `prepare.py`) verified
all 51 prepared product file pins. For all 22 target crops and six reference
crops, it extracted native source slices by the declared half-open coordinates,
expanded rows/columns with independent `numpy.repeat`, and compared every RGB
image-interior value at the stated display offset (50,35). All 28 crop
interiors matched exactly: 12,149,184 display pixels / 36,447,552 RGB channel
values. Target displays have shape 785×770×3; reference displays have shape
(35+8×side)×(50+8×side)×3. This confirms crop coordinates, enlargement and no
in-image ruler contamination; it is not a second video decode.

One small presentation defect is preserved: the ruler formula uses
`(factor-1)//2`. At factor3 this is the exact center (1) of each three-pixel
block. At factor8 it is 3, whereas the geometric midpoint is 3.5, so the
reference ticks sit half a display pixel up/left of the replicated block's
geometric midpoint (1/16 native pixel). Each remains inside the correct native
pixel block. The blanket receipt wording “tick at center” is thus exact for
target displays but approximate for reference displays. No target-coordinate
offset follows from this; no frozen preparation or receipt was rewritten.

The preparation script's failure export is narrower than a blanket durable-
failure guarantee: explicit decode-identity failures get `failure.json`, but
timeouts and some later exceptions are not enclosed in a general receipt
handler. This completed run's receipt exists and passes, so that robustness
limitation does not invalidate its actual image products. Preserve this as a
future tool improvement, not an invented failed run.

## Evidence strength and what this does not establish

The direct calculation claim is that these pinned encoded-image textures
have the stated integer NCC maxima under the frozen finite search. Its
separate reproduction is pending the parent's different implementation.
This is positive evidence against a nonzero *common integer vertical image
translation* within the tested ±6-pixel search and the stated texture
associations in these sampled frames. It is not proof of exact camera
stationarity, a bound of less than half a pixel, a subpixel error model, or a
proper camera/perspective calibration. Flat regions, compression, local
texture evolution and different depths remain relevant limitations.

A common same-frame vertical translation cancels algebraically from A−B,
regardless of these measured optima. Rotation, depth effects, shape change,
silhouette-versus-material identity and annotation error do not thereby
cancel. Fresh target annotation, comparison and direct A−B interval fits are
the next tests; reference matches alone cannot establish target acceleration,
force, simultaneous support loss, initiation mechanism or intent.

## Artifact pins

| Artifact | SHA-256 |
|---|---|
| reference_diagnostic.py | `f2cb0ae86e4d040ede3c6227cc1a83860f2d2cdbb54544dc5db50e18c758e371` |
| reference01/controls.json | `4753a42906ded0f88ead1b339bc6a675111774365c6588a7a05d59ff7bb7c2f5` |
| reference01/scores.json | `2ffe62689d95524fb28290709deca8f56d49fada9d167d9cfba48166016d2e94` |
| reference01/summary.json | `ff3a485bc436290378d645d18c0d1f6783388ad26716fad7e108c0d130d34799` |
| reference01/receipt.json | `39e2729c06729806937504a9f00238c94e5c053ec0289d4e2cb0bce948932c57` |

All files are working research derivatives. Source files, frozen declarations,
legal record, other worktrees and canonical spines were left unchanged. No
outreach, sensitive export, publication, accepted finding or Faraday run occurred.
