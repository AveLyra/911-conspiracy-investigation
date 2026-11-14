# Native workbook inventory

This directory records a read-only ZIP/XML examination of six unchanged NIST XLSX files. It contains 30 worksheet inventories and 90,340 timed records across nine measurement sheets. Workbook hashes and CRC checks are in `summary.json`. The separate direct ambient download has the same SHA-256 as the ambient download through the document route; it is not counted as another specimen.

## What the inventory means

`sheet_inventory.csv` distinguishes the worksheet's declared dimension, the extent of stored XML cells (including formatting-only cells), the nonempty cell extent, and the timed-data extent. Drawing objects have their own anchors in the drawings inventory: an image can extend beyond the nonempty cell range.

Each workbook directory includes:

- `inventory.json`: sheet names/state, ranges, merged cells, hidden rows/columns, source metadata, exact row-1 headers, column summaries, clock diagnostics, comments, drawing relationships, and style definitions.
- `*_observed_cells.json` and `observed_metadata_cells.json`: all nonempty cells from notes, channel lists, event tables, and drawing captions, retaining exact address, XML value/type, resolved shared-string text, and style.
- `channel_headers_and_quality.csv`: header addresses, counts, source first/last nonempty addresses, blank-versus-absent counts, numeric extrema, and formula counts.
- `formulas_and_cached_values.ndjson.gz`: every formula cell's original `<f>` text/attributes and stored `<v>` cache. No recalculation occurred.
- `shared_formula_groups.json`: each shared-formula master, worksheet-local shared index, source range, and raw master expression. An empty shared follower `<f t="shared" si="…"/>` is a formula; it is not a missing formula.
- `comments_and_style_review.json`: exact source comments joined to worksheet names, threaded-comment/person XML, data style definitions, and observed metadata checks.

All summaries, counts, missingness diagnostics, numerical extrema, parsed dates, and time differences are **derived**. They are not additional measured cells. Original workbooks remain the authority for exact source representation.

## Timed sheets

Counts exclude each header row. Column counts include both clock columns and, where present, native formula-derived summaries.

| Workbook | Worksheet | Timed range including header | Records | Columns |
|---|---|---|---:|---:|
| CB-DA-AMB | CB-DA-AMB Data | A1:DG7778 | 7,777 | 111 |
| CB-DA | CB-DA-AmbientLoadingData | A1:AZ2357 | 2,356 | 52 |
| CB-DA | CB-DA-FireLoadingData | A1:JN13086 | 13,085 | 274 |
| CB-DA-SC | CB-DA-SC-AmbientLoadingData | A1:BG6201 | 6,200 | 59 |
| CB-DA-SC | CB-DA-SC-FireLoadingData | A1:JN14767 | 14,766 | 274 |
| CB-SP | CB-SP-AmbientLoading | A1:AX9219 | 9,218 | 50 |
| CB-SP | CB-SP-FireLoading | A1:IG12819 | 12,818 | 241 |
| CB-SP-SC | CB-SP-SC-AmbientLoadingData | A1:BG7172 | 7,171 | 59 |
| CB-SP-SC | CB-SP-SC-FireLoadingData | A1:JR16950 | 16,949 | 278 |

CB-DA-AMB is a separate specimen. The ambient-loading sheets inside the four fire-specimen files belong to those fire specimens; they are not repetitions of CB-DA-AMB. Retain source event/phase comments when joining loading periods.

The CB-SP-SC fire worksheet's nonempty range extends one row further, through row 16951. That row contains only `DK16951 = MAX(DK2:DK16950)` and `HR16951 = MAX(HR2:HR16950)`. Their cached results are 716.12760000000003 and 736.43740000000003. These two summary cells are preserved separately and excluded from timed-record counts and missingness. There are 217,389 source formula cells in total, of which 217,387 lie in timed records. Every formula has a stored cache, and all shared groups have a master.

## Primary-pair clock and event findings

The matched-pair CSV files preserve original stored values, including source formula caches, and add an explicitly derived `source_excel_row` field. They resolve shared strings but perform no unit conversion, smoothing, interpolation, deletion, or recalculation. Blank and absent cells both appear empty in CSV; their source distinction remains in XLSX and the inventory. Formula origin remains in the formula ledger and per-column inventory.

`matched_pair_time_audit.json` supplies exact source cells for clock/event comparisons:

- CB-DA-AMB has nominal one-second recorded spacing with six longer intervals after rows 609, 1209, 2435, 3466, 4703, and 5303: 814, 872, 783, 224, 2,439, and 480 seconds. Comments at those rows expressly record data deletion, including fiber-optic pauses and intervals between loading cycles. No replacement rows were created.
- CB-DA-AMB `User Events!B6` stores 4344 seconds. Its `C6` timestamp matches data row 3466, whose `B3466` stores 5930 seconds and whose comment identifies the end of the first load cycle. The 1,586-second conflict is retained; any corrected event alignment must be a separate derived annotation.
- CB-DA fire time zero is gas-flow initiation (`User Events!B3 = 0`), while ignition is `B4 = 23.001399999999194` seconds and is also annotated at data cell A25. The elapsed-time column advances by approximately 1.0000 or 1.0001 seconds. The timestamp column has one two-second step at A10437–A10438, without a corresponding elapsed-time gap. This is not classified as a missing measurement.
- CB-DA-SC and CB-SP-SC store time-of-day fractions in column A, with date text in A1. Their inventories preserve that distinction instead of assigning an invented 1899/1900 calendar date. No timezone is supplied by this audit.

## Quality and reductions

The primary ambient data and CB-DA preload have no blank data cells. CB-DA fire has 775,423 blank/absent cells across 65 columns. Exact column counts, first/last values, and internal blank runs are supplied. The other specimens have their own missingness inventories.

No Excel error or nonnumeric marker occurs in the nine timed-data tables. No data header matches the inspected standard-deviation, uncertainty, quality-flag, or calibration terms. No conditional formatting, data validation, hidden data rows/columns, or colored data-cell fill supplies a per-sample validity mask. The 66 source comments and threaded metadata are retained, including data deletions, event timing, and load sign conventions. These observations do not establish physical sensor validity. Blank cells, absent uncertainty records, and unreliable nonblank physical measurements require different treatment. Channel-list installation marks and instrument ranges do not supply a calibration certificate or measurement uncertainty.

The fire-file average columns are native reductions. For example, CB-DA `JN2` (`AvgAxialLoad`) is `AVERAGE(F2,G2,H2,I2,J2,K2,L2,P2,Q2,R2,S2,T2,U2,V2)*3.9`, with a stored cache of 27.739223571428571 kN. It is derived from brace strains. Source comments at `Channel List!A272` and fire `JN1` state that negative denotes compression. It is not an independent connection-force measurement.

## Reproduction

The three Python scripts use the standard library and read native files without saving changes to them. With the scripts together and six staging filenames retained, run:

```bash
python3 scripts/inventory_native.py --input native --out rebuilt_inventory
python3 scripts/audit_primary_time_and_export.py --input native --out rebuilt_inventory
python3 scripts/finish_inventory.py --input native --out rebuilt_inventory
```

Adjust the two directory arguments to the package layout. The duplicate ambient-direct comparison is `null` if the redundant seventh download is not supplied. No structural model is present or run.
