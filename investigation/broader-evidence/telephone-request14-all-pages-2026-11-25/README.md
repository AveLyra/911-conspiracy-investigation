# Request 14: all 28 same-position page comparisons

AUD016-A1 / TEL01–TEL04 · 2026-11-25. This extends the [four-page sample and single negative control](https://github.com/AveLyra/911-conspiracy-investigation/blob/5091e85dff207ec8eabb86150fe7ee437dbab49e/investigation/broader-evidence/telephone-request14-page-similarity-2026-11-25/README.md); it preserves the earlier sample and conflicting value readings.

## Test and result

The previously acquired [Commission archive member](https://archive.org/download/911datasets/NARA_9-11_Commission_Records_Released_Jan_14_2009.zip) is a 28-page PDF, SHA-256 `957eecd527e1f1ee56867704b630c81edb766e76b8519b95abb5e660ac335f20`. The [previously reviewed public-reader copy](https://github.com/AveLyra/911-conspiracy-investigation/blob/dfed2c22cd6a6f58d77af80c8d3865fd3032baab/investigation/broader-evidence/telephone-full-row-comparison-2026-10-28/README.md) consists of 28 saved JPEGs. This run checked the PDF hash and all **28/28** reader JPEG hashes against the earlier acquisition manifest.

Using the prior method—PyMuPDF 1.27.2.2 rendering at a 2× matrix, grayscale, Pillow 12.0.0 Lanczos resizing and NumPy 2.3.4 pixel Pearson correlation—we compared each PDF page with its same-number reader page and with the next reader page, wrapping page 28 to page 1 as a control. In **28/28** pairs the same-position correlation exceeded its adjacent-page control. Same-position correlations ranged **0.6824–0.8322**; adjacent controls ranged **0.0232–0.2355**. The [full 56 numerical comparisons](ALL-PAGES-RESULTS.json) are supplied, including mean absolute intensity differences. The tests do not expose page contents.

The result is consistent with substantial positional overlap, so the two copies should not be treated as independent evidence of the telephone events. This metric is sensitive to resampling, contrast, layout and blank areas; adjacent pages may themselves share templates. It does **not** prove pixel or byte identity, identical redactions or text, source chronology, who created either copy, or whether the 28-page objects represent the 50 enclosures described in the cover. It is not a visual or content audit of every page. No formal similarity threshold was established.

Earlier readings remain: low-resolution **130** and possible **138**, archive-image **138** in Duration Connect, FBI interview-reported **138 seconds**, and briefing **0 seconds**. A related FBI interview describes Connect as setup time, but default handling, actual event joins and the briefing source worksheet remain open. This image-comparison test does not resolve the values, prove a conversation or show falsification.

## Reproduction and TODOs

Run `python3 compare-all-pages.py /path/to/archived.pdf /path/to/reader-image-directory READER-HASHES.json` with the exact preserved files, PyMuPDF/Pillow/NumPy versions above and Python 3.13.7. The script verifies hashes and prints only metrics. Images, PDF and sensitive payment/contact data are not included here. The supplied [reader hash manifest](READER-HASHES.json) is a non-sensitive subset of the earlier source manifest, not a new provenance claim.

- [ ] Check individual page content and redactions where material; similarity cannot certify their equivalence.
- [ ] Obtain the complete agency-native Request 14 delivery, attachment and production manifests, and version/custody information.
- [ ] Obtain native carrier data, field/failure rules and the source-to-briefing and exhibit worksheets. No agency outreach or request was made in this step.
