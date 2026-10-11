# Animation–footage visual comparison (review only)

**Completed:** 2026-09-30

**Scope:** qualitative progression in a candidate NIST simulation derivative versus the repository’s Camera 3 secondary copy. This is a review-only comparison; the experiment registry remains blocked/unreviewed and no data were registered. The timestamps were selected after viewing the sequences, and the written protocol was prepared afterward; this is exploratory, not a prospective or confirmatory comparison.

![Independent source-time progression samples: candidate simulation derivative (top) and Camera 3 secondary copy (bottom). Columns are not synchronized pairs.](/Users/admin/docs/911-worktrees/faraday-wtc7-model-compare/review/animation-footage-comparison-2026-09-30.png)

## Result

The broad views are compatible enough for a qualitative juxtaposition: NIST labels a full-building visualization “View from Northwest,” and its report places Camera 3 near street level on the west side of West Street near Harrison. That supports a broad viewing-quadrant comparison, not an exact camera match or pixel-level registration. ([NIST briefing](https://www.nist.gov/system/files/documents/2017/05/09/WTC7TechnicalBriefing_082608-WEBCAST.pdf), pp. 37 and 23; [NCSTAR 1-9](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf), printed pp. 262–263.)

**Direct observations in these copies:**

- Across the sampled Camera 3 frames (file t=10.5–14.0 s), the visible roofline and façade descend substantially in the image. Smoke and foreground buildings increasingly obscure the structure; the clip does not show a clean, unobstructed view of the complete final collapse.
- Across the sampled animation frames (file t=16.8–24.8 s; displayed simulation-clock overlay visible in the frames), the model’s near-side exterior mesh becomes progressively discontinuous and deformed. The other large blue façade and most of the model’s overall vertical extent remain visible through the last sampled frame.
- Those are different visible descriptions: a camera image of apparent whole-building descent/occlusion versus a rendered structural mesh with progressive local/side deformation. The samples do not establish that the animation’s deformed side corresponds to the specific façade plane visible in Camera 3.

**Interpretation, limited:** these sampled sequences do not visually match in a simple frame-for-frame sense. That is a qualitative observation about the derivative and secondary copy, not a measurement of the original NIST model’s accuracy. No claim is made here about physical cause, structural mechanics, or whether the model was intended to reproduce the exact camera footage.

## Synchronization and limits

No compatible event with defensible common timing was established. The animation’s embedded simulation clock is not the Camera 3 file clock, and neither the Commons derivative nor the Camera 3 secondary copy has been authenticated here as a native/master export. Frame selections are labeled on their own source clocks and intentionally are not presented as paired timestamps. Accordingly, this comparison does **not** evaluate onset timing, collapse rate, displacement, or time-aligned shape agreement. The NIST report’s published event timeline is context, not a substitute for syncing these exact files.

The candidate Commons item is a derivative and contains concatenated clips. The Camera 3 source is 720×480 at 15 fps and 15.464 s; the animation derivative is 464×338 at 25 fps and 24.880 s. The montage preserves aspect ratio and makes no geometric registration. Provenance and resolution limit what can be inferred.

## Reproduction record

- Candidate animation SHA-256: `d926028f5ad980e3f1126071c834ffc85d3d5c4976e68cf2f7a9a543ed424193`.
- Camera 3 SHA-256: `0c147549fa51c57686bd506c1d979af23835e72ac777fa30e2f2eb8b15aeb8be`.
- Frame extraction/metadata inspection used `ffmpeg` and `ffprobe`; the contact sheet was assembled with Pillow, aspect-preserving fit, no interpolation between frames, and no perspective or spatial registration.
- Public source description: [NIST August 26, 2008 briefing](https://www.nist.gov/system/files/documents/2017/05/09/WTC7TechnicalBriefing_082608-WEBCAST.pdf), [NCSTAR 1-9](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf), [candidate Commons derivative](https://commons.wikimedia.org/wiki/File:NIST_WTC_7_collapse_model_with_debris_impact_damage.ogv), and [NIST WTC 7 FAQ](https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation). NIST’s FAQ discusses differences in late-stage upper-wall deformation; that is NIST’s stated assessment and is not independently tested by this visual exercise.

## Status

The requested exploratory comparison is complete. Exact synchronization, exact camera/view calibration, and comparison against authenticated native/master files remain unresolved. This artifact does not change the blocked/unreviewed experiment status or register the material as evidence.
