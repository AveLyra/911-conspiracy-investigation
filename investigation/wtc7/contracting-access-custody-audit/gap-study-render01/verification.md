# Gap-study acquisition, render and review receipt

September27,2026. These are public-report reading derivatives, not a thermal
simulation or an independently authenticated historical condition record.
Scientific interpretation and PDF byte/hash pins are in the
[applicability audit](../gap-study-applicability-2026-09-27.md).

## Executed acquisition and rendering

Official-source locator queries, before acquisition:

1. `site:nist.gov "NCSTAR 1-6" "gaps" "plate"`
2. `site:nist.gov "NCSTAR 1-6A" "Chapter 5" thickness`
3. `site:nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-6.pdf`
4. `site:nist.gov "Structural Fire Response and Probable Collapse Sequence of the World Trade Center Towers" "1-6"`

The third query did not establish a usable report URL; the title query located
the volume1 URL used below. Final and draft landing pages were distinguished;
no unsuccessful locator or unacquired alternate edition supplied a scientific
result. These searches locate the reports, not native study inputs.

Two create-only official downloads used `test ! -e <exact target> && curl
--fail --location --max-time 60 --silent --show-error --output <exact target>
--write-out <HTTP/type/bytes/final-URL fields> <official URL>`. Sources:

- `https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-6a.pdf`
- `https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-6v1.pdf`

Download sessions69417 and81471 were polled to terminal exit0 before parsing.
Both returned HTTP200,`application/pdf` and the same final URL. The first
source has328 physical pages; the second270. Both are unencrypted. Metadata
processing dates in2015 are not publication or event dates.

After the scope/page declaration, Poppler rendered each selected page using
the existing `protection-render01/fonts.conf` as `FONTCONFIG_FILE`. Executed
command form (each output also guarded by a no-existing-PNG test):

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f <physical page> -l <same page> -r 200 -singlefile -png <exact source PDF> <new output prefix>
```

Selected prefixes: `n6a-3`, `n6a-103` through `n6a-114`, `n6-5`, `n6-109`
through `n6-114`. Batch sessions35458 and38779 reached terminal exit0 with
no diagnostics before their images were opened for review. No render replay
was run in this unit; file-integrity and decode checks are a separate check.

## Independent artifact check

The independent checker ran one read-only inline script with:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B - <<'PY'
```

The script used Python3.12.14, pypdf6.10.0 and Pillow12.3.0. It compared exact
PDF size/SHA-256 pins; parsed metadata/page count and only the20 selected page
boxes/rotations; called `Image.verify()` then fresh-open `load()` on every PNG;
and compared size,mtime and SHA-256 before/after for all22 artifacts.
Terminal exit0; no diagnostics or failed assertions. No source-text extraction
or new page content was inspected by this artifact check.

| Selected images | PNG geometry | PDF geometry check |
|---|---|---|
| `n6a-3.png` |1570×2128|Matches selected page at200dpi|
| `n6a-103.png` through `n6a-114.png` |1570×2125|Matches each selected page at200dpi|
| `n6-5.png`, `n6-109.png`, `n6-111.png`, `n6-113.png` |1559×2125|Matches each selected page at200dpi|
| `n6-110.png`, `n6-112.png`, `n6-114.png` |1559×2139|Matches each selected page at200dpi|

All20 PNGs fully decode as RGB,single-frame. Every selected PDF page has
MediaBox=CropBox and rotation0. Both PDF pins match the audit table; all22
artifacts remained unchanged during the check. This establishes copy identity,
geometry and decoding, not independent page-content/render equivalence,
historical authenticity, complete directory inventory or scientific validity.

## Actual reading and display limits

Root read all20 complete page images, including the two title pages and blank
printed62 in1-6A. Printed footers confirm the physical/printed mapping. Although
original detail was requested, the display resized the PNGs to1344 pixels wide
(heights1819/1821/1831/1843 according to source). Readable text and the complete
figures were reviewed; no pixel measurement, graph digitization or color-based
curve identification was performed. The scan's grayscale appearance does not
establish the colors referred to by its captions.

The separate source reader also inspected all20 complete images and exact-page
text, then froze findings before opening the FAQ excerpt and root synthesis.
Shared scope and root progress messages mean this is not a blinded experiment.
The reviewer subsequently checked the bounded FAQ excerpt and whole draft;
the parent audit records the substantive wording corrections. Both PDF pins
and the FAQ HTML pin were freshly confirmed by that reader. No actual-human
acceptance or independent numerical reproduction is implied.
