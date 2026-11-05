# Claircom and GTE Airfone application and attachment index records
# Claircom and GTE Airfone application and attachment index records


November 5, 2026. This **TEL03/TEL04** follow-up recovered the actual database rows for two 2001 carrier engineering applications. FCC's public archive guide classifies Commercial Air-ground Radiotelephone service, `CA`, under Paging. I used the FCC's October 31 snapshot of `a_paging.zip` and joined the header, detail and attachment tables on both application file number and system identifier. [FCC archive guide, p. 11](https://wireless.fcc.gov/uls/documentation/pa_intro24.pdf#page=11) · [Public FCC snapshot](https://data.fcc.gov/download/pub/uls/complete/a_paging.zip)

| Carrier and application | FCC system ID and call sign | Detail fields | Attachment index |
| --- | --- | --- | --- |
| Claircom **0000421562** | **741133**, **KNKG801** | Receipt Date **04/09/2001**, Date Entered **04/09/2001**, How Many Waivers Requested **4** | **7** rows. Three named waiver requests, an overview, Public Notice, Comments dated **06/14/2001**, and Order dated **10/05/2001**. |
| GTE Airfone **0000420815** | **740283**, **KNKG804** | Receipt Date **04/09/2001**, Date Entered **04/08/2001**, How Many Waivers Requested **1** | **6** rows. Four code `W` entries dated **04/08/2001** with blank descriptions, a Public Notice and Comments dated **06/14/2001**. |

The three Claircom request descriptions identify **§22.857**, **§§22.857 and 22.869**, and **§22.381**. The FCC notice and order describe three categories of joint requests. Preserve that description alongside the application-detail fields **4** and **1** and the attachment index counts. They use different labels and scopes. Neither the 4/1 fields nor the number of attachment rows is a verified count of distinct requests across both applications. Both files index a June 14 Comments row. The order reports one supporting comment, from Claircom. Whether the two rows refer to the same file remains untested. [FCC notice](https://docs.fcc.gov/public/attachments/DA-01-1216A1.pdf) · [FCC order, ¶¶1–2](https://docs.fcc.gov/public/attachments/DA-01-2336A1.pdf#page=1) · [Earlier comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/074c917cf37ad6b90751c6d9375a3d215362cc47/investigation/broader-evidence/telephone-claircom-2001-engineering-waivers-2026-11-05/README.md)

All **13** matching attachment filename fields are blank in the bulk export. The public ULS search form and both exact application pages returned HTTP **403** on this route. The ZIP and its selected rows are preserved. The export's metadata and these access outcomes leave the attachment bodies, their identifiers in other systems, and their availability elsewhere open. [Claircom application page](https://wireless2.fcc.gov/UlsApp/ApplicationSearch/applMain.jsp?applID=741133) · [GTE Airfone application page](https://wireless2.fcc.gov/UlsApp/ApplicationSearch/applMain.jsp?applID=740283)

## Reproduction and deferred originals

The source pins retain the verified ZIP hash, member and physical row locators, and only the fields needed for the comparison. The script verifies the snapshot hash and regenerates the two header rows, two detail rows and thirteen attachment rows. The current archive URL can serve a newer snapshot. This test is keyed to the preserved bytes. [Source pins](SOURCE-PINS.json) · [Verification script](verify_index.py) · [FCC record format](https://wireless.fcc.gov/wtbfiles/pa_ddef51.pdf)

- [ ] Locate original application bodies, the three titled Claircom requests and overview, GTE's four undifferentiated waiver entries, and the June 14 comments. Compare native files and version identifiers across the two applications before classifying duplicate records.
- [ ] Locate the actual exchanged test schedules and matched equipment installation or maintenance records. The attachment index and FCC order leave actual implementation and date of use open.
- [ ] Retain the independent call-specific switch, operator and event-dictionary dependencies and the carrier-custody TODOs. No September 11 call or technical configuration was identified by this index join.
Public derivative of the November 5, 2026 FCC archive study. The native FCC ZIP remains separately preserved.

November 5, 2026. This **TEL03/TEL04** follow-up recovered the actual database rows for two 2001 carrier engineering applications. FCC's public archive guide classifies Commercial Air-ground Radiotelephone service, `CA`, under Paging. I used the FCC's October 31 snapshot of `a_paging.zip` and joined the header, detail and attachment tables on both application file number and system identifier. [FCC archive guide, p. 11](https://wireless.fcc.gov/uls/documentation/pa_intro24.pdf#page=11) · [Public FCC snapshot](https://data.fcc.gov/download/pub/uls/complete/a_paging.zip)

| Carrier and application | FCC system ID and call sign | Detail fields | Attachment index |
| --- | --- | --- | --- |
| Claircom **0000421562** | **741133**, **KNKG801** | Receipt Date **04/09/2001**, Date Entered **04/09/2001**, How Many Waivers Requested **4** | **7** rows. Three named waiver requests, an overview, Public Notice, Comments dated **06/14/2001**, and Order dated **10/05/2001**. |
| GTE Airfone **0000420815** | **740283**, **KNKG804** | Receipt Date **04/09/2001**, Date Entered **04/08/2001**, How Many Waivers Requested **1** | **6** rows. Four code `W` entries dated **04/08/2001** with blank descriptions, a Public Notice and Comments dated **06/14/2001**. |

The three Claircom request descriptions identify **§22.857**, **§§22.857 and 22.869**, and **§22.381**. The FCC notice and order describe three categories of joint requests. Preserve that description alongside the application-detail fields **4** and **1** and the attachment index counts. They use different labels and scopes. Neither the 4/1 fields nor the number of attachment rows is a verified count of distinct requests across both applications. Both files index a June 14 Comments row. The order reports one supporting comment, from Claircom. Whether the two rows refer to the same file remains untested. [FCC notice](https://docs.fcc.gov/public/attachments/DA-01-1216A1.pdf) · [FCC order, ¶¶1–2](https://docs.fcc.gov/public/attachments/DA-01-2336A1.pdf#page=1) · [Earlier comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/074c917cf37ad6b90751c6d9375a3d215362cc47/investigation/broader-evidence/telephone-claircom-2001-engineering-waivers-2026-11-05/README.md)

All **13** matching attachment filename fields are blank in the bulk export. The public ULS search form and both exact application pages returned HTTP **403** on this route. The ZIP and its selected rows are preserved. The export's metadata and these access outcomes leave the attachment bodies, their identifiers in other systems, and their availability elsewhere open. [Claircom application page](https://wireless2.fcc.gov/UlsApp/ApplicationSearch/applMain.jsp?applID=741133) · [GTE Airfone application page](https://wireless2.fcc.gov/UlsApp/ApplicationSearch/applMain.jsp?applID=740283)

## Reproduction and deferred originals

The source pins retain the verified ZIP hash, member and physical row locators, and only the fields needed for the comparison. The script verifies the snapshot hash and regenerates the two header rows, two detail rows and thirteen attachment rows. The current archive URL can serve a newer snapshot. This test is keyed to the preserved bytes. [Source pins](SOURCE-PINS.json) · [Verification script](verify_index.py) · [FCC record format](https://wireless.fcc.gov/wtbfiles/pa_ddef51.pdf)

- [ ] Locate original application bodies, the three titled Claircom requests and overview, GTE's four undifferentiated waiver entries, and the June 14 comments. Compare native files and version identifiers across the two applications before classifying duplicate records.
- [ ] Locate the actual exchanged test schedules and matched equipment installation or maintenance records. The attachment index and FCC order leave actual implementation and date of use open.
- [ ] Retain the independent call-specific switch, operator and event-dictionary dependencies and the carrier-custody TODOs. No September 11 call or technical configuration was identified by this index join.
