# DistantView native video coverage

October 8, 2026. Research-only source triage, not a new motion measurement or
cause finding. The full investigation remains incomplete. This unit examines
one previously held but natively unreviewed video; it does not repeat the
completed saved-coordinate inventory.

## Result

The fixed eight-frame screen supplies a concrete follow-up candidate: the
outer image-right roof corner is visible in standing scenes and again at a
lower position relative to nearby structures in frame411. This can justify
a separately declared continuity and event-correspondence test. It does not
yet establish that one material point can be tracked continuously, that the
video is an independent camera recording, or that its measurements would be
more accurate than Camera2.

The record also adds a timing limitation. The962 probed frames include329
without stored presentation timestamps; the last also lacks a decoder
best-effort timestamp. These are distinct metadata fields. No missing value
was filled from frame rate, the saved project, or the visible broadcast clock.
The original complete matching-timestamp test failed. The subsequent visual
screen uses frame ordinals only and does not turn that failure into a pass.
Missing timestamps alone do not show editing, manipulation or an erroneous
historical measurement.

## Source and fixed coverage

The source is the byte-pinned DistantView AVI within the already held public
motion-lab archive, not a new download or an original-camera master. Its two
embedded copies are identical, not independent evidence. The
[protocol](PROTOCOL.md) fixes the archive/member identities, target features,
eight-ordinal selection and two Camera2 contextual images. The
[addendum](ORDINAL-ADDENDUM.md) preserves the failed clock test and declares
the separate ordinal-only method before frame extraction or viewing.

| Layer | Verified held result |
|---|---|
| Selected AVI | 4,749,520 bytes; SHA256 `a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e` |
| Probe | MPEG4,704 by480,YUV420P; sample aspect1:1;962 frame records; declared time base100/2997. These are encoded-file properties, not original-exposure certification. |
| Fixed visual sample | Ordinals0,137,274,411,549,686,823,961; whole native Y-plane PNGs only. No additional historical frames were viewed. |
| Context | Two previously reviewed Camera2 standing images,6593 and6841. They are not synchronized or descending comparison images. |
| Repeats | Two fresh probes and two full decodes; all962 saved decoded-frame hash records agree. No warnings occurred in these completed source runs. |

The first three samples show the high facade/roof outline; frame411 shows a
lower remaining corner/facade edge. Later sampled images show the cloud and
foreground rather than a separately identifiable target roof. Broadcast
graphics are visible and change across the sample. Such graphic changes do
not establish a camera cut, and eight frames cannot exclude intervening edits.
The images are grayscale reading derivatives, not sound or color evidence.

The [root first pass](root-observations.md) was frozen before receipt of the
peer's substantive findings. It identifies standing lower-step-junction
candidates but does not recover them separately in the sampled descending
scene. No new side-view geometry or exposed structural attachment was
established. A source family must not be split merely because framing,
graphics, file bytes or apparent tilt differ.

The separately frozen [peer first pass](peer-observations.md) agrees on those
limited visibility findings. Both readers identify the outer image-right
corner in standing and lowered scenes, but neither recovers the lower step
junctions in the sampled descending scene or establishes new attachment
geometry. Image-right is not an authenticated compass/member assignment;
the clearer outer corner cannot substitute for a west-center step target.
There is no material descriptive disagreement to reconcile. Their notes
were saved before substantive exchange, but both are AI readers of shared
images and protocol framing, not independent human or engineering review.

Root note SHA256: `23bb34818fac5f7508c8e014b539453c736ad6e10c8c912a92a682c106b78e53`.
Peer note SHA256: `4ea522072ae6e566fc0499061972005f72f4b02437dc6ecd46bdd8c1c03a089f`.
The peer also cross-read the report without finding a material visual
overclaim; neither frozen first pass was changed.

## Why no publication table comparison was run

The optional Dan Rather saved-state comparison is not a ready substitute for
the already completed Tilted-project comparison. The paper distinguishes the
earlier Dan Rather/global-collapse zero from its later Camera2/east-penthouse
zero, and no common exposure/event mapping has been recovered. Comparing
the same nominal times could manufacture a mismatch; optimizing a lag could
manufacture agreement. Two saved tracks also cannot resolve the complete
eight-track state or the Tilted east-center nonkey discrepancy.

This screen supplies a positive native-coverage lead, not that missing time
mapping. Its strongest limitation is that related skyline imagery and an
apparently usable corner can still inherit shared processing and ambiguous
feature identity. The image sample does not validate the point-to-center-of-
mass relationship, dimensional calibration or structural load path.

## Executed checks and retained failures

Commands used the bundled Python3 runtime and the pinned existing FFmpeg/
FFprobe binaries. From this worktree, the actual sequence was:

```text
python3 -B research/sherlock-wtc7-investigation/distant-view-source-screen/prepare.py test
python3 -B research/sherlock-wtc7-investigation/distant-view-source-screen/prepare.py preserve
python3 -B research/sherlock-wtc7-investigation/distant-view-source-screen/prepare.py probe --out probe01
python3 -B research/sherlock-wtc7-investigation/distant-view-source-screen/ordinal_screen.py test
python3 -B research/sherlock-wtc7-investigation/distant-view-source-screen/ordinal_screen.py probe --out probe02
python3 -B research/sherlock-wtc7-investigation/distant-view-source-screen/ordinal_screen.py probe --out probe03
python3 -B research/sherlock-wtc7-investigation/distant-view-source-screen/ordinal_screen.py decode --probe probe02 --out views01
python3 -B research/sherlock-wtc7-investigation/distant-view-source-screen/ordinal_screen.py decode --probe probe03 --out views02
```

Here `python3` denotes
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Twelve initial synthetic tests passed; they did not cover all new protocol
requirements. Thirteen ordinal-adapter tests then passed, including null/zero
separation, timestamp disagreement, nonmonotonicity, short counts, format,
geometry and diagnostic-path fixtures. A separate static review found the
initial missing-PTS relabeling, short-sample and diagnostic-retention gaps.
The original producer and first adapter remain unchanged; the new adapter
records its own identity and narrower method.

The initial preserve attempt was blocked by the worktree filesystem sandbox;
the approved scoped retry succeeded without changing the source. Probe01's
FFprobe process returned0 with no stderr, but the parser raised `KeyError`
on the final missing best-effort timestamp. Its raw stdout was not retained
by that original wrapper. A read-only repeat inspected the missing fields,
and fresh probe02/03 retain their complete raw metadata and empty stderr.
No native image was viewed before the addendum and fixed selection.

The new adapter retains timeout status/stderr, but not partial stdout on
timeout; an oversized probe response can still stop before its execution
receipt. These known unused failure-path limits are not claimed fixed.
None of the completed historical probes/decodes timed out, exceeded the
probe bound or emitted warnings. This is not a general decoder certification.

Root's `cmp` checks passed for both probes, selections and full frame-hash
records. Each decode checks its selected PNG pixels against its source Y
bytes. Source and producer hashes are retained in the receipts. Same-code
repeats are repeatability, not independent capture or independent decoding.

A separately written [checker](verify_independent.py) reconstructs every
nullable timing row from the raw probe JSON without importing either producer,
compares all962 saved decoded/luma hash rows across runs, and independently
decodes all16 saved PNGs with standard-library PNG chunk/filter processing.
It rechecks the exact archive-member bytes and59 source/control/result pins
before and after. Its13 synthetic tests and historical check passed, including
root's rerun. The [receipt](independent-verification.json), SHA256
`72eefba7acb6fbd2970d6aaef6ae8b274056170a805b467f1ad178a723c772c4`,
retains the explicit scope limits. Its commands are:

```text
python3 -B research/sherlock-wtc7-investigation/distant-view-source-screen/verify_independent.py --self-test
python3 -B research/sherlock-wtc7-investigation/distant-view-source-screen/verify_independent.py
```

That checker does not independently decode the video or rehash unselected
frame pixels: it compares their saved hash records. The two readers and
separate checker do not supply human acceptance or qualified engineering
review. The original matching-clock test still fails. This finite ordinal
source screen is complete within those limits.

## Next discriminating work and boundaries

The supported next candidate is a fixed interval around the standing-to-lower
corner change, with explicit feature identity, static references and event
correspondence before any trajectory or time comparison. A new declaration
must state its interval, sampling, visibility criteria and uncertainty before
additional viewing. Preserve the two clock fields and missing states; do not
align the video by making its roof motion match a paper or model. That work
is not authorized by this unit's finished sample alone.

Full-reasoning method design with a separately frozen reader/checker is
appropriate for that next step. Do not replay this eight-frame screen or the
completed saved-project inventory as new empirical progress. The version2
material-claim index predates this unit; this report is linked from current
STATUS and the research map, not silently represented as already integrated
into that frozen index snapshot.

No ranking among fire-triggered and deliberate support-removal explanations
changes here. No canonical fact, legal document, original source, frozen
annotation, accepted Sherlock/Faraday state, external transmission, commit or
push changed. The new nullable-clock lesson is deduplicated locally under
SFB-002/SFB-005; feedback remains unsent at the archived-destination boundary.
The evidence/source-preservation skills kept the failed timing test separate
from the new ordinal screen, and the verification skill reused the existing
decoder instead of silently replacing its contracts.
