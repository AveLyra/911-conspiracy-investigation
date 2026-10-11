# First floor public document search

Declared October 5, 2026 before requests. Research only. The completed
held-metadata lookup did not identify an applicable underlying S-1 or clearer
same-revision S-S-1; its known drawing packet escaped the label predicates.
This unit tests the public index, not PDF contents, engineering or cause.

## Exact bounded requests

Use only the previously established read-only search endpoint
https://sept11documents.cityofnewyork.us/api/v2/search.
Four JSON request bodies are saved in this directory before execution:

| Label | Exact unparsed query |
|---|---|
| control | `ALL extension:pdf source:"WTC 7" box_name:"7DCAS" folder_name:"Mayor's Office of Emergency Management Alt. Route for Oil Pipes"` |
| ss1 | `ALL extension:pdf source:"WTC 7" "S-S-1"` |
| skss2 | `ALL extension:pdf source:"WTC 7" "SKS-S-2"` |
| s1_first | `ALL extension:pdf source:"WTC 7" "S-1" "first floor"` |

Each asks for count50, content_sample_length0 and exactly the existing eleven
VALUE properties: mes:key, title, source, agency, box_name, folder_name,
page_count, pdf_size, production_volume, production_end, mes:date.
No alternate spelling, punctuation removal, OR expansion, pagination or
increase in cap in this unit. Preserve every result, not just selected hits.
A quoted sheet identifier may match token sequences or compound labels;
a returned hit does not establish literal contents or a standalone sheet.
The paired phrases in s1_first are the exact request, not a verified assertion
about Boolean/full-text/OCR semantics.

Send the control first. The earlier record indicates the exact folder
contains NYC-WTC_000166828, but current contents/count are observed rather
than hard-coded as a successful outcome. A successful control is retrieval
of the known packet, not calibration of sheet/OCR recall. If it returns
valid metadata without the known record, retain that diagnostic and still
perform the three fixed target searches; no interpretation of absence.
If the route is denied or returns an HTTP/transport/content error, preserve
the response/exit and stop that route; do not switch hosts or bypass controls.

One HTTPS attempt per payload, 20-second connection limit, 60-second total
limit, 10MiB maximum, TLS verification enabled, no redirect, credentials,
cookies or headers containing case data. A sandbox-local DNS/network failure
may receive one explicitly approved network retry of the same request;
this is not permission to retry a server refusal. Observe live handles to
completion; no restart merely because a tool yielded. Curl status/byte/type/
redirect receipt and raw body are enough; do not collect session-cookie
headers. At most one web-reader open of the public portal supplies access
context, not search results. No other web sources or PDF acquisition.

## Extraction and checks

Preserve exact request/response bytes and hashes, execution time/receipts and
all failures. Validate request echoes and required result structure; reject
duplicate JSON keys/properties, multivalues, inconsistent IDs, nonpositive/
nonintegral page or byte counts and cross-query property conflicts. Keep
missing folder_name distinct from literal None. A record missing folder_name
may be inventoried with an explicit exception, never passed as eleven-field
complete. Unexpected omissions or schema shapes stop interpretation until
a declared diagnostic; do not invent sentinels or silently discard records.
Retain query appearances/ordinals and deduplicate unique document IDs only
for summaries. Different IDs are not automatically independent sources.

Reuse the inspected existing strict/diagnostic helpers where suitable; do
not import a module with uncontrolled execution. Record every dependency
pin. Existing relevant tests must pass and the new result must replay; a
separate reader independently extracts raw responses before reading root
results. Another method/preservation review checks scoped claims and bytes.
Report actual returned/estimated counts, results-key presence, page flags
and service termination. Capped or incomplete response sets stay incomplete;
NO_MORE_RESULTS describes the query return, not archive-wide recall.

## Selection and acceptance

Deliver all four outcomes (or exact stopped-route limit), reproducible
extraction, independent reconciliation and a concise source-pinned report.
Mark previously held IDs using the existing municipal synthesis/source logs
only when a specific candidate needs that check; no broad corpus census.
Prioritize newly returned exact sheet/drawing/index labels over accounting
context, preserving nonselected leads and labels with no presumed contents.
A potentially relevant new source requires a separate prospective complete
reading: actual sheet number, date/revision, first-floor subject and usable
member/grid correspondence to October15 S-S-1. If searches return only known
records or nonmatches, consider a separately declared finite drawing-index
packet from the held catalog, not an undirected attachment queue.

Main controls and the complete charter remain authoritative. This is local
working research; original records and earlier findings stay unchanged.
Public sheet/folder queries contain no confidential case material. No
image-budget reopening, model execution, legal/fact promotion, outreach,
fees, sensitive transfer, publication, staging, commit or push. The previous
goal turn made progress; this is the next source test, not a narrower goal.
The data-quality and document skills support the existing repository output,
not a new notebook, dashboard, cloud Page or scheduled task.
