# Wayback companion-index ordinary-route retry — 2026-10-10T125812Z

**Record type:** source-pinned public access check. This is one read-only retry of the listed companion CDX index through the ordinary Internet Archive download URL. It does not inspect the index, authenticate an ARC record, or explain the earlier CDX/replay discrepancy.

## Request and observed response

At the response-header times recorded below, an unauthenticated GET was made to the public item-metadata download URL for `live-20110512001821253-00298.arc.os.cdx.gz`. The client followed the server's ordinary redirect; no credentials, cookies, alternate storage host, or access-control bypass were supplied.

- At the archive.org endpoint: HTTP/2 `302`, header `Date: Sat, 10 Oct 2026 12:58:12 GMT`, redirecting to the storage URL listed below.
- At the redirect target: HTTP/2 `401`, `Date: Sat, 10 Oct 2026 12:58:13 GMT`, `content-length: 172`. The final response was `text/html; charset=UTF-8`, 172 bytes, and identified by `file` as ASCII HTML—not a gzip index.
- Final URL: <https://dn721500.ca.archive.org/0/items/live-20110511220555245-00271-00372/live-20110512001821253-00298.arc.os.cdx.gz>
- The captured response body SHA-256 is `9371176869a945e2958e43b349397210a1b72b83f11c67e02e0be1f950254ef2`.
- The complete captured redirect/final response-header file SHA-256 is `69673f169f35ac5584a7bed5a00e07b6be90d4052a404ea498b97ca30ce85663`.

The 172-byte body was byte-compared with the earlier 2026-10-10 03:14:57–03:14:58 GMT retry body preserved in the Faraday worktree; `cmp` found them identical. The full header captures are not identical: this retry has its own timestamped header file and hash. The earlier retry's header hash was `e8ed8ba4937d058dce33313d057729bbdf1ba74aa517191bc73c7e811959a814`.

## Interpretation ceiling

This retry records that the ordinary listed download route again returned a redirect followed by HTTP `401`, rather than the requested index bytes, at the stated time. It confirms the missing-input condition for this retrieval attempt only. It does not show why the storage endpoint returned `401`, whether the index or ARC is absent, what either contains, or whether the service will respond differently later. No access-control bypass or alternate-host attempt was made.

This result does not change or resolve the separate CDX-versus-replay discrepancy. It supplies no new payload evidence and does not support a conclusion of deletion, substitution, or deliberate withholding.

## Source and preserved bytes

- Requested public URL: <https://archive.org/download/live-20110511220555245-00271-00372/live-20110512001821253-00298.arc.os.cdx.gz>
- Final redirect target: <https://dn721500.ca.archive.org/0/items/live-20110511220555245-00271-00372/live-20110512001821253-00298.arc.os.cdx.gz>
- Item metadata listing the companion index and ARC: <https://archive.org/metadata/live-20110511220555245-00271-00372>
- Faraday source files for this retry:
  - `review/wayback-index-download-retry-2026-10-10T125812Z.response.html`
  - `review/wayback-index-download-retry-2026-10-10T125812Z.response-headers.txt`
- Public redundant copies:
  - `investigation/wtc7/wayback-replay-capture-2026-10-09/wayback-index-download-retry-2026-10-10T125812Z.response.html`
  - `investigation/wtc7/wayback-replay-capture-2026-10-09/wayback-index-download-retry-2026-10-10T125812Z.response-headers.txt`
- Earlier retry record: `review/wayback-cdx-arc-index-access-retry-2026-10-10.md` in Faraday; public and private copies remain in their respective worktrees.
- Retrieval method and access times are recorded above; no data from the requested index were retrieved.

