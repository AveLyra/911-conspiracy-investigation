# CBS Clips 5 and 6 scene identification results

2026-10-04 UTC, October 3 locally. Working research; stage 3 of the fixed
eight-candidate screen. **Neither clip meets the declared scene/view association
threshold. Clip 6 supplies a partial local lead for Figure 5-143, not a verified
match.** These results narrow the source-follow-up while leaving the earlier
Clip 3 association intact. They do not measure fire severity or rank collapse
mechanisms.

## What the sampled images establish

Both readers inspected the same nine fixed samples per clip and saved their
complete observations separately before exchanging new judgments. Their
reference descriptions and the two-distinctive-relationship threshold stayed
unchanged. The complete records retain every sampled image, including poor
and contrary views: [root Clip 5](root-clip5.md), [root Clip 6](root-clip6.md),
[second reader Clip 5](reader-clip5.md) and
[second reader Clip 6](reader-clip6.md).

| Clip and reference | Result within the fixed sample | Decisive evidence and limit |
| --- | --- | --- |
| 5 to 5-141 | No supported association; contrary view cue | The upward samples expose a broad pale face left of a corner and a dark/veiled region right of it, unlike the frozen reference's opposite ordering. Paired dark bands alone do not establish a match. Lower context is hidden by the banner. |
| 5 to 5-142 | No supported association | Street samples have a curved traffic fixture, but not the distinctive direction/street/one-way sign assembly in its specified relation to the corner and upper-right overhang. |
| 5 to 5-143 | Unresolved local identity | The particular upper irregular group and fine pale-edge/boundary relationships to the lower grid are not jointly resolved. Broad facade resemblance is insufficient. |
| 6 to 5-141 | Partial architectural compatibility; unresolved association | Pale face/right and veiled region/left are compatible, but the paired upper bands, separating pale rows, lower interrupted band and neighboring-building context are not jointly recovered. |
| 6 to 5-142 | Compatible lower facade; unresolved wider view | Lower rectangles and louvers are compatible. The distinguishing foreground sign assembly and opposed overhang relation are not established. |
| 6 to 5-143 | Partial positive local lead; unresolved association | Index 172 shows a near-corner irregular upper group above a pale interval and lower grid. The distinguishing fine relationship remains unresolved. Indices 123 and 147 crop upper context; 196 is severely impaired. |

The readers agree on these dispositions, but not through identical small-feature
judgments. For Clip 6, root could not confidently resolve its frozen pale-edge
and descending-trace relationship. The second reader could not securely resolve
its frozen near-corner pale patch and irregular-boundary arrangement. It did
not require or independently confirm root's trace. Neither borrowed fine detail
from the earlier Clip 3 result. Agreement on an unresolved result does not
authenticate the underlying scene.

Clip 5's contrary ordering weighs against the specific reference view, **not
against every possible view of the same building**. Another face, camera
position, crop or unestablished source processing remains possible. No mirror
or other transform was assumed to force correspondence. Likewise, omitted
signs or upper features in Clip 6 do not prove their absence outside the frame.
Repetitive facade geometry is a surviving alternative to a genuine local match.

The last Clip 6 sample displayed successfully but contains severe horizontal
banding and mixed-looking street/person/vehicle/facade content. Its origin is
not diagnosed. Clean decoder diagnostics and repeatable pixels do not make its
fine geometry usable. All such impairment remains in the observation record.

## Coverage and source identity

These are the exact `Vince Demetri Clip 5.avi` and `Vince Demetri Clip 6.avi`
items from the fixed catalogue, not the separately named Dimentri WMV. The
[fresh metadata](metadata-refresh.json), [acquisition record](acquisition.json)
and [selected inputs](input.json) preserve the provider IDs, requests, literal
names and obtained-byte identities. Requested checksum fields were omitted
from normalized metadata; omission does not establish provider absence.
Provider visibility remains `access_not_verified`. Local integrity is not
historical camera custody.

| Selected access copy | Bytes and SHA-256 | Full inventory | Inspected indices | Not inspected |
| --- | --- | ---: | --- | ---: |
| Clip 5 attempt 1 | 65,881,740; `8a7c04527e7807ec141c9da2af65d7a654493c462ecdff238764d3760196727f` | 529 | 0, 66, 132, 198, 264, 330, 396, 462, 528 | 520 |
| Clip 6 attempt 2 | 24,615,508; `c68e8b3b3c82bc980addbfc00c767ba486e8e54826e48427f0d57f5fdac9d074` | 197 | 0, 25, 49, 74, 98, 123, 147, 172, 196 | 188 |

Each reader viewed **18 distinct samples from 726 inventory frames; 708 frames
remain unviewed**. This is sampled non-recovery, not whole-clip absence or
continuous shot analysis. Samples came from the frozen first-at-or-after rule
at nine exact rational targets, not a search for the most persuasive images.
The [selection table](preparation01/selection-targets.json) predates extraction.
There were no extra frames, crops, enhancements, audio checks or repeat views.

Both sources retain native 720 by 480 pixels, sample aspect ratio 8:9 and
bottom-field-first interlacing. Their encoded time base is
`333673/10000000` seconds per PTS unit; PTS equals source index in these
inventories. This is not an authenticated historical clock. No aspect or field
transformation was applied, and metric shapes or apparent motion were not used
to decide associations. The report reference JPEGs are processed derivatives,
not camera originals or unused holdouts.

## Verification and retained operational exception

Fresh synthetic controls reported 14 parent-helper and 25 adapter tests passing.
Preparation and two native extractions passed unchanged diagnostic gates.
The [independent artifact audit](artifact-review.md), rerun by root, reconciled
all three received attempt files, the two selected complete inputs, 18 exact
targets, 726 preparation frame records, both repeated inventories, 36 PNG/RGB
identities, 18 repeat pairs and the recorded commands/diagnostics. Repeating the
same toolchain checks determinism, not independent decoding or source truth.
Actual invocations, outcomes and freeze hashes are in the
[execution record](execution.md) and [command record](commands.json).

**The transfer-time cap was not met on Clip 6 attempt 1.** Although requested
with `--max-time 55`, it reported 71.150559 seconds, exit 28 and only 2,686,193
of 24,615,508 expected bytes. The failed partial and its diagnostic are preserved
and excluded from analysis. The single permitted retry began after confirmed
terminal failure and completed successfully. The overrun cause remains unknown;
this is not an unqualified protocol-compliance pass. No timeout was enlarged,
partial admitted or third attempt made. Selected-source integrity and timing
noncompliance are separate findings.

The separate visual reader is the same replacement reader as stage 2, using
the original observer's frozen textual reference descriptions under the
[recorded setup](../stage2/reader-setup.md). It did not independently reopen
reference pixels. Both readers had prior source/outcome knowledge, so this is
separately frozen computational review, not blinding, a new camera, qualified
expert review or actual-human acceptance. No original annotation was rewritten.

## Claim strength and what would change the result

| Claim | Evidence type and strength | Strongest limitation or next discriminator |
| --- | --- | --- |
| The selected copies and 18 repeated samples reconcile with their recorded identities and selection. | Derived, A within the audited local artifact scope. | Edited or mislabeled upstream footage can remain perfectly repeatable. Original custody and edit records are not established. |
| Clip 5 does not recover the specified reference views in this sample. | Observed/inferred, C because the sample is sparse and views are partly obscured. | A different view or an unsampled exposure of the same building may contain the target. Contrary ordering applies only to the exposed composition. |
| Clip 6 index 172 is a useful partial 5-143 lead, not a supported full match. | Inferred, D for the stronger identity claim. | A declared source/frame test resolving the fine landmark relationships could establish a match; incompatible exposed geometry could disconfirm it. |

No result establishes exact exposure identity, a common original recording,
physical glazing state, floor assignment, fire area/temperature/duration,
acceleration, support loss, intent or a collapse mechanism. The strongest
scientific limitation is still the missing source-and-detail bridge, not an
arithmetic failure that can be repaired by repeating the same extraction.

## Next required work

Complete Clips 7–8 under the unchanged [protocol](../PROTOCOL.md). Do not stop
the eight-item screen because Clip 3 matched or promote Clip 6's partial lead
to rescue an unresolved comparison. After all eight, declare the bounded
exact-frame/field/source-transform follow-up for the strongest supported leads;
source association alone cannot accept a glazing or fire-input claim.

The [separate synthesis critique](synthesis-review.md) found no material
scientific correction required. This bounded stage is complete, retaining
its explicit transfer-time deviation rather than claiming full compliance.
The full charter remains active and incomplete. Other human checks and
matrix-save permission remain separate.
The timeout lesson is deduplicated locally under SFB-005; archived-destination
routing remains unresolved. No accepted Sherlock/Faraday finding, external
disclosure, legal promotion, staging, commit or push is claimed.
