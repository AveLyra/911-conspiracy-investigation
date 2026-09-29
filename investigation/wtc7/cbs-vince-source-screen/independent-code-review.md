# Fixed CBS sample adapter: bounded code review

2026-09-28. Research-only, before this reader's historical media processing.
**No blocking adapter defect found within the reviewed contract.** Ready for
the declared preparation step, conditional on the separate source/acquisition
and input-manifest checks. This is not historical-media admission, source
authentication, visual matching or scientific acceptance.

## Scope and independence

Read completely: `PROTOCOL.md` (150 lines), `prepare_samples.py` (280),
`test_prepare_samples.py` (327), the imported
`../late-fire-sequence/sample_sequence.py` (377), its tests (197), and
`controls-parent01/test-results.json` plus
`adapter-controls-root01/test-results.json`. Current main AGENTS, WORKFLOW,
START-HERE and CHARTER hashes match the versions already read completely in
this task context. No visual reference notes, historical images or source
media were inspected; no network call or historical decode occurred.

This reader did not author the new adapter/tests, but **did author the pinned
inherited sample_sequence helper in earlier work**. This is a separate review
of the new adapter and its integration, not a wholly independent authorship
audit of the inherited executor. Root's acquisition crosscheck is separate
and was not rerun here.

## Findings

- Nine exact targets implement `p0 + j*(pL-p0)/8`, `j=0..8`. `bisect_left`
  chooses the first PTS at or after each target, including an exact equality.
  Endpoints, negative/nonzero starting PTS and one-frame clips are handled;
  all nine target rows remain, while selected indices are deduplicated and
  sorted. These are encoded-time fractions, not scene or event-time quantiles.
- Strict increasing integer PTS, positive rational time base, constant native
  geometry, selected-stream identity, SAR, pixel format and interlace fields
  are checked. Available header/read counts must equal the inventory; missing
  or `N/A` counts are not silently zero. AVI DV/yuv411p and the retained
  FFV1/bgr0 synthetic lane are explicit; unknown container/codec lanes stop
  before the frame-inventory probe.
- Input JSON rejects duplicate keys and nonfinite constants. The manifest
  requires exactly the ordered two-clip stage, valid absolute paths, lowercase
  hashes, positive integer byte counts, and distinct IDs/paths. It does not
  itself prove that local declarations correspond to the intended remote IDs;
  that is the separate acquisition/selection audit, not an implicit code pass.
- Protocol/manifest snapshots are exclusive, hashed and rechecked; helper
  imports are pinned. Source size/hash is checked before and after each probe
  and again before issuing the stage manifest. Relevant code/runtime/probe
  input pins are compared after preparation. One refused source prevents a
  complete-stage sampling manifest; successful per-source target records may
  remain and must not be mistaken for stage clearance.
- Any warning-level probe stderr byte is refused, including whitespace or
  undecodable text; nonzero and launch-failure statuses/logs are retained.
  Exceptions do not substitute an empty inventory. Existing output directories
  are refused without overwrite. Guards use explicit exceptions, not assertions
  removed by optimized Python. `prepared_not_executed` and false scientific/
  human acceptance accurately limit the output.

Important terminology: `ffprobe -show_frames` performs frame-decoding work to
produce the inventory even though this adapter does not extract/display PNGs.
Do not describe a historical preparation run as “no media decoding.” Successful
preparation also does not replace the inherited extraction diagnostic gate,
two-run product comparison, independent artifact check, or the declared visual
review. Nine samples cannot exclude an unsampled scene.

## Actual checks

`cat` read the files above; `wc -l` established read lengths;
`shasum -a 256` checked current pins. The retained parent control receipt reports
14 tests, 0 failures, 0 errors; the adapter receipt reports 25 tests, 0 failures,
0 errors. Their helper/adapter/test pins match current files. **Those two
complete suites were not rerun by this reader.**

A fresh `python3 -B - <<'PY'` stdout-only check imported the pinned adapter and
enumerated every strictly increasing sequence of length 1–6 from integers
`-4..7`. For each target it independently selected
`next(k for k,p in enumerate(pts) if 8*p >= 8*pts[0]+j*(pts[-1]-pts[0]))`,
using linear traversal and integer cross-multiplication, not the adapter's
binary search. It checked all target indices/PTS, target rational strings,
selected exact seconds, endpoint retention and deduplication. Result:
**2,509 sequences, 22,581 target checks, zero failures**. Nine invalid cases
(empty, repeated/decreasing/non-integer PTS and nonpositive/non-rational time
bases) were refused. Tool output chunk `b80850`, process exit 0. The check
created no files and invoked no media subprocess. Only this review note was
authored, with apply_patch; no implementation or control artifact changed.

## Reviewed SHA-256 pins

| Artifact | SHA-256 |
|---|---|
| Protocol | `5dbaca2b2329db7bc85f67fc0995adf5fd15b8fe3fd0c4b0e50f445179dd35bc` |
| Adapter | `5992d2a95be2dd8587a13980a7c05b363bd9760d24dc9768c345a3733049bb87` |
| Adapter tests | `484d1f391b3d4e0bf0116fa35e6f2f20bd264c0098b255a1b59dff0d27e74c55` |
| Imported helper | `c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d` |
| Imported helper tests | `cd997911f50d89d57c65906a1ac4eef3cda09ac4667a1f07307f9945068fcc43` |
| `controls-parent01/test-results.json` | `5241f8566563764c068d0060b33eb8a07d70f64dff236c6d9503e43d40ba1744` |
| `adapter-controls-root01/test-results.json` | `f8bab2e2fa7dd00f2b0d1e2b1ff7635d51f311f96d8db4bb82036ca103dc9682` |

Development-verification and evidence-falsification skills guided this bounded
review. No browser/UI validation applies. Remaining strongest limitation is
the difference between correctly selecting sparse encoded frames and correctly
identifying historical scenes; the latter remains an independent task.
