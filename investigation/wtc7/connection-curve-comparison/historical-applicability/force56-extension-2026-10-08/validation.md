# Actual verification and retained failures

October 8, 2026. Local research derivative, not physical or human acceptance.
Commands below ran in this batch directory unless the relative directory is
specified. `P` denotes
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Producer/tests used Python 3.14.0; independent checking used Python 3.12.14.

## Preflight, correction and historical runs

1. `python3 -B -m unittest -v test_extend.py` initially failed with six errors
   across eleven tests, receipt53a5f6, exit1. Synthetic temporary paths used
   macOS `/var` while resolved child paths used `/private/var`; relative-key
   construction mixed those bases. This was a local implementation error,
   not a missing historical dependency. The displayed traceback was truncated;
   it is not represented as a complete saved log.
2. Before any historical run, `key` changed its return from
   `os.path.relpath(resolved, root)` to
   `os.path.relpath(resolved, root.resolve())`; `closure` added
   `root = root.resolve()` before forming its queue. No selection or numerical
   rule changed. Initial producer SHA256 was
   `d9a090193d4e938b6df6d329f44f6e6568450d7f12a2ec7ea2d8745650a162fd`.
   The exact reverse of those two edits reconstructs that hash without writing
   a file, verified at41cc49. Corrected, frozen v1 producer SHA256 is
   `a085e680a4d3d6a892429e12adb30364d1858b7d0799054652afe9dfec53b5b6`.
3. The unchanged eleven tests then passed, af00ed. Additional actual commands:
   `python3 -B -m unittest -v test_calculate.py` in the prior conditional
   directory: twelve pass, a25f95; `python3 -B -m unittest -v test_extend.py
   test_extend_v2.py` in the prior approach extension: twelve pass,437659;
   `python3 -B -m unittest -v test_compare.py` in the F5/F6 source batch:
   eighteen pass,47eb0f. These are synthetic controls, not historical accuracy.
4. `python3 -B extend.py run01` computed but could not create its output under
   the default sandbox: session16759, terminal receiptf14702, exit1,
   `PermissionError` at exclusive open. No output was created. The same command
   with scoped permission to write the existing investigation directory then
   succeeded, session44943/receipt9af37c. `python3 -B extend.py run02` succeeded
   at184ea3 with terminal exit0 confirmed at210695. The two outputs are identical.
5. Read-only method review found the omitted prior inventory caveat after those
   saves. Both files/code/tests remain unchanged. The prospective V2 protocol
   and wrapper restore only two explicit qualifications. `python3 -B -m
   unittest -v test_extend_v2.py`: four pass,35668c; separate review reran
   them successfully before output. `python3 -B extend_v2.py 01` and `02`
   succeeded with exclusive creation, e69e43 and7ed9b3. These wrapper executions
   preserve prior computed arrays rather than recomputing different physics.

| Output copies | Bytes each | SHA256 |
|---|---:|---|
| run01.json / run02.json | 7,686,747 | 79f63ff2618de2d53ad7467a19372b1f5ba97ff36677f6ca61d13d51ff8c6d8f |
| run-v2-01.json / run-v2-02.json | 7,689,225 | 3b9e96e03a0daa37a0c30e8b9e4eb540b0b350a1b3ae832eeb3acc161815dd07 |

## Independent checking and root replay

The separate method reviewer read protocol/producer/tests and the V2 repair.
Its independent saved-object check b3daa4, exit0, confirms the exact permitted
V2 changes, all 173 pins, all 38 earlier reading objects, all four prior and
four new embedded originals, and unchanged numerical payload. This review
does not substitute for coordinate recomputation.

The separate arithmetic checker imports only two pinned earlier independent
oracles: source-annotation bookkeeping and raw-CTM/axis-corner arithmetic.
It imports no producer, producer adapter, classifier or mapping function and
performs no source pixel reading. Its first unsaved full check stopped at its
intentional pending semantic-review hash gate,5e0a5f; synthetic controls had
passed at1c9048. That was an unfinished review, not an arithmetic pass receipt.
The final V2 run passed atf96425. Exclusive saved receipt:3f2d5d, exit0; tool
display was truncated but the complete JSON file is retained. Same-agent
fresh `check_all()` exactly matched it at84bbfe.

The final checker is 33,256 bytes, SHA256
`06cc701d601d2cb12806fb769c6517dce7161b32609bceeec9519bf54c613ac2`.
Its saved receipt is 24,399 bytes, SHA256
`89b2948f2233fe0ae1883245fbe5166a84de586d707b510ae195578b8216081b`.
Root read all 511 lines in bounded sections and the reused 382-line arithmetic
oracle. Root then independently invoked `P -B` to import the final checker,
run `check_all()` and compare its entire return object to the saved JSON with
type-sensitive `exact`: pass, session98011/receipt0acd76, exit0. No saved file
was overwritten in this replay.

Verified coverage: 740 new decisions, 215 base rectangle conversions, 318
coordinate hulls, 159 new windows, 581 new exclusions, 50 original bands,
38 preserved earlier readings/12,500 decisions, four preserved earlier
embedded originals and twelve unchanged pair objects. The exact required union
has 173 inputs; the new source closure contains 46 files/14 JSON nodes, with
only the six declared external authority-context paths. Those paths are
method context, not independent scientific evidence.

The 222 controls include 173 deliberate one-at-a-time required-pin omissions
and 49 other arithmetic/schema/preservation controls. Do not describe these
as 222 independent experiments. Exact earlier-object preservation is not
fresh recomputation of all 12,500 earlier decisions. Neither arithmetic
agreement nor pin integrity establishes original-curve containment or cause.

Root's direct saved-row check97c3c9 confirms the reported F5/F6 illustrative
columns are excluded in both readings, with their different reasons intact.
Per-reading route counts were independently read atde6d73. These are checks
of the same records, not new observations or independent corroboration.

## Closeout scope

The current report/status/navigation must point to version 2 while preserving
the V1 failure history. Only this research unit, research navigation and a
deduplicated local software-feedback note are changed. Source files, earlier
results, legal spines and accepted engine state remain outside the edit scope.
The separate final report review requested no corrections. It checked report
SHA256 `476e653c2445faacc0149f7cf562b210febca4a01bd4ecffedcb42e267c6a182`;
its direct sentinel/table check was d33a9c and checker-metadata check2a5027.
Root's final `python3 -B -m unittest -v test_extend.py test_extend_v2.py`
rerun passed all fifteen tests,477356, exit0.

Root's bounded documentation/JSON/pin check f65382, exit0, inspected all four
batch Markdown files (no trailing whitespace/conflict markers), all eight
local batch links, all four newly introduced navigation links, all five
batch JSON files and all 173 current input pins. Targets exist, JSON parses,
input pins are unchanged and V2 copies remain identical. This verifies only
this batch and its current navigation references, not the entire historical
research map. The unrelated historical missing-link issue documented in the
preceding source batch has not been silently repaired or declared clean here.

`git diff --check` and scoped status/branch/HEAD inspection completed atd1f40c,
exit0: branch `research/sherlock-wtc7-investigation`, HEAD
`ca1c223335c20905d6608eb15c676f88cbfac734`. New batch files and the narrow
navigation/feedback edits remain intentionally uncommitted. No commit or push.
