> **Redacted historical receipt:** This copy omits one absolute local executable path. Original receipt SHA-256: `07d24740059d33b8e29e8792df6f454f546fdc6effb2471a2a3feb0737aa31b1`. It reports checks performed on 2026-09-11; they were not independently rerun for this publication. The original receipt and source media remain in retained local storage.

# Initial relevance-review coverage and reproduction receipt

Completed 2026-09-11. This receipt covers the initial NCSTAR 1-9 review only. The original report snapshot SHA-256 is `a73606443e106890875d5fd5a5a3bd7abc72c12b77938f880fae4de21fb00729`.

## Source identity

- Preserved source: `authority/nist/wtc7/ncstar-1-9.pdf` (repository-root relative).
- Independently recomputed SHA-256: `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.
- Acquisition date/HTTP custody was not re-audited; this task used an existing preserved public government report and made no web request. The hash establishes byte identity, not historical authenticity.
- Existing text aid: `fuel-system-audit/nist-source-review/derivatives/ncstar-1-9-pages.json`, SHA-256 `ff66c642761ade27ae993927a8343bf6a28d3390150e31be4fe58d56a3d9fbc7`. Its recorded source hash equals the recomputed source hash. Only the selected page objects were read, plus its schema/source metadata.
- Parent fuel-audit report lead snapshot: SHA-256 `ab2288d5dbf47960d36ee37e4e90ffc0b22400e9b235e4db9e3e2810d85c607e`.
- Parent equipment report lead snapshot: SHA-256 `b724674dbce14d75011eb1ed73ee4b7ba5980cd7345788c260bee486bffbbe7c`. Its opening paragraph is line 3; the relevant analysis is lines 35-46 in this snapshot. Those prose files were not treated as corroborating sources.

## Complete visual and text coverage

The whole images were inspected, including headers, figures, legends/captions, footnotes and page numbers. All displayed images were complete pages, reduced by the display from 1700x2200 to 1376x1780 pixels. Selected text was also read, and the initial physical 432-440 text was freshly extracted directly from the source with Poppler `pdftotext -f 432 -l 440 -layout ... -`. Printed-page mapping was checked in the images.

| Physical | Printed | Coverage | SHA-256 of existing and freshly reproduced PNG bytes |
|---|---|---|---|
| 432 | 366 | Section 9.2/9.2.1, Figure 9-1, footnote 2 | `79511ea0aed0a344eb24e75ef5ea5d02f6ede33356ec70161df1e3d4f31119ea` |
| 433 | 367 | Figure 9-2 complete plan and caption | `10b951a85ed929c90977152267ec63412cca5a474ed5b6219cc1be0324a0487f` |
| 434 | 368 | Geometry/visibility, Figure 9-3 and footnote 3 | `c9ce1d869873b1271eda9dc65e41f3962f7050faf3c2a41d5254a714b8803722` |
| 435 | 369 | Scenario Set 1 and complete Scenario 1a text | `dc5923925cf975efa8f3e9d0f1cc36dba4b79fb586c9e0030a50fc11d1bbf4e7` |
| 436 | 370 | Scenario 1b, Figures 9-4/9-5 | `258f1101601ffbcf19676194f2df0ac01069b0016a437ec2fd3b79449d7690f3` |
| 437 | 371 | Scenario 1c, Figure 9-6 | `9d930c52178192059335b94440e8a29894d39802580a24e38aec21338608996a` |
| 438 | 372 | Scenario 1c continuation, Scenario 1d, Scenario 2 | `ac4b1f9dae2733016da2933e248475a9f9da613f33f6008c389cfaac4231885d` |
| 439 | 373 | Figure 9-7, Section 9.2.2, footnote 4 | `f892460e1a68981551a2dc5b93409bd9778cdd653849793451249f57b4a9a5b7` |
| 440 | 374 | Section 9.2.2 continuation, summary 9.2.3, beginning of 9.3/9.3.1 | `1efd44e08f9b590f4bed2718bfb26b1bf4ad9d2a23d46151fe2cef103a6a0b83` |
| 679 | 613 | Chapter 13 sequence/sensitivity summary and beginning of Section 13.3 diesel discussion; supplemental selection deviation | `466ca08c470d144ca6e15bd7bb38dc7c961de851a9347a00bfae8e63e8d2c626` |
| 680 | 614 | Section 13.3 diesel continuation and beginning of blast discussion; supplemental selection deviation, blast content not analyzed | `cc6813beb1c8c5918ed7dbe8653dccc18019480c186e637b230c24d0b2df065b` |

Existing images are `fuel-system-audit/nist-source-review/derivatives/ncstar-1-9-physical-NNN.png`. Initial coverage was prospectively selected. The two Chapter 13 pages were also declared before reading, but the declaration incorrectly joined a Chapter 11 reference to the parent report's Chapter 13 locator; the [selection record](page-selection.md) preserves that deviation. No Chapter 11 content was independently inspected.

## Reproduction and retained failed methods

All 11 selected PNGs were freshly rendered in memory from the hashed PDF with Poppler 26.05.0 at 200 dpi using, for each physical page N:

```text
pdftoppm -f N -l N -r 200 -singlefile -png authority/nist/wtc7/ncstar-1-9.pdf
```

The executable was `[local executable path redacted]`. Standard-output PNG bytes were decoded with Pillow and compared against the existing PNG's RGB pixels. All 11 RGB comparisons were equal; all 11 freshly produced PNG SHA-256 values exactly equaled the existing PNG SHA-256 values listed above. No recreated source PDF or render file was written, and preserved images were not modified. This verifies the reviewed images' derivation from these source bytes; it does not verify the underlying engineering.

Earlier attempts are retained here to avoid overstating reproducibility: the bundled Python lacked `fitz`; system `python3` supplied PyMuPDF 1.27.2.2, but its 200-dpi renders had different RGB bytes from the existing images on every selected page. No claim of source corruption was made from a different renderer's output. Repeating with the available Poppler renderer produced the exact matches above. The fresh text extraction used Poppler `pdftotext` 26.05.0 and confirmed the selected source prose/page mapping.

The controlling files and three skill files were read completely before substantive source review. All new artifacts are working research within this reviewer directory. No confidential packet, original interview/transcript, raw acquisition/process log, legal file, external service or underlying solver input was inspected or changed. Computational-review independence and engineering limits are stated in the report.
