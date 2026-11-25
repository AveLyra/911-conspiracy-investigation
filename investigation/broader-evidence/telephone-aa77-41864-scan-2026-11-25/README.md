# September 20 Airphone analysis: released packet scan checked

AUD016 / TEL01–TEL04. November 25, 2026. The [earlier review](../telephone-usage-report-2026-10-27/README.md) examined a public reader's rendering of this FBI analysis, while the underlying agency-native source and complete production chain remained unverified. This supplement examines a separately retained Commission-packet PDF scan; it is not a newly discovered analysis or a native carrier record.

## Observations

Team 7 Box 19 physical pages **43–44** visibly reproduce the two report pages headed “American Airlines Airphone Usage.” The first carries identifiers `M-INT-00158680` and `265A-NY-280350-IN-41864` and an analysis date of September 20, 2001. The report describes charts for American Flights 11 and 77, says times are Eastern, and expressly excludes personal cell-phone calls and cell-site handoff phases. Those are the analyst's scope statements; they do not establish that every other call was impossible.

The Flight 77 list includes a minute-labeled **9:18 a.m.** entry. The report's results text says another caller dialed zero and was subsequently connected to the Solicitor General's office. The [earlier source comparison](../telephone-usage-report-2026-10-27/README.md) separately preserves the later court presentation's **09:18:58 unconnected** label. The early results sentence does not supply an event ID or establish which table row it describes. No exact row-to-call join, consistent leg definition, carrier clock, or reason for different descriptions has been established. Do not treat these reproductions as independent carrier measurements or infer that a particular conversation did or did not occur.

The scan includes private financial and contact details; none is reproduced here. No obscured data were reconstructed.

## Provenance and test limits

The previously acquired [Commission archive ZIP](https://archive.org/download/911datasets/NARA_9-11_Commission_Records_Released_Jan_14_2009.zip) member `NARA_9-11_Commission_Records_Released_Jan_14_2009/911 NARA/Team 7 Files/Team 7 Box 19/T7 B19 Key 302s Fdr- Entire Contents- FBI 302s.pdf` is 52 pages, SHA-256 `01daa2ea6683aacbbb7918086fb8328e7803810087cc3160a352377be056dc4e`, acquired and rehashed November 25, 2026. Only physical pages 43–44 were rendered at 1.7× with PyMuPDF and visually examined in this step. The scan is a Commission working-file reproduction, not an authenticated native FBI production or source billing file. This check confirms visible scope and wording; it does not validate the events historically or the completeness of the agency's underlying production.

TODO: obtain the original analyst inputs and attachments, carrier/operator switch and billing records, definitions for attempt/connection/leg and clock handling, and source-to-exhibit mapping. Preserve the earlier reader capture, minute labels and court presentation unchanged. Checklist: [x] inspect both scan pages and verify source hash; [x] retain conflicting source descriptions; [ ] recover carrier records and prove or disprove the proposed event join.
