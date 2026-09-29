# Restraint follow-through: actual execution receipt

September27,2026. Source reading/derived display only; no solver, curve tracing,
historical measurement, human acceptance or legal promotion.

## Sources and transport

| Preserved source | Bytes | SHA-256 | Physical pages |
|---|---:|---|---:|
| [Progress compilation](../pub-860567-source01.pdf) |48124241|449cba29b3a8f1727f12866aca8ea0491d9f3c634746942390a5ef53928c0655|1095|
| [Final volume1, held](../ncstar-1-6v1-source01.pdf) |23824565|9874df97f3ce7bffb048fa9390823599f733cfed5549ca14b934a126f62240d4|270|
| [Final volume2, new](../ncstar-1-6v2-source01.pdf) |19845494|cfc847c22beebfc87ff5e15af5c604f945f2ff1b6d9e62c16b381e10ae8a4f43|208|

Official new-source URLs:
`https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=860567` and
`https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-6v2.pdf`.
Create-only guarded transport used `test ! -e DEST && curl --fail --location
--max-time 60 --silent --show-error --output DEST --write-out 'HTTP
%{http_code} TYPE %{content_type} BYTES %{size_download} FINAL
%{url_effective}\n' URL`. Exact targets are the table's new-source paths;
no existing file was overwritten. Sessions91363 and74351 were polled to
terminal exit0 before parsing, HTTP200, unchanged finalURLs. MIME types were
`application/pdf;charset=UTF-8` and `application/pdf`, respectively.

## Parsing/rendering and actual scope

Read-only parsing used bundled Python3.12.14/pypdf6.10.0 via `python3 -B -`
stdout-only scripts. Metadata dates are digitization/file dates, not report
dates. Exact declared text and visual coverage is in the
[source note](../restraint-followthrough-2026-09-27.md).

Public split-volume v2 starts substantive Chapter7 at physical3. Its initial
1–16 extraction complied with the numeric range but missed the front-matter
purpose, exposing unrelated3–16 text. Those results were not used. The source
note explicitly retains this scope mismatch; it was not a successful
front-matter-only read. Corrected locator used held v1front matter/page labels,
then exact v2physical147–149. No whole-document body search was run.

Rendering used bundled Poppler at
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm`,
with `FONTCONFIG_FILE` pointing to the existing audit
`protection-render01/fonts.conf`. Per-page flags were `-f PAGE -l PAGE -r160
-singlefile -png SOURCE PREFIX` (actual command separated `-r 160`), guarded
against an existing output. No cropping. Sessions70365,8739,56479 all terminal
exit0, no diagnostics. Exact image selection:

- Progress:1–5,10–12,46,146–147,152–153,710–714,733–738,744–745;
  `progress-{page}.png`,26files. Root completed all26;17were completed on this
  continuation, not rerendered.
- Final v1:5,14; `final-v1-{page}.png`,2files.
- Final v2:1,147,148,149; `final-v2-{page}.png`,4files.

Root read all32 complete images. Separate reader covered13progress pages
(1,11,147,710,714,733–738,744–745) and all6final images, independently freezing
findings before synthesis. No numerical curve coordinates were extracted.

## Independent artifact checks

Two read-only stdout-only scripts used bundled Python3.12.14, pypdf6.10.0,
Pillow12.3.0: expected PDF size/hash/count, selected page geometry only,
Pillow `verify()` then fresh-open full `load()`, format/mode/frame count,
ceil(width/height in points×160/72), and before/after size/mtime/SHA-256.
Both commands exited0 with no errors. All35unique artifacts remained unchanged
within their respective verification intervals, not a later combined recheck.

All26progress PNGs are single-frame RGB1360×1760, with selected source
MediaBox=CropBox612×792pt. The6final images are:

| Source/page | Source MediaBox=CropBox points | Expected/observed pixels |
|---|---|---|
|v2/1|580×764|1289×1698|
|v2/147|567×765|1260×1700|
|v2/148|567×767|1260×1705|
|v2/149|567×765|1260×1700|
|v1/5|561×765|1247×1700|
|v1/14|561×767|1247×1705|

Selected rotations0/UserUnit1. Both final PDFs and progress PDF unencrypted.
These checks verify integrity, decoding and geometry, not pixel-content
identity to the source, historical authenticity, scientific execution or
physical validity. Main's visual read is a distinct inspection.

## Searches/failures retained

Earlier independent metadata pass: exactly two NIST-domain queries, zero
HTML opens; no independently resolved edition date. Current root refined
query: one NIST-domain query, returning only the existing June2004minutes;
no additional opens. Search excerpts were not counted as complete PDF reads.
Exact strings and coverage are in the note.

A web-tool open of the official v2PDF failed its19.8MB size limit; there was
no retry or claimed successful web read. The separate local acquisition
had already completed successfully. Local filename/Markdown searches were
bounded discovery, not global source-absence tests. A guessed
`alteration-render01/verification.md` and later guessed investigation README
paths did not exist; these failed read-only lookups caused no mutation and
are not evidence of a missing scientific source. A combined instruction
display was truncated; charter/PDF instructions were subsequently read in
bounded complete outputs before continuing substantive work.

No new original drawing/private production access, solver, human-gate
substitution, publication, outreach, canonical fact, legal amendment,
staging, commit or push. All sources/derivatives remain research WIP.

## Integrated documentation check

Separate scientific draft review corrected individual-draw/profile-set
wording, tightened the execution ceiling and clarified next-test boundary
conventions. The originating metadata/artifact reviewer confirmed its own
attribution. Both read the complete draft/receipt and verified six local
targets, zero missing, exit0; external targets were not tested. These are
not another independent search, acquisition or experimental verification.

Root `awk` checked all seven touched Markdown files for trailing whitespace
and conflict markers: PASS. `wc -c` and `shasum -a 256` matched the three PDF
pins above; `git diff --check` exited0. Main's tracked dirty-file listing was
unchanged. A failed multi-file navigation patch had applied none of its
first two hunks; subsequent explicit patches saved the intended updates.
No failed action is counted as successful. No original/source file changed.
