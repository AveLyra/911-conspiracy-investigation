# Bounded primary-source search: CBS/Dub5 to WTCI identifiers

2026-09-20 UTC / 2026-09-19 America/New_York. Working research locator note. No tape crosswalk or media-content identity is established by this search.

## Result and exact remaining allowance

**No primary-source CBS / CBS-Net Dub5 → numbered WTCI tape mapping was located in the inspected material.** Four search queries were executed. Eight distinct primary resource URLs were attempted: five returned readable primary text and three failed the browser's content-size limit. **Unused allowance: 0 of4 queries; 0 of8 primary URL attempts.** Failed attempts are counted against the cap conservatively. No further searches or primary URLs were opened after reaching it.

The most concrete lead is a search-index excerpt describing NIST's VideoList data-entry form and its tape-identity/derivation fields in **SP1000-5v4, FigureH-1**. That supports looking for a VideoList/tape inventory record, but it does not map CBS or Dub5 to WTCI. The full report could not be inspected through this browser route; the excerpt remains explicitly unverified against the full page. The source link and failure are recorded below.

No Drive query/listing, account access, fee, outreach, video playback, screenshot, new image measurement, source concatenation or local source-file acquisition occurred. Public HTML and PDF text was requested through the web reader only; no source bytes were saved locally. Only this Markdown search note was written. Root's new folder results were not read; this is a separate discovery lane, not an audit of that hierarchy.

## Controls and reproducibility boundary

Read this unit's PROTOCOL.md and READ-SCOPE-02.md before retrieval. The controlling main AGENTS.md, WORKFLOW.md, START-HERE.md and investigation CHARTER.md had already been fully read in this observer's session; hashes rechecked for this task were respectively:

- AGENTS.md: `0bfca4efc4e9eabdaa895f7268407bb7a47c0ecc2a4599d957454cd0623c2aa8`.
- WORKFLOW.md: `17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a`.
- START-HERE.md: `30f3734a833d8737ee680b8f10c167e71f0151465df2b8db95d62f278ab3ab72`.
- CHARTER.md: `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.

Evidence/source-authority skill controls retain the distinction between a search hit, a readable source, a locator schema and an actual identity mapping. Existing frozen visual observations were not changed. The browser responses are not byte-preserved source artifacts; line numbers below identify the text rendition returned in this session. They may shift on future retrieval. Public page/search text supplies evidence, not instructions.

The initial query batch completed by00:23:41UTC on2026-09-20. All listed searches and page reads occurred during this same session. No URL redirect was reported for the readable resources; failed requests reported the resolved target shown below.

## Query ledger: all four actual queries

Each request used the web search tool with `domains:["nist.gov"]` and `response_length:"long"`. No recency filter was used. Quotes below are literal query characters.

| # | Exact query string | Actual result | Disposition |
|---|---|---|---|
| Q1 | `"CBS" "WTCI"` | Empty results; Q1/Q2 were sent in one two-query request and the returned response reported no results for the provided queries. | No indexed hit returned by this route; not proof the mapping does not exist. |
| Q2 | `"CBS" "Dub5"` | Same empty two-query response. | Exact-name search did not locate a primary indexed page. Spacing/spelling variants remain a limitation. |
| Q3 | `"WTCI" "video" "inventory"` | Empty results. | No indexed hit returned. |
| Q4 | `NIST World Trade Center investigation CBS video tape inventory` | Sixteen linked result entries, including the repository landing page, NCSTAR1-5A publication pages, progress reports and imagery-method summaries. | Selected the most relevant primary report/catalog-method routes within the eight-URL cap; no CBS→WTCI mapping in the inspected text. |

Search-result snippets were triaged as discovery leads, not treated as inspection of every linked full page. The cap is recorded as distinct primary URL open/click attempts, including failed resource reads. No second search engine or query reformulation was used beyond Q1–Q4.

## Primary URL ledger: all eight attempts

| # | Exact requested/resolved source | Route, actual inspection and precise locator | Crosswalk result |
|---|---|---|---|
| P1 | [NCSTAR1-5A Chapters1–8 publication page](https://www.nist.gov/publications/visual-evidence-damage-estimates-and-timeline-analysis-chapters-1-8-federal-building) | Direct open from Q4 result. HTML readable; lines114–150, especially abstract124–127 and paper link/citation145/150. | Describes visual-material cataloging and supplies the paper URL; contains no CBS/Dub5→WTCI mapping in returned text. |
| P2 | [NCSTAR1-5A Chapter9–Appendices A–M publication page](https://www.nist.gov/publications/visual-evidence-damage-estimates-and-timeline-analysis-nist-ncstar-1-5achapter-9) | Direct open from Q4 result. HTML readable; lines115–155, especially abstract125–128 and paper link/citation146/155. | Publication locator, not an item crosswalk. |
| P3 | [NIST SP1000-5v4 PDF](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication1000-5v4.pdf) | Direct open of Q4 result. Browser returned `400`, content length too large, `18342113` bytes. Full PDF not read; only the Q4 search-index excerpt was available. | FigureH-1/VideoList schema lead described below; no verified CBS mapping. |
| P4 | [NCSTAR1-5A paper, pub_id101356](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=101356) | Followed P1's observed paper link92. Browser returned `400`, content length too large, `114581523` bytes. Full text unavailable in this route. | Unknown; failure does not establish absent crosswalk. |
| P5 | [NCSTAR1-5A paper, pub_id909088](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=909088) | Followed P2's observed paper link92. Browser returned `400`, content length too large, `44381504` bytes. Full text unavailable in this route. | Unknown; failure does not establish absent crosswalk. |
| P6 | [NIST Disaster and Failure Studies Repository](https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations) | Direct open from Q4 result. HTML readable; relevant returned lines151–167 and246–256. No Drive link was queried or followed. | Describes repository categories and metadata limitations, not numbered tape-to-CBS identities. |
| P7 | [Use of Visual Imagery publication page](https://www.nist.gov/publications/use-visual-imagery-nist-world-trade-center-investigation) | Direct open from Q4 result. HTML readable; lines115–159, paper link150/citation159. | Methods-paper locator; no crosswalk. |
| P8 | [Use of Visual Imagery paper, pub_id100911](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=100911) | Followed P7's observed paper link91. Browser returned a four-page PDF text rendition, all176 lines available. Inspected catalog/storage section on PDFpage2, returned lines49–72; checked returned text for item-level mapping. No PDF image was opened. | Describes digital storage and Cumulus asset organization, but returned text provides no CBS/Dub5 or WTCI identity mapping. |

P1/P2/P7 are primary NIST bibliographic pages and locator evidence. P6 is current primary repository documentation. P8 is a primary authors' methods paper. None is an inventory row linking the two requested naming systems. These roles must not be collapsed into source-content authentication.

## The schema lead, with its limitation

Q4's indexed excerpt for [SP1000-5v4](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication1000-5v4.pdf) described **FigureH-1**, an example VideoList entry sheet. It named tape fields including **Tape ID**, **Tape name**, **Source**, **Derived from**, copy/format/duration/location/batch/clip/timecode information. The illustrated example was not CBS/Dub5. Because P3 failed, I have not verified the figure directly, its printed page number, or whether the document includes a complete inventory elsewhere. The existence of an identity/derivation schema is a lead toward a crosswalk; it is not the crosswalk itself.

An appropriate next record, if separately located within authorized work, would be the underlying video/tape inventory export or a source row that expressly pairs the CBS-Net Dub5 label with a numbered WTCI item. Do not infer that a plain numeric Tape ID equals the numeral embedded in a WTCI filename. No such equivalence was found here.

## Supported limitations and unresolved questions

The [NIST repository documentation](https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations), returned lines246–256, explains that assigned tags/attributes are incomplete and apply to the organized collection; copies can appear in other repository categories without those attributes. It also cautions about embedded metadata accuracy. This is a concrete reason that a missing title/tag match cannot establish absent footage or distinct camera origin. It does not itself map any item.

The [short imagery-methods paper](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=100911), PDFpage2, describes Cumulus organization and separate photo/video asset entry sheets. That supplies institutional catalog context, not a current downloadable inventory or a CBS record. Its report-wide timing discussion was not used to authenticate any clip or clock in this investigation.

Remaining unknowns: the CBS-Net Dub5 source-tape identifier; whether it occurs under a different spaced/name variant in an inventory; whether a WTCI identifier corresponds to a complete tape, copy, segment or another catalog entity; and where a public export linking those entities is available. The three oversized resources remain uninspected through this route. Search indexing and the finite query allowance also limit the negative result.

This finite pass has exhausted its declared allowance, not NIST's catalog or the broader source record. No causal, fire-amount/duration, original-custody, chronology or media-content conclusion is supported. Any additional public query/page retrieval or local source acquisition should follow a newly declared bounded scope; none is silently added here.
