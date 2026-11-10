# Cleveland NTAP archive objects and the file 7 trail

November 5, 2026. **B129 / PD07.** The earlier FAA inventory comparison identified **ual93-file 7**, entered as **9/27** under **To NTSB** in the copy circulated October 3. This follow-up acquired the 12 digital objects in the FAA collection's **ZOB-40** two-floppy listing, a printout counterpart, a separate TSA-column inventory and a September 25 FAA routing message. It tests whether those holdings can identify the original file or document delivery. [Preceding inventory comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/b70b23fc7c261c174ee5b9c7f263c03715729b7c/investigation/broader-evidence/faa-eastern-radar-inventory-followup-2026-11-05/README.md) · [NARA Box 70, ZOB-40 and its twelve digitized files](https://www.archives.gov/research/foia/faa-finding-aid-60-71)

## The sender-side filename request

At **1:38 PM on September 25, 2001**, the regional reply in **ZOB-475** reports that the headquarters contact said the posted data need not be sent again. The reply specifically requests the **file name** and says the region will compile files from all facilities and send one email to headquarters. It quotes the Cleveland **12:26 PM** account already seen in ZOB-244 and ZOB-261. The message identifies a concrete next document, the compiled regional list. Its sender and reported conversation are distinct from the **3:25 PM** FAA reply calling the already-sent NTAP sufficient. The **12:02 PM** reply above the **12:26 PM** quotation remains a separate header discrepancy in ZOB-261. [ZOB-475 p. 1, lines 2 and 8–20](https://catalog.archives.gov/id/7597479) · [Cleveland replies and their limits](https://github.com/AveLyra/911-conspiracy-investigation/blob/5486d2e73b4e53e922946b41d3ac8b4b53cb20db/investigation/broader-evidence/faa-cleveland-request-returns-2026-11-05/README.md)

## Twelve objects and nine distinct suffixes

The 12 catalog entries yielded 12 distinct SHA-256 values and 12 distinct JES2 start-header job numbers. The filenames expose nine distinct numeric suffixes. The list contains no literal **ual93-file 7** or **.file7**. It uses **.file1** three times and **.file2** twice. These are catalog filename fields, and the duplicated suffixes distinguish why a join based on the last digit alone is unsafe. The bytes begin with JES2 job-log text. Any relation between these objects, the original floppy directory entries and FAA transmission filenames remains open. [NARA Box 70, ZOB-40](https://www.archives.gov/research/foia/faa-finding-aid-60-71) · [Exact labels, job starts and source hashes](SOURCE-PINS.json)

| Repeated suffix | Time spans as cataloged | Job numbers at line 3 of the downloaded bodies |
| --- | --- | --- |
| **.file1** | **1320-1335**, **1330-1334**, **1356-1400** | **873**, **706**, **807**, respectively |
| **.file2** | **1334-1338**, **1400-1404** | **707**, **809**, respectively |

The **1356-1400.file1** text object and the **ZOB-480** scanned printout for the same labeled range share **job 807**, start text **20.17.18**, and **502 SYSOUT PRINT RECORDS**. The comparison joins three printed fields and the cataloged interval. It gives a candidate printout counterpart for that export, with no native floppy image, line-for-line equivalence or identification of the inventory's **ual93-file 7**. [ZOB-40 text, lines 3 and 10](https://catalog.archives.gov/id/7597041) · [ZOB-480 physical p. 1, lines 20, 23–25 and 36](https://catalog.archives.gov/id/7597047)

The body cataloged as **1402-1406.file9** contains eight consecutive NUL bytes at zero-based offsets **32862–32869**, with job-log text also present. The capture preserves the bytes as received. No format, generation or transfer explanation for these bytes was tested. [ZOB-40 file9](https://catalog.archives.gov/id/7597044)

## A third inventory entry with a different destination column

**AWA-423**, in the AAL77 catalog branch, also includes a UAL93 radar table on physical **p. 5**. The row **ZOB / ual93-file 7 / NTAP** appears there, and its **To TSA** cell is blank on the inspected scan. The printed table also lists the other nine numbered Cleveland file labels. Preserve this record beside the NTSB inventory entries. The recipient column differs, and the blank cell supplies no date or acknowledgment for TSA. It also supplies no independent receipt for the NTSB entry. [AWA-423 p. 5, extracted lines 2–10 and 56–85](https://catalog.archives.gov/id/7596129) · [Earlier NTSB inventory comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/b70b23fc7c261c174ee5b9c7f263c03715729b7c/investigation/broader-evidence/faa-eastern-radar-inventory-followup-2026-11-05/README.md)

## Open records and tests

- [ ] Find the September 25 compiled regional filename email, exact upload manifest, FAA onward transmittal and NTSB item-level acknowledgment. Match the literal **ual93-file 7** to a stored file with a dated transfer identifier. TSA's separate delivery records would test the destination column in AWA-423.
- [ ] Locate the original ZOB-40 disk directory or images and exact extraction/export logs. Compare full paths, names, size, timestamps and hashes against each of the catalog copies. Retain the candidate ZOB-480 printout comparison and keep any actual track interpretation in the recorder/radar work.
- [ ] Keep the Washington Operations Center Activity Report's original version and receipt and the May 2003 corrected answer and delivery, signed disposition, recommendation response and closure, and applicable policy/custody crosswalk open under PD01–PD04 and PD07.

Fourteen source response bodies came from the catalog media route for ZOB-40, ZOB-475 and ZOB-480. AWA-423 was also acquired from the catalog route after a separate indexed S3 URL returned a 403 XML response. The error body is separately pinned. Checks cover body hashes, literal filename labels, selected job headers and source paragraphs, and the visible TSA row and printout fields. No radar measurements were decoded and no event clock was inferred. [Source manifest](SOURCE-PINS.json)
