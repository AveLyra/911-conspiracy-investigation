# Floor-model source and derivative integrity check

September 28, 2026. Independent artifact-only check by the existing metadata
locator agent, separate from root's scientific source reading. Research only.
This is not historical authentication, experimental validation, a model replay,
or endorsement of the report's scientific conclusions.

## Scope and controls

Main AGENTS/WORKFLOW/START-HERE and the main investigation CHARTER control.
The [declared source scope](floor-model-validation-followup-2026-09-27.md)
controls page selection. The evidence-falsification-auditor,
source-of-truth-guardian and PDF skills were applied to keep byte/representation
checks distinct from source-content review. Only this new note was written.
No source, receipt, rendering, legal record, model, drawing or other note was
edited; no new network retrieval occurred in this artifact check.

Root reported all three rendering batches terminal with exit 0 before the
successful check. Render03 was not inspected until that notice. The successful
check used one combined before/after interval for the two source PDFs, three
receipts and all 164 receipt-listed products: **169 distinct files unchanged**.
This does not attest to their state before acquisition or after that interval.

No PDF body text was extracted, no source page or PNG was displayed, and no
extracted-text product was read as text. Existing text products were hashed as
opaque bytes. In particular, summary physical pages **140 and 141 remain
content-unviewed and excluded from the scientific review**; checking their
geometry, PNG decoding and hashes does not cure or erase the earlier locator
error. The other pages were also not substantively read by this verifier.

## Verified source pins

| Receipt source label / local file | Bytes | Pages | SHA-256 |
|---|---:|---:|---|
| summary / `ncstar-1-6v1-source01.pdf` | 23,824,565 | 270 | `9874df97f3ce7bffb048fa9390823599f733cfed5549ca14b934a126f62240d4` |
| component / `ncstar-1-6c-source01.pdf` | 8,363,877 | 252 | `aab90082f22baaa41ed8dd22c89192040aa6f629b0cc800d1b47f07a5c7ef411` |

Pypdf reports the summary PDF unencrypted. The component PDF has an encryption
flag; its empty password is accepted (return value 1). These checks establish
local byte identity and parser access, not the report's historical authenticity.

## Batch coverage and receipts

Physical page numbers, not inferred printed labels, are the integrity keys.

| Batch | Exact source/page membership | PNGs | All products rehashed | Receipt bytes | Recorded commands with exit 0 |
|---|---|---:|---:|---:|---:|
| [render01 receipt](floor-model-render01/receipt.json) | summary 11, 137, 138, 139, 140, 141 | 6 | 28 | 40,091 | 7 |
| [render02 receipt](floor-model-render02/receipt.json) | summary 135, 136; component 3, 7, 8, 9, 10, 49 | 8 | 40 | 53,435 | 9 |
| [render03 receipt](floor-model-render03/receipt.json) | component 76-81 and 117-132 | 22 | 96 | 122,795 | 23 |

Receipt SHA-256 values, independently recomputed:

- render01: `a9575f0162ecdc35a13a9c82a5633945d882a5e343868d0c1d46aed58416e511`
- render02: `fa533cf3031ace6e3de3ec09e6bc78ae33bca7a72c804febdef5653dfc7942d6`
- render03: `7afc2b9f92789882fbf1c1ab05fb451982a40e0978287333372ea8d7440f40b7`

The product counts include images, extracted-text files, rendering/parser/version
logs, font configuration and any receipt-listed font-cache files. Every listed
product's actual size, SHA-256 and resolved path matched its receipt. The actual
file inventory of each batch directory equaled its listed products plus its
receipt; no missing or extra files were found. Receipt page order/membership
matched the separately declared lists above.

All 36 PNGs passed PNG signature/IHDR checks, Pillow `verify()` followed by a
fresh `load()`, expected dimensions, RGB mode, single-frame status and exact
SHA-256 of decoded pixel bytes against the receipt's `pixel_sha256`. PNG headers
were 8-bit truecolor. Source PDF geometry was accessed only for those 36 pages.

## Native geometry

All selected pages have equal MediaBox and CropBox, origin (0, 0), rotation 0
and UserUnit 1. Expected dimensions were calculated independently with exact
fractions as `ceil(page_points * 200 / 72)` for each dimension, accounting for
rotation in the checker. No crop or rescaling command was present.

| Source and physical pages | Page dimensions, points | Native PNG pixels |
|---|---|---|
| summary 11, 135, 141 | 561 x 766 | 1559 x 2128 |
| summary 137, 139 | 561 x 765 | 1559 x 2125 |
| summary 136, 138, 140 | 561 x 770 | 1559 x 2139 |
| component 3, 7-10, 49, 76-81, 117-132 | 612 x 792 | 1700 x 2200 |

## Commands, diagnostics and actual outcomes

The checker was run as an inline, read-only, stdout-only program through:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -
```

It imported only standard-library modules, Pillow and pypdf, not the renderer or
other investigation code. Runtime: Python 3.12.14 (Clang 22.1.3), pypdf 6.10.0,
Pillow 12.3.0. The inline checker is preserved in the task tool-call history,
not as a separate repository program or independently pinned script.

For each saved rendering command, the checker compared the complete argument
list to the declared page, source and output prefix using this recorded form:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f PAGE -l PAGE -singlefile -r 200 -png SOURCE OUTPUT_PREFIX
```

`PAGE`, `SOURCE` and `OUTPUT_PREFIX` above are explanatory placeholders; the
actual receipt argument arrays were checked exactly, not re-executed. Each
receipt also contains one `pdftoppm -v` command, explaining the command counts
of 7, 9 and 23 for 6, 8 and 22 renderings. All recorded exit codes are 0.

- The actual 12, 16 and 44 per-page stdout/stderr files are empty: **72 empty
  rendering logs** total.
- All three `parser.stderr` files are empty; all three recorded warning arrays
  are empty.
- Each version command has empty stdout and a 144-byte stderr banner identifying
  Poppler/pdftoppm 26.05.0 and its copyright notices. The banner was read and is
  not a rendering warning; it would be inaccurate to call all stderr files empty.
- Fresh PDF/PNG checking emitted no captured Python warnings or pypdf logger
  diagnostics in the successful run.
- Each receipt's recorded input-before list equals its input-after list. The
  source entries were freshly checked against actual files. **Seven non-source
  dependency entries per receipt were not freshly rehashed**; equality of their
  recorded pins is not an independently verified or hermetic dependency closure.
- No renderer was rerun. Matching receipts/pixels/geometry does not independently
  establish visual fidelity to a newly rendered PDF or correctness of extraction.

The first attempt, tool chunk `f50d54`, exited 1 because the verifier itself
opened hash/header files without explicitly closing every handle, triggering
ResourceWarnings under its strict warning check. It did not reach a completed
before/after result and is **not counted as a pass**. No files were written.
The corrected checker used file-handle context managers and closed readers;
it then checked all three batches together, tool chunk `5bb93f`, exit **0**,
reported wall time about **1.27 seconds**. All source, receipt, product,
page-membership, geometry, PNG and diagnostic assertions passed without
relaxing their conditions.

The successful before/after snapshot covers 169 files and was unchanged. Its
digest is `bf52f9a1e3204a425eefe904b3d2d292631e37d1f62c8f92e14e89ba925c515e`,
computed over compact, sorted-key JSON mapping absolute paths to byte counts
and SHA-256 values. This is a digest of the check's local inventory, not a new
historical provenance seal or an independently saved full snapshot artifact.

## Earlier public metadata locator: exact search record

This section records the prior bounded metadata pass; no queries were repeated
during the artifact check. Exactly two queries were submitted once each with
`domains: ["nist.gov"]`:

1. `"floor truss" "finite element" "NCSTAR"`
2. `"Component, Connection, and Subsystem Structural Analysis" "2005"`

Three official HTML pages were opened successfully:

- [Final publication catalog](https://www.nist.gov/publications/component-connection-and-subsystem-structural-analysis-federal-building-and-fire-0): all 168 returned lines; metadata at 114-155. Exact final title is *Component, Connection, and Subsystem Structural Analysis. Federal Building and Fire Safety Investigation of the World Trade Center Disaster (NIST NCSTAR 1-6C)*; date December 1, 2005; download/citation `pub_id=101043`. The separate report-number field says `1-6`, despite `1-6C` in the title.
- [DOI catalog](https://www.nist.gov/publications/component-connection-and-subsystem-structural-analysis): all 166 returned lines; metadata at 115-153. DOI `10.6028/NIST.NCSTAR.1-6c`; report number `NIST NCSTAR 1-6c`; date January 1, 2005. Author spellings/order differ from the other catalog and were not silently reconciled.
- [Final-report index](https://www.nist.gov/el/final-reports-nist-world-trade-center-disaster-investigation): first return reached line 191; one continuation exposed the NCSTAR 1-6C entry at 204 and final-release heading at 157, which says September 2005. The three displayed dates remain separately attributed.

The final catalog's author list, retaining catalog spelling, is Mehdi S.
Zarghamee; S Bolourchi; D W. Eggars; Omer O. Erbay; F W. Kan; Y Kitane;
P R. Barrett; John L. Gross; Therese P. McAllister; A A. Liepins; M Mudlock;
W I. Naguib; R P. Ojdrovic; Andrew T. Sarawit.

Search results also supplied final PDF leads for 1-5G (`101039`) and 1-6D
(`101366`), and the separately labeled 1-6C draft (`909153`). The search service
automatically displayed extended PDF snippets; no PDF was opened/downloaded
by this locator and those snippets were not treated as reviewed report content.
There were no failed network routes. The exact final-PDF locator handed to root
was `https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=101043`; subsequent
root acquisition/content review is a separate activity from this metadata pass.

Metadata identified a final-report candidate. It did not establish the specific
four-test comparison, prediction/calibration history, available native inputs,
validation criteria or transferability to WTC 7. Those questions remain for the
separately attributed scientific source review and reproducible model work.

## Separate render04 interval: final eight declared pages

September 28, 2026, appended after the preceding check. This is a **separate
42-file before/after interval**, not an expansion or replacement of the earlier
169-file interval. The earlier record above is unchanged. Root declared the
eight-page extension before rendering, then notified this verifier of terminal
exit 0 and the receipt pin before any render04 artifacts were inspected.

Exact page membership is component physical **109, 110, 111, 112, 113, 114,
115 and 133**. No page content was displayed, interpreted or extracted by this
verifier. Geometry access was restricted to those eight PDF pages. Existing
text products were hashed as opaque bytes, not read as text. No new searches,
downloads, source files, renderer execution or scientific-source expansion
occurred in this check; only this appendix was added to the verification note.

Results:

- Source `ncstar-1-6c-source01.pdf`: **8,363,877 bytes, 252 pages**, SHA-256
  `aab90082f22baaa41ed8dd22c89192040aa6f629b0cc800d1b47f07a5c7ef411`,
  freshly verified. Encryption flag true; empty-password return value 1.
- [render04 receipt](floor-model-render04/receipt.json): **52,581 bytes**, SHA-256
  `972c8cbb8cfdd2bbf38925cb601e4d1245ab62e4764c5095aa0f868e5ef62767`.
- All **40 listed products** matched their actual sizes, hashes and resolved
  paths. The directory's actual file inventory equaled those products plus its
  receipt. Page membership/order matched the eight separately declared pages.
- All **8 PNGs** passed signature/IHDR checks, Pillow verification and fresh
  complete decoding, RGB single-frame mode, exact native dimensions and decoded
  pixel hashes against the receipt. All were 8-bit truecolor **1700 x 2200**.
- Each selected PDF page has MediaBox = CropBox = `(0, 0, 612, 792)` points,
  rotation 0, UserUnit 1. Exact-fraction, ceiling-rounded 200 dpi dimensions
  matched the PNGs. The complete recorded render arguments matched the stated
  source, page and output prefix with no crop flag.
- All **9 recorded commands** have exit 0: eight page renderings and one version
  command. All **16 per-page stdout/stderr files** and `parser.stderr` are empty.
  The version command's stdout is empty; its 144-byte stderr is the normal
  Poppler/pdftoppm 26.05.0 banner, not a rendering warning. The receipt's warning
  array and the fresh checker's captured Python/pypdf diagnostics were empty.
- Recorded input-before and input-after lists matched. The source pin was
  freshly checked; the **seven non-source dependency pins were not freshly
  rehashed**, as in the earlier check. No claim of hermetic dependency coverage.

Actual command: the same bundled `python3 -B -` inline, read-only, stdout-only
method described above, scoped to this batch's declared pages and receipt
pin. Runtime remained Python 3.12.14, pypdf 6.10.0, Pillow 12.3.0. Tool chunk
`d06a5a` exited **0**, reported wall time about **0.38 seconds**, with no failed
attempt in this additional check.

The 42-file snapshot comprises one source PDF, one receipt and 40 products.
Before/after bytes and hashes were identical; snapshot digest under the same
compact sorted-key JSON convention is
`7a210a8d4d395fc2ac64ae0be5a18b61ffa18ce0f1f545d0a66a36a70cbca958`.
The PDF is shared with the earlier interval: these are not 211 independent
files or one combined observation window. This appendix verifies saved
representation integrity only, not scientific correctness, model validity,
historical authenticity or fidelity to an independently rerendered PDF.
