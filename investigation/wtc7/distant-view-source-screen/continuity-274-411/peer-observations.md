# Peer first pass: finite outer-corner continuity screen

Frozen first pass by `/root/envelope_arithmetic`, October 8, 2026. This is a same-source AI observation record, not human acceptance, expert review, independent camera evidence, historical authentication, or physical-model admission.

The complete expanded record is [peer-observations.json](peer-observations.json), 99,995 bytes, SHA256 `542bdc67e45335355a007a93ee56225b4410a5100b3efe8a94698083228ef32b`. The JSON contains all 138 separate frame records and all 137 separate adjacent-link records with reasons, plus the explicit observed ranges from which those full rosters were expanded. It is the detailed first-pass record; this note does not replace its roster.

## Scope and prior knowledge

The frozen [protocol](PROTOCOL.md), SHA256 `230777a8aff939d2fcc76386fcdc18e26449305c8ba1da34874cdf387af9b970`, fixes decoded ordinals 274–411 inclusive and the building silhouette's outer **image-right** top/side junction. That is not a compass label, identified member, raised roof-step foot, smoke boundary, foreground roof, or background-building corner.

I previously inspected the parent unit's eight native frames (0000, 0137, 0274, 0411, 0549, 0686, 0823, 0961) and the two fixed Camera2 contexts, then froze [my earlier note](../peer-observations.md), SHA256 `4ea522072ae6e566fc0499061972005f72f4b02437dc6ecd46bdd8c1c03a089f`. After that earlier freeze I read the parent's first-pass note/report. I therefore knew the endpoints were positive corner candidates, knew the lower-step and source-independence limits, and knew this interval and crop had been selected from prior endpoint knowledge. This new pass was not blind to those facts.

Before this peer freeze, root sent completion and SHA256 `e3b979379c16ccda89c191f9a20a323d3b202bb8caed22be91bda4bf6637a40b` for its new JSON, but no substantive new findings. I did not open root's new observation files or receive their classifications before saving this pass.

The evidence-falsification-auditor and source-of-truth-guardian skills were applied to keep image observation separate from material identity, retain disconfirming alternatives, pin the exact displayed derivatives, and avoid promotion of this working record into accepted scientific evidence.

## Actual viewing coverage

I used `view_image(detail="original")` and forwarded each result with `detail="original"`. First I viewed the three complete 704×480 native contexts: 274, 342, and 411. Next I viewed all twelve complete 1180×984 source-order contact pages in six successive two-page batches. All crop cells remained at their prescribed native 280×290 construction scale. No image was cropped again, resized, filtered, photometrically changed, annotated with coordinates, or substituted.

All 138 nonblank cells were examined, with each frame judgment made explicitly. Separately, all 137 adjacent pairs were examined: 126 within-page links and the eleven page-boundary links 285→286, 297→298, 309→310, 321→322, 333→334, 345→346, 357→358, 369→370, 381→382, 393→394, and 405→406. The six last-page blank cells were not assigned frame identities.

The exact labeled image-output references and viewing order are in JSON `actual_views`. These reference actual preserved tool outputs; no separate image-tool receipt identifier was exposed. Whole-page labels and cells were legible enough for this descriptive corner screen. That sufficiency does not imply pixel-level precision or structural-detail resolution.

No additional full frames, individual crop files, alternate display, new decode, timing recovery, image algorithm, or automatic rescue was used. Source metadata retains its original `index` fields and nullable timestamps; the observer rosters use the separately agreed `ordinal` / `from` / `to` fields.

## First-pass result and reasons

My finite descriptive classification is 138 V frames, zero A/O/X frames; 137 supported links, zero uncertain/broken links. The single supported inclusive run is 274–411. This is the result of examining the adjoining contour/context relationship in each pair, not an automatic conversion from V to supported.

The dark facade's top run and right side remain separately visible and meet in the named corner throughout this packet. The raised roof detail farther left changes appearance and becomes low/indistinct; plume increasingly obscures the left roof area. Neither was substituted for the outer corner. In the later cells, a lighter stepped background form becomes exposed beside/above the dark corner, but its outline remains distinguishable from the target's joined top and side.

Frame 300 has a conspicuous tonal/texture softening relative to 299. I retained the 299→300 correspondence because the step-to-corner outline, long right side, and neighboring scene arrangement still match. That judgment is not proof of no edit, no duplication, unchanged exposure, or unmodified original recording.

The three prescribed full contexts support the interpretation of the selected outline as the building's outer image-side junction. They do not establish the same physical material particle or structural member across frames. The result says only that this peer found an uninterrupted **observational candidate** within the declared finite interval. It is not a combined-reader result and does not select a favorable subset beyond the frozen interval.

## Strongest limitations and disconfirming alternatives

A visibly corresponding silhouette can change its material boundary while retaining a similar corner. That is the strongest limitation: these views do not prove rigidity, a fixed material point, center of mass, attachment geometry, or three-dimensional continuity. Raster softness and compression also limit the ability to exclude small unresolved competing edges or replacements.

Visible background persistence is not calibrated camera stability. Source-order adjacency is not a recovered clock or proof of equal exposure intervals. No coordinates, trajectory, onset, velocity, acceleration, cause, cross-camera timing, or hypothesis ranking were measured or inferred.

The observations do not resolve the lower raised-step foot, compass orientation, independence from Camera2, provenance beyond preserved bytes, or whether a future physical measurement would be admissible. Same-evidence AI readers are not independent captures or human/expert adjudicators. A different qualified reader finding a competing/obscured junction or unsupported adjacent correspondence would limit or break the combined criterion; that disagreement must be preserved, not voted away or bridged.

## Actual integrity and roster checks

The before-view check was a read-only invocation of `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -` in the research worktree (exec receipt `962a4a`, exit 0). It SHA256-checked [pre-view-verification.json](pre-view-verification.json) against `e9d751b20d749186117796316f5f481ddb700bab0051b81ffa559724d7a0e96a`, then reread and matched all 658 declared input size/hash pins, including the fifteen displayed PNGs. This did not rerun the independent pixel checker or decode the video.

The corresponding after-view invocation (receipt `b8355b`, exit 0) again matched all 658 pins and confirmed both peer output paths were absent before the first save. The source AVI remained 4,749,520 bytes with SHA256 `a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e`.

After the JSON save, the roster-only invocation below ran with the same Python `-B` interpreter (receipt `79a822`, exit 0). Only `require`, `expand_ranges`, and `validate_roster` were extracted from SHA-pinned producer code using Python AST; no module import, media run, or source decoding occurred.

```python
from pathlib import Path
import ast, json, hashlib, collections
u = Path("research/sherlock-wtc7-investigation/distant-view-source-screen/continuity-274-411")
producer = (u / "derive.py").read_bytes()
assert hashlib.sha256(producer).hexdigest() == "f261b0f516c90b3ae274b8d3d49e7453e7a2c80eb323f9cdcf3ca176067ae68a"
module = ast.parse(producer)
keep = {"require", "expand_ranges", "validate_roster"}
selected = [n for n in module.body if isinstance(n, ast.FunctionDef) and n.name in keep]
assert {n.name for n in selected} == keep
ns = {"FIRST": 274, "LAST": 411}
exec(compile(ast.Module(body=selected, type_ignores=[]), "derive.py:roster-only", "exec"), ns)
p = u / "peer-observations.json"
raw = p.read_bytes()
d = json.loads(raw)
assert ns["expand_ranges"](d["observed_frame_ranges"], "frames") == d["frames"]
assert ns["expand_ranges"](d["observed_link_ranges"], "links") == d["links"]
result = ns["validate_roster"](d["frames"], d["links"])
assert len(d["actual_views"]) == 15
for item in [d["protocol"]] + d["input_pins"] + d["actual_views"]:
    q = (u / item["path"]).resolve()
    b = q.read_bytes()
    assert len(b) == item["bytes"] and hashlib.sha256(b).hexdigest() == item["sha256"], str(q)
assert dict(collections.Counter(x["status"] for x in d["frames"])) == {"V": 138}
assert dict(collections.Counter(x["status"] for x in d["links"])) == {"supported": 137}
assert result["supported_runs_inclusive"] == d["summary"]["supported_runs_inclusive"]
assert d["counterpart_new_annotations_read_before_freeze"] is False
```

Result: the explicit range expansions exactly equal both complete saved rosters; 138 frames and 137 links satisfy the helper's structural checks; all fifteen displayed-image pins and all seven direct protocol/input pins match. The helper reports `semantic_or_human_acceptance_implied: false`. It checks roster structure, not truth of the visual judgments, actual viewing, or the semantics of reasons. No source authentication, new scientific acceptance, or broader next-step authority follows.

Both peer files were created with `apply_patch`; no existing source, image, protocol, or other observer record was edited. This first pass is frozen before any cross-reading of the new root findings.
