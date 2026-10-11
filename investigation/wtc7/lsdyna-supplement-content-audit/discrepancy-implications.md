# Discrepancy implications (investigation vs case)

2026-09-11; expanded the same day to all FOIA-released model files. Research only. Lookup IDs in the [released-file discrepancy index](../released-file-discrepancy-index/README.md). [CHARTER.md](../CHARTER.md) forbids converting an engineering mismatch into intent, fraud, or a named operation.

**Answer first:** the indexed mismatches **exacerbate already-identified sensitivity and testability problems**. They do **not** newly establish a conspiracy, a false official mechanism, or a FOIA completeness violation beyond the named-file and category-boundary questions in the index.

Old D1–D10 are aliases for DISC-001–010. June APDL/thermal/slides rows are DISC-011–023. The full-file Phase 1/2 sweep added DISC-024–028 (floor-tree split, 22AUG vs 15 Aug header, Case B `SLNo`, `mover`, Draft 2 vs APDL category). The second sweep added DISC-029 (Case B `1C137-2` is NULs) and corrected DISC-013/016 pins. Cause ranking is unchanged.

## Investigation track

Use counterfactual labels. The demanding hypothesis remains a concealed intentional operation. Model-file oddities are not that hypothesis.

If testing a concealment/intervention hypothesis against this index, emphasize three older findings, in this order. They are the strongest relevant facts in the set. They are still not that hypothesis.

1. **The handoff (DISC-004/005/017/018).** Strongest *technical* fact. The live deck is gravity. Damage is a later, commented deletion list with no residual-stress import. The 2008 slides already prescribe that. The published collapse path depends on an imposed later-stage deletion transfer. A conspiracy reading wants this to mean “they deleted the building.” It does not. It means the fire-to-failure chain is not independently replayable from these files, and the method was documented.
2. **The one-sided hour cut (DISC-001/007).** Strongest *sensitivity* fact. A 4.0-hour list arrived; the 3.5-hour control did not; the master names a 4.1-hour file that was not produced. The published collapse/no-collapse pair is still one-sided. A conspiracy reading wants this to mean they picked the hour that collapsed and hid the control. The files only show that the control was not in this package.
3. **The June omission, later acknowledged (DISC-016).** Strongest *production* fact. NIST said LS-DYNA inputs were included; the June extract had none; September sent six and said so. A conspiracy reading wants motive. The record shows an omission and a partial cure, not a concealment order.

Mention DISC-015/024 and DISC-013/026 only as follow-ups to (2): more places where a published variant exists without its twin. Do not use DISC-009 (penthouse), DISC-008/023 (hot unlabeled nodes), DISC-027 (mover), DISC-029 (NUL placeholder), or “they hid all connections” (DISC-006/019/028 cut the other way: geometry was released; specialized materials were not).

Even those three do not get to a conspiracy. They have no decision, no access, no residue, no command, and no independently identified device or actor. They make the official fire path harder to test and the FOIA production incomplete as to named files. That is already the claim ceiling. Crossing from “the control is missing” to “they made the building fall” is the inference the charter forbids, and the files do not support it.

| IDs | Role | What they advance |
|---|---|---|
| DISC-001, 003, 007, 011, 012, 016, 022, 025 | Compatible with incomplete production or ordinary versioning. Missing as concealment-with-intent | Named retrieval: 4.1hr, 3.5hr, July APDL copies, FL2–FL7 loads, ANSYS↔LS-DYNA thermal map, 15 Aug vs 22AUG ground-to-7 date |
| DISC-002, 013, 015, 024, 026, 027, 029 | Compatible with leftovers or documented case variants. Not discriminating | Ask what G6A set 1, Case B +10%, Fl07 on/off, thin Fl11/13 trees, `SLNo`/`mover`, and the NUL `1C137-2` placeholder mean before treating them as hidden cases |
| DISC-004, 005, 017, 018, 020, 021 | Compatible with staged numerical initialization. Not discriminating of intervention | SC02/SC03 are now in slides *and* keyword/APDL text |
| DISC-006, 019, 028 | Slightly contrary to “they hid all connection information” | Geometry and deletion lists were released; specialized materials/results were not. Draft 2’s “no connection models” label still does not match the inspectable APDL delete/copy steps |
| DISC-008, 023 | Not yet a discrepancy | Do not cite as overheating |
| DISC-009 | Compatible with a damaged penthouse state *or* with cueing penthouse motion | Sensitivity: retain those six beams |
| DISC-010, 014 | Compatible with the 2010 releasable-input story | Crosswalk, not forgery |

Nothing here is decision/command, operational access, residue, or a concealment order. Instantaneous “connection shell” deletion is a **model assumption** already flagged in the [claim-strain audit](../../nist-claim-strain-audit.md). Calling it “they deleted the building” is the misreading those memos rejected.

Cause ranking does not change. Fire-path underdetermination is sharper. Deliberate support removal is not newly evidenced.

## FOIA-case track

| Issue | Indexed rows | Do not say |
|---|---|---|
| Present nonreceipt of the six LS-DYNA inputs | DISC-016 historical only | That SRC-116–121 are still missing |
| Search / crosswalk / include-graph catch-all | DISC-001, 003, 007, 011, 012, 022, 025 | That a commented 4.1hr name proves a seventh June-2025 file |
| Readable Case B member | DISC-029 | That the NUL `1C137-2` member is spoliation |
| 2010 identity | DISC-010, 014, 026 | That the Sept bytes are the 2010 bytes, or that `SLNo` is a hidden fire case |
| Finding / Draft 2 / slides | DISC-006, 019, 028 | That connection information is entirely absent, or that the Finding is invalid |
| Segregability | DISC-006, 018, 019 | That released geometry makes every remaining file segregable |
| Results / other categories | DISC-004, 021 | That gravity-stage inputs moots results |
| June description | DISC-016 | Motive from the 4.1/4.0 or July/August label difference |

Case-useful ask: filename/path crosswalk for DISC-001, 003, 007, 010, 011, 012, 013, 014, 016, 022, 025, and 026; whether a non-null agency original of DISC-029 exists; identify-or-produce live include/input names from the six LS-DYNA files and three APDL files, plus the specifically named commented companions (`4.1hr`, LS-DYNA `WTC7-1.int`); map withheld “connection material properties” onto cards **not** already in the `no-conn-matl` deck. Leave DISC-027 (`mover`) and floor-tree / `SLNo` / penthouse / hot-node rows off the complaint. Do not demand a repaired NUL file or a comment search of the thermal archive.

## Which older assumption findings get worse

| Prior finding | Rows that instantiate it | Effect |
|---|---|---|
| Instantaneous ANSYS→LS-DYNA transfer | DISC-004, 005, 017, 018 | Exacerbated. Slides and the Sept deck now say the same thing in two formats |
| Thin 3.5 / 4.0-hour threshold | DISC-001, 007 | Exacerbated. One list arrived; control did not; a 4.1hr name appeared |
| Connection rules not independently testable | DISC-006, 019 | Partly narrowed (geometry), partly sharpened (materials still withheld) |
| Slides about component removal / restarts | DISC-017, 018, 020 | Exacerbated. Matching APDL/LS-DYNA objects exist |
| Floor 11/13 fire substitutions | DISC-015, 013, 022, 024, 026 | More inspectable. All 12 A/B hour drivers pull Fl11/13 and drop Fl07; Fl11/13 are Core/SLAB-only trees; Case B adds a live `SLNo` class. Not quantified |
| Video/model exterior divergence | — | Unchanged. No results |
| Floor 5 / substation idealizations | DISC-021 | Illustrated. Released ANSYS file is a gravity deck |
| “All supports vanished together” | DISC-005, 009 | Not exacerbated. Lists are regional |

Strongest upgraded statement:

> NIST’s published path still depends on a lumped later-stage deletion transfer and a narrow hour cut. The released slides already prescribed that transfer; the Sept deck shows it as unused countable input; the June APDL/thermal trees have the same include-name / variant-label pattern. That makes the old sensitivity findings more specific. It does not show that deletions were invented to force collapse or that an operation occurred.

## Claim ceiling

| Claim | Grade |
|---|---|
| DISC-001–007, 009, 011–013, 015–018, 020, 022, 024–027, 029 exist as file text or archive names | A |
| They make prior handoff and threshold findings more concrete | B |
| They identify named files still not in this package | B |
| They prove NIST chose 4.0 hours or +10% in order to obtain collapse | E |
| They prove a conspiracy, cover-up, or demolition | E |
| They prove the FOIA production is complete or remaining withholdings are invalid | E |
