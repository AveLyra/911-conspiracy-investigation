# WP3 structural completion and dependency review

2026-09-24. Independent completion reader `/root/completion_structure`.
Research only; not a licensed structural review, source authentication of a
historical run, or cause assessment. Initial findings were sent to root before
reading any other completion-audit report. No other completion report was read.

## Finding

**WP3 is partial, with important completed bounded audits and unresolved
historical/physical dependencies. It is not complete.** The repository has much
more than an animation critique: typed model-input inventories, source-to-part
joins, contact-geometry calculations, calibration and physical-test source
reviews, independent computational checks, and explicit contradictory results.
None of those supplies an independently reproduced building-specific chain from
justified fire exposure to timed failure and global collapse. Nor does that
missing reproduction establish that the historical chain was impossible or
that deliberate removal occurred.

There remains a feasible, finite quantitative source test on already-held public
material: measure the **published seven spring/shell force and energy curve
pairs**, with graphical uncertainty, instead of leaving their mismatch entirely
qualitative. That is a calibration-fidelity test, not a replacement constitutive
law or validation of historical WTC7 failure. It has a lower inferential ceiling
than the paired 3.5/4.0-hour run and residual-restraint tests, which require the
specific dependencies below. Root should compare its value with the remaining
observation and documentary tasks before selecting the next unit.

## Authority and actual coverage

Read main AGENTS.md, WORKFLOW.md, START-HERE.md, the complete main charter, this
unit's SCOPE.md, and the repo-orchestrator, evidence-falsification-auditor and
source-of-truth-guardian skills and routed references. Main is read-only.
Only this new working review is authored. No packet/PDF/image was newly viewed,
source payload acquired, solver installed/executed, source promoted, gate
changed, private record transmitted, or historical model input repaired.

Read the reports in causal-chain-synthesis, common-observable-crosswalk,
material-run-crosswalk, thermal-assignment-trace, thermal-transfer-crosswalk,
connection-calibration-audit, assembly-test-source-audit, c79-restraint-audit,
c79-contact-geometry, c79-casea-spring-audit, c79-member-detail-crosswalk,
c79-original-sheet-review, curve-release-search and uaf-native-case-locator.
Also read main's structural-chain-source-audit.md, structural-bounds.md and
lsdyna-supplement-content-audit/report.md. These are derivative source guides,
not new witnesses. Selected validation/source-reading notes were inspected for
the connection-calibration lead.

Underlying checks went beyond report titles:

- Read the complete elementary `bounds.py` implementation. Its products are
  point-mass work/impact, Euler ratios and gravity-only travel, not a frame load-
  redistribution solution. Verified all six saved output hashes and all three
  code/test/protocol hashes against its saved manifest. The separately authored
  saved review reports 42 idealized cases and 252 visited stages; that review
  was inspected, not rerun here.
- Read `material-run-crosswalk/map_materials.py` lines 75–230: allowlisted
  assembly transform, typed material/part/section extraction, shell-thickness
  row handling, separate beam/discrete selection and unresolved-MID calculation.
  Independently recomputed from the saved full typed registry: 392 used parts,
  23 unresolved-material parts, 19 distinct unresolved effective MIDs and
  16,324 affected shell records. The four saved source receipts say EOF; the
  saved active-delete list is empty. This is a derivative audit, not a fresh
  scan of the four original streams or a general LS-DYNA parser certification.
- Inspected the final material comparison: `PASS_COMPARABLE_SCOPE`, no failures,
  zero numeric difference; coverage includes 459 part-reference rows, 392 used
  part/family rows, 1,904 damage matches, 20 material blocks, 47 part cards and
  24 section blocks. The scope is narrower than every material field in every
  possible run.
- Read the complete `spring_arithmetic.py`. Its historical branch refuses
  unresolved curve dependencies instead of fabricating values. The actual
  primary receipt is `UNRESOLVED_DEPENDENCY`, with 59 available curves and
  **zero historical curve evaluations**. The separate receipt is
  `SOURCE_DEPENDENCY_UNRESOLVED`: all 17 selected chains depend on LCD602 or
  LCD803 and its evaluated curve list is empty. Passing synthetic controls is
  not a historical stiffness/capacity calculation.
- Inspected the exact-contact 120-bit result and independent comparison, not
  merely the word “pass.” Each of three settings retains contact1 classes
  `[2840,28,0,288]` and contact2 `[0,0,0,608]`; these are repeated candidate
  node/face computations. Independently checked all nine saved dependency
  hashes and the array/proof product hashes: all match. The comparison covers
  11,292 pair proofs and 2,226 geometry proofs and explicitly limits its claim
  to the parsed-input geometric surrogate. No exact-proximity implementation
  or physical contact initialization was independently recoded in this review.
- Inspected saved thermal rows and recomputed the selected topology result:
  63 regional nodes each have two unequal assignments and one incident part;
  the later coefficient is lower at 45 and higher at 18. Thus “all repeats
  merely reflect different-part sharing” is contradicted in this selection;
  “all repeats increased heating” is also unsupported. The applicable solver
  processing rule remains unresolved.
- Inspected main's saved supplementary control/curve extraction: active
  termination is 4.50; thermal curve 2 has offset 6.5 with its normalized
  ramp reaching one at abscissa 2. These are recorded input values, not proof
  of runtime continuation or effective nodal temperatures. The early report's
  doubled shell-row count and broad material-substitution inference are not
  adopted over the later typed inventory.

## Requirement-level matrix

States concern charter completion, not probabilities. “Bounded complete” never
means physical/historical validation. Paths below are relative to the
investigation root unless explicitly marked main.

| WP3 requirement | Located evidence and completed portion | Remaining work / state / discriminator |
|---|---|---|
| Map exposure → temperatures | Thermal-transfer report separates FDS/FSI thermal generation, ANSYS load set and LS-DYNA load set; source pins include NCSTAR1-9 printed389/391/457. | **Partial.** No source-field-to-selected-LS-DYNA-row reproduction. D1/D2 below; a verified mapping could vindicate or expose a consequential mismatch. |
| Map thermal expansion/weakening → floor/connection response | Structural-chain SC01; connection-calibration source review; corrected 2012 axial/lateral/seat dimensions; material definitions and selected thermal rows. | **Partial.** Actual installed member geometry, combined loading, temperature-dependent failure and residual bearing remain unjoined. D3/D4. |
| Map floor damage → bracing loss → instability | SC04–SC05; restraint, contact, Case A and member-detail audits retain north seats and Floor14 west attachment. | **Partial.** Candidate topology is established; effective directional restoring force and C79 stability are not. D3–D6. |
| Map redistribution → global motion | SC07–SC09 identify differentiated internal load paths, Truss2 failure, Truss1 nonfailure, perimeter unloading/sway and later buckling. | **Partial documentary map.** No independent force/impulse/propagation accounting; no demonstrated historical dynamic sufficiency. D5/D6. |
| Audit initiation separately from post-initiation replay | Causal-edge ledger and common-observable crosswalk expressly separate fire initialization from computed propagation; UAF prescribed-removal timing separately identified. | **Bounded distinction complete; empirical test partial.** A successful removal replay cannot identify its initiating means or intent. |
| Identify simulated versus imposed/removed/transferred quantities | SC02–SC03; supplementary cards; material active-delete audit; UAF removal and acceleration-function role explicitly separated. | **Partial.** Released gravity-stage text is inspectable; actual continuation and UAF function implementation/calibration remain unresolved. D5/D7. |
| Dimensional and bounded dynamic floor-impact calculations | Main structural-bounds supplies work-energy, first-stop, fixed/pickup cases, collision energy/momentum checks and both toy outcomes. Saved six-table hashes match. | **Bounded elementary work complete.** No floor-specific mass/area, force-displacement, impact distribution, support impulse or debris trajectory. D6; toy eight-target counts are not eight real floor predictions. |
| Energy absorption | Same code explicitly retains gravity work, resistance work and pickup loss without skipping an earlier stop. Connection studies distinguish shape from accumulated energy. | **Partial overall.** No global/cascade kinetic/internal/contact/fracture/hourglass energy audit. Native outputs and compatible accounting needed, D5/D6. |
| Bracing length / buckling calculations | Euler scaling tested; direct/contact topology and retained support classifications independently reconstructed. | **Partial.** No building-specific nonlinear C79 stability calculation with directional springs, splices, imperfection and axial-load history. D3/D4/D6; one guessed K is not a substitute. |
| Load redistribution calculation | Source descriptions and force-law requirements are mapped; elementary script has no frame/transfer-structure equilibrium solver. | **Incomplete in the reviewed implementation.** No actual quantitative redistribution calculation located in this structural selection. Source-pinned reaction histories and independent equilibrium/impulse checks are the first step, D5/D6. Do not claim whole-repository absence. |
| Propagation times | Gravity travel examples and reported model/event timing comparisons exist; common crosswalk retains west-penthouse mismatch. | **Partial.** Gravity drop time is not a stress-transfer or failure clock. Need member-specific causal dependencies plus native histories and independently matched observed events, D6/D8. |
| Geometry and drawings to primary records | Diagnostic→set→PID mappings for C44/76/79; typed mesh and existing reduced drawing/source depictions. | **Partial.** No applicable complete original-sheet/installed-condition/member-to-element join for selected seats or Floor14 west attachment. D3; pending acquisition is not failed access. |
| Materials, connections and failure criteria | Material registry, selected MAT024 and spring cards, calibration/assembly source reviews, displayed-ratio checks. | **Partial.** 19 effective MIDs unresolved; LCD602/803 absent under declared searches; exact connection grouping/calibration and heated/post-ultimate applicability unverified. D4/D9. |
| Boundary/contact conditions | Six selected contact definitions and control fields; exact candidate geometry and qualified rigid base/substation/WT model descriptions. | **Partial.** Realized ties, untied warnings, stiffness, slip and surviving response not recovered. Numerical geometric precision does not fix physical state; D3/D5/D6. |
| Solver versions and thermal fields | Reported mpp971dR4 beta revision41161, double precision; May2007 Version971 manual; destination nodal thermal file and large June load corpus. | **Partial.** No authenticated historical executable/input echo/duplicate-load behavior; no thermal-generation closure. D1/D2/D5. |
| Handoff and output/render provenance | SC02–SC03 and static delete-list joins; NIST clock/reference distinctions and UAF screenshot names documented. | **Partial.** No complete output-to-run/input/build/render crosswalk or conserved state/energy transfer. D5/D7/D8. |
| Attempt genuinely available reproductions; do not guess withheld choices | Multiple independent source/geometry/arithmetic readers, controls and failures preserved; no substituted curves/materials or falsely runnable collapse case. | **Bounded implementation checks complete.** No claim that a full physical reproduction was performed. An exact historical reproduction is dependency-limited, not a reason to call all models unavailable. |
| Alternative inputs; collapse AND non-collapse, reaction forces, energy, residual support, failure sequence, warnings | Toy grids have both outcomes; source account supplies 3.5-hour stable-at-end versus 4.0-hour collapse; exact geometry compares three diagnostic extensions. | **Incomplete building-specific sensitivity.** No authorized/native paired run audit or independently justified intermediate histories; no complete reaction/energy/warning outputs. D5/D6. Fixed geometric extensions are not collapse alternatives. |
| Assumption/dependency ledger and common-observable comparison | Causal-edge ledger, detailed dependency reports and five-feature NIST/UAF source crosswalk exist. | **Partial exit.** The source comparison is complete within its fixed pages but not an executed same-feature/same-camera/same-clock residual test. D8. |
| Separate numerical verification, physical validation, calibration and historical identification | Reviewed reports generally preserve these distinctions; original Thompson experiments strengthen empirical background while exposing mismatch/fit limits. | **Bounded discipline present.** No competent independent structural/forensic approval is located by this review; AI agreement cannot fill it. |
| Each infeasible material test: precise dependency and result changing assessment | D1–D9 consolidate actual file/version/record/expertise boundaries below. | **Partial, improved by this audit.** Dependencies do not assert what missing results would be. Feasible published-curve measurement remains unperformed. |

## Q02, Q06 and Q10 disposition

- **Q02 — modeled fire inputs versus independent evidence: partial.** This
  review covers the structural thermal-transfer branch, not the complete WP1
  visibility/input audit. Organized loads and destination coefficients are
  present; generation, repeated-load processing and downstream effects remain
  unverified. No conclusion about exaggerated historical temperatures follows.
- **Q06 — localized initiation to rapid widespread loss: unresolved
  building-specific sufficiency, with a substantial mapped candidate chain.**
  Regional floor failure, direction-specific residual support and differentiated
  exterior response are the actual published propositions. There is no verified
  time/force/energy chain here demonstrating or excluding them. The reported
  non-collapse state and retained supports are necessary contrary evidence.
- **Q10 — modeling and tool dependencies: substantial bounded completion, not
  global completion.** Exact missing references/build and candidate drawing/run
  identities are known. The gap is not a generic lack of all model data. Future
  evidence can change a dependency finding without validating historical cause.

## Exact dependency ledger and outcomes that matter

| ID | Needed record/test, not merely “more data” | Present status and consequential outcome |
|---|---|---|
| D1 | Actual WTC7 thermal-result→LS-DYNA exporter/mapping chain: upstream field/time, destination IDs, coordinates/units, component selection, ties/repeats, serialization and invocation matched to SRC118 `WTC7_CaseB_400pm.int.gz`. | Unidentified after finite June/September lexical audits; eight literal APDL .apdl dependencies unmatched. Reproduction of selected rows would strengthen input provenance; a reproducible mismatch would identify what needs physical sensitivity testing. Do not assume the tower predecessor algorithm. |
| D2 | Applicable repeated LOAD_THERMAL_VARIABLE_NODE behavior for reported `mpp971dR4 beta revision41161`, plus run input echo/warnings/effective nodal temperature histories. | Version is source-attributed, not executable-authenticated. A first/last/sum rule cannot be chosen by convenience. Effective values could resolve the 63-node ambiguity in either direction. Licensed/expensive execution and expert engagement require approval. |
| D3 | Applicable original erection/fabrication/modification details and location-specific photos, then installed-state→mesh transform and exact seat/clip/stud/west-attachment element mapping. | C44-C79 Floors8–12/14 and C79-C76 Floor14 unresolved; Floor13 E12/13→A2001/A1091/A1370 and 9114 are leads, not universal details; S-8-10 modifications require separate treatment. Named FOIA11-209/12-009 drawing packets remain approval-pending; denied TIFF route remains denied. Agreement could narrow omission criticisms; disagreement requires controlled response sensitivity, not an automatic collapse verdict. |
| D4 | Effective master-region MID definitions and specific LCD602/LCD803 definitions plus original connection location/group/capacity/calibration crosswalk. | 23 parts reference 19 unresolved effective MIDs; +1000-namespace counterparts are not authenticated replacements. Selected spring cards exist but force curves do not in the finite checked inventories. Authentic definitions permit the already-declared diagnostics; by themselves they still do not give historical force histories. |
| D5 | Exact input/include/continuation/restart/run/build package, applicable 4.0/4.1-hour damage linkage, CaseA role, D3HSP/input diagnostics, contact initialization/untied warnings and actual output identities. | Supplied active deck stops at4.50; thermal ramp later; damage hooks inactive. Supplied4.0 versus referenced4.1 and separate unused CaseA cannot be silently harmonized. Proper closure could enable reproduction or reveal a real run mismatch. No native collapse results were produced by the reviewed audits. |
| D6 | Paired3.5/4.0-hour runs and coherent intermediate states: regional failed area/mass, impact/contact impulse, receiving-floor work capacity, retained deformation/stress/velocity, member reactions, C79 axial load/section/splices/imperfections/directional restraints, Truss2 control and energy/warning histories. | Published3.5-hour state is stable at end, not indefinite stability. No independent paired reproduction. A credible retained-support/arrest result challenges robustness; robust failure matching observations strengthens the specified mechanism. Requires authenticated inputs, approved resources and competent engineering review. |
| D7 | UAF final Figure4.17–4.20 native `Penthouse49`/`ACASE2` case/member/version crosswalk, both height bands, acceleration/resistance function definition AND assignments AND derivation/calibration record, removal schedule and unaltered NW-point output. | Held ZIP is README wrapper, not native models; bounded locator complete, underlying case unresolved. Different input/function roles or documented fitted targets materially change interpretation of the apparent match. Do not retry denied aggregate routes or treat access difficulty as a scientific flaw. |
| D8 | Named same physical features, native coordinate/time outputs, camera projections, clock joins and visibility rules for five common observables; no per-feature retiming. | Source crosswalk, not full reproduced comparison. NIST west-penthouse damaged-case differences are attributed−2.4/−2.0s, with exact event/view uncertainty unresolved; UAF onset is not the same endpoint. A real incompatible fixed-case residual can reject that implementation without proving another cause. |
| D9 | Exact2008 Sadek paper/inputs and relevant original test data; Thompson synchronized channels, event selectors/normalization/rotation reduction and TN1749 case membership; historical WTC7 parameter transfer and relevant heated/composite/multiaxial validation. | Original2009 apparatus/methods recovered; channel reduction and later pairing unresolved. No contact/outreach authorized. Better tests may strengthen or weaken constitutive fidelity; neither later publication nor a good fit establishes contemporaneous historical use. |

## Highest-value currently feasible WP3 source test

The native paired-collapse and residual-restraint tests have the highest causal
value but presently need D3–D6. A smaller **genuinely feasible** test can quantify
a still-qualitative input to those questions without substituting for them:

1. Create a **new prospective unit**, preserving the earlier no-digitization
   protocols. Fix inclusion to all seven 3–9-bolt spring/shell pairs in
   NCSTAR1-9A Figures3-4/3-5, physical PDF76 / printed25, with PDF73–75 as method
   context. Do not select only the visibly discrepant seven-bolt pair.
2. Rehash the already-held public PDF. The cited temporary render
   `/private/tmp/material-method-source.rQlqbx/ncstar1-9a-p76.png` is **not
   currently present** (read-only existence check this review). A new bounded
   full-page render is needed under the PDF skill; this is not a new source
   acquisition or permission to open pending drawing packets.
3. Before curve extraction, fix axis registration, colors/dash identification,
   pixel/line-width envelopes, curve-crossing/occlusion rules, source-domain
   coverage and independent annotation. Include an explicit unreadable status
   if the PDF cannot support reliable separation; do not interpolate missing
   identities or silently treat a graphical digitization as raw solver output.
4. Compare force differences at common displacement and accumulated work over
   the jointly observable domain, retaining local sign changes, terminal-domain
   mismatch and uncertainty. Test integrated force against the separately shown
   energy figure only after confirming units/normalization/event definitions.
   This checks the published calibration, not absolute physical truth.
5. Outcomes that matter: robust local-force disagreement despite similar energy
   would quantify the known calibration limitation; agreement within graphical
   uncertainty would narrow that criticism; inseparable curves would produce a
   precise request for original paired numeric arrays. None alone determines
   whether the difference changes global failure or historically occurred.

No graphic was viewed or digitized in this completion review. The first safe
execution action is the protocol/coverage declaration followed by fresh source
hash verification and full-page render. It requires no new paid service, solver,
outreach, private payload or legal promotion. It does require actual independent
measurements and a subsequent bounded numerical review; an AI “looks similar”
judgment is not the acceptance criterion. The exact-2008 paper and withheld
native law remain separate dependency questions, not prerequisites for measuring
what the published calibration figure actually shows.

## Verification record and pins

Commands actually run were read-only `sed`, `rg --files`, bounded `rg -n`,
`wc -l`, repository intake, and `python3 -B` JSON/schema/arithmetic/SHA checks;
all substantive checks exited0. The material/thermal recomputations and
9-input/2-product contact hash checks are described above. No old expensive
geometry calculation, completed solver test or complete source-stream scan was
repeated merely to create activity. Combined read outputs truncated on several
calls; affected controls, material report, structural-source opening and contact
report opening were reread separately. A broad spring-result print was redundant
and truncated; the decisive 17-chain/zero-curve/dependency values were reread
through allowlisted fields. That was technical derivative data, not new private
source disclosure.

Paths beginning `MAIN/` below are relative to main's investigation root;
others are relative to this worktree's investigation root. Hashes record the
current evidence snapshot, not independent historical authenticity.

| Artifact | SHA-256 |
|---|---|
| causal-chain-synthesis/report.md | `3ab4479ab789d204ebd1760aac97191b5ac90fbf69756cb66e76c9657a947269` |
| common-observable-crosswalk/report.md | `952628e3fbb405f2a9f05af09546f876a567a5c9975da21442de7a74c26e6024` |
| material-run-crosswalk/run01.json | `b69c12ec0668c9bdf5f5ea59dbf483d2a959de7bd477c172efe69c2f03e33594` |
| material-run-crosswalk/independent-comparison03.json | `da3bf4338cc6ab1134207609b66d22db31687bfbe410fc578230009e8ee6dd02` |
| material-run-crosswalk/map_materials.py | `dede959bc9f440b6b0bab8784e8c8b7c7a461cd7bcfef820487b3ff2538bc469` |
| thermal-assignment-trace/run01.json | `54f20f57b06948f95a1ad8d384fd5f8a1778c0a6c0d2d8966efa139addac13ae` |
| thermal-transfer-crosswalk/report.md | `3c5fef1f646e0179e3badfd4f0a4d8e1128deae5060e6054e84cf86b93ae374d` |
| c79-casea-spring-audit/spring-arithmetic01.json | `20ef34c949bf6721f2c2c39b571b73bd2a3520cb2b2197d3d2a1381ac4d8ae95` |
| c79-casea-spring-audit/independent-spring-arithmetic01.json | `4feec116a86871cf5168e17daf4a0477d0bf2ccb8faf2d6187f8370ac36a09d7` |
| c79-casea-spring-audit/spring_arithmetic.py | `8e2ed43c3dacfa56bd096475eafad70e92e45a6b38672f09ce86bbe56513e92b` |
| c79-contact-geometry/exact-proximity120.json | `ec72208fb65f7a849efebae77af5c834c4eb17e1180dddca2f1a17fb525d0711` |
| c79-contact-geometry/independent-exact-reference120-root01.json | `5535deca74b1eed2c187a58a77c892e7b34ad206ec6b92ca82aea8015a91b4ef` |
| connection-calibration-audit/report.md | `9b4d9c4b6a3a54b2abb4d1751fbc46d325d7ea981f76c832425c293c03c6e1ff` |
| assembly-test-source-audit/report.md | `e0d12644ba8cc3037705c9bc19baa08a78e522e8b44a6e655739aac75a7f68be` |
| c79-member-detail-crosswalk/report.md | `54326664ec394421ae7894c3a634c417a03bddbd8facdde15a07800a6d0d000a` |
| c79-original-sheet-review/report.md | `1f7805337632f0f3b03b399cb64dd54d27a3d48bce3f5ba69dc2caf876bbb53c` |
| curve-release-search/report.md | `e186fc2fe9d532809f58f13459a54fed72ee4117244c29d0c54752de8b6b3ca8` |
| uaf-native-case-locator/report.md | `c744f9d047d0c67f8f5de6e4168e41ef286c88bccbfd9d63223dca2c8ae21d0a` |
| MAIN/structural-chain-source-audit.md | `7ae495511780584a9c87d9ed9527ee593fae221e9c3a6b7a9927003007d2c06c` |
| MAIN/structural-bounds/bounds.py | `d3af3a004d7d555241c78dee13597005a675da505dc6254914fbe024dd9beec0` |
| MAIN/structural-bounds/run-v1/manifest.json | `c277e0d34a34945e8fa8974f7af8eceb223e715746ca41cc05ca362be776b96d` |
| MAIN/structural-bounds/main-review.json | `a27beffff1b138af051dfb575096a0bcaff0f5873a3b3cb58a53a8efa4b16cb9` |
| MAIN/lsdyna-supplement-content-audit/inventory.json | `391b13a37df24c9b2c987d0e1d03bf27513bd718fa3fecd168a95f614104dbf3` |

No claim of full coverage of every structural file follows from this selection.
Root must integrate this review with WP1/WP2 observations, comparator and
documentary work, the competing-hypothesis ledger and final critical review.
There is no new cause ranking, expert approval or completion finding.
