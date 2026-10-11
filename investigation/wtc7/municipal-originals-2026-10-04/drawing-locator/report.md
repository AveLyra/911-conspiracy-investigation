# Named drawing search results

October 4, 2026. Metadata only; working research. The live City index returns
sixteen distinct document IDs for the three named-sheet queries and the
known-cover control. These include a three-page record labeled **Drawings**,
an **Architectural Sketch Log**, and an eight-page **Alt. Route for Oil Pipes**
record. They are specific new content-review candidates, not demonstrated
copies of the sought sheets or evidence that the work was performed.

## Search coverage

The [prospective protocol](PROTOCOL.md) fixed two held locator files, three
literal sheet-number queries and one exact-folder control. The held September
11 catalog and main archive-leads memo identify only the already-read 167873
cover under the name SKP-3/SKP-4/revised S-TS-7. The complete current responses
provide further IDs. This is a difference in search scope, not evidence that
the older catalog omitted documents: it catalogued folder labels, whereas the
query can return documents whose folder labels lack those exact strings.
Actual matching fields, tokenization and OCR recall remain unverified.

| Saved query | Returned document occurrences | Sum of reported document pages | Pagination |
|---|---:|---:|---|
| SKP-3 | 13 | 35 | No previous/next page; NO_MORE_RESULTS |
| SKP-4 | 12 | 34 | No previous/next page; NO_MORE_RESULTS |
| S-TS-7 | 3 | 10 | No previous/next page; NO_MORE_RESULTS |
| Exact known-cover folder | 1 | 1 | No previous/next page; NO_MORE_RESULTS |

The 29 query occurrences reduce to 16 IDs and 47 reported pages. These are
**metadata counts, not newly read pages**. The same document across searches
is counted once; four hits on 167873 do not make four sources. All selected
properties agree across repeated IDs. All returned records identify WTC 7,
box 7DCAS, and the requested agency/production fields are preserved in the
[checked metadata](checked-metadata.json). Service estimates equal returned
counts, within the fixed cap of fifty per query. These flags establish only
the complete returned result sets, not complete historical archive recall.

## Exact candidates

The table preserves the document-level page counts and original folder labels.
Labels are source metadata, not findings about contents, approval or execution.
The known cover was read in the preceding content unit; the other candidates
have not been read in this lookup.

| ID suffix | Pages | Folder label | Query matches |
|---|---:|---|---|
| 166828 | 8 | Mayor's Office of Emergency Management Alt. Route for Oil Pipes | S-TS-7 |
| 167170 | 2 | Various Change Orders Mayor's Office of Emergency Management 7 World Trade Center New York, New York | SKP-3 |
| 167873 | 1 | SKP-3 & SKP-4 AND REVISED S-TS-7 FOR YOUR USE | All three; control |
| 167874 | 3 | Drawings | SKP-4 |
| 168580 | 1 | 7 World Trade Center Mayor's Office of Emergency Management - 1st, 7th, & 23rd Floors Chang Order #38 | SKP-3; SKP-4 |
| 168581 | 1 | 7th Floor Louvers 7 World Trade Center Change Order #038 Amb. Job #S57-5175 | SKP-3; SKP-4 |
| 171286 | 5 | Breakdown of approved Change Orders | SKP-3; SKP-4 |
| 171620 | 3 | Mayor's Office of Emergency Management®7 World Trade Center®Breakdown of approved Change Orders | SKP-3; SKP-4 |
| 171802 | 2 | Various Change Orders Mayor's Office of Emergency Management 7 World Trade Center New York, New York | SKP-3 |
| 171840 | 6 | 7 World Trade Center Mayor's Office of Emergency Management 1st, 7th, & 23rd Floors Chang Order #38 | SKP-3; SKP-4 |
| 172947 | 3 | MOEM 7 WTC Breakdown of approved Change Orders | SKP-3; SKP-4 |
| 172953 | 5 | None | SKP-3; SKP-4 |
| 173670 | 1 | Architectural Sketch Log | S-TS-7 |
| 173920 | 2 | Change Order Request Clarification | SKP-3; SKP-4 |
| 173949 | 2 | Breakdown of Approved Change Orders | SKP-3; SKP-4 |
| 174004 | 2 | Breakdown of Approved Change Orders | SKP-3; SKP-4 |

`None` is the literal returned label, not a parser-invented null. Odd spelling
and the registered-sign separators are preserved. Dates in `mes:date` are not
treated as document authorship, work or completion dates. Relevance scores
are not evidence-confidence scores. The adjacent-looking ID 167874 was
actually returned by the SKP-4 query; it was not inferred by incrementing the
cover's ID. Proximity alone does not prove it was that cover's attachment.

## Verification and limitations

The [source log](source-log.md) records every request/response, local DNS
failure, approved network execution, hashes and parser correction. The
[read-only checker](check_metadata.py) rejects duplicate JSON keys/property
IDs, multivalues, malformed IDs, nonintegral byte counts, mismatched query
echoes and cross-query property disagreements. It checks the known-cover
control against actual 167873. The first run failed because this service
represents byte counts as whole-valued JSON floats; the correction retains
the finite, positive, integral requirement rather than changing the data.
No result is claimed from that failed run. The separately frozen
[metadata review](metadata-review.md) agrees on query echoes, all sixteen
IDs, repeated-property equality, counts and termination. It also joins every
candidate to exactly one held source/box/folder row while keeping that row's
aggregate counts separate. Root read the complete review. This independent
parsing did not repeat HTTP acquisition or inspect PDF contents.

The strongest objection is that these are search hits, not viewed contents:
punctuation/token handling, references to other sheets, copied correspondence
and incomplete OCR could explain matches or nonmatches. A known-cover control
does not calibrate recall for unindexed drawings. No PDF was acquired or viewed
in this unit, no approval or installed condition established, and no cause
ranking changed. The previous seventeen-PDF/thirty-nine-page content count
remains unchanged.

## Next content review

First declare complete reading of exact **NYC-WTC_000167874** (three reported
pages, 258425 bytes) and **NYC-WTC_000173670** (one reported page, 67561 bytes).
Their drawing/log labels are the closest task-specific leads. Check actual
sheet identifiers, revisions, dates, discipline, subject, geometry, approval
and joins to the held cover without assuming attachment or construction.
Keep **NYC-WTC_000166828** (eight reported pages, 533928 bytes) as the next
explicit oil-route candidate, not a missing lead silently dropped. The change
order matches remain the finite queue above, with potential copy families to
be checked before claiming corroboration.

Main/legal records and frozen observations remain unchanged. No outreach,
fees, private-record retrieval, engine/bridge action, publication, canonical
promotion, staging, commit or push. The complete investigation remains active.
