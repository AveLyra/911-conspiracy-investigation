# First floor plan metadata search

The fixed held-metadata search does **not identify the applicable underlying
S-1 or a clearer same-revision S-S-1**. It finds only lower-specificity context
leads. This is a limitation of this metadata screen, not a finding that the
drawings do not exist or were withheld. The known packet containing S-S-1
is itself a text-predicate nonmatch, providing a concrete reason not to use
these labels as an absence test.

## What was searched

The [protocol](PROTOCOL.md) fixes 24 local JSON files: one captured folder
catalog and 23 saved search responses. The catalog has 4,205 folder rows,
including 1,639 labeled WTC 7. The responses have 302 returned appearances
representing 208 unique document IDs. Repeated appearances are not additional
documents, and different document IDs are not necessarily independent sources.
The catalog was captured September11,2026; this unit did not refresh it.

Only folder labels in the catalog and supplied title/folder properties in
the responses were searched. All 24 files, totaling 933,955 bytes, have saved
hashes in the [complete result](result.json). Echoed search requests and
available-field definitions were not searched as document descriptions.
Source fields and one-based row/result positions are retained verbatim.
No PDF, image, original drawing, model input or new archive response was read.

The three declared term categories found 38 catalog rows: 36 WTC 7 context
leads and two off-source drawing labels. The returned-document metadata has
11 matched appearances representing eight unique IDs, all context leads.
There are **no sheet-token leads and no combined first-floor/structural
subject leads** under the declared predicates. This classification is not
an engineering relevance score; for example, the first-floor rebar labels
below lack the declared structural-context words and remain context leads.

## Why the negative result is limited

Four already-known controls were located by exact document/first-Bates ID,
independently of text matching. Their prior contents are known from earlier
source reviews, not inferred afresh from their labels here.

| Known source | Metadata location and result | Consequence |
|---|---|---|
| 166828, held S-S-1 packet | Catalog row3653 and drawing-locator/sts7 result1: Alt. Route for Oil Pipes; no declared text match | A known relevant drawing packet escapes this metadata screen. |
| 173199, May drawing index | Catalog row2904: Addendum to Specifications and Drawings dated 5/4/1998; context match only | The label does not expose the S-1 sheet or establish the October underlying revision. |
| 173529, April comments | Catalog row2836: 7 World Trade Center, Manhattan Freedom of Information Request; no match | Administrative packaging can hide structural subject matter. |
| 173670, partial sketch log | drawing-locator/sts7 result3: Architectural Sketch Log; context match only | A log title is not the referenced drawing or a complete revision register. |

The eight unique document-level context matches are 166842, 167235, 167240,
167759, 167874, 168697, 173670 and 173834. They include antenna, engineering
services, drawings and shop-drawing labels; their presence alone does not
identify the requested first-floor plan. The complete labels, properties and
query appearances remain in the result, including the two off-source matches.

## Retained context leads

These are catalog labels, not newly read contents or a mandatory acquisition
queue. Counts are folder aggregates, even when a folder has one document.
The first Bates locates the first reported document, not every page or member
of a multi-document folder.

| First Bates suffix | Catalog row | Reported documents / pages | Original label |
|---:|---:|---:|---|
| 171851 | 4126 | 1 /1 | The Cantor Seinuk Group P.C. First Floor - rebars |
| 171853 | 4127 | 1 /1 | The Cantor Seinuk Group P.C. First floor - rebars |
| 172319 | 3272 | 1 /4 | List of Drawings |
| 173192 | 3273 | 1 /4 | List of Drawings Addendum #1 |
| 167669 | 3274 | 1 /4 | List of Drawings Issued for Bulletin # 1 |
| 167655 | 3654 | 1 /4 | Mayor's Office of Emergency Management Drawings |
| 173363 | 2905 | 1 /6 | Addendum to Specifications and Drawings dated 5/4/98 |
| 166752 | 2941 | 10 /18 | Architectural Sketch Log |

These labels could refer to correspondence, copied indexes, unrelated sheets
or later revisions. The first-floor rebars may relate to the separate slab
work, not the unresolved notched-beam plan. Shared subject, nearby IDs and
matching page counts do not establish attachment, copying or revision identity.
The complete 38-row result is retained rather than replacing it with this
shorter navigation table.

## Coverage and missingness

Three saved searches were capped: generator returned50 of an estimated144,
punch50/91, and penn50/157. Each explicitly reports more results available.
The other twenty response sets say NO_MORE_RESULTS for their particular
queries, not for the archive as a whole. The date query supplies zero results
and omits the results member. No new pagination was attempted.

Eight appearances, each a different document ID, omit folder_name:
165940,165962,166093,166099,166345,166386,166426,166435. Their supplied titles
were searched, but their missing folder fields cannot be called nonmatches.
No sentinel was inserted. Across repeated IDs, supplied properties agree;
there are no within-response duplicate document IDs. The zero sheet-token
finding therefore describes only fields actually supplied. These selected
responses are not an inventory of all municipal documents or all held PDFs.

The catalog is a held transcription of City physical labels, with earlier
provenance in the [folder lookup](../municipal-originals-2026-10-04/folder-document-locator/report.md).
It is not another independent historical witness. The raw saved service
responses supply document-level metadata, not verified historical drawing
dates; mes:date was not used as a drawing date.

## Verification and claim strength

The [read-only query](lookup.py) implements the declared fields and preserves
missingness, appearances, unique IDs and coverage. Sixteen synthetic tests
passed before execution. Pre-result critical review caught a substring
boundary issue: S-1 inside a compound identifier must not be called an exact
standalone sheet match. The protocol explicitly retained such tokens only as
leads before the run, with synthetic examples; there were no actual sheet
matches. Root replayed the complete result and rechecked all24 source pins.
Execution receipts and version pins are in [verification](verification.md).

The [independent extraction](independent-review.md) froze before reading the
root implementation/result. Root replayed that independent command: all 44
final tests passed, and its saved complete matches, controls and context joins
reproduced. Cross-comparison agrees on all 24 pins, 38 matched catalog rows,
11 matched response appearances, exact match spans and selected properties,
23 coverage rows, 208 IDs, missingness count and absence of property conflicts.
An initial independent synthetic compound-token expectation failed; the
corrected expectation and later added accounting check remain documented.

The separate [method review](method-review.md) reran the 16-test suite and
added mocked integration checks for repeated IDs, duplicate results, malformed
catalog rows and invalid field types. It found no material correction needed
for this fixed dataset. Its reuse caveat remains: if supplied properties
disagree in a future run, a first-occurrence summary cannot resolve that
conflict. No such conflict occurs here. Independent computation is not a new
archive, source-content review, historical authentication or human acceptance.

The bounded match/count observations are directly established by the saved
metadata and reproducible query. Applicability of any context lead to the
October S-S-1 remains underdetermined. Archive-wide absence or concealment is
unsupported, and the known packet nonmatch actively weakens that inference.
No alteration-to-model join, installed-condition finding or cause-ranking
change follows.

## Next discriminating step

The next useful step is a separately declared, finite public document-search
test using S-S-1, SKS-S-2 and S-1 with first-floor context, plus the known
166828 packet as a retrieval control. Preserve exact request syntax, counts,
caps, missing fields and nonmatches; do not assume literal full-text semantics
or calibrated OCR recall. This is a proposed metadata retrieval, not an
automatic PDF acquisition or permission to reopen the exhausted image review.
Any returned candidate needs its own sheet/date/revision/member-key admission
before it can resolve the beam mapping. CO23 seventh-floor and CO40 backup
questions remain separate.

The existing SFB-005 feedback fixture already covers a known original hidden
by a generic catalog label and the prohibition on turning nonmatches into
absence. This unit reproduces that workflow limitation, not a new inspected
Sherlock defect. Feedback routing remains locally pending under the archived
destination boundary. Main/legal and source records remain unchanged; no fee,
outreach, engine action, transfer, promotion, staging, commit or push occurred.
The full investigation remains active and incomplete.
