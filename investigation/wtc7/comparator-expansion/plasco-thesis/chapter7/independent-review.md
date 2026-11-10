> **Preservation note:** This is a public derivative of a dated working research document. Source-access and verification statements below are historical reports; they were not independently rerun for this package. No source media, full-text papers, images or rendered pages are included. Missing linked items are identified in the text; local filesystem paths, if any, are withheld. The companion [provenance record](../../PROVENANCE.json) records the changes and original hashes.

# Chapter 7 independent method review

2026-09-09. Research-only second-agent review of the preserved thesis Chapter 7. **The primary assessment's central result is supported:** the chapter presents calculated thermal response, conditional instability and a reconstructed collapse sequence, not an uninterrupted dynamically validated collapse of the complete tower. No critical reversal of that assessment is requested. Two source-level qualifications below should be retained, including a slab-temperature labeling inconsistency additional to the primary draft's timing checks.

## Independence and coverage

This reviewer authored the earlier Chapter 6 audit and therefore has source-family familiarity. The reviewer did not author the Chapter 7 primary assessment, protocol or original derivative run. Reading the same thesis is an independent interpretation/integrity check, not an independent historical evidence family, structural qualification or laboratory validation. Root communicated its initial scope findings and landscape-page diagnostic before completion of this pass; the review was not blinded.

All **51 complete Chapter 7 text pages**, physical 227-277 / printed 212-262, were read in order before reading the primary assessment. **34 complete source-page renders** were then visually inspected: physical **228, 231, 232, 241, 242, 245, 246, 247, 248, 250, 251, 254, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277**. This includes every physical page 262-277, not merely selected text from the global-collapse discussion. Figure legends, page orientation, construction-photo annotations, video-frame annotations and the author's limiting prose were inspected together.

Below, **P** denotes physical PDF page and **R** printed thesis page. The source is the same 291-page, 12,229,604-byte institutional thesis, SHA-256 `0d76577bbf898dfa2d1587d02f1cc51378d531e3b59983fc0d4db8665fd575b4`. No network retrieval, solver execution, model reconstruction or camera-original analysis was performed. No files outside this review were authored.

## Independently supported findings

| Question | Decisive source evidence | Permitted conclusion |
| --- | --- | --- |
| Full tower or truncated frame? | P228/R213 specifies the upper eight floors of the 16-storey building, 102,000 nodes, 147,000 elements, 29.5 by 31.0 by 30.4 m. P231/R216 shows separate floor CFD/heat-transfer paths entering a combined structural model. | A large multi-floor model, not all 16 storeys or a monolithic six-storey CFD fire-spread calculation. The repeated virtual thermocouples are not measurements of historical in-building temperatures. |
| Are connection failures solved? | P247/R232 explicitly says connection behavior is not modeled and all connections are rigid; nodal rotations are extracted at the already assigned time of the first observed collapse. P248/R233 and P256/R241 show rotation contours and interpretation. | Computed nodal orientation is not a calibrated relative joint-deformation/fracture criterion. The chapter proposes connection failure from demand and construction/debris evidence; it does not supply independently predicted rupture time/capacity. |
| Are thermal/composite assumptions consequential? | P246/R231 leaves core columns unheated on a masonry assumption while acknowledging incomplete coverage. P250-251/R235-236 assumes full slab/truss composite action, omits slip and says important details/sensitivity lie outside scope. | Core heating and semi-composite behavior remain alternatives or uncertain inputs, not historically resolved facts. The two Chapter 6 interaction extremes do not prove every partial-interaction case lies numerically between them. |
| Is the final cascade dynamic output? | P232/R217 calls the thermo-mechanical procedure static without dynamic effects. P262/R247 Fig.7.31 illustrates a 4-5-second downward floor-loss sequence. P263-264/R248-249 then introduces missing southeast floors and states static reliability is limited to failure initiation. | The floor cascade, impact and seconds-scale timing are reconstructed/inferred, not established by the disclosed static calculation. The revised frame begins with prescribed floor loss. No mass/contact/impact-energy or continuous damage-state transfer is supplied for reproducing that bridge. |
| What does the revised calculation show? | P264/R249 Fig.7.33 labels a deformed column as failed and plots lateral displacement over about 0-12,000 seconds. P265/R250 shows reactions and neighboring-column response. | Reported conditional instability/load redistribution merits analysis. The figure is not a resolved 4-5-second inertial trace. The chapter does not establish that the solver stopped at a particular step or that non-convergence defined failure; substituting either claim would overstate the evidence. |
| Does video agreement independently identify initiation? | P266-270/R251-255 contains selected frames, arrows, dotted lines and a summary sequence. P267/R252 explicitly notes the main columns are not visible in some frames. P268/R253 describes the initiating member as likely. | The chapter offers retrospective sequence interpretation, not direct visibility of every interior failure or a held-out quantitative validation. The source's own drawings and inferred support loss cannot independently authenticate themselves. |

The primary report accurately distinguishes the source's phraseology about complete collapse from the narrower demonstrated scope. It also correctly restricts the chapter's WTC connection comparison to WTC 1 and 2 (P257/R242), not WTC 7.

## Negative results and alternatives that must remain visible

1. **Large floor displacement can stabilize:** P245/R230 describes growth slowing and stabilizing after initial large bowing; it is not a universal displacement-to-collapse threshold. The less-displaced 11th floor being the first reported local collapse is an adverse result for a simple maximum-displacement-only rule (P251/R236).
2. **Northwest damage is not immediate total failure:** P254/R239 and P272/R257 retain the roughly half-hour interim stability and structural-segmentation explanation. This does not show every possible corner fire/damage configuration must remain stable.
3. **Heated members can shed load successfully:** P258-259/R243-244 expressly reports adjacent columns remaining stable and attributes redistribution to cooler structure and intact peripheral connectivity. This is a genuine conditional negative result, not evidence that heating always produces collapse.
4. **Original and revised models are not a demonstrated one-variable ablation:** revised geometry and the stated loading description both change; P264/R249 says external columns alone receive thermal loading. The state transfer, retained loads and exact thermal histories are not specified sufficiently to attribute every response difference to floor removal alone. The primary report's proposed matched cases are the correct next test.
5. **Intact-connection collapse remains hypothetical here:** P261/R246 proposes alternative fire conditions in which geometry changes might trigger collapse without connection rupture. It is not a displayed complete no-removal dynamic-collapse reproduction. P275/R260 separately preserves a possible core-heating pathway attributed to earlier work; this pass does not independently audit that earlier case.
6. **The visual sequence is not simultaneous all-facade failure:** P266-269/R251-254 describes staged southern-frame, roof and other-facade responses. Claimed exterior alignment/roof changes and dust emissions do not resolve the invisible interior mechanism or native timing.

## Arithmetic and source-precision checks

Elementary arithmetic was independently executed locally using Python's standard `math` module; no FE or CFD model was run:

| Expression | Result | Consequence |
| --- | --- | --- |
| 3 hours 20 minutes | 12,000 s | Not 12,600 or 126,000 s as equated at P232/R217 and P239/R224. |
| 200 steps times 63 s | 12,600 s = 3 hours 30 minutes | The multiplication agrees internally, but the stated duration does not. |
| 126,000 s | 35 hours | Native history arrays are required before diagnosing executed input values. |
| 2 hours 50 minutes | 10,200 s | Not 102,000 s at P238/R223 and P254/R239; 102,000 s is 28 hours 20 minutes. |
| 0.37 radians | 21.199438 degrees | Near the source's approximately 22-degree description; it does not fix the missing joint-capacity law. |
| 0.33 radians | 18.907607 degrees | Consistent with an approximately 19-degree statement. |
| Fig.7.35 intervals, if successive | 4.2 + 1.5 + 5 = 10.7 s | Different start/end stages may explain a shorter final-collapse description. Original frames and event definitions are needed. |
| Fig.7.36 intervals, if successive | 0.16 + 1.5 + 1.5 + 1 + 6 = 10.16 s | A source-annotation arithmetic check only; no new calibrated collapse duration is measured. |

These inconsistencies do not prove incorrect model execution or fraud. The primary report's distinction between document error, executed input error and historical event duration is supported.

## Specific review recommendations

**R1 - Add the slab-temperature label discrepancy before numerical reuse.** Complete P241/R226 Fig.7.10 labels the hotter curve as the bottom surface and the coolest as the top surface; the bottom-heated discussion is consistent with that ordering. P242/R227 prose instead assigns the roughly 523-degree plateau to the top and 179-degree plateau to the bottom. These surface assignments are reversed between prose and figure. Because thermal-gradient direction drives the bowing interpretation, record the discrepancy and require section-location/output metadata before using either assignment as a verified historical or executed-model gradient. This is a source-labeling problem, not an established defect in the executed model. Suggested wording: "The slab's top/bottom temperature assignments conflict between Fig.7.10 and the following prose; native section-coordinate histories are needed to resolve the intended gradient."

**R2 - Keep the construction-photo tangent distinct from observed rotation.** P248/R233 Fig.7.17(b) is explicitly a construction-stage photograph with a drawn 22-degree tangent, paired with the model rotation map. It is illustrative, not photographic measurement of a joint during the fire. The primary report already treats nodal rotation as modeled, and this caption-level qualification strengthens that boundary. Debris photographs of buckled/ruptured parts likewise need time/location/custody links before identifying the initiating failure.

Neither recommendation changes the primary report's main conclusion. There is no requested claim that all fire pathways are excluded, that connection failure is impossible, that the source is fraudulent, or that a specific numerical failure mode was reproduced here. Recommendations were sent to the primary author; this file does not imply their implementation or the author's acceptance.

## Verification of derivative/source integrity

The frozen `derive.py` and protocol were read. Rather than rerendering already inspected pages, an independent read-only check verified source/code/protocol bytes against `run01/receipt.json`, all 102 text/PNG hashes and sizes, all 51 successful empty-output render receipts, and fresh pypdf extraction against all 51 saved texts. All checks passed. Expected PNG sizes were computed from each PDF media box/rotation at 110 dpi: P231 is legitimately landscape, **1210 by 935**, while the other selected pages are **935 by 1210**. Root's earlier portrait-only check failure is already preserved as a validation-assumption correction; it was not reproduced as a source/render defect.

Receipt SHA-256: `b0af034428537d4978f9f475a93da27d7c404909a5a6f9cf4c500150be636d6d`. Source hash remained the pinned value. No `review02` output was created and no pixel-rerender claim is made. Hash equality verifies preserved derivatives, not the correctness of plotted mechanics or the reader's comprehension.

The primary documents were read after the independent source pass: `report.md` SHA-256 `bcd1fbef93179d74b7ce5ab7cf91d604d1644e1e7eb2e6e74fc659da734056d3` and `validation.md` SHA-256 `a30e00e9c855f6555cc016a49d3696c23753f42262195821ace0bb786d9e5474` at review. Later edits need their own change-specific check rather than inheriting blanket approval.

## Limits and disposition

The documentary findings are directly established for this thesis version; historical reliability of the model remains conditional. No executable case, native camera recording, raw thermal array, tested connection-capacity dataset, dynamic impact model, independent calibration/holdout or licensed engineering validation was obtained through this local pass. Earlier chapter methods and journal equivalence remain outside its independent coverage. Only this working review file was authored; no canonical record, status, source or primary report was changed.

Retain the primary assessment with the above source-precision qualifications. The smallest consequential next test remains a source-pinned intact/revised case comparison with explicit clocks and state transfer, followed by independently constrained connection and dynamic-impact tests if actual inputs and competent review become available. A guessed model would not be a reproduction.

## Completion addendum

After the primary-draft review, three supplementary complete source pages were viewed: **P238/R223, P239/R224 and P244/R229**. They confirm the printed 102,000/126,000-second caption discrepancies and the deformation curves that slow or stabilize. Total actual visual coverage for this reviewer is therefore **37 distinct complete pages**; the earlier 34-page pre-draft set above is preserved. No new graph values were digitized.

Root subsequently reported incorporating R1, R2 and the not-one-variable-ablation qualification after its own source checks, and reported an exact `root02` rerender match. Those are acknowledgments of root's work, not this reviewer's independent reinspection of the revised primary report or rerender. The source findings and earlier reviewed-document hashes above remain the scope of this signed-off pass.
