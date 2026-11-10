# Column 79 matched model comparison protocol

The comparison will separate the effect of the western side-plate obstruction from the effect of the increased thermal-expansion coefficient in UAF's girder A2001 analysis. Its four-case design is frozen before any new native model results are inspected. Execution is not ready: the exact baseline and modified input/output files, their final-report mapping, and numerical reference histories remain unverified in the scoped holdings.

This is a prospective test design, not a new finding that either model is correct or that the historical building could or could not collapse. The original reports, conflicting publication versions and earlier audit remain unchanged.

## Source observations

UAF's March 2020 report, section 3.2.1, printed pages 77-79 (PDF pages 90-92), describes axial expansion placing girder A2001 behind the western Column 79 side plate. Section 3.2.2, printed pages 80-81 (PDF pages 93-94), describes a separate case that removes the interfering plate protrusion and raises the thermal-expansion coefficient for beams K3004, C3004, B3004 and A3004 by approximately 40 percent, to 11.5e-6 in/in/degree F. That is a coefficient change, not a 40-percent temperature increase. The original coefficient must come from the identified baseline material cards; it must not be reconstructed by dividing the reported modified value by 1.4.

Source A: [March2020 report](https://files.wtc7report.org/file/public-download/A-Structural-Reevaluation-of-the-Collapse-of-World-Trade-Center-7-March2020.pdf), SHA-256 `f3a001ab68dcc6b6e230456aac4729613740336796c1b2515671141589c38bfa`.

Source B: [March-2020 report](https://files.wtc7report.org/file/public-download/A-Structural-Reevaluation-of-the-Collapse-of-World-Trade-Center-7-March-2020.pdf), SHA-256 `41dd3390627fac24c2bd696160c48f15e05d3213cc05325c4e4e89608df96d27`. Both versions remain separate; this protocol does not adjudicate their Figure 3.3 publication difference.

The [existing technical audit](https://github.com/AveLyra/911-conspiracy-investigation/blob/2201bbaf726572d1d19fd9c836b614153f1f8bb0/investigation/wtc7/uaf-c79-side-plate-audit-2026-10-18/README.md) documents the scoped native-file limitation and conditional geometry calculation. Its 3.678-inch contact distance and 6.290-inch web-clearance distance are not a capacity calculation or a definition of global collapse. No new source acquisition or finite-element execution is claimed here.

## Four cases and permitted contrasts

| Case | Western plate protrusion | Expansion coefficient for the four named beams | Purpose |
| --- | --- | --- | --- |
| P0 A0 | Intact baseline geometry | Exact original material definition | Reproduce the published trapping case |
| P1 A0 | Published notch or protrusion removal | Same original definition | Isolate the geometric intervention at original expansion |
| P0 A1 | Intact baseline geometry | Reported modified definition | Isolate the coefficient intervention with the plate intact |
| P1 A1 | Published notch or protrusion removal | Same modified definition | Reproduce the published compound modification |

Use P1 A0 versus P0 A0 for the plate intervention at original expansion, and P1 A1 versus P0 A1 for that intervention at modified expansion. Use P0 A1 versus P0 A0 and P1 A1 versus P1 A0 for the coefficient intervention at each geometry. Their difference of differences measures interaction for a chosen common scalar observable. P1 A1 versus P0 A0 changes both factors and cannot isolate either one's effect. A single-factor result may not generalize across the other factor if an interaction is present.

The geometric intervention must match the documented protrusion modification, not delete an entire column side plate. Record resulting changes in mass, stiffness and mesh; geometric removal cannot honestly be described as leaving those quantities identical. Disabling contact while keeping geometry unchanged would be a different, nonphysical numerical diagnostic, not a substitute for the four cases.

## Conditions required before execution

1. Identify the exact inputs and outputs for the baseline trapping case and published modified case, with hashes, solver version/build, units, coordinate systems, source drawing revisions and a figure-to-case mapping. A screenshot label such as `Model-9_Nonlinear_10s.odb` is a locator, not sufficient authentication.
2. Inspect initial axial gap, three-dimensional plate overlap, vertical engagement, girder skew, all restraints/ties and contacts, plate/girder material and failure laws, bolts/welds, friction, gravity and thermal histories. Keep G3005 and every unnamed member's material definitions unchanged across the coefficient factor unless the native files establish a different published scope; a scope difference requires an additive protocol amendment before results are viewed.
3. Preserve every source file unchanged. Run separate copies and retain all cases, including failed, nonconvergent and inconvenient ones. Do not tune temperatures, expansion coefficients, contact stiffness or restraints to obtain an expected outcome.
4. Before inspecting new outputs, freeze observable definitions, quantitative baseline-reproduction tolerances, contact/support-loss thresholds, convergence criteria, mesh/time-step sensitivity and output sampling. Their numerical values remain null here because the native units, baseline data and runtime have not been verified. The four-case design is frozen; those execution details are not.
5. Reproduce both identifiable published cases within those predeclared tolerances before interpreting the added controls. If the report supplies only images and no numerical baseline, label numerical reproduction unverified rather than accepting a visually selected match.

Keep shared model regions, loads, temperature histories, restraints, contact laws and solver controls the same except for the two declared factors and unavoidable documented consequences of the geometric intervention. Compare common physical locations and surfaces, not raw element numbers where remeshing changes their identity.

## Required outputs and interpretation

Preserve time histories of axial/lateral/vertical girder-end displacement, rotation, axial overlap, side-plate gap/contact state and force, seat contact area and reaction, plate and weld response, bolt/failure/deletion events, and available energy/convergence diagnostics. Report temperature and analysis time separately; do not equate imposed heating time with the historical fire or an observed collapse clock.

Define loss of seat contact separately from loss of all vertical support. Neither the 6.290-inch geometric threshold nor one reaction-force change alone establishes a complete failure mechanism. Record residual contact, bolt/weld restraint and other load paths. Compare rocking and translation explicitly rather than naming every loss of support a sideways slide.

For each outcome, retain source observation, numerical result, uncertainty, and inference separately. A conditional obstruction, successful alternate pathway, failed reproduction, mixed outcome and unresolved result are all admissible. None identifies historical cause, deliberate support removal or intent.

## Separate NIST mechanism comparison

[NCSTAR 1-9](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf), printed pages 351 and 353, describes side-plate contact and rocking in the preliminary LS-DYNA model. Printed pages 482-483 describe the reduced ANSYS connection. Source SHA-256: `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.

The four UAF cases do not themselves reproduce either NIST model. Cross-model comparison needs the particular NIST input state, boundaries, materials, thermal histories, contact and failure definitions, and matching observables. A contact representation in the preliminary model is not verification of the reduced ANSYS implementation; UAF's blocking of translation is not automatically a test of NIST's rocking pathway.

## Status and preservation

`protocol.json` is the machine-readable design. `verification.json` records document/design consistency checks, not solver or engineering validation. No native case has run and no numerical or historical conclusion is authorized by freezing this design. The next indispensable input is a verified case-to-figure mapping with the baseline and modified native files and usable reference outputs. This step does not authorize contacting anyone, reopening rejected download routes, acquiring an aggregate archive, installing a solver, or changing litigation records.

The source research copy remains separate from its additive public mirror. Later changes must use dated addenda and retain this original design. No earlier discrepancy has been resolved or overwritten.
