# Column 79 side plates and girder walk off

The available record supports a real, potentially important obstruction to a simple sideways slide of girder A2001. It does not yet establish that the side plates prevented every route to loss of support. The decisive missing link is the identified UAF native model case and its three-dimensional contact, restraint, failure and motion histories.

This audit checks public drawing copies, the UAF report, relevant NIST report passages, the currently held UAF download wrapper, and scoped tracked-file inventories. It includes a reproducible conditional geometry calculation, not a finite-element reproduction. No native UAF input deck, model database or result database was recovered or executed. That input limitation must not be presented as evidence that UAF never released its models, that NIST is correct, or that either side concealed information.

## What was checked

- UAF final report, March2020 URL, SHA-256 `f3a001ab68dcc6b6e230456aac4729613740336796c1b2515671141589c38bfa`: printed pp. 50, 52-56, 58, 75-81, including Figures 2.44 and 3.3-3.7. The separate [all-page version comparison](../uaf-pdf-comparison-2026-10-18/README.md) preserves both final-report PDFs and their differences; this audit does not replace it.
- NIST NCSTAR 1-9, SHA-256 `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`: printed pp. 348-354 and 482-483. These distinguish the preliminary detailed floor model from the 16-story ANSYS connection representation. [Official report](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf).
- NIST's June 2012 errata, preserved two-page source SHA-256 `d5b006c0580acc73683660ec39eecbc2b4eefeba13d7ecbbf5ffa3787561d9c7`. The original report wording and subsequent corrections remain separate records.
- Newly acquired public copies of Frankel sheets [9114](https://www.metabunk.org/attachments/9114-pdf.28807/) and [1091](https://www.metabunk.org/attachments/1091-pdf.28913/). Each complete one-page PDF was preserved unchanged and viewed, with additional high-resolution detail crops. They are public attachment copies, not independently authenticated agency-release originals or proof of installed conditions.
- The 834-byte held UAF ZIP and its one README, plus tracked-name inventories covering 62,691 public-repository paths and 6,209 main-research paths. None had one of the declared ABAQUS/SAP/native suffixes. This is not an exhaustive untracked-file, whole-disk or archive-content absence finding.

## Conditional geometry supports interception before web clearance

UAF printed p. 79 states a 12-inch bearing-seat width, 0.580-inch girder-web thickness, 11.510-inch flange width, 17.89-inch distance between side plates, and 3.678-inch western clearance. These are UAF's reported drawing-derived dimensions, not newly measured as-built dimensions.

For the stated centered-web/seat projection:

| Quantity | Calculation | Result |
| --- | --- | --- |
| Travel until the far side of the web clears the seat | 12 / 2 + 0.580 / 2 | 6.290 in. |
| Reported travel to western side-plate contact | UAF's stated clearance | 3.678 in. |
| Distance from first contact to the web-clearance threshold | 6.290 - 3.678 | 2.612 in. |

Thus, **if the girder is axially and vertically engaged behind the side plate and the contacting components retain adequate resistance**, it encounters that plate before completing this idealized lateral translation. The arithmetic supports UAF's obstruction argument under those conditions. The 2.612 inches is a displacement difference, not a strength margin or safety factor.

The code does not establish the historical engagement or resistance. Its qualified result is `null` for prevention when those inputs are unknown, rather than a false assertion that prevention either succeeded or failed. The earlier `conditional-geometry.json` remains a local preliminary output: its Boolean false meant not established, not established absence of prevention. `conditional-geometry-qualified.json` is the explicit three-valued output used here; the source PDFs and earlier records were not changed.

NIST's original p. 482 assigns 6.25 inches axially and 5.5 inches laterally. Its June 2012 errata reverses those assignments to 5.5 axially and 6.25 laterally, changes the p. 527 seat width from 11 to 12 inches, and states that the corrected dimensions were used in the analyses. That historical-use statement is NIST's assertion, not a run-card verification performed here. UAF's 6.290-inch web-clearance statement and NIST's corrected 6.25-inch lateral threshold differ by 0.040 inch. Both values and their definitions are retained without deciding that the two thresholds are identical or identifying the cause of the difference.

## Why the lateral distance alone is insufficient

There are three distinct questions:

1. **Does the girder reach the side plate in three dimensions?** A smaller lateral gap does not prove collision if its end is still outside the plate's axial reach, has lifted above or dropped below the effective obstruction, or has rotated. UAF explicitly says axial heating moves the girder into a trapped position. The initial end gap, column/girder skew, temperatures and subsequent axial movement therefore need an identified model and time history, not just a plan sketch.
2. **What happens after contact?** Plate and girder deformation, local bearing, weld/bolt failure and changing support reactions require constitutive laws and force/displacement results. A plate drawn as present is not an independently verified finite-capacity stop. Conversely, merely suggesting that it could deform is not a demonstrated bypass mechanism or a calculation that defeats UAF.
3. **Is pure lateral sliding the failure mode actually being tested?** Rocking or twisting off a seat after surrounding beams buckle is not the same motion as an intact girder translating sideways. Blocking one route does not establish that every route to support loss is blocked.

The column side cover plates must also be distinguished from the girder's partial-height web stiffeners, its bearing seat, and the top clip. They have different functions. The drawing's vertical connection reaction/capacity annotation is not a measured horizontal side-plate resistance.

## What the drawing copies add

Sheet 9114 explicitly identifies a Column 79 seat-connection detail and W33x130 girder, depicts the built-up column with side plates, and shows the girder's web stiffeners and seated/top-clip arrangement. Its Column 79 label allows different side-plate thickness variants; it is not by itself a floor-specific authentication of every dimension in UAF's reconstruction. Sheet 1091 depicts the built-up Column 79 assembly and a section through its connection region, with fabrication marks and erection references.

The copies corroborate that these components are not merely invented additions to UAF's illustration. They do not independently settle the exact installed Floor 13 member/revision chain, all tolerances, initial axial clearance, or the 3.678-inch derived lateral clearance. UAF Figure 3.5 is a 2012 Brookman reconstruction attributed to Frankel 9114, not an untouched scan of the entire shop sheet. The acquired scan copies also have clipped sheet edges; viewing each complete retrieved PDF does not restore missing original margins or authenticate the revision history.

| Public copy | Bytes | SHA-256 |
| --- | --- | --- |
| Frankel 9114 | 1,134,231 | `c02608a6b90c11b7d06a8d6d515fe3d264cebe0f92babd5183c9a0527030caf6` |
| Frankel 1091 | 2,222,126 | `640cad6a983a269c77f52ae72224365ed2b4d1c6c90fb7959c2d0865c3a4c343` |

The original retrieved drawing bytes, complete-sheet renders and detail crops remain in the verified Intel operational store. This public package supplies original analysis, hashes, acquisition receipts and links to the existing public drawing copies; it does not newly republish the complete third-party drawing PDFs or full-sheet images. HTTP response dates are retrieval metadata, not authentication of a drawing's 1985 date or revisions.

## What the UAF report establishes and does not establish

The report describes nonlinear connection work and a detailed ABAQUS column/girder model. Printed p. 56 identifies a seated top-clip connection at Column 79 on Floors 12 and 13, pictured in Figure 2.44. Printed pp. 77-79 report axial expansion and trapping behind the side plate in the separate Chapter 3 analysis.

Printed pp. 80-81 then explicitly describe a separate counterfactual: removing the side-plate protrusion and increasing the beam thermal-expansion coefficient by approximately 40 percent to drive the girder further west. This is an openly described modified test, not evidence that those settings were the historical building conditions or the baseline trapping case. Its inputs and outputs must be kept separate from the unmodified case.

The report-level descriptions do not supply a verified figure-to-native-file mapping or permit this audit to inspect the actual contact surfaces, tie constraints, boundary conditions, weld/bolt laws, plate plasticity, active failure criteria, convergence or contact-force histories. Therefore it would be inaccurate to say this audit inspected UAF's actual Column 79 input deck, confirmed a rigid-contact artifact, reproduced its result, or disproved it.

## NIST provides a material counterpoint but not a substitute for the missing test

NIST NCSTAR 1-9 printed p. 351 expressly states that the north flange and extending side cover plates at Column 79 were represented for contact with the girder in the **preliminary detailed LS-DYNA floor model**. Figure 8-23 displays that connection. Printed pp. 352-354 then describe heating, bolt failures, contact and beam buckling, culminating in the girder rocking off its Column 79 seat.

That is an explicit reported alternative motion in a model containing side-plate contact. It prevents treating the existence of side plates as proof that all support-loss paths are impossible. It is not an independently reproduced historical result, and the preliminary model's prescribed temperatures and boundaries are not the full 16-story fire-history model.

UAF's specific criticism targets the **16-story ANSYS analysis**. NIST printed pp. 482-483 describe its connection using beam/spring, break, node-contact and control elements, with laterally monitored walk-off. Showing contact in the preliminary shell model does not establish that the reduced 16-story representation retained the same obstruction, rotation and failure behavior. Conversely, the reduction is not proof that it omitted every relevant restraint. The exact active element definitions, initialization and result histories are needed.

A [publicly hosted copy of NIST's 2020 response](https://richardgage911.org/wp-content/uploads/August-2020-NIST-Denial-of-AE911Truth-et-als-2020-Request-for-Correction.pdf), section A, disputes the omission claim and refers to detailed connections and the girder's skew. That is NIST's stated answer, not this audit's verification of the hidden contact path. Preserve the competing assertions rather than choosing one by institutional status or by absence of the other side's native inputs.

## Findings and remaining uncertainties

| Proposition | Evidence layer and disposition |
| --- | --- |
| The public Column 79 drawing copies depict side plates and a seated girder connection | Direct source observation; strong within the copies' custody/revision limitations |
| UAF's stated lateral dimensions place side-plate interception before its web-clearance threshold in the specified projection | Reproducible conditional calculation; strong for that idealization, not a capacity or as-built conclusion |
| UAF's actual native case correctly models initial engagement, contact, deformation and failure | Not established by this audit; indispensable native inputs/results absent from the scoped holdings |
| NIST never represented the Column 79 side plates in any model | Contradicted as a description of its published preliminary-model account |
| NIST's 16-story connection preserved the relevant three-dimensional obstruction throughout the reported initiating failure | Not established here; preliminary-model contact and the agency's response are not the exact reduced-model audit |
| Side plates made all physically possible support-loss paths impossible | Not established; lateral interception alone does not test rocking, changing engagement or component failure |
| Either account is thereby shown fraudulent, or a historical collapse cause established | Unsupported by these checks |

## The precise records to request from UAF

The first contact should be **J. Leroy Hulsey**, identified as project lead on the [official UAF project page](https://ine.uaf.edu/wtc7) and listed as Professor Emeritus on the [current department page](https://www.uaf.edu/cem/people/cgee.php). Ask him to identify or include the team member responsible for the detailed ABAQUS case; the project page names Feng Xiao and Zhili Quan as coauthors. A project-team listing does not establish which person created this particular model. The departmental office is the institutional routing fallback. No one has been contacted by this audit.

Ask for a small targeted package rather than another undifferentiated hundreds-of-gigabytes archive:

1. The native input/model and matching output that produced Figure 3.4, with case name, dates, file hashes and a final-report crosswalk. The displayed `Model-9_Nonlinear_10s.odb` label is a locator, not by itself an authenticated final-case identity.
2. The complete Floor 13 erection/fabrication chain for girder A2001 and Column 79, including sheets 1091/9114, applicable revisions, both girder-end details, and the coordinate transformation used in the model.
3. Initial and time-dependent girder-end position, axial gap and side-plate overlap, lateral gap, vertical engagement, rotation, and the exact nodes/surfaces used for contact.
4. Contact normal/tangential definitions, friction, ties, constraints, plate/girder material laws, bolt/weld laws, temperature dependencies, damage and deletion criteria, gravity and thermal histories.
5. Contact gaps/forces, seat reactions, girder translations/rotations and plate/weld response through the attempted walk-off; solver/build, convergence and energy diagnostics.
6. A clean paired comparison retaining all other inputs while adding/removing the actual plate obstruction. Separately identify the published notched-plate plus 40-percent-expansion case; changing both features is not an isolated estimate of the plate's effect.
7. Any existing analysis of the rocking pathway reported in NIST Chapter 8, and a comparison of baseline temperatures/boundaries with the specific 16-story ANSYS state UAF challenges.

These requests would discriminate among a robust physical restraint, a boundary/contact idealization, a misidentified construction detail, and a different support-loss pathway. None is selected as the cause here.

## Verification and preservation

Nine deterministic geometry controls passed after the nullable-result qualification. They verify arithmetic, conditional logic and reproducibility, not engineering capacity. The native-file inventory is scoped and has explicit exclusions. The wrapper still matches its historical 834-byte hash and contains only the known 1,625-byte README. Four main technical source hashes matched before and after extraction/rendering. Twenty-three complete report-page review renders were created; actual visual-review coverage is listed separately in `verification.json`, not inferred from render count.

Earlier PDF discrepancies, both UAF final-report versions, the original NIST prose, later errata and prior research notes remain unchanged. No solver, third-party contact, private correspondence, litigation-record change or historical-cause ranking was performed. New findings are research, not an engineering certification or court allegation. Public-export metadata omits the operational private-repository HEAD identifier while retaining a separate local original.
