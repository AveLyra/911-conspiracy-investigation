# Wayback access and CDX-field review — 2026-10-08

**Record type:** bounded source-access and documentation review. This note
records one public-document check and failed access attempts. It does not
authenticate a NIST animation, explain the specific Wayback records, or infer
alteration, substitution, concealment, or intent.

## Model attribution and review status

- **Requested attribution:** Luna.
- **Verification limit:** the runtime model identifier was not exposed to this
  review, so “Luna” is recorded as the user's requested attribution, not as an
  independently verified model identity.
- **Astra pass:** requested if material uncertainty remains. Material
  uncertainty remains because the identified WARC records and the May/July 2011
  replay bodies were not obtained in this pass. An Astra review has not been
  performed.

## Scope and source record

This review concerns the unresolved Wayback/CDX/replay discrepancies already
recorded in:

- `wayback-flv-capture-inventory-2026-10-05.md`
- `wayback-2016-flv-replay-check-2026-10-05.md`
- `wayback-cdx-capture-locators-2026-10-06.md`
- `wayback-cdx-public-fields-doc-2026-10-06.md`

Those notes report: (a) 2011 CDX rows for the two NIST-named FLV URLs with
status 200, while the retrieved April identity replay was an HTML error page;
(b) 2016 CDX status/length/digest fields that differ from the retrieved
12,761-byte identity-replay HTML pages; (c) different `x-archive-src` WARC
names in the two 2016 replay headers; and (d) `null` values for requested CDX
`filename` and `offset` fields. These are separate observations. Their
relationships remain unresolved.

The earlier access record lists these WARC-name values:

- `WPO-20160304104805-crawl892/WPO-20160304111005-00385.warc.gz`
- `WPO-20160304092823-crawl892/WPO-20160304093852-00350.warc.gz`

The May and July 2011 identity-replay bodies were not present in the reviewed
notes as retrieved artifacts.

## Public documentation checked in this pass

1. Internet Archive's `wayback-cdx-server` README, read from the rendered
   `master` page:
   <https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md>
   Accessed 2026-10-08. Its history page identifies
   `7f6ee86b35790c3cb10ea1115a0eeb9c7a432e09` as the latest listed README
   change (2018):
   <https://github.com/internetarchive/wayback/commit/7f6ee86b35790c3cb10ea1115a0eeb9c7a432e09>
   The direct commit-addressed README page could not be fetched by the web
   reader (`Cache miss`), so the text read was not independently confirmed
   against that immutable snapshot. The README calls itself a beta API
   document; its embedded changelog is dated 2013. No raw-file byte hash was
   obtained.
2. Internet Archive Help Center, “Using The Wayback Machine”:
   <https://archivesupport.zendesk.com/hc/en-us/articles/360004651732-Using-The-Wayback-Machine>
   Accessed 2026-10-08.

### Direct documentation observations

- The CDX README lists the publicly available fields as `urlkey`, `timestamp`,
  `original`, `mimetype`, `statuscode`, `digest`, and `length`; it does not list
  `filename` or `offset` in that public-field list.
- The README describes `offset=` as a query parameter for pagination, not as a
  CDX response field. It also says that some fields, including `filename`, may
  be restricted and that its software supports an API-key cookie for restricted
  data.
- The Help Center describes incomplete captures and says a replay of an
  incomplete archived site may use a closest-date capture for missing links.
  Its general guidance does not identify what happened to either NIST-named
  FLV URL.

### Interpretation ceiling

The documentation supplies ordinary, testable alternatives for interpreting
the earlier `null` fields: `offset` may have been requested as a column even
though the README describes it as a pagination parameter, and `filename` is
among the fields the README says can be restricted. This makes a general
access-control or query-semantics explanation plausible; it does **not** show
that either mechanism caused the particular 2026-10-06 response. The README is
software documentation, not the production configuration or a record of the
live service's settings for these captures. The `null` values remain preserved
as observed; this note does not resolve them.

Likewise, general Wayback documentation about incomplete captures does not
explain the specific differences among the 2011/2016 CDX rows, replay headers,
and replay bodies. No explanation is selected.

## Access attempts in this pass

- The web reader could not open the 2011-05-12 CU-animation identity-replay
  URL: <https://web.archive.org/web/20110512003203id_/http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv>.
- The web reader also could not fetch the direct CDX query for the CU-animation
  URL with requested `filename`/`offset` fields. No fresh CDX response was
  received.
- Prior run context records a terminal DNS failure for `web.archive.org` on
  the same May replay attempt. The web-reader failures in this pass likewise
  produced no response from Wayback.

**Result:** no replay body, HTTP response headers, WARC bytes, or fresh CDX
response was obtained. These are access/tool limitations, not observations
that the archive returned 404 or that the records do not exist.

## Best discriminating next steps

1. From a network where Wayback resolves, retrieve the May and July 2011
   identity replays for both exact FLV URLs. Preserve each request, timestamp,
   headers, body, content type, byte count, and SHA-256 separately; do not
   replace the existing April or 2016 records.
2. Determine whether the two named 2016 WARC files can be obtained by a
   documented public route. If obtained, preserve the WARC bytes and inspect
   each record's target URL, date, response headers, payload, and applicable
   digests independently. If not publicly obtainable, record the exact route
   and response as an access limitation—not proof of deletion or concealment.
3. If a later CDX query is possible, request only documented public fields
   first, then separately test `filename` and `offset`; retain each exact
   query and response. Do not treat the README as proof of the live server's
   configuration.
4. Keep the NIST-origin-file question separate from Wayback storage: archived
   replay bytes can describe an archive capture, but cannot alone authenticate
   a NIST master or identify who created or changed a file.

No conclusion about WTC 7's collapse mechanism, video substitution, deliberate
removal, or historical intent is drawn from this review.
