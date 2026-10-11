# Independent approval-breakdowns-a derivative check

October 4, 2026. All eleven initial rasters and one requested larger raster
reproduce exactly. Four renderer processes exited 0 with empty diagnostics.
Final coverage is closed, and all twenty preserved files match root scratch.
This is local same-renderer derivation verification, not historical
authentication, source interpretation, visual readability or engineering validity.

## Scope and pinned inputs

Read this unit's full protocol, incorporated change-order and various-orders
protocols and acquisition source log (`0824d7`, exit 0), plus the PDF,
source-of-truth and evidence-falsification skills (`5a9054`, exit 0).
Main AGENTS/WORKFLOW/START-HERE and investigation CHARTER hashes match their
previously read versions (`200ee8`, exit 0). Source-preservation controls keep
this note derivative-only: no source/image content views, OCR, crops,
rotation, enhancement, network, root/peer interpretation reads, source or
frozen-note edits, Git or engine actions. Only this new note and own scratch
are writable within this task.

Protocol SHA-256:
`fa18d2a1954ff128e948036c911f80fedede736e9b908f0f9d48ae2c68bef732`.

Command path abbreviations:

```sh
U=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/approval-breakdowns-a
T=/private/tmp/approval-a-derivative.UJPOmO
R=/private/tmp/wtc7-approval-a.IM4mAE
P=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm
I=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo
```

`shasum -a 256` and `wc -c` verified all three declared source pins/sizes
before rendering (`200ee8`, exit 0). Source hashes remained unchanged after
rendering (`7baf05`, exit 0). Total source bytes: 1171404.
Each `$I <source>` call exited 0, with empty saved stderr, and reported the
page counts below, no encryption and PDF 1.5 (`c69285`, exit 0). Only those
metadata fields were printed; no page content was extracted or viewed.

| Source filename | Pages | Bytes | SHA-256 before/after |
|---|---:|---:|---|
| NYC-WTC_000171286.pdf | 5 | 489175 | `e0776e7605d5136b5f73863acbf4c8b8654ac7c70cf83d9ef0596053e13d660b` |
| NYC-WTC_000171620.pdf | 3 | 326462 | `3b2d1b201e25385391cc9efb72ce044c80006d6e4cbae8e3fac16f5804eb30e7` |
| NYC-WTC_000172947.pdf | 3 | 355767 | `667a70850ca01b211fa0f21ace5774a06acbd77bf02bbf723ea11eb3b5dc79f6` |

## Fresh executions

`mktemp -d /private/tmp/approval-a-derivative.XXXXXX` created `T`
(`200ee8`, exit 0). Created `T/fonts.conf` via `apply_patch` and explicitly
created `T/font-cache` via `mkdir` before rendering (`c69285`, exit 0).
Config uses `/System/Library/Fonts`, `/Library/Fonts`, `fonts.dtd` and own
private cache. `$P -v` reported Poppler 26.05.0 (`200ee8`).

Checker config SHA-256:
`58abc2a38466928190e5d16f06822a71c61c8f4e4368e8edbb73d34f7737e799`.
Root config SHA-256:
`0f63dd2e113feae474b242435df3dfbdc2f822483c621429abc35ab7546ce167`.
`diff -u "$R/fonts.conf" "$T/fonts.conf"` returned expected exit 1
(`e29abb`): only the cache path differs.

Exactly one fresh execution per PDF, concurrently in separate subprocesses:

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 5 -png -scale-to 2400 "$U/NYC-WTC_000171286.pdf" "$T/171286" >"$T/171286.stdout" 2>"$T/171286.stderr"
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 3 -png -scale-to 2400 "$U/NYC-WTC_000171620.pdf" "$T/171620" >"$T/171620.stdout" 2>"$T/171620.stderr"
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 3 -png -scale-to 2400 "$U/NYC-WTC_000172947.pdf" "$T/172947" >"$T/172947.stdout" 2>"$T/172947.stderr"
```

Each Python subprocess wrapper saved its expanded command, UTC times,
monotonic runtime, actual renderer return code and wrapper streams in
`T/<ID>-receipt.json`, then propagated that return code. Original handles
were polled to terminal; no live process was restarted.

| ID | Start UTC | End UTC | Seconds | Handle / terminal receipt | Renderer exit |
|---|---|---|---:|---|---:|
| 171286 | 23:29:57.475473 | 23:30:28.769650 | 31.292882 | 28305 / 837464 | 0 |
| 171620 | 23:29:57.481180 | 23:30:16.283387 | 18.801871 | 94584 / 649ff3 | 0 |
| 172947 | 23:29:57.505414 | 23:30:13.921751 | 16.416036 | 74056 / 8b9a85 | 0 |

All wrapper streams were empty. All six renderer stdout/stderr files are
zero bytes with SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
(`7baf05`, exit 0); no renderer warning was emitted. Saved receipt pins:

- `171286-receipt.json`: `690057fab78733e241ce3921bc3007024d72958005a7e0072ef905205f2a87fb`.
- `171620-receipt.json`: `572e09498b8a5194491a30bbd5eb7c1e29df08dc5d18f940d2ef0b215303386e`.
- `172947-receipt.json`: `2899f8d2bdf993f941de0c11b33bbaaa85b0e5bb322a8db71eafde4f699c97e7`.

## Eleven initial comparisons

Root notified completion of all three root renderers (`b23d01`, `9f4ef3`,
`ff2a9f`, exit 0) and eleven ready PNGs before comparison. These root process
statuses are attributed; the three checker exits above are separate actual
executions. All checker processes were also terminal before comparison.

At `2026-10-04T23:31:03Z`, check `7baf05` exited 0: explicit
`cmp -s "$T/$artifact" "$R/$artifact"` for each basename below, with each
return code retained; `shasum -a 256` and `file` on both copies; `wc -c` on
fresh files and streams. `rg --files -g '*.png' "$T" | wc -l` returned 11.
All eleven comparisons returned 0. Both headers match; equal full bytes also
establish equal size. All PNGs are 8-bit RGB, non-interlaced.

| PNG basename | Dimensions, both | Bytes per copy | SHA-256, fresh and root |
|---|---:|---:|---|
| 171286-1.png | 1791 x 2400 | 220832 | `0dee89beb41e303faa46792b106c3942f9bee723381691284065e9eeff795a64` |
| 171286-2.png | 1787 x 2400 | 271821 | `5f01b3b4311bf2c0a01666a701a9376478c69e5946df42d61ae634f58456d975` |
| 171286-3.png | 1787 x 2400 | 231584 | `464b395f1418f37c72f766522cf7272a37ccb2e0ede1ffea925d0d97d18034dd` |
| 171286-4.png | 1788 x 2400 | 189744 | `1511d9b772d4d7a0b4242895df20f028921d595c114eb14827ccdeddcc3ffa7c` |
| 171286-5.png | 1783 x 2400 | 88493 | `73825c2e52ae216b95cb1d4b9d2577608be1fb167bdbf7722b65b08c7b005923` |
| 171620-1.png | 1780 x 2400 | 201698 | `8453c7345ae66e3d1abc173ed5981822f5640b143700c86b8c10b037377bcf9a` |
| 171620-2.png | 1782 x 2400 | 289243 | `f452af03642cc73cf297dce3cfc5162d19b896ca52bdccb29e9fe3279b37f4c7` |
| 171620-3.png | 1788 x 2400 | 168474 | `1ab20566feb7b50dc20b3218de14cd7e62d4e7faf8e8da2fe5c45876628ba695` |
| 172947-1.png | 1784 x 2400 | 235881 | `99b7714dbca5dc5b6f9c4fed41c78d0a96d315afb05772f2f2d8d60d36a00316` |
| 172947-2.png | 1788 x 2400 | 279588 | `f78d5a159cd3dd684b3177dd06aaac7d8763b3b209adf905891274d6123aa49e` |
| 172947-3.png | 1779 x 2400 | 124733 | `616333ca7c487d9f147f4bda71a970d549c12d80d36a3dd864515021f2c34bc8` |

Total initial PNG bytes: 2302091. No missing initial page, source-pin change,
renderer failure or byte/header-dimension mismatch occurred. Expected
cache-path `diff` exit 1 is not a render failure. Scratch outputs, diagnostics
and receipts remain retained; temporary storage is not a durability guarantee.

## Requested whole-page repeat: 171286 physical page 3

Root requested this one repeat and confirmed its renderer terminal exit 0
(`712ab1`) before comparison; root reported both readers independently
requested the same page. The reasons/notes were not read by this checker.
Source and private config pins remained unchanged before this execution
(`e9cf6a`, exit 0). Executed once with the same private cache:

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 3 -l 3 -png -scale-to 4800 -singlefile "$U/NYC-WTC_000171286.pdf" "$T/171286-3-repeat" >"$T/171286-3-repeat.stdout" 2>"$T/171286-3-repeat.stderr"
```

Original handle 41174 was polled to terminal (`bf2fa7`, exit 0), not
restarted. UTC start `23:33:31.379242`, end `23:33:50.174165`, monotonic
runtime 18.794092 seconds; actual renderer exit 0, empty wrapper streams.
The saved stdout/stderr are both zero bytes with the empty-file hash above.
`171286-3-repeat-receipt.json` SHA-256:
`9d39c79967354139167e7f73d7825c976cc0855f64c47abd08e4db7e1fc19385`.

At `2026-10-04T23:34:07Z`, check `51fc52` exited 0:
`cmp -s "$T/171286-3-repeat.png" "$R/171286-3-repeat.png"` returned 0;
both SHA-256 hashes are
`cf05b4439ca8e9c9e895c0476e5ef53edc1fd6582507256a060af75cc8499687`.
`file` on both confirms 3574 x 4800, 8-bit RGB, non-interlaced;
`wc -c` reports 2205494 bytes per identical PNG. Source hash remained
unchanged after rendering. Scratch PNG count is now 12, total 4507585 bytes.
Root reported its viewer resized this file to 2740 x 3680; that attributed
display limit was not tested here and is distinct from saved raster geometry.

## Final coverage and preservation

Root confirmed both readers closed their coverage at eleven pages/twelve
views each, using only the same physical-page-3 repeat. That reader closure
is attributed to root's message, not independently reviewed here. Root supplied
frozen note pins `bd0524506ba40572ae443099781107cd3b48db3c6ef1054c602cd0259ee5667d`
and `d65ed3af56a2f171da2257d3ecb50d04ecfbd14b9a13be21188d0bd1ddf8379c`;
those notes were neither opened nor independently hashed by this checker.
No further render was needed or executed after closure.

At `2026-10-04T23:40:32Z`, independent preservation check `afec47` exited 0.
Ran `cmp -s "$U/$artifact" "$R/$artifact"` with each return code retained,
plus `shasum -a 256 "$U/$artifact"`, for these exact twenty files:

- The three PDF basenames in the source table.
- `fonts.conf`.
- The eleven initial PNG basenames in the comparison table.
- `171286-3-repeat.png`.
- `171286.stderr`, `171620.stderr`, `172947.stderr` and `171286-3-repeat.stderr`.

All twenty pair comparisons returned 0; zero failures. Every preserved hash
matches the corresponding source/config/PNG/empty-stream pin above. `file`
confirmed the twelve preserved PNG headers/dimensions; `wc -c` confirmed all
four preserved stderr files are zero bytes. The protocol and private config
pins remained unchanged. Rehashed all four checker receipt JSON files, which
retain the pins above; `jq '{id,renderer_exit,elapsed_seconds,wrapper_stdout,
wrapper_stderr}'` confirmed all four saved exits 0 and empty wrapper streams.

Root separately reported `cp -n` completion (`8b4acb`, exit 0) and its own
copy check (`3ac642`, exit 0). Those attributed receipts were not substituted
for the independent comparisons. Post-copy equality does not independently
establish the historical copying method or exclude an earlier overwrite.

Final mechanical coverage is three PDFs, eleven initial pages and one used
larger repeat: twelve rasters, four successful independent renderer processes,
eight empty renderer streams and twenty exact preserved-copy comparisons.
No missing required raster, source-pin change, render failure, byte/header
dimension mismatch or preservation mismatch occurred. The expected cache-path
`diff` exit 1 remains disclosed, not treated as a render failure.

## Limits

Shared Poppler and fonts may reproduce the same defect. No visual correctness,
readability, display geometry, historical authenticity/completeness,
construction, inspected performance, engineering validity or human acceptance
was tested. Source/image contents and reader interpretations were not viewed.
