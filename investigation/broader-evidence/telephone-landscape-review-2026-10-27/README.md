# UA93 telephone tables: one SCP-field mismatch and limits on counting

October 27 investigation unit; follow-up inspection completed October 28, 2026 UTC. Existing AUD016-A1 / TC05-B105 / TC06-B110. This adds a narrow held-record comparison to the [carrier-enclosure study](https://github.com/AveLyra/911-conspiracy-investigation/blob/ad7be60185f5d3a49f0e0b7564f4da3610afaf92/investigation/broader-evidence/telephone-carrier-enclosures-2026-10-27/README.md). Earlier records and assessments remain preserved.

**One candidate-matched UA93 row has different visually read “Scp Duration” values: 7565 in the airline summary and 7555 in the carrier-table continuation. Its “Duration Connect” value is 14 in both.** The ten-unit difference is an unresolved image-level observation. It is not a measured ten-second difference in conversation length, evidence of an altered call, or an authenticated carrier-database inconsistency.

## Sources and actual inspection

The held [public reader](https://www.scribd.com/document/13499791/T7-B13-Flight-11-Calls-Fdr-Response-From-DOJ-to-Doc-Req-14-Calls-From-AA-11-and-77-and-UA-175-and-93-ATT-Wireless-UA-And-GTE-Airphone-Call-Record) supplies JPEG reproductions. The acquisition study already obtained these images; this unit made **no new source download or network search**. All four originals were viewed and their SHA-256 values rechecked. They are not agency-native PDFs, authenticated original releases or native network exports. SOURCE-PINS.json preserves the exact asset URLs, original access UTC, byte lengths and digests.

| Reader page | Printed subject | Inspection in this unit |
|---|---|---|
| [25](https://html.scribdassets.com/5bafzdomdce6sz3/images/25-a00d283656.jpg) | United Airlines Flight #93 — Telephone Calls | Header, row accounting, timezone legend, two cellular additions and one selected key/time/duration row |
| [26](https://html.scribdassets.com/5bafzdomdce6sz3/images/26-6b763d149c.jpg) | United Airlines Flight #175 — Telephone Calls | Header and column structure; no complete numeric transcription or call reconstruction |
| [27](https://html.scribdassets.com/5bafzdomdce6sz3/images/27-e74aaab25b.jpg) | UA 93 GTE Airfone Records, 1 of 2 | Body-row accounting and selected final-row printed key/time |
| [28](https://html.scribdassets.com/5bafzdomdce6sz3/images/28-778a401475.jpg) | UA 93 GTE Airfone Records, 2 of 2 | Body-row accounting, continuation fields and selected final-row time/durations |

The four landscape pages therefore concern UA93 and UA175, not AA77. GTE table semantics cannot be imported into the earlier AA77 AT&T/Claircom evidence merely because these pages occur in the same reader. This is not a transcription of every cell on four pages or an independent census of calls.

## L01 — Candidate row association, with its assumptions exposed

Count data rows from the top below the headers. Summary page 25 row 9 and carrier page 27 row 35 have the same manually read full printed Acis Call Id and time label **9:37:41**. Raw identifiers remain local. The public label **U93-A** is our temporary association label, not a caller identity or an assertion that the carrier key is globally unique.

Page 28 does not repeat that Acis key. The association from page 27 row 35 to page 28 row 35 relies on the two printed continuation labels, equal visible body-row counts, final-row position and the repeated **9:37:41** date/time label. This is a candidate continuation join, not an authenticated database join. Misassembly, independent sorting, a repeated/reused key, a transcription error or a changed export could weaken it. No full cross-page uniqueness or ordering validation was performed.

Native upper-left pixel locators, with rectangles interpreted as left/top inclusive and right/bottom exclusive:

- Summary page 25 selected time/key: **[140,257,277,283]**; durations: **[1018,257,1144,283]**.
- Carrier page 27 final-row key/time: **[148,411,521,435]**. This rectangle also includes the preceding row; the final row is the selected one.
- Carrier page 28 final-row durations: **[583,410,717,435]**. This rectangle also includes the preceding row. The time is on the same final row in the full source image and the separately inspected left-hand strip.

Focused nearest-neighbor reading crops preserve the underlying pixels; they add no source detail. Source bytes remain unchanged. Independently recheck the linked original images, especially the small digit under discussion, before relying on this as a precise numerical discrepancy.

## L02 — Preserve the two SCP readings and the agreement beside them

| Source row for U93-A | Printed time label | Duration Connect | Duration Operator | Scp Duration |
|---|---|---:|---:|---:|
| Summary page 25, row 9 | 9:37:41, ET | 14 | 0 | **7565** |
| Carrier continuation page 28, row 35 | 9:37:41, no timezone established here | 14 | 0 | **7555** |

These are **manual image readings**, not values extracted from a native carrier table. The conditional arithmetic is 7565 − 7555 = **10 field units**. The units and operational definition of “Scp Duration” were not established. Neither the matching 14 nor the zero operator field establishes an actual conversation, its participant, its length or the absence of operator handling.

The matching Duration Connect and Duration Operator fields are contrary evidence to a claim that every duration on this candidate row differs. They do not explain the SCP difference. The summary and carrier reproduction may derive from the same source and cannot be counted as independent corroboration of historical events.

One initially considered difference in Duration Connect did **not** survive focused reading: a coarse view of the continuation could be misread as 10, but its enlarged original pixels read 14. That was our viewing limitation, not a conflict between historical versions. We did not publish the provisional 10 as a source value. The SCP readings remain side by side; no source is selected as controlling and no cause is adjudicated.

Possible explanations include a reading error, copying/assembly error, or differing export/transformation states. These are **untested hypotheses**. They do not establish tampering, fabricated calls, a cover-up or why either value was printed. A higher-resolution authenticated scan, native export, field dictionary and source-to-summary transformation history are the discriminating records.

## L03 — Table rows, service categories and clocks are different quantities

Manual visual row accounting gives:

| Held representation | Visible rows in counted scope | Counting limit |
|---|---:|---|
| UA93 summary, keyed airphone portion | 35 | Printed data rows, not independently established calls or conversations |
| UA93 summary, separately labeled cellular portion | 2 | Two additions below the keyed portion; not silently merged into carrier-table coverage |
| UA93 carrier page 27 | 35 | First half of a two-page table |
| UA93 carrier page 28 | 35 | Continuation columns; **not 35 additional calls** |

Thus the summary contains 35 + 2 = **37 visible rows in those categories**, while the carrier table has 35 row positions across two pages. This is not an inconsistency merely because the totals differ. Nor does equal row count prove a complete 35-row match, 35 unique attempts, 37 unique people or any particular number of successful conversations. No all-key uniqueness test or full row-by-row transcription was performed. The counted scope excludes headers, legends, annotations, footers and privacy notices.

The summary explicitly distinguishes **ET / Eastern Time Zone** and **INT / Indiana Time Zone**. Two early keyed rows carry INT; later rows carry ET. The selected row carries ET. The carrier pages do not establish equivalent timezone calibration here. Preserve the source's mixed labels; no automatic offset, clock conversion or inference about post-crash calls is applied. Source labels, real elapsed time and synchronized historical clocks remain separate.

## Verification and remaining records

`verify_landscape.py` checks the four original source digests, the supplied local selected-key equality with an unequal-key negative control, selected repeated time labels, the supplied duration-field agreement/difference, continuation row counts and counting-category arithmetic. RESULTS.json records the actual checks. These are checks of pinned bytes and manually supplied observations, **not independent OCR, historical authentication, a network-schema test, validated clock alignment or a physical experiment**. There is no false precision about the fraction of all telephone evidence verified.

Raw source images, crops, full OCR, printed network/payment/contact identifiers, local paths and coordination material are excluded from the public payload. Safe field transcriptions, precise source locators, source pins, code, results and revision records are included. No external OCR, downloaded executable, dependency installation, outreach, fee, new request, filing or personal mailbox access occurred.

Priority telephone inputs remain the complete agency Request 14 release and assembly/receipt history; carrier-native events and Acis key/field/time definitions; the summary's compilation/version history; OSPS transfer/collect/billing legs and office switch records; the original September 20 analysis and attachments; and source-to-court-exhibit worksheets. The earlier **154/159**, **eight/seven**, **direct/collect**, **connected/unconnected**, uncertain **07:26:18/07:26:28**, and hosted **609–631 / fax 011–033** gap remain unchanged and unresolved. This UA93 finding does not supply the missing AA77 caller/operator/office joins.

All five original-record tracks remain active: FAA correction/delivery and signed disposition; telephone originals and leg joins; recorder continuity/custody/schema/clocks; materials native measurements/specimen joins; and steel preservation/intake/attribution. This small table comparison advances held-source checking and identifies a source-to-summary retrieval question. It does not complete those criteria or turn an uncertainty into conspiracy evidence.

CHECKLIST.md accounts for scope, findings, contrary evidence, unresolved inputs and publication. README.diff is the exact first-addition diff. REVISION-STATUS.json records earlier-report hashes, checked unchanged. Publication and delivery to Overview are verified separately after the research check; successful delivery does not prove integration into the destination chat's master list.
