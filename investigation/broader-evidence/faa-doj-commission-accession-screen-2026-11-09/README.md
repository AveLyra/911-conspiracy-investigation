# Public accession register check for the DOJ Commission collection

Public derivative of the November 9, 2026 Eastern source review · B129 / PD04–PD05, supporting PD01. I checked the National Archives’ three linked fiscal-year registers for an accession of DOJ’s retained 9/11 Commission records. No RG 60 row in those registers named the collection or either of its schedule authorities. The FY 2023 register supplies one date-overlapping identifier under a generic title. The item remains unidentified beyond what the register says. [National Archives accession table and downloads](https://www.archives.gov/research/accessions)

## What the register records

| Source | Scope and result |
| --- | --- |
| FY 2021 workbook, sheet 1 | **1,848** data rows, **35** RG 60 rows, **zero** exact target hits. |
| FY 2022 workbook, sheet 1 | **4,974** data rows, **62** RG 60 rows, **zero** exact target hits. Row **2248** identifies an Executive Secretariat project-file transfer, **TR-0060-2017-0146 / W060-04-1480**, with a record span of **2000**. |
| FY 2023 workbook, sheet 1, and HTML table | **4,816** data rows and **62** RG 60 rows in each. Their RG 60 accession IDs and the nine compared fields agree after date-format and whitespace conversion for this comparison. Neither edition supplies an exact hit. The HTML and workbook are two versions of the register and do not increase the search count. |
| FY 2023 workbook row **3794** and HTML table row **3794**, raw HTML lines **52991–52999** | **“Significant case files,”** January 1 to June 30, 2004, **17 containers**, National Archives at College Park, Textual Records Division. Accession **TR-0060-2022-0041**, Federal Records Center transfer **W060-06-0937**. |

The time window of the 2004 row overlaps part of the successor schedule’s stated **2002–2004** initial transfer record span. The accession row gives no originating office, schedule assignment or container titles. The identifier search located no item-level confirmation that this row concerns the Commission. The **2000** Secretariat record separately confirms that the register can expose that office’s name and both transfer identifiers. It has a different record span. [DOJ schedule successor, PDF p. 4](https://www.archives.gov/files/records-mgmt/rcs/schedules/departments/department-of-justice/rg-0060/daa-0060-2017-0034_sf115.pdf#page=4)

## Scope and open records

The accessions page says its table displays the **“current fiscal year”** (captured HTML line 314). The body returned on **November 10, 2026 UTC** contains **FY 23** quarter labels exclusively. Preserve both observations. The linked workbooks are labeled FY 2021 through FY 2023. The page describes the data as agency-supplied accession metadata that may be revised during processing. The tested tables cover those fiscal-year releases and are not an inventory of every historical or current accession. [NARA New Accessions](https://www.archives.gov/research/accessions)

The separately captured RG 60 public export listing reports **400** objects, **3,040,176,635 bytes** and `IsTruncated=false`. This check read the object listing. It left the JSONL contents unsearched. The historical RG 60 guide’s heading gives **1790–1989, 1991**, a different scope. [RG 60 export listing](https://nara-national-archives-catalog.s3.amazonaws.com/?list-type=2&prefix=descriptions%2Frecord-groups%2Frg_60%2F&max-keys=1000) · [Historical guide](https://www.archives.gov/research/guide-fed-records/groups/060.html)

- [ ] Obtain the originating office, schedule and container list for **TR-0060-2022-0041 / W060-06-0937** before considering it a Commission source. Separately seek the actual DOJ Executive Secretariat transfer and receipt under **N1-060-05-001 / 1** or **DAA-0060-2017-0034-0002**. A match requires an authority, title or item-level join beyond a shared year.
- [ ] Carry forward the FAA corrected answer and receipt, signed administrative disposition and recommendation-specific closure. This register screen yielded no evidence of a 2006 FAA correction or administrative outcome.

Six original response hashes verified. Each of the three received XLS bodies matches the prior capture used to study DOT accessions. The originals remain separate. LibreOfficeDev 26.8.0.0.alpha0 converted the workbooks in an isolated profile. Python parsed the resulting worksheet XML and the captured HTML. The screen checked both schedule numbers and the collection and authority titles in RG 60 fields. Raw dates and source wording remain in the original bodies. [Sources, terms and verification](SOURCE-PINS.json)
