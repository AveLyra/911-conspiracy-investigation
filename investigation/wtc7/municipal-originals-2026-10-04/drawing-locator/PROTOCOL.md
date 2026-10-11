# Named drawing lookup

Declared October 4, 2026 before this unit's searches. Working research.
Find exact indexed records that might contain SKP-3, SKP-4 or revised S-TS-7,
named by the already-read December 3, 1998 transmittal 167873. The cover
concerns toilet drains and loading-dock slab replacement; no causal connection
to collapse is presumed. This is a locator, not a drawing-content review.

## Fixed search scope

1. Search two held locator files only: the prior unit's `folders.json` and main
   `research/WTC7_archive_leads_2026-09-16.md`. Case-insensitive patterns are
   `SKP[ -]*[34]` and `S[ -]*TS[ -]*7`. Retain actual original labels, row/line
   positions, collection/box and counts; normalization is for matching only.
   Inspect JSON field names, types and unique keys before interpreting rows.
   Restrict folder-result relevance to source `WTC 7`; retain off-source hits
   as excluded locator results if encountered, without inferring their content.
2. Use three public City search requests, one per literal phrase `SKP-3`,
   `SKP-4`, `S-TS-7`, each restricted by `ALL extension:pdf source:"WTC 7"`.
   Known read-only route: `https://sept11documents.cityofnewyork.us/api/v2/search`.
   Use count 50, content_sample_length 0, and the same eleven explicit metadata
   properties as the validated preceding folder lookup. Preserve exact payloads
   before requests. No implicit assertion about full-text/OCR search coverage.
3. At most one additional metadata request may retrieve the exact named folder
   from the held catalog as a positive route/known-record control, with identical
   field selection and cap. This is not a different cause or content search.
4. One web-reader open of the public portal is allowed for access context.
   No open-ended web search, neighboring-ID guessing, arbitrary alternate
   spellings, broad crawl, source-body extraction or PDF acquisition here.

Requests: one HTTPS attempt per saved payload, 60 seconds/10 MB, no redirect,
credentials or cookies. Preserve returned bodies, code/status and actual exits;
stop that route after an access denial. Observe any live handle to completion.
If there are more than fifty records or a next page, preserve an explicitly
incomplete listing; do not expand the cap after seeing results. Returned files
remain unread until a separate admission/content protocol.

## Acceptance and interpretation

Distinguish query occurrences from unique document IDs and folder totals from
individual page counts. Check query echo, result fields, pagination and counts.
Report query errors, empty results and unexpected matches rather than assuming
literal phrase semantics. An exact known-cover match is a route/control result,
not proof that the three missing sheets were indexed or would be retrievable.
Catalog labels are not contents, and token punctuation/OCR may limit recall.

Deliver preserved requests/responses, a scoped unique-ID candidate list and
an independently checked metadata receipt, or the precise finite retrieval
limit. A negative lookup is not archive-wide absence or concealment. Select
the next content candidates by explicit drawing labels and page coverage,
not by a preferred hypothesis. No cause ranking changes from metadata alone.

The data-quality skill is a scoped companion for grain, ID and pagination
checks within the existing repository investigation, not a new dashboard,
publication or separate analytics product. Existing research notes are the
user-selected output. Main controls and charter remain authoritative; source
records and frozen readings are not changed. No legal promotion, private data,
fee, outreach, engine/bridge action, stage, commit or push.
