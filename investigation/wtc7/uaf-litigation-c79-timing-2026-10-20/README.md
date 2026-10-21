# UAF litigation history and Column 79 timing followup

October 20, 2026, America/New_York. Public-source research, not a pleading, a new historical video measurement, or a finding about collapse cause or intent. Acquisition timestamps after midnight UTC fall on October 20 locally.

The UAF final report was released on March 25, 2020, after Quick was decided and one week after the last merits brief listed in the mirrored Column 79 Cole docket. A later lawsuit expressly relied on UAF, but it was an administrative-law correction challenge, not a FOIA case, and was dismissed for lack of standing. New technical leads identify different UAF output-database names and plot states, and an apparent order conflict between NIST's narrative and its own failure table. Neither establishes erroneous solver calculations.

## UAF availability and the litigation record

| Record | What is established | What remains unknown |
| --- | --- | --- |
| [UAF project page](https://ine.uaf.edu/wtc7) and [contemporaneous release](https://www.ae911truth.org/images/PDFs/UAF-Final-Report-Release-03-25-2020.pdf) | Draft release September 3, 2019; final release March 25, 2020. | Availability does not show any litigant downloaded, read or filed either version. |
| [Quick, ECF 24, April 7, 2011](https://www.govinfo.gov/content/pkg/USCOURTS-dcd-1_09-cv-02064/pdf/USCOURTS-dcd-1_09-cv-02064-0.pdf) | The decision predates both versions and UAF's listed 2015 project start. This case could not have considered the later UAF report. | No claim about every scientific criticism available in 2011. |
| [Cole, No. 19-1182, ECF 20, November 30, 2020](https://www.govinfo.gov/content/pkg/USCOURTS-dcd-1_19-cv-01182/pdf/USCOURTS-dcd-1_19-cv-01182-0.pdf) | The opinion postdates the final report. Its 18 pages contain no whole-word matches for Hulsey, Alaska, Fairbanks or UAF and no express weighing of UAF against NIST. | Whether Cole actually submitted or relied on the 2019 draft cannot be determined without the briefs and exhibits. Silence in an opinion is not proof of absence from its record. |
| [Mirrored Cole docket](https://foiaproject.org/case_detail/?case_id=32511&style=foia&title=on) | ECF 12-14 were filed February 4, 2020; government ECF 16-17 March 4; Cole's ECF 19 reply March 18. The reproduced entries list no supplemental merits submission between that reply and judgment. | This is a third-party docket transcription, not a fresh PACER certification. Its linked docket PDF and the underlying briefs were not retrieved. No paid retrieval or third-party contact occurred. |

The important distinction is **pre-decision availability versus pre-briefing availability**. The final UAF report was available before Cole's decision but was released seven days after its last listed merits brief. The 2019 draft was available during that briefing. Neither chronology establishes actual consideration. Calling Cole a judicial rejection of the UAF analysis would exceed the reviewed record; calling its FOIA holdings irrelevant would also be wrong.

Quick decided search, withholding and segregability merits; it was not merely an unopposed motion. Cole upheld NIST's request interpretation, search, Exemption 3 withholding and segregability on its record, including rejecting creation of new screenshots. Those decisions concern access to records, not a comparative engineering trial of NIST and UAF. A later scientific disagreement does not automatically defeat the withholding statute.

### Confirmed later use outside FOIA

The [January 31, 2022 first amended complaint, ECF 14](https://www.ae911truth.org/images/PDFs/AE_FAC_Court_file_date_stamped_and_redacted.pdf#page=6), in *Architects & Engineers for 9/11 Truth v. Raimondo*, No. 21-2365, expressly discusses the UAF study at paragraph 15 and elsewhere, including paragraphs addressing Column 79. That is a demonstrable example of UAF being advanced against NIST in litigation. Allegations in a complaint are not judicial findings or a showing that every cited underlying file was admitted in evidence.

The [court's August 2, 2022 opinion, ECF 22](https://www.govinfo.gov/content/pkg/USCOURTS-dcd-1_21-cv-02365/pdf/USCOURTS-dcd-1_21-cv-02365-0.pdf#page=9), pp. 3-4, 8-10 and 14, describes a challenge to denial of an April 2020 information-quality correction request under administrative law and dismisses for lack of standing. It directs claims for unreleased investigation materials to FOIA, citing the Cole decisions. This is **not** a merits determination that UAF's calculations are wrong, and **not** a FOIA adjudication accepting UAF as a basis to release the models. The present review has not established any prior FOIA adjudication that weighed the UAF report as technical counterevidence. That remains a bounded search result, not a claim that none exists.

The court-authored 2020 Cole PDF newly obtained from govinfo differs in bytes from the earlier held copy: SHA-256 `f99ab6540aa1156e65be7eb9f9afd971f3fdc4df13080f9099baa2d24575c100` versus `fb99c61e142de8f681126d3510c6806b894b67ffcf2984d572744472df6ca889`. All 18 extracted page texts match exactly with the tested extractor. Both hashes are retained; that text comparison neither establishes full visual/metadata identity nor explains the byte differences.

## New UAF output identifiers and displayed states

In [UAF's final report](https://files.wtc7report.org/file/public-download/A-Structural-Reevaluation-of-the-Collapse-of-World-Trade-Center-7-March2020.pdf), the image footers provide these locators:

| Figure and location | Visible database label | Displayed state |
| --- | --- | --- |
| 3.4, printed 78 / physical 91 | `Model-9_Nonlinear_10s.odb` | Step-1, increment 63, step time approximately 8.60 s; the small raster's last displayed digits are not certified here. |
| 3.7, printed 81 / physical 94 | `Model-16_Linear_10s_No_Protrusion1.odb` | Step-2, increment 25, step time 1.000 s. |

The previously recorded facts remain: Section 3.2.2 removes the plate protrusion and raises the named beams' thermal-expansion coefficient by approximately 40 percent. These footers add precise native-file locators, not another executed experiment. The words `Linear` and `Nonlinear` in filenames do **not** establish the actual geometric-nonlinearity, material, contact or solver settings. Step time can reset between analysis steps; 8.60 versus 1.000 does not establish unequal total elapsed time or loading. Neither plotted state is silently substituted for the other.

The corresponding Figure 3.4 and 3.7 decoded image streams match across **both preserved final-report PDFs**. Their presentation differences on physical page 91 remain separately preserved; matching image content does not make the PDFs identical or authenticate the native outputs.

**Why this matters:** a clean plate-effect comparison needs matching loading, contacts, nonlinear geometry, material laws and output states. The report's two known parameter changes already prevent treating this as a one-variable test. The filenames and step labels identify additional settings to verify, not proof they differed. Obtain both named ODBs, matching INP/CAE files, step definitions, `NLGEOM` settings, thermal histories and the figure-to-case mapping. Existing [factorial protocol](https://github.com/AveLyra/911-conspiracy-investigation/tree/main/investigation/wtc7/c79-factorial-protocol-2026-10-19) remains unexecuted and unchanged.

## New NIST narrative versus failure table order

[NCSTAR 1-9](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf#page=396), printed pp. 352-353 / physical 396-397, narrates all four Column 44 erection-bolt failures at girder temperature 398 C before describing first northmost-beam buckling at beam temperature 436 C. The source sentence crosses the page boundary. Table 8-2 on printed 353 gives a different apparent order:

| Table time s | Beam C | Girder C | Table event |
| --- | --- | --- | --- |
| 2.04 | 406 | 339 | Both Column 44 seat bolts failed. |
| 2.10 | 436 | 364 | Northmost floor beam began lateral buckling. |
| 2.18 | 476 | 398 | Both Column 44 top-plate bolts failed. |

The table places first buckling **0.08 simulation seconds before** the last two Column 44 bolt failures; the narrative presents all four failures earlier in its sequence. This is an apparent narrative-order discrepancy, not conflicting numerical temperatures for one material: beam and girder temperatures must not be interchanged. The nearby prose specifically refers to seat-bolt failure before buckling, which agrees with the 2.04 row; that limits any claim that the entire passage has an unambiguous, internally consistent alternative chronology. No account is selected as controlling.

These seconds belong to a deliberately accelerated preliminary loading analysis: gravity is ramped over 1 s, with member temperatures then rising to 600 C for beams and 500 C for the girder. They are **not seconds of the observed building collapse**. No comparison equates them with west-penthouse video times. A reordered narrative, an event-definition difference, or a tabulation/run discrepancy are untested possibilities. The exact event histories, bolt-spring states, buckling criterion and source of Table 8-2 would discriminate among them. No solver error, consequential changed outcome or deceptive intent is established.

## Model equivalence and earlier timing conflicts remain open

UAF's Chapter 3 discusses several NIST stages. NIST's preliminary detailed model explicitly represents side-plate contact and predicts bolt/stud failures; the later ANSYS model uses a reduced connection representation. A demonstration about one stage is not automatically a test of the other. [NIST FAQ Q28](https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation) expressly describes different temperatures and boundary conditions and the transfer of failure modes using connection elements and APDL scripts. This makes the exact transfer scripts and plate-contact equivalence important records; it does not establish that those scripts omitted the restraint. The current direct FAQ capture returned 403, while the web reader succeeded; the failure and the earlier successful preserved capture are both retained.

The earlier [animation timing audit](https://github.com/AveLyra/911-conspiracy-investigation/tree/main/investigation/wtc7/animation-timing-audit-2026-10-16) is unchanged. Figure 12-68 still has 13.3 s panel offsets versus 16.0 s caption offsets. The west-penthouse comparison remains reported observation 9.3 s versus model views 6.9/7.3 s. The 12.9 s validation interval still relies on an inferred interior-failure start. These are not new independent video measurements. The underlying run/time/figure map and validation worksheets remain necessary to evaluate them.

## Verification and preservation

`audit.py` checks source hashes before and after, both UAF image identities, the NIST table with two extraction libraries, timing arithmetic and the two Cole texts. `observations.json` preserves the output and manual image transcriptions separately. Source links, receipt hashes, access failures and unfilled retrieval targets are in `sources.json`. The new raw public court opinions are redundant preservation copies through LFS; old PDFs, notes and conflicting values are not edited.

Complete pages visually reviewed: NIST physical 396, 397 and 659; UAF physical 89, 93, 94 and 97; Cole physical 18; AE2022 physical 9. Figure 3.4 and 3.7 embedded original images were also inspected. Additional pages were text-reviewed, not all visually reviewed. No historical footage was newly timed; no finite-element model was run; no private correspondence, pleading, discovery position or case registry was changed.

To reproduce, install/use the already available PyMuPDF and pypdf environment and run `audit.py --nist <NCSTAR1-9.pdf> --uaf <March2020.pdf> --uaf-other <March-2020.pdf> --cole <govinfo-Cole.pdf> --cole-prior <earlier-Cole-copy.pdf>`. The source hashes and public locators are recorded, not inferred from filenames.
