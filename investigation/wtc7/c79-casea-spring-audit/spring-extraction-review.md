# Independent selected-spring numeric extraction

September 13, 2026. Arm B; research-only. This is an independently authored
numeric source reader, not a solver or physical validation. The source-of-truth,
evidence-audit and development-verification safeguards limited the work to the
declared isolated unit, typed provenance and tested create-only artifacts.

## Independence and frozen artifacts

The complete protocol was read under SHA256
`b616114713bdfb20765bc033adc12d38cf888ae95704a41c17f705c3e791ea41`, with current
main AGENTS/WORKFLOW/START-HERE and the investigation charter. Prior candidate
IDs and material keyword types were known. The fixed contact-damage selection
was read only for its selected typed identities and membership lineage; the
new Case A result, parent reader/result, and old material inventory were not
consulted before this source extraction froze. The new reader imports no other
investigation reader. The independent manual arm communicated card layouts,
without model values, before the extraction. Its complete review was read after
this extraction froze; this arm does not claim to have visually inspected those
manual pages itself.

| Artifact | SHA256 | Actual disposition |
|---|---|---|
| `independent_springs.py` | `e816725d3cbd6bf919dac8809559d993c3b89551b8f70165dd48d536468432ca` | Frozen before historical source evaluation |
| `independent-springs-controls01.json` | `5f0b07171ff02e4bffcc212916545b3587189bf0fc33551080cd605901aaf12a` | All 12 synthetic groups passed before source evaluation |
| `independent-springs01.json` | `0940e45f99999bb69bac8ee898c47dd967baae03a134a83be62fedd425520116` | Passed complete extraction; 6.808667 s, peak RSS 32,391,168 bytes on macOS |
| Fixed `../c79-contact-geometry/contact-damage01.json` | `e43d8922c511debb4a004f6342fbdb8c16e76ff26cdb306fbd161c77a536d479` | 51 selected setting-specific rows reconcile to 17 typed discrete element identities |

There was no failed historical extraction or failed controls receipt. One
initial file-creation tool request timed out during automatic permission review;
no file was created. A single retry succeeded. An initial read-only selection
inspection used the main checkout instead of the worktree and returned a
file-not-found error; rerunning at the correct worktree succeeded. Neither
event is a failed model calculation or evidence about the source.

Actual commands, from `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`:

```text
python3 research/sherlock-wtc7-investigation/c79-casea-spring-audit/independent_springs.py --controls-only --output research/sherlock-wtc7-investigation/c79-casea-spring-audit/independent-springs-controls01.json
python3 research/sherlock-wtc7-investigation/c79-casea-spring-audit/independent_springs.py --output research/sherlock-wtc7-investigation/c79-casea-spring-audit/independent-springs01.json
```

## Full-stream source coverage

The compressed originals were read in place as data. Each stream reached EOF;
uncompressed hash, byte count and physical-line count matched the admitted pins.
Compressed hashes were checked before and after each stream. Protocol/selection
pins were checked before and after the historical extraction. Limits were
512 MiB uncompressed per source and 16 KiB per physical line; nothing was
truncated. No raw plaintext source copy, arbitrary comment/title, executable
input action or external transmission was produced. Selected title lines are
represented only by hashes and line locators.

| Source | Compressed bytes / SHA256 | Uncompressed bytes / lines / SHA256 |
|---|---|---|
| SRC119 `discrete_mass.k.gz` | 70,199 / `2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7` | 508,372 / 7,905 / `8e1c2c5e101ed133411acd905079fb128579ab48a591b508b8e9883fc7038601` |
| SRC120 `elem_thick_to-renum.k.gz` | 23,162,693 / `c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59` | 232,959,541 / 4,088,491 / `7ac5918eb9eb2368cffc84aeef29fb104314115cda5baab2a0b93788b46abfda` |
| SRC121 `wtc7_global_8a_no-conn-matl.k.gz` | 47,520,888 / `f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d` | 333,947,423 / 7,196,443 / `8a00ca2ba51912837ff8960cdef2977d9cf4de3a7d2b13d8a4336c66ef5e4bbf` |

SRC120's prospective +1000 transform applies only to PART/MAT/SECTION IDs;
node, element and curve IDs are not shifted. The reader applies and tests that
declared transform but does not freshly interpret INCLUDE_TRANSFORM cards.
Every selected chain here is in SRC121, with original IDs equal to effective
IDs. No physical part/floor/member name is assigned from an identifier.

The reader internally inventories all 33,364 discrete rows, 459 base PART
blocks, 56 SECTION_DISCRETE blocks, 56 MAT_SPRING_NONLINEAR_ELASTIC blocks and
59 admitted DEFINE_CURVE blocks; it encountered no admitted
DEFINE_SD_ORIENTATION block. These are keyword-specific inventory counts, not
counts of all material/section types. Complete curves were retained internally
until EOF to avoid reference-order assumptions. Output exposes only the selected
chains, their selected-element cards, full selected-PID membership identities,
and inventory counts. Numeric lexemes and values preserve nulls versus explicit
zeros; all selected cards and their physical source lines are in the frozen JSON.

## Positive cards and bounded missing dependencies

All following locators are one-based physical lines in SRC121. `null` means a
blank field in the parsed card, not an applied solver default.

| Effective PID | Selected / full discrete population | PART card | SECTION cards | MAT card | MAT card numeric fields |
|---|---:|---:|---|---:|---|
| 820 | 7 / 991 | 7,162,741 | 7,162,737–738 | 7,162,735 | `[820,602,0,null,null,null,null,null]` |
| 821 | 7 / 991 | 7,162,749 | 7,162,745–746 | 7,162,743 | `[821,602,0,null,null,null,null,null]` |
| 859 | 3 / 84 | 7,163,053 | 7,163,049–050 | 7,163,047 | `[859,803,0,null,null,null,null,null]` |

Each PART card is `[PID,PID,PID,null,null,null,null,null]`. Each SECTION first
card is `[PID,0,0.0,0.0,0.0,0.0,null,null]`; its second card is
`[0.0,0.0,null,null,null,null,null,null]`. These positive supplied definitions
disconfirm a blanket assertion that those three material cards or sections
are missing. They do not establish complete constitutive dependencies.

Selected discrete EIDs and source lines:

- PID820: 11343@7174400, 11344@7174401, 11395@7174452,
  11396@7174453, 11447@7174504, 11448@7174505, 11499@7174556.
- PID821: 12334@7175391, 12335@7175392, 12386@7175443,
  12387@7175444, 12438@7175495, 12439@7175496, 12490@7175547.
- PID859: 33293@7196350, 33295@7196352, 33297@7196354.

The JSON preserves all eight discrete numeric fields, both endpoint IDs,
keyword/card lines and matched-node/source-list lineage. All 17 selected cards
have field5=0, field7=0 and field8=0.0. Field6=1.0 for the 14 selected
PID820/821 cards and 0.5 for the three selected PID859 cards. Under the separate
manual mapping these are VID, PF, OFFSET and S respectively; this is not a
force or stiffness calculation. No selected nonzero VID triggers an orientation
or orientation-node dependency. The selection is not the full part population.

Material first-card field2 references 602 for PID820/821 and 803 for PID859.
Neither ID is present in the complete admitted DEFINE_CURVE registry. Field3
is an explicit zero on each material card, not a missing requested curve.
Consequently there are **no selected supplied curve headers/points to transform
or evaluate in this extraction**. This is a bounded missing dependency within
SRC119–121's admitted DEFINE_CURVE blocks, not proof that a historical run had
no such curve, a solver would assign zero force, the model had zero capacity,
or any input was deliberately omitted.

The manual review notes that DEFINE_TABLE shares a reference ID space with
DEFINE_CURVE. This frozen reader did not inventory DEFINE_TABLE or another
alternative consumer syntax. Until that separate keyword/dependency closure is
verified, its result must not be promoted from “no admitted DEFINE_CURVE602/803”
to “no applicable table/function anywhere.” The files outside the fixed source
boundary, actual include/run state, build-specific handling and solver output
are also not authenticated here.

## Tests, inference ceiling and remaining checks

The 12 pre-source synthetic groups cover fixed/comma blanks and explicit zeros;
validated numeric lexemes including D/implicit exponents; rejection of nonnumeric
payload and nonblank overflow; forward/backward/missing/zero/blank curve links;
title hashing and EOF digests; duplicate curve IDs; namespace transforms;
mixed-width discrete fields, ground zero and line/endpoint lineage; rejecting
orientation-only endpoint matches; duplicate discrete IDs; unsupported curve
variants; line caps; and changed pins/create-only output refusal. No unsupported
selected syntax was silently defaulted. The stream cannot establish a global
absence of every keyword family it does not parse.

This arm establishes a reproducible numeric source-card account and preserves
the strongest positive and negative information together: supplied PART,
SECTION and spring-material cards; a strict subset of each part's elements;
explicit field values; and unresolved selected curve IDs in the admitted curve
registry. It does not compute law arithmetic, assign units or physical axes,
validate support directions, activate any list/contact, reconstruct time/state,
or authenticate historical execution. The root's independent complete common-
field comparison, dependency-syntax closure and report integration remain
separate acceptance checks; no pending check is certified from a filename.
