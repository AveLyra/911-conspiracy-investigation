# Separate review of the frozen target-annotation comparison

Research-only review after the two annotation sets were frozen and released on **2026-09-11 at 19:46:28 UTC**, as recorded in [annotation-release.json](annotation-release.json). This review preserves disagreement rather than recalibrating, averaging or replacing either observation set.

**Main result:** all 23 co-localized pairs have overlapping subjective rectangles and mutual center containment, but this is not agreement on every appearance-continuity judgment or on the first selected sample satisfying the declared displacement test. T2 f6946 has identical centers but a material correspondence disagreement. At T2 f6931, small baseline/coordinate/envelope differences produce different zero-exclusion results.

## Scope, authority and exact inputs

The [charter](../CHARTER.md) and frozen [protocol](PROTOCOL.md) control scope. The original annotation JSON files control what each analyst recorded; neither supersedes the other. This document is an exploratory comparison/review, not a corrected annotation set, verified case fact, human review or physical calibration. No authority promotion or downstream source mutation occurred.

I read both complete JSON sets, both accompanying notes, and the release record. I reviewed **all 34 matched frame/target pairs**, including all 68 original row notes. This pass opened **no additional images** and did not re-annotate. My prior actual visual coverage remains the 17 native images and 17 coordinate panels recorded before release; root separately attests its corresponding coverage. The current pass is a post-release comparison of those records, not another independent visual observation.

No new root numerical-comparison output or reference-map results were read for this review. The small arithmetic checks below were computed directly from the two frozen annotation sets, independently of root's developing comparison implementation. No reference map was fitted, evaluated, selected or revised.

SHA-256 and byte identities checked in this pass:

| Input | Bytes | SHA-256 |
|---|---:|---|
| `annotation-release.json` | 1072 | `8331cdcffc3b4c1d3eeecac8c85361e05d7026b4310dafd3d932635a6970bcde` |
| `root-annotations.json` | 13771 | `1a6e6b4dc0b34b9f0e33746cc6a568c137311e65493c7e612cd5fa3f3eb72e0f` |
| `annotator-annotations.json` | 23962 | `885b9ca6ef2d762efe44ada1572e56962f81e7e53452f903471949c8e3eeeb2a` |
| `root-annotations.md` | 2389 | `121fcd398aa5d9558090ea171d3dc9237eb3ded6c20653f0b417c4f62e6c7e7a` |
| `annotator-annotations.md` | 5344 | `26dfd0643d1c705e52dd9c79165bc4a1be31ab4ebe9e6469f9bd39b2c194340e` |
| `PROTOCOL.md` | 9294 | `a5c8382402a1afec577b6e1d3c862b0d1a4bd4bac0f5511d5983547686eaf934` |
| `selection.json` | 1821 | `bd87f75f8a0677aa9e8edbf62d0f868eb341088d838c6ec3e3358f36f897190c` |
| `present01/receipt.json` | 9449 | `7ca7abe5bc9d67511213a627a5ae65b1e506952b88896f780779d5fbf7c63f29` |
| `present01/detail.json` | 15486 | `9ae284c756b7b8ae18665ac1b41e97fd442c5f4f38bcd3959438b18c5bdd844a` |
| `../multiview-onset-review/refine01/camera2/selection.json` | 113222 | `dda0cb2e9f17240562e2aafa9443f05df0c2047fd93d8a4e643233cf53e3175e` |
| `../CHARTER.md` | 24068 | `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd` |

The two JSON hashes and byte lengths equal the release pins. Both files contain the same 17-frame schedule and target ordering, share protocol/selection/presentation/source-manifest pins, and record that the other's new coordinates were not seen before their own save. Hashes establish the bytes compared, not chronology by themselves; the release record and local no-coordinate-before-freeze messages document that ordering. Shared proposal knowledge, the same underlying images, computational-AI review and prior event familiarity all limit independence.

## Complete pair coverage

Abbreviations: L = localized; A = ambiguous; N = unavailable; C = appearance-consistent; U = uncertain correspondence; NA = not assessable. Coordinate difference **Δ = separate minus root (x,y)** in native pixels. “Both” applies only to the stated fields, not calibrated correctness or material identity.

| Frame | C2-T1 pair | C2-T2 pair |
|---:|---|---|
| 6593 | Both L/C; Δ=(0,0) | Both L/C; Δ=(0,1) |
| 6654 | Both L/C; Δ=(0,-1) | Both L/C; Δ=(0,1) |
| 6751 | Both L/C; Δ=(0,0) | Both L/C; Δ=(0,1) |
| 6841 | Both L/C; Δ=(0,0) | Both L/C; Δ=(0,0) |
| 6886 | Both L/C; Δ=(0,-1) | Both L/C; Δ=(0,0) |
| 6916 | Both L/C; Δ=(-1,0) | Both L/C; Δ=(0,1) |
| 6931 | Both L/C; Δ=(0,0) | Both L/C; Δ=(0,-1) |
| 6946 | Both L/C; Δ=(0,0) | Root L/C; separate L/U; Δ=(0,0) |
| 6961 | Both L/C; Δ=(1,0) | Both A/U; no coordinate |
| 6976 | Both L/C; Δ=(0,0) | Both N/NA; no coordinate |
| 6991 | Both L/C; Δ=(-1,0) | Both N/NA; no coordinate |
| 7006 | Both L/C; Δ=(-1,0) | Both N/NA; no coordinate |
| 7021 | Both L/C; Δ=(0,0) | Both N/NA; no coordinate |
| 7036 | Both L/C; Δ=(0,0) | Both N/NA; no coordinate |
| 7051 | Both L/C; Δ=(0,0) | Both N/NA; no coordinate |
| 7081 | Both N/NA; no coordinate | Both N/NA; no coordinate |
| 7104 | Both N/NA; no coordinate | Both N/NA; no coordinate |

All 34 localization-status pairs agree: 23 localized, 1 ambiguous and 10 unavailable in each set. Twelve of the 23 localized centers are exactly equal; the other 11 differ by one pixel on one axis. Every co-localized pair has overlapping intervals on both axes, and each center is inside the other's subjective rectangle. These are exact comparisons of the records, not an accuracy or success rate.

The only correspondence-status difference is T2 f6946. Root has 23 appearance-consistent and 1 uncertain row; separate has 22 appearance-consistent and 2 uncertain rows; both have 10 not-assessable rows. Neither analyst asserts a changed replacement identity. Both mark T2 f6961 ambiguous/uncertain and leave it uncoordinated; both mark T2 f6976 through f7104 unavailable/not assessable. Both mark T1 f7081 and f7104 unavailable/not assessable.

Envelope differences also remain substantive inputs: root uses ±(4,4) for T2 f6931 and f6946 while separate uses ±(3,3); separate uses ±(4,4) for T1 f7036 while root uses ±(3,3). Both use ±(4,4) for T1 f7051. Every other localized halfwidth pair is ±(3,3). These are subjective center-localization judgments, not statistical confidence levels.

## Material disagreements and their consequences

### Same center, different appearance-continuity judgment

At T2 f6946 both analysts placed the local corner at **(420,160)**. Root describes a barely separable short upper-step endpoint and retains `appearance_consistent`. Separate describes the near-merger with the lower boundary and marks continuation of the original upper endpoint `uncertain`.

This is not a coordinate-entry error resolved by spatial agreement. It is disagreement about whether the observed local corner continues the accepted image-feature definition. Root's broader envelope concerns localization; it does not itself express or resolve the separate correspondence uncertainty. Under the frozen rule, root's row remains eligible for its own same-feature displacement arithmetic, while separate's row remains localized but **ineligible**. Do not replace either label, report a consensus continuity judgment, or infer that the material point is authenticated.

### Close coordinates, different selected-sample results

For an eligible later sample, the conservative native-y interval is:

`[(y - h) - (y0 + h0), (y + h) - (y0 - h0)]`,

using that analyst's own baseline and halfwidths. A strictly positive lower endpoint excludes zero under this declared arithmetic; a lower endpoint equal to zero does not. These rectangles are not probabilities and may include dependent errors.

- **T1:** both sets first satisfy that condition at selected f6946: center displacement 8 pixels, interval **[2,14]**. The preceding scheduled f6931 is localized/appearance-consistent in both, with interval **[-4,8]**. This is native-image sampled arithmetic, not first physical motion.
- **T2 root:** f6931 has y=152±4 against its own baseline y=144±3, giving **[1,15]**. This is root's first selected eligible positive interval; preceding f6916 gives **[-4,8]**.
- **T2 separate:** f6931 has y=151±3 against its own baseline y=145±3, giving **[0,12]**, which does not exclude zero. Its later f6946 coordinate is not eligible because correspondence is uncertain; subsequent rows are ambiguous/unavailable. Therefore **no selected T2 row in this separate set has an eligible strictly positive native-y interval**. This is not evidence of no motion: nominal positions change, but the accepted arithmetic/identity conditions do not establish that particular result.

The exact source-time pins for these examples are f6916 = PTS 691603, f6931 = PTS 693102, and f6946 = PTS 694600, each with time base 1/2997 second (f6931 reduces to 231034/999 seconds). They are within-camera source times, not wall-clock synchronization or a physical-onset bracket. No interval was filled across the missing/uncertain samples.

These examples expose two distinct limitations: baseline/localization sensitivity at f6931 and correspondence eligibility at f6946. Neither is cured by one-pixel inter-annotator proximity. Root's earlier selected T2 result versus its T1 result also does **not** establish an agreed order of first physical motion or support failure: separate does not reproduce that positive T2 sample condition, sample coverage is sparse, and image-feature identity is not a structural measurement.

### Shared limits, not independent confirmations

Both records describe loss of separately identifiable T2 geometry and eventual T1 obscuration without substituting lower rooflines, nearer-building corners or plume boundaries. Agreement on “unavailable” is agreement on identification limits, not evidence of physical destruction. The shared image source and point definitions can produce shared systematic error; mutual envelope containment cannot authenticate the projected silhouette as the same material point.

The two selected points have limited baseline spatial spread, both on the visible upper outline. Their agreement does not establish whole-building motion, deformation, tilt, symmetry, floor/member identity or a physical camera calibration. In particular, small early nonmonotonic nominal changes remain in the originals rather than being smoothed into a motion narrative.

## Claim audit and bounded wording

| Claim | Layer and strength | Decisive limit / disconfirming evidence |
|---|---|---|
| The stored localization labels match for all 34 pairs, and all 23 paired coordinates mutually fall within recorded envelopes. | Derived record comparison; A for these exact stored values. | Does not validate the image feature or calibrate either envelope. |
| T2 f6946 continues the accepted appearance definition for both analysts. | Interpretation; contradicted as a cross-annotator claim. | Separate's frozen `uncertain` row disagrees despite the same center. |
| Both analysts obtain an eligible positive T2 displacement interval at f6931. | Derived claim; contradicted. | Separate's interval is [0,12], versus root's [1,15]. |
| The comparison validates a physical order of first motion or a cause. | Physical/causal inference; unsupported here. | Sparse samples, correspondence disagreement, uncalibrated projection and missing late features prevent that conclusion. |

Recommended report wording: **“The analysts' localized centers agree within their subjective envelopes, while T2's appearance correspondence and first-selected positive native-y interval are not fully reproduced across the two records. These differences are preserved; no consensus track or physical-onset inference is created.”**

The highest-value follow-up is a separately declared human/specialist review of the accepted point definition and the f6931/f6946/f6961 transition, with a missing-feature option and the two original records preserved. That may clarify appearance identification, but it would still not independently establish material identity or physical calibration. No such review, extra image inspection or retrieval was performed here.

## Check method and execution history

A read-only Python check matched all frame/target keys, computed the 23 coordinate differences, per-axis rectangle overlap and mutual-center containment, and applied the explicit native-y subtraction only to localized/appearance-consistent rows. The actual interpreter was `/Users/admin/.pyenv/versions/3.13.7/bin/python3` and reported **3.13.7**.

The first inline check exited 1 with a `SyntaxError` in the final combined print expression (a missing closing dictionary brace). It failed at parsing, produced no comparison result and wrote no file. The corrected inline check exited 0. No failed numeric result was discarded, and neither attempt modified an input. This report is the only new file written in this comparison scope.

The following read-only core reproduces the row comparisons and eligible later-sample intervals from this directory, without importing root's implementation:

```python
import json
from pathlib import Path

root = json.loads(Path("root-annotations.json").read_text())
separate = json.loads(Path("annotator-annotations.json").read_text())
key = lambda r: (r["frame"], r["target"])
assert list(map(key, root["rows"])) == list(map(key, separate["rows"]))
assert len(root["rows"]) == 34
for r, s in zip(root["rows"], separate["rows"]):
    if r["localization"] == s["localization"] == "localized":
        delta = [s["xy"][i] - r["xy"][i] for i in range(2)]
        overlap = [
            max(r["xy"][i] - r["halfwidth_xy"][i],
                s["xy"][i] - s["halfwidth_xy"][i])
            <= min(r["xy"][i] + r["halfwidth_xy"][i],
                   s["xy"][i] + s["halfwidth_xy"][i])
            for i in range(2)
        ]
        mutual = all(abs(delta[i]) <= min(r["halfwidth_xy"][i],
                                          s["halfwidth_xy"][i])
                     for i in range(2))
        print(key(r), delta, overlap, mutual)
    else:
        print(key(r), r["localization"], s["localization"], "no coordinate")
for name, data in [("root", root), ("separate", separate)]:
    for target in ["C2-T1", "C2-T2"]:
        rows = [r for r in data["rows"] if r["target"] == target]
        baseline = rows[0]
        for r in rows[1:]:
            if (r["localization"] == "localized"
                    and r["correspondence"] == "appearance_consistent"):
                dy = r["xy"][1] - baseline["xy"][1]
                hw = r["halfwidth_xy"][1] + baseline["halfwidth_xy"][1]
                print(name, key(r), [dy - hw, dy + hw])
            else:
                print(name, key(r), "same-feature displacement withheld")
```

The embedded core was subsequently extracted from this Markdown and executed successfully with the same explicit Python 3.13.7 interpreter: 34 pair outputs and 64 later-sample status/interval outputs. Assertions confirmed the material T1/T2 examples above. The original JSON/Markdown annotation files and frozen protocol/selection hashes remained unchanged after the check.

The full protocol's reference-map sensitivity and cross-target interval calculations are separate work; this note does not claim to reproduce those still-separate products.
