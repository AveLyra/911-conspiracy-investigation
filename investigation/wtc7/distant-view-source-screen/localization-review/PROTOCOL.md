# DistantView human localization pilot

October 8, 2026. Research only. The previous complete interval screen supports
an identifiable outer image-right silhouette junction in decoded ordinals
274–411. It does not yet supply reliable coordinates, a fixed material point
or a physical motion measurement. This protocol freezes a six-frame human
localization-feasibility pilot and its display checks before implementation.

## Scope and selected inputs

Use the unchanged complete native grayscale frames274,300,342,365,388,411
from `../continuity-274-411/run01/native/`. The earlier endpoints and midpoint
cover broad appearance changes;365 and388 distribute the later coverage;300
includes the peer-noted tonal-softness concern. This is a purposive sample
informed by prior viewing, not a random sample or unused holdout. It does not
test the299→300 transition and must not substitute for all138-frame coverage.
All selected images are704×480, with no new crop, rescaling, filtering,
enhancement, interpolation, annotation overlay or re-decoding of source files.
Display zoom may enlarge source pixels without modifying the image asset.

Pin the source AVI, the prior frame/mapping records, both frozen first-pass
observations and the final verification receipt. The latter is
`4d98bc4c4f26a0b889466071419a8f3edeb090c1798e1ccae0db325cf5e34325`.
Retain native ordinals and separate nullable stored/best-effort timestamps.
No time value may be inferred, substituted or adopted as a capture clock.

Reuse the existing R1 synthetic control PNG without alteration
(SHA256 `f0a96bf21d7ec0d2b8b486050d111b803dd708645fb1b3ad1659c3eda2edaf48`,
1280×720 RGB). It remains labeled synthetic and cannot become a historical
observation. It is a coordinate-mapping UI fixture, not a calibrated model
of this footage's blur or an accuracy benchmark for human feature localization.

## Human question and response contract

The target is the junction of the dark target facade's outer image-right
top outline and right side outline. It is not the raised roof-step foot,
bright compression rim, plume edge, foreground roof or adjacent background
building. Image-right assigns no compass direction or structural member.

For each of the six full frames, request actual inspection confirmation,
one status, an optional plausible-position box as specified below, and a
short explanatory note. Initially every item is **not inspected** and has
no coordinates. Display no AI-suggested positions, default intervals or prior
reader boxes. Do not calculate a suggested center.

- Localizable: give an inclusive native-pixel rectangle covering the junction
  placements the reader considers plausible from the adjoining contours.
- Ambiguous: competing junctions or insufficiently resolved identity. A box
  is optional; when no single useful region can be given, leave it null and
  describe the competing alternatives. Never use its center as an estimate.
- Obscured: the target cannot be localized because it is hidden; null box.
- Not located: the reader cannot find the target, without claiming physical
  absence; null box.
- Outside or display inadequate: localization cannot be assessed in this
  display; null box and the specific problem.

All non-localizable states require a reason. A one-cell rectangle may be
reported if that is the reader's actual judgment, but software must not supply
it automatically or call it a confidence interval. A box is a subjective set
of plausible pixel cells, not a statistical distribution, guaranteed error
bound or proof of a fixed material point. Uncertainty about identity is not
resolved by drawing a very large box around unrelated alternatives.

Coordinates are zero-based native pixel-cell indices: x0–703 and y0–479,
origin upper-left, increasing right/down. Rectangles use inclusive endpoints
`xmin,ymin,xmax,ymax`; bounds must be in the image and ordered. A reversed
pair is rejected rather than silently swapped. Mouse hits use floor within
the image rectangle, whose right/bottom edges are excluded. Markers center
on the chosen pixel cell. The interface must distinguish hover, locked point,
pending box and a recorded session-only draft row. Selecting a frame clears
transient point/box state; separately recorded draft rows remain only in memory.

The viewer neither saves nor accepts evidence. The user can manually copy
its displayed response text into this chat; only an actual user response
can become a preserved human observation. Future corrections must be saved
separately, not overwrite the first response. No click, test injection or
agent-written fixture may be represented as human review.

## Existing components and minimal implementation

Create only a small packet adapter in this directory. Do not change the R1
viewer, graph viewer, earlier observations or accepted records. Reuse the
exact pure prefix of the pinned R1 `coordinate.js`, bytes[0,2524), SHA256
`9cff4290fc41e27126b36402818b1ecb55057e003f819ecbe8cef53281d2e2c4`,
as a generated derivative module. Its full source SHA256 is
`38cc0cd9b0947e05072ec8656c58e4fc4ca95d968bd1a903af26afe43db0b05b`.
Verify exact byte equality, not a fresh reimplementation of the mapping math.
Do not import the original full browser module, which starts its old UI.

Reuse the unchanged R1 server's `handler_for` and path/Host/Origin refusal
contract through a pinned import; source SHA256
`1ea233c4fa8074298f9791a305fa46f0b1ac3151ce00ce48c8edd7e99de48142`.
Serve only seven explicitly pinned image assets plus this packet's declared
UI/code assets on127.0.0.1. No directory listing, arbitrary file path, network
asset, write/upload endpoint, analytics, storage, clipboard API or export.
Grayscale historical images must remain grayscale; do not convert them to
RGB to satisfy an inherited check. Do not expose raw case/pleading files.

A local session is not a permanent hosted link or protection against every
same-machine process. Report the actual server handle and URL if started.
Do not restart a process merely because a status observation timed out.

## Verification and acceptance

Before human use, verify exact asset hashes and dimensions/modes, unchanged
historical pixels, nullable metadata, exact helper extraction, route allowlist
and source preservation. Generate the packet twice in fresh output directories
and compare deterministic assets/manifests. Preserve any failed output.

Run the existing shared component controls and focused new synthetic tests:
mapping at704×480 and1280×720; fit/100%/200%; fractional offsets, scroll and
negative origins; image borders/padding; first/last pixel and excluded edges;
pixel-center round trips; keyboard nudges; inclusive/reversed/out-of-bounds
boxes; missing or forged inspection confirmation; absent/partial box;
non-localizable status handling; no default acceptance; frame/loading/error
resets; and no fabricated answer for an uninspected row. Check routes and
refusals with synthetic content, including changed/missing asset rejection.

Use the native browser for UI QA on the synthetic control only: real pointer
selection, lock/clear, one-pixel keyboard moves, zoom/scroll/resize, box/status
recording, and readable response text. Record actual device-pixel ratio and
viewport; do not claim untested physical-display configurations. Historical
image loads may be checked through DOM dimensions/metadata but receive no
agent clicks, boxes or screenshots as part of this UI test. The prior visual
coverage remains separate. Browser interactions use only documented tools.

These controls establish coordinate bookkeeping and safe packet behavior,
not localization accuracy. No automated historical locator or track runs in
this unit. Before a future consequential automated localization method is
admitted, test that actual method against independently specified synthetic
junctions with subpixel phase, blur, compression, contrast/polarity changes,
competing edges, partial occlusion and unidentifiable examples; freeze error
and abstention rules before evaluation. Simple visible control shapes cannot
stand in for that challenge. The current human packet must not activate it.

This turn's deliverable is a tested, reproducible packet and clear human
question. The human pilot itself remains incomplete until all six actual
responses or explicit user-reported unavailability are preserved. Six positive
responses do not estimate an error rate, certify the remaining132 frames or
replace timing, camera/scale, feature/body-geometry or expert prerequisites.

Stop after packet verification and presenting the question. No historical
coordinate estimates by agents, acceleration, time shifts, physical calibration,
model fit, cause ranking, legal promotion, source expansion, outreach, fees,
accepted Sherlock/Faraday state, commit, push or external disclosure. Keep the
full charter goal active. Existing actual R1 human review is complete and is
not reopened; other human/peer and held-matrix boundaries remain independent.
