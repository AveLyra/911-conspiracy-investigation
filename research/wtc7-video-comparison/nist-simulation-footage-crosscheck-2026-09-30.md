# Exhibit A — NIST's methodologically dubious late-stage exterior-motion validation

**Status:** working research exhibit, completed 2026-09-30; not filed or authenticated as an evidentiary exhibit. This document presents an exploratory visual check against NIST-published materials. It is not a registered experiment or an independent engineering validation.

## Question and short answer

Does the candidate animation correspond to an official NIST-published simulation, and do official sources support the observation that its late-stage exterior motion differs from the footage?

One frame in the candidate derivative visually corresponds to the Northwest full-building visualization on NIST briefing slide 38. More significantly, NIST's own FAQ acknowledges that its predicted inward deformation of the upper exterior walls is not visible in the video after global collapse begins. NIST also reports sharply increased uncertainty in this phase and says its analysis omitted nonstructural components that contribute stiffness and strength.

**Finding:** NIST's late-stage exterior-motion validation is methodologically dubious. Its predicted upper-wall behavior conflicts with the observed video, while the agency identifies major uncertainty and omitted contributors that directly affect structural response. The animation therefore cannot serve as visual confirmation of NIST's account of late-stage upper-wall behavior. This finding concerns that phase and observable; it does not depend on authenticating every frame of the candidate derivative or synchronizing the two local files.

The review contact sheet is included below. The columns are samples from separate file clocks, not synchronized pairs.

![Review-only frame progression: candidate simulation derivative above and Camera 3 secondary copy below; each row uses its own file time.](review/animation-footage-comparison-2026-09-30.png)

## Materials and source status

- Candidate animation: [Wikimedia Commons Ogg/Theora derivative](https://commons.wikimedia.org/wiki/File:NIST_WTC_7_collapse_model_with_debris_impact_damage.ogv), SHA-256 `d926028f5ad980e3f1126071c834ffc85d3d5c4976e68cf2f7a9a543ed424193`. It is a low-resolution derivative containing concatenated clips; it is not authenticated as a NIST-native/master file.
- Footage: `media/analysis-source/NIST Camera 3.mp4`, SHA-256 `0c147549fa51c57686bd506c1d979af23835e72ac777fa30e2f2eb8b15aeb8be`. The acquisition manifest identifies it as a secondary-hosted 15 fps copy, not a native camera original or complete broadcast master.
- Official comparators: NIST's [August 26, 2008 technical briefing](https://www.nist.gov/system/files/documents/2017/05/09/WTC7TechnicalBriefing_082608-WEBCAST.pdf), [NCSTAR 1-9](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf), [WTC 7 FAQ](https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation), and [photos, videos, and simulations archive](https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations).

## Findings

### Simulation sequence

NIST briefing slide 38 (PDF page 38) is titled “Physics-Based Visualization of WTC 7 Collapse.” It labels the view “North-west” and shows an LS-DYNA simulation clock reading 8.5. The candidate derivative frame at source file time 8.8 seconds has the same view label, clock reading, framing, and visible model pose. I visually compared the two frames; I did not calculate image registration or pixel similarity.

This is strong visual correspondence to a frame in NIST's published sequence. It supports that the candidate's full-building segment carries at least this NIST-published visualization frame. It does not establish byte identity, continuous lineage, or that every part of the concatenated derivative is an official NIST file. The NIST archive distinguishes collected materials, original video from tapes, and NIST-generated simulations, but the existence of those archive categories does not authenticate these particular copies.

### Camera 3 report images

NCSTAR 1-9 reproduces Camera 3 views at event-relative times, including figure 5-193 at 1.0 second after east-penthouse descent begins and figure 5-202 at 8.1 ± 0.1 seconds after it begins. By manual inspection, frames from the local Camera 3 copy at file times about 4.7 and 11.8 seconds broadly correspond to those report reproductions. This comparison uses an approximate file-time offset of 3.7 seconds. It was not registered or tested by pixel correlation, and it does not establish an exact offset or synchronization.

These report figures are official reproductions of footage used in NIST's analysis; they are useful source checks, but they are not a separate camera master or an independent analysis.

### What differs in the sampled images

In the candidate simulation samples (file t=16.8–24.8 s), the rendered building starts nearly full-height. As the sequence advances, the left-facing wireframe side folds and loses alignment; by the last samples it is ragged and discontinuous, while the large blue face remains mostly upright. In the Camera 3 samples (file t=10.5–14.0 s), the visible roofline and broad façade descend lower in the image over time. Smoke and foreground buildings increasingly block the view, so the footage copy does not give a clean view of the building base or a complete final collapse.

The concrete visual contrast is therefore between a simulation in which one rendered exterior side deforms inward and breaks up while another face remains largely upright in the final sampled frame, and footage in which the visible roofline/façade moves downward as smoke and foreground occlusion grow. The Camera 3 view does not clearly display the same inward upper-wall deformation visible in the render. This is consistent with NIST's FAQ description of the late-stage difference. The viewpoints are not calibrated to show that the deforming mesh side is the exact façade seen by Camera 3, and the samples are not synchronized; this is a comparison of visible progression, not proof that two paired instants behave differently.

### NIST's admitted late-stage difference

In its answer to FAQ question 25, NIST states that “only in the later stages of the animation, after the initiation of global collapse,” do the upper exterior-wall deformations differ from the video images. More specifically, NIST notes that large inward deformations of the upper exterior walls in its analysis are not visible in the footage. NIST says late-stage disparities were expected because collapse progression became highly uncertain and the analysis did not include the stiffness and strength contributions of nonstructural components such as cladding, walls, and partitions.

That official statement corroborates the qualitative observation that the model's late-stage upper-wall deformation does not closely reproduce the visible exterior motion in the footage. NIST also identifies why its own result is less secure at this stage: its analysis faced sharply increased uncertainty and omitted contributions from nonstructural components.

### Methodological finding

The methodological defect is specific: the late-stage simulation predicts inward deformation of the upper exterior walls that the video does not show, yet the simulation remains part of NIST's account of the collapse sequence. NIST's stated defense—that late-stage disparities were expected—confirms the limitation; it does not make the model/video mismatch disappear. NIST's acknowledged uncertainty and omitted nonstructural contributions make the late-stage exterior result a weak basis for confident claims about what the visible upper walls did.

The contact sheet illustrates the difference: the rendered mesh folds and breaks up on one side while another face remains mostly upright in the last sample; Camera 3 shows the visible roofline and broad façade descending as smoke and foreground obstruction increase, without clearly showing that inward upper-wall deformation. These samples are not synchronized, but the methodological finding does not rest on treating them as simultaneous frames: NIST itself states the event-relative model/video discrepancy in FAQ question 25.

## What the comparison supports

| Proposition | Assessment |
|---|---|
| The candidate contains a frame visually corresponding to NIST's published Northwest simulation sequence. | Supported at the frame level by the matching view, simulation clock, and pose. Native-file provenance remains unverified. |
| NIST acknowledges a late-stage difference between modeled upper-wall deformation and the video. | Supported directly by NIST FAQ question 25. |
| NIST's late-stage exterior-motion validation is methodologically dubious. | Supported by NIST's acknowledged mismatch between predicted inward upper-wall deformation and video, together with its stated uncertainty and omitted nonstructural contributions. |
| This exhibit establishes that every part of NIST's investigation was methodologically invalid or establishes another cause of collapse. | Not established here; the finding is about late-stage upper-exterior motion and its visual validation. |

The briefing, report, FAQ, and simulation publication all come from NIST. They are official source checks, not independent validation. A stronger test would require authenticated source files, defensible synchronization and viewpoint calibration, and a reproducible comparison using declared features and uncertainty before selecting frames or time offsets.

## Method and limits

The comparisons above were visual and retrospective. The sampled file times were inspected after viewing the sequences. There was no prospective protocol, exact camera calibration, synchronized frame pair, image-registration score, displacement estimate, or model rerun. The NIST event-relative report timings were used only to contextualize the sampled Camera 3 frames; they do not synchronize the two local files.

The NIST archive's current page lists separate categories for collected photographs/videos, original video from tapes, and NIST-generated computer simulations. The current public archive review did not identify an authenticated native copy of the particular full-building animation used here. The Commons derivative's NIST label and visual match to one official slide are not sufficient to prove the derivative's complete provenance.

## References

1. NIST, *WTC 7 Technical Briefing*, Aug. 26, 2008, slide 38, “Physics-Based Visualization of WTC 7 Collapse,” Northwest view, LS-DYNA clock 8.5.
2. NIST NCSTAR 1-9, printed pp. 262–263 (Camera 3 location and timeline) and figs. 5-193, 5-202 (event-relative Camera 3 views).
3. NIST, WTC 7 FAQ, question 25 (model/video differences and late-stage uncertainty).
4. NIST, WTC photos, videos, and simulations archive (collection categories and generated-material categories).
