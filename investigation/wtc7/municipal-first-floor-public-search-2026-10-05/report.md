# Public search for the first floor drawing

The four fixed searches returned **17 unique document IDs**, including two
useful content-review candidates: **173192, List of Drawings Addendum #1**,
and **169180, Blue Prints / Haz Mat Info / Fire Reports / Fire Prevention
Records**. Neither is yet a verified applicable S-1 or clearer S-S-1. This
unit locates records; it does not read their PDFs, identify altered beams,
establish installed conditions or change a collapse-cause ranking.

Unlike the preceding label-only screen, the public index retrieves the known
166828 drawing packet for both S-S-1 and SKS-S-2. That is evidence of successful
retrieval of this particular known packet, not a calibrated recall rate or
proof that every returned hit contains an exact standalone sheet identifier.
The S-1 plus first-floor query does not retrieve it, and other results have
oven, appliance, lease and schedule labels. Their contents remain unread;
these are not proved false positives or evidence of query tampering.

## Exact coverage

The [protocol](PROTOCOL.md) and [saved query strings](queries.json) preceded
all requests. Each read-only request to the [City document portal](https://sept11documents.cityofnewyork.us/)
asked for at most50 records and no content sample, using the existing eleven
metadata properties. Exact response bodies, queries and file/ordinal
memberships are preserved in the [complete extraction](result.json).

| Query label | Search focus | Returned / estimated | Known166828 returned |
|---|---|---:|---|
| control | Exact previously verified source/box/folder | 1 /1 | Yes |
| ss1 | Quoted S-S-1 | 15 /15 | Yes |
| skss2 | Quoted SKS-S-2 | 1 /1 | Yes |
| s1_first | Quoted S-1 and quoted first floor | 3 /3 | No |

All four return NO_MORE_RESULTS with next/previous-page flags false. No cap
was reached, but these are complete returned sets for these requests, not
complete archive coverage. Quotation marks, hyphens, ALL and paired terms
retain unverified indexing/token/OCR semantics. No spelling variants, new
Boolean expressions, pagination or cap increases were tried after results.

Twenty returned appearances reduce to17 unique IDs: 166828 appears in three
queries and173670 in two. The unique metadata-reported total is306 pages,
not306 acquired or reviewed pages. Shared IDs/properties are consistent;
different IDs may still contain copies or related portions of one source.

## Complete returned record list

These are original folder labels supplied by the index, not newly verified
document titles or subjects. Source for every returned record is WTC7 in the
service metadata, which does not by itself establish each packet's historical
building/project scope. Page/byte counts are per returned document.

| ID suffix | Supplied folder label | Pages | Bytes | Query membership |
|---:|---|---:|---:|---|
| 166099 | Omitted property, not a literal label | 6 | 463073 | ss1 |
| 166571 | Proposal for Full Comprehensive MEP Engineering Services for Forest City Tech Place Associates | 127 | 5943038 | s1_first |
| 166828 | Mayor's Office of Emergency Management Alt. Route for Oil Pipes | 8 | 533928 | control, ss1, skss2 |
| 167943 | Project Schedule with Project Progress | 5 | 647582 | ss1 |
| 168282 | Space Analysis by Unit Project #96-1346 | 4 | 666805 | ss1 |
| 168526 | 7 World Trade Center Mayor's Office of Emergency Management -1st, 7th, & 23rd Floors Change Order #56 | 1 | 43286 | s1_first |
| 169180 | 7 World Trade Center Blue Prints Haz Mat Info Fire Reports Fire Prevention Records | 25 | 4451736 | ss1 |
| 169723 | AGREEMENT OF LEASE | 91 | 4685110 | ss1 |
| 170916 | Project SFummary Sheet | 6 | 1259922 | ss1 |
| 171506 | None | 4 | 382269 | ss1 |
| 172415 | HERE ARE THE FOLLOWING ITEMS: | 5 | 413005 | ss1 |
| 172779 | 7 World Trade Mayors Office | 1 | 56938 | ss1 |
| 173070 | Gringer & Sons Quotation for Appliances | 1 | 93120 | ss1 |
| 173192 | List of Drawings Addendum #1 | 4 | 253273 | ss1 |
| 173374 | Door Schedule | 16 | 1164314 | ss1 |
| 173670 | Architectural Sketch Log | 1 | 67561 | ss1, s1_first |
| 173923 | Alto-Shaam.  Cooking and Holding Ovens | 1 | 77917 | ss1 |

166099 omits folder_name: one occurrence, one ID. It has the ten other
expected scalar properties and is retained as an explicit metadata exception,
not eleven-field complete. By contrast,171506 supplies the literal string
None; it is not converted to a missing value. The extraction reports
explicit_metadata_exceptions, not a clean full-property-set pass. The source
responses and original exception are unchanged.

## What should be read next

The first candidate is **NYC-WTC_000173192**, four reported pages/253273bytes.
Its drawing-index label and S-S-1 query membership make it a focused way to
test sheet/revision relationships. It could be another copy of the already-read
May index, an updated index or something else; none is assumed. Compare actual
contents and dates with held173199 only after a separately frozen new reading.

The second is **NYC-WTC_000169180**, 25 reported pages/4451736bytes. The broader
blueprint/fire-record label could supply geometry or a source path, but may
instead be unrelated in floor, project, era or document type. Its25 pages
require a separately declared complete-content review, not a single favorable
page or a claim that the packet already supplies the plan. These two candidates
are prioritized for drawing/index labels, not for a preferred collapse theory.

A bounded exact-filename check in the municipal research directory found the
known166828 and173670 PDFs but no173192,169180 or166571 file. That is a
filename/holding check within that directory, not proof that no copy exists
elsewhere or that any candidate is new historical evidence. No PDFs were
acquired in this unit. The earlier49-file/123-page content census is not
increased by the306 metadata-reported pages.

The other fifteen IDs remain in the complete result. In particular, the
first-floor/Change Order56 label of168526 remains a distinct source lead;
the127-page166571 proposal has unresolved project scope. Neither is silently
equated with the desired S-1, discarded as irrelevant from title alone, or
converted into an automatic archive-reading queue. The applicable October
revision, complete notch leaders/member endpoints and model correspondence
are still unresolved. CO23 seventh-floor and CO40 backup questions remain
separate.

## Verification and evidentiary limit

All four HTTP responses were200 JSON with no redirects. A preliminary
sandbox-local DNS failure was retained and the same control request succeeded
under approved network execution; this was not a server refusal or a bypass.
Raw scratch/preserved copies match byte-for-byte. The [small adapter](extract.py)
reuses the inspected existing strict/diagnostic functions, retaining actual
missingness and all returned memberships. Source and code dependency pins,
actual commands and timing are in the [source log](source-log.md).

The existing test command initially made48 passing invocations because an
imported20-test class was discovered twice. The explicit class invocation then
ran28 distinct tests, all passing. No48-distinct-test claim is made. The
complete parsed extraction replays exactly, including dependency/source pins.
The [independent extraction](independent-review.md) froze before access to the
root result. Root replayed its 20-test command and reconciled all 17 records,
20 memberships and four coverage rows. The independent reader's subsequent
112-check reconciliation also passed, including the complete report table.
The [method review](method-review.md) separately checked request scope, exact
copy preservation, dependency isolation and synthesis limits. Neither review
requested a factual correction. These are independent software/research checks,
not another archive source, transport witness or engineering validation.

The returned IDs, labels, counts and limited control outcome are observed
metadata plus reproducible calculation. Their applicability to the unresolved
structural question is an inference to test by content, not an engineering
finding. A wrong-project packet, different revision, duplicate index or an
unreadable drawing could defeat the proposed connection. No cause ranking,
missing-record accusation or legal conclusion follows from this search.

The existing SFB-005 fixtures cover query recall, missing versus literal labels,
source roles and independent reproduction. No new product defect or fix is
established. Feedback delivery remains pending locally under the archived-task
boundary. Main/legal, prior source bytes and readings remain unchanged; no
fees, outreach, engine action, sensitive transfer, publication, promotion,
staging, commit or push. The complete investigation remains active.
