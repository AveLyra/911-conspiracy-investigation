# WF334 name check: a court-presentation candidate, not a verified message

The held court presentation contains **“Reuben, Todd”** and separate **“Reuben” / “Todd”** text definitions. The previously reviewed FBI-form tip **WF334** reports **“TODD RUBEN,”** described there as a passenger on **Flight #77**. Preserve both spellings. This is a specific identity-check lead; **the records have not been joined to the same person, message or call**. It is not yet a demonstrated contradiction about one established individual.

## Exact source trail

The [official court page for prosecution exhibit P200054](https://coop.vaed.uscourts.gov/moussaoui/exhibits/prosecution/flights/P200054.html) describes a Flight 77 summary of crew identities, passenger seat assignments and telephone calls, and expressly also includes information about the other three hijacked flights. The complete held HTML is **2,117 bytes**, SHA-256 `866887c38f78c1f5b68ab73a695ae5345812eaf53a3e34da240f5345a1cd96c5`. Exact saved-file lines: **25** (prosecution exhibits), **45** (P200054), **51** (description), **73** (ZIP link). These are local HTML line numbers, not transcript pages. The separate HTML receipt lacks an access timestamp; none is invented.

The [court archive](https://coop.vaed.uscourts.gov/moussaoui/flights.zip) was acquired **October 27, 2026, 13:40:38.310051 UTC**, as a 200 response. The preserved ZIP is **28,304,524 bytes**, SHA-256 `3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801`. Its exact **AA77.swf** member is **5,162,821 bytes**, SHA-256 `844dfb545c8414f9e7da1edc89ffe090a09d00d721a2c65c820e15f5fe201a06`. This unit verifies the held bytes and re-decodes the member without executing Flash. No new download or repeated source query occurred. The HTML's HTTP download link and acquired HTTPS URL are recorded separately, without assuming response equivalence.

[The prior WF334 review](https://github.com/AveLyra/911-conspiracy-investigation/blob/6e9ce8fa287fa4410241bc8fba303cefd6476467/investigation/broader-evidence/telephone-wf334-recording-lead-2026-11-02/README.md) pins the other record to [physical 68–70](https://www.les-crises.fr/wp-content/uploads/2016/06/Team7-Box13-Flight-Call-Notes-and-302s.pdf#page=68), production footers **000000766–768**, in a 73-page third-party public reproduction of FBI-form records. The literal name is on **physical 68, Event paragraph, footer 000000766**. PDF SHA-256: `e3cf374351cb753d1297433f86bb5807c56cb42a6dc69837a9df02dd0d54f4aa`. This unit reuses that full-page reading; it does not newly authenticate an FBI master or reread all 73 pages.

## Exact decoded locators

Offsets start at zero at the beginning of the **uncompressed AA77.swf**, including its file header. The member is **FWS**, already uncompressed. IDs are dictionary-character identifiers, not frames, people, calls or page numbers. Body lengths exclude the tag header. Text comes from glyph indices and embedded font mappings, not assumed literal ASCII substrings in the binary.

| Text | Character ID | Tag offset, bytes | Body length, bytes | Font ID |
| --- | ---: | ---: | ---: | ---: |
| `Reuben, Todd` | 331 | 61,801 | 49 | 158 |
| `Reuben, Todd` | 930 | 192,906 | 49 | 126 |
| `Reuben` | 1786 | 3,576,769 | 41 | 1012 |
| `Todd` | 1787 | 3,576,816 | 37 | 1014 |
| `American Airlines Flight #77` | 433 | 113,604 | 81 | 126 |

All five are root-level **DefineText**, tag **11**. [OBSERVATIONS.json](OBSERVATIONS.json) also preserves four navigation definitions: IDs **422** (Flight 93), **427** (Flight 11), **429** (Flight 77), **431** (Flight 175), with exact glyph, offset, bounds and font locators. Their presence fits the court page's stated multi-flight scope and cautions against inferring a specific flight/call relationship from the filename alone.

The four name definitions belong to **one presentation**. They are not four independent confirmations or four calls. Independent origin of the court summary and investigative accounts is not established.

## What this can test

The name similarity supplies a candidate for checking WF334's spelling and identification basis. It does **not** establish that the names identify the same person, that this person left the alleged message, that it came from Flight 77, or that it falls within the previously reviewed family-canvass scope. No court seat, native manifest row, recipient, device, carrier event or session is assigned here.

The title and names coexist in the asset; their display-list/action relationship and actual runtime display were **not** tested. Nearby unrelated personal/profile fields were not interpreted. A prosecution summary is not a native airline manifest or a judicial finding authenticating every assertion.

An inaccurate tip, clerical spelling variation, a different person, an earlier or misattributed message, and a genuine relevant message remain untested possibilities. None is selected. The original tip identification basis, contact/disposition, recording/custody, independent passenger/flight record and carrier/canvass join would discriminate between them.

Nothing here adds a verified canvass recipient or refutes the prior four-unknown-call attribution account. It does not establish fabricated calls, concealed evidence or coordinated wrongdoing. The prior header/receipt/event/assignment values, typed **WF334** and handwritten **WF8406** remain preserved in their original record roles.

## Reproduction and limits

The earlier decoder was reused unchanged: SHA-256 `62f254468e5bbc265d3a04a44c735a09da65339c3a13e1f79046b6e503410617`. It passively re-decoded **548 text definitions**, producing exactly the same JSON-serialized result as the preserved extraction. This unit examines and publishes **nine selected definitions**, including four name definitions; it does not substantively review every name, call or screen.

Run `python3 verify.py --court-zip /path/to/court-flights.zip` to verify archive/member bytes and reproduce the selected font/text records. `python3 verify.py` alone checks the published bundle. [VERIFICATION.json](VERIFICATION.json) records actual runs. Reproduction using the same decoder is not independent method validation, identity authentication, audio analysis, carrier reconciliation or runtime-display verification.

Two initial local comparisons failed: numeric keys in raw Python font/tag dictionaries differ from JSON string keys; the first correction overlooked the tag dictionary. Complete JSON-serialized equality was subsequently tested. These are our comparison errors, preserved locally, **not historical source anomalies**.

[OPEN-TODOS.md](OPEN-TODOS.md) carries forward all five tracks and 18 original requirements plus the identity/message/court-source targets. Earlier records, assessments and conflicts remain unchanged. [REVISION.diff](REVISION.diff) is the actual additive text diff against the preceding combined review. [CHECKLIST.md](CHECKLIST.md) separates completed source work from unperformed authentication. Neither this bounded check nor publication completes an original-record criterion.
