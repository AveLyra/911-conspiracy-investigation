# Bounded publisher/release-root search

2026-09-20, completed approximately 01:19 UTC. Independent source-locator lane;
working research, not media authentication or a legal-record finding.

## Result and strongest objection

No exact filename, inspectable target inventory, file size, checksum, or
publisher-to-file join for Release 25 / `42A0122 - G25D33` was obtained in this
lane. This is a bounded retrieval gap, not evidence that the folder, footage,
or a public copy does not exist. Four public queries and eight page opens were
used, counting three failed opens. No media was acquired or played; no image
was displayed; no torrent, account, outreach, upload, or source-supplied code
was used. Root separately handles the literal-folder and linked-video routes.

The strongest objection to treating repeated web mentions as corroboration is
source dependence: IC911's [archive introduction](https://ic911.org/wtc-collapse-video-archive/)
expressly describes restoring Matt Nelson's former 911conspiracy.tv archive
(returned text lines 59–60). Its completeness claim was not independently
tested. A restored secondary index is not a release inventory or independent
authentication. Conversely, failed catalog access and limited indexed results
do not disprove that index's lead. A folder mentioned for several shots could
contain a compilation; common folder naming alone would not establish a
continuous recording or an exact scene join.

## Actual query ledger

All queries used the web search tool with `response_length: long`, no recency
restriction. Q1/Q2 were submitted together, as were Q3/Q4; combined responses
do not establish separate per-query zero-result counts.

| ID | Exact query | Domain parameter |
| --- | --- | --- |
| Q1 | `site:911datasets.org "Release 25" NIST` | Omitted |
| Q2 | `site:ic911.org "Release 25" NIST` | Omitted |
| Q3 | `"NIST FOIA" "Release 25"` | `911datasets.org`, `archive.org`, `nist.gov`, `ic911.org` |
| Q4 | `site:archive.org "NIST" "25" "911datasets"` | Omitted |

Both combined responses supplied IC911 articles/index excerpts, not a target
release-root inventory. Besides the opened pages below, returned excerpts
included the North/South Tower collections; CBS Mark LaGanga; Chris Hopewell;
MSNBC Live; CBS on West Street; Extra West; Sumner Jules Glimcher;
NIST-14CBS-Net-Dub2-11unknown; NIST-14-WNBC-Dub9_02-Jersey; Evan Fairbanks;
and a journal article/PDF about South Tower light appearances. These other
clips were not opened as substitute target sources. One excerpt exposed an
Internet Archive item for `42A0106-G25D16`, a different folder; it was not
followed or treated as the target. Search excerpts alone were not footage
inspection or primary inventory verification.

## Actual page/open ledger

Each row is one counted open, including clicks and failures. Successful
results were parsed web text, not preserved raw HTML or a live-media preview.
The tool supplied crawl-age labels, not byte-level retrieval receipts.

| ID | Requested URL or observed link destination | Actual result and inspection limit |
| --- | --- | --- |
| P1 | `http://911datasets.org/` | Internal Error; one-line result. No catalog body. |
| P2 | `https://ic911.org/building-7-collapse/` | Page returned, 334 reported lines; visible response ended at line 191. Observed navigation links supplied P3/P5/P7. No claim to inspecting the remaining live page text. |
| P3 | `https://ic911.org/data-archives/` — P2 link 37 | Page returned, 167 lines. Lines 58–64 describe a planned archive and inactive archive links; Videos/Photos/Documents point to the same About link in this parsed response, not a Release 25 inventory. |
| P4 | `http://911datasets.org/index.php/SFolder:3IAGVZVIFRCYCZVEEMC4QG2NSIE3UGAF` — literal URL displayed in a search excerpt | Internal Error: tool reported `https://911datasets.org/index.php/SFolder%3A3IAGVZVIFRCYCZVEEMC4QG2NSIE3UGAF` inaccessible. This was the displayed literal, not a resolved archive hyperlink; see P8. |
| P5 | `http://911datasets.org/index.php/Release_14_-_NIST_Cumulus_Video_Database` — P2 link 58 | Internal Error: HTTPS fetch reported `(400) Timeout fetching`. This observed Release 14 entrypoint was attempted for release-navigation context, not misidentified as Release 25. |
| P6 | `https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations` — previously preserved official URL | Page returned, 299 lines. Category labels appear at lines 159–167, but this parsed response does not expose their folder hyperlinks or a Release 25 crosswalk. |
| P7 | `https://ic911.org/wtc-collapse-video-archive/` — P2 link 36 | Page returned, 168 lines. Lines 59–65 explain restored-index provenance and link the three building collections, not a numbered-release file inventory. |
| P8 | `https://ic911.org/consensus-panel/consensus-points/point-wtc7-8/` — returned search result | Page returned, 273 lines. Inspected footnote 18, lines 162–171, for the observed release/SFolder route; substantive historical/causal argument was not adopted. |

These failures describe the tool's routes, not independently verified HTTP
origin-server status or a worldwide availability test. No retries through
guessed identifiers, alternative schemes, or unobserved API endpoints occurred.

## What the sources actually support

The [current IC911 Building 7 page](https://ic911.org/building-7-collapse/),
returned line 139, associates the target folder with a different shot, labeled
NBC Leaning Cam, and gives `24:49`. That is not a time established for Window
Shot. The preserved older index, local line 509, separately associates Window
Shot with Dub5 14/15 and Dub6 45/44 and links `tZlENw_xuXU` while naming Release
25 / `42A0122 - G25D33`. It does not supply a target filename, size, checksum,
catalog ID, or authenticated capture time. No new viewing was inferred from
either description.

The [IC911 footnote](https://ic911.org/consensus-panel/consensus-points/point-wtc7-8/)
quotes a video description naming NIST FOIA #09-42, Release 25, **different**
folder `42A0120 – G25D31`, a DVD container, and 3.82 GB. Those are quoted
publisher assertions, not independently verified file metadata, and must not
be transferred to `42A0122 - G25D33`. Its displayed SFolder URL is the literal
used at P4. On P8 inspection the actual hyperlink is identified by the tool as
pointing to `web.archive.org` (link 96), not directly to 911datasets. The full
archive target was not resolved because the eight-open budget was exhausted.
This corrects any assumption that the displayed URL and actual href were the
same. P4 did not inspect a Wayback snapshot.

The [official NIST page](https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations)
describes its NIST-owned Google repository and distinguishes Organized,
Original Tape, and Other collections. Lines 248–256 warn that tags are
incomplete, copies may occur across categories, and NIST takes no position on
embedded camera/photographer metadata accuracy. It supplies no observed
Release 25-to-WTCI filename mapping in this response. Its current parsed text
was not hashed or equated byte-for-byte to the older preserved HTML.

## Reproducibility pins and remaining discriminating record

Local checks used `sed -n '495,513p'` on the preserved index and `shasum -a 256`
on the following files. No local source was edited. All main controls and the
charter had been read fully; their current hashes were rechecked unchanged.
Provenance/falsification and source-of-truth checks kept secondary assertions
separate from verified catalog content and the research lane separate from
the legal record.

| Local file | SHA-256 |
| --- | --- |
| This unit's `PROTOCOL.md` | `b68b2b5de728f1a66950b67eb787f5dd06e7920875ba65f2cce362d93ee79662` |
| Investigation `CHARTER.md` | `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd` |
| Main `/Users/admin/docs/911/AGENTS.md` | `0bfca4efc4e9eabdaa895f7268407bb7a47c0ecc2a4599d957454cd0623c2aa8` |
| Main `WORKFLOW.md` | `17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a` |
| Main `START-HERE.md` | `30f3734a833d8737ee680b8f10c167e71f0151465df2b8db95d62f278ab3ab72` |
| `/Users/admin/docs/911/research/wtc7-video-comparison/sources/911conspiracy-tv-7-WTC-2020-07-01.html` | `1d01d8ffce7358095c7aaf605d9f6dd91c69ab1eaa5440afb19ab2402dd33a2a` |
| `../late-fire-catalog-join/sources/nist-repository.html` | `af73969464f1d1a32fb96b169af129a21fd6781cdc18766c26d203bb0dfc5dfa` |

No new web response body was saved or assigned a fabricated source hash.
The smallest useful next source is the observed footnote's actual archive
hyperlink, followed only if it exposes a release-root navigation path; its
other-folder listing cannot itself resolve this target. A decisive locator
would be an inspectable Release 25 inventory explicitly listing
`42A0122 - G25D33` and constituent filenames/identifiers, or a publisher
crosswalk linking that exact folder to a current host item. Further browsing
requires an explicit scope extension. Located, retrievable, acquired,
content-matched, continuous, historically timed, and cause-discriminating
remain separate states; none of the latter states was established here.
