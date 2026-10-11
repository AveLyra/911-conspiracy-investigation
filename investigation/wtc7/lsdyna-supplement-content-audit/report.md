# What the September 11 LS-DYNA files convey

2026-09-11. Research only. This memo interprets the six keyword-format inputs released with [SRC-115](../../../intake/source-inventory.csv) (`SRC-116`–`SRC-121`). It does not execute LS-DYNA, authenticate historical-byte identity with the 2010 release, promote complaint facts, or rank collapse causes. [CHARTER.md](../CHARTER.md) controls scope. The files remain preserved under `exhibits/raw/`; this audit streamed gzip text and wrote only local derivatives here.

The six files are a **WTC 7 global-model input package**, not results and not a self-running collapse case. The master deck is titled `LSDYNA Model of WTC-7` and is named `wtc7_global_8a_no-conn-matl`. As currently configured it would apply gravity and stop at 4.50 seconds. The Case B 4:00 p.m. thermal field is included but scheduled to start later. The ANSYS damage/deletion step is present as companion lists and as commented hooks, not as an active include.

## File roles

| File / SRC | Observed contents | Inferred role | Wired into the active deck? |
|---|---|---|---|
| `wtc7_global_8a_no-conn-matl.k.gz` / SRC-121 | Title, controls, ~3.59 million nodes, ~1.93 million fire-zone/slab shells, 3,190 beams, 33,364 discrete elements, 59 curves, contacts, rigid wall, 280 parts | Master 47-story deck | Master |
| `elem_thick_to-renum.k.gz` / SRC-120 | 4,085,686 `*ELEMENT_SHELL_THICKNESS` rows; comment “Shell Elements outside fire zone”; 175 `*MAT_PIECEWISE_LINEAR_PLASTICITY` parts | Outside-fire-zone shell geometry and bulk materials, included with part/material/section ID offset 1000 | Yes, `*INCLUDE_TRANSFORM` |
| `discrete_mass.k.gz` / SRC-119 | 5,366 nodes, 2,461 solids, four rigid parts: `7th floor mass1/2`, `46th floor cooling towers`, `46th floor water tank` | Lumped floor/roof equipment masses | Yes, `*INCLUDE` |
| `WTC7_CaseB_400pm.int.gz` / SRC-118 | 870,201 `*LOAD_THERMAL_VARIABLE_NODE` rows; all use load curve 2 | Spatially varying Case B 4:00 p.m. nodal temperatures | Yes, `*INCLUDE` |
| `Damage_Global_ANSYS_CaseB_4.0hr.k.gz` / SRC-116 | Set 2: 1,543 shells and 361 beams, labeled connection shells, buckled-beam shells, connection beams, and “Beams to decouple E&W Penthouse” | ANSYS 4.0-hour Case B damage/deletion list | No. A commented include names a **4.1-hour** file instead |
| `G6A_CaseA_El_Delete_List.k.gz` / SRC-117 | Set 1: 45,152 unlabeled shell IDs | A second deletion list; filename says Case A | No. Not named in the master include block |

Reproducible counts and hashes are in [inventory.json](inventory.json) and [focus.json](focus.json). All six gzip streams reached EOF under the 512 MiB cap. Uncompressed totals match the earlier integrity audit: about 603 million bytes. No model was run.

## What the assembled deck is doing

The master file actively includes three supplied companions and no others:

1. `elem_thick_to-renum.k`
2. `discrete_mass.k`
3. `WTC7_CaseB_400pm.int`

A commented alternate thermal filename, `WTC7-1.int`, is not in the package. Immediately after the thermal include, the deck says “Incorporate ANSYS Damage” and then comments out `*INCLUDE` of `Damage_Global_ANSYS_CaseB_4.1hr.k` plus `*DELETE_ELEMENT_SHELL` / `*DELETE_ELEMENT_BEAM` against **set 2**. Set 2 is exactly what the supplied 4.0-hour damage file defines. The 4.1-hour file named in that comment is not supplied.

### Active run window

`*CONTROL_TERMINATION` is `4.50` seconds. Two commented alternatives sit above it: `20.0` and `8.501`.

Curve 1 is labeled “Gravity Curve.” Its scale factor is 4.0 on a 0–1 ramp, then a hold at 100. Gravity therefore rises over 0–4 seconds and stays on. `*LOAD_BODY_Z` applies 9.81 to that curve. This matches the public NCSTAR initialization: gravity over 0–4.5 s ([structural-chain pin SC02](../structural-chain-source-audit.md)).

Curve 2, which every thermal node references, has time offset 6.5 and a 0–2 second ramp, then a hold. Temperatures are scheduled for 6.5–8.5 s. That also matches SC02. It is **after** the active 4.50 s termination. If this deck were executed exactly as written, the thermal include would be present but would not yet change temperatures, and the ANSYS damage include would not run.

`*DATABASE_BINARY_D3DUMP` / `RUNRSF` cards are present, so a staged restart is technically provided for. This audit did not find `*INITIAL_STRESS`, `*STRESS_INITIALIZATION`, or an active `*DEFINE_ELEMENT_DEATH` card. Residual ANSYS stress/strain state is not in these six files as an initial-condition deck.

### Geometry and materials

The master is a large explicit-dynamics building model in SI-like units (meters, 9.81 m/s², 25 as ambient). It contains:

- a ground rigid wall and a `substation-rigid` part
- composite concrete decking
- temperature-dependent `*MAT_ELASTIC_VISCOPLASTIC_THERMAL` (13 cards) for fire-zone steels
- bulk `*MAT_PIECEWISE_LINEAR_PLASTICITY` (MAT 24) elsewhere, including the outside-fire-zone include
- 56 nonlinear spring materials and 33,364 discrete elements
- fifth-floor WT slab beams, penthouse beams, and many W14 x-bracing beam parts
- 83 column cross-section database planes, including one titled `All Columns X-Sect`

The filename `no-conn-matl` is consistent with specialized connection-failure materials having been replaced by bulk MAT 24. It is **not** a model without connection geometry. Both the master and the thickness include still name parts such as `3 Bolt Shear Connection` through `9 Bolt Shear Connection` and `Algoma 44W bearing & seat plate steel`. That is the Draft 2 / 2009-finding distinction: releasable inputs with connection material models removed, not a model that omits seats, bolts, or plates.

### Thermal field

`WTC7_CaseB_400pm.int` is a node-by-node Case B 4:00 p.m. temperature assignment, not a single building-wide number.

| Quantity | Value |
|---|---:|
| Nodal assignments | 870,201 |
| Load curve | 2 on every row |
| Base temperature | 0.00 on every row |
| Assigned TS minimum | 25.0 |
| Assigned TS maximum | 735.6 |
| TS ≤ 25.01 | 194,075 |
| TS > 100 | 374,708 |
| TS > 200 | 198,633 |
| TS > 300 | 114,523 |

These are input temperatures, not solved steel temperatures and not column-only values. NCSTAR’s statement that initiating **column** temperatures were below 300 °C is not tested here; this file does not label which nodes are columns. The 25 °C-wide histogram in `focus.json` is the reproducible summary. Do not use the earlier unique-count field in `inventory.json` (it over-counts after 500 distinct samples).

### Damage and deletion lists

`Damage_Global_ANSYS_CaseB_4.0hr.k` is a compact handoff list, not a mesh:

| Comment label | Set | Count |
|---|---:|---:|
| Connection shell elements | shell 2 | 243 |
| Buckled beam shell elements | shell 2 | 1,300 |
| Connection beam elements | beam 2 | 355 |
| Beams to decouple E&W Penthouse | beam 2 | 6 |

That labeling matches the public description of ANSYS-to-LS-DYNA transfer by element deletion and coarse connection mapping (SC03). The file does not itself say when it should be applied. The master comments place that application after the thermal include and point the delete cards at set 2.

`G6A_CaseA_El_Delete_List.k` is an order of magnitude larger (45,152 shells) and has **no** explanatory comments. It is not referenced by the master’s commented delete cards, which use set 2. The filename can be read as a Case A list, a mesh-region name, or an impact-damage list. None of those readings is established by the file body.

Twelve commented beam cards in the master use part ID 79. That is a local commented edit, not evidence that Column 79 was removed from the live mesh.

## What the files do not convey

- A complete, currently runnable collapse simulation. Active termination ends at gravity. Damage include is commented and names a missing 4.1-hour filename. No results (`d3plot` or equivalent) were produced here or supplied in this package.
- The 3.5-hour non-collapse control (SC10). That paired damage state is still absent.
- Specialized connection material models, break-element source, or a custom executable.
- Residual stress/velocity/energy from the 16-story ANSYS run. Only deletion ID lists are present.
- Proof that these bytes are the six 2010 Case B Impact releases. The count is six, the category matches “inputs without connection details,” and the names fit that description. Historical-byte identity is unproven.
- Proof that NIST’s published collapse sequence is correct, incorrect, or intentionally tuned. A deletion list is a modeling choice that can now be inspected; it is not a demonstration of what happened in the building.
- A FOIA completeness finding. Receiving these six files confirms they now exist locally. It does not identify every other requested category or reconcile the 2010/2025 counts.

## Claim ledger

| Claim | Type | Support | Best alternative | Falsifier | Grade |
|---|---|---|---|---|---|
| The six files are LS-DYNA keyword inputs for a WTC 7 global model | Observation | `*TITLE` `LSDYNA Model of WTC-7`; keyword inventory; hashes in SRC-116–121 | Misnamed non-solver text | Absence of `*KEYWORD` / `*END` or a different title | A |
| The live assembly is master + thickness + mass + Case B 4:00 p.m. thermal | Observation | Active `*INCLUDE` / `*INCLUDE_TRANSFORM` names, all supplied | Additional runtime files outside the deck | A different include graph in another released deck | A |
| As written, the deck would stop at 4.50 s, after gravity and before the 6.5–8.5 s thermal ramp | Derived from cards | `*CONTROL_TERMINATION` 4.50; gravity curve 1; thermal curve 2 offset 6.5 | Operators overrode termination at run time; this file is only stage 1 of a restart series | A companion restart deck or run log using 8.501 / 20.0 | A for the text; C for how NIST actually ran it |
| The 4.0-hour file is an ANSYS Case B damage/deletion list | Inference from filename + comments + set IDs | Set 2; connection/buckled/penthouse labels; master comment “Incorporate ANSYS Damage” | A leftover list from another case | A NIST crosswalk assigning it a different function | B |
| `no-conn-matl` means specialized connection materials were replaced by bulk MAT 24, not that connections were omitted | Inference | Filename; 175/125 MAT 24 cards; surviving bolt/seat part names; Draft 2 wording | The named parts are unused labels | A material-card audit showing live specialized connection-failure models | B |
| These are the six 2010 Case B Impact releases | Hypothesis | Count of six; category match to Fletcher ¶36 / EXH-014 | A later or different six-file subset | A filename/hash crosswalk from the 2010 production | D |
| `G6A_CaseA_El_Delete_List` is WTC 1 impact-damage removal | Hypothesis | Filename; Fletcher’s debris-impact step at 4.5 s | Case A fire list, mesh-region extract, or unused leftover | A comment, include, or agency map tying set 1 to impact | D |
| This package can reproduce NCSTAR’s collapse figures | Unsupported | No | It is a gravity-stage input plus unused later hooks | Native results, solver/version, and an activated 4.0/4.1-hour handoff | E |

## Relation to the public report and the FOIA record

The cards that *are* active line up with the first NCSTAR initialization step: gravity, a rigid base/substation idealization, and a prepared but later thermal curve. The cards that are *commented* line up with the later handoff: include an ANSYS damage file, then delete shell and beam set 2. That is useful because it makes SC02/SC03 inspectable as input text rather than only as prose.

It also bounds what this production is. Fletcher’s 2010 declaration said six Case B Impact **inputs** were released and that withheld inputs were those with connection material properties, plus all results (EXH-014 ¶¶34–36). These files look like that releasable class. They do not look like the withheld results, the 3.5-hour control, or a connection-material deck.

Two internal mismatches should stay visible rather than being smoothed:

1. The master comments a **4.1-hour** damage filename; the supplied file is **4.0-hour**. Set IDs match, names do not.
2. A **Case A** deletion list is packaged with Case B thermal/damage files and is unused by the master’s commented hooks.

Neither mismatch proves a defective search or an altered model. Both are reasons to ask for a filename/path crosswalk rather than to treat the package as a closed reproduction set.

## Highest-value next checks

1. **Member map, not a solver run.** Join set-2 IDs and high-TS nodes to part titles / cross-section planes before claiming which floors, seats, or columns are deleted or heated. The penthouse-decoupling comment is already specific enough to test against NCSTAR’s penthouse timing.
2. **Agency crosswalk.** Ask whether these six files are the 2010 Case B Impact releases; where `Damage_Global_ANSYS_CaseB_4.1hr.k`, `WTC7-1.int`, and the 3.5-hour damage list sit; and whether `G6A_CaseA_El_Delete_List` is impact damage, Case A, or unused.
3. **Do not execute the model** as intake or as a causal test. A later executable protocol would need an explicit termination/restart choice, the missing or substituted damage file, solver version, and a plan that treats comments as data. That is a separate approval.

Indexed IDs: [released-file discrepancy index](../released-file-discrepancy-index/README.md) (`DISC-001`–`DISC-028`). Investigation and case implications: [discrepancy-implications.md](discrepancy-implications.md).

No source, exhibit, fact, timeline, pleading, or outbound message was changed by this audit.
