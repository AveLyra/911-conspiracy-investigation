# Independent design/sprinkler derivative check

October 4, 2026. Three independent render processes completed with exit 0 and
empty stdout/stderr. All four admitted page images match root's corresponding
outputs byte for byte and by SHA-256. The three source hashes are unchanged
before/after rendering. No page content or reader annotations were viewed.

## Scope, source pins and setup

Read the complete `PROTOCOL.md` before source checks or rendering; its
unchanged SHA-256 is
`57abb5f9c48443dd9defe9972f1cc9779190c23a8cc32733685f1e1149e716d8`.
Prior-read main controls and the PDF skill continued to apply. Root admitted
2, 1 and 1 actual PDF pages respectively; all four were selected here. Catalog
group counts are not these individual PDFs' page counts, and their difference
is not treated as proof of missing pages or failed acquisition.

Sources are in `/private/tmp/wtc7-design-sprinkler.5CKjlR/`. Before-render
`shasum -a 256` / `wc -c` (`f58e93`, exit 0) and after-render hashes
(`488700`, exit 0) confirmed all assigned pins:

| PDF | Bytes | Selected pages | SHA-256 before and after |
| --- | ---: | --- | --- |
| `NYC-WTC_000167235.pdf` | 79607 | 1-2 | `e05450bbef04fc1df6005a97233ca8c341f900033f425131686592f2feb9dbd7` |
| `NYC-WTC_000167873.pdf` | 40327 | 1 | `21dfad1a9da62a6e88869612309277f386f6600e54dfa34889ef4da8975e8b3d` |
| `NYC-WTC_000171300.pdf` | 84808 | 1 | `8643cab6ed8e8c0caff7cd23c73b1841f6bf6f85a90415786cdf92de530db841` |

`mktemp -d /private/tmp/design-sprinkler-derivative.XXXXXX` created
`/private/tmp/design-sprinkler-derivative.6EOLrY` (`f58e93`). A `fonts.conf`
created there with `apply_patch` uses `/System/Library/Fonts`, `/Library/Fonts`
and its own `/private/tmp/design-sprinkler-derivative.6EOLrY/font-cache`.
The cache directory was explicitly created with `mkdir` before execution and
confirmed afterward. Configuration SHA-256:
`022bcc9e1fc512a52796d5377ac75cafcb5ca7646d33403b35c14f3db625a531`.

## Exact rendering and diagnostics

The bundled executable's `-v` reported Poppler 26.05.0 (`f58e93`). Each command
ran exactly once, concurrently, with
`FONTCONFIG_FILE=/private/tmp/design-sprinkler-derivative.6EOLrY/fonts.conf`:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 2 -png -scale-to 2200 /private/tmp/wtc7-design-sprinkler.5CKjlR/NYC-WTC_000167235.pdf /private/tmp/design-sprinkler-derivative.6EOLrY/167235
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 1 -png -scale-to 2200 /private/tmp/wtc7-design-sprinkler.5CKjlR/NYC-WTC_000167873.pdf /private/tmp/design-sprinkler-derivative.6EOLrY/167873
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 1 -png -scale-to 2200 /private/tmp/wtc7-design-sprinkler.5CKjlR/NYC-WTC_000171300.pdf /private/tmp/design-sprinkler-derivative.6EOLrY/171300
```

A stdout-only Python subprocess wrapper recorded each process's UTC start/end,
monotonic elapsed time, return code and separate stdout/stderr. Original session
31662 was polled to terminal exit 0 (`41ce09`); all three renderer results were
individually captured. No observation timeout caused a restart.

| PDF | UTC start / end | Elapsed seconds | Renderer exit | Stdout / stderr |
| --- | --- | ---: | ---: | --- |
| 167235 | 19:13:33.704548 / 19:13:40.896293 | 7.188118 | 0 | 0 / 0 bytes; empty |
| 167873 | 19:13:33.735381 / 19:13:37.031066 | 3.261649 | 0 | 0 / 0 bytes; empty |
| 171300 | 19:13:33.773384 / 19:13:40.471664 | 6.697673 | 0 | 0 / 0 bytes; empty |

## All four output comparisons

After root reported its renders terminal and ready, an explicit four-filename
loop ran `cmp -s /private/tmp/design-sprinkler-derivative.6EOLrY/<image>
/private/tmp/wtc7-design-sprinkler.5CKjlR/<image>` for every image below.
The fresh glob count was four; every `cmp` returned 0, with
`checked_pairs=4 failures=0` (`fd5046`, exit 0). Fresh and root image hashes
were measured independently (`488700` / `fd5046`, both exit 0). Fresh byte
counts and PNG headers were checked with `wc -c` and `file` (`488700`).
All match root's declared pins, sizes and dimensions.

| Image / physical page | Dimensions | Bytes | SHA-256 of fresh and root PNG |
| --- | --- | ---: | --- |
| `167235-1.png` / 1 | 1645 x 2200 | 132640 | `92a2268c2ec12afbc4231721852ea6a96bf5fcd9ccc57f6fdb6899b028f129de` |
| `167235-2.png` / 2 | 1649 x 2200 | 68763 | `6802e3137dd2ee20992c542ae7f55470cf1fa6490d2b1251207c9c22d329c5d9` |
| `167873-1.png` / 1 | 1645 x 2200 | 78966 | `cbc7813ddd99bd8126855b681c5bd852969d1a203f921c449f479e38c62372c8` |
| `171300-1.png` / 1 | 1639 x 2200 | 196764 | `8172f42bb17102ead5eb705ea7163cc0ca5e1c03b1854869f31f2b7d98c270b1` |

All headers report 8-bit/color RGB, non-interlaced; total fresh PNG size is
477133 bytes. Header inspection did not involve content viewing. No selected
page was omitted, and there were no warnings, render failures, mismatches or
retries. No larger readability render was performed.

Only this new note and the separate temporary configuration/cache/outputs were
created. Sources, frozen records, other notes and main/legal files were not
edited. Temporary outputs are not durable archival storage. No network,
re-fetch, OCR, source-content view, Git or engine action occurred. Shared-
renderer agreement establishes local derivation only, not historical
authenticity, archive completeness, attachment completeness, installation,
approval, event-day state or reader interpretation.
