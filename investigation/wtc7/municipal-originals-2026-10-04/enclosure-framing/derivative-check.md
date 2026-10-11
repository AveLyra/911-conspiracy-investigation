# Independent enclosure-framing derivative check

2026-10-04. Research only. The held PDF matched its declared 145,877-byte size
and SHA-256 pin. One fresh two-page render reached terminal exit 0 without
warnings. Both PNGs match the saved files byte for byte and by SHA-256.

## Scope and execution receipt

Read `PROTOCOL.md` completely before rendering. Its unchanged SHA-256 is
`53468027e199431d5bd50a4558f312a687924c05d5183b38158420a44eca1bf8`.
The previously read main `AGENTS.md` and `WORKFLOW.md` also retained their
checked hashes; the PDF skill continued to apply. Scope: only pages 1-2 of
the one held PDF, one render, and comparison of every output. No network,
OCR, crop, enhancement, content interpretation or source re-view occurred.

`mktemp -d /private/tmp/municipal-enclosure-derivative.XXXXXX` created
`/private/tmp/municipal-enclosure-derivative.H3mZNC` (`abf73f`, exit 0;
UTC timestamp 14:35:00). The same receipt records the specified executable's
`-v` output: Poppler 26.05.0. From this `enclosure-framing` unit directory,
exactly one render command ran:

```sh
/usr/bin/time -p /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 2 -r 150 -png NYC-WTC_000172233.pdf /private/tmp/municipal-enclosure-derivative.H3mZNC/172233
```

The wrapper printed UTC before/after, captured the render status, and exited
with it. Original session 51086 was polled to terminal completion (`f7281b`,
exit 0), without restart. UTC window: 14:35:21-14:35:26. Timing in seconds:
real 5.07, user 1.21, sys 0.07. No renderer warning/error text was returned;
only timestamps and timing measurements appeared.

`wc -c NYC-WTC_000172233.pdf` returned 145877. `shasum -a 256` before
(`4b5bf9`, exit 0) and after (`38a847`, exit 0) returned the same PDF pin:
`0c1a0d8ea7c269d297e1d5374c4fa2118b848293a8f6cf49c263c82a6830b3f1`.

## Complete comparison and limits

Shell glob counts returned exactly two generated and two saved PNGs. A loop
explicitly enumerated `172233-1.png` and `172233-2.png`, running
`cmp -s /private/tmp/municipal-enclosure-derivative.H3mZNC/<name> render/<name>`
and recording each status. Both returned 0; `comparison_failures=0`
(`96a377`, exit 0). There were no missing or extra pages.

`shasum -a 256 /private/tmp/municipal-enclosure-derivative.H3mZNC/*.png
NYC-WTC_000172233.pdf PROTOCOL.md render/*.png` completed (`38a847`, exit 0).
The fresh and saved PNG hashes agree with each other, the assigned expected
hashes, and the saved-image pre-render check:

| Filename / physical page | SHA-256 of fresh and saved PNG | `cmp` exit |
| --- | --- | --- |
| `172233-1.png` / 1 | `df32ceda93b84dd08a84b802b7c2e3c42f973f828f5c5815e6c9883471af3513` | 0 |
| `172233-2.png` / 2 | `6cd6caac18cb208ca4cb9c6be56d4a7b9c1b4313ca35c6a7f1c06c46c228fa78` | 0 |

No render or comparison failure was discarded, and no retry was required.
The source, protocol and saved images retain their pre-render hashes. Only
this new note was written in the unit; other WIP was not edited. Fresh PNGs
remain in the named temporary directory, which is not durable storage.

Byte agreement verifies local derivation with the same renderer version; it
does not test another renderer, authenticate historical contents, establish
custody/completeness, validate either reader's interpretation, or resolve
existing visual uncertainty. No canonical promotion, human acceptance,
transmission, staging, commit or push occurred.
