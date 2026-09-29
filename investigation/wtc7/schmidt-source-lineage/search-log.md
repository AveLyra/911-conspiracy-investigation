# Bounded source search, 2026-09-24

Six targeted queries, in two batches; no further general query. Returned
items cannot be uniquely attributed to individual queries within a batch.
Only relevant source-route leads are recorded; incidental personal-directory
and namesake results were not followed or retained in research files.

| ID | Exact query |
|---|---|
|Q1|`"Terry Schmidt" "WTC 7" photographs`|
|Q2|`"Terry Schmidt" "September 11" photos original`|
|Q3|`"Terry Schmidt" "5-127"`|
|Q4|`"Terry Schmidt" WTC photographs -site:scribd.com -football -NFL`|
|Q5|`"Terry Schmidt" "wtc7" photos`|
|Q6|`"Terry Schmidt" photos 911 photographer New York`|

The first batch surfaced a GovInfo copy of NCSTAR1-9 with indexed Figure5-30
and several secondary references. Root used the already-held PDF, not a fresh
GovInfo download. The second batch supplied two historical published routes:

- `http://www.nycwireless.net/Images/wtc2/`, cited in a secondary blog's
  reproduced footnote as a Schmidt gallery. The footnote's ownership and time
  claims are not independently verified. No secondary technical claim is used
  as evidence of fire severity, opening state, cause or an authenticated clock.
- `http://ken.ipl31.net/gallery/albums/wtc/img_1479_001.jpg`, cited in a
  secondary filing/book extract as a Schmidt debris photograph. This is a
  source-family navigation lead, not an identified match to Figure5-127.

## Actual page attempts

|Route|Tool outcome|Permitted conclusion|
|---|---|---|
|NYCWireless gallery|Web reader reported its HTTPS form inaccessible.|No content or asset list obtained; reason not diagnosed from this result.|
|Ken image|Web reader reported its HTTPS form inaccessible.|No image acquired/inspected; no original-image absence finding.|
|NYCWireless gallery, ordinary in-app browser|Displayed an explicit Cloudflare access block.|Present access denied on this route. Stopped; no alternate host, identity, proxy, header or login attempt.|

Two unique external targetURLs attempted, within the ten-page ceiling. The
browser attempt followed a generic web-reader access failure, before the
explicit block was known. No block was bypassed; no owner contacted. The
agent-created browser tab was closed after reading the block. No remote media,
origin HTML, EXIF, original filename, adjacent exposure or timing record was
acquired. No private browser state or blocked-page identifiers were exported.

Search snippets are discovery evidence, not byte-preserved origin documents
or independently authenticated historical statements. The six-query ceiling
is a finite search, not proof that no better image exists elsewhere. Sources
merely surfaced in results were not thereby read in full.

## Existing holdings and new local title query

The independent reviewer searched existing textual research in main and the
worktree and read specific source maps/acquisition notes. No earlier
Schmidt-specific gallery/original-name/adjacent-frame/clock record was found.
That was not an archive-interior, all-PDF/OCR or complete-filesystem review.
Prior Didik and NIST-folder refusals were retained, not retried.

After the newly viewed Figure5-31 supplied a workbook-title lead, root used
these case-insensitive alternatives against all returned file names in the
main and investigation roots, excludingGit:

`north[ _-]*face[ _-]*at[ _-]*3[ _:-]*12|312[ _-]*pm.*draw|updated[ _-]*vl[od].*draw`

Command: `rg --files --hidden --no-ignore -g '!**/.git/**' -g '!**/.git'`
with both explicit roots, piped to `rg -i` with that expression. Exit1, no
matches or diagnostics. A separate `rg -n -i` using the same alternatives
searched main `intake` and `facts` with `--glob '*.csv' --glob '*.json'`:
exit1, no matches or diagnostics. An independent per-process/NUL-delimited
check supplies the search-coverage validation; this first pipeline alone is
not a proof of each constituent's exit status.

This new title predicate is distinct from the prior native FDS-input locator.
It cannot detect differently named/unindexed spreadsheets, archive-interior
files, image-only titles or unsearched record bodies. No claim that the file
was withheld, destroyed, fabricated or globally absent follows.
