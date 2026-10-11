# Independent approval-breakdowns-b derivative check

October 4, 2026 America/New_York; October 5 UTC. All nine initial page rasters
reproduce exactly. Three renderer processes exited 0 with empty diagnostics.
All sixteen preserved files match root scratch. Final coverage is closed
with zero larger repeats. This is local same-renderer derivation verification, not
historical authentication, content interpretation, readability or engineering
validity.

## Scope and sources

Read the complete new protocol plus incorporated batch-A, change-order and
various-orders protocols (`070ffa`, exit 0). Read PDF, source-of-truth and
evidence-falsification skills; main AGENTS/WORKFLOW/START-HERE and investigation
CHARTER hashes match their previously read versions (`255748`, exit 0).
Preservation controls limit writes to this new note and own scratch; sources,
existing/frozen notes and main/legal files remain untouched. No image/source
content view, OCR, crop, rotation, enhancement, network, root/peer substantive
note reading, Git or engine action was performed.

Protocol SHA-256:
`f9a127482c9509df5509f5bee4ba6dce93493c0b665423c4979062e17d42d4a3`.

Command path abbreviations:

```sh
U=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/approval-breakdowns-b
T=/private/tmp/approval-b-derivative.JJaWox
R=/private/tmp/wtc7-approval-b.dZp5SN
P=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm
I=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo
```

`shasum -a 256` and `wc -c` verified the three declared PDF hashes and sizes
before rendering (`09938c`, exit 0); all hashes remained unchanged afterward
(`d7c690`, exit 0). Total source bytes: 809957. Each `$I <source>` call exited
0, with empty saved stderr, and reported the following physical page counts,
no encryption and PDF 1.5 (`d38429`, exit 0). Only those metadata fields were
printed, not page content.

| Source filename | Pages | Bytes | SHA-256 before/after |
|---|---:|---:|---|
| NYC-WTC_000172953.pdf | 5 | 345271 | `b981e1fde92775b1c59b2d4370488c2d70591efcbb3b98e9a621b2d32e814f00` |
| NYC-WTC_000173949.pdf | 2 | 232649 | `c480f2a9635763caf4cc17be6a3500c1ec2cb42c878165d863192f6e255e3809` |
| NYC-WTC_000174004.pdf | 2 | 232037 | `89de4a3ae1e611c2c27993ced26f4e921650022b7864713c29cce9095f08c93e` |

## Independent rendering

`mktemp -d /private/tmp/approval-b-derivative.XXXXXX` created `T`
(`09938c`, exit 0). Created `T/fonts.conf` via `apply_patch` and explicitly
created `T/font-cache` via `mkdir` before rendering (`d38429`, exit 0).
Config uses `/System/Library/Fonts`, `/Library/Fonts`, `fonts.dtd` and own
private cache. `$P -v` reported Poppler 26.05.0 (`09938c`).

Checker config SHA-256:
`5899779be80cf4b6590c33838f1e2b308a2bfe2489fe67e6ae20bbf1fb697dcc`.
Root config SHA-256:
`b1835e6f03d9d04308f0eb24d7d020b14003301669995b136cacaeea690e764d`.
`diff -u "$R/fonts.conf" "$T/fonts.conf"` returned expected exit 1
(`126d66`): only the private cache path differs.

Exactly one initial execution per PDF, concurrently in separate subprocesses:

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 5 -png -scale-to 2400 "$U/NYC-WTC_000172953.pdf" "$T/172953" >"$T/172953.stdout" 2>"$T/172953.stderr"
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 2 -png -scale-to 2400 "$U/NYC-WTC_000173949.pdf" "$T/173949" >"$T/173949.stdout" 2>"$T/173949.stderr"
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 2 -png -scale-to 2400 "$U/NYC-WTC_000174004.pdf" "$T/174004" >"$T/174004.stdout" 2>"$T/174004.stderr"
```

Each Python subprocess wrapper saved the expanded command, UTC start/end,
monotonic runtime, actual renderer return code and wrapper streams in
`T/<ID>-receipt.json`, then propagated the return code. Original live handles
were polled to terminal; none was restarted.

| ID | Start UTC, October 5 | End UTC | Seconds | Handle / terminal receipt | Renderer exit |
|---|---|---|---:|---|---:|
| 172953 | 00:08:39.765082 | 00:08:53.121449 | 13.356199 | 47282 / 44d4ed | 0 |
| 173949 | 00:08:39.763224 | 00:08:49.083988 | 9.319193 | 16015 / 6e8ef5 | 0 |
| 174004 | 00:08:39.767207 | 00:08:49.518343 | 9.751002 | 13733 / a64a0b | 0 |

All wrapper streams were empty. All six saved renderer stdout/stderr files
are zero bytes with SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
(`d7c690`, exit 0); no renderer warning was emitted. Receipt pins:

- `172953-receipt.json`: `8cca2c9d68158ac2e48e3181f49b2e0e638bbe22015ee2f82cdd72024d246c9a`.
- `173949-receipt.json`: `23b8f467521f3ab578cd11d48c86b060c2d7664b605377626651d13567308b5a`.
- `174004-receipt.json`: `37455d4469b90be0cbaffc5271ed53672ad45f9845f77360c386842b2425bae9`.

## Nine initial comparisons

Root reported its three renderer terminal exits 0 (`eb0cc5`, `9e3573`,
`b177f2`) and all nine rasters ready before comparison. Those root statuses
are attributed, distinct from this checker's actual process receipts above.
All checker processes were terminal before comparison.

At `2026-10-05T00:09:23Z`, check `d7c690` exited 0: ran explicit
`cmp -s "$T/$artifact" "$R/$artifact"` for each basename below, recording
every return code; `shasum -a 256` and `file` on both copies; `wc -c` on
fresh files and streams. `rg --files --hidden --no-ignore -g '*.png' "$T"
| wc -l` counted exactly nine. All nine comparisons returned 0. Headers
match; equal full bytes also establish equal size. All PNGs are 8-bit RGB,
non-interlaced. Landscape dimensions are retained without rotation.

| PNG basename | Dimensions, both | Bytes per copy | SHA-256, fresh and root |
|---|---:|---:|---|
| 172953-1.png | 1776 x 2400 | 115572 | `dc309b5b3bac1e0db685e46b010f3793a93d937bfa2c602154abc47ac9f4db2d` |
| 172953-2.png | 2400 x 1915 | 61346 | `c55912dd605f09abd3e698beb6a1707de261c024383fa5eab8a3b7004493ded4` |
| 172953-3.png | 2400 x 1913 | 137337 | `6ee111688d19f9d49072d346bcc8f3c19cd54bb9eea20dbc8fff857eb5bc9eba` |
| 172953-4.png | 1783 x 2400 | 273792 | `c2b6cf4ae26b64ec075ae4825942bf2677af03124bf528501e8940c218a7b6bb` |
| 172953-5.png | 1783 x 2400 | 117332 | `34782176a2da70738d9e2ab7b4b1b575445d15537c895cb2f98eab3d8c16a9ff` |
| 173949-1.png | 1785 x 2400 | 219671 | `3db319dcab1883c354d6d749f72d1975499b574f89e4139aba86806b72dbb74c` |
| 173949-2.png | 1782 x 2400 | 174799 | `b4cbb946bffb0bc473496a6ef09e10f90fbcd4378c695658285a42cf2d931047` |
| 174004-1.png | 1784 x 2400 | 192428 | `5c7722137f88a185e36038c389d06476ec052eafaf5418a063e303983c670451` |
| 174004-2.png | 1783 x 2400 | 243586 | `afd88ffb362e64568c87e8c333c2ad742963302aca6f45cbaf3358e24a9b8598` |

Total initial PNG bytes: 1535863. No missing page, source-pin change,
render failure or byte/header-dimension mismatch occurred. The expected
cache-path `diff` exit 1 is not a render failure. Scratch outputs, diagnostics
and individual receipts remain retained; temporary storage is not a durability
guarantee.

## Preserved copies

After the temporary pause, complete note readback and saved receipt checks
(`853715`, exit 0) confirmed the checkpoint. `shasum -a 256` on all three
receipt JSON files retained the pins above; `jq` confirmed the three actual
renderer exits 0, runtimes and empty wrapper streams. No renderer restarted.

Root reported preservation complete (`cp -n`, `eb20de`, exit 0) and its own
nine-page reading closed with zero repeats. At `2026-10-05T00:23:01Z`,
independent check `f52c98` exited 0. Ran explicit
`cmp -s "$U/$artifact" "$R/$artifact"` with each return code retained,
plus `shasum -a 256 "$U/$artifact"`, on all sixteen exact basenames:
the three PDFs in the source table, `fonts.conf`, the nine PNGs in the
comparison table, and `172953.stderr`, `173949.stderr`, `174004.stderr`.

All sixteen pair comparisons returned 0; zero failures. Every preserved
hash matches its source/config/PNG/empty-stream pin above. `file` confirmed
all nine preserved PNG headers/dimensions, and `wc -c` confirmed all three
preserved stderr files remain empty. The protocol and private font-config
hashes remained unchanged. This independently verifies current post-copy
equality, not the historical copying method or absence of any earlier overwrite.

## Final coverage and limits

Root subsequently confirmed both readers closed at nine initial page views
each, zero larger repeats. This reader closure is attributed to root's
messages, not an independent content review. Supplied frozen note pins are
`fa3ed5e83bbf90c007e4a833d6324a7b84f538eec2d9c57732fabe71614f1bf1`
and `5bfaced1c2644a66212fb5f4e921c3608e36e16472c3d78abdc845bb11cf1050`;
those notes were neither opened nor independently hashed by this checker.

Final coverage is three PDFs, nine whole-page rasters, three successful
independent renderer executions, six empty renderer streams and sixteen
exact preserved-copy comparisons. No additional raster was requested or
executed, and no required derivative remains unchecked. No source-pin,
renderer, byte/header-dimension or preservation mismatch occurred.

Shared Poppler and fonts can reproduce the same defect. No content accuracy,
readability, display geometry, historical authenticity/completeness,
construction, inspected performance, engineering validity or human acceptance
was tested. Source/image contents and reader interpretations were not viewed.
