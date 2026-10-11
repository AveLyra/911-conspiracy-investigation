# Wayback CDX versus replay-response discrepancy — 2026-10-10

**Record type:** additive cross-reference of two existing observation sets. This note preserves their reported values side by side. It is not a new retrieval, does not replace either source record, and does not explain or resolve the discrepancy.

## Observation A — CDX index response

The saved 2026-10-10 CDX JSON response for the exact whole-building animation URL lists these May and July 2011 rows:

| Capture timestamp | CDX `statuscode` | CDX `mimetype` | CDX `digest` value | CDX `length` |
|---|---:|---|---|---:|
| `20110512003203` | `200` | `text/html` | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | `4113` |
| `20110704075052` | `200` | `text/html` | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | `4113` |

The same response also lists an April 27, 2011 row (`20110427194914`) with the same status, MIME label, and digest value, and a length of `4112`. In the Faraday source worktree, the response body is preserved at `review/wayback-cdx-corrected-fields-2026-10-10.response.json` (SHA-256 `5492d9e948eef130887a3365a0134f87172457acb979ccf030b1cda109dfb046`); its separately saved response-header file has SHA-256 `0ea51e04bc56aa448ec568b3efcb7d88149089bb707ad0bed8ab810f88e38fe4`.

These are values reported in the CDX response. The raw ARC record and its encapsulated original response were not inspected. The CDX digest string is retained as reported; it is not treated here as a SHA-256 value or compared directly with the replay-body SHA-256.

## Observation B — identity-replay response bodies

The previously saved browser captures for the corresponding May and July identity-replay URLs each contain a 13,113-byte HTML entity. All four replay bodies in that capture set—including the two CU-animation requests—were byte-identical, with SHA-256 `27c355ac556ac27556a08b871be9a5336f321de931fcfb540562b2632c48a98a`. Their sidecars report the replay request's outer HTTP status as `200` and MIME/content type as HTML. The bodies identify a NIST error page and include “Page Not Available.” They are browser-decoded response entities; compressed on-the-wire bytes and ARC payload bytes were not captured.

The two whole-building identity-replay URLs were:

- May: <https://web.archive.org/web/20110512003203id_/http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv>
- July: <https://web.archive.org/web/20110704075052id_/http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv>

The corresponding body files in the Faraday source worktree are `inputs/wayback-replay-captures/2026-10-09/03-whole-may-response.html` and `04-whole-july-response.html`; their sidecars are the matching `.json` files in that directory. Each body has the SHA-256 above. The sidecars preserve distinct `x-archive-src` values; those ARC objects were not obtained or authenticated.

## Preserved discrepancy; no reconciliation

For the May and July timestamps, the CDX response reports a length of `4113` bytes, while each corresponding saved replay body is `13113` bytes—a numerical difference of 9,000 bytes. Both records describe HTML and display a status value of `200`, but the CDX `statuscode` field and the browser-observed outer replay status are observations from different response layers. The repeated CDX digest label and the replay-body SHA-256 are also different kinds of recorded values and have not been compared as though they identify the same bytes.

The difference is preserved as an **unresolved discrepancy between the index output and the replay-response capture**. The current record does not establish that CDX `length` and browser body size count the same object, representation, or processing stage. It also does not establish whether the replay body matches the archived payload, whether the indexed payload was an error page, or why the reported byte counts differ. No cause is selected or proposed as established.

This discrepancy alone is not evidence that a video was deleted, substituted, or deliberately altered. The shared HTML labels do not authenticate the historical payload either.

## Evidence that could test the relationship

The most direct comparison would require the exact index bytes and the corresponding ARC record, including the record locator, encapsulated original-response headers, and payload, with hashes and retrieval details. The item metadata lists the companion index and ARC, but the ordinary public index-download attempt recorded on 2026-10-10 redirected and received HTTP `401`; no index or ARC bytes were obtained. No access-control bypass was attempted. A future retrieval, if available through the ordinary documented route, should be recorded as a new observation and compared without replacing this discrepancy record.

## Source and provenance links

- CDX endpoint: <https://web.archive.org/cdx/search/cdx>
- Faraday CDX response capture and prior query details: `review/wayback-cdx-corrected-fields-2026-10-10.response.json`, `review/wayback-cdx-corrected-fields-2026-10-10.response-headers.txt`, and `review/wayback-cdx-offset-field-qualification-2026-10-10.md`.
- Faraday replay-response captures and sidecars: `inputs/wayback-replay-captures/2026-10-09/` and `review/wayback-2011-replay-response-captures-2026-10-09.md`.
- Listed May ARC: <https://archive.org/download/live-20110511220555245-00271-00372/live-20110512001821253-00298.arc.gz>
- Listed May companion index: <https://archive.org/download/live-20110511220555245-00271-00372/live-20110512001821253-00298.arc.os.cdx.gz>
- Public item metadata: <https://archive.org/metadata/live-20110511220555245-00271-00372>
- Captured CDX response access date: 2026-10-10 UTC. Captured replay response access date: 2026-10-09 UTC.

## Redundant-copy locations

- Faraday source record: `review/wayback-cdx-replay-layer-discrepancy-2026-10-10.md`
- Public research copy: `investigation/wtc7/wayback-replay-capture-2026-10-09/cdx-replay-layer-discrepancy-2026-10-10.md`
- Private research copy: `research/wtc7/wayback-replay-capture-2026-10-09/cdx-replay-layer-discrepancy-2026-10-10.md`
