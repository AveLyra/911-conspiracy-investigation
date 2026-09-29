# Furnace-sag claim pages: artifact-only verification

2026-09-28. **Pass within the checks below.** This is local representation and
file-integrity verification, not source-content review, scientific validation,
historical authentication or proof that a recorded command was historically run.
No renderer, source, existing derivative or prior note was edited. No network,
native model, drawing, raw/private production or legal record was accessed.

## Scope and inputs

Read the complete prospective
[claim-trace note](furnace-sag-claim-trace-2026-09-28.md) and
[render receipt](furnace-sag-render01/receipt.json). Main controls/CHARTER and the
evidence-falsification, source-of-truth and PDF skills govern this narrow check.
Only PDF page count and geometry metadata were parsed; no PDF body text was
extracted or scientifically interpreted. Complete image decoding below is not
claimed as visual review of page wording or figures.

The receipt SHA256 matches the supplied expected pin:
`9df8ffc838b3115c99121fd67b797a4bff607166a89e34300b4b3321a250d3b7`.
Its selected pages are exactly `summary` 138/139 and `final` 148/149, in that
order. The four command records map to those source volumes, pages and PNG
output stems, with single-page 200-dpi PNG arguments.

| Source | Bytes checked | Physical page count checked | SHA256 |
|---|---:|---:|---|
| NCSTAR 1-6 v1 | 23,824,565 | 270 | `9874df97f3ce7bffb048fa9390823599f733cfed5549ca14b934a126f62240d4` |
| NCSTAR 1-6 v2 | 19,845,494 | 208 | `cfc847c22beebfc87ff5e15af5c604f945f2ff1b6d9e62c16b381e10ae8a4f43` |

## Actual checks and results

The two stdout-only checking invocations were
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -`
with the bounded Python here-document checks described below. Both returned
exit 0; no files were written by either check. Runtime: Python 3.12.14,
Pillow 12.3.0, pypdf 6.10.0.

1. First check (tool chunk `4d76d2`, reported command time 0.635 s): used
   `hashlib.sha256`, byte lengths and `Path.resolve()` on every recursively
   recorded file-pin object. All **56 pin occurrences**, representing **29
   unique files** (9 inputs and 20 products), agree with disk; duplicate pin
   records agree with each other. Recorded before/after input arrays are equal.
   The output directory's files are exactly those 20 products plus its receipt.
   The current hashes/lengths/resolved paths of all 29 files and the receipt
   bytes were rechecked at the end: **30 files unchanged** during this check.
2. The same check loaded each PNG completely with `Image.load()`: **4/4 are
   single-frame PNG, RGB**, with dimensions and raw `Image.tobytes()` SHA256
   matching the receipt. All four selected PDF pages have equal MediaBox and
   CropBox, rotation 0 and UserUnit 1. Dimensions equal the ceiling of their
   point extents times 200/72, as shown below.
3. The receipt records five exit-0 commands: four renders and the version
   query. All four render stdout/stderr pairs and the parser-stderr artifact
   are empty. The 144-byte version stderr is a normal `pdftoppm version
   26.05.0` banner, not a rendering failure. Receipt warnings are empty. This
   independent page-count/geometry parse emitted **0 stderr bytes, 0 pypdf log
   bytes and 0 caught warnings**. No render was rerun.

| Volume / physical page | MediaBox = CropBox (points) | Decoded pixels | Pixel SHA256 |
|---|---|---|---|
| v1 / 138 | 0,0,561,770 | 1559 × 2139 | `09ad2d6dc3508639fa562c9dbdbb840d1d051148216c0fb7e646b90d582f7d5a` |
| v1 / 139 | 0,0,561,765 | 1559 × 2125 | `0f8c58ae1875d72b5096b4b8125a0f12b1da79366df599e4583e491def6621f2` |
| v2 / 148 | 0,0,567,767 | 1575 × 2131 | `0d45bd7edd2a0833f1db08eea8b940a015dcf08240c379330c21a8583d32d230` |
| v2 / 149 | 0,0,567,765 | 1575 × 2125 | `4841aa6bc9d941a50d62d207a0de5b7df837d68176efd4d98e4a57a7d4e5f42b` |

The optional old/new v1 comparison used filename-only discovery:

```text
rg --files /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/contracting-access-custody-audit -g '*138*.png' -g '*139*.png'
```

That command returned only the two current and two prior v1 images (chunk
`7d34b8`). The second Python check (chunk `70aeed`, 0.080 s) fully decoded and
compared `floor-model-render01/summary-page-138.png` and `-139.png` with their
same-named `furnace-sag-render01` counterparts. Both pairs are **byte-identical
and pixel-identical**; all four files remained unchanged during that check.
The paired PNG hashes are respectively
`6fe6d3c33249d720d7cfb3600b59593f0cefdcfab362166450ac81a10098a43a`
and `6927ba8a617094ea649d468d7d8154f5101dd857cdb303f958c3e2694d7b372d`.
No old v2 image comparison or other body range was opened. That same second
check confirmed all four receipt command source/output mappings explicitly.

## Failures and limits

No check failed, and no parser/decode warnings were observed. These checks do
not replay the renderer, authenticate the reports' historical provenance,
establish pixel-to-PDF rendering correctness by an independent implementation,
or provide a complete dependency closure. The prior-image equality is a
representation consistency check, not independent scientific corroboration.
The claim's scientific interpretation remains the source reader's and root's
separate work; this note does not endorse it.
