# Flight 93 briefing: archived copy and call-row text

November 25, 2026 · TEL02–TEL04 / AUD016-A1. An additional publicly accessible archive member supplies the May 13, 2004 Flight 93 briefing discussed in the [preceding source crosswalk](https://github.com/AveLyra/911-conspiracy-investigation/blob/c6b3101ad1a19a20314602ac8a784cd91becd85c/investigation/broader-evidence/telephone-wainio-briefing-crosswalk-2026-11-25/README.md).

## What was tested

Using the existing 2009 ZIP central-directory index, we retrieved only the named member `MFR NARA- T7- DOJ- DOJ Briefing on UA93 Calls- 5-13-04- 00217.pdf` from the [public archive](https://archive.org/download/911datasets/NARA_9-11_Commission_Records_Released_Jan_14_2009.zip). The member is **447,885 bytes**, SHA-256 `2f72baa3c4b248ab7034d7a20240dafbf285bc7fbc07e3e80650877d2177bb6c`. It exactly matches the hash and byte count recorded for the previously acquired [official NARA copy](https://catalog.archives.gov/medialz/legislative/rg-148/2524787/t-0148-911MFR-00217.pdf), per the earlier [source manifest](https://github.com/AveLyra/911-conspiracy-investigation/blob/681797a20a39d8c30e367c2220be15a191e3a409/investigation/broader-evidence/telephone-may13-briefings-2026-10-29/SOURCES.json). Archive acquisition November 25, 2026; member ZIP CRC-32 `4d70d592` also verified. Matching bytes identify the two retrieved copies, not their original creation history or the authenticity of the underlying telephone data.

## Observations and limits

On **physical PDF page 3**, PDFKit text extraction puts **“9:53:43 Honor Wainio”** on the same line, with the row-33-ABC block label in nearby extracted text. That advances the source association from the prior third-party reproduction to the text layer of a byte-matching archived copy. The PDF is a Commission briefing memorandum, not a native carrier export. The link from the briefing's named entry to a particular authenticated carrier record remains untested.

The same page's extracted duration list reads **“F69 seconds”** at the corresponding ordered position. The prior analyst's [published visual transcription](https://github.com/AveLyra/911-conspiracy-investigation/blob/681797a20a39d8c30e367c2220be15a191e3a409/investigation/broader-evidence/telephone-may13-briefings-2026-10-29/SAFE-MFR-ROWS.json) records **269 seconds** for page 3, block 8, row 3. Those are distinct observations: the garbled text-layer character is not silently corrected, and this pass did not independently inspect the page image or establish the alignment of extracted columns. Preserve the [Park Service's 9:53 and 9:54 labels](https://github.com/AveLyra/911-conspiracy-investigation/blob/2d645076866855e1e4a0723134b678eaeac40131/investigation/broader-evidence/telephone-wainio-nps-timing-2026-11-25/README.md), the Commission report's 9:54 label and the previously reported candidate FBI account separately.

## TODOs

- [ ] Visually recheck the named entry, adjacent duration and column alignment when verified media is available; preserve both glyph readings.
- [ ] Obtain the original carrier record, its call key, event/time-zone/rounding and duration definitions, and the source-to-briefing worksheet.
- [ ] Obtain and visually check the relevant FBI interview release, its date and relationship to Commission note 375.

No raw carrier row, original recording or calibrated clock was acquired. The archive member is a second access route to matching bytes, not independent corroboration of the historical call. This finding does not establish fabrication, intent or conspiracy. Earlier source reports remain unchanged.
