# Root exact-copy follow-up ledger

September20,2026 UTC. Local working research. Read PROTOCOL.md and the preceding
release25-source-locator/report.md. Initial scope: four queries/eight metadata
requests maximum; actual use: **two queries/four metadata-page requests**.
No need to exhaust a cap after the relevant archive endpoint rate-limits.

## External requests

1. Web open <https://archive.org/help/wayback_api.php> returned241 parsed lines.
   The API section describes the read-only availability endpoint, its returned
   closest-capture record and an empty available-snapshot result. Inspected
   lines178–238. This supplies endpoint semantics, not any target availability
   result. No new response body was pinned locally.
2. Anonymous curl, documented availability endpoint for the exact observed
   first-title-segment wiki page:
   `https://archive.org/wayback/available?url=http%3A%2F%2Fwww.911datasets.org%2Findex.php%2FSFile%3AW3UYIIVYDLXD7AUBDCPMEYX7L74N6JRY`
   → exit56, reported HTTP429; no body saved.
3. Same route for the second title segment:
   `https://archive.org/wayback/available?url=http%3A%2F%2Fwww.911datasets.org%2Findex.php%2FSFile%3AB5F6OLNOMMZPUDDARF3QIT62BCVZJXAC`
   → exit56, reported HTTP429; no body saved.
4. Same route for the third title segment:
   `https://archive.org/wayback/available?url=http%3A%2F%2Fwww.911datasets.org%2Findex.php%2FSFile%3AGNKALFTXU3LVPSPQVRM3GALVZ6FCMDQC`
   → exit56, reported HTTP429; no body saved.

Requests2–4 formed one parallel batch, not retries. All disabled curl config,
required HTTPS/HTTPS redirects, and used a25-second/2000000-byte ceiling.
After that batch root stopped Archive requests and asked the independent lane
to defer them too. No hostname/transport cycling, immediate retry or account
was used. These failures do not return `archived_snapshots:{}` and must not be
reported as an availability search proving no snapshot. No media or torrent
metadata was transferred; no private case payload or credentials were sent.

The two public indexed queries were submitted together:

- `"W3UYIIVYDLXD7AUBDCPMEYX7L74N6JRY"`
- `"42A0122" "VTS_01_1.VOB"`

The combined response was explicitly empty. Do not infer independent per-query
coverage or an exhaustive web absence. Root did not repeat the other lane's
excluded-domain folder query. Four page slots and two query slots remained
unused; neither cap is a mandatory quota.

## Held official-catalog response check

Local parsing searched all returned fields of each file object in the six
previously saved normalized official-catalog responses below. Case-insensitive
pattern: `42A0122|G25D33|Video[_ ]?List|\.mdb\b|VTS_01`.
Result:282 rows/282 unique IDs, zero matches. These are held responses, not
new live catalog requests. A name/metadata nonmatch is not a content screen
or proof that a renamed/transcoded copy is absent. Each structured response
has only the `files` key; this does not demonstrate exhaustive pagination.
The previous unit's35 returned-but-unlisted folders remain unlisted here.

Paths below are under `../late-fire-original-tape-catalog/sources/`:

| File | Rows | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| root-list.response.json | 9 | 7720 | d0e5b9b4af8251e29909e1a95e36bffa9b82936b9586ae50546635806cf4f0af |
| general-list.response.json | 239 | 200598 | 13cea8a3bb6a53a851b58058985e3b93c6eb3f07dcdf76160b61aadb5eb443db |
| other-list.response.json | 6 | 5179 | c78a9572c6013303ef67a33ee9da995cfff82f21bc72eeba589cdabbce43cac2 |
| cd-list.response.json | 2 | 1800 | 4496ca5171344d2c0f4f69da409ad8049536788696cde04be0f3787253f756bb |
| cdvideo-list.response.json | 24 | 20161 | 13684f381a30e3571566fd88f0e64c15635e78faf981f972fb20d10f21174931 |
| analysis-list.response.json | 2 | 1838 | 2c6a1dd87bf581a970979cd7f88b563c9fa7f8e26b6e5753d9b61be702b37145 |

Execution: a Python standard-library read-only loop loaded each
`structuredContent.files` array, applied the pattern to `json.dumps(item)`,
counted rows/unique IDs and computed SHA-256 on raw saved response bytes.
It returned0 and the counts above. It did not inspect source media, query
private account data, or authenticate historical production completeness.

## Disposition

No exact-copy or populated official-catalog join obtained. The previous exact
eight-file directory locator remains valid and distinct. Archive rate limiting
is a temporary route failure, not evidence about retention, withholding,
concealment or cause. Current-copy searching is deferred within this unit;
another feasible charter test should proceed rather than recursive speculative
locator work. Future archive retries need a separately declared respectful
backoff scope or a concrete newly observed source, not a guessed item ID.
