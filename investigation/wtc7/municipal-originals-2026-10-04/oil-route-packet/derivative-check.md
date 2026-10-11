# Independent oil-route derivative check

October 4, 2026. All eight initial 2400-pixel rasters and the requested
4800-pixel repeats of pages 4, 5 and 6 reproduce exactly.
**Complete declared coverage: eleven used new rasters, no repeat gap.**
This checks local PDF-to-PNG derivation with the same renderer, not historical
authenticity, engineering validity or source interpretation.

## Scope and source

Read the complete unit protocol and PDF skill before execution; main
AGENTS/WORKFLOW/CHARTER hashes match the previously read versions. Applied
source-preservation/evidence-audit controls. Only this new note and the
private checker scratch directory were written. No source/image content
views, OCR, crops, network, source or frozen-note edits, Git or engine actions.

Protocol SHA-256:
`760851891417a23f6a33a70eea7977b5712da87831752ff078b9dff4e73ee0f2`.

Command path abbreviations:

```sh
U=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/oil-route-packet
T=/private/tmp/oil-route-derivative.GjrOty
R=/private/tmp/wtc7-oil-route.5rvgAx
P=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm
I=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo
```

After root's source-admission notice, `shasum -a 256` and `wc -c` confirmed
`U/NYC-WTC_000166828.pdf`: 533928 bytes, SHA-256
`3812f9cf9399f044943bf718dcdc5cdad42dd0416a9cea7be10714168edca2e9`.
`set -o pipefail; "$I" <source> | rg '^(Pages:|Encrypted:|File size:|PDF version:)'`
completed exit 0 and reported 8 pages, no encryption, PDF 1.5 and the same
size (`8ce1b1`). No content was printed. The source hash was checked again
unchanged after rendering (`0e2f61`, exit 0).

## Fresh renderer execution

`mktemp -d /private/tmp/oil-route-derivative.XXXXXX` created `T`
(`a5e072`, exit 0). Created `T/fonts.conf` with `apply_patch`, then explicitly
created `T/font-cache` with `mkdir` (`3a0c38`, exit 0). Config uses
`/System/Library/Fonts`, `/Library/Fonts`, `fonts.dtd` and the private cache.
Checker config SHA-256:
`c09cf407728efedc2c0dc9f2115e70f7a81a7cd78cc2a73ea0b084df16d0db43`.
Root config SHA-256:
`7c3e552818e62e3d9135a33ae77a4ff58dc8a03072193963c524cf14784fbb67`.
`diff -u "$R/fonts.conf" "$T/fonts.conf"` returned expected exit 1
(`7862d6`): only cache path differs. `$P -v` reported Poppler 26.05.0.

Executed once, all admitted pages in physical order:

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 8 -png -scale-to 2400 "$U/NYC-WTC_000166828.pdf" "$T/166828" >"$T/166828.stdout" 2>"$T/166828.stderr"
```

A Python subprocess wrapper saved expanded command, UTC start/end, monotonic
elapsed time, actual renderer return code and wrapper streams to
`T/166828-receipt.json`; its exit propagated the renderer code. The original
live handle 48439 was polled to terminal `0fcc57`, exit 0, never restarted.
Actual renderer exit: 0. Start UTC 22:04:33.078356; end 22:04:49.642636;
elapsed 16.564502 seconds. Both wrapper streams were empty.

Receipt JSON SHA-256:
`daa2461b6271bfc1133422259fe82d8ac27ed3d824bfe0901a43daedfb0c82ab`.
Saved renderer stdout and stderr are each zero bytes with SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
No warning or other diagnostic was emitted into those files.

## All eight initial comparisons

Root reported its original render terminal `0378cf`, exit 0, and eight ready
images with empty stderr (`b528b0`) before comparison. These root process
facts are attributed reports, separate from the independent execution above.
Both executions were terminal before the following tests.

Actual checks (`0e2f61`, exit 0): for explicit pages `1 2 3 4 5 6 7 8`,
`cmp -s "$T/166828-$page.png" "$R/166828-$page.png"`, recording each
status; `find "$T" -maxdepth 1 -type f -name '*.png' | wc -l` counted 8;
`shasum -a 256` covered all eight fresh and eight root images; `wc -c` measured
fresh image/diagnostic sizes; `file` checked both sets' PNG headers without
viewing content. Exact byte equality also establishes equal file size.

| Page | Dimensions, both copies | Bytes per copy | SHA-256, fresh and root | cmp exit |
|---|---:|---:|---|---:|
| 1 | 2400 x 1929 | 241966 | `2667cd775630f67c704b48b388a823368f0cb35e6a848ef950906ad95b0400d9` | 0 |
| 2 | 1800 x 2400 | 119572 | `d3ced4439b31286082d95ea0a3532eab637017b2fee1ed9f66214748f4d6ad7a` | 0 |
| 3 | 1794 x 2400 | 90445 | `266790e6de754871b2b74da62554b3eda063f2c9d72a1ed598f93a536b1e2737` | 0 |
| 4 | 1797 x 2400 | 214105 | `9e26270b70e21e0abd83c9785f049cadc4955c8dbc9d153fd1cf71d60479a78d` | 0 |
| 5 | 1804 x 2400 | 179740 | `468ba74c8a32bf088959e3631dc1546ff92728f1ca6a3666ea14217bbb4ab03a` | 0 |
| 6 | 1794 x 2400 | 168135 | `f41a06cffe8c69fa260d6872999333576fcb0531b6b3cbbb36e7b1dd7eac73e8` | 0 |
| 7 | 1947 x 2400 | 161557 | `ed11e6e92e61fb63cf5cab7461e0c00b58fc6b0aae6c38ee442ce05446744f60` | 0 |
| 8 | 1794 x 2400 | 173719 | `750c98176524c373ee4f8575c1ecaa461afc3a7e8c7228323aa01d44abe3f77d` | 0 |

All PNGs are 8-bit RGB, non-interlaced; total fresh image bytes: 1,349,239.
No missing initial page, mismatch or renderer failure was observed. Scratch
outputs, receipt and diagnostics remain available; temporary storage is not
a durability guarantee.

## Requested 4800-pixel repeats: pages 4 and 5

Root requested these two complete-page readability repeats after saving the
material legibility reasons. The checker did not read source content or reader
interpretations. Both repeats used the same private config/cache and source;
the source pin matched immediately before both runs (`927e29`, exit 0) and
after both (`0b2924`, exit 0).

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 4 -l 4 -png -scale-to 4800 "$U/NYC-WTC_000166828.pdf" "$T/166828-large" >"$T/166828-large-4.stdout" 2>"$T/166828-large-4.stderr"
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 5 -l 5 -png -scale-to 4800 "$U/NYC-WTC_000166828.pdf" "$T/166828-large" >"$T/166828-large-5.stdout" 2>"$T/166828-large-5.stderr"
```

Each expanded command ran once, with a separate saved JSON receipt and
stdout/stderr. Original live handles were polled to terminal, not restarted:

| Page | Start UTC | End UTC | Elapsed seconds | Handle / terminal receipt | Renderer exit |
|---|---|---|---:|---|---:|
| 4 | 22:08:05.740998 | 22:08:26.967112 | 21.233558 | 49799 / 76a097 | 0 |
| 5 | 22:08:07.607679 | 22:08:30.410095 | 22.802706 | 27420 / e05220 | 0 |

All wrapper streams are empty. The four separately saved renderer stream
files are each zero bytes with the empty-file hash above; no warning was
emitted. Receipt SHA-256 values:

- `T/166828-large-4-receipt.json`: `a7df17fd6dfceda4defd92871eefecdd675d3b96e3fcc7941970180e96f9fd26`.
- `T/166828-large-5-receipt.json`: `1bf3792200b1e432aef9cdfbbcf1da32a5deaedf0459296a72b5291432bd5992`.

Root reported page 4 terminal `a93a85`, exit 0, zero stderr (`5186b6`);
page 5 terminal `5e0bc1`, exit 0, zero stderr (`bef99a`). Each comparison
waited for its corresponding root and checker terminal confirmations.
`cmp -s` returned 0 for both same-basename file pairs in `T` and `R`.
`shasum -a 256`, `file` and `wc -c` established:

| Basename | Dimensions, both copies | Bytes per copy | SHA-256, fresh and root |
|---|---:|---:|---|
| 166828-large-4.png | 3593 x 4800 | 1757977 | `4332f6cdec6bf169373a34d561bda80e1e87eecd53fa9e160a9a426772fe56da` |
| 166828-large-5.png | 3607 x 4800 | 1524739 | `58647f697a76e0d38207ab1028cf2bfd95a18335e4c527a1f4e9bf92ed976d61` |

Both are 8-bit RGB, non-interlaced. Page-4 comparison, both checker image
headers/sizes and repeat diagnostics are recorded in `0b2924`, exit 0.
Page-5 root comparison was performed separately after its terminal notice
(`7d2a5b`, exit 0).
The checker scratch directory now contains ten PNGs: eight original page
representations and these two larger full-page representations. They do not
constitute ten distinct source pages.

The initial note-save operation took a pending tool interval (cell 148);
it was waited to successful completion without restart before repeat renders
began. No renderer or byte-comparison failure occurred.

## Later requested 4800-pixel repeat: page 6

The peer reader subsequently requested page 6 after recording a material
legibility reason. Root reported rendering it without root viewing it at the
larger size. This checker executed the following once with the same source
and private cache; no content was viewed:

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 6 -l 6 -png -scale-to 4800 "$U/NYC-WTC_000166828.pdf" "$T/166828-large" >"$T/166828-large-6.stdout" 2>"$T/166828-large-6.stderr"
```

The source pin matched before (`a6c6b1`) and after (`c0513f`), both exit 0.
Original live handle 3318 reached terminal `00e43e`, exit 0, without restart.
Its saved JSON receipt records renderer exit 0, UTC start 22:13:41.924367,
end 22:13:47.889674, elapsed 5.965153 seconds, and empty wrapper streams.
`T/166828-large-6-receipt.json` SHA-256:
`f714ba9888ab5fcbeae073618e71b87d904d896eed21cdfea5f78586c25705f3`.
Both saved renderer streams are zero bytes with the empty-file hash above.

Root reported terminal `412b44`, exit 0, and zero stderr (`61e1dd`) before
comparison. `cmp -s` of `T/166828-large-6.png` and its same-basename root
copy returned 0 (`9d86cd`, exit 0). Both are 3588 x 4800, 8-bit RGB, non-interlaced,
1,308,093 bytes, with SHA-256
`4825bb5d192df744451dd978fbc73f46fdfb0ce5f814bb4183eda1b93e80915f`.
`shasum -a 256`, `file` and `wc -c` verified these properties. The scratch
count is now eleven PNGs: eight initial pages plus three larger representations.

## Final coverage and limits

Root confirmed that both readers' new-source viewing is complete: root used
the eight initial rasters plus repeats 4/5 (ten views), and peer used the
eight initial rasters plus repeats 4/5/6 (eleven views). These are attributed
view-count reports, not observations made by the checker. The union is exactly
the eleven rasters verified above. The later comparison declaration reuses
already-rendered material; it adds no new render to this unit's coverage.

Final local check `67bfd6`, exit 0, at 22:21:24 UTC: `shasum -a 256` confirmed
the source and checker config unchanged; `find` counted eleven scratch PNGs;
`wc -c` totaled 5,940,048 PNG bytes and zero bytes in all eight saved renderer
streams; all eight stream hashes equal the empty-file hash. `jq -s` read all
four saved execution receipts and confirmed renderer exits 0 with empty
wrapper streams and the exact timings recorded above. All eleven byte
comparisons are accounted for, including all three larger repeats. No source
pin change, missing output, renderer failure or comparison mismatch occurred.
No additional rendering was performed or remains live.

Shared renderer and system fonts can reproduce a common defect. No visual
correctness, readability, display scaling, historical authenticity, engineering
validity, installed state or human acceptance was tested. Source hashes pin
the held input; they do not authenticate its historical origin or completeness.
