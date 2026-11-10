> Public derivative of the November 5, 2026 native GMS transmittal study. This copy contains original research, source links, and metadata.

# GMS steel-photo disc and transmittal crosswalk

November 5, 2026. STL02–STL03. This follow-up compares two disc folders in the Release 32 catalog and pins the court opinion that identifies the underlying GMS transmittals. The [earlier photo catalog review](https://github.com/AveLyra/911-conspiracy-investigation/blob/5e114e895f1cb43ecb8d0e60aa79192c2008b5e7/investigation/broader-evidence/steel-released-photo-catalog-r32-2026-11-05/README.md) preserves the 17 target photographs and the field attribution issue.

## Archive catalog observations

| Literal disc and folder labels | File paths |
| --- | ---: |
| `42A0375 - G33D9` / `WTCI-102-I -GMS-CD#8-Multiple STEEL` | 725 JPEG |
| `42A0376 - G33D10` / `WTCI-102-I GMS-Keasbey` | 6 MPG |
| `42A0377 - G33D11` / `WTCI-134-I GMS NIST Steel Multiple` | 459 JPEG |
| `42A0378 - G33D12` / `WTCI-134-I WTC7 Analysis Photos` | 49 images |
| `42A0379 - G33D13` / `WTCI-134-I Elev Photos` | 22 JPEG and 1 PDF |
| `42A0380 - G33D14` / `WTCI-134-I WTC7 Analysis Videos` | 3 videos |

Within all 58,466 paths, the identifier scan found no directory segment bearing `WTCI-93-I` or `WTCI-143-I`, including the scanned leading-zero, case and separator variants. The separate expanded mirror's notice addresses NYPD photographs. The scanned CD #8 entries are all JPEGs. [Release 32 compressed-copy catalog listing](https://archive.org/metadata/nist-foia-09-42-r32) · [Expanded mirror notice](https://archive.org/download/NIST_9-11_Release_32/International_Center_for_911_Studies_NIST_FOIA/Release_32/Release%2032%20Notice.txt)

Comparing only G33D9 and G33D11 produced **20 shared case-folded basenames and 21 candidate pairs**. Each pair has equal catalog-declared byte length. All **17** previous W14B, W14A and C12 target basenames appear in G33D9. **Zero** appear in G33D11 by this test. Same-name and same-length hits are candidates for byte-level comparison. Renaming or editing could evade the basename join, and the archive catalog alone cannot establish disc-level equivalence, contents of individual images, or steel specimen identity.

## Court record and unresolved wording

Locators below are physical PDF pages and one-based PyMuPDF sorted text lines, including blank lines.

| Source account | Locator | Record as published |
| --- | --- | --- |
| Opinion background citing the second Fletcher declaration | pp. 8–9, p. 8 lines 14–22 and p. 9 lines 4–10 | The opinion associates `WTCI-93-I` with the January 2003 GMS transfer and request `12-168`, closed March 4, 2013. It calls `WTCI-134-I` an updated record and associates it with `12-188`, closed September 25, 2015. It reports 1,312 files released in full for 12-188 and separately reports redactions, withholdings and a referral. |
| Cole's account as summarized by the court | p. 27 lines 4–16 and 21–27 | Cole distinguished receipt of the 34-page transmittal from receipt of the underlying listed BPS materials. |
| Agency declaration as summarized and evaluated by the court | pp. 28–29, p. 28 lines 17–27 and p. 29 lines 4–11 | The declaration described the 34 pages as the entirety of `WTCI-93-I`, including release forms and a catalog, and described `WTCI-134-I` as including added and replacement materials. The court accepted the account that Cole received the nonexempt records from the two record sets. |
| Alternating identifiers in the opinion | p. 29 lines 12–27 and p. 30 lines 4–16 | The narrative repeatedly prints `WTCI-143-I`, including when discussing replacement. The adjacent descriptions and exhibit references print `WTCI-134-I`. Both strings are retained as printed. |

[Cole memorandum opinion, ECF 71](https://www.govinfo.gov/content/pkg/USCOURTS-dcd-1_15-cv-01991/pdf/USCOURTS-dcd-1_15-cv-01991-2.pdf#page=27)

The court dismissed the claim against NIST as moot (p. 3) and accepted the agency account on production of the records at issue (pp. 28–30). That account and the mirrored catalog supply retrieval leads at different levels. The opinion passage identifies no disc-by-disc mapping to G33D9 or G33D11. The mirrored folder labels cannot establish that the archive reproduces Cole's separate 12-168 or 12-188 production. The cause of the identifier discrepancy remains open.

## TODOs

- Obtain the 34-page `WTCI-93-I` transmittal and catalog (ECF 61-4) and the supplemental transfer (ECF 69-1 exhibit C, pp. 12–13, cited on pp. 29–30 of the opinion). Also seek ECF 64-2 and the 12-168 and 12-188 production indexes. Two candidate public RECAP attachment URLs returned HTTP 404. Revisit when an authenticated public docket attachment, a catalog copy with provenance, or an independent agency index becomes available.
- Check which original and replacement discs the transfer lists, including any explicit mappings for `WTCI-102-I`, `WTCI-134-I`, and the disputed `WTCI-143-I` string. Require item identifiers plus contemporaneous disc or file references before asserting a match.
- When the verified media store is available, compare SHA-256 for the 21 candidate pairs and inspect the 17 previously cataloged targets against field and inventory records. Keep specimen attribution open pending an item-level match.

The source pins record URLs, access date, lengths and SHA-256. To reproduce, run `python3 compare_catalog.py <manifest> <prior-source-pins.json>` with the [earlier catalog parser and source pins](https://github.com/AveLyra/911-conspiracy-investigation/tree/5e114e895f1cb43ecb8d0e60aa79192c2008b5e7/investigation/broader-evidence/steel-released-photo-catalog-r32-2026-11-05) on the Python import path. The test reads the manifest as a static file.

[Source pins and machine-readable counts](SOURCE-PINS.json)
