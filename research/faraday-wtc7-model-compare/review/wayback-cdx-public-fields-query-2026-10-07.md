# Wayback CDX query using documented public fields (2026-10-07)

**Record type:** live archive-index response, plus a separately preserved
failed request attempt. This note records the endpoint's outputs; it does not
authenticate archived video bytes or reconcile prior capture/replay metadata.

## Query and response artifacts

The query used the seven field names listed as publicly available in the
source-pinned Wayback CDX Server README. It requested the same NIST-named CU
animation URL as the prior locator query, but did not request `filename` or
`offset`:

`https://web.archive.org/cdx/search/cdx?url=www.nist.gov%2Fpublic_affairs%2Freleases%2Fwtc_videos%2FCU%20animation.flv&output=json&fl=urlkey%2Ctimestamp%2Coriginal%2Cmimetype%2Cstatuscode%2Cdigest%2Clength&gzip=false`

The pinned documentation and its hashes are recorded in
[`wayback-cdx-field-semantics-2026-10-07.md`](wayback-cdx-field-semantics-2026-10-07.md).

### First attempt — failed response

- HTTP status: `502`.
- Response `Date`: `Wed, 07 Oct 2026 15:10:30 GMT`.
- `content-type`: `text/html`; `content-length`: `107`.
- Preserved response-header bytes:
  [`wayback-cdx-public-fields-2026-10-07.headers.txt`](wayback-cdx-public-fields-2026-10-07.headers.txt)
  SHA-256: `924e3c322de4f83bcfa372eaf1303723ec4dd54d69d659b0c9225f29d35eee43`.
- No response-body file was retained: curl was run with `--fail`, and the
  command exited with error 56. The failure is not evidence about the archived
  URL's capture or contents.

### Retry — successful response

- HTTP status: `200`; response `Date`: `Wed, 07 Oct 2026 15:11:14 GMT`;
  `content-type`: `application/json`.
- Response body: 1,410 bytes, preserved at
  [`wayback-cdx-public-fields-2026-10-07-retry1.json`](wayback-cdx-public-fields-2026-10-07-retry1.json).
  SHA-256: `a0f1c79071c1723aa9c8cc06e753e01bca052205e5c579099e35c1db9e33bbc6`.
- Response headers, 577 bytes, preserved at
  [`wayback-cdx-public-fields-2026-10-07-retry1.headers.txt`](wayback-cdx-public-fields-2026-10-07-retry1.headers.txt).
  SHA-256: `6e2fc15f9c09de610e410661943acd8775a268bef6d63d957961133352c271ae`.

The first 502 and later 200 are retained as distinct retrieval observations.
No cause for the difference is assigned.

## Direct response observations

The successful JSON contains six rows. Every row's `mimetype` value is
`text/html`:

| Timestamp | Status | MIME type | CDX digest | CDX length |
| --- | ---: | --- | --- | ---: |
| 20110427193523 | 200 | `text/html` | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | 4107 |
| 20110512003203 | 200 | `text/html` | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | 4107 |
| 20110704075052 | 200 | `text/html` | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | 4107 |
| 20160304111136 | 404 | `text/html` | `5SJXT7LNUFKYY2APULQKG5MBHEUJTC5A` | 4125 |
| 20250514101052 | 301 | `text/html` | `QRDVOOVICNUU2ABQT4DWOC7F76EMMRG3` | 646 |
| 20250514103155 | 404 | `text/html` | `7H32AS5KGCWT7IJ7JXKIGLZLJVEJFAYF` | 1099 |

The response also gives the original URL for each row. The last row is the
HTTPS URL; the preceding five are HTTP. The exact rows and field values are
preserved in the JSON artifact.

## Comparison with the earlier query; preserve, do not reconcile

The 2026-10-06 locator note records a different query that requested
`timestamp,original,statuscode,digest,length,filename,offset`. It reports six
rows with `filename:null` and `offset:null`. For the six timestamps above, its
transcribed status, digest, and length values match the corresponding values
in this 2026-10-07 response. This new query adds the `urlkey` and `mimetype`
fields and does not request either locator field.

The CDX result labels all six captures `text/html`, including three 2011 rows
whose status is reported as `200`. This is an observation about the returned
index metadata. The `200` status, `text/html` MIME type, CDX digest/length,
prior identity-replay body sizes/hashes, and prior replay-header WARC names
remain separate reports. No archived payload or WARC record was retrieved or
compared in this step. In particular, this query does not establish that the
2011 replay body was or was not an FLV, or explain any difference between
CDX lengths and replay-body lengths.

## Inference ceiling and next test

This response establishes that the live CDX endpoint returned these six
metadata rows at the recorded access time for this query. It does not
establish the content or authenticity of any capture, WARC availability,
substitution, deliberate removal, or the cause of the recorded status/MIME
values. It has no bearing on the physical collapse mechanism.

**Next test, not performed:** obtain and inspect the exact WARC records named
in the prior replay headers, if accessible, preserving each archive object,
record payload, response, and hash separately. A CDX MIME label is not a
substitute for that payload inspection.
