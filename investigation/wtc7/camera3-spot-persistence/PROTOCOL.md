# Camera3 spot persistence protocol

2026-10-04. Version1, declared before new extraction or image viewing.
Research only under the full main CHARTER and current repository controls.
The previous goal turn made **progress**: charter-wide reconciliation and
same-packet competing arguments were completed and critically reviewed.
That result did not complete the full investigation or identify a cause.

## Question and fixed sample

Does the small light-looking feature previously noted near the upper-left
banding of Camera3's target face persist in the adjacent encoded images,
remain tied to a façade/background pattern, appear in a limited subset, or
remain unresolved? This is qualitative source observation, not calibrated
photometry, an automated event detector, motion measurement or charge test.

The selection is fixed at **zero-based decoded WMV indices255–261 inclusive**.
The historical observer's frame258 note is the prior target description; no
new images have been inspected in this unit at declaration. Root and other
agents are prior-informed, not blind. Earlier exposure across sessions cannot
be excluded. No unused event-level holdout is claimed.

Only the held 442-frame WMV is eligible, not the older 232-frame MP4. The
default map gives encoded PTS17000,17066,17133,17200,17266,17333,17400 with
time base1/1000, spanning17.000–17.400 encoded seconds. This is not an
authenticated camera exposure clock or a measured physical event duration.

## Sources and allowed derivatives

Source under the main investigation directory:
`camera3-provenance/kit-inventory/run-v1/outer/The Kit/WTC7-Camera 3/videos/Camera3.wmv`
has expected SHA256
`48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722`.
The held `camera3-recording-comparison/wmv-diagnostic/run02/default-frames.json`
has expected hash
`8afdf759ecc45215b9212699ef2adb72de553c52667d82b39c9382df8e6b36c2`.
Its442 per-frame gray hashes and raw-stream hash are comparison targets,
not independently authenticated historical truth.

Reuse the exact pinned `camera3-late-reannotation/prepare.py` decode recipe,
without executing its larger selection or changing it. A small adapter may
save only seven unmarked720×480 8-bit grayscale PNGs and their index/clock/
pixel/byte mapping. No scaling, crop, ruler, overlay, contrast change, color
inference, deinterlacing, synthesis, interpolation, stabilization or adaptive
selection. No additional images or playback are authorized by this protocol.

The earlier raw stream was not retained as a complete file in the located
products. One exact-recipe decode is therefore allowed after method/source
checks; verify all442 output-frame hashes and the raw-stream hash against the
held map before admitting the seven PNGs. Preserve return status and warnings
in local logs, not selectively discarded output. Reopen every saved PNG and
verify its grayscale bytes against the selected hash. Frame258 must also
match the existing frame258 decoded PNG bytes; PNG compression differences
alone are not pixel differences. No fresh repeated full decode is required
merely to obtain another success.

Retain diagnostic-only status. Earlier warning indices37,55,63 and three
corruption mentions are not at the selected indices, but absence of a local
warning does not establish absence of propagated artifacts. Neither a hash
match nor two observers authenticates original recording/exposure or emission.

## Preflight and finite repair boundary

Before viewing: independent source/clock/version preflight; root review of the
adapter and nearby implementation; synthetic selection/PNG round-trip and
failure tests; separate method review; protocol/code hashes saved before the
historical decode. The adapter refuses an existing output directory and
invalid frame selections, requires source/map/binary identity and exact raw
length/count/hashes, and rechecks input identities afterward. No package
installation, runtime upgrade or fallback decoder is part of this unit.
Use the existing `/Users/admin/.pyenv/shims/python3` route, verified as
Python3.13.7 with Pillow12.0.0, not bare `python3` currently lacking Pillow.
Record the actual resolved interpreter/version in the extraction receipt.

A mismatched source, map, binary, raw stream or selected pixel closes the
historical execution without viewing. Preserve its failure; do not relax the
criterion. At most one narrowly diagnosed adapter repair may be made before
viewing under a separately logged version, after a new method review. An
environment-permission failure may be retried only after resolving that exact
boundary, not by changing scientific criteria. Two actual image-display
retries total across both readers are allowed only for failed displays, never
for a different look. Notify root before using either shared retry.

## Separate observation records

Two readers view full images at original detail, in the fixed order
**258,255,256,257,259,260,261**. The anchor comes first to localize the already
reported spot before examining its neighborhood. Each reader saves its
per-frame record before opening the next image and does not read the other's
new record until both are complete and hashed. Both may read the original
frame258 note and the same source/method preflight.

For258, describe the candidate by façade band, neighboring patterns and shape.
If the old verbal location fits multiple distinct spots, name every plausible
candidate within that region and retain ambiguity; do not choose the one with
the most interesting temporal behavior. Freeze candidate IDs/descriptions
at258 and carry every candidate through all seven frames. If candidates differ,
the old target's identity remains unresolved; if all persist, report only that
shared outcome without selecting one retrospectively. No numerical position/intensity/area
measurement is performed. For every frame record:

- Successful/failed display and exact file identity.
- Whether the candidate's region is inspectable, masked or unresolved.
- Candidate appearance and relation to the local façade/sky/foreground pattern.
- Presence as **visible**, **not resolved despite inspectable region**, or
  **region uninspectable**; lack of resolution is not physical absence.
- Target-identity ambiguity, plausible ordinary/processing alternatives, and
  any limit preventing cross-frame comparison.

After all seven first-view records, each reader gives one summary without
reopening images: **persistent appearance** if a single comparable candidate
is visible throughout; **limited resolved appearance** if it is resolved only
in a subset while other regions remain inspectable; or **unresolved comparison**
if identity, visibility or representation does not support that distinction.
State which frames support the judgment and whether relation to the local
pattern can be described. Preserve disagreements; no majority-vote truth.

Persistence weakens a reading of this spot as an isolated one-frame event in
this derivative; it does not exclude variable illumination of a persistent
surface or an event outside this0.4-second window. A limited appearance retains
a better-source lead, not proof of transience in the original recording.
Neither outcome identifies reflection, window, emission, a charge or an
initiating mechanism. No complete-video nondetection follows.

## Deliverables and stopping rule

Save source/method checks, implementation/control and extraction receipts,
two frozen observation records, independent selected-pixel verification,
comparison/claim ceiling, critical review and actual execution log here.
Check invariants, cited paths and unchanged sources. Root updates research
navigation only after outcomes and critique, using the existing local format.
Source preservation, development verification and evidence-audit skills guide
the bounded checks; none grants extra authority or expert acceptance.

Stop after the seven-frame/two-reader comparison and its technical/scientific
review, even if unresolved. No automatic neighborhood expansion or new
quantitative event/detection analysis. Human142-N12, calibration-curve human
checks, user coordinate locks, pending matrix save, expert and privacy gates
are unchanged. No acquisition, outreach, costs, engine/bridge use, transmission,
canonical/legal promotion, staging, commit or push. The whole goal stays
active until its independent charter-wide completion conditions are met.
