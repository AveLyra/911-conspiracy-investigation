# Approval-breakdowns-a post-freeze comparison

October 4, 2026. Separate, prior-informed AI review after both readings froze. No fresh primary views, retrievals, rendering or source authentication. The original reading notes remain unchanged. Only this additive research review is edited; no engineering, human, historical or full-goal acceptance follows.

## Scope and exact receipts

- Own complete reading, `review.md`: SHA256 `d65ed3af56a2f171da2257d3ecb50d04ecfbd14b9a13be21188d0bd1ddf8379c`.
- Root complete reading, `root-observations.md`: SHA256 `bd0524506ba40572ae443099781107cd3b48db3c6ef1054c602cd0259ee5667d`.
- Governing protocol: SHA256 `fa18d2a1954ff128e948036c911f80fedede736e9b908f0f9d48ae2c68bef732`.
- After own freeze, complete root text was read with `sed -n '1,340p'` (`e2f58d`, exit0, untruncated), and both observation pins checked (`4e66b1`, exit0). The substantive disagreements below were then sent to root before drafting a synthesis.
- For this additive review, own frozen lines47-188 were read using `sed` (`4a11a8`, exit0, untruncated), covering the recorded arithmetic inputs and later comparison conclusions. `shasum -a 256` reconfirmed both notes and the protocol unchanged (`b0ceb5`, exit0).
- Both readers covered all11pages with12views each, including one separately requested/shared repeat of171286physical3. This is separately frozen interpretation of the same source family, not historical independence. Own original view count and immediate page saves were already recorded; this text review does not re-audit invocation chronology.

## Two numeric disagreements requiring explicit disposition

| Field | Own frozen reading | Root frozen reading | Safe treatment before targeted source check |
|---|---|---|---|
| 171286 physical3, row114, switch amount | 1,221 | 1,210 | Preserve both transcriptions; do not describe their difference as a source discrepancy. Own1,221 plus row115's39,264 equals the printed40,485 subtotal, but arithmetic alone cannot authenticate the source numeral. |
| 172947 physical2, July row87, UPS proposal | No proposal amount visible; not received | 1,276; not received | Do not import1,276 from the later November/2002 schedule states into July. Until adjudicated, omit an exact July amount and retain the not-received status and disagreement. |

Root has proposed a separately declared two-field source correction check of the held pages. That is post-result targeted adjudication, not another blind reading or automatic permission to revise the original notes. This review has not performed or received its results. Any later correction should identify the initial transcription error rather than turn an agent error into an alleged historical source anomaly.

Both readers retain the **qualified handwritten12/14/00/bracket interpretation**, versus printed budget dates12/18/00 for40,485 and4/17/01 for762. Do not use the amount reconciliation to resolve that separate chronology/annotation question. The apparent76th payment ordinal is also preserved, not silently normalized. Root's initial Halon shorthand was explicitly corrected to Halotron after its permitted repeat; the own initial reading already used Halotron. That resolved terminology point need not be presented as continuing source disagreement.

## Shared substantive findings and limits

The three related schedules have distinct printed dates and states: July12,1999; November19,1999; April12,2002. Repeated identifiers and scopes support an accounting lineage, but do not produce three independent approval witnesses. Printed dates alone do not authenticate creation dates. Pending, HOLD, being revised, being voided, VOID, zero and blank are not interchangeable. The July far-right numerical column is contextualized by the explicit proposed-cost column on its budget page, not a payment column; the November budget also has approved/to-be-approved and anticipated wording.

All three schedules report CO40's three-inch trench description and1/25/99 approval, CO44R's FSK50/SK58 March19 revision reference and4/8/99 approval, CO55's electrical rerouting and3/11/99 approval, and CO88's **second-floor machine-room corridor fuel piping**,7/7/99 approval130,000 plus prior-line credit85,000. The matching credit is evidence about commercial replacement/adjustment, not proof of two additive installed routes or identification of every physical segment. It does not resolve CO40's exact floor/member/joint.

The November and2002 states report CO97's **two-hour sheetrock in lieu of two-hour vermiculite** fuel-line enclosure,10/27/99. The2002 state adds valve, hatch and suppression-control scopes. These are affirmative protective/coordination descriptions and useful underlying-order leads, not proof of installed rating, inspected completion, event-day functionality or deliberate weakening. Changing scope or status can reflect ordinary project administration. Contrary field records or a different segment/revision could defeat a proposed historical join.

The payment tables expressly assert amounts paid; this is positive documentary reporting, not merely unaccepted proposals. Preserve their mixed approved-for-payment aggregate headings, blank versus populated dates, and November anticipated-balance language. The tables are not independently verified bank transactions or per-order performance evidence. No source in this batch supplies the actual governing route sheets, field-certified fireproofing, member mapping or inspection needed to establish the installation assertions.

## Independent arithmetic on frozen recorded values

Executed a stdout-only `python3 -` calculation with inline lists and assertions (`92f4af`, exit0). It wrote no files and performed no source reads. **All24 asserted arithmetic equalities matched.** The checks are internal numerical consistency of the recorded inputs, not24 independent pieces of evidence, a complete row1-115 cost audit, or financial/engineering validation.

Reproducible input definitions:

```python
base = 12864619
additional = 117684
budget = 14287986
landlord = 1668858
co_july = [7000,102705,28442,26483,42887,125453,27821,3941,
           78288,22721,220262,4874,85000,130000,-85000]
co_nov = co_july + [-419,32110,82787,50000]
co_final = co_nov + [136001,8072,4258,17198,19732,3253,40485,762]
pay_first4 = [3500000,3500000,2500000,1884322]
pay_final = pay_first4 + [300000,340007,504232]
```

| Calculation group | Result |
|---|---|
| Own row114 + row115 | 1,221 +39,264 =40,485 |
| Root initial row114 diagnostic | 1,210 +39,264 =40,474;11 short of40,485 |
| Maximum City | 14,287,986 -1,668,858 =12,619,128 |
| July dated CO sum | 820,877 |
| July approved/proposed construction | base +additional +820,877 =13,803,180; replacing820,877 with864,577 gives13,846,880 |
| July approved/proposed City and balance | 12,134,322 /12,178,022 after landlord;484,806 /441,106 remaining |
| November dated CO sum/construction | 985,355 /13,967,658 |
| November City/budget balance | 12,298,800 /320,328 |
| November four reported payments/balance | 11,384,322 /914,478 |
| Final dated CO sum/construction | 1,215,116 /14,197,419 |
| Final City/budget balance | 12,528,561 /90,567 |
| Final seven reported payments/balance | 12,528,561 /0 |
| Revised-line approval minus prior credit | 130,000 -85,000 =45,000 |

TheJuly andNovember dated-list endpoints are selected from the respective frozen budget descriptions, with the common earlier history explicitly preserved; final totals use the2002 dated entries. No later approval date, status or missing July proposal amount was imputed. Matching arithmetic supports internal consistency and the1,221 transcription; it does not determine why figures were entered, whether payments cleared, whether work was adequate, or the correct handwritten date.

## Disposition

Shared substantive conclusions are usable with the qualifications above. Two numeric reading differences require an explicit correction/disposition in the synthesis, not silent editing of the frozen notes. Final report critique remains pending its supplied path/hash and the separately documented targeted-check outcome. The remaining three metadata candidates are still unread; this check neither retrieves them nor completes the wider investigation.

## Final synthesis critique

Complete text reads, with untruncated output:

- `report.md`, SHA256 `96562b6de07bd4ac40b00cb921f5e88e9c7aacacf26d6660157b48a22c0669e8`, `sed -n '1,320p'` (`746c19`, exit0).
- `CORRECTION-PROTOCOL.md`, SHA256 `53a0721647b6e915ec289ae21f11fc49615cd792d65a67db31eacbebe5935375`, `sed -n '1,240p'` (`49d884`, exit0).
- `correction-review.md`, SHA256 `08c615677e49516b2a91a1f79bdd57d6a29f477f500b1b506d692af09a785aa6`, `sed -n '1,260p'` (`cb3599`, exit0).
- `derivative-check.md`, SHA256 `9d18aa9ee2bc64776e23f4378fe6fbc7885b8ea179c4ced07348df5dcab9f2e6`, `sed -n '1,300p'` (`618818`, exit0).

Exact first-three pins were verified by `shasum -a 256` (`c12058`, exit0). Derivative pin and both unchanged initial-observation pins were verified (`e89a0c`, exit0). This was text-only: no new source/image views, retrievals, rendering, raw-copy comparisons or new arithmetic. The 24 earlier arithmetic checks remain the calculations actually run by this reader; root's separate16checks are attributed, not personally rerun here.

### Source and method assessment

The report properly resolves the two numeric differences as **root transcription/cross-version errors**, not source accounting anomalies. The separately declared corrective views agree with the own frozen values:1,221 in row114, and all July row87amount cells blank/notreceived. The report preserves both initial records and identifies the correction as targeted/unblinded rather than new initial agreement. This reader inspected the correction text, not its two source views anew. The amount correction does not eliminate the separate qualified handwriting-versus-printed-date issue.

All11page coverage, dated schedule distinctions and substantive route/protection/payment claims are consistent with the frozen readings. In particular, the report does not sum approved and credited routes as two installed lines, collapse all pending/voided states, import later dates into blank earlier payment fields, omit affirmative payment assertions, or equate two-hour-rated scope with verified field performance. The March-routing reference is no longer described as the last documented route; the later commercial revision is supported without claiming exactly how the field installation changed. Negative assertions are bounded to the admitted packets: absence of underlying drawings/inspection is not global absence or proven model omission.

The stated derivative scope agrees with the complete receipt:12rasters,4rendererprocesses and20preserved-copy pairs, not12differentphysicalpages. Original view counts and two later corrective views remain distinct. Same-renderer equality is not independent visual/historical validation. No blanket acceptance claim follows from reading that receipt.

### One requested next-test wording correction

The reviewed report says: **Only after actual location/configuration is established should an exact crosswalk test whether the relevant NIST or alternative model represents it.** This unnecessarily conditions even a **documented-design-to-model** comparison on verified installed state. It risks turning a legitimate limit on historical inference into a gate against useful conditional model-input review.

Recommended replacement distinction: **A conditional crosswalk can now test whether a model represents the documented design or revision, with missing inputs and scope explicitly identified. Claiming that an omission matters to the actual collapse requires establishing the relevant installed member/route/configuration and its physical consequence.** This does not authorize a solver, promote a design to as-built fact, or clear independent model-access/authority gates. It preserves a feasible investigative next step without pretending the installation is known. The remaining three exact metadata candidates and targeted order/detail leads are otherwise concrete and accurately bounded.

**Disposition:** no blocking source-content or correction-method defect found in this snapshot. One material next-test framing correction requested above; no change to the reported historical findings or cause ranking is warranted by this critique. Final status/navigation/source-log validation was not performed here. Full-goal, engineering, historical-authenticity and human acceptance remain outside this review. Any later report revision should retain a new hash and a separately recorded disposition rather than changing this reviewed snapshot retrospectively.

### Narrow correction follow-up

Read final report lines170-230 with `sed` (`71ba00`, exit0) and verified final report SHA256 **`2500a4d7710068654b287b08fb25a831a8cf4c16296d262ca538f2cf5412613d`** (`a8e321`, exit0). The next-test paragraph now expressly permits a source-pinned, conditional documented-design/model crosswalk in parallel, separates it from claims about an actual installed configuration, and requires the actual joint/revision before a historical member-capacity claim. The review-disposition paragraph accurately identifies the removed restriction. **The requested framing correction is addressed.**

The same hash command confirms both initial observation notes and the corrective declaration/finding retain every previously recorded pin. This follow-up does not replace or relabel the earlier96562b6d report snapshot. No full re-review, images, new source work, arithmetic, status/source-log validation or authority promotion occurred. No unresolved blocking issue remains from this bounded critical review; engineering, historical-authenticity, human and full-investigation acceptance are not conferred.
