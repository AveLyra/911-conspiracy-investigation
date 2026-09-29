# Methodology-slide derivative verification

September27,2026. Scope and source identity belong to
[native-input follow-up](../gap-study-input-followup-2026-09-27.md).

Prospective render selection: physical1–29 of the acquired42-page presentation,
200dpi, individual full-page PNGs, create-only output guards. Do not inspect
30–42 by implication. No curve digitization or source-pixel measurements.
Actual execution, artifact checks and reading coverage will be appended below.

## Actual acquisition and rendering

The source HTML download returned session13415; the linked PDF returned84784.
Both were polled to terminal exit0 before parsing. Each used a create-only
`test ! -e` destination guard followed by `curl --fail --location --max-time 60
--silent --show-error --output <new-path> --write-out <http/type/bytes/final-url>
<declared-url>`. Source-specific URLs, HTTP/content types, sizes and SHA-256
values are in the linked note. These transport responses do not authenticate
the historical document or the simulations it describes.

Metadata/page count and physical1–3 text were inspected first. Physical4–18
and19–29 were separately declared before text extraction. No physical30–42
text, image or content inspection occurred. Source page count is42; unencrypted.
PDF creation/modification metadata both say `D:20040901105638-04'00'`; producer
Acrobat Distiller5.0.5 and creator PScript5.dll5.2.2. Cover/link-date differences
are preserved in the note, not resolved from metadata.

Actual bundled tools:

- Python: `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`, version3.12.14, invoked with `-B`.
- pypdf6.10.0 and Pillow12.3.0.
- Poppler: `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm`.
- Existing font configuration: `../protection-render01/fonts.conf`.

For each declared page1–29, the guarded command had this form, with explicit
absolute source/output/font paths in actual execution:

```sh
FONTCONFIG_FILE=<existing-font-config> <bundled-pdftoppm> -f <page> -l <page> -r 200 -singlefile -png <source-pdf> <this-directory>/slide-<page>
```

The render batch returned session24212 and was polled to terminal exit0,
without diagnostics, before image review. No output was overwritten. These
are full-MediaBox renders; the command does not request CropBox clipping.
No fresh rendering replay was performed during this unit.

## Independent artifact verification

A separate read-only verifier ran `wc -c`, `shasum -a 256` and a bundled
Python `-B` script. Both source pins matched:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| minutes HTML |198270|`04646c9d3291085a87d6ead8cfb02022a95a56d2a90c381b90a9a31ac761ee3a`|
| presentation PDF |2873713|`15c07d18c21c6242bffa139ebb5493ec0da30864d6b9648365903d19301068db`|

All29 selected PNGs passed Pillow `verify()` and a fresh-open full `load()`:
PNG, RGB, single frame,2200×1700 pixels. Selected PDF pages1–29 have MediaBox
`[0,0,612,792]`, CropBox `[36,36,576,756]`, rotation90°. Raster dimensions agree
with200dpi full-MediaBox rendering after rotation, **not** CropBox rendering.
Do not copy the unrotated/full-crop geometry from earlier report receipts.

All31 artifacts retained size, modification time and SHA-256 before/after that
check. Commands exited0 without diagnostics. The verifier parsed only PDF
metadata/geometry, not content, and did not rerender. It separately isolated
the two minutes disclaimer paragraphs and twelve insulation-section paragraphs
with HTMLParser and confirmed the exact presentation href. It did not independently
resolve the href's network redirect; root's acquisition recorded that finalURL.
This is integrity/format verification and the stated HTML-section check, not
an independent presentation-content or scientific audit.

After resumption, root again read/hash-checked both source files and obtained
matching sizes/SHA-256, page count and metadata. The initial literal disclaimer
locator (`These minutes`) returned no match; root then read the actual two
disclaimer paragraphs. A character-count section preview exposed the beginning
of the following section and was replaced by an exact next-heading bound.
No conclusion relies on that excess text. The earlier long-line/truncation
failure is also retained in the main note.

## Visual reading and limits

Root visually inspected all selected physical1–29, across the interrupted unit:
1–17 before the coordinate-response turn,18–29 after it. Each complete page was
displayed; tools resized2200×1700 to1780×1376, including original-detail requests
earlier in the unit. No source-pixel measurement was attempted. The displayed
page5 photo was not treated as blank because text extraction was empty.
Charts were read qualitatively with titles, axes and legends retained; no
digitization, fitted equivalence criterion or numerical simulation was performed.

Selected-page coverage is not full-deck coverage. Render success and separate
decoding do not establish original observations, representative sampling,
thermal-model validity or historical WTC7 applicability. No live download,
render process or browser viewer remains claimed from these terminal handles.
