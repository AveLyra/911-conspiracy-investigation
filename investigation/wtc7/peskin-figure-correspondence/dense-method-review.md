# Independent dense-pass safety and bookkeeping review

2026-09-13. Static source review plus synthetic text/selection tests only. No
historical media, dense/sparse candidate-result files, archive or source frame
index was opened, and no production entry point was executed. The declaration
itself includes the already reported sparse-screen synopsis; reading it is not
an independent inspection of those results. This arm owns this note and the
synthetic fixtures only; it did not alter either producer.

## Reviewed versions and actual scope

- [DENSE-01](DENSE-01.md): all 53 lines, read SHA256
  `8a7ac08aa7901c0de5956b617950f9fda35a786b7a9b58a26c7ba54c785413f8`.
- `dense_match.py`: all 175 lines at initial SHA256
  `93da7a1bb47c29420228c998331183d5ac090353169725b096b6770cf8cec712`;
  all 175 lines again at SHA256
  `4d8afe6485f37b6bf2b5dd531f6b30664f019d90f68fdd1cf3c96943be527c86`
  after the parent changed the ffprobe interval end.
- The second version is preserved as [tested subject snapshot](fixtures/dense-subject01.py),
  with that same hash. It is not a replacement current producer or a run script
  to execute against historical data.
- Earlier [core method review](method-review.md) supplies the independent
  Pearson/linear-correlation tests. Those do not verify dense decoding or image
  matching. Current main controls, charter and applicable development/evidence
  skills retain that boundary.

Importing the reviewed module defines functions/constants and imports the
already reviewed core; it does not run `main`. The synthetic harness called only
`parse_showinfo` and `get_shortlist`. No source hash check, decoder, ffprobe media
read, target reader, canvas registration or historical comparison was invoked.

## Concrete findings before production acceptance

| Finding in the tested version | Consequence and required disposition |
|---|---|
| `parse_showinfo` accepts displayed `pts_time:nan` | A malformed nonfinite display value escapes `abs(actual-shown) > .01`. Explicitly reject nonfinite displayed times, then replay the preserved synthetic suite. Integer PTS remain parsed, but the claimed display-consistency check otherwise has a real hole. This is not a finding that historical logs contain NaN. |
| Initial ffprobe used `{start-2}%+12`; tested revision uses `{start-2}%{end+1}` | The correction avoids defining the end relative to an earlier keyframe actually reached. Installed documentation supports the distinction. Still require exact filtered probe/showinfo list equality and anchor-pixel agreement; an absolute probe end alone does not demonstrate complete decode coverage. |
| Core/control hashes are gated, while METHOD-01 is not pinned in the dense receipt; DENSE/PROTOCOL hashes are recorded but not compared with approved expected hashes | Retain and check the actual agreed declarations/approval checkpoint before historical acceptance. Recording whichever bytes happen to exist is not an unchanged-method gate. The earlier independent comparison is not automatically applied to arbitrary later code. |
| Per-chunk frame/storage checks do not enforce the combined 1,100-frame or whole-unit 2 GiB limits | A coordinator or added aggregate gate must account for all four chunks and existing/new derivatives, including failures and comparison runs. Four independent 550-frame caps do not logically imply 1,100 combined. A completed unit must not claim an aggregate limit was enforced by this version alone. |
| `--compare-to` reads old surfaces/rows without first requiring a successful, same-chunk/core/protocol receipt; it does not decode/check the saved shortlisted PNGs | Exact surfaces, candidate rows and fresh raw-pixel digests are useful reproduction tests, but not proof that the prior accepted run or saved native PNG products were verified. Require prior-run identity/status and actual selected-image pixel checks, or narrow the reproduction claim explicitly. |
| FFmpeg is timer-killed at approximately 270 seconds, loop checks 275 seconds, and final elapsed-time acceptance checks 300 seconds | These are useful guards, but setup, post-decode probe and final hashing do not have a single interrupt enforcing the entire invocation budget. A final rejected run can already exceed 300 seconds. Either add an overall bounded watchdog or accurately report this as eventual acceptance checking rather than a guaranteed wall-time ceiling. |

All findings were promptly sent to the parent. This preliminary disposition
does **not** certify a later edited producer; any correction needs an identified
version and change-specific review or test. Aggregate acceptance and historical
results remain the parent's responsibility.

## Positive static findings and remaining limitations

The read loop demands a full `1620*1080*3` byte frame and rejects partial data
or a 551st frame. This was code inspection, not a synthetic subprocess/pipe
test. After decoding, showinfo count must equal raw-frame count; parsed filter
indices are consecutive, dimensions/timebase checked, PTS strictly increasing,
and every PTS inside the half-open declared interval. The probe sequence is
filtered to that same interval and compared exactly. Existing anchor images
are checked by decoded RGB bytes rather than by equating container hashes with
pixel hashes. These are concrete association safeguards, not authenticated
camera clocks or independent decoder-family validation.

`finally` cancels the child timer and kills/reaps a still-running FFmpeg process.
Exceptional pipe-closing and termination paths were inspected but not exercised
with real or synthetic media. FFmpeg and ffprobe failures are retained in the
new run directory; a run cannot pass merely because it created `start.json`.
Run names have a restricted alphabet and output directories are create-only.
NPZ reads use `allow_pickle=False`. Main paths are read-only dependencies.

The shortlist uses the first (best-static) geometry candidate's dynamic score;
it does not choose a second geometry to improve dynamic ranking. Ties use
ascending frame index. Four static and four dynamic choices per each of two
targets imply at most 16 unique frame indices. With fixed per-frame scores,
an old frame outside every prefix top-four cannot reenter when more candidates
are added. Thus retaining a frame when it first qualifies, then discarding it
only after loss of shortlist membership, is sufficient. Synthetic tests below
check that actual implementation, not merely the proof idea.

The per-chunk size gate is periodic (every 80 frames and near completion), so it
can detect an excess after a write rather than prevent every transient excess.
Diagnostics and final receipts also occupy storage. No hard peak-memory limit
or global accounting is certified by this review. Malformed/nonfinite synthetic
score dictionaries outside the core producer's established output domain were
not treated as admitted historical candidate records.

## Synthetic controls and reproducibility

[Fixture source](fixtures/dense_controls01.py), SHA256
`ccdd76b0554b32162d576ec285648f71d054ac5bd775fae081f0b2d1db4d3b0a`,
pins the tested producer before import. The [create-only receipt](fixtures/dense-controls01.json),
SHA256 `140345f4703bfe08e7693caddcabae55b050bc986a4aaa4b516fca0085322a3b`,
records **21/22 checks passing**, with only `nonfinite_shown_time` failing.

Passing parser checks: correct index/PTS identity; short and extra showinfo
lists; duplicate/decreasing PTS; nonsequential filter index; below-start and
exact-end exclusion; wrong dimensions; missing PTS/timebase; wrong timebase;
and ordinary displayed-time mismatch. These are synthetic strings, not actual
FFmpeg output generated from a media fixture.

Passing selection checks: deterministic tie ordering, static/dynamic union,
both-target 16-frame bound, same-frame deduplication across targets, empty
candidate and unselected-target behavior, and exclusion of runner-up geometry
from dynamic reranking. A deterministic 100-prefix sequence (seed 14092026)
retains exactly the freshly recomputed shortlist at every prefix; maximum
retained count is 15 in that random fixture. The separate constructed test
reaches 16. Prefixes are algorithmic tests, not independent video observations.

Actual executable:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Working directory: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
Actual arguments:

```text
-B research/sherlock-wtc7-investigation/peskin-figure-correspondence/fixtures/dense_controls01.py --output research/sherlock-wtc7-investigation/peskin-figure-correspondence/fixtures/dense-controls01.json
```

The invocation used scoped permission solely to save its own fixture receipt,
returned exit 1 for the real parser-control failure, and read no media. The
failure is not recast as a passing run or a historical decode failure.

## Installed interval documentation

Installed ffprobe is version 7.1.1. Full executable help was inspected for
`-read_intervals` and FFmpeg's seek/copy-timestamp/duration flags; its brief help
alone does not explain keyframe-relative interval duration. The local primary
[ffprobe man page](/opt/homebrew/share/man/man1/ffprobe.1), lines 913–976, does:
an absolute end and a relative duration are different; when duration is used,
the actual seek point rather than requested start determines the computed end.
No network documentation request occurred.

- Man-page SHA256: `2a89764d12e2c4d1a5679454e2d7d8e3a3bcd6cc48c7452d5795e60559ae0f4b`.
- `/opt/homebrew/bin/ffprobe`: `fd670257233c93c88608a62ed8b5ddeeb812bd341dfb39bbe0e1c654b91672ad`.
- `/opt/homebrew/bin/ffmpeg`: `7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569`.

These identify installed documentation/tools, not a historical video pipeline.
No package installation, runtime/global edit, source acquisition, solver,
historical candidate finding, external transmission or canonical change.
