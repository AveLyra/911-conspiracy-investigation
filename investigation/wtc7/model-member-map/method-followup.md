# Method follow-up: material vocabulary and duplicate thermal assignments

2026-09-12. Working WP3 source-method supplement. This does not revise the frozen `method-source-review.md`, SHA-256 `cbea5556de774752fefc82ff5c49ed299bb73ea3fb65af0fcafc7c0e7f24fe5f`. No historical mesh-join output or independent-verifier artifact was opened for this supplement. No raw deck was inspected, and no solver or case communication was run.

## Opaque material-keyword hash resolved against the primary manual

The parent supplied keyword-name SHA-256 `607ae2a6f6001165b8bb8cf5b6447d744368a747cf9e9de5f1993a1edfe9bda0`, with the leading asterisk excluded. The existing read-only inventory was searched internally for this exact hash; it identified one distinct token. That token was then matched against the primary manual before its name was emitted. Arbitrary inventory names, titles, and paths were not displayed.

The confirmed standard keyword is **`*MAT_PLASTICITY_COMPRESSION_TENSION`**, Material Type **124**. Its exact name without the leading asterisk produces the supplied hash. This is not the separate `_EOS` variant / Material Type 155.

Primary evidence is LSTC's [May 2007 Version 971 Keyword User's Manual](https://lsdyna.ansys.com/wp-content/uploads/2025/02/ls-dyna_971_manual_k.pdf), physical PDF pages **1865–1866**, printed **473–474 (MAT)**. Both complete pages were rendered and independently viewed. Page 1865 presents the first card as eight standard-width fields:

`MID, RO, E, PR, C, P, FAIL, TDEL`

MID is the first field, with type **A8** within the standard 10-character card field. Page 1866 defines it as the material identifier, allowing a unique number or a label of at most eight characters. Consequently:

- This exact keyword can enter the explicit standard-material allowlist.
- Its first numeric field identifies a **material definition**, not a part, element, or modification-only card. The documented material-ID namespace applies.
- A scoped numeric-only parser may accept numeric MID while rejecting unsupported alphanumeric labels; it must not silently manufacture an integer from a label.
- Recognizing the keyword does not authenticate its supplied parameter values or establish that failure, rate effects, or any other optional behavior was enabled. No parameter or engineering-effect inference was made here.

The public source copy remains `/private/tmp/lsdyna-keyword-source-review.6f36b5/ls-dyna_971_manual_k-ansys.pdf`, SHA-256 `f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d`. New local renders are `p-1865.png` and `p-1866.png` in that same temporary directory. For each N in 1865, 1866:

```sh
FONTCONFIG_FILE=/Users/admin/docs/911/research/sherlock-wtc7-investigation/nist-camera-method-audit/fonts.conf /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f N -l N -singlefile -r 110 -png /private/tmp/lsdyna-keyword-source-review.6f36b5/ls-dyna_971_manual_k-ansys.pdf /private/tmp/lsdyna-keyword-source-review.6f36b5/p-N
```

The commands succeeded without stderr output. The original inventory dependency is `/Users/admin/docs/911/research/sherlock-wtc7-investigation/lsdyna-supplement-content-audit/inventory.json`, pinned in the frozen source review at SHA-256 `391b13a37df24c9b2c987d0e1d03bf27513bd718fa3fecd168a95f614104dbf3`.

## Duplicate thermal cards: assignment description is not solver resolution

The parent reports that the continued thermal-card pass found unequal TS values at repeated node IDs. This reviewer did not independently inspect those historical values or certify their counts. The controlling new analysis declaration read here is `THERMAL-DUPLICATE-ADDENDUM.md`, SHA-256 `7433fb5d5b4e151eb70df22b1c40825939d3868842af0ee0ff816c830f236b94`, adopted before a successful new mesh join.

The frozen primary-source pin for `*LOAD_THERMAL_VARIABLE_NODE` remains physical PDF page **1011**, printed **22.67 (LOAD)**: card fields NID, TS, TB, LCID and expression `T(t)=TB+TS*f(t)`. That section does not specify how repeated cards for one node combine or which card prevails. It therefore supplies no source basis for selecting first, last, maximum, sum, or average. Nor does equal TS prove that a historical solver treated repeated cards as redundant.

For the declared bounded input map, preserve assignment-row counts separately from unique node counts, duplicate/ambiguous-node counts, TB/LCID checks, and per-node extrema of **supplied TS coefficients**. Union node IDs before aggregating parts or diagnostic part sets. A node with unequal supplied coefficients is not an established single-temperature node.

Crucially, a minimum/maximum supplied-coefficient envelope is **not a demonstrated bound on the solver's resulting temperature**. An unknown duplicate-card composition rule could produce a different quantity, and the curve/reference conventions remain separate dependencies. The envelope is a descriptive property of available input cards, not a probability interval, physical temperature uncertainty, solved field, or bound on historical structural response. This is consistent with the addendum and narrows any casual reading of “temperature envelope.”

The highest-value source remains the exact historical executable/build's duplicate thermal-card rule, together with the model-author thermal-transfer convention. A documented synthetic solver test could later clarify a particular executable's behavior, but this source-method review authorizes no solver run and no extrapolation from another version. Any historical scalar field must remain unresolved until the applicable rule is established.

The original source-only review, preserved inputs, main checkout, case records, and earlier failed runs were not changed. This follow-up introduces no causal ranking or physical-column temperature finding.

## 2026-09-12 follow-up 2: beam sets, discrete elements, and restart deletion

Review history: before this append, `method-followup.md` had SHA-256 `0f0c3feaacacaa132584c12d3688d9fa6078216b2b252623a4004986eff1b5d8`. Its earlier material and thermal sections are preserved above. The original `method-source-review.md` remains frozen at `cbea5556de774752fefc82ff5c49ed299bb73ea3fb65af0fcafc7c0e7f24fe5f`.

This is a source-semantic question, not a result from the historical model. No source payload, element-ID list, member-map output, or verifier result was read for this append. The parent asked whether beam-set IDs could resolve to discrete spring/damper entities before treating an explicit-beam join failure as absence from the mesh.

### What the primary manual establishes

The same May 2007 Version 971 PDF and acquired-byte hash cited above controls these pins. Page numbers before the slash are physical PDF pages; numbers after the slash are printed pages.

| Source pin | Documented distinction |
|---|---|
| 1151 / 31.1 (SET) | The set index separately lists SET_BEAM and SET_DISCRETE families. Set types have their own identification requirement. |
| 1152–1154 / 31.2–4 (SET) | `*SET_BEAM` defines a beam-element set. The first card is SID; subsequent plain-form fields K1…K8 identify beam elements. GENERATE and GENERAL are separate forms. |
| 1156–1158 / 31.6–8 (SET) | `*SET_DISCRETE` independently defines a discrete-element set, with the analogous SID and discrete-element ID fields. This is not merely an alternative title for SET_BEAM in the inspected definitions. |
| 1227–1228 / 35.27–28 (RESTART) | `*DELETE_OPTION` lists ELEMENT_BEAM, ELEMENT_SHELL, ELEMENT_SOLID, and ELEMENT_TSHELL. For these four options, each data card supplies ESID, an element **set** ID, with corresponding references to SET_BEAM/SET_SHELL/SET_SOLID/SET_TSHELL. ELEMENT_DISCRETE is not listed as a DELETE option here. |
| 758–759 / 14.14–15 (ELEMENT) | `*ELEMENT_DISCRETE` defines a spring/damper between two nodes or a node and ground. The EID note says visualization null beams are created, explaining why these EIDs ordinarily must differ from explicit BEAM and SEATBELT IDs. |
| 750 / 14.6 (ELEMENT) | The BEAM EID note says setting BEAM=1 in DATABASE_BINARY_D3PLOT suppresses visualization null beams for discrete/seatbelt entities, in which case their IDs can coincide with explicit BEAM IDs. |

Thus the documented route for `*DELETE_ELEMENT_BEAM` is **beam set ID -> beam-element selection**, not a direct list of arbitrary element IDs. The manual does not document a general rule in these sections that SET_BEAM includes every ELEMENT_DISCRETE spring/damper.

There is an important terminology distinction: a discrete **beam formulation** defined through `*ELEMENT_BEAM` (for example, type 6 discussed on page 750) is still an explicit BEAM record. It must not be confused with the separate `*ELEMENT_DISCRETE` input family. A generic “spring” description does not establish which family was used.

### What remains unresolved

The visualization-null-beam notes are a concrete reason not to infer historical deletion behavior solely from the separate keyword names. Neither the inspected set sections nor the restart DELETE section states whether a generated null beam enters beam sets, whether deleting it also removes its underlying discrete element, or which historical implementation/version conditions might govern that linkage. A shared-ID restriction for visualization is not itself a deletion rule.

Accordingly, these sources support the separate documented families but **do not establish either universal inclusion or a universal historical exclusion of ELEMENT_DISCRETE through generated beam representations**. No version-specific executable test or historical run record was inspected. The absence of an ELEMENT_DISCRETE DELETE option in this edition does not prove that discrete elements could never be removed by another mechanism.

The safe input-map treatment is:

1. Report explicit-family joins separately: IDs found in supplied ELEMENT_BEAM records, IDs found only in supplied ELEMENT_DISCRETE records, IDs present in both, and IDs found in neither examined family. Preserve source/type provenance.
2. Describe a discrete-family numeric match as a **cross-family candidate match**, not an authenticated beam deletion. Do not silently fold it into the count of matched explicit BEAM records.
3. Phrase a failed explicit-beam join as “not found in supplied ELEMENT_BEAM records,” not “missing from the model,” “deleted,” or “never existed.” A complete absence claim requires checking the relevant other input/generated namespaces and stating coverage.
4. Leave the historical operation of a beam-set deletion on a discrete/null-beam candidate unresolved. None of these input-record matches establishes an active deletion, structural failure, or physical member removal.

This both preserves possible cross-family evidence and prevents a numerical ID coincidence from becoming an invented solver rule. No live-model count or ID-level result is asserted here.

### Search coverage and next discriminating source

The complete selected M971 set, restart-delete, and element pages above were read. Full-PDF exact-term discovery also checked SET_BEAM, DELETE_ELEMENT_BEAM/DELETE_ELEMENT, ELEMENT_DISCRETE, and null-beam wording. DELETE is organized under `*DELETE_OPTION` with separate option names, so an empty exact search for the expanded keyword was not treated as absence of the feature. Targeted official-site web searches for SET_BEAM/discrete, DELETE_ELEMENT_BEAM/discrete, and DELETE_ELEMENT_BEAM/spring did not yield an explicit generated-null-beam deletion-coupling rule in the retrieved material. This is bounded coverage, not proof that no such documentation exists.

The highest-value next source is historical-version documentation or implementation notes specifying the relationship among generated null beams, SET_BEAM membership, and ELEMENT_BEAM restart deletion. A future authorized synthetic test would need to inspect the underlying spring/damper's retained force/response, not merely disappearance of its visualization, and distinguish the output BEAM flag settings. No such test was performed or authorized here.

Complete pages 750, 1152, 1153, 1156, 1157, 1227, and 1228 were additionally rendered and visually checked; page 758 had already been rendered and checked for the original source review. Derivatives use `/private/tmp/lsdyna-keyword-source-review.6f36b5/p-N.png` and the identical page-specific Poppler/font-configuration command recorded above. Render commands succeeded without stderr output. All primary source bytes and the original source-review freeze remain unchanged.
