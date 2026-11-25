# Request 14 copies: selected page-image similarity

AUD016-A1 / TEL01–TEL04 · 2026-11-25. This is a bounded source-dependence test following the [new archive acquisition](https://github.com/AveLyra/911-conspiracy-investigation/blob/12f56e7554306cebd6998979492c00e602d610bb/investigation/broader-evidence/telephone-request14-archive-office-call-2026-11-25/README.md). It does not adjudicate any duration or identify an original carrier record.

## Method and observations

We compared four corresponding rendered pages from the 28-page [2009 Commission archive member](https://archive.org/download/911datasets/NARA_9-11_Commission_Records_Released_Jan_14_2009.zip), PDF SHA-256 `957eecd527e1f1ee56867704b630c81edb766e76b8519b95abb5e660ac335f20`, with the previously saved public-reader JPEGs documented in the [earlier source review](https://github.com/AveLyra/911-conspiracy-investigation/blob/40fed9bab3fa93b8a929f1210580750a1d8f63dd/investigation/broader-evidence/telephone-gte-box13-public-reader-2026-11-06/README.md) and the [full-row comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/dfed2c22cd6a6f58d77af80c8d3865fd3032baab/investigation/broader-evidence/telephone-full-row-comparison-2026-10-28/README.md). The PDF was rendered with PyMuPDF 1.27.2.2 at a 2× matrix, converted to grayscale and resized to each reader image's dimensions with Pillow 12.0.0 Lanczos; NumPy 2.3.4 computed pixel Pearson correlation and mean absolute intensity difference (0–255). One deliberately mismatched pair is a negative control. This is a fixed, unregistered image test; resampling and contrast affect scores.

| PDF page | Reader page | Correlation | Mean absolute difference |
| ---: | ---: | ---: | ---: |
| 1 | 1 | 0.6959 | 8.176 |
| 25 | 25 | 0.8230 | 9.407 |
| 27 | 27 | 0.7883 | 7.608 |
| 28 | 28 | 0.7865 | 3.880 |
| 25 | 28, mismatched control | 0.0744 | 19.400 |

The four selected same-number comparisons are more similar under this metric than the one mismatched control. This is consistent with overlapping page content and cautions against counting the copies as independent call evidence. It does **not** prove byte identity, a parent-child relationship, which party made either copy, equality of all 28 pages, or a specific scan or redaction history. A single negative control does not establish a general classification threshold. A source-to-production manifest remains necessary.

The earlier 50-enclosure cover description and 28-page archive and reader observations remain separate. This test cannot identify which pages are missing, why counts differ or whether the original response was complete. It also leaves the earlier **130 / possible 138** reading, visually read **138** in the archive page's Duration Connect field, FBI interview **138 seconds**, and briefing **0 seconds** unchanged. These values may concern different fields or events; no semantics or cause is resolved here.

## Reproduction and limits

The four reader JPEG SHA-256 values, rechecked against the earlier source manifest, are: page 1 `768e2958ead0b39867d197fd5350a8505944139b9edbb88c415f02bc8c693fc9`; page 25 `52264933cdb47bef34b2ed6d0a8721f8ae0480820f5b36371cb7f3c693b0969d`; page 27 `48e329bd0e7136c6a6aa2187c76e471d3da34b22a2df2ebb7a7965455a6cc9a4`; page 28 `6f0622a3663d5eb3349a8b995fd3753b06054e2cedd92df1932a3eedf7bb060b`. The PDF was acquired and hashed in the preceding archive step. The first attempted script run used a Python environment lacking PyMuPDF and failed before computing results; rerunning with Python 3.13.7 and the versions above produced the table. The script itself does not verify input hashes.

Run `python3 compare-page-similarity.py /path/to/archived.pdf /path/to/reader-image-directory`. The directory must contain the previously preserved `reader-page-01.jpg`, `reader-page-25.jpg`, `reader-page-27.jpg` and `reader-page-28.jpg`. The script prints only page numbers and metrics, not page contents or sensitive fields. Results depend on the exact image copies and software versions. The source images and PDF contain payment/contact data and are retained in research storage rather than published in this bundle.

- [ ] Compare the remaining page content, labels and redactions where appropriate; do not imply this sample covers them.
- [ ] Obtain the agency-native complete Request 14 delivery, attachment manifest and production/version history; obtain carrier field definitions, source-to-briefing records and native event data.
- [ ] Keep previous contradictory readings and each copy's provenance intact.

No original dispatch, native carrier export, message content, or evidence of suppression was established; no outreach or request was made.
