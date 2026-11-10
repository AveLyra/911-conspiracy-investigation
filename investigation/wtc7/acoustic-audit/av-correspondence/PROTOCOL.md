> **Historical research:** This document reports a past, bounded computational audit, not a new reproduction or current instruction. Missing image, media and receipt links are marked as unavailable in this package; see the [publication note](README.md).

# Video edit and audiovisual-correspondence screening

Declared 2026-09-11 before new frame inspection or extraction. This follows the audio audit (historical local reference `../report.md`; not included here) under charter WP2/Q07/Q10. It checks the preserved compilation's visual sequence, not the original camera clock, historic sound source, or collapse cause. Previous edit/timing descriptions are leads, not ground truth; selection is retrospective.

## Inputs and declared coverage

Use the unchanged VID-WTC7-006 and VID-DEM-001 video-only access copies, with the exact hashes/sizes in the prior audio run receipts and acquisition manifest. Use the previously full-decoded, stereo audio derivatives only with their recorded start/end and hashes; no re-seeking audio, gain correction, reconstructed soundtrack, platform metadata export or fresh media acquisition. Original bytes, prior outputs and transcript remain untouched.

Initial visual coverage uses the half-open intervals below. **Prospective amendment before extraction:** independent review identified that the originally proposed separate [434,436) and [441,443) quarter-second samples left the intervening passage unchecked. Those two intervals are replaced by every presented frame in [434,443), so a statement about the between-cut sequence is not based only on endpoints. Other intervals retain the first presented frame in each quarter-second bin. This amendment was made before any new video inspection or source extraction; original proposed coverage was 68 compilation plus 12 comparator samples.

| Video | Interval(s), uploaded-track seconds | Question |
|---|---|---|
| 27 Angles | [434,443), every presented frame | Do apparent cuts replace the view near the prior 435 / 441.9 s references? Is continuous building descent actually shown in the passage or across the latter transition? |
| 27 Angles | [580,582) | What visual transition accompanies the old transcript's start-of-live-segment neighborhood? |
| 27 Angles | [599,610) | When does the image change from foreground reporting toward the building/dust, independently of transcript segment labels? What is visible versus blocked or outside frame? |
| Comparator | [12,15) | Is there visible building change or initiation imagery in the previously cited neighborhood? This is not a refreshed method label or acoustic classification. |

Expected coverage at the declared stream cadences is 322 compilation and 12 comparator frames, with true source PTS retained rather than relabeling each as exactly the bin boundary. Each whole frame must be preserved before thumbnail assembly. Any missing bin or conflicting frame clock is a failure/limit, not permission to substitute interpolated imagery. Reading every frame as an overview is not the same as full-resolution examination; state both coverage levels.

## Method and checks

1. Read only allowlisted stream/frame timing/geometry/color fields. Pin sources, old helper used as an implementation reference, new code/protocol, binaries and runtime. Before any historical frame extraction, validate the same selection/RGB-output procedure on a deterministic synthetic lossless video with known pixel values and source timestamps; include a nonzero timestamp fixture and reject uncovered bins. Synthetic success is software verification, not historic authentication.
2. Adapt the already reviewed `fire-originals/peskin/sample_every_second.py` selection/showinfo/preservation pattern. For this short source, decode from the beginning, disable autorotation/autoscaling and requested frame-rate conversion, preserve source timestamps, select quarter-second bins, and explicitly convert to RGB for full-frame PNGs. Record that RGB conversion is not colorimetric calibration. Separately probe frame PTS and require exact selected-index/timestamp/dimension agreement, not only an equal file count. Preserve native raster aspect metadata; no display-aspect correction or cropping of preserved frames.
3. Create labeled overview sheets from the saved frames. Two runs must reproduce selected PTS, PNGs and overview bytes; receipts may differ in paths. Existing output directories must be refused without source/output change. Diagnostics stay local; no blanket metadata clearance.
4. Root and a separate computational reviewer inspect the overview frames, then full-size frames around candidate transitions. Record uncertain/obscured imagery. A cut is a change of shot/content, not automatically a jump in event time; a camera pan is not automatically a cut. Text overlays, person reactions and background building/dust changes are different observable categories. Do not assign a causal mechanism from image morphology.
5. Permit **one declared refinement pass** after initial screening: all source frames in at most four one-second intervals bracketing candidate visual transitions, chosen and logged before extracting them. The purpose is to narrow access-copy cut/visibility brackets, not to infer sub-frame precision or a physical collapse start hidden from view. Preserve the first-pass outputs and selection rationale.
6. Compare visual screening brackets with the existing transcript navigation intervals only as a coordinate crosswalk. A text segment need not begin at its first word, describe a current event, or share the video scene's original clock. Where useful, calculate per-channel digital power around an observed edit from the retained full-decode WAV, recording exact sample indices and window sizes. This is not listening, sound-source identification, or an A/V-delay calibration. Any exploratory subwindows must be declared before those calculations.

## Acceptance and scope ceiling

Deliver a source-pinned visual coverage and transition ledger with frame references, agreement/disagreement and uncertainty; distinguish statements actually supported by the images from legacy interpretations. Retain incomplete or contradictory outcomes. A separate computational review is not a genuine human spot-check or qualified acoustic review. No consequential automated event classification or calibrated motion/acceleration measurement is authorized by this screening protocol.

No explosive/nonexplosive verdict, absence-of-sound inference, recovered native camera chronology, or numerical causal ranking follows. A demonstrable compilation edit limits chronology but is not evidence of deceptive intent. Human sound review, original-source lineage, microphone/distance and scene synchronization remain separate gates. No legal record promotion, held packet use, bridge invocation, feedback transfer, outreach, commit or push.

Root owns code/protocol/runs/report/verification in this new directory; the second reviewer owns `independent-review.md` and its agreed `reviewer-check/` outputs. Existing parent audit receipts/review attestations remain historical and unmodified.
