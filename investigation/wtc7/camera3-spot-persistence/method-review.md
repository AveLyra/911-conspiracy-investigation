# Separate method review — Camera3 spot persistence

2026-10-04. Research-only, prehistorical review by the sibling method reviewer.
No new historical decoding, image viewing, quantitative measurement or peer
observation exchange has occurred in this review. Only this working method
note is authored. Implementation/source preflight and output admission remain
separate from scientific-method review.

## Protocol judgment

The initial [protocol](PROTOCOL.md), SHA-256
`db02d0a499e378ce1aac8ecbef67dbecb24d09cf210a9516c6450a0c112576d3`,
addresses the real unresolved question in the
[October media review](../completion-audit-2026-10-04/media-review.md): whether
the previously described frame258 light-looking spot persists in a fixed
seven-frame neighborhood. It does not repeat the completed Camera2 screen or
claim a video-wide flash search. Qualitative full-frame comparison is meaningful
within the diagnostic derivative even without calibrated radiometry or a
filming clock, provided the stated ceiling is retained.

**One pre-view clarification recommended:** freeze every plausible candidate's
ID and spatial description in the anchor258 record, then carry every candidate
through all seven images. If plausible anchor candidates have different temporal
appearances, preserve the original target's identity as unresolved rather than
selecting the more interesting or persistent one afterward. If all candidates
persist, that shared result may be reported without choosing which was the old
observer's target. The initial ambiguity/unresolved rules strongly imply this;
making it explicit prevents the singular summary from becoming a selection rule.

The anchor-first order is otherwise fair: it localizes the *already nominated*
feature before seeing its neighbors. It is intentionally prior-informed and
does not supply blinding, independent source evidence or a held-out event.
Readers save each first-view record before the next image and freeze complete
records before exchange. This reviewer has method involvement and extensive
prior source familiarity; neither should be hidden in the observation record.

The three appearance categories distinguish unresolved visibility from physical
absence. Persistent appearance rejects only an isolated one-frame reading of
this derivative in this window. It does not exclude persistent/reflected
illumination, temporal variation below resolution, coding artifacts or events
outside the sample. Limited resolution is not an authenticated transient, and
neither outcome establishes reflection, glass, emitted light, a charge or cause.

No numerical localization, intensity, area, duration, motion or detector result
is authorized. Thus this does not substitute an AI annotation for the charter's
human gate on consequential automated measurement. Human142-N12, the separate
curve checks, user coordinate locks and matrix/expert/privacy boundaries remain
unchanged. A later quantitative or causal use requires its own justified scope.

## Source, recipe and execution boundaries

The fixed sample is decoded indices255–261 from the held442-frame WMV, not the
232-frame MP4. PTS17.000–17.400 are encoded positions, not measured exposure
times or physical event duration. All442 decoded gray hashes and the complete
raw hash must match the held map before selecting the seven unmarked native
PNGs. This verifies repeatability of that representation, not clean originals.
The warning history remains consequential even if no warning names these indices.

The complete existing [prepare.py](../camera3-late-reannotation/prepare.py) was
read but not imported or executed. Its recipe uses copyts/noautorotate, the
specified video stream, noautoscale, gray, passthrough rate and demux time base.
Its larger22-frame selection, rulers, crops and overlays are **not** reusable
outputs for this unit; the new adapter must emit only the fixed seven full
720×480 L images. The old script's `stderr_not_exported` practice must not be
carried forward: this protocol expressly requires retained diagnostic logs.

The earlier receipt records152,755,200 raw bytes, complete442-frame equality,
three corruption mentions and raw hash
`1244ddf86418a17a1f4140c979268d33a5964a098da4fd6fd7817499bcb60b6b`.
Frame258's saved gray-pixel hash is
`486e653f5100477a6ab2b6994aff023a4e4aae2ed22c24ef72c67956fe6976ea`;
its PNG-container hash is different by design. Container equality is not the
only way to establish identical decoded PNG pixels. These are receipt facts,
not a fresh source decode or image inspection.

Prospective implementation review must check exclusive output creation; fixed
indices and map row identities; exact recipe/binary/source/control pins; complete
raw length/frame count and every-frame hash; timeout/nonzero-return failure
preservation; seven reopened PNG shapes/modes/pixel hashes and anchor equality;
and post-input checks before any completed receipt. Synthetic tests must exercise
refusals, not just happy-path selection. No new decoder, automatic source
substitution or changed criterion may rescue a mismatch.

The one diagnosed adapter-repair allowance is bounded and requires a new logged
version/review before viewing; it is not permission to repair historical pixels
or relax a source mismatch. Keep failures. Treat the two actual failed-display
retries as a **shared unit budget**, coordinated with parent before a retry;
they are not repeat looks. Stop after seven frames and two frozen records plus
review, including if unresolved. No automatic neighborhood expansion.

## Actual coverage and checks

Full reads in this task: current main/worktree AGENTS; main WORKFLOW,
START-HERE and full CHARTER; initial protocol; complete old prepare.py and
flash-opportunity observer record; evidence-falsification/source-of-truth/
development-verification skills and required audit references. Earlier complete
October assessment/media reads were supplemented with the current finite-test
paragraphs; the media freeze hash was rechecked. The old views01 receipt was
read selectively for inputs, execution/recipe and anchor fields, not claimed
as a fresh validation of all products. No root new observation was read.

Read receipts: `61c05c` protocol/skills, `8d88c8` recipe/observer/references,
`602ea1` current AGENTS, `2bcd84` workflow/start and partial combined charter/
receipt, `bb88a2` complete charter recovery and pins, `e966ba` exact receipt
fields/current dependency paragraphs; all exited0. Combined charter output
truncation was not counted as a complete read until the separate recovery.

Read-only Python `e966ba` checked saved diagnostic status, before/after pin
equality, current old-code hash,442×720×480 raw length, saved all-frame-match
flag and exact anchor record. It did not open raw WMV/PNG content, run FFmpeg,
or newly verify all historical pixels. Pin command `bb88a2` returned:

| Artifact | SHA-256 |
|---|---|
| Old prepare.py | `0b7baeb81236a7ab8fdb5435ed7d86e10c754e22fd35f94051d96538ae29d139` |
| Old views01 receipt | `8bf54e80ccb0eb823cd9a09fc45e285fa4a649c166aaf2b26d551c13782c3161` |
| Original observer record | `0c22f63fd028bfb4bdf0097f34d4ebf157a4003bfd1437ccb15335889574a80e` |
| October media review | `10110423e5c6458420e94dbdbba15b67e20a59acaac2726503fa547d9b55c8bb` |

**Initial disposition, before adapter review:** method acceptable with the ambiguity clarification;
new adapter/tests, source preflight and prospective code freeze have not yet
been reviewed here. This note is not historical-execution or image-viewing GO.

## First adapter review — before historical execution

The revised protocol, complete new `prepare.py` and complete `test_prepare.py`
were read in `adf2b3` (exit0). The candidate-ID and shared retry clarifications
are now explicit and resolve the initial method concern. The code imports only
the pinned old definitions, not old main; it constructs the identical decode
command, checks fixed map clocks, all442 pixel hashes and complete raw hash,
retains stderr, reopens seven native PNGs, checks old258 pixels and rechecks
input pins before a passing receipt. Existing-destination rejection plus
`mkdir()` without exist_ok prevents adopting/clobbering an existing run.

**Material failure-record correction requested before execution:** basic decode
metadata must be attached to the receipt before `selected_planes()` validates
length. In the first adapter, short output raises `raw_length` before recording
return code, actual byte count/hash and warning count. Saved stderr alone does
not preserve the required return status. This is an adapter traceability defect,
not a failed historical run; no decode has been performed by this reviewer.

The initial seven synthetic tests cover helper selection, dimensions, invalid
indices, PNG round trips/refusals and output naming. They do not exercise main's
failure publication or postchecks. Requested minimum addition: a mocked short/
nonzero decode whose failure receipt retains status/count/hash and admits no
images. A successful synthetic seven-image pipeline plus post-input-change and
anchor-mismatch refusals would also check the integration boundary proportionately.
No historical input should be read by those fixtures. Final code/test review and
synthetic execution will be recorded below before any scoped clearance.

## Final prehistorical review — correction resolved

Root applied one bounded pre-execution repair, before any historical decode or
view. Complete final code and tests were read in `e5f2b9`, exit0. Basic decode
return code, raw length/hash, warning count and stderr hash are now recorded
before `selected_planes()`. Timeout failures separately preserve partial-byte
length/hash, stderr, timeout status and no successful receipt. Thus the
identified short-output traceability defect is resolved, not hidden by a
successful historical rerun. No historical run was used to test the repair.

The final suite adds five mocked main-path fixtures to the seven helper tests:
seven-image success, short/nonzero output, timeout, changed input and old-anchor
mismatch. It constructs a temporary synthetic source/map/receipt/PNG tree,
patches the old-module loader and decoder call, and uses small synthetic planes.
It never loads the real old module or decodes/reads historical media. The
unchanged real code/interpreter files are read for identity bookkeeping. These
fixtures exercise acceptance/failure plumbing, not FFmpeg correctness, original
image fidelity, source authentication or a historical light event.

Independent command:

```text
/Users/admin/.pyenv/shims/python3 -B -m unittest -v test_prepare.py
```

Run from this unit directory in `d90914`: **12 tests passed**, 0.282 seconds;
command exit0. A separate interpreter/version print in the same command
confirmed `/Users/admin/.pyenv/versions/3.13.7/bin/python3`, Python3.13.7 and
Pillow12.0.0. All three hashes below matched before and after that test run:

| Final prehistorical artifact | SHA-256 |
|---|---|
| PROTOCOL.md | `bb2e8f38e7c0d7aadb3421252a2fe054dfa36d00101403e5250f161df1cba2b0` |
| prepare.py | `f498addbabe11fec2e4e3e0ced8834a9702f2c1fecd28d5a4e964433e6ebc480` |
| test_prepare.py | `f1dbd648e5e1fefcda9994a9e818206f33e5cfb6428c5cd96752df3ec55422bb` |

**Scoped method/code clearance:** no unresolved material issue found in this
reviewed snapshot. It may proceed to the one declared historical extraction
only after the separately assigned source/clock/binary/version preflight and
prospective pins are complete. This is not acceptance of unproduced outputs
or image-viewing GO: all442 hashes/raw identity, seven reopened PNG checks,
old258 equality, independent selected-pixel verification and final source
checks still have to pass before either reader views a new image. Do not
consume another automatic repair if a new substantive failure occurs; preserve
it and return the exact blocker under the protocol. No viewing, historical
decoding, cause conclusion or human approval was supplied by this reviewer.
