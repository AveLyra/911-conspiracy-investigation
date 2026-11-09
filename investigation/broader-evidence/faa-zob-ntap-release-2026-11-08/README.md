# Cleveland NTAP file 7 and the September 17 FTP report

November 8, 2026 Eastern · **B129 / PD07**, with **PD01–PD04** open. A newly acquired FAA note says it removed **UAL93.file7** as a duplicate. The same note lists two release ranges that skip 7 and gives an FTP posting range that includes 7. A previously acquired FAA inventory later lists **ual93-file 7** under **To NTSB**. These records now give a specific duplication claim and a later inventory entry to test. The native file, its alleged duplicate and the FTP and recipient manifests remain unacquired. [Release note](https://catalog.archives.gov/id/7597443) · [Later FAA inventory](https://catalog.archives.gov/id/34912007)

## Exact fields on the release note

| Field on ZOB-345, physical p. 1 | Observation |
|---|---|
| Release description, OCR line 2 | Says NTAP data were released to **AAT200**. The archive description gives **AAT-200**. |
| Filename block, OCR lines 4–5 | **UAL93.file1-6** and **UAL93.File8-13**, preserving case and punctuation. Interpreted strictly as written numeric ranges, these contain 12 positions and skip 7. |
| Duplicate account, OCR line 7 | Says **UAL93.file7** was a duplicate and was removed. The visual line says **I remove**. OCR renders **\| remove**. The note gives no matching filename, size or hash. |
| FTP sentence, OCR lines 7–9 | The last sentence ends the first line with **UAL93.file1-** and starts the next line with **13**. It reports posting to FTP on **09/17/01**. Taken as a numeric range, the statement includes 7. The posting date is in the body. The scan has no visible message date or subject header. |

Preserve the separate release list, duplicate statement and FTP range. Their relationship and actual upload contents are unresolved. The reference to removal supplies a reported action on one copy of one data file. The location, version and retention of other copies are unverified. [ZOB-345, p. 1](https://catalog.archives.gov/id/7597443)

## Compare the held inventories and read notices

- **AEA-2353**, physical p. 7, carries nine numbered Cleveland **ual93-file** rows under **To NTSB**, all marked **9/26** and with no file 7 row. **AEA-2354**, physical p. 7, includes **ual93-file 7** marked **9/27** in that column. **AWA-423**, physical p. 5, includes a **ual93-file 7** row with an empty **To TSA** cell. The filename styling and the destinations differ from the new note. The inventories give FAA-side fields. No NTSB or TSA recipient evidence establishes exact delivery or identifies the reported duplicate. [AEA-2353](https://catalog.archives.gov/id/7600802) · [AEA-2354](https://catalog.archives.gov/id/34912007) · [AWA-423](https://catalog.archives.gov/id/7596129)
- **ZOB-40** lists 12 archived objects with nine distinct suffix numerals. The held bytes have 12 distinct hashes. The literal suffixes include three **.file1** and two **.file2** entries, with no **.file7**, **.file11**, **.file12** or **.file13**. Comparing numerals only, those nine are in both the ZOB-345 release list and the later AEA-2354 numbered series. The equal count of 12 archive objects and 12 nominal release positions cannot establish a one-to-one join. The original floppy directory and FTP transfer ledger are needed. [Prior archive objects and hashes](https://github.com/AveLyra/911-conspiracy-investigation/blob/ced1d5dec3c03b71a4849cbb3a2f4b3f16f474f5/investigation/broader-evidence/faa-cleveland-native-ntap-labels-2026-11-05/README.md) · [NARA Box 70](https://www.archives.gov/research/foia/faa-finding-aid-60-71)
- **ZOB-366 and ZOB-367** show **UAL93 NTAP** sent **9/12/01 5:09:00 PM** with distinct recipients and read stamps. **ZOB-345** gives the **09/17/01** FTP date in its body and lacks a message header. The shared data category identifies related records for further comparison. No message ID or native attachment joins the notes. [Read-notice comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/38d397410cd48630f14278769e4e693fba7c16f8/investigation/broader-evidence/faa-zob-retention-receipts-2026-11-08/README.md)

## Verification and remaining records

I acquired the exact catalogue response and its linked one-page PDF, then read the page visually. The catalogue object size is **7,359** bytes and the returned PDF is **11,943** bytes. Both are preserved with the edition relationship open. pypdf and PyMuPDF returned zero embedded files, no file-attachment annotations and no catalogue associated-files entry. I rechecked the held inventory and archived-object hashes and compared literal suffix counts. The tests cover document fields and received bytes. No NTAP tracks or historical clocks were decoded here. [Source pins and exact checks](SOURCE-PINS.json) · [Preceding report diff](TEXT-CHANGES.diff)

- [ ] Locate the September 17 FTP directory and upload record, the source file 7 and the file described as its duplicate. Compare full names, exact bytes, extraction settings, record content and revision history. Retain both raw artifacts and any later copies.
- [ ] Find the September 25 compiled regional filename list and NTSB's actual September 27 item-level intake. Join by accession, original name, size and hash. Retain the separate TSA list and test whether the 2001 notice refers to the same distribution.
- [ ] The corrected May 2003 answer, recipient acknowledgment, signed administrative disposition and recommendation-specific records remain priority missing originals.
