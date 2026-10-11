# Independent Chapter 3 source/derivative audit

2026-10-04. **Pass within the artifact-integrity scope below.** All 41 selected
text extracts reproduce byte-for-byte, all 41 main PNGs and both authorized
supplement PNGs pass integrity checks and full pixel decoding, and every
declared product and dependency matches its saved receipt. No scientific
conclusion, model validation, historical authentication or human acceptance is
established by this result.

## Authority, independence and scope

Read current main `AGENTS.md`, `WORKFLOW.md`, `START-HERE.md`, the full WTC7
charter, the evidence-falsification and source-of-truth skills and their
referenced checklist/template, then this unit's complete `PROTOCOL.md`,
`execution.md` as available at inspection, `derive.py`, and later the complete
`render_supplements.py`. The sole authored output is this working research
audit. No raw/main/legal records or authority boundaries changed.

This auditor previously identified the unreviewed chapter as a source lead,
but did not author the derivative adapter and did not read either reader's
new scientific notes. This is independent artifact-checking code, not a blind
historical investigation or a separate primary evidence family. The checks
did not import or execute either project rendering script, launch a renderer,
display an image, execute embedded PDF content, run a solver or retrieve any
new source. Text was parsed for byte comparisons and page/chapter boundaries,
not interpreted as structural evidence.

## Fixed identities

The source is the already-held main-repository
`research/sherlock-wtc7-investigation/comparator-expansion/plasco-thesis/sources/domada-2025-plasco-thesis-8358.pdf`.
Freshly checked: 12,229,604 bytes, 291 physical pages, unencrypted; SHA-256
`0d76577bbf898dfa2d1587d02f1cc51378d531e3b59983fc0d4db8665fd575b4`.

| Record | SHA-256 checked |
|---|---|
| `PROTOCOL.md` | `c53267b049e8241465a224825c32aabbe82e0cce59c2cce85da5174fcf30c304` |
| `derive.py` | `f0792ef91f36509940abf683103f1a12ff3b86a065b7c8907675403b42a43230` |
| `run02/receipt.json` | `d2c203d1bb9cf243e1cbdfc68a204c3996df358b65528d8df171fe0ec645524c` |
| `render_supplements.py` | `019fbf087eb9dbbe6d8cd17850cf5986c3ce961b6e81387b22755d5c4426583e` |
| `supplements01/receipt.json` | `304438b81f95bd532fe453cd8d9ae217a1bebd13d026129220e6c96e54c32693` |
| preserved `run01/receipt.json` | `5a02e6c8bc313448efec6d957bc0d0f0cb80636b7a870c5c5dd5b3446feb3190` |
| preserved `archive-v1/derive.py` | `24ddf78dcf89e994ba1fa717cf514408d20cb6677c46da2e031bef15a970cdb9` |
| preserved `archive-v1/test_derive.py` | `57f54ff7c9bd9ece62c3055477a1d34e062f762034c45ea5d3575d44d8bf89cf` |

The eight main dependency records identify the source, adapter, protocol,
font configuration, resolved Python executable, renderer entry wrapper,
intermediate wrapper and native renderer binary. Every current byte length
and hash matched the receipt's identical before/after maps. The supplement's
ten dependencies preserve those exact eight identities and additionally pin
the main receipt and supplement harness. All were checked again at audit end.

## Exhaustive main-run checks

The independently written, assertion-enabled inline Python check used bundled
Python 3.12.14, pypdf 6.10.0 and Pillow 12.3.0; these matched the saved versions.
It checked the following for **every page**, not a sample:

- Exact ordered physical population 92–132, with no missing or duplicate row,
  and printed labels 77–117. Each freshly extracted first nonblank line agrees.
- Fresh `PdfReader(...).pages[n-1].extract_text().encode('utf-8')` bytes equal
  the entire corresponding saved text file, with no text normalization.
  All 41 row identities also join the product manifest exactly.
- PNG signature/format and `Image.verify()`, then a separate open and
  `Image.load()` to decode all pixel data. All are RGB; no display was made.
- Image dimensions agree with their row, zero page rotation, unit user scale,
  and `ceil(MediaBox dimension * 110 / 72)` for both axes.
- Exact inner render argument vector, separately saved command JSON and row
  agreement: one page per command, `-f n -l n -r 110 -singlefile -png`, exact
  fixed source and page-specific output stem, 60-second requested timeout,
  `status=returned`, exit 0, and empty saved stdout and stderr.
- All 209 declared top-level products match byte length/hash: 41 sets of text,
  PNG, command JSON, stdout and stderr (205 files), plus `start.json` and the
  three renderer-version records. The exact top-level file set is these 209
  plus the separately pinned receipt. No product path is a symlink or a path
  outside that set. The task-local font-cache directory is not a declared
  receipt product and was not represented as fully inventoried evidence.
- `start.json` equals the corresponding receipt fields. The recorded isolated
  environment has the expected task-local font configuration/cache paths.
- The renderer-version command record is exactly `pdftoppm -v`, returned 0;
  stdout is empty and stderr contains only the exact Poppler 26.05.0 version
  and two copyright lines. This expected version output is distinguished from
  the empty rendering diagnostics.

Dimensions are **not uniformly portrait**: 34 images are 935×1210; seven are
1210×935, at physical pages 97,98,99,102,103,104,105. Their respective PDF media
boxes are 612×792 and 792×612 points. This is consistent orientation handling,
not a missing-page or scaling discrepancy.

The additional boundary check freshly extracted physical 92,132,133, verified
initial printed labels 77,117,118, Chapter 3/4 markers where applicable and the
Chapter 3 title. All three complete UTF-8 byte counts/hashes match the saved
boundary records, including the unselected Chapter 4 opening. No Chapter 4
method or result was evaluated.

## Two predeclared legibility supplements

After root's explicit audit-scope extension, checked every product in
`supplements01`: physical 117/120, printed 102/105, 300 dpi, both 2550×3300 RGB.
The two PNGs passed both integrity verification and full pixel decoding.
All eight products (two PNGs plus two command/stdout/stderr triples) match
their receipt; that exact file set plus the receipt exhausts top-level files.
Both per-page commands match the declared source, page, scale and output,
returned 0 with empty stdout/stderr, and retain the 60-second timeout setting.
Their page identities join the main receipt; all ten dependencies and the
supplement receipt match before and after this check. No additional rendering,
text extraction, visual inspection or claim of improved legend legibility
was made by this auditor.

## Actual verification record and failures

All checks ran from this unit's absolute worktree directory. Both complete
audit programs were supplied on stdin using the actual invocation
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -`.
They used standard-library hash/JSON checks, direct pypdf extraction and Pillow
decoding rather than importing the producer. Both begin with `assert __debug__`.
The full inline bodies and JSON outputs are retained in this task's command
transcript; no parallel checker framework or generated audit data was added.

| Command receipt | Actual result |
|---|---|
| `a17573`, exhaustive main-run inline check | exit 0, 2.606 seconds; 41 exact texts, 41 labels, 41 decoded PNGs, 41 clean render records, 209 products, eight dependency pins, three boundaries; all checked inputs/products unchanged at end. Captured pypdf/Pillow warnings and diagnostics empty. |
| `774426`, receipt-only dimensions/count listing | exit 0, 0.842 seconds; 34 portrait and seven landscape pages with exact landscape list above; only top-level directory is `font-cache`. |
| `2795be`, exhaustive supplement inline check | exit 0, 1.162 seconds; two decoded PNGs, eight products, ten dependency pins, two clean render records; all checked identities unchanged at end; captured decode warnings/diagnostics empty. |

No audit assertion failed and no failed verification was retried or relaxed.
An initial combined instruction-read output was truncated; the affected
charter tail and the full protocol were reread before verification. This was
an inspection-output limitation, not a source or derivative failure.

The failed production **run01 remains failed**: zero selected-page products,
empty boundary list, and `Unexpected terminal printed label at physical page
92`. Its only declared product is `start.json`; its own dependency maps remain
equal, and the archived v1 code matches that receipt's old code hash. Both
run01 files and both archived v1 files were byte-checked unchanged across the
main audit. The corrected producer checks the first nonblank label. The
historical failure is not overwritten, relabeled successful, or evidence of
a physical/model defect. No synthetic test suite was rerun here.

## Acceptance ceiling

No material artifact-integrity discrepancy was found in this fixed population.
The reproducibility claim is **exact text extraction using the same parser
version**, not an independent text-recognition method. Valid decoded PNGs and
consistent render receipts do not independently establish every glyph's
visual fidelity. There was no fresh render comparison, complete font/shared-
library pinning, outer-terminal replay, or measurement of actual subprocess
duration against its requested timeout; inner argv/status records were checked
as saved records, not independently witnessed historical execution.

The source and derivatives are unchanged relative to the declared captures.
This does not authenticate thesis author/custody, event observations, model
inputs or results, validate collapse physics, settle source interpretation,
or satisfy the separate reader/human gates. The two scientific readings and
their comparison remain separate work. A failed byte, page, command or decode
join would defeat this integrity disposition; none occurred in these checks.
