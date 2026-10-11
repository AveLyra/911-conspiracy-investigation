# Wayback CDX locator fields and capture-length observations (2026-10-06)

**Record type:** source-pinned archive-index observation with an unresolved
cross-interface discrepancy. This note preserves the values returned by one
CDX query and by earlier replay observations; it does not reconcile them.

## Question and retrieval

The bounded check asked whether the public Wayback CDX response for the
NIST-named CU-animation FLV URL exposes `filename` and `offset` fields for its
indexed captures. The query requested:

`timestamp,original,statuscode,digest,length,filename,offset`

Source URL:
<https://web.archive.org/cdx/search/cdx?url=www.nist.gov%2Fpublic_affairs%2Freleases%2Fwtc_videos%2FCU%20animation.flv&output=json&fl=timestamp%2Coriginal%2Cstatuscode%2Cdigest%2Clength%2Cfilename%2Coffset>

Access date: 2026-10-06. Retrieved response: 1,002 bytes; SHA-256
`f603430497d07b1b473afa40935785a308d42a27e1c0485c8092b4055105b6cd`.

## Direct CDX response observations

| Timestamp | Indexed original URL | Status | CDX digest | CDX length | `filename` | `offset` |
| --- | --- | ---: | --- | ---: | --- | --- |
| 20110427193523 | `http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv` | 200 | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | 4107 | `null` | `null` |
| 20110512003203 | `http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv` | 200 | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | 4107 | `null` | `null` |
| 20110704075052 | `http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv` | 200 | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | 4107 | `null` | `null` |
| 20160304111136 | `http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv` | 404 | `5SJXT7LNUFKYY2APULQKG5MBHEUJTC5A` | 4125 | `null` | `null` |
| 20250514101052 | `http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv` | 301 | `QRDVOOVICNUU2ABQT4DWOC7F76EMMRG3` | 646 | `null` | `null` |
| 20250514103155 | `https://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv` | 404 | `7H32AS5KGCWT7IJ7JXKIGLZLJVEJFAYF` | 1099 | `null` | `null` |

In this returned JSON, all six rows have `filename: null` and `offset: null`.
This is the result of the specified CDX query; it is not evidence that the
underlying WARC records do not exist or cannot be obtained by another route.

## Preserve the related observations without reconciling them

1. The existing replay-check note
   (`wayback-2016-flv-replay-check-2026-10-05.md`) records that the 2016
   identity replay returned 12,761 bytes of NIST “Page Not Found” HTML, while
   its CDX row listed status `404` and length `4125`. Its replay headers also
   reported an `x-archive-src` WARC filename. In this new CDX response, the
   corresponding `filename` and `offset` fields are `null`. These are
   separately observed interface fields; the WARC payload and its relationship
   to either representation were not inspected here.
2. The local derivative inventory (`media/derivatives/README.md`, “Internet
   Archive capture of the CU-animation URL”) records a 2011-04-27 replay body
   of 13,113 bytes, identified there as NIST “Error Page” HTML, with SHA-256
   `27c355ac556ac27556a08b871be9a5336f321de931fcfb540562b2632c48a98a`. The
   CDX response above lists the matching timestamp `20110427193523` with
   status `200`, digest `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX`, and length `4107`.
   The replay-body size/hash and the CDX row’s status/digest/length are
   recorded as different reported values. Their semantics and relationship
   have not been adjudicated.

## Interpretation ceiling and next discriminating check

The query establishes what this CDX response returned for these fields on the
access date. It does not establish why locator fields are null, whether the
named WARC files are directly accessible, what bytes they contain, whether an
FLV was captured, whether a replay was substituted, or whether anyone acted
deliberately. No conclusion about WTC 7 collapse cause or historical intent is
drawn.

**Next check, not performed:** retrieve and inspect the exact WARC records
named in the prior replay headers, if obtainable, and preserve each WARC
record, CDX row, and identity-replay response as separate artifacts with
separate hashes. Compare the actual record payloads to the replay bodies only
after recording their formats and lengths; do not infer equivalence from a
matching timestamp or status alone.
