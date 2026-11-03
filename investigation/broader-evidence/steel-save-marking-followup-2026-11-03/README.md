# SAVE markings in collected-steel footage: identifier and retention-record leads

November 3, 2026. A bounded follow-up to SV03 supplies a **provisional visual reading of “M2” beside “SAVE”**, another visible “SAVE” on an end plate, and measuring-tape activity. A second marking remains partly unreadable. These are leads to identification and handling records, not proof of specimen identity, retention, loss or wrongdoing. Missing originals remain TODOs.

## Source and unchanged earlier reading

The source is the already preserved public **[WTC Tape 3.mov](https://drive.google.com/file/d/1UkHot_5JcamIUEYnbtLSw8NgBdI7MeeY/view)**, reached through [NIST’s image/video navigation](https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations) and its [linked collection](https://googledrive.nist.gov/folders/1mO5PPh1ZyZafGUtWrzqhiaDwzTqyEPG-). The October 27 acquisition and November 3 full-file hash check identify **468,978,020 bytes**, SHA-256 **`a74ade3e8cbdf0df5976b67c60ee0a211937440e90d4a29bc211cdfc13057dcd`**. The movie was not downloaded again. The public route and file hash do not authenticate an original camera tape, filming date or physical custody. [Source pins](SOURCE-PINS.json).

The [October 27 report](https://github.com/AveLyra/911-conspiracy-investigation/blob/75347e9c38e09b5c2037ee9490e6c2c5acf0f799/investigation/broader-evidence/steel-candidate-originals-2026-10-27/README.md#sv03--a-directly-visible-preservation-related-marking), native report lines 27–31, recorded “SAVE” in zero-based input frame **3597**, reported presentation time **240.04004 seconds**, but did not confidently join the preceding identifier to an inventory entry. It expressly left an M/N alias unselected. That report, its native frames and its uncertainty remain unchanged. The new reading comes from additional angles in the same source; it is not an independent witness or an adjudication of the old prefix uncertainty.

## What was actually read

All times below are the decoder’s **presentation timestamps**, not a camera clock, filming date or historical elapsed time. All locators refer to the hash above. [Exact frame metadata](FRAME-MANIFEST.json) and [observation locators](LOCATORS.json) permit independent retrieval.

| Observation | Native zero-based frame / presentation seconds | Accepted observation and unresolved portion |
| --- | --- | --- |
| SAVE-O01 | **3630 / 242.242242**; supporting view 3660 / 244.244244 | A marking beside SAVE looks more like **M2** in this angle. This remains a provisional transcription. No source-written hyphen, full catalog designation or inventory match is accepted. The earlier M/N uncertainty remains in the record. |
| SAVE-O02 | **4050 / 270.27027** and **4080 / 272.272272** | **SAVE** is readable on a near end plate. The sampling does not establish whether the two SAVE writings concern one object, separate objects, portions, or one repeated instruction. |
| SAVE-O03 | 4050, 4080, **4170 / 278.278278**, **4230 / 282.282282** | A separate visible long member carries an **MS1/MSI-like token and an N-prefixed string**. The suffix remains unaccepted after the short adjacent-frame extension. No N11, N14, N17 or other complete identifier is assigned. |
| SAVE-O04 | **3660 / 244.244244**, **3990 / 266.266266**, **4080 / 272.272272** | A measuring tape is held across or along visible material. No numerical dimension, calibrated endpoint, result, responsible person or date is identified. |

The M2 candidate was written down **before** the attempted inventory consultation. An inventory label must not be used to supply unreadable characters. Adjacency in a view does not establish that markings on different visible surfaces belong to the same physical specimen. [Observations](OBSERVATIONS.json) · [unjoined provenance leads](PROVENANCE-LEADS.json).

## Meaning and competing interpretations

The useful lead is a possible route from a visible marking to an intake, marking, measurement or retention record. A SAVE marking could be a handling or preservation direction; its author, date, scope and effect are untested. It does not show whether the whole member or a portion was retained, sampled, transferred or later disposed of. An identifier-shaped marking might also be a field notation rather than a final catalog number. Those possibilities remain separate from the observed lettering.

The strongest objection to any claimed retention failure is that **we have neither an authenticated instruction nor the linked disposition record**. Conversely, a visible SAVE marking or measurement activity cannot prove successful long-term retention, representative sampling or scientific adequacy. The two writings and repeated frames are not counted as independent corroboration or as a count of unique specimens. No link to W14A/W14B, C12, FEMA Sample 1, I0137, WTC 7 or Column 79 has been demonstrated. Nothing here measures material composition, temperature, fracture mechanism, thermite or historical cause.

## Reading and verification scope

The initial selection used `select='between(n,3150,4050)*not(mod(n-3150,30))+eq(n,3597)',showinfo`: **32 native PNGs**. A concrete partly clipped marking then justified a prospectively recorded extension using `select='between(n,4050,4230)*not(mod(n-4050,30))',showinfo`: **7 PNGs**, including duplicate control frame 4050. Both FFmpeg 7.1.1 runs completed with exit status 0, with overwrite disabled and audio excluded.

The **39 files represent 38 distinct input indices**, not 39 independent events. Four initial indices had been extracted previously; 34 indices are newly selected relative to that earlier 16-frame set. Only **11 unique full native frames** were individually viewed: 3480, 3570, 3630, 3660, 3900, 3990, 4020, 4050, 4080, 4170 and 4230. Three labeled contact sheets were viewed for navigation; their thumbnails are not a full-detail reading of every selected image. The initial eight-view limit and the later three-view extension were respected.

The two earlier controls, frames 3597 and 3600, match the new decoded pixels; duplicate 4050 also matches. All 39 PNG hashes/dimensions and three overview hashes were checked. These are reproducible derivation checks, not historical authentication. The original file hash was checked before processing; size and modification time were unchanged after both read-only runs. No continuous visual census, new full-video count, audio review, independent or blinded transcription, AI enhancement, camera-clock test, specimen test or custody authentication was performed. [Reading scope](READING-SCOPE.json) · [verification](VERIFICATION.json).

## Missing inventory and next discriminating records

The previously recorded NCSTAR 1-3B PDF path was absent from the verified operational media store. That is a specific storage-path limitation; the share was available. One ordinary credential-free request to the [official PDF URL](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3b.pdf) on November 3 returned **403 / text/plain, 17 bytes**. Its response entity was retained and hashed. It is not a PDF or evidence of a changed report, deleted record or deliberate obstruction. The attempt stopped; no alternate-client or alternate-host retry was made. No inventory page or row was read or adopted in this unit. [Acquisition limits](SOURCE-PINS.json).

New TODOs are: **SAVE-01**, original tape/camera and slate/marking crosswalk; **SAVE-02**, actual intake/alias/geometry and inventory records for the candidate markings; **SAVE-03**, original SAVE instruction and subsequent cutting, sampling, transfer, receipt and disposition records; **SAVE-04**, original measurement sheets and any higher-quality source needed to test the unreadable suffix. Each requires a real record, not a presumed match. [Acceptance criteria and carried-forward TODOs](OPEN-TODOS.json).

The earlier Beverly Hills certification/attachments, museum accession and transfer chains, WTC 7-attribution questions and all **18 original-input criteria** remain open or partial. The broader acquisition/testing goal remains **blocked on original inputs**; this available reading is a separate partial research result. No new original-input acceptance criterion is closed.

## Preservation and publication boundary

The movie, earlier frames, reports and conflicting or uncertain readings remain preserved. The [immediately preceding public review](https://github.com/AveLyra/911-conspiracy-investigation/blob/c282a14153df29812b7f365e1ae441329666b4b4/investigation/broader-evidence/steel-nysa-flatbed-photo-2026-11-03/README.md) remains unchanged; [REVISION.diff](REVISION.diff) records only the appended current text against its immediately preceding preserved combined version. [Checklist](CHECKLIST.md).

The public copy contains original research notes, source links, hashes, locators and limits. Raw video, audio, frames, contact sheets, PDF/error bodies, personal information, private correspondence, litigation strategy and credentials are excluded. There was no outreach, request submission, fee, physical test, private-repository push, deletion or history rewrite. Publication verification is recorded separately after the push; it does not authenticate the historical claims.
