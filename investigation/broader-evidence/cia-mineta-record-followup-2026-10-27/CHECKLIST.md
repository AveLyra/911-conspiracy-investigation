# Publication checklist

This update turns the October 27 source reviews into a public, source-linked summary. It is an addendum to the existing CIA and FAA/Mineta studies, not a replacement for their source records or acceptance criteria.

| Reviewed point | Outcome and location | Source verification | Still unresolved |
| --- | --- | --- | --- |
| Scheuer's allegation about the March 25, 1999 PDB | Included with attribution and a clear limit: it is one interview account, not an independently established motive. `REPORT.md`, section 1. | NARA Document 6: all 11 text pages read; selected native pages include page 7. Hash and URL in `SOURCES.json`. | Author's memorandum, PDB drafts/final, instruction, recipients, and receipt records. |
| Scheuer's UAE-call chronology and “less than 30 hours” statement | Included; the duration is not misdescribed as a call-to-departure delay. `REPORT.md`, section 2. | NARA Documents 7 and 8: all 16 text pages read; selected native pages include the relevant pages. Hashes and URLs in `SOURCES.json`. | Actual call record, clearance, decision chronology, diplomatic cable, source movement, and objection response. |
| Clarke's contrary UAE-call account and page 9 correction | Included; the native page says agreement to call off the attack, not agreement to make the UAE call. `REPORT.md`, section 2. | NARA Documents 2 and 3: all 42 text pages read; native pages 9 and 10 of Document 3 viewed. Hashes and URLs in `SOURCES.json`. | Contemporaneous decision and clearance records; the MFRs are not verbatim transcripts. |
| Clarke's account that he was not told Mihdhar and Hazmi were in the United States | Included as a bounded nonreceipt account, without inferring that nobody at FBI knew or identifying a knowing hold. `REPORT.md`, section 3. | NARA Document 3, especially page 16; fully text-read and selected native images reviewed. | Original visa draft/hold, cable versions, actual recipients, watchlist actions, and later oversight search/production records. |
| CIA draft's systemic watchlisting and tactical/strategic critique | Included with its partial-reading and source-dependence limits. Its August 7 bulletin listing and post-attack effects are separated from recipient knowledge and prior intent. `REPORT.md`, section 4. | 21 of 80 pages fully text-read; six native pages viewed. Exact source and hash in `SOURCES.json`. | Remaining 59 pages, CIA system original, authorship/distribution, underlying event records, and recipient/action evidence. |
| Mineta's January 8, 2004 follow-up memorandum | Included as evidence of a follow-up meeting, not as a timing resolution or retraction. Calendar mismatch is reported only as a literal consistency issue. `REPORT.md`, section 5. | NARA catalog item 2610327: all three pages text-read and viewed as native images. Hash and URLs in `SOURCES.json`. | Meeting notes, question outline, PEOC/call records, contemporaneous movement records, and independent clock evidence. |
| Prior public CIA and Mineta studies | Cross-linked and left unchanged; this supplement does not duplicate their findings or claim to close their open records. | Compared against the immediately preceding public base `7c9530c5`. | Prior reports retain their own methods and open questions. |
| WTC 7 collapse assessment | Explicitly stated unchanged; these records provide no physical mechanism evidence about WTC 7. | Scope comparison with the public repository's WTC 7 charter and synthesis. | All WTC 7 causal-chain tasks remain governed by their existing reports. |
| Raw/private material and legal-case content | Not copied. The publication consists of a report, a source index, a checklist, a text diff, and a one-line navigation update. | Exact changed paths and diff reviewed before commit. | None for this payload; this does not certify unrelated local records for publication. |

## Change and verification record

- Text changes are preserved in [`TEXT-CHANGES.diff`](TEXT-CHANGES.diff), comparing the new report and root navigation edit with their immediately preceding public versions. The new checklist and source index have no earlier public version.
- The existing CIA lead report and Mineta/FAA chronology report are unchanged.
- The deliverable is Markdown and JSON. PDF layout verification does not apply.
- Verification commands: `python3 -m json.tool SOURCES.json` and `git diff --check`.
- A passing hash or JSON check preserves file identity and syntax; it does not authenticate a witness's recollection or prove a historical claim.
