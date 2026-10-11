# Drawing packet acquisition and reading receipts

October 4, 2026. Working research. The protocol was saved before acquisition
or new-page viewing, SHA256
`b0076f130b9f6004534c89a4ab074881422d1401661dddb68f2a504763887048`.
Current status and the complete prior lookup report were inspected. Main
AGENTS/WORKFLOW/START-HERE/CHARTER hashes match the fully read controls.
Intake `db72c0` printed the expected ca1c2233 HEAD and research WIP; its
combined exit 1 was the final `rg --files -g AGENTS.md research` no-match,
not a failed status/hash check. No nested research AGENTS file was found.

## Acquisition

The exact public URLs are fixed in [PROTOCOL.md](PROTOCOL.md). Two web-reader
opens were tool-inaccessible (`turn750view0`, `turn750view1`), not demonstrated
server refusals. One approved direct GET for each exact URL succeeded with
HTTP 200, application/pdf and zero redirects. No credentials, cookies,
private payload, neighboring-ID probe or crawl was used.

Scratch created with `mktemp -d /private/tmp/wtc7-drawing-review.XXXXXX`:
`/private/tmp/wtc7-drawing-review.4PgqcG`. Actual command pattern:

```sh
curl -q --proto '=https' --connect-timeout 20 --max-time 60 \
  --max-filesize 10485760 --fail --silent --show-error \
  --output <scratch-PDF> \
  --write-out 'http=%{http_code} bytes=%{size_download} type=%{content_type} redirects=%{num_redirects}\n' \
  <exact-PROTOCOL-URL>
```

| Source | Terminal receipt | Bytes | Actual pages | SHA256 |
|---|---|---:|---:|---|
| NYC-WTC_000167874.pdf | e042ed | 258425 | 3 | 18fd09dd9631551ab11f88fc18f56b759338707739463e2a313cc601c2d705af |
| NYC-WTC_000173670.pdf | a4ddd4 | 67561 | 1 | 89dfc492e45ca53e8e1247b07d3bd34cd476d80d5a2f13107f7846a162dc0627 |

167874 handle 99735 was polled to its terminal exit 0; 173670 completed exit
0 initially. Basic pypdf admission (`981433`, exit 0) confirmed PDF magic,
expected size/pages, no encryption, AcroForm or OpenAction for both. This is
not exhaustive safety or historical authentication. No confidentiality marking
was observed in root's full-page reading; personal contact/signature fields
are not transcribed into research narrative or feedback.

File completion mtimes (`2d8cd9`, exit 0) were October 4, 2026, 16:29:23
and 16:29:21 America/New_York (UTC-04:00), respectively. They are acquisition
file times, not historical issue dates. Approved `cp -n` source preservation
completed `1ae22c`, exit 0.

## Rendering and preservation

Configured bundled dependencies were refreshed. Version check `62a896`,
exit 0: Poppler 26.05.0, Python 3.12.14. Font configuration was created via
apply_patch, naming `/System/Library/Fonts`, `/Library/Fonts` and an explicitly
created private scratch `font-cache`; the cache's existence does not prove
use. Saved config is 227 bytes, SHA256
`f9499b5297acac777a3d1f2a34e95d90c848dd78458f92410d396c6003579b9d`.

Root commands used this config through FONTCONFIG_FILE and the bundled
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm`:

```sh
pdftoppm -f 1 -l 3 -png -scale-to 2400 <167874-PDF> <scratch>/167874
pdftoppm -f 1 -l 1 -png -scale-to 2400 <173670-PDF> <scratch>/173670
pdftoppm -f 1 -l 1 -png -scale-to 4800 <167874-PDF> <scratch>/167874-large
```

These are abbreviated command bodies; the actual tool calls had explicit
absolute source/config/destination paths and redirected stderr to separately
saved files. Initial handles 15798/29885 reached terminal exits 0 at
`ecefb0`/`1bdab0`; no stdout. The larger repeat was declared in root's page-1
notes before its render; handle 64875 reached terminal exit 0 at `b0901c`.
All three stderr files are empty (`505b3a`, `0eb9b2`, `2d8cd9`), SHA256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

| Raster | Bytes | Saved dimensions | SHA256 |
|---|---:|---|---|
| 167874-1.png | 165868 | 1794 x 2400 | ab2795f787efa3c647bfc490565048f6dec3ac03a35187831fa569b99b02f177 |
| 167874-2.png | 214621 | 1808 x 2400 | 7e858a2730345108a0286f19806b944639bb5fdacbb4589a2e9e70d92b7ab7fc |
| 167874-3.png | 191288 | 1796 x 2400 | 4eaee541f0229937f5b94881835a73dcba7586f20ae5417c383245be09e67926 |
| 173670-1.png | 158480 | 1785 x 2400 | 78a23519c065afb9d06119f70f5b99e4085fb598887356163c0b47646189430f |
| 167874-large-1.png | 1225932 | 3588 x 4800 | f942fadce34f3a1305bc9943c74db238a4a3565f89b58fd8655994acbd96e032 |

Five images, three diagnostics and the config were preserved without overwrite
at `7be3c3`, exit 0. A byte/hash/PNG-header check (`2d8cd9`, exit 0) confirmed
all eleven source/derivative/diagnostic/config files equal their scratch copies.
This does not compare different historical documents for pixel identity.

## Root coverage and freezes

Root viewed 167874 pages 1, 2, 3, then 173670 page 1. A single permitted
larger page-1 repeat followed a saved unreadability reason before advancing
to page 2. All notes were saved before the next view. Four initial views
returned no explicit resize notice to root, which does not establish calibrated
native display. The 3588 x 4800 repeat explicitly displayed at 2750 x 3680.
Dense small callouts remain unresolved; no OCR, crop or measurement substituted.

Root new reading froze at SHA256
`6b9a12d6da02d26d9e8e7b70ffb662d781c31a74ab42fcbe3f88a1a44793f927`
before the prior-cover view. The printed hash at `1871ee` succeeded; its
combined exit 1 was a following formatting search with no matches. A literal
stray plus sign was later noticed and disclosed in the comparison; the frozen
reading was not edited. Both pins rechecked at `7be3c3`, exit 0.

Only then did root view the complete held 167873 cover once, with no repeat.
Separate comparison froze as
`7b40b2e9cb31d047a2ce8932abd998bee856a3926ced3c523a56bc00713650ee`.
Total root views: four new first views, one larger repeat, one prior cover.
No peer substantive findings were consulted before either freeze. Original
source notes and main/legal records remain unchanged.

## Independent reading and derivative receipts

The second reader completed the same four new-page first views, the sole
permitted larger page-1 repeat and one old-cover view. New reading froze
before the cover view at `3e6bd4`, exit 0, SHA256
`a494d998cc4bf5a1ddb2f314234f3906683b59def76ca46898f46e6857fa4df1`.
Its separate comparison froze at `e73091`, exit 0, SHA256
`995e12d126768cab045a3aa9b61c0e72cbdc94fca79252dc22751f80728abc2e`.
Substantive exchange followed both readers' freezes. Root read both complete
peer records; the peer's root-text/hash check `c46ca6` exited 0.

The material disagreement is the reinforcement-overlap numeral: root reads
1 foot 0 inches, peer 1 foot 6 inches. Neither is promoted to an agreed
dimension or used numerically. The peer also retains lower confidence in the
base date and work-with lettering. The final report preserves those differences
and the disparate returned display sizes. No extra source views resolve them.

The complete independent rendering receipt, `derivative-check.md`, froze at
SHA256 `81fa3f3eb3286e1befafdb7308f4c076598fa3c4c4c56b5ed2a3351e35f0f43e`.
It records three actual fresh renderer executions, all exit 0, empty stdout
and stderr, and exact byte/dimension matches for all five used new-page rasters.
Terminal receipts were `a4bb3e`, `144dc8` and `be8200`; comparisons were
`0d79dd` and `6e5c19`, exit 0. Source pins remained unchanged. Root read the
complete receipt at `a82da9`, exit 0. Same-renderer reproduction is not an
independent source or a resolution of viewer resampling and legibility.

## Synthesis continuation

The intervening coordinate reply reconfirmed an already recorded result and
was no new investigation progress. This continuation resumes the unfinished
source synthesis. Root reread the complete new notes, cover comparison and
source log (`7ee011`, exit 0), and complete peer notes (`81c7b8`, exit 0),
without image views or acquisition. Main controls retain the previously
recorded hashes. A narrow read-only peer crosscheck completed `0cc4da`, exit
0, with protocol and four frozen-reading pins unchanged. It found no further
substantive disagreement and emphasized preserving revision-versus-issuance
dates and the distinct FSK-E5/E5 labels. Final report review and verification
are recorded below when actually completed.

## Final review and verification

The independent reviewer read the complete report and derivative receipt,
plus targeted locator fields, without new images or source acquisition.
Full-report read `a2c6d3` reached terminal `8223d3`, exit 0; derivative/locator
check `b9c2ee` reached `2deeaa`, exit 0. It found no blocking issue and
confirmed the date, drawing, uncertainty, coverage and reproduction limits.
Reviewed report SHA256:
`0661d0ddaf3398332905565921591a981490eda9b9b212f88f957073b9b9cd7d`.
This is analytical critique, not expert/human acceptance or a new independent
rerun of rendering.

Root's stdout-only bundled-Python check `c891ef`, handle 28024, reached
terminal `9023af`, exit 0. It used pathlib/hashlib to compare 16 fixed
protocol/reading/receipt/source/configuration pins, including the old cover
PDF and raster; all matched. It checked the five new PNG signatures and
header dimensions with struct. A metadata-only pypdf enumeration of every
`NYC-WTC_*.pdf` under this municipal unit found **19 unique filenames,
43 physical pages and 10 content-unit directories**. Per-unit page totals:
root 11, design-sprinkler 4, drawing-review 4, enclosure-framing 2,
folder-siblings 5, followup 8, FSK-56 3, fuel-route 1, hatch 2, structural 3.
Metadata enumeration is not itself content reading; coverage is supported
by this and the earlier reading records. No new page content was viewed.

Actual final checks from the investigation worktree:

```sh
git diff --check -- research/README.md research/sherlock-wtc7-investigation/STATUS.md
```

That command passed. A subsequent stdout-only Python check verified the
reviewed report hash, final new-file newlines, trailing-whitespace absence
in the two current unit narratives and edited navigation sections, **17 local
link targets**, and presence of the next-task navigation. It passed in
`cf39ee`; handle 6386 then returned the complete report and edited navigation
for root readback, terminal `2e43d0`, exit 0. Git does not check untracked
file whitespace, which is why the new narratives were checked separately.
No historical result was recomputed or uncertainty criterion changed.

Repository intake finished `ef2d1d`, exit 0; scoped status finished `be32ad`,
exit 0. Branch remains research/sherlock-wtc7-investigation at ca1c2233 with
intentional research WIP. Slow live reads were polled to terminal, not
restarted. An incidental process-list diagnostic was denied (`95350e`,
exit 127); no process-state or scientific finding relies on it.

The existing SFB-002/SFB-005 display-integrity, conflicting-transcription and
acquired-attachment-closure notes already cover this recurrence (bounded
read `9a20f9`, exit 0). No duplicate product-defect claim, new feedback send,
archived-task change or delivery acknowledgment is made. Updated existing
STATUS and research navigation point to the completed report and the exact
next unreviewed route candidate; they do not replace the charter or source
records. The full goal remains active and incomplete.
