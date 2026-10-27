# Collected-steel photographs: acquired sources, an alias control and open candidate records

October 27, 2026. Original-record work plan track 5, B188/H005 and AUD011/AUD016. This supplements the [June 2004 inventory comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/88831b1b5436958547c9399306ff3c60ad8e1baf/investigation/broader-evidence/steel-attribution-roots-2026-10-27/README.md) without changing its sources, conflicting attributions or unresolved questions.

## Actual acquisition

The current [official NIST repository page](https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations) links **Images of Collected Steel** to a [Collected Steel folder](https://googledrive.nist.gov/folders/1mO5PPh1ZyZafGUtWrzqhiaDwzTqyEPG-), redirecting to NIST's linked Google Drive collection. Its Photos branch has scanned-hard-copy, scrapyard, miscellaneous and sample-cutting folders. The official link and collection notice establish the agency-published route; they do not independently authenticate each photograph's historical custody or authorship.

**56 archive image file IDs were acquired unchanged:** all 50 listed `WTC001.jpg`–`WTC050.jpg` scans, four selected sampling/packing images, and the same named scrapyard example from two different folders. Their source entities total **40,908,936 bytes**, with **55 distinct SHA-256 hashes** because the two scrapyard copies match. The scan subset alone totals **37,796,640 bytes**. These are file/byte counts, not counts of independent specimens, witnesses, photographic exposures or evidentiary confirmations. `IMAGE-SOURCES.json` supplies every acquired file's canonical URL, hash, size and acquisition time.

All 50 scan files are **3456 pixels wide**, with five recorded height groups: **2484 (1 file), 2490 (2), 2501 (4), 2502 (33), and 2508 (10)**. These are different scan files; variation in their raster sizes is not itself an inconsistent description of one file. The viewed pages show mounted-print composites, including a two-print last page. They are the archive's JPEG entities, not authenticated camera originals, negatives or a complete intake-photo archive. Source bytes and redundant aliases remain in the verified local media store.

## A directly inspectable sampling and alias control

Within the folder [WTC_05-16-02 (Cutting Large Pieces for Boulder)](https://drive.google.com/drive/folders/1P9UugcRWc_WyZDnr3mOmhcmrBYLxE-8A), three acquired files show a marked N8 member, cutting activity and a detached section:

| Exact archive file | Observation from the viewed image | Limit |
|---|---|---|
| [N8-C3B1 uncut#1.jpg](https://drive.google.com/file/d/1V024MWbvD1jUiXLSsHVEWHGM4DZ3GkBL/view) | Painted **N-8** and **M-7** occur on the member; a sampling outline/annotation is visible. | The filename's uncut label concerns the selected sampling operation. Other older cuts and damage are visible; it does not mean the whole recovered member had never been cut. |
| [Cutting of N8-C3B1 #1.jpg](https://drive.google.com/file/d/1t3V_wgjZWYzG58nR1XouR27-3WPdmP7m/view) | A worker uses a torch on the marked N-8 member. | No person is identified here. The scene does not establish the cause or timing of all other damage. |
| [N8-C3B1 cut#1.jpg](https://drive.google.com/file/d/1ln8oE8zTeRb5HBpbdmHa7gWqnAYDfTTd/view) | A detached section bears **N8 (M7)**. A handwritten line appears as **C1 A142**, followed by **97–100**; those smaller characters are a qualified visual transcription. | These annotations are not an independent construction-origin authentication. The source JPEG has no EXIF returned by the inspection used here. |

The final inventory lists **N-8 or M-7**, with assigned building **WTC 1**, column **142**, floors **97–100**: [NCSTAR 1-3B, physical page 92 / printed 64, Table A-1](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3b.pdf#page=92). The visible alias pair and the inventory entry agree. This supports a specific archive-to-identifier and sampling-scene association, rather than relying only on the report's generic description of photography. Common analyst attribution may underlie both the photograph's writing and the table; they are not independent confirmations of original building location.

An inspection crop of the cut photograph uses native coordinates **x=1000–1600, y=1100–1536**, with an upper-left origin. It is a derived reading aid, not a source replacement or measured physical geometry. The original JPEG is unchanged. The earlier, narrower crop clipped part of the annotation and remains preserved alongside the wider crop.

The fourth selected file, [Pieces on pallet #1.jpg](https://drive.google.com/file/d/1EmJ8kilTXiLvZSubr6o3mnfDYX-JCAqS/view), shows pieces on a pallet. The folder title indicates a Boulder-related purpose. The image does **not** establish a shipment date, completed transport, receiving signature, exact packing list, or the identity of every piece. No depicted pallet piece is silently equated with the N8 section.

The folder-name date is an archive label. It is not a calibrated camera timestamp or a signed date-of-cutting record. The photographs support some post-recovery sampling activity, not a general conclusion about every cut, every lost specimen or the collapse mechanism. This control concerns N8/M7; no join to W14A/W14B, C12a/b, FEMA Sample 1 or Column 79 is established.

## Readable tags and a failed automated exclusion method

Six scans were viewed individually, and all 50 were overviewed through five clearly marked derived contact sheets. Four directly viewed label controls were selected **after acquisition**, not preregistered as an accuracy study:

| Archive scan and inspected region | Visually read handling tag | Inventory locator |
|---|---|---|
| `WTC005.jpg`, lower-left photograph | **C-14** | Physical 87 / printed 59, Table A-1: **C-14 or S-18**. |
| `WTC009.jpg`, upper-left and lower-right photographs | **C40** | Same page: **C-40**. |
| `WTC037.jpg`, upper-left photograph and paper label in the upper-right | **N8** | Physical 92 / printed 64: **N-8 or M-7**. |
| `WTC040.jpg`, paper label in the upper-right and associated painted mark | **N-11** | Physical 92 / printed 64: **N-11 or M-9**; physical 94 / printed 66, Table A-4 lists it among unidentified exterior panels. |

Full file URLs and SHA-256 values are in `IMAGE-SOURCES.json`; the [inventory PDF](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3b.pdf) is pinned in `CONTEXT-SOURCES.json`.

The N-11 example makes a useful distinction visible: a recovered piece can carry a handling identifier while its original building position remains unidentified in the published inventory. A sample ID and a construction-origin identification are different records. This does not supply the missing W14A/B rationale or establish that either field attribution was wrong.

Tesseract **5.5.2**, one unrotated `--psm 11 -l eng` pass, returned exit code zero on all 50 scans but **missed all four visually readable control tags** under the recorded rules. Much of its output is noise. Successful execution is not successful label recognition. The absence of a W14A/B match in this OCR output has no dependable exclusion value. No claim that the candidates are absent from these images or the larger collection is made. The exact OCR output, control rules, scan hashes and script are preserved separately from visual observations.

## Metadata and duplicate qualifications

Pillow's EXIF reader returned no EXIF fields for all 50 scanned JPEGs and the four selected sampling/packing JPEGs. This is a bounded metadata observation, not proof that no other metadata format exists, that camera originals lacked timestamps, or that anyone removed metadata deliberately. Scanning and subsequent export are untested possibilities. XMP, original negatives and historic camera settings were not reconstructed.

The acquired `DSCN1291.JPG` from each of the two Scrapyard folders has **75,948 bytes** and SHA-256 **34f6cf81cc7cf9d24ab9693fe4561c99439251bb1342ec21448178159e4bf23a**. Both copies remain preserved. One image's IFD0 EXIF reports Nikon E990 and `DateTime` **2002:07:10 07:01:14**; no clock calibration is established and this is not asserted to be a January 2002 candidate photo. All 18 returned names and sizes match between those two folder listings; only this one pair was byte-compared. The two folders must not be counted as independent photographic corroboration merely because their paths differ.

## Coverage, publication and outstanding originals

The miscellaneous folder and one inspected cutting subfolder each returned the connector's **100-child limit**. Their complete contents were not enumerated. Two metadata-search pages returned no permitted results but supplied continuation tokens; pagination was not exhausted, so those searches are not negative folder censuses. A browser showed a different partial alphabetical slice of the miscellaneous folder; attempted navigation timed out. These are access/coverage limits, not evidence of missing, withheld or deleted images.

The public packet contains original research notes, source links/hashes, selected metadata, listings, preserved OCR output and reproducible inspection code. Raw photographs and contact sheets remain local because the collection notice does not establish redistribution rights for every underlying photograph. NIST's publication of a file and copyright permission to republish it are distinct. No Drive files were created, changed or shared.

Still required for the selected WTC 7 candidates are the original January 30, 2002 W14A photographs **68–73**, W14B photographs **63–67**, and January 21 C12a/b photographs **40–45**, with their photo index/camera or negative provenance; candidate-specific NIST intake/alias/transfer/coupon records; measured-geometry/drawing comparisons and attribution decisions; and the actual DOC-NIST-2013-001311 request/response file. No recovered image has been authenticated as one of those precise field series in this pass. FEMA's WTC#7 labels and NIST's unidentified entries remain intact and unresolved.

This pass acquires photographic source material and tests one alias/sampling control and the OCR method's limitations. It performs no new metallurgy, source-clock calibration, custody certification or WTC 7 simulation. The other four work-plan tracks and their missing originals remain open. Earlier reports and the shared master list are unchanged.

## Correction caught during verification

The first draft generalized the 3456 × 2502 dimensions of the first two acquired scans to all 50. The first verifier then failed on WTC007.jpg (3456 × 2501), exposing that unsupported generalization. The complete saved inspection shows the five groups above. The earlier draft and checker are retained under `drafts/`, and `DIMENSION-CORRECTION.diff` records the report and checker changes. The new check compares each JPEG with its own captured dimensions and the full recorded distribution. It does not normalize images, change any source, adjudicate historical evidence, or relax a user requirement that images share one resolution—there was no such requirement. An empty redirected output from the failed verifier is not treated as a valid result.
