# Independent structural follow-up derivative check

2026-10-04. Research only. Both PDF pins matched; exactly one fresh render per
PDF reached terminal exit 0 without warnings. All three resulting PNGs match
the saved `render/` files byte for byte. This replicates derivation with the
same renderer version; it does not authenticate historical source contents.

## Scope and execution

Read the complete local `PROTOCOL.md`; its before/after SHA-256 is
`34c26009cfec63e0fd1ce4b22680e4a82f092435ae6774ea1f690af3392892a2`.
Previously read current main instructions and the PDF skill remain applicable.
Acceptance covered the two exact source pins, terminal statuses, complete
one-page/two-page outputs, and all three byte comparisons. No network, OCR,
crop, enhancement, source interpretation or re-view was performed.

`mktemp -d /private/tmp/municipal-structural-derivative.XXXXXX` created the
fresh directory `/private/tmp/municipal-structural-derivative.CjYULh`
(`70ebb2`, exit 0; UTC timestamp 14:19:21). The same receipt confirms
`command -v pdftoppm` resolved to
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm`
and `pdftoppm -v` reported Poppler 26.05.0.

Working directory was this `structural-followup` unit. These commands ran
concurrently, once per PDF:

```sh
/usr/bin/time -p pdftoppm -f 1 -l 1 -r 150 -png NYC-WTC_000171807.pdf /private/tmp/municipal-structural-derivative.CjYULh/171807
/usr/bin/time -p pdftoppm -f 1 -l 2 -r 150 -png NYC-WTC_000173900.pdf /private/tmp/municipal-structural-derivative.CjYULh/173900
```

Each wrapper printed UTC immediately before/after and exited with the captured
render status. Original live handles were polled to terminal completion.

| PDF | UTC start / end | Time, seconds (real / user / sys) | Terminal receipt |
| --- | --- | --- | --- |
| 171807 | 14:19:49 / 14:19:52 | 2.18 / 0.23 / 0.03 | Session 96669; `29c78d`, exit 0 |
| 173900 | 14:19:49 / 14:19:53 | 3.62 / 0.70 / 0.04 | Session 54294; `d72ca9`, exit 0 |

No renderer warnings or errors were returned. Only timestamps and timing
measurements appeared. No render was restarted. `shasum -a 256` checked both
input pins before (`159a33`, exit 0) and after (`153fb0`, exit 0):

| PDF | SHA-256, matching both times |
| --- | --- |
| `NYC-WTC_000171807.pdf` | `1c0753e27edd92e4bc4dde5389f1b1a291bf3ee113a1600b47e73bc373816ab4` |
| `NYC-WTC_000173900.pdf` | `6dac8359d2f3c9ea98721c1b69f55038838d6755ea806d114cd55ff0b81d86df` |

## Complete comparison and preservation

Shell glob counts found exactly three fresh and three saved PNGs. An explicit
loop over the three filenames below ran
`cmp -s /private/tmp/municipal-structural-derivative.CjYULh/<name> render/<name>`
and recorded every exit status (`372caf`, exit 0). Every comparison returned
0, with `comparison_failures=0`; no page was missing or extra.

`shasum -a 256 /private/tmp/municipal-structural-derivative.CjYULh/*.png
NYC-WTC_000171807.pdf NYC-WTC_000173900.pdf PROTOCOL.md root-observations.md
review.md render/*.png` completed with exit 0 (`153fb0`). Fresh and saved
PNG hashes agree, and saved hashes also match the pre-render check:

| Filename / physical page | SHA-256 of fresh and saved PNG | `cmp` exit |
| --- | --- | --- |
| `171807-1.png` / 1 | `968cf1c81dd9f5dc0a25cd1464d54820c409d019b6958695caaf5e903da426a8` | 0 |
| `173900-1.png` / 1 | `c4b522152823ef70480ec38e1d9c3c9cf5db98e8d6339e8acf9a098a84cb0ed0` | 0 |
| `173900-2.png` / 2 | `1acae7ef30423d43103c6d8b9e026dba1c743bc0909a4a5127aa92ce8f34f769` | 0 |

Only this new note was written in the unit. Reader-note hashes sampled during
and after rendering also matched: `root-observations.md`
`34034cd7a6d2f03aad34db9430e3359233f8b1f965988b08e3e5c23eed2a5808`;
`review.md` `f9058df2d766816f4b2e720b31f7271aab6c69a1c72af51aeec33bc5e8357d00`.
Fresh PNGs remain in the named temporary directory, not durable storage.

No rendering or comparison failure was discarded, and no retry was required.
Earlier acquisition/copy events were not repeated by this check. Exact byte
agreement made a decoded-pixel fallback unnecessary. Same-runtime replication
does not test a different rendering implementation, historical completeness,
custody, source authenticity, engineering effect, installed state or reader
interpretation. Existing visual uncertainty remains. No canonical promotion,
human acceptance, transmission, staging, commit or push occurred.
