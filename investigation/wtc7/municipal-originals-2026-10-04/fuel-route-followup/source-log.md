# Fuel route source and verification

October 4, 2026. Research only. This record preserves actual retrieval and
rendering, not an inference from the catalog. No overwrite, main/legal edit,
outreach, fee, external source transfer or source promotion.

## Acquisition and identity

Exact official URL from the selected catalog:
https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000171753.pdf

The single tool-reader open returned an internal/inaccessible-tool result,
not a verified server refusal. The separately permitted direct acquisition
succeeded in one request (receipt ad1402, terminal exit0): HTTP200,
application/pdf, 62089 bytes, zero redirects. No retry or guessed neighboring
identifier was used. Command:

```sh
curl --proto '=https' --connect-timeout 20 --max-time 60 --max-filesize 10485760 --fail --silent --show-error --dump-header /private/tmp/wtc7-fuel-route.i3Z5nq/response-headers.txt --output /private/tmp/wtc7-fuel-route.i3Z5nq/NYC-WTC_000171753.pdf --write-out 'http=%{http_code} bytes=%{size_download} type=%{content_type} redirects=%{num_redirects}\n' https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000171753.pdf
```

Headers remain in the local temporary acquisition directory, unprinted and
not copied into the research packet. Python3.12.14/pypdf inspection found
one page, no encryption, no AcroForm or OpenAction. The bytes begin `%PDF-`.
These checks do not establish absence of every possible active object or
historical authenticity. Root's complete visual read found no confidentiality
marking; business contact details/signature remain in the source and are not
transcribed in the research notes or cleared for export.

The inspected source is a June30,1999 letter; fax overlays have separate
July1/July2 dates. The acquisition date is not the letter date. The access
copy bears a matching municipal Bates label and portal overlay; no earlier
custody history is independently authenticated by this download.

## Root render and preservation

`mktemp -d /private/tmp/wtc7-fuel-route.XXXXXX` created the exact acquisition
directory above. A new fonts.conf specifies `/System/Library/Fonts` and
`/Library/Fonts` plus a cache in that temporary directory. No main source or
prior render configuration was modified.

```sh
FONTCONFIG_FILE=/private/tmp/wtc7-fuel-route.i3Z5nq/fonts.conf /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -png -scale-to 2200 /private/tmp/wtc7-fuel-route.i3Z5nq/NYC-WTC_000171753.pdf /private/tmp/wtc7-fuel-route.i3Z5nq/page 2>/private/tmp/wtc7-fuel-route.i3Z5nq/render.stderr
```

Poppler26.05.0 was confirmed by `pdftoppm -v` (session61628, terminal ed42d0,
exit0). Render session36509 was polled to terminal f0b1a5, exit0; stderr is
zero bytes (2aece2). The full PNG is1638x2200,127842 bytes. Root viewed it
once at original detail before freezing notes; no text extraction or repeat.

Approved `cp -n` of the PDF, PNG, fonts.conf and empty render.stderr to this
directory completed exit0 (04aa37). The stdout-only four-file source/destination
byte comparison completed exit0 (c97c41); all four copies exactly matched.
This is preservation, not a second acquisition or independent rendering.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| NYC-WTC_000171753.pdf | 62089 | `537331e3169cc995e7729b60c61a806fb65348eae916f93f6f1bbc48bed47310` |
| page-1.png | 127842 | `eb8b4cb43b9cf48fef81d1b32c8480351614dce9a0ee7e10c5b56c61503e701a` |
| fonts.conf | 238 | `ebcb3597eeb9d0576cbf96be259a78c63cf8cecc1c4b1fc07d1153d531aa02e3` |
| render.stderr | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Protocol SHA-256: `6fb954173ef52b90815ff28717e4577d28b800c39e49ecdc04387ab07df5488f`.
Frozen root notes: `ce298f97d6930307cba4315be82016619c212a1031d748e14a0ea22053ecec80`.
Both pins returned with PNG dimensions in session23066 terminal04e6dd, exit0.

Independent reading, fresh-render reproduction and final synthesis verification
are pending at this log's initial save. Append their actual results; do not
infer success from a requested check or a merely existing output.

## Completed independent review

The separate reader froze complete one-page observations before reading root's
notes: review.md SHA-256
`b270ff8ddea5c7bcfbe5eacf655a74c24a8fd641c534aa25d2c8162dd26bcc60`.
Root then read the complete note (session20278 terminal106784, exit0) and found
material agreement. Both readers made one full-page view, no repeats.

The independent reproduction used a new temporary directory and font cache,
the same admitted PDF and Poppler26.05.0. Render terminal fede91 exited0;
stdout/stderr were empty. `cmp -s` exit0 (0c7f72), image size and SHA all match
root's PNG. Full commands and limitations are in derivative-check.md, SHA-256
`51ed53aa625cbdfc5b82905e0180abd13dae450413f96ea8930b4c43fe1b8181`.
This is independently executed derivation with the same renderer, not an
independent acquisition or different rendering engine.

The separate reader fully checked report.md at then-draft SHA-256
`91fd30e7943a06feed23e46c5339e8a711c7021a1b78f38078d211cc4955defc`
(1066e2 read;208c2d hash, exit0), found no material correction, and permitted
replacing the pending-render/review paragraph with the actual completed checks.
The later report version preserves the substantive findings. The reader did
not independently reverify the next candidate's catalog row; root's explicit
catalog check remains separately attributed.

## Final local checks

Root read the entire saved derivative check and separately verified the next
candidate's exact catalog row83 and official link104 (session99534 terminal
8f9631, exit0). This did not retrieve or interpret that candidate.

A stdout-only bundled-Python integrity/link check completed in session17925,
terminal9abc7a, exit0: all11 frozen/input pins across the two new units match;
the PDF still has one page; PNG dimensions remain1638x2200; root's preserved
PNG exactly equals the independent temporary render. All10 new Markdown
files ended with a newline, had no trailing whitespace, and all13 local links
resolved. This check is not a whole-repository audit or an engineering test.

Final reports at that check:

- Held-record locator: `53625d5b825d8ad81d7e4d4cc2f27cb14463bf228b8b9df18ad20008c13b3845`.
- Fuel-route comparison: `9f2146edeab41447edd31f2043a9d1e570828ab25476f05a6f85855965a05df6`.

The separate twelve-file metadata recheck (7df699, exit0) confirmed all sizes,
hashes and the reported13/8 token totals. `git diff --check` ran separately
and completed exit0 (session21130 terminalf5cac9). The status/HEAD check
(session83150 terminalb5e918, exit0) confirms the same ca1c2233 HEAD and
intentional research WIP; no staging, commit or push. Existing unrelated WIP
was preserved. Navigation and the deduplicated SFB-005 local note were updated;
the archived feedback destination was not contacted or silently changed.

This log's appended completion record is not included in its own checksum.
All live command handles from these two units have reached terminal receipts.
