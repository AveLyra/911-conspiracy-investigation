# New York Center NTAP disk copies and the AEA-2394 email

November 5, 2026. **B129 / PD07.** The FAA's public archive lists nine text files from floppy-disk item **ZNY-36**. This pass acquired all nine and compared their job-log fields with the previously acquired 52-page **AEA-2394** email and printout PDF. The disc image, exact email attachment bytes and delivery records remain open. This is the New York Center set. The separately sought Cleveland **ual93-file 7** remains unidentified. [National Archives, Box 80, ZNY-36](https://www.archives.gov/research/foia/faa-finding-aid-72-83) · [Earlier inventory and printout review](https://github.com/AveLyra/911-conspiracy-investigation/blob/b70b23fc7c261c174ee5b9c7f263c03715729b7c/investigation/broader-evidence/faa-eastern-radar-inventory-followup-2026-11-05/README.md)

## AT022 and AT027 survive as separate text exports

| Record | Observed text or fields |
| --- | --- |
| **AT022** | AEA-2394 p. 1 says **“AT022 had no data”** and shows no AT022 attachment label in the inspected page. The acquired **3,674-byte** object starts **JOB 225 / AT022 / 13.01.31** and reports **86 SYSOUT PRINT RECORDS**. It contains **COND CODE 0000**, then **FORMAT ERROR ON THE FOLLOWING CARD** and **UNDEFINED FIX**. Those diagnostics precede the listed plot card. Preserve the printed system condition, the application diagnostics and the email's description separately. A card-parsing or fix-definition problem is a candidate explanation for the reported outcome. The available text cannot establish whether the underlying radar tape lacked returns. [Email p. 1, lines 5–7](https://catalog.archives.gov/id/7597091) · [AT022 export, LF lines 3, 10, 60 and 83–86](https://catalog.archives.gov/id/7597009) |
| **AT027** | The email names AT027 in the sequence and displays **at027.txt**. The PDF's extractable job-start census has no AT027 entry. The acquired **16,351-byte** object starts **JOB 266 / AT027 / 16.30.46** and reports **278 SYSOUT PRINT RECORDS**. It includes a **PLOT** request, an **NTAP PLOT** section, an **LST3** plot-symbol list and the later message **NO DATA STORED FOR THIS INTERVAL**. Preserve the output sections and terminal message together. Their scope and the identity of the original attachment remain open. [Email p. 1, lines 8–18](https://catalog.archives.gov/id/7597091) · [AT027 export, LF lines 3, 10, 84, 105, 243 and 276](https://catalog.archives.gov/id/7597014) |

The earlier counts remain attributable to their original layers. The email reports **nine files**, displays **eight attachment labels**, and gives a **seven-label** east-to-west sequence. The public disk listing yields **nine distinct text-export bodies**, including AT022 and AT027. The scan yields **seven extractable job-start headers**. A disk copy, an icon printed on an email scan and the actual delivered email attachment are separate records. [Email and printouts](https://catalog.archives.gov/id/7597091) · [Disk listing](https://www.archives.gov/research/foia/faa-finding-aid-72-83)

## Seven printout-to-text counterparts

For each job-start line extractable from the scanned output pages, the scan and catalog text file agree on the **AT identifier**, **job number**, **start field**, and **SYSOUT print-record count**. The check searched all 52 pages and normalized only the whitespace around the extracted identifiers. It compares the generated job identifiers and header fields. No page-by-page equality, received attachment identity or data interpretation follows. [AEA-2394 PDF](https://catalog.archives.gov/id/7597091) · [Exact page and line pairs, text-object locators and hashes](SOURCE-PINS.json)

| AT identifier | PDF physical page | Job number | Start field | SYSOUT print records |
| --- | ---: | ---: | --- | ---: |
| AT029 | 2 | 272 | 16.51.11 | 251 |
| AT023 | 8 | 229 | 13.09.18 | 384 |
| AT024 | 16 | 239 | 14.07.06 | 295 |
| AT025 | 23 | 256 | 15.49.52 | 346 |
| AT026 | 31 | 263 | 16.13.24 | 401 |
| AT028 | 40 | 269 | 16.43.27 | 270 |
| AT021 | 46 | 221 | 12.43.24 | 308 |

## Open originals and tests

- [ ] Locate the original ZNY-36 floppy image or directory listing, original email with attachment bytes and any transfer log or receiving copy. Compare path, size, hash and the job fields, particularly AT022 and AT027. Check the archive's print-selection history before attributing the missing extractable headers to the sender or recipient.
- [ ] Seek AT022 job-control input and its syntax or format documentation, tape records and any corrected rerun. To test the email's no-data description, distinguish command acceptance, selection output and returns on the underlying tape. Leave flight track interpretation and any clock test to the assigned recorder/radar work.
- [ ] Carry forward the Cleveland file 7 and recipient intake dependencies, the May 2003 corrected answer and delivery, signed administrative disposition, recommendation response and closure, and the applicable policy and custody records.

All nine public objects returned HTTP 200 labeled **text/plain**. They are largely plain text with retained non-ASCII/control bytes. The manifest records their received hashes and the reused PDF's hash. Tests cover selected job and diagnostic fields, with no raw radar decoding or event-time inference. [Source manifest](SOURCE-PINS.json)
