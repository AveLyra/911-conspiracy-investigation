# Independent printed-table transcription

Status: frozen September 19, 2026, before reading the root agent's transcription or calculations. Factual number transcription only. No fitting, velocity recomputation, interpolation, raw-video work, or scientific inference was performed.

## Source and scope

Source: `research/sherlock-wtc7-investigation/luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf` in the Sherlock WTC7 investigation worktree. SHA-256 verified with `shasum -a 256`:

`cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394`

The PDF has 51 physical pages. Physical pages 47 and 50 have printed page numbers 47 and 50 respectively. Page headers identify Journal of 9/11 Studies, Volume 42, June 2023.

Page 47 title: “All Camera 2 Points Vertical Positions and Velocities vs. Time.” Transcribed every row of `t`, Ref Building `x`/`y`, NE Corner `y`/`v`, EC Roofline `y`/`v`, WC Roofline `y`/`v`, and NW Corner `y`/`v`. E Penthouse, N Screen Wall, and W Penthouse are excluded by the assigned scope. The source footnote, “Start times of descent are bolded and outlined,” is preserved in JSON metadata; typography is not a numeric measurement or independently determined onset.

Page 50 title: “All Western Camera Points Vertical Positions vs. Time.” Transcribed all 25 rows and all 10 numeric columns, including `t`. The grouped headers are Reference Point (`y`), NW Corner (`y`, `relative y`), Center (`y`, `relative y`, `adjusted y`), and SW Corner (`y`, `relative y`, `adjusted y`). The complete relative/adjusted-y footnote is preserved in JSON metadata. The page also contains “Materials for Reproducing the Measurements,” references to the downloadable kit and Tracker, and camera links. Those references were visually covered but neither opened nor transcribed as table data.

## Method and actual visual coverage

The PDF skill and evidence-falsification-auditor skill were read, together with the worktree's AGENTS.md, WORKFLOW.md, and START-HERE.md. The narrow acceptance criterion is a faithful, independently sourced token transcription, not validation of the source measurements or conclusions.

1. Verified the designated source SHA-256. Extracted the two complete page texts and the word coordinates with `pdfplumber` using `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
2. Inspected the supplied `paper-page-47.png` and `paper-page-50.png`. The supplied page-50 image did not display the full heading/header area, so it was not the sole visual basis for source metadata.
3. Rendered physical page 50 directly from the verified PDF with `pypdfium2`, scale 2, with no crop. Inspected its entire page, including heading, all table rows, footnote, materials section, links, and printed page number.
4. Inspected page 47's complete page and three overlapping table renderings at scale 4. PDFium crop tuples (left, bottom, right, top), in PDF points, were `(30,490,30,95)`, `(30,300,30,295)`, and `(30,90,30,485)`. These cover the headers and all 70 numeric rows; boundary rows are shared between adjacent renderings. The last rendering includes the final numeric row and lower table edge.
5. Assigned exact extracted tokens to rows by time-token vertical position and to selected columns by observed horizontal location. Every selected numeric token and every selected blank was then visually checked row by row against the full page or enlarged sections. No other agent's transcription was read.
6. Stored printed decimal strings without converting numeric data to floats. JSON `null` means the printed cell is blank. Row numbers, page numbers, and PDF coordinates are locator metadata, not source numeric measurements. The field name `time_s` follows the requested data contract; the printed header is only `t` on these pages, and this transcription does not independently establish units.

Scratch PDF renders were saved under `/private/tmp/independent-page47-top.png`, `/private/tmp/independent-page47-middle.png`, `/private/tmp/independent-page47-bottom.png`, and `/private/tmp/independent-page50-full.png`. They are review aids, not source replacements. All originals were preserved. No network access or external transmission was used for this subtask.

## Counts and blank coverage

| Page | Rows | Selected numeric columns including t | Printed numeric tokens | Blank selected cells |
|---|---:|---:|---:|---:|
| 47 | 70 | 11 | 541 | 229 |
| 50 | 25 | 10 | 250 | 0 |

Page 47 has 70 time tokens, from `-1.0` through `12.8`. Selected column counts and populated endpoints:

| Column | Printed numeric tokens | First t | Last t |
|---|---:|---|---|
| Ref Building x | 70 | -1.0 | 12.8 |
| Ref Building y | 70 | -1.0 | 12.8 |
| NE Corner y | 16 | 6.4 | 9.4 |
| NE Corner v | 14 | 6.6 | 9.2 |
| EC Roofline y | 43 | 3.0 | 11.4 |
| EC Roofline v | 41 | 3.2 | 11.2 |
| WC Roofline y | 40 | 5.0 | 12.8 |
| WC Roofline v | 38 | 5.2 | 12.6 |
| NW Corner y | 70 | -1.0 | 12.8 |
| NW Corner v | 69 | -1.0 | 12.6 |

Page 50 has 25 time tokens, from `8.00` through `8.80`, and 25 numeric tokens in each of its nine other columns. Original two-decimal time strings are preserved.

## Ambiguities and limitations

No unresolved legibility ambiguity was found among the selected cells. Endpoint blanks were verified visually rather than replaced by calculated values. Equal or seemingly surprising printed values were retained exactly; agreement with arithmetic from other columns was not a transcription acceptance criterion. Bold/outlined rows were not used to infer unprinted values.

This checks fidelity to a derivative published table. It does not authenticate the original measurements, calibration, point tracking, camera timing, velocity method, uncertainties, or authors' interpretation. Agreement between the PDF text layer and its rendering is a source transcription check, not independent measurement replication. The omitted page-47 feature groups remain outside this transcription.

## Files, freezing, and verification

`table47.json` SHA-256: `fe5e566dff8cbff6aa80a00656820504b2542bc5468eef96eb9911d5e4aea2f8`

`table50.json` SHA-256: `9af054e9730915e35a429f2d846f3450120ea19b41a7c166b917b8f82e643c34`

`extract_tables.py` SHA-256: `02b84edf711894aa341add2e03a61a96d94776145eb723ccdb541cb91270f0b2`

The JSON files were first frozen in `/private/tmp/wtc7-independent.fPdhFq/` because creating the worktree parent initially failed. After the root agent created the parent, this agent installed its own files through `apply_patch`; hashes remained identical. The root agent was informed of the frozen hashes before comparison. No source values were revised after freezing.

The read-only `extract_tables.py` emits the independently assigned source tokens as JSON to standard output. It has an exact source-hash assertion, decimal-token format assertions, expected row-count assertions, and a one-token-per-cell assertion. It reads only the designated PDF. It neither imports nor reads the root transcription.

Actual verification executed from the investigation worktree with the bundled Python: `runpy.run_path` executed `extract_tables.py` while capturing standard output, parsed that output, loaded both saved JSON files, required full object equality with the fresh source extraction, verified one-based sequential source-row locators, and required every selected value to be a string or null. Results:

```text
page 47: exact source-extraction match; 70 rows; 541 numeric strings; 229 blanks; SHA256 fe5e566dff8cbff6aa80a00656820504b2542bc5468eef96eb9911d5e4aea2f8
page 50: exact source-extraction match; 25 rows; 250 numeric strings; 0 blanks; SHA256 9af054e9730915e35a429f2d846f3450120ea19b41a7c166b917b8f82e643c34
```

This verification passed. No model fitting or scientific hypothesis test was run in this subtask.
