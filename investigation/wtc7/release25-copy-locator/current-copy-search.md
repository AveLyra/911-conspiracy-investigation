# Current-copy search: target join unresolved

2026-09-20 UTC. Independent locator lane; research only. No source-copy
identity, acquired footage, historical clock, continuity, thermal result or
cause ranking is established. Only this note was written.

## Outcome and bounds

No current public copy or populated crosswalk for the exact
`Release25/42A0122 - G25D33/VIDEO_TS` eight-file inventory was identified in
the returned search results. This is a limited failed join, **not** evidence
that the DVD or a public copy does not exist. Four queries and one page
request were used; seven of the eight permitted page/metadata requests
remained unused. No media, torrent, account, upload, outreach or fee occurred.

After the one successful documentation-page open, root reported that its
parallel Wayback availability requests returned curl exit 56 with reported
HTTP 429, and directed this lane to defer further archive.org requests.
I complied: no Archive item/API call, retry, alternate transport, hostname
cycling, or alternate-service retrieval of those blocked routes followed.
That diagnostic is root-reported, not a response independently obtained in
this lane. The remaining indexed-web query did not contact that host directly.

The strongest competing interpretation is that a copy exists under another
name or in a file listing not indexed by these web queries. Generic DVD names
such as `VTS_01_1.VOB` cannot discriminate the target from other discs. The
eight-file catalog is a useful reference inventory, but its SFile IDs are
catalog record identifiers, not verified media hashes. Sparse search results
therefore cannot support withholding, intent, global absence, or a substantive
historical conclusion.

## Exact query/request ledger

Queries used the web search tool, `response_length: long`, with no separate
domain-array or recency parameter. Q1–Q3 were submitted in one batch; the
combined response does not assign a separate zero-result count to each query.

| ID | Exact query | Actual returned scope |
| --- | --- | --- |
| Q1 | `"42A0122" archive video` | Combined Q1–Q3 response below |
| Q2 | `site:archive.org "NIST" "Release 25"` | Combined Q1–Q3 response below |
| Q3 | `site:archive.org/developers "advancedsearch.php"` | Combined Q1–Q3 response below |
| Q4 | `"G25D33" -site:ic911.org -site:911datasets.org -site:911conspiracy.tv` | Tool explicitly returned Empty search results |

The combined Q1–Q3 response contained only excerpts from
[IC911's Building 7 collection](https://ic911.org/building-7-collapse/) and
[South Tower collection](https://ic911.org/south-tower-collapse/).
They repeat the known target-folder reference among descriptions of multiple
shots, not a current host inventory or DVD-to-current-item crosswalk.
Neither page was opened in this lane. Advocacy, timing and physical claims
in those excerpts were not adopted; the separately assigned `24:49` marker
was not transferred to Window Shot. Prior review established the restored
index's dependence on the older secondary archive.

| ID | Exact requested URL | Result / limits |
| --- | --- | --- |
| P1 | `https://archive.org/developers/` | Successful parsed web text, 87 reported lines; read the returned page. It identifies the official item/metadata documentation and links Item Metadata API: Read. No item identifier, target record or current-copy evidence was supplied. |

The [developer landing page](https://archive.org/developers/) was opened to
locate documented public metadata/search entrypoints, not to infer a source
item ID. Its API documentation links were not followed after root's deferral.
No failed page request occurred in this lane; the absence of an API response
must not be relabeled a successful empty catalog search. No raw response body
was saved, so no new web-source byte count or SHA-256 is claimed. Tool-returned
parsed text and search excerpts are not immutable raw HTML captures.

## Inputs and next discriminator

Read the new protocol and the entire preceding report before searching.
Main authority/charter hashes were rechecked unchanged from the preceding
fully read controls; the orchestration, evidence-falsification and
source-of-truth disciplines preserved the research/record boundary.

| Local input | SHA-256 |
| --- | --- |
| This unit's `PROTOCOL.md` | `2f6a4cd493afe5dae652404c12566e160f93abbe2ea2cd4ed21f31721570f491` |
| `../release25-source-locator/report.md` | `368334e0c23da89b0aa428693d67e2f8b90875fa5775675aedcf19f58d512b3e` |
| Investigation `CHARTER.md` | `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd` |
| Main `AGENTS.md` | `0bfca4efc4e9eabdaa895f7268407bb7a47c0ecc2a4599d957454cd0623c2aa8` |
| Main `WORKFLOW.md` | `17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a` |
| Main `START-HERE.md` | `30f3734a833d8737ee680b8f10c167e71f0151465df2b8db95d62f278ab3ab72` |

Actual local checks were complete reads of the two task documents and
`shasum -a 256` of the listed inputs. No local source or prior report changed.
No independent current-host inventory was available to reconcile against
the eight catalog names; filename/content/size/hash joins remain untested.

The next discriminating record would be a current public item manifest or
populated production crosswalk explicitly associating the **full** target
folder with a host item and file sizes/checksums. A previously observed but
uninspected generic Archive item, `vts-01-1_20260507`, remains only a lead in
the preceding root search ledger, not a candidate match established here.
Any later metadata inspection must wait for the access deferral to be lifted
and be separately declared; no media acquisition is authorized by this note.
This bounded lane stops without another speculative query or absence claim.
