# Second Flight 93 SWF: static placement comparison

November 16, 2026 · TEL02–TEL04 / AUD016-A1. The [court P200055 ZIP](https://coop.vaed.uscourts.gov/moussaoui/exhibits/prosecution/flights/P200055.html) contains two differently named Flight 93 SWF files. A static check of its second member, `UA93.swf`, found the same local position pattern for the three short-call entries as the first member. The files are related parts of one archive, not independent records of events.

## Input and result

The source ZIP and both member hashes are recorded in the [archive source pin](https://github.com/AveLyra/911-conspiracy-investigation/blob/bf46236c949033a54d8ec6d52007ad95070388d1/investigation/broader-evidence/telephone-p200055-court-bundle-2026-11-16/README.md). The uncompressed second member is **3,464,811 bytes**, SHA-256 `f104ab54492e05550c9e776894e0dbb0d9238039a8f2e9c40be41b1a122d7675`. No launcher, SWF script or media was executed.

The [text probe](extract-static-text.py) decodes characters **1358, 1357 and 1360** as **09:42:03, 09:42:25 and 09:42:45**, and characters **1359 and 1034** as **2 SECONDS and 3 SECONDS**. The [placement probe](inspect-sprite-1369.py) finds all five in sprite **1369**, local frame **20**. Time labels have x = −3677 twips; duration labels have x = −2302. The y values and pairs are:

| Time | y, in twips | Duration character | Decoded value |
| --- | ---: | ---: | --- |
| 09:42:03 | 10983 | 1359 | 2 seconds |
| 09:42:25 | 11361 | 1034 | 3 seconds |
| 09:42:45 | 11739 | 1034 | 3 seconds |

These are the same local frame, depths and translations found in the [first member's static audit](https://github.com/AveLyra/911-conspiracy-investigation/blob/85f6ab2ff0e3ff9c90e645a899f6a63557ec823e/investigation/broader-evidence/telephone-p200055-sprite-placement-2026-11-16/README.md), though the files and internal character IDs differ. Both match the third-party image and NARA briefing's 2/3/3 sequence; NPS's 2/3/2 remains a separate observation with a row join unverified. [Prior image comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/a554abb6f2957b23c9d455b1bca204ca289d7578/investigation/broader-evidence/telephone-grandcolas-exhibit-image-2026-11-16/README.md).

## Limits and TODOs

Run `python3 extract-static-text.py /path/to/flights.zip` and `python3 inspect-sprite-1369.py /path/to/flights.zip` to reproduce the selected static results. These research parsers are not a certified Flash implementation. They do not prove stage visibility, court playback, parent transforms or historical events; the files could share production data. **TODO:** independently validate the exact court presentation via safe rendering and obtain the NPS source-to-row and carrier field/clock records. No motive, suppression, conversation or message content follows from this result. Preserve prior files and conflicting values unchanged.
