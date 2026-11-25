# Correction: an attributed GTE field explanation was already available

AUD016-A1 / TEL02–TEL04 · 2026-11-25. Our [recent carrier-row note](https://github.com/AveLyra/911-conspiracy-investigation/blob/97c62e3b068a02e323882a0617e923e480a19c16/investigation/broader-evidence/telephone-ua93-office-call-carrier-row-2026-11-25/README.md) said that “the field dictionary, unit, default/blank handling and source-to-briefing worksheet are unavailable.” **That statement was too broad.** Our investigation had already documented an attributed explanation of these GTE fields, including seconds for Duration Connect. The recent note omitted it; this is our sourcing error, not a new discovery. The native vendor specification, applicable export/version, default/failure/blank rules, event-level join and source-to-briefing worksheet remain unlocated.

## Existing explanation checked again

The released Team 7 Box 19 FBI interview, physical **pp. 24–25**, concerns a June 28, 2002 interview of a GTE manager. The [public scan reproduction](https://www.scribd.com/document/24392516/T7-B19-Key-302s-Fdr-Entire-Contents-FBI-302s) is also in a [Commission archive mirror](https://archive.org/download/911datasets/NARA_9-11_Commission_Records_Released_Jan_14_2009.zip). In the report, **Duration Connect** is described as the time in seconds taken by the network to connect a call to the dialed number; **SCP Duration** is described separately as the duration of the telephone call. **Duration Operator** is discussed separately. These are statements attributed in an FBI report, not an authenticated engineering specification or proof of each field's behavior on failed or incomplete calls.

The already-held 52-page Box 19 PDF's SHA-256 was rechecked as `01daa2ea6683aacbbb7918086fb8328e7803810087cc3160a352377be056dc4e`, matching its earlier acquisition pin. We newly rendered physical p. 25 at 144 dpi, visually inspected the field descriptions, and retained the page image on the verified research-media store (PNG SHA-256 `3c53eb7003341643bc8afd7f42e9546ede0b63884d6b68cf573fdddc5b54d841`). The earlier November 6 research review had already located this interview, and the [October 29 public briefing review](https://github.com/AveLyra/911-conspiracy-investigation/blob/681797a20a39d8c30e367c2220be15a191e3a409/investigation/broader-evidence/telephone-may13-briefings-2026-10-29/README.md) had already recorded related field descriptions. This correction does not claim an independent discovery.

## Effect on the 0 / 138 / 130 question

If the attributed explanation applies to the table and its particular event, **Duration Connect is described as setup time**, not as the length of a conversation. This makes differing setup and call-duration fields a concrete, source-supported **possibility**, not an established resolution. It does not establish what a blank SCP field means, that the network completed a connection, how the briefing's **0 seconds** was computed, or the provenance of the interviewee's **138 seconds**. The low-resolution table's prior **130** reading and possible **138** reading remain separate and unadjudicated, as do the FBI interview, briefing and court-presentation observations. The records may share upstream sources.

## Remaining work

- [ ] Obtain the native carrier dictionary and export version, including failure, default and blank-field rules; test applicability of the attributed explanation to the exact table.
- [ ] Obtain a higher-quality source for the ambiguous digit and carrier/operator/receiving-office events; establish the candidate event association using privacy-protected identifiers.
- [ ] Obtain the source-to-briefing and exhibit worksheets and verify what the 0 and 138 values actually measure. Do not infer conversation, deception, motive or concealment from a field label or unresolved values.

This additive correction preserves the earlier notes and conflicting readings. Source images and sensitive billing or contact information are not published here. No outreach, request submission or native carrier test was performed.
