# Heated-connection data: nine-sheet audit crosswalk

The following values are the delivered R08 audit’s counts, checked for arithmetic consistency here; they were not independently recomputed from every native cell. Each row is one worksheet, not an independent experiment. All six workbook byte hashes were separately matched to the delivery manifest. Blanks are counted within the audit’s timed-record/column frame: a blank cell is not automatically instrument failure, and a numeric reading is not automatically physically valid.

| Worksheet | Timed records | Columns, including time and formulas | Blank cells in timed records | Columns containing blanks |
|---|---:|---:|---:|---:|
| CB-DA-AMB Data | 7,777 | 111 | 0 | 0 |
| CB-DA-AmbientLoadingData | 2,356 | 52 | 0 | 0 |
| CB-DA-FireLoadingData | 13,085 | 274 | 775,423 | 65 |
| CB-DA-SC-AmbientLoadingData | 6,200 | 59 | 6,549 | 2 |
| CB-DA-SC-FireLoadingData | 14,766 | 274 | 532,208 | 52 |
| CB-SP-AmbientLoading | 9,218 | 50 | 1,885 | 5 |
| CB-SP-FireLoading | 12,818 | 241 | 408,215 | 54 |
| CB-SP-SC-AmbientLoadingData | 7,171 | 59 | 8,162 | 7 |
| CB-SP-SC-FireLoadingData | 16,949 | 278 | 473,395 | 64 |

Total: **90,340 timed records** across nine sheets. Different worksheets cover different specimen phases and clocks. The record count is not a count of independent tests or uniformly spaced time steps; the ambient sheet has documented deleted intervals. Interpret values with the specimen-specific event log, formula ledger, instrument map, calibration records and validity limitations. The report distinguishes 1,398 header occurrences from unique sensors, and notes that many raw description differences are terminology rather than demonstrated instrumentation errors. No structural simulation or historical WTC 7 attribution was performed in this crosswalk.
