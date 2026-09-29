# Thermal-property crosswalk: independent source-reading freeze

September 28, 2026. Working research only. This note freezes the assigned source reading before the root's new property-crosswalk findings or another reviewer's results were read. It is a prior-informed AI reading, not a blinded study, independent laboratory experiment, native-model reproduction, licensed engineering review, or historical authentication.

## Controls, scope, and actual checks

The current main-repository AGENTS, WORKFLOW, START-HERE, and investigation CHARTER were read, together with the evidence-falsification-auditor, source-of-truth-guardian, and PDF skills. The initial combined control-file output was truncated; the affected WORKFLOW/START-HERE and charter opening were read separately to recover that coverage. Only the prospective scope/selection portion of [thermal-property-source-crosswalk-2026-09-28.md](thermal-property-source-crosswalk-2026-09-28.md) was read. No later root findings were read before this freeze.

The assigned report is [NCSTAR 1-6A](ncstar-1-6a-source01.pdf), held 328-page source, 22,813,796 bytes, SHA-256 `75b910620ee9c9f202256acd898f01f28a0df23546132c2108a2a1735cb021b3`. The comparison source is the already-reviewed [TN 1771](nist-tn1771-source01.pdf), 2,084,385 bytes, SHA-256 `c94d92defa00689c906f54a7075e4887a1bdd86731688b34d98200ec29fc94e3`. The reviewer independently ran `shasum -a 256` and `wc -c` on these two files, exit 0, matching both pins and byte counts. This was a byte-integrity check, not PDF parsing or historical authentication.

The parent confirmed renderer session 59781 terminal exit 0 before any new NCSTAR derivative was opened. The reviewer subsequently hashed [the receipt](thermal-property-render01/receipt.json), matching `21d1df4b9ad38fbe51e29a41cadcedd8629f1ec572e310badd349dbcdee224b1`. Renderer execution, page-warning accounting, image decode/pixel-hash auditing, and dependency verification belong to the producer/artifact checker; they were not independently replayed here.

Actual full-page image **and** complete corresponding text-derivative coverage:

- NCSTAR 1-6A physical 115–126, printed 63–74: 12 pages.
- NCSTAR 1-6A physical 171–174, printed 119–122: 4 pages, including printed 122's intentionally blank page.
- NCSTAR 1-6A physical 305–314, printed 253–262: 10 pages.
- TN 1771 existing physical/printed 38–42: 5 reread pages, not newly acquired evidence.

Total: **26 selected NCSTAR pages plus 5 TN comparison pages**. Images were requested at original detail and inspected as complete pages. All selected page footers confirmed the NCSTAR physical-minus-52 mapping. The text derivatives have OCR joins and some incorrect table characters; conclusions use the page images, not an unqualified text-search nonmatch. Small product-label text inside the sample photographs was not fully legible and is not transcribed. Table headings, material names, decisive numerical cells, units, footnotes, body qualifications, and graph legends used below were readable. No curves were traced or digitized.

This pass does **not** cover the full NCSTAR report or all of Chapter 6. Printed page 74 ends mid-sentence in §6.3.5, “Concluding Remarks”; its continuation on the next page remains unreviewed in this freeze. The root was notified of that boundary. No original drawings, unselected body pages, network, raw/private production, native inputs, solver, formula evaluation, table-arithmetic model, outreach, or navigation edit was used. The only authored file in this subtask is this note, after a successful create-only absence check.

## Material identity and origin of the measurements

**Printed 63–66 / physical 115–118.** Table 6-1 distinguishes BLAZE-SHIELD DC/F and Type II used in the towers from Monokote MK-5 used in WTC 7. It does not make DC/F a WTC 7 floor-protection material. The surrounding description separates portland-cement/mineral-fiber DC/F and Type II from gypsum/vermiculite MK-5. The report's use of MK-5 as representative of older vermiculite plaster is an explicitly adopted proxy based on the stated information, not a laboratory identity demonstration for every historical installation.

Table 6-3 on printed 65 is **manufacturer-reported** information: nominal DC/F density 13 pcf, conductivity 0.042 W/(m·K) at 24°C; Type II 16 pcf and 0.043 W/(m·K) at 24°C; MK-5 density 20–25 pcf, with its conductivity unavailable there. Those values must not be mislabeled as the subsequent Laboratory A measurements. The table and its footnotes preserve different origins for the quantities.

Section 6.3 on printed 65 describes a commercially procured Laboratory A study, with results delivered as a letter report and data/plot attachments. Printed 66 says the samples were purchased from their manufacturers; discontinued MK-5 was specially manufactured to the original formulation. Three samples of each material were sent: two for thermal conductivity and one for preparing other test specimens. Nominal sample dimensions were 9 × 4.5 × 3 in. The displayed sample photographs and method description provide an identifiable material/test lineage; they are not original production logs, a chain-of-custody authentication, or proof that the thermal model's specimen coating had identical applied density, moisture, or microstructure.

The cited ASTM methods on printed 64 mainly concern physical/mechanical characteristics. Printed 65 expressly says methods developed for other materials were used because there were no ASTM methods specifically characterizing SFRM thermophysical properties as a function of temperature. This is a stated method adaptation, not proof the measurements are invalid or an unqualified claim of a dedicated SFRM standard.

## Conductivity: positive source values, not an established zero input

**Printed 67–68 / physical 119–120; TN 1771 page 42.** Section 6.3.2 describes the ASTM C 1113 platinum hot-wire method. Table 6-4 gives the Laboratory A DC/F conductivity in **W/(m·K)** at temperatures in **°C**, including:

| Temperature | NCSTAR Table 6-4 DC/F conductivity | TN 1771 printed conductivity |
| --- | --- | --- |
| 25°C | 0.0460 | 0.0 |
| 50°C | 0.0687 | 0.1 |
| 100°C | 0.0628 | 0.1 |
| 600°C | 0.2142 | 0.2 |
| 800°C | 0.3380 | 0.3 |
| 1,000°C | 0.5010 | 0.5 |
| 1,200°C | 0.5329 | 0.5 |

These are direct transcriptions, not a numerical model or extracted graph points. The source's four-decimal positive room-temperature value and the TN graph's positive start supply a concrete, favorable explanation for the later one-decimal 0.0: loss of display precision. They substantially weaken the inference that the native solver necessarily used exactly zero conductivity. The selected source does not prove which unrounded number, interpolation, or unit conversion was actually supplied to a particular run.

The DC/F column is materially distinct from Type II and MK-5. For example, at 25°C Table 6-4 lists 0.0534 for Type II and 0.0954 for MK-5, and at 1,000°C lists 0.3708 and 0.2618 respectively. Thus calling this just a generic “SFRM” curve conceals material identity. The TN values and shape align with the DC/F family, consistent with the previously reviewed floor-test material description; that is published-source lineage, not proof of a native case assignment.

Printed 67 also reports substantial specimen shrinkage. MK-5 shrinkage exposed the wire and prevented measurement at 1,200°C; its Table 6-4 cell is blank. That missing MK-5 result must not be replaced with the DC/F 1,200°C value. Figure 6-4 displays Harmathy's older DC/F measurements alongside Laboratory A, with a similar broad increasing trend but nonidentical values. No graph-based exact comparison was performed.

## Density: source linkage is strong, but the source expressly limits validity

**Printed 72–74 / physical 124–126; TN 1771 page 41.** Section 6.3.4 distinguishes room-temperature direct density from elevated-temperature density **calculated** using thermogravimetric mass change and thermal-expansion measurements. X and Z were measured separately because the material was anisotropic; X and Y expansion were assumed equal, and Z was defined perpendicular to the fibrous strands. Expansion testing used a 2°C/min heating rate. All specimens reportedly shrank and lost pushrod contact at about 1,100°C.

Table 6-6 gives mass loss; Table 6-7 gives directional expansion/shrinkage; Table 6-8 and Figure 6-8 give calculated density. The source therefore supplies an ordinary measurement/volume explanation for increasing calculated density despite decreasing mass. **But it expressly calls the high-temperature density variation unrealistic and states that the density values are only valid up to 600°C (printed 72).** This qualification is central. A source match to the rising density curve is not validation of the curve beyond that stated domain.

Selected direct source-to-TN comparisons, both in kg/m³:

| Temperature | NCSTAR Table 6-8 DC/F | TN 1771 page 41 |
| --- | --- | --- |
| 25°C | 236.8 | 237.0 |
| 600°C | 218.2 | 218.4 |
| 800°C | 361.1 | 361.4 |
| 1,000°C | 375.8 | 376.1 |
| 1,200°C | 432.1 | 432.4 |

The similar temperature grid and distinctive rise support lineage to the DC/F calculated-density series, but the printed decimals are **not literally identical**. Unit conversion, rounding, or a different working-data version are plausible explanations for the small differences; this pass did not calculate or establish such a transformation. Table 6-8 gives a conversion footnote, but that footnote alone does not prove the later transformation used.

The later table retains values at 800–1,200°C that correspond to the earlier table's explicitly qualified region. That is a concrete **published-property-domain concern**. It does not yet establish that an executed model used those precise values, how much modeled insulation reached those temperatures, whether a geometry/mass convention compensated, or the magnitude/direction of an output error. Those require native material commands, geometry/volume conventions, temperature histories, and a controlled sensitivity comparison. No such calculation was attempted.

Printed 74 begins §6.3.5 by noting dependence of conductivity and bulk density on spraying/application and expected sample-to-sample variation. The paragraph continues beyond the selected page. The unread continuation cannot be assumed to confirm, qualify, or eliminate the concern.

## Heat capacity: measurement-method distinction and nonidentical later decimals

**Printed 69–72 / physical 121–124; Appendix B printed 253–254 / physical 305–306; TN 1771 page 42.** Laboratory A's heat capacity was calculated indirectly from conductivity, diffusivity, and density. Printed 69 explicitly says that this indirect technique does not directly measure heat-capacity contributions associated with chemical reactions, visible as peaks in the compared calorimetry curve.

NCSTAR Table 6-5 DC/F values include 826.4 J/(kg·K) at 25°C, 941.5 at 50°C, 723.9 at 100°C, 1,189.7 at 600°C, and 1,391.7 at 1,200°C. TN 1771's corresponding entries are 826.9, 942.0, 724.3, 1,190.3, and 1,392.5. The distinctive grid/profile and close values support lineage to Laboratory A DC/F, but the decimal differences should be retained, not described as an exact cell-for-cell identity. Their conversion/version explanation was not evaluated here.

The report did not simply suppress evidence of reaction peaks. Printed 70 describes a separate Laboratory B DSC study after the NIST DSC was unavailable. Printed 71 reports problems with results above 350°C and presents only the lower-temperature results. Appendix B Table B-1, printed 253–254, gives those DSC results; they are **not** the smoother Laboratory A series used for the TN crosswalk. For example, DC/F at 125°C is 2,756 J/(kg·K), and the two source methods plainly have different profiles. That difference is not itself proof that one can substitute the DSC series directly into the old model without new assumptions.

The source discusses plausible contributors to differing peak locations/magnitudes: procedural and operational effects, milligram-scale sample homogeneity/representativeness, and loss from the sample holder. Harmathy and Laboratory B both used a reported 5°C/min heating rate, so their differences cannot be attributed merely to an asserted difference in those stated rates. The material is inhomogeneous, and the selected pages do not give a complete executed model treatment of reaction enthalpy, moisture migration, or evolving geometry.

The rest of the declared Appendix B selection, printed 255–262 / physical 307–314, consists of specific-heat tables and paired plots for 5/8 in gypsum panel A, a 1/2 in panel, 5/8 in panel B, and a 1 in liner panel. These full pages were inspected, including units, table/figure identities, and plotted reaction annotations. They are not steel or concrete-property tables and are not another DC/F property dataset. No inference from these gypsum-panel results is used to close the concrete or steel questions.

## Concrete and steel: unresolved within this actual selection

TN 1771 pages 38–39 show steel density 7856.2 kg/m³, heat-capacity and conductivity tables ending at 702°C, and a statement that the properties came from reference 7. Pages 40–41 show concrete density 2101.7 kg/m³ at 23°C, 1951.5 at 600°C, and 1701.3 at 800/1,000°C; the associated heat-capacity and conductivity tables are also displayed. These TN pages were reread in full.

The **selected NCSTAR material pages, references, and Appendix B do not supply an exact steel-property expression or a continuation rule beyond 702°C**, and they do not identify the concrete material/density/moisture choice behind that TN series. The finding is limited to this 26-page selection. No full-body search or whole-report absence claim was made. A reference could point to unreviewed content, a differently identified source, or a working data file; this pass does not prove a misreference or resolve it by guessing a familiar steel law.

The reference pages printed 119–121 give the ASTM method editions, Harmathy's *Properties of Building Materials at Elevated Temperatures*, DBR Paper 1080 (1983), and other cited literature. They were read as locators only; none of their underlying sources was acquired or inspected. A bibliography is not a native input or a demonstrated material-to-specimen assignment. Printed 122 is intentionally blank.

## Per-question disposition and strongest challenges

| Question | Disposition supported by this reading | Remaining discriminating evidence |
| --- | --- | --- |
| Does printed 0.0 establish zero conductivity? | No. Positive DC/F source value 0.0460 at 25°C and the positive TN graph strongly support a display-precision explanation. | Exact executed material values, units, interpolation, and run identity. |
| Why does SFRM density rise at high temperature? | The source calculates density from mass/volume changes and discusses shrinkage; it also explicitly restricts validity to 600°C. | Actual native density law and volume convention, exposure of relevant elements above the domain, and controlled response sensitivity. |
| Is this generic WTC 7 SFRM? | No. The relevant series follows tower-floor DC/F, while the source identifies WTC 7 MK-5 separately. | Building/specimen-specific material assignment and independently grounded transfer, if such a comparison is later proposed. |
| Are heat capacity and density exact repeated tables? | Close DC/F series/grid correspondence, but the printed decimals differ. The smooth heat-capacity series is Laboratory A, not Laboratory B DSC. | Documented unit/precision/version transformation and choice of reaction/moisture treatment. |
| Which concrete does TN represent? | Not resolved by the selected NCSTAR pages. | Exact material-source page/data, specimen density/moisture convention, and case assignment. |
| How was steel continued beyond 702°C? | Not resolved by the selected pages or the reread TN tables. | Original property function/material commands, temperature domain, and applicable solver interpolation/extrapolation setting. |

The strongest challenge to an unfavorable reading is that the values have an identifiable experimental/material basis and openly discussed limitations; the apparent zero has a concrete positive source value, and numerical similarity is not evidence of fabrication. An adverse conclusion must not erase the report's explicit method discussion or treat a small decimal difference as evidence of a large physical error.

The strongest challenge to a favorable reading is that source provenance is **not** domain validity or execution fidelity. The density source explicitly limits its high-temperature applicability, the specific-heat methods differ in their ability to resolve reaction contributions, material application is variable, and the model's actual data transformations are not supplied. A future native case showing that the qualified values were not used, or that a justified physical/mathematical convention handled them, could weaken the execution concern. Conversely, a pinned case using them without such treatment would make a bounded sensitivity test concrete; it would still not establish WTC 7 causation or intent by itself.

## Freeze boundary

No new causal ranking, accepted source grade, legal fact, or current navigation state is created. This completes only the assigned bounded independent reading, **not the root's whole property-source unit**. The parent advised that its own 26-page pass and synthesis were still incomplete and asked for this note only; no root synthesis was reviewed. Any later expansion, arithmetic comparison, or root-draft critique must be separately labeled after this frozen body. Earlier independent-review files and source bytes remain untouched.

## September 28 pre-synthesis continuation supplement: printed 75

This separately authorized continuation preserves the initial **17,973-byte** body above, frozen at SHA-256 `20b465a321f98eeaedb25b5ace5ed18bc053f86d8f58cd0784252313ef0ab331`. The initial freeze had already been saved when the parent's one-page extension message arrived. The parent prospectively selected NCSTAR 1-6A physical **127**, printed **75**, and confirmed the create-only `thermal-property-render02` run had terminated successfully before this reviewer accessed its products. The reviewer independently hashed [the new receipt](thermal-property-render02/receipt.json), matching `deb31251a6659031c699ea30b63164f3051a74c6231d00bd617dd7459af323db`; the renderer's execution was not replayed here.

The reviewer read the complete `6a-page-127.png` and the complete accompanying text derivative. The image was requested at original detail; the tool reported display resizing from 1570 × 2125 to 1344 × 1819. All body text, headings, two footnotes, and the printed footer used below were readable. This adds **one NCSTAR page**, for cumulative coverage of **27 NCSTAR pages plus 5 previously held TN comparison pages**. No other pages, underlying cited sources, or root findings were opened for this supplement.

The top of printed 75 completes §6.3.5. Following the prior page's discussion of conductivity as a function of bulk density, porosity, and other material properties, it says attempts to apply existing predictive methods for porous-media conductivity to SFRMs show promise and mentions alternative approaches proposed for future research. Footnote 17 identifies Bentz, Prasad, and Yang (2004), *Towards a Methodology for the Characterization of Fire Protection Materials with Respect to Thermal Performance Models*, as accepted for publication in *Fire and Materials*. This is a cited future-method lead, not a reported implementation in TN 1771, an executed material law, or a relaxation of printed 72's density-validity limit. The citation was not followed.

The remainder starts §6.4, on four gypsum-panel materials, and identifies the same four panel types whose Appendix B heat-capacity tables were already read. Unless otherwise stated, their measurements were performed by Laboratory B. Section 6.4.1 describes commercially available panels purchased locally and samples cut before dispatch to the testing laboratory. Section 6.4.2 describes heated-probe conductivity measurement under ASTM D 5334: a combined heater/temperature-sensor probe, measurement of its heating rate, and selection of a semi-logarithmic segment for calculating conductivity. It points to Table 6-9 and Figure 6-9, which are not on this page and were not newly inspected. These are gypsum-panel methods; they do not establish the DC/F SFRM input, the concrete choice, or steel continuation. Footnote 18's laboratory-method URL was treated only as a printed locator and not opened.

**Disposition:** the previously explicit unread boundary at §6.3.5 is now closed within this supplement. The continuation provides a favorable acknowledgement of promising conductivity-prediction research, but no new numerical property law, native-run evidence, or qualification that removes the source's stated 600°C density-domain limit. It neither resolves the small NCSTAR/TN decimal differences nor the concrete and steel questions. No inference is made about the unreviewed remainder of §6.4, and no experimental, historical, causal, or legal conclusion is added. This supplement remains a source-first, prior-informed reading before root synthesis, not an independent laboratory validation or completion of the parent's full source unit.

## September 28 post-freeze source-synthesis critique

This is a separately requested, non-blinded draft critique, not additional primary-source reading. Before reading the synthesis, the combined source freeze and continuation above were **21,672 bytes**, SHA-256 `b81d98910c56140524cbb71ea2781648bbf9e3c5082e327ac7d0aeae09e03349`. Both that prefix and the earlier 17,973-byte prefix are to remain unchanged. Main AGENTS, WORKFLOW, START-HERE, and CHARTER, and the evidence-falsification and source-of-truth skills were reread for the critique.

Actual draft coverage was the complete then-current 257-line [property-crosswalk note](thermal-property-source-crosswalk-2026-09-28.md); only the newly added paragraph beginning “Following the cited property source” and footnote 24 in [the causal synthesis](../causal-chain-synthesis/report.md); the final “September 28 material-property source crosswalk” section of [SCOPE](../causal-chain-synthesis/SCOPE.md); and [STATUS](../STATUS.md) from its opening through, but excluding, “Previous completed thermal-provenance stage” (then lines 1–40). This is not a review of the rest of the investigation, all preceding synthesis, or the later proposed WTC 7 source task. No new source pages, images, PDFs, network, graph extraction, model runs, table calculations, or code/artifact verification were undertaken.

### Two precise wording corrections requested

1. In the source/material table's “What was tested?” row, **“supplied from a common raw-material batch”** can be read as one common batch across DC/F, Type II, and the chemically distinct MK-5. Keep the batch statement explicitly within each material's sample group, if confirmed by the root's source wording, rather than implying shared cross-material composition. The already supported observations are three samples of each material, two used for conductivity and one for other test specimens; this correction does not question the existence of those tests or establish a batch discrepancy.
2. In “Method limits and favorable evidence,” **“states that application affects density/conductivity and that results vary among samples”** should retain the source's expectation language: density and conductivity depend on application and variation between samples is **expected**. The frozen reading did not establish a quantified, experimentally demonstrated between-sample variability distribution. This is a precision correction, not a claim that the expected variability is physically implausible.

### Substantive disposition within the reviewed scope

The central source conclusions agree with the frozen reading. Positive higher-precision DC/F conductivity is favorable counterevidence to interpreting the printed 0.0 as proof of a zero native input. The source explicitly qualifies its calculated density domain to 600°C; the later printed series's higher-temperature entries therefore require a case-linked explanation rather than being validated merely by matching an earlier table. The synthesis correctly distinguishes that published-property question from actual material cards, applicable temperature histories, geometry/volume treatment, physical error magnitude, or historical execution.

The Laboratory A indirect heat-capacity series and Laboratory B reaction-resolving DSC results remain separate, with problematic higher-temperature DSC results and method limitations retained. Material attribution remains tower-floor DC/F versus WTC 7 MK-5, not generic interchangeable SFRM. Concrete and steel remain unresolved **within the selected source route**, rather than asserted absent from the entire report or improperly supplied to a model. The earlier nominal concrete-specimen number is an inherited source claim, not a newly authenticated value from these 27 NCSTAR and five TN pages.

The new causal paragraph and footnote preserve the permitted inference ceiling, correct printed-page locations, and distinction between source critique, arithmetic, and derivative checks. SCOPE does not promote this work to a causal-grade change or a new historical experiment. STATUS accurately labels the independent reading as 27 plus five pages and, as read, still lists draft critique/documentation QA as pending rather than preemptively cleared.

The next WTC 7 relevance task is appropriately framed as a prospectively scoped source/assignment inquiry with an exact unresolved-input outcome allowed. “Used, replaced, or inapplicable” should be read with that explicit unresolved outcome, not as a demand to classify an unknown native assignment. The proposed work must not infer WTC 7 error from the DC/F issue alone. Existing-coverage checking before new page selection is important to prevent repeated source reading from masquerading as new corroboration.

The strongest favorable explanation remains transparent experimental provenance, a concrete display-precision explanation for the apparent zero, and published thermal agreement that need not be erased by a domain question. The strongest adverse limitation remains that provenance, method plausibility, and repeated publication do not establish valid implementation outside the stated domain. The root note retains both sides and does not claim the selected property pages supply structural-sag execution or prove misconduct.

The reported 33-pair comparison, the 400°C transcription correction, rounding totals, signed differences, artifact counts, renderer/runtime assertions, and code behavior were read as the other reviewers' recorded work, **not independently reproduced or cleared here**. This reviewer did not reopen the 400°C source cell in this critique, so the reported correction is not an additional source vote from this reviewer. Likewise, no claim is made about unselected report content or the correctness of future WTC 7 assignments. Apart from the two wording refinements above, no material source-interpretation or inferential overclaim was found in the exact additions reviewed. Only this appended critique was authored; root must implement and record any corrections to its own files.

## September 28 change-specific correction readback

The reviewer read only the two corrected passages in [the root crosswalk](thermal-property-source-crosswalk-2026-09-28.md), with their immediate text context. The same-batch sentence now explicitly labels the within-material reading and excludes one batch shared across chemically distinct products. The variation sentence now says variation among samples **is expected** and expressly disclaims a quantified measured between-sample distribution. Both requested wording corrections are incorporated; no remaining discrepancy was found in these two changes.

This readback did not reopen source pages, independently verify the root's reported text reinspection, repeat the broader synthesis review, or validate arithmetic, artifacts, links, or runtime claims. The pre-readback note was 27,788 bytes, SHA-256 `d7d27fd4ce56b1abbb3cef6c7e263f109d23e0ce9f42194e3b4ca6322349ec09`. This disposition is appended after that critique and preserves both earlier source-reading freezes; it is a narrow correction check, not a new scientific or historical validation.
