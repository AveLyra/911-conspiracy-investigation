# Independent generator-test-results derivative check

October 4, 2026 America/New_York / October 5 UTC. All four initial rasters
reproduce exactly. Three renderer processes exited 0 with empty diagnostics.
Final coverage is closed with zero repeats. All eleven preserved files match
root scratch; an initial checker diagnostic-filename error is retained below.
This checks local same-renderer derivation, not historical authenticity,
content accuracy, visual readability or engineering validity.

## Scope and pinned inputs

Read this complete protocol and PDF skill (`2e162f`, exit 0); main
AGENTS/WORKFLOW/START-HERE and investigation CHARTER hashes matched their fully
read versions. Applied the already-read source-preservation and evidence
controls. Only this new note and private scratch were written. No source or
image content view, OCR, crop, enhancement, rotation, network, root/peer note
reading, main/legal/STATUS/README edit, Git or engine action occurred.

Protocol SHA-256:
`09ffc83e3e3519365d82bfe5c739eabc4ac3c624c60458c04307505a7d79459a`.

Command path abbreviations:

```sh
U=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/generator-test-results
T=/private/tmp/generator-tests-derivative.9OrP3G
R=/private/tmp/wtc7-generator-tests.eDRPkp
P=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm
I=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo
```

Root admitted and supplied these scratch sources before this check; no source
was acquired by this checker. `shasum -a 256` and `wc -c` verified all three
declared pins/sizes before rendering (`a1d706`, exit 0), and source hashes
remained unchanged afterward (`ff804d`, exit 0). Total source bytes: 175510.
Each `$I <source>` call exited 0 with empty saved stderr and reported the
page counts below, no encryption and PDF 1.5 (`00d328`, exit 0). Only those
metadata fields were printed, not page content.

| Source basename under R | Pages | Bytes | SHA-256 before/after |
|---|---:|---:|---|
| NYC-WTC_000172395.pdf | 2 | 103619 | `f31ce35607d9017d01748dbf4240a4b6a29fa0d2a0f64f83c3b98317861852b1` |
| NYC-WTC_000172397.pdf | 1 | 35481 | `9507ff6e2e6b1171f2ba5024a979c7d4e6538070bcf00917e7b27020f68b55d1` |
| NYC-WTC_000173715.pdf | 1 | 36410 | `6593c96c2511dd7c668af62143d2038145112b81dc78cf87ec0711a573d61e8f` |

## Independent executions

`mktemp -d /private/tmp/generator-tests-derivative.XXXXXX` created T
(`a1d706`, exit 0). Created `T/fonts.conf` via `apply_patch`, then explicitly
created `T/font-cache` via `mkdir` (`00d328`, exit 0). Config uses
`/System/Library/Fonts`, `/Library/Fonts`, `fonts.dtd` and own private cache.
`$P -v` reported Poppler 26.05.0 (`a1d706`).

Checker config SHA-256:
`7023059d5d122d577c7a53823bbe5b40555676eace0125091df8b26581951cb4`.
Root config SHA-256:
`f3ee2e7a52784cac0e5bbbb0d9423789a8a3c512d30f66a2c5c3ac64c1a5fe57`.
`diff -u "$R/fonts.conf" "$T/fonts.conf"` returned expected exit 1
(`13bfe0`): only the private cache path differs.

Exactly one initial execution per PDF, concurrently in separate subprocesses:

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 2 -png -scale-to 2400 "$R/NYC-WTC_000172395.pdf" "$T/172395" >"$T/172395.stdout" 2>"$T/172395.stderr"
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 1 -png -scale-to 2400 "$R/NYC-WTC_000172397.pdf" "$T/172397" >"$T/172397.stdout" 2>"$T/172397.stderr"
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 1 -png -scale-to 2400 "$R/NYC-WTC_000173715.pdf" "$T/173715" >"$T/173715.stdout" 2>"$T/173715.stderr"
```

Each Python subprocess wrapper saved expanded command, UTC start/end,
monotonic runtime, actual renderer return code and wrapper streams in
`T/<ID>-receipt.json`, then propagated the return code. Original live handles
were polled to terminal; none was restarted.

| ID | Start UTC, October 5 | End UTC | Seconds | Handle / terminal receipt | Renderer exit |
|---|---|---|---:|---|---:|
| 172395 | 01:00:19.935818 | 01:00:33.460331 | 13.524593 | 38563 / d599b0 | 0 |
| 172397 | 01:00:19.933480 | 01:00:28.949822 | 9.015345 | 86380 / ef0ecc | 0 |
| 173715 | 01:00:20.859612 | 01:00:26.860296 | 5.999688 | 45255 / 9326c1 | 0 |

All wrapper streams were empty. All six renderer stdout/stderr files are
zero bytes with SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
(`ff804d`, exit 0); no warning was emitted. Saved receipt pins:

- `172395-receipt.json`: `38994248e342e42caa5d6ebbb3e89f1539fa359204211db1bba638e30cf3e913`.
- `172397-receipt.json`: `bfc30b91f8a18c4a7d342e410b563ded5531370b9a8b67cbc5ccc079855bcd66`.
- `173715-receipt.json`: `8f03e0629963bfa1b2e46773c90a8701bef3fa7db37cc44409d1340ff1f8b321`.

## Four initial comparisons

Root reported three completed renderers, exit 0 and empty stderr, with four
ready rasters (`6953e3` header/hash check) before this check. Root process
statuses are attributed; this checker's actual executions are recorded above.
All checker processes were also terminal before comparison.

At `2026-10-05T01:00:58Z`, check `ff804d` exited 0: explicit
`cmp -s "$T/$artifact" "$R/$artifact"` for each basename below, retaining
each return code; `shasum -a 256` and `file` on both copies; `wc -c` on fresh
PNGs and diagnostics. `rg --files --hidden --no-ignore -g '*.png' "$T" |
wc -l` counted four. All four comparisons returned 0 and headers match;
equal full bytes also establish equal size. All are 8-bit RGB, non-interlaced.

| PNG basename | Dimensions, both | Bytes per copy | SHA-256, fresh and root |
|---|---:|---:|---|
| 172395-1.png | 1783 x 2400 | 138090 | `cdb4f617cb55cd26ccf221fbc0da880844ef37e0b51c7fec0769b1dc01a2d3cb` |
| 172395-2.png | 1787 x 2400 | 110203 | `b6e4b8634b48c3bf78f4749df8a859cd119854ee67c23806960aec1f0faa2f53` |
| 172397-1.png | 1787 x 2400 | 77901 | `b5ba6f21464999767d9a9a2e40d1ff3951936d98af2786d7bdb6bf3fffeeb081` |
| 173715-1.png | 1778 x 2400 | 74211 | `41c7bb778fe1033afca95744f68cca842ef555aa9b480e40293ac9da940b321e` |

Total initial PNG bytes: 400405. No missing page, source-pin change,
render failure or byte/header-dimension mismatch occurred. Expected cache-path
`diff` exit 1 is not a renderer failure. Scratch outputs, diagnostics and
receipts remain retained; temporary storage is not a durability guarantee.

## Preserved-copy check and retained naming failure

Root reported all eleven files copied without overwrite (`12f9f9`, exit 0).
The independent copy check did not substitute that report for byte comparison.
At `2026-10-05T01:03:31Z`, command `311a31` **exited 1**. Its explicit
`cmp -s "$U/$artifact" "$R/$artifact"` calls returned 0 for all three PDFs,
`fonts.conf` and four PNGs; `shasum -a 256` on those preserved files matched
the pins above. `file` confirmed all four preserved PNG headers/dimensions.
Protocol and private font-config hashes remained unchanged.

The same command mistakenly assumed root diagnostics used `172395.stderr`,
`172397.stderr`, `173715.stderr` (the checker's own naming). All three `cmp`
calls returned 2; all three `shasum` calls reported missing files, producing
six counted comparison/hash failures. `wc -c` also reported the three files
missing; its printed zero total was not accepted as evidence of empty files.
This was a checker path-selection failure, not a detected rendering or source
copy mismatch, and was reported to root before correction.

Bounded `rg --files --hidden --no-ignore -g '*stderr*' "$U" "$R"`
(`7b73ab`, exit 0) located the actual three diagnostic basenames in both
directories: `172395-render.stderr`, `172397-render.stderr`,
`173715-render.stderr`. At `2026-10-05T01:04:32Z`, corrected-path check
`604cbf` exited 0: explicit `cmp -s` for each pair returned 0; `shasum -a 256`
and `wc -c` on both copies confirmed the empty-file pin above and zero bytes.
No file was renamed, replaced, created as a substitute or rerendered to pass.

Together, eight original successful pairs plus three corrected-path pairs
cover all eleven actual preserved files: three PDFs, config, four PNGs and
three root renderer diagnostics. All current bytes/pins agree. `604cbf` also
rehashed the three saved checker receipts and used `jq` to confirm unchanged
receipt pins, actual renderer exits 0, runtimes and empty wrapper streams.
Post-copy equality does not independently establish the historical copying
method or exclude an earlier overwrite.

## Final coverage and limits

Root subsequently confirmed both readers closed at four complete initial
views each with zero repeats. That closure is attributed to root's messages,
not an independent content or viewing-chronology review. This checker did not
open or hash reader notes. No larger raster was requested or executed.

Final coverage is four whole-page rasters from three PDFs, three successful
independent renderer executions, six empty renderer streams and eleven actual
preserved-copy comparisons. No required derivative remains unchecked. There
was no source-pin, renderer, byte or header-dimension mismatch; the failed
diagnostic-name assumption and its bounded resolution remain explicit above.

Shared Poppler and fonts may reproduce the same defect. No content accuracy,
display geometry, readability, historical authenticity/completeness,
construction, actual test performance, engineering validity or human acceptance
was tested. Source/image contents and reader interpretations were not viewed.
