# Camera2 source, settings and calibration review

2026-09-19. Bounded independent source/settings review for `camera2-paper-frame-join`, under the investigation charter. Research only. This reviewer inspected the held paper, acquisition record, prior source reviews and sanitized settings, without seeing root's new frame annotations or deriving a trajectory, acceleration or cause. The review is independent of root's new placements, not independent of the shared paper, held media or earlier research.

## Finding

**The paper-to-download join is established at the public file-ID level; no Camera2-specific saved Tracker project or calibrated frame/time origin was identified in the searched extracted holdings.** The located saved project is explicitly Camera3. Its scale, start frame, time zero and three-frame step cannot be transferred to Camera2.

The narrower wording matters: the kit inventory includes WTC7 projects under other names whose contents were not inspected in this unit. An original Camera2 project may be differently named, unextracted, held elsewhere or not acquired. This search does not establish its nonexistence, destruction or unavailability from the author. Missing configuration also does not demonstrate that the paper's measurement procedure was wrong.

## Paper-to-source joins

Primary paper: Chandler, Walter and Szamboti, *The Instantaneous Free Fall of World Trade Center Building 7 and NIST's Attempt to Hide It*, Journal of 9/11 Studies 42, June 2023. Held at `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf`; 51 physical pages. Fresh SHA-256: `cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394`. Its earlier acquisition note records `https://ic911.org/wp-content/uploads/2023/06/chandler-walter-szamboti_instantaneous-free-fall_june-2023.pdf` on September 19. That acquisition is attributed to the earlier record, not newly repeated here.

| Source pin | Directly supported content | Remaining join |
|---|---|---|
| Paper p. 50, Camera2 bullet and embedded URI annotations | Google Drive file ID `1RGWHdqt_PO_Z-KlWhXza0QBq909BEGmC`. | Matches the acquisition manifest's `VID-WTC7-001` row exactly. The PDF has two identical Camera2 URI annotations because the visible link wraps; these are one source link, not independent sources. No current remote byte comparison or native-master authentication was performed. |
| Main acquisition manifest, row `VID-WTC7-001` | Held `analysis-source/NIST Camera 2_CBS-Net Dub6 48 (Converted).mov`; 208,810,910 bytes; acquired September 2, 2026; preserved analysis-source copy. | Its express `Converted` title and secondary hosting do not establish the native camera, CBS tape, NIST production or original analysis input chain. |
| Paper p. 13, section 3.1 / Figure 4 | Camera2 north roofline identities: neon-green NE, blue east-center, orange west-center, red NW; separate dark-green north screen wall and light-blue west penthouse. | The source image is illustrated with circles, not a native-pixel coordinate export. Exact pixel placement, material-feature continuity and a particular source frame need the separate image join. |
| Paper p. 13, sentence immediately before Figure 4 | East penthouse had already collapsed when the illustrated frame was taken. | Figure 4 alone cannot identify the paper's zero frame. No timestamp or frame index is printed there. |
| Paper p. 15, Table 1 and footnote | The authors assign east-penthouse collapse start to 0.0 s and say tracking uses 0.2-second intervals on even decimal values. | No Camera2 start frame, file PTS, frame-step property, original exposure rate, six-frame selection, loading override or source-time export is supplied on this page. The onset labels are author assignments. |
| Paper p. 10, discussion and Figure 3 | Earlier Dan Rather footage and Camera2 are described as different footage; Figure 3's earlier-analysis clock uses global-collapse/Stage 1 initiation as zero. | Do not carry that earlier graph zero into Appendix A. The paper's current event clock is the p. 15 east-penthouse origin. |
| Paper p. 50, reproduction-material paragraph | Links a physics-lab kit, calibration data/tutorial and Tracker; the three camera download links are separately listed. | A link to a general kit does not identify which saved example produced the current Camera2 measurements. No numerical Camera2 scale or architectural calibration endpoints were recovered from the inspected paper pages. |

The earlier full-paper method search and complete Appendix A review are recorded in [method-review.md](../multipoint-table-reproduction/method-review.md); this reviewer newly viewed complete physical pages 10, 13, 15 and 50 and extracted their text/URI annotations. Broader paper-method claims remain attributed to that prior review.

## Held records and exact pins

In the following table, `MAIN` is `/Users/admin/docs/911`; `INV` is `MAIN/research/sherlock-wtc7-investigation`; `KIT` is `INV/camera3-provenance/kit-inventory/run-v1`. All hashes below were freshly checked with `shasum -a 256`. These are byte-identity pins, not historical-authenticity findings.

| Held path | SHA-256 |
|---|---|
| `MAIN/research/wtc7-video-comparison/media/analysis-source/NIST Camera 2_CBS-Net Dub6 48 (Converted).mov` | `84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730` |
| `MAIN/research/wtc7-video-comparison/media/video-acquisition-manifest.csv` | `5f39f34f6ba978ff8e030c632ab49c54950faaaf2fb3654ccd5cdc14bdfee6dc` |
| `INV/timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/frame-map.csv` | `ccc78c7ff933710f8e8e767dce5e05855fefb05bb75241d2bec01b4739c3b812` |
| `INV/timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/streams.json` | `d54e30ca5e8bece9ba61769e3916741caa14ea3f4b4c0b6dc7757685ec50daa1` |
| `INV/camera3-provenance/WTC-911-Motion-Lab.zip` | `c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189` |
| `KIT/outer-entries.json` | `f1b2e18d9d1f0c2b4c3c90129d28d59bac6649d46af7e4ef48ff5d742a168161` |
| `KIT/saved-tracker-settings.json` | `ccfd9c4de098539680caf9f296eb5ea784ade27497d860a32284285e577cefeb` |
| `KIT/nested/Camera3-test_Camera3-test.trk` | `955d1c2d00d7c287f4f235063eb603a0080cf0941595a5419aa7c94726c1a41c` |
| `KIT/outer/The Kit/WTC7-Camera 3/Camera3-test.trz` | `aceb800c8baa6b39ceba698fcf16198fe9f0480c66673065d31e0203c09306a8` |
| `KIT/outer/Lab-Instructions.pdf` | `c3a9c7aa44f914dbcc7dd2e5604020db0466de8c27f9d71f70d485b80aeb5557` |
| `KIT/outer/The Kit/WTC7-Camera 3/WTC7 Floor Spacing.pdf` | `8dacd6cbb61b554c21da2cfa6447ebbb3248a06d04a44596b5c31088e5beb411` |

Fresh read-only `ffprobe` on the Camera2 MOV reports H.264, 640 x 480, 8,042 frames, `r_frame_rate=30000/1001`, `avg_frame_rate=2997/100`, `time_base=1/2997`, `start_pts=0`, duration 268.335002 s. Encoded PTS zero is the file origin, not an observed east-penthouse onset. The prior timing audit documents 99/100/104-tick adjacent intervals; no full decode or row-by-row frame-map verification was rerun here. The source-specific six-frame hypotheses in [CLOCK-ADDENDUM.md](../multipoint-table-reproduction/CLOCK-ADDENDUM.md) remain hypotheses, even though they account for the prior derivative-rounding discrepancy.

## Camera3 settings that must remain separate

The selected settings JSON is already sanitized. This unit read that JSON and rehashed the original TRK, but did not emit the TRK's author-machine path fields or launch Tracker. The prior source-unit audit, [clock-source-review.md](../metric-motion-audit/clock-source-review.md), independently inspected the original XML and relevant versioned source semantics. Its findings are attributed prior work here.

All XML field pins below start at `object:org.opensourcephysics.cabrillo.tracker.TrackerPanel`; abbreviations retain the exact property and class names represented in the JSON's `xml_path` fields.

| Field pin under TrackerPanel | Saved value and Camera3-only meaning |
|---|---|
| `semantic_version`; `videoclip/VideoClip/video/XuggleVideo/path` | `6.1.2`; sanitized referenced basename `Camera3.wmv`. This is affirmative evidence that the located saved analysis belongs to Camera3. |
| `videoclip/VideoClip/{video_framecount,startframe,stepsize,stepcount,starttime}` | `442, 138, 3, 102, 0.0`. These do not set a Camera2 source frame, step or time zero. |
| `clipcontrol/StepperClipControl/{delta_t,rate,frame}` | `66.66666666666667, 1.0, 138`; prior source audit identifies mean frame milliseconds versus playback rate. It does not authenticate the historical engine time array. |
| `coords/ImageCoordSystem/framedata/[0]/ImageCoordSystem$FrameData/{xorigin,yorigin,angle,xscale,yscale}` | `(515.7950065703022,400.52562417871223)`, `0.7240787271407187`, and equal scales `3.3366687576783383`. Prior source audit identifies degrees and pixels per assigned metre. No cross-camera/raster/projection map exists in these fields. |
| `tracks/item/TapeMeasure/worldlengths/[0]`; `length_unit` | `58.293`; `m`. The saved endpoint pair is `(414.3770672546858,196.24035281146615)` to `(416.95700110253586,390.7276736493937)` in the TapeMeasure's `[0]` framedata. No Camera2 correspondence or architectural endpoint labels are supplied. |

The prior six-page calibration review found a coherent floor-spacing method and seven possible 15-floor-interval pairs for the assigned 58.293 m. It did not recover a unique saved floor pair. Both that positive dimensional lead and its provenance/endpoint limit remain: [calibration-source-review.md](../metric-motion-audit/calibration-source-review.md). The lab page 3 timing example is explicitly Camera3/15 fps/three frames. It is not documentary proof of Camera2's proposed six-frame step.

## Search coverage and unsearched material

1. Filename searches ran under main's `research/` and this investigation worktree's `research/`, including ignored files (`rg --files -uu`), for `.trk`, `.trz`, calibration/settings names, and Camera2 names. Main's only extracted TRK/TRZ hits were `run-v1` and `run-v1-repeat` copies of Camera3; worktree had no extracted TRK/TRZ hit. Broad private directories, mail, legal productions and other worktrees were not scanned. The root's new `camera2-paper-frame-join` content was excluded/unread.
2. Read all 55 entry names in the existing `outer-entries.json` inventory and queried them for `camera[ _-]*2`: no named hit. This is an inventory-name result. The ZIP was rehashed but not reopened, extracted or recursively inspected in this unit.
3. Besides Camera3 entry 34, the inventory contains entry 41, `The Kit/WTC7-Dan Rather/DistantViewWTC7.trz` (member hash `8afe02fa78440768ff01bf4cd7cdcd27cbe872466f46be80d79115708c381c0e`), and entry 54, `The Kit/WTC7-Tilted Camera/WTC7TiltedCamera.trz` (`7eee39a3f9c802343204d7f3f595478ab4c5a7c6c54ca8e2928c46c7ed8b7552`). Both remain `inventory_only`. Member hashes are reported from the preserved inventory, not freshly recomputed. Page 10 distinguishes Dan Rather footage from Camera2; the Tilted Camera name alone does not prove or exclude a Camera2 relationship. Associated counted-window pictures, the overview and unextracted documents were not inspected for hidden calibration references.
4. Consulted multipoint `report.md`, `method-review.md`, `validation.md`, clock addendum, main's acquisition and timing records, Camera3 provenance/kit inspection, and the metric-motion source reviews/report's source-specific sections. Existing research Markdown searches located no new Camera2 saved-settings artifact beyond these leads. Search snippets were not treated as complete source review.
5. No new web retrieval, current-site query, author contact, account access, original project request or archive extraction occurred. Whether newer or differently named Camera2 settings are available from the paper's source remains untested.

## Next independent calibration and clock work

The highest-value local calibration step is a Camera2-specific architectural correspondence: freeze the exact source frame and independently mark two clearly identifiable, vertically separated features on the same north-façade plane, then join those exact feature definitions to a dimensional source. Record endpoint intervals, axis direction, pixel aspect/crop, optical-depth assumptions and variation across the façade before calculating a scale. The held floor-elevation sheet can supply an explicitly conditional dimensional lead; it cannot by itself identify window tops, parapet tops or slab levels in Camera2. Original drawing/elevation pins would strengthen that join. Do not estimate scale by forcing the resulting motion to match gravity.

For the clock, freeze an east-penthouse appearance/onset definition and bracket it in native PTS before assigning a new relative zero. Preserve smoke-related ambiguity and distinguish that new analyst-defined origin from the author's unrecovered zero frame. The existing prior screening's left-raised-outline change around f6699-f6729 is only a source-selection lead with smoke/identity caveats, not a recovered paper onset. Do not choose the offset by making the later roofline match the paper's 8.0/8.2-second labels. A Camera2 project/export with its loaded source identity and exact point/time table would test the author-clock join directly.

## Claim grades and executed checks

The file-ID match, held byte identities and literal saved Camera3 fields are **A for the records inspected**. A Camera2-specific original scale, project configuration or zero frame is **D/unresolved**. The strongest objection to an absence claim is the unexamined differently named kit content; the strongest objection to a clock/scale error claim is that no measured error follows from missing provenance. Either an explicitly source-linked Camera2 project or an independently calibrated Camera2 feature/time mapping could change these conclusions.

Actual commands included read-only `shasum -a 256`, `ffprobe -show_entries`, scoped `rg --files -uu`/Markdown searches, `jq` inventory/settings queries, and bundled Python `pypdf.PdfReader` on four pages and p. 50 URI annotations. Complete p. 10 and p. 13 images were newly rendered with `pdftoppm -f PAGE -l PAGE -r 110 -png`; existing complete p. 15 and p. 50 derivatives were viewed. Rendering produced readable pages with Fontconfig configuration/cache warnings. Several overly combined text outputs were truncated; targeted rereads recovered the material relied on. An initial top-level `media` lookup and a guessed `multi-view-screening.md` name did not exist; the located research-media and `multiview-onset-review` paths were used. None of those failures was treated as evidence of absent source material.

No old source, raw result, main-repository file or canonical record was changed. No full media decode, historical fit, all-paper visual review, independent human/expert review, source authentication or causal conclusion is claimed. The evidence-audit skill kept claims conditional and coverage explicit; the PDF skill required complete relevant page review. This completes the bounded settings search, not the wider Camera2 reconstruction.
