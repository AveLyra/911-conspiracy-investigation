# Independent integrity and diagnostic-stage review

2026-09-20 UTC. Reviewer: `next_discriminator`. Bounded research-only check
under the current main controls and full charter. PDF, evidence-falsification,
source-preservation and development-verification safeguards govern this work.
I read the complete PROTOCOL.md, PAGE-SELECTION.md and render.py, and parsed
all start/receipt fields. No network request, source repair, dependency install,
solver, canonical change or external disclosure occurred. Root/observer
substantive notes were not read. No page images were displayed or substantive
decision findings interpreted by this reviewer.

## Result and admission limit

**Integrity/reproduction passes with reproduced rendering diagnostics.** Both
complete 37-page passes reproduce every stored PNG byte stream, decoded RGB
pixel array and text byte stream exactly. All five input pins, all 75 recorded
product identities, the complete 76-file render directory, and the preserved
HTTP-header identity remain unchanged across the check.

The warning is **not an extraction-only warning** and is **not just caused by
whichever operation first visits a page**. It appears during `get_pixmap()` on
every page in both tested operation orders. Neither `get_text()` nor PNG
encoding returns a warning in either order. This is not a clean-render result.

Technical disposition: the saved pages are complete single-image, fully
decodable and reproducible full-page products suitable for a **qualified
visual-reading assessment**, with the diagnostic retained. Actual legibility,
glyph/footnote completeness and absence of visual omissions must be checked
by the separate complete-page readers; this integrity check does not certify
those properties. Extracted text is reproducible and usable for navigation,
not a substitute for that visual review or validated logical reading order.
No source repair or replacement is warranted by these checks alone. A reader
finding a concrete missing/incorrect visible element would require a separately
declared comparison, not silent admission or silent repair.

## Source, runtime and exact inventory

Source `source/817373.dec.pdf` is exactly **294,760 bytes**, SHA-256
`962c2f2faf8fa7f17ef7a16efa6cbc8d036e4d82b6d8cc86e9237c2ff3234acc`.
The file has a PDF1.4 header and a terminal `%%EOF` marker. MuPDF opens it as
PDF1.4 with 37 pages, without repair, encryption, password requirement or
opening warnings. All 37 page objects load without warnings. Matching byte
count/hash, captured response length, EOF and parseability support local
transfer completeness, not official authenticity or semantic correctness.

Only allowlisted header fields were printed: `HTTP/1.1 200 OK`,
Content-Length `294760`, Content-Type `application/pdf`. They agree with the
saved source. I did not witness or repeat the original transfer. The complete
665-byte header file remained local and unchanged, SHA-256
`bf82621e88dc782fd582c5fe06a3a6ced13a24580362b7415ad54c9bdbffc853`.
No cookie, session or other header fields were printed.

Freshly checked pins:

| Input | Bytes | SHA-256 |
|---|---:|---|
| PROTOCOL.md | 4025 | `13659d152ea17822e35f4816f47e0f28fe0f0731b7a099f3f13ffce1ebf4da5b` |
| PAGE-SELECTION.md | 2429 | `afc662ab02fb75fe0f835a6204ab90f406e506dab9db966b3c9c36e557292ae4` |
| render.py | 2952 | `8562380b6db77be55c3ba557398bf53426f5c50d001d192f60d5ba8104a9e442` |
| Python executable | 33816 | `7d29600aa971dfd764a15b113d5964b1e74a18176a6b70cb31646d45e9e5018e` |

The source is the fifth input. start.pins, receipt.before and receipt.after
are identical and match all current bytes. Runtime identity agrees with the
receipt: explicit `/Users/admin/.pyenv/versions/3.13.7/bin/python3`, Python
3.13.7, PyMuPDF1.27.2.2, MuPDF1.27.2. Pillow12.0.0 supplied a separate PNG
parser and complete RGB decode. These checks do not attest all loaded native
library or font binaries.

The independent expected page sequence is exactly physical **1–37**. It
matches both start and receipt, without duplicates or omissions. Each page
uses source index `physical_page - 1`; every checked source page is
zero-rotation, 612-by-792 points. Every saved and fresh image is 1275-by-1650
RGB, no alpha, at the declared full-page 150 dpi. No crop or enhancement was
performed. Printed page numbering, exhibit identity and substantive coverage
remain the visual readers' questions, not consequences of this physical map.

The exact 75-name receipt product set is start.json plus 37 PNGs and 37 text
files. Actual directory membership equals that set plus receipt.json: **76
regular nonsymlink files**, no extras. Every product size/hash matches.
receipt.json deliberately does not hash itself in its product mapping.

- start.json: 1,668 bytes, SHA-256
  `ff3000a368a6d9be195f1dbe73145d7b415a88b4cf7f7b9b0fae34174aad89f4`.
- receipt.json: 20,163 bytes, SHA-256
  `d834d55db51091fd11207e79bfc3cbd762b78f4d3cf7fec9e23df35b6141d7f1`.

## Actual checks, failure and diagnostic isolation

The first inline verifier exited **1**, with `AssertionError: 1`, at its
premature assertion that the rendering stage should have no warning. Source
and product guards had passed before that point. The failure was a reviewer
assumption, not evidence that the source bytes or saved products had changed.
No file was created or modified. This failed check is preserved here rather
than retrospectively labeled a pass.

A fresh one-page diagnostic then opened a new document and collected/reset
the MuPDF warning buffer separately after opening, page loading, rendering,
PNG encoding and text extraction. It exited **0**: page1's warning came from
rendering; both fresh image and text bytes matched their saved counterparts.

The complete diagnostic replay then ran with this invocation prefix from the
investigation worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B - <<'PY'
# Inline standard-library/PyMuPDF/Pillow verifier, method below.
PY
```

Session **37631** reached terminal **exit0**. It did not import or execute
render.py and wrote no derivatives. All fresh products remained in memory.
The comparison ran twice, opening a fresh document for each pass:

1. Page load, render, encode PNG, extract text.
2. Page load, extract text, render, encode PNG.

Actual warning-stage counts:

| Stage | Render-first pass | Text-first pass |
|---|---:|---:|
| Document opening | 0 | 0 |
| Page loading | 0/37 | 0/37 |
| Full-page rendering | 37/37 | 37/37 |
| PNG encoding | 0/37 | 0/37 |
| Text extraction | 0/37 | 0/37 |

Each nonempty warning is exactly:

```text
format error: No common ancestor in structure tree
structure tree broken, assume tree is missing
```

In render-first order, joining the separately collected nonempty stage
diagnostics exactly reproduces every producer combined warning string. The
second order rules out treating the observed warning as a generic first-
page-traversal or text-extraction-only effect in this tested runtime. It does
not establish the underlying defect's complete origin or visual consequences.

Reproducible verification method:

- Independently construct pages1–37, five expected input paths and the exact
  product set. Require terminal `complete_not_visual_review` status, true
  unchanged flag, equal before/after/start pins, and current matching hashes.
  Require actual directory membership and nonsymlink regular files to match.
- Check source header/EOF, pinned bytes/hash and the three allowlisted header
  fields. Open the PDF without repair/encryption and check 37 pages and PDF1.4.
- For each page in each pass, reset/read diagnostics after each operation.
  Use `get_pixmap(dpi=150, alpha=False)`, compare saved PNG bytes with fresh
  `pix.tobytes('png')`, and compare saved UTF-8 text bytes with fresh
  `page.get_text().encode('utf-8')`.
- Open each saved PNG with Pillow, require PNG/RGB/single image/expected size,
  run `verify()`, reopen and fully `load()`, then compare `im.tobytes()` with
  fresh `pix.samples`. Each pass obtains **37 exact PNG, RGB and text matches**;
  both orders therefore give 74 of each comparison without new saved files.
- Rehash all five inputs, all76render files and the captured header after
  both passes. Every value remains unchanged.

## Producer and usability limits

Code reading confirms the existing-directory refusal, fixed-source guard,
full physical-page selection, before/after pins and finally-block receipt.
Per-page warnings are recorded, not fatal; its completion status expressly
does not claim visual review. No new synthetic branch-control execution is
claimed here. The protocol's earlier description of the route as clean must
not be used to describe this warned historical run.

Same-renderer reproduction can reproduce the same omission. The named
structure-tree fallback is a real diagnostic, not proven harmless by stable
pixels or clean text extraction. Conversely, it is not evidence that all
page content is unreadable or that a substantive passage is wrong. The
bounded admission decision therefore rests on preserved diagnostics plus
the separate full-page reading, not automatic rejection or automatic fidelity
certification. No procurement inference, person/actor allegation or legal
conclusion follows from this integrity pass. The sole new file from this task
is this review; all existing sources, products and WIP remain preserved.
