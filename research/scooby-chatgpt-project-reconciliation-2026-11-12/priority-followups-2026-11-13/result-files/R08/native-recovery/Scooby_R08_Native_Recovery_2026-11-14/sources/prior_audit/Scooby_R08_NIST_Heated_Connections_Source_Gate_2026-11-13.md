# Scooby R08 — heated-connection experimental benchmark: native-data gate

**Review date:** 2026-11-13  
**Mode:** regular GPT-6 chat; no Deep Research, no model execution  
**Disposition:** **Inputs partially documented; independent numerical benchmark NOT yet supportable.**

## Scope and prior-work distinction

Scooby T1 §42 (2026-11-12) specified Choe component testing and a subsequent held-out comparison, but explicitly did not inspect the original measurement workbooks or run a structural solver. This continuation inspected the NIST public project page and read its official *Technical Note 2055* (November 2019), including experimental design, instrumentation, uncertainties and results. **The six original XLSX workbooks were linked and identified but their bytes/sheets/cells could not be retrieved in this environment.** Thus, the present review is an improved source-and-instrument map, **not the requested measurement-file audit**. Do not count summarized curves or tabulated endpoints as extracted native time-series data.

## Original source/route register

1. NIST project page: https://www.nist.gov/programs-projects/measurement-structural-performance-fire/steel-concrete-composite-floors — page states *Created December 6, 2019; Updated June 3, 2025*. Its test links explicitly advertise downloadable spreadsheets. This review verified the webpage's five test names and routes.
2. Instrumentation layout workbook, `cbtestsetupinstrumentationdrawings`: https://www.nist.gov/document/cbtestsetupinstrumentationdrawings — **not acquired** (XLSX response inaccessible through retrieval interface).
3. Ambient baseline, `cbdaambientdata` / `CB-DA-AMB`: https://www.nist.gov/document/cbdaambientdata — **not acquired** (XLSX response inaccessible).
4. Fire specimen `CB-DA`, `cbdadata`: https://www.nist.gov/document/cbdadata — **not acquired** (XLSX too large for one retrieval interface).
5. Fire specimen `CB-DA-SC`, `cbdascdata`: https://www.nist.gov/document/cbdascdata — **not acquired**.
6. Fire specimen `CB-SP`, `cbspdata`: https://www.nist.gov/document/cbspdata — **not acquired**.
7. Fire specimen `CB-SP-SC`, `cbspscdata`: https://www.nist.gov/document/cbspscdata — **not acquired**.
8. Choe et al., *NIST TN 2055: Compartment Fire Experiments … Part 2: Test Results*, **November 2019**, https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2055.pdf, DOI https://doi.org/10.6028/NIST.TN.2055 — **official PDF text inspected**; not a substitute for raw XLSX.
9. Ramesh et al., *NIST TN 2054: … Part 1: Experiment Design and Beam Behavior at Ambient Temperature*, **2019**, https://doi.org/10.6028/NIST.TN.2054 — official publication identified; its full large PDF could not be retrieved here. Original baseline calibration and acquisition details therefore not independently audited.

**Version/identity limitations:** No spreadsheet filenames resolved from the HTTP content-disposition, workbook hash, byte size, Excel sheet names, channel headers, cell addresses, formula/value distinctions, file dates, update history or rows were verified. No invented workbook citations appear in this report.

## Initial matched family and known design: CB-DA-AMB versus CB-DA

According to TN 2055 Table 1 (printed p. 17), `CB-DA-AMB` was tested **2017-09-21** at ambient temperature and `CB-DA` was tested **2017-12-19** in fire. Both use double-angle end connections without slab continuity over the support girders, but **they are distinct specimens**; the ambient specimen cannot be presumed to provide the fire specimen's own zero-strain or as-built measurements.

From TN 2055 §§2.2–2.3 and Figs. 1–4 (printed pp. 17–22): nominal span between support columns **12.8 m**; steel beam length **12.3 m**; bolt-line spacing **12.2 m**; W18×35 beam; slab **1.83 m** wide; **83 mm** lightweight-concrete topping above a **76 mm** deep ribbed deck; nominal **19 mm** stud anchors at **305 mm** spacing; double-angle connections with **three 19 mm bolts** and **8 mm fillet welds** to sacrificial plates. The beam and connection regions were coated with SFRM, nominally to two- and three-hour ratings, respectively; for CB-DA the measured *mean ± sample variation* was **20 ± 3 mm** over beam, **28 ± 7 mm** over connection elements and **22 ± 3 mm** on beam web near connection edges (TN 2055 Table 2, printed p. 20). These variations are not spatial thickness maps or metrological confidence intervals.

The fire specimen was loaded through **six hydraulic actuators** with approximately **106 kN total applied**, plus specimen/fixture dead loads. The total ASCE 7 combination was reported as **210 kN**; calculated specimen and fixture weights were **58 kN** and **46 kN**, respectively (TN 2055 §3.2.1, printed p. 38). The column restraint assembly had measured lateral stiffness **190 kN/mm** pushing away from compartment and **170 kN/mm** pulling toward it (TN 2055 §2.3, p. 21). The furnace used natural-gas burners with a controlled **up-to-4000 kW** rate, but the **measured** histories, not the nominal target, are the requisite thermal input. The loading/unloading protocol differs across specimen types: `CB-DA` automatically unloaded at approximately 30 min after fire ignition on a 90 kN actuator-load threshold, so *survival after unloading is not evidence of surviving full sustained applied load* (TN 2055 §3.1 p. 37; §3.2.2 pp. 40–41).

**Published experimental landmarks, not a sampled time-series:** For CB-DA, the maintained ambient actuator total was **106.1 ± 0.1 kN**, and mean point load **17.7 ± 0.4 kN** (TN 2055 Table 5, p. 38; the ± values are reported sample SDs, not Table 4 expanded uncertainties). Both beam ends underwent local buckling at about **30 min**. After actuator unloading the specimen did not collapse, and its maximum recorded downward deflection was about **330 mm**; the gas-firing decay ended around 68 min (TN 2055 §3.4.2, printed p. 70). An **estimated** peak compressive beam-end load of **716 ± 85 kN at 30 min** appears in Table 12 (printed p. 67); the calculation uses measured brace strain multiplied by **3.90 kN/με**, and thus is **not a directly measured connection force** (TN 2055 §3.4.1, pp. 66–67). The experiment documents both *damage* (local buckling) and *survival* (no collapse); neither means the connection was undamaged.

## Instrument, reporting-unit and expanded-uncertainty map

The accompanying `Scooby_R08_instrument_map_2026-11-13.csv` is machine-readable. Below, reported uncertainties are **TN 2055 Table 4 expanded uncertainties (k = 2, approximately 95%)**, NOT verified workbook-cell uncertainty; several quantities need further instrument-specific calibration.

| Quantity and sensor family | Published physical units / typical channel IDs | U(k=2) reported | Direct observation or derived? | Official locator |
|---|---|---:|---|---|
| Actuator forces, six load channels | kN; `LoadNE`, `LoadSE`, `LoadNM`, `LoadSM`, `LoadNW`, `LoadSW` | ±8% | Measured load at actuators, **not connection force** | TN 2055 pp. 24, 26, Table 4 |
| Actuator strokes | physical displacement, published plots use mm; `DispNE` etc. | Instrument class not separately established | Direct actuator strokes, not necessarily beam deflection | TN 2055 pp. 24, 70 |
| Vertical slab displacement, string transducers | mm; **`VD2`–`VD5`** in Table 13 | ±5% | Measured deflection | TN 2055 pp. 23, 26, 70–71 |
| Slab inclinometers | rotation; `RotSlabEx`, `RotSlabWx`, `RotSlabEy`, `RotSlabWy` (raw units unverified) | ±9% at ambient 25°C | Measured rotation | TN 2055 pp. 23, 26, Fig. 6 |
| Brace strain gauges | µε; `ColE2`–`ColE8`, `ColW2`–`ColW8` for CB-DA in Table 12 | ±5% | **Measured strain**; connection axial force *inferred* via calibration | TN 2055 pp. 24–26, 66–69 |
| FBG concrete strain | µε; FBG gauges in CB-DA and CB-DA-AMB | ±3.1 µε **standard** uncertainty, not expanded | Measured averaged strain along gauge length; thermal sensing limitations | TN 2055 p. 24, Figs. 12–13 |
| Beam steel thermocouples | °C; `TC1`–`TC8` section families; supplementary `STC` not installed in CB-DA | ±5% | Measured temperature; failures/dislodgment not covered | TN 2055 pp. 24, 26, Fig. 7 |
| Concrete thermocouples | °C; channel names to be checked | ±7% | Measured temperature | TN 2055 p. 26 Table 4 |
| Steel deck thermocouples | °C; channel names to be checked | ±5% | Measured temperature | TN 2055 p. 26 Table 4 |
| Compartment gas thermocouples | °C; `TCC1`–`TCC24` | ±4% | Measured temperature | TN 2055 pp. 24, 26, Fig. 9 |
| Plate thermometers | temperature / derived flux; `PT1`–`PT3` in **CB-SP, CB-SP-SC only** | ±5% for temperature | Not present in CB-DA | TN 2055 pp. 24, 26, Fig. 10 |
| Burner HRR from fuel flow | kW; `HRRburner` | ±2% | Fuel-flow-derived thermal-source rate | TN 2055 pp. 25–27 |
| Hood calorimeter HRR | kW; `HRR` | ±15% | Calorimetric derived heat release | TN 2055 pp. 25–27 |
| Rebar anchor load cells | kN; **SC specimens only** | ±11% | Direct force at monitored reinforcing bars | TN 2055 pp. 24, 26 |
| Nominal dimensions | mm | ±27 mm (>0.5 m); ±8 mm (<0.5 m) | Survey dimensional uncertainty, not as-built connection tolerances | TN 2055 p. 27 Table 4 |

**Channel discrepancy to resolve from original files:** TN 2055 §2.4 printed p. 23 calls the four vertical channels `VD1`–`VD4`, whereas its Fig. 6 caption and Table 13 (printed p. 70) identify `VD2`–`VD5`. Do **not** select one set silently. Likewise the exact workbook unit for rotation must be read from the headers, not inferred from publication plots.

## Numerical benchmark decision

**Current gate: FAIL.** NIST provides enough design information to formulate the *class* of a component finite-element model, but **not enough verified native input data in this review to perform an independent numerical benchmark**. Specifically missing/not independently checked:

- Downloadable **actual CB-DA-AMB and CB-DA XLSX bytes** (all sheets, exact headers, units, time origins, pre-ignition baselines, sample rate, gaps, quality flags, corrections and original precision); plus `cbtestsetupinstrumentationdrawings` for channel-to-position matching. No exact sheet/cell citations are possible yet.
- A reconciled, time-synchronized **six-actuator force/stroke history; beam/slab displacement and rotation; measured brace strain; connection/beam/deck/slab thermal histories; burner/compartment temperatures through cooling**. The report's figures are not numerical data exports.
- NIST TN 2054's complete **ambient force–deflection baseline, sensor calibration and fixture effects**, where not confirmed by independently readable workbooks and supporting Part 1 documentation.
- Verified per-specimen material and constitutive inputs for **temperature-dependent steel, welds, bolts, studs, concrete cracking/crushing, interface slip, local buckling/contact**, and appropriate uncertainty bounds. TN 2055 Table 3 gives useful **room-temperature coupon values**, not an observed high-temperature fracture law. Any missing laws must be identified as modeling assumptions and tested for sensitivity, not fitted solely to reproduce observed rupture.
- Residual-support/damage and actuator-control assumptions across unloading/cooling, plus failure-time precision and missing/dislodged sensors, to compare prediction with observations on a common clock.

**Validation targets provisionally locked before any calibration**, using only the publication: for CB-DA, (i) six-point loading and displacement profile, (ii) measured beam/deck/connection temperature curves, (iii) local buckling onset around 30 min, (iv) response to actuator unloading and fire decay, (v) no gravity collapse and about 330 mm peak recorded displacement, and (vi) measured brace strain rather than force inferred by the model. The **numerical acceptance tolerances and full time-series targets cannot be frozen** until original measurement rows and acquisition quality are inspected. A subsequent genuine holdout should use one **entire fire specimen**, e.g. `CB-SP-SC`, excluded from calibration, with survival/damage evaluated under the same predeclared material and connection laws. `CB-DA-AMB` is a **separate ambient baseline specimen**, not a fifth fire replicate.

Dai C2/C6 are two instrumented connections **within one full-floor experiment**, not independent trials. They are outside this initial CB-DA source gate. Orabi's 2.3-second termination is a computational endpoint, **not** independently observed physical arrest or global collapse. A validated component law cannot establish historical WTC 7 fire exposure, fireproofing condition, load paths or boundary supports.

## Reproducibility and stopping statement

- **Native workbook cells/versions verified:** none.
- **Measured native time-series rows exported:** **0**. No synthetic series, plot digitization or interpolation was substituted. **There is no measured time-series dataset in the deliverables.**
- **Numerical runs/calibration/holdout:** none. No objective error metrics, predictions or specimen-level validation results can be claimed.
- **Artifact produced:** source-audited instrument map CSV, not an experimental dataset.
- **Required next input:** accessible original NIST `.xlsx` files with their exact sheets, and the drawing workbook. Once available, extraction should preserve `(source URL, binary hash, workbook sheet, cell coordinate, channel, raw unit, measurement time)` per value, distinguish each missing/invalid point and transform units only after reading channel definitions.

No contacts, records requests, payments, Deep Research or external software experiments were initiated.
