# WTC7 property-applicability derivatives: independent artifact check

2026-09-28. Working research; integrity verification only, not a scientific
source review, model validation, historical finding or legal promotion.

## Authority, independence and checked scope

Main `AGENTS.md`, `WORKFLOW.md`, `START-HERE.md` and the main investigation
`CHARTER.md` control. The worktree's instructions were also read. Applied the
evidence-falsification-auditor, source-of-truth-guardian and PDF skills, including
the evidence claim-ledger and source-of-truth audit references. The independent
checker used the [prospective scope](wtc7-property-applicability-2026-09-28.md)
and the [render01 receipt](wtc7-property-render01/receipt.json), after the root
reported rendering had terminated successfully. It did not import or run either
renderer module, inspect the scientific readers' interpretations, or review PDF
body text or displayed page images.

The exact selected page sequence checked was:

- NCSTAR 1-9 (`n9`): physical 78, 79, 80, 455, 456, 457.
- NCSTAR 1-9A (`n9a`): physical 106, 107, 108.

No other page geometry or page content was inspected. File hashing necessarily
reads source bytes, and the parser reads PDF structure to count pages; these
operations are not substantive reading of unselected pages. Printed-page
labels were not independently certified here. This check covers only the new
`wtc7-property-render01` interval, not earlier derivatives or source acquisitions.

## Fresh source and receipt identities

| Held file | Bytes | PDF pages | Fresh SHA-256 |
|---|---:|---:|---|
| `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf` | 52,766,002 | 797 | `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f` |
| `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf` | 26,952,697 | 173 | `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4` |
| `wtc7-property-render01/receipt.json` | 56,152 | Not applicable | `6383655c2d9822a7d61b4720511fba799f77c7760c366c99f608b087030ca891` |

Both PDFs have the encrypted flag. Each opened through the empty-password
route, with pypdf decryption return code 1. This includes N9A, not just N9.
The source byte counts, SHA-256 values and page counts agree with the declared
scope. This is a match to the locally held identities; no fresh official-server
byte comparison or original transport verification was performed.

## Method and actual commands

The independent read-only checker was an inline script executed with:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -
```

Working directory:

```text
/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/contracting-access-custody-audit
```

The complete script and output remain in this task's tool history, command
chunk `d0cd52`. It exited 0, reporting `PASS`; tool-reported wall time was
1.089634875 seconds. The script is not a separately saved or pinned checker
program. Runtime: Python 3.12.14 (Clang 22.1.3), pypdf 6.10.0, Pillow 12.3.0.
The bundled dependency-location tool was consulted; no dependency was installed.

The checker independently specified the two expected source identities, page
counts, selected-page lists and receipt hash rather than taking them solely
from the receipt. It then:

1. Rehashed the receipt and both complete source files using closed file
   handles; checked recorded resolved paths.
2. Required the exact nine-page source/physical-page order, 200 dpi,
   `complete_pages: true`, `complete-derivatives-only`, and no recorded warnings.
3. Compared the actual recursive render-directory file inventory to the
   receipt's product paths plus the receipt itself. Required unique product
   paths confined to that render directory, with no missing or extra files.
4. Rehashed all 44 products, checking byte counts, hashes and resolved paths.
   Existing text derivatives and font/cache files were hashed only, not read
   as scientific text or executed.
5. For each selected page only, independently read MediaBox, CropBox, rotation
   and UserUnit. Calculated expected pixel dimensions with exact rational
   arithmetic and ceiling at 200/72 pixels per point, including rotation.
6. Checked each PNG signature and IHDR dimensions, 8-bit truecolor encoding,
   Pillow `verify()`, then a fresh full `load()` in a separate context. Required
   one RGB frame, matching dimensions and the decoded-pixel SHA-256 in the
   receipt.
7. Required each page's image and text entries to equal their product records
   and have the expected source-labelled filename. Matched every recorded
   render command to the corresponding physical page, actual source path,
   output prefix, resolution and PNG format. No crop flag was recorded.
8. Checked every recorded command's exit status and associated logs, and
   captured fresh Python warnings and pypdf logging. All opened source, image
   and logging handles were closed.
9. Rehashed all scoped files after checking, and repeated directory membership
   checking, requiring unchanged contents and inventory.

The nine recorded page commands were checked against this exact argument
pattern, with each declared source and physical page substituted separately:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f PAGE -l PAGE -singlefile -r 200 -png SOURCE ABSOLUTE_OUTPUT_PREFIX
```

The tenth recorded command was the same executable with `-v`. These commands
were inspected in the receipt, not rerun by this verifier.

## Results and checked interval

All nine selected pages have MediaBox and CropBox `(0, 0, 612, 792)` points,
rotation 0 and UserUnit 1. All nine PNGs are single-frame RGB, 1700 by 2200
pixels, as expected at 200 dpi. Their full decoding, encoded-file identities
and decoded-pixel hashes passed.

- 44 of 44 receipt products matched their recorded bytes, hashes and resolved
  paths. Actual directory membership matched exactly.
- Nine page entries matched their declared source/page pair and corresponding
  product entries and recorded command.
- Ten recorded commands had exit code 0: nine renders and one version query.
- All 18 per-page stdout/stderr files were empty. `parser.stderr` was empty.
- Receipt warnings, fresh Python warnings and fresh pypdf logs were empty.
- The version-query stdout was empty. Its 144-byte stderr was the normal
  `pdftoppm version 26.05.0` and copyright banner, not a renderer warning.
- Recorded input pins before and after rendering were equal. The two source
  pin entries were independently matched to the current files.

The verifier's separate before/after interval comprised **47 distinct files**:
the two source PDFs, the receipt and its 44 products. All byte counts and hashes
were unchanged across that interval. The compact, sorted-key JSON inventory
mapping absolute paths to `{bytes, sha256}` had SHA-256:

```text
c5d08d62bc2f32e1d3fe8855acbbbf64b5501b9511092e47d579496e8413d958
```

That inventory was held in memory and reported by the checker; it was not saved
as another artifact. The digest identifies this check's snapshot representation,
not a complete historical custody record or a continuous mutation monitor.

## Dependency and evidentiary limits

Seven non-source input pins recorded by the renderer were **not freshly
rehashed by this verifier**: the two renderer modules, pdftoppm wrapper, input
font configuration, Python executable, and PIL/pypdf package entry files.
Their recorded before/after equality is not an independent check of those
current files. Output font/cache products were checked as receipt products;
that does not certify the entire font or native-library dependency tree.
Runtime version strings and recorded command lines do not establish a hermetic
environment or independently prove execution history.

Page correspondence here means exact agreement among declared page membership,
source pins, source-labelled derivative records, page geometry and recorded
commands. There was no independent rerender and no visual comparison to PDF
content. A hash match to a renderer's own receipt does not by itself prove that
the rendered pixels reproduce the intended scientific content accurately.

No source-body interpretation, new text extraction, displayed-image review,
network request, source acquisition, model or solver run, or source/derivative
mutation occurred. No historical authenticity, scientific adequacy, material
assignment, property-domain applicability, native model execution or collapse
mechanism is established by this integrity check. Those questions remain with
the separately scoped source review and subsequent tests.

## Errors, recovery and write boundary

No artifact-check assertion failed and no checker retry was needed. During
instruction orientation, one combined tool response was truncated; separate
bounded reads recovered `WORKFLOW.md`, `START-HERE.md` and the full main charter.
The skills and their referenced checklists were read completely. A scoped
`rg --files -g AGENTS.md` search under worktree `research/` returned exit 1 with
no matches, not a source-integrity failure. The worktree-root instructions were
read separately.

Only this new working verification note was authored. Main sources, render01,
existing research notes, source readers' work, canonical case records and legal
materials remained unchanged by this verifier. No commit, push or transmission
was performed.

## Separate render02 interval: continuation and predecessor appendix

This is a later, separately scoped artifact check of
[render02](wtc7-property-render02/receipt.json), after its successful terminal
render notification and the scope note's prospective continuation declaration.
It does not retrospectively enlarge render01's 47-file interval. The preceding
note was frozen at **9,492 bytes**, SHA-256
`42e6fd29245aca1395c60bfa8dc2b47963bba39c17c37e125034b1072b731839`;
that original byte prefix is preserved unchanged.

The exact new page sequence is N9 physical **458**, then NCSTAR 1-5G physical
**315, 316, 317, 318, 319, 320**, using receipt source labels `n9` and `5g`.
No N9A file or prior render01 product was included in this new source/product
verification interval. No printed footer or scientific page content was read.

Fresh source checks:

- N9: the same main source path as above; 52,766,002 bytes, 797 pages,
  SHA-256 `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.
  Its encrypted flag remains true and empty-password decryption returned 1.
- `ncstar-1-5g-source01.pdf` in this audit directory: 29,847,167 bytes,
  340 pages, unencrypted, SHA-256
  `f6aa637c05c4ff1ae2a6a5e9192471aa69e6e0aa97a4bbe5aa33afd68a3526ea`.
- `wtc7-property-render02/receipt.json`: 47,410 bytes, SHA-256
  `e5ba38da31f0dff7d345f6967e61fa4ddfd7c5376ff6e08371204412a97a5828`.

The independent inline checker used the same bundled Python `-B -` command,
working directory, closed-handle method and runtime versions documented above.
The complete new script/output are in task tool-history chunk `ff0812`:
exit 0, `PASS`, tool-reported wall time 0.8948845 seconds. It did not import the
renderer. This was a fresh verification, not an assertion copied from render01.

All **36 products** matched their recorded byte counts, SHA-256 and resolved
paths. Actual recursive directory membership was exactly those products plus
the receipt. Each of the seven page entries matched the expected source/page
order, image/text product entries, filenames and exact recorded command using
that source and physical page. All seven PNGs passed header/IHDR checks,
Pillow verification, a fresh full load, single-frame RGB mode, dimensions and
decoded-pixel hashes. The selected PDF geometries were independently checked
and produced the following dimensions using exact rational ceiling at 200 dpi:

| Source and physical pages | MediaBox and CropBox, points | PNG pixels |
|---|---|---|
| N9 458 | `(0, 0, 612, 792)` | 1700 by 2200 |
| 1-5G 315, 317, 319 | `(0, 0, 561, 770)` | 1559 by 2139 |
| 1-5G 316, 318, 320 | `(0, 0, 561, 765)` | 1559 by 2125 |

All seven selected pages have rotation 0 and UserUnit 1. The variable 1-5G
page heights were retained, not forced to a common size. Full MediaBox rendering
without a crop flag was recorded.

All **eight recorded commands** had exit code 0: seven page renders and one
version query. All **14 per-page stdout/stderr files** and `parser.stderr`
were empty. Receipt warnings, fresh Python warnings and fresh pypdf logging
were empty. Version stdout was empty; version stderr was the normal 144-byte
pdftoppm 26.05.0 copyright/version banner. No check failed or required a retry.

Recorded rendering-input pins before/after were equal. The two source entries
were freshly verified; the same seven non-source dependency categories listed
above were not freshly rehashed. Their recorded equality is not an independent
dependency or hermetic-environment certification.

This new before/after interval covered **39 distinct files**: the two PDFs,
the new receipt and its 36 products. Every byte count and hash remained
unchanged, and actual directory membership was unchanged. The compact,
sorted-key JSON inventory snapshot digest was:

```text
59b51aef3c41aaab372918e988c6ac9e72197701e1a79e1f2ffbf650427cda05
```

The snapshot was held in memory, not saved as an additional artifact. The two
verification intervals share the N9 source and must not be summed as a
distinct-file count or represented as one continuous checked interval.

All earlier limits remain: page association is a receipt/command/geometry
consistency check, not an independent rerender or visual comparison. No source
interpretation, displayed-image review, new extraction, network, acquisition,
solver run, source mutation or scientific validation occurred. Only this
appendix to the existing verification note was authored; earlier review bytes
and source/derivative artifacts were preserved.

## Separate render03 interval: four final new derivatives

The next prospective scope selected N9 physical **459** and NCSTAR 1-5G
physical **58, 59, 60**, in that order, for
[render03](wtc7-property-render03/receipt.json). This check followed the root's
terminal-success notification. It is separate from both earlier render intervals.
Before this append, the note's frozen **14,003-byte** prefix had SHA-256
`3ab0b2236cfd73a6db292226c019884a0f2e5ae4d9b5e6f506962bb9df97de16`;
that prefix is preserved byte-for-byte.

Fresh N9 and 1-5G checks again matched the source paths, sizes, hashes, page
counts and encryption states recorded in the render02 section. Specifically,
N9 was 52,766,002 bytes/797 pages with SHA-256
`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`,
encrypted and readable by the empty-password route (return code 1); 1-5G was
29,847,167 bytes/340 pages, unencrypted, SHA-256
`f6aa637c05c4ff1ae2a6a5e9192471aa69e6e0aa97a4bbe5aa33afd68a3526ea`.
The new receipt was **32,642 bytes**, SHA-256
`e0b9e0d7adb10bfe87d3dc37bdcc0149e78172898f0efc0b7eec80c511f4507d`.

The independent closed-handle inline checker used the same Python `-B -`
command, working directory and versions documented above. Its complete script
and output are in tool-history chunk `edde3f`, exit 0, with `PASS` results for
this interval and the separately described reuse check below. Combined
tool-reported wall time was 1.153136333 seconds. No renderer was imported or run.

Exact source/page membership, page image/text product association and recorded
render commands matched. All **24 products** matched their sizes, hashes and
resolved paths. Actual directory membership was exactly those products plus
the receipt. All **four PNGs** passed signature/IHDR, full Pillow verification
and fresh load, single-frame RGB, dimensions and decoded-pixel hashes. Selected
PDF geometry independently gave:

| Source and physical pages | MediaBox and CropBox, points | PNG pixels at 200 dpi |
|---|---|---|
| N9 459 | `(0, 0, 612, 792)` | 1700 by 2200 |
| 1-5G 58, 60 | `(0, 0, 561, 765)` | 1559 by 2125 |
| 1-5G 59 | `(0, 0, 561, 770)` | 1559 by 2139 |

All four pages had rotation 0 and UserUnit 1. Dimensions used exact rational
ceiling, not a common-size assumption. Commands recorded full MediaBox
rendering without a crop flag.

All **five recorded commands** exited 0: four page renders and one version
query. All **eight per-page stdout/stderr files** and parser stderr were empty.
Receipt warnings, fresh Python warnings and fresh pypdf logs were empty.
Version stdout was empty; its stderr was the normal 144-byte pdftoppm 26.05.0
banner. There was no failed assertion or retry. The two source input pins were
freshly checked; recorded input before/after equality also passed. The same
seven non-source dependency pins remained outside fresh verification.

The distinct render03 interval contained **27 files**: its two PDFs, receipt
and 24 products. All hashes, sizes and actual directory membership were
unchanged across the check. Its in-memory compact sorted JSON inventory digest
was:

```text
a6504c590ee7aaa4d038f29464534248e22da6319da6dac7684450a140c49e3f
```

This interval shares source files with earlier intervals; their file counts
must not be summed as distinct files or treated as one continuous observation.
The scientific and dependency limits stated above remain unchanged.

## Separate limited reuse check: three existing 1-6A derivatives

This was **not a new render or a revalidation of the whole older run**. It
covered only the already-existing `6a-page-115`, `6a-page-124` and `6a-page-126`
PNG/text pairs in `thermal-property-render01`, their
[old receipt](thermal-property-render01/receipt.json), and the held 1-6A source.

Fresh source verification found `ncstar-1-6a-source01.pdf` to be 22,813,796
bytes, 328 pages, unencrypted, SHA-256
`75b910620ee9c9f202256acd898f01f28a0df23546132c2108a2a1735cb021b3`.
The old receipt matched its previously frozen identity: 139,610 bytes,
SHA-256 `21d1df4b9ad38fbe51e29a41cadcedd8629f1ec572e310badd349dbcdee224b1`.
The receipt's source entry was matched to the current source bytes.

The selected receipt entries were exactly source `6a`, physical **115, 124,
126**, with their expected filenames and matching product entries. All **six
selected product files** matched byte counts, encoded-file hashes and resolved
paths. Each of the **three PNGs** passed signature/IHDR checks, Pillow
verification and fresh full load, single-frame RGB, 1570 by 2125 dimensions
and its old receipt's decoded-pixel hash. Text files were hashed only; their
scientific contents were not read.

No PDF page geometry was freshly inspected for this limited reuse check.
No old render commands, logs, remaining products, directory-wide inventory or
runtime-dependency pins were revalidated. Fresh Python warnings and pypdf logs
were empty for the source count/encryption and selected-image operations.
No assertion failed and no retry occurred.

This separate before/after interval comprised **eight files**: one source,
the old receipt, three PNGs and three text files. All sizes and hashes remained
unchanged. Its in-memory compact sorted JSON inventory digest was:

```text
73bc78c4965208244a1a885503bfd7a4e8565f1129c89314c36b5a29fc89e28c
```

The three selected old pages are reused evidence, not three additional new
renders or independent historical corroboration. Together, the declared source
unit comprises 20 new page derivatives across render01-03 and three reused
pages; that is a page-selection count, not an artifact count or a scientific
validation claim. This verifier did not read the scientific contents of any
of those pages. Only this note was appended; no source, derivative, model,
canonical record or legal document was changed, and no network or solver
operation occurred.
