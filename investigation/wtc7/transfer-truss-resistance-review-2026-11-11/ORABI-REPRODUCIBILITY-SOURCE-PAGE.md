Research date: 11 November 2026.

**The software search has advanced, but an authenticated WTC 7 rerun remains blocked by missing case inputs and reference outputs.** A public author release, the complete doctoral thesis, and a component example with outputs are available. They support a reproducibility program; they do not complete the structural calculation linking the proposed transfer-truss failure to the observed roofline.

The decisive next step is to recover or independently reconstruct the case, then test connections, upper-floor load redistribution, and the transition into real-time dynamics under independently justified assumptions. No matched structural run was performed in this review. The findings do not establish a probability ranking between competing causes.

# What the public search recovered

| Material | Verified status and significance |
|---|---|
| [Orabi accepted manuscript](https://ira.lib.polyu.edu.hk/bitstream/10397/92640/1/Orabi_Collapse_World_Trade.pdf) | Downloaded and text-extracted, 29 pages. Provides methods and selected outputs. |
| [Complete doctoral thesis](https://theses.lib.polyu.edu.hk/bitstream/200/11622/3/6151.pdf) | Downloaded and text-extracted, 198 PDF pages: 12 preliminary pages and 186 numbered pages. Printed page + 12 gives PDF page. No appended runnable case or embedded attachments found. |
| [Author release 3.2.3](https://github.com/Anwar8/MyOpenSees/releases/tag/3.2.3) | Windows executable downloaded; matching source tag identified. A thesis-linked candidate, not authenticated as the precise binary behind every journal figure. |
| [Simply supported slab example](https://openseesforfire.github.io/Subpages/Examples/Simply-plate.html) | Downloaded package contains Tcl input, temperature data, a separate executable, and reference outputs. Useful for component verification. |
| [Project acceleration-transition audit](https://github.com/AveLyra/911-conspiracy-investigation/blob/main/investigation/wtc7/acceleration-transition-test/report.md) | Full current text retrieved. Preserves the limits of the published-position analysis. |
| WTC 7 model decks and figure-linked outputs | Not located in the inspected branches, releases, selected archives, or institutional records. |
| [Torero 2010 litigation report](https://nsarchive.gwu.edu/sites/default/files/2022-01/Aegis%20-%20Colaco%20and%20Torero%20Expert%20Reports.pdf) | Original document located in a public mirror; indexed passages inspected. A completed local retrieval was not confirmed; web readers hit size/time limits. No complete numerical cross-comparison is claimed. |

The [publisher record](https://link.springer.com/article/10.1007/s10694-022-01225-2) dates the article online to 15 March 2022 and assigns it to Fire Technology 60, 2963–2990 in 2024. These are versions of the same DOI, not independent studies. The 2020 conference contribution and the 2010 Torero work are antecedents in the research lineage. Shared authors, assumptions, and sources must be carried into any assessment of independence.

# What the published cases establish

| Feature | Documented condition or result | Accepted-manuscript pages |
|---|---|---|
| Extent | Model 2: nine slabs, Floors 6–14; columns through Floor 15 | 16, 21 |
| Connections | Fixed joints; rigid, nonfailing shear-stud links | 13 |
| Heating | Upper-floor fires omitted | 16 |
| Protection comparison | 22 mm protected diagonals survived the tested three-hour exposure; bare diagonals failed | 17–20 |
| Motion | Approximately 0.8 m local floor deflection in two seconds | 21–22 |
| Termination | Computation stopped at 2.3 of five planned dynamic seconds for runtime/output limits | 21 |
| Proposed extension | Connection failure and global propagation require further modeling | 23–25 |

Source: [accepted manuscript](https://ira.lib.polyu.edu.hk/bitstream/10397/92640/1/Orabi_Collapse_World_Trade.pdf).

**Computational termination is not physical arrest.** The published endpoint cannot establish either eventual stabilization or eventual total collapse. Similarly, local floor displacement cannot be relabeled as a roofline trajectory. Calculating acceleration from two displacement/time numbers would introduce an assumed motion law and initial velocity.

The protected case is a meaningful negative control within the tested scenario. It also shows why “underprotected” cannot be treated as a measured historical condition or a known failure threshold: the endpoint comparison does not establish the response at every intermediate coating thickness. The proposed mechanism remains conditional on the exposure, protection, restraint, and load paths that actually existed.

The broader interpretive limit is symmetrical. A partial fire model does not demonstrate the complete event. Its incompleteness also does not establish that a complete fire-driven sequence is impossible, or that a specified alternative caused the collapse.

# What the thesis adds

The thesis names OpenSees for Fire 3.2.3, the GiD thermomechanical interface, and a parametric runner as public software (printed p. 5; PDF p. 17). It acknowledges unknown actual Truss 2 connection details and discusses several possible explanations for protected-truss survival, including structural robustness and model limitations (printed pp. 163–164). A deliberately weaker W33×118 diagonal demonstration is not an as-built WTC 7 result.

Printed p. 173 limits the structurally meaningful portion of its accelerated-heating run to about the first 30 minutes, before subsequent dynamics require different treatment. Printed pp. 183–185 leave realistic connection behavior and larger propagation calculations as development work. The thesis therefore adds methods and qualifications, rather than the missing complete collapse calculation. [Full thesis](https://theses.lib.polyu.edu.hk/bitstream/200/11622/3/6151.pdf).

# The thermal to dynamic transition needs verification

The article compresses one hour of Model 2 heating into 0.36 solver seconds, then switches to unscaled dynamics. Its reported Rayleigh coefficients are not percentages of critical damping. [Manuscript, pp. 15–16](https://ira.lib.polyu.edu.hk/bitstream/10397/92640/1/Orabi_Collapse_World_Trade.pdf#page=15).

This is an audit question, not a demonstrated numerical error. Quasi-static loading can be appropriate while a structure follows stable equilibrium. Freezing temperature during a few seconds of rapid motion can also be reasonable. But accelerating the applied thermal history does not automatically preserve the effects of inertia, damping, creep, instability, or stored energy.

A defensible continuation must preserve the state that produced it. At the switch, the required record includes displacement, velocity, acceleration, member stress, damage, contact state, kinetic energy, internal energy, damping, and any reset operation. The result should be compared with slower numerical heating and with transition times tied to the onset of instability.

Model 1's first diagonal failure need not be Model 2's global instability, because added floors alter redistribution. The decisive test is whether an admissible pre-collapse state and subsequent motion persist when numerical choices change. Without the input decks and state histories, the published settings do not reveal the size or direction of any numerical bias.

# The mechanical room fire remains a historical condition to establish

NIST's original fuel-system report documents a pressurized Salomon Brothers loop and says a supply-line break could keep discharging while pumps operated. It also leaves material details unresolved: whether one or both tanks supplied the pumps, the purpose and action of a collecting-tank switch, possible leak shutdown, and electrical behavior. Its 12,000-gallon storage figure is capacity under stated assumptions, not measured fuel burned. [NCSTAR 1-1J, printed pp. 46–48; PDF pp. 80–82](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=101010#page=80).

NIST's [FAQ, question 19](https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation) gives its contrary assessment: insufficient duration or heating, and predicted smoke it says was not observed. The same answer distinguishes recovered fuel from the unknown fate of fuel in the day tanks and the two 6,000-gallon tanks. The small residual associated with recovered fuel should not be used as a demonstrated limit on the separate Salomon system.

These records support a physically specified scenario and identify evidence against it. They do not resolve where any unrecovered fuel went. Nor does smoke color alone determine fuel identity, burning rate, ventilation, or exposure of a particular truss.

The causal test needs a joined history: supply and pump operation, breach location, compartment boundaries, ventilation, burning rate and duration, heat transfer, and the protection actually present on critical members. A standard hydrocarbon curve supplies an assumed exposure for a feasibility calculation; it does not recover that history.

The [2010 Torero report](https://nsarchive.gwu.edu/sites/default/files/2022-01/Aegis%20-%20Colaco%20and%20Torero%20Expert%20Reports.pdf) begins at appellate case 11-4403, Document 75-2, page 8 of 58, stamped JA-2897. Its original case files and protected-case thermal assumptions are a useful comparison target. The protected-case comparison remains unfinished; no difference in outcome is asserted here without that comparison.

# Experimental evidence for the connection extension

Choe and colleagues tested four 12.8 m composite beams with different connections and slab continuity. They observed weld or bolt failure during heating or cooling, with strong effects from restraint. This supports testing force and rotational demand alongside temperature-dependent strength. It does not supply WTC 7 connection capacities or demonstrate propagation through a complete building. [Choe et al. 2020, publisher abstract and original manuscript](https://ascelibrary.org/doi/10.1061/%28ASCE%29ST.1943-541X.0002627); [author manuscript](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=928766), pp. 17–18, 22–24.

Dai, Choe, Fischer, and Clifton's full-floor experiment provides a particularly useful paired test. A simplified calculation predicted bolt failure at connection C2 that was not observed, while connection C6 developed partial bolt ruptures despite a simplified survival prediction. Restraint, rotation, slab cracking and connection geometry mattered. The paper explicitly distinguishes its inferred axial forces from measured strains and displacements, recommending the latter for model validation. [Fire Technology, DOI 10.1007/s10694-023-01452-1, §§4–5 and Appendix A](https://link.springer.com/article/10.1007/s10694-023-01452-1).

A connection model should reproduce both kinds of result before its parameters are transferred, with justified differences, to WTC 7. Merely lowering an assumed strength until collapse occurs would not establish the proposed mechanism. Conversely, insisting that all joints remain ideal would exclude the very mechanism under examination.

# Resistance and the Korol energy challenge

Korol, Heerema, and Sivakumaran estimate 309.1 GJ of potential dissipation against 75.7 GJ of gravitational energy. Their concrete particle-size distribution is acknowledged to be an estimate: half the mass in 100 mm chunks, the remainder split among seven smaller fractions. The column treatment uses representative sections and specified folding assumptions. [Original paper, pp. 27–30](https://www.challengejournal.com/index.php/cjsmec/article/download/50/41).

From their rounded totals, the concrete contribution is 218 + (45.6 − 13.56) = 250.04 GJ, or about 80.9% of the 309.1 GJ total. This arithmetic identifies a dominant assumption; it does not independently validate or invalidate the fragmentation model.

The relevant distinction is between a structure's available energy-absorption capacity and the work that a particular failure path must actually perform. A gravity-collapse exclusion requires the proposed deformation and fragmentation work to be unavoidable along the admissible path. The actual debris distribution, fracture process, timing, and column deformation therefore matter.

The reciprocal requirement is just as strong: a simulation cannot answer the challenge by silently deleting the mass, momentum, stored energy, or resistance of failing components. It must account for the work and energy its own sequence requires. Total-energy feasibility and agreement with a short roofline interval are separate tests; success on either alone does not establish the other.

# What the roofline record can test

The [project acceleration-transition report](https://github.com/AveLyra/911-conspiracy-investigation/blob/main/investigation/wtc7/acceleration-transition-test/report.md) tests published positions from Chandler, Walter, and Szamboti, not freshly calibrated original footage. On its declared grid, abrupt acceleration fits three points slightly better, while a finite ramp fits the fourth better. Every tested family requires more allowance than printing precision alone. The report does not infer a physical transition duration or a building-wide force history.

The [underlying method audit](https://github.com/AveLyra/911-conspiracy-investigation/blob/main/investigation/wtc7/multipoint-table-reproduction/method-review.md) preserves the 0.2-second sampling, missing processing/calibration details, and dependence of four points on one camera chain. These constraints do not erase rapid descent; they determine which sharper claims the data presently support.

NIST's event table uses east-penthouse descent as its zero. Its separate roofline analysis uses perceived roofline motion as zero. Those clocks must be joined explicitly. Selected entries from [NCSTAR 1A, Table 3-1, printed p. 43; PDF p. 85](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861610#page=85):

| Event | Observed seconds | Model with debris damage | Model without debris damage |
|---|---:|---:|---:|
| East penthouse disappears | 2.0 | 2.4 / 2.7 | 2.3 / 2.6 |
| Eastern north roofline begins descending | 6.9 | 6.3 | 9.8 |
| East screenwall disappears | 8.5 | 7.3 / 7.7 | 8.7 / 9.2 |
| West penthouse disappears | 9.3 | 6.9 / 7.3 | 10.6 / 10.9 |

Paired predictions represent different viewpoints. These are comparison targets, not evidence of an exact timing match.

NIST reports about 32 m of travel during its 1.75–4.0-second gravitational-acceleration interval. The often-computed 24.8 m assumes rest at the interval's beginning, which is inappropriate for a roofline already moving. Its assignment of earlier small east–west motion to hidden floor failures is interpretation rather than direct interior footage. [NCSTAR 1A, printed pp. 42–46](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861610#page=84).

A meaningful comparison should project simulated visible points into each camera, preserve uncertainty in geometry and timing, and compare the entire event sequence with one justified alignment. Roof-point acceleration cannot be inserted into a whole-building force equation without demonstrating that the tracked point represents the mass and motion assumed by that equation.

# Audible and visible consequences

The mechanism must predict the observables used to test it. Hidden floor movement may produce externally visible changes, but assigning a particular window or façade motion to a particular internal break requires a structural calculation and visibility assessment.

An acoustic exclusion needs original audio covering the predicted interval, recording gain and clipping behavior, distance and propagation delay, obstructions, background noise, and a physically justified sound source. Conversely, an unexplained sound does not identify its mechanism merely by temporal proximity. No calibrated acoustic comparison was performed here; the missing inputs do not establish either audibility or silence of the proposed sequence.

# A matched test that can change the assessment

| Stage | Required result | Material failure condition |
|---|---|---|
| Reproduce the published baseline | Recover both case decks, exact dependencies, reference histories and figure mappings | Results cannot be reproduced within specified numerical tolerances |
| Validate connection behavior | Predict surviving and failing independent experiments with their actual restraints and heating | Parameters only succeed after fitting to the desired building outcome |
| Establish the historical scenario range | Bound fuel, protection, fire exposure, geometry and loading from records | A necessary condition conflicts with reliable event-specific evidence |
| Verify transition into dynamics | Preserve mechanical state and energy; test heating rate, handoff time, damping and step size | Propagation depends on unexplained resets, energy, or numerical settings |
| Represent the roof and façade | Include sufficient upper-structure stiffness, bracing and mass to predict visible features | Truncated boundaries determine the result or required observed features cannot be produced |
| Compare held-out observations | Use fixed camera calibration and alignment; predict multiple positions, shapes and event times | Fit requires separate arbitrary time shifts or unsupported synchronized removals |
| Retain the full ensemble | Preserve stable, partial, propagating and numerically invalid outcomes | Only successful-looking cases survive reporting |

The minimal recoverable package should contain geometry and node/element identities; section and material assignments; gravity and mass definitions; fire and heat-transfer inputs; connection/contact laws; boundary conditions; solver source/build and dependencies; numerical controls; transition checkpoints; all termination logs; and outputs mapped to published figures. File counts or rendered animations cannot substitute for that correspondence.

If the original cases remain unavailable, an independent reconstruction is possible in principle. It should be labeled as such, with uncertain inputs exposed. A successful reconstruction would add feasibility evidence, while exact reproduction would answer a different question about the authors' published calculation.

The strongest positive outcome would be an independently calibrated model predicting several unused observations with physically admissible parameters and satisfactory mechanical checks. A single tuned animation would be weaker evidence.

The strongest negative outcome would be a necessary historical condition ruled out, or well-supported variants repeatedly unable to produce required observations without unsupported intervention. Failure of one pathway should be attributed to that pathway. Identifying an alternative cause still requires its own positive evidence and predictions.

The [current project causal assessment](https://github.com/AveLyra/911-conspiracy-investigation/blob/main/investigation/wtc7/causal-chain-synthesis/report.md) withholds a comparative cause ranking. This review supplies additional tests and source detail without reinstating an earlier ranking.

# Software and repository audit

The downloaded [3.2.3 release](https://github.com/Anwar8/MyOpenSees/releases/tag/3.2.3) is 15,619,584 bytes, with source tag resolving to commit `0e88c261b7bc4b0846a1ff3db964f06fcefa22a1`. Release notes identify changes to thermal-insulation functions and layered-section recording. Those details make software provenance consequential.

The author's later [3.2.8 assets](https://github.com/Anwar8/MyOpenSees/releases/tag/3.2.8) distinguish calcareous and siliceous concrete variants. The [general fire-software download page](https://openseesforfire.github.io/download.html) instead advertises a base-3.0 Windows build with Tcl 8.6. Interchanging these builds requires verification of the needed commands and material behavior.

The acquired slab example has its own `OpenSees_withLITS.exe`, `example6.tcl`, `temp.dat`, and output histories including `midNodeU3.out`. It supplies a useful component-level starting point, not the WTC 7 building model. [Example and package link](https://openseesforfire.github.io/Subpages/Examples/Simply-plate.html).

| Public repository or branch | Returned tree entries | Scope of negative result |
|---|---:|---|
| Anwar8/MyOpenSees master | 5,008 | No WTC7-named case input/output path located |
| Anwar8/MyOpenSees 3.2.3 | 5,006 | Versioned solver, no identified WTC7 case package |
| Anwar8/gidopensees master | 412 | Full archive also searched; WTC7 hit was a thesis/material citation |
| Anwar8/gidopensees parametric_manager | 409 | No WTC7-named case path located |
| Anwar8/OSPCR-MP master | 21 | Generic parametric runner; archive searched |
| Anwar8/Temperatures_Interpolater master | 36 | Slab-experiment temperatures, not identified WTC7 heating |
| Anwar8/Blaze main | 551 | Generic solver and examples; no WTC7-named case path located |
| OpenSeesforFire website master | 278 | Documentation, software and examples |
| OpenSeesforFire OpenSees-SRC | 5,372 | Fire-specific solver source |

All returned recursive inventories reported that they were not truncated. Repository links: [author](https://github.com/Anwar8), [fire-software repository](https://github.com/OpenSeesforFire/openseesforfire.github.io).

The GiD and OSPCR source archives were searched internally for WTC7, World Trade, Truss 2, and Column 79. Selected generic example archives were inspected too. This search did not cover every historical commit, fork, deleted asset, private repository, or compressed package. The correct conclusion is “not located within the inspected material.”

Stock OpenSees contains thermal capabilities, and its official documentation provides a [component removal command](https://opensees.github.io/OpenSeesDocumentation/user/manual/misc/remove.html). These capabilities do not establish equivalence to the paper's modified implementation. A removal command also does not supply a validated failure criterion, debris contact, or mass/energy treatment.

The session environment had no OpenSees command on PATH and no installed OpenSeesPy module. This was an observation about this research environment, not the user's Mac. No executable was run.

Two adjacent publications were checked for a completed extension. The [2022 integrated-framework paper](https://discovery.ucl.ac.uk/10139972/1/Orabi-Uploaded.pdf) demonstrates Cardington modeling and points generally to GitHub software; no WTC 7 case package was located in that manuscript. The [2023 load-redistribution paper](https://research.polyu.edu.hk/en/publications/reconstruct-the-3d-load-redistribution-paths-of-framed-structures/) describes an eight-story Cardington-based structure with local column failure and multi-floor fire. The latter was checked through its institutional abstract and indexed publisher introduction; full journal text was not acquired. These are useful methodological developments, not a completed WTC 7 roofline comparison.

# Search limits and retained source identities

Exact-title, DOI, author, dataset, supplementary-material, GitHub and Zenodo searches located the paper, thesis and generic software. The [coauthor publication list](https://www.limingjiang.net/Publication/) includes 2026 work but did not identify a completed WTC 7 roofline comparison. This is a bounded search result, not proof that no later or private work exists.

Crossref, DataCite and public-gist API checks did not finish before the workspace became unavailable and are not counted as negative searches. The supplied Mac-only model-access-audit path could not be reopened. The public motion audit and causal synthesis were retrieved directly instead.

The downloaded primary files and software were acquired before the workspace outage. Their hashes below record the bytes inspected; they do not authenticate unpublished model provenance. Raw downloads could not be packaged for delivery after the outage.

The following SHA-256 values identify the acquired bytes. File names are descriptive labels.

```text
PolyU accepted manuscript — 10,032,966 bytes
10bd6bcd03a41b2c687140a81ccabe2346e1091a7d050a8d04732e4a438bfc81

Orabi thesis — 12,112,438 bytes
f158532d5300295ad7ae5389274ca961b506f61b3543f095b7abdea2508e12b9

Author OpenSees 3.2.3 executable — 15,619,584 bytes
faca02cf35f9de508c3721bc655a4c9d2d99e1c40abfb9bebb91e583cae54437

GiD source archive — 19,037,408 bytes
bfd8ee8e3adcdf442471746690884ba62f2922cb577d5e40df7f54d1b26f2409

OSPCR source archive — 56,302 bytes
034d2ffe3e4aa63b2df118314c00d139ee33a6062c08b5fb12c9e477a9f900ce

Simply supported slab archive — 5,971,580 bytes
7bc74a6987f687b79f542a6bdebb8e60575e23f770e038464c0a801025a74d9c

Project acceleration-transition report — 10,550 bytes
7e6a1cc28b4b8d1bd8f5cb0759ced9a6d450c740ee300e90b3439e17add4275a
```

# Priority records still needed

The most consequential missing items are the authors' two exact WTC 7 input/output packages; their transition-state records; the actual transfer-truss and upper-floor connection/protection details; the underlying fire/ventilation models; and calibrated camera-to-model correspondence. Obtaining only a newer executable would not fill these gaps.

Public-source follow-through should prioritize those joins, preserve the protected and nonpropagating possibilities, and use the independent connection experiments to constrain any extension. No outreach, information request, or contact with an author was undertaken.
