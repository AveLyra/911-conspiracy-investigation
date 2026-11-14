# R08 native-data gate: NOTE, User Events, comments and acquisition evidence

Review date: 2026-11-14. This subtask inspected original XLSX ZIP/XML for every `NOTE` and `User Events` sheet. It reused the independent full-workbook inventory for numerical sampling and legacy-comment checks, rather than parsing all measurement sheets twice. It also recovered and read the official TN 2054 and TN 2055 PDF bytes. No structural model, calibration, plot digitization or synthetic measurement series was produced.

## Decision

**The native-file access and source-identification gate passes.** The requested ambient specimen, all four fire specimens and the layout are available as original official bytes, with actual stored measurements and source-linked instrumentation. The earlier access failure must no longer be reported as the blocker.

**A quantitatively specified thermo-mechanical survival/damage benchmark is not yet ready to execute merely because the files are open.** Its remaining work is bounded: freeze clocks and channel validity, assemble the reported geometry/restraint/material inputs, choose and label any constitutive/heat-transfer assumptions, and predeclare outputs, tolerances and a whole-specimen holdout. These are substantive input-definition checks; they do not require an impossible complete sensor record or a new experiment. A limited ambient or structural-response benchmark can proceed once its scope and exclusions are declared. The principal CB-DA thermal caveat is real, not hypothetical: published steel-beam thermocouple readings can be invalid while remaining numeric.

## What the original notes establish

- `CB-DA-AMB.xlsx`, `NOTE!B4`: this is the separate specimen tested at ambient temperature. `NOTE!B5:B7` directs the reader to the layout, channel list and `CB-DA-AMB Data` sheet.
- Each fire file, `NOTE!B5:B8`: identifies its own channel list and event log; distinguishes that fire specimen's **mechanical preload before ignition** from its **fire-loading** sheet. In particular, `CB-DA-AmbientLoadingData` is CB-DA's own preload, not a substitute name for CB-DA-AMB.
- Layout workbook, `NOTE!B6:B9`: specifies separate ambient and fire instrumentation/channel-list sheets. `NOTE!B10` spells one file `CB-DA-AMP`; the same cell maps it to specimen `CB-DA-AMB`, corroborated by the actual downloaded workbook. Retain this source typo; do not invent a sixth specimen.
- Layout workbook, `NOTE!B11`, `D12:D13`: refers readers to TN 2055 and TN 2054 for experiment descriptions and measurement uncertainties. The reviewed NOTE sheets do not supply a full calibration certificate, per-row validity mask, or declared resampling/filter algorithm. Absence from these notes alone is not evidence that every channel is uncalibrated.

## Native clocks and event anchors

Every event sheet has `B1=Time (s)`, `C1=Time Stamp`, `D1=Event Description`. Excel numeric timestamp serials are preserved; reviewed cells do not declare a timezone.

| Specimen | Elapsed zero and meaning | Ignition in source elapsed seconds | Native cells |
|---|---|---:|---|
| CB-DA-AMB | Mechanical loading initiated | Not a fire test | `User Events!B2:D2` |
| CB-DA | Natural-gas flow initiated | 23.001399999999194 | zero `B3:D3`; ignition `B4:D4` |
| CB-DA-SC | Natural-gas flow initiated | 12 | zero `B4:D4`; ignition `B5:D5` |
| CB-SP | Natural-gas flow initiated | 53.003200000000106 | zero `B3:D3`; ignition `B4:D4` |
| CB-SP-SC | Natural-gas flow initiated | 21 | zero `B4:D4`; ignition `B5:D5` |

TN 2055 figure narratives use time after ignition. Therefore a later ignition-relative comparison needs a separately named derived field, e.g. `elapsed_seconds - User Events!B4` for CB-DA. Neither the input elapsed values nor timestamp serials should be overwritten. Each preload sheet starts its own elapsed clock; connect phases using timestamps plus explicit phase/event anchors, not by concatenating equal-looking elapsed values.

### Ambient event correction supported by native cross-evidence

`CB-DA-AMB User Events!B6` stores **4344** seconds. `C6` stores **42999.732881944445**; `(C6-C2)*86400` is **5930.000000064** seconds. The discrepancy is approximately **1586 seconds**.

The same timestamp occurs in `CB-DA-AMB Data!A3466`; `B3466` stores **5930**, and the attached comment identifies the end of the first loading cycle and deleted intervening data. A **derived reconciled event-time field of 5930 seconds** is thus supported by the original data row, exact timestamp match and comment. Preserve `User Events!B6=4344` with a discrepancy flag. This is a documentary correction, not a fabricated measurement or a reason to discard the entire ambient specimen. `User Events!D6` identifies shear-stud fracture at the **west** end, consistent with TN 2054's discussion and Fig. 5-12 caption.

### Survival is conditional on actual unloading

CB-DA `User Events!B5:D5` records actuator-limit unloading at **1802.1081000000004** seconds from gas-flow initiation; `B6:D6` records controlled cooling at **2143.1285999999991**, and `B7:D7` fire out at **4070.2442000000001**. A survival comparison must use that actual load history.

CB-SP-SC `User Events!B6:D9` separately records east-connection bolt fracture/load drop (4344 s), manual unloading (4350 s), fire out (4355 s) and later east-portion collapse (15583 s). It supplies distinct damage and late-collapse observations; they must not be collapsed into a single fire-end event.

## Declared sampling versus the delivered series

[TN 2054](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2054.pdf), §4.3, printed p.64 / PDF p.82, states **1 Hz recording**, together with standard deviations from the averaging process. It identifies NI cDAQ hardware, sensor-specific modules and LabVIEW acquisition, with different strain hardware for the ambient test. This is publication evidence about acquisition, not a claim that the delivered XLSX contains every underlying acquisition statistic.

The native-inventory calculations find 7777 stored ambient measurement rows, mostly at one-second spacing. Both ambient clock columns show six longer jumps. Comments establish deliberate data omission at those boundaries:

| Data-sheet boundary | Elapsed seconds before → after | Native comment at first row |
|---|---:|---|
| `A609:A610` / `B609:B610` | 607 → 1421 | Fiber-optic pause; data deleted |
| `A1209:A1210` / `B1209:B1210` | 2020 → 2892 | Fiber-optic pause; data deleted |
| `A2435:A2436` / `B2435:B2436` | 4117 → 4900 | Fiber-optic pause; data deleted |
| `A3466:A3467` / `B3466:B3467` | 5930 → 6154 | End first load cycle; data deleted |
| `A4703:A4704` / `B4703:B4704` | 7390 → 9829 | End second load cycle; data deleted |
| `A5303:A5304` / `B5303:B5304` | 10428 → 10908 | Data deleted; no more specific reason in this comment |

These omissions remain missing; do not interpolate and relabel them measurements. They do not invalidate intact loading segments. The measured discontinuities are larger elapsed intervals, not 7777 uniformly consecutive seconds.

CB-DA preload has 2356 rows and fire has 13085. Its elapsed column increments alternate between approximately 1.0000 and 1.0001 seconds. Its timestamp column normally advances one second, with one two-second step in the fire sheet that is **not** accompanied by a comparable elapsed-clock jump. Do not infer an omitted sample solely from that timestamp step. The two native clocks and diagnostics should both remain visible. Full row/channel/missingness counts and exact anomaly coordinates belong to `native_inventory`, not this note.

The inventory found no header explicitly identifying a standard-deviation, quality-flag, calibration or uncertainty column in the initially completed ambient/CB-DA/CB-DA-SC measurement sheets. This is a header-level observation, not a categorical claim that acquisition uncertainty records never existed. Published formula-derived aggregate columns must remain distinguished from stored individual channels.

## Measurement-validity consequences from recovered official reports

[TN 2054](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2054.pdf), §4.5, printed pp.77-81 / PDF pp.95-99, explains sensor uncertainty components and operating limitations. [TN 2055](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2055.pdf) documents specimen-specific failures.

| Relevant evidence | Consequence for later benchmark |
|---|---|
| TN 2055 §3.3.3, p.56 / PDF p.59: exposed CB-DA beam-thermocouple insulation failed around 10 min after ignition, enabling secondary junctions | Numeric TC values after the affected interval are not automatically true steel temperatures. They cannot be used wholesale as imposed temperature histories or thermal validation targets. |
| Same section: CB-DA-SC protected glass-wire readings diverge around 11 min; CB-SP readings become unreliable after approximately 32 min; CB-SP-SC routing under SFRM was more reliable | Use specimen- and sensor-specific validity rules. Do not transfer a single cutoff across all four fire tests. |
| TN 2054 p.79 / PDF p.97 and TN 2055 §3.3.3: added sheathed probes can lose steel contact during large movement and read hotter gas | A functioning numeric sensor can have changed physical meaning. A blank-cell mask alone is insufficient. |
| TN 2054 p.78 / PDF p.96: inclination uncertainty grows from ±9% near 25°C to ±29% up to 85°C, with 85°C the operating limit | Do not apply the ambient rotation uncertainty to the complete fire trace. |
| TN 2055 §3.4.3, p.74 / PDF p.77: CB-DA-SC rotation readings unreliable after ~56 min; CB-SP-SC inclinometer failure indicated near ~54/57 min and burned cables confirmed | Label valid rotation windows and preserve suspect stored values without counting them as trusted targets. |
| TN 2054 §4.3 and native ambient deletion comments | Describe the XLSX as official published engineering measurement data, preserving its documented reduction; do not claim untouched continuous raw DAQ output. |

Approximate publication times do not identify an exact first invalid worksheet cell. A later channel-validity table should state its conservative/sensitivity-window rule and convert ignition-relative limits using the recorded offsets. That transformation is derived analysis and should be named as such.

## Smallest next benchmark-preparation action

Produce one bounded model-input specification from the recovered sources: (1) corrected event crosswalk and explicit elapsed/ignition conventions; (2) valid channel/window mask with exclusions and reasons; (3) reported geometry, loads, restraint and material properties, with any selected heat-transfer or temperature-dependent constitutive laws identified as assumptions; (4) separately defined thermal-input and thermal-validation roles so no channel validates what it was imposed to determine; and (5) frozen survival, damage, displacement, strain and temperature targets, acceptance tolerances and whole-specimen holdout. Evaluate the intact ambient segments first; do not block them solely on deleted pause records. CB-DA's missing trustworthy late steel temperatures require an explicit thermal strategy or a narrower validation scope. No additional contact, request or fee is needed to perform this preparation from the recovered files.

This recovery stage supplies no numerical predictions and claims no successful benchmark.
