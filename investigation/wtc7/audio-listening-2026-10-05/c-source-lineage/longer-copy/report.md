# Longer WTC 7 recording source follow up

October 7, 2026. Research only under the full investigation charter.

The catalog search located a Gilsanz February presentation folder with four
differently named video files, but did not establish that any is the longer
`WTC7COLLAPSE.MPG` described by the secondary index. Two selected files received
download references; both subsequent transfers returned HTTP 403, and neither
produced a local media file. This is a more precise source lead, not new footage,
a source match, an acoustic finding or evidence of deletion or concealment.
The full investigation remains active and incomplete; no cause ranking or
legal-record status changes.

## Source question and declared scope

The preserved secondary index describes a 6:22, 720×480 recording as Release 28
`42A0309 - G28D14/WTC7COLLAPSE.MPG`, with Gilsanz/CD138/CD137 aliases. These are
locator claims, not independently verified properties of acquired bytes. The
[earlier source report](../report.md) preserves that lead and the previously
completed CD138 listing. This stage did not repeat that listing or the denied
YouTube mirror route.

[NIST's repository page](https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations)
links its public Google collection. The saved route runs through Other Photos
and Videos → PhotosAndVideoFromCDorDVD → Video. The earlier
[provenance audit](../../../late-fire-original-tape-catalog/independent-provenance.md)
and [Video listing](../../../late-fire-original-tape-catalog/sources/cdvideo-list.response.json)
ground the two initial folder IDs; a NIST catalog connection does not identify
the cameraman, establish continuous recording or authenticate original sound.

The [protocol](PROTOCOL.md) allowed those two initial listings and up to eight
additional listings, within two descendant levels. The actual eight calls
used two initial folders and six descendants. The later
[metadata addendum](METADATA-ADDENDUM.md) specified four item checks. A separate
[acquisition addendum](ACQUISITION-ADDENDUM.md), declared after method review
and before fetching, explicitly broadened the original exact-name/known-alias
criterion to two unverified alternatives. It retained the two-file and
300-MB-per-file caps, preservation requirements and stop-on-denial rule.
This was a prospective change, not a retrospective claim of an exact match.

## Catalog coverage and its limits

Each request used the exact returned public folder URL with `top_k: 1000`.
Every request and normalized response is retained in `sources/`.

| Requested folder | Depth from initial folder | Returned files | Returned folders |
|---|---:|---:|---:|
| [RamonGilsanzfromCD](sources/ramon-list.response.json) | 0 | 3 | 0 |
| [GilsanzMurraySteficek](sources/gms-list.response.json) | 0 | 0 | 4 |
| [WTCI-101-I-GMS-CD#7](sources/gms-child-0.response.json) | 1 | 2 | 0 |
| [WTCI-102-I-GMS-Keasbey](sources/gms-child-1.response.json) | 1 | 6 | 0 |
| [WTCI-134-I-WTC7AnalysisVideos](sources/gms-child-2.response.json) | 1 | 3 | 0 |
| [WTCI-97-I-Multiple](sources/gms-child-3.response.json) | 1 | 0 | 4 |
| [Gilsanz Pres-Feb 9-10-WTC7](sources/presentation-0.response.json) | 2 | 4 | 0 |
| [Gilsanz Pres-Jan11-12 -WTC7](sources/presentation-1.response.json) | 2 | 0 | 1 |
| Total | | 18 | 9 |

The 27 returned IDs are distinct; that does not mean 18 independent recordings.
No returned title equals `WTC7COLLAPSE.MPG`, including case-insensitive matching.
Three returned branches were not listed: two Baker presentation folders and
the January presentation's Video-NBC child. The normalized responses contain
no pagination/completeness proof and have null parent fields. Exact joins
between requested folders and previously returned child IDs verify the saved
traversal, not a stronger native-parent-field or exhaustive-archive claim.

The four February presentation entries are `wtc 7-b1.mpg`, `wtc 7-b.mpg`,
`WTC7fall.m1v` and `WTC7-145040.m1v`. A second `WTC7-145040.m1v` elsewhere in
the traversal has the same reported size but a different ID; byte identity
remains untested. Folder naming motivates this lead but establishes no alias.

All four metadata requests asked for duration/dimensions, checksums, parents
and download capability as well as identity and size. The normalized responses
returned identity, MIME and size but omitted the requested video metadata and
checksums. That prevents the proposed 6:22/720×480 metadata comparison; it is
not a mismatch, proof the provider lacks those fields, or proof of withholding.

A separate reviewer made six targeted public searches. The
[exact search log](sources/public-search-log.json) records the queries and
opened pages. The IC911 page repeats the secondary index's claim rather than
independently corroborating it; its linked processed YouTube derivative could
not be opened through that web route. No exact MPG download was independently
grounded by this bounded search. Batched results do not support invented
per-query negative findings or archive-wide absence.

## Attempted transfers and preservation

The two `.mpg` alternatives were selected first because of the target's named
container family, not because their content had matched. This does not exclude
the `.m1v` files or renamed/reencoded footage. The native Drive fetch requests
used the returned file URLs, `download_raw_file: true` and
`include_base64: false`. They supplied temporary remote references, not local
files. Candidate identities and reported sizes remained consistent:

| Candidate | Reported bytes | Local transfer | Local media |
|---|---:|---|---|
| `wtc 7-b1.mpg` | 86,021,896 | HTTP 403 | None |
| `wtc 7-b.mpg` | 30,330,880 | HTTP 403 | None |

The bounded local procedure received temporary locators through standard
input with terminal echo disabled. It restricted the transport host and HTTPS,
disabled redirects, pinned the two IDs/sizes, enforced byte/time limits and
exclusive output creation, and did not repair or remux. Syntax/import,
allowlist-positive, five rejection and candidate-cap checks passed before
execution. The transfer command exited 1; the
[receipt](acquisition-receipt.json) preserves both HTTP errors. The current
`media/` directory is empty. No denial was retried or bypassed. The cause of
the transfer-layer rejection is undiagnosed; it is not a demonstrated denial
at the NIST source.

Temporary signed links were inadvertently printed in a diagnostic tool output.
That workflow/privacy error was disclosed to the user. Saved fetch responses
replace those links with explicit omission markers while retaining stable
file identities and metadata. Saved-file redaction does not erase the earlier
output and is not blanket disclosure clearance. No temporary link is included
in this report or the proposed generic software feedback.

## Verification and remaining scientific work

The [separate review](independent-review.json) reproduces saved parent/child
joins, listing counts, metadata/fetch identity and size consistency, the
procedure pin and empty local media directory. Its final 89 assertions pass.
Two failed privacy-check attempts remain documented: the initial rule wrongly
flagged a public YouTube query parameter; the corrected public-URL classification
passed without relaxing the temporary-secret checks. A subsequent wording
correction distinguishes the allowed listing cap from the eight actual calls.
This is same-source, nonblind AI review, not independent historical evidence,
expert validation, human acceptance or reproduction of the network event.
The [final verification receipt](final-verification.json) pins this report and
records the main agent's local checks separately.

There are no acquired candidate streams to probe or pictures to compare. An
authorized source-native file, with its source route preserved, would permit
stream inspection and a prospectively specified sequence comparison around
the known discontinuity. Duration, familiar skyline and filenames alone would
not establish a match; an absent audio stream would not establish silence at
the scene. Neither the thermal-support-loss hypothesis nor the fire hypothesis
gains evidentiary weight from these catalog results or transfer failures.

This source route is stopped, not the full investigation. Held-media picture
correspondence and the already authorized curve-preparation work remain
available within their existing review and uncertainty requirements. Do not
retry denied transfers, tune the completed waveform test after its result, or
re-request completed human coordinate/legend checks as substitutes for those
distinct tasks.
