# Heat-storage source derivatives: independent artifact verification

2026-09-28. Working research. This records a bounded file/derivative-integrity
check, not scientific source interpretation, historical authentication, native
model execution or legal promotion.

## Authority, scope and independence

Main `AGENTS.md`, `WORKFLOW.md`, `START-HERE.md` and the main investigation
`CHARTER.md` control. The previously read controls and the applicable evidence-
falsification-auditor, source-of-truth-guardian and PDF skills remain the basis
for this check. The [prospective source scope](heat-storage-implementation-2026-09-28.md)
was read in full before checking the new package. Root reported render session
18210 terminal exit 0 before artifact access; the verifier did not poll or
restart that session.

The check covers only `heat-storage-render01`, its
[receipt](heat-storage-render01/receipt.json), and the held NCSTAR 1-5G source.
The exact source-labelled page sequence is `5g` physical **99, 100, 101, 102,
103, 155, 156, 157, 158**. Only those nine pages' PDF geometry was inspected.
Printed-page labels and scientific text were not independently read or
certified. Other pages and earlier render packages were not included.

The verifier did not import either renderer module, rerender, run a solver,
extract PDF text, display page images, read existing text derivatives as
scientific content, inspect the scientific reviewers' interpretations, acquire
sources or use the network. Complete-source hashing and structural page-count
parsing necessarily read source bytes; neither is substantive source review.

## Fresh identities

- Source: `ncstar-1-5g-source01.pdf` in this audit directory;
  **29,847,167 bytes, 340 pages, unencrypted**; SHA-256
  `f6aa637c05c4ff1ae2a6a5e9192471aa69e6e0aa97a4bbe5aa33afd68a3526ea`.
- Receipt: `heat-storage-render01/receipt.json`, **54,391 bytes**; SHA-256
  `b5c01aed08fa52c52b80d2fe76293ffa19ce27ac309d4218dfab9accb27b4b66`.

Both identities match the independently supplied scope pins. This verifies
agreement with the locally held bytes, not a new official-server comparison,
original transport or historical chain of custody.

## Actual execution and method

Executed the independent inline checker with:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -
```

Working directory:

```text
/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/contracting-access-custody-audit
```

The complete script and output are in task tool-history chunk `a96d2b`. It
exited **0**, reporting `PASS`, with tool-reported wall time **0.958961458
seconds**. It is an inline script, not a separately saved or pinned checker
program. Actual versions were Python **3.12.14** (Clang 22.1.3), pypdf
**6.10.0**, and Pillow **12.3.0**. No dependency was installed.

The checker independently supplied the expected source hash/size/page count,
receipt hash and page list, then performed these read-only checks:

1. Hashed the source and receipt with closed file handles; checked the source
   record's resolved path, bytes and hash against the current file.
2. Required the exact nine-page order, source label `5g`, 200 dpi,
   `complete_pages: true`, `complete-derivatives-only`, and no receipt warnings.
3. Compared the actual recursive render-directory inventory with receipt
   products plus the receipt itself. Required unique product paths confined to
   the render directory, and no missing or extra files.
4. Rehashed all product files, matching recorded byte counts, SHA-256 and
   resolved paths. The nine existing text derivatives were hashed only.
5. Matched each page's image/text entries to its corresponding product records,
   expected filename, source path, physical page and recorded render command.
6. Read MediaBox, CropBox, rotation and UserUnit only for the selected pages.
   Calculated pixel dimensions using exact rational ceiling at 200/72 pixels
   per point, allowing for rotation and variable page dimensions.
7. Checked PNG signatures/IHDR, 8-bit truecolor encoding and dimensions; used
   Pillow `verify()`, then a separate fresh `load()` and checked single-frame
   RGB mode, dimensions and the receipt's decoded-pixel SHA-256.
8. Checked every recorded command's exit status and actual log files. Captured
   fresh Python warnings and pypdf logging. Source, image and logging handles
   were closed.
9. Rehashed the scoped inventory after checking, and repeated directory
   membership checking, requiring unchanged sizes, hashes and membership.

All nine recorded page commands were checked against this exact pattern, with
each selected physical page, actual source and absolute output prefix supplied:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f PAGE -l PAGE -singlefile -r 200 -png SOURCE ABSOLUTE_OUTPUT_PREFIX
```

The tenth recorded command used the same executable with `-v`. The verifier
inspected these recorded commands but did not execute them.

## Results

**All 40 products passed.** They comprise nine PNGs, nine text files, 18
per-page stdout/stderr files, `fonts.conf`, `parser.stderr`, and two version-query
logs. Unlike some earlier packages, this exact product inventory contains no
font-cache files; no such files were assumed or silently added to coverage.

All nine PNGs passed full decoding and encoded-file/decoded-pixel hash checks.
Actual selected-page geometry and expected image sizes were:

| Physical pages | MediaBox and CropBox, points | PNG pixels at 200 dpi |
|---|---|---|
| 99, 101, 103, 155, 157 | `(0, 0, 561, 770)` | 1559 by 2139 |
| 100, 102, 156, 158 | `(0, 0, 561, 765)` | 1559 by 2125 |

All selected pages have rotation 0 and UserUnit 1. Every PNG is single-frame
RGB. Variable page heights were retained rather than imposing one common size.
Recorded commands contain no crop flag; MediaBox and CropBox coincide here.

All **10 recorded commands** have exit code 0. All **18 per-page log files**
and `parser.stderr` are empty. Receipt warnings, fresh Python warnings and
fresh pypdf logging are empty. Version-query stdout is empty; its 144-byte
stderr is the normal pdftoppm **26.05.0** version/copyright banner, not an error
or rendering warning. No checker assertion failed and no retry was required.

Recorded renderer input pins before and after rendering are equal. The one
source pin was independently matched to current source bytes.

## Checked interval and dependency limits

The separate before/after interval covers **42 distinct files**: the source
PDF, receipt and its 40 products. All sizes and hashes remained unchanged, and
actual directory membership remained unchanged. The in-memory compact,
sorted-key JSON inventory mapping absolute paths to `{bytes, sha256}` had
SHA-256:

```text
7e8ba4484d89e97b979fe5149724d66b0854cebf3f7e9efe1f2a2b231c855cbc
```

This snapshot was not saved as a separate artifact. Its digest identifies the
check's snapshot representation, not a historical custody record or continuous
monitor. The shared source does not make earlier checked intervals one larger
continuous interval or allow their file counts to be added as distinct files.

Seven non-source pins in the renderer's receipt were **not freshly rehashed**:
the two renderer modules, pdftoppm wrapper, input font configuration, Python
executable, and PIL/pypdf package entry files. Their recorded before/after
equality is not an independent present-byte check. The output `fonts.conf`
product was checked, but the complete font/native-library dependency tree was
not. Version strings and recorded commands do not prove a hermetic environment
or independently authenticate execution history.

Page association here is consistency among the declared selection, pinned
source, product records, page geometry and recorded commands. There was no
independent rerender or visual comparison with scientific PDF content. Matching
a renderer's own receipt does not alone establish correct scientific rendering.
No heat-storage formulation, material assignment, solver activation, historical
run, source accuracy, physical validation or WTC7 consequence is established
by these checks.

Only this new working verification note was authored. Existing research WIP,
main/raw/legal records, source bytes and render products were not changed.
There was no commit, push, disclosure or other external action.

## Separate render02 interval: six-page continuation

This later check covers only [render02](heat-storage-render02/receipt.json)
and the shared held NCSTAR 1-5G source. The prospective continuation declaration
was read before checking artifacts, and main AGENTS, WORKFLOW, START-HERE and
the complete main charter were reread. Root confirmed render session 39539
terminal exit 0 (root command chunk `d5a4df`) before access; this verifier did
not poll or restart it. The source-reader's interpretation was not inspected.

The preceding note was frozen at **8,462 bytes**, SHA-256
`9a9fcf49f406bed677419e0d4d1455f4464d6fd09c5db20a01cae725ccb1b67f`.
That prefix is preserved byte-for-byte. The new interval does not enlarge or
rerun the earlier 42-file verification interval.

The exact selected receipt sequence is `5g` physical **73, 74, 75, 76, 115,
116**. The source was freshly rehashed and counted: **29,847,167 bytes,
340 pages, unencrypted**, SHA-256
`f6aa637c05c4ff1ae2a6a5e9192471aa69e6e0aa97a4bbe5aa33afd68a3526ea`.
The new receipt is **39,656 bytes**, SHA-256
`363edc39a11ecc3428f3f2e59c61a16beb7b5fec42c1e0fdd43c29455ca01652`.

The independent closed-handle inline checker used the same bundled Python
`-B -` command and working directory documented above, with Python 3.12.14,
pypdf 6.10.0 and Pillow 12.3.0. Complete script/output are in tool-history
chunk `56ce2d`: exit **0**, `PASS`, tool-reported wall time **1.07595225
seconds**. No renderer was imported or executed. No checker assertion failed,
no warning was suppressed, and no retry was required.

Fresh checks covered exact page order, source label, 200 dpi, completed
derivative status, every product's size/hash/resolved path, unique confined
product paths, exact actual directory membership, and each page's image/text
entry and recorded source/page/output command association. All **28 products**
passed: six PNGs, six text derivatives, 12 per-page stdout/stderr files,
`fonts.conf`, parser stderr and two version-query logs. Text files were hashed
only; their scientific contents were not read.

All **six PNGs** passed signature/IHDR checks, Pillow verification and a fresh
full load, single-frame RGB, dimensions and decoded-pixel hashes. Geometry was
freshly inspected only for these six PDF pages, with exact rational-ceiling
dimensions at 200 dpi:

| Physical pages | MediaBox and CropBox, points | PNG pixels |
|---|---|---|
| 73, 75, 115 | `(0, 0, 561, 770)` | 1559 by 2139 |
| 74, 76, 116 | `(0, 0, 561, 765)` | 1559 by 2125 |

All six pages have rotation 0 and UserUnit 1. Recorded commands have no crop
flag. Each of the **seven recorded commands** has exit code 0: six renders
and one version query. All **12 per-page log files** and parser stderr are
empty; receipt warnings, fresh Python warnings and fresh pypdf logs are empty.
Version stdout is empty, and its 144-byte stderr is the normal pdftoppm
26.05.0 version/copyright banner. These are recorded-command/log checks, not
new execution of those commands.

The renderer's before/after input pin lists are equal. The source entry was
freshly verified; the same **seven non-source dependency pins** listed above
were not freshly rehashed. The output font configuration was verified as a
product, without claiming complete font/native dependency coverage.

The separate before/after inventory comprises **30 distinct files**: the
source, new receipt and 28 products. All sizes, hashes and actual directory
membership remained unchanged. Its in-memory compact sorted JSON inventory
digest is:

```text
883e3e0c85a3683e1ae242d4f5347b693825f91b78366b88d346f1451188bdeb
```

This is not a saved inventory artifact or a continuous monitor. The two checked
intervals share the source file; their counts must not be summed as distinct
files or treated as one uninterrupted checked interval.

All earlier limits remain. Printed footers, report semantics, physical
accuracy, native thermal formulation and historical execution were not
independently evaluated. No displayed-image review, text extraction, rerender,
network access, solver run, source mutation or main-repository edit occurred.
Only this appendix to the existing artifact-verification note was written.
