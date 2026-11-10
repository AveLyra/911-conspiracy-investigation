> **Historical research:** This document reports a prior source review, not a current instruction or new model run. Missing sources and run artifacts are identified; see the [publication note](../README.md).

# NIST generator/fuel source audit

2026-09-10. Research-only, bounded local documentary review; not a legal finding, a reproduced simulation, or a ranking of the whole collapse. Read with [claim ledger](claim-ledger.md), actual coverage and validation (historical local reference `source-log.md`; not included here), and [selection](SELECTION.md). Parent [protocol](../PROTOCOL.md) controls. No network retrieval occurred in this child task.

## Outcome

The two reports supply a checkable equipment map and conditional fuel-fire arguments, not a measured account of how much fuel burned. They expressly rely on assumed starting inventories, an estimated recovery, interviews, historical drawings and hypothetical fire scenarios. Several summaries flatten those distinctions or retain apparently superseded equipment. Those seams justify obtaining the underlying records and testing the assumptions; they do not establish fabrication, deliberate concealment, or a competing collapse mechanism.

The most important ceiling is that NIST's conclusion concerns the contribution of selected diesel-fire scenarios to its critical structural sequence. It is not a demonstrated absence of every fire in every mechanical space. Conversely, evidence that generators operated, or that an evacuee encountered heat and a fuel smell, is not a measurement of burning generators, spilled diesel, coolant composition or structural heat exposure.

Two reports from the same investigation are one source family. Where the account depends on a building-engineer interview, it must not be counted as an independent witness corroborating the earlier Commission interview merely because it appears in a different publication.

## Source pins and status

The inputs are existing local November 2008 editions. Their original acquisition route/date was not reverified here; no fresh official-download authentication is implied. Hashes establish the bytes reviewed, not the truth of underlying claims.

| ID | Existing source | SHA-256 | Extent |
| --- | --- | --- | --- |
| N9 | NCSTAR 1-9 (historical local reference `../../../../authority/nist/wtc7/ncstar-1-9.pdf`; not included here) | `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f` | 797 physical pages; combined volume file; title and November 2008 edition visually checked |
| NA | NCSTAR 1A (historical local reference `../../../../authority/nist/wtc7/ncstar-1a.pdf`; not included here) | `03c801bc1338533b54c6a64a66f074165c9429a59df11e2f58a19f5da91aef09` | 130 physical pages; title and November 2008 edition visually checked |

Pins below are **printed page / physical PDF page**. Physical page numbers are one-based. N9 selected chapter-3 through chapter-8 pages have physical offset +44; chapter 9 and Appendix A +66. NA selected text has offset +42. Do not apply one offset to the whole N9 file. Complete-page images are `derivatives/ncstar-1-9-physical-NNN.png` and `derivatives/ncstar-1a-physical-NNN.png`. The source log lists every page actually reviewed, including the blank page and out-of-scope adjoining page.

## 1. What fuel and equipment the reports describe

N9 §3.4.2, pp. 60–63 / physical 104–107, expressly abridges **NCSTAR 1-1J**; its reproduced schematics are not newly acquired original drawings. NA Table 1-2, p. 11 / physical 53, supplies a compact cross-check within the same source family.

| System | Published nominal inventory and location | What is not established by that description |
| --- | --- | --- |
| Base building | Two 12,000-gallon tanks below the loading dock; two 900-kW generators on floor 5; 275-gallon day tank within a 550-gallon collecting tank | Catch-basin capacity is not another fuel inventory. Installation and design do not establish actual contents, flow or operation throughout the day. |
| Salomon Brothers/SSB | Two 6,000-gallon tanks below loading dock; nine generators on floor 5; pressurized circulating loop, no day tank; valve/piping startup stock described as 35 gallons | Neither 12,000-gallon nominal storage nor the presence of a supply loop establishes a rupture, release location, pump duration or combustion. |
| Mayor's OEM | Separate 6,000-gallon tank on floor 1; three generators and 275-gallon day tank on floor 7 | This is not the Commission MFR's 15,000-gallon description. The difference needs a dated inventory/source reconciliation, not an assumption that either is a measured September 11 quantity. |
| American Express | Floor-8 generator and 275-gallon day tank explicitly described as removed in 2000/prior to September 11 | Historical plans and later summary tables retaining it cannot establish active equipment on September 11. |
| U.S. Secret Service | Floor-9 generator and 50-gallon day tank | This is a published tenant/system attribution, not an established identity match to the MFR's different agency grouping or 10,000-gallon quantity. |

The three main storage capacities sum to **42,000 gallons nominal**, using the reports' gallon figures (24,000 + 12,000 + 6,000). This simple bookkeeping sum is not an estimate of fuel present, fuel burned or heat release, and does not add day tanks or collecting basins. No thermodynamic or structural calculation was performed.

N9 pp. 49–52 / physical 93–96 and Figs. 3-1/3-2 map the mechanical spaces, vents and generators. Footnote 1 explicitly warns that the drawing-derived floor-5/6 details may differ from the September 11 layout. Walls, transformer rooms, plenums and louvers obstruct outside views. Large fires might nevertheless produce observable exhaust or wall damage, depending on the scenario. The negative-visibility argument therefore requires particular source views, times, vent states and expected signal sizes; it cannot be generalized to an unobstructed observation of all interior spaces.

### Actual contents and recovery

N9 p. 62 / physical 106 states that regular supplier checking/filling was the reason to **assume** the base tanks full. It cites **GZA GeoEnvironmental, Inc. 2002, Underground Storage Tank Closure Report, September 9** for estimated recovery of 23,000 gallons. The review has the citation, not that original report, gauge sheets, removal tickets, tank IDs or recovery uncertainty.

The empty, damaged SSB tanks and absence of a significant amount of fuel identified beneath them are reported retrospectively. N9 pp. 613–614 / physical 679–680 explicitly acknowledges that empty tanks cannot determine whether fuel burned before collapse, burned in the rubble afterward, or otherwise dissipated. Missing OEM tank/fuel similarly becomes an availability assumption, not measured combustion. An inference that all missing fuel burned inside the standing building would exceed even the report's stated evidence.

### Publication seams requiring reconciliation

These are verified textual differences, not findings about their cause:

- **Recovery timing:** N9 p. 62 says recovery in the days after the attacks; NA p. 12 / physical 54 says several months. The original dated recovery records decide the issue.
- **Unaccounted quantity:** N9 p. 62 prints `10 m³ ± 10 m³`; NA p. 12 prints `1000 gal ± 1000 gal`. They are not interchangeable precision inputs. N9 says uncertainty is unknown; NA states the base tanks were full without carrying forward the explicit assumption language.
- **Day-tank date/accounting:** N9 p. 62 retains three base-supplied day tanks totaling 600 gallons, while pp. 52 and 60 say the floor-8 equipment was removed. NA's removal footnote coexists with a three-day-tank statement and historical schematic. A date-specific system allocation is needed before adopting either aggregate.
- **Removed generator:** N9 Table A-6, p. 654 / physical 720, lists floor-8 generation as available, although §3.3.2 says it had been removed. N9 p. 614 / physical 680 and NA p. 52 / physical 94 also retain floor-8 day-fuel language. Historical carryover is a plausible explanation; this review does not infer fabrication.
- **Smaller diagram/unit seams:** Floor-5 day-tank labels in Figs. 3-1 and 9-1 give 250 gallons, versus 275 in text/table. N9 pairs 70 gallons/min with 5.3 L/s on p. 61 and 4.4 L/s on p. 369. Fig. 9-7's caption says southeast while the scenario-2 text says southwest. Preserve the exact source notation rather than silently normalizing it. None alone demonstrates a material collapse-analysis effect.

## 2. Operation and observations are not fuel-burn measurements

N9 pp. 295–297 / physical 339–341 attributes an engineer's sequence to **SSB Interview 1, January 2004**: equipment operating around 9:30, emergency lighting/generators after the WTC 2 collapse, and a subsequent exit account of heavy smoke/dust, reddish glow above, heat and fuel-oil smell. The published passage is not an instrument record or an observation of a specific generator burning. Its interview identity/provenance is not acquired here; the similarity to the prior Catalano account cannot create a second independent witness.

Appendix A, pp. 645 and 654–655 / physical 711 and 720–721, says the base generators operated after the WTC 2 collapse, referencing **WTC 7 Interviews 1, 2 and 3, January 2004**. It reports no information about their operation after WTC 1's collapse. Unknown later operation is neither observed shutdown nor proof of uninterrupted pumping. Automatic-start design for the other generators is not an actual run history; the report acknowledges unavailable operational information for other tenant units.

The Con Edison circuit/alarm tables, pp. 643–648 / physical 709–714, must be read by circuit and timestamp. Utility delivery to the building, live upstream feeders serving other networks, generator output, and SCADA reporting are distinct. The afternoon utility isolation is not a measured generator stop. Some table rows carry different manual-trip times. Alarm/normal transitions can reflect a reset or a cleared condition; the published interpretation considers dust as well as fire. They are not a thermal survey or a certificate that the whole building was fire-free.

N9 p. 70 / physical 114 reports that extensive internal fire-alarm-system information was not recovered; this is NIST's search/destruction account, not an independently audited archive inventory. P. 80 / physical 124 distinguishes installed suppression from unavailable evidence of actual performance in generator/tank spaces.

### Witness coverage and the lower-floor inference

N9 pp. 298–304 / physical 342–348 contains both fire reports and qualifications. A reported floor-6 fire appears among a chief's uncertain floor/time estimates (p. 302); the report also warns that some witnesses' floor identifications may be off by several stories (p. 299 footnote 19). The liquid-fuel non-observation is attributed to **FDNY Interview 3, winter 2004**, not every possible observer.

Section 9.2.3, p. 374 / physical 440, invokes a lower-floor reconnaissance without reported fire, heat or smoke. The underlying chapter-6 summary, p. 300 / physical 344, is narrower: observers saw limited damage from their particular viewing location on floors 4/5, changed stairs on floor 5, did not observe fire at their floor-8/9 location, and reportedly heard fires above. Nearby text describes another officer finding a smoky stairway and fire inside the building. The page cites **OEM Interviews 4 and 16, April/July 2004**, **FDNY Interview 73, summer 2004**, and **FDNY Interview 14, winter 2004**. This does not demonstrate an inspection inside every generator compartment. Original interviews and route/vantage reconstruction are needed before expanding omission into absence.

## 3. What the published diesel simulations do—and do not—test

N9 §9.2, pp. 366–374 / physical 432–440, describes hypothetical pool-fire scenarios, not measured fuel-release histories. It varies ventilation, fan/louver conditions and fuel flow, with northeast and southwest floor-5 locations. The argument uses the published compartment/column map, fuel/pump dependencies and modeled thermal effects. It is technically inspectable in outline, but this child task neither acquired executable models nor reproduced numerical results.

Important conditional links:

1. The scenario assumes a supply rupture and ignition, rather than establishing either from a recovered pipe or operating record.
2. For a northeast scenario, simulated hot gas around water-cooled generators leads to an inference of engine/cable failure and cessation of fuel pumping within roughly one to two hours (pp. 369–370 / physical 435–436). The relevant pages do not reproduce manufacturer-specific coolant composition/pressure, cooling-loop topology, allowable operating envelope, trip settings or actual shutdown logs. Gas near 100 °C is not itself a measured coolant temperature or demonstrated device failure time. Those records could strengthen or weaken the assumed self-limiting fire.
3. Under-ventilated flame migration is expressly described as speculative (pp. 371–372). A different ventilation case is rejected partly for predicted visible plumes. This review has not independently validated continuous exterior-view coverage or predicted signal detectability.
4. The southwest case allows local column damage but is discounted as a cause of the relevant east-side failure because of the assumed gas path and structural layout. The report acknowledges that a southwest plume could be obscured. A different breach/compartment path is a testable competing fuel scenario, not a demonstrated event.
5. Floor-7 and floor-9 pumped-supply fires are considered possible under specified circumstances; the report says a significant south-floor-7 fire might not be distinguishable within the south smoke/dust plume. Their distance from the critical east-side structural systems is part of the dismissal. The small day-tank stock comparison does not alone exclude an ignition/spread contribution.

At p. 374, those conclusions propagate into the main model: floors 5/6 begin at ambient temperature and heat only conductively from fires above; diesel is not explicitly included in floor-7/9 fire simulations. That is a disclosed **model-input choice derived from the preceding rejection arguments**, not an independently measured temperature boundary. The appropriate test is to audit its equipment, compartment, visibility and structural-sensitivity premises—not to treat either NIST's input or a contrary speculative fire as already observed.

## 4. Coolant, transformer oil and heat-source identity

The two PDFs do not identify the MFR's claimed 20,000 gallons of coolant by chemical composition, location, tank ID or measurement. Full-text locator results and full relevant pages were checked; this is bounded coverage, not proof that no other equipment inventory exists.

N9 Appendix A p. 641 / physical 707 describes the **Con Edison substation** transformers as mineral-oil/cellulose insulated. P. 642 / physical 708 describes the **building's floor-5** transformers as silicone-oil units. The former page also contrasts WTC 1/2 transformer fluid. Those are separate systems; a fluid label from one cannot be transferred to another. The summary's coolant-boiling discussion (p. 614 / physical 680) concerns a hypothesized generator failure, not a 20,000-gallon inventory.

The mid-October transformer photographs and damage discussion, pp. 650–651 / physical 716–717, are embedded derivatives attributed to **G&S Technologies**. Some transformer identities are uncertain. NIST explicitly cannot determine whether the thermal damage arose before collapse, after monitored data ended, or in later rubble fires. The photographs therefore cannot independently timestamp a pre-collapse fuel fire.

## 5. Exact underlying records that would discriminate

Every item below is **merely cited in the reviewed NIST inputs**, not separately acquired or authenticated by this child. Parent retrieval outcomes must remain separate. A table of contents listing a report is not acquisition of that report.

| Priority question | Exact published locator | Next discriminating content |
| --- | --- | --- |
| What was recovered, when, from which tanks? | N9 §3.5 p. 63 / physical 107: GZA GeoEnvironmental, Inc. 2002, *Underground Storage Tank Closure Report*, September 9 | Full report/enclosures, dates, tank IDs, gauge/recovery method, removal tickets, soil sampling and uncertainty; distinguish recovery from September 11 starting contents. |
| What equipment actually remained on September 11? | N9 p. 52 / physical 96 fn. 3: Trammel Crow Company, as manager for American Express, letter to Silverstein Properties, April 12, 2002; N9 §3.4.2 depends on NCSTAR 1-1J | Removal scope/date, revised inventory, connections left in place, dated as-built plans. |
| What sustained or stopped pumping? | N9 p. 387 / physical 453: Flack & Kurtz 1987, *Design Criteria for Mechanical, Electrical, Plumbing, Salomon Brothers 7 World Trade Center Headquarters*, April 20; p. 63 / physical 107: Flack & Kurtz 1988 mechanical/electrical drawings | Pump/engine/control dependency map, cooling/cable limits, protection settings, actual runtime/trip records and leak-detection behavior. |
| Is the engineer account an independent source? | N9 p. 295 / physical 339 fn. 3: SSB Interview 1, January 2004; Appendix A p. 645 / physical 711 fn. 2: WTC 7 Interviews 1–3, January 2004 | Full statements and identity/source map; segregate observation, interpretation and retrospective opinion; do not double-count Catalano-derived material. |
| How much lower-floor space did witnesses actually inspect? | N9 pp. 298–300 / physical 342–344: FDNY Interview 3, winter 2004; OEM Interviews 4/16, April/July 2004; FDNY Interviews 73 and 14 | Full interview context, time uncertainty, stairs/doors/routes, compartment visibility, whether fuel was specifically considered. |
| What did utility sensors measure? | N9 p. 656 / physical 722: Con Edison 2005g, Appendix F alarm list relating to TC1/TC2 from SOCCS X; 2005h, Appendix E district-operations incident report; 2005a, July 21 phone call; 2005b, August 19 email | Original SCADA data, alarm key, clocks/reset semantics, exact device mapping and original incident documents. Reference entries labeled 2005c–j print a 1984 letter date; preserve that discrepancy until resolved. |
| Which equipment/fluid belonged where? | N9 pp. 656–657 / physical 722–723: Con Edison 2005d Appendix A Rubenstein specifications EI-5451/EI-5413; Syska & Hennessy 1984a E-23 single-line, 1984b E-3 first-floor power, 1984c E-11 fifth-floor power | Dated as-built equipment/chemical inventory, fluid quantities, service revisions and manufacturer information; do not join by generic 'coolant' label. |
| Can fire/damage be located and timed independently? | N9 p. 649 / physical 715: embedded NYPD 2-50 #21, NIST-assigned 2:57 p.m. ±5 min; pp. 650–651 / physical 716–717: G&S photographs, August 2005 interview | Original imagery/metadata, wider scene and tank/transformer identity; separate post-collapse damage from pre-collapse heat. |

## Disposition

Advance the narrow leads for underlying inventory, recovery, equipment and interview records. Retain the unresolved publication seams. Do not promote assumed availability into a burned volume, a hypothetical engine shutdown into an observation, witness silence into complete coverage, or missing data into proof of intent. This audit identifies concrete ways to test the diesel/fire inputs; it does not supply a new overall likelihood ranking.
