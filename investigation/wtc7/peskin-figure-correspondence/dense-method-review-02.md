# Dense safeguard review — versioned supplement

2026-09-13. **Bounded PASS** for the final inspected runner and the synthetic
checks specified below. No remaining critical issue was found in that scope.
This is an additive follow-up to [the frozen first review](dense-method-review.md),
not a replacement of its failed test, source snapshot or findings. No historical
image/media, dense/sparse result file, production frame index, source archive or
raw payload was opened by this arm; no production entry point was executed.

## Inspected changes and version boundary

[DENSE-GATES-01](DENSE-GATES-01.md) was read in full (38 lines), SHA256
`8d0c5bae4654c99813d0d896989963c2b557e80e87a160cbedc5edcebce3ebda`.
The initial hardened runner was read in full at SHA256
`7efba329b18613e8ad94ce29584b5c8349fe7e4936b4fd354d326982ab62ce93`.
The final complete **247-line** source was then read and tested at SHA256
`8c5c92932c43183d0861e16282f95e7be360a36bd9ee016c639e638ebed82bb1`.
The parent announced an intervening `299297ce…` checkpoint; this review does
not claim a separate full inspection or test of that intermediate version.

Current METHOD-01 was read in full (65 lines), including the preserved
pre-score population-variance clarification; the runner pins it to
`412c7aae4da6010d4323d900182c8419dc314fd64953ed9c2c3878b3bd335e6c`.
The original correlation boundary/wording limits remain in DENSE-01 and the
[core method review](method-review.md). Main controls, charter, development-
verification and evidence-audit boundaries remain unchanged: passing software
checks are not source authentication, physical validation or a cause finding.

| Earlier concern | Disposition in final inspected source |
|---|---|
| `pts_time:nan` passed the comparison | Explicit `math.isfinite` check now precedes numerical comparison. The old failed test passes unchanged against the new parser; positive/negative infinity also reject. |
| Per-chunk limits did not imply aggregate bounds | Four fixed primary slots cap each chunk at 275 frames, implying at most 1,100 accepted primary frames. Primary slots are 450 MiB each; four reproduction slots 10 MiB each; remaining baseline 150 MiB. Their total is 1,990 MiB, below 2 GiB. Excess fails, not truncates. In-memory size/symlink controls pass. |
| Method/control state merely recorded | Exact declaration, original-control, independent-oracle and core-comparison pins are checked before source processing; original control status/core identity also checked. |
| Prior reproduction identity/products incompletely checked | Requires completed primary receipt, same interval/source/code/declarations/tools/Python/NumPy/Pillow, expected manifest membership, file size/hash checks, bounded unique native indices and frame counts. Saved native PNG dimensions and decoded RGB are compared at the matching new stream index; every score/coverage array and result/pixel row is compared. These paths were statically reviewed, not exercised on media here. |
| Receipt shortlist could omit an image consistently from both native list and shortlist | This follow-up identified that residual internal-consistency gap. Parent added native-list uniqueness and comparison against the freshly recomputed shortlist before production; focused synthetic guard cases reject duplicates/omission and accept the correct list. |
| Decoder timer was not an overall process deadline | A process SIGALRM is installed for 300 seconds and disabled/restored in `finally`, alongside the decoder timer and child cleanup. Elapsed time is refreshed after manifest/storage checks. The declaration correctly excludes a formal guarantee for uninterruptible OS I/O. Only direct alarm-handler behavior was tested, not a real timed signal or process kill. |

The absolute ffprobe end correction is preserved. Its installed primary
documentation and tool pins are in the first review; no new media probe or
network lookup occurred. Fixed run/compare names constrain this runner's writes,
not unrelated concurrent agents. Size checks and conservative write reserves
support the declared acceptance budget but do not certify every operating-system
failure mode, arbitrary concurrent writer or hard peak-memory limit.

## Versioned synthetic tests

New [fixture](fixtures/dense_controls02.py), SHA256
`d0b2af1d280392970e98095bc7d6d6d0e2c001b929210e3cf17218b95c3a2bde`,
pins the final runner and imports the unchanged previous fixture solely to reuse
its 22 tests. It never invokes either fixture's historical/production entry
point. The runner's `main` is not called.

The [new receipt](fixtures/dense-controls02.json), SHA256
`87fabd4499058c4f237e17387539669eb56fd545543a0d08dea1fec75df2a168`,
records **63/63 passing checks**, including:

- All 22 prior parser/shortlist/100-prefix-retention checks, with the previous
  NaN failure now rejected; additional infinity cases.
- In-memory storage at exact slot/baseline limits; one-byte excesses for primary,
  reproduction and baseline; undeclared-slot data counted as baseline; symlink
  rejection; and the 1,990 MiB ceiling arithmetic.
- All eight permitted run slots, wrong chunk/compare/path names, each changed
  pinned dependency, unchanged pin and failed-control rejection.
- Full/partial frame and 275-index cap conditions, failed prior status, wrong
  prior interval, missing manifest member/path escape, duplicate native indices,
  omitted recomputed shortlist, correct shortlist and alarm exception.

For checks embedded in `main`, the fixture selects a unique inspected AST
`If` statement whose direct body raises the specified `ValueError`, then executes
**only that guard** over explicit synthetic values. This checks those conditions,
not all surrounding control flow or an end-to-end run. Storage uses fake files
and sizes in memory; it does not census the actual unit or open source files.
The alarm test calls the handler directly and expects `TimeoutError`; it does
not install/fire a real alarm. These distinctions prevent a mocked guard test
from being described as successful real decoding or timeout handling.

Actual executable:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Working directory: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
Actual arguments:

```text
-B research/sherlock-wtc7-investigation/peskin-figure-correspondence/fixtures/dense_controls02.py --output research/sherlock-wtc7-investigation/peskin-figure-correspondence/fixtures/dense-controls02.json
```

The create-only receipt save used scoped worktree permission and completed with
exit 0. The first follow-up fixture run passed; no failed follow-up run or
unrecorded scientific correction is claimed.

## Independent replay and retained history

Parent reported reading the complete new fixture and independently running it.
Its [replay receipt](fixtures/dense-controls-root02.json), SHA256
`78bbfef5668c8b9bb206d3168c57d2266286a4322f163f2535e8bfa7f95df5b4`,
was compared directly here. The entire JSON matches after deleting `argv`;
inspection of both argument arrays shows the **only difference is the requested
output filename**. Both receipts therefore contain the same 63 results and pins,
not merely matching summary counts. This is a separate execution of the same
fixture/subject, not a second independently implemented decoder.

The first fixture and failed receipt remain unchanged at
`ccdd76b0554b32162d576ec285648f71d054ac5bd775fae081f0b2d1db4d3b0a`
and `140345f4703bfe08e7693caddcabae55b050bc986a4aaa4b516fca0085322a3b`,
respectively. No prior review, fixture, runner, main source or STATUS was edited.

## Acceptance ceiling and stop

The code contains concrete gates for actual RGB/showinfo/probe association,
source-anchor pixels, complete interval coverage, score/PNG reproduction,
decoded-image checks, storage and process cleanup. Their real outcomes must be
established by the run receipts and separate result review; this synthetic pass
does not supply them. Foreground/background alignment, unique frame identity,
historical clocks, exposure cadence, thermal fields and physical consequences
remain outside scope. No package installation, browser, media/production
execution, source acquisition, transmission, solver or canonical change.
This bounded review stops here.
