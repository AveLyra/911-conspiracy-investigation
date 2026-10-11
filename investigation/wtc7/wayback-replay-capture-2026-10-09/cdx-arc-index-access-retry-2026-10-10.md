# Wayback CDX and ARC-index access retry — 2026-10-10

**Record type:** bounded public-source access audit. This note records current index, metadata, and HTTP-header observations. It does not authenticate the historical capture payload, explain any discrepancy, or establish deletion or substitution.

## Scope and method

On 2026-10-10 UTC, read-only requests were made to the public Wayback CDX and replay endpoints and Internet Archive item-metadata/download endpoints. The request was limited to the whole-building animation capture at `http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv`. No credentials, cookies, alternate storage hosts, or access-control bypasses were used. The 100 MB ARC file was not downloaded. The companion index download did not yield usable index bytes.

The Wayback CDX documentation describes CDX as the index used by Wayback to look up captures and lists fields including `timestamp`, `original`, `mimetype`, `statuscode`, `digest`, and `length`. It also documents that some fields, such as `filename`, may be access-restricted: [Internet Archive Wayback CDX Server README](https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md).

## Direct observations

### 1. Repeated CDX query, including locator fields

A read-only query to `https://web.archive.org/cdx/search/cdx` requested the exact URL, the 2011 date range, JSON output, and fields `timestamp,original,statuscode,mimetype,digest,length,filename,offset`. The endpoint returned HTTP 200 and these rows:

Query parameters were `matchType=exact`, `from=2011`, `to=2011`, `output=json`, `limit=10`; the `url` value was `http://www.nist.gov/public_affairs/releases/wtc_videos/whole building animation.flv` (submitted with `--data-urlencode`). The exact `fl` value was `timestamp,original,statuscode,mimetype,digest,length,filename,offset`.

| Timestamp | Status | MIME type | Digest | Length | `filename` | `offset` |
|---|---:|---|---|---:|---|---|
| `20110427194914` | `200` | `text/html` | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | `4112` | `null` | `null` |
| `20110512003203` | `200` | `text/html` | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | `4113` | `null` | `null` |
| `20110704075052` | `200` | `text/html` | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | `4113` | `null` | `null` |

Thus, this query again displayed capture metadata, including the repeated digest and HTML classification, but did not return a filename or offset in the requested fields. The response body was not separately saved or hashed; the rows above are transcribed from the command output.

### 2. Current identity-replay response headers

A read-only `HEAD` request to the May 12, 2011 whole-building identity-replay URL returned HTTP/2 `200` with `content-type: text/html; charset=UTF-8`. The response included:

```text
date: Sat, 10 Oct 2026 03:00:10 GMT
x-archive-orig-date: Thu, 12 May 2011 00:32:03 GMT
x-archive-orig-server: Apache
x-archive-orig-nist: g4
x-archive-orig-transfer-encoding: chunked
memento-datetime: Thu, 12 May 2011 00:32:03 GMT
x-archive-src: live-20110511220555245-00271-00372/live-20110512001821253-00298.arc.gz
```

These are the selected fields as returned in the present Wayback response. The complete raw response-header block was not saved. The `x-archive-orig-*` fields are reported here as header observations; this check did not inspect a raw ARC record to authenticate their correspondence to its original HTTP block.

### 3. Public item metadata lists a matching ARC file and a companion index

The public metadata endpoint for item `live-20110511220555245-00271-00372` returned HTTP 200 and identified it as `Liveweb Capture 2011-05-11T22:05:55PDT to 2011-05-12T01:40:59PDT`, media type `web`. Its file listing included:

| File listed by item metadata | Size | Metadata-reported MD5 | Metadata-reported SHA-1 | Metadata `source` |
|---|---:|---|---|---|
| `live-20110511220555245-00271-00372.cdx.gz` | 49,124,545 bytes | `e646d8bb031a4922fc5301baf360e6f4` | `e39b75680a54572c69e225dccf5d5338d6b6914a` | `original` |
| `live-20110512001821253-00298.arc.gz` | 100,048,974 bytes | `a088b5339f89faa5282adfa6cefc713f` | `4e0f70d0237ee6c10e0f78c38821d11bda6243ee` | `original` |
| `live-20110512001821253-00298.arc.os.cdx.gz` | 655,107 bytes | `afb00b6ecd49f4e8e3d659c6c3b085cb` | `28d6a398083c183ea0aeac6e2dc6a733c43d81ad` | `derivative` |

The exact item path and filenames correspond to the `x-archive-src` value observed in the replay response. The item metadata exposes source-reported MD5 and SHA-1 values; these hashes were not recomputed locally because the files were not retrieved. The `.arc.gz` suffix identifies the listed container as ARC-named, not WARC-named. No ARC record was inspected.

### 4. Companion-index download attempt returned an access error

A streamed GET attempt for the 655,107-byte companion index did not yield a usable gzip stream (`gzip: (stdin): unexpected end of file`). The follow-up HEAD request with redirects showed:

```text
archive.org download endpoint: HTTP/2 302
redirect target: https://dn721500.ca.archive.org/0/items/live-20110511220555245-00271-00372/live-20110512001821253-00298.arc.os.cdx.gz
storage-host response: HTTP/2 401
```

This is one observed response sequence at the recorded time. It does not establish that the file is permanently unavailable, absent, or intentionally withheld. No retry against another host, credentialed request, or other bypass was attempted.

## Interpretation and limits

- **Observed:** the public CDX query lists three 2011 entries classified as `text/html`, all with the same CDX digest label and lengths of 4,112–4,113 bytes; the queried public response gave `null` for `filename` and `offset`.
- **Observed:** the current replay HEAD response is HTTP 200 HTML and exposes an `x-archive-src` path naming an `.arc.gz` file.
- **Observed:** the matching Internet Archive item metadata lists that ARC-named file and a 655,107-byte companion `.arc.os.cdx.gz` index, with source-reported hashes.
- **Observed:** a direct public request for the companion index redirected and then received HTTP 401; no index bytes were obtained.
- **Not established:** what the companion index contains; the target record's offset; whether its ARC payload is HTML or video; the original HTTP status/header block; whether the April/May/July records contain byte-identical content; or why the replay response differs in size from the indexed lengths and previous 13,113-byte error-page captures.
- **Not evidence of:** deletion, substitution, deliberate interference, or a particular historical cause.

The next discriminating step, if the same public download route becomes available, is to retrieve and hash the exact companion index, find the target URL/timestamp row, and use the listed locator to inspect only the matching ARC record and its encapsulated HTTP response/payload. If the public endpoint continues to return 401, preserve that access result and stop; do not bypass it.

## Source URLs and retrieval record

- CDX endpoint: <https://web.archive.org/cdx/search/cdx>
- May 12 identity-replay URL: <https://web.archive.org/web/20110512003203id_/http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv>
- Item metadata endpoint: <https://archive.org/metadata/live-20110511220555245-00271-00372>
- Companion-index download URL: <https://archive.org/download/live-20110511220555245-00271-00372/live-20110512001821253-00298.arc.os.cdx.gz>
- ARC-file download URL listed by item metadata: <https://archive.org/download/live-20110511220555245-00271-00372/live-20110512001821253-00298.arc.gz>
- Access date: 2026-10-10 UTC. HTTP `Date` values are reproduced above where the endpoint returned them.
- SHA-256 of downloaded CDX/ARC bytes: not available; neither file was retrieved. IA metadata-reported MD5/SHA-1 values are listed above and were not locally verified.
