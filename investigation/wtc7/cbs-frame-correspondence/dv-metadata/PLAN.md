# DV stream metadata test

2026-10-04. Previous goal turn: progress. It completed the published timing
basis review and narrowed the next question to camera versus copy/edit clocks.
This test asks whether retained DV metadata can discriminate those alternatives.
It is one research work package, not a replacement for the full charter.

## Fixed scope

Use all eight already admitted access copies in
`../sibling-lineage/inputs.json`, with its exact hashes and acquisition choices.
The declared population is 5,567 encoded frames. No endpoint-only sampling,
new media, decoder, frame/audio output, image comparison or provider query.
Generic public technical-source retrieval is allowed for format interpretation.
Pin versioned source text; implementation sources describe format behavior,
not proof of software used to create these particular files.

Before historical execution, implement and separately review a finite parser
and synthetic controls. Reconcile RIFF boundaries, video chunk sizes/counts and
DV DIF IDs before interpreting metadata. The admitted saved probes describe
720x480 DV video; this implementation is limited to the 120,000-byte, ten-DIF-
sequence SD profile. Reject other layouts explicitly instead of guessing.
Traverse every frame in the fixed population, retaining absence and failure.

Within each frame inspect the header, both subcode blocks, three VAUX blocks,
nine AAUX pack positions per sequence and the DIF block IDs. Preserve subcode,
VAUX and AAUX separately; preserve every pack variant and its location. Skip
compressed picture/audio-sample interpretation. Whole-file integrity hashing
still reads all bytes. No probe/codec subprocess or hidden decoder is permitted.
Run-length or lossless compression is allowed for the retained metadata only;
record its serialization and verify round-trip length/hash. No generated media.

## Interpretation and controls

Identify timecode0x13, video recording date/time0x62/0x63 and audio counterparts
0x52/0x53 only at verified pack positions. Record all other pack-type counts.
Raw fields precede interpretation. Never substitute a majority value, a missing
frame component with zero, a century pivot, an assumed timezone, midnight
rollover, or an original-camera provenance claim. A valid-looking value may
belong to a camera, copy, export or edited master. Compare clock fields with
the existing AVI labels only after collection is complete.

Synthetic controls must reject truncated/shifted chunks and wrong DIF IDs;
ignore false pack signatures in picture/sample positions; preserve empty packs,
unknown types, partially available and contradictory packs. If semantic date/
time conversion is implemented, separately test invalid BCD/calendar values,
midnight, unavailable components, century ambiguity and drop-frame boundaries.
A continuous reassigned timecode over reordered synthetic clips must not be
treated as authenticated event chronology. Packet extraction alone must not be
described as validation of date/time arithmetic not yet implemented.

## Acceptance and bounded execution

Record code/input/reference hashes and actual test results before reading new
historical metadata. One fixed collection per clip, with source hashes checked
before/after, and a separate direct audit of material findings. Maximum2,500
frames per clip,10,000 RIFF chunks,12 container levels,25,000 raw timing variants,
1MiB compressed metadata and8MiB serialized JSON per clip. Only AVI/AVIX → movi
and its direct `rec ` list children are admitted movie hierarchy. Verify complete
JSON capture before creating a result artifact; a truncated tool capture is not
an admitted result. No unbounded resynchronization or signature search. A malformed layout,
exceeded limit or truncated capture remains a refused/incomplete result. Preserve
the error and define any correction before a new attempt; never silently discard
frames or switch to a favorable metadata lane.

Deliver a coverage/presence/conflict table, reproducible raw-metadata artifact,
source-pinned interpretation and concrete effect on the unresolved chronology.
If metadata cannot discriminate original versus copy timing, say so and move
to a different available physical/documentary discriminator. Do not make this
test a universal gate on qualified spatial fire observations.

Keep all outputs research-only in this existing worktree. Prior sources,
scores, annotations and user-assessed pixel ranges remain unchanged. No human
acceptance, engine activation, matrix save, legal promotion, costs, outreach,
staging, commit or push. Generic feedback remains locally queued while the
designated Sherlock destination is archived; no substitute recipient.
