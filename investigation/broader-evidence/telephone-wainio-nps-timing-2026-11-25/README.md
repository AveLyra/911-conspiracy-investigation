# Flight 93 call: two National Park Service time labels

**Scope:** TEL02–TEL04 / AUD016-A1. Public HTML sources fetched November 25, 2026. Both NPS pages describe the same named passenger calling her stepmother from row 33. They appear to present the same call, but the underlying call record has not been joined independently. This is a comparison of published accounts, not a new measurement.

## Observations preserved

- The [NPS phone-call listing](https://www.nps.gov/flni/learn/historyculture/phone-calls-from-flight-93.htm) labels the entry **“9:53, Row 33 ABC”** and gives a duration of **4 minutes, 29 seconds**. It attributes the entry to FBI, trial evidence and a family statement. Acquired HTML lines 3335 and 3342–3345; SHA-256 `3521bd59a1c42b8f33a449465336597ce493ae2a64693ee289bd802b9d40f076`.
- The [NPS general timeline](https://www.nps.gov/flni/learn/historyculture/september-11-2001-timeline.htm) labels the event **“9:54 am: Passenger phones stepmother”**, describes about four and a half minutes and cites note 81. Acquired HTML lines 692–694; SHA-256 `fbd2315314ae337ff39e5a3838a691ff8f9c79a02cf0cbf3f4baf5979e64f243`.

The one-minute label difference is unresolved. The descriptions are consistent in broad duration, and neither page is an independent carrier record. Different rounding, transcription, clock conventions or selection of an event time are **untested possibilities**, not findings; neither label is selected as controlling. The discrepancy alone does not establish a fabricated call or deliberate alteration. The underlying records and time-field definitions could change this assessment.

## Additional candidate; not yet verified from source bytes

A search service text rendering of a separately released [FBI interview bundle](https://vault.fbi.gov/9-11%20Commission%20Report/9-11-interviews-2001-09-sep-01-of-08/at_download/file) attributes approximately **10:00 a.m.** to the recipient's recollection. This is a candidate account, not a validated transcription: the direct retrieval returned HTML rather than the expected PDF, so the document bytes, page placement and visual reading were not verified in this pass. An approximate recollection and a published call label do not necessarily represent the same defined time. The source may contain personal information; no such details are reproduced here.

## TODOs

- [ ] Obtain the actual FBI release PDF and visually inspect the relevant interview and page, including time wording; retain its source, hash and release version. Do not reconstruct redacted information.
- [ ] Obtain the original call record and its time-zone, rounding, event and duration field definitions; join the row to the two NPS descriptions before testing the one-minute difference.
- [ ] Inspect the trial evidence and primary family-statement sources underlying the two pages, including their edition and chronology; independently preserve inconsistent accounts and any contrary evidence.

The two NPS HTML responses were acquired and searched; no carrier data, original recording, timestamp calibration or field mapping was acquired. This additive report does not change prior findings.
