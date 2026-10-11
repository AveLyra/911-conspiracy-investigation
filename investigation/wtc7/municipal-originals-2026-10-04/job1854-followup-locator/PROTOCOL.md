# Job 1854 follow-up metadata lookup protocol

2026-10-04. Research only. Declared before this unit's requests or results.
The preceding coordinate reconfirmation added no investigation evidence.
This unit follows the five-file Job 1854 report review, not a new general
screen for evidence supporting a preferred cause.

## Question and authority

Can the public City archive identify exact candidate records for the July 31,
1999 H.O. Penn test report, APT transient recordings or review, dated closure
of the reported corrective work, or a July 17/31 date bridge? The preceding
report names these records but does not supply them. Positive operation and
unfinished work both remain in the source account.

Main AGENTS.md, WORKFLOW.md, START-HERE.md and the complete main investigation
CHARTER control. This dedicated investigation worktree is the only write
destination. Main/legal files, old sources, frozen notes and previous metadata
remain read-only. This is a metadata lookup, not inspection of newly acquired
PDF content, source authentication, archive exhaustion or legal promotion.

## Fixed requests and acquisition

Use the previously observed public read-only search endpoint:
https://sept11documents.cityofnewyork.us/api/v2/search

POST each of the ten saved label-request.json files once successfully. Every
request fixes count=50, content_sample_length=0 and the eleven VALUE properties
used by the preceding lookup. The exact label and query map is:

- penn: `ALL extension:pdf source:"WTC 7" Penn`
- penn_phrase: `ALL extension:pdf source:"WTC 7" "H.O. Penn"`
- apt: `ALL extension:pdf source:"WTC 7" APT`
- transient: `ALL extension:pdf source:"WTC 7" transient`
- date_slash: `ALL extension:pdf source:"WTC 7" "7/31/99"`
- date_words: `ALL extension:pdf source:"WTC 7" "July 31"`
- load_shedding: `ALL extension:pdf source:"WTC 7" "load shedding"`
- fuel_pump: `ALL extension:pdf source:"WTC 7" "fuel oil pump"`
- break_glass: `ALL extension:pdf source:"WTC 7" "break glass"`
- control: `ALL extension:pdf source:"WTC 7" box_name:"7DCAS" folder_name:"SKP-3 & SKP-4 AND REVISED S-TS-7 FOR YOUR USE"`

These source-specific strings were chosen from the already reviewed report.
The bare/quoted supplier forms address possible punctuation and phrase behavior;
they do not validate the archive's tokenizer or OCR. The control must retrieve
NYC-WTC_000167873. Passing it verifies that narrow known-record retrieval works,
not general content coverage or punctuation sensitivity.

Use HTTPS-only curl with configuration disabled, 20-second connection timeout,
60-second total timeout and 10 MiB response cap; no redirects, credentials,
cookies, personal material or private query terms. Preserve raw response bytes,
HTTP status/content type, redirect count and failures. A sandbox DNS failure
may receive one scoped network retry of the same public payload; HTTP refusal
is not authorization to bypass access controls. Re-poll an actual live handle;
do not restart because observation timed out. No pagination or query enlargement
after seeing outcomes belongs to this unit. Maximum 500 returned occurrences;
server estimates and completeness indicators must be retained.

## Derivation and acceptance

Reuse the inspected test-acceptance-locator/check_metadata.py scalar/property
contract through a narrow adapter. Require exact request echo, eleven distinct
scalar properties, well-formed IDs/titles/source, positive page/byte metadata,
no duplicate IDs within a query and identical metadata across shared IDs.
An absent results key is allowed only for estimated zero and no next page.
Record estimated_count, actual returned count, next/previous availability,
termination causes and whether results key exists. Previous/next availability,
estimate above returned count, missing termination evidence or any cause other
than NO_MORE_RESULTS prevents a complete-query label. An estimate below returned
count or malformed response stops analysis for explicit review; it is not proof
of source falsity. Do not disable Python assertions.

Report query membership, all unique IDs and all eleven source fields. Page
totals describe archive metadata, not pages inspected. No live filesystem join
is part of the deterministic result. Compare resulting IDs with the previous
111-ID extraction only after independently freezing the new extraction. A new
ID is new to this extraction, not a new historical document or independent source.

Run synthetic checks for duplicates, conflicting metadata, empty results,
request mismatch and incomplete coverage. A second reader derives its own
coverage/ID/property table from raw responses without reading root output;
freeze both before comparison. Separately verify all request/response hashes
and raw-response preservation. Independent method review should flag schema or
inference errors before final synthesis. Mechanical agreement validates the
extraction, not the archive's labels, OCR or historical statements.

Acceptance is preserved exact requests/responses, validated extraction,
independent reconciliation, explicit coverage/negative-evidence limits and a
bounded next content selection grounded in returned IDs. An empty or capped
result is retained. Deliver protocol, root extraction/code and tests, independent
metadata review, preservation/method checks, source log and concise report.
Update existing navigation/status only; use deduplicated generic feedback.

## Exclusions and stopping point

No newly found PDF downloading/reading, page guessing, presumed enclosures,
source-family independence, correction completion or installed-state conclusion
from labels alone. Select any next content packet separately, fixing exact
returned IDs, expected pages and interpretation questions before views.
This unit cannot establish a 2001 condition, fire/support-loss mechanism,
deliberate operation or concealment, or change a collapse-cause ranking.

No outreach, fee, external disclosure of sensitive material, engine activation,
legal edit, canonical promotion, staging, commit or push. Archived Sherlock
feedback routing remains pending; do not reopen or substitute a destination.
The full charter and other human/expert/model/permission gates remain active.

