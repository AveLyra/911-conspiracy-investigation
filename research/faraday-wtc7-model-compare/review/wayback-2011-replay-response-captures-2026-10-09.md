# Four 2011 Wayback identity-replay response captures — 2026-10-09

**Record type:** dated response-body and replay-metadata observation. It records what four Wayback identity-replay requests returned on 2026-10-09. It does not authenticate the original NIST videos, establish what an underlying WARC record contains, or explain any discrepancy.

## Capture preservation and method

The eight supplied files (four HTML response entities and four JSON metadata sidecars) were copied without modification from:

`/var/folders/tr/qmsqldfn59591rbflj14mc4r0000gn/T/wayback-replay-capture-EhSnAe/`

Durable Faraday copies are in [`inputs/wayback-replay-captures/2026-10-09/`](../inputs/wayback-replay-captures/2026-10-09/). `cmp` verified each copy against its temporary source. SHA-256 values are listed below. The HTML bodies were obtained through browser `Network.getResponseBody`; as each JSON sidecar says, these are browser-decoded response entities, not compressed on-the-wire bytes. The capture set contains no WARC payload bytes.

## Direct observations

Each sidecar reports an outer replay response status of `200`, `mimeType` of `text/html`, and `content-type: text/html; charset=UTF-8`. Each identifies the requested capture through `memento-datetime` and `x-archive-orig-date`. The HTML bodies are 13,113 bytes each; `file` identifies each as ASCII HTML. Their title is “National Institute of Standards and Technology Error Page,” and the body includes “Page Not Available.”

| ID | Requested replay URL / capture time (UTC) | HTTP `Date` in sidecar | `x-archive-src` value in sidecar | Body size / SHA-256 | Sidecar SHA-256 |
| --- | --- | --- | --- | --- | --- |
| 01 CU May | [2011-05-12 00:32:03](https://web.archive.org/web/20110512003203id_/http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv) | 2026-10-09 13:21:23 GMT | `live-20110511220555245-00271-00372/live-20110512001336222-00296.arc.gz` | 13,113 / `27c355ac556ac27556a08b871be9a5336f321de931fcfb540562b2632c48a98a` | `d884aed4e492865bbfbeb162bcfdd9cf52febd3fd2325f2bebcc0f4d2f2f54e7` |
| 02 CU July | [2011-07-04 07:50:52](https://web.archive.org/web/20110704075052id_/http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv) | 2026-10-09 13:19:34 GMT | `live-20110704071136426-01161-01254/live-20110704073939689-01167.arc.gz` | 13,113 / `27c355ac556ac27556a08b871be9a5336f321de931fcfb540562b2632c48a98a` | `83dde13db2d9e5f7fb8f7c9b47171eaa3565883bfaa46e2e49ef5bb9e7cba6d7` |
| 03 Whole-building May | [2011-05-12 00:32:03](https://web.archive.org/web/20110512003203id_/http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv) | 2026-10-09 13:19:47 GMT | `live-20110511220555245-00271-00372/live-20110512001821253-00298.arc.gz` | 13,113 / `27c355ac556ac27556a08b871be9a5336f321de931fcfb540562b2632c48a98a` | `69d7bf746a2bc13b55146d148b5a7544de2e4afae8096890d5f4e491677e7356` |
| 04 Whole-building July | [2011-07-04 07:50:52](https://web.archive.org/web/20110704075052id_/http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv) | 2026-10-09 13:19:52 GMT | `live-20110704071136426-01161-01254/live-20110704072058886-01163.arc.gz` | 13,113 / `27c355ac556ac27556a08b871be9a5336f321de931fcfb540562b2632c48a98a` | `ba13ddf026840f8801369db04bf79ed6fb15711a3c0b894109398b285b660543` |

`cmp` found all four HTML files byte-identical. The `x-archive-src` strings differ across the four sidecars; they are preserved as header values, not treated as obtained or authenticated WARC files.

The sidecars themselves have differing field names/structures. For example, ID 01 uses `bodyBytesUtf8` / `bodySha256Utf8` / `base64Encoded`, while IDs 02–04 use `bodyBytes` / `bodySha256` / `cdpBase64Encoded` and include additional CDP completion fields. The original JSON files remain unchanged; no schema normalization was performed.

## Relationship to prior records — unresolved

- The earlier local derivative inventory reports the 2011-04-27 replay body as 13,113 bytes with the same SHA-256, and labels it NIST “Error Page” HTML. This is a match to the previously recorded hash; the April body itself was not part of this four-file capture set, so no direct byte comparison with that earlier body is claimed.
- The CDX inventory records May and July 2011 rows with status `200`; its reported lengths are 4,107 bytes for the CU path and 4,113 bytes for the whole-building path, with CDX digest `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX`. Those index values and the present replay-response entity sizes/hashes describe separately reported outputs. Their semantics and relationship remain unresolved.
- The status `200` in these JSON sidecars is the observed replay response status, not proof that the original NIST request returned a video or any particular HTTP status. The sidecars identify the body as HTML. They do not establish whether the error-page HTML was the archived payload, a replay-layer result, or another outcome.
- The `x-archive-src` header values may be useful locators for later public-source testing, but no corresponding WARC bytes were obtained or inspected in this capture step.

## Interpretation ceiling and next discriminating evidence

**Established for these four saved responses:** on the recorded 2026-10-09 requests, the four specified Wayback identity-replay URLs produced byte-identical, 13,113-byte NIST-branded HTML error-page entities rather than FLV bytes. The response metadata reports HTTP status `200` and `text/html`.

**Not established:** the original archived HTTP status; whether the WARC records contain video or error HTML; why the replay service returned this entity; whether video bytes were ever held, later removed, or substituted; or any deliberate act or intent.

The highest-value next step is to obtain the exact WARC records or underlying archived HTTP records through an authorized, documented route and compare each record's target URL, timestamp, original-response status/headers, payload, and digest to the CDX entries and these replay responses. Until then, retain the responses and CDX values side by side; do not interpret an access or replay result as proof of deletion or substitution.

## Source files

The durable HTML bodies and JSON sidecars are preserved under `inputs/wayback-replay-captures/2026-10-09/` using the IDs in the table. No raw compressed wire capture or WARC object is included.
