# Independent follow-up derivative check

2026-10-04. Research only. Both held PDF pins matched; one fresh render per
PDF reached terminal exit 0 without warnings. All eight PNGs are byte-for-byte
identical to the corresponding saved `render/` files. This is same-runtime
derivation replication, not independent historical authentication or source
interpretation.

## Scope and execution

Read the complete follow-up `PROTOCOL.md` before rendering. Its SHA-256 was
`bef0e57dc5993c8c1061235f97987aa57b2b77f022ec6139724d895bb08296e6`
before and after. The previously read current main controls and PDF skill
continued to apply. Acceptance: pinned inputs, one execution per PDF, complete
six-page/two-page output, terminal statuses, and all eight comparisons accounted
for. No network, OCR, crops, enhancement, source re-view or interpretation.

`mktemp -d /private/tmp/municipal-followup-derivative.XXXXXX` created
`/private/tmp/municipal-followup-derivative.H77SmN` (`c44632`, exit 0; UTC
timestamp 13:58:18). `command -v pdftoppm` resolved to the bundled
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm`;
`pdftoppm -v` reported Poppler 26.05.0. No dependencies were installed.

Working directory:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/followup`.
Exactly these two render commands ran, concurrently, once each:

```sh
/usr/bin/time -p pdftoppm -f 1 -l 6 -r 150 -png NYC-WTC_000173199.pdf /private/tmp/municipal-followup-derivative.H77SmN/173199
/usr/bin/time -p pdftoppm -f 1 -l 2 -r 150 -png NYC-WTC_000172166.pdf /private/tmp/municipal-followup-derivative.H77SmN/172166
```

Each wrapper printed UTC immediately before and after, captured the render's
status, and exited with it. Both original process handles were polled to
terminal completion; there was no restart or retry.

| PDF | UTC start / end | Time, seconds (real / user / sys) | Terminal receipt |
| --- | --- | --- | --- |
| 173199 | 13:58:58 / 13:59:17 | 19.03 / 2.35 / 0.11 | Session 99528, `8a92fe`, exit 0 |
| 172166 | 13:58:58 / 13:59:10 | 11.17 / 0.98 / 0.06 | Session 17050, `a8ec52`, exit 0 |

No renderer warning/error text was returned. Only UTC timestamps and timing
measurements appeared. The two PDF SHA-256 pins matched before (`16b660`,
exit 0) and after (`96142f`, exit 0):

| PDF | SHA-256 |
| --- | --- |
| `NYC-WTC_000173199.pdf` | `37b65cb843cd81716df26af8780627e27bed6d0557eb4b3419945ef742495903` |
| `NYC-WTC_000172166.pdf` | `362ad11e3e7b5ac89183be9fa0095f2b0803518e3c854a77ae34f8e626012193` |

## Complete byte comparison

Shell glob counts returned eight generated PNGs and eight saved PNGs. A loop
explicitly enumerated the eight filenames below and ran
`cmp -s /private/tmp/municipal-followup-derivative.H77SmN/<name> render/<name>`
for each, printing each status and accumulating failures (`d35768`, exit 0).
Every status was 0; `comparison_failures=0`. No page was missing or extra.

`shasum -a 256 /private/tmp/municipal-followup-derivative.H77SmN/*.png
NYC-WTC_000173199.pdf NYC-WTC_000172166.pdf PROTOCOL.md root-observations.md
render/*.png` also completed (`96142f`, exit 0). All eight fresh PNG hashes
equal their saved counterparts and the saved hashes checked before rendering:

| Filename / physical page | SHA-256 of fresh and saved PNG | `cmp` exit |
| --- | --- | --- |
| `173199-1.png` / 1 | `0801d39df1b19903c6bbe469d7f96ea90ac547571394e5468932c9b01a048f62` | 0 |
| `173199-2.png` / 2 | `32f93b41f342789be67762b146052aa4e156053db28e6637d453ac61f5dd59b6` | 0 |
| `173199-3.png` / 3 | `9c74ec79024f7e23b50e022f7797f3a5d03ebbe940cbbfa9f0cc6ceb106de1a1` | 0 |
| `173199-4.png` / 4 | `cd721595feb50da44709c482040f2c1299e19322adc2204f01c1705b392e2553` | 0 |
| `173199-5.png` / 5 | `01821bed2c8209a0bd12de3a85c1a874a8c509cf5d65552c4dab266f5d025907` | 0 |
| `173199-6.png` / 6 | `623e27eed964881f62003a50a8f8e69c3b4fea9042eba1dd562b4f31b4d4e12d` | 0 |
| `172166-1.png` / 1 | `128e33b4d14e6a8cdaf27b5e2fbf7caecbe7ccac16c5635d7a7a874e836f6812` | 0 |
| `172166-2.png` / 2 | `08fd0c5c4deece650e673a046ae573d9785eb859864b4af2c4ce71054b6c866e` | 0 |

## Preservation and limits

No failed render or comparison was discarded. Exact byte equality made a
decoded-pixel fallback unnecessary. Only this new note was written in the
follow-up unit; existing PDFs, renders, protocol and reading notes were not
edited. The root note hash sampled during and after rendering also matched
(`f7a55784f03e5a646ba811b97c9364623dcc0853e54946a477305bce26197e78`).
Fresh PNGs remain in the named temporary directory; that is not durable storage.

The check used the same renderer version and is not a second rendering
implementation. It does not verify historical completeness, custody,
authenticity, approval, installation, event-day conditions, or either reader's
interpretation; existing visual uncertainty remains. No human acceptance,
legal-record promotion, transmission, staging, commit or push occurred.
