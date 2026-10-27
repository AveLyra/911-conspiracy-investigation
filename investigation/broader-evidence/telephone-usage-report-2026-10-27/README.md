# September 20 Airphone report: scope, connection description and entry count

October 27, 2026. Supplement to AUD016-A1, TC05/B105 and TC06/B110 and the [preserved TEL01–TEL06 review](https://github.com/AveLyra/911-conspiracy-investigation/blob/639bd09f9f8116707df2be5fb04d87472afd58cb/investigation/broader-evidence/telephone-originals-2026-10-27/README.md). Earlier records and conflicting values remain unchanged.

**An early FBI analysis says an operator-routed caller was connected to the Solicitor General's Office. Later records label the 09:18:58 entry unconnected.** The early report does not give a switch/leg identifier or identify the caller, and its table uses minute labels. The exact event join and reasons for the different descriptions remain unverified. This is a concrete record-comparison lead, not proof of fabricated calls or concealment.

## Source and actual acquisition scope

The [normally accessible public reader](https://www.scribd.com/document/24392516/T7-B19-Key-302s-Fdr-Entire-Contents-FBI-302s) displays the September 20, 2001 **American Airlines Airphone Usage** record at reader pages **43–44**, internal report pages **1–2**. Its header identifies **M-INT-00158680** and **265A-NY-280350-IN-41864**. The reader lists a 52-page collection; only these report pages are the new substantive review here. The source appears to reproduce a released Commission/FBI record; its agency-native PDF, release cover and complete production chain were not authenticated in this unit. Earlier embed access exposed only three pages; normal public reader navigation now exposed the report. These different access scopes are preserved, not treated as a contradiction in the historical record.

We preserved local browser screenshots and the report's rendered text. These are derived capture entities, not native PDF bytes or raw carrier records. The header/scope, second-page results and table continuation were visually reviewed. The upper table was inspected at reduced scale with its DOM text; no second-resolution measurement is claimed. [Source identifiers and capture hashes](SOURCES.json) · [Exact observation locators](OBSERVATIONS.json).

Raw screenshots/text include financial identifiers and are retained locally, excluded from the public payload. Some capture filenames do not match the actual displayed page, and two initial PNG-named files contain JPEG bytes. Those are our capture/naming errors, not anomalies in the FBI record. An accidentally captured unrelated page45 is preserved locally and excluded. No download signup, paywall or access gate was bypassed.

## U01 — What the early report covers and excludes

Internal page1 describes a chart of airphone calls in Eastern time. It explicitly excludes personal cell-phone calls and hand-off phases and states that caller identities and seat numbers could not be determined. It defines NA as missing information in the flight records and gives an explicitly tentative operator explanation for the dialed digits0 and3. The table labels do not identify a human caller or provide native switching definitions.

Consequently this source cannot serve as a census of every cellular attempt, every hand-off leg or every completed conversation. Later caller identifications may use additional interviews or account information; the early uncertainty does not itself contradict later identification. To test either account we still need the particular evidence used for the later assignment.

## U02 — Preserve the connection descriptions side by side

| Record | Exact location | What it says or stores | Limits |
|---|---|---|---|
| September20,2001 FBI analysis | Reader44 / internal2 / RESULTS—FLIGHT77 | An unnamed caller dialed zero and **“was subsequently connected”** to the Solicitor General's Office. | The paragraph does not name Barbara Olson, specify a call/leg ID or supply a second-resolution start. A table entry at9:18 includes zero and a redacted destination; the narrative-to-row link is plausible, not authenticated. |
| May20,2004 Commission briefing | [Public scan, page2](https://www.scribd.com/document/18886083/T7-B12-Flight-93-Calls-General-Fdr-52004-DOJ-Briefing-on-Cell-and-Phone-Calls-From-AA-77-408) | The09:18:58 entry attributed to Barbara Olson is labeled no connection. | Staff's record of a briefing, not a switch trace or recording. This page was visually reviewed in TEL01–TEL03; no new native briefing file acquired here. |
| Court AA77.swf | [Official exhibit package](https://coop.vaed.uscourts.gov/moussaoui/flights.zip); IDs1691,1692,1694; uncompressed offsets3183776,3183822,3183950 |09:18:58; zero seconds; Department of Justice / unconnected-call label. | Static text definitions re-decoded here; no Flash execution or proof of the trial's displayed screen. No native carrier classification independently validated. |

The difference matters because the early analyst's connection description and the later no-connection label are not interchangeable. It does not establish which reflects the actual network event. Different legs, an operator connection versus an end-recipient conversation, a changed analytical classification or an error are **untested possibilities**, not resolutions. We have no instruction, edit trail or switch evidence selecting among them. No individual caller is newly identified here.

## U03 — Eight early entries provide a concrete comparison for the later count

The early Flight77 table has eight numbered entries across the two pages. Their labels, in original row order, are9:11,9:14,9:12,9:15,9:18,9:20,9:25 and9:30AM. Preserve the nonchronological row order; do not silently sort row2 after row3. The table contains minute labels, not a duration column.

The May2004 briefing's introductory text says eight calls, while its displayed table has seven rows. The court SWF separately stores a09:14:57 button-pressed/unconnected entry. These earlier TEL03 observations remain. The newly reviewed early report has an entry at9:14, giving a specific candidate to compare with that button event.

[The crosswalk](MINUTE-CROSSWALK.json) matches all eight early minute labels to eight stored court timestamps, including09:14:57. [Reproduction](verify_comparison.py) re-decodes the held official ZIP and verifies13selected text definitions/offsets and the eight candidate minute matches. [Output](COMPARISON-RESULT.json). This tests label agreement only. It does not establish the same call/leg, calibrated clocks, eight completed calls, or why one entry is absent from the briefing's seven-row table. A common underlying record can produce agreement across these derivative presentations; the match is not independent corroboration of eight real conversations.

## U04 — The five-second discrepancy remains open

The early table supplies no duration for the09:25-minute entry and cannot adjudicate the earlier **159seconds versus154seconds** conflict. The May2004 briefing and court label say159seconds; Commission final-report note57 says2minutes34seconds. See [TEL02 and exact locators](https://github.com/AveLyra/911-conspiracy-investigation/blob/639bd09f9f8116707df2be5fb04d87472afd58cb/investigation/broader-evidence/telephone-originals-2026-10-27/README.md). This unit rechecks the court159label only. It did not newly reauthenticate the Commission note or decide whether the records use the same duration definition.

## Missing originals and discriminating tests

1. The actual September20 analysis, its charts/source attachments and revision history as released by the agency, with production cover and complete page accounting. A reader rendering is useful evidence of the record's text, not full release authentication.
2. The corresponding AT&T/Claircom call-service and operator records, network/leg identifiers, start/answer/billing/disconnect semantics, clock definitions and any bridge/transfer accounting. These would test what connected and unconnected mean for the proposed9:18 match. Do not transfer meanings between event types without those definitions.
3. The record chain explaining the09:14 entry, eight-call count and seven-row table: analyst worksheets, briefing attachments and source-to-exhibit mappings. A button event may be counted differently; that remains untested.
4. Office switch/transfer records and the underlying Keyton/Voss interview notes/audio, along with the already acquired released forms. A witness describing a received call does not by itself identify a particular switch leg. Conversely, an unconnected leg label does not exclude every communication with the office.
5. Original duration fields and calculation rules for the09:25:48 entry. The public reader's early minute-only table cannot settle159versus154seconds. The separate carrier-reader observations remain provisional until native/image verification.

None of those missing inputs was obtained merely by reviewing this report. No new request, outreach, fee, private-case disclosure or personal mailbox access occurred. The broader five-track goal remains incomplete.

## Reproduce and review

Run `python3 verify_comparison.py --court-zip /path/to/court-flights.zip` with the official ZIP above. The ZIP and SWF SHA-256 values in COURT-PINS.json must match; the script fails on a changed entity. The copied static decoder is unchanged from the earlier published analysis. It never runs ActionScript.

CHECKLIST.json records outcomes and open requirements. REPORT.diff is the exact first-addition text diff; prior published/native reports are not rewritten. Source capture integrity, manual reading, computational accounting and historical interpretation are separate verification scopes. REVIEW-CHANGE.diff preserves the verifier review that removed an unchecked legacy duration constant from its output; the conflict remains documented here, outside the new test's claims. This public package contains original notes, source URLs/hashes, selected public court text and code, not raw financial/account data or full reader captures.
