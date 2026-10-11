# CBS correspondence pilot: independent artifact audit

2026-10-04 UTC. Reviewer `/root/one_pixel_check`. Local computational audit
only; no candidate/reference image display, image decoding, historical score
execution, network access or terminal polling/restarting.

## Disposition

**Pass within this audit's artifact, ranking and repeatability scope.** No
mismatch was found. This is not independent verification of the historical
pixel correlations or a source/exposure finding. Root's separate direct-score
and visual checks are outside this audit and are not represented as completed.

The protocol, regions, method review and complete adapter were read before
checking completed `pilot01/receipt.json` and `pilot02/receipt.json`. No producer
ranking, summary or mask function was imported into the checker. Independent
NumPy/standard-library calculations used the saved numeric arrays and records.

## Verified coverage and calculations

| Check | Verified result |
| --- | --- |
| Input pin checks | All 39 paths rehashed successfully, including acquired source files, stored PNGs, references and controlling code/records |
| Selected source indices | 18 unique `(clip,index)` pairs: nine each from Clips 3 and 7 |
| Comparison membership | Exactly 108 unique `(target,clip,index,arm)` keys: 54 paired and 54 cross-view |
| Static surfaces | All 108 score/coverage pairs have shape 13 × 51 × 51; 3,651,804 score cells, of which 2,408,670 are finite |
| Preserved transforms | All 216 top-two static transforms agree with independent ranking across the full saved surfaces, including scale/top/left tie order |
| Masks/transforms | Both target masks and their disjointness, working validity, all 13 scaled guarded validity masks and transform parameters independently reconstructed |
| Selected-transform coverage | Static overlap agrees with mask counting; dynamic overlap independently counted; sub-85-percent dynamic coverage does not receive a score |
| Summary groups | All 24 target/clip/arm/metric groups independently reconstructed with ranked entries, null treatment and reasons |
| Near-best sensitivity sets | All 72 sets at 0.005, 0.01 and 0.02 agree; no all-invalid group occurs in this actual output |
| Paired-only shortlist | Eight unique native candidates, correctly excluding cross-view contributions |
| Material repeatability | All 112 material products byte-identical across runs, including 108 NPZs, masks, inputs, results and summary |

The verified shortlist is Clip 3 indices **71, 118, 141, 165, 188** and Clip 7
indices **0, 282, 564**. It is a computational review selection, not a visual
match verdict. The 42 null dynamic scores at best static transforms (85 among
all 216 preserved transforms) remain null, not zero or fabricated comparisons.

Each output directory contains exactly 114 expected files, with no failure
receipt. Actual totals including terminal receipts are **21,531,968 bytes**
for pilot01 and **21,531,967 bytes** for pilot02, below 268,435,456 bytes.
Receipts report **41.55241379200015** and **41.8640411660308 seconds**, below
240 seconds. Receipt contents agree after normalizing only run name and elapsed
time; `scientific_or_human_acceptance` remains false. Reported durations are
checked receipt values, not a separate external timing measurement.

## Actual verification and pins

Read-only commands were `cat`, `sed`, `rg`, `jq`, `shasum -a 256`, and two
stdout-only assertion scripts invoked with:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -
```

The full aggregate assertion call exited **0** (tool chunk `6311cc`), reporting
the counts above. It independently sorted every finite static surface using
`numpy.lexsort`, reconstructed summary rankings and sensitivity sets, calculated
native-center masks and nearest-sampled guarded validity, rehashed input/output
bytes, checked frame/PTS record joins, and verified exact run product membership.
The follow-up normalized-receipt/null-count check and hash command exited **0**
(chunk `fc1467`). Neither call reported a failure. The adapter's saved root
control receipt records 25 passing tests with no errors, failures or skips and
matching current code/test hashes; those tests were **not rerun by this reviewer**.

| File | SHA-256 |
| --- | --- |
| PROTOCOL.md | `4cf06e45c4216fa8662c90b84d4a9f78278b6704b1fcae342746cc9f4c556faa` |
| regions.json | `5bec4e5a1275f3cfaafd82fc534065ff190b3278c33bc1a5beb8f482de111694` |
| pilot.py | `b561aaae16cb1d68f1252f7ca496c6de2fe0407f79219fa096bdd437cd00cee8` |
| test_pilot.py | `cffa4d160de892439ef9e1e02ec0994d536812ae46ed6826111b7afad86522ab` |
| pilot01/verified-inputs.json | `f91ef2d693ab0835f6d30b71af1f139fefa77ae420725f0bb02c5a06dbd62fd9` |
| pilot01/masks.npz | `2f684fa174e189816cca4ca7caf71a8f6a6b9e8761f43eb64a9d9d24f5b47669` |
| pilot01/results.json | `8058581b27d454bfb8b30624e620fdaecf266aa2af7d08207531aa8c903870e3` |
| pilot01/summary.json | `4af3dae359eeba6df1ba39bd06b44e40d95c25ef084fcbc097ee1437bdbb2bc1` |

## Inferential boundary

The checker did not reconstruct image pixels, remeasure RGB hashes from decoded
images, recompute Pearson scores from historical pixels, or test visual content.
Correct sorting and identical repeats can preserve the same upstream error.
Byte hashes and source-index/PTS joins do not authenticate camera custody or
physical exposure timing. Eighteen source frames remain eighteen source frames;
the 108 comparisons, field treatments and repeated run are not independent
historical evidence. The pilot leaves **1,299 of the 1,317 indexed frames**
outside its selected sample. No whole-clip absence, exact exposure, window state,
fire magnitude, causal ranking, human acceptance or dense-execution approval
follows. Only this review file was authored; prior observations and outputs
were left unchanged.
