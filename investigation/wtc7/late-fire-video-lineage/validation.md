# Execution and validation record

2026-09-19. Research-only; finite partial admission, not full eight-source
screening or scientific validation. Paths below are relative to this unit
unless absolute. Results distinguish root execution, independent computation
and descriptive AI viewing. No human review or historical authenticity claim.

## Frozen controls and actual execution

Root read the original implementation, tests, selection, protocol and reviews
completely before historical execution. A separate code reviewer ran the
original suite before historical processing. Root inspected the complete v2
helper/test diffs before the separately declared historical v2 attempts.

| Control | SHA-256 |
|---|---|
| PROTOCOL.md | `f81d1e7e1d8ae914cd62e182cd6f2db642bd60e19737d204f18d3b97d1e70486` |
| selection.json | `e5abd641738cbbb7656f2c4d0f70336725247787d8955637082a44401047fdc0` |
| screen_local.py | `b5048a0a19347861fe8567ffcffd54a69dfb9df284ebb6bc66c503b54723375c` |
| test_screen_local.py | `5988d73bfb93e24546f015983c0070f7e767c831f8330973b03f962731337b74` |
| GRAMMAR-FOLLOWUP.md | `8c1f26316c6ace3f68fb06881b9eed465827672bb7d7168aa250275ae8efa723` |
| screen_local_v2.py | `890963c2104f53813593b4e09da9b3c5892d2461a2a6a415f06f84842b31d8f9` |
| test_screen_local_v2.py | `61fee5f4bd23a6ce3b6abd372c3f40d6d9e0d3ea9ab3d71ebe745c239c731c83` |

Runtime for processing: bundled Python 3.12.14 at
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`,
with `-B`, Pillow12.3.0 and installed `/opt/homebrew/bin/ffmpeg` / `ffprobe`7.1.1.
The [code review](helper-critical-review-2026-09-19.md),
[v2 review](v2-review.md) and per-run receipts pin executable identities,
arguments and diagnostics. No dependencies installed or global settings changed.

Actual root synthetic invocations, from this unit directory, were:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B test_screen_local.py --artifacts /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/late-fire-video-lineage/controls-2026-09-19-root01
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B test_screen_local_v2.py --artifacts /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/late-fire-video-lineage/v2-controls-root02
```

They passed 16 and 26 tests respectively. The separate code-reviewer suite
also passed 16. Producer v2 used the same revised test script with the absolute
artifact directory ending `/late-fire-video-lineage/v2-controls01` (26 passed).
V2 retains the original 16 tests and adds 10 targeted controls, including refusal
of unsupported late-SEI warnings and declaration identity changes. These are
synthetic tests, not historical measurements. Intentional negative fixtures
remain stored. See the linked reviews for exact absolute command forms.

Historical execution used this command form, shown for original source 002
from the unit directory:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B screen_local.py --selection selection.json --protocol PROTOCOL.md --source-id VID-WTC7-002 --run /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/late-fire-video-lineage/run01-VID-WTC7-002
```

Other source IDs and their exclusive absolute run directories were substituted
as listed below. Admitted repeats use corresponding absolute `run02-ID`
destinations; at most two jobs ran concurrently. The separately declared v2
uses `screen_local_v2.py` and absolute `v2-run01-ID` / `v2-run02-ID` destinations.
Exact decoder-subprocess arguments are retained in receipts. Both `--run`
and test `--artifacts` destinations must be absolute. These commands record
completed execution, not permission to overwrite or reuse the existing outputs.

- Original002/003/004/005/PESKIN first passes and repeats: completed.
- Original001 and kit: `frame_inventory_malformed`; no extracted samples.
- Original006: `decode_diagnostic_review`; 53 partial PNG filenames, no accepted
  frame table or overviews. Unsupported late-SEI warnings remain unresolved.
- V2kit first pass and repeat: completed; one terminal delimiter recognized.
- V2Camera2: `decode_diagnostic_review`; 135 partial PNG filenames, no accepted
  frame table or overviews. Sole unreviewed category: guessed stereo layout.

Four failed historical directories remain intact. Zero process exit alone was
not admission. Diagnostic review reconciled the saved timing logs for the two
decode refusals; this is not pixel validation or acceptance of partial images.

## Independent reproduction and exact coverage

The [independent reconciliation](independent-reconciliation-2026-09-19.md)
documents each actual command and its output identity. Its original checker
does not import the producer or its binning function. A separate pinned kit
adapter recognizes only the declared grammar revision; original checking
products remain unchanged. Before source checking, four positive groups and
six negative fixtures passed; the kit adapter adds three positive grammar variants and thirteen
negative fixtures. These differ from the16/26 producer-helper suites.

Five original pairs plus one kit v2 pair reconcile241,001 integer inventory
rows per pass,579 selected native images and50 overviews. Complete plans,
frame tables and raw inventories (18 data products) match between their paired
runs. All629 material image files match byte-for-byte. Across twelve runs,
2,854 product-hash references pass; duplicate references are not independent
files. Whole path-bearing receipts need not be byte-identical. Each admitted
decode has exactly13 previously reviewed software-conversion fallback notices
and no unknown warning/error; source/tool/control pins match.

Key comparison outputs:

- `independent-repeat-comparison-01.json`: four original pairs,397 images and12
  data products; SHA `3f6112de27195cb572d19a9293eaba4ab03510d5c3481bb05f8fe9234b71c61b`.
- `independent-repeat-comparison-02.json`: Peskin pair,215 images and3 data
  products; SHA `83f943389a2395ffe4b772b33d1ad79d517f286d4ac4054d0fd365bcf92ff67d`.
- `independent-v2-repeat-comparison.json`: kit pair,17 images and3 data products;
  SHA `a2e7bc7a60648c433da5090f1ba08253a32c76ac9122cab95c63db33d71006a0`.

This is independent arithmetic/product verification on common decoder outputs,
not a second historical decoder, distinct camera evidence or physical validation.
Root's separate earlier four-source comparison checked405 pairs (397 images
plus8 plan/frame-table files), not an additional independent629-image test.

## Actual visual coverage and frozen records

Root and the separate AI observer each viewed all50 admitted overview sheets
covering579 samples, not every decoded frame. The observer additionally viewed
27 complete native images; after first-pass exchange root viewed the same27.
Both reference JPEGs were separately inspected. No crop, enhancement, acoustic
analysis, continuous-event duration or metric-motion measurement was performed.

Root's native follow-up hash/index/size check passed27/27. The initial truncated
multi-image output for Peskin144–146 was excluded until each image was displayed
separately. First-pass candidate differences and prior familiarity remain in
the linked [root](root-screening-2026-09-19.md) and
[observer](observer-2026-09-19.md) records. Independent saved observations are
not a human-review attestation.

Observer final six-source note:29,410 bytes, SHA
`07ddca744d7ffe6a871d997e18756a5e8e37f61160495d64c7370a19df18837e`.
Its [freeze file](observer-2026-09-19-freeze-pins.json) retains the earlier
reference/four-source/five-source prefix identities. Root's preserved
six-source first-pass prefix:9,895 bytes, SHA
`7a32b86c8e2f0226f1f39064638a2c615bfc44fce35a7c4e515c0da4d7c0458b`.

## Failures, review and final checks

Permission-review timeouts occurred on several scoped agent file/command
requests. Existence/output checks preceded the permitted retries. Two note-edit
context mismatches were corrected without changing computation. A premature
read of a pending file and one incorrect working-directory path were execution
errors, not source absence. No historical refusal was erased or acceptance
criterion silently weakened.

Two bounded [critical wording reviews](critical-review.md) checked the summary
against the independent computation and frozen visual record. Corrections
clarify absolute output paths, fixture counts, per-still anchors, shared task
framing and provisional-lead differences. This is not new independent visual
or numerical execution.

Root's final read-only bundled-Python check exited zero: 16 exact pinned files
match (controls, checker identities, comparison outputs, reviews and observer
note); four frozen-prefix checks pass (three observer prefixes and root's
9,895-byte first-pass prefix). All nine root-level Python files parse with
`ast.parse`; all 13 root-level JSON files parse. The four new/updated unit
documents (report, validation, critical review and root observations) have no
trailing whitespace, and all 17 local Markdown links resolve. This is a scoped
check, not recursive validation of every historical artifact or all repository
links. The final report SHA-256 is
`05ad2671abd073a30206a05b44cc41f96ef57be130d23d8ab68a32ccbc8ab31c`;
the complete appended root note is
`e269bcc5bae8f74a648ceba980ea4ee5991a6bcee550f88865d7caa4ea9385e7`.

`git diff --check -- research/README.md
research/sherlock-wtc7-investigation/STATUS.md
research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md` exited zero. This
tracked-diff check does not include the untracked unit; its document whitespace
was checked separately above. The first record-validator attempt used the
sparse worktree-relative `tools/validate_record.py` and failed because that
file is not populated there. After locating the actual main-repository script,
`python3 /Users/admin/docs/911/tools/validate_record.py --strict`, run from
`/Users/admin/docs/911`, exited zero: headers, issue/fact links and citation
tags pass. It checks the unchanged canonical legal record, not scientific
claims or this unit's untracked outputs. A discovery command also reported
the missing sparse `tools` directory; neither is evidence of a missing source.

The complete investigation remains active. This unit does not promote legal
facts, accept a Sherlock finding, activate Faraday, publish, commit or push.
