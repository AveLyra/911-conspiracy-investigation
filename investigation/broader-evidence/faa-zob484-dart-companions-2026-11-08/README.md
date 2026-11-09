# Two Cleveland DART outputs and their shared tape labels

November 8, 2026 Eastern · **B129 / PD07**, with **PD01–PD04** open. The two DART files archived with Cleveland's NTAP host output contain distinct job logs dated **21 OCT 2005**. The second DART job and the NTAP job both name **AC8270** in setup and tape-mount fields. The two DART jobs share **AC8251**. Those exact identifiers give a way to look for common source media. Physical tape identity, the recorded ranges and any relationship to the 2001 FTP files remain open. [NARA Box 77, ZOB-484](https://www.archives.gov/research/foia/faa-finding-aid-72-83)

## Archive labels and job fields

The finding aid groups all three objects under a compact disc described as **9/11/01 Host Outputs**. Each returned body gives **21 OCT 2005** as the job execution date. Those fields describe different aspects of the archive record. Keep the disc label, job dates and any future source-data dates separate.

| Catalogue filename | Logged job name and number | Start and end fields | Setup tape labels |
|---|---|---|---|
| **dartzob1.txt** | **DARTZOB1**, **JOB02355** | **07.43.35**, **07.51.13** | **AC8245**, **AC8251** [NAID 7597049, lines 5, 22, 24 and 36](https://catalog.archives.gov/id/7597049) |
| **dartzob2.txt** | **DARTZOB1**, **JOB02440** | **08.28.28**, **08.40.52** | **AC8251**, **AC8270**, **AC8313** [NAID 7597050, lines 5, 26, 28 and 40](https://catalog.archives.gov/id/7597050) |
| **ntapzob1.txt**, held | **NTAPZOB1**, **JOB02760** | **09.59.44**, **10.03.44** | **AC8270** [NAID 7597051, lines 5, 13, 15 and 28](https://catalog.archives.gov/id/7597051) |

Both DART bodies display **A5F1.1 RDART II(R1)** at line **8**. The held NTAP body displays **1.1-0 00.192** at line **68**. The **dartzob2.txt** filename and its internal **DARTZOB1** job label remain separate. The three job numbers and start and end fields are distinct. The time zone and any alignment to event clocks remain unverified. [Exact response and field locators](SOURCE-PINS.json)

## What the shared labels establish

Both newly acquired DART bodies list **AC8251** in setup and have exact **VOL=SER=AC8251** fields. The second DART body lists **AC8270** in setup, in two **VOL=SER** fields and in IEC501A and IEC502E job messages. The NTAP body likewise has **AC8270** in setup, volume fields and IEC501A and IEC502E job messages. The message codes are consistent with tape mount and demount instructions in IBM’s documentation. The checked documentation is a later edition. This is a label match across separate logs and multiple field roles. The output logs alone leave actual tape contents, volume reuse and the precise extraction ranges unresolved. The first DART body has no literal **AC8270** hit. [DART1, lines 36, 71 and 76](https://catalog.archives.gov/id/7597049) · [DART2, lines 18, 21, 40, 75 and 80](https://catalog.archives.gov/id/7597050) · [NTAP, lines 8, 11, 28, 42 and 47](https://catalog.archives.gov/id/7597051) · [IBM tape-message reference](https://www.ibm.com/docs/en/zos/3.2.0?topic=routines-openeov-volume-security-verification-exit)

## Byte counts and remaining records

| Object | Catalogue bytes | Received bytes | SYSOUT printed record count | Received lines from Python `bytes.splitlines()` | NUL runs |
|---|---:|---:|---:|---:|---|
| dartzob1.txt | 712,709 | 706,648 | 6,059 | 6,062 | 13 runs of 7 bytes |
| dartzob2.txt | 9,897,175 | 9,822,319 | 74,854 | 74,857 | 19 runs of 7 bytes |
| ntapzob1.txt | 33,605 | 33,231 | 371 | 375 | 2 runs of 8 bytes |

The body hashes are distinct. Preserve the two size fields and two record-count fields for each file. Their relationships and the origin of the NUL bytes remain unresolved. The first dartzob2 request exceeded the **4,000,000-byte** cap and retained a receipt for an incomplete read. A separately named acquisition with a **12,000,000-byte** cap obtained the full body. Structural checks cover the exact received bytes and selected log lines. Radar observations, tracked aircraft, event clocks and actual media custody are outside the tested scope. [Hashes, exact offsets and both request receipts](SOURCE-PINS.json) · [Preceding report diff](TEXT-CHANGES.diff)

- [ ] Obtain the physical disc manifest, tape handling log, and job requests and exact input and output parameters for **JOB02355**, **JOB02440** and **JOB02760**. Test whether **AC8251** and **AC8270** are the same physical volumes across the logs.
- [ ] Obtain the September 2001 FTP manifest and original file 7 and duplicate counterpart. Compare contents only after verifying their source and format. Keep the 2005 outputs separate pending an exact media or record join.
- [ ] Keep the corrected FAA answer and delivery acknowledgment, signed administrative outcome and recommendation-specific records open.
