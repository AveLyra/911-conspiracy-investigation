# Independent review of the single harness repair

October 5, 2026. Reviewer: Codex integration-scope subagent, separate from the
harness author and root executor. Source review only; no target import,
native test, matrix, guard execution, or application command was performed.

## Disposition

The repaired source is ready for the protocol's declared bounded retry,
subject to every unchanged runtime gate. No blocking source issue was found
in the two-line change. This is not an observed test pass or a broader safety,
scientific, privacy, endpoint, or human-acceptance finding.

Reviewed runner SHA-256:
`b5b6fac51b2785af156eca0542771028f44df2b5017b2476849e25d4305bb3df`.
The preserved pre-repair runner is
`5747e97e9f08220c1f09ef49701464b152c9e1910c94dc9ae6caada0e772d3fd`,
matching the exact source covered by the earlier independent harness review.

## Change and failure record

The complete difference from `verify_bridge-before-repair.py` adds a comment
and `os.environ.pop("__CF_USER_TEXT_ENCODING", None)` before the unchanged
strict environment-key assertion. It removes that one process-local key;
it does not add it to the permitted environment or bypass checking other keys.
The exact Python/platform, isolated/bytecode flags, pytest-autoload requirement,
empty add-on check, pre-import guard ordering, allowed run parent, guard
controls, pinned inputs, fixed cases and result checks are unchanged.

The saved `native-launch01-failure.json` records the original assertion failure
before guard installation, Faraday/pytest import and run-root creation. It
reports a names-only diagnostic showing the one extra encoding key and zero
executed native/matrix cases. I read that preserved record; I did not repeat
the failed invocation or independently reproduce its diagnostic. My separate
directory listing found the scratch parent empty at review time. The source
ordering corroborates that this assertion precedes target imports and writes.

Removing an unwanted process-local key meets the cleared-environment purpose
without changing the export acceptance criteria. The attribution of that key
to macOS startup is supported here by the root's recorded diagnostic and the
observed Darwin target, not by a separate platform investigation. No value of
the key was read or recorded in this review.

This is the sole post-launch harness repair allowed by the frozen protocol.
Preserve the failed attempt and original source. Further failures do not
authorize another repair, an expanded environment allowlist, wider filesystem
access, changed test expectations, or engine/test edits in this pilot.

## Coverage and actual checks

Read the full original protocol, separate protocol erratum, source review,
prior harness review, complete 445-line pre-repair harness and exact repair
diff. Read the saved failure record and relevant execution log. The main 911
controls and entire investigation charter were read earlier in this task; the
full Faraday operating contract was also read, completing a truncated output
with the missing range. Applied development-verification, evidence-falsification
and source-of-truth guidance to preserve existing criteria and separate source
readiness from actual results.

Shell `cat`/`sed` reads, `diff -u`, `shasum -a 256`, directory listing and
Faraday Git status/revision checks were the only checks. The diff returned 1
because the two added lines differ, as expected; it was not a failed test.
The first combined protocol read named nonexistent `ERRATUM.md`; its correct
existing name `PROTOCOL-ERRATUM.md` was then read fully. No document was silently
substituted. Faraday `git status --short` was empty and HEAD was
`26ab7c96228b3c7ddcec0539f187d104ba49b47b` at this read-only review.

Rechecked inputs:

| Input | SHA-256 |
|---|---|
| `PROTOCOL.md` | `d6b9a077c97dc2b207a587739f7e697f1b94c055bedee1f7a536c022da2569da` |
| `PROTOCOL-ERRATUM.md` | `727bc53e3ee790cfc560630f237297f1ce25ace83596ba293793d4b98096acf8` |
| `source-review.md` | `c7b92dd3cb5b02b5ecb556c5e9bd0c4adfbcd25dd576b4532942e0bb12bdd3c4` |
| `harness-review.md` | `d67175ca9bde033966233e1cfbed445d499f6fbac1c8a9610e545b82ef25dfd6` |

This file is my only write. Root must still execute and retain the declared
native file and two matrices, inspect actual mutation snapshots, compare the
matrix semantics, and obtain outcome review. The existing limitations remain:
Python audit instrumentation is not an OS sandbox; native fixture prose does
not supply the missing typed synthetic flag; synthesis has separately expected
writes; ledger validity and export preservation do not validate science.
