# Full Clip 7 post-aggregate artifact review

2026-10-04 UTC. Separate method/artifact reviewer, continuing the earlier CBS review. **Passed within the bounded artifact scope below.** This is a new execution of the supplementary checker, not an independent historical source, a new visual reading, or acceptance of a physical explanation. No image was displayed or decoded, no matcher was run, and no source, implementation, control or result was changed.

## Actual execution and preserved output

After root explicitly released the completed aggregate, the reviewer reconfirmed the checker and extraction-review hashes and confirmed that the two review outputs did not exist. From this `dense-clip7` directory, the exact command was:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B audit_artifacts.py --extraction-review-sha256 c3e2708cb6696ad85d97ab2ad7b82c83342a177f6734c3c73dc61186983fc108 --frames01-sha256 a7793e5d1f4a7faafe102029ebf99aede540021c83f292e5c9232de13622c13c --frames02-sha256 a7793e5d1f4a7faafe102029ebf99aede540021c83f292e5c9232de13622c13c
```

The invocation started after the 06:29:51 UTC clock read, terminal **66511**, initial tool chunk `8431c5`; final chunk **`4161f8`**, **exit 0**, was observed complete by 06:31:33 UTC. The process reported `status: passed`; no error or failed historical audit attempt occurred. There was no synthetic-test rerun during this execution.

Exact stdout was saved create-only with `apply_patch` as [artifact-audit.json](artifact-audit.json), then read back and compared to the complete captured stdout string: **exact equality**. Its SHA-256 is `63b8895f37d9e7b9ac2551bc5c46e19508eafab24b959e8eb9bb120c0288ffad`. This review and that stdout file are the only artifacts authored in this post-aggregate task.

## What the audit established

- Both full populations contain **3384 comparisons**, representing **1128 frames × three correlated representation arms** per pass. Every repeated frame record agrees; the nine earlier pilot frames and **27 paired pilot comparisons** reconcile.
- Every saved score/coverage surface and mask was checked. Across both passes the audit examined **228,846,384 static-score cells**, including **125,383,968 finite cells**, and independently reconstructed mask coverage and sorted the saved surfaces to check **13,536 retained transforms**. It retained **2948 null dynamic scores** at those transforms rather than converting them to zero or omitting them. Coverage comparison tolerance remains `1e-10`; inherited count-gate tolerance remains `1e-7`.
- **All 36 chunk maps** contain the independently enumerated **2349 required input identities** per chunk, including the source, paired Figure 142 reference, both extraction sets, pilot records and current controls. A complete union cannot substitute for completeness in each chunk. Conflicting resolved-path pins are refused. There were **9291 unique saved dependencies** and **9497 total audit input hashes**; each captured input retained its hash at the final check.
- All **39 historical jobs** have completed supervisor and wrapper records, matching start/end identities, declared arguments, serial predecessor pins and actual directory byte counts. The current control gate is explicitly `controls-root02`, not the incomplete earlier root run.
- Independently rebuilt global ordering, all **six metric/arm groups**, **eighteen near-best sets**, and the saved shortlist agree with the aggregate. The union is **538, 539, 540, 541, 543, 544**. These are computational candidates; this reviewer did not view them. Dynamic ranking remains at each frame's best static transform, not the best dynamic result over both retained alternatives.

## Recorded resources

Every job met the recorded 240-second ceiling and its declared byte-stop threshold. The extraction directories each contain **883,725,454 bytes**, with supervisor durations **25.260862249997444** and **25.099711541901343 seconds**. The 36 scoring jobs span **74.37439462495968–85.66057741700206 seconds** and **30,795,067–34,359,972 bytes**. Aggregation used **68.83327745902352 seconds** and **13,003,714 bytes**. The exact per-job rows are in the saved stdout.

At audit end, before saving this review/output, the lane contained **3,008,302,135 bytes** (about 2868.94 MiB), below the 3456-MiB stop; reported free space was **7,982,333,952 bytes**, above the 4096-MiB floor. These are actual observed/saved resource checks, not a hard OS quota or a reconstructed continuous trace. Root's audit rerun and direct-arithmetic results are separate executions and are not claimed here.

## Pins, prior failures and scope limits

| Reviewed artifact | SHA-256 |
| --- | --- |
| Frozen supplementary checker | `c7342eb153dcdfed1762d9d312b46a26b1e4d84f7a3eac6849a38eab0b99cfe8` |
| Frozen plan | `0404e0a819e7d8392ad3a320a4cb018ecef02c4d9d3f72337d4b3d1d131f6d70` |
| Source manifest | `ece7d7fbae14d3ec043c16eb845d74af617a06854c267b1e686e7b33d4e6e3ad` |
| Root's completed extraction review | `c3e2708cb6696ad85d97ab2ad7b82c83342a177f6734c3c73dc61186983fc108` |
| Both extraction frame manifests | `a7793e5d1f4a7faafe102029ebf99aede540021c83f292e5c9232de13622c13c` |
| Implementation review | `17b338a58697d0b2249056341cb5b2adaf7e192884df3f02b69adb8dfdbd0f9a` |
| Aggregate terminal receipt | `6625308f1cfb653540729a7342c50c5af8c58d6c9b18f75f5ae44d98e9288457` |
| Aggregate first-pass results | `0d64451b232987e457997663caeff4bcefecbc0465e1fd14d21ff63dcda212e7` |
| Aggregate repeated results | `22b35b732332f997fc772a66d5c43514a55e4503ea9360932ca014fecee86056` |
| Aggregate summary | `191e9efd672ac33f833c35acc0637272ac53f52592040f2a8adb6e9f371aa09d` |

The checker also verified the original Clip 3 refused extraction's pinned receipts/log, retained product count/bytes and continued absence of an admitted frame manifest. It did not retroactively admit that failure. The [implementation review](implementation-review.md) records the earlier 110-pass author run as earlier-code evidence, the incomplete `controls-root01` concurrency failure, and subsequent serial 111-pass author02/root02 controls. A separate read/listing during this review confirmed that root01 has no whole-suite `summary.json`; that listing returned exit 1 for the expected absent file, not an artifact-audit failure. No old result, failed run or code version was deleted or overwritten.

This checker shares the configured sampler's diagnostic/inventory parsing, the application's control gate and NumPy. It does **not** recompute Pearson correlation for every surface cell, prove every variance-based null from image pixels, or independently decode the native products. PNG byte checks and metadata are bound to root's separately completed **2256 fresh plus nine pilot PNG/RGB** check through the supplied review/frame pins. Direct retained-score arithmetic is a separate check, not silently included in this pass.

The strongest substantive objection remains: repeated geometry and stable background can correlate across different moments despite complete computation. Prior-informed masks, limited transforms, unknown published-image processing, interlacing, obscuration and multiple search opportunities remain. A deterministic pass and agreeing representation arms do not authenticate a camera original, identify an exact exposure, or quantify fire severity, temperature, window material, mechanism or intent. This is source-candidate retrieval only. The main charter, actual-human consequential-measurement gate and research-to-case/promotion boundaries remain unchanged. The evidence-audit and source-of-truth skills governed those distinctions.
