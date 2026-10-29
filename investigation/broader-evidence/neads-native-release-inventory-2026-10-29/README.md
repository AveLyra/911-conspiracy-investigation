# A public archive catalog matches the held NEADS MP3, but supplies no native clock package

October 29, 2026. Original recording-provenance and clock-input work, REC01–REC03, alongside FAA operational-clock questions. This is an acquisition/source-selection supplement to the existing technical owner's FA041/FA042 work. It does not rerun decoding or substitute metadata examples for calibrated historical time.

## New source-level result

The [public Internet Archive metadata endpoint](https://archive.org/metadata/NORAD_9-11_audio) returned a complete JSON entity of **75,905 bytes**. It lists **257 file records**, including **21 MP3 offerings**. None of the returned names ends in `.wav`, `.mdb`, `.accdb`, `.arc`, `.iso`, `.zip` or `.7z`. These are observations about this returned item inventory, not proof that original recordings or a database never existed or are unavailable elsewhere.

One catalog entry names **DRM1_DAT2_Channel_2_MCC_Op.mp3**, the same basename as the held file previously extracted from a Government Attic ZIP. The offered size is **137,854,277 bytes**, with SHA-1 **34d8e0d6bbc8926adeaa9a590cd640c6f63fcdb2**. The existing local file was read and both size and computed SHA-1 match those catalog fields. Its computed SHA-256 also matches the preceding held-source pin: **ad66977c17384288096b4ccb99758c6e14f1c1efa2972f1491946845ae1da1e1**.

No archive audio body was downloaded for this check. Thus this is a held-file-to-catalog fingerprint match, not a new byte-by-byte comparison of two retrieved media entities. It does not authenticate agency custody, recording date, channel meaning, unchanged timing, native format or independent UTC. The ZIP and catalog distributions may share a lineage; they are not counted as independent witnesses to historical events.

## “Original” is an archive field, not a recording-master finding

The catalog labels the selected MP3 `source: original` and `format: VBR MP3`. Those are the archive's supplied classification fields. They do not turn an MP3 into a native recorder export or uncompressed master.

The 257 records include many derivatives: waveform/peak data, Ogg files, images and spectrograms, as well as collection metadata. The `source` field classifies **23 entries as original**, including entries other than the 21 MP3 audio offerings. Neither 257 nor 23 is a count of independently recorded calls, original tapes, recovered channels or native source carriers. [CATALOG-RESULTS.json](CATALOG-RESULTS.json) preserves the exact accounting and the selected entry without uploader/contact fields. No duration, waveform, continuity, call attribution or clock fit was newly tested.

## A separate carrier-inventory lead remains qualified

The public reader of [Releases Spreadsheet 2012-01-04](https://www.scribd.com/document/78046326/Releases-Spreadsheet-2012-01-04) presents a 13-page reproduction. Its parsed text, reader line **148** in the saved representation, includes **RDOD 03012646–RDOD 03012647** described as two NEADS DAT-audio DVDs; **RDOD 03011011**, another NEADS DAT-audio DVD; and **RDOD 04020857**, a DRM-1 dictaphone remake DVD.

These are literal retrieval leads from a later third-party representation. The original PDF/spreadsheet, native row definitions and actual media are unacquired. Flattened text does not establish which box/date cells belong to these descriptions. No page-image reading, native-file hash, release-date/box assignment, metadata-database schema or waveform join is claimed. The participant article's shorter literal **RDoD0312646** remains beside the reader's longer string; no identifier was silently corrected or selected as controlling. The DRM-1 remake description is not automatically the source carrier for the held DAT2-named MP3.

One official NARA collection-index navigation, its linked FAQ and two exact-title official-domain searches did not recover the matching original release spreadsheet in this bounded pass. Unrelated general declassification results were excluded. This is not evidence of missing holdings or a withholding determination. Historical FAQ wording is not adopted as proof of present access status or as a rule for agency records in another proceeding.

## What this advances and what remains unperformed

The new catalog entity narrows acquisition: re-downloading the listed MCC MP3 would repeat a held representation, not supply the sought continuous WAV/database. The reproduced inventory supplies more specific carrier targets. Neither source provides the missing typed `Call`/`Callfile` rows, recorder/export/receipt mapping, corresponding native waveform or independent clock authority. Those remain necessary for the proposed pairing and calibration tests; the previously completed FA042 example arithmetic is not repeated here.

Only public metadata and reader text were inspected in this unit. The full catalog entity and reader responses remain locally preserved; public files contain reviewed source pins, selected nonpersonal metadata, original notes and verification code. No raw metadata with uploader/contact fields, bulk reader text, images, audio, private correspondence, signatures or credentials are published. The catalog's small file inventory was inspected; no media, MDB, ARC or disk image was downloaded, decoded, played or uploaded.

[SOURCES.json](SOURCES.json) distinguishes source-entity and reader-representation hashes. [verify_catalog.py](verify_catalog.py) checks the catalog identity/accounting and selected entry when supplied the preserved metadata; [RESULTS.json](RESULTS.json) records actual execution. The earlier held-file fingerprint check is separately pinned, not presented as an independent historical validation. [OPEN-TODOS.json](OPEN-TODOS.json) retains the exact source relationships and all five work-plan tracks. [REVIEW-AND-CHECKS.json](REVIEW-AND-CHECKS.json) and [TEXT-CHANGES.diff](TEXT-CHANGES.diff) record scope and additive revision accountability.

Source research and the technical owner's reports/registers are unchanged. All eighteen original-input requirements retain their substantive acceptance criteria. No FAA corrected-answer/disposition, telephone carrier join, aircraft association, native timing test, specimen test, steel attribution rationale or historical-intent conclusion is completed by this catalog check. No outreach, fees, new request/filing, mailbox access, private push, merge, deletion or history rewrite occurred.
