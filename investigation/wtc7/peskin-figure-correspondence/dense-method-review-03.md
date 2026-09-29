# Dense continuation — bounded code and synthetic review

2026-09-13. **Bounded PASS:** no critical issue found in the scoped continuation
change, with 100/100 synthetic checks passing. This does not certify historical
extraction completeness, frame identity, physical interpretation or cause.
The earlier failed extraction and all earlier code/test artifacts are preserved;
this arm did not open media, production results or failure payloads, or execute
either historical runner's `main`.

## Actual coverage and version pins

Read current main AGENTS, WORKFLOW, START-HERE and investigation CHARTER; applied
development-verification, evidence-falsification-auditor and source-of-truth-
guardian controls. Writes are new working research artifacts only, not canonical
record changes. Read the complete 41-line [continuation](DENSE-CONTINUATION-02.md),
SHA256 `f532f8376db02f01f5943ea7f1df99719a016a57eecaee2185db079b320f5156`.

Compared the complete diff from [preserved first runner](dense_match01.py),
SHA256 `8c5c92932c43183d0861e16282f95e7be360a36bd9ee016c639e638ebed82bb1`,
to the complete 252-line [continuation runner](dense_match.py), SHA256
`b76788bf65e74fa464c060ee0a5831aba27eb864f6139f2c6c2f5a604bf2ce59`.
The earlier [versioned review](dense-method-review-02.md) remains in force for
unchanged logic and its exact testing limits. No unreviewed later code version
is covered by this disposition.

The diff changes the input-read allowance from 12 to 24 seconds, adds the
continuation declaration pin, revises fixed slots and budgets, excludes chunk 0
from this runner's CLI choices, and requires the first chunk's reproduction
receipt before source processing. The mathematical core pin, four eight-second
intervals, half-open selection, PTS parser, shortlist metric/ties/retention,
registration calls, comparison gates and accepted 275-frame cap are unchanged.
This is not a new candidate definition or a changed scoring method.

## Failure interpretation and continuation gates

The continuation reports that original `dense01` produced 215 filter frames
versus 240 probe frames, missing a final 25-frame suffix, and that `dense00`
completed with eight anchor matches. Those are root-reported execution facts
recorded in the declaration, **not independently reconstructed by this arm**.
The failed partial run must remain excluded from accepted aggregate coverage,
not silently filled or counted as another independent source.

Personally read installed primary FFmpeg manual lines 1174–1208 at
`/opt/homebrew/share/man/man1/ffmpeg.1`, SHA256
`9fc9e9de43802330ce84988ccf46c2fbd669eca2f034478b7543cd2b4ce3b611`.
The complete relevant input-duration and input-seek paragraphs distinguish
duration of data read from requested seek position and preserved earlier seek
lead-in under `-noaccurate_seek`. This supports a read-window explanation as
consistent with the reported suffix cutoff; it does not identify an unlogged
exact seek point or prove that explanation uniquely. No media probe was run.

The new allowance remains subject to exact probe/filter PTS-list equality and
eight exact anchor-pixel matches. If 24 seconds is insufficient, it still fails.
Such failure is extraction evidence, not historical footage anomaly, NIST
misconduct or causal evidence.

The new runner admits only `dense11`–`dense13` and their matching reproduction
slots for chunks 1–3. The successful chunk 0 must use its exact old runner for
`repro00`. The new gate requires that receipt to say completed, identify
`dense00`, and record 480 surface comparisons before decoding begins. It is an
execution-sequencing guard, not independent authentication of that receipt;
actual first-reproduction identity/integrity still belongs to root's run review.
A run directory/start receipt can be created before this gate, but no new
source decoding or scoring occurs before it. The declared sequence still
requires root to finish `repro00` before launching new production.

Slots reserve 450 MiB for `dense00`, 100 MiB for preserved failed `dense01`,
3 × 400 MiB for continuation primaries, 4 × 10 MiB for reproductions, plus
150 MiB baseline: **1,940 MiB**, below 2 GiB. This is an acceptance/storage
budget, not a physical-memory bound or protection against unrelated concurrent
writers. Failed attempts consume their retained slot; this review authorizes
no automatic retries, deletion or slot reuse.

## New synthetic artifact and execution

[Fixture03](fixtures/dense_controls03.py), SHA256
`8bbb52d9cdb0168e59903bb9b21911b822eab81718e93c4b9ea7226fc8a466d4`,
was frozen before execution. It derives from fixture02 while preserving both
prior versions and reusing the original 22 parser/selection/retention checks.
It imports pinned code as definitions only; no runner `main` or media is called.

The [create-only receipt](fixtures/dense-controls03.json), SHA256
`a2873b353d59e04cb64f18dac82d6363e10c8e82f6ff078af0d148dd8d2e6d77`,
records **100/100 PASS**, exit 0 on its first run. Added/updated checks cover
exact slots and 1,940 MiB arithmetic, every slot's one-byte excess, baseline
and symlink rejection; six permitted continuation run names, three correct
comparators, old/wrong names, CLI choices 1–3; each first-repro status,
comparison-name and count rejection plus missing fields; the new declaration
pin; and 24-second input allowance with unchanged lead-in and half-open filter.
Unchanged controls still check NaN/infinite displayed PTS, frame caps, pins,
prior manifest/path/identity, native uniqueness, recomputed shortlist and direct
alarm-handler exception.

Embedded guards are isolated inspected AST `If`/raise statements exercised
on explicit synthetic values. CLI choices and the decoder argument list are
evaluated as isolated expressions, not a parser/main/subprocess execution.
Storage uses in-memory fake files and sizes, not an actual unit census. The
alarm test calls its handler, not a timed signal. Thus the pass is deliberately
narrower than end-to-end decoding, process cleanup or real file reproduction.

Actual executable:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Working directory: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
Command arguments (scoped permission for the new receipt only):

```text
-B research/sherlock-wtc7-investigation/peskin-figure-correspondence/fixtures/dense_controls03.py --output research/sherlock-wtc7-investigation/peskin-figure-correspondence/fixtures/dense-controls03.json
```

Root's [separate execution receipt](fixtures/dense-controls-root03.json), SHA256
`bd05f6ebe0222a120c9d506757a5fc15fb2b56a9462960e6692ee38ca3b2e4c5`,
also records 100/100 PASS. Direct full-JSON comparison here matches after
deleting `argv`; both inspected argument arrays differ only in output filename.
This is a replay of the same fixture, not another independent implementation.
No production receipt was read as part of this comparison.

Fixture02 and receipt02 remain at `d0b2af1d…a2bde` and `87fabd44…2a168`;
full pins are preserved in review02. No root runner, original fixture, prior
receipt, media, STATUS, main file or source evidence was edited. No package
installation, network, transmission or physical finding. Bounded review ends.
