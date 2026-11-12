# Orabi follow-up: experimental benchmark source checks

11 November 2026. This checks selected experimental and historical claims from the recovered body of Scooby report 30 against the original published studies. It is not a completed audit of that report, its attachments, or the 30-report set. It does not report a new numerical simulation.

## Choe / NIST composite-beam experiments

The primary [NIST Technical Note 2055](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2055.pdf), pp. 66–67 and 89, and the authors' [journal article](https://pmc.ncbi.nlm.nih.gov/articles/PMC7542547/) support the following:

| Recovered claim | Check and qualification |
|---|---|
| Four 12.8 m composite beam specimens were subjected to fire; CB-DA survived and CB-SP and CB-SP-SC failed. | **Supported with an essential qualification:** the tests used different unloading criteria. CB-DA was automatically unloaded at 30 minutes when its actuator load limit was reached; it did not collapse during the subsequent decay/cooling. This is survival under that specific loading and unloading history, not proof it would have survived continued design loading. CB-SP collapsed during heating from shear-tab **weld** failure. CB-SP-SC lost a bottom bolt during heating and later collapsed during cooling when remaining shear-tab bolts fractured. |
| CB-SP-SC peak compressive beam-end load was 1,020 ± 35 kN. | **Supported as an estimate:** NIST Table 12 reports 1,020 ± 35 kN at 41 minutes, derived from brace strain and calibration; it is not a direct force-gauge measurement. This peak compression is distinct from the later tensile loading and connection fracture during cooling. |
| A simulation without connection fracture cannot establish that it reproduces the observed fracture. | **Sound model-validation principle**, not a previously executed test. It could still be assessed on prior thermal/deformation response or a survival case, provided the exact loading and unloading histories are represented. |

## Dai full-floor connection experiment

The original [Dai et al. paper](https://link.springer.com/article/10.1007/s10694-023-01452-1), sections 2, 4 and 5, supports the recovered distinction between observed and calculated outcomes:

| Recovered claim | Check and qualification |
|---|---|
| The floor specimen was hydraulically loaded to 5.3 kPa. | **Supported:** the paper states the load and specified load combination. These experiment conditions are not direct measurements of WTC 7 loading. |
| Connection C2 reached a maximum measured component temperature of 660 °C but did not show the bolt shear failure predicted by the simplified calculation. | **Supported:** Table 1 and section 4 give the component maximum; the paper says the simplified comparison predicted failure at about 575 °C and that this was not witnessed. The 660 °C is a maximum for a measured connection component, not necessarily the uniform temperature of all bolts. |
| Connection C6 showed partial bolt shear rupture. | **Supported:** the paper says post-fire inspection found partial shear rupture in three of five bolts in the specified middle-to-lower region. Its explanation invokes thermal restraint and bowing; the inferred force and moment are not independently measured failure causes. |
| The plotted connection axial forces were calculated from measured strains rather than measured directly. | **Explicitly supported:** section 5.2 cautions that the calculated axial forces are not measured and recommends measured strains and displacements for validation. The calculation also relies on assumptions about composite action, fixed bases and elastic columns. |

Both the survival and damage examples are useful as *potential* benchmarks. Success requires a frozen model, the actual specimen geometry and thermal/loading histories, defined tolerances and independent comparison; no OpenSees-for-Fire reproduction was run in this review. Neither laboratory test by itself establishes a WTC 7 failure mechanism, explosives, or the involvement of Urban Moving Systems.

## Fuel, fireproofing and missing dependencies

NIST's [WTC 7 report](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861611) says the two 6,000-gallon Salomon tanks were found damaged and empty, with no significant fuel identified in adjacent soil and gravel. That post-collapse observation and a modeling assumption that fuel was available do **not** measure how much fuel burned in the fifth-floor room. [NIST's FAQ](https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation) says it modeled fireproofing as undamaged except near southwest debris damage, based in part on reviewed photographs; this is not a direct inspection of every Truss 2 member on September 11.

The retrieved original benchmark reports do not settle the actual fire exposure and protection of Truss 2. The particular executable, WTC input decks, active settings, dynamic handoff and experimental comparison runs remain unverified. The captured research text also makes other claims about solver builds, fire histories and model settings that this focused check does not resolve.
