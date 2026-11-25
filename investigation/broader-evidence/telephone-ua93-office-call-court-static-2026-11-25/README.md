# Flight 93 office call: static test of court presentation

AUD016-A1 / TEL02–TEL04 · 2026-11-25. This additive test follows the [visually verified briefing entry](https://github.com/AveLyra/911-conspiracy-investigation/blob/3f4f9e5ab309850d1e39731dfbe0b3f85353fb34/investigation/broader-evidence/telephone-ua93-office-call-visual-2026-11-25/README.md). It preserves the briefing's 0 seconds and the FBI interview's reported 138 seconds separately.

## Source and reproduction

The [court's P200055 exhibit page](https://coop.vaed.uscourts.gov/moussaoui/exhibits/prosecution/flights/P200055.html) identifies a summary presentation and links the [court archive](https://coop.vaed.uscourts.gov/moussaoui/flights.zip). The preserved archive, previously acquired 2026-11-16, was read from the verified research-media store on 2026-11-25. Its SHA-256 `3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801` matched the prior acquisition pin. This test used member `UA 93 Calls.swf`; it did not execute the Flash or other archive executables.

Run the two accompanying Python 3 scripts with the archive path as their sole argument. They adapt the previously published static-text and sprite-placement probes: the text selection and target IDs were changed; the placement probe now scans sprites for those IDs. They are purpose-limited research parsers, not an independent certified decoder or a rendering of the exhibit.

## Observations

The text probe reports 15 fonts, 420 nonempty text tags and zero parser-reported errors. Among its outputs: character **989** = `Martinez`, **995** = `09:45:37`, and **505** = `0 SECONDS`. A separate character, 348, also contains `0 SECONDS`; that reuse matters and zero text alone cannot identify a call.

The placement probe reports, within **sprite 1001**, a placement of character 989 at local frame **1**, and placements of 995 and 505 at local frame **14**, depths **475** and **476**, respectively. Their translations in twips are `(1198, 8942)` and `(2573, 8942)`. It also reports a character 989 placement at frame 12. These are parsed local display-list entries, not screenshots: the probe does not track all removals, parent transforms, clipping, visibility or ActionScript navigation. The presence of the surname in the same sprite and the matching time support a candidate association; they do not independently prove the name, time and value were simultaneously visible or shown in court. Other text or image elements were not exhaustively reconstructed.

The [2004 Commission briefing](https://catalog.archives.gov/medialz/legislative/rg-148/2524787/t-0148-911MFR-00217.pdf#page=3) visually lists the 9:45:37 office call as **0 seconds**. The [FBI interview report](https://vault.fbi.gov/9-11%20Commission%20Report/9-11-interviews-2001-09-sep-02-of-08) separately says the interviewee was told a 9:45 call lasted **138 seconds**; it also records that she received no message. The interview page remains a text-extraction reading in this work. The FBI interview, Commission memo and court presentation may have related source material and are not counted as independent native measurements. No difference is resolved or assigned a cause.

## What remains untested

- [ ] Validate the display using a safe independent renderer and full display-list/frame-state analysis; do not assume this static parse proves courtroom playback or NPS's specific source.
- [ ] Visually inspect the FBI interview page and check its file provenance.
- [ ] Obtain native carrier/operator event records, clock and duration definitions, and the briefing/exhibit source worksheets. Test whether 0 and 138 describe the same interval, different legs, or another difference.

No call recording, native carrier output, private correspondence or sensitive billing details were reproduced. No inference of falsification, message content, or motive follows from these values.
