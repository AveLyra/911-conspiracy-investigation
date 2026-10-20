# Comparison of the two UAF final report PDFs

The two public March 2020 UAF report files differ visibly on physical PDF page 91, printed page 78, containing Figures 3.3 and 3.4 about Column 79. The difference is not confined to metadata. All other 124 corresponding pages have identical extracted text and identical complete-page RGB pixels under the fixed 150 dpi MuPDF test. Additional internal differences remain recorded below; matching page images do not erase them.

Both originals are preserved unchanged, separately, with acquisition receipts and complete SHA-256 hashes. Neither is designated the correct edition. This comparison concerns the report files, not a rerun or validation of UAF's structural model and not a finding about NIST's conduct or the historical collapse cause.

## Source identities

The filenames below retain the exact distinction in the two download URLs. Fresh ordinary HTTPS GETs on October 18, 2026 returned complete PDFs matching both independently recorded historical size and hash pins.

| Observable | March2020 URL | March-2020 URL |
| --- | --- | --- |
| Preserved original | [march2020.pdf](sources/march2020.pdf) | [march-2020.pdf](sources/march-2020.pdf) |
| Exact source URL | [March2020 download](https://files.wtc7report.org/file/public-download/A-Structural-Reevaluation-of-the-Collapse-of-World-Trade-Center-7-March2020.pdf) | [March-2020 download](https://files.wtc7report.org/file/public-download/A-Structural-Reevaluation-of-the-Collapse-of-World-Trade-Center-7-March-2020.pdf) |
| Bytes | 45,196,602 | 45,194,303 |
| SHA-256 | `f3a001ab68dcc6b6e230456aac4729613740336796c1b2515671141589c38bfa` | `41dd3390627fac24c2bd696160c48f15e05d3213cc05325c4e4e89608df96d27` |
| Physical pages | 125 | 125 |

The 2,299-byte size difference remains part of the record. Both hashes also matched after the complete comparison and its repeat. The earlier source-access and prospective-protocol records are unchanged: public commits `57a69046` and `0a6d707e` respectively.

## Visible differences on printed page 78

Inspect the complete pages side by side, not just a cropped detail:

| March2020 | March-2020 |
| --- | --- |
| ![Complete page 91 from March2020](images/march2020-page-091-150dpi.png) | ![Complete page 91 from March-2020](images/march-2020-page-091-150dpi.png) |

1. Figure 3.3 has a substantially different presentation. March2020 shows a complete column illustration with labels and arrows inside a 626 by 433 pixel image resource and a soft mask. March-2020 uses a 218 by 429 pixel image resource without that mask; the complete page visibly includes a PTC Creo View Express toolbar fragment above a column whose lower portion is clipped. Labels and arrows are separately drawn. Both pages retain the same Figure 3.3 caption identifying Column 79 and the W14x730 section.
2. The labels describing the 2 by 26 inch side plates and the W14x730 shape are extractable text in March-2020 but not in March2020. They are visibly present in both. The extra extracted words therefore must not be reported as new engineering prose without the image context.
3. Figure 3.4 has the same 681 by 513 pixel embedded image data, compressed data and soft-mask hashes in both PDFs. Its placement changes by approximately 9.20 PDF points vertically. Its caption moves too. The underlying embedded image match is distinct from full-page equality: the full pages differ.
4. The Figure 3.3 and Figure 3.4 captions and printed page number remain textually the same. The preceding page's discussion of the side plate and girder is also textually the same in the all-page comparison.

This matters because Figure 3.3 illustrates a connection feature used in the report's criticism of NIST's proposed initiation sequence. Readers should be able to identify exactly which published illustration they inspected. The measured PDF differences do not establish that dimensions in a native model, calculations, numerical results or the underlying connection geometry were changed. A source publication history and original figure/export files would be needed to establish who changed what, when and why. Document metadata dates alone do not establish that history.

## Other differences retained

| Channel | Observation |
| --- | --- |
| Text | MuPDF exact UTF-8 extraction and, separately, NFC plus whitespace-collapse extraction differ only on physical page 91. Independent strict pypdf extraction also differs only on that page. Each parser is compared against itself across the two sources, not against the other parser's output. |
| Page images | All 125 pairs were rendered in original order at 150 dpi, RGB, alpha disabled, without registration, cropping or rescaling. Only page 91 has unequal decoded-pixel hashes. All page rectangles, media boxes, crop boxes and rotations match. |
| Decoded page drawing commands | Physical pages 6, 13, 91, 99, 102 and 103 differ. The complete command diffs are preserved. Pages 6 and 13 include different grouping of text-showing operations; pages 99, 102 and 103 include different font-resource identifiers. Their raw differences are retained even though extracted text and fixed-test pixels match. |
| Image resources | Page 91 is the only page with differing image data or placements after excluding xref numbers. Figure 3.3's image and mask differ; Figure 3.4's image and mask hashes match but its placement differs. |
| PDF information title | March2020: `A Structural Reevaluation of the Collapse of World Trade Center 7-March 2020`; March-2020: `A-Structural-Reevaluation-of-the-Collapse-of-World-Trade-Center-7-March-2020.pdf`. |
| Declared creation and modification fields | March2020: `D:20200326015004Z00'00'`; March-2020: `D:20200325034446Z00'00'`. These are file-declared fields, not independently authenticated publication dates. |
| Trailer identifiers | March2020 repeats `39BC147D765E707AD654734D03D88C74`; March-2020 repeats `FE59F6511539B25A967FB6801C996696`. Trailer `/Size` values are 1268 versus 1270, and root object references are 1164 versus 1161. |
| Objects | 1,267 versus 1,269 active nonzero xref slots; 601 same-numbered slots have different dictionary text, stream bytes or presence. This is a same-index inventory, not 601 independently changed scientific items: object references themselves differ. All entries, hashes and unequal dictionary texts are retained. |
| Streams | Each has 448 streams. Their decoded-hash multisets share 418 entries; each has 30 entries not matched in the other multiset. The unmatched dictionaries, xrefs and hashes are retained without treating this as an aligned count of altered figures. |
| Raw file structure | First 2,759 bytes and last 7 bytes are identical. Full-file lengths and hashes differ. These prefix/suffix observations are not a global edit alignment of the two byte strings. |

Both have a byte header declaring PDF 1.3 and a catalog `/Version /1.4`; both are reported as effective PDF 1.4. Their reported author, Word creator and Quartz producer match. Neither required repair or a password; neither exposes attachments, bookmarks, links, annotations or form widgets through the inspected interfaces. XMP metadata is absent in both. These equal observations do not cancel unequal observations in other channels.

## Verification and reproducibility

The prospective protocol is preserved in `frozen-protocol.json`; `prospective-extension.json` adds the object and resource inventory before document-content inspection. Acquisition receipts retain exact URLs, UTC times, response metadata, complete sizes and hashes. No PDF was repaired, rewritten or selected as authoritative.

Seven in-memory synthetic controls passed before real measurement: metadata-only changes, text changes, graphics-only changes, malformed and truncated sources, forced extraction failure, and repeatability. After the real measurements, all eleven control and acceptance tests passed. A second complete invocation reproduced all 125 page records, object inventories, differences and document records exactly; only the completion time in the summary changed. Independent pypdf text extraction covered all 125 pages. A second renderer, Poppler 26.05.0, also displayed the toolbar fragment and clipped column on March-2020 page 91; both complete MuPDF page 91 images and the representative cover page were visually inspected.

Reproduce in a Python environment with PyMuPDF 1.27.2.2 and pypdf (the exact used version and native-library hashes are recorded):

```sh
python3 -m unittest -v test_compare_pdfs test_results
python3 compare_pdfs.py compare --media /path/to/preserved/originals --results /new/results --rasters /new/raster/directory
python3 supplemental_checks.py /path/to/preserved/originals /new/results
```

`test_results.py` checks the supplied saved `results` and `repeat-results` directories. The comparison commands require new output paths and never overwrite either PDF. Actual code, outputs, receipts and manifests are retained beside this report. Large operational copies remain on the verified Intel media store, with redundant originals and page images tracked using Git LFS.

## Scope and open questions

The high-confidence findings are a reproducible page-level publication difference, different internal representations, and different declared metadata. Cause, responsible editor, public release chronology and any effect on native analysis remain unknown. Ordinary figure-layout/export changes and other editing histories are untested possibilities, not resolved explanations.

This records every difference found in the defined file, active-object, stream, resource, text and fixed-raster channels. It does not claim exhaustive equivalence of all possible PDF behavior or every discarded revision. In particular, equal 150 dpi pixels do not guarantee equality at every resolution, and same-numbered xref differences are not a semantic object-graph alignment. Both complete original byte sequences remain available for additional tests. No inference about deliberate concealment follows from these observations alone, and the comparison does not rank collapse explanations.

### Detailed records

- `results/documents.json`: metadata, trailer and document-level records.
- `results/pages.json` and `results/page-differences.json`: every page and changed-text records.
- `results/object-inventories.json` and `results/object-differences.json`: every inspected xref and all unequal same-index records.
- `results/page-resource-and-command-differences.json`: every page's image resources, placements and complete command diffs.
- `results/stream-multisets.json`: matched counts and all unmatched decoded-stream records.
- `results/independent-pypdf-text-check.json`: all-page independent text check.
- `repeat-results/`: complete second primary comparison.
- `verification.json`, `native-renderer-runtime.json` and `manifest.json`: actual checks, runtime and preservation hashes.
