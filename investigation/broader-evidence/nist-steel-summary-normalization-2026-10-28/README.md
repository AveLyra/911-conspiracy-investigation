# NIST steel summary data acquired: source populations and an unresolved normalization check

October 28, 2026. Existing STL01–STL04 / SPT01–SPT08 / B188-H005 / AUD011-AUD016. This records a newly acquired published scientific dataset and a conditional field calculation. It does **not** recover DOC-NIST-2013-001311's disposition, the native inventory, field/coupon custody or W14A/B attribution rationale. Those original-record requirements remain open.

## Actual source and quantities

The [Data.gov manifest](https://catalog.data.gov/dataset/data-from-high-temperature-tensile-constitutive-data-and-models-for-structural-steels-1714) exposes the [NIST data CSV](https://data.nist.gov/od/ds/59275E35E82149D8E0531A57068146E31859/TN1714data.csv), [attribute CSV](https://data.nist.gov/od/ds/59275E35E82149D8E0531A57068146E31859/TN1714data-attributes.csv) and [bibliography](https://data.nist.gov/od/ds/59275E35E82149D8E0531A57068146E31859/TN1714-data-bibliography.pdf). All three original entities are preserved unchanged: **208,148 bytes total**. Exact source/access/hash records are in [SOURCES.json](SOURCES.json).

The data have **756 rows and 22 columns**, with 22 corresponding attribute definitions. Source labels divide them into **688 Literature rows** and **68 This study rows**. The latter have 68 unique nonmissing Sample strings and nine distinct specimen strings. Rows, test-sample strings and parent-component designations are different units; these are not 756 recovered pieces, nor an independently authenticated count of nine recovered columns.

The documentation attributes This study to NIST tests associated with the WTC investigation. The dataset supplies specimen strings and a literature-reference key, not the complete original collection/alias/transfer or instrument histories. None of the selected W14A/B, C12a/b, M4/M14/M10a/b targets matched the Sample/specimen fields under the stated lookup. This bounded field result does not establish their absence from NIST holdings or other files.

## Preserve the conditional arithmetic discrepancy

The attribute file defines RFy as normalized **0.2%-offset yield strength**, FY002 as reported **0.2%-offset yield strength**, and FY20 as that strength at 20 °C. We tested the *possible row-level relation* RFy = FY002/FY20, preserving every original value. It remains necessary to establish that FY20 is the intended normalization baseline for each row.

| CSV physical line, header included | Source / identifying fields | Original RFy | Original FY002 | Original FY20 | Conditional ratio |
|---|---|---:|---:|---:|---:|
|717|This study; luecke2011; C65H-.5-L1; C65_FL; T=20|1|263.5 MPa|226 MPa|1.1659292035|
|268|Literature; harmathy1970; T=152|1.038|369 MPa|534 MPa|0.6910112360|

Both tuples remain unchanged. No preferred value or corrective denominator is substituted. Different baseline/series assignments, normalization conventions, aggregation, transcription or later version differences are untested possibilities. A conditional mismatch does not establish a bad original measurement or a collapse-model error.

There were **68 eligible This study rows** and **631 eligible Literature rows**; 57 Literature rows lacked usable numeric inputs. Median absolute residuals were approximately **0.000605** and **0.000387**, respectively. The examples above are the largest absolute residual in each group, not representative of every row. All eligible row calculations and exclusions were retained locally; [results](RESULTS.json) record the summaries and largest rows. No undocumented pass tolerance or scientific-error verdict was applied. [Method](DATA-TEST-PROTOCOL.md); [reproducible code](analyze_dataset.py).

RFy02/FY02 instead concern **2% total elongation**. They were not tested with a 0.2%-offset denominator without a supported baseline rule. Similar-looking yield-field names cannot be treated as interchangeable.

## Date, test and provenance limits

**T is the tensile-test temperature**, not a measurement of the steel's 2001 fire exposure. The dictionary also gives Year a source-dependent publication/manufacturing meaning. All 68 This study rows carry Year=1972, and their test T values range from 20 to 701 °C; those fields do not date the laboratory tests or independently reconstruct fire temperatures.

The catalogue's displayed last-updated label is **October 1, 2011**. The explanatory PDF is dated **March 5, 2018**, cites the 2011 TN1714 report and describes later augmentation associated with **TN1907 (2016)**. Keep these edition/date accounts separate; this review does not determine why the catalogue label differs, silently date the CSV, or treat this compilation as the original 2005 input/delivery file.

The strongest limitation on the arithmetic criticism is the unverified row-to-baseline mapping. The decisive next records are the normalization worksheet, specimen/test-series baseline identifiers, original machine curves/calibration and source/edition crosswalk. An authenticated baseline rule could explain why the simple quotient is inapplicable; an unsupported denominator or transcription could instead sustain a data-quality concern. Neither outcome is selected.

## Reading and preservation

All 22 attribute definitions were read. The complete CSV was parsed for the disclosed fields and calculations; every numeric cell was not independently verified against an instrument record. Three bibliography page images—1, 2 and 4 of five—were inspected; full text extraction served navigation. No raw instrument, physical calibration, historical-temperature, custody or collapse test was performed.

Earlier evidence, conflicting records and shared registers remain unchanged. The original four-query repository search exposed this dataset route but recovered no W14B disposition or native attribution worksheet. No exhaustive public-record absence or withholding conclusion follows.

Raw CSV/PDF entities, full residual exports, private case/correspondence and personal/contact/signature data are excluded from this separate local publication candidate. No new push, PR, outreach, request, fee, source overwrite, deletion or history rewrite occurred. Earlier pending public approvals are not expanded. [Open records](OPEN-RECORDS.md), [locators](CLAIM-LOCATORS.json), [checklist](CHECKLIST.md), [verification](VERIFICATION.json), [revision status](REVISION-STATUS.json) and [exact additions](TEXT-CHANGES.diff).
