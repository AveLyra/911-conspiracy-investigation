# Independent drawing derivative check

October 4, 2026. Complete declared coverage: initial four 2400-pixel rasters
and the sole requested 4800-pixel page-1 repeat match exactly. Root confirmed
both readers completed new-source viewing with these five rasters only.
This is a local same-renderer derivation check, not historical or engineering
authentication.

## Controls and sources

Read the complete protocol and PDF skill before execution. Main
AGENTS/WORKFLOW/CHARTER hashes match the previously read controls. Applied
source-preservation and evidence-audit boundaries: no PDF/image content views,
OCR, crops, network, source edits, reader-note inspection, Git or engine actions.
Only this note and the private checker scratch directory were written.

Protocol SHA-256:
`b0076f130b9f6004534c89a4ab074881422d1401661dddb68f2a504763887048`.

Path abbreviations used below:

```sh
U=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/drawing-review
T=/private/tmp/drawing-review-derivative.bQAoal
R=/private/tmp/wtc7-drawing-review.4PgqcG
P=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm
I=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo
```

`shasum -a 256` checked both unit source pins before and after rendering;
`wc -c` checked sizes (`8bbad4` and `0d79dd`, exit 0). Each `$I` call exited
0 with empty stderr and reported PDF 1.5, no encryption, and counts below
(`ae9df8`). Only metadata fields were printed, not page content.

| Source filename | Pages | Bytes | SHA-256, unchanged before/after |
|---|---:|---:|---|
| NYC-WTC_000167874.pdf | 3 | 258425 | `18fd09dd9631551ab11f88fc18f56b759338707739463e2a313cc601c2d705af` |
| NYC-WTC_000173670.pdf | 1 | 67561 | `89dfc492e45ca53e8e1247b07d3bd34cd476d80d5a2f13107f7846a162dc0627` |

## Fresh execution and saved receipts

`mktemp -d /private/tmp/drawing-review-derivative.XXXXXX` created `T`
(`c3fe11`, exit 0). Created `T/fonts.conf` with `apply_patch`, then explicitly
created `T/font-cache` with `mkdir` before execution (`daab84`, exit 0).
The config uses `/System/Library/Fonts`, `/Library/Fonts`, `fonts.dtd`, and
only the private cache. Checker config SHA-256:
`3bf24ca5ae79f2ae53cbcebf3dce93e353a4b1fc17b529504ad3e1cf5e08ff18`.
Root config SHA-256:
`f9499b5297acac777a3d1f2a34e95d90c848dd78458f92410d396c6003579b9d`.
`diff -u "$R/fonts.conf" "$T/fonts.conf"` returned expected exit 1
(`52ddb6`): only the private cache path differs. `$P -v` reported 26.05.0.

Each expanded command ran once, in separate observed subprocesses:

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 3 -png -scale-to 2400 "$U/NYC-WTC_000167874.pdf" "$T/167874" >"$T/167874.stdout" 2>"$T/167874.stderr"
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 1 -png -scale-to 2400 "$U/NYC-WTC_000173670.pdf" "$T/173670" >"$T/173670.stdout" 2>"$T/173670.stderr"
```

A Python subprocess wrapper for each command recorded the expanded command,
UTC start/end, monotonic elapsed time and actual renderer return code to
`T/<ID>-receipt.json`; its own exit propagated the renderer return code.
Original live handles were polled to terminal, never restarted.

| ID | Start UTC | End UTC | Seconds | Handle / terminal receipt | Actual exit |
|---|---|---|---:|---|---:|
| 167874 | 20:31:48.537285 | 20:32:04.119613 | 15.581813 | 6047 / a4bb3e | 0 |
| 173670 | 20:31:48.537612 | 20:31:54.583759 | 6.046023 | 85900 / 144dc8 | 0 |

Both wrapper stdout/stderr fields were empty. Each saved renderer stdout and
stderr file is zero bytes; all four have SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
No warning was emitted. Individual saved receipt hashes:

- `167874-receipt.json`: `c6d0724363c57c11a4f5f3ff6dd2983e66a6987668d8e0b0647a86f6c92b9285`.
- `173670-receipt.json`: `919e1dece0fea419c0991a154ae0f5c21c8b0171bc68eb5f84bd6a7875b1c937`.

## Four initial comparisons

Root reported its initial render processes terminal exit 0 (`ecefb0`,
`1bdab0`) and both stderr files empty (`505b3a`) before comparison. These
root process facts are attributed reports, separate from the independent
executions above. Both checker executions were also terminal before comparison.

Actual commands in `0d79dd` (exit 0): explicit `cmp -s "$T/$name"
"$R/$name"` for every basename below, reporting each status; `find "$T"
-maxdepth 1 -type f -name '*.png' | wc -l` counted four; `shasum -a 256`
covered all four PNGs in each directory; `wc -c` checked fresh sizes and
diagnostics; `file` checked both sets' dimensions without viewing images.

| PNG basename | Dimensions | Bytes per copy | SHA-256, fresh and root | cmp exit |
|---|---:|---:|---|---:|
| 167874-1.png | 1794 x 2400 | 165868 | `ab2795f787efa3c647bfc490565048f6dec3ac03a35187831fa569b99b02f177` | 0 |
| 167874-2.png | 1808 x 2400 | 214621 | `7e858a2730345108a0286f19806b944639bb5fdacbb4589a2e9e70d92b7ab7fc` | 0 |
| 167874-3.png | 1796 x 2400 | 191288 | `4eaee541f0229937f5b94881835a73dcba7586f20ae5417c383245be09e67926` | 0 |
| 173670-1.png | 1785 x 2400 | 158480 | `78a23519c065afb9d06119f70f5b99e4085fb598887356163c0b47646189430f` | 0 |

All are 8-bit RGB, non-interlaced; total fresh PNG bytes: 730257.
No missing initial page, byte/hash/dimension mismatch or renderer failure was
observed. Outputs and diagnostics are retained in temporary storage, which
does not itself guarantee durable preservation.

## Requested page-1 repeat at 4800

After both content readers independently requested page 1 of 167874 at the
larger size, root reported its full-page repeat terminal exit 0 (`b0901c`)
and zero stderr (`0eb9b2`). This checker performed only that additional
requested render, with the same separate config/cache as above:

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 1 -png -scale-to 4800 "$U/NYC-WTC_000167874.pdf" "$T/167874-large" >"$T/167874-large.stdout" 2>"$T/167874-large.stderr"
```

167874's source hash matched before (`deecd1`, exit 0) and after
(`6e5c19`, exit 0). The original live handle 9001 was polled without restart
to terminal `be8200`, exit 0. Its saved individual receipt records actual
renderer exit 0, UTC start 20:34:39.344623, end 20:34:47.638138, elapsed
8.293095 seconds, and empty wrapper streams. Both saved renderer streams
are zero bytes with the same empty-file hash given above. Receipt file
`T/167874-large-receipt.json` SHA-256:
`04d90acf71725b465242d85597c702112fc8b7da376ee547dc7732074ac82d68`.

After both root and checker execution were terminal, `cmp -s` of
`T/167874-large-1.png` and `R/167874-large-1.png` returned 0 (`6e5c19`).
Both header dimensions are 3588 x 4800, 8-bit RGB, non-interlaced; each is
1,225,932 bytes and has SHA-256
`f942fadce34f3a1305bc9943c74db238a4a3565f89b58fd8655994acbd96e032`.
`shasum -a 256`, `file` and `wc -c` supplied these checks. The scratch PNG
count is now five: four initial pages plus this one larger representation.
No source/image content was viewed. Root later reported that this same saved
3588 x 4800 raster was displayed at 2750 x 3680 for root and 1363 x 1824 for
the peer. Those attributed display-resolution limits are not byte-render
mismatches; the checker did not view or independently measure either display.

## Final coverage and limits

This establishes local reproducibility of the five tested rasters only.
Shared Poppler and fonts
can reproduce the same renderer defect. No visual correctness, readability,
viewer-display geometry, document authenticity, attachment relationship,
historical completeness, installed condition or human acceptance was tested.
Root confirmed the final repeat set: only 167874 page 1 at 4800. Thus all four
initial pages and the sole used larger representation have separate execution
and comparison coverage; no repeat gap remains in that declared set. No
additional renders were performed. Both source pins and the checker config
were checked again unchanged before freezing this receipt (`b583aa`, exit 0,
20:38:12 UTC). Existing source,
root output, protocol and reader-note files remain untouched by this checker.
