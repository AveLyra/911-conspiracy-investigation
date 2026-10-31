# FBI-hosted operator interview: speech, open connections and indirect contacts

October 31, 2026. **An official FBI-hosted release now supplies a primary interview report with GTE operator Lisa Jefferson.** It distinguishes a reported direct passenger conversation, a silent but open connection and a later Verizon-mediated contact she could not hear directly. Those distinctions matter when testing what a call duration, connection endpoint or witness time actually describes.

This is a new agency-hosted source acquisition in this work, not a claim that the historical account was previously unknown or independently confirmed. It is **not** the missing September 20 American Airlines Airphone Usage analysis, Keyton's interview, a raw network export or an authenticated source-to-exhibit worksheet. Those targets remain open.

## Source and actual coverage

The ordinary FBI Vault search for Airphone returned five titles. The [September 2001 interviews, part 08 of 08 item](https://vault.fbi.gov/9-11%20Commission%20Report/9-11-interviews-2001-09-sep-08-of-08/view) exposed [this actual PDF](https://vault.fbi.gov/9-11%20Commission%20Report/9-11-interviews-2001-09-sep-08-of-08/at_download/file): **21 pages, 1,985,063 bytes**, SHA-256 **`a7d3d872daf33d41c993ade5ccf2e9aa5421ffb1f4cda6164d6bb712372dde41`**. The exact-title follow-up displayed zero items; that bounded index observation does not establish that the usage analysis is absent from FBI holdings or releases. Other returned September parts 01/02 remain unexamined candidate routes.

We extracted ordinary text on 21 pages only for navigation and visually read complete physical pages 3–5. **Pages 4–5 are the selected Jefferson record**; page 3 is another report's continuation and was not attributed to her. The other 18 pages were not visually read. Source identity, rendering and scope are in `SOURCES.json` and `READING-SCOPE.json`; page/paragraph pins are in `OBSERVATION-PINS.json`.

Page 4 gives a September 11, 2001 visible date and identifies her role as **GTE Airphone**; page 5 supplies the continuation name/date/page 2. The visible case field is **265D-NY-280350**. These are this record's fields, not the different M-INT/265A identifier sought for the September 20 analysis. A visible unclassified-information stamp is dated 12-14-2006; that stamp is not treated as the interview or release date. Official hosting supports the retrieved release's provenance; it does not independently verify its historical assertions or supply native interview audio.

## What the report distinguishes

| Phase | Source account and exact location | What remains unknown |
| --- | --- | --- |
| Reported direct conversation | [Page 4](https://vault.fbi.gov/9-11%20Commission%20Report/9-11-interviews-2001-09-sep-08-of-08/at_download/file#page=4), body paragraphs 2–5: a caller identified himself as Todd Beamer; Jefferson reports speaking with him and hearing changing cabin activity. | Voice/caller identity, actual network event, precise aircraft-event sequence and clock are not independently authenticated here. |
| Silence while connected | [Page 5](https://vault.fbi.gov/9-11%20Commission%20Report/9-11-interviews-2001-09-sep-08-of-08/at_download/file#page=5), first paragraph: after the last reported exchange, she heard nothing and kept the connection open for another 20 minutes before disconnecting. | An open connection is not automatically continuing passenger speech. Its native switch/session/leg and duration definitions are missing. |
| Later provider-mediated contact | Page 5, second paragraph: a Verizon Quality Control contact relayed information from relatives reportedly speaking with another passenger. Jefferson says she could not hear that passenger and received information second hand. | Exact routing, simultaneous legs, caller identity and which connection ended at the reported endpoint are unverified. No redacted identity or LNU surname is reconstructed. |
| Equipment indication | Page 5, end of first paragraph: tracking equipment reportedly indicated a Pittsburgh transceiver/service area. | Actual equipment logs, field definitions, service-area bounds and clock were not acquired. This is not a pinpoint aircraft location or validated flight path. |

These are statements recorded in one FBI interview report, not raw audio, switching evidence or separate independent witnesses. The firsthand/secondhand distinction is explicit in the source and must survive later summaries. Neither the silence nor the continuing provider conversation alone establishes the aircraft's physical condition or a time of passenger speech.

## Preserve the time fields and conditional arithmetic

The report gives an initial **approximately 8:45 a.m. Central** call, **seven minutes** before a described change, **another eight minutes**, and a last exchange around **9:00 a.m. Central**. It then gives **another 20 minutes** open, a callback **approximately five minutes later**, a separate **9:30 a.m. Central** callback estimate and an **approximately 9:43 a.m.** conversation/connection endpoint. The last label's clock basis is read in its paragraph context, not independently calibrated.

Two nominal calculations can be reproduced from those printed values: **8:45+7+8→9:00**, while **9:00+20+5→9:25**, beside the separately estimated **9:30** callback. `TIMING-ARITHMETIC.json` retains the inputs and conditional five-minute difference. This is not an independently measured gap: the source uses estimates and supplies no uncertainty bounds. We preserve both accounts without selecting a corrected time, assigning a cause or converting them into synchronized aircraft/network timestamps. No timezone conversion, crash-time comparison or offset fit was performed.

The next useful evidence is the operator/session and Verizon transfer record, its clock basis and the interview's underlying notes/audio. Those could show whether the statements concern different legs or different events, an estimated chronology or another explanation. None is established here.

## Effect on the existing telephone investigation

This advances **TEL02/TEL04** only through an agency-hosted primary operator record and a clearer source-specific retrieval target. It does not resolve the AA77 connected/unconnected descriptions, 154/159-second values, eight-call/seven-row presentation or the 35-of-37 reconstruction. GTE terminology cannot define AT&T/Claircom records automatically. The already reviewed GTE tables also contain repeated timestamps and uncertain operator-field readings; a name, similar minute or estimated duration does not create a unique row/leg match. Existing table and decoder checks were not rerun.

The source is relevant contrary evidence to flattening every connection interval into a continuing passenger conversation. Equally, it does not prove that a particular carrier row represents the silent interval or resolve the later endpoint. Native records are needed to distinguish those possibilities. No fabrication, deliberate alteration, suppression or historical cause is established by these interview estimates.

All earlier records and conflicting values remain unchanged. `OPEN-TODOS.json` retains the original 18 requirements and previous dependencies, adding the operator/Verizon/transceiver and actual report/version targets. FAA corrected-QFR/receipt and signed disposition, native recorder/calibration/clock, materials specimen/run/measurement and steel preservation/inventory/attribution/delivery gaps remain open or partial. No original requirement closes from this acquisition.

The original PDF, separate page rasters and raw extraction remain in the verified native store. Public notes exclude raw documents/images, financial/contact/home/work information, signatures, redacted identities and private case material. `VERIFICATION.json` separates source integrity/conditional arithmetic from historical validation; `CHECKLIST.md` records outcomes; `TEXT-CHANGES.diff` preserves actual new-document additions. `EDITORIAL-REVISION.diff` retains the first draft while qualifying the form-date/stamp wording and improving spacing; no source value changes. No outreach, fee, request, filing, mailbox/private correspondence, deletion, source overwrite, private push, merge or public-history rewrite occurred. Publication and goal completion remain separate milestones.
