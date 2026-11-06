# United's Flight 93 relay and message timing

November 6, 2026 UTC · TEL02–TEL04 / AUD016-A1

United’s written hearing statement labels the San Francisco maintenance message to Flight 93 **9:47 a.m. Eastern**. The Commission staff report labels it **9:46 A.M.** Both accounts are preserved beside the two numeric fields documented in the earlier ACARS review. The same staff report identifies a specific United explanation for the lack of call-by-call details on a maintenance-to-headquarters tie-line. [United hearing statement](https://govinfo.library.unt.edu/911/hearings/hearing7/witness_studdert.htm#:~:text=At%209%3A47) · [Commission staff report, pp. 43 and 91](https://www.archives.gov/files/research/9-11/staff-report-sept2005.pdf#page=43) · [Earlier printout review](https://github.com/AveLyra/911-conspiracy-investigation/blob/dea827163a66c9054cf731d3eff98109743a6750/investigation/broader-evidence/telephone-ua93-acars-relay-2026-11-06/README.md)

| Record | Observation and scope |
| --- | --- |
| United written statement, January 27, 2004, web lines 27, 39 and 44, local HTML stripped strings 52 and 57 | Gives **9:35** for maintenance receiving the attendant’s call and describes a quick relay to Chicago, with no minute assigned to Chicago receipt. Gives **9:47** for the San Francisco ACARS message and renders it as “Heard of incident, is all normal?.” It reports that Flight 93 did not respond. The statement supplies neither a delivery receipt nor a call log. [United statement](https://govinfo.library.unt.edu/911/hearings/hearing7/witness_studdert.htm#:~:text=At%209%3A47) |
| Commission staff report, PDF and printed p. 43, extracted lines 35–45 | Gives **9:46 A.M.** for the message, rendered as “Heard report of incident. Plz confirm all is normal.” Separately gives **9:45 A.M. and 9:50 A.M.** as the bounds for the operations manager receiving a maintenance report. [Staff chronology](https://www.archives.gov/files/research/9-11/staff-report-sept2005.pdf#page=43) |
| United ACARS printout, Team 7 Box 13, member 787, PDF p. 37 | Gives `111346/PRI` in the sender line and `09111347 108575 0647` in the record line. Under the previously documented UTC assumption, the nominal minute labels correspond to **9:46** and **9:47** EDT. Field semantics and actual transmission, receipt and acknowledgment remain open. [Prior scan, source pins and clock check](https://github.com/AveLyra/911-conspiracy-investigation/blob/dea827163a66c9054cf731d3eff98109743a6750/investigation/broader-evidence/telephone-ua93-acars-relay-2026-11-06/README.md) |

The two public accounts align with different minute labels in the printout under that assumption. A difference in the field each account used is an **untested explanation**. No worksheet ties either account to a particular field, and both minutes fall within the staff report's range for the separate telephone relay. A reported lack of reply leaves the message’s delivery status open.

## Which records could time the relay?

On printed p. 91, note 179, Commission staff say they sought to time the **Flight 175** maintenance-to-headquarters relay. The note attributes to United the absence of audio recording at the maintenance center, usage billing for the tie-line calls and call-by-call detail for that tie-line. It names United’s *Explanation of SAMC Phone Records for Calls to United WHQ*, dated **July 16, 2004** in the citation. United’s hearing statement describes the San Francisco-to-Chicago relay for both flights. Whether the two specific calls used the same line requires a circuit or routing record. The reported tie-line limitation does not determine what was recorded by the separate aircraft-to-maintenance carrier or by the receiving operations center in its operational logs. [Staff report, note 179](https://www.archives.gov/files/research/9-11/staff-report-sept2005.pdf#page=91) · [United statement, both relays](https://govinfo.library.unt.edu/911/hearings/hearing7/witness_studdert.htm)

The public National Archives finding aid lists **UAL QFR responses** and **United AL 9/11 ACARS** together under Team 7 Box 18. A targeted archive check located a title match for the July 16 citation and a separate ACARS compilation. These are acquisition leads. The scan packets are held locally pending confirmation of release and reuse status. This note relies on the published hearing, published staff report, public finding aid and earlier unmarked printout review. [Finding aid, Box 18](https://www.archives.gov/files/research/9-11/finding-aid.pdf#page=109)

## TODOs

- [ ] Obtain an officially cleared copy of the United explanation and its transmittal. Check the cited date, any enclosures and whether it identifies the Flight 93 relay’s routing. Check the separate ACARS compilation under the same handling constraint.
- [ ] Look for the receiving operations-center log or dispatch desk notes, crisis-center intake, any separate switch evidence and the dated source notes behind note 367. To identify the actual receipt time, match the aircraft and sender to a timed receiving-side entry.
- [ ] Obtain the native ACARS schema, ground event log and matching network or aircraft receipt record. Test whether the minute fields represent distinct processing events and preserve the reported lack of a reply separately.
- [ ] Keep the aircraft-to-maintenance carrier, queue and transfer records on the separate acquisition list. The tie-line account addresses a ground-to-ground leg.

[Source hashes and verification scope](SOURCE-PINS.json)
