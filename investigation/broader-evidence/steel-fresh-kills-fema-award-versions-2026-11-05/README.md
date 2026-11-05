# FEMA award versions for debris transport and landfill worksheets
# FEMA award versions for debris transport and landfill worksheets


November 5, 2026. This STL01 follow-up queries FEMA's **v2 award-activity** endpoint for nine DR-1391-NY worksheets identified in the project-index review. The earlier v1 access failure and prior project snapshot are separately preserved. These entries supply dates and version numbers for retrieving the approved worksheets and financial amendments. Each row describes a funding record. Facility, contractor, cargo and service dates still require underlying documents. [Prior project-index report](https://github.com/AveLyra/911-conspiracy-investigation/blob/3be431db4686a561ac0a8dcfe179b0ac09e07b3c/investigation/broader-evidence/steel-fresh-kills-fema-project-index-2026-11-05/README.md) · [FEMA award-activity dataset description](https://catalog.data.gov/dataset/public-assistance-grant-award-activities-emmie)

## What the entries show

| Applicant and PW | Version entries with FEMA obligation date and federal-share amount | Federal-share sum |
| --- | --- | ---: |
| City 1 | v0 2001-09-14 +$25,000,000; v1 2001-09-17 +$100,000,000; v2 2001-10-22 +$145,532,687; v3 2001-11-08 +$57,558,412; v4 2001-12-18 +$44,596,009 | +$372,687,108.00 |
| City 2 | v0 2002-02-16 −$372,687,108 | −$372,687,108.00 |
| DDC 952 | v0 2002-10-03 +$4,894,954.05; v1 2003-03-27 +$2,500,000; v2 2003-06-30 −$3,025,173.05 | +$4,369,781.00 |
| DSNY 928 | v0 2002-08-29 +$193,680.26 | +$193,680.26 |
| DSNY 1004 | v0 2002-07-30 +$245,775.00; v1 2003-06-12 +$5,328.82 | +$251,103.82 |
| DSNY 1010 | v0 2002-08-23 +$2,458,800.00 | +$2,458,800.00 |
| DSNY 1093 | v0 2002-07-30 +$62,517.70 | +$62,517.70 |
| DSNY 1318 | v0 2002-09-27 +$95,314.47; v1 2003-07-10 −$34,785.00 | +$60,529.47 |
| DSNY 1349 | v0 2002-11-27 +$1,035,372.22; v1 2003-06-30 −$1,035,372.22 | $0.00 |

The transaction sums equal the project-details `federalShareObligated` field for **all nine** disaster/applicant/PW keys. The endpoints come from the same agency. The check establishes cross-endpoint agreement for that field and cannot independently validate the underlying transactions. Row IDs, native field labels, exact timestamps, JSON pointers, access date, SHA-256 values and the full query are in [Source pins](SOURCE-PINS.json). [FEMA scoped award response](https://www.fema.gov/api/open/v2/PublicAssistanceGrantAwardActivities?%24filter=disasterNumber+eq+1391+and+%28%28applicantId+eq+%27061-51000-00%27+and+%28pwNumber+eq+1+or+pwNumber+eq+2%29%29+or+%28applicantId+eq+%27061-51000-19%27+and+pwNumber+eq+952%29+or+%28applicantId+eq+%27061-51000-49%27+and+%28pwNumber+eq+928+or+pwNumber+eq+1004+or+pwNumber+eq+1010+or+pwNumber+eq+1093+or+pwNumber+eq+1318+or+pwNumber+eq+1349%29%29%29&%24top=1000)

## Unresolved relationships

- **City PW 1 and 2.** The five positive entries for PW 1, `(PW# 1) DEBRIS REMOVAL`, sum to the exact opposite of the single later negative entry for PW 2, `(PW# 2) Not Provided`. The transaction titles and amounts supply no explicit linkage. The separate project-details `totalObligated` fields remain **+$376,495,476.25** and **−$376,423,296.25**, a **+$72,180.00** sum. The source also gives different `paCloseoutStatus` values, `C` on the PW 1 rows and `O` on PW 2. Preserve the literal codes pending the codebook and signed dispositions. A cross-worksheet transfer or adjustment is an untested hypothesis. A linked funding action or ledger journal is needed to establish it.
- **DSNY PW 1349.** Both rows retain `(PW# 1349) REPAIR / CLEANING MARINE TRANSFER STATION` and `paCloseoutStatus: C`. The federal-share entries cancel at the worksheet key. The project snapshot separately reports **$1,035,372.22** as `projectAmount`, **$0.01** as `totalObligated` and **$0** as `federalShareObligated`. The fields and source labels are preserved. The reason for the offset, meaning of the one-cent entry and station identity require the underlying records.
- **DDC PW 952.** Both endpoints report **Queens County**. The negative v2 entry changes the financial total. Its connection to a specific Ground Zero monitoring contract remains unverified.
- **API scope.** The scoped response has `metadata.count: 0` and an array of **18 records with unique IDs**, below the requested cap of 1,000. The count and the array are preserved side by side. The query covers the nine listed worksheet keys and leaves completeness outside the returned payload unverified.

[Project-details source pins and snapshot field values](https://github.com/AveLyra/911-conspiracy-investigation/blob/3be431db4686a561ac0a8dcfe179b0ac09e07b3c/investigation/broader-evidence/steel-fresh-kills-fema-project-index-2026-11-05/SOURCE-PINS.json)

## Deferred originals

- [ ] **City PWs 1 v0–v4 and 2 v0.** Obtain approved worksheets, the February 16, 2002 funding action and any linked journal, authorization or worksheet cross-reference. Check the two federal-share amounts and the separately reported total fields against the underlying ledger.
- [ ] **DSNY PW 1349 v0–v1.** Obtain signed scope, station address, the November 27, 2002 and June 30, 2003 financial backup, and closeout records. Check the reason for the offset and any accounting entry behind the reported cent.
- [ ] **DSNY transport and landfill PWs 928, 1004, 1010, 1093 and 1318, and DDC 952.** Obtain worksheet versions and supporting invoices. Join contract, facility and service period before connecting any costs to a Fresh Kills route or Ground Zero contract.
- [ ] **Separate custody records.** Obtain barge dispatch logs, weigh tickets, manifests, screening records and specimen identifiers. Financial records alone leave shipment and specimen attribution open. Carry forward the prior inbound/landfill/recycling weight discrepancy and competing screening accounts as recorded.
- [ ] **Codebook and distributions.** Locate FEMA's source definitions and disposition records for the literal status codes. The [February 2025 DataLumos release](https://doi.org/10.3886/E218481V1) lists an archived award-activity ZIP. A vintage comparison remains deferred until the archive can be handled through the approved storage route.

The source acquisition and reconciliation checks concern database entries. They leave physical work, cash disbursement, steel disposition and any historical intent untested.
Public derivative of the November 5, 2026 OpenFEMA award-activity source review. The native response is preserved separately and identified by SHA-256 in the source pins.

November 5, 2026. This STL01 follow-up queries FEMA's **v2 award-activity** endpoint for nine DR-1391-NY worksheets identified in the project-index review. The earlier v1 access failure and prior project snapshot are separately preserved. These entries supply dates and version numbers for retrieving the approved worksheets and financial amendments. Each row describes a funding record. Facility, contractor, cargo and service dates still require underlying documents. [Prior project-index report](https://github.com/AveLyra/911-conspiracy-investigation/blob/3be431db4686a561ac0a8dcfe179b0ac09e07b3c/investigation/broader-evidence/steel-fresh-kills-fema-project-index-2026-11-05/README.md) · [FEMA award-activity dataset description](https://catalog.data.gov/dataset/public-assistance-grant-award-activities-emmie)

## What the entries show

| Applicant and PW | Version entries with FEMA obligation date and federal-share amount | Federal-share sum |
| --- | --- | ---: |
| City 1 | v0 2001-09-14 +$25,000,000; v1 2001-09-17 +$100,000,000; v2 2001-10-22 +$145,532,687; v3 2001-11-08 +$57,558,412; v4 2001-12-18 +$44,596,009 | +$372,687,108.00 |
| City 2 | v0 2002-02-16 −$372,687,108 | −$372,687,108.00 |
| DDC 952 | v0 2002-10-03 +$4,894,954.05; v1 2003-03-27 +$2,500,000; v2 2003-06-30 −$3,025,173.05 | +$4,369,781.00 |
| DSNY 928 | v0 2002-08-29 +$193,680.26 | +$193,680.26 |
| DSNY 1004 | v0 2002-07-30 +$245,775.00; v1 2003-06-12 +$5,328.82 | +$251,103.82 |
| DSNY 1010 | v0 2002-08-23 +$2,458,800.00 | +$2,458,800.00 |
| DSNY 1093 | v0 2002-07-30 +$62,517.70 | +$62,517.70 |
| DSNY 1318 | v0 2002-09-27 +$95,314.47; v1 2003-07-10 −$34,785.00 | +$60,529.47 |
| DSNY 1349 | v0 2002-11-27 +$1,035,372.22; v1 2003-06-30 −$1,035,372.22 | $0.00 |

The transaction sums equal the project-details `federalShareObligated` field for **all nine** disaster/applicant/PW keys. The endpoints come from the same agency. The check establishes cross-endpoint agreement for that field and cannot independently validate the underlying transactions. Row IDs, native field labels, exact timestamps, JSON pointers, access date, SHA-256 values and the full query are in [Source pins](SOURCE-PINS.json). [FEMA scoped award response](https://www.fema.gov/api/open/v2/PublicAssistanceGrantAwardActivities?%24filter=disasterNumber+eq+1391+and+%28%28applicantId+eq+%27061-51000-00%27+and+%28pwNumber+eq+1+or+pwNumber+eq+2%29%29+or+%28applicantId+eq+%27061-51000-19%27+and+pwNumber+eq+952%29+or+%28applicantId+eq+%27061-51000-49%27+and+%28pwNumber+eq+928+or+pwNumber+eq+1004+or+pwNumber+eq+1010+or+pwNumber+eq+1093+or+pwNumber+eq+1318+or+pwNumber+eq+1349%29%29%29&%24top=1000)

## Unresolved relationships

- **City PW 1 and 2.** The five positive entries for PW 1, `(PW# 1) DEBRIS REMOVAL`, sum to the exact opposite of the single later negative entry for PW 2, `(PW# 2) Not Provided`. The transaction titles and amounts supply no explicit linkage. The separate project-details `totalObligated` fields remain **+$376,495,476.25** and **−$376,423,296.25**, a **+$72,180.00** sum. The source also gives different `paCloseoutStatus` values, `C` on the PW 1 rows and `O` on PW 2. Preserve the literal codes pending the codebook and signed dispositions. A cross-worksheet transfer or adjustment is an untested hypothesis. A linked funding action or ledger journal is needed to establish it.
- **DSNY PW 1349.** Both rows retain `(PW# 1349) REPAIR / CLEANING MARINE TRANSFER STATION` and `paCloseoutStatus: C`. The federal-share entries cancel at the worksheet key. The project snapshot separately reports **$1,035,372.22** as `projectAmount`, **$0.01** as `totalObligated` and **$0** as `federalShareObligated`. The fields and source labels are preserved. The reason for the offset, meaning of the one-cent entry and station identity require the underlying records.
- **DDC PW 952.** Both endpoints report **Queens County**. The negative v2 entry changes the financial total. Its connection to a specific Ground Zero monitoring contract remains unverified.
- **API scope.** The scoped response has `metadata.count: 0` and an array of **18 records with unique IDs**, below the requested cap of 1,000. The count and the array are preserved side by side. The query covers the nine listed worksheet keys and leaves completeness outside the returned payload unverified.

[Project-details source pins and snapshot field values](https://github.com/AveLyra/911-conspiracy-investigation/blob/3be431db4686a561ac0a8dcfe179b0ac09e07b3c/investigation/broader-evidence/steel-fresh-kills-fema-project-index-2026-11-05/SOURCE-PINS.json)

## Deferred originals

- [ ] **City PWs 1 v0–v4 and 2 v0.** Obtain approved worksheets, the February 16, 2002 funding action and any linked journal, authorization or worksheet cross-reference. Check the two federal-share amounts and the separately reported total fields against the underlying ledger.
- [ ] **DSNY PW 1349 v0–v1.** Obtain signed scope, station address, the November 27, 2002 and June 30, 2003 financial backup, and closeout records. Check the reason for the offset and any accounting entry behind the reported cent.
- [ ] **DSNY transport and landfill PWs 928, 1004, 1010, 1093 and 1318, and DDC 952.** Obtain worksheet versions and supporting invoices. Join contract, facility and service period before connecting any costs to a Fresh Kills route or Ground Zero contract.
- [ ] **Separate custody records.** Obtain barge dispatch logs, weigh tickets, manifests, screening records and specimen identifiers. Financial records alone leave shipment and specimen attribution open. Carry forward the prior inbound/landfill/recycling weight discrepancy and competing screening accounts as recorded.
- [ ] **Codebook and distributions.** Locate FEMA's source definitions and disposition records for the literal status codes. The [February 2025 DataLumos release](https://doi.org/10.3886/E218481V1) lists an archived award-activity ZIP. A vintage comparison remains deferred until the archive can be handled through the approved storage route.

The source acquisition and reconciliation checks concern database entries. They leave physical work, cash disbursement, steel disposition and any historical intent untested.
