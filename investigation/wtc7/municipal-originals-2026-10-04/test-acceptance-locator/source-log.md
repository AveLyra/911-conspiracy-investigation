# Test and acceptance lookup execution record

Research branch `research/sherlock-wtc7-investigation`, HEAD `ca1c223335c20905d6608eb15c676f88cbfac734`.
Existing WIP remains intentional. The intervening coordinate turn confirmed an
existing result without new investigation progress. This resumed unit completes
the saved metadata analysis. Main control/charter hashes remain unchanged
(`c85c49`, exit 0); the full charter was reread at `af1ab3`, exit 0.

## Acquisition already completed

Protocol froze before requests: SHA256
`3938808129a75bf279e8ca8edb885282a7eb96bd4a58514556091e4254d09163`.
One public portal web-reader open returned an HTML shell without readable
content. No historical content was inferred from that response.

The first sandbox request failed DNS (`f6f70c`, exit 6, HTTP000/zero bytes).
Scoped permission then allowed the five exact saved JSON POST requests to
`https://sept11documents.cityofnewyork.us/api/v2/search`. Each used `curl -q`,
HTTPS only, 20-second connection/60-second total timeout, 10 MiB cap,
`Content-Type: application/json`, exact `--data-binary @request`, saved output,
and no redirects, credentials, cookies or private payload.

| Query | Terminal receipt | HTTP and content type | Bytes |
|---|---|---|---:|
| generator | deb23e, exit 0 | 200, application/json;charset=utf-8 | 66134 |
| signoff | a1fa66, exit 0, original handle 57068 | 200, application/json;charset=utf-8 | 30480 |
| punch | 815271, exit 0 | 200, application/json;charset=utf-8 | 65056 |
| date | 65eb1a, exit 0 | 200, application/json;charset=utf-8 | 1760 |
| control | a05238, exit 0 | 200, application/json;charset=utf-8 | 8451 |

All reported zero redirects. Responses were preserved non-overwriting from
`/private/tmp/wtc7-test-locator.g4fXce` (`fdc28d`, exit 0). The independent
[preservation receipt](preservation-check.md) contains full request/response
pins and all five byte-equality checks. No request was repeated on resumption.
These are acquisition receipts, not proof of the archive's historical claims.

## Reproducible analysis

`check_metadata.py` adapts the preceding drawing-locator contract, adding the
five fixed queries, specified catalog/memo search and local filename joins.
It reads only these local sources and writes only stdout. Run with normal
non-optimized Python; its assertions must not be disabled:

```sh
python3 -B research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/test-acceptance-locator/check_metadata.py
```

The initial complete run ended successfully after original handle 40508.
Its stdout was saved using apply_patch as `root-metadata.json`; freeze checked
at `27c948`, exit 0, before reading peer findings:
`ee1f627b30ad1bdf5cc1073f1b52a6c4aae88b6364e2fd5e65b1c948d080b4c6`.
Initial checker SHA256 was
`873a440c9d223cea470756384b102fb914862e827e3af1532569fe6235aa10d7`.

Ten direct checks passed (`057043`, exit 0): duplicate nested JSON rejection,
invalid scalar shapes/types, preserving literal None, finite numeric scalar,
and equality of a full fresh calculation to saved output. These are focused
checks, not complete parser certification. The independent reader's frozen
review is `5091aad0e76a20f63e082cd2929aa0c7bf852bfe220e3c3978d7f54a4760c34b`.
Its initial assumption that empty results always have a results key failed;
that failure and subsequent explicit empty-response checks remain in its note.

After both freezes, root parsed the peer's complete 111-row table and compared
every ID, query membership, page count and byte count; all agreed. Root also
checked all 111 catalog-folder joins and the 29 matching folders' 37-document/
163-page totals (`fe1730`, exit 0). No PDF content was read for these joins.

## Method corrections without result replacement

Independent synthetic review exposed three checker weaknesses: previous-page
availability and absent termination evidence could be labeled complete, and
an estimate below the returned count went unflagged. Actual saved responses
have none of those conditions. Root added the first two to the incomplete
flag and makes the third stop for explicit review; that stop is not a claim
the source is false. Revised code SHA256:
`d561ee20e778bd0111103b3352f251396f618f2be2a23ad172ad96efb7ac6d7a`.
The complete rerun still equals the frozen result (`026d62`, exit 0).
Final independent correction checks are recorded in `method-review.md`.
The equality checks preceded the next unit's acquisitions. The filename join
reads current local holdings, so a later rerun may legitimately add held-name
matches while all frozen response/catalog-derived records remain identical.

Independent post-freeze comparison (`2619a2`, exit 0) also confirmed all 111
records' eleven scalar fields, 29 catalog matches, five coverage states and
four then-held filename joins. Final report critique found no substantive
issue (`45837d`, exit 0); its temporal wording clarification is incorporated
above and in the report. No historical content was used to select candidates.

The saved metadata, protocol, peer notes, raw responses and original sources
are unchanged. No pagination, new PDF reading, cause ranking, canonical/legal
promotion, engine action, sensitive transmission, fee, staging, commit or push
belongs to this lookup. A separately frozen content protocol is required before
reading the selected four pages. Archived Sherlock feedback routing is unchanged.
