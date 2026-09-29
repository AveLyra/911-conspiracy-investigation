# Exact saved-point / native-frame audit

2026-09-24. Previous goal turn: progress; completed lower-junction sampled
visibility review, not physical kinematics. Main charter and current main
controls remain authoritative. Main, raw evidence and accepted engines are
read-only; this isolated research worktree holds derived working products.

## Question, inputs and hypothesis

What do the exact saved PM05/PM08 image-space positions land on in their own
video frames? This is explicitly **source-guided reconstruction**, not independent
point selection, a new trajectory, a recovered publication version, or a
test that assumes the old lower-step definition remained visible.

Use only the held `tilted-camera-source-join` inputs:

- `project01.json`, SHA256
  `4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8`;
- `source/TiltedCameraWTC7Clip.mp4`, SHA256
  `393d76f986d0771c5ec38352bf29470a81a3c685bb8a1c7ea565ceefa334843f`;
- existing complete probe,476-frame hash record, source/export receipts and
  held primary-code semantics review. Preserve literal row indices and values.

H0: the saved image-space x/y refer directly to the current native720x480
video raster with x right and y down. This is conditional. Historical engine
aspect/display handling is not established; current sample aspect131:144 and
absence of saved filters must remain explicit. Do not rotate with the saved
world-axis angle, change scale, apply sample-aspect correction, move a point,
or fit any transform to improve agreement. A source-grounded alternative needs
a separate declaration before evaluation, not a favorable post-hoc adjustment.

## Exact full selection

Include every saved row for `pointmass05` and `pointmass08` from the pinned
export: PM05 indices150,156,…,402 (43rows;35nonkeys then8keys at360,…,402),
PM08 indices210,216,…,444 (40rows, all keys). The union is50distinct indices
150,156,…,444. Retain83rows, including every nonkey, missing counterpart and
out-of-bounds/ambiguous case. Do not infer that keys were manually marked or
that earlier nonkeys are confirmed interpolations.

Decode from start at native geometry, without autorotation, autoscale, timestamp
normalization, interpolation or invented frames. Reuse inspected existing
decode/parse contracts rather than a new general framework. Compare all476
decoded frame/luma hashes and PTS against existing records; save only the50
selected native-Y PNGs in a fresh create-only directory. Retain diagnostics,
failed attempts, source/procedure/runtime hashes and exact rational encoded
PTS. These PTS are not authenticated exposure times or the assigned analysis
clock. An error/warning or changed source stops admission pending review.

## Reading presentation and synthetic gates

Each of50reading panels must contain one complete unmarked native720x480
image, plus a separate pair of local reading crops for each present saved
point: unmarked then marked. Never overwrite a source PNG. Marking derives
only from the saved coordinate, not a newly picked landmark.

For each finite point, r=floor(x+0.5), s=floor(y+0.5). Crop the half-open60x60
source rectangle[r-30,s-30,r+30,s+30), enlarged3x nearest-neighbor. A marked
copy uses an exterior/gapped crosshair centered on display cell(91,91), the
center of the replicated(r,s)pixel; preserve an unmarked copy alongside it.
This nearest-pixel rendering is not subpixel localization. Record the exact
saved x/y, rounded indices, rounding difference and source rectangle. Outside-
source padding must be explicitly indicated/masked, never treated as evidence;
an out-of-frame point remains flagged, not clipped into a preferred location.
Keep all labels outside the unmarked source/crop pixel regions. Distinguish
PM05/PM08, key flags, frame index, exact PTS and H0 conditional status in labels.

Before historical presentation, use known synthetic coordinate-pattern images
and declared point fixtures to test integer/fractional/tie rounding, origin and
axis signs, source-crop inverse mapping, near-edge padding, out-of-frame and
nonfinite input behavior, missing-track rows, wrong pins/indexes and overwrite
refusal. Independently verify every native/unmarked crop pixel and marker
location, not just successful image generation. Retain earlier tested scripts
unchanged; any adapter has its own version/hash and controls. Run two fresh
deterministic extraction/presentation sets and compare substantive products;
path-bearing receipts may differ explicitly. No historical viewing before
applicable representation checks pass.

## Separate descriptive review

Root and a separate prior-informed AI reader inspect all50complete panels,
including every full native scene and83unmarked/marked crop pairs, in ascending
frame order. Save83row observations before exchanging findings. Existing
source labels, coordinates and earlier footage are familiar; no blind or
holdout claim is allowed. Record all actual viewed products and skipped/failed
views, with hashes. No new point coordinate or historical motion fit is made.

For each PM/frame row classify the location neighborhood under H0:

- host: `building`, `smoke_or_background`, `foreground`, or `mixed_or_unresolved`;
- feature: `corner_or_junction`, `roof_edge_only`, `facade_texture`,
  `none_resolved`, or `uncertain`;
- relation to the predefined lower step foot: `candidate`, `different_feature`,
  or `unresolved`.

These distinguish source-guided visual agreement from historical material
identity. A straight roof-edge construction may be legitimate without being
a persistent corner. Preserve competing interpretations, occlusion and border
cases in per-row reasons; do not force a positive/negative causal label. A
point near an edge is not a calibrated residual test; no pixel-distance cutoff
is invented after inspection. Compare all83categorical pairs without voting,
recoding into consensus, or turning agreement into accuracy. Human/qualified
review and physical calibration remain separate unmet gates.

## Ownership, acceptance and boundaries

Root owns protocol, source-guided observations, synthesis and navigation.
Preparation agent owns `prepare.py`, `test_prepare.py` and fresh generated
control/run directories only. Method reviewer owns `method-review.md`; an
independent verification file may be assigned explicitly. Separate observer
owns `observer.md` only. No concurrent changes to another owner's source.

Acceptance: exact50frame/83row coverage, successful bounded representation
controls/repeats/independent checks, separately frozen full observations,
preserved disagreements and a result identifying what H0 does and does not
explain about the saved points. Failure of H0 is not fabrication or refutation
of a collapse cause; compatibility is not proof of the historical pipeline,
physical scale or a specific mechanism. Full investigation remains open.
No external retrieval/provider transfer, private-packet access, outreach,
fees, legal drafting, promotion, engine acceptance, commit or push. Generic
software feedback stays local under the existing archived-destination rule.
