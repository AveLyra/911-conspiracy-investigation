# Timecode continuity and label comparison protocol

2026-10-04. Research only. Previous turn completed the all-eight DV metadata
inventory and independent direct-byte audit. This follow-up interprets those
retained timecode candidates, not the picture or sound. Raw endpoints and AVI
labels have already been seen: this is a prospective specification for the next
calculation, not a blind study or retroactive preregistration.

## Question and fixed population

Do the timecode components and drop-frame bit describe a continuous counter
inside each of the eight access copies, and do their first values agree with
the independently collected AVI original/alternate text labels? Which rate or
counter convention changes that answer? Does any result independently establish
original-camera chronology? Answer the last question separately from arithmetic.

Use all eight version 2 result files, 5,567 frames and 5,559 within-clip adjacent
transitions. The prior audit established one distinct raw `13` pack repeated 40
times per frame, unique within each clip. Require that exact input structure and
full frame coverage when reconstructing the ordered candidate array; stop on a
schema/population mismatch instead of choosing a majority or filling missing
frames. This requirement concerns the fixed input representation, not semantic
validity: invalid digits/labels must be retained as results, not dropped.
Requiring raw-value uniqueness checks the already audited input representation,
not a general claim that real counters cannot repeat. A repeated numeric counter
with different ancillary bits still remains an observable zero-step transition.

All eight starts are compared with both `tc_O` and `tc_A` text prefixes from
the frozen sibling-header results. Preserve text syntax and binary tails there;
this unit only compares parsed components, not full payload identity. Evaluate
all 28 inter-clip pairs and seven adjacent gaps conditionally, with no assumed
24-hour rollover or bridging of unrecorded intervals. Do not identify source
gaps as historical missing frames.

For each pair, boundary distance is next-first minus previous-last. Subtracting
one gives unrepresented counter positions between those endpoints; it is not
the same as a first-to-last span or evidence of missing historical footage.
The stored difference is signed: a negative value indicates overlapping or
reset counter ranges, not a negative count of missing video frames.

## Conversion and uncertainty rules

Read the four bytes after identifier `13` in big-endian order, using the pinned
FFmpeg definitions. Digit masks by payload byte are `3f`, `7f`, `7f`, `3f` for
frames, seconds, minutes and hours. Check each BCD nibble and limits 0–29,
0–59, 0–59 and 0–23. Preserve invalid components with reasons; do not use the
display library's invalid-BCD-to-zero fallback. The DF bit is payload byte 0,
bit 6. Preserve other flag bits by exact numeric position; do not infer field
count, synchronization, recording mode, validity or authenticity from them.

Calculate nominal-30 non-drop ordinal `30*(3600*h+60*m+s)+f` and drop-frame
ordinal subtracting `2*(60*h+m-floor((60*h+m)/10))`. The drop-frame lane rejects
labels with seconds zero, minutes not divisible by ten and frames 0 or 1.
The flag-selected lane uses the pack's DF bit for this verified 525/60 profile;
forced non-drop and forced drop-frame are explicitly counterfactual sensitivity
lanes, not equally supported clock interpretations. Retain failures in all lanes.

Check every neighboring pair: report the signed ordinal difference, invalid
endpoint, DF-bit change, normal one-step progression and every non-one-step
transition. A backward jump is not silently unwrapped. A delta equal to one
minus the applicable daily modulus may be labelled a possible rollover, not
accepted as an authenticated next day. Other flag changes remain separately
listed even when the ordinal advances normally. No interpolated or repaired
values. Component equality with a header label does not authenticate that label.
On a DF-bit change, retain the raw numeric difference between flag-selected
ordinals but mark the stable-convention transition unavailable, even if that
raw difference happens to equal one.

Report the exact AVI frame period alongside nominal DV `1001/30000`; preserve
their difference. First-to-last encoded-frame span is `(N-1)*period`, separate
from `N*period` container duration. These are representation-based elapsed-time
calculations, not camera-clock measurements. Use frame ordinals for conditional
cross-clip comparisons; do not infer event-day time from counter values.

## Reproducibility and limits

Freeze this plan, reference note, implementation/tests, three new public format
sources, held DV generator/profile definitions, prior raw results/audit/freeze,
and sibling input/header results before historical conversion. Validate all
input hashes before/after. No new raw-media traversal, probe, decoder, download
of footage, image view or sound analysis is needed. Do not execute fetched code.

Use synthetic tests for endianness, every BCD component, out-of-range values,
unknown/all-ones data, DF minute/tenth-minute/hour/day boundaries, flags, repeated
and skipped counters, backward jumps, missing/conflicting input rows, strict
ASCII header parsing and denominator/count errors. Obtain separate review before
execution. Preserve failed tests/runs and any protocol correction explicitly.

The generated result contains every decoded candidate and transition plus a
summary, at most 8 MiB of JSON. The program creates only a fixed local result
file exclusively after successful source/method post-checks, with readback; no
overwrites, deletion or remote transfer. A failed command is not accepted simply
because it leaves an output. Independent arithmetic reproduction must cover all
material results, not just selected endpoints.

Strongest alternatives: a continuous original camera recording, copied camera
timecodes in an edit, regenerated continuous master timecodes, or an incorrect
association with a published still. Counter consistency alone cannot distinguish
these. Missing recording-date packs from the prior unit do not establish intent.
This unit may improve the lineage test but cannot determine fire severity or
collapse cause. Broader charter work must not be held behind this clock check.
Human review, coordinate tolerance, source protection, archived-feedback routing,
no legal/main promotion and no commit/push boundaries remain unchanged.
