# Independent PDF preservation and render-integrity check

October 8, 2026. Scope: local preservation, frozen-roster reproduction and
decoded-image equality only. No scientific interpretation, source acquisition,
historical authentication, visual-content reading, expert review or human
acceptance was performed. Root/observer findings were not read.

## Result

**Pass for the declared integrity checks.** All 77 independently regenerated
PNGs are exactly byte-identical to the 77 held files in `render/`. Their decoded
RGB pixel arrays, dimensions and modes also match exactly. All are 910 x 1287;
total PNG bytes are 9,822,021. The held file roster has no missing or extra page.
Their individual hashes remained unchanged before and after this operation.

The source PDF begins with `%PDF-`, is 4,425,293 bytes, and has 207 pages according
to pypdf. Before and after rendering its SHA256 is:

`4066628f6c6a8b13f7fef63e1602a1b3eae807acbac7f032b67e68c1718a1543`

These checks bind the held source and derivatives. They do not establish the
PDF's historical authenticity, scientific accuracy or faithful authorial intent.

## Frozen roster and isolation

The page roster was transcribed from `PAGE-SELECTION.md` and
`SCOPE-EXPANSION.md`, not selected from scientific findings or discovered by
globbing the PDF. Physical one-based pages:

```text
1; 11-15; 33-34; 81-94; 114-138; 139-152; 153-154;
161-162; 166-171; 197-202
```

This is exactly 77 unique pages: the original 61 plus the declared 16-page
expansion. No other page was rendered or semantically read by this reviewer.

`mktemp -d /private/tmp/windsor-integrity.XXXXXX` created
`/private/tmp/windsor-integrity.QxjmlU` (receipt `58ef61`). The fontconfig file
and bounded driver were authored there with `apply_patch`. Font directories
were checked equal to the root render configuration: `/System/Library/Fonts`
and `/Library/Fonts`. The independent configuration uses only its own
`/private/tmp/windsor-integrity.QxjmlU/font-cache`; it does not use the root
temporary cache or the main user cache. Source, existing PNGs and earlier
diagnostics were never overwritten. Temporary products remain preserved.

## Commands and actual execution

The independent command was:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /private/tmp/windsor-integrity.QxjmlU/verify_render.py
```

It launched as tool session `12193` (receipt `b93dd4`). The same session was
polled to terminal exit 0 (`0b15d9`), not relaunched or assumed complete.
Rendering and comparison took 13.771122417063452 seconds.

For each of the ten ordered ranges above the driver ran this exact argument
template, substituting only the declared FIRST and LAST values:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f FIRST -l LAST -r 110 -png /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/windsor-thesis-2026-10-08/fletcher-2009-thesis.pdf /private/tmp/windsor-integrity.QxjmlU/page
```

The process environment set `FONTCONFIG_FILE` to the independent `fonts.conf`
and `FONTCONFIG_PATH` to that temporary directory. Every range returned exit 0,
zero stdout bytes and zero stderr bytes. The driver required those results and
the expected page files before proceeding. Existing destination images were
refused before starting; logs and JSON receipts were exclusively created.
Per-command timeout was 60 seconds, with a 600-second overall between-range
guard. No failed independent command was retried and no criterion was weakened.

The runtime was Python 3.12.14, pypdf 6.10.0, Pillow 12.3.0 and Poppler
`pdftoppm` 26.05.0. The wrapper, selected runtime/module files, driver,
configuration, source and declared instruction/receipt inputs were pinned
before and after, with equality. This is not a complete operating-system,
shared-library or font-file environment lock.

## Retained machine evidence

All paths in this table are relative to `/private/tmp/windsor-integrity.QxjmlU`.
The final receipt retains all ten literal command arrays, log hashes, source
and held-image before/after hashes, and each page's PNG and decoded-pixel hash.

| File | Bytes | SHA256 |
|---|---:|---|
| `fonts.conf` | 240 | `4ba42b9cb35a67e70216ba99bffdf0c866f9c3ccbb3a854f356fa212417f87dd` |
| `verify_render.py` | 5848 | `c7921b267b7513414ea8ac8dddbfd366474b4d87d209ae128cd8418ef4256c4a` |
| `start.json` | 15706 | `55ace890a0b9cbeb86219556c44f6012da1242f5c1e9004791ef70b9201ff016` |
| `receipt.json` | 69026 | `109f6b230bbbdc22696d291cad9d217e32fa96e7367955bc89155a0428461228` |

Post-run compact receipt/pin inspection (`1a61e6`) independently confirmed
source, selected method and held-image before/after equality and the dimensions
reported above. No rendering or comparison result was inferred from file
existence alone.

## Earlier render diagnostics

`failed-render-receipts.json` is preserved at 77,843 bytes, SHA256
`493e2ea0c333139f5dc4972b432097aeb6b92d8be216bf4591410227c1397d18`.
Structured inspection (`178ad9`) confirms eight terminal exit-1 receipts,
for starts 1, 11, 33, 81, 114, 153, 166 and 197. Each retained projection reports
Fontconfig errors and an inability to write its first image. Initial and final
tool outputs are explicitly truncated; they are not complete stderr streams.
The retained description reports that directory creation failed and subsequent
jobs were not gated on that failure. This historical failure is not erased by
the successful independent run, and missing historical stderr is not recreated.

The root's `render/render-receipts.json` contains seven successful ranges;
`render/expansion-render-receipts.json` contains two. Their nine saved stdout
and stderr file pairs are all empty and their recorded return codes are all 0
(`8cc6cf`). Those two JSON arrays cover 76 pages. Root subsequently preserved
the separate preflight as `render/title-render-receipt.json`, inspected here
in `272a41`, SHA256
`7cd88e6d329228f3ca23ab3c2b42d708e71f6560239c18e8e9de01eac6a7607f`.
It records the exact page-1 command, initial tool receipt `c12dc1`, session
`41646`, and terminal receipt `f210b8`, exit 0 with empty combined tool output.
There were no separately captured stdout/stderr files for that preflight;
empty combined output is not relabeled as two independently retained streams.
Together, the three receipt files document all 77 originally held pages.
This title receipt was inspected after the independent run, not included in
its earlier before/after pin set. The title PNG was independently reproduced
and byte/pixel-checked as part of the new 77-page run.

The initial combined inspection display was truncated (`4fc06b`); the expansion
was reread and failure information was reissued in compact, untruncated form.
No truncated display was treated as a complete diagnostic archive.

## Boundary

This is independent execution using the same renderer and font directories,
not an independent PDF-rendering algorithm or original-source acquisition.
Matching outputs can share a rendering defect. No page-content correctness,
equation reading, graphical measurement, physical model, or thesis conclusion
is certified here. The PDF skill supplied the Poppler workflow; the source-of-
truth boundary preserved the PDF, failed attempts and existing derivatives.
