> **Preservation note:** This is a public derivative of a dated working research document. Source-access and verification statements below are historical reports; they were not independently rerun for this package. No source media, full-text papers, images or rendered pages are included. Missing linked items are identified in the text; local filesystem paths, if any, are withheld. The companion [provenance record](../../PROVENANCE.json) records the changes and original hashes.

# Plasco Chapter 7: global-collapse model and inference audit

The chapter develops a physically specified candidate pathway from fire-related deformation to loss of restraint and perimeter instability. It does **not** compute an uninterrupted, dynamically validated collapse of the complete tower. The reported structural model contains the upper eight floors, assumes rigid connections, excludes dynamic effects, and later introduces a revised geometry with southeast floor sections removed. Its strongest contribution is a conditional instability and load-redistribution analysis supplemented by interpreted video evidence. Its central limitation is the uncomputed bridge between connection demand, actual rupture, falling-floor impact and the prescribed damaged geometry.[^1]

These distinctions narrow the use of Plasco as a comparator without dismissing the observed fire-associated collapse. They neither validate NIST's WTC 7 sequence nor supply affirmative evidence of deliberate intervention. No WTC 7 ranking changes through this source audit alone.

## Source, scope and claim layers

Source: Domada Veera Venkata Ramakanth, *Multidisciplinary forensic investigation of buildings in fire: the case of the Plasco Tower*, Hong Kong Polytechnic University doctoral thesis, institutional edition 2025, inner submission date August 2024. [Institutional record](https://theses.lib.polyu.edu.hk/handle/200/13847?mode=full); preserved PDF (supporting item not included in this public package). The prior [source/version audit](../report.md) records the exact 12,229,604-byte, 291-page baseline and the unresolved relationship to the separately identified 2025 journal article.

This extension reads all **51 Chapter 7 pages**, printed **212–262**, physical **227–277**, under the prospective [protocol](PROTOCOL.md). Pins below are **printed / physical**. Thirty-three complete pages were additionally inspected visually; [validation.md](validation.md) gives the exact set and actual checks. Chapter 7 does not automatically validate earlier chapters' inherited inputs, and this is not a full audit of Chapters 1–5 or the journal edition. All scientific claims remain research-only.

“Documentary observation” below means what the inspected thesis contains. A published graph is observed as a publication; its plotted values remain model outputs, not new historical measurements. Likewise, a reproduced video still is directly visible in the thesis, but its timing, identification and causal interpretation are separate propositions.

## Computational extent and inherited assumptions

The model has 102,000 nodes, 147,000 beam/shell elements, 17 steel section types and a concrete slab. Its reported dimensions are 29.5 × 31.0 m in plan and 30.4 m high. The chapter explicitly truncates the 16-storey tower to its **upper eight floors**. A single-floor CFD geometry is used for six fire scenarios; six heat-transfer models feed the combined structural model. Each floor scenario uses 4,307 virtual temperature sampling locations. Figure 7.1 illustrates this data flow; these are simulated temperatures, not 25,842 independent field thermometers. **213–217 / 228–232**.[^1]

The model inherits a calibrated fire reconstruction from earlier work. It does not declare a fresh, independently measured fire field or an unused evaluation dataset. Exact fuel, ventilation, suppression, floor-clock shifts, lower-model restraints, gravity loads, mesh/material definitions and temperature-to-element files require the executable case and upstream source checks. A description of automated coupling is not a case archive or a physical validation.

Three material assumptions are explicit:

- **Connections remain rigid:** the chapter extracts nodal rotations because actual connection behavior is not modeled. **232 / 247**.
- **Full composite action:** slab and truss nodes are rigidly coupled without slip, despite acknowledged construction uncertainty. A broader parameter study of shear connection, reinforcement and concrete is explicitly outside the thesis scope. **235–236 / 250–251**.
- **Core columns are unheated:** masonry is assumed to protect them, while the text acknowledges incomplete coverage at some locations. The chapter deliberately explores a pathway different from an earlier core-heating scenario. **231 / 246; 260 / 275**.

These assumptions are not necessarily unreasonable simplifications. They materially affect stiffness, force redistribution and predicted failure opportunities, and therefore must remain visible in any causal assessment.

## Where prediction ends and reconstruction begins

| Stage | What is calculated or presented | What remains assumed or inferred |
|---|---|---|
| Original geometry under thermal loading | Floor displacements, member forces, nodal rotations and differing column movements; some movements stabilize and cooler regions take redistributed load. | Historical exposure and connection capacities are not independently measured here. Rigid nodal rotation is not a validated joint-rupture calculation. |
| Northwest local collapse | Rotations are extracted at the time assigned to the observed first collapse; the less-displaced 11th floor is explained through longer exposure and restraint. **232–237 / 247–252**. | The time of actual detachment is not predicted by an explicit rupture law. Debris photographs do not by themselves date each deformation or weld failure to initiation. |
| Southeast floor cascade | Smoke/dust emergence and inferred floor loss are compared with deformation/rotation concentrations. Figure 7.31 depicts a proposed downward sequence. **240–247 / 255–262**. | No falling-floor mass/contact/impact-energy calculation establishes the depicted cascade or its 4–5-second duration in this chapter. An illustration overlaid on model contours is not a dynamically generated failure trace. |
| Revised damaged structure | Southeast floor sections are removed; external columns alone receive thermal loading. The source reports column instability, load shedding and adjacent-column response. **248–250 / 263–265**, Figs.7.33–7.34. | The missing floors are a prescribed starting condition for this analysis, not autonomously detached by the preceding rigid-connection calculation. Exact removal list, state transfer, exposure history and failure criterion are not supplied as an executable case. |
| Terminal sequence | Three groups of annotated video stills and a summary diagram support a proposed horizontal propagation of perimeter failures. **251–255 / 266–270**. | The entire tower's contact, fragmentation, acceleration and multi-second collapse are not independently simulated or measured by this review. |

The original thermo-mechanical calculation is described as a static sequence without dynamic effects. It uses UmfPack, ModifiedNewton for gravity loading, KrylovNewton for thermal loading, a stated maximum of 100 iterations per step, and 200 nominal 63-second steps. Heat-transfer attempts at larger sampling intervals reportedly had convergence difficulties. These are useful disclosed numerical details, but successful convergence is not a demonstrated stability boundary or a time-step-converged dynamic collapse. **217 / 232**.

The revised calculation explicitly limits reliability to failure initiation because loading is static. Its prose nevertheless refers to the last 4–5 seconds before collapse. Figure 7.33's horizontal axis spans approximately 0–12,000 seconds, not a resolved 4–5-second inertial trajectory. The required mapping between slow thermal loading, prescribed damage state and rapid event time is not demonstrated. No claim that the solver actually failed at a particular step, or that non-convergence alone defined collapse, is made here; the relevant logs are absent. **249 / 264**.

The original and revised calculations also do not establish a one-variable controlled comparison: both geometry and the stated thermal-loading description change. Without the actual paired cases, their different responses cannot be attributed exclusively to floor removal.

Figure 7.38's assertion of accurate propagation toward complete collapse is consequently stronger than the disclosed dynamic scope supports. A defensible description is **conditional instability analysis plus a retrospectively interpreted collapse sequence**, not a complete end-to-end reproduction. This is a limitation of demonstrated scope, not evidence that the author fabricated the calculation. **255 / 270**.

## Contrary outcomes and alternative pathways

The source contains several checks against an oversimplified “local heat necessarily produces immediate total collapse” claim:

1. **Long-lived local damage and stabilized deformation.** The reported initial corner response does not cause immediate global failure. Figure 7.14 shows large deformation followed by much slower change; the text describes roughly half an hour of stability after northwest local collapses. The assumed strength and connectivity of the remaining primary system matter. This is not a demonstrated universal threshold. **229–230 / 244–245; 239 / 254**.
2. **Successful load redistribution before the revised damage state.** The original geometry's heated east/southeast columns shed load to neighboring regions that remain stable in the calculation. The chapter attributes this partly to cooler structure and an intact peripheral beam. Strong coupling can provide alternative support; its mere existence does not require either survival or collapse. **243–244 / 258–259**.
3. **Unequal local responses.** West/southwest regions have smaller reported displacements. The proposed collapse sequence includes a south-facade failure while another facade persists, with later rigid rotation and additional facade failures. This is not a demonstrated globally simultaneous/symmetric terminal motion, nor a measured matched analogue for WTC 7. **239 / 254; 251–254 / 266–269**.
4. **Another fire pathway remains hypothetical.** Out-of-phase column movements motivate a proposed geometry-driven collapse even if connections survived, but the text expressly treats those fire conditions as hypothetical. It does not establish that the original rigid-connection calculation reproduced total collapse without prescribed floor loss. **246 / 261**.
5. **Different load paths can matter.** The author explores perimeter failure with unheated core columns instead of treating core heating as necessary. That is a useful alternative scenario, not proof that the historic core remained cool. **260 / 275**.

The strongest inference in favor of the proposed fire pathway is a conjunction: source-documented fire exposure, calculated thermal deformation/force redistribution, visible signs compatible with local failure, and a revised structural response compatible with perimeter instability. Its weight is conditional on the input and rupture/impact gaps. The same material does not warrant the opposite claim that fire-driven progression is mechanically impossible. The proper next test is to determine whether independently constrained connection and impact behavior actually produces the required damaged state.

## Video evidence and temporal consistency

The thesis stills visibly depict changes in roof shape, perimeter alignment and smoke/dust distribution. But their arrows, dotted column extensions, frame selections and interval labels are author annotations. The text expressly says some columns are not visible in the second sequence. It infers interior floor loss from exterior emissions and proposes a likely column sequence; these are not equivalent to directly seeing every interior connection fail. **240 / 255; 251–254 / 266–269**.

This audit did not acquire or decode those camera originals, establish their native frame timing, calibrate scale/perspective, test possible duplication across clips, or measure their displacement histories. They therefore cannot yet supply an independent common-feature video comparison with WTC 7 or demolition cases. The source's statements about only three available videos are historical source assertions, not a current exhaustive video census.

Several time labels conflict internally:

| Source statement | Direct arithmetic / consequence |
|---|---|
| 3 h 20 min equated to 126,000 s and, separately, to 12,600 s. **217 / 232; 224 / 239**. | 3 h 20 min = **12,000 s**; 126,000 s = **35 h**; 12,600 s = **3 h 30 min**. The stated 200 × 63 s does equal 12,600 s. Native time arrays are needed to resolve what was actually applied. |
| 2 h 50 min captioned as 102,000 s. **223 / 238; 239 / 254**. | 2 h 50 min = **10,200 s**, consistent with a separate Fig.7.20 label. Do not silently repair all arrays from a likely typographical error. |
| Broad 2–3-second final-collapse description alongside Fig.7.35 intervals of 4.2, 1.5 and 5 seconds. **250–251 / 265–266**. | The listed intervals total **10.7 s** if consecutive, as the prose describes. They may cover different stages; stage endpoints and original frames must be reconciled before claiming a duration contradiction in nature. |

The approximately 0.37-radian/22-degree and 0.33-radian/19-degree rotation statements are much less significant precision issues: direct conversion gives about 21.20° and 18.91°. Rounded prose is not the source of the fundamental rupture-model gap. The stronger issue is that these are nodal rotations in a rigid-connection model, without a tested joint-capacity comparison.

Figure 7.17(b)'s 22-degree tangent is drawn on a **construction-stage photograph** to illustrate deformation; it is not a photograph measuring that joint's historical fire-time rotation. Figure 7.18's buckled debris member likewise does not by itself identify when that buckling occurred. **233 / 248**.

The independent reviewer also identified a thermal-gradient labeling conflict, then checked by root on both complete pages. Figure 7.10 labels the hotter slab curve as the **bottom** surface and cooler curve as the **top**, consistent with the adjacent bottom-heating discussion. The next page's prose reverses those surface assignments while reporting stabilized values around 523°C and 179°C. **226–227 / 241–242**. Because gradient direction matters to the proposed bowing mechanism, section coordinates and native histories must resolve this before quantitative reuse. This is a source-description conflict, not proof that the executed model used a reversed gradient.

The time conflicts are source-document inconsistencies, not proved errors in executed input files and not evidence of intent. A clock crosswalk could resolve them; until then, exact model/event timing is not verified.

## Claim ledger and discriminating next tests

A separate [critical review](independent-review.md) read the full chapter and visually checked 34 complete pages. It supports the central scope assessment; its two requested source-precision additions, on thermal-gradient labeling and the construction-photo annotation, are incorporated above after root source-page checks. The review discloses prior Chapter 6 authorship and non-blinded communication; it is not independent historical corroboration or licensed expert approval.

| ID / claim | Layer and grade | Assumptions, alternative, and next falsifier/test |
|---|---|---|
| P7-C01: upper-eight-floor scope, rigid connections and static loading are explicitly reported. | Documentary observation, **A**. | Checked original methods pages; a materially different edition or case requires its own audit. |
| P7-C02: revised southeast floor removal is prescribed, followed by reported column instability. | Documentary observation **A**; physical historical inference **C–D**. | Requires exact removed elements, residual geometry, loads, state transfer and thermal histories. Test paired intact/removed and heated/unheated cases rather than infer the cause from a chosen damaged geometry. |
| P7-C03: rigid-node rotations identify actual connection failure times/capacities. | **Unsupported as an established result, E**; connection-failure hypothesis remains **C–D**. | Need independently constrained temperature-dependent connection laws, weld/gusset capacities and sensitivity. A connection model that retains support under the same exposure would weaken this specific pathway. |
| P7-C04: the chapter dynamically reproduces complete tower collapse and its seconds-scale timing. | Scope claim, **E**. | Contradicted by explicit static/dynamic limitation and truncated extent. Need a separate dynamic model with contact, mass, residual support, energy accounting and converged timing; none was run here. |
| P7-C05: visible sequence independently validates the entire initiating chain. | Inference, **D**. | Same reconstruction supplies chronology and damaged-state interpretation; no held-out metric. Need native multi-camera measurements, declared holdouts and competing predictions that can fail. |
| P7-C06: intact connectivity and cool regions redistribute load; different damage states yield different outcomes. | Published conditional model output, **C** pending reproduction. | Keep original and revised case identities separate. Test uncertain composite action, restraint, heating and residual capacity; neither selected result is a universal law. |
| P7-C07: this source supplies a direct WTC 7 precedent or identifies deliberate intervention. | **E** for either asserted conclusion. | Different structure/exposure and no actor/operation evidence. The chapter's explicit WTC connection comparison concerns **WTC 1 and 2**, not WTC 7. **242 / 257**. |

The immediate case request is concrete: original and revised FE scripts, source-controlled solver/interface versions, gravity/support definitions, six CFD and thermal-field packages, floor/element clock maps, connection assumptions, removal/state-transfer scripts, run logs and raw force/displacement outputs. A model title or open-source engine repository does not substitute for these records. A bounded original-chapter inspection did not locate a downloadable complete case identifier; no new availability search was conducted in this branch.

The highest-value scientific extension would implement independently constrained connection behavior and test whether the same thermal histories actually generate the proposed floor-loss sequence, then dynamically test impact and propagation while retaining stable outcomes. That requires actual case inputs and competent structural review. Guessing missing inputs and calling the result a reproduction would not answer the question.

## Sources

[^1]: Domada Veera Venkata Ramakanth. *Multidisciplinary forensic investigation of buildings in fire: the case of the Plasco Tower*. Hong Kong Polytechnic University, institutional edition 2025. Chapter 7, printed pp.212–262, especially pp.213, 217, 231–236 and 248–255. [Institutional source](https://theses.lib.polyu.edu.hk/handle/200/13847?mode=full); preserved original (supporting item not included in this public package). One research/source family, not multiple independent confirmations.
