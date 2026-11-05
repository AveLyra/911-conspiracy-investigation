# Release 32 catalog links for the W14A, W14B and C12 field photographs

Public research copy. [Source URLs, hashes and catalog paths](SOURCE-PINS.json).

November 5, 2026. STL02–STL03, SPT01–SPT08 and B188/H005. This archival catalog test follows the exact photo indices identified in the [earlier attribution review](https://github.com/AveLyra/911-conspiracy-investigation/blob/88831b1b5436958547c9399306ff3c60ad8e1baf/investigation/broader-evidence/steel-attribution-roots-2026-10-27/README.md). It identifies release paths for all 17 requested photo indices. Image inspection and physical-origin tests remain open.

## What matches the FEMA field references

The Internet Archive's compressed-copy item lists **42A0375 - G33D9.rar**. Its supplemental Release 32 file manifest enumerates the expanded paths under the same disc identifier, including **WTCI-102-I -GMS-CD#8-Multiple STEEL**. I fetched the manifest over HTTPS and parsed it as a local catalog. Its SHA-1 matches the checksum in the archive metadata. The complete manifest contains **58,466** file paths. The target disc contributes **725**, all in the named WTCI-102-I directory. Of these, **345** are under `Claremont`. [Archive item metadata](https://archive.org/metadata/nist-foia-09-42-r32) · [Supplemental manifest](https://archive.org/download/nist-foia-09-42-r32/Supplemental%20Files/International_Center_for_911_Studies_NIST_FOIA_-_Release_32.torrent)

| FEMA Appendix D physical p. 16 | Field date and indices | Catalog filenames | Catalog structure |
| --- | --- | --- | --- |
| Row 20, **A or W14A** | Jan 30, 2002, **68–73** | `CM-pieceW14A-01-30-02-photo68-byDK.jpg` through `photo73` | `Claremont/AA-HH-W14A&B/_W14B 2002-01-30/_W14A 2002-01-30/` |
| Row 21, **B or W14B** | Jan 30, 2002, **63–67** | `CM-pieceW14B-01-30-02-photo63-byDK.jpg` through `photo67` | `Claremont/AA-HH-W14A&B/_W14B 2002-01-30/` |
| Row 24, **C12a and C12b** | Jan 21, 2002, **40–45** | `CM-pieceC12-01-21-02-photo40-byDK.jpg` through `photo45` | `Claremont/C10s&20s&30s/C12 2002-01-21/` |

[FEMA field summary p. 16](https://www.fema.gov/pdf/library/fema403_apd.pdf#page=16) · [All 17 exact catalog paths, URLs and sizes](SOURCE-PINS.json)

The W14A folder is nested within a folder named for W14B. The inner folder and filename still carry the W14A label, and the W14B images are directly in the outer folder. Preserve that hierarchy and both labels. The C12 catalog filenames use **C12** without splitting **a** and **b**. The field row names both candidates. The file-list test cannot assign the photographs to either individual C12 piece.

## Representative availability checks

A separate expanded Archive item, `NIST_9-11_Release_32`, accepted HTTP HEAD for **W14B photo 63**, **W14A photo 68**, and **C12 photo 40**. Each redirected to an archive storage host and returned **200**, `image/jpeg`, and a length matching the manifest (**214,451**, **272,133**, and **205,849** bytes, respectively). The other 14 exact URLs are constructed from catalog paths and were not probed individually. The full expanded item metadata request timed out and is preserved locally as an incomplete response. Neither the HEAD probes nor the manifest checksum verifies any JPEG body's bytes, pixels, embedded metadata, camera date, or continuity back to a camera original. The verified media store was unavailable, so the acquisition stopped at metadata and headers. No BitTorrent client was used. [Representative URLs and receipt fields](SOURCE-PINS.json)

## Attribution and remaining work

The filename and sequence matches supply a retrievable counterpart for each field reference. They leave the field **WTC#7** description and NIST's later **unidentified** W14A/B classifications side by side. Nothing here establishes a building, floor, member position, a link to Column 79/G3005, or an identity with the separate Appendix C sample. The archive's third-party metadata does not authenticate a file as an unchanged camera original. [FEMA field record](https://www.fema.gov/pdf/library/fema403_apd.pdf#page=16) · [NIST NCSTAR 1-3B, Table A-7](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3b.pdf#page=96)

- [ ] When the verified media store is available, acquire the 17 exact JPEG bodies, record per-file SHA-256 and HTTP metadata, and compare visible marks and seat geometry to the field sheet and later NIST intake views. Keep all originals and dated derivatives separate.
- [ ] Locate the dated camera or negative index, W14A/B and C12 field-to-intake transfer records, NIST attribution worksheet and the actual W14B FOIA response. Photo identification and classification rationale require different records.
- [ ] Keep FAA PD01–PD04 and the remaining work-plan dependencies open on their assigned tracks.

**Reproduction.** Run `python3 inspect_release32.py <archive-metadata.json> <release32-manifest.torrent>` against the two pinned source entities. Compare their SHA-256, the disc and subfolder counts, and the exact 17 paths. This is a catalog comparison. The media themselves were outside this run's reading scope.
