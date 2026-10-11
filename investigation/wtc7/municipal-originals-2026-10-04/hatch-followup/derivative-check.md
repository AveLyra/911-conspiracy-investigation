# Independent hatch-unit derivative check

October 4, 2026. All three selected first-page renders completed with exit 0,
empty stdout and empty stderr. Each fresh PNG matches root's corresponding
output byte for byte and by SHA-256; source-before/after pins are unchanged.
No primary content or reader annotations were viewed.

## Scope and inputs

Read the complete `PROTOCOL.md`, unchanged SHA-256
`20a72b569b175598d6e957f11974cb07e18c811f049880fd6b553230e13eb58c`.
The already-read main controls and PDF skill continued to apply. Scope is
physical page 1 of each of the three named PDFs, one render per source at
maximum dimension 2200. Physical page 2 of held 172166 was not rendered.

`shasum -a 256` / `wc -c` before (`0667bd`, exit 0), and source hashes after
(`a06085`, exit 0), agree with the assigned inputs:

| Source | Bytes | SHA-256 before and after |
| --- | ---: | --- |
| `/private/tmp/wtc7-hatch.7raRXT/NYC-WTC_000172163.pdf` | 49507 | `163f7e8a65d719ec14affd8591faea94b425abe1424941ca57309086d2735ee2` |
| `/private/tmp/wtc7-hatch.7raRXT/NYC-WTC_000171497.pdf` | 69607 | `62fb129a8860774a6ffd624915ffd0461340e6dfe4113b7d3227993d1d1ba433` |
| `../followup/NYC-WTC_000172166.pdf` | 147759 | `362ad11e3e7b5ac89183be9fa0095f2b0803518e3c854a77ae34f8e626012193` |

`mktemp -d /private/tmp/hatch-derivative.XXXXXX` created
`/private/tmp/hatch-derivative.vJOIOs`. `fonts.conf` was created there with
`apply_patch`, with `/System/Library/Fonts`, `/Library/Fonts`, and its own
`/private/tmp/hatch-derivative.vJOIOs/font-cache`. That cache directory was
explicitly created with `mkdir` before rendering and confirmed afterward.
Configuration SHA-256: `2867d4b7b0b5a4f306d59b479f675319163d2b3c41604e8e205267a3a179b146`.

## Actual execution

The bundled executable's `-v` reported Poppler 26.05.0 (`0667bd`). Each command
below ran once, concurrently, with
`FONTCONFIG_FILE=/private/tmp/hatch-derivative.vJOIOs/fonts.conf`:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 1 -png -scale-to 2200 /private/tmp/wtc7-hatch.7raRXT/NYC-WTC_000172163.pdf /private/tmp/hatch-derivative.vJOIOs/172163
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 1 -png -scale-to 2200 /private/tmp/wtc7-hatch.7raRXT/NYC-WTC_000171497.pdf /private/tmp/hatch-derivative.vJOIOs/171497
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 1 -png -scale-to 2200 /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/followup/NYC-WTC_000172166.pdf /private/tmp/hatch-derivative.vJOIOs/172166
```

A stdout-only Python subprocess wrapper captured each return code, stdout and
stderr separately, plus UTC and monotonic elapsed time. The original wrapper
session 27450 was polled to terminal exit 0 (`aae9b3`); individual records are
in `c513d2` / `aae9b3`. No process was restarted.

| PDF / page | UTC start / end | Elapsed seconds | Renderer exit | Stdout / stderr |
| --- | --- | ---: | ---: | --- |
| 172163 / 1 | 18:57:41.806889 / 18:57:46.647950 | 4.836884 | 0 | 0 / 0 bytes; empty |
| 171497 / 1 | 18:57:41.821350 / 18:57:47.457415 | 5.634737 | 0 | 0 / 0 bytes; empty |
| 172166 / 1 | 18:57:41.837705 / 18:57:46.125937 | 4.288122 | 0 | 0 / 0 bytes; empty |

## Complete comparison

Comparison began after root reported its three renders terminal and ready.
The fresh set contained exactly three PNGs. An explicit loop over 172163,
171497 and 172166 ran
`cmp -s /private/tmp/hatch-derivative.vJOIOs/<id>-1.png /private/tmp/wtc7-hatch.7raRXT/<id>-1.png`.
Every pair returned 0: `checked_pairs=3 failures=0` (`4c23b8`, exit 0).
`shasum -a 256` checked all six PNGs; `wc -c` checked fresh sizes; `file`
inspected fresh PNG headers (`a06085`, exit 0). All agree with root's supplied
pins, sizes and dimensions. No pixel-content view was used.

| Image | Dimensions | Bytes | SHA-256 of fresh and root PNG |
| --- | --- | ---: | --- |
| `172163-1.png` | 1636 x 2200 | 91382 | `63cae1c65bae835e2442cc5e3f099cf27682352bb181473f855f545460ca8079` |
| `171497-1.png` | 1630 x 2200 | 132625 | `fb8ecc896037b46300c7d7a82c04b05ccf13da77f81f56f7d4a3678b54cb54fb` |
| `172166-1.png` | 1636 x 2200 | 96193 | `d549de24f49df4b55332212d8e1b1e7d28e54a75b6d3732bcfb8334b4cd5b543` |

All headers report 8-bit/color RGB, non-interlaced; combined fresh image size
is 320200 bytes. There were no warnings, failed renders, mismatches, retries
or omitted selected pages. No readability supplement was performed.

Only this new unit note and the separate temporary configuration/cache/images
were created. Sources, earlier records and other notes were not edited.
Temporary outputs are not durable storage. No network, OCR, content reading,
new acquisition, main/legal write, Git or engine action occurred. Shared-
renderer agreement tests local derivation, not historical authenticity,
approval, installation, event-day condition or reader interpretation.
