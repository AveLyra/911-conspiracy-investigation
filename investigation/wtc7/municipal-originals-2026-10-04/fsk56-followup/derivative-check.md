# Independent FSK-56 derivative check

October 4, 2026. Research only. One independent 2200-pixel render of all three
pages completed with exit 0 and empty stdout/stderr; all three images match
root's initial outputs byte for byte. A separately requested page-2-only
4400-pixel readability render also completed with exit 0 and empty streams
and matches root's corresponding saved raster byte for byte. No page content
or reader annotations were viewed.

## Scope, source and runtime

Read `PROTOCOL.md` completely before rendering, SHA-256
`4552522ed7f5f54502ee4b864f94cda0e5ef5da70be3005edf450b511bd93bca`.
The prior-read, unchanged main controls and PDF skill continued to apply.
The initial scope was all three pages at maximum dimension 2200. Root later
explicitly requested the protocol-permitted single readability repeat for
physical page 2 only at 4400 because of small-label ambiguity; this checker
did not inspect or independently interpret that ambiguity.

Source: `/private/tmp/wtc7-fsk56.4NS5KF/NYC-WTC_000174022.pdf`, 135742 bytes,
SHA-256 `a2d7dc4ce0e26ac431e98691d387161657f989d1d685a300731aec3b8d79735f`.
`shasum -a 256` and `wc -c` confirmed the assigned input before execution
(`85abd6`, exit 0). The source hash matched after both the initial render
(`9c83bf`, exit 0) and readability render (`c57f45`, exit 0). A filtered
`pdfinfo` metadata check reported 3 pages, no encryption and PDF 1.5; see the
combined-command/cache status qualification below.

`mktemp -d /private/tmp/fsk56-derivative.XXXXXX` created
`/private/tmp/fsk56-derivative.57ESnp` (`85abd6`). The bundled executable's
`-v` reported Poppler 26.05.0. A Python 3.13.7 stdout-only subprocess wrapper
captured actual renderer return code and stdout/stderr separately, printed
UTC timestamps plus elapsed monotonic time, then exited with the renderer's
return code. Original live handles were polled to terminal completion; no
render was restarted because a tool observation yielded.

`fonts.conf` was created with `apply_patch` in the fresh temporary directory,
using exactly `/System/Library/Fonts`, `/Library/Fonts`, and
`/private/tmp/fsk56-derivative.57ESnp/font-cache`. Its SHA-256, unchanged across
both renders, is `21614dcd03db2278e85e8b76db6e3b9e07842165f04de354e6f52dbaee3d1f14`.
Both processes set `FONTCONFIG_FILE=/private/tmp/fsk56-derivative.57ESnp/fonts.conf`.
No main font cache was selected.

## Actual executions

Working directory: this `fsk56-followup` unit. The subprocess argument vectors
were the following commands, each invoked exactly once under the font
configuration above:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 3 -png -scale-to 2200 /private/tmp/wtc7-fsk56.4NS5KF/NYC-WTC_000174022.pdf /private/tmp/fsk56-derivative.57ESnp/physical
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 2 -l 2 -png -scale-to 4400 /private/tmp/wtc7-fsk56.4NS5KF/NYC-WTC_000174022.pdf /private/tmp/fsk56-derivative.57ESnp/readability
```

| Scope | UTC start / end | Elapsed seconds | Terminal result | Stdout / stderr |
| --- | --- | ---: | --- | --- |
| Pages 1-3 at 2200 | 18:32:35.057905 / 18:32:40.340142 | 5.281753 | Session 22403; `0b89c1`, exit 0 | 0 / 0 bytes; both empty |
| Page 2 at 4400 | 18:35:11.404212 / 18:35:23.783603 | 12.378769 | Session 67474; `193cac`, exit 0 | 0 / 0 bytes; both empty |

No renderer warning text appeared in either run. The readability run was
new, explicitly requested scope, not a retry or replacement for the initial
outputs. It did not include pages 1 or 3.

## Initial three-page comparison

Root reported its initial run terminal before comparison. A fresh-file glob
count returned three initial PNGs. An explicit loop over pages 1, 2 and 3 ran
`cmp -s /private/tmp/fsk56-derivative.57ESnp/physical-<page>.png /private/tmp/wtc7-fsk56.4NS5KF/page-<page>.png`.
Every pair returned 0; `checked_pairs=3 comparison_failures=0` (`dfefe8`,
exit 0). `shasum -a 256` covered all six files; `wc -c` checked fresh sizes;
`file` read both sets' PNG headers (`9c83bf`, exit 0). No decoded content
viewing occurred. All sizes, dimensions and hashes match root's declared pins.

| Page | Dimensions | Bytes | SHA-256 of fresh and root PNG | `cmp` exit |
| --- | --- | ---: | --- | --- |
| 1 | 1633 x 2200 | 65514 | `a40a3125d96a90e5f03bb19eeb10c270bf24aa3e6852e7b5e5753f63d795fde6` | 0 |
| 2 | 1641 x 2200 | 133902 | `4a8277c344339c5c3e92e5cc71876df1d3d1b567e22ae0557cad732bf9abc180` | 0 |
| 3 | 1648 x 2200 | 111977 | `5eebe37c8b9657b497886ab3d1b56687ee76db77b71b74d86949452a951972a3` | 0 |

## Page 2 readability output

The independent `readability-2.png` is 3281 x 4400, 945816 bytes, SHA-256
`63e3559dbfd6763a2895f45306e80fede115b73a78b55d556d22fc5bfe3d7028`
(`c57f45`, exit 0). This is the only independently added readability page.
After root reported its readability process terminal (session 39789,
`562819`, exit 0; root-reported zero stderr), this checker ran:

```sh
cmp -s /private/tmp/fsk56-derivative.57ESnp/readability-2.png /private/tmp/wtc7-fsk56.4NS5KF/readability-2.png
```

The comparison returned 0 (`63fdef`, exit 0). Fresh `shasum -a 256` checks
confirmed both readability images share the stated pin; `file` confirmed
root's saved image is also 3281 x 4400. The three initial independent-image
pins and the PDF source-after pin remained unchanged in that same receipt.
Thus all four selected saved-raster pairs were compared successfully: the
initial three pages plus the one separately requested page-2 repeat.

Root separately reported that its viewer displayed the full readability
image at 2744 x 3680 despite requesting original detail. This check compares
the saved 3281 x 4400 rasters, not that displayed resampling. The checker did
not view or validate the display or assess whether it resolved the label
ambiguity. No claim of an unresized 4400-pixel content view follows from byte
equality of the saved outputs.

## Retained diagnostic and limits

After the initial render, `stat` found no directory at the configured private
font-cache path. The combined filtered-`pdfinfo`/`stat` call therefore ended
exit 1 (`639ce1`); its preceding metadata output is not represented as a
separately captured `pdfinfo` exit code. This was not a renderer failure:
the actual initial renderer had exit 0 and empty stderr. No cause is inferred
from the absent cache directory. It was explicitly created with `mkdir`
before the newly authorized 4400 run; subsequent `stat` confirmed that same
private directory exists (`c57f45`, exit 0). No initial render was retried.

No failed render/comparison was discarded. The original PDF, initial PNGs,
protocol and earlier records remain unchanged. Only this new unit note and
the independent temporary configuration/outputs/cache were created. Temporary
files are not durable archival storage. There was no network, re-fetch,
external transfer, OCR, crop, image enhancement or content interpretation.

Agreement with a shared renderer verifies local derivation, not independent
historical authenticity, drawing completeness, approval, installation or
either reader's interpretation. No canonical promotion, human acceptance,
engine/bridge action, staging, commit or push occurred.
