# Eight held clips: consistent tape labels, unresolved historical ordering

2026-10-04. Research only. **All eight access copies contain the same tape-name
prefix, and their timecode labels increase in clip-number order.** This supplies
a usable source/edit-order lead, not an authenticated camera chronology.

There is a consequential tension to investigate: the clip associated with
Figure5-143 has an **earlier** embedded label than the clip associated with
Figure5-142, whereas NIST's text places5-143 later. Edited-tape labels, a wrong
source/exposure association, incorrect metadata and an incorrect published
chronology remain competing explanations. This check does not choose among
them or establish exaggerated fire, fabrication or collapse cause.

## Observed fields in all eight copies

The [fixed manifest](inputs.json) includes every previously selected complete
copy, not only the two promising views. The [complete output](results.json)
retains192 header records and6928 metadata payload bytes, including every
field's raw bytes, offsets, hash, text prefix and binary tail. Each file has
exactly one occurrence of each of the five selected tags. All eight original
and alternate tape-name prefixes are `Vince Demetri CBS`; original/alternate
timecode prefixes agree within every clip. They are repeated fields in the
same files, **not independent clocks or corroborating witnesses**.
Their full original/alternate payloads differ in the retained binary tails in
every clip. Agreement here means the text prefixes, not byte-identical fields;
the tail contents remain uninterpreted.

| Clip | Original and alternate timecode prefixes | Header video frames | Stored duration, seconds | Embedded comment, paraphrased — not a new visual finding |
| ---: | --- | ---: | ---: | --- |
| 1 | `00;00;05;17` | 418 | 13.947490 | Distant Tower1 view from north. |
| 2 | `00;00;33;14` | 809 | 26.994146 | WTC7 from north/northeast. |
| 3 | `00;01;00;28` | 189 | 6.306420 | WTC7 window flames and smoke. |
| 4 | `00;01;07;09` | 206 | 6.873684 | Window smoke, broken-window levels and flames below. |
| 5 | `00;01;54;22` | 529 | 17.651302 | WTC7 window smoke. |
| 6 | `00;02;47;06` | 197 | 6.573358 | Window flames/smoke and falling debris. |
| 7 | `00;03;12;26` | 1128 | 37.638314 | Similar description plus corner damage. |
| 8 | `00;08;35;13` | 2091 | 69.771024 | Tower2 impact from north, described as slow motion. |

These comments are source metadata of unverified authorship. They neither
independently establish the scenes nor validate the asserted fire/damage or
slow-motion descriptions. Clip8's comment is nevertheless an affirmative
warning against assuming the whole labelled sequence is a continuous camera
clock. The [earlier fixed screen](../../cbs-vince-source-screen/stage4/report.md)
found a different, distant two-tower composition in its nine sampled frames;
it did not authenticate the comment or inspect every frame. No new media view
or essence decoding occurred in this unit.

All eight video header lengths, rational timebases, zero start values and
rounded durations agree with the saved container inventories. Stored timebases
are `333672/10000000` for Clip1, `333674/10000000` for Clip4 and
`333673/10000000` otherwise. Those small differences are retained, not replaced
by exactly30 or30000/1001. Stream-field meaning follows
[Microsoft's AVIStreamHeader specification](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/api/avifmt/ns-avifmt-avistreamheader).

## Conditional arithmetic, not historical elapsed time

All four declared comparisons—original/alternate crossed with nominal30
non-drop/30000-over-1001 drop-frame—are available and order the labels
**1,2,3,4,5,6,7,8**, with no ties. Both lanes give the following results.
Units below are conditional source-frame counts, **not observed missing video
frames or measured historical gaps**. Half-open intervals use full earlier
clip length: gap = next start − previous start − length.

| Adjacent clips | Non-drop start difference | Drop-frame start difference | Non-drop gap | Drop-frame gap |
| --- | ---: | ---: | ---: | ---: |
| 1→2 | 837 | 837 | 419 | 419 |
| 2→3 | 824 | 822 | 15 | 13 |
| 3→4 | 191 | 191 | 2 | 2 |
| 4→5 | 1423 | 1423 | 1217 | 1217 |
| 5→6 | 1574 | 1572 | 1045 | 1043 |
| 6→7 | 770 | 768 | 573 | 571 |
| 7→8 | 9677 | 9667 | 8549 | 8539 |

Exact rational seconds for every row and interpretation are in results.json.
They require one-to-one, uninterrupted, same-rate source mapping; this check
does not establish that mapping. The two-frame3→4 gap makes an adjacent-source
segment hypothesis worth testing, not a finding of continuity. No gaps are
filled, no edit is bridged, and no24-hour rollover is assumed.

The drop-frame component arithmetic follows
[FFmpeg's published7.1 source](https://ffmpeg.org/doxygen/7.1/timecode_8c_source.html).
Our strict ASCII parsing and omitted-label rejection are separately declared
rules; semicolons alone do not prove a drop-frame historical clock. The
[reference note](references.md) states the precise definition and source limits.

## The Figure5-142/5-143 ordering tension

This is a **post-output contextual comparison**, not a newly measured camera
clock or an amendment to the frozen primary arithmetic test. The prior
[Clip3 comparison](../dense-clip3/v2/report.md) associates it with5-143; the
[Clip7 comparison](../dense-clip7/report.md) associates it with5-142. Both have
strong changing-detail candidates, but neither proves the exact original
exposure/field or complete image-generation chain.

The held [NCSTAR1-9 printed page228/PDF page272 text](../../fire-coverage-batch3/assets/run01/context/P-8338c00a97d8.txt)
describes5-143 as coming from a clip recorded about a minute after5-142.
The native labels put Clip3 before Clip7 under both tested interpretations.
Changing the drop-frame convention does not reverse that direction.

Exact frame identity is **not needed to retain the sign of this tension**:
under those within-clip associations and the one-to-one mapping assumption,
every exposure in Clip3 precedes every exposure in Clip7. Neighboring frame
or field ambiguity cannot account for the reversal. The unresolved historical
clock/source premises, not a one-frame precision issue, control the conclusion.

Thus the following three propositions cannot all be accepted without a
reconciliation: these are the corresponding historical source intervals;
their labels preserve chronological recording order without reordering;
and the published later/earlier relationship is correct. **The contradiction
is conditional on those premises.** We have not independently established
the first two, so the headers alone do not falsify NIST's relative timing.

The strongest ordinary alternative is a tape/export containing reordered
excerpts or replay material. The generic source name and slow-motion comment
make that concrete enough to investigate, but do not prove how this particular
sequence was assembled. Other live alternatives are copied/stale labels, a
similar exposure from a different, incorrectly associated recording interval,
or a publication timing/association mistake.
Neither an innocent workflow nor intentional alteration receives a finding
merely because it is possible. A demonstrably unedited original with verified
source-to-still joins would materially change the assessment.

## What is established, and what would change it

| Claim | Evidence strength and limit | Disconfirming or resolving evidence |
| --- | --- | --- |
| The eight acquired copies contain these tags and header values. | Direct byte observation; strong for the pinned copies, not original-camera authenticity. | A wrong hash, offset, length, transcription or independent byte mismatch. |
| Four declared calculations give the same increasing label order. | Exact conditional calculation; repeated lanes are dependent. | Arithmetic error, different applicable timecode semantics, or invalid source mapping. |
| That ordering independently confirms the publication's event chronology. | Not established; the associated pair instead exposes a conditional directional tension. | Original reel/capture/edit records plus a source-frame/field-to-still crosswalk. |
| NIST exaggerated the fire or deliberately misrepresented evidence. | Not established by header data; intensity adjustment itself is already disclosed. | A controlled comparison showing an unsupported change that materially inflates a reported fire observation or specific model input; intent requires additional evidence. |
| Fire or deliberate support removal becomes more probable from this unit. | No defensible ranking change. These tags do not test structural initiation or support loss. | Case-specific discriminating physical evidence or a validated causal-chain test. |

The next distinct local task is a bounded review of the **timing basis and
source-generation references for Figures5-141–143** in the held report,
attribution inventory and already admitted production records. Look for an
actual original/edit sequence and clock derivation keyed to the recovered
tape name and labels; report where the chain stops. Seek a **paired5-142/5-143
provenance chain**, including camera-versus-master timecodes; a record for5-142
alone may not resolve the comparison. Do not rerun the completed
matcher or treat another metadata pass as physical validation. The missing
exact still/export worksheet remains a record lead, not an asserted document.

In parallel, bounded qualitative fire observations may use the established
scene relationships with timing, visibility and processing limitations made
explicit. Unknown exact exposure is not a universal reason to suspend all
physical analysis. Pane-state change, precise time-dependent fire spread and
particular model inputs require the tighter joins appropriate to those claims.
Do not use this pair to establish progressive glazing loss or fire growth
until ordering and comparable window visibility are supported.
Human142-N12 inspection and all other charter work remain unresolved.

## Verification status

The method was separately reviewed before execution; root and reviewer each
passed18 final synthetic controls, including independent-lane and mixed
lossless-byte representation cases. The frozen run completed once, exit0,
with no probe/decoder/subprocess. All declared input and dependency hashes
matched before/after; Clip7's twelve payloads/866 bytes equal the earlier saved
inventory. The separate result audit directly verified all192 listed headers,
96 retained payloads/6928 bytes, all40 selected tags, eight video headers and
all28 conditional edges, without the production parser. No substantive result
discrepancy was found. Its two prior-schema lookup failures were corrected and
preserved. [Execution and review](execution.md) distinguish actual checks,
pre-run corrections, auditor failures and their limits. Direct reported-offset
verification is not an independently rediscovered complete container tree.

This unit changes source-lineage knowledge, not the legal record, actual-human
acceptance, the user-assessed±1 native-y-pixel placement ranges, or a collapse
cause ranking. No disclosure, outreach, matrix save, commit or push. The full
investigation goal remains active and incomplete.
