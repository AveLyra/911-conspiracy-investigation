# Independent nonvisual catalog/source review

2026-09-19. Research working record; not evidence promotion, a visual finding,
a legal conclusion, or an assessment of the collapse mechanism.

## Scope and result

The two acquired AVI files match the reported local sizes and SHA-256 hashes.
All four exact target names, IDs, sizes, MIME types and file URLs agree between
the saved listing responses and the corresponding individual metadata responses.
The official NIST landing page and normalized Organized-root capture support
the current catalog route to VideoClips; the folder-search response places the
two named CBS dub folders beneath that VideoClips ID.

The original dub-listing responses do not themselves preserve their request
folder IDs, and all their returned file `parent_ids` are null. Their exact
containing-folder attribution therefore needs the request record as well as
the returned data. The acquiring agent subsequently preserved
`listing-request-receipt.md`, explicitly reconstructed from its tool history
after acquisition. Its two request URLs match the returned Dub #5/#6 folder
IDs, and its response counts match the saved 24/49-entry captures. This
supplies a documented retrospective attribution, not provider-native parent
metadata, an independently retrieved request log or historical custody proof.

These findings establish a useful current catalog/file-identity chain, not
historical camera originality, an unedited sequence, a camera clock, or a
correspondence with a particular NCSTAR figure. No images were viewed, no
audio was heard, and no media were downloaded, decoded or probed by this
reviewer. The two acquired byte streams were read only to count and hash them.

## Evidence layers and exact mappings

The preserved NIST HTML identifies its canonical URL as
`https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations`.
At lines 688–697, the anchor
`https://googledrive.nist.gov/folders/17lDS4YslnUaOHv-x2CEhWLVzmceNllk1`
has the caption **Organized Photos and Video Clips**. The separately labeled
**Original Video from Tapes** category points to a different folder at lines
700–710. It would be wrong to transfer that latter label to the acquired
Organized-category AVI files.

The normalized `nist-organized-root.connector.json` names root ID
`17lDS4YslnUaOHv-x2CEhWLVzmceNllk1` and includes a JSON-encoded folder-content
listing with three entries: ReadMe.txt, VideoClips and Photos. VideoClips is
exactly `1mKqRTrMFX4VDnxW_-VU3pByhfqqs1uwn`. Its child `parent_ids` is null;
the association is established by its inclusion in that root's returned
content, not by a populated child parent field. The duplicated content inside
the response agrees byte-for-byte as JSON string values; it is one response,
not two independent corroborations.

The ten-result scoped folder-search capture includes these exact entries:

| Folder title | Folder ID | Captured parent ID |
| --- | --- | --- |
| CBS-Net NIST Dub #5 | `1eCHR_lbdScxLb2F-LUJo_FOdXpo5kzFK` | `1mKqRTrMFX4VDnxW_-VU3pByhfqqs1uwn` |
| CBS-Net NIST Dub #6 | `1h4A6pKPMjdJKyF4fQfkjmCOylQzeWAIB` | `1mKqRTrMFX4VDnxW_-VU3pByhfqqs1uwn` |

The saved dub-listing responses contain 24 and 49 distinct IDs and distinct
titles respectively. All 73 returned `parent_ids` values are null. Their
structured content contains only `files`; no pagination/cursor field was
captured. This is the coverage of the saved responses, not proof that no other
files, versions, pages or repositories exist.

The retrospective request receipt gives `top_k: 200` for each exact dub-folder
URL. It also records a `CBS` folder query with the VideoClips ID in a parent
filter and `topn: 100`. Those IDs, returned folder titles and stated counts
agree with the inspected captures. This reviewer read the receipt but did
not independently access the acquiring agent's tool history; its retrospective
origin must remain visible rather than being promoted to a contemporaneous
provider log. No null source fields have been filled in.

Preserving the secondary lead's order, the exact targets are:

| Target title | File ID | Catalog bytes | Locally acquired in this audit's supplied set |
| --- | --- | ---: | --- |
| CBS-Net Dub5 14.avi | `1cero39dWDYw60oQ4LUaw_Uk939KdBAKP` | 73,206,324 | No |
| CBS-Net Dub5 15.avi | `1j6wE4s-bmFHqMMnmJZ1yqajsUKPeNfAN` | 60,183,924 | Yes |
| CBS-Net Dub6 45.avi | `1jKJ0OdPswfyuuDxUVRxDazgK020ngJka` | 234,785,572 | No |
| CBS-Net Dub6 44.avi | `1hNNuWhtzaJVMJPY1GjVcE3iSe-OH6qyR` | 104,308,572 | Yes |

Each target appears exactly once in its saved listing, and an independent
`jq -e` comparison of `{id,title,size,mime_type,url}` against the four separate
metadata captures returned `true` (exit 0). Each MIME type is `video/avi`.
The public file URL in each record is
`https://drive.google.com/file/d/<the exact ID>/view?usp=drivesdk`.

The individual metadata captures have null `parent_ids` and omit the requested
MD5, version and video-duration fields. This describes the normalized captures,
not the capabilities or holdings of Google Drive. Likewise,
`source_visibility_status: access_not_verified` is a connector status, not
evidence that these records are private or inaccessible. Their 2019 creation
and modification timestamps cannot date the depicted 2001 events.

The saved official landing notice and ReadMe say the repository is in an
NIST-owned Google account and includes collected historical materials. This
supports the official-publication route. Repetition of the notice is not a
second independent historical chain of custody. Neither a NIST filename nor
the present official link establishes who originally filmed a scene, when it
was filmed, whether a dub was edited, or that a catalog label is correct.

## Acquired local bytes

Both independent `wc -c` and `shasum -a 256` checks exited 0:

| Local file | Actual bytes | Actual SHA-256 |
| --- | ---: | --- |
| `sources/cbs-net-dub5-15.avi` | 60,183,924 | `8a4e3e02105d65140c2a3dc0bc95af0d907866de85353d5c9f498636aea79781` |
| `sources/cbs-net-dub6-44.avi` | 104,308,572 | `c3a19c895f5bcacdb473745641dbbd500982219a6de57726920125477a12f90c` |

Their total is 164,492,496 bytes. These counts match the individual catalog
records and the acquiring agent's supplied pins. The local hashes identify
the exact bytes now held and permit repeat checking; they are not a comparison
against a provider-supplied checksum, which is absent from the captured
normalized metadata. This reviewer did not independently repeat acquisition
or inspect transport headers. Media validity, scene content and continuity
are outside this review.

## Internet Archive and the time distinction

The separately preserved public IA metadata identifies
`cbs200109111856-1938`, titled **CBS Sept. 11, 2001 6:56 pm - 7:38 pm**, with
creator/publisher CBS 9, Washington, D.C. It describes a Television Archive
broadcast recording and labels its air time `2001-09-11 18:56:30 EDT`, paired
with `2001-09-11 22:56:30 UTC` and timezone `-4`. The description gives length
0:41:41. These are catalog assertions about the broadcast recording, not an
authenticated camera clock.

The secondary page's exact link adds `start=2322`. This is 38 minutes 42
seconds. Only if playback zero aligns with the catalog air time, with no
intervening timing discontinuity, does addition yield **19:35:12 EDT**.
The calculation was checked independently using Python datetime arithmetic.
It is consistent with the secondary author's approximate 7:35 PM broadcast
claim, but cannot establish when a shown scene was photographed, whether it
was live, or whether the linked scene actually occurs at that offset. No IA
video was inspected in this lane.

The IA catalog explicitly lists:

| Catalog file | `source` | `original` link | Catalog bytes | Catalog length, seconds |
| --- | --- | --- | ---: | ---: |
| V08553-31.mpg | original | null | 1,073,741,824 | 2501.94 |
| V08553-31.ogv | derivative | V08553-31.mpg | 179,675,595 | 2501.9 |
| V08553-31_512kb.mp4 | derivative | V08553-31.mpg | 181,701,857 | 2501.9 |

Those derivative references support a repository-level relationship, not
independent recordings of the event. The MPG's `original` designation does
not by itself mean original camera media, an unedited broadcast, or a
first-generation recording. These IA media bytes and their listed digests
were not independently acquired or verified. No metadata field inspected
joins an IA file to either acquired NIST AVI. The metadata describes stream/
loan-only access and an access-restricted item; catalog availability is not
an inference that unrestricted file access exists.

## Strongest objection, alternatives and next discriminator

The strongest positive result is that specific filenames in a secondary lead
can now be traced to concrete IDs and byte counts in a current official-linked
catalog, with two locally pinned files. This is materially more specific than
an unattributed online compilation.

The strongest remaining objection is a layer mismatch: present official
custody and reproducible byte identity cannot prove historical camera custody,
an unedited wide/zoom sequence, event time, or a report-figure match. A copied,
renamed, edited or rebroadcast segment could satisfy all metadata checks in
this note. Duplication across dubs or repositories could also produce apparent
corroboration without a second independent camera/source.

The catalog-level request-context gap is now documented by a retrospective
receipt, with the limits above; a provider-native parent-bearing record or
contemporaneous request/response capture would strengthen that attribution.
The next substantive discriminator is a separately declared
source-content comparison that identifies each candidate frame and report
still, checks distinctive scene anchors individually, and tests the asserted
transition for an edit. A historical timing claim additionally needs a
separately supported camera/event-time chain. This note does not authorize
or perform those tasks and draws no conclusion about fire severity, fire
area, temperature, pulse duration or collapse cause.

## Actual review and verification coverage

Controls: main AGENTS.md, WORKFLOW.md, START-HERE.md and investigation CHARTER
were read earlier in this continuing review lane and their current hashes
rechecked; the new unit PROTOCOL.md was read completely. The applicable
evidence-falsification and source-of-truth skills and their required references
were read in this lane. No instructions in retrieved source material were
treated as authority.

Source reading: the existing `late-fire-video-lineage/source-leads.md` and
the preserved secondary page's lines 499–510 were read directly; the latter
is a lead, not adopted as a factual account. Read the normalized folder-search,
four individual metadata, Organized-root and ReadMe responses, and the entire
subsequently supplied retrospective listing-request receipt. Inspected all
73 list entries through explicit identity-field projections and inspected the
listing schema. IA review covered allowlisted item/title/date/description/
access fields and the three listed video-file relationships, not all account
or catalog administrative fields. NIST HTML review was limited to canonical
metadata, the repository notice and the category links around lines 687–724;
the full 101,629-byte HTML was hashed but not fully interpreted. No transport
header files, preview sheets, root visual notes, report-figure images or
unrelated case records were read for this task.

Commands actually used from this unit include `wc -c`, `shasum -a 256`,
`sed -n '499,510p'` on the preserved secondary HTML, bounded `sed`/`rg` reads
of the NIST HTML, `jq` projections and exact-match assertions, and read-only
datetime arithmetic. An initial `jq` inspection incorrectly assumed listing
responses used `.structuredContent.results`; it failed with “Cannot iterate
over null.” Schema inspection established `.structuredContent.files`, and
the corrected checks passed. The failed command's chained byte/hash checks
did not run and were separately rerun successfully; it was not a source
absence or acquisition failure. A filename search for not-yet-created
request receipts returned no matches at that time, not a global record
absence finding.

This is an independent computational/read-only audit by another AI agent of
shared captured sources. It is not independent source acquisition, a human
forensic opinion, or new historical corroboration. No previously frozen
research, source file, producer or legal record was changed.

## Pinned inspected records

SHA-256 values computed during this review; paths below are relative to this
unit unless explicitly stated. Hashes authenticate the current local version,
not the historical assertions within it.

| Record | Bytes | SHA-256 |
| --- | ---: | --- |
| PROTOCOL.md | 4,719 | `7d0fb79d2a1a5cdfc92a7062221e75cd2a2a5caf5f85919c48d3d58bbabb0e2b` |
| sources/nist-repository.html | 101,629 | `af73969464f1d1a32fb96b169af129a21fd6781cdc18766c26d203bb0dfc5dfa` |
| sources/ia-cbs-metadata.json | 15,348 | `ed316aadb7cab3bf1e9163a74de4e35e66f6b094d9d10ff9412bf1df92abd9db` |
| sources/nist-cbs-folder-search.connector.json | 7,843 | `64fb1e41b773e10da666899b32e6a42c6afd823dfb76b4a239c2b36a2dfa5be8` |
| sources/nist-dub5-listing.connector.json | 20,209 | `d0ed7273e30ca088edcb8da854dfdcaf5969798ae8574cbdb40aa1057039d359` |
| sources/nist-dub6-listing.connector.json | 41,099 | `09c1c4009ab6fc257a34e0ec6e70852367d5b01dd034d04665b02165b88c24c4` |
| sources/cbs-net-dub5-14.metadata.connector.json | 829 | `6f957c4b6e6c76975fad97b6f45763fe62671ef62b32f2f140eadd132892568c` |
| sources/cbs-net-dub5-15.metadata.connector.json | 829 | `10abfa37acc5f22b71d095d2a5ed1cbb65b5e1a986ade04b0c30b03fd8f014e2` |
| sources/cbs-net-dub6-45.metadata.connector.json | 830 | `ab6806128b2ae9aee8ca07a50eb577edae8bd35a48d05c682648d525fcbc270b` |
| sources/cbs-net-dub6-44.metadata.connector.json | 830 | `b2ec8e0c146153e84ff505ec460fa8950c8e2d4465a8d91d1142384ec7bffc60` |
| sources/nist-organized-readme.connector.json | 3,887 | `0a15b65bfe7ee9fd75af6e813b8c243c9614e3b0655b4fb9bd00ecf310b20d6a` |
| sources/nist-organized-root.connector.json | 6,065 | `93658f5427045ae96bd6dfd086427ca3093c9b2fed01c26a3e03ff214653a9ec` |
| listing-request-receipt.md | 2,219 | `9919f84d826594809f0b2513ea21b3ad6772f0c420e5144ae0a8c0f162fe137f` |

Preserved secondary HTML (main, read-only):
`/Users/admin/docs/911/research/wtc7-video-comparison/sources/911conspiracy-tv-7-WTC-2020-07-01.html`,
SHA-256 `1d01d8ffce7358095c7aaf605d9f6dd91c69ab1eaa5440afb19ab2402dd33a2a`.
