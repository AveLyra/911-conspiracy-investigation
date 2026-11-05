# Sample 03825B and Fresh Kills screening-station records

Public research copy. [Source URLs, exact locators and SHA-256](SOURCE-PINS.json).

November 5, 2026. STL01–STL02 follow-up to the [screening and load-record review](https://github.com/AveLyra/911-conspiracy-investigation/blob/699ac9c0a038b6bd4ed0515ac2898f2676af8712/investigation/broader-evidence/steel-fresh-kills-screening-and-load-records-2026-11-05/README.md). This comparison follows public monitoring records to concrete location and sample identifiers that can be tested against steel routing records.

## Unresolved collection date and location

Both contractor reports were prepared for EPA under contract **68-W-01-010**, bear **Special Investigative Audit #14**, and carry sample ID **03825B**. The earlier City-held copy is labeled **2nd Draft** and dated **November 20, 2001**. EPA's later copy is labeled **Final Update** and dated **October 23, 2003**. [Draft cover](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000130438.pdf#page=1) · [Final-update cover](https://nepis.epa.gov/Exe/ZyPDF.cgi?Dockey=9100KDEY.PDF#page=1)

| Record | Collection date as displayed | Location as displayed | Result as displayed |
| --- | --- | --- | --- |
| 2001 draft narrative, PDF p. 22, printed p. 20, Bates 000130459, lines 26–31 | `October 10th` | `Bulk Steel Pile`, described in the `Disposal Zone` paragraph | `2.7% Chrysotile` |
| 2003 final update, Appendix I, PDF p. 580, printed I-11, line 18 | `11-Oct-01` | `DISPOSAL ZONE` | `DETECTED`, `2.68` `%`, `CHRYSOTILE` |

[2001 draft narrative](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000130438.pdf#page=22) · [2003 final row and neighboring rows](https://nepis.epa.gov/Exe/ZyPDF.cgi?Dockey=9100KDEY.PDF#page=580)

**Comparison.** The displayed dates differ by one calendar day. Rounding 2.68% to one decimal gives 2.7%. That numerical check leaves the two reported values, collection dates and location descriptions in place. The final table uses `LF - BULK STEEL PILE (NE)` for other IDs on the same page. No entry assigning that more specific label to **03825B** was verified. Table 9 in the draft covers the Work Zone and other Lower Manhattan locations and does not list 03825B on its two displayed pages. The final appendix is a later report from the same audit series and does not independently corroborate collection. [Draft Table 9, pp. 31–32](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000130438.pdf#page=31) · [Final Appendix I, p. 580](https://nepis.epa.gov/Exe/ZyPDF.cgi?Dockey=9100KDEY.PDF#page=580)

## Separate Fresh Kills air-station records

- The draft reports **17 of 1,243** Fresh Kills TEM samples above **70 S/mm²**. It reports a range of **88–128 S/mm²** for the highest results, identifying **Screening Operations (Locations 09-A & 09-B)** and **Location 12-A** between **October 8 and October 31**. These are monitoring locations and an aggregate date window. [Draft p. 21, printed p. 19, lines 11–18](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000130438.pdf#page=21)
- The October 20 EPA situation report, enclosed in an October 23 DEP daily report, lists **2 of 19** for **Oct 17, 0700–1900 hrs**. The locations given are **Sift Location #9C** at **97.78 S/mm²** and **Barge Location #14** at **80 S/mm²**. [Situation report, PDF p. 3, lines 51–55](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000154488.pdf#page=3)
- Its next page lists **3 of 19** for **Oct 17, 1830–Oct 18, 0630 hrs**, at **Sift Location #9B**, **indoor Wash Location #11**, and **indoor Wash Location #12**, each **96.24 S/mm²**. The two reported windows overlap by **30 minutes**. Their sample counts stay separate because the summary does not identify individual filters or rule out duplication. The audit's `09-B` and the situation report's `#9B`, and the audit's `12-A` and the situation report's `#12`, remain distinct labels pending a station crosswalk. These ambient-air measurements are separate from the bulk-dust sample. [Situation report, PDF p. 4, lines 8–11](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000154488.pdf#page=4)

## What remains open

- [ ] **03825B:** Find the field collection sheet, lab accession and custody record, NYC Response database row and revision history. Compare collection and accession dates, exact site and sample type, and the original result. The sample is listed under bulk dust. Its location label alone supplies no steel item, load, building attribution, or chain to an engineering specimen.
- [ ] **Station crosswalk:** Find October Fresh Kills monitoring site maps and station histories, original shift sheets and filter IDs for the two windows. Test the station-label joins and whether any filters appear in both summaries. Compare those location/time fields with screening shifts and separately dated load and outbound records.
- [ ] **Steel custody:** Obtain site/yard logs and piece or load identifiers before making a routing or building-origin claim. The documents reviewed here provide no record of the screening or re-sifting of a specific load and do not determine what happened to any individual steel piece.

**Method.** Retrieved two City release PDFs and the EPA archive PDF. Preserved the acquisition receipts and direct-source bytes locally. The City audit transfer timed out after 41,647,611 bytes. The server returned the remaining 11,960,720 bytes as HTTP 206 with matching weak ETag and Last-Modified and a contiguous Content-Range. The assembled 53,608,331 bytes opened as 78 pages without PDF repair. The pinned digest identifies that assembly. Inspected the cited prose, Table 9 and final Appendix I row. Line locators use PyMuPDF 1.27.2.2 sorted embedded text, one-based with blank lines counted. Read dates, station codes, values and the final row against their scans. Scope was a targeted provenance and record-locator comparison, with no sample retest or complete audit of the other tables.
