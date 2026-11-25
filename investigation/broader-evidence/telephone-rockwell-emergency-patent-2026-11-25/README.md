# Rockwell emergency-recording patent: a technical lead, not SERO configuration evidence

2026-11-25 · TEL01–TEL04 / AUD016-A1. A pre-2001 Rockwell patent describes an emergency-recording design and a possible event-reporting trail. It does **not** establish that American Airlines installed this patented design, that it governed the Flight 11 recording, or that any particular event log exists.

## Source and design statements

[U.S. Patent 5,392,329, *Automatic Call Distribution System with Emergency Recording System and Method*](https://patentimages.storage.googleapis.com/a0/db/cf/65bde35b0e7e93/US5392329.pdf), filed October 27, 1992 and granted February 21, 1995, identifies Rockwell International Corporation as assignee. The 19-page public patent PDF was retrieved 2026-11-25; SHA-256 `7a50e7c42be420ded1d226e5c2545d8c91c28a8a0f97cb5a589a27ab0eefd257`. The separately retrieved [patent text and metadata](https://patents.google.com/patent/US5392329A/en) has HTML SHA-256 `25410c333cd9e2bf594eda60488c7a82462e0e023620ef67eeecf87dc052b121`.

- In the described embodiment, an operator uses an emergency key to request a recorder for a call. The patent discusses a second press by the requesting unit to terminate recording, and distinguishes an emergency key pressed on another connected unit. [PDF p. 13, column 7](https://patentimages.storage.googleapis.com/a0/db/cf/65bde35b0e7e93/US5392329.pdf#page=13); [PDF p. 15, columns 11–12](https://patentimages.storage.googleapis.com/a0/db/cf/65bde35b0e7e93/US5392329.pdf#page=15).
- The design describes an emergency report that can contain the **time recording was requested**, date and unit/recorder identifiers; it also describes a zero recorder identifier when none was found and connected. These are proposed fields and behavior in this patent, not an observed report from the airline center. [PDF p. 13, column 7](https://patentimages.storage.googleapis.com/a0/db/cf/65bde35b0e7e93/US5392329.pdf#page=13).
- A text-layer search of all 19 PDF pages found no literal `timer`, `minute`, `duration`, or `Spectrum`. This is a bounded search of the extracted layer, not proof that the document or every related design lacks a timed stop. Patent claims and illustrations are not a deployed-system configuration.

## Compare with the released 2001 accounts

An FBI interview report states that the airline reservation-center system used an emergency-button recording function, stopped automatically after approximately **four minutes**, and produced proprietary-format and WAV copies. The previous comparison preserves the three CD descriptions and the unacquired media. A separate representative's interview attributes **8:20 A.M., EST** to the center's computer system. Preserve both reported accounts and the patent's separate design description; no direct link between this patent and the installed version is documented. [Interview comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/e6e368c27fa2357c255aba95147143a28f8a1e9a/investigation/broader-evidence/telephone-sero-three-discs-2026-11-25/README.md) · [Representative's time account](https://github.com/AveLyra/911-conspiracy-investigation/blob/816480f5b05e653096108e3588d81dc2bcfd9902/investigation/broader-evidence/telephone-sero-system-timing-302-2026-11-25/README.md).

The patent makes an emergency report and recorder-identification fields **specific candidate records to look for if the installed system had that feature**. It does not establish a printout was generated, retained, or discarded, or that a button was pressed a second time. The patent's manual-stop description and the interview's reported automatic stop have different scopes and are not a demonstrated contradiction about this actual call.

## TODOs

- Obtain the actual 2001 center's switch, recorder and software versions; manuals and deployment/feature configuration; event or printer reports if generated; recording and timer settings; and clock configuration.
- Obtain original Rockwell-format and WAV files, CDs, conversion records, checksums, intake, dispatch and receipt documents. Test the real audio and event data rather than inferring behavior from patent claims.
- Preserve the separate FAA correction, AA77 carrier and all other original-record tasks. No source reviewed here establishes the original call's duration, deliberate truncation or motive.

Reading scope: visually checked patent PDF pp. 13 and 15 and searched the embedded text of all 19 pages for the four exact terms above; checked the recorded source hashes and prior cited interview comparisons. No hardware, software, recording, deployment record, or physical experiment was examined.
