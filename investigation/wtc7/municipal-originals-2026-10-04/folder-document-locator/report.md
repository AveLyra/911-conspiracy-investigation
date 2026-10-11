# Structural and sprinkler folder document identities

October 4, 2026. Working research. **The public search endpoint returned five
document records in the two selected folders, including three PDFs not yet
read in this investigation.** The listings reconcile to the dated folder
catalog's three documents/six pages and two documents/two pages. This resolves
the immediate ID lookup; it does not establish source-document contents,
completed construction, inspections, or archival completeness.

## Exact returned records

Both folders belong to source `WTC 7`, box `7DCAS`, agency `Citywide
Administrative Services, Dept. of`, production volume `NYC-WTC0007`.
The folder names below are metadata, not independently verified document titles.

| Folder | Document ID | Reported end Bates | Reported pages | Reported PDF bytes | Content review status |
|---|---|---|---:|---:|---|
| Structural services | NYC-WTC_000167235 | NYC-WTC_000167236 | 2 | 79607 | Read in prior unit |
| Structural services | NYC-WTC_000167240 | NYC-WTC_000167241 | 2 | 79462 | Not acquired or read in this unit |
| Structural services | NYC-WTC_000167759 | NYC-WTC_000167760 | 2 | 79419 | Not acquired or read in this unit |
| Sprinkler quotation | NYC-WTC_000171300 | NYC-WTC_000171300 | 1 | 84808 | Read in prior unit |
| Sprinkler quotation | NYC-WTC_000171557 | NYC-WTC_000171557 | 1 | 85393 | Not acquired or read in this unit |

Exact structural folder label: `Mayor's Office of Emergency Management 7 World
Trade Center, 23rd Floor Structural Engineering Services`.

Exact sprinkler folder label: `Fire Sprinkler Quotation®Fuel Tank Room`.
The registered-sign character is present in both captured catalog and live
response. It was preserved in the query rather than silently replaced with
the slash used in the human-readable lead table.

The three new IDs come from actual response records, not increments from the
first Bates number. Similar sizes and shared folder labels do not establish
that the files are duplicates, amended terms, signed acceptances, calculations,
or completed-work records. Those remain content questions.

## Evidence and checks

The [folder catalog](folders.json), acquired from the
[independent repository](https://github.com/pranava0x0/sept11documents-mcp/blob/main/docs/data/folders.json),
reports capture at September 11, 2026 12:57 UTC. Its columns explicitly
separate folder document totals, page totals and first Bates. Rows 3645 and
3189, respectively, are the zero-based structural and sprinkler matches.
Each first-ID match is unique among the 4205 captured folder rows.

The published [adapter](portal.py) and its directly referenced
[CLI](portal_api.py) document a read-only JSON search operation. Their source
was inspected, not executed. Root submitted the saved
[structural request](structural-request.json) and
[sprinkler request](sprinkler-request.json) to the documented public endpoint.
Each requested at most 25 metadata records and no content excerpt. Both
responses were HTTP 200, JSON, with no redirects.

The preserved [structural response](structural-response.json) and
[sprinkler response](sprinkler-response.json) echo the exact queries. Every
result's source, box and folder matches its target catalog row. All five
document keys are unique; their result IDs and `.pdf` titles agree. Counts
and page sums match the two captured folder totals. Both have
`prev_avail=false`, `next_avail=false`, and a service termination of
`NO_MORE_RESULTS`; no second page was requested. Root's stdout-only Python
checks passed. Exact commands, file pins and acquisition receipts are in the
[source log](source-log.md).

The same saved requests were then sent directly to
`https://sept11documents.cityofnewyork.us/api/v2/search`, the City portal
hostname. Both returned HTTP 200 JSON with zero redirects. The
[structural City-host response](structural-front-response.json) and
[sprinkler City-host response](sprinkler-front-response.json) contain exactly
the same document IDs and every selected property value as their backend
counterparts, with the same echoed requests/counts and no further results.
This verifies the public portal route, not an independent historical source.
There were four metadata requests total and ten returned record appearances,
representing five unique document IDs.

The separately frozen [catalog review](metadata-review.md) and
[response review](response-review.md) independently confirm the literal
folder joins and ID/count calculations without seeing root's report first.
The response review covers the first backend pair; root checked the later
City-hostname pair. This is independent analytical checking, not a second
archive or independent content corroboration.

This is complete coverage of the records returned by these two specific
queries at acquisition, not proof that the City holds no additional records,
that indexing is exhaustive, or that all relevant work is filed under these
labels. The unrequested `related_document` field supplies no relationship
values here; this is not an attachment or cross-folder relationship search.
No new PDFs were fetched or reviewed. The earlier municipal content
coverage remains fourteen PDFs/thirty-four physical pages, including copies.

## Date and source limits

The separately acquired [catalog summary](catalog-summary.json) describes a
September 9 snapshot, not the September 11 folder snapshot. Its aggregate
24441 documents differs from the latter's 24437. This unit did not reconcile
the entire archive or determine why those dated snapshots differ; it does
not classify the difference as deletion or concealment. The two selected
folder totals do reconcile to the current query results. The portal's
`mes:date` is index metadata, not a document's historical date or proof of
the date the described work occurred.

## What this changes

The missing lookup step is resolved: the next source review can select exact
IDs 167240, 167759 and 171557, five reported pages in total. A prospective
content-review protocol should compare them with the already-read 167235 and
171300, checking for repeated content, changed dates/terms, client acceptance,
actual drawings/calculations and evidence of installed or inspected work.
Neither acceptance nor those technical contents are assumed in advance.

The finding strengthens the retrieval map, not either collapse hypothesis.
There is no cause-ranking change, legal promotion, engine/bridge activation,
spending, commit or push. The full investigation remains active and incomplete.
Public metadata retrieval is not a case-sensitive transfer; no outgoing
correspondence or source publication occurred.
