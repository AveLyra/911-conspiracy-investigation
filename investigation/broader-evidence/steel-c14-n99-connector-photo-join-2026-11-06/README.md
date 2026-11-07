# Archive photographs for the C14-C3B and N99-C1B connector figures

Public derivative of the November 6, 2026 steel archive review · STL02–STL03 / AUD011 / AUD016 / B188 / H005. Three image files were acquired from NIST’s public collected-steel archive. Two show the same photographic views as the corresponding NIST report panels. The higher-resolution color files give exact photo targets for the connector custody trail. The test coupon and shipment links remain open. [NIST archive landing page](https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations)

## Acquired image entities

| Archive title | Held JPEG | Catalog locator |
| --- | ---: | --- |
| [SPANDRELS C14-C3B_1.jpg](https://drive.google.com/file/d/1a3o9lYrOzR6IOo91_tKhMBDPzR5tFWoz/view) | 411,609 bytes, 2,048 × 1,536 px | `files[882]` |
| [SPANDRELS C14-C3B_2.jpg](https://drive.google.com/file/d/1qOiB4hoqbzVzqfIZgVtdXZZ88haav85V/view) | 454,766 bytes, 2,048 × 1,536 px | `files[881]` |
| [SPANDRELS N99-C1B_1.jpg](https://drive.google.com/file/d/1MDN1SJPv6t23uHot1VN-KE4wZ1m7NaUE/view) | 726,380 bytes, 2,272 × 1,704 px | `files[742]` |

The catalog locators are zero-based in the previously held 1,000-row listing. Its hash was rechecked. Each direct public download returned HTTP 200 with a JPEG and the listed byte length. Pillow found zero EXIF entries in each acquired file. The image entities are released archive copies. Camera-original status and capture dates are unverified. [Download URLs, hashes and region coordinates](SOURCE-PINS.json)

## Photo-to-figure comparison

The verifier used two fixed report regions, rendered in grayscale at 0.45× page-point scale. For each region and each of the three archive files it searched four 90-degree rotations, aspect-ratio-preserving scales, and translations. The table gives the highest normalized grayscale correlation for each pair. This is a small comparison set, with one alternate view by filename and cross-item controls. It does not give a general false-match rate. The archive photos and figure regions were also compared visually after rotation. [Verifier](verify.py)

| Report region | C14-C3B_1 | C14-C3B_2 | N99-C1B_1 |
| --- | ---: | ---: | ---: |
| B–4(i), PDF p. 23 | 0.5956 | **0.9370** | 0.5437 |
| B–35(c), PDF p. 115 | 0.4732 | 0.4443 | **0.9463** |

- **C14-C3B.** After a 270° counterclockwise rotation of `_2`, the diagonal rod, curved plate edges, seat and hole shapes line up with Figure B–4(i). The archive `_1` file gives a different view. The figure identifies the pictured connector as **WTC 2, column 259, floor 86**, under parent panel **C-14 (B300: 85-87)**. The color image supplies no separate certification of that building assignment. [Figure B–4(i), PDF p. 23 lines 12–21](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3cv2.pdf#page=23)
- **N99-C1B.** After a 270° counterclockwise rotation, the outlined patch around the connector, the chalk identifier and the edge geometry line up with Figure B–35(c). The figure identifies the connector as **WTC 1, column 149, floor 100**, under parent panel **N-99 (A148: 99-102)**. Its note says Boulder had begun cutting before the photograph and that the damper unit was already removed. The match connects the visible state to the published note. The photo does not supply the cutting date, complete cut sequence or shipment history. [Figure B–35(c), PDF p. 115 lines 22–36](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3cv2.pdf#page=115)

**Evidence boundary.** These are photo-view joins. The high-correlation pairs should be counted as one underlying photograph per pair. The archive JPEG, grayscale report image and report caption remain separate records. The C14-C3B connector is a different component from the reported **C14-C1-RF** flange and **C14-SP** spandrel test specimens. Preserve the connector appendix’s column **301** recovery wording and the test report’s **301** flange assignment side by side. The archive connector photos supply no original cut plan, receipt or sample crosswalk to adjudicate those statements. [C-14 specimen review](https://github.com/AveLyra/911-conspiracy-investigation/blob/89444d152c05a6e3b0f740402adbb44647a89582/investigation/broader-evidence/steel-c14-panel-to-test-trace-2026-11-06/README.md)

## Open records and next test

- [ ] **C-14 / S-18** · Seek the original C14-C1-RF and C14-SP cutting plans, labelled pre/post views, accession card and dated sample receipts. Compare against the recovered panel diagram and the named connector photos, testing where each flange or spandrel sample came from.
- [ ] **N-99 / M-16** · Seek original pre-cut images, date and operator/office record, the N99-C1B preparation worksheet and Boulder intake. Match the photographed outline and recorded damper removal against a dated cut plan. Keep the July 2002 shipment linkage open.
- [ ] **WTC 7** · Continue to seek the W14A/B tag images, aliases and attribution worksheets. These two connector photos concern WTC 2 and WTC 1, respectively.

The three raw JPEGs are retained in the verified media store. The public derivative contains research notes, source pins and code. Verification covers the three JPEGs, the previously held PDF, the fixed image regions, and six candidate comparisons. It supplies no independent camera chronology or metallurgical test.
