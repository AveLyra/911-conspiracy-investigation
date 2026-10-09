# Four 2011 Wayback identity-replay responses — 2026-10-09

**Record type:** original summary of a dated replay-response capture. This report records what four specified Wayback identity-replay requests returned on October 9, 2026. It does not authenticate the original NIST videos, establish what an underlying WARC record contains, or explain any discrepancy.

## Observations from the saved capture set

The four browser-captured response entities were each 13,113 bytes and had the same SHA-256:

`27c355ac556ac27556a08b871be9a5336f321de931fcfb540562b2632c48a98a`

The saved sidecars report outer replay HTTP status `200`, MIME type `text/html`, and `content-type: text/html; charset=UTF-8`. The bodies identify themselves as a National Institute of Standards and Technology error page and include “Page Not Available.” The bodies were obtained as browser-decoded entities; compressed on-the-wire bytes and WARC payload bytes were not captured.

| Capture | Requested identity-replay URL | `x-archive-src` response-header value | Sidecar SHA-256 |
| --- | --- | --- | --- |
| CU, May 12, 2011 00:32:03 UTC | <https://web.archive.org/web/20110512003203id_/http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv> | `live-20110511220555245-00271-00372/live-20110512001336222-00296.arc.gz` | `d884aed4e492865bbfbeb162bcfdd9cf52febd3fd2325f2bebcc0f4d2f2f54e7` |
| CU, July 4, 2011 07:50:52 UTC | <https://web.archive.org/web/20110704075052id_/http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv> | `live-20110704071136426-01161-01254/live-20110704073939689-01167.arc.gz` | `83dde13db2d9e5f7fb8f7c9b47171eaa3565883bfaa46e2e49ef5bb9e7cba6d7` |
| Whole-building, May 12, 2011 00:32:03 UTC | <https://web.archive.org/web/20110512003203id_/http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv> | `live-20110511220555245-00271-00372/live-20110512001821253-00298.arc.gz` | `69d7bf746a2bc13b55146d148b5a7544de2e4afae8096890d5f4e491677e7356` |
| Whole-building, July 4, 2011 07:50:52 UTC | <https://web.archive.org/web/20110704075052id_/http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv> | `live-20110704071136426-01161-01254/live-20110704072058886-01163.arc.gz` | `ba13ddf026840f8801369db04bf79ed6fb15711a3c0b894109398b285b660543` |

The four body files were directly compared and found byte-identical. The four `x-archive-src` strings above were read from response sidecars; no corresponding WARC objects were obtained or authenticated. Sidecar field names and structures are not identical and were preserved without normalization in the local capture set.

## Other recorded values — unresolved

An earlier local inventory reports an April 27, 2011 replay body with the same size and SHA-256. That earlier body was not included in this four-response comparison, so this is a reported hash match, not a new direct byte comparison.

A separate CDX inventory records May and July 2011 rows with status `200`, lengths of 4,107 bytes for the CU path and 4,113 bytes for the whole-building path, and digest `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX`. These index values and the present replay-response entity sizes and hashes are preserved as separate observations. Their meanings and relationship remain unresolved. The `200` recorded in the replay sidecars describes the replay response; it does not establish the original archived response's status.

## Interpretation limits and next evidence

For these four saved responses, the supported result is that the specified replay requests returned byte-identical HTML error-page entities rather than FLV bytes. This does **not** establish whether the underlying WARC records contain videos or error pages, the original HTTP status, why the replay service returned this content, whether video bytes were once archived and later removed, or whether anything was substituted deliberately.

The most discriminating next evidence would be the exact underlying WARC or archived HTTP records, including each record's target URL, timestamp, original-response status and headers, payload, and digest, compared with the corresponding CDX entries and replay responses. Until those records are obtained and checked, the distinct observations should remain side by side and unresolved.

## Local provenance

The exact four HTML response entities and four unmodified JSON sidecars are retained in the Faraday research worktree at `inputs/wayback-replay-captures/2026-10-09/`. The accompanying detailed local note is `review/wayback-2011-replay-response-captures-2026-10-09.md`, committed as Faraday commit `9504f972a691cacd866e5ffc54fce87ec9e42f8e`. The raw HTML entities are not duplicated in this public repository; the captured pages contain a NIST copyright notice. The public report is an original summary, not a substitute for the local bytes or a claim of historical authenticity.
