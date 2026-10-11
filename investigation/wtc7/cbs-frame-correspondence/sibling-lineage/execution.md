# Eight held AVI header comparison — execution

2026-10-04, research only. Worktree
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, branch
`research/sherlock-wtc7-investigation`, HEAD `ca1c2233`. Changes remain WIP;
no staging, commit, push, main/legal edit or source-byte rewrite.

## Before historical parsing

Root preparation commands use `python3 -B` from this directory unless stated
otherwise. The PATH executable is `/opt/homebrew/bin/python3`, Python3.14.0,
verified by `dad09e`; it must not be mislabeled as the bundled runtime. The
separate bundled Python runtime used for final collection is
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
No historical collector run occurred during the following preparation.

- Input inventory review (`602a2d`, exit0) verified32 saved-record hashes and
  existence/size of all eight selected complete copies, without reading their
  headers or rehashing their raw content. The two partial failed transfers stay
  preserved and excluded. This is an earlier reviewer result, not a new run.
- Initial parser controls: `python3 -B test_headers.py`,16 passed (`926669`).
  The separate original/alternate lanes were added before any new historical
  header read; updated17 passed (`00f9df`). The original equality gate was not
  used to select historical results.
- Saved-record schema inspection `fd9507` passed. An earlier attempted read of
  a nonexistent top-level input manifest (`dcdaa5`) failed; stage-specific
  acquisition records were located. This was a path mistake, not source absence.
  A plan-edit patch failed on a nonexistent context line and made no change;
  the narrower correct patch succeeded. Neither is a media-analysis failure.
- Manifest derivation (`fdeb06`, exit0) checked all four acquisition hashes,
  selected attempts and source file sizes, then copied the raw hashes and eight
  saved-container summaries into [inputs.json](inputs.json). Population8,
  aggregate692988832 bytes. Saved via apply_patch, not a media retrieval.
- Independent method reviewer: corrected an initial documentation-path error
  (`2e6374`) before synthetic tests.17 passed (`0fe022`). A separate enumeration
  over19800 nominal labels across11 minutes mapped19782 legal drop-frame
  labels consecutively (`c01c94`); it also confirmed Unicode digit acceptance.
  Root changed the parser to ASCII digits and added rejection coverage before
  historical execution. Updated17 tests and three AST checks passed (`1e3909`).
- Reviewer `46a774` verified all four acquisition and eight container hashes,
  all eight selected-attempt/path/size/hash/summary joins, arithmetic and ASTs;
  updated17 controls passed. No AVI was opened or hashed by that review.
  Documentation now distinguishes a cited source from byte-pinned publication
  content, and no invocation from no installed binary.
- Root saved-prior-output diagnostic `3e4e6f` failed with `KeyError: hex`:
  the old collector preserved some payloads as lossless UTF-8, others as hex.
  Direct schema inspection (`1ecb6d`) and original implementation reading
  (`27ac6e`) identified the mixed representation. New `prior_payloads` handles
  both and validates reconstructed lengths/hashes. Root18 controls passed and
  all12 prior retained payloads/866 bytes reconstructed (`1117b4`). No fresh
  AVI read had occurred; this correction was not informed by new clip results.
- Reviewer cleared the final amendment:18 tests passed (`380b8b`); independent
  synthetic checks of hex/multibyte UTF-8 and invalid length/hash, missing/both
  forms and duplicate offsets passed (`d419b9`). No historical data opened.

This log distinguishes commands that ran from intended later checks. Final
freeze, header collection and result verification are recorded below only
after they actually execute.

## Frozen run

- Root ran the final18 controls with the explicit bundled executable above
  (`3e206a`, exit0); all passed. Seven-file freeze capture `fb8517` was saved
  through apply_patch as [freeze.json](freeze.json),1114 bytes, SHA256
  `3fc64c0f741afab02126905c1c049768642f4b52cd6b12b1d091d649e906d3b2`.
  It records source/plan/manifest/reference dependencies after separate review,
  before reading new clip headers. It is not retrospective preregistration of
  previously known Clip7 fields or a pin of remote publications.
- Exact command: the bundled executable with `-B collect.py`, working directory
  this unit. One invocation `9ab42d`, exit0,3.955715041 seconds reported command
  wall time, Python3.12.14. Complete127195-byte stdout parsed as JSON and was
  saved verbatim through apply_patch as [results.json](results.json), SHA256
  `f64e1f29ee19e0bb5bdac42fd95222c46304c4d0af5259acbf14a227fac224dc`.
  No output truncation or historical collector retry occurred.
- Each of8 files yielded24 headers and866 retained bytes:192/6928 total.
  Forty selected tag occurrences; one per tag per file. All eight header/saved
  inventory joins passed; all raw/record/frozen dependency hashes matched
  before/after. Clip7's12 retained payloads/866 bytes exactly reconstruct the
  earlier output. Original/alternate text prefixes agree in all cases; this
  does not assert equality of their full binary payloads. All four
  declared comparisons are available, with seven edges each and no ties.
- No subprocess, media probe, codec, DV-pack interpretation, frame/audio output
  or historical media view was invoked. Whole-file SHA256 hashing read source
  bytes twice for integrity. Header bounds are parser limits, not OS resource
  quotas. The run does not establish arbitrary-file safety or image authenticity.
- Root `a885a1` verified saved result/freeze hashes and five contextual-source
  pins. The contextual interpretation is post-output; these documents were
  not newly added to the frozen primary arithmetic population. Pins below.

| Context source, relative to this directory | SHA256 |
| --- | --- |
| `../dense-clip3/v2/report.md` | `d90d6b387a180015aba1cd2dccdb8df9270091f6ba900ac7faedd4d62c6eafce` |
| `../dense-clip7/report.md` | `984f3132fae5016cc01bdf2a68831b2147963fc0db9fd541e4aa908ce96ff470` |
| `../../cbs-vince-source-screen/stage4/report.md` | `5408e26089855db635ffee0f4fea453d7bb2a4ba5b59203c962900431db2f733` |
| `../../fire-coverage-batch3/assets/run01/context/P-ebeb74127e68.txt` | `2772110710b61a13af806b2f77829bde1af0b2f570ecbc6c0df6edfe647f927b` |
| `../../fire-coverage-batch3/assets/run01/context/P-8338c00a97d8.txt` | `f5a4c9ef7d07a1d153c7f208693eccb97d58542cf170498fe3a64102e5ab2735` |

## Separate interpretation review

The method reviewer separately examined results and the saved contextual
sources without new media reads. Independent interval arithmetic `db3b88`
finds a positive Clip7-minus-Clip3 offset for any discrete exposure in their
respective held intervals under both interpretations: approximately125.659
to169.536 seconds overall. This is a post-output conditional check, not a
historical time measurement, and was not used to select frames. It shows why
nearest-frame ambiguity alone cannot reverse the ordering. It leaves original
clock versus edited-master semantics and exact source associations unresolved.

The review also narrowed the useful documentary lead to a paired5-142/5-143
source/timing/edit chain and rejected treating Clip8's metadata comment as a
verified visual observation. Those points are incorporated in the report.
Neither review is human source acceptance, another camera or cause evidence.

Final synthesis review required two additional clarifications: only an
incorrectly associated recording interval, not a nearby frame within the same
interval, could explain the sign reversal; and disclosed intensity adjustment
is not itself evidence of exaggeration. A supported exaggeration finding would
require an unsupported material inflation of a particular observation/input.
The final text incorporates both corrections.

Root post-output check `67279b`, exit0, separately reproduced the discrete
interval endpoints from stored counts/labels: ND377/3 to339/2 seconds and
DF1884883/15000 to5086081/30000, identical across O/A lanes. It also verified
that every original/alternate timecode and tape-name full-payload hash differs.
The equal textual prefixes do not imply equal binary tails or two clocks.

## Independent byte and arithmetic audit — complete

Separate reviewer `sibling_byte_audit` executed a read-only inline Python
program with the bundled executable and `-B`, without importing the production
parser or collector. Final command `9863ba`, exit0,3.424 seconds reported wall
time, verified:

- Seven frozen-file pins, the freeze pin, and all20 dependency pins, including
  every complete raw AVI hash. Result127195-byte hash matches the value above.
- Direct seeks to all192 listed chunk headers and96 retained payloads,
  totaling6928 bytes; no movie/index/essence interpretation.
- All40 selected tag occurrences/2976 bytes: IDs, sizes, offsets, exact payloads,
  hashes, UTF-8 prefixes and binary tails; eight video stream headers and their
  joins to saved inventories.
- All28 adjacent edges in O/A × ND/DF, independently using integer and
  Fraction arithmetic, plus all12 prior Clip7 retained payloads.
- All eight O/A textual pairs agree; all eight full timecode pairs and all
  eight full tape-name pairs differ. No arbitrary interpretation of tails.

The independent audit had two failed attempts, both preserved in the tool
record: `65c829`, exit1, assumed flattened prior payload fields; `f5f135`, exit1,
then omitted the prior UTF-8 representation. The corrected rerun handled
both lossless representations with length/hash checks. Neither historical
results nor method were changed to obtain a pass. The root pre-run schema
correction and these later auditor errors are distinct events.

These are direct checks of reported offsets/payloads and conditional arithmetic,
not an independently rediscovered complete container tree, second camera,
human inspection, or authenticated historical clock. No file edits, media
probe, decoder, new views or production imports occurred in that review.

Root final consistency check `260784`, exit0, verified the seven frozen
dependencies, exact result hash, aggregate counts, three Python ASTs,13 local
Markdown links, whitespace and both navigation entries. `git diff --check`
also passed. Before that consistency check, root corrected a prose transcription
of total retained bytes as6936 instead of6928; the JSON and per-file866 values
were always unchanged. A patch attempt with incorrect context made no edits before the
correct narrow patch. Source findings and arithmetic did not change.
