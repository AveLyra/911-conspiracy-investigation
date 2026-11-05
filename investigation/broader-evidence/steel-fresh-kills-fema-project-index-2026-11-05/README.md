# FEMA worksheet identifiers for debris transport and landfill operations

November 5, 2026. This study follows STL01 from the [Fresh Kills screening and load-record review](https://github.com/AveLyra/911-conspiracy-investigation/blob/699ac9c0a038b6bd4ed0515ac2898f2676af8712/investigation/broader-evidence/steel-fresh-kills-screening-and-load-records-2026-11-05/README.md) into FEMA's public grant index for **DR-1391-NY**. The House staff report names debris-removal obligations to both city agencies and separately describes a federally funded Army Corps sifting effort. Those administrative routes are distinct. [House staff report, Stafford Act obligations and debris-removal sections](https://www.govinfo.gov/content/pkg/CPRT-109HPRT20452/html/CPRT-109HPRT20452.htm)

## Verified worksheet locators

FEMA's applicant table identifies **061-51000-49** as the New York City Department of Sanitation (DSNY), **061-51000-19** as the Department of Design and Construction (DDC), and **061-51000-00** as the City of New York. The disaster number, applicant ID and worksheet number form the join key used here. The grant index separately supplies a Grants Manager project ID. It contains financial records and short titles. The original worksheet, work location, contractor, service period, signed determination and backup attachments remain separate retrieval targets. [OpenFEMA project response](https://www.fema.gov/api/open/v2/PublicAssistanceFundedProjectsDetails?%24filter=disasterNumber%20eq%201391%20and%20%28damageCategoryCode%20eq%20%27A%27%20or%20applicantId%20eq%20%27061-51000-49%27%20or%20applicantId%20eq%20%27061-51000-19%27%29&%24top=1000) · [OpenFEMA applicant response](https://www.fema.gov/api/open/v1/PublicAssistanceApplicants?%24filter=disasterNumber%20eq%201391&%24top=1000)

| Agency | PW | Grants Manager ID | FEMA application title, excluding PW prefix | Federal share obligated |
| --- | ---: | ---: | --- | ---: |
| DSNY | **1004** | **451377** | CONTRACT COSTS - ENG SERVICES -LANDFILL OPERATIONS | $251,103.82 |
| DSNY | **1010** | **451380** | BARGE USAGE | $2,458,800.00 |
| DSNY | **928** | **451373** | CONTRACT - BARGE TOWING | $193,680.26 |
| DSNY | **1093** | **451383** | CONTRACT COSTS - BARGE TOWING | $62,517.70 |
| DSNY | **1318** | **451395** | EMERGENCY BARGE WORK | $60,529.47 |
| DSNY | **1349** | **451399** | REPAIR / CLEANING MARINE TRANSFER STATION | $0.00 |
| DDC | **952** | **450988** | COST ESTIMATE -  CONTRACT MONITORING / MGMT | $4,369,781.00 |

The titles make these candidates for landfill service, transport or oversight backup. The DSNY annual report names temporary and permanent transfer points used for Fresh Kills barges, but the cited FEMA entries omit a route and the worksheet contents are still needed to join any specific site or movement. DDC PW 952 also lists **Queens County** in the index. Its link to the Ground Zero audit records therefore remains unverified. The reported obligation dates are financial events. Barge logs and manifests are needed for service dates, routes and tonnage. [DSNY 2002–2003 annual report, printed p. 15](https://www.nyc.gov/assets/dsny/downloads/pdf/studies-and-reports/2002-2003_Annual_Report.pdf)

## Reproducible checks and unresolved fields

The scoped project response returned **120 rows**, including **107 Category A** entries, and no repeated disaster/applicant/PW keys. Of these, **58** rows belong to DSNY and **32** to DDC across the queried categories. The DR-1391 applicant response returned **195 rows** and a unique row for each of the three applicant IDs above. The API envelope says `metadata.count: 0` even though the scoped project response contains 120 records. These counts come from the returned arrays. The filter and selected rows are preserved in [the source pins](SOURCE-PINS.json). A broader 1,000-row probe hit its requested cap and was kept separate from the scoped results.

The snapshot lists **City PW 1** and **City PW 2** with federal-share fields of **+$372,687,108** and **−$372,687,108**. Those fields sum to zero. The separate `totalObligated` fields are **+$376,495,476.25** and **−$376,423,296.25**, which sum to **+$72,180.00**. The dataset's title for PW 2 is `(PW# 2) Not Provided`. The equal and opposite federal-share amounts are an arithmetic observation. A paired adjustment, cause and accounting treatment would require the transaction history and worksheet versions. PW 1349 likewise has different values across the index fields, including a zero federal share, $0.01 total obligated and a $1,035,372.22 project amount. Preserve each field under its original label. The catalog describes limitations of the project data relative to official federal financial systems. [FEMA project dataset description](https://catalog.data.gov/dataset/public-assistance-funded-projects-details) · [FEMA award-version dataset description](https://catalog.data.gov/dataset/public-assistance-grant-award-activities-emmie)

## Remaining originals

- [ ] **STL01 / Worksheet scope.** Obtain the approved scopes, original and revised worksheets, obligations and supporting invoices for PW **1004, 1010, 928, 1093, 1318, 1349 and 952**. Check facility, route, service period and contract references against DSNY and DDC records.
- [ ] **STL01 / Load joins.** Obtain barge dispatch and receiving records, weigh tickets and outbound steel manifests. Keep WTC inbound weight, recycled steel and landfill placement separately labeled. The prior 10-ton discrepancy and screening dispute remain unresolved.
- [ ] **STL01 / Financial versions.** Obtain the award versions, accounting classification and closeout backup for City PW **1 and 2** and DSNY PW **1349**. An unverified v1 award-activity URL returned 404. The award-version dataset's documented coverage and current distribution remain to be checked.
- [ ] **STL02–03 / Item provenance.** A financial project identifier still needs a separate join through item markings and custody records before it can support a specimen claim.

The native public responses remain in the research checkout. Only selected public fields, source hashes and the analysis are included in this report bundle. The 18 original-input criteria retain their prior statuses.
