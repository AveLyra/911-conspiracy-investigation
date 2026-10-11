# Wayback CDX records for the two NIST-named FLV paths

**Record type:** bounded archival-index observation. This records the CDX rows
retrieved on 2026-10-05; it does not authenticate an original video or explain
why any URL returned the status recorded for it.

## Source and retrieval

The Internet Archive Wayback Machine CDX index was queried on 2026-10-05 for
each exact URL named by the archived NIST Flash wrappers:

- CU animation: `http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv`
- Whole-building animation: `http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv`

The queries requested `timestamp, original, statuscode, digest, length` and
returned JSON. The query URLs were:

- <https://web.archive.org/cdx/search/cdx?url=www.nist.gov%2Fpublic_affairs%2Freleases%2Fwtc_videos%2FCU%20animation.flv&output=json&fl=timestamp%2Coriginal%2Cstatuscode%2Cdigest%2Clength>
- <https://web.archive.org/cdx/search/cdx?url=www.nist.gov%2Fpublic_affairs%2Freleases%2Fwtc_videos%2Fwhole%20building%20animation.flv&output=json&fl=timestamp%2Coriginal%2Cstatuscode%2Cdigest%2Clength>

SHA-256 of the exact JSON responses retrieved in this check:

- CU query: `ec87e332b11bde132a23477f2e6affc786f2e6b689bd174659f767468ca4f57e`
- Whole-building query: `6704ebf50d03dda3f267dd86b558812c4920ae3e05d7eb65150a059f9c8a5ec8`

These hashes identify the two locally received CDX response bodies, not the
archived video files or immutable Wayback records. The index is live and can
change; the rows below preserve what this dated query returned.

## CDX rows observed

Values below are transcribed from the JSON response. Timestamps are UTC. The
`digest` and `length` columns are retained exactly as reported; differences
between them are not reconciled here.

| NIST-named path | Capture timestamp | Original URL recorded | Status | CDX digest | CDX length |
| --- | --- | --- | ---: | --- | ---: |
| CU animation | 2011-04-27 19:35:23 | `http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv` | 200 | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | 4107 |
| CU animation | 2011-05-12 00:32:03 | `http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv` | 200 | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | 4107 |
| CU animation | 2011-07-04 07:50:52 | `http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv` | 200 | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | 4107 |
| CU animation | 2016-03-04 11:11:36 | `http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv` | 404 | `5SJXT7LNUFKYY2APULQKG5MBHEUJTC5A` | 4125 |
| CU animation | 2025-05-14 10:10:52 | `http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv` | 301 | `QRDVOOVICNUU2ABQT4DWOC7F76EMMRG3` | 646 |
| CU animation | 2025-05-14 10:31:55 | `https://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv` | 404 | `7H32AS5KGCWT7IJ7JXKIGLZLJVEJFAYF` | 1099 |
| Whole-building animation | 2011-04-27 19:49:14 | `http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv` | 200 | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | 4112 |
| Whole-building animation | 2011-05-12 00:32:03 | `http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv` | 200 | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | 4113 |
| Whole-building animation | 2011-07-04 07:50:52 | `http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv` | 200 | `5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX` | 4113 |
| Whole-building animation | 2016-03-04 09:40:30 | `http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv` | 404 | `5SJXT7LNUFKYY2APULQKG5MBHEUJTC5A` | 4132 |
| Whole-building animation | 2025-05-14 10:19:30 | `https://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv` | 404 | `TW6NTJZ2QZ3R5OYMLO6PAMMANRSMZT2H` | 1112 |

## What this adds—and what it does not

**Observation:** for both named paths, the index lists three 2011 captures
with status `200`, a 2016 capture with status `404`, and one or more 2025
records. The CU path has a 2025 HTTP record with status `301` and a separately
listed HTTPS record with status `404`; the whole-building HTTPS record has
status `404`. The three listed 2011 captures for each path share one CDX
digest, while the reported lengths are not identical across both paths.

**Prior source record:** the existing derivative audit reports that the
April 2011 identity replays for both paths were HTML NIST error pages, not FLV
video. This run did not retrieve the May 2011, July 2011, March 2016, or May
2025 identity-replay bodies. Therefore the later 2011 `200` index statuses
are not treated here as proof that those replays contain playable video.

**Inference ceiling:** these entries extend the documented archive-access
history and identify exact replay timestamps for follow-up. They do not show
that an original video was ever or never available, that the archive captures
are complete, that any video was substituted or altered, why the later
statuses differ, or who made any relevant change. Stale/migrated paths,
server behavior, archival capture details, and other possibilities remain
untested. No cause or intent is inferred.

**Discriminating follow-up, not yet done:** retrieve the listed identity
replays and preserve response bodies, headers, and hashes; compare each body
with the corresponding CDX record; separately seek a provenance link from any
actual video bytes to the 2008 SWF wrappers or the Commons Ogg derivative.
Those tests could establish what particular archived replays contain, but
would not by themselves authenticate a NIST master or explain why a resource
became unavailable.

This is a source-access record, not a conclusion about the collapse mechanism
or evidence of deliberate concealment.
