# Remaining folder files acquisition and reading record

October 4, 2026. Working research; no legal-record promotion. The protocol
was saved before external acquisition and viewed pages. SHA256:
`d5ca86e049eb57af1d62e9fb0c30a80b9742c65be45af426a7352d1e94595262`.
Main AGENTS/WORKFLOW/START-HERE/CHARTER pins matched the previously fully read
controls (`3ad941`, exit 0). Intake confirmed the same research branch,
ca1c2233 HEAD and intentional uncommitted research WIP.

## Retrieval and admission

Exact City PDF URLs are fixed in [PROTOCOL.md](PROTOCOL.md), using actual
document IDs from the preceding metadata unit. Three web-reader opens
returned tool-inaccessible errors (`turn748view0` through `turn748view2`),
not demonstrated City refusals. One direct HTTPS GET for each exact URL then
succeeded. No neighboring-ID probe, retry, redirect or crawl occurred.

Scratch created by `mktemp -d /private/tmp/wtc7-folder-siblings.XXXXXX`:
`/private/tmp/wtc7-folder-siblings.oMfxnD`. Commands used:

```sh
curl -q --proto '=https' --connect-timeout 20 --max-time 60 \
  --max-filesize 10485760 --fail --silent --show-error \
  --output <scratch-PDF> \
  --write-out 'http=%{http_code} bytes=%{size_download} type=%{content_type} redirects=%{num_redirects}\n' \
  <exact-PROTOCOL-URL>
```

The bracketed placeholders identify the three actual literal URL/file pairs,
not a verbatim replay command. User curl configuration was disabled. No
cookies, credentials or case payload were supplied. All three responses were
HTTP 200, application/pdf, zero redirects and terminal exit 0.

| PDF | Receipt | Bytes | Pages | SHA256 |
|---|---|---:|---:|---|
| NYC-WTC_000167240.pdf | 553fb5 | 79462 | 2 | 311bd1d07101b27d4055560cfc95b514c1d4a698a6a3c46bf4c367dbf4ca9321 |
| NYC-WTC_000167759.pdf | fc2f32 | 79419 | 2 | 88d8cce3415188e9c24c01b43cb64a3ac1219c681626d65b914c127ad4cedf31 |
| NYC-WTC_000171557.pdf | c19b34 | 85393 | 1 | d1b979b49cb0f13259ec08a514d2e5629265f1d0f08df4fd2cd7c905cacf615a |

Bundled Python 3.12.14/pypdf admission (`0b1f5d`, exit 0) confirmed PDF
signatures, exact metadata sizes/page counts, no encryption, no AcroForm and
no OpenAction. This is basic file screening, not exhaustive safety or
historical authentication. No confidentiality marking was observed in root's
complete-page reading. Routine contact/signature details stay in originals;
they were not transcribed into the research synthesis or software feedback.

Scratch-file completion mtimes (UTC, not historical document dates): 167240
19:56:00.924551; 167759 19:55:57.561424; 171557 19:55:58.788356.
Three source PDFs were copied without overwrite (`8cb8fe`, exit 0).

## Derivation and source preservation

Dependencies came from the configured bundled runtime; Poppler version
26.05.0 and Python 3.12.14 were checked (`94d013`, exit 0). Root's
apply_patch-created font configuration names `/System/Library/Fonts`,
`/Library/Fonts` and an explicitly created private font-cache directory.
Configuration SHA256:
`15b893a735c43ebdbfbe93e9e298ce12edef1ed21cde7e165934328c47c726cb`.
Its existence does not establish cache use.

Each PDF was rendered exactly once, with `FONTCONFIG_FILE` set to the saved
scratch configuration and the bundled `pdftoppm` executable:

```sh
FONTCONFIG_FILE=/private/tmp/wtc7-folder-siblings.oMfxnD/fonts.conf \
  /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm \
  -f 1 -l <2-or-1> -png -scale-to 2200 <scratch-PDF> <scratch-ID-prefix> \
  2> <scratch-ID.stderr>
```

Actual page limits were 2, 2 and 1. Render handles 19229/78541/6143 reached
terminal receipts `b986f2`/`9a6a3e`/`929c31`, respectively: exit 0 and no
stdout. All three preserved stderr files are empty (`1ef9d1`, exit 0), each
SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
No rerender, OCR, crop, rotation or enhancement occurred.

| PNG | Bytes | Saved dimensions | SHA256 |
|---|---:|---|---|
| 167240-1.png | 129872 | 1645 x 2200 | 8a5607a7c00615267ab79c75a2050c4d7460b6a598c4e6360529b25b1d156c7e |
| 167240-2.png | 68398 | 1648 x 2200 | 4c1e7f64256d3ad51c6bdf2acfe44d6a7c5549286032348a7fb90afae8b59766 |
| 167759-1.png | 129849 | 1647 x 2200 | 94162430e835e4f4a2877fd1cf6f5a1a46dce71d816751007567c606fe91dba7 |
| 167759-2.png | 67579 | 1645 x 2200 | 151e4d9193f14d769a146b7749869735e4e5e0460fae758f95a4ced311650391 |
| 171557-1.png | 193572 | 1636 x 2200 | e893eb6eff3be34e71ed2e1d743e49be11fbc57cacb70a9715c8a80a56ad0c6f |

Five PNGs, configuration and three diagnostic files were copied without
overwrite (`be2af7`, exit 0). A stdout-only file/hash/PNG-header check
(`3aeb28`, exit 0) verified all twelve preserved files against their scratch
bytes and produced the dimensions, sizes and hashes above. This is not a
test that different historical document copies have identical pixels.

## Root reading and comparison freezes

Root requested five complete new-page original-detail views in declared
order, saving each page's notes before the next. No explicit resize notice
was received; this is not certified native-display geometry. Material fields
were readable; zero 4400-pixel repeats were needed.

The complete [new reading](root-observations.md) froze before any older-page
revisit or peer reading at `be2af7`, exit 0:
`d728463a155c2eaab1140aae951db57a2a7c35509204f2b8ac515b5dfc5df072`.

Root then viewed the complete earlier 167235 pages 1/2 and 171300 page 1,
one view each, saving observations before advancement. These existing renders
were not regenerated or changed. The separate
[comparison addendum](root-comparison.md) froze before peer content at
`3aeb28`, exit 0:
`71ba02db89fdbaba8a9c8ba1392326ddb4379f5a7e1b76d31dc5d14db24098f5`.
Eight whole-page views total, zero repeats; no image measurement, OCR or
physical capacity calculation. Minor marginal/forwarding differences are
retained, not erased by a same-content classification.

## Independent completion and synthesis

The second reader completed the same five new full-page views and three
declared prior-page revisits, saving each note before advancing, with no
repeats. The new reading froze before old-page comparison at `c8c403`, exit 0,
SHA256 `493bda42365a758568df8c0f685ce2a2f964cdfd85724354624c5a6eee5a3947`.
The comparison froze at `d88bba`, exit 0, SHA256
`8f980af0ce05a8ad565dda93b2a1bdcc23c38b9c5c3f2df84d08bcb0a20d3982`.
Only then did the peer read root's two frozen notes, reporting no material
disagreement (`6a1d81` and `10f788`, exit 0). Root subsequently read both
complete peer records, including the start omitted by a truncated combined
tool display (`0db52b` and `dfaf5b`, exit 0). No new image views occurred in
this synthesis step. Original readings were not rewritten.

The complete derivative receipt was read by root, with its final limitation
paragraph recovered separately after a truncated combined display. Its SHA256
is `cb78af7d54b78a46fc017071c6daa3a20c70a221835eb8c3f505f7f941555d20`.
All five independently rendered page images match exactly, all sources remain
unchanged, and renderer exits/diagnostics support successful execution. The
two unavailable individual timing lines and font-config differences are not
concealed or replaced by reruns. See the receipt for exact commands and limits.

The intervening coordinate reply reconfirmed an already recorded result; it
was no new goal progress and did not reopen or change this unit's protocol.
Finalizing this comparison is a completed evidence disposition, not a repeated
status assertion. The next action changes from reading these IDs to locating
the specifically referenced design sheets. Full goal remains incomplete.

Post-result peer review found no material correction. It checked the complete
report/source log and six hashes (`150105`, exit 0), then the earlier coverage
counts and named transmittal (`bbc67f`, `8c5890`, exit 0). The reviewed report
SHA256 is `b46a2a4bf0ced2125dbe50fc29e004f76e25358c42b2b63f28f16e0e04d3e451`.
The review confirms 5 PDFs/8 pages across the two folders and the cumulative
17 PDFs/39 pages/nine content-unit arithmetic. It did not revisit images or
independently certify the renderer. This paragraph is a subsequent receipt,
not a change to either reader's frozen notes.
