# Normalization follow-up: fit-selection limits and a figure/export question

October 28, 2026. Existing STL01–STL04 / SPT01–SPT08 / B188-H005 / AUD011-AUD016. This adds source-based qualifications to the conditional CSV calculation. Earlier records and every original value remain unchanged.

## Source acquired

The cited DOI supplied the currently hosted [NIST TN1714 report](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.1714.pdf): **6,682,019 bytes / 137 pages**. Eight selected page images were inspected. Its citation year is 2011 and HTTP Last-Modified date is 2015; neither authenticates unchanged 2011 bytes. [Hashes and source relationships](SOURCES.json).

Physical pages 9–10 / printed 7–8 describe a generic-steel model, distinguishing retained yield, post-yield hardening and rate sensitivity. That stated purpose matters when interpreting mixed literature/WTC-test data. The earlier 688/68 counts are not a fraction of recovered material released or proof all rows entered the same fit.

## Reported baseline and conditional row

[Figures 1 and 16](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.1714.pdf#page=11) label C65's room-temperature yield strength **226 MPa**. Table 6 lists varying room-temperature measurements. In the later CSV, six lower-rate C65 rows have descriptive mean **225.9 MPa**, with FY20=226; the separate higher-rate row has FY002=223.4 and FY20=223. Keep these scopes separate. A mean's proximity is an exploratory pattern, not recovered proof of an author baseline rule.

Line 717 remains **RFy=1, FY002=263.5, FY20=226**; its simple quotient remains **1.165929…**. The source now supports a group/series baseline question. It does not establish that each individual replicate's RFy must equal its own FY002 divided by the listed FY20. No source value or explanation is selected or corrected.

## Fit selection is disclosed

At [physical 38 / printed 36](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.1714.pdf#page=38), Table 6 contains a C65 row: T=20, rate=8.75×10⁻⁵/s, yield=264 MPa, 2%-strain strength=370 MPa, tensile strength=469 MPa, elongation=38 and reduction of area=63.1. Its **lm flag is 0**.

With an explicit tentative C65-to-C65_FL cross-reference and 0.5 MPa precision allowance for 264 versus 263.5, one CSV row matches this selected tuple: line 717, Sample C65H-.5-L1. Both original numbers remain. This is a candidate numeric association, not independently authenticated coupon identity or an original export manifest.

The table defines lm as inclusion in computing **Equation 10 stress–strain parameters**. Zero marks non-use for that fit. It does not prove exclusion from retained-yield analysis, Figure 2, every model or the 2005 collapse calculation. The CSV has no lm field. It cannot alone reconstruct the fit's inclusion decisions, and its conditional discrepancy cannot by itself establish an error that entered a collapse model.

## Figure/export relationship remains open

The current [Figure 2, physical 12 / printed 10](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.1714.pdf#page=12), visibly has green This-study points above and below unity near the room-temperature end. This is qualitative: no point was digitized or assigned to a coupon. Meanwhile, **all 22 current This-study CSV rows at T=20 have RFy=1**. Both records are retained.

Of all 68 This-study CSV rows, **47** meet the figure caption's literal rate interval, 3.30×10⁻⁵ < rate < 1.35×10⁻⁴/s; **21** do not. The body separately allows values within or slightly outside standards' ranges. No precise filter is invented from that allowance, and the 21 are not declared erroneous. The later compilation's multiple-figure/edition scope is also retained. Exact point lineage and when or why a representation changed remain unverified.

Replicate aggregation, separate populations/fit selection and export/version conventions are competing possibilities. This source qualification weakens any inference that the earlier quotient alone proves faulty NIST science; it neither erases the values nor authenticates the missing pipeline.

## Next records and limits

Obtain normalization worksheets/code, baseline coupon/series identifiers, original figure data and selection masks, lm/export mapping and dated revision/delivery records. These can distinguish an intended representation from an unsupported transformation or transcription. Original machine curves/calibration remain missing.

The report was read at physical pages **1, 9, 10, 11, 12, 38, 39 and 43**. No physical, custody, historical-temperature or collapse experiment occurred. W14A/B disposition/attribution, native inventory/transfers and the FAA, telephone, recorder and Harrit/Millette input/test requirements remain open.

Raw report/rasters/extractions and private case/correspondence are excluded from this separate local candidate. No push, PR, message, outreach, fee, source overwrite or history rewrite occurred; earlier pending approvals are unchanged. [Locators](CLAIM-LOCATORS.json), [observations](OBSERVATIONS.json), [code/results](RESULTS.json), [checklist](CHECKLIST.md), [reading scope](READING-SCOPE.json), [revision status](REVISION-STATUS.json) and [exact additions](TEXT-CHANGES.diff).
