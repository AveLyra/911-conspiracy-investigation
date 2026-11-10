> **Historical research:** This is a dated computational record, not a new analysis or instruction. Local paths are redacted and omitted dependencies marked; see the [publication note](README.md).

# Independent comparison results and post-output visual review

2026-09-11. Completed bounded comparison of the 60 frozen feature/frame annotation rows at two template sizes: **120 records**, using `run01`; the corresponding 120 `run02` records are exactly equal. This is a computational AI review, not human ground truth, forensic authentication, a pristine holdout or camera calibration.

The original [comparison plan](independent-comparison.md) remains unchanged, including its historical pending-status text. This companion is the additive execution result. The [annotations](independent-annotations.json), their [notes](independent-annotations.md), baseline configuration, run products and original PNGs were not changed.

## Planned numerical comparison

All 120 expected keys were present once, with exact rational PTS and native PNG identities matching the frozen annotations. Both runs report `complete_diagnostic_not_camera_calibration`. The comparison checked consumed product hashes against each receipt, copied protocol/code/configuration lineage against the initial pins, and the 12 baseline/evaluation PNG byte hashes against both runs' input pins. Camera/source association is inherited from the frozen annotations and exact PNG/PTS link, not independent source authentication. No nearest-time or row-order join was used.

| Camera | Template | Frozen localized rows: inside / outside / no coordinate | Passed / rejected among localized | Frozen no-coordinate manual rows | Passed / rejected among those rows |
|---|---:|---:|---:|---:|---:|
| Camera 2 | 19×19 | 30 / 0 / 0 | 23 / 7 | 0 | 0 / 0 |
| Camera 2 | 27×27 | 30 / 0 / 0 | 25 / 5 | 0 | 0 / 0 |
| Camera 4 | 19×19 | 18 / 0 / 0 | 18 / 0 | 12: 6 ambiguous, 6 unavailable | 0 / 12 |
| Camera 4 | 27×27 | 18 / 0 / 0 | 18 / 0 | 12: 6 ambiguous, 6 unavailable | 0 / 12 |

“Inside” means only the prospectively declared inclusive rectangular coordinate test against the **frozen** subjective envelope. The rejected records retain their finite candidate coordinates and rejection flags. These counts are not an accuracy percentage: notably, the R3 annotation error below affects ten nominally inside comparisons. The 24 ambiguous/unavailable size-specific rows have no coordinate error calculated and no replacement identity assigned. No automatic acceptance without manual identity support occurred in those rows.

Specific results:

- C2-R3 is rejected in all ten evaluation comparisons for `low_seed_texture` and `low_ncc`. Its fixed seed standard deviations are approximately 1.8064 Y units (19×19) and 1.8198 (27×27), below the protocol's 2-unit minimum. Its candidate at f6751 is (288,402) for 19×19 and (288,400) for 27×27; all other evaluated R3 candidates are (288,400). Mechanical agreement with the original coordinates does **not** rescue the mistaken feature selection.
- C2-R6 at f6654 and f6751 is inside the manual envelope but rejected for `ambiguous_competitor` with 19×19; 27×27 passes. This is a template-size sensitivity, not disappearance of the visible region.
- Other localized size-specific candidate differences occur for C2-R1 f7013, C4-R2 f1162 and C4-R5 f1162. They remain inside the original envelopes. Each exact signed difference and all supplied scores, competitors, quality flags and coordinates are retained in the JSON.
- All 24 late Camera 4 comparisons (f1259 and f1350, both sizes, six references) are rejected for `low_ncc`; eight also have `search_boundary`, and five also have `ambiguous_competitor`. No late manual coordinate was invented. The two sizes often propose different rejected regions, which are not successful reacquisitions.

## Post-output annotation error: C2-R3

After the automatic overlays became available, the main investigator flagged a possible coordinate/description mismatch. I then re-inspected the **native Camera 2 baseline f6593 and its separately labeled baseline grid**. The mismatch is confirmed: my declared seed (288,400) lies in a dark, low-feature area, whereas the described small bright cap/roof junction is visibly farther right and lower. It is not centered on, or a reliable local anchor for, that named cap. This is a **reviewer coordinate-selection/description-association error**, not merely an unavoidable low-resolution uncertainty.

The frozen annotation's statement that all six named Camera 2 anchors remained identifiable is therefore not supported for R3. The five R3 evaluation annotations, and their ten size-specific comparison records, cannot validate the claimed cap identity. Their original `localized` labels, nominal coordinates and envelopes are retained to preserve the pre-output record, with a separate post-output caution on every affected comparison. No replacement coordinate, reference exclusion, corrected template or rerun was introduced. The baseline patch-center caveat in the original annotation does not excuse the description mismatch.

The fixed low-texture seed also fails the matching protocol's gate, which requires all six references before any transform fit. The outcome cannot support a six-reference Camera 2 registration claim. It must not be converted into evidence that the camera was physically stationary or that no usable alternative reference exists.

## Actual post-output visual coverage

All **24 distinct run01 analytical overlays** were displayed and inspected at original stored resolution, including the derivative's added footer:

- Camera 2: f6593 baseline, f6654, f6751, f6931, f7013, f7104; each at halfwidth 9 and 13.
- Camera 4: f899 baseline, f960, f1042, f1162, f1259, f1350; each at halfwidth 9 and 13.

The [JSON ledger](independent-comparison.json) enumerates every overlay path and receipt-checked SHA-256. Beyond those 24 derivatives, this post-output review revisited one native original and one existing grid (Camera 2 baseline) for the R3 association check. Earlier annotation coverage remains separately recorded: two baseline plus ten evaluation native images and their twelve grids, before automatic outputs. No run02 overlays were visually reviewed in this task, and no unlisted historical frames were inspected for this comparison.

Observed overlay limitations:

- The other five Camera 2 reference markers remain associated with their broad declared neighboring-building regions in this sample. No additional gross reference swap was identified. R6's striped architecture still supplies competing local patterns. Soft silhouettes, background inclusion and different depths remain unresolved.
- Camera 4's six early markers lie on their declared broad regions; banner stationarity remains unproven, and R4 may mark an overlap of structures rather than one material point. The overlays do not cure those role uncertainties.
- In the late Camera 4 frames, red R1/R3/R6 candidates lie on different facade or background regions, while the original sign/lens/window anchors are unavailable. R2's candidates do not securely identify the original banner tip; R4/R5 land among changed-scale foreground corners without establishing original anchor identity. All are rejected, not accepted tracks. The manual ambiguous/unavailable judgments remain unchanged.
- Some late C4-R3 labels are clipped by the right edge. The full reference IDs remain in the JSON; this is a display limitation, not an identity recovery. Colored markers and text obscure a few underlying pixels, so the overlay alone cannot provide precise independent localization at its center.

No claim is made that these image regions are surveyed stationary points. Banner motion, changing illumination, repeated edges/windows, uncertain depth, overlap/parallax, occlusion and scale/reframing alternatives remain active. A passing match or a consistent image transform cannot establish transfer to the target building. No physical displacement, acceleration, support-failure timing, camera synchronization or cause is inferred.

## Reproduction and checks

The small [comparison helper](compare_annotations.py) uses the Python standard library, reads the frozen files and supplied outputs, and does not import or modify the matcher. It writes a new output exclusively, refusing to overwrite an existing file. The original comparison and this annotator's temporary repeat were invoked with bare `python3`; **both outputs record Python 3.14.0**, not the Python 3.13.7 used by the historical matcher. Focused self-tests passed for inclusive/outside envelope boundaries, rejected finite winners, invalid/no coordinates, missing records, ambiguous/unavailable status handling, duplicate-key rejection and exact rational PTS arithmetic. The production comparison completed with no missing keys or provenance-contract failure. The second helper execution wrote `[local-path-sha256:82ea5c4092b93c7e3dc4feafbe7f8294731c7544cdeb027e72a7dafba9e612d2]`, byte-identical to the original comparison JSON as verified by `cmp`; root preserved it as [the agent repeat record](independent-comparison-agent-repeat01.json). Syntax and JSON coverage checks also passed. This byte-identity claim applies to those two **3.14.0 helper outputs**, not to root's later 3.13.7 helper output. Separately, all 120 historical match rows compared between run01 and run02 are exactly equal; broader historical-run verification belongs to the separate verifier.

**Documentation correction:** the earlier version of this note incorrectly stated that this helper ran with Python 3.13.7. That was my runtime-reporting error, confusing the historical matcher environment with the helper's top-level runtime. The original JSON and its reported SHA-256 were already correct and have not been changed. Root's [3.13.7 comparison output](independent-comparison-root02.json) differs from the original JSON only at the top-level `python` field; all other structured fields, including all 120 records, agree. The [additive validation record](independent-comparison-validation.md) preserves the erroneous note's hash, actual runtimes and precise repeat-comparison scope. Re-executing the helper reproduces arithmetic and copies the recorded visual attestations; it does not perform or independently validate the visual review again.

Artifact SHA-256 values:

- Frozen plan: `fc47df3a43e955674a57a87273a6e1dc7c60c9c9cbe921276cff21a54ff800f3`.
- Frozen annotations: `c323d66d504c264df6792e7e5681b2d828dc6ab85db842bde0711a0e94b98b70`; frozen annotation notes: `bd001a83628b0a7725292a9fd957651b7268c88f2b051fcb13fb446fb0fd882e`. All three were checked before and after execution.
- Comparison helper: `98a430f63db694c027f0be190ac7d1772b8376d2b5843f33bcedae6ae8378636`.
- Comparison JSON: `70f4579bea27fc2f31a31303b22c5e50721b8bd7650f72204532d92bbc872937`.
- Agent's retained 3.14.0 repeat JSON: `70f4579bea27fc2f31a31303b22c5e50721b8bd7650f72204532d92bbc872937` (byte-identical to the original).
- Root's 3.13.7 repeat JSON: `83b804897041ca369bfc956e1bf1422ce4347cd8540553beba755202530ee50c` (only top-level runtime field differs).

The development-verification skill guided the helper's narrow independent checks; the evidence and source-of-truth controls kept post-output criticism additive and prevented rewriting the original annotations. No browser was needed for this local file comparison. No new source, supplementary agency-production contents, held packet, raw media decoding, bridge, network, outbound disclosure or causal model was used.
