# DV metadata execution record

2026-10-04. Research worktree `research/sherlock-wtc7-investigation`, starting
HEAD `ca1c223335c20905d6608eb15c676f88cbfac734`. Prior WIP remains preserved.
The previous goal turn made progress by completing the source timing-basis
review. This unit tests the resulting stream-metadata lead; the full charter
remains active. No physical cause or historical clock finding follows from
synthetic tests or a refused run.

## Method and source preparation

The root read current main/worktree instructions, the full main charter, the
completed timing report, source input manifest, saved Clip3 probe and existing
header code. General public format retrieval used no case payload. The required
format definitions and observed capture limits are in [references.md](references.md).
Root read the relevant primary layout/generation functions and every line of
the new extractor/tests/collector before execution. No downloaded source code
was executed or installed.

The separate method reviewer identified three pre-execution corrections:
an exact frozen dependency set, movie-list hierarchy restrictions, and a
serialized-output cap distinct from the compressed metadata cap. All were
incorporated and tested before the first historical run. Raw pack candidates
are not validated clocks; full calendar/timezone/continuity conversion was not
implemented or tested. Original source-control/SSYB fields remain retained.

The extractor author ran20 synthetic tests (`c94d2b`, exit0) and an AST/API
check (`c4ada7`, exit0), without historical source reads. Root's combined36-test
suite passed (`2ec25b`/session99952, completion`ddb0e7`; repeated
`a9e010`/session70480, completion`946c43`, both exit0). The separate method
reviewer independently passed all36 tests (`5f5e36`, exit0) and gave scoped
prehistorical raw-inventory clearance, not historical/clock acceptance.

The original11-file [freeze.json](freeze.json) was saved from command`f9d77f`,
exit0. Root then saved the complete fresh36-test output from command`17cc3c`,
exit0, in [root-tests.log](root-tests.log). The unchanged synthetic suite uses
`python3 -B -m unittest -v test_dif_metadata test_collect_dv`. These are code
and extraction-contract controls, not historical calibration or codec certification.

## Original historical attempts refused

| Clip | Command | Initial / terminal handle | Result |
| --- | --- | --- | --- |
| 1 | `python3 -B collect_dv.py --clip 1` | `5a7d9b`, session97920 / `2aff70` | exit1 at the1MiB compressed-metadata cap |
| 2 | `python3 -B collect_dv.py --clip 2` | `f0139a`, session89828 / `26692c` | exit1 at the same cap |

Both exceptions arose inside `compress_metadata`, after frame extraction and
slot accumulation. Complete error outputs are preserved in
[clip1-refused.log](clip1-refused.log) and [clip2-refused.log](clip2-refused.log).
No successful JSON or admitted clock inventory was produced. The code's normal
post-run gates were not reached; do not describe those as passed automatically.
Root separately rechecked both complete source hashes and all11 frozen
dependencies after failure (`9bae7e`, exit0); they matched. No other version1
historical clip was started. Both process handles are terminal, not live waits.

The failure diagnoses an inadequate compression/storage allowance. It is not
a demonstrated DV-layout failure, a metadata-absence finding, or evidence of
alteration. The two already performed traversals remain part of cumulative
execution history; a later pass does not erase them.

## Versioned storage correction

The [version2 plan](v2/PLAN.md) preserves the same extraction and population,
with exclusively created binary chunks of100 complete retained frames. Each
artifact remains limited to1MiB; total capacity explicitly rises to at most25MiB
compressed/23925000 raw bytes per clip. This revises the old total per-clip
cap; it does not retroactively satisfy it. The8MiB JSON cap remains.

The conceptual correction was independently reviewed before implementation.
Required acceptance includes exact frame coverage, reopened per-chunk hashes,
strict decompression, concatenated byte equality, exclusive output paths and
post-source/dependency checks before a final result. Version1 and both refusals
remain frozen. Version2 execution/review results must be recorded below before
calling its outputs admitted; its presence on disk alone is not success.

### Version 2 prehistorical verification

The extractor/storage author implemented `v2/storage.py` and its 19 synthetic
tests; the root implemented the wrapper and its tests. Root read all of these
files. Separate method review was by a different agent, not the implementation
author. The storage author's own checks are not described as independent review.

Root's initial 25-test version 2 suite passed (`b0e751`, exit 0). Before the
freeze, root added two tests: collision refusal before source/control reads,
and a real synthetic 101-frame AVI through the extractor, collector, chunk
storage and wrapper, including reconstructed-byte equality. The 27-test suite
then passed (`91e5c0`, session 61131 / `58ccc7`, exit 0), and the complete fresh
repeat is saved in [v2/root-tests.log](v2/root-tests.log) (`ba212f`, exit 0).
Command: `python3 -B -m unittest -v test_storage test_run`, from `v2/`.

The separate reviewer read all five version 2 method/test files. Its 27 version
2 tests passed (`62f6ec`, exit 0); the unchanged 36 parent tests also passed
(`d882fc`, exit 0). Its additional high-entropy 101-frame storage/wrapper test
(`08695a`, exit 0) recovered exactly 966,570 raw bytes from chunks of 957,301
and 9,581 compressed bytes, with callback/argument restoration. That check
also rejected an empty version 2 freeze before pinning. No historical media
was used in these synthetic checks. Scoped prehistorical clearance was given,
not clock authentication, human acceptance, or historical interpretation.

The 17-file [version 2 freeze](v2/freeze.json) was generated by `801fc8`
(exit 0) and checked by `691400` (exit 0), before historical version 2 scans.
Its SHA-256 is `9ab5b4770c66ba8600f4eb1d82a6caaa79045f9767ed84c6a001d630ac606e4f`.
It pins both plans, both implementations/tests, all four format references,
the original freeze and the eight-item input manifest. Binary artifacts use
individual raw/compressed hashes and one concatenated raw hash, not a claimed
single aggregate compressed hash. The ordered manifest defines assembly order.

### Version 2 historical execution

All commands ran from `v2/`, producing local derivative files only. Every run
returned exit 0 after source/dependency post-checks and artifact verification.
Complete returned metadata and result pins are in
[v2/command-results.json](v2/command-results.json).

| Clip | Command | Initial / terminal handle | Result |
| --- | --- | --- | --- |
| 1 | `python3 -B run.py --clip 1` | `d6c62e`, session 77020 / `28b822` | exit 0 |
| 2 | `python3 -B run.py --clip 2` | `8e7911`, session 59217 / `b13108` | exit 0 |
| 3 | `python3 -B run.py --clip 3` | `834103`, session 84987 / `794dce` | exit 0 |
| 4 | `python3 -B run.py --clip 4` | `65c247`, session 22477 / `e3723a` | exit 0 |
| 5 | `python3 -B run.py --clip 5` | `4f8ec0`, session 42079 / `286300` | exit 0 |
| 6 | `python3 -B run.py --clip 6` | `7aee96`, session 33789 / `ae99c5` | exit 0 |
| 7 | `python3 -B run.py --clip 7` | `741a69`, session 90473 / `9dd70d` | exit 0 |
| 8 | `python3 -B run.py --clip 8` | `31f5f1`, session 51342 / `ebf5d2` | exit 0 |

The admitted version 2 population is 5,567 distinct frames across eight files.
Cumulative execution also includes the two earlier refused version 1 traversals;
version 2 is not described as the first-ever read of Clips 1 and 2. All process
handles above are terminal, not live waits. No historical collection rerun was
needed after these successful commands.

Root's first read-only summary check supplied a relative directory to the
absolute-path-only artifact verifier (`5f0ae8`, exit 1). It refused before
reading the first chunk. The complete diagnostic is preserved in
[v2/summary-refusal.log](v2/summary-refusal.log). Correcting only the caller's
path, root rechecked all 60 artifacts and the version 2 freeze, reconciled all
per-frame target candidates and saved the [raw summary](v2/inventory-summary.json)
(`52a549`, exit 0). This verification used the production storage verifier;
it is a repeat/readback check, not an independently implemented byte audit.

### Separate direct-byte audit and root reproduction

The method reviewer wrote [independent-audit.py](independent-audit.py) outside
both frozen method sets. It imports standard-library modules only, not the
producer's parser, extractor or storage helpers. It uses an iterative RIFF walk,
individual retained-block reads, its own slot counters and strict artifact
decompression, comparing all retained bytes directly to source locations.
It independently checks exact frame/chunk coverage, source and dependency pins,
all candidate counts/frame bounds and identifier distributions in every frame.
Common dependencies remain the declared FFmpeg-based layout, the same held
sources, Python runtime and standard-library SHA-256/zlib. This is not a second
historical source or independent proof of camera provenance.

Reviewer synthetic controls passed three positive cases and six refusals
(`da7ade`, exit 0). Its complete historical audit then passed (`53b63f`, session
71903 / `a90dda`, exit 0), saved in [independent-audit.json](independent-audit.json).
All 5,567 frames, 3,674,220 slots, 53,276,190 retained bytes and 60 artifacts
matched; all 107 watched file pins matched before/after. The separate per-frame
check confirms the report table, not merely aggregate totals. Supplementary
check `b1f099` verified the first/last raw values and actual compressed-file
total of 19,906,399 bytes. Its initial broad JSON display was truncated
(`352861`); that display was not accepted as a complete audit output. The later
complete persisted audit is the reported result.

Root read all 310 lines of the separate implementation, reran its synthetic
controls (`82cc28`, exit 0), then reproduced the entire historical audit
(`666c62`, session 86563 / `7f82b4`, exit 0), saved as
[root-independent-audit.json](root-independent-audit.json). This rerun is not
another independently authored implementation. The audit code hash is
`93e9be0d7efe6a6c267442444abcc338913c62c8c2e401da66911f2323400213`;
the reviewer's result hash is
`6be26eb11762fb4e1c1e11dab2b1d497530a19e78a2d343d7bd5c90b3a5a9d54`.

Separate synthesis critique found no material overclaim after clarifying that
the eight held copies—not authenticated original-camera media—match their
acquisition pins and replacing the provisional pending-audit label. No clock
calendar/flag conversion or historical cause inference was added. All review
and historical audit processes above have completed.

Final reconciliation initially asserted byte identity of the two saved audit
JSON files (`c38613`, exit 1), so checks after that assertion did not run.
Inspection (`2c07b5`, exit 0) found equal parsed objects but different formatting:
the reviewer's file is indented (13,754 bytes), while root preserved compact
stdout (8,594 bytes). Both representations remain unchanged and separately
hashed. Do not claim byte-identical saved JSON; every parsed field is equal.
This distinction does not relax the exact source-to-metadata byte comparison,
which passed in both complete audits.

The corrected final reconciliation (`c563a1`, exit 0) verified both distinct
audit-file hashes, equality of every parsed field, all 14 JSON files, all nine
Python ASTs, 18 local links in the five unit Markdown documents and the complete
summary-to-audit count/pin join. `git diff --check` passed (`06c50a`, exit 0);
that tracked-diff check does not by itself validate untracked files. The JSON,
AST, link and artifact checks above cover the named untracked unit outputs.
The report hash at reconciliation was
`c6bd4c85a87a56d36610517a008e0fd3e84535a6c3afaa304408139c61b7bd68`.
No staging, commit or push occurred; prior unrelated research WIP remains.

## Unchanged boundaries

No image/audio decoding, new media acquisition, mathematical collapse analysis,
human acceptance, accepted Sherlock findings, model/window join, legal/main
promotion, external disclosure, staging, commit or push. User coordinate locks
and placement ranges remain untouched. Generic improvements stay locally queued
under the archived-destination boundary. All reviews here are computational
agent reviews, not licensed expert or user approval.
