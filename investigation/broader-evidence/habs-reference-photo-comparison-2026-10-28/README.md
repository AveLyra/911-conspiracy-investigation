# HABS photographs: matching scene content, different digital reproductions; custody still unverified

October 28, 2026. Existing STL01–STL04 / B188-H005 / AUD011-AUD016 / SPT01–SPT08 / SR01; follows IDR06 and HBR02/HBR03/HBR05. This acquires and inspects four actual reference photographs, advancing beyond the earlier caption-only comparison. The earlier report's unperformed-test statement remains preserved as its creation-time status; it is not silently rewritten.

## What changed

A documented **legacy Library of Congress catalogue API succeeded**, although earlier modern-page reader requests failed. The parent catalogue and two resource listings are now preserved as actual response entities, not only indexed snippets. The parent resource response lists 103 results and the child lists 26; only the four relevant image bodies were acquired. [Metadata source pins](METADATA-SOURCES.json).

The acquired JPEG reference views total **432,606 bytes**. All four were viewed in full at their available 640-pixel height. Each source's original bytes, SHA-256, dimensions, decoded-RGB hash, exact URL, catalogue item and field-specific metadata are preserved in [SOURCES.json](SOURCES.json). No raw image, negative or catalogue response is included in this publication candidate.

| Proposed pair | Parent reference | Child reference | Source subject |
|---|---|---|---|
|Paint detail|[NY-6369-31](https://www.loc.gov/pictures/collection/hh/item/ny2014.photos.362115p/), 529×640|[NY-6369-A-26](https://www.loc.gov/pictures/collection/hh/item/ny2396.photos.387822p/), 511×640|Captioned J3/10, B2|
|Smoke detail|[NY-6369-29](https://www.loc.gov/pictures/collection/hh/item/ny2014.photos.362113p/), 527×640|[NY-6369-A-21](https://www.loc.gov/pictures/collection/hh/item/ny2396.photos.387817p/), 512×640|Captioned J4/12, B2|

The intended pairs show closely matching column, surface, cable/netting or surrounding structural details. Their borders and reproduction labels differ; some border writing is partly obscured or too small to read confidently. No hidden text was reconstructed. **Both original-file hashes and both raw decoded-pixel comparisons differ.** Thus the delivered files are not identical, even though the pictured scene content strongly overlaps. Crop, scan, reproduction and different-exposure possibilities are not adjudicated by those hash differences.

## Reproducible, limited image comparison

The [method](IMAGE-COMPARISON-PROTOCOL.md) was saved before numeric results. It uses grayscale conversion, equal fractional crops and bicubic resizing to 256×256 in memory, then bounded translation of a 224×224 comparison region. It fits and evaluates the same pixels. No transformed source file is written. These are descriptive similarity calculations, not a probability of authenticity or independently validated exposure identification.

At the predefined 10% margin:

| Comparison | Centered Pearson r | Best translated r |
|---|---:|---:|
|31 versus A-26|0.672398|0.788351|
|29 versus A-21|0.733800|0.790636|
|31 versus A-21, cross-column control|0.095433|0.203774|
|29 versus A-26, cross-column control|0.100430|0.166423|

Across 5%, 10% and 15% margins, intended-pair best correlations were **0.783561–0.792821**; the two cross-column controls were **0.145388–0.203774**. Identical-source controls returned 1.0 at zero shift. These six intended, six cross-column and six identical-source calculations are not eighteen independent historical tests. Four source-byte/dimension/decoded-pixel checks also passed. [Actual results](RESULTS.json); [standalone verifier/comparison](compare_reference_images.py).

The cross-column controls are limited: some best offsets reach the allowed search boundary, and different photographs of the same static scene were not used as a validated alternative population. Resizing also changes aspect geometry. No universal threshold, confidence percentage or same-negative conclusion is justified. A larger negative/exposure corpus and original film identifiers could weaken or strengthen the reuse interpretation.

The defensible inference is that the two catalogue-number pairs represent highly overlapping photographic content and should not be assumed to be independent damage observations. **Whether either pair is the same original exposure remains unverified.** Distinct catalogue labels do not by themselves prove distinct exposures; visual similarity does not by itself prove one negative.

## What remains separate

The catalogue now explicitly supplies the N1200 field-material locator, but those field records remain unacquired. Source fields report 2004 as the photo-date label, while backend created/modified and source-created fields contain different dates. Preserve them by field name; they are not treated as interchangeable exposure, submission or digitization dates. The earlier HAER/HABS caption-label and October 2004/2006 inventory accounts remain untouched.

These photographs do not establish which parts were cut or transported, whether they match the two columns described among four Hangar 17 remnants, or whether a NIST candidate came from either location. Component material, coating, calibration and cut/transfer/object/sample records remain necessary. No join to W14A/B, C12a/b, Sample 1 or Column 79 is established; WTC6 substructure and WTC7-adjacent geography remain separate. A photographic paint description is not a calibrated temperature or incendiary identification.

The next decisive records are original negative/exposure identifiers and contact sheets, N1200, caption/reproduction history, selected-column drawings/material/coating records, and cut/mark/removal/transport/intake registers. The actual inventory editions, August 2005 submission/receipt and NIST attribution rationale remain missing. [Remaining records and falsifiers](OPEN-RECORDS.md).

This local addition does not close the FAA correction/disposition, telephone native call-leg/schema/custody, recorder clocks/configuration, materials specimen/calibration or steel native-custody requirements. No outreach, request, fee, mailbox, source overwrite, history rewrite, public push or PR occurred. The preceding two steel commits and their pending 24-file approval request are unchanged; that request does not cover this separate addition. [Checklist](CHECKLIST.md), [exact locators](CLAIM-LOCATORS.json), [revision status](REVISION-STATUS.json), [addition diff](TEXT-CHANGES.diff).
