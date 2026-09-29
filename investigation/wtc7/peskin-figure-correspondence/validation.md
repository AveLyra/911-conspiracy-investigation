# Verification record and reproducibility boundary

Research-only, September 13, 2026. All listed calculations used the bundled
Python 3.12.14, NumPy 2.3.5 and Pillow 12.3.0; media tools are the locally
installed FFmpeg/ffprobe 7.1.1. Full environment, commands, source/tool hashes
and frame-level data are retained in the run receipts. These checks are not
historical authentication, physical validation or a licensed expert report.

## Frozen methods and code

- Mathematical core `match_screen.py`:
  `06a400fbb378dfa710dd86799792f8f615a40eea19e82c23b9f3e0592a3b64a8`.
- First completed dense runner, preserved exactly as `dense_match01.py`:
  `8c5c92932c43183d0861e16282f95e7be360a36bd9ee016c639e638ebed82bb1`.
- Continuation `dense_match.py`:
  `b76788bf65e74fa464c060ee0a5831aba27eb864f6139f2c6c2f5a604bf2ce59`.
- Independent result checker:
  `3f4a8d5547e387ec3dbfd72a8425a477269c2884195598ef0b3f6320eac93455`.

The original [protocol](PROTOCOL.md), [method](METHOD-01.md),
[dense declaration](DENSE-01.md), [safeguards](DENSE-GATES-01.md),
[decoder continuation](DENSE-CONTINUATION-02.md) and
[regional-review declaration](CANDIDATE-REVIEW-01.md) retain their sequence.
No mathematical score was tuned after the historical dense results.

## Controls, failures and reviews

The core passed 11 synthetic controls. The independent direct-summation
comparison passed 73 checks covering 71 surfaces / 1,593 offsets, including
492 admissible scores, within its stated tolerances; see
[method review](method-review.md). Its earlier roundoff-sensitive fixture
failure remains preserved, not reclassified as a producer failure.

The first dense parser/control suite passed 21/22: a displayed NaN escaped its
consistency check. The failed fixture, receipt and tested source snapshot are
preserved. Versioned corrections passed 63/63 synthetic checks, and the later
decoder-continuation gate suite passed 100/100. Root independently replayed
both suites into separate receipts; their substantive contents agree. The
reviews preserve actual test scope: [initial](dense-method-review.md),
[corrected](dense-method-review-02.md), [continuation](dense-method-review-03.md).
Isolated guard/handler tests are not end-to-end process-kill or media tests.

Historical `dense01` failed probe/filter PTS equality after 215 frames, missing
a final 25-frame suffix. It and all partial NPZs remain intact. The fresh
continuation changes the read allowance, not the selected interval. Accepted
aggregation excludes that failed run. No decoder warnings were accepted.

## Actual complete coverage and same-code reproduction

| Primary / reproduction | Frames | First / last source PTS (1/1000) | Exact surface pairs | Exact saved-native pixel matches |
|---|---:|---|---:|---:|
| dense00 / repro00 | 240 | 2502013 / 2509989 | 480 | 16 |
| dense11 / repro11 | 240 | 2510022 / 2517996 | 480 | 15 |
| dense12 / repro12 | 239 | 2518029 / 2525971 | 478 | 12 |
| dense13 / repro13 | 240 | 2526004 / 2533979 | 480 | 16 |
| Total | 959 | Complete declared [2502,2534) selection | 1918 | 59 |

Each reproduction uses its primary's exact runner bytes, checks the completed
prior receipt and output manifest, compares every score/coverage NPZ array
with equal NaN placement, and compares complete frame/result records. Each
saved native PNG is hash-checked and decoded against the fresh RGB stream at
its selected index. Every primary/reproduction also matches the exact filtered
ffprobe PTS list and all eight existing one-second source-anchor pixel hashes.
Thus there are 32 anchor matches in each complete four-chunk pass, not 32
independent historical sources. FFmpeg and ffprobe share a decoder family.

All eight accepted invocations completed in under 162 seconds each, below the
300-second cap. There are 59 newly saved full native PNGs, below 64; reproduction
adds none. The unit including preserved failures and derivatives was about
400 MB at closeout, below 2 GiB; the final verification receipt records the
exact pre-receipt total. This is disk usage, not a measured peak-memory bound.

## Summaries and independently checked regional arithmetic

[Primary summary](primary-summary.json):
`c34061bdc218dfd9c818766066ed5aecc636a39f815ef1340ca57dae769327b3`.
[Reproduction-qualified summary](reproduced-summary.json):
`68b89297bb6acebe9d2cc05fd87d81eb439610fe22fbe60189e58d6933ddcc4d`.
Their complete scientific result dictionaries match exactly; the latter adds
all four reproduction receipts. The summarizer's three small island controls
pass. Empty metrics now return explicit empty candidate/band sets after a
pre-result code review identified the earlier unguarded first-element access.

[Regional run 1](regions01.json) and [run 2](regions02.json) are byte-identical:
`9e9639e15ea1385ae7aa09bfb206f6b333cb68939fa526bd04448a9682936868`.
Seven T148 and five T149 candidate-target pairs produce all 86 declared regional
diagnostics; none is null. Overlay exclusions and four-pixel resampling guards
remain explicit, with geometry held at the original foreground fit.

The [independent checker/review](independent-result-review.md) passed 24 controls
before reading results and then reconstructed all rankings/disconnected bands,
frame/target/PTS joins, masks, counts and fixed-image regional scores. Maximum
absolute Pearson difference: 1.4432899320127035e-15, against the predeclared
1e-12 tolerance; coverage/counts agree exactly. Root read the complete checker
and replayed it successfully. Its [root receipt](independent-result-root01.json)
agrees with the independent receipt except the output filename in argv.
The shared Pillow rasterizer and attributed region definitions are not an
independent camera, independently selected geometry or independently recomputed
FFT search. Pillow's getdata deprecation warning was retained as a runtime
notice, not mistaken for a media-decode failure or silently fixed mid-analysis.

## Actual visual coverage and disclosure

The [dense visual note](dense-candidate-review.md) records all 12 global native
candidates and both complete targets, with each selected file's byte/hash
identity checked before and after viewing. No new images were generated by
that reviewer. The reviewer saw targets and five candidates before receiving
root's score-aware leader identities and interpretation, but had not frozen
any qualitative checkpoint. Seven remaining candidates were seen afterward.
Numeric dense scores and regional results were not read before the note was
frozen. This is not a wholly rank-blind interpretation or an independent source.

Root's separate post-score views cover the two full leaders and both targets;
earlier full-page/target and three one-second candidate familiarity is disclosed
in the report. The numerical pass is not a claim that every frame was visually
inspected. Exact native-pixel reproduction and visual interpretation are
different checks. Neighboring-frame ambiguity remains despite high scores.

## Final artifact-integrity check

`verify_artifacts.py` checks Python syntax, JSON readability, Markdown local
links/whitespace, accepted output-manifest membership/size/hash, primary and
reproduction recipe identities, exact saved result rows, aggregate summary
agreement, regional repeat bytes and independent-checker replay agreement.
Its create-only `verification01.json` records actual counts, the final Markdown
size/hash pins and exact unit bytes before that receipt. Reopening those pins
and a separate scoped git whitespace check complete the document closeout.
These are integrity checks, not fresh physical calculations, source-clock
authentication, a new production rehash or disclosure clearance.

## Replay order and preservation

The recorded commands use the bundled Python executable with `-B`, the unit's
relative script path, and create-only output names. The sequence was controls,
screen01, dense00/dense01, preserved first-runner repro00, continuation
dense11/dense12/dense13, and matching repro11/repro12/repro13. For example:

```text
dense_match01.py --chunk 0 --run repro00 --compare-to dense00
dense_match.py --chunk 1 --run dense11
dense_match.py --chunk 1 --run repro11 --compare-to dense11
summarize_dense.py --require-reproduction --output reproduced-summary.json
check_regions.py --summary primary-summary.json --output regions02.json
```

Arguments in receipts identify the actual working-directory-relative paths;
the examples above omit that repeated directory prefix. Existing run names
must not be reused or overwritten. A fresh full replay requires a separately
declared clean output context containing the same frozen dependencies, running
the original first-chunk reproduction before populating continuation outputs
so the original runner's baseline budget remains valid. Do not loosen frozen
guards merely to overwrite old results.

Original sources, legal records and prior research remain intact. Research is
uncommitted in the dedicated worktree; no acquisition, transmission, solver,
bridge, canonical promotion, merge, commit or push occurred. Remaining exposure,
clock, photometric and physical limitations are substantive, not erased by
passing software tests.
