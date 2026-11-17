# Claircom terminal manual: follow-on and blocked-call records

November 16, 2026 · AUD016-A1 / TEL02–TEL04. The [publicly hosted manufacturer manual](https://christner.co/pdf/techdoc/install/TTWsample09.pdf) is *Air Terminal Installation, Operation, and Maintenance Manual*, document 8018721, version 3, dated May 17, 1993, for models 264 and 296. Retrieved November 16, 2026; PDF 98 pages, 738,865 bytes; SHA-256 `4fce58612d06a9f112b4d81b04b1dd901f5618794de7f0116dc6b79418847e2c`. The document says copyright Claircom, all rights reserved; this report links to it and does not republish the manual. PDF metadata lists a 1997 creation and 2020 modification date, distinct from the document’s printed 1993 date; neither metadata date establishes a revision or the date the text was authored. The hosted copy is an author's portfolio copy, not a contemporaneous airline maintenance log.

## Source observations

- In section 5.6, printed pp. 5-7–5-8, the manual describes dialing, operator access and use of a NEW button to end a call without dropping the air-to-ground link. It says a follow-on call using NEW need not re-enter a credit-card number and that this feature's use is recorded in the call data record. The source describes a system design, not a demonstrated event on September 11.
- On printed p. 5-9 it says a carrier can configure blocks for called numbers and that blocked calls are recorded as such. This identifies a potentially informative field or event category; the manual does not provide the case-specific field dictionary needed to identify it in the released records.
- The source's discussion describes the specified models and version. It does not establish which hardware, software, carrier options or settings were installed on a particular aircraft in 2001, nor whether the historical records contain every call leg. The patent-based [prior platform review](https://github.com/AveLyra/911-conspiracy-investigation/tree/codex/faa-warning-court-exhibits-2026-10-28/investigation/broader-evidence) remains a distinct design account, not evidence that this manual was deployed on a specific aircraft.

## Interpretation and open tests

A retained radio link and a telephone call are distinct concepts in this manual. If an applicable later system and record format used a follow-on marker, native field documentation could test whether closely spaced records are related; the manual alone cannot link any particular entries, caller, recipient, operator or conversation. Nor does a blocked-call description show that a particular attempted call was blocked. The existing collect/direct, connected/unconnected and timing accounts remain unchanged; this source does not resolve them or establish fabrication, suppression or intent.

- [x] Acquire and hash a public manufacturer manual; limit the read to cover and section 5.6, pp. 5-7–5-9.
- [ ] Obtain aircraft-specific equipment and software configuration, 2001 operating procedures, and effective carrier record layout/field definitions.
- [ ] Obtain source-native carrier/operator and office records with timestamps and event keys; test any proposed linkage against alternative call-leg mappings.
- [ ] Preserve independent, potentially conflicting service descriptions and the unlocated underlying recordings. No native voice or switch evidence was acquired in this step.

Earlier findings are unchanged; this is a separately named source pin and does not replace the previous analysis. A hash confirms the acquired file's bytes, not its applicability to a particular flight.
