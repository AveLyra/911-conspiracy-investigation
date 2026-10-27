# Candidate-specific steel photographs and a shipping-month discrepancy

October 27, 2026. Original-record investigation track 5; existing B188/H005 and AUD011/AUD016. This adds source entities and comparisons to the [steel attribution study](https://github.com/AveLyra/911-conspiracy-investigation/blob/88831b1b5436958547c9399306ff3c60ad8e1baf/investigation/broader-evidence/steel-attribution-roots-2026-10-27/README.md) and [photo-source study](https://github.com/AveLyra/911-conspiracy-investigation/blob/7fdee56fbc807ef5d7f5eeda85f7ad0b24935a33/investigation/broader-evidence/steel-photo-roots-2026-10-27/README.md). Their records remain unchanged.

**Three candidate-specific JPEGs were acquired from NIST's linked public archive. Visible handling labels support a qualified link to W14A/B, but do not authenticate the steel's original building. Separately, NIST's published accounts give different months for the start of shipping to its campus: February and March 2002.** Neither difference is adjudicated here.

## SI01 — Actual candidate images, rather than only a filename or inventory row

[NIST's archive entry](https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations) links the [Collected Steel repository](https://googledrive.nist.gov/folders/1mO5PPh1ZyZafGUtWrzqhiaDwzTqyEPG-). Under Photos → Miscellaneous Photos, a different listing capability returned 1,000 items, beyond the earlier 100-item fetch slice. It exposed the following files; **1,000 may itself be a capped listing, not an exhaustive archive census**. [Discovery scope](DISCOVERY-SCOPE.json).

| Acquired file | Actual bytes | Visible observation |
|---|---:|---|
| [W-14a OVERALL_3.jpg](https://drive.google.com/file/d/1Z-L6C3KbG-1ha1Uslsa_wfA7zupmiTvq/view) |1,085,099|Clear orange W-14A marking on a deformed steel member.|
| [W-14b OVERALL_3.jpg](https://drive.google.com/file/d/1d2V_gxfzVg-tsjXzK8UeGUTZcvYb96tD/view) |1,215,948|Orange W-14B marking, upside down in the original view. A local QA crop was rotated 180 degrees for reading; the original was not changed.|
| [W-14B OVERALL.jpg](https://drive.google.com/file/d/1qqh3qzI0Xk9JckcSYqOeC4ghI6MHUEuT/view) |1,268,430|White marking read as W14B, with a stylized first character; the filename independently supplies the archive label, not independent building-origin evidence.|

All three are complete current JPEG entities, each 2,272 × 1,704 pixels, totaling **3,569,477 bytes**. Ordinary anonymous public downloads returned HTTP 200 and the expected sizes. [Exact source URLs, timestamps and SHA-256 values](IMAGE-SOURCES.json). [Native pixel rectangles, rotations and reading limits](PIXEL-LOCATORS.json).

The full three images and three selected label crops were viewed. They show outdoor storage among other steel. No calibrated ruler, original building/floor/column stamp or camera date was established from these selected views. Visible deformation, surface colour and apparent cut edges do not by themselves measure temperature, chemistry or the sequence of damage. No physical specimen was examined.

## SI02 — What this does, and does not, join

The newly visible labels strengthen the association between these archive images and the previously published **W-14A or A / W-14B** inventory identifiers. This is a qualified identifier crosswalk, not an independently authenticated custody chain. A handling label may have been applied after recovery. Filenames, painted labels and a report can share the same underlying labeling process.

Keep the conflicting records side by side:

- [FEMA Appendix D, physical page 16, rows 20–21](https://www.fema.gov/pdf/library/fema403_apd.pdf#page=16) labels A/W14A and B/W14B as **WTC#7**, with a December 19, 2001 trip date and later January 30 photograph references.
- [NIST's June 2004 progress report, physical 163 / F-47](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication1000-5v3.pdf#page=163), and [September 2005 inventory, physical 96 / printed 68](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3b.pdf#page=96), list the corresponding candidates as **unidentified wide-flange sections**. These earlier table comparisons are reused, not new discoveries in this unit.

These images are **not authenticated as the January 2002 field-photo series**. The exact photograph indices, original negatives/camera files, intake and alias records, transport/coupon logs, drawing comparisons and dated classification rationale remain missing. No link to FEMA Appendix C Sample 1, C12a/b, Column 79 or G3005 is established by a W14 label. The source shapes and labels cannot supply that missing join on their own.

## SI03 — Internal previews and metadata: qualified checks

All three complete current rasters decoded. A bounded JPEG/Photoshop-resource parser, independently cross-checked against Pillow's resource decoder, found a resource 1036 embedded JPEG preview in each file. Adobe documents [that resource and its 28-byte header](https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/#50577409_74450). Each preview is 112 × 84 pixels; actual resource offsets, sizes and hashes are preserved in [the inspection output](JPEG-INSPECTION-RESULT.json).

Each preview depicts the same overall scene as its own full image. The previews and resized full rasters are **not pixel-identical** and differ in colour/tonal rendering in the local comparison. On an uncalibrated RGB 0–255 comparison, root-mean-square differences were 24.04, 25.38 and 18.44 for the corresponding scenes; the six other-scene comparisons ranged 69.02–85.15. No ICC transformation, registration or threshold tuning was used. The result is limited coarse scene consistency, **not an editing detector or camera-original authentication**. Its processing differences remain observations, not a selected explanation.

Pillow returned zero EXIF entries and no IPTC fields for each image. That is not a claim of no metadata: APP0, APP13, APP2 and APP14 structures are present. All three share the same APP2 payload hash. Shared metadata does not make the image entities identical or authenticate a common photographer, capture session or editing history. Photoshop-format resources can be written by software; they do not establish which application/version/person created or changed these files. No absent camera timestamp was reconstructed.

Drive's catalog dates are November 26, 2019, between 06:07:32 and 06:07:35 UTC. Those object dates are not capture dates or evidence of when the steel was received. No historical photographic clock was calibrated.

## SI04 — Preserve February versus March shipping accounts

Three selected pages were re-rendered from the hash-pinned held PDFs and directly viewed:

| Source / exact locator | Published shipping-start account |
|---|---|
| [June 2004 SP 1000-5, volume 3, physical 119 / F-3](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication1000-5v3.pdf#page=119) |March 2002|
| [September 2005 NCSTAR 1-3B, physical 32 / printed 4](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3b.pdf#page=32) |March 2002|
| [September 2005 NCSTAR 1-3, physical 76 / printed 28](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3.pdf#page=76) |February 2002; it also identifies S. Cauffman as coordinating environmental testing, transportation and delivery.|

[Preserved values and extraction anchors](SHIPPING-OBSERVATIONS.json). The disagreement is in published narrative accounts. It does **not** establish an exact month of missing custody, which particular shipment is meant, or a candidate-specific dispatch/receipt. Editorial differences, different shipment sets or different event definitions are possible but untested. No cause is selected, and no value is silently corrected.

The highest-value underlying records are shipment authorizations, dispatch and receiving logs, environmental-clearance records, bills of lading/packing lists, accession photographs and the source/edit history behind these passages. They could support either account, distinguish their scopes or expose an unsupported chronology. The cited coordination role identifies a specific record trail; it is not an accusation against the named official.

## Verification, preservation and limits

[inspect_candidate_jpegs.py](inspect_candidate_jpegs.py) verifies source hashes/sizes, decodes the current rasters, bounds-checks JPEG and Photoshop resource offsets, cross-checks the two parsers and compares embedded previews with all three full scenes. Two malformed-input controls were rejected, and all six foreign-scene comparisons were more different than the corresponding own-image comparison. [Actual controls](CONTROL-RESULT.json). These checks cannot establish an unbroken historical chain or resolve the building attribution.

[verify_shipping.py](verify_shipping.py) checks the three PDF entities and selected extraction anchors while requiring both month values to remain. [Actual shipping checks](SHIPPING-CHECK-RESULT.json). Source integrity and text checks are distinct from direct page/image reading and physical custody. The public-download reproduction utility is separately described in [verification notes](VERIFICATION.md); no unrun network check is claimed.

Source JPEGs, embedded thumbnails, QA crops and PDF renders remain local. No redistribution basis for the photographs was established, so this public package contains original research notes, source links/hashes, selected safe metadata and code. Earlier records, failed access/processing attempts and exact source values are retained. [Access and method limits](METHOD-LIMITS.md) · [Checklist](CHECKLIST.json) · [Open originals](OPEN-RECORDS.md) · [Exact addition diff](README.diff) · [Earlier-document status](REVISION-STATUS.json).

The strongest limitation is that these are later archive entities with handling labels and incomplete capture/custody provenance. They can assist a documentary identification test but cannot substitute for it. No specimen's WTC 7 origin, NIST rejection rationale, deliberate alteration, loss or concealment is established here. The full five-track original-record goal remains incomplete.
