<!-- Public derivative of the separately retained November 6, 2026 research record. Source provenance and reading scope appear in SOURCE-PINS.json. -->

# Pier 6 dredging contract candidate and transaction history

November 6, 2026 · Steel custody · B188 / H005 / STL01–03

The federal procurement export identifies **DACW3301C0026** as a strong candidate for the Pier 6 emergency dredging contract. The initial obligation, contractor, timing, New York performance location, dredging category and competition field match the reported award. The federal description is blank. The signed instrument or a contemporaneous record naming both the pier and contract number is still needed. [USAspending award record](https://api.usaspending.gov/api/v2/awards/CONT_AWD_DACW3301C0026_9700_-NONE-_-NONE-/) · [Army Corps district reprint, printed p. 10](https://www.nan.usace.army.mil/Portals/37/docs/history/NAN_9-11_tribute_web_smaller.pdf)

## Match test and counterchecks

The USAspending bulk export covered contracts and indefinite-delivery vehicles awarded by the Department of the Army, with New York as the reported place of performance and action dates **September 20–27, 2001**. The archive contains one CSV with **255 transaction records**. Two base rows report the recipient **GREAT LAKES DREDGE & DOCK CO, LLC** and a dredging product or service code. Only one has the exact initial amount reported for Pier 6. Record ordinals below include the CSV header and count parsed records, so they remain meaningful if a quoted field spans multiple lines. [Export definition](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/bulk_download/awards.md) · [Request filters and source hashes](SOURCE-PINS.json)

| CSV ordinal | Contract | Action date | Initial obligation | Dredging code | Competition | Awarding office code |
| --- | --- | --- | ---: | --- | --- | --- |
| 76 | DACW3301C0026 | 2001-09-23 | $790,500.00 | Z216 | NOT COMPETED | CW33 |
| 53 | DACW5101C0031 | 2001-09-21 | $76,667.00 | Y216 | FULL AND OPEN COMPETITION | CW51 |

The second row illustrates why contractor name and work category alone are insufficient. Both rows leave the transaction description blank. The matched row leaves the awarding office name blank and shows Department of the Army as the awarding subagency. The Corps district publication discusses Pier 6 in its New York response narrative without supplying a contract identifier. A separate period project filed by the **New England District** uses a **DACW33** prefix. That is a lead to check the contracting office separately from the work location. It supplies no office name for this specific transaction. [Army Corps district reprint](https://www.nan.usace.army.mil/Portals/37/docs/history/NAN_9-11_tribute_web_smaller.pdf) · [New England District comparison, cover](https://www.nae.usace.army.mil/Portals/74/docs/Topics/FTDevens/AR/Site%20Management%20Records/7.0%20Remedial%20Removal%20Action_Long%20Term%20Management%202024/7.08-RA-Documents/OTH-2001-01-16-Final-Closure-Rpt-SA-71.pdf#page=1)

## Keep award, change order and completion dates separate

| Source | Observation |
| --- | --- |
| USAspending transaction history, complete first page | September 23 base action **0**, **+$790,500.00**. November 15 action **P00001**, labeled **CHANGE ORDER**, **−$79,512.00**. Both descriptions are null. |
| USAspending award detail | **$710,988.00** total obligation. Signed date **September 23**, reported performance dates **September 23–October 2, 2001**. |
| Corps New York District fall 2001 text, printed p. 10 | A permit was issued to the City on **September 20**. Dredging started **September 24** under a **$790,500** emergency contract with Great Lakes. The publication reports **more than 55,000 cubic yards** moved. |
| Corps operational update, October 9 at 0900 | Reports Pier 6 dredging concluded **October 4**. It places the dredged material at the **Newark Bay Confined Disposal Facility** and separately describes the improved route for WTC debris barges to the **Staten Island Landfill**. |

The two returned action amounts sum to **$710,988.00**, the award-detail total. This check concerns reported obligations. The scope, reason and payment effect of the change order remain unknown. The October 2 performance-end field and October 4 mission-end account are preserved under their own labels. A completion or acceptance record could test the relationship. [Award detail](https://api.usaspending.gov/api/v2/awards/CONT_AWD_DACW3301C0026_9700_-NONE-_-NONE-/) · [Transaction history API](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/transactions.md) · [Corps district reprint](https://www.nan.usace.army.mil/Portals/37/docs/history/NAN_9-11_tribute_web_smaller.pdf) · [October 9 update, Yale reproduction](https://avalon.law.yale.edu/sept11/eng_003.asp)

A September 25 industry archive item gives a prospective volume of **up to 75,000 cubic yards**, separately from the Corps’ later **more than 55,000** outcome. The November *Engineer Update* and the district reprint also preserve different versions of the barging status. The former says **“will be implemented shortly”** and the latter says **“have already been implemented.”** Their underlying interview or copy dates remain unverified. The first documented loaded barge and receiving receipt would provide a better date anchor. [September 25 item](https://www.fireengineering.com/firefighting/archive-of-week-3-events-at-wtc-pentagon/) · [November issue, reader excerpt](https://upload.wikimedia.org/wikipedia/commons/9/92/Engineer_update_-_USACE-p16021coll8-2157.pdf) · [District reprint](https://www.nan.usace.army.mil/Portals/37/docs/history/NAN_9-11_tribute_web_smaller.pdf)

## Remaining record targets

- [ ] Locate the signed base contract **DACW3301C0026**, the **P00001** change order, award justification and completion or acceptance records. Check for an explicit Pier 6 identifier, scope, awarding office and disposition terms.
- [ ] Locate the **September 20** City permit and related FEMA mission assignment. Keep this Pier 6 file distinct from the earlier **September 13 Pier 25** application. Dated work maps and disposal reports would clarify what was dredged and where it was placed. [Earlier pier routing study and preserved 6/25/26 accounts](https://github.com/AveLyra/911-conspiracy-investigation/blob/a3e6f2e19d79f523840d84bcc4a9688ee155a43f/investigation/broader-evidence/steel-pier-routing-and-dredge-permit-2026-11-06/README.md)
- [ ] For WTC steel custody, locate a matched barge dispatch and receiver record with a specific load identifier and contents. Keep the reported steel shipment permission, individual steel transfer records and W14A/B attribution separate from harbor sediment disposal. [Prior load-ticket and manifest study](https://github.com/AveLyra/911-conspiracy-investigation/blob/dca6f3cf5f0eed427f1cade3f9f0133d3abbee08/investigation/broader-evidence/steel-load-tickets-joint-appendix-2026-11-06/README.md)

The scoped export, award JSON, transaction history and two HTML captures are retained locally. The Corps district and November period publications were read in indexed PDF text. Direct retrieval yielded an access error or incomplete body, and the larger mirror exceeded the size limit. The preceding broad export was 18,562,400 bytes and was left outside the local study. The smaller export is the tested dataset. [Acquisition scope and hashes](SOURCE-PINS.json)
