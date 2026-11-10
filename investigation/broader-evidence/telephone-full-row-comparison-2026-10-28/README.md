# UA93: all 35 keyed row positions compared, with uncertain joins retained

October 28, 2026. Existing **AUD016-A1 / TC05-B105 / TC06-B110**. This extends the [earlier selected-row review](https://github.com/AveLyra/911-conspiracy-investigation/blob/74b2133ec389d68dd9906ccf89894442d07b58b7/investigation/broader-evidence/telephone-landscape-review-2026-10-27/README.md). No new native carrier record was acquired.

**The supplied readings give 33 matching full printed keys, two uncertain-key candidate associations and matching Duration Connect fields across all 35 candidate pairs. One apparent operator-field discrepancy needs a better source.** This is evidence about the held images and our readings, not an authenticated reconstruction of calls.

## Scope and preserved sources

The three held JPEGs are hosted reproductions of released records: [reader 25, airline summary](https://html.scribdassets.com/5bafzdomdce6sz3/images/25-a00d283656.jpg); [reader 27, UA93 GTE table 1 of 2](https://html.scribdassets.com/5bafzdomdce6sz3/images/27-e74aaab25b.jpg); [reader 28, continuation 2 of 2](https://html.scribdassets.com/5bafzdomdce6sz3/images/28-778a401475.jpg). Exact entity URLs, original access times, dimensions, lengths and SHA-256 values are in [SOURCE-PINS.json](SOURCE-PINS.json). They remain unchanged.

All 35 keyed row positions in each representation were inspected in the time, key and three duration columns. The two separately labeled cellular additions are excluded from this comparison. This is **not every cell, caller identity or table in the larger release**. Full pages and focused nearest-neighbor reading copies were inspected; enlargement added no information. No new OCR, software installation or downloaded executable was used. Raw identifiers, card/contact data and images remain local and are excluded from this public addition.

Both representations were transcribed separately by the same analyst before the comparison. This was not a blinded or independent-expert reading. Uncertain characters were retained rather than filled from the desired match. The [row locators](ROW-LOCATORS.json) preserve original order and approximate native-pixel bands; the row number below the header is the primary locator. The continuation carries time/position but no repeated full Acis key, so its association to reader 27 remains a source-page continuation assumption.

## F01 — Most selected fields agree, and time alone is insufficient

| Checked quantity | Result | What it does not prove |
|---|---:|---|
| Keyed row positions per representation | 35 | Not 35 independent people or conversations. |
| Accepted full printed key pairs | 33 | Key allocation/global uniqueness and historical event identity unverified. |
| Uncertain-key candidate pairs | 2 | Summary rows 25 and 31 remain candidate associations, not full-key matches. |
| Repeated time-label groups per representation | 2 | A time-only match can pick the wrong row. |
| Matching Duration Connect pairs | 35 | Field semantics, units and completed conversations unverified. |
| Operator fields reading zero per representation | 34 | Not proof of no operator handling. |
| SCP pairs with accepted numbers in both | 25 | No inference from the ten unaccepted/blank pairs. |
| Equal SCP numbers / differing SCP numbers | 24 / 1 | Not independent network corroboration; sources may share inputs. |

Full-key matches do not depend on source order; the carrier rows are in a different sequence. The two masked-key candidates use repeated time plus Connect value in the remaining rows, and are explicitly weaker. In particular, two rows share **9:42:44**, and two share **9:43:48**, within each representation. That is a reason to avoid treating a timestamp as a unique event key; it is not proof of duplicated or fabricated calls.

All 35 candidate-paired Connect fields have positive supplied numbers and agree. This is contrary evidence to an interpretation that the two held presentations generally disagree in that column. It does not establish 35 successful conversations or change what the AA77 zero fields mean: those involve a different service/source. Nor do the two source presentations provide independent corroboration if one was compiled from the other.

## F02 — Apparent operator-duration difference; exact digits unresolved

Summary **row 26**, reader 25, and carrier **row 34**, reader 27/28, have matching accepted printed keys, the **9:43:48** label and Connect **77**. Their operator fields have incompatible manual readings:

| Source | Retained operator-field reading | Limit |
|---|---|---|
| Reader 25, summary row 26 | **3?25** | Second glyph unaccepted; do not publish a precise 3925 as established. |
| Reader 28, continuation row 34 | **14?5** | Third glyph unaccepted; do not publish a precise 1435 as established. |

The accepted leading glyphs differ, but **these low-resolution readings could still be wrong**. The apparent difference therefore remains a qualified source-reading lead. No subtraction, seconds/minutes conversion, post-impact interval or conversation length is inferred. A blank/unaccepted SCP field on this row is not set to zero.

Native-pixel inspection bands: summary **[1018,506,1150,528]**; continuation **[580,405,716,431]**, with row 34 the middle of the three visible continuation rows. These bands include context; they do not add detail. Seek the authenticated higher-resolution scan/native export, exact operator-duration definition and source-to-summary compilation/version history. Those could remove, change or substantiate this apparent difference. No cause is selected.

## F03 — The earlier SCP readings remain, with broader controls

Summary **row 9** versus carrier **row 35** retains **7565 versus 7555**, time **9:37:41**, Connect **14** and operator **0**. The earlier [source-level discrepancy](https://github.com/AveLyra/911-conspiracy-investigation/blob/74b2133ec389d68dd9906ccf89894442d07b58b7/investigation/broader-evidence/telephone-landscape-review-2026-10-27/README.md) is not a newly acquired independent measurement. Its unit and cause remain unknown.

The full-row accounting adds 24 equal accepted SCP pairs around it. Ten pairs have no accepted numeric reading in one or both sources; they were excluded from numerical comparison and not silently converted to zero. A reading error, copying/compilation difference or different export state could affect either apparent discrepancy. These are untested hypotheses, not explanations established by this work. A native dictionary and original source/version join remain necessary.

## F04 — Clocks and identities remain separate

The two early summary rows retain **INT**, and the later keyed rows **ET**. No equivalent timezone field or clock calibration was established for the carrier table. Equal printed time strings therefore do not measure synchronized clocks or authorize an automatic offset. No person was identified from a matching key. The reported 35+2 summary accounting remains a count of visible categories, not an independently verified FBI reconstruction of 37 calls.

## Reproduction, limitations and outstanding originals

[compare_tables.py](compare_tables.py) and [RESULTS.json](RESULTS.json) record **18 passed scoped checks**: three source entities; all row positions; accepted-key subset comparisons; uncertain-key candidate accounting; order reversal and an altered-key negative control; repeated-time ambiguity; and the supplied time/Connect comparisons. The code calculates, rather than assumes, the duration comparison counts. It checks the supplied transcriptions; it cannot certify that the analyst read each glyph correctly. [Input commitments](INPUT-COMMITMENTS.json) identify the unchanged local input without publishing the full keys. Independently transcribe the linked originals before rerunning; do not derive a second input from the first to manufacture agreement.

No agency-native Request 14 delivery, missing Bates 609–631/fax 011–033 pages, network export/schema, operator ticket, office switch log, source-to-exhibit worksheet or authenticated clock join was acquired. The AA77 154/159, early connected/later unconnected, eight/seven, direct/collect and uncertain routed-event digit remain unresolved. This UA93 comparison supplies none of those missing joins.

The current public search pass also acquired no FAA corrected QFR/receipt or signed action/no-action/disposition record. Some queries repeated earlier routes; they were stopped and logged locally as a process limit, not published as evidence of absence or concealment. The recently acquired FAA policy is separate from the actual case acts.

Original images, earlier reports, conflicting values and the full five-track work plan remain unchanged. The [revision record](REVISION-STATUS.json), [exact predecessor diff](diffs/selected-row-to-all-row-review.diff) and [checklist](CHECKLIST.md) account for this additive update. No private case/correspondence, outreach, new request, fee, private push, physical experiment, deletion or source overwrite occurred. All five native-input/testing gates remain open. Public branch/PR delivery and Overview integration are verified separately; publication cannot complete the scientific or historical questions.
