# SkyWay temporary authorization and FCC location records
# SkyWay temporary authorization and FCC location records


November 5, 2026. This **TEL03/TEL04** follow-up tests two FCC data snapshots against the order and company descriptions already preserved for the Claircom asset-custody trail. The snapshots contain native licensing database records. They do not supply the signed sale agreement, station installation histories or legacy call records. [Prior acquisition review](https://github.com/AveLyra/911-conspiracy-investigation/blob/cb41b35033b5a40182f4b51cac98fea4c3487db1/investigation/broader-evidence/telephone-claircom-transfer-filings-2026-11-05/README.md)

## Renewal identifier and reported outcome

FCC 04-287, footnote 32, refers to a then-pending WPYZ281 extension as **`00019331747`**, filed **November 11, 2004**. The application snapshot returns six header rows for **WPYZ281**. One has file number **`0001931747`**, system ID **`2665105`**, purpose **`RM`**, and receipt and entry dates **November 10, 2004**. The differences in file number and date remain attributed to their sources. A shared call sign, nearby date and renewal context make this a candidate counterpart. The signed filing and correspondence are needed to confirm the relationship. [FCC order, n. 32](https://docs.fcc.gov/public/attachments/FCC-04-287A1.pdf#page=9) · [Exact application rows](SOURCE-PINS.json)

The later ULS snapshot records `APDIS` on **March 3, 2006** and `LETDIS` on **March 4, 2006** for `0001931747`. The FCC's code definitions identify those as application dismissed and dismissal letter sent. The same application's attachment table indexes a March 3 entry titled **Special Temporary Authority (STA)**, with a blank filename. The title and dismissal history are preserved separately. The underlying letter and attachment content remain unverified. The license table gives **November 30, 2004** as WPYZ281's expiration date, matching the date the earlier order describes. [FCC history code definitions](https://wireless.fcc.gov/uls/releases/d992205c.pdf) · [Source pins](SOURCE-PINS.json)

## Location records differ by source

| Record or test | Result |
| --- | --- |
| SkyWay 10-KSB | **136 sites** described as covered by temporary authorization. The 166-tower purchase claim from earlier publicity remains a separately attributed claim. |
| FCC application snapshot, all WPYZ281 file keys | **137 location rows**, **135 distinct location numbers**, **136 distinct coordinate tuples**. Location numbers 5 and 20 each appear twice across files. |
| FCC license snapshot, WPYZ281 | **135 location rows**, **135 distinct numbers** and **135 distinct coordinate tuples**. |
| Exact coordinate-field comparison | All **135** license tuples occur in the applications. One application tuple appears only in the application snapshot, at `LO.dat` line **8254**, application **0001604737**, location number **20**, action field **A**. **Eight** exact coordinate matches have different location numbers across the two datasets. |

The application-only location number **136** and license-only number **128** do not uniquely identify unmatched physical sites. The exact coordinates of application location numbers **129–136** appear under license location numbers **128–135** respectively. This is a reproducible comparison of stored coordinate fields. It leaves the reason for differing numbers, actual station operation, and why the other coordinate tuple is absent from the license snapshot unresolved. The February 4, 2004 application indexes an **Additional 21 site amendment**, an exact attachment target. [Company 10-KSB, printed pp. 3–4](https://www.sec.gov/Archives/edgar/data/1128723/000107087604000086/skyway10ksb2004.htm) · [FCC application snapshot](https://data.fcc.gov/download/pub/uls/complete/a_paging.zip) · [FCC license snapshot](https://data.fcc.gov/download/pub/uls/complete/l_paging.zip)

## Deferred originals

- [ ] Locate WPYZ281's signed authorization, site schedules, amendments, **0001604737** attachment, **0001931747** application and March 2006 letter. Compare original schedule versions against both FCC data snapshots.
- [ ] Locate the Claircom sale agreement and inventory of conveyed assets and records. FCC location data alone leaves equipment ownership and historical call-data custody open.
- [ ] Retain the independent September 11 call-event, clock and operator record requirements. Neither snapshot contains the carrier call data needed for those tests.

The [source pins](SOURCE-PINS.json) give ZIP hashes and exact physical record locators. The [verification script](verify_locations.py) regenerates the comparison from the two preserved exports. Only counts, identifiers and comparison results are published. The native archives remain separate.
Public derivative of the November 5, 2026 FCC snapshot comparison. The native sources are separately preserved.

November 5, 2026. This **TEL03/TEL04** follow-up tests two FCC data snapshots against the order and company descriptions already preserved for the Claircom asset-custody trail. The snapshots contain native licensing database records. They do not supply the signed sale agreement, station installation histories or legacy call records. [Prior acquisition review](https://github.com/AveLyra/911-conspiracy-investigation/blob/cb41b35033b5a40182f4b51cac98fea4c3487db1/investigation/broader-evidence/telephone-claircom-transfer-filings-2026-11-05/README.md)

## Renewal identifier and reported outcome

FCC 04-287, footnote 32, refers to a then-pending WPYZ281 extension as **`00019331747`**, filed **November 11, 2004**. The application snapshot returns six header rows for **WPYZ281**. One has file number **`0001931747`**, system ID **`2665105`**, purpose **`RM`**, and receipt and entry dates **November 10, 2004**. The differences in file number and date remain attributed to their sources. A shared call sign, nearby date and renewal context make this a candidate counterpart. The signed filing and correspondence are needed to confirm the relationship. [FCC order, n. 32](https://docs.fcc.gov/public/attachments/FCC-04-287A1.pdf#page=9) · [Exact application rows](SOURCE-PINS.json)

The later ULS snapshot records `APDIS` on **March 3, 2006** and `LETDIS` on **March 4, 2006** for `0001931747`. The FCC's code definitions identify those as application dismissed and dismissal letter sent. The same application's attachment table indexes a March 3 entry titled **Special Temporary Authority (STA)**, with a blank filename. The title and dismissal history are preserved separately. The underlying letter and attachment content remain unverified. The license table gives **November 30, 2004** as WPYZ281's expiration date, matching the date the earlier order describes. [FCC history code definitions](https://wireless.fcc.gov/uls/releases/d992205c.pdf) · [Source pins](SOURCE-PINS.json)

## Location records differ by source

| Record or test | Result |
| --- | --- |
| SkyWay 10-KSB | **136 sites** described as covered by temporary authorization. The 166-tower purchase claim from earlier publicity remains a separately attributed claim. |
| FCC application snapshot, all WPYZ281 file keys | **137 location rows**, **135 distinct location numbers**, **136 distinct coordinate tuples**. Location numbers 5 and 20 each appear twice across files. |
| FCC license snapshot, WPYZ281 | **135 location rows**, **135 distinct numbers** and **135 distinct coordinate tuples**. |
| Exact coordinate-field comparison | All **135** license tuples occur in the applications. One application tuple appears only in the application snapshot, at `LO.dat` line **8254**, application **0001604737**, location number **20**, action field **A**. **Eight** exact coordinate matches have different location numbers across the two datasets. |

The application-only location number **136** and license-only number **128** do not uniquely identify unmatched physical sites. The exact coordinates of application location numbers **129–136** appear under license location numbers **128–135** respectively. This is a reproducible comparison of stored coordinate fields. It leaves the reason for differing numbers, actual station operation, and why the other coordinate tuple is absent from the license snapshot unresolved. The February 4, 2004 application indexes an **Additional 21 site amendment**, an exact attachment target. [Company 10-KSB, printed pp. 3–4](https://www.sec.gov/Archives/edgar/data/1128723/000107087604000086/skyway10ksb2004.htm) · [FCC application snapshot](https://data.fcc.gov/download/pub/uls/complete/a_paging.zip) · [FCC license snapshot](https://data.fcc.gov/download/pub/uls/complete/l_paging.zip)

## Deferred originals

- [ ] Locate WPYZ281's signed authorization, site schedules, amendments, **0001604737** attachment, **0001931747** application and March 2006 letter. Compare original schedule versions against both FCC data snapshots.
- [ ] Locate the Claircom sale agreement and inventory of conveyed assets and records. FCC location data alone leaves equipment ownership and historical call-data custody open.
- [ ] Retain the independent September 11 call-event, clock and operator record requirements. Neither snapshot contains the carrier call data needed for those tests.

The [source pins](SOURCE-PINS.json) give ZIP hashes and exact physical record locators. The [verification script](verify_locations.py) regenerates the comparison from the two preserved exports. Only counts, identifiers and comparison results are published. The native archives remain separate.
