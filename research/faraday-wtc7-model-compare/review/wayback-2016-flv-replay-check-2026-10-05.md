# 2016 Wayback identity-replay check for the two NIST-named FLV paths

**Record type:** source-access observation with a bounded provenance inference.
This records the replay responses retrieved on 2026-10-05. It does not
authenticate either video as a NIST master, determine what video was served in
2008, or explain why the resources were unavailable in later captures.

## Sources and retrieval

The Internet Archive Wayback CDX index lists 2016-03-04 captures for the
two exact URLs named by the archived NIST Flash wrappers. Their identity
replays were retrieved on 2026-10-05:

- CU animation, capture `20160304111136`:
  <https://web.archive.org/web/20160304111136id_/http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv>
- Whole-building animation, capture `20160304094030`:
  <https://web.archive.org/web/20160304094030id_/http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv>

The corresponding [CU CDX query](https://web.archive.org/cdx/search/cdx?url=www.nist.gov%2Fpublic_affairs%2Freleases%2Fwtc_videos%2FCU%20animation.flv&output=json&fl=timestamp%2Coriginal%2Cstatuscode%2Cdigest%2Clength)
listed status `404`, digest `5SJXT7LNUFKYY2APULQKG5MBHEUJTC5A`, and length
`4125`. The [whole-building CDX query](https://web.archive.org/cdx/search/cdx?url=www.nist.gov%2Fpublic_affairs%2Freleases%2Fwtc_videos%2Fwhole%20building%20animation.flv&output=json&fl=timestamp%2Coriginal%2Cstatuscode%2Cdigest%2Clength)
listed status `404`, the same CDX digest, and length `4132`. The two lengths
and the shared digest are recorded as reported; no explanation for their
relationship is adopted.

## Direct replay observations

| Item | CU animation replay | Whole-building replay |
| --- | --- | --- |
| HTTP response observed | `HTTP/2 404` | `HTTP/2 404` |
| Response date header | `Mon, 05 Oct 2026 21:54:55 GMT` | `Mon, 05 Oct 2026 21:54:54 GMT` |
| `x-archive-orig-date` | `Fri, 04 Mar 2016 11:11:36 GMT` | `Fri, 04 Mar 2016 09:40:30 GMT` |
| `memento-datetime` | `Fri, 04 Mar 2016 11:11:36 GMT` | `Fri, 04 Mar 2016 09:40:30 GMT` |
| `x-archive-src` | `WPO-20160304104805-crawl892/WPO-20160304111005-00385.warc.gz` | `WPO-20160304092823-crawl892/WPO-20160304093852-00350.warc.gz` |
| Content type / downloaded bytes | `text/html;charset=UTF-8` / 12,761 | `text/html;charset=UTF-8` / 12,761 |
| `file` identification | HTML document text, ASCII | HTML document text, ASCII |
| Page title in body | `National Institute of Standards and Technology Page Not Found` | `National Institute of Standards and Technology Page Not Found` |
| Response-body SHA-256 | `e3a5cbf074a6a3d50407287d791b418fd7f7213507baa5d0ff47dfd20e959fa1` | `e3a5cbf074a6a3d50407287d791b418fd7f7213507baa5d0ff47dfd20e959fa1` |
| Retrieved-header SHA-256 | `5af18bd9b1f13f52cd11dc6f0469e3cf91b367f70cf06ab3c5bf5b1fa7e91e8f` | `5212b0f32213b12f71a7c623b843485cacb6b5203cfa313dcaa0a5904d3cf61f` |

The two fetched response bodies were byte-identical by SHA-256 and byte count.
The replay headers report different `x-archive-src` WARC names. Those are
separate observations; the WARC payloads themselves were not retrieved or
validated in this check.

## Claim ledger and limits

| Claim | Type | Primary support | Assumptions / best alternative | Reproduced? / weakening test | Grade |
| --- | --- | --- | --- | --- | --- |
| These two identity-replay requests returned the listed 404 HTML bodies and headers on 2026-10-05. | Direct retrieval observation | Wayback identity-replay responses; local HTTP headers, `file`, byte counts, and SHA-256 | Applies to these replay requests at this retrieval time, not necessarily to every Wayback interface or the original 2016 source response. | Hash and byte-count checks performed locally; a fresh retrieval producing different bytes would change this observation for a later request. | A, for the received bytes only |
| The 2016 archived origin responses were NIST “Page Not Found” pages. | Inference from archive metadata and replay | CDX status/date plus replay `x-archive-orig-date`, `memento-datetime`, `x-archive-src`, and page body | The replay service could return or transform an error response; the underlying WARC record has not been independently inspected. | Not independently reproduced against the WARC. Inspecting the named WARC record and its HTTP payload could weaken or strengthen this inference. | C, materially dependent on the replay chain |

## Relationship to prior records; unresolved items

The earlier derivative audit (`../media/derivatives/README.md`, “Internet
Archive capture of the CU-animation URL”) reports that the April 2011 identity
replays returned a different NIST HTML “Error Page” body: 13,113 bytes with SHA-256
`27c355ac556ac27556a08b871be9a5336f321de931fcfb540562b2632c48a98a`. The
2016 identity replays retrieved here instead have the page title “Page Not
Found,” 12,761 bytes, and SHA-256 shown above. Those reported page labels,
byte counts, and hashes differ. The difference is preserved; this check does
not explain or reconcile it.

The CDX `length` values (`4125` and `4132`) also differ from each other and
from the 12,761-byte identity-replay bodies. The CDX digest is the same for
both rows, while the retrieved bodies are byte-identical. These fields and
outputs are recorded together without deciding what accounts for the length
and digest relationship.

**Inference ceiling:** the retrieved Wayback responses are NIST-branded
HTML not-found pages associated by response metadata with the two 2016 capture
timestamps. They are not the requested FLV video bytes. This does not show
that the videos never existed, were substituted, or were deliberately
removed; it does not identify why the archived response is a not-found page.

**Discriminating follow-up, not done:** obtain and inspect the WARC records
named in the response headers; separately retrieve the May and July 2011
identity replays and the May 2025 entries. Preserve each response and its
headers as a separate record. A replay result or status alone cannot
authenticate the 2008 video content or a NIST master.

No conclusion about collapse cause, historical intent, or deliberate
concealment is drawn from this access check.
