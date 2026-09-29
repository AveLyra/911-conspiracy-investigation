# Photometric sensitivity verification record

Calculations were completed September 13; report closeout continued September
15, 2026 after rechecking current repository controls and frozen pins. This is
research-only integrity/arithmetic verification, not historical authentication,
engineering validation, discovery narrowing or disclosure clearance.

## Inputs and procedure

The [protocol](PROTOCOL.md) hash is
`edbc10c984c45e915d40853ea1ea0e9aa97f256af47643afa944dda278a8b7ed`.
The unchanged [producer](measure.py) hash is
`eff2aa28a85d303ec6f17b47be312bfc13de35dbaa1c117a2d8ade5a7a03041a`.
The protocol and the pre-result portion of the independent method review were
saved before historical calculation; subsequent review addenda are explicitly
labeled. The Figure 149 fit/test overlap and comparable holdout baseline
issues were corrected before controls and data, not after seeing their scores.

Inputs are the twelve saved native-image candidates and two target JPEGs named
in each result's `inputs`, with exact byte/hash checks before and after the
producer calculation. Prior summary, mask/core code and completed image receipts
are pinned. No source video was re-decoded or newly rehashed for this unit.
The source relationship still depends on the preceding verified extraction.

Environment: bundled Python 3.12.14, NumPy 2.3.5, Pillow 12.3.0. No install,
browser, network retrieval, model solver, bridge or new source import occurred.
The absolute interpreter is
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.

## Executed checks

| Check | Actual result | Scope |
|---|---|---|
| Producer synthetic controls | 28/28 | Recoverable curves, ties, quantization, displaced/altered patches, masks, padding, clipping and gates; not historical equivalence. |
| Historical coverage | 12 pairs, 48 processing branches, 672 fitted curves | All declared pairs, branches, folds and powers; no W/D-selected curve winner. |
| Complete same-code reproduction | Exact results bytes, exact compressed-array archive bytes, all 208 loaded arrays equal | Two fresh runs using identical source/recipe/environment pins. |
| Separate checker controls | 23/23 | Different OLS/rank/quantile/error/coverage implementations and corruption detection. |
| Independent historical arithmetic | All 454,236 compared leaves pass | 672 fits; 392 baseline/rank region rows; 6,832 fitted-region rows; 1,344 repeated foreground-baseline rows. |
| Root checker replay | Exact substantive agreement, apart from argv and elapsed time | Root read the full 407-line checker before replay; not a third independent method. |

The largest independent float difference is `7.016609515630989e-14`.
Coefficient tolerance is 1e-10 absolute; other floats 1e-9; counts/nulls exact.
The independent solver uses a least-squares design matrix instead of the
producer's covariance formula. After coefficient verification it uses the saved
coefficients for prediction diagnostics to avoid solver-rounding changes at
exact thresholds/endpoints. It separately reconstructs masks, folds and validity
geometry but shares saved source/target arrays and NumPy. It does not independently
decode or resample the historical files. Root replay preserves this limitation.

Both production runs completed in 6.29–6.49 seconds, below 300 seconds. The unit
was approximately 51.3 MB before report closeout, below the 100 MiB aggregate
cap. The final artifact receipt records exact then-current size and document
pins. Disk checks do not establish peak memory bounds or actual forced-timeout
behavior.

## Output pins and replay

Both `run01/results.json` and `run02/results.json`:
`9d6ca5108b3c779f16f4174987577865962983ed90bf2eb577edf30aa25aed55`.
Both `arrays.npz`:
`f4b1da4be7e3bd1df467e60979d383a5dfb418e0d0b33cca7b7770e0fc62c02e`.
[Summary](summary01.json):
`024f7c989deda3663df78caaff82cafac98d5079ea084057019e15288353e17e`.
[Independent checker](independent_check.py):
`029f3bdcd582c96ff0e2a440ae8c66c6133c8280bfe209e6da6843fdc63c1497`.
[Root check](independent-root01.json):
`5d9bcc214bdd88906807f6896dbdf8511f0944a879b2aebe4d6e5d81ca5bcf91`.

Commands used the bundled interpreter with `-B`, from the investigation root:

```text
research/sherlock-wtc7-investigation/peskin-photometric-sensitivity/measure.py --run controls01 --controls
research/sherlock-wtc7-investigation/peskin-photometric-sensitivity/measure.py --run run01
research/sherlock-wtc7-investigation/peskin-photometric-sensitivity/measure.py --run run02
research/sherlock-wtc7-investigation/peskin-photometric-sensitivity/summarize.py
research/sherlock-wtc7-investigation/peskin-photometric-sensitivity/independent_check.py --run run01 --output independent-root01.json
```

These output slots are create-only and already occupied; do not overwrite them
or weaken guards. A fresh full replay needs a declared clean derivative context
with identical dependencies and recorded paths. The existing independent checker
can also audit either preserved run with a fresh scoped output filename.

An initial `py_compile` attempt was denied while trying to create `__pycache__`;
subsequent read-only AST parsing passed. The reviewer's initial output-writing
attempt needed scoped worktree permission. Neither was a failed historical
measurement. No failed scientific control was erased. Report and final review
changes do not alter the frozen protocol, measurement code or data.

## Inspection and authority limits

Root re-viewed the full original-size Figure 5-149 target in this unit, without
transforms, confirming that a mathematical mask overlap is not itself a physical
foreground classification. The preceding study's full-target/native-image
reviews remain the visual context; there was no new blinded image-rating trial.
Independent arithmetic review viewed no historical images. Numerical resampling
arrays are derivatives, not newly generated historical imagery or thermal maps.

Main/raw/legal records and previous research outputs were untouched. Main was
clean at the September 15 resumption check; other tasks' intervening commits
were not altered. This investigation remains uncommitted in its dedicated
worktree. Generic fit/test-mask and extrapolation lessons were added under the
existing local Sherlock feedback item; delivery remains pending the archived
destination's routing decision. No publication, canonical fact promotion,
outreach, commit or push occurred.
