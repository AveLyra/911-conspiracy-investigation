# Independent scene arithmetic review

## Method frozen before reading root implementation or scores

2026-09-19. This reviewer has read the main repository controls, investigation
charter, unit protocol and scene addendum, plus the two source-image manifests.
No historical image has been displayed, annotated or decoded by this reviewer.
The root implementation and numerical results have not been read at this freeze.

Coverage is **all 67,296 comparisons**: 701 Camera2 candidates × 8 Tilted queries
× 3 Pillow resampling branches × 4 masks, for both MAE and correlation. There
is no adaptively selected correlation subset. The independent implementation
will build coordinates by testing all global grid points (x,y) with x and y
multiples of four against each stated half-open rectangle. It will read the
native L-mode PNGs, verify their file and luma hashes, and resize only query
width 720→640 using Pillow NEAREST, BILINEAR and BOX, height fixed at 480.

For each paired vector x,y of n unsigned luma samples, convert before subtraction.
The exact MAE numerator is `sum(abs(int(x_i)-int(y_i)))`, accumulated as int64;
MAE is that integer divided by n. Correlation uses the independent integer
sum/product identity:

`(n*sum(x*y)-sum(x)*sum(y)) / sqrt((n*sum(x*x)-sum(x)^2)*(n*sum(y*y)-sum(y)^2))`.

The integer variance/covariance terms must stay within int64; multiply the two
variance terms as Python integers before square root. Any zero variance returns
null. Full-scene rankings use exact MAE numerators then ascending source index;
report all exact first-place ties, runner-up, gap, boundary minima and selected
sequence monotonicity. Region-specific order/rank comparison is also complete.
Declared float comparison bounds against root: absolute MAE error ≤1e-12,
absolute correlation error ≤1e-12. These bounds compare implementations and
do not quantify observation uncertainty or source authenticity.

Before reading historical pixels, run synthetic exact-copy, positive/negative
brightness, localized-content, constant-image, repeated-tie, uint8-subtraction,
global-grid membership and width-only resize controls. Resize remains a shared
Pillow/API dependency, not an independent implementation of filter kernels.

Pin the exact manifest/protocol hashes below and halt if any varies; recheck
them after the run. Preserve all checked image hashes/PTS and complete arrays.
Compare root results only after this independent method and controls are frozen.
Repeat from source inputs with the same pins; root output files will likewise
be pinned before comparison rather than silently reloaded during a run.

- PROTOCOL.md: `0bec10bef245cf59d62800dce2c67913da62b90cbb8b42a42d9d9ce2555614e1`
- SCENE-ADDENDUM.md: `f54b1eac8df8d069806ba60df36865ce0dcda2c52f163963e28b6059e5d3777d`
- candidates01/selection.json: `360d4646eb9318da7dd741f3c6be4d57c6c7c6879313514c98826257c7f89552`
- views01/receipt.json: `4570095ea9c35fac86302f2443969a87261130175edb0de1b7eafa4eefefad29`

## Results

The first controls-only invocation failed before any historical pixels were
loaded. Its hard-coded expected sum for [5,5,5,5] versus [0,1,4,7] was 14;
both independent arithmetic paths returned the correct value 12 (=5+4+1+2).
That fixture typo was corrected without changing a scoring formula or scope.
The failing invocation is preserved here rather than represented as a pass.

Both complete historical runs succeeded and produced byte-identical outputs:
`scene-independent01.json` and `scene-independent02.json`, SHA-256
`280f247c7561e1625361daab9e1f4c6ea0f9b066c034d9ea7d7cd59fea8c3dd7`.
Their unchanged independent producer is SHA-256
`4f2deeec53d768de631405f10b0d12abecde3011dc8b21785d8c93f7f0d953f4`.
Runtime: Python 3.12.14, Pillow 12.3.0, NumPy 2.3.5, using
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
All 709 PNG files were checked against both file-byte and native-luma hashes;
all four manifest/protocol pins were checked before and after each run.
The complete source-image records, including all PTS and hashes, are retained
in both independent outputs. Source file metadata did not vary.

The full source-media byte hashes were also rechecked, without video decoding:

- Camera2 MOV: `84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730`.
- Tilted MP4: `393d76f986d0771c5ec38352bf29470a81a3c685bb8a1c7ea565ceefa334843f`.

All **67,296 MAEs exactly equal the root's stored floating values**, with zero
absolute difference; each root MAE also recovers the independent integer sum
by multiplying by the mask count and rounding. This is a check against exact
integer sums divided by counts, not a claim that a non-dyadic rational has an
exact binary representation. All **67,296 correlations** agree within the
predeclared 1e-12 absolute bound. Maximum difference is
`4.591882429849647e-13`, at query 475, NEAREST, full mask, candidate 6581:
independent 0.8533258305805517 versus root 0.8533258305800925.
There are no undefined historical correlations; both-constant and one-constant
null behavior passed the separate controls.

All **96 entire 701-candidate rank arrays** agree, including 3,303 adjacent
equal-score positions across all region arrays. This count is not 3,303 unique
frames or first-place ties. All 24 full-scene reported selections, complete
minimum-tie lists, runner-up indices/scores, gaps, boundary flags and selected
source PTS/time fields agree with both root scores and summary. No full-scene
minimum is tied or at candidate 6500/7200. All three selected index sequences
are strictly increasing:

| Query | NEAREST / BOX | BILINEAR |
|---|---:|---:|
| 0 | 6613 | 6613 |
| 67 | 6681 | 6681 |
| 135 | 6749 | 6748 |
| 203 | 6817 | 6817 |
| 271 | 6884 | 6884 |
| 339 | 6952 | 6952 |
| 407 | 7020 | 7020 |
| 475 | 7088 | 7088 |

Minimum full-scene MAEs range from 1.1516667 to 1.4373810 native luma units.
Runner-up gaps range from 0.0130357 to 0.3406548; every runner-up is one source
index away. Query 135 under BILINEAR changes the selected source frame from
6749 to 6748, with the smallest gap. These are measured diagnostic distances,
not confidence intervals or probabilities of unique exposure identity.
Region selections also differ: the right-background mask selects 6749 for
query 135 under BILINEAR, and 7089 for query 475 under NEAREST/BOX. It would be
incorrect to claim exact agreement of every region or preprocessing branch.

**Shared-dependency issue:** NEAREST and BOX produce different full resized
luma hashes on all eight queries, yet every retained region's entire score,
integer-sum and ranking result is identical. An added, explicitly post-scoring
synthetic diagnostic using a 720-column ramp finds 38,400 differing full-image
pixels between those two filters but zero on the fixed every-fourth-pixel grid.
Thus the present sample can erase filter differences; NEAREST/BOX agreement
does not count as independent corroboration or two distinct robustness results.
Pillow is shared with root, and no independent BOX/BILINEAR kernel was implemented.
The native L-mode PNG and resize APIs are dependencies; native encoding and
physical calibration are outside this arithmetic check.

**Claim ledger and strongest objection.** (A) The declared source-content
arithmetic is reproduced on every planned comparison, supported by byte-pinned
inputs, exact sum identities and repeated outputs. An altered pin or any score
outside tolerance would falsify that result. (B) Closely corresponding image
content is consistent with common footage, but this reviewer contributes no
independent visual authentication. (E, unsupported by this check) Unique native
camera/exposure identity, an unedited clock, saved-project linkage to a paper,
physical calibration, onset/acceleration or collapse mechanism. A resampled or
otherwise edited derivative of the same footage is a strong competing account
of numerical similarity, and the one-frame branch sensitivity limits exact
frame identity. This reviewer did no image display/annotation, video decode,
motion fit, table join, causal ranking, external disclosure or legal promotion.

**Actual commands and outcomes.** The controls-only command below first failed
on the documented expected-fixture typo, then passed all 12 controls. The first
historical invocation completed arithmetic but could not create its output
under the default filesystem sandbox; no output was written. It was rerun with
the authorized worktree write escalation, and both output commands exited zero.
The root comparison block below exits zero with the coverage/error totals above.
Root output/receipt hashes are rechecked at the end of that comparison. The
first adapter's uppercase-key failure is preserved below. No passing result is
attributed to a failed invocation.

```sh
PYTHON=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
UNIT=research/sherlock-wtc7-investigation/tilted-camera-source-join
"$PYTHON" -B "$UNIT/scene-independent-check.py" --controls-only
"$PYTHON" -B "$UNIT/scene-independent-check.py" --output "$UNIT/scene-independent01.json"
"$PYTHON" -B "$UNIT/scene-independent-check.py" --output "$UNIT/scene-independent02.json"
```

The output commands intentionally use exclusive creation and refuse to replace
existing results. Reproduction elsewhere requires a copied unit with the two
output names absent and all pinned dependencies retained.

## Reproducible root-output comparison

This adapter was written only after independent scoring code and synthetic
controls were frozen, and both historical calculations had finished. It maps
the root's lowercase branch and longer region labels without changing any
independent score. The first adapter invocation stopped on `KeyError` because
it used uppercase branch keys; no numerical comparison pass was claimed.

Run the following Python block from this worktree's repository root after the
two independent outputs exist. It reads and pins outputs, checks every score
and entire ranking array, and produces a compact result; it writes no files.

<!-- BEGIN COMPARISON CODE -->
```python
import pathlib, json, hashlib, math
p = pathlib.Path('research/sherlock-wtc7-investigation/tilted-camera-source-join')
pins = {
    'scene01/scores.json': 'f9dda2fe913ccf39c2caf4794812c7c7fee388f53f0bb0c55c50a808212cdc17',
    'scene01/summary.json': '3226887dc47bf4f187c0dd593ab1f816a41a8b4fe5900186e20ba3b744f16c70',
    'scene01/receipt.json': '4f882a621f827ab798a2cb1070e17d2a273bfe6621ccbf5ad93f7ee6a2ebcf54',
    'scene-independent01.json': '280f247c7561e1625361daab9e1f4c6ea0f9b066c034d9ea7d7cd59fea8c3dd7',
    'scene-independent02.json': '280f247c7561e1625361daab9e1f4c6ea0f9b066c034d9ea7d7cd59fea8c3dd7',
}
def load(name):
    b = (p/name).read_bytes()
    assert hashlib.sha256(b).hexdigest() == pins[name], name
    return json.loads(b)
a = load('scene-independent01.json')
assert a == load('scene-independent02.json')
r = load('scene01/scores.json')
s = load('scene01/summary.json')
receipt = load('scene01/receipt.json')
assert a['candidate_indices'] == r['candidate_indices']
indices = a['candidate_indices']
for name, h in a['source_pins'].items():
    assert receipt['inputs'][name] == h
    assert hashlib.sha256((p/name).read_bytes()).hexdigest() == h
for row in a['source_candidates']:
    assert receipt['inputs']['candidates01/'+row['png']] == row['png_identity']['sha256']
for row in a['source_queries']:
    assert receipt['inputs']['views01/'+row['png']] == row['sha256']
region_map = {'full': 'full', 'left': 'left_foreground',
              'right': 'right_background', 'target': 'target_smoke'}
root = {(row['query_index'], row['branch'].upper()): row for row in r['results']}
summary = {(row['query_index'], row['branch'].upper()): row for row in s['selections']}
assert len(root) == len(summary) == len(a['scores']) == 24
mae_err = corr_err = 0.0
exact_mae = checked_mae = checked_corr = null_corr = rank_arrays = tied_ranks = 0
rows = []
for row in a['scores']:
    key = (row['query_index'], row['branch'])
    rr, ss = root[key], summary[key]
    for k, other in region_map.items():
        x, y = row['regions'][k], rr['regions'][other]
        assert x['n'] == y['pixels'] == a['regions'][k]['count']
        assert a['regions'][k]['rectangle'] == r['regions_half_open'][other]
        assert len(x['mae']) == len(y['mae']) == len(x['correlation']) == len(y['correlation']) == 701
        for numerator, independent, published in zip(x['mae_numerator'], x['mae'], y['mae']):
            assert independent == numerator/x['n']
            err = abs(independent-published)
            mae_err = max(mae_err, err)
            assert err <= 1e-12 and round(published*x['n']) == numerator
            exact_mae += independent == published
            checked_mae += 1
        for independent, published in zip(x['correlation'], y['correlation']):
            assert (independent is None) == (published is None)
            if independent is None:
                null_corr += 1
            else:
                assert math.isfinite(independent) and math.isfinite(published)
                err = abs(independent-published)
                corr_err = max(corr_err, err)
                assert err <= 1e-12
            checked_corr += 1
        order = sorted(range(701), key=lambda i: (y['mae'][i], indices[i]))
        assert [indices[i] for i in order] == x['ranking']['order']
        rank_arrays += 1
        tied_ranks += sum(y['mae'][order[i]] == y['mae'][order[i-1]] for i in range(1, 701))
    x = row['regions']['full']
    rank, published = x['ranking'], rr['selected']
    exact_fields = {'candidate_index': 'minimum_index', 'exact_minimum_ties': 'minimum_ties',
                    'runner_up_index': 'runner_up_index', 'at_candidate_boundary': 'boundary_minimum'}
    for fk, ik in exact_fields.items():
        assert published[fk] == ss[fk] == rank[ik], (key, fk)
    for fk, expect in [('mae', rank['minimum_numerator']/x['n']),
                       ('runner_up_mae', rank['runner_up_numerator']/x['n']),
                       ('gap', rank['gap_numerator']/x['n'])]:
        assert abs(published[fk]-expect) <= 1e-12 and abs(ss[fk]-expect) <= 1e-12, (key, fk)
    candidate = a['source_candidates'][indices.index(rank['minimum_index'])]
    for fk, ik in [('candidate_pts', 'source_pts'),
                   ('candidate_time_seconds_exact', 'source_time_seconds_exact')]:
        assert str(published[fk]) == str(ss[fk]) == candidate[ik], (key, fk)
    rows.append({'query': key[0], 'branch': key[1], 'selected': rank['minimum_index'],
                 'runner_up': rank['runner_up_index'], 'mae': rank['minimum_numerator']/x['n'],
                 'gap': rank['gap_numerator']/x['n'], 'ties': rank['minimum_ties'],
                 'boundary': rank['boundary_minimum']})
assert checked_mae == checked_corr == s['comparisons'] == 67296
assert s['visual_candidate_union'] == sorted({row['selected'] for row in rows})
for name in pins:
    load(name)
print(json.dumps({'mae_checked': checked_mae, 'mae_exact_float_equal': exact_mae,
                  'maximum_mae_error': mae_err, 'correlations_checked': checked_corr,
                  'maximum_correlation_error': corr_err, 'null_historical_correlations': null_corr,
                  'full_rank_arrays_checked': rank_arrays, 'adjacent_exact_tied_ranks_all_regions': tied_ranks,
                  'selected_rows_checked': 24, 'verified_input_png_hashes': 709,
                  'input_and_root_files_rechecked': True, 'rows': rows}, indent=2, sort_keys=True))

# Post-scoring branch redundancy diagnostic, not a new historical selection.
import numpy as np
from PIL import Image
own = {(row['query_index'], row['branch']): row for row in a['scores']}
for query in (0, 67, 135, 203, 271, 339, 407, 475):
    assert own[query, 'NEAREST']['resized_luma_sha256'] != own[query, 'BOX']['resized_luma_sha256']
    assert own[query, 'NEAREST']['regions'] == own[query, 'BOX']['regions']
ramp = np.tile(np.arange(720, dtype=np.uint16) % 256, (480, 1)).astype(np.uint8)
nearest = np.asarray(Image.fromarray(ramp).resize((640, 480), Image.Resampling.NEAREST))
box = np.asarray(Image.fromarray(ramp).resize((640, 480), Image.Resampling.BOX))
assert np.count_nonzero(nearest != box) == 38400
assert np.count_nonzero(nearest[::4, ::4] != box[::4, ::4]) == 0
print('Post-scoring synthetic branch redundancy diagnostic passed.')
```
<!-- END COMPARISON CODE -->
