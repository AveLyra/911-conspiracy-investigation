# Carrier records: duration fields, event context and a page gap

October 27, 2026. Existing AUD016-A1 / TC05-B105 / TC06-B110. This supplements the [telephone-source review](https://github.com/AveLyra/911-conspiracy-investigation/blob/639bd09f9f8116707df2be5fb04d87472afd58cb/investigation/broader-evidence/telephone-originals-2026-10-27/README.md) and [September 20 analysis](https://github.com/AveLyra/911-conspiracy-investigation/blob/5031c6dfa73e1f59491f259e00f168c37cb21788/investigation/broader-evidence/telephone-usage-report-2026-10-27/README.md). Neither is rewritten.

**The acquired carrier-record images supply the printed value 159, but do not authenticate a particular conversation or caller.** They also show why a zero-duration field needs its event and call-leg context. A hosted-copy page gap is documented. The 154/159 discrepancy and early connected/later unconnected accounts remain unresolved.

## C01 — Acquired record and limits

Normal navigation of the [public reader](https://www.scribd.com/document/13499791/T7-B13-Flight-11-Calls-Fdr-Response-From-DOJ-to-Doc-Req-14-Calls-From-AA-11-and-77-and-UA-175-and-93-ATT-Wireless-UA-And-GTE-Airphone-Call-Record) exposed 28 page images: one DOJ cover letter and 27 enclosure images, totaling 2,565,900 bytes. [SOURCE-IMAGES.json](SOURCE-IMAGES.json) records exact queryless URLs, access times, formats, dimensions and SHA-256 values. All 28 JPEG entities were obtained without cookies, tokens, sign-in or the gated download action. These are hosted image reproductions, **not the agency-native PDF, a complete authenticated release or native switching data**.

The [April 26, 2004 DOJ letter, reader page 1](https://html.scribdassets.com/5bafzdomdce6sz3/images/1-65f7ebcbf8.jpg) describes 50 enclosed pages from the EDVA USAO in response to Commission Request 14. It says the records were sent before formal processing, with Bates-stamped copies to follow. The held carrier images already bear Bates stamps; this hosted object cannot simply be identified as the original pre-Bates delivery. The letter, selected fields and page boundaries were read. **Not every table entry on all 28 pages was transcribed or checked.** The final landscape headers identify UA93, UA175 and two UA93 GTE record tables; their substantive call tables are not analyzed here.

## C02 — Preserve the hosted-copy page gap

Source-pixel inspection verified reader pages 2–10 as **M-WFA-00000600 through 608**, fax labels 002–010; pages 11–24 as **M-WFA-00000632 through 645**, fax labels 034–047. Thus Bates suffixes 609–631 and fax labels 011–033, 23 labels in each series, are absent between adjacent reader images 10 and 11. [Every inspected label](PAGE-ACCOUNTING.json).

The letter's 50 minus the 27 held enclosure images also equals 23. This is a useful accounting lead, **not proof that these counts describe exactly the same omitted material**. The missing contents, responsible version/compiler and release history remain unknown. A partial upload, assembly/version differences and more consequential omissions remain untested possibilities. No agency destruction, withholding or deliberate exclusion is established. Bates values for reader pages 25–28 were not authenticated here.

## C03 — A carrier field supports 159; 154 remains on record

[Reader page 21 / M-WFA-00000642, lower block](https://html.scribdassets.com/5bafzdomdce6sz3/images/21-1a330ff42d.jpg) prints Start Time 07:25:48, Billing Start and Answer Supervision 07:26:22, Duration 159 and Event Time 07:29:01, on September 11, 2001. Event Time minus Billing Start is 159 seconds; minus Start Time is 193 seconds. The difference is 34 seconds. No universal billing or conversation-duration rule is inferred.

The court's held AA77 SWF separately stores 09:25:48 and 159 SECONDS. [Static pins, offsets and source hashes](COURT-PINS.json). A **conditional +2-hour label comparison** gives matching starts, and the duration values agree. That is a candidate record-to-exhibit association, not clock calibration, a network-ID join, independent corroboration of a conversation or identification of its caller. Both presentations may derive from the same carrier evidence.

The Commission's [final-report note 57, printed page 455](https://www.9-11commission.gov/report/911Report_Notes.pdf#page=7) says 2 minutes 34 seconds, or 154 seconds; the May 2004 briefing and court store 159. Those earlier conflicting values are preserved. The new carrier field strengthens the source trail for 159; it **does not establish why 154 was written or adjudicate the discrepancy**.

## C04 — Zero fields occur in specific event contexts

The upper block on [reader page 21](https://html.scribdassets.com/5bafzdomdce6sz3/images/21-1a330ff42d.jpg) prints Event Type Routed to AT&T OSPS (29), Duration 0, the 1969 date in Billing Start/Answer Supervision and Event Time 07:26:28. The neighboring lower block prints 159; both show Start Time 07:25:48. This is a reason to acquire event and leg definitions before treating any zero as an end-to-end no-conversation finding. A common printed start alone does not prove the same physical call or leg.

Separately, [reader page 16 / M-WFA-00000637, upper block](https://html.scribdassets.com/5bafzdomdce6sz3/images/16-6aa0e8fe82.jpg) prints Air Party Disconnect (4), Claircom (1), Duration 0, the 1969 fields and Event Time 07:19:57. Zero appears in more than one displayed event type; **it is not universally explained here as a routing-only field**. The court's 09:18:58 zero/unconnected label remains as published. Its native event join, recipient and network classification remain unverified. The September 20 report's description of a caller connected to the Solicitor General's Office remains alongside it. Different legs, classifications or error remain untested possibilities.

The 1969 fields are observed values. A default/epoch display is a hypothesis requiring system definitions, not evidence of a 1969 conversation or an authenticated explanation. Anonymous annotations are not promoted into a carrier data dictionary.

## C05 — Check duration against both possible anchors

[Reader page 13 / M-WFA-00000634, top continuation](https://html.scribdassets.com/5bafzdomdce6sz3/images/13-ec2683a0f2.jpg) prints Billing Start 07:13:11, Answer Supervision 07:13:23, Duration 158 and Event Time 07:15:49. The billing interval is 158 seconds; the answer interval is 146 seconds. The 12-second difference warns against simply equating this Duration with answer-to-disconnect talk time. [Reader page 15 / M-WFA-00000636, upper block](https://html.scribdassets.com/5bafzdomdce6sz3/images/15-d3c94df2c0.jpg) prints Billing Start and Answer Supervision 07:16:59, Duration 102 and Event Time 07:18:41; both intervals equal 102 seconds. These selected checks do not establish how every call was billed or connected.

## Verification and remaining work

[FIELD-OBSERVATIONS.json](FIELD-OBSERVATIONS.json) provides manually read values, source hashes, page/Bates references and native image rectangles. [verify_fields.py](verify_fields.py) checks those inputs, interval arithmetic, page accounting, a deliberately wrong duration anchor, and five stored court-text definitions from the hash-pinned official ZIP. It never executes Flash. [Actual output](COMPARISON-RESULT.json). Hashing, arithmetic and static-text decoding are separate from historical authentication and caller/leg identification.

OCR misread dates, time digits and Bates suffixes. Original OCR remains local; source pixels control our reported transcription. Automated field views clipped fields or included adjacent fragments; manual strips also included neighboring fragments. **No source images, full OCR, QA crops or raw financial/contact/network identifiers are in this public payload.** Poor crops and navigation mismatches are our processing limitations, not anomalies in the carrier records. [Exact scope and failures](METHOD-AND-LIMITS.md).

[Outstanding originals](OPEN-RECORDS.md) include the complete agency release/version chain, native carrier events and definitions, operator and office records, exact call/leg joins, clock settings and source-to-exhibit mapping. No caller was newly identified, no historical discrepancy adjudicated, and no fabricated call, unlawful disposal or concealment established. These findings can weaken simplistic interpretations of zero fields while leaving substantive questions open. The broader original-record investigation remains incomplete.

[Checklist](CHECKLIST.json) · [Diff from the preceding preserved draft](README.diff) · [Complete public addition](PUBLIC-ADDITION.diff) · [Earlier-document status](REVISION-STATUS.json). Earlier sources, reports and published history remain unchanged.
