# Exact candidate-to-part dependency summary

September 13, 2026. Post-result descriptive arithmetic over the frozen,
previously verified exact-proximity and stage arrays. This is not a prospective
claim about the original selection, an independent new source reconstruction,
a physical member identification or a contact/restraint calculation. The unit
protocol, exact-arithmetic addendum and investigation charter control.

## Result and overlap reconciliation

The summary retains all 18 combinations of three settings, two CIDs and classes
0/2/3, including every zero group. Across those selected classes there are
**406 unique slave nodes and 14 typed incident parts**. Repeated appearances
under the three settings are not new physical samples. The selected
`(master index, node ID, class)` membership is the same at all three settings.

The following counts apply separately at each setting:

| CID | Class | Node-master relations | Unique slave nodes | Distinct master records |
|---|---|---:|---:|---:|
| 1 | 0: unknown thickness | 2,840 | 4 | 710 |
| 1 | 2: unresolved gate | 0 | 0 | 0 |
| 1 | 3: inside low scenario gate | 288 | 122 | 174 |
| 2 | 0 | 0 | 0 | 0 |
| 2 | 2 | 0 | 0 | 0 |
| 2 | 3 | 608 | 280 | 32 |

The selected groups have no shared nodes between CIDs or selected classes at
the same setting: their union is 406, including 402 class-3 nodes and four
class-0 nodes. Nevertheless, **28 selected nodes also have a class-1 outside
relation to another master record**. A node is not globally “inside” or
“outside” independently of the master being tested. The output retains those
class-1 overlaps even though class 1 is not a selected summary group.

CID1's 122 class-3 nodes have 153 typed-part memberships; 31 nodes have more
than one typed incident part. Thus the part counts below must not be summed
as distinct nodes. CID2's class-3 group has 280 typed-part memberships and
280 unique nodes. The output explicitly records every pairwise CID/class
overlap, including zero intersections, and every group's zero entries for
the complete selected typed-part universe.

Across all settings the selected classes contain 11,208 relation rows out of
the exact diagnostic's 11,292 admitted rows. The remaining 84 rows are class 1
(28 per setting), not omitted source records or failures. Relation rows refer
to ordered master records; duplicate geometric faces are not silently merged.

## Part and property dependencies

All 14 selected parts have PART and SECTION definitions marked present in
the frozen registry. Twelve have a material keyword recorded; two have an
absent material-definition lookup. These are the registry's statuses, not a
new search of the raw decks or a certification of complete constitutive data.

Each table node count is a distinct-node count for that typed part across the
selected settings/CIDs/classes. Overlap across rows is retained in the JSON.
The source locator is the PART-card source ID and line, not a material-card
locator. IDs are effective IDs unless an original PID is separately shown.

| Typed part | Original PID | Selected unique nodes | CID/class | SID | MID | Material lookup | PART source:line |
|---|---:|---:|---|---:|---:|---|---|
| Shell 11 | 11 | 70 | 1/3 | 11 | 11 | Present | SRC121:2178 |
| Shell 12 | 12 | 280 | 2/3 | 12 | 12 | Present | SRC121:2196 |
| Beam 66 | 66 | 4 | 1/0 | 66 | 51 | Present | SRC121:1887 |
| Shell 773 | 773 | 21 | 1/3 | 773 | 773 | Absent | SRC121:4236 |
| Shell 803 | 803 | 28 | 1/3 | 803 | 803 | Absent | SRC121:4292 |
| Discrete 806 | 806 | 1 | 1/3 | 806 | 806 | Present | SRC121:7162629 |
| Discrete 820 | 820 | 7 | 1/3 | 820 | 820 | Present | SRC121:7162741 |
| Discrete 821 | 821 | 7 | 1/3 | 821 | 821 | Present | SRC121:7162749 |
| Discrete 852 | 852 | 7 | 1/3 | 852 | 852 | Present | SRC121:7162997 |
| Discrete 855 | 855 | 1 | 1/3 | 855 | 855 | Present | SRC121:7163021 |
| Discrete 859 | 859 | 8 | 1/3 | 859 | 859 | Present | SRC121:7163053 |
| Shell 1034 | 34 | 1 | 1/3 | 1034 | 1034 | Present | SRC120:4085993 |
| Shell 1783 | 783 | 1 | 1/3 | 1783 | 1783 | Present | SRC120:4088425 |
| Shell 1803 | 803 | 1 | 1/3 | 1803 | 1803 | Present | SRC120:4088489 |

The 21 nodes incident to shell PID773 and 28 incident to shell PID803 do not
overlap: **49 distinct class-3 nodes have those missing-material dependencies**.
That is a traceable input dependency, not a count of failed connections,
unsupported nodes or historically deleted members. A defined MID1803 does
not automatically replace missing MID803 merely because their original-ID
history is related.

The recorded material types are:

- PIDs11/12: `*MAT_ELASTIC_VISCOPLASTIC_THERMAL`.
- PID66 and PIDs1034/1783/1803: `*MAT_PIECEWISE_LINEAR_PLASTICITY`.
- Discrete PIDs806/820/821/852/855/859: `*MAT_SPRING_NONLINEAR_ELASTIC`.

In particular, the spring keywords for PIDs820/821/859 are positively supplied
by the frozen registry. This schema does **not** supply their material-definition
source/line, curve references or full constitutive cards. That limitation is
not a finding that those records are absent from the production or model.
Likewise, a true `section_defined` flag remains true when `section_shell` is
null: beam/discrete section detail is not a missing section merely because
this derivative preserves shell-specific locators only.

The four PID66 beam nodes have no supplied shell-corner thickness. They remain
class 0 and were admitted against all CID1 master records under the diagnostic's
unknown-priority rule. Their 2,840 relations per setting must not be described
as 2,840 geometrically close or initialized contacts, or as zero thickness.

## Output schema and reproducibility

`exact-parts01.json` retains:

- `part_reference_registry`: every selected part's effective/original PID,
  SID/MID, definition status, PART source/line, available shell-section locators
  and material keyword. Unavailable material locators are explicit nulls.
- `node_registry`: node source/line, no-shell/unknown-thickness status and every
  typed node-part incidence. Its element-incidence counts are not unique EIDs.
- `groups`: every setting/CID/class0/2/3 group, full relation identities,
  unique nodes, typed-part node lists/counts and explicit zero entries.
- `same_setting_reconciliation`: cross-CID/class overlaps, union counts and
  selected nodes also having class-1 relations. Across-setting totals use a
  node-ID union, not addition of scenario counts.
- `missing_material_dependencies`: the exact node lists for the two missing
  material-reference lookups, without a mechanical failure inference.

The complete stage incidence for selected nodes was compared exactly with
the incidence already preserved in the exact output. All input pins were
checked before and after; no raw/source program was executed.

Actual producer command:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B summarize_exact_parts.py --output /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/c79-contact-geometry/exact-parts01.json
```

The working directory was this unit. All 12 named synthetic controls ran before
historical-array loading: complete/zero groups, typed-part zeros, CID/class/
setting overlap, outside overlap, unknown beam nodes, absent material/section,
missing registry vs absence, non-shell section locator limits, duplicate
relation rejection, create-only protection and pin mutation rejection. The
producer completed successfully in 0.752242 s. The original and root replay
each contain those controls and unchanged before/after pins.

| Artifact | SHA-256 |
|---|---|
| `summarize_exact_parts.py` | `95f78eb2b6abe8496e2d882e599480617c2f18ea4b9d7d420367dd6219d941d1` |
| `exact-parts01.json` | `fe62487947a64dd4816c398cc92124073c4253a1d04f40c5401aa18b2e893e1e` |
| Root-owned replay `exact-parts-root01.json` | `4358020def13b035b5579e89424de5f3f3bfda28e39609183107c7b13c2c958c` |
| `exact-proximity80.json` | `25cb6d5a71a5d34908368523725cfe8612a4d8cf37de616220cf36e9663a4324` |
| `exact-proximity80.npz` | `79bbdc475b2680034096092e207bdd95250e4e7191ae4275ace4106e526c5628` |
| `stage-root01.json` | `deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963` |
| `stage-root01.npz` | `2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf` |
| `PROTOCOL.md` | `b18a519ba88e7d61d331d821232e269c3e3f9a5e690a3e25e3e108e1e70df1ea` |
| `EXACT-ARITHMETIC-ADDENDUM.md` | `b02c1e3c08c8ab976cafba990088a4d80b06e7db9fea5d2d927fb7d0a9f8bb89` |

The root reported reading the complete producer and executing its own replay.
This reviewer independently hash-checked and recursively compared **both full
receipts and their results**: the only differing paths are `/command/4` (the
actual output pathname) and `/elapsed_seconds`. Every other value, including
all node/part/relation arrays and source pins, is equal. The replay took
0.804314 s. This establishes consumer reproduction of this descriptive summary,
not a second independent source extraction or newly independent geometric
implementation.

## Bounded disposition

The source-of-truth and evidence-audit controls keep these numeric references
in the working investigation layer. The development-verification controls
required the pre-evaluation synthetic tests, create-only output and actual
replay comparison. This subtask authored only the requested producer, result
and this review; root owns the replay. Main/raw/legal records, source PDFs,
frozen geometry and source programs were not modified or newly inspected.

The highest-value dependency now visible is the exact node-to-PID773/MID773
and node-to-PID803/MID803 reference chain, plus the positively present spring
material types whose detailed laws/locators are not carried by this schema.
Physical seat/floor attribution, full constitutive dependencies, run identity,
initialized pairing, force/capacity, activation and survival remain separate
questions. This reviewer did not inspect or certify the contact-damage join
or infer a collapse cause from any part, material or class label.
