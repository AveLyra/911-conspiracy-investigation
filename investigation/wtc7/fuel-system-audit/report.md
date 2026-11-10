> **Historical research:** This document reports a prior source review, not a current instruction or new model run. Missing sources and run artifacts are identified; see the [publication note](README.md).

# Generator fuel and structural-heating evidence

The available witness memorandum does not establish how much diesel burned, its location or duration, or the heat delivered to structural members. NIST supplies a substantially more specified equipment and scenario account, but several important links remain reported, assumed or model-dependent rather than independently verified here. Its rejection of a significant diesel contribution to collapse is therefore a testable conclusion, not an observation that no diesel burned.[^1][^2]

This is a research-only documentary audit. It neither reproduces a fire/structural solver nor changes the collapse-mechanism ranking. The [claim crosswalk](claim-ledger.md), search coverage (historical local reference `source-log.md`; not included here) and [validation record](validation.md) distinguish completed checks from open work.

## Fuel quantity and location

The MFR's four attributed storage amounts total 47,000 gallons, while a later passage refers to 50,000 gallons. Those statements do not distinguish installed capacity from actual contents. NIST's table instead organizes main storage into base-building, Salomon and OEM systems, with separate day tanks and locations. Similar totals do not reconcile the different ownership/system assignments, and a rounded inventory discrepancy is not a measurement of consumption. Tank drawings, dated fill/gauge records and a system-by-system identity crosswalk are the appropriate checks.[^1][^3]

For the base-building system, NCSTAR1-9 explicitly assumes the tanks were full because of a regular filling contract, then reports an estimated recovery of 23,000 gallons from a nominal 24,000-gallon capacity. It says the uncertainty in these volumes is unknown. NCSTAR1A presents the initial fullness more categorically. Neither publication supplies the original gauge readings and recovery tickets in the reviewed pages. The underlying GZA report is precisely identified but has not been acquired.[^2][^3]

Three reconciliation issues should remain visible:

- **Recovery chronology:** NCSTAR1-9 printed62 says recovery occurred in the days following the attacks; NCSTAR1A printed12 says several months. The contractor's dated field records could resolve whether these describe the same recovery operation. The discrepancy alone does not determine how much fuel burned before collapse.
- **Installed configuration:** NCSTAR1-9 printed52/60 says the Floor8 generator and day tank were removed in2000, while printed62 retains a three-day-tank/600-gallon account. NCSTAR1A's table footnote also records removal. A schematic showing the earlier system is not proof that all its equipment remained installed on September11.
- **Units:** NCSTAR1-9 printed61 gives the same nominal 70-gallon/minute pump rate as 5.3 L/s, whereas printed369 gives 4.4 L/s. The original specification and actual simulation input must determine which value entered the calculation. Do not silently normalize the published volume/rate pairs or infer a downstream error magnitude without the input deck.[^2][^3]

For the Salomon tanks, NCSTAR1-9 printed614 explicitly acknowledges that their damaged, empty post-collapse condition cannot distinguish pre-collapse fire consumption from later consumption or dissipation in burning rubble. That qualification blocks the inference “empty tanks prove a long-duration generator-room fire.” Conversely, it also blocks treating the recovery account as proof that such a fire did not happen.[^2]

## Morning observations and later exposure

The MFR preserves an account of smoke, heat, obstructed escape and equipment involvement during the morning emergency. Its generator-jamming explanation, precise operating-duration assertion and counterfactual collapse opinion go beyond those sensory observations. They require different corroboration: equipment inspection, transfer/control records, and a building-specific thermal/structural analysis, respectively.[^1]

NIST's emergency-response narrative includes a building engineer's account of a reddish glow, heat and fuel-oil smell near an east exit after the first tower collapse. That narrative cites a January2004 SSB interview. It must not be counted automatically as a second witness independently corroborating Catalano. The underlying interview and exact identity/source join have not been independently obtained here. Likewise, NIST's AppendixA statement that some emergency generation operated relies partly on interviews; it is not a continuous generator log.[^2]

The reported continued energization of parts of the Con Edison substation is also not equivalent to continued utility power at every WTC7 consumer or fuel pump. AppendixA distinguishes these circuits. An argument for long-duration pump operation needs the actual wiring, switching and operating state of the relevant pump, not merely evidence that a nearby high-voltage circuit was live.[^2]

No reviewed source identifies the MFR's asserted 20,000 gallons of coolant with a measured combustible inventory. Engine coolant, rooftop cooling equipment, substation transformer fluid and building transformer fluid cannot be joined by the word “coolant” alone. Preserve chemical identity and system boundaries before assigning any heat contribution.

## NIST's diesel exclusion: the consequential dependency

NCSTAR1-9 §9.2 tests selected hypothetical pool fires under prescribed rupture locations, ventilation and supply conditions. In Scenario1a, the model predicts high gas temperatures near Column79 under a sustained fire. NIST then reasons that heat affecting generators and/or distribution cables would interrupt electrical power to the fuel pumps within roughly one or two hours, cutting the sustained supply before significant predicted strength loss in the relevant column. That is an explicit causal chain worth auditing.[^2]

NIST does supply a structural-heating timescale: printed368, Figure9-3, describes a modeled W14×730 section with9/16-inch insulation under continuous1100°C exposure and approximately seven hours to a50% strength reduction. Its footnote identifies the reduced insulation thickness relative to the nominal7/8-inch value. This is a published model basis, not a measured historical temperature or a universal failure threshold. The unresolved verification concerns both its historical applicability and the equipment/power/shutdown chain; it is not an absence of any column heat-transfer calculation.[^2]

The reviewed passage does not itself provide an equipment-specific transient calculation connecting surrounding gas temperature to actual coolant/engine temperature, protective shutdown, cable failure and loss of every available pump-power path. Comparing gas temperature with a nominal coolant boiling threshold is not by itself that calculation. A check needs the cooling arrangement, fluid/pressure, heat-removal capacity, protective settings, exposure history, cable protection and actual electrical connections. This is a missing verification dependency, **not proof that the equipment could survive or that NIST's inferred shutdown was wrong**.

Stopping a pump and extinguishing a fire are also separate events. Scenario1a does give a steady-supply balance premise: its pool consumes fuel at the assumed pumping rate, with a prescribed area and regression rate. The remaining audit is whether that case's initial and residual pool inventory, drainage, burn rate and ventilation after interruption support the stated burn-out timing. An unspecified reserve cannot be assumed to sustain the fire; nor does a steady inflow/consumption balance alone measure the inventory remaining when supply stops. The required test is the retained time-resolved fuel/energy/equipment calculation using identified inputs, not a claim that NIST supplied no fuel-balance reasoning.

NIST does not dismiss every possible diesel fire on the ground that it would have been visually obvious. For its southwest scenario, printed372 explicitly recognizes that smoke and dust could obscure the fire and that nearby columns might weaken. Its rejection of that route to eastern initiation depends on the assumed compartment/path geometry. This is different from demonstrating no lower-floor heating anywhere.[^2]

Printed374 separately allows diesel to contribute to ignition/spread on Floors7/9 and, under specified supply conditions, a potentially significant south-Floor7 fire hidden within the south-side plume. NIST discounts those possibilities as contributors to the critical eastern structural failure; it does not say that all diesel ignition/spread effects were impossible. Retain this distinction when testing its decision not to model diesel explicitly.[^2]

These decisions have a documented downstream effect: printed374 initializes Floors5/6 at ambient temperature, with subsequent heating only by conduction from above, and omits diesel explicitly from the Floors7/9 fire simulations. Reproducing that modeled collapse therefore cannot independently validate the earlier exclusion that determined its thermal inputs. A discriminating sensitivity test would vary only documented, physically supportable lower-floor exposure histories and preserve both collapse and non-collapse results; no such run was performed here.[^2]

## Effect on the competing explanations

This audit makes the challenge more specific: original fuel accounting, pump survival, compartment integrity and thermal input selection are identifiable places where evidence could strengthen or weaken NIST's diesel exclusion. It does not establish that ordinary office fires were sufficient, that a diesel fire caused the collapse, or that deliberate intervention occurred. The current sources cannot supply the missing historical heat field or distinguish intent.

Neither a fuel inventory nor an alternative model's existence earns credit for an unverified initiating event. NIST's exact sequence and other fire-triggered pathways remain separate hypotheses; a failure of one exclusion or one initiation model does not automatically settle the others. The broader motion, acoustics, physical provenance and critical-review requirements of the charter remain open.

## Highest-value next records and tests

1. **Fuel accounting:** GZA GeoEnvironmental's *Underground Storage Tank Closure Report*, September9,2002, with tank IDs, recovery dates, measurements, uncertainty, photographs and disposal/transfer tickets; pre-event fill/gauge records. Resolve chronology and contents before calculating missing fuel.
2. **Actual equipment configuration:** NCSTAR1-1J's full equipment account and its original drawings/specifications; the April12,2002 Trammel Crow removal letter cited at NCSTAR1-9 printed52; dated modifications and pump controls. A later synthesis is not a substitute for these records.
3. **Power and shutdown:** relevant original Con Edison incident/alarm records, pump electrical schematics, generator cooling/protection specifications and operating records. Establish which power paths and protective devices were actually available before coupling fire and shutdown calculations.
4. **Reproducible §9.2 cases:** exact geometry/openings, ventilation, fuel inflow/pool/drainage histories, engine/cable thermal-failure assumptions and output histories. Check the fire-duration exclusion and its propagated floor-temperature boundary, including physically defensible contrary cases.
5. **Witness-source reconciliation:** the exact January2004 SSB interview and NIST engineering follow-up, preserving event time, vantage and direct observation versus mechanism attribution. Do not count retellings as independent support.

These are record/test specifications, not authority for outreach, fees, another FOIA request, sensitive transfer or litigation promotion.

## Sources

[^1]: 9/11 Commission staff memorandum of the January16,2004 interview, preserved three-page source (historical local reference `../warning-chain/sources/nara-catalano-mfr.pdf`; not included here), pp1–3; [NARA original](https://catalog.archives.gov/medialive/22/6097/2609722/content/arcmedia/9-11/MFR/t-0148-911MFR-00136.pdf). Staff summary, not a recording or engineering calculation. Prior full-page review and custody are preserved in the warning audit.
[^2]: NIST, NCSTAR1-9, preserved government report (historical local reference `../../../authority/nist/wtc7/ncstar-1-9.pdf`; not included here), printed52,60–63,295–296,366–374,614,645; physical96,104–107,339–340,432–440,680,711. Detailed selection and source pins are in `nist-source-review/`.
[^3]: NIST, NCSTAR1A, preserved government report (historical local reference `../../../authority/nist/wtc7/ncstar-1a.pdf`; not included here), printed11–12, physical53–54, including Table1-2 and its removal footnote. Repeats the same underlying equipment-source family; not independent corroboration of NCSTAR1-9.
