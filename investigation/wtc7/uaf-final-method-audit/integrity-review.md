# Independent source and derivative integrity review

2026-09-20 UTC. Reviewer: `next_discriminator`. Research-only, bounded
integrity check under the main controls and full charter. The PDF,
evidence-falsification and source-preservation safeguards apply. I read
PROTOCOL.md, PAGE-SELECTION.md, all of render.py, and the saved start/receipt
records. I did not read root/observer substantive notes, display page images,
interpret report findings, retrieve anything externally, or run a solver.

## Disposition

**Pass within this scope:** the complete admitted source matches its pinned
45,196,602 bytes/hash and the preserved response length. All 37 specified
physical pages map exactly to the 37 PNG/text pairs. A fresh implementation
that does not import or execute render.py reproduces all 37 PNG byte streams,
all decoded RGB pixels, and all extracted text bytes. All five recorded input
pins and all 76 files in render01 remain unchanged across the check. No MuPDF
opening, page-loading, rendering or extraction warning was returned.

This is an independent invocation/code path using the **same renderer/version**,
not an independent rendering engine, visual typography review or validation
of the report's science. It does not certify all runtime dependency binaries.

## Source completeness and pins

- Source: `source/uaf-final-2020.pdf`, 45,196,602 bytes, SHA-256
  `f3a001ab68dcc6b6e230456aac4729613740336796c1b2515671141589c38bfa`.
- PROTOCOL.md: 4,350 bytes, SHA-256
  `bacffb9075dbc0a946b255c7835158179bd4419614743b38c9795bc47d7978e1`.
- PAGE-SELECTION.md: 2,558 bytes, SHA-256
  `52af38a17f046736078ed53eee035636493002e492baf598e1ef9d87b8848e5a`.
- render.py: 3,045 bytes, SHA-256
  `215521a1ebbd69cdc940c904032bfd0ad9489d66f23d62bb8c841676dfd1810f`.
- Recorded Python executable: 33,816 bytes, SHA-256
  `7d29600aa971dfd764a15b113d5964b1e74a18176a6b70cb31646d45e9e5018e`.

The start pins equal receipt.before and receipt.after, and every recorded
size/hash freshly matches the corresponding local file. Actual runtime
versions agree with start.json: Python 3.13.7, PyMuPDF 1.27.2.2, MuPDF 1.27.2.
Pillow 12.0.0 supplied a separate PNG parser/full RGB decoder for the pixel
comparison; a separate read-only version command exited 0.

Both captured HTTP header files contain status 200, content type
application/pdf and Content-Length 45,196,602. Only those allowlisted fields
were printed; no full-header or session-field disclosure occurred. The
27,341,395-byte `attempt01.partial` is an exact prefix of the admitted source;
it remains excluded and unchanged. I did not witness or repeat either download
and do not infer success of the initial transfer from its HTTP status.

The admitted file ends with a complete `%%EOF` marker and one trailing newline.
It opens as a PDF without repair, encryption, password requirement or warning;
all 125 page objects load with positive page dimensions. Only the selected
37 pages were rendered/extracted in this replay. This establishes bounded
local completeness/parseability relative to the captured transfer and pinned
source, not publisher authenticity, content accuracy or all-object validation.

## Preserved checker failure: header versus catalog version

The first read-only inline verifier exited 1 at its assertion that the file
header itself was `%PDF-1.4`. It had already checked the source size/hash,
five input pins, page-list membership, 75 recorded product pins and exact
76-file inventory. It had not begun the fresh rendering loop. No file was
created or changed.

An explicit byte-envelope inspection found a `%PDF-1.3` header and intact EOF.
A separate parser inspection found catalog `/Version /1.4` and effective
metadata `PDF 1.4`, with 125 pages, no repair/encryption and no warnings. Thus
the page-selection document's effective PDF1.4 description is consistent
with the catalog; my header-only assumption was wrong. The corrected
read-only verifier checks the header and catalog separately. It does not
repair the PDF, discard a source defect or relax the source hash/length gate.

## Actual independent replay

The successful invocation ran from the investigation worktree with:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B - <<'PY'
# Inline, read-only source/receipt/PNG verifier; method recorded below.
PY
```

Session **53533** reached terminal **exit 0**. It imported only standard
library modules, PyMuPDF and Pillow, not render.py. All generated pixmaps and
fresh text stayed in memory. No second derivative directory was created.

The expected physical-page list was independently literalized from the
prospective selection, not accepted from the producer output:

```text
1, 3, 4, 34, 35, 36, 37, 38, 39, 40, 44, 50, 51, 52,
65, 66, 67, 68, 105–123 inclusive.
```

It contains 37 distinct ascending values and exactly matches start.json and
receipt.pages. The mapped pages are zero-rotation 612-by-792-point pages;
fresh full-page rendering at 150 dpi gives 1275-by-1650, three-channel RGB,
without alpha. No crop, resize, enhancement or selected-region render was used.
Physical-page mapping uses `doc.load_page(physical_page - 1)`; this does not
independently authenticate the report's printed page labels.

Reproducible check recipe:

1. Parse start.json and receipt.json. Require terminal status
   `complete_not_visual_review`, true inputs_unchanged, equal start/before/after
   pins, exactly the five expected input paths and current matching hashes.
   Require runtime strings and 150 dpi to match the executing environment.
2. Construct the exact product set as `start.json` plus `pN.png` and `pN.txt`
   for each of the 37 independently declared physical pages. Require the
   receipt's product keys to equal that 75-name set and the directory's actual
   set to equal those products plus receipt.json: **76 files**, all regular
   nonsymlink files. Rehash every product and compare its recorded bytes/hash.
3. Check the source length/hash/header/EOF and allowlisted transfer headers,
   compare the excluded partial to the full source's prefix, then open the PDF
   and check the catalog version, page count and no-repair/encryption/warnings.
   Load every page object without rendering the unselected pages.
4. For each selected N, render directly with
   `doc.load_page(N-1).get_pixmap(dpi=150, alpha=False)`. Require dimensions,
   RGB channel count and no alpha. Open the saved PNG with Pillow, require
   PNG/RGB/one image and expected dimensions, run `verify()`, reopen and fully
   `load()`, then compare `im.tobytes()` with fresh `pix.samples`. Also compare
   saved PNG bytes directly with `pix.tobytes('png')`. Compare saved text bytes
   with `page.get_text().encode('utf-8')`. All **37** pixel, PNG-byte and text
   comparisons pass. Recorded and freshly returned per-page warnings are empty.
5. Rehash all five inputs and all 76 render files after the full loop and
   require equality with the independently captured before values. All pass.

The receipt deliberately does not hash itself within its products mapping;
that is not an omitted derivative. Its separately checked identity is
16,653 bytes, SHA-256
`aec3b332d38c90ec682e46eac8684a551ad9e0f7fb72ca57de1b53c4d7d32749`.
start.json is 1,703 bytes, SHA-256
`980ecc4fc95a7ca3856ced2257537bb16c906f8d5857f13689649225e916537d`.

## Code review and limits

The producer refuses an existing output directory before writing, validates
the fixed source and 37 unique pages, pins inputs, checks opening state, uses
one-based-to-zero-based page mapping, and preserves an incomplete receipt on
exceptions within the rendering block. Each PNG/text pair is generated from
the same page object. Per-page warnings are recorded rather than automatically
fatal; this reviewer explicitly checked that all saved and fresh warnings are
empty. These are code-reading observations, not new synthetic branch tests.

The source/render equality check detects wrong-page products, altered pixels,
altered text and changed pinned inputs in this saved run. Shared-library
rendering defects could reproduce identically. Successful image decoding is
not visual confirmation of legible glyphs or semantic completeness; those
remain the separate readers' task. No claim about P-delta, model execution,
failure mechanism, source truth or causal ranking is made here. No original,
existing output, main/canonical record or other WIP was modified. The sole
new file from this task is this integrity review.
