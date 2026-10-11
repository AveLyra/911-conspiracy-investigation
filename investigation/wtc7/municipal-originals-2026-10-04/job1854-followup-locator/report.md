# Generator test follow-up records located with search limits

The fixed public-archive search returned new, exact document leads for the
July 1999 generator-test follow-up. It has **not yet located and verified the
underlying test measurements or completion of the seven reported corrections**.
No newly returned PDF was downloaded or read in this unit.

The result is a qualified diagnostic inventory: 142 returned occurrences,
97 unique document IDs, including 80 not present in the preceding 111-ID
extraction. Eight records omit folder_name, so the original eleven-property
acceptance check failed. That failure remains; no folder value was invented.

## What was searched and returned

The [frozen protocol](PROTOCOL.md) fixes ten queries, 50 results per query and
no pagination. Exact payloads and raw responses are preserved alongside the
[diagnostic inventory](root-diagnostic.json). The [source log](source-log.md)
records actual commands, source pins, failures and derivation.

| Query label | Returned / server estimate | Server termination | Missing-folder occurrences |
|---|---:|---|---:|
| penn | 50 /157 | Capped, COUNT_LIMIT; more available | 3 |
| penn_phrase | 16 /16 | NO_MORE_RESULTS | 0 |
| apt | 19 /19 | NO_MORE_RESULTS | 4 |
| transient | 4 /4 | NO_MORE_RESULTS | 1 |
| date_slash | 9 /9 | NO_MORE_RESULTS | 0 |
| date_words | 19 /19 | NO_MORE_RESULTS | 0 |
| load_shedding | 7 /7 | NO_MORE_RESULTS | 0 |
| fuel_pump | 9 /9 | NO_MORE_RESULTS | 0 |
| break_glass | 8 /8 | NO_MORE_RESULTS | 0 |
| control | 1 /1 | NO_MORE_RESULTS | 0 |

The exact known-record control returned 167873. The nine uncapped responses
satisfy the declared server-termination checks. Neither that status nor a
passing control establishes complete archive, OCR or document-body coverage.
The chosen terms do not exhaust all seven corrective items. The Penn query
covers only 50 of 157 estimated hits. No source was declared absent.

The 97 IDs have 519 metadata-reported pages, not 519 pages reviewed. They share
17 IDs with the preceding extraction. Repeated IDs across queries do not add
documents; different IDs can still be copies of one source. Municipal PDF
holdings remain 40 files/104 physical pages, including related copies.

## A direct warning against absence inferences

The previously read five-copy Job 1854 report family discusses transient
testing in both readers' frozen notes. Yet none of those five IDs occurs in
the saved transient-query response, even though it says NO_MORE_RESULTS.
They do occur in several other new queries, including the APT and exact-date
queries. This is a concrete retrieval nonmatch against already reviewed
content, not evidence that the reported tests or records did not exist.

The reason remains unknown: OCR, tokenization, indexing or other search
behavior could contribute. The check did not inspect the archive's index or
prove a particular defect. It establishes that this keyword screen cannot
bear a strong missing-document conclusion. It also explains why the earlier
folder/title nonmatches did not settle availability.

## The missing field is retained as missing

The strict adapter stopped as required. A separately declared
[diagnostic continuation](DIAGNOSTIC-CONTINUATION.md) inventories the actual
source fields without making the original test pass. 134 occurrences representing
89 unique IDs satisfy the original property contract. Eight occurrences,
eight unique IDs, are quarantined for omitted folder_name:

165940, 165962, 166093, 166099, 166345, 166386, 166426 and 166435.

Those rows retain the ten supplied scalar fields and raw result objects.
Their absent folder property is not the literal label None used elsewhere.
Quarantining does not assert that the files are false, unusable for every
purpose or evidence of concealment. Exact supplied IDs/titles/page/byte fields
can still locate a candidate, but the full metadata contract remains unmet.

## Next content packet and retained leads

The following six exact returned IDs form a useful next packet: seven
metadata-reported pages. Selection is based on labels and query membership,
not unread contents or guessed neighboring Bates numbers. A separate source
acquisition/content protocol must precede any reading.

| Returned ID | Archive label or locator basis | Reported pages / bytes | Question for the actual source |
|---|---|---:|---|
| 171251 | Cosentini's feild observation report; supplier and 7/31/99 queries | 1 /64028 | Does it identify supplied measurements, attachments or correction follow-up? |
| 172976 | Cosentini's Field Report Dated 8/2/99; same queries | 1 /67745 | What was transmitted, requested or completed, and when? |
| 172977 | Same field-report label and queries | 1 /60316 | Duplicate, annotation variant, or a materially different response? |
| 171520 | OEM -7 WTC fuel oil pump; APT query | 1 /44470 | Does it identify the reported temporary/intended pump arrangement or a dated correction? |
| 174095 | OEM/Ambassador project label; July31 and load-shedding queries | 1 /55156 | Does it document testing, software work, a schedule or closure? |
| 167866 | OEM/7WTC label; transient query | 2 /114201 | Measured results, requirements, correspondence, or unrelated content? |

These are questions, not answers inferred from labels. Dates in folder labels
remain archive descriptions until source inspection; the mes:date field is
not substituted for a historical document/test date.

Other retained leads include 172371 (maintenance contracts, 2 pages),
172958 (service agreement, 9), 168654 (Peoria generator test, 1), 171905/171909
(CO016 and break-glass query), the 52-page generator prepurchase specification
166874, and the other transient matches 166426/169094. A prescribed test
standard or service proposal must not become evidence that a test or repair
occurred. The 191-ID union of this and the preceding extraction is a locator
set, not a corpus of independent evidence or a completed reading queue.

## Verification and inferential ceiling

Root ran 20 strict synthetic tests and 8 diagnostic tests. Independent method
review reran those and added 22 strict and 9 diagnostic cases; the diagnostic
replay matches the frozen result and the unchanged strict calculation still
fails. The [preservation checker](preservation-check.md) verified ten exact
requests, 40 raw acquisition-file copy pairs and the separately preserved
diagnostic pair. These checks establish bounded software/copy integrity, not
historical authenticity.

A [separately implemented raw-response extraction](metadata-review.md) is now
frozen and reconciled. All 97 IDs, every supplied field, 142 query memberships
and ordinals, ten coverage rows, eight exceptions and 21 input pins agree.
Root also reran the peer method: its parsed JSON matches the peer's frozen
inventory. Both readers knew the missing-field issue; coordination also exposed
the 97-ID count. This is independent implementation, not numerical blindness,
another archive, or independent historical corroboration. The original strict
acceptance failure remains unchanged.

The captured returned-ID/count observations are directly established within
these responses (grade A). Treating labels or query matches as proof of raw
test performance or correction closure is unsupported (grade E); the actual
historical conditions remain unknown, not disproved.

The strongest finding is that there are specific accessible locator leads,
with a demonstrated search-coverage limit. What those documents show remains
unread. Nothing here verifies test performance, correction closure, permanent
fuel routing, event-day condition, intentional intervention or evidence
suppression. No physical-compatibility or overall collapse-cause ranking
changes. The full charter remains active and incomplete.

Raw response headers contain server-issued session cookies and are retained
local-only with an ignore guard; they are not approved for publication or push.
Generic schema/search feedback stays locally deduplicated under the archived
Sherlock-routing boundary. Main/legal, previous sources and frozen observations
are unchanged. No PDF content views, pagination, outreach, fees, engine action,
canonical promotion, staging, commit or push occurred.
