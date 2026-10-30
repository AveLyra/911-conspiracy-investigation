# FAA retention instruction: the released email behind an earlier OIG quotation

October 30, 2026. Existing B129 / PD04–PD05, with PD01–PD03 and FAA01–FAA04 still open. **An official released one-page email now supplies the wording and scope of a September 14, 2001 retention instruction previously known here through a DOT OIG quotation.** It does not recover the corrected May 2003 answer, signed action/no-action decision or recommendation-closure record.

## The newly acquired original-record copy

NARA item [7596109 / AEA2579](https://catalog.archives.gov/id/7596109) directly exposes the [email PDF](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/1-AAL-77/e-Other/1-AEA-2579-EMAIL--REF-RECORD-RETENTION-REGARDING-09-11-EVENTS.pdf). The response acquired October30 at15:32:26UTC was HTTP200, application/pdf, **24,441 bytes / one page**, SHA-256 **ace9aa35cb266decd2344d48c06bd0d2625cfc5ce2bded8dd2bafdca67898329**. The complete page image was visually read. This is a released printout/scan of an email, not its native mailbox message, message-ID headers, server delivery record or independently authenticated sender signature. The hash identifies these acquired bytes.

The page prints **09/14/2001 01:00 PM** and a subject concerning record retention for September11. No time zone for the header timestamp is established. The body addresses all facilities and directs them to **“Retain and secure until further notice”** administrative and operational data and records. It ends the uncertainty instruction with **“RETAIN IT.”** Exact page and extraction-line locators are in [SOURCE-PINS.json](SOURCE-PINS.json).

Preserve the time expressions as printed, without substituting a reconstructed interval:

| Field on original page1 | Recorded expression | Boundary |
|---|---|---|
| UTC window, extraction line12 | **110000 UTC to 120400 UTC** | Day/time notation is not expanded into a newly authenticated clock timeline. |
| Local example, lines12–13 | **September 10, 2001; 2000 - 2400 local** | The printout supplies this example; no independent zone/clock calibration is acquired. |
| Local example, lines14–15 | **September 11, 2001; 0000 - 2400 local** | The source splits the word September across lines; the ranges and original printout remain unchanged. |

The facility examples on line16 include Centers, Terminals, AFSS's, FSDPS's and FCT's; line17 asks hub managers to notify appropriate FCTs. These provide distribution and acknowledgment retrieval targets. A body addressed to all facilities does not prove actual delivery to every office or person. No recipient list, signature image, contact detail, raw scan or full extraction is republished here.

## Compare the instruction with the earlier accounts

| Source layer | What it says or supplies | What remains unproved |
|---|---|---|
| New released email, page1 | Date, exact retention wording, time examples, facility categories and an instruction to pass the notice to appropriate FCTs | Native authenticity, transmission, acknowledgment, execution, later withdrawal or amendment, and actual records retained. |
| Held [DOT OIG CC-2004-003](https://www.oig.dot.gov/sites/default/files/cc2004003.pdf#page=8), physical/printed8 | Quotes a September14 directive; reports that the two managers received it and did not follow it; records the quality-assurance manager's explanations, including that the tape fell outside the instruction | Those receipt/action findings remain OIG's findings based on its investigation. The newly read email alone does not independently prove them. |
| Same OIG report, physical/printed22 | Records an investigation-staff manager's narrower description of the intended preservation of voice communications, radar data and facility records that otherwise faced the normal fifteen-day cycle; also records the local manager's contrary application to the taped statements | The underlying interviews, complete question/answer context and governing-policy/case-specific reasoning are not acquired by this pass. Broad source wording and reported interpretations remain side by side. |
| Later [2005 special records schedule, pages2–3](https://www.archives.gov/files/records-mgmt/rcs/schedules/departments/department-of-transportation/rg-0237/n1-237-05-004_sf115.pdf#page=2) | Separates permanent originals/audio re-recordings from temporary backup, convenience and dissemination/revision copies | No acquired document establishes how this later schedule interacted with the September2001 instruction, identifies an actual disposal under it, or includes every 2003–2006 correction/action record. |

The held OIG source pin is 400,367bytes,24pages,SHA-256 **4eb4bff61710c3d339d98fdcd222bdc86a2dd775a086f0a2b45a7988e50ffdd5**. This pass reused the earlier preserved page-text/passages for pages8 and22; it did not freshly acquire, visually reread or reauthenticate the entire report. The two accounts' close date/wording match supports tracing the released email as a counterpart of the quoted directive. It is not native-message authentication or two independent witnesses to the underlying destruction.

The 2004 OIG tape inquiry is distinct from the later May2003-answer/correction and 2006 administrative-disposition trail. The email's stated September2001 data window does **not** by itself establish coverage of documents created in2003–2006. No source is declared controlling, and the later schedule is not treated as an automatic withdrawal of the earlier instruction.

## What this changes, and what could weaken it

We can now inspect a released counterpart of a specific preservation instruction rather than relying solely on an investigator's selective quotation. Its explicit temporal and facility scope narrows the next retrievals. **The instruction is evidence of a preservation direction; it does not by itself establish compliance, unlawful disposal, intent, coordination or a cover-up.** Ordinary preservation efforts and disputed application to a specially created tape are relevant contrary evidence; neither is silently adopted as the resolved explanation.

A different native version, a documented superseding instruction, incomplete distribution, or a supported case-specific interpretation could change applicability or receipt. Conversely, actual distribution acknowledgments and records of deliberate noncompliance could strengthen an event-level conclusion. Those discriminating records remain unacquired. The managers' underlying actions are not independently retested here.

## Search, reading and publication limits

Two within-series catalogue queries were performed: `corrected` showed117hits and `administrative`219. These are search results, not numbers of relevant events or independent records. Only selected first-page titles were inspected, with NARA-ID and relevance sorting; no complete census or negative existence conclusion is claimed. The intended ten-title display cap was exceeded in the corrected views:20titles and16complete titles plus one ID were emitted. The administrative views each read10titles. The deviation is preserved in [READING-SCOPE.json](READING-SCOPE.json); capturing a full DOM is not reading every title or PDF. Raw DOM remains local.

One directly exposed PDF was acquired; one complete page image was read. Text extraction used Python3.12.14 / pypdf6.10.0; an earlier fitz import failed before extraction and was not reported as successful. The verifier checks source bytes/page count and six selected textual anchors. These checks verify documentary transcription and source identity to that scope; they are not an experiment, delivery proof or native-email authentication. [Actual checks](VERIFICATION.json), [reproducer](verify_original.py).

The source research and original PDF are preserved separately from this public derivative. Previous source records and public versions remain unchanged. The exact additive text diff is [REVISION.diff](REVISION.diff); image reading is separate from that text diff. All five work-plan tracks and eighteen substantive acceptance criteria remain unfinished. [Open records and discriminating tests](OPEN-RECORDS.md), [requirements checklist](CHECKLIST.md).

This bundle's creation is not evidence of a public push. Commit/push/PR status must be verified separately; no absent public file or unpushed commit is presented as published.
