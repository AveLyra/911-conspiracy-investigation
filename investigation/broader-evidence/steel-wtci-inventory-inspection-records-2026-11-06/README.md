# NIST WTCI inventory and the WTC 7 drawing and inspection records

November 6, 2026 · Steel track · STL02–STL03 / AUD011 / AUD016 / B188 / H005

The public **12-090** mirror contains a NIST catalog entry and a scanned-directory listing for **WTCI-000320-I.PDF**, described as a WTC 7 shop-drawing transmittal dated **May 17, 2007**. It also identifies **WTCI-000193-I.PDF**, a separate transmittal for **42 GMS erection-plan sheets**. These are exact retrieval targets for the drawing trail. The PDFs and their enclosures remain unacquired. [Public 12-090 archive](https://archive.org/download/911datasets/NIST_FOIA_12-090_Jun_13_2012.zip) · [Source ledger](SOURCE-PINS.json)

## Two complementary inventory sources

The June 13, 2012 final-response scan describes seven released electronic records, six spreadsheet exports and one text directory listing of scanned hard copies. NIST said it lacked one consolidated inventory of all WTCI materials. The mirror separately includes a correspondence PDF and disc image file. This pass read the response scope, the main workbook and the text directory. The workbook has **4,315 data rows**. The seven released records are inventory artifacts. Their file count and workbook row count do not measure the total number of original WTCI records. [12-090 archive, response scan p. 1 and workbook](https://archive.org/download/911datasets/NIST_FOIA_12-090_Jun_13_2012.zip)

The prior study identified **22 numbered Frankel PDFs** in the separate **12-009** drawing release. I joined each filename to exactly one **12-090** catalog row using the assigned number and category, and exactly one directory entry. All **22 of 22** directory size strings match the corresponding held PDF's byte count divided by 1,024 and rounded down. I reread and rehashed all 22 held files. The directory supplies dates described in the response as scan dates. It does not supply cryptographic hashes, so the metadata agreement cannot establish exact byte identity with the historical files. [Prior Frankel PDF review](https://github.com/AveLyra/911-conspiracy-investigation/blob/de6091608d43e095592c787bf5292e8ed03e9a6d/investigation/broader-evidence/steel-frankel-wtci-drawing-index-2026-11-06/README.md) · [22-row join and hashes](SOURCE-PINS.json)

| Preserved observation | Scope |
|---|---|
| **WTCI-000268-I.PDF** is cataloged as **Fabrication Drawings WTC7 Steel, Plate Girder Schedule**, `DocID` **Detail.2**. Workbook **O4095/Q4095**, directory line **8618**. | The earlier scan read found a plate girder schedule and could not read the sheet number at the cropped bottom edge. **Detail.2** is catalog evidence. The drawing face designation remains unverified. |
| **WTCI-000270-I.PDF** is cataloged as an 8th and 9th floor framing plan and has a blank `DocID` cell. Workbook **O4097/Q4097**, directory line **8620**. The prior visual read found **E8/9**. | Keep the blank metadata field beside the drawing-face observation. |
| **WTCI-000265-I.PDF** has catalog `DocDate` **11/1/1985**. **21 other rows** in the checked block show **11/1/2001**. Workbook **P4089:P4110**, exception at **P4092**. The directory prints **4/15/2010** for all 22 entries. | Catalog document dates, 2006 entry dates, 2010 scan dates and drawing revisions are separate observations. The reason for the 1985 exception remains open. |

## Original records to locate

| WTCI record | Catalog and directory locator | What its contents could test |
|---|---|---|
| **WTCI-000320-I.PDF** | Workbook row **4149**, directory line **7869**, **596 KB**, catalog `DocDate` **5/17/2007** | Which shop drawings were transmitted, their source, and whether the transmittal names a register or enclosures. |
| **WTCI-000193-I.PDF** | Row **3812**, line **7639**, **281 KB**, catalog `DocDate` **2/26/2004** | Which **42** erection-plan sheets were transmitted. The same number of TIFFs in a mirror folder would not establish an item-by-item match. |
| **WTCI-000001-I.PDF** | Row **291**, line **7410**, **162 KB** | The actual SEAoNY steel identification and inspection guide, including any criteria for retaining or revising a provisional building attribution. |
| **WTCI-000049-I.PDF** | Row **531**, line **7458**, **249 KB** | The catalog title describes a required structural-steel inspection program. Its project, scope and relation to WTC 7 remain unverified. |
| **WTCI-000704-P.PDF** | Row **4008**, line **5302**, **17 KB** | The catalog title describes a WTC 7 condition survey from **1997**. It may illuminate later inspections. Original construction inspection scope remains separate. |

NIST's construction report says the project specifications called for a **separate fabrication testing and inspection contract** that included welding. NIST reported that the contract was unavailable and implementation could not be established. It separately attributed to the Port Authority an account that the general contractor discarded WTC 7 inspection records after seven years. Preserve these statements alongside the drawing notes calling for test reports and certification. The newly located catalog entries give routes to records with distinct purposes. Their descriptions do not establish that they contain original construction weld results or corroborate the scope of the reported disposal. [NIST NCSTAR 1-1, printed pp. 97, 102–103](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-1.pdf) · [S-20 and E120 note review](https://github.com/AveLyra/911-conspiracy-investigation/blob/2d07b40365e1e2650a375218b805ff9b9933ed9e/investigation/broader-evidence/steel-cantor-s20-connection-note-crosscheck-2026-11-06/README.md)

## Open TODOs

- [ ] Obtain the listed transmittals, the signed testing and inspection contract, certification records tied to fabrication marks, and any original retention or disposal documentation. Track each custodian and record class separately.
- [ ] Trace the steel guide and field measurements into the transfer and inventory records for **A or W14A** and **B or W14B**. FEMA's field attribution and NIST's unidentified classification remain unresolved.
- [ ] Continue looking for **A2540**, **A2547** and **E117B** through enclosures, internal drawing marks and alternate holdings. Exact token searches in catalog `DocTitle` and `DocID` and in the text directory found zero hits. This leaves unindexed content and holdings outside these exports open.
