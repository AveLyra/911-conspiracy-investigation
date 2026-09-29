# Thermal-property pages: independent artifact verification

September 28, 2026. Research only. This verifies selected saved derivatives and
held-source integrity, not source content, original experiments, native model
execution, historical authenticity or scientific adequacy.

## Scope and controls

Main AGENTS/WORKFLOW/START-HERE and the main investigation CHARTER were reread,
along with the evidence-falsification-auditor, source-of-truth-guardian and PDF
skills and relevant evidence/source checklists. The
[prospective crosswalk scope](thermal-property-source-crosswalk-2026-09-28.md)
limits this unit to 26 selected pages from the held NCSTAR 1-6A source.

The checker waited until root reported renderer session 59781 terminal exit 0
and supplied the receipt pin. No new receipt or product was inspected before
that notice. Root and the separate source reader own the scientific reading;
this checker did not read their findings or interpret source pages.

Exact PDF geometry and image coverage: physical **115-126, 171-174 and
305-314**, in that order, with receipt source label `6a`. This is not a
whole-report content review. Old TN1771 images, any source-reader rereads and
all earlier derivative batches are **outside this verification interval**.

Only this new note was written. No source, existing derivative, receipt,
renderer, model, drawing, other research note or legal/main record was edited.
There was no network request, acquisition, renderer import, rerender, PDF text
extraction, image display, graph tracing, simulation, stage, commit, push or
external transfer. Existing text products were hashed as opaque bytes, not
read as text; PNG decoding for hashes was not visual/content review.

## Verified source and receipt

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `ncstar-1-6a-source01.pdf` | 22,813,796 | `75b910620ee9c9f202256acd898f01f28a0df23546132c2108a2a1735cb021b3` |
| [render receipt](thermal-property-render01/receipt.json) | 139,610 | `21d1df4b9ad38fbe51e29a41cadcedd8629f1ec572e310badd349dbcdee224b1` |

Actual byte counts and SHA-256 values matched. Pypdf reports the PDF
unencrypted and containing **328 pages**. Only the 26 selected page geometries
were inspected; no page-content extraction was performed. Receipt page order,
membership and source label matched the independently specified list, with no
missing or duplicate page. The receipt's source pin matched the actual PDF.

## Product, image and geometry checks

All **108 receipt-listed products** matched their actual byte counts,
SHA-256 values and resolved paths. Product paths stayed within the declared
render directory. Its actual file inventory equaled the listed products plus
its receipt: no missing or extra files. This includes images, extracted-text
products, per-page/parser/version logs and font configuration.

All **26 PNGs** passed:

- PNG signature/IHDR checks, including 8-bit truecolor headers;
- Pillow `verify()` followed by a fresh open and full `load()`;
- RGB mode, single-frame status and the recorded native dimensions;
- exact SHA-256 of decoded pixel bytes against the receipt's `pixel_sha256`;
- independent dimensions computed from the selected source page geometry.

Every selected source page has MediaBox = CropBox = `(0, 0, 565, 765)` points,
rotation 0 and UserUnit 1. At the recorded **200 dpi**, every PNG is
**1570 x 2125 pixels**. The checker used exact fractions and ceiling rounding,
`ceil(page_points * 200 / 72)`, with explicit rotation handling. The exact
recorded rendering arguments contained no crop flag.

## Actual command and diagnostics

The independent, read-only, stdout-only checker ran inline through:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -
```

It imported only standard-library modules, Pillow and pypdf, not renderer or
investigation code. File-handle context managers and explicit reader/image
closure were used. Runtime: **Python 3.12.14** (Clang 22.1.3), **pypdf 6.10.0**,
**Pillow 12.3.0**. The full inline command remains in the task's tool-call
history, not a separately saved or pinned verification program.

For each page the checker compared the complete saved argument array against
the exact source, page and output prefix, using this recorded form:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f PAGE -l PAGE -singlefile -r 200 -png SOURCE OUTPUT_PREFIX
```

Uppercase terms are explanatory placeholders. Actual arrays were checked;
the renderer was not executed. All **27 recorded commands** have exit 0:
26 page renderings and one `pdftoppm -v` command.

- All **52 per-page stdout/stderr files** and `parser.stderr` are actually empty.
- The receipt's warning array is empty. Fresh checking emitted no captured
  Python warnings or pypdf logger diagnostics.
- Version-command stdout is empty. Its **144-byte stderr** was read and contains
  the normal Poppler/pdftoppm **26.05.0** banner and copyright notices, not a
  rendering warning. Not all stderr files are empty.
- Recorded input-before and input-after lists agree. The source pin was freshly
  checked. **Seven non-source dependency pins were not freshly rehashed**:
  the two renderer modules, pdftoppm executable, input font configuration,
  Python executable and Pillow/pypdf package entry files. Their recorded-pin
  equality is not an independent dependency audit or a hermetic-runtime claim.

Actual checker result: tool chunk `288208`, **exit 0**, reported wall time about
**0.98 seconds**. All source, receipt, inventory, page-order, PNG, geometry,
command-record and diagnostic assertions passed. There was no failed checker
attempt in this unit. No acceptance condition was relaxed.

## Exact interval and limitations

One before/after interval covered **110 distinct files**: the source PDF,
receipt and 108 products. Actual sizes and hashes were unchanged. The compact,
sorted-key JSON snapshot mapping absolute paths to sizes and SHA-256 values
has digest:

`9f4b42514eef847c78f346e4ee5d8a9a0c98f84c9a27bfee68244cc79415e363`

The full inventory existed within the checker; only its digest is recorded
here. This is not a separately preserved full snapshot or an attestation about
the files before acquisition or after this interval. The source PDF was held
before this unit; rechecking its bytes does not independently authenticate the
earlier transport, publisher identity or historical source provenance.

No TN1771 artifact was added to this interval. Shared source files and repeated
checks across earlier stages are not independent historical observations.
Matching hashes, pixel bytes and geometry do not independently verify rendering
fidelity against a fresh PDF render, correct text extraction, material-property
formulae or test results, native inputs actually executed, calibration status,
structural response, or a WTC 7 causal conclusion. Those are separate source,
method and model questions, not results of this artifact check.

## Separate render02 interval: physical page 127

September 28, 2026. Appended after root prospectively declared physical127
to complete the interrupted subsection and reported the one-page render
terminal exit 0. This is a **new, separate 10-file interval**, not part of the
earlier 110-file interval. The preceding 7,016-byte verification record is
preserved unchanged, SHA-256
`07e48eed7b820c730d094abc565dbcb54df762146c2629fbe70798224309ae72`.

Only `thermal-property-render02`, its receipt and the same held source PDF
were checked. Exact receipt membership is source label `6a`, physical page
**127 only**. No content was displayed, extracted or interpreted. This checker
does not independently certify the printed page label, subsection content or
scientific implications. No previous batch or TN1771 artifact was rechecked
or added to this interval.

- Source pin freshly matched: **22,813,796 bytes, 328 pages, unencrypted**,
  SHA-256 `75b910620ee9c9f202256acd898f01f28a0df23546132c2108a2a1735cb021b3`.
- [render02 receipt](thermal-property-render02/receipt.json): **15,238 bytes**,
  SHA-256 `deb31251a6659031c699ea30b63164f3051a74c6231d00bd617dd7459af323db`.
- All **8 products** matched actual size, SHA-256 and resolved path. The actual
  directory inventory equaled those products plus the receipt, with no missing
  or extra file. The existing text derivative was hashed as opaque bytes.
- The **one PNG** passed signature/IHDR, 8-bit truecolor, Pillow verification
  and fresh complete decoding, RGB single-frame status, native dimensions and
  decoded-pixel hash agreement with the receipt.
- Only source physical127's geometry was checked: MediaBox = CropBox =
  `(0, 0, 565, 765)` points, rotation 0, UserUnit 1. Exact-fraction 200 dpi
  dimensions matched **1570 x 2125 pixels**.
- Both recorded commands have exit 0: one exact page/source/output rendering
  command, with no crop flag, and one version command. The **two page-render
  stdout/stderr logs** and `parser.stderr` are empty. Version stdout is empty;
  its144-byte stderr is the normal Poppler/pdftoppm26.05.0 banner. Recorded
  warnings and fresh captured Python/pypdf diagnostics are empty.
- Recorded input-before/input-after lists match, and the source entry was
  freshly verified. The same **seven non-source dependency pins were not
  freshly rehashed**; no expanded dependency or hermetic-runtime claim.

The independent command was the same bundled `python3 -B -`, inline,
read-only, stdout-only method described above, scoped to this one page and
receipt. It imported no renderer, used explicit handle closure, and did not
rerender. Runtime remained Python3.12.14, pypdf6.10.0, Pillow12.3.0. Tool chunk
`3233bd` exited **0**, reported wall time about **0.16 seconds**; no failed
attempt occurred in this additional check.

The 10-file snapshot comprises the source PDF, receipt and eight products.
Actual sizes and hashes were unchanged before/after. Snapshot digest under
the previously described compact sorted-key JSON convention:
`8257ab41466c2e629eb72d6b52e4a6b39483de2016a9621bd136b297d37357f3`.
The source is shared with the earlier interval; these are not 120 distinct
files or one combined observation window. The snapshot's full mapping was
not independently saved. All prior authenticity, transport, rendering-fidelity
and scientific limitations remain. Only this appendix was added to this note;
no source, derivative or other record was changed.
