# Released-input member map: independent keyword-method source review

2026-09-12. WP3 / Q06 / Q10. Working research, not a solver reproduction, physical-member authentication, expert opinion, or causal ranking. This review was developed independently of the forthcoming member-map parser and its results; neither was read. The only permanent write by this reviewer is this file. Main, preserved inputs, prior reports, canonical spines, and correspondence remain unchanged.

## Finding

The primary manual supports a bounded input-graph reconstruction, with three consequential safeguards:

1. `*ELEMENT_SHELL_THICKNESS` has a connectivity card followed by a thickness card. The old inspector counted both as data lines. Its master total is not a count of shell elements.
2. Beam `N3` is an orientation reference, not a third endpoint. Include ID offsets rename identifiers; they are separate from coordinate transformations.
3. A named cross-section diagnostic links through `PSID` to a **part set**, then through its listed part IDs to elements. A normalized “column 79” label can support model-authored attribution through that chain, not a guess that part ID 79 is architectural Column 79. Neither route independently authenticates an original drawing or historical physical member.

## Scope, sources, and acquisition

Controls read: current main `AGENTS.md`, worktree `WORKFLOW.md`, `START-HERE.md`, and this investigation's `CHARTER.md`. The evidence-falsification-auditor and source-of-truth-guardian skills keep observed source cards, derived joins, and physical interpretation separate. The PDF skill was used to check actual card layouts visually.

Existing local source review was bounded to the main checkout's `research/sherlock-wtc7-investigation/lsdyna-supplement-content-audit/PROTOCOL.md`, `report.md`, relevant inspector code, and selected numeric/count fields in `inventory.json` and `focus.json`. No full raw payload, private comments, path-bearing titles, held packet, or new case production was inspected or exported. One subsequent explicit parent authorization allowed the raw master **transform block only**, with comments and the filename suppressed; that check is recorded below.

Local manual discovery used `rg --files -uu authority research/sherlock-wtc7-investigation tools` with LS-DYNA/manual/keyword/dynasupport filename filters; no existing manual was found in those selected public/research/tool locations. This is bounded filename coverage, not a claim that the entire repository lacks manuals. The primary [DynaSupport manuals index](https://www.dynasupport.com/manuals/ls-dyna-manuals) identifies the May 2007 Version 971 manual. The DynaSupport PDF route failed locally (HTTP/2 error; HTTP/1.1 timeout), and the web reader could not open that large PDF. These acquisition failures have no engineering significance. The official Ansys-hosted copy was then acquired successfully:

- [LSTC, LS-DYNA Keyword User's Manual, Volume I, May 2007, Version 971](https://lsdyna.ansys.com/wp-content/uploads/2025/02/ls-dyna_971_manual_k.pdf), designated **M971** below.
- Local public-source copy: `/private/tmp/lsdyna-keyword-source-review.6f36b5/ls-dyna_971_manual_k-ansys.pdf`.
- 17,476,361 bytes; 2,206 physical PDF pages; SHA-256 `f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d`.
- Cover independently viewed: May 2007 / Version 971 / LSTC. The URL's 2025 directory is not the manual's edition date. A hash pins acquired bytes, not historical solver identity.

Acquisition command (public technical documentation only):

```sh
curl --fail --location --silent --show-error --http1.1 --max-time 60 --output /private/tmp/lsdyna-keyword-source-review.6f36b5/ls-dyna_971_manual_k-ansys.pdf 'https://lsdyna.ansys.com/wp-content/uploads/2025/02/ls-dyna_971_manual_k.pdf'
```

M971 text was read with bundled Python 3.12.14 / pypdf 6.10.0. Complete layout-sensitive pages 1, 47, 609, 610, 611, 747, 758, 787, 788, 794, 797, 859, 1011, 1016, 1029, and 1167 were rendered and independently viewed. Page-specific derivatives are `/private/tmp/lsdyna-keyword-source-review.6f36b5/p-N.png`, where N is the **one-based physical PDF page**, not the printed section page. The command for each N was:

```sh
FONTCONFIG_FILE=/Users/admin/docs/911/research/sherlock-wtc7-investigation/nist-camera-method-audit/fonts.conf /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f N -l N -singlefile -r 110 -png /private/tmp/lsdyna-keyword-source-review.6f36b5/ls-dyna_971_manual_k-ansys.pdf /private/tmp/lsdyna-keyword-source-review.6f36b5/p-N
```

Poppler 26.05.0; existing font configuration SHA-256 `5be7be745aea3718d078c9a1c0c1b5cff5b3cae779084c13e2047dcc1b3f6e42`. Render commands succeeded without stderr output. No temporary derivatives were deleted. Additional complete text pages inspected for definitions/qualifications include 46, 65–66, 750, 754–755, 789–790, 795–799, 861–863, 1032, and 1168. No third-party technical explanation supplies a substantive rule below.

## Exact schemas and minimum interpretation

All M971 pins give physical PDF page / printed page. M971 pp. 46–47 / GS.2–3 and 65–66 / GS.21–22 distinguish keyword/comment lines and comma-separated versus fixed-field cards. Most cards have eight 10-character fields, but explicitly specified formats override that default. Fixed and comma formats may coexist in a deck, not within a card. A comma parser must preserve empty positions; a whitespace split cannot correctly parse adjacent full-width fields. Required blank cards must not disappear in a global blank-line filter. Retain record boundaries, source line numbers, keyword variants, and include lineage.

| Keyword / record | Minimum schema and meaning | Primary pin |
|---|---|---|
| `*NODE` | `I8,3E16.0,2F8.0`: `NID,X,Y,Z,TC,RC`. X/Y/Z are global coordinates; TC/RC are constraint codes, not additional coordinates. NID must resolve uniquely. | M971 1016 / 23.2 |
| `*ELEMENT_SHELL` | `10I8`: `EID,PID,N1,N2,N3,N4,N5,N6,N7,N8`; later nodes default to zero. Preserve ordered connectivity and distinguish actual nodes from padding. | 787, 789 / 14.43, 14.45 |
| `*ELEMENT_SHELL_THICKNESS` | Same connectivity, then required `5E16.0`: `THIC1,THIC2,THIC3,THIC4,BETA-or-MCID`. The fifth field may be blank; four thickness floats are not another element. Zero thickness can inherit section properties. | 788–789 / 14.44–45 |
| `*ELEMENT_BEAM` | `10I8`: `EID,PID,N1,N2,N3,RT1,RR1,RT2,RR2,LOCAL`. N1/N2 are endpoints; N3 determines orientation. | 747, 750, 754–755 / 14.3, 14.6, 14.10–11 |
| `*ELEMENT_DISCRETE` | `5I8,E16.0,I8,E16.0`: `EID,PID,N1,N2,VID,S,PF,OFFSET`. N2=0 means ground. VID is an orientation reference, not a third endpoint/node. | 758 / 14.14 |
| `*ELEMENT_SOLID` | Documented two-card form: `2I8` EID/PID, then ten 8-wide node fields N1…N10. Older single-card `10I8` EID/PID/N1…N8 is expressly still accepted for 4–8-node elements. Detect the actual form; do not infer row count from keyword alone. | 794, 797 / 14.50, 14.53 |
| `*PART` | Heading card, then eight standard fields `PID,SECID,MID,EOSID,HGID,GRAV,ADPOPT,TMID`. Several references have A8 type in this historical table; an unsupported string/parameter reference must not silently become zero. This joins an element to section/material properties, not to an architectural column number. | 1029, 1032 / 25.3, 25.6 |
| `*SET_PART_LIST` | Header `SID,DA1,DA2,DA3,DA4`, then repeated eight 10-wide PID fields until the next keyword. SID is the set ID; header attributes are not members. | 1167–1168 / 31.17–18 |
| `*LOAD_THERMAL_VARIABLE_NODE` | Standard 10-wide fields `NID,TS,TB,LCID`; the time-dependent prescribed quantity is `T(t)=TB+TS*f(t)`, with f supplied by the referenced load curve. | 1011 / 22.67 |

A bounded parser should reject or explicitly inventory unsupported variants, not process them as the base keyword. Unsupported global format declarations, parameter references, or numeric syntax must likewise be reported, not silently coerced. In particular, an integer-search regex must not harvest apparent IDs from thickness values in scientific notation. Shell OFFSET/DOF and beam THICKNESS/SECTION/OFFSET/ORIENTATION add cards or change geometric interpretation. Beam formulations may allow an absent N3; spot-weld endpoints can be generated, and negative N2 can mean a generated ground node. Beam nodal endpoints are not necessarily section centroids when offsets apply. SOLID ORTHO/DOF add cards; TET4TOTET10 can generate nodes. Repeated solid connectivity nodes can intentionally encode tetrahedra or pentahedra (M971 797 / 14.53). `SET_PART_COLUMN` is an attribute-bearing **format option**, not a building-column label; `LIST_GENERATE` contains ranges, not eight independent PIDs.

For member geometry, beam orientation N3 belongs in a separate dependency field. Do not include it in endpoint centroids, lengths, vertical spans, or endpoint thermal summaries. For shells/solids, retain ordered connectivity but use a declared unique nonzero node set for simple coordinate summaries. Such a summary is a mesh envelope or node average, not a physical member centroid, capacity, or mass center.

## Include transformation: identifier namespace versus placement

M971 859 / 17.5 defines the TRANSFORM cards after the filename; 861–862 / 17.7–8 supplies their meanings:

| Card | Fields / namespace |
|---|---|
| 2 | `IDNOFF,IDEOFF,IDPOFF,IDMOFF,IDSOFF,IDFOFF,IDDOFF` |
| 3 | `IDROFF` |
| 4 | `FCTMAS,FCTTIM,FCTLEN,FCTTEM,INCOUT1` |
| 5 | `TRANID`; zero means no referenced geometric transformation |

For this edition: IDNOFF applies to nodes; IDEOFF to elements; IDPOFF to parts, nodal rigid bodies, and constrained nodal sets; IDMOFF to materials and equations of state; IDSOFF to sets; IDFOFF to functions/tables; IDDOFF to DEFINE IDs except FUNCTION; IDROFF to sections/hourglass IDs. Apply the appropriate offset to both definitions and corresponding references, without turning zero sentinel/default references into fabricated entities. Do not apply a universal +1000 to every number. The exact historical namespace wording should not be generalized to all newer keywords or releases.

FCTMAS/FCTTIM/FCTLEN convert mass/time/length units. They are not ID offsets. FCTTEM is specified as a character conversion flag, with conversions between Fahrenheit, Centigrade, and Kelvin; it is not documented here as an arbitrary numeric multiplier. TRANID selects `*DEFINE_TRANSFORMATION`; a nonzero or unsupported transform requires its explicit definition and ordering before a coordinate join is accepted. M971 allows nested includes and says `*END` terminates the included file (862 / 17.8). This review did not implement a general transformation engine or execute INCOUT1.

### Narrow source check, explicitly authorized after initial metadata review

The master SRC-121 compressed SHA-256 was independently recomputed as `f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d`, matching the existing inventory. Only the block from keyword line 5,520,133 through the next keyword at 5,520,148 was interpreted. The input path was resolved internally from the existing inventory; it was not printed. The filename card and all comments were suppressed. Each non-comment card was validated as numeric/blank before output; numeric fields were read at their actual 10-character positions.

| Source line | Typed card | Observed fields |
|---|---|---|
| 5,520,136 | Card 2, ID offsets | `0,0,1000,1000,0,0,0` |
| 5,520,138 | Card 3, remaining offsets | `1000` |
| 5,520,140 | Card 4, conversion/output fields | `1,1,1,1,0` |
| 5,520,142 | Card 5, TRANID | `0` |

There were no intervening blank data cards. Thus the inspected include has unchanged node/element IDs, +1000 part/material/EOS/section/hourglass namespaces (and the other documented IDPOFF categories), and **unchanged geometric placement under the documented FCTLEN=1 and TRANID=0 semantics**. No coordinate translation by 1000 is authorized by these cards. The fourth card's numeric FCTTEM token remains an edition/accepted-input-convention uncertainty; it does not affect the coordinate-placement conclusion, and must not be represented as a documented arbitrary temperature multiplier.

## Cross-section diagnostic to model member association

M971 609–611 / 10.13–15 gives this exact `*DATABASE_CROSS_SECTION_PLANE_ID` sequence:

- ID card: `CSID` in the first 10-wide field, followed by `HEADING` (A70).
- Plane card 1: `PSID,XCT,YCT,ZCT,XCH,YCH,ZCH,RADIUS`.
- Plane card 2: `XHEV,YHEV,ZHEV,LENL,LENM,ID,ITYPE`.

CSID identifies the diagnostic; HEADING is a postprocessing descriptor. PSID is explicitly a **part-set ID**, with zero selecting all parts. The tail coordinates locate a point on the cutting plane; the head coordinates define its normal direction. Edge/length/radius fields define the cut's extent. The second card's ID concerns the output coordinate/body reference, not a part or building-column ID. The default plane is not an independently observed architectural cross section. The separate CROSS_SECTION_SET variant has a different schema and must not be parsed as PLANE.

Consequently, the minimum defensible chain is:

`normalized diagnostic label -> PSID -> SET_PART_LIST.SID -> listed PID -> ELEMENT.PID -> connectivity -> NODE coordinates`

Every arrow needs source/include provenance and cardinality checks. Parent-reported preliminary metadata gives the useful lead “column 79” -> PSID 179, with neighboring normalized labels 78/80 associated with 178/180. This reviewer has **not** independently read the new plane-label or complete set table and does not certify that model-specific join here. The manual establishes the rule needed to test it. An anchored, declared normalization of the diagnostic heading can retain only a column number plus local label hash; ambiguous or absent labels remain unresolved. A hash alone does not establish what a label meant.

Even a successfully resolved diagnostic-to-part-set join gives model-author labeling, not a drawing-authenticated physical column. A set may contain multiple parts, overlapping assignments, or only a subset of a member. The force diagnostic further selects elements intersected by its cutting plane; it need not measure every element in the set. M971 Fig. 10.1 expressly notes that automatic plane selection does not check springs/dampers and excludes elements intersecting plane edges. A full-set geometry map is therefore distinct from a reproduced SECFORC selection/result. No solver output was generated here.

## Verified cardinality correction and thermal ceiling

The old inspector's `analyze_lsdyna_inputs.py` lines 421–424 increments `element_line_counts[keyword]` once for each data line under any ELEMENT keyword. It has no shell thickness continuation state. The existing inventory reports:

| File role | Stored ELEMENT_SHELL_THICKNESS data lines | Conditional element count if every element is one valid two-card record |
|---|---:|---:|
| Outside-fire-zone include / SRC-120 | 4,085,686 | 2,042,843 |
| Master / SRC-121 | 1,928,134 | 964,067 |

The report's outside-include table correctly says “rows,” but the master table's “~1.93 million fire-zone/slab shells” is an overstatement of what that counter measures. Existing numeric-only samples independently support the continuation interpretation: outside lines 6/7 and 8/9 alternate connectivity and four thickness values; master lines 642/643 and 3,591,982/3,591,983 do likewise. The half-counts above are **arithmetic expectations**, not newly certified complete-stream cardinalities. A complete parser must validate pairing within every block, reject orphan or malformed cards, and count connectivity records. The same line-counter design means the old 2,461 SOLID total is not independently certified here without confirming which accepted solid card form was used.

Thermal TS is a per-node scale coefficient in the prescribed input expression; it is not itself a time-history observation, solved material temperature, or column-only statistic. M971 1011 / 22.67 also describes the temperature reference convention in terms of a null reference state and temperatures relative to the initial reference. Accordingly, report a bounded join as, for example, “selected model-element nodes carrying input TS above threshold,” with unmatched nodes and duplicate assignments retained. Do not silently rename it an observed Celsius maximum for an entire physical column. Evaluation of T(t) requires the referenced curve, scale/time offsets, temperature-unit convention, reference state, and applicable solver documentation. LS-DYNA requires consistent units but does not itself establish that this deck uses meters or Celsius (M971 65 / GS.21).

## Contrary evidence, historical uncertainty, and acceptance boundary

The old report already warns that commented beam cards with PID 79 do not show removal of Column 79. The explicit part-set route offers a stronger, testable model association; it does not overturn that warning. Other contrary clues are structural: orientation nodes can be far from beam endpoints; intended solid degeneracies repeat node IDs; blank cards can be required; shell thickness rows contain numbers but no EID/PID; part headings may identify materials or modeling groups rather than single members.

M971 is a contemporaneous primary specification, not evidence of the exact historical executable/build. The official [Version 971 R5.1.1 release notes](https://lsdyna.ansys.com/ls-dyna-v971-r5-1-1-r5-65550-released/), General section, document corrections to nested INCLUDE_TRANSFORM handling and to offset namespaces for specific keyword references. This is concrete evidence that version-dependent implementation matters, not proof that any listed defect affected the released deck. The source review therefore supports an independently testable **documented input interpretation**, not numerical reproduction of a historical run.

| Material claim | Type / strength | Decisive support and weakening test |
|---|---|---|
| Old shell totals are data-line counts, not element counts | Observed code + derived interpretation / A | Explicit counter and M971 two-card schema; weakened only by a different inspector/hash or materially different counted-record path. |
| Inspected include does not reposition coordinates | Observed cards + documented interpretation / A for this block | Hash-matched SRC-121, FCTLEN=1 and TRANID=0; a different include graph, overwritten definitions, or other coordinate-changing cards would limit assembly-wide extension. |
| N3 is not an ordinary beam endpoint | Primary specification / A | M971 750; actual keyword/formulation/offset variants still require separate handling. |
| PSID supports a diagnostic-to-part-set join | Primary specification / A for semantics | M971 611 and 1167–1168; unresolved/missing set membership would block the particular model join. |
| A successful named set identifies the corresponding historical physical column | Inference / D without external crosswalk | Model naming alone is insufficient; a drawing/member-ID crosswalk plus geometric agreement could strengthen it. |
| TS threshold identifies a physical column's historical temperature | Unsupported in this pass / E | Requires membership, curves, reference/units, and physical validation not supplied by a coefficient histogram. |

Highest-value immediate check: independently resolve the named diagnostic's complete part set, element connectivity, transformed namespaces, and node references, reporting overlap, missing references, unsupported variants, actual record counts, and label ambiguity. Highest-value **next source** for physical attribution is the model-author part/element-to-drawing-member crosswalk (or original labeled mesh/assembly documentation), matched to these exact released bytes. The historical solver build/run header and associated keyword-version record are the concrete next source for unresolved parser/thermal conventions. Neither source is invented or acquired through this review, and no solver/outreach is authorized by naming it.

## Pinned local dependencies

Paths in this table are relative to read-only `/Users/admin/docs/911/research/sherlock-wtc7-investigation/lsdyna-supplement-content-audit/`.

| Artifact | SHA-256 |
|---|---|
| `PROTOCOL.md` | `8b5b79357f9b0093611fcac60901b721294c6c3d05e6ef8139cb2019e430d6bc` |
| `report.md` | `1d0b1d3031d7ee5b8baa87459c166fb5460954cc96e864a45199a52365483f9e` |
| `inventory.json` | `391b13a37df24c9b2c987d0e1d03bf27513bd718fa3fecd168a95f614104dbf3` |
| `focus.json` | `9d90e1cccce799af0d92470dedc6444c04dde35cf050c933d3a55b0135dd18a6` |
| `analyze_lsdyna_inputs.py` | `bc3af2d226fd47dd879039feaf88efde6eecfeeec1954f5beaf60e8573090b40` |

These are dependencies and research corrections, not replacements for the preserved audit. No canonical promotion, source rewrite, source-file deletion, case disclosure, model execution, commit, or push occurred.
