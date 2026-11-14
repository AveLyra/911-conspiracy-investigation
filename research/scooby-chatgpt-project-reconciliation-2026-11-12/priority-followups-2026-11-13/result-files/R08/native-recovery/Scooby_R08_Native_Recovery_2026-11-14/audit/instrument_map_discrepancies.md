# Corrected native instrument map: joins, conflicts, and limits

## Scope and reproduction

`corrected_instrument_map.csv` contains **1,398 header occurrences across nine measurement sheets**: 1,365 sensor-named columns, 18 time-coordinate columns, and 15 formula-based summary columns. These are not 1,398 unique sensors. The same fire specimen has distinct ambient-loading and fire-loading sheets. CB-DA-AMB is a separate baseline specimen.

The audit reads original ZIP/XML without opening and saving a workbook. Every mapped row retains the original header text, unit text, exact sheet/cell, original local and drawings dictionary descriptions, scaled units, ranges, types, source URLs, and source hashes. The explicitly derived join operation removes the trailing parenthesized unit and trims surrounding legend whitespace. It does not remove hyphens, merge ambient/fire specimens, or convert measurement values. Formula presence, formula text/attributes, and cached raw values from row 2 are separate fields; full-sheet formula/cache inspection belongs to the native inventory.

Reproduce with `build_channel_crosswalk.py --native-dir PATH --retrieval-manifest PATH --output-dir PATH`. The retrieval manifest is the direct GET attempts array. The script does not edit native XLSX files.

## Vertical displacement: labels established, descriptions conflict

The native fire sheets use **VD2–VD5**, not VD1–VD4. For CB-DA they occupy `CB-DA-FireLoadingData!IK1:IN1`; corresponding definitions occupy `Channel List!A243:G246` and `drawings.xlsx / Channel List-FireTests!A267:K270`.

Both dictionaries assign, successively, Mid Span / West / Mid West / Mid East descriptions. Those descriptions conflict with the original fire layout Figure C1 (`xl/media/image12.emf`, caption `InstrumentationLayout-FireTests!B32`), visually reviewed by the root agent, which places VD2/3/4/5 west-to-east at the outer/inner/inner/outer slab points. TN 2055 Table 13, printed p.70, agrees with that ordering. Its §2.4 p.23 phrase VD1–VD4 is not the native header sequence.

| Channel | Native diagram dimension expression, inches | Derived distance, cm | Published Table 13 distance, cm |
|---|---:|---:|---:|
| VD2 | 132 | 335.28 | 336 |
| VD3 | 132 + 84 | 548.64 | 548 |
| VD4 | 504 − 132 − 84 | 731.52 | 732 |
| VD5 | 504 − 132 | 944.88 | 944 |

The derived distances use 2.54 cm/in. They are not worksheet measurements. Keep the diagram's **west drawing datum** separate from Table 13's **west-column centerline**: datum equivalence has not been established. Do not silently round one set into the other. The CSV therefore retains the conflicting dictionary descriptions while adding a separate diagram-supported provisional spatial interpretation.

CB-DA's native summary formula independently preserves its selected middle pair: `JM2 = AVERAGE(IL2,IM2)`, i.e. VD3 and VD4. This is a workbook formula, not a newly calculated measurement.

The baseline workbook instead contains **VD1–VD6** at `CB-DA-AMB Data!BE1:BJ1`. Drawings ambient rows 82–87 distinguish beam-midspan VD1, slab-midspan VD2, and outer/inner west/east slab VD3–VD6. These cannot be renamed into the fire sequence by shared suffix alone.

## Rotations and units

The ambient dictionary describes RotLT1/2/3 as west/middle/east (`Channel List-AmbientTest!A97:B99`). The fire dictionary reverses the outer descriptions: east/middle/west (`Channel List-FireTests!A275:B277`), and the specimen dictionaries inherit that reversal. Original drawings B1(f) (`image11.emf`) and C6(b) (`image19.emf`), visually checked by the root agent, support **RotLT1 west, RotLT2 middle, RotLT3 east**. The CSV retains both the original text and that provisional diagram-based correction.

All **75 rotation header occurrences state rad**. No rad-versus-deg header mismatch was observed in these nine measurement sheets. Ambient CB-DA-AMB actuator headers `BW1:CH1` use **in/kip**, matching its dictionaries; fire-specimen actuator channels use **mm/kN**, including their ambient-loading stages. No conversion was performed. Ambient `µmm/mm` headers versus dictionary `microstrain` are retained as a notation difference, not a numerical discrepancy.

## Specimen-dependent temperature descriptions and usage flags

The generic drawings fire list is not an adequate universal channel dictionary. For example, CB-DA `TCE_4` at `AG1` is defined by its local `Channel List!A37:B37` as an angle-leg/top-bolt location; the generic list `A36:B36` describes a shear-tab location. Analogous TCW/TCE differences require the specimen's connection type to remain explicit.

Some differences are actual location conflicts. CB-DA `TC6_26` (`DB1`) is North in local `A110:B110` but South in drawings `A122:B122`; `TC4_13` (`HG1`) is Mid Web locally (`A219:B219`) but Top Web in drawings (`A240:B240`). CB-DA-SC STC1 is 7.25 in east of Section 2 locally (`A243:B243`) versus 5.75 in west in drawings (`A191:B191`); other STC offsets differ too. These remain unresolved for precise thermal mapping.

There are **28 header occurrences with blank specimen X flags** in the drawings matrix: CB-DA 18, CB-DA-SC 7, CB-SP 3, CB-SP-SC 0. A blank X does not erase an observed measurement column or prove missing data. Four drawings channels marked X lack any matching header in their specimen workbook: CB-DA-SC TC7_14 and TC5_15; CB-SP TC2_12 and TC2_14. CB-DA's local list additionally contains TC4_20 (`B229`) without a measurement-sheet header. Full lists are in `instrument_map_dictionary_channels_without_headers.json` and `instrument_map_definition_discrepancies.json`.

Root's visual review also found a duplicated TCC1 label in Figure C4(a) (`image16.emf`): the southeast elevated location is TCC13 in C4(b). The crosswalk flags this diagram disagreement without renaming a measured header.

## Unjoined channels and native derived results

**41 headers do not join the local dictionary:** 18 time fields, 15 native formula summaries, and eight sensor-named auxiliary temperatures. The latter are CB-DA's `HY1:IE1` (ColW_TT, ColW_TB, ColW_BT, WaterTempSW, RotWTemp, ColWTop1, ColWTop2) and CB-DA-SC's `IC1` (RotMTemp). Their names and units are observed, but precise physical locations are not supplied by either inspected channel list. Do not infer the locations from abbreviations alone.

**102 headers do not join the generic drawings list:** the same 33 time/summary columns plus 69 sensor-header occurrences, including specimen-specific channels that do have local dictionary entries. `instrument_map_unjoined_channels.json` makes those cases explicit.

CB-DA `AvgAxialLoad` is a native calculated result, not a connection load-cell channel. In `CB-DA-FireLoadingData!JN2`, the formula is:

```text
AVERAGE(F2,G2,H2,I2,J2,K2,L2,P2,Q2,R2,S2,T2,U2,V2)*3.9
```

This selects fourteen brace-strain channels and excludes ColW1 (`E1`) and ColE1 (`O1`). The unmodified formula/cache record is evidence of the workbook's computation, not proof of the calibration's sufficiency. Publication uncertainty and the force-to-strain factor remain separately sourced; dictionary ranges are not calibration certificates.

## Reading the discrepancy count

The automatic raw comparison lists **1,047 header occurrences with differing definition fields**, mostly vocabulary changes such as *Strain gauge* versus *Quarter bridge*. Of those, 888 differ only in instrument type, 143 in description and type, 12 in group and type, and four in description/group/type. These counts are not 1,047 substantive errors. No literal header-unit versus local/drawings-unit mismatch was found apart from the separately labeled microstrain notation difference.

The recovery establishes inspectable channel evidence. It does not by itself validate calibration, locate every thermocouple, settle all geometry datums, or authorize a numerical model.

## Publication uncertainty companion

`published_uncertainty_map.csv` adds 26 separately classified publication records, verified against the recovered official PDFs. It preserves combined standard versus expanded uncertainty (k=2), absolute versus percentage units, operating conditions, non-assigned quantities, and two published SD landmarks. Every row explicitly states **publication only; not per-cell native uncertainty/calibration**. No values were attached to native samples.

The rotation budget is **9% expanded at 25°C** and **29% within -40°C to 85°C**; 29% does not validate failed or overheated sensors. TN 2054 §4.5, printed p.78, and Table 4-3 p.81 supply that distinction. TN 2055 Table 4 p.26 excludes steel-thermocouple insulation failure and dislodging from its budget. Its Table 5 **106.1 ± 0.1 kN** is a maintained-load mean and temporal SD; Table 12 **716 ± 85 kN** is an inferred peak and dispersion among brace-based estimates. Neither ± value is the complete measurement uncertainty.

The map's `phase` field follows the worksheet designation. It does not assert non-overlapping recording intervals: the separate native inventory found CB-SP-SC preload-sheet annotations marking the fire data-file start and the last record before ignition. Event/timestamp alignment must remain explicit before analysis.
