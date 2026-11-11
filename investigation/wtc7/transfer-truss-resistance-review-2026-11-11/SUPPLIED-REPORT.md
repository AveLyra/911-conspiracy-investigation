# WTC 7: transfer-truss failure, structural resistance and observable precursors

**Focused audit | 11 November 2026**

## Assessment

The objection about resistance identifies a real requirement, not a detail that a collapse explanation may waive. A surviving load path must exert force; if its net upward force is appreciable, the supported mass cannot simultaneously accelerate downward at exactly gravity. Arrest is a further question: it requires enough force, work and deformation capacity at the relevant time. The correct test is not whether resistance existed before initiation, but how much remained during each subsequent phase.

Column 79's off-center position is also substantive. The structural plan places it at the northeastern edge of the interior column array, unlike centrally situated Columns 68 and 71. However, perimeter columns also carry gravity loads, so it is not a corner of *all* load-bearing columns. The distinction does not settle propagation. [N1, printed pp.5–6, Figure 1–5; figure visually checked]

The principal finding is narrower than either “fire explains the collapse” or “progressive collapse is impossible”: **the reviewed alternative fire paper does not complete the bridge from local support damage to the observed exterior motion.** Its framework makes that bridge testable, but the missing stages cannot be supplied by an animation, a publication's abstract or the term “progressive.”

## 1. The Orabi paper: compact source ledger

Orabi, Jiang, Usmani and Torero, *The Collapse of World Trade Center 7: Revisited*, DOI 10.1007/s10694-022-01225-2, appeared online in 2022 and in volume 60 (2024), pp.2963–2990. Page references here use the 29-page accepted manuscript, not journal pagination. UCL and PolyU copies are versions of the same work. [O1, O2]

| Item | Reported fact | Manuscript locator |
|---|---|---|
| Initiation tested | Mechanical-room hydrocarbon exposure of Truss 2, supporting 77/78 | pp.12–16 |
| Control | Protected diagonals survive; bare-diagonal case fails | pp.17–20 |
| Model 2 | Regional model, nine slabs through Floor 14; upper-floor fires excluded | pp.15–16 |
| Connections | Fully fixed joints; rigid, non-failing studs | p.13 |
| Output | About 0.8 m deflection after 2 s; run stopped at 2.3 s | pp.21–22 |
| Missing extension | Additional heated-floor/connection failures proposed | pp.23–25 |
| Numerical settings | Rayleigh factors 0.05/0.005; thermal time scale 10,000 | pp.15–16 |

This is evidence of conditional vulnerability and meaningful redistribution, not a computed global free-fall result. The protected case and the resisting upper floors are particularly important controls. [O1]

## 2. What the research must establish next

The competing causal chains should not be merged:

**NIST route:** eastern floor/connection failures and loss of Column 79 bracing precede the wider internal progression. **Orabi route:** transfer-system failure is the candidate initiator. A later effect in one account becomes an earlier cause in the other. Agreement that the east penthouse moved first does not make these the same explanation. [N1, printed pp.22–23; O1]

The next analysis should retain four separate questions.

**Exposure.** Is there evidence for the required fire at the required location, intensity and duration? A prescribed standard exposure tests response to that exposure; it does not reconstruct its occurrence. Fuel availability, fuel release, ignition, ventilation and sustained supply are different propositions.

**Protection.** Was the relevant member actually bare, partly protected or adequately protected? A matched protected/unprotected calculation is useful precisely because the physical condition changes the result. An undocumented choice must remain a scenario, not be promoted to an as-built fact.

**Propagation.** Do independently calibrated connections and slabs fail in the needed sequence, or do they bridge the damaged region? A load path cannot be removed simply because retaining it prevents the desired result. Conversely, making a connection incapable of failure cannot establish that the real connection would survive.

**Motion.** Does the unforced response reproduce multiple observed points, with one time reference, including the penthouses, onset of façade motion, roofline distortion and acceleration? A local deflection and a roofline trajectory are not interchangeable observables.

These are proposed evidentiary tests, not conclusions that the missing conditions were absent.

### The strongest countercase to a mechanical-room fire

NIST evaluated hypothetical diesel scenarios and raised specific problems: partition locations separating some critical members, loss of the electrical supply needed to continue pumping fuel, and predicted smoke not matched by its visual record. It also described a lower-floor stairway observation after 1 p.m. that did not report heat or smoke from the observers' position. [N2, printed pp.366–374]

Those are substantive constraints, not merely an institutional rejection. A revised scenario could differ in leakage location, damaged partitions, ventilation or start time. To count as a stronger explanation, it must calculate those differences and meet the observations; listing possible differences does not do so. Equally, rejecting one partition/ventilation configuration does not exclude every mechanically different scenario.

## 3. Numerical issues that are directly auditable

### A. Static top loads are not automatically dynamic upper-building mass

For a dynamic equation, applied force and inertia are separate inputs. A downward load representing omitted stories can preserve a static reaction without automatically preserving their mass, modal behavior, bracing or redistribution. The native model must show what was assigned at the cut boundary: forces, masses, stiffness, constraints and damping. Until that is recovered, do not treat a regional displacement as the motion of the full upper building.

The appropriate comparison is an expanded model versus a reduced model with a demonstrably equivalent boundary representation. Agreement in one gravity-load case is insufficient; compare relevant low-frequency modes, static compliance and nonlinear force transfer too. This is an audit requirement, not a finding that the published boundary is wrong.

### B. Damping coefficients are not damping percentages

The official OpenSees documentation distinguishes mass-proportional damping and current-, initial- and committed-stiffness terms. [D1] For a single linear mode sharing the stiffness used in the damping matrix,

`zeta = alpha / (2*omega) + beta*omega/2`, with `omega = 2*pi*f`.

Using the transcribed coefficients gives the following **new calculations**, not measured modal damping:

| Hypothetical modal frequency | Calculated damping ratio |
|---|---:|
| 0.1 Hz | 4.14% |
| 0.5 Hz | 1.58% |
| 1 Hz | 1.97% |
| 5 Hz | 7.93% |
| 10 Hz | 15.75% |

The minimum is about 1.58% at 0.503 Hz. Therefore, neither “5% damping” nor “50% damping” follows from the two coefficients alone. Nonlinear response requires the actual matrix choice, assigned regions, masses and modes. Check whether damping energy remains small relative to the structural work relevant to the comparison, and rerun a justified coefficient range. Do not set damping to zero merely to obtain a faster descent.

Physical bridging resistance and numerical damping are also different mechanisms. Losing a brace can reduce load capacity; it does not justify silently deleting a numerical damping term, or vice versa.

### C. Accelerated heating needs a handoff audit

The transcribed settings yield 10,800 seconds of fire time in 1.08 analysis seconds and 3,600 seconds in 0.36 seconds. This arithmetic reproduces the stated scaling. It does not show that inertial effects are negligible during instability.

A useful reproduction varies the heating acceleration while keeping the physical thermal history fixed, then checks reactions, kinetic energy and the displacement/velocity state at transition to real-time dynamics. Preserve both an unmodified handoff and a separately justified equilibrated comparison; do not reset velocity after inspecting the target collapse. Any discrepancy must be attributed to numerical procedure before it is interpreted historically.

### D. The deflection number is not an acceleration measurement

The transcribed displacement divided by its interval is 0.4 m/s. A hypothetical from-rest, constant-acceleration motion covering that displacement would have acceleration 0.4 m/s². **That is not the simulation's acceleration.** Initial velocity and the full nodal trajectory are unavailable, and the tracked model location is not the observed roofline. This dimensional check prevents a speed from being mislabeled as an acceleration or a small-region displacement from being compared directly with whole-building free fall.

## 4. Visible and audible evidence: what is actually identified

NIST describes east-penthouse descent before exterior descent and a small lateral vibration beginning roughly six seconds before the penthouse motion. Its timing table also contains unobserved internal events. The vibration is an observation; its assignment to cascading floors is an interpretation. Its preferred modeled west-penthouse disappearance is about 2.0–2.4 seconds earlier than the observation. [N1, printed pp.42–44, Table 3–1; table visually checked]

The evidence therefore supports **internal disturbance before global exterior motion**, but does not directly expose the proposed Floor-13-to-Floor-5 cascade. A rooftop failure, window breakage or vibration is not an image of a particular lower floor connection breaking. The same precursor can constrain several mechanisms without choosing among them.

### The sound record must not be overstated

A NIST audio passage, retrieved here through a reproduction of its draft report in the official public-comment compilation, describes three street-level recordings at least 640 m away, with intervening buildings. It reports no sound attributable to WTC 7 before global collapse in the reviewed recordings and notes a roughly two-second transmission delay. [N3, compilation printed p.425, reproduced §5.7.5]

This is a **reported non-detection in particular recordings**, not proof of silence at the building. It is also not affirmative acoustic corroboration of the floor cascade. The draft reproduction is not a newly acquired final-report source; the final §5.7.5 locator is printed p.289, but the complete final-file download failed in this review.

The useful criticism is quantitative: an explanation predicting impacts before exterior descent should state what sounds and ground motions those impacts generate and what the actual recorders could detect. “The failures were inside” is not a sufficient calculation. Nor is “they must have been loud” a microphone-specific threshold calculation.

A proper test needs the original continuous recording, source-to-camera distance and obstruction, timebase, automatic gain control/compression, background sound, and event timing. For visibility it needs the expected moving surfaces or dust outlets, clear sightlines, camera resolution and occlusion. Route air through the actual available openings rather than assume every failed floor must emit a façade plume facing the camera.

NIST's seismic interpretation is likewise not a floor-by-floor observation. This audit does not promote uncertain seismic timing or mechanism attribution into a verified cascade; the detailed appendix remains an acquisition/rechecking target. No new acoustic or seismic measurement was performed.

## 5. Korol resistance calculation: new arithmetic and sensitivity checks

The 2016 paper estimates energy absorption for an idealized crush-down/crush-up path. Its concrete term depends on an assumed particle-size distribution, rather than a measured WTC-7-specific distribution. [K1, printed pp.27–31]

### An internal inconsistency to reconcile

Using its stated inputs,

`5 * 3853 m² * 0.1016 m * 2400 kg/m³ * 4900 J/kg`

produces **23.018 GJ**, not the published **32.01 GJ**. For 34 floors, the same inputs give **156.523 GJ**, not **218 GJ**. The published results imply slab depths of about **141.3 and 141.5 mm**, respectively, instead of the stated 101.6 mm. The printed pages were visually checked. [K1, pp.30–31]

This is an **unreconciled input/arithmetic discrepancy**, not yet proof of which value should be changed. Total slab depth, deck-flute geometry and solid-equivalent concrete thickness must be reconciled before selecting a physical correction. NIST describes a typical upper-floor total slab thickness of about 140 mm over corrugated decking, which makes the distinction relevant. [N1, p.6]

Substituting the stated 101.6 mm into the concrete terms while retaining the paper's published column terms yields **238.60 GJ**, approximately **3.15 times** its 75.7 GJ gravitational estimate. Thus the correction alone does **not** reverse its total-energy inequality.

### The stated arrest location is sensitive within that idealization

A separate check substitutes the printed rounded speed and `MA + 2*Mi` into Equation 5. It gives about 6.935 GJ of initial kinetic plus gravitational energy, 2.396 GJ of column work and 4.595 GJ of concrete work, leaving approximately **−0.056 GJ**. The arrest result is retained, but only narrowly with these transcribed values.

A reduction of about **1.21%** in that equation's specific concrete-energy input changes the sign of this particular residual. This does not show that the building would then collapse completely: it shows that the asserted stopping floor is not a robust consequence of the rounded equation without uncertainty analysis. This check treats each added floor as Mi and does not add a separate lower-column mass term. That is an explicit reconstruction, not an acquired author workbook; small mass or indexing changes can matter to such a small residual. The calculation is preserved in `analysis_checks.py`; it is not a replacement model.

### What the energy argument still needs

The decisive issue is whether the assumed work is unavoidable on the actual path. Energy absorbed by aligned columns crushed over particular rotations is not automatically a lower bound for columns losing multi-story bracing, fracturing connections or moving out of alignment. Concrete comminution after ground impact is not necessarily work that must be completed during an earlier free-fall interval. These alternatives require analysis too; they are not licenses to discard resistance.

A simplified sensitivity ledger is `E = 59.06*p + 250.01*q` GJ, using the paper's published column and concrete totals. Here `p` and `q` denote hypothetical engaged fractions, not empirical estimates. The ledger is useful only to expose dependence. It cannot decide which fractions a physical mechanism permits. A valid lower-bound impossibility argument must establish unavoidable work, not simply available energy-absorption capacity.

## 6. Reproduction status and project integration

The project's earlier structural review already noted the partial-model and protected/unprotected limits. This follow-up adds the explicit audit tests and reproducible arithmetic above. The live repository's acoustic-search report also records missing correspondence and an unresolved receiver-detectability connection. That earlier bounded search should not be repeated and counted as new corroboration. [P1–P3]

The generic solver-source repository was inspected at its root. A bounded WTC code search did not identify the exact study inputs. Solver source is not a specimen-specific simulation package. Native model decks, mass assignments, thermal mappings, run commands, solver commit, complete outputs and a figure-to-run manifest remain missing. [G1]

**Next decisive work:** implement the protocol in `MODEL_AUDIT_PROTOCOL.md` only after acquiring or explicitly reconstructing those inputs. Preserve the no-additional-failure control, quantify surviving reactions and energy, and test one common observed timeline. Keep a new reconstruction separate from a claimed reproduction.

No finite-element model was rerun; no original video was retracked or audio independently listened to; no source PDF bytes were successfully downloaded into this runtime. Selected source pages were visually checked through the web renderer, with failures logged. All generated numerical outputs are arithmetic diagnostics. No contacts, records requests, fees or repository writes occurred.

## Sources and exact locators

See `source_register.json` for retrieval status and alternate locations.

- **O1:** Orabi et al., accepted manuscript, https://discovery.ucl.ac.uk/id/eprint/10146056/1/WTC7%20Revisited-uploaded.pdf ; institutional mirror https://ira.lib.polyu.edu.hk/bitstream/10397/92640/1/Orabi_Collapse_World_Trade.pdf . Principal locators pp.13–25.
- **O2:** Version-of-record metadata, https://link.springer.com/article/10.1007/s10694-022-01225-2 . Full publisher text not acquired.
- **N1:** NIST NCSTAR 1A, November 2008, https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1a.pdf . Printed pp.5–6,22–23,42–46. PDF page48 is printed6; PDF85 is printed43.
- **N2:** NIST NCSTAR 1-9, Vol.2, §9.2, printed pp.366–374. Agency-authored report on a third-party mirror: https://www.911facts.dk/resources/NIST/NCSTAR_1-9_Vol_2_Chapters_9_-_Appendix_E.pdf . Official combined locator https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861611 . Combined retrieval exceeded the web-reader size limit.
- **N3:** NIST-hosted public comments, https://www.nist.gov/system/files/documents/2017/05/09/combined2008publicComments-2.pdf , printed compilation p.425 reproducing draft §5.7.5. The surrounding commenter's conclusions are not NIST findings.
- **K1:** Korol, Heerema and Sivakumaran (2016), *Challenge Journal of Structural Mechanics* 2(1),25–31, https://www.challengejournal.com/index.php/cjsmec/article/download/50/41 . DOI10.20528/cjsmec.2016.02.004. Printed30–31 / PDF6–7 visually checked.
- **D1:** OpenSees official Rayleigh command documentation, https://opensees.github.io/OpenSeesDocumentation/user/manual/model/damping/rayleigh.html . General command semantics, not the missing study input.
- **G1:** https://github.com/Anwar8/MyOpenSees ; root inspected via connected GitHub. Search also included https://github.com/Anwar8/gidopensees . No exact WTC model recovered.
- **P1:** Live project README, https://github.com/AveLyra/911-conspiracy-investigation/blob/main/README.md , inspected via connected GitHub.
- **P2:** Live acoustic-search report, https://github.com/AveLyra/911-conspiracy-investigation/blob/main/investigation/wtc7/acoustic-correspondence-locator/report.md , inspected via connected GitHub.
- **P3:** Project Library report `WTC7_Structural_Explanation_Public_Review_2026-11-06.pdf`, particularly pp.8–12. Prior project analysis, not independent primary evidence.
