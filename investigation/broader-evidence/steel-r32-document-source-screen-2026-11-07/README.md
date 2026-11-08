# Release 32: document-name screen and archived notice

Study date: November 7, 2026 Eastern. Notice retrieved November 8, 2026 UTC. This is an ancillary source and publication-scope check under STL01–STL04, not a new finding about collapse or wrongdoing.

**Result:** the pinned catalog contains three document-like filenames: two text notices and a PDF named for Silverstein's WTC7 photographs. A filename screen did not locate a clearly named nonimage inventory, caption index or transmittal. The separately retrieved release notice asserts rights over NYPD photographs; it supplies no specimen-to-photo or custody crosswalk.

## Observations and source assertions

| Layer | Finding | Exact locator and limit |
| --- | --- | --- |
| Derived catalog result | 58,466 entries; 37 lack one of the selected image suffixes. Of these, 34 have video suffixes and three have text/PDF suffixes. | [Pinned catalog](https://archive.org/download/nist-foia-09-42-r32/Supplemental%20Files/International_Center_for_911_Studies_NIST_FOIA_-_Release_32.torrent); entry numbers below are zero-based. This is a filename census, not body-format verification. |
| Direct retrieval | Entry 1's notice response is 1,054 bytes, matching its catalog length; SHA-256 is `7a8730fcc8090cb82403c68f64f59f1294f82493356379e475e7b2da7893465c`. | [Archived Release 32 notice](https://archive.org/download/NIST_9-11_Release_32/International_Center_for_911_Studies_NIST_FOIA/Release_32/Release%2032%20Notice.txt), complete body read. HTTP 200 identifies this retrieval, not agency authentication. |
| Source assertion | The notice says New York City claims copyright in the enclosed NYPD photographs. It describes permission, use and accompanying-notice requirements, including a reference to fair use. | Notice lines 3–10, using strict UTF-8 and `splitlines()`. This records the assertion; it does not decide its validity or which individual images belong to that set. |

The text/PDF filenames are:

- Entry **0**, **1,423** declared bytes: `Release_32/NIST FOIA Terms of Use.txt`.
- Entry **1**, **1,054** declared bytes: `Release_32/Release 32 Notice.txt`.
- Entry **58,465**, **227,393** declared bytes: `Release_32/Release 32/42A0379 - G33D13/WTCI-134-I Elev Photos/WTC7-Silverstein photos/Silverstein-Pics. of 7 WTC on Sept.11.pdf`.

Their shared omitted prefix is `International_Center_for_911_Studies_NIST_FOIA/`. The other text file and PDF bodies were **not** acquired or read in this unit.

## Scope, contrary evidence and unresolved records

The nonimage-path filter, applied case-insensitively, was `draft|appendix|caption|index|manifest|inventory|database|field.?note|transmittal|codebook`; it returned **zero** matches. This narrow negative does not establish that the release lacks documentation. The catalog contains **38,088 .tif filenames**, whose bodies could include scanned records. Those bodies were not reviewed here. Filename suffixes can also misdescribe content.

The notice's reference to NYPD photographs does not identify the rights holder or licensing status of the GMS/Claremont steel views examined previously. It also does not show that those views are NYPD photographs. Neither the catalog name nor the notice authenticates an original NIST production, the release's completeness, a photographer, or any physical specimen's provenance. No discrepancy was resolved and no new mismatch was established by the matching length.

The [previous four-photo comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/142ee01c3603bf649fc0a81d3a7ac7e8f38d9711/investigation/broader-evidence/steel-r32-c30-photo-comparison-2026-11-07/README.md) remains unchanged: the C30-related views show retention lettering, while physical identity with the reference member, building origin and custody remain unconfirmed. This notice provides no new join between those photographs and an inventory.

## TODOs and discriminating inputs

1. Obtain the original release inventory/cover documentation identifying the enclosed NYPD set and source disks; compare it with this catalog and notice without assuming the catalog is exhaustive.
2. Locate native caption drafts, identifier codebooks and specimen/yard/coupon transfer records. A linked row with original identifiers and provenance could test the photo-to-specimen association.
3. Inspect a bounded, preselected set of potentially relevant TIFF/PDF bodies if an index, folder context or substantive lead identifies them. No exhaustive scan, hidden-data review or blanket absence claim has been performed.
4. Keep the remaining use-notice body and image-specific rights provenance as unresolved source checks before any proposed image redistribution. No raw photograph, crop or notice body is included in this public addition.

All five original-record tracks and their eighteen acceptance requirements remain open at their existing scope; this unit closes none of them. Missing inputs stay TODOs, not evidence of suppression or a reason to claim empirical completion.

## Reproduction and preservation

`SOURCE-PINS.json` preserves the URLs, access time, hashes, entry indices, byte lengths, all suffix counts, filter and limits. `verify.py NOTICE CATALOG PARSER` checks the raw notice/catalog hashes, passive parser hash, selected entries and the filename calculation. It performs no network requests and executes no source attachments. A pass establishes reproducible byte and index observations only.

The complete downloaded notice and prior catalog remain preserved separately in native research storage. This report is an additive public derivative; previous reports, originals and conflicting identifiers/timestamps remain unchanged. The raw notice, source images, private correspondence and personal data are excluded.
