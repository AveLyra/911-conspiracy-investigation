# Independent figure-supplement derivation check

2026-10-04. Research only. One fresh render of physical pages 62-64 completed
with terminal exit 0 and no renderer warnings. All three output PNGs match the
saved supplement images byte for byte. This is a fresh derivation check,
separate from the earlier integrity-only check of pages 59-61.

## Scope, source and configuration

Read `FIGURE-SUPPLEMENT.md` completely before execution; its before/after
SHA-256 is `674e9bf12918b1d64e48630802804d8362951acffe1875cf4f26679c7f8cdc8d`.
The existing main controls and PDF skill continued to apply. Scope was only
one render of these three pages and complete byte comparison. No content
viewing, interpretation, text extraction, OCR, crops or network occurred.

The read-only source remained at
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup/sources/ncstar-1-1j-attempt02.pdf`.
`shasum -a 256` confirmed its assigned pin before (`f9fccd`, exit 0) and after
(`44f2c2`, exit 0):
`7b1fe2a7a94a67c54fdaabe27e3309b439551512cff97e5026e0b62bb51bf623`.

`mktemp -d /private/tmp/oem-figure-derivative.XXXXXX` created the fresh private
directory `/private/tmp/oem-figure-derivative.H702Ab` (`4a3a8b`, exit 0;
UTC timestamp 14:55:12). An independent `fonts.conf` was created there with
`apply_patch`, using `/System/Library/Fonts`, `/Library/Fonts`, and its own
cache `/private/tmp/oem-figure-derivative.H702Ab/font-cache`.

| Configuration | SHA-256 |
| --- | --- |
| Saved `figure-render/fonts.conf` | `71464029ed6cc6dcca2c8daf2dc6e5f60516ea3645d71a4e4f9b08b32dc4b61f` |
| Fresh temporary `fonts.conf` | `955f07dc2d76d59286fe32db5312ce5cf4b00d0a972f820a239908c69dc765d5` |

`diff -u figure-render/fonts.conf /private/tmp/oem-figure-derivative.H702Ab/fonts.conf`
showed exactly one changed line: the saved cache directory
`/private/tmp/wtc7-oem-figures.aVe622/font-cache` became the fresh cache above
(`5a0ba8`, exit 1, the expected difference result). Font directories and every
other configuration line agree. The temporary cache directory existed after
execution (`stat -f '%N %Sp'`, `8002fc`, exit 0). No main cache was selected.

## Actual render and terminal result

The specified executable's `-v` output reported Poppler 26.05.0 (`4a3a8b`).
From this `oem-comparison` unit, exactly one render command ran:

```sh
/usr/bin/time -p env FONTCONFIG_FILE=/private/tmp/oem-figure-derivative.H702Ab/fonts.conf /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 62 -l 64 -scale-to 2200 -png /Users/admin/docs/911/research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup/sources/ncstar-1-1j-attempt02.pdf /private/tmp/oem-figure-derivative.H702Ab/physical
```

The wrapper printed UTC before/after and exited with the captured render
status. Original session 98121 was polled without restart until terminal
exit 0 (`f716c1`). UTC window: 14:55:55-14:56:14. Timing (`557028`): real
18.41 s, user 1.71 s, sys 1.68 s. No renderer warning/error text appeared;
the wrapper returned only its configuration hash, timestamps and timing data.

## All outputs accounted for

Shell glob counts found three fresh PNGs (`3ad5cb`, exit 0) and three saved
PNGs (`8002fc`, exit 0). An explicit loop over 62, 63 and 64 ran
`cmp -s /private/tmp/oem-figure-derivative.H702Ab/physical-<page>.png figure-render/physical-<page>.png`.
All three statuses were 0; `checked_pairs=3 comparison_failures=0` (`3ad5cb`).
No missing, extra or byte-different page was found.

`shasum -a 256` checked every fresh/saved PNG and both configurations, the
supplement and the source after execution (`44f2c2`, exit 0). All image pins
match the assigned values and the saved images' pre-render hashes. `file`
reported every fresh and saved PNG as 1700 x 2200, 8-bit/color RGB,
non-interlaced; this was header inspection, not a content view.

| Physical page / filename | SHA-256 of fresh and saved PNG | `cmp` exit |
| --- | --- | --- |
| 62 / `physical-62.png` | `bd558d4b49cf52bb7b9e41b4384308032136d7a842a446dd5ce38c0ee6d6a9ab` | 0 |
| 63 / `physical-63.png` | `2f66674ad64d43a9bda0cd2fd85b4c157fba815390a23f50a52d293cb6c1510f` | 0 |
| 64 / `physical-64.png` | `29c31d34e7e2a6eb98440a4432bf2bc35bff8f2d9dccc9106fe48fd047116f55` | 0 |

No rendering or comparison failure was discarded and no retry occurred.
The expected configuration `diff` status 1 was retained as such. Only this
new note was written in the unit; source, saved images/configuration, prior
receipt and other notes were not edited. Fresh outputs/configuration/cache
remain in the named temporary directory, not durable storage.

Byte agreement verifies local reproducibility with the same renderer and
matching font configuration apart from cache location. It does not test a
different renderer, authenticate historical contents, establish a drawing
join or installed condition, or validate either reader's interpretation.
No canonical promotion, human acceptance, transmission, staging, commit or
push occurred.
