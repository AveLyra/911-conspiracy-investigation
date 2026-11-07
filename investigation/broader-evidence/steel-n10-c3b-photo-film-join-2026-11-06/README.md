# N10-C3B in the photo archive, NIST report and steel film

Public derivative of the November 6, 2026 steel archive review · STL02–STL03 / T23-03 / AUD011 / AUD016 / B188 / H005. The public archive supplied the two named JPEGs for **N10-C3B** and **N10-C3M**. Both match their respective views in NIST Figure B–32. The saved film frame independently shows the **N10-C3B** handling identifier from a different angle. The film and photograph are joined at the identifier level. A physical custody join requires further evidence.

## Source observations

| Record | Observation |
| --- | --- |
| [N10-C3B archive photograph](https://drive.google.com/file/d/1BN8cuz5mbLP_zHp9EvOjBILdwIYPMsQe/view), zero-based catalog row 805 | The acquired JPEG is **748,330 bytes**, **2,272 × 1,704**. Its visible upper marking reads **N10-C3B**. A second chalk line corresponding to the uncertain line in the film is not readable in this view. |
| [N10-C3M archive photograph](https://drive.google.com/file/d/1qqUbzPIj8begxjNM1jsl0mVw7X6K04CW/view), catalog row 804 | The acquired JPEG is **665,120 bytes**, **2,272 × 1,704**. It shows the neighboring **N10-C3M** marking and provides a within-panel comparison. |
| [NCSTAR 1-3C Fig. B–32(h–i), PDF p. 108 / printed p. 392](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3cv2.pdf#page=108) | The page face labels **N10-C3B** as **WTC 1, column 114, floor 90**, **Type C**, **Seat Detail 5110**, and says its gusset plate was ripped off at the weld. **N10-C3M** is labeled **column 114, floor 91**. The parent panel is **N-10 (A115: 89–92)**. The panel and connector column fields describe different objects. In the held PDF, extracted line 15 retains only part of the C3B label. The page face supplies the full label. |
| [WTC Tape 2-3.mov](https://drive.google.com/file/d/1UzY8uR-jH_pmgTzRPok5zgrvB7xfZ4iw/view), prior decoded frame 09 | The frame is **640 × 480**, decoder-input index **8440**, reported presentation time **563.229897 s**. It shows the **N10-C3B** marking, a diagonal mark and a lower line previously read as **B-1/8-1**, uncertain. The film angle and visible background differ from the archive photo. The lower line remains unresolved. [Prior frame and extraction record](https://github.com/AveLyra/911-conspiracy-investigation/blob/da9fd9dfb7d1af87c88143b0148914439420c4cd/investigation/broader-evidence/steel-tape2-3-source-2026-11-03/README.md) |

The two anonymous public downloads returned HTTP 200 and matched their catalog lengths. Pillow reports no EXIF entries in either file. The catalog's 2019 object timestamps are distinct from camera capture dates. The PDF face was read directly in the previously acquired NIST copy. This advances the earlier report-index lead to a checked publication record. [Source pins and exact input hashes](SOURCE-PINS.json)

## Comparison of the report and archive views

Using the same method as the previous connector study, the verifier searched rotations in 90° increments, aspect-ratio-preserving scales and translations. It compared each of two fixed grayscale regions with both JPEGs. Rotating the matched JPEGs 270° counterclockwise aligns the chalk strokes, plate edges, surface marks and surrounding features with the printed views. The cross-pairs score lower. The small test is specific to these two views and supplies no general false-match rate. [Verifier](verify.py) · [Preceding photo-join study](https://github.com/AveLyra/911-conspiracy-investigation/blob/4f66546e4055b525a6493719225b497913123eda/investigation/broader-evidence/steel-c14-n99-connector-photo-join-2026-11-06/README.md)

| Report region | N10-C3B_1 | N10-C3M_1 |
| --- | ---: | ---: |
| B–32(i) | **0.9582** | 0.3830 |
| B–32(h) | 0.6559 | **0.9514** |

Each matched archive-and-report pair shows one underlying photographic view. The duplicate views and the associated caption may share the same handling identification. The film-to-still comparison was a separate visual reading of the same upper label in a different view. No multi-view geometric registration was performed. The film frame's byte hash matched the prior derived frame. This unit leaves the earlier **11,607 reported versus 11,606 decoded/read** values and the missing twelfth selected image separate.

## Deferred records and tests

- [ ] **T23-03 / STL02.** Obtain camera originals, film log, marking register, intact-panel overview images and dated intake/transfer records. Look for independent geometry and a legible lower marking across multiple film angles before using the label to establish physical identity and continuity.
- [ ] **STL03.** Obtain the construction drawings, connector worksheet, any cutting or coupon records and an accession-to-disposition history for N-10 and C3B. The publication provides an assigned location and condition. The original identification and preparation trail remains open.
- [ ] **WTC 7.** The two connector records describe WTC 1 material. W14A/B original attribution and custody remain separately outstanding.

The two acquired JPEGs and the existing film frame remain on the verified media store. Scope was those two photo bodies, the single saved frame and the two report regions. The public derivative contains source links, hashes, research notes and the verifier.
