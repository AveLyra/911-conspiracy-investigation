# Qualification: CDX `offset` output — 2026-10-10

**Record type:** additive methodological qualification to the 2026-10-10
Wayback CDX/ARC-index access retry. This note preserves that report unchanged;
it does not replace its captured output or resolve any archive discrepancy.

## Qualification

The 2026-10-10 retry requested `offset` in the CDX `fl` (field-list) parameter
and recorded `null` in the returned column. The upstream Wayback CDX README
describes `offset=` as a **request parameter for pagination** and does not list
`offset` among its public response fields. Therefore, the observed
`offset:null` from that query is not evidence that the CDX record lacks a
storage offset or locator. It is a literal output of a request for a name not
documented as a response field; its meaning in that response is undetermined.

The same README does not list `filename` among the public fields and says
filename access may be restricted. The query's `filename:null` remains a
recorded output, but the README does not establish why that value appeared in
this particular response. Neither null should be used to infer missing,
deleted, or withheld underlying archive records.

## Corrected-field query and index-download retry

At 2026-10-10 03:15:51 UTC, a second CDX query requested only the six
documented public response fields (`timestamp,original,statuscode,mimetype,digest,length`),
omitting both `filename` and `offset` from `fl`. The endpoint returned HTTP/2
200 with `application/json`. It returned the same three 2011 rows, statuses,
MIME labels, digest labels, and lengths recorded in the earlier retry:

| Timestamp | Status | MIME type | Digest | Length |
|---|---:|---|---|---:|
| `20110427194914` | `200` | `text/html` | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | `4112` |
| `20110512003203` | `200` | `text/html` | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | `4113` |
| `20110704075052` | `200` | `text/html` | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | `4113` |

The response body and headers were saved separately. Body SHA-256:
`5492d9e948eef130887a3365a0134f87172457acb979ccf030b1cda109dfb046`;
header-file SHA-256:
`0ea51e04bc56aa448ec568b3efcb7d88149089bb707ad0bed8ab810f88e38fe4`.

At 2026-10-10 03:14:57–03:14:58 UTC, an ordinary GET of the metadata-listed
companion index again received HTTP/2 302 from `archive.org`, then HTTP/2 401
from the redirect target `dn721500.ca.archive.org`. The final response was
`text/html; charset=UTF-8`, 172 bytes, and its body says “401 Authorization
Required”; it is not a CDX index payload. Captured response-body SHA-256:
`9371176869a945e2958e43b349397210a1b72b83f11c67e02e0be1f950254ef2`;
captured header-file SHA-256:
`e8ed8ba4937d058dce33313d057729bbdf1ba74aa517191bc73c7e811959a814`.
This repeats the access barrier through the ordinary listed download route; it
does not show why that route returned 401 or what the index/ARC contains.

## Preserved observations and limits

- The original retry note remains the record of the exact query, its displayed
  values, the replay response headers, the Internet Archive metadata listing,
  and the observed redirect/401 sequence for the per-ARC index download.
- The query's `offset:null` and `filename:null` outputs remain preserved as
  returned. This qualification changes only what can reasonably be inferred
  from those outputs; it does not alter their recorded values.
- The corrected-field CDX response and the earlier response are both
  preserved. The corrected-field response gives the same digest string in all
  three rows and reproduces the earlier query's documented-field values.
- The public item metadata listed `live-20110512001821253-00298.arc.os.cdx.gz`
  and `live-20110512001821253-00298.arc.gz`. Neither file's bytes were obtained
  in these retries. The ordinary index download redirected and received HTTP
  401 twice; these are time-specific access observations, not proof of
  permanent unavailability or intentional withholding. The saved second
  retry response is an HTML error page, not the requested index.
- No ARC/CDX-index record, encapsulated original response headers, or payload
  was inspected. The relationship among the 2011 CDX rows, replay HTML bodies,
  and the listed ARC remains untested and unresolved.

## Evidence that would advance the test

If the ordinary public download route becomes available, retrieve the exact
listed companion index, preserve and hash its bytes, locate the target URL and
timestamp row, then inspect only the corresponding record in the listed ARC.
Record the ARC record's locator, original response-header block, and payload
separately, with hashes and retrieval details. If the public route continues
to return 401, preserve that result and stop; do not bypass access controls.

## Sources and provenance

- Upstream CDX documentation inspected 2026-10-06:
  <https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md>
  The `master` URL is mutable; the previously recorded documentation note
  states that no source revision or local source-file hash was pinned.
- Corrected-field CDX endpoint and query: <https://web.archive.org/cdx/search/cdx>;
  exact request parameters are recorded above. Response body and response
  headers are preserved in the adjacent files
  `wayback-cdx-corrected-fields-2026-10-10.response.json` and
  `wayback-cdx-corrected-fields-2026-10-10.response-headers.txt`.
- Ordinary index download URL:
  <https://archive.org/download/live-20110511220555245-00271-00372/live-20110512001821253-00298.arc.os.cdx.gz>.
  The 2026-10-10 response body and redirect/header chain are preserved in
  `wayback-index-download-retry-2026-10-10.response.html` and
  `wayback-index-download-retry-2026-10-10.response-headers.txt`.
- Related access retry, left unchanged:
  `wayback-cdx-arc-index-access-retry-2026-10-10.md`.
- Access retry public commit: `fda174cf06473ce553e9b4954aa785cb42b6d518`.
- Access retry private-repository commit: `3cf02472a040e633c3a38e0cace20e498a75ef80`.
- Access retry Faraday commit: `ba7102f6b51df9016a174de7806089453716c767`.

**Interpretation ceiling:** this is a correction to the evidentiary meaning of
one requested CDX column, not a new finding about the historical video. It
does not favor deletion, substitution, ordinary archival behavior, or any
other cause.
