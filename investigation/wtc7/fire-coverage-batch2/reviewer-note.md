# Independent batch-2 visual review — frozen before cross-review

Research-only AI review, 2026-09-15. Reviewer: `/root/fire_batch2_visual`.

The six disclosed text controls were saved before opening any batch image. I then inspected each complete report-native JPEG with `view_image(detail="original")`, in the declared order. No source pages, captions, figure associations, prior/current appearance labels, model inputs or other reviewer results were opened before this freeze. The provenance key was projected only to IDs, native-image hashes, dimensions and paths; that projection included metadata-only entries outside this batch. No outside-batch images were inspected.

Inspected images, all in full:

1. A-873f87e7149b — 480 × 311
2. A-e1b0c06ad11d — 293 × 359
3. A-9e7b4935c8aa — 432 × 291
4. A-0b722775db93 — 384 × 451
5. A-fa6f410444bb — 432 × 359
6. A-ffe3726a0312 — 351 × 468
7. A-0e60b82a1a4c — 431 × 292
8. A-6902e91e39ee — 432 × 316
9. A-671f312eade8 — 384 × 511
10. A-69d899e75343 — 674 × 764
11. A-8bc36f05fe38 — 697 × 480
12. A-7b61385d1373 — 699 × 480
13. A-f1e2fa01e344 — 903 × 740

No crop, enhancement, new resampling, synthetic media or automated flame classifier was used. Rectangles locate approximate regions on original rasters; they are neither segmentations nor window counts, smoke coverage fractions or burning-area measurements. Broad locators can include clear, dark or occluded intervals.

## Evidence and limits

The evidence-falsification-auditor skill shaped the separation of observable appearance from physical interpretation. The structured record keeps luminous morphology, candidate target evaluability, smoke appearance and qualified local nondetection on separate axes. The strongest supported statements concern features visible in these derivative JPEGs and the limits of this review. Flame-like labels describe resolved morphology consistent with flame; reflection, illuminated material, saturation, processing and projected depth remain alternatives. Smooth or poorly resolved luminous patches retain the ambiguous-glow label.

The direct basis for each visual claim is its identified, hashed raster and approximate locator. A repeat inspection or a higher-quality original could weaken a morphology judgment by resolving reflected or illuminated material instead. Dark, smooth, obscured or saturated regions cannot establish interior conditions. A nondetection reports only that this review identified no flame form in an actually visible patch, under the stated opportunity limits. Empty luminous lists and obscured regions are not negative evidence of no fire.

Candidate frontages are localized from visible architecture and retained framing limits. Their identities, hidden edges and floor assignments are not authenticated. Printed labels, arrows and credits were visible and recorded as overlays where relevant. They compromise blindness; neither those marks nor any other image text was treated as an instruction. I am an AI reviewer, not a qualified human forensic examiner. Source selection, general knowledge, low resolution, exposure, oblique views, smoke, glazing, foreground obstruction and unknown original processing constrain these judgments.

In claim-strength terms, the occurrence of this review and the pinned-byte/dimension matches are directly established by the tool observations and checks (A). The image descriptions remain derivative-image observations; their physical interpretation as emitting flame or smoke is materially assumption-dependent (C), and building identity or depth can be underdetermined (D). No temperature, heating history, extinction time, model error, structural consequence, causation or intent is asserted. A higher-quality native sequence with authenticated source/time and the relevant input records would be needed to test those separate questions.

Source-family repetition and clocks were not assessed from captions in this independent phase. Separate filenames do not establish independent events or corroboration. The record covers only these 13 declared images, not the full photographic corpus, report, chronology or investigation.

## Freeze and verification

Frozen observation record:

- `reviewer.json` SHA-256: `2f31b1db855ec6533cd6bb9e7a43670ecc54520fa179a7b2ae4f8e55aa404ac7`
- `reviewer-controls.json` SHA-256: `5de6151bd8d860b4b97db11a332e13cb19a8b6ed1b72fe4bace06161c0eda97c`
- `PROTOCOL.md` SHA-256: `8ea3df6a4550e55de334ac20ce45a8fb05aa00f47800a6ca7b874f74803d94ff`
- Source provenance key SHA-256: `c0361c5a3ae52c2663a6772db6078824b4b123e59d8e50d2e24b26d85855afa3`

Two local deterministic checks passed: exact ordered sample membership; duplicate-key rejection; exact per-asset field set; enums; substantive reason strings; alternatives lists; positive native dimensions; JPEG-header dimensions against the safe metadata projection; every image hash; finite non-boolean in-bounds nondegenerate rectangles; visible-smoke locator consistency; unresolved-target/null consistency; and all six saved controls. All source images, protocol, provenance key, controls and reviewer record were hashed before and after those checks and remained unchanged.

These are integrity/schema checks, not optical-detection calibration or independent physical validation. The separate batch pipeline's synthetic-record tests and cross-review are outside this review note. No disagreements have been reconciled or labels changed after viewing another review. Subsequent comparison must preserve this frozen record and explicitly retain differences.
