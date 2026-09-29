# Longer-footage search: catalog candidate and a verified records lead

September20,2026 UTC / September19 local. Working research; full investigation
and Luna follow-through active and incomplete. This follows the failed proposed
14→15 source join, not a new determination of collapse cause.

## What changed

**NIST's June2004 progress report describes a specific tape/clip database that
could resolve the missing source relationships.** The actual pages—not merely
a search snippet—identify VideoList tape/copy records, derivation fields,
clip-break records and reference-based timing. The corresponding populated
records have not been acquired. This is a better-defined record lead, not a
finding that those records are withheld or still retained.

A bounded official-catalog traversal also located **CBS-VMS-Wtc7.wmv**, but
only its metadata has been read. It is under **Other Photos and Videos**, not
Original Video from Tapes. Neither its title nor its8,717,690byte size proves
that it contains the target fire view, a longer version, or an original camera
recording. No new video was acquired, played or measured in this unit.

## Catalog coverage and limits

Six immediate listings returned282 distinct IDs:39 folders,2 text files,
239 MP4s and2 WMVs. The General Investigation Collection supplied the239
MP4 entries with numbered WTCI-style titles; none of those returned titles
matches CBS/Dub5/42A0122/G25D33. That is a name-search result, not evidence
that the sought footage is absent. Thirty-five returned folders remain
unlisted. All list requests used top_k1000; normalized responses contain no
pagination/completeness indicator or populated parent_ids. Do not turn a
below-limit response into a demonstrated exhaustive inventory.

The exact route and every request/response are preserved under sources/ and
independently reconstructed in [independent-provenance](independent-provenance.md).
NIST's official page identifies the category folder IDs. Those IDs were queried
on Drive; no new HTTP redirect between the NIST proxy and Drive was captured.
Each followed descendant URL was returned in its parent listing.

Candidate: ID `1Iiw99TkBywBLRXvHAekU1Y0DKV85sFBo`, `video/x-ms-wmv`,
8,717,690bytes, [current catalog item](https://drive.google.com/file/d/1Iiw99TkBywBLRXvHAekU1Y0DKV85sFBo/view?usp=drivesdk).
Path: Other → PhotosAndVideoFromCDorDVD → Video → WTCI-134-I WTC7 Analysis
Videos. Eight identity fields agree between its listing and refreshed metadata;
no source-byte hash/checksum or content identity has been verified. The sibling
Dimentri-wtc7vid.WMV is a separately listed item, not an established duplicate.

The root ReadMe is a generic archive notice, not a source crosswalk. The NIST
landing page also explicitly allows copies in more than one category and
cautions about embedded metadata accuracy. Repository category, filename,
encoded clock and historical camera provenance remain different things.

## Primary document: what is actually specified

Acquired [NIST SP1000-5, volume4, June2004](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication1000-5v4.pdf),
18,342,113bytes, SHA-256
`19281ca238382466a4a0029784d4789fb78cf4d8e4785ac49370c01f9aa94433`.
This is an interim progress report, not NCSTAR's final WTC7 report or a current
database export. PDF metadata describes a later digitized edition; that is
distinct from the June2004 report date. Root visually checked12 complete pages;
whole-document text searches do not amount to reading every page's images.

| Printed / PDF locator | Published description or visible example | Specific evidentiary use and limit |
|---|---|---|
| H-3 /145 | Collection includes CBS material and broadcast airchecks/outtakes | Confirms a general source category, not CBS-Net Dub5 identity |
| H-4 /146; FigureH-1, H-5 /147 | VideoList logs incoming videos/copies; example fields include Tape ID, Tape name, Source, Derived from, Copy, Format and timecode-related flags | Seek populated tape/copy/derivation rows; do not equate a numeric Tape ID with a WTCI filename |
| H-4 /146 | Clipping follows natural breaks/camera changes; longer continuous recordings can also be divided because of the then-system's1GB AVI limit | Supports more than one ordinary reason for file boundaries; does not explain these exact CBS endpoints |
| H-8 /150 | Only selected collected material enters the catalogs; camera clocks can be inaccurate | No title/tag hit is not a source-exhaustion finding; published general timing confidence is not clip-specific validation |
| TableH-2, H-9–H-11 /151–153 | Video asset path/name/category, beginning/end time, duration, uncertainty, view, content and timing notes | Identifies record fields relevant to source/clock verification, not values proven correct or populated for these clips |
| FigureH-5, H-14 /156 | Tape identity, DV in/out, actual in/out, row selection and reference-time calculation | Seek actual reference event, clip-file rows and replay exclusions. Broadcast timing method is conditional on real-time recording and excludes replays |

The2004 video table defines **Fireball** specifically as the initial plane-strike
fireball; **Flames Visible** and **Major Fire Change** are separate categories.
Searching a tag without its definition could miss a later flame event. Do not
assume these2004 definitions are unchanged in today's public interface, or
that any tag was correctly assigned to the target clip.

No CBS-Net Dub5→WTCI mapping was established in the reviewed pages or text
searches. The screenshot examples are not a complete tape inventory. Text
extraction misses some visible form fields and concatenates words; it cannot
support a blanket assertion that the PDF lacks a record or label everywhere.
The [root observations](root-pdf-observations.md) and
[linked-table follow-up](root-pdf-followup.md) preserve actual coverage and
distinguish the photographic and video tables.
The [separate12-page review](pdf-schema-review.md) agrees on these boundaries;
both root records were saved before its substantive findings were received.

## Claim assessment

- **Directly established:** exact current catalog identities and the fields/
  workflow described in the pinned2004 publication; two different source roles.
- **Reasonable inference:** populated VideoList/Cumulus records and clip-file
  timing/break notes would be more informative than filenames for testing the
  missing relationships. Their existence in today's custody is unverified.
- **Unresolved:** whether the candidate contains the target view; which tape
  produced Dub5 14/15; exact stills, elapsed gap, event clock and fire duration.
- **Unsupported by this work:** camera-master authentication, NIST exaggeration,
  intentional editing/concealment, withholding of these specific records or a
  change in comparative collapse-cause ranking.

Strongest alternative: the acquired excerpts and new candidate may be different
editions/views or selections of ordinary rebroadcast material. Even an accurate
database description cannot authenticate their individual lineage. A content
mismatch would defeat the candidate; a populated row linked to exact bytes and
a verified continuous source would strengthen the join. No probabilities are
assigned, and an unresolved comparison does not mean equal odds.

## Search scope, review and next step

[The separate public search](crosswalk-search.md) used four queries and eight
primary URL attempts, including three browser-size failures, without locating
an item mapping. One such failure was resolved by the separately declared
direct PDF acquisition. The other oversized reports remain uninspected through
that route; no general source unavailability claim follows. Six of the original
eight allowed folder listings were used. Scope additions were declared before
each new branch/document read; unused allowance is not evidence of exhaustion.

The independent catalog audit checked all nine request/response pairs, all282
rows and the exact path/identity joins without new retrieval. The PDF review is
a separate reading of the same primary pages, not independent historical
corroboration. The original search note's inability to read the PDF remains
preserved as earlier access history, superseded only by this later acquisition.
See [validation](validation.md) for actual commands, source pins, failures and
the distinction between numerical checks, document review and scientific approval.

**Next concrete test:** acquire only the exact small CBS-VMS candidate under a
declared source/diagnostic plan, then determine whether it contains the same
scene before investing in timing or thermal analysis. In parallel or if it
fails, pursue the literal Release25 /42A0122 - G25D33 locator through a bounded
public release inventory, not by selecting arbitrary WTCI numbers. A source
database export remains a precisely defined separate lead; this note does not
authorize a new request, outreach or legal drafting.

No source originals, canonical facts, legal filings, accepted Sherlock/Faraday
state or causal synthesis changed. Feedback remains locally queued under the
existing archived-task routing limit. Nothing committed or pushed.
