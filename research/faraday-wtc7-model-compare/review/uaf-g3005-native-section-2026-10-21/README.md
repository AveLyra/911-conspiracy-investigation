# UAF G3005 section verification and implications

October 21, 2026. **The available checked files do not establish whether UAF actually modeled G3005 as W21x44 or W24x55 in Figure 3.14.** The W21 caption and rendered annotation, the underlying W24 raster label, and NIST's separate W24 figure labels remain preserved. No native section was inferred from an annotation and no collapse model was run.

G3005 is a **floor beam**, not the Column 79 girder A2001. NIST's Figure 8-22 separately labels that girder W33x130. This distinction matters: uncertainty about one adjoining beam does not, by itself, establish the girder's section or invalidate every Column 79 result.

## Available file checks

The Intel operational-store identity passed. The public Git tree at `a1979eb700276e13e46e67cceff6a0954a55a649` contains 62,740 tracked paths and no candidate ending in the declared ABAQUS/SAP/native suffixes. The expanded, ignore-inclusive physical inventories also found no such standalone candidate:

| Physical research scope | File paths enumerated |
| --- | ---: |
| Active public checkout research directory | 45 |
| Active public checkout investigation directory | 281 |
| Intel operational public research tree | 39,037 |
| Current local Sherlock research tree | 4,364 |
| Retained Sherlock preservation tree | 10,034 |
| Intel operational Sherlock research tree | 9,046 |

These are overlapping storage snapshots, not counts of independent evidence. All six completed without enumeration errors. Exact roots, sorted path-list hashes and suffixes are recorded in [sources.json](sources.json) and [observations.json](observations.json). Symlink destinations and Git internals were not traversed. A small-plaintext native-keyword scan of the active public research/investigation checkout found no candidate. It did not search every historical Git blob, every possible extension, other disks, or proprietary embedded formats.

Five ZIP directories were inspected: the current and retained UAF wrappers, two Motion Lab archive copies and the compartment-data archive. None lists a member with a declared native suffix or a nested archive. The UAF copies are the same 834-byte, one-README wrapper, not the advertised model dataset. The other archives' directory checks do not authenticate their complete payloads; full-file SHA-256 was deliberately omitted for the two 172,774,879-byte copies. The named motion-score GZIP files were not decompressed. See [archive-directory-checks.json](archive-directory-checks.json).

Neither UAF final PDF has an attached embedded file in its PDF embedded-file directory. Thus no hidden INP/CAE/ODB attachment was recovered from the reports. This does not exclude model information in another unexamined representation.

UAF's [official project page](https://ine.uaf.edu/wtc7) still advertises a 256 GB open-data download. That public-release claim and the checked local wrapper are different records. The wrapper refers to a repaired dataset corresponding to the September 2019 draft; the final-report case mapping remains unverified. This followup did not acquire the aggregate dataset or retry an inaccessible archive through another tool. Missing local inputs are not evidence that UAF never released models or that either party concealed them.

## Conflicting representations and case locators

Both preserved final PDFs retain the previously documented Figure 3.14 [PDF-layer discrepancy](../c79-and-timing-crosschecks-2026-10-21/README.md):

| Source and location | Directly observed representation | What it does not establish |
| --- | --- | --- |
| UAF printed p. 86, physical p. 99, Figure 3.14 caption | W21x44 G3005 | Native geometry or assigned section |
| Same figure, visible vector annotation | `W21x44;  G3005 w/o bracing` | Native geometry or assigned section |
| Same figure, underlying embedded raster viewed separately in the preceding audit | `W24x55; G3005 w/o bracing` | Whether that label is stale or the actual input |
| NIST printed pp. 350 and 354, physical pp. 394 and 398, Figures 8-22 and 8-27 | Floor beams labeled W24x55 | The exact native assignment for the member called G3005, or assignments in later NIST models |

The whole rendered UAF page agrees with its caption; this is **not a visible caption-versus-plot-label disagreement**. Both versions have the same Figure 3.14 raster hash. This followup rechecked those hashes and the W21 text without altering either PDF. The preceding layer audit remains the source for the separate-raster manual transcription and covering vector rectangle.

Complete-page visual inspection identifies the braced Figure 3.11 on UAF printed p. 84 / physical p. 97 as `Model-9_Nonlinear_10s.odb`. Figure 3.14 names `Model-10_Nonlinear_10s_No_Support.odb`. The former locator had already appeared in the Figure 3.4 audit; this followup links it to the braced comparison as well. These are figure locators, not recovered files or proof that only bracing changed between the jobs. Both cases' section definitions are needed.

UAF printed p. 84 attributes W21x44 G3005 and four adjoining W24x55 beams to erection drawing E12/13. NIST's preliminary figures visibly group the floor beams under W24x55 labels. Consequently the UAF section criticism has a **publication-level basis**, independently of UAF's own Figure 3.14. Establishing an actual NIST modeling error still needs the member-specific native definition and applicable drawing/revision chain. The complete E12/13 original was not newly acquired or authenticated in this followup. The previously reviewed Column 79 shop details do not substitute for that floor-beam schedule.

## How the actual section could affect UAF criticism

| What native evidence eventually establishes | Consequence for this specific comparison |
| --- | --- |
| G3005 is W21x44 in the matching Figure 3.14 job | The W21 caption would be supported; a stale W24 raster annotation would remain a possible explanation, not an established editing history. The existing label conflict alone would not show a numerical-model defect. |
| G3005 is W24x55 in that job | The figure would not demonstrate the claimed W21x44 case. That would weaken its use as a quantitatively matched counterexample and require a correctly identified W21 comparison. It would not, by itself, refute the independently documented question about NIST's preliminary-model section. |
| The braced and unbraced jobs use different G3005 sections | Their difference could not be attributed solely to bracing. Section and bracing would need matched controls, even if each individual job ran correctly. |
| Native case or assignment remains unidentified | Both the section and its numerical effect remain unresolved; neither side gains a demonstrated physics result from the access gap. |

Changing a section can change axial and bending stiffness, torsional/warping response, local slenderness, thermal force transfer and the buckling sequence. A larger section can increase both restraint-generated force and resistance; the direction and magnitude of the resulting system effect are not determined from the designation alone. For illustration, free uniform thermal expansion is `alpha * deltaT * L`, whereas an ideal fully restrained elastic axial force is `E * A * alpha * deltaT`. These identities are not calculations of this heated composite floor or of lateral-torsional buckling. No numerical sensitivity or change in collapse outcome is claimed here.

The beam-size issue, the three lateral support beams, the exterior restraint, the girder-side-plate engagement, and whole-building propagation are separate questions. A native W24 assignment would not automatically falsify all UAF conclusions; a native W21 assignment would not automatically validate all its criticism of NIST. The [existing plate/expansion factorial protocol](../c79-factorial-protocol-2026-10-19/README.md) is unchanged.

## Smallest package that can settle the section question

Obtain the two named ODBs and corresponding INP/CAE files, or authenticated read-only exports with original-file hashes and a final-report figure crosswalk. For G3005, the export must identify instance/element-set membership and active section/material assignments. Beam elements require profile dimensions or generalized properties and orientation. Shell/solid representations require actual node geometry, web/flange thicknesses and relevant section assignments. A section called W21x44 is not enough if the underlying dimensions differ.

The [Abaqus ODB instance reference](https://docs.software.vt.edu/abaqusv2025/English/SIMACAEKERRefMap/simaker-c-odbinstancepyc.htm) and [section-assignment reference](https://docs.software.vt.edu/abaqusv2025/English/SIMACAEKERRefMap/simaker-c-sectionassignmentcpp.htm) identify the relevant model-data relationships. The [assignment-manager documentation](https://docs.software.vt.edu/abaqusv2025/English/SIMACAECAERefMap/simacae-t-prpassignsectionmanage.htm) also warns that overlapping assignments have precedence. These are current vendor documentation, not proof of UAF's installed build or settings. A compatible read-only export may settle section identity without a new solve; it may still leave result provenance or omitted model data unresolved.

If a new numerical comparison is needed, first reproduce the identified published cases, then hold other inputs fixed while crossing G3005 section (W21/W24) and lateral bracing (present/absent). That prospective four-case comparison is separate from the existing plate/expansion design. No new jobs, thresholds or results have been accepted or executed here.

## Verification and preservation

Eighteen source/integrity assertions passed, including all four before/after input hashes. Six synthetic inventory/archive controls passed; they test the checker, not UAF's engineering. Complete UAF physical pages 97 and 99 and NIST physical pages 394 and 398 were rendered and visually reviewed. Their review images remain on the verified Intel store; this public package does not newly reproduce full UAF figures. [verification.json](verification.json) identifies the checks, review hashes, initial interrupted slow traversal and remaining exclusions.

The new work is an expanded availability check, a figure-to-case locator and a conditional assessment of the criticism. It is **not a determination of the native section**, a new model result, a judgment of fraud or a cause/intent finding. Both original UAF PDFs, NIST's original report, the wrapper copies, earlier discrepancies and prior published history remain unchanged.
