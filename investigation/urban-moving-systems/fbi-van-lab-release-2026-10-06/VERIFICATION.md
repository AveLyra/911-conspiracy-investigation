# Research verification

Checks performed October 6, 2026. These checks validate acquisition integrity, the stated search coverage, and pinpoint reading. They do not establish a chemical result or prove universal nonrelease.

## Acquisition checks

Original public PDFs were downloaded with commands of this form, preserving response headers:

```text
curl -L --fail --silent --show-error --max-time 60 -D <header-file> -o <local-file> <source-URL>
```

The six core files contain 141, 87, 100, 16, 141, and 94 PDF pages, totaling 579. Their MD5 digests match the corresponding original-file values in the retained Internet Archive metadata. SHA-256 digests and byte sizes are in source-manifest.json. A police report and 15 unique IRmep PDFs were also acquired, followed by the two NARA PDFs. The source register supplies the URLs.

An attempt to download the separate 2019 photo release from the public PDFCoffee download link returned HTTP 403. It was not a successful PDF acquisition, is not part of the full-PDF corpus, and was not bypassed. The accessible Scribd and PDFCoffee text previews were read as limited previews only.

## Text search and scan checks

The retained Internet Archive text PDFs were read using pypdf, producing separate page arrays and text with explicit PDF page markers. All six sections were searched. Representative actual searches included:

```text
rg -n -i 'explos|residu|laborator|chemical|swab|bomb|trace result|results of traces|discontinu|sample' /private/tmp/fbi-van-lab-release/derived/irmep-13-ocr.txt /private/tmp/fbi-van-lab-release/derived/irmep-14-ocr.txt
rg -n -i 'explos|residu|laborator|chemical|swab|bomb|trace result|results of traces|discontinu|sample' /private/tmp/fbi-van-lab-release/derived/irmep-[0-9]*.txt
```

The core-page concordance also searched `explos|swab|laborator|chemic|residu|vacuum` across the six page arrays. Broader laboratory, evidence, trace-results, and disposition searches supplied candidate pages. A keyword match was not treated as proof that a document concerned this examination.

Two IRmep documents initially contained no selectable text: the six-page Philadelphia Serial 357 and the 99-page New York Serial 221. All 105 pages were rendered and passed through local Tesseract OCR, with four concurrent OCR workers. The extraction command used these tools and settings:

```text
pdftoppm -r 120 -png <original-PDF> <image-prefix>
/opt/homebrew/bin/tesseract <page-image> stdout --psm 3
```

The 99-page source produced recoverable PDF stream-length warnings while rendering. It rendered 99 images and yielded 99 OCR page entries. The resulting text remains a derivative finding aid, with OCR uncertainty. Native text extraction covered the other IRmep files. The combined set contains 180 unique PDF pages, including the three-page cover letter, or 177 document pages. Repeated content and outside attachments are not separate agency findings.

Eight core pages initially had empty OCR: Section 5 pages 84, 97, 101, 102, and 123; Section 6 pages 13, 17, and 35. Each was rendered at 150 dpi, given a local OCR pass, and visually inspected in the retained contact sheet. They consist largely of blank/redacted filing pages and handwritten evidence covers. Section 6 page 13 refers to a handwritten letter and backpack; page 17 to a book. Sparse or absent text on these pages was not silently treated as clearance.

Original scan images were rendered with commands including:

```text
pdftoppm -f 52 -l 53 -r 120 -png /private/tmp/fbi-van-lab-release/raw/section-6.pdf /private/tmp/fbi-van-lab-release/page-images/s6-closing
pdftoppm -f 69 -l 71 -r 115 -png /private/tmp/fbi-van-lab-release/raw/section-5.pdf /private/tmp/fbi-van-lab-release/page-images/s5-lab
pdftoppm -f 36 -l 37 -r 115 -png /private/tmp/fbi-van-lab-release/raw/section-6.pdf /private/tmp/fbi-van-lab-release/page-images/s6-lab
```

Visual inspection verified the September 23 date and pending-results sentence; inventory date, item numbers, and barcodes; all three alleged chemical-result citations; the July 2003 discontinuation instruction and accompanying sample narrative; the video-examination specimen list and examination description; the notebook examination’s date and specimens; and the April 2004 and February 2005 property memoranda. The 2013 cover letter’s printed main-file notice was inspected separately; its paragraph-selection marking remains unclear and was not used as proof of a specific omitted file.

The source-register CSV records official log pinpoints confirmed through the public FBI source. The full determination letters and productions for the 2018–2023 logged requests were not acquired. The NARA finding aid and notice were read; the underlying electronic assets were not acquired.

## Public search coverage

Executed queries included Urban Moving Systems combined with laboratory, lab results, explosives, negative, release, FOIA, 2024, and 2025; the JRJ13Y registration with laboratory; the E01889035 barcode; Dancing Israelis combined with laboratory negative and lab results released; official FBI log searches; and individual request numbers 1423771, 1432694, 1481545, 1568844, and 1591512. Searches also sought requester-hosted productions, including MuckRock. Reposts of the same secondary article were not counted as independent confirmation.

No final chemical finding tied to this van or its evidence barcodes was located. The strongest competing lead was the claim of September 17 laboratory results, which was checked against its cited originals. A negative-test passage in a later outside attachment concerned another van in Washington state. Neither settled this test.

## Reproducible integrity check

The bundled Python runtime is `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`. The retained read-only verification program checks the file manifest, archive digests, page counts, and coverage of initially empty pages:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /private/tmp/fbi-van-lab-release/package/verify_sources.py /private/tmp/fbi-van-lab-release/package
```

The actual run result is retained in verification-output.txt. The same check is repeated on the saved worktree package after copying; its result is retained in the worktree verification record. A pass does not validate agency authenticity, unseen records, or the chemical outcome.

## Repository boundaries

The investigation checkout was created with:

```text
git worktree add /Users/admin/docs/911-worktrees/fbi-van-lab-release -b research/fbi-van-lab-release HEAD
```

Its base commit is c9d32e40d1deabc04277323f4eb2b40f1bbf7ba6. Creation emitted an unrelated pre-existing Git LFS pointer warning for a Sherlock score array. A subsequent `git status --short` in the new checkout was empty before saving this investigation; no repair of that unrelated file was attempted.

Only this investigation package and the worktree-local research/WORKTREES.md registration are written. No canonical fact, exhibit, correspondence, pleading, or main-checkout index was updated. No commit, push, merge, export to an external service, or outbound request was performed.
