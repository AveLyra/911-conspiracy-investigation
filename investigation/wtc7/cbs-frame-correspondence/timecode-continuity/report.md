# The eight clips have consistent drop-frame counters

2026-10-04. Research only. This test checks the internal timing metadata of the
held access copies. It does not authenticate an original camera clock.

## What changed

The counters are not merely plausible-looking strings. **Every one of the 5,559
within-clip transitions advances exactly one frame under the encoded drop-frame
convention**, and all eight first-frame values match both original and alternate
AVI header labels. All 5,567 candidates have valid component digits and ranges;
none has an omitted drop-frame label. No mode change, other retained flag change,
counter repeat, counter skip, backward counter step or day-rollover candidate
occurs within these clips. This is counter continuity, not proof of picture continuity.

This rules out disagreement between the parsed header start components and
each first stream counter in these copies.
It strengthens the description of their **internally consistent counter order**,
not the identification of that order as original filming chronology. The
conditional Clip 3 / Figure 5-143 versus Clip 7 / Figure 5-142 ordering tension
survives. Neither the published chronology nor deliberate alteration is proved
or disproved by this test alone.

The frozen [full result](result01.json) contains every decoded frame, transition
and pairwise comparison, not only the favorable summaries below. The
[execution record](execution.md) distinguishes method checks, historical execution
and independent arithmetic reproduction. A separately authored checker and
root's read-only replay agree on every frame, transition, pair, header join and
rational span. This is reproduction using the same inputs, not a second clock.

## Fixed results

These are normalized **counter labels**, not event-day local times. The semicolon
before the frame field denotes the interpreted drop-frame convention; the raw
file-header strings use semicolons throughout and are retained in the inputs.

| Clip | Frames | First counter | Last counter | One-step transitions |
| --- | ---: | --- | --- | ---: |
| 1 | 418 | `00:00:05;17` | `00:00:19;14` | 417 / 417 |
| 2 | 809 | `00:00:33;14` | `00:01:00;14` | 808 / 808 |
| 3 | 189 | `00:01:00;28` | `00:01:07;06` | 188 / 188 |
| 4 | 206 | `00:01:07;09` | `00:01:14;04` | 205 / 205 |
| 5 | 529 | `00:01:54;22` | `00:02:12;12` | 528 / 528 |
| 6 | 197 | `00:02:47;06` | `00:02:53;22` | 196 / 196 |
| 7 | 1,128 | `00:03:12;26` | `00:03:50;13` | 1,127 / 1,127 |
| 8 | 2,091 | `00:08:35;13` | `00:09:45;05` | 2,090 / 2,090 |

The drop-frame bit is set in all candidates. Retained noncomponent flag bytes
are uniformly `c08080c0`; their equality is not evidence of camera synchronization
or a software fingerprint. Ancillary bits were preserved positionally because
their names/roles depend on the profile and source convention.

Forcing a non-drop interpretation creates three apparent three-position jumps:
Clip 2 at frames 795→796, Clip 5 at 157→158 and Clip 8 at 736→737 (zero-based).
Each is an ordinary drop-frame minute transition and is a one-frame step under
the encoded convention. Thus the data support drop-frame counter arithmetic;
the forced non-drop lane is a sensitivity diagnostic, not an equally supported
continuous clock. No actual picture frames are shown missing by those jumps.

All 28 ordered clip pairs have every earlier clip's counter value below every
later clip's value. Under the encoded convention, the seven adjacent differences
between the next first counter and the prior last counter, minus one, are
419, 13, 2, 1,217, 1,043, 571 and 8,539. These are unrepresented counter positions,
**not measured omissions from the original event**. Clip 3's last counter is
3,766 counter steps before Clip 7's first, so neighboring-frame choice cannot
reverse their counter order.

The earlier header-only study used a conditional start-plus-frame-count model
for each convention. Its forced non-drop gaps for 2→3 and 5→6 were 15 and 1,045.
The present endpoint-based forced non-drop differences are 13 and 1,043 because
the intervening clips contain the two-label jumps just identified. This is a
difference in declared arithmetic and its continuity assumption, not a silent
correction to source bytes or an unexplained disagreement. The encoded
drop-frame results agree with that earlier study's drop-frame lane.

The exact AVI periods remain separate from nominal DV `1001/30000` seconds.
Their first-to-last representation spans differ by at most about 1.324 ms
(Clip 8). This bounds only the comparison of those stored rate conventions;
it is not an estimate of camera-clock accuracy, editing error or event timing.

## Claims and strongest alternatives

| Claim | Evidence and present strength | Alternative or weakening evidence |
| --- | --- | --- |
| The held counters are internally continuous under their DF bit and match header starts. | A within the declared computational scope: independently reproduced from all audited raw candidates and transitions, not a clock-origin finding. | Wrong input pins, masks, profile, frame mapping or independent arithmetic discrepancy. |
| The counter labels preserve original chronological filming order. | D, underdetermined; continuity alone does not establish it. | Copied or regenerated master counters, reordering, replay material, or a mistaken source-to-still association. Original tape/edit/export records could resolve it. |
| NIST's relative chronology is independently validated by these labels. | E, unsupported by this test. The known conditional directional conflict remains. | Correct source associations plus an authenticated original recording-order map could turn the conditional conflict into a demonstrated timing discrepancy; a documented edit map could reconcile it. |
| This unit changes which collapse mechanism is most probable. | E, unsupported. The computation tests file lineage, not structural initiation, heating or support loss. | A separate causal-chain or case-specific physical test is needed. |

A continuous original recording is compatible with this result. So is a
continuously numbered edited master. The pinned
[DV generator definition](../dv-metadata/sources/ffmpeg-n7.1-libavformat-dvenc.c)
demonstrates that software can generate such fields; it does not identify the
historical software or show that this occurred here. Agreement between embedded
and header copies of one counter is not independent corroboration from two clocks.
The prior absence of recording-date/time packs does not supply the missing origin.

The specific original-camera→copy/edit→published-still mapping remains a useful
record lead. This finite counter check is now reproduced and complete; it should
not expand indefinitely into metadata checks or delay unrelated physical work.

## Next physical work

The prepared seven-pair spring/shell force-and-energy comparison is a concrete
model-fidelity test, but its actual-human axis/legend check remains outstanding;
the user's roof-point review does not satisfy it. Its existing arithmetic should
not be rebuilt. See the [separate graph review packet](../../connection-curve-comparison/human-review-packet.md).

An available parallel task is a finite same-target visibility comparison across
the already extracted CBS candidate frames: determine whether the particular
edges and surfaces needed for window-state interpretation are actually resolvable.
Preserve neighboring alternatives, source processing and reader disagreement;
do not turn an untimed still count into a thermal or ventilation-input test.
Human142-N12 and consequential physical-state review remain separate requirements.

No coordinates, raw evidence, accepted Sherlock state or legal records changed.
The broader charter remains active and incomplete; no cause-ranking update,
external disclosure, human acceptance, commit or push follows from this result.
