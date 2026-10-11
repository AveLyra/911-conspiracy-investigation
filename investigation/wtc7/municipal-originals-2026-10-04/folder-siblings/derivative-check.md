# Independent derivative check

October 4, 2026. Derivation-only check; no source or image content viewed.
All five selected pages reproduced with exact PNG byte agreement. All three
source pins matched before and after. This is a separate execution using the
same renderer, not historical authentication or independent engineering evidence.

## Scope and inputs

Read the complete unit protocol and PDF skill before execution. Main
AGENTS/WORKFLOW/CHARTER hashes remained the previously read versions. The
source-of-truth and evidence-audit controls keep this receipt separate from
source interpretation and canonical findings. Only this new note and the
checker's temporary outputs were written; existing unit/main/legal files,
reader notes and sources were not edited. No network, OCR, crops, image views,
content extraction, Git or engine actions occurred.

Protocol SHA-256:
`d5ca86e049eb57af1d62e9fb0c30a80b9742c65be45af426a7352d1e94595262`.

Path abbreviations for the commands below:

```sh
U=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/folder-siblings
T=/private/tmp/folder-siblings-derivative.Agyw9M
R=/private/tmp/wtc7-folder-siblings.oMfxnD
P=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm
I=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo
```

`shasum -a 256` and `wc -c` verified the following held unit files before
rendering (receipt `ea2364`, exit 0); the same source hashes were rechecked
afterward (`965fd2`, exit 0).

| PDF suffix | Admitted pages | Bytes | SHA-256, unchanged before/after |
|---|---:|---:|---|
| 167240 | 1-2 | 79462 | `311bd1d07101b27d4055560cfc95b514c1d4a698a6a3c46bf4c367dbf4ca9321` |
| 167759 | 1-2 | 79419 | `88d8cce3415188e9c24c01b43cb64a3ac1219c681626d65b914c127ad4cedf31` |
| 171557 | 1 | 85393 | `d1b979b49cb0f13259ec08a514d2e5629265f1d0f08df4fd2cd7c905cacf615a` |

Each source is named `NYC-WTC_000<SUFFIX>.pdf`. Total source bytes: 244274.
Separate `$I "$U/NYC-WTC_000<SUFFIX>.pdf"` calls each exited 0, with empty
stderr, and reported page counts 2/2/1, no encryption and PDF 1.5
(`bec91e`). Only these metadata fields were printed, not page content.

## Fresh execution

`mktemp -d /private/tmp/folder-siblings-derivative.XXXXXX` returned `T`
(`4b941c`, exit 0). A new `fonts.conf` was created with `apply_patch`, and
`mkdir "$T/font-cache"` explicitly created its cache before rendering.
The configuration uses `/System/Library/Fonts` and `/Library/Fonts`, with
only `T/font-cache` as its cache. Checker configuration SHA-256:
`d94d16e98182013a193f9f49871e993b9a362d9f816a4a3874721c7c58e0cad9`.
`$P -v` reported Poppler 26.05.0 (`ea2364`).

Each of the following expanded commands ran exactly once, concurrently in
a three-worker Python subprocess wrapper; no retry or larger rendering ran:

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 2 -png -scale-to 2200 "$U/NYC-WTC_000167240.pdf" "$T/167240" >"$T/167240.stdout" 2>"$T/167240.stderr"
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 2 -png -scale-to 2200 "$U/NYC-WTC_000167759.pdf" "$T/167759" >"$T/167759.stdout" 2>"$T/167759.stderr"
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 1 -png -scale-to 2200 "$U/NYC-WTC_000171557.pdf" "$T/171557" >"$T/171557.stdout" 2>"$T/171557.stderr"
```

The original live session `32780` was polled to terminal receipt `6c7e96`,
exit 0. The wrapper collected each shell/renderer return code and ended with
`SystemExit(0 if statuses == [0, 0, 0] else 1)`, establishing all three exit
codes as 0. The returned per-render JSON also explicitly recorded 171557
exit 0, UTC start `2026-10-04T20:02:15.878780+00:00`, end
`2026-10-04T20:02:28.036889+00:00`, elapsed 12.157936 seconds.

Receipt limitation: the tool response retained only that one per-render JSON
line; individual elapsed times/start/end records for 167240 and 167759 are
not available in the returned receipt. They are not reconstructed or claimed.
The aggregate exit condition above verifies their zero return codes, not
their missing timings. No rerender was used to replace this incomplete
timing receipt.

All six separately saved `T/{167240,167759,171557}.{stdout,stderr}` files
were measured as zero bytes and hashed after execution (`965fd2`). Each has
the empty-file SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
Thus no renderer warning or other diagnostic was emitted into those files.

`diff -u "$R/fonts.conf" "$T/fonts.conf"` returned the expected difference
status 1 (`adc4dd`): the root DOCTYPE is `fonts.dtd`, while the checker uses
`urn:fontconfig:fonts.dtd`; the cache paths also differ. Both use the same
two system-font directories. Root configuration SHA-256:
`15b893a735c43ebdbfbe93e9e298ce12edef1ed21cde7e165934328c47c726cb`.
This configuration difference is retained, not hidden by an identical-config
claim; it did not change any compared output bytes.

## Complete output comparison

Root reported all three root processes terminal exit 0 before comparison
(root receipts `b986f2`, `9a6a3e`, `929c31`; root diagnostic receipt
`1ef9d1`). Those root execution statuses are reported, not independently
re-executed here. Fresh checker execution was terminal before comparison.

Actual checks (`965fd2`, exit 0): `find "$T" -maxdepth 1 -type f -name
'*.png' | wc -l` counted exactly five PNGs; `cmp -s "$T/$name" "$R/$name"`
returned 0 for each of the five explicit names below. `shasum -a 256` covered
all five files in both directories, `wc -c` measured the fresh files, and
`file` inspected both sets' PNG headers. All dimensions agree; all are
8-bit RGB, non-interlaced. Exact byte agreement also establishes equal size.

| PNG basename | Dimensions | Bytes per copy | SHA-256, fresh and root | cmp exit |
|---|---:|---:|---|---:|
| 167240-1.png | 1645 x 2200 | 129872 | `8a5607a7c00615267ab79c75a2050c4d7460b6a598c4e6360529b25b1d156c7e` | 0 |
| 167240-2.png | 1648 x 2200 | 68398 | `4c1e7f64256d3ad51c6bdf2acfe44d6a7c5549286032348a7fb90afae8b59766` | 0 |
| 167759-1.png | 1647 x 2200 | 129849 | `94162430e835e4f4a2877fd1cf6f5a1a46dce71d816751007567c606fe91dba7` | 0 |
| 167759-2.png | 1645 x 2200 | 67579 | `151e4d9193f14d769a146b7749869735e4e5e0460fae758f95a4ced311650391` | 0 |
| 171557-1.png | 1636 x 2200 | 193572 | `e893eb6eff3be34e71ed2e1d743e49be11fbc57cacb70a9715c8a80a56ad0c6f` | 0 |

Total fresh PNG bytes: 589270. All five admitted pages and all five comparisons
are accounted for. No hash/size/dimension mismatch or renderer failure was
observed; the missing two timing records and expected configuration difference
remain explicit above. Temporary outputs and diagnostics are retained, but
temporary storage is not a durability guarantee.

## Limits

This directly establishes local byte reproducibility and unchanged selected
inputs for this execution. The strongest limitation is the shared renderer:
a common renderer defect could reproduce identically. No visual correctness,
readability, source authenticity, historical completeness, installed condition,
engineering conclusion, content-family equivalence or human acceptance was
tested. Neither identical derivatives nor new Bates identifiers establish
independent historical evidence. A source-pin or output mismatch would defeat
the narrow agreement result; none occurred in this finite check.
