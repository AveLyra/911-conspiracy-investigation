# Validation and reproducibility

2026-09-12. This validates the bounded numeric/property inventory and its reporting,
not LS-DYNA execution, the physical model or a collapse explanation.

## Sources and scope

The [protocol](PROTOCOL.md) SHA-256 is
`4406af3500c495adc95edd1c86e07901f73e6cafa43a39bfc57a8920c34c552a`.
The four raw files remain at the original repository's inventoried supplementary
production path. They are dependencies, never rewritten inputs. Source aliases,
compressed pins, full decompressed byte/hash/line receipts and EOF status are in
both root results and the independent source receipt. Total decompressed coverage:
567,432,650 bytes and 11,294,760 physical lines. CRC/EOF and hashes provide integrity
checks relative to those bytes, not historical authentication.

The selected set was known from the prior member map. The independent reviewer
used prior pins and card-layout constraints, not producer code or new results,
to construct and freeze a fresh parser and extraction. That is independent
implementation verification, not blind discovery of a collapse hypothesis or
review by a licensed engineering expert.

## Root production and repeated arithmetic

Runtime: bundled Python 3.12.14, bundle26.905.11957; standard library only.
[map_materials.py](map_materials.py) SHA-256:
`dede959bc9f440b6b0bab8784e8c8b7c7a461cd7bcfef820487b3ff2538bc469`.

Both full passes passed 11 synthetic controls: fixed-width and CSV blanks,
nonfinite rejection, duplicate definitions, namespace zero/offset handling,
shell row pairing/missing continuation, commented/unused definition treatment,
curve-namespace independence, unsupported required keyword rejection, and data
following END. Neither root pass failed. Control success does not establish
general format support or element-ID uniqueness.

| Artifact | SHA-256 | Timing / interpretation |
|---|---|---|
| [run01.json](run01.json) | `b69c12ec0668c9bdf5f5ea59dbf483d2a959de7bd477c172efe69c2f03e33594` | 35.7043 s; initial complete pass |
| [run02.json](run02.json) | `7663fa0b97ea7f3177aca68de215115db77b499da97530250d382d0214b129b3` | 35.1423 s; all fields identical except elapsed time |
| [crosswalk-summary01.json](crosswalk-summary01.json) | `5c8c8c468670a9f7c5a91e245b24e2b694636533d7ce954978d565615ecfa757` | Deterministic repeat check and report arithmetic |
| [summarize_materials.py](summarize_materials.py) | `b97edb66bc7a6c75b9a4e822f787014f8c3fd696b4946966dc54c68b5ba18732` | Pins both root results; does not re-read source bodies |

Root commands were issued from the dedicated worktree using the bundled Python
and `research/sherlock-wtc7-investigation/material-run-crosswalk/map_materials.py
--output research/sherlock-wtc7-investigation/material-run-crosswalk/run01.json`,
then `run02.json`. The summary helper takes no arguments and creates its named
output only if absent. Preserve existing results; use a separately named output
for a new producer pass, and compare scientific fields separately from timing.

## Independent verification

[independent01.json](independent01.json) was frozen before root output access,
SHA-256 `1cd998cff02b9cf4e947339fa1efbdaf1ae8bb6703fa644a61bab8ca26416a3c`.
Its extraction core SHA-256 is
`4caa98ce70e5eb78125052da7ee97c42e3aac415fe25a28dcf66a1a77072fca2`
(bytes preceding the explicit INDEPENDENT_EXTRACTION_END marker).
The initial complete script hash in its receipt is
`4c75b9a5e2d017928be05db9de8473c226718e1fcd282407c522dbd02714db79`.
The core remains unchanged as later comparison/report adapters are added.

The independent pass took 45.8701 s, observed peak 222,314,496 bytes, and passed 15
controls. It verifies element-ID uniqueness separately within each element family,
unlike the root producer. It derives the SRC-120 offset only after comparing all
specified transform fields. It retains47 complete selected PART cards,47 SECTION
blocks and24 MAT blocks; the latter two selections are broader than the root's
24 sections/20 materials. The extra four MATs belong to the included counterparts
of parts722/752/753/782 and are not proposed substitutions.

The first adapter run, [independent-comparison01.json](independent-comparison01.json),
failed with a sanitized KeyError because plain INCLUDE records omit a `cards`
key. The extraction itself was not changed. The failed receipt is preserved;
its result is null and is not scientific contrary evidence. After a post-core
schema correction, [independent-comparison02.json](independent-comparison02.json)
passed, SHA-256
`3997f9409c02bffc6c3d0d757da7b2b19d5336a1dcf5d27df52a2ee7f825ffcc`.

Comparable scope:459 part-reference rows,392 used-part family rows,47 complete
PART cards,24 full SECTION blocks,20 full MAT blocks,1,904 damage candidates,
all effective material IDs, include locators/transforms and four full source
receipts. There are25,227 independently reconstructed numeric scalar comparisons;
maximum observed absolute difference is0 (declared adapter tolerance1e-8).
The much larger root-repeat check is separately counted and is not independent
source verification. This extraction did not retain all curve numeric arrays;
59 curve keyword blocks can be checked by the preserved keyword hashes.

[independent-report01.json](independent-report01.json), SHA-256
`2b521f5b6dbbe037e56ecd9a07ffac46d106300f906434c1971435aa5c801846`,
checks all14 independently derivable summary fields, all23 displayed table rows
and13 additional numeric assertions. Its reviewed report SHA-256 is
`3aa26d1afa723da8c69876ff3711964259562cf6824a142176ff93909cd7dee9`.
That exact version is preserved as [report-before-review-edits.md](report-before-review-edits.md),
reconstructed from the final version by reversing three known edits and checking
the original hash. It is history, not another current report authority.

The [current report](report.md), SHA-256
`a9afca6aa6221db2f96bb0d2720cadb7094532105f5e86661fb591b9315babcf`,
qualifies historical non-use, distinguishes curve-array verification coverage,
and spells out the six full beam line numbers. Those are the only three changes;
the inference reviewer independently confirmed them by reverse-hash comparison.

## Source-page and inference review

### Root consumer replays

Root read the independent implementation and its post-freeze adapters before
running it. [independent03.json](independent03.json), SHA-256
`037f94228f5f8a6dce2514eb84abf95df5c3201492c3e25e88d2b3edba495a27`,
is a fresh complete four-source pass under code
`d0138111f29ce25796d923b7fc0a8d21ffac87cc57f48fcb420696711f10e0e1`:
45.3056 s, 220,135,424-byte observed peak, 15 controls, PASS. Its entire scientific
`result` object equals independent01 exactly; runtime/command receipts differ.
That source version is retained as
[verify_materials-before-report-pin.py](verify_materials-before-report-pin.py).

Only the post-core report hash was then intentionally changed after reviewing
the exact three-edit diff. The final [verify_materials.py](verify_materials.py)
SHA-256 is `f29bd685260fcc86d9b5cc64aebfb81ee7d05ced716e6f6064ba537a0486ac07`;
the frozen extraction prefix is unchanged. Root reran:

- `--compare --output independent-comparison03.json`: PASS, 0.1031 s,
  [receipt](independent-comparison03.json) SHA-256
  `da3bf4338cc6ab1134207609b66d22db31687bfbe410fc578230009e8ee6dd02`.
- `--report --output independent-report02.json`: PASS for the current a9af…
  report, 0.00893 s, [receipt](independent-report02.json) SHA-256
  `23b8c47373c38b958e8a7eebc8c0f74c2247f4b9a35001e6a0ed00a8a643a3ff`.

The source replay used `--output independent03.json`; all commands used the
bundled Python with the worktree-relative verifier path. These runs are consumer
reproductions of the independently written method, not further independent
historical witnesses. Current Python processes are terminal.

### Primary-method review

[method-source-review.md](method-source-review.md), SHA-256
`84e2c98335c2a00ee7615fe412f7eda4367fb72f84cc366185163f9d057b68e9`,
pins the three public source PDFs, selected text/search coverage and full-page
rendering checks. Root and the separate inference reviewer each inspected these
14 complete pages: NCSTAR1-9A59,73,74,75,104; NCSTAR1-9 539,540; May2007
Version971 manual1086–1089 and1502–1504. This independently checks the passages
used by the current report, not every source page reviewed by the source agent.

[inference-review.md](inference-review.md), SHA-256
`3fd44fd238534bedae7607271d83d92aef537f43d8c3bd6b89680f20d9a977b1`,
documents four synthetic parser-limit demonstrations and the final report review.
Corrections distinguish inactive-in-this-assembly from historical non-use, and
separate run repetition from independent curve-array reconstruction. No additional
material source/inference correction was requested.

The conditional manual interpretations do not establish exact behavior of NIST's
reported beta revision or authenticate the produced deck. The published calibration
description is not independent validation of the connection capacities. Numeric
counterparts, hashes, ordinary material names and matching mesh counts cannot
supply missing history or an evidentiary cause.

## Limits retained

The root reader does not enforce element-family ID uniqueness, require an END
keyword at EOF, implement all control cards, or derive every offset dynamically.
The independent source pass covers uniqueness and fully checks this explicit
transform, but is also not a general solver parser. Positive shell/beam joins
remain scoped and family-qualified. Ignored keyword hashes are not interpreted
properties; blank numeric slots remain null even where a manual lists defaults.
An unhandled root failure would not itself create a durable JSON receipt; that
robustness limitation is recorded, not claimed tested by the successful passes.

The final [independent review](independent-review.md) SHA-256 is
`304c3bf48188e5d32cb29c9db6d20cce8552c9e55b5049a1693f12bcd146b863`.
It includes the source freeze, schema-adapter failure, final-report version change
and attributed root consumer replays. All bounded reviewers are terminal.

Final structural checks parse all 4 Python ASTs and 11 JSON files and resolve all
46 local links in the 7 unit Markdown files, with no trailing whitespace. Scoped
tracked `git diff --check` passes. Read-only strict record validation reports OK
for headers, issue/fact links and citation tags; that is not engineering validation.
The worktree navigation and existing handoff are updated. Earlier research WIP
and all original/superseded artifacts remain preserved.

No source execution, solver reproduction, property substitution, damage activation,
restart, cause ranking, canonical promotion, legal edit, external transmission,
commit or push occurred. The full investigation goal remains active.
