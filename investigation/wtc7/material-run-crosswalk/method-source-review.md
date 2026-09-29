# Connection materials and run provenance: primary-source crosswalk

2026-09-12. WP3 / Q06 / Q10. Research only. This independent source reviewer read no raw produced model contents and did not reproduce the numerical joins. The protocol's 19 unresolved material references across 23 used parts, and the root reviewer's reported PID98/SEC98/MID50 beam chain, select questions; they are not new independently verified findings of this note. No identity is inferred from numeric labels, model titles, or comments.

Current main `AGENTS.md`, `WORKFLOW.md`, `START-HERE.md`, the investigation `CHARTER.md`, and this unit's `PROTOCOL.md` control. The source-of-truth and evidence-falsification skills keep documentary descriptions separate from implementation and execution. The PDF skill required complete-page visual checks. Only this new note and temporary public-source renders were written. No held packet, flagged modern command documentation, solver, outreach, private transmission, main/canonical edit, commit, or push was used.

## Result and permitted conclusion

The published record supplies material-model families, connection construction/calibration methods, some numerical capacities, damage-transfer conventions, and a reported solver build. It does **not** identify the missing active definitions by material ID or authenticate the released assembly as the historical executable input. Missing definitions therefore remain a specific reproducibility dependency; the reports are neither a replacement deck nor evidence that every connection property was unpublished.

There are four distinct links to verify: physical connection/location to model component; component to part/section/material/curve definitions; definitions to the assembled input and initialization/restart state; and that input/state to the historical executable and output. The public method descriptions inform those links without closing them.

## Supplied-versus-unsupplied ledger

Pins are **physical PDF page / printed page**. Documentary statements below are **A: directly established as statements in the cited report**, not validation of their physical accuracy or historical implementation. “Not supplied” means not identified in this bounded inspected material, not universal nonexistence.

### LS-DYNA account: NCSTAR 1-9A

Source: [official final-report publication entry](https://www.nist.gov/publications/global-structural-analysis-response-world-trade-center-building-7-fires-and-debris-0), [official PDF](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861612).

| Pin | Supplied documentary information | Unsupplied bridge / overclaim to avoid |
|---|---|---|
| 54/3, §2.2; 59/8, §§2.2.2-2.2.3 and footnote | Steel types 24/106; Algoma model restricted to seats; other connection components use custom models. | A generic steel curve cannot automatically replace a missing connection law. Material **type** is not material **ID**. |
| 73-75/22-24, §3.3.1; Figures 3-2/3-3 | Calibrated shell-tab behavior/failure strain; location/geometry/capacity spreadsheet; depth/type groupings, geometric scaling, added elastic-perfectly-plastic discrete shear capacity. | No retrieved spreadsheet-to-PID/MID/SECID/curve-ID crosswalk, calibrated card set, or per-location scaling assignment. |
| 76/25, Figures 3-4/3-5; 77/26 | Model-comparison force/displacement and energy plots; selected ANSYS/LS-DYNA agreement reported. STP bolt shear: 35 kip yield, 45 kip failure, 0.45 in. failure displacement. | Calibration/selected model agreement is not an independent validation of every connection or authentication of these released cards. Plots were not digitized into replacement curves. |
| 83/32, Moment Connections | Wind-girder properties with failure strain reduced 30% for weld zones. | No mapping of this relative adjustment to a selected missing ID or beam. |
| 85/34, §3.3.3 | Nonfailing shear-stud tied contact; constituent material failure severs attachment. | Do not assume an independently failing connector law for every modeled attachment. |
| 100/49, Model of Penthouse Structures | Simplified beam framing; no detailed connection models; stated decoupling. | No identification of the six selected beams from this paragraph or numeric labels. |
| 103-104/52-53, load distribution | Equipment weights modeled separately; densities scaled for the 25%-live-load case. | A material density needs units, base density, scaling and mass-allocation provenance before comparison with physical steel density. No particular factor or density value is authenticated here. |
| 109-110/58-59, Figure 3-58; 117/66, §3.6.3 | Damage-index approximation and restart deletion; reported mpp971dR4 beta revision 41161, double precision. | No exact released-input hash/include manifest, checkpoint, restart invocation, input echo, executable hash, or output provenance supplied by these passages. |

### ANSYS account: NCSTAR 1-9

Source: [official publication entry](https://www.nist.gov/publications/structural-fire-response-and-probable-collapse-sequence-world-trade-center-building-7), [official PDF endpoint](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861611).

| Pin | Supplied documentary information | Limit |
|---|---|---|
| 536-537/470-471, Tables 11-2/11-3 | Typical-floor connection capacities, failure modes and design-load comparisons. | Positive quantitative disclosure, but not the missing LS-DYNA material cards or a material-ID map. |
| 539-540/473-474, §11.2.5/Table 11-5 | USER102-105 break elements; temperature-dependent capacities; force/deformation limits; series/parallel failure modes; post-failure stiffness at 10^-6 to 10^-9 of initial stiffness. Table 11-5 specifies required degrees of freedom, capacities and stiffness categories. | ANSYS element types are not LS-DYNA material IDs. The table describes a parameter schema, not all per-connection parameter values. |
| 541/475, Analytical Modeling of Connections | Limited detailed-connection region; shear-stud capacity scaled to modeled stud count. | Do not assume detailed break elements everywhere or a one-to-one physical-stud/model-element relation. |
| 601/535, §11.5/Table 11-7 | Case B four-hour damage carried forward; separate horizontal/vertical damage estimates from bolt, weld and walk-off conditions. | This is a transfer convention, not an executable match between a particular produced list and a historical restart. |

The reports describe related stages of one NIST investigation; repeated descriptions are not independent corroboration. NCSTAR 1-9A's shell/discrete calibration and NCSTAR 1-9's break-element logic must not be blended into a fictitious single implementation.

## Narrow card-field review requested during this pass

The root reviewer requested the previously approved **May 2007 Version 971** manual route for the reported `*MAT_PIECEWISE_LINEAR_PLASTICITY` and `*SECTION_BEAM` cards. Source: [official Ansys-hosted legacy manual](https://lsdyna.ansys.com/wp-content/uploads/2025/02/ls-dyna_971_manual_k.pdf), locally hash-verified as M971 below. This manual supplies a version-specific reading convention, not proof of behavior in revision 41161 or of a historical run.

| Card | Physical / printed pins | Field order |
|---|---|---|
| MAT024 card 1 | 1502-1503 / MAT110-111 | `MID RO E PR SIGY ETAN FAIL TDEL` |
| MAT024 card 2 | 1502-1504 / MAT110-112 | `C P LCSS LCSR VP` |
| MAT024 cards 3/4 | 1502-1504 / MAT110-112 | `EPS1..EPS8` / `ES1..ES8` |
| SECTION_BEAM card 1 | 1086-1088 / SECTION29.2-29.4 | `SECID ELFORM SHRF QR/IRID CST SCOOR NSM` |
| SECTION_BEAM card 2, integrated type 1 | 1086, 1088-1089 / SECTION29.2, 29.4-29.5 | `TS1 TS2 TT1 TT2 NSLOC NTLOC` |

M971 defines `RO/E/PR` as mass density/Young's modulus/Poisson's ratio. Positive `FAIL` is plastic strain at deletion; `TDEL` concerns minimum time-step deletion. EPS/ES pairs define effective plastic strain/yield stress and supersede `SIGY/ETAN`; zero values in the latter are permitted. `LCSS` can instead reference a curve/table. `ELFORM=1` is Hughes-Liu integration; `QR=3` is 3x3 Gauss; `CST=1` selects circular tubular geometry. TS/TT then mean outer/inner diameters, not areas. `NSM` is nonstructural mass per length. Element-level thickness input can override section dimensions.

Accordingly, **conditional on the root's extraction**: `LCSS=0` with supplied EPS/ES pairs is not an absent stress-strain definition; `FAIL=0.084` is not a timestamp or a demonstrated attained strain; and the reported section's `0.2175` values occupy diameter fields. The EPS/ES instructions require at least two points and a zero first plastic-strain point, warning of extrapolated initial yield otherwise. Blank source fields remain blank/null in the numerical record, even where the manual lists defaults. This source review did not validate the points, confirm element overrides, infer SI units from magnitudes, or calculate effective section properties or mass. Finite parameters are not verified building-specific properties, and a complete selected beam material does not supply missing shell materials.

## Competing readings and resolution tests

- **Missing active definition:** a scoped static finding can establish an unresolved reference in the inspected assembly. Another included definition, documented namespace transform, or materially different assembly would change that finding. A same-original-ID counterpart alone is not a substitute.
- **Connection identity:** shell/discrete topology may be consistent with the published method, but location/geometry and the assignment records must establish a specific connection identity. Numeric labels or apparent color matches cannot do so.
- **Density:** load allocation is an expressly documented alternative to treating every modeled density as physical steel density. It does not prove that a particular value is correct; source units, load budgets and versioned assignments would discriminate.
- **Historical execution:** an authenticated input/include manifest, material/curve definitions, versioned generation records, solver/build record, run header/input echo, and matched initialization/restart/output records would close or contradict specific links. A general build citation or matching mesh count cannot authenticate all of them.

Claims that the missing definitions are identified, that the selected beams are a particular published connection, or that the inspected files establish the historical effective failure law remain **D: underdetermined**. This is a provenance ceiling, not a conclusion about cause, intent, withholding, or the relative ranking of collapse explanations.

## Source pins, coverage and reproducibility

The selected protocol SHA-256 was `4406af3500c495adc95edd1c86e07901f73e6cafa43a39bfc57a8920c34c552a`. Existing public sources were read without alteration and rehashed:

| Source | Local copy / edition | SHA-256 |
|---|---|---|
| NCSTAR 1-9A | `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf`; November 2008 with January 2009 change sheet; 173 pages | `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4` |
| NCSTAR 1-9 | `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf`; November 2008 cover; 797 pages | `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f` |
| M971 | `/private/tmp/lsdyna-keyword-source-review.6f36b5/ls-dyna_971_manual_k-ansys.pdf`; May 2007, Version 971; 2,206 pages | `f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d` |

The earlier thermal-assignment source pass established a fresh official byte match for 1-9A. No new download/official byte match is claimed here. Hashes identify these inspected copies, not historical executable inputs.

Three targeted public searches, restricted to `nist.gov`, were performed:

1. `"NCSTAR 1-9A" "connection" "material"`
2. `"WTC 7" "LS-DYNA" "break elements"`
3. `"NCSTAR 1-9A" "connection" "failure" "curve"`

Final-report publication entries were opened to verify official endpoints. A draft-report result and FAQ were returned but not used as implementation evidence. No modern command reference or new vendor search was used. This closes the finite public search pass.

Discovery searched full 1-9A text for connection/material/failure terms, then input-file/keyword/restart/ID/spreadsheet terms and density/load terms. In 1-9 the first 25 pages and PDF 521-651 were searched for connection-model terms; PDF 606-647 received the narrower provenance-term search. M971 discovery searched the opening 44 pages and PDF 1001-1850 for the relevant keyword headers. Search coverage is not full substantive reading; extraction warnings about rotated text were not treated as negative evidence.

Complete selected text read: **1-9A 54, 59, 67, 73-77, 80, 83-85, 92-93, 100, 103-104, 109-110, 117; 1-9 526, 536-537, 539-541, 600-601, 621; M971 1086-1089, 1502-1504**. Truncated combined outputs were re-read where needed. Full-page visual checks, including figures, tables and footnotes, covered **1-9A 54, 59, 73-77, 83, 85, 100, 103-104, 109-110, 117; 1-9 536-537, 539-541, 601; all seven selected M971 pages**. No graph digitization or quantitative calibration check was performed.

Public-source renders are in `/private/tmp/material-method-source.rQlqbx/`, with exact naming `ncstar1-9a-pN.png`, `ncstar1-9-pN.png`, and `m971-pN.png` for the visually checked page numbers above. Extraction used bundled Python 3.12.14 / pypdf 6.10.0, including layout extraction and whitespace normalization for readable output. Rendering used bundled Poppler 26.05.0 `pdftoppm`, `-f N -l N -singlefile -png`, 95 dpi for the initial 1-9A pages and 105 dpi for 1-9, M971 and 1-9A 103-104. The existing font configuration was `/Users/admin/docs/911/research/sherlock-wtc7-investigation/nist-camera-method-audit/fonts.conf`. Render batches completed successfully without stderr. No source PDF was rewritten.
