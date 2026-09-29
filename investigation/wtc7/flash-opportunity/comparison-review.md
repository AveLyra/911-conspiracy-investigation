# Independent comparison of frozen spatial-opportunity records

2026-09-24. Qualitative record comparison only. Both complete observation
records were read after their freezes; no images, new annotations, historical
pixel/time/intensity calculation, detector result or cause ranking was made.
The original records remain unchanged. This file is the only authored artifact.

## Input identity and reading scope

The supplied frozen pins match freshly computed SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| root-observations.md | `1fcc884256604817ac9992b9e6ab61b7ae216a1d4e660d135a0b8856fea1e5d4` |
| observer-observations.md | `0c22f63fd028bfb4bdf0097f34d4ebf157a4003bfd1437ccb15335889574a80e` |
| PROTOCOL.md | `5cb7933fbdc109801245363b0bd15e49622907dd85fb4fdb8eec08f4cf346ff0` |

Root's 207 lines and the observer's 141 lines were read completely using
`sed -n '1,260p'` for each. `wc -l` confirmed those extents;
`shasum -a 256` supplied the pins. Filename-only `rg --files` located this
unit's records. No source media or new report interpretation was inspected.
The evidence-falsification and source-of-truth controls keep shared descriptive
agreement distinct from physical truth, source independence or human review.

Both records attest to the same eight complete native images, in protocol
order, with one successful display each and no retries or additional images.
The listed displayed paths correspond across records. This comparison verifies
their recorded coverage and correspondence, not the truth of the viewing
attestations through independent UI telemetry or fresh pixel verification.
Root's preserved pre-view line explicitly says it remains as history; it is
not inconsistent with the later completed entries and freeze.

## All eight row comparisons

Each cell below is **root / observer**. V/P/H/O/U retain the protocol's
region-specific meanings; they are not area measurements or accuracy scores.

| Frame | Roof / raised region | Upper exterior wall | Ground / base | Meaning-level comparison |
|---|---|---|---|---|
| Camera2 6593 | P / P | V / V | **H / U** | Both describe a distinguishable right/central roof and substantial banded face, left cloud interference and lower foreground obstruction. Root assigns the actual base to foreground masking; observer cannot separate masking from possible below-frame exclusion. |
| Camera2 6717 | P / P | **V / P** | **H / U** | Both describe center/right wall and roof visibility with cloud to the left. Root calls most of the upper face resolved; observer expressly includes left-wall/edge cloud overlap or indistinctness in a partial-wall judgment. Base difference has the same meaning as 6593. |
| Camera2 6958 | P / P | P / P | **H / U** | Both describe an exposed central/right wall/top edge and a cloud-veiled left portion, with roof-adjacent light forms not classified as events. Root is more definite about masking of the actual base; observer preserves its location/framing uncertainty. |
| Camera2 7013 | P / P | P / P | **H / U** | Both describe limited central/right wall/top-edge access and substantial cloud/foreground obstruction. Neither identifies target ground contact; they differ on whether foreground masking alone can be assigned as the base's visibility state. |
| Camera3 258 | V / V | V / V | U / U | Both describe a substantial upper silhouette/banded face against light background, not an exposed whole roof surface or interior. Both leave foreground masking versus below-frame exclusion unresolved for the actual base. |
| Camera3 300 | V / V | V / V | U / U | Both describe a substantial upper outline and broad banded face, with the lower building screened. Neither identifies ground contact or claims useful flash contrast merely from spatial exposure. |
| Camera3 330 | P / P | P / P | U / U | Both describe central/right visibility with left cloud/foreground interference and softened/uneven appearance; the base remains unidentifiable. The described appearance is not attributed to a physical or processing cause. |
| Camera3 348 | P / P | P / P | U / U | Both describe only a small apparent target edge/banded strip between foreground structures and cloud. Neither treats that remnant as authenticated material continuity or identifies the ground-contact region. |

This exhausts the roof/wall/base label comparison for the fixed rows. The
five differing labels are qualitative bookkeeping, not five independent
physical contradictions or an observer-accuracy score. No consensus code,
majority result or accuracy percentage is substituted for either record.

## Substantive disagreements and uncertainty

**All four Camera2 base labels require explicit preservation.** Root's H is
more specific than the observer's U about where the unobserved base lies
relative to foreground structures and framing. Both agree in their prose
that no target ground-contact region is seen. The safe shared statement is
therefore: *neither observer identifies target ground contact; foreground
obstruction is described, while one observer retains possible additional
out-of-frame exclusion.* Do not write that both independently established
the actual base entirely inside the frame and hidden. Nor does U mean that
the observer saw the base or disputed all foreground masking. Without images
or a geometry check, this reader cannot adjudicate H versus U.

**Camera2 6717 upper-wall extent is not a measured disagreement.** Root's V
and the observer's P coexist with similarly described central/right wall
visibility. The observer explicitly treats the left-wall/edge portion as
masked or indistinct. Root describes most of the broad face as resolved but
does not supply a fixed visible-area denominator. The difference may reflect
region extent or the threshold for "substantially visible," and may also
reflect a genuine difference in perception of the left wall. The record
cannot separate those possibilities. Preserve both codes and their reasons;
do not average them, infer a visible fraction, or retroactively redefine the
region/threshold to erase the difference.

**A uniquely mentioned light detail is not a disagreement or event.** The
observer records a small light spot near Camera3 258's upper-left banding.
Root's corresponding entry describes alternating wall tones and bright
background/foreground but does not mention that specific spot. Omission
does not mean root denied its existence, independently failed to detect a
flash, or recognized it as ordinary. Retain it as one observer's single-frame
description if relevant to a prospectively declared temporal follow-up.
Neither record supplies adjacent-frame transience or source attribution.

## Shared observations and their permitted ceiling

Both records describe some exposed upper exterior/roof-outline regions in
the selected images, alongside substantial masking and an unlocated base.
Both retain exposed surface/background as a possible place where sufficiently
conspicuous outward illumination could appear. Neither establishes that a
specific internal source would illuminate that region or be recorded. Thus
the records support neither "nothing could have been visible" nor a calibrated
negative inference from failure to recognize a light event.

Both retain bright sky/cloud/foreground and wall-pattern/edge confounders.
These are appearance descriptions and alternative explanations, not verified
reflections, emitted-light mechanisms, clipping statistics or quantified
sensitivity. Both retain grayscale and unknown exposure limits and Camera3's
diagnostic/warning history. Their agreement does not remove common source,
method, prior-knowledge or interpretive dependencies.

The records make no flash-present/absent classification and supply no paired
temporal record. Cross-row descriptions must not be promoted here into
duration, rate, physical sequence or synchronized cross-camera findings.
The all-native temporal continuation identified in `method-review.md` remains
a separate future task; this eight-image comparison does not complete it.

Disposition: **all eight frozen rows compared; disagreements preserved;
no observation adjudicated or promoted to a consequential measurement**.

## Final report critique

The complete `report.md` was subsequently read with bounded `sed`; its reviewed
SHA-256 is
`be15e8cac028d21535bb8832c5e163b0b4f8800e06793e96c95b28514479c5e6`.
This read occurred after the independent comparison above. No image or
additional historical measurement was used to assess the report.

**No material unsupported observation or premature acceptance was identified
in the reviewed synthesis.** Its eight-row table matches the frozen labels.
It expressly qualifies the four root H base attributions, preserves the wall
V/P disagreement, retains the observer-only light detail without turning an
omission into nondetection, and distinguishes spatial opportunity from actual
transience or detector sensitivity. Neither categorical agreement nor matching
source hashes is presented as human review, authenticated exposure timing or
evidence favoring a cause. The full temporal review remains explicitly future
work, with one-frame candidates retained rather than excluded by persistence.

The report's phrase that the Camera2 6717 readers "disagree whether left cloud
makes the wall category partial" should be read as a description of their
different codes/reasons, not a demonstrated diagnosis of why they differ.
The records do not separate a perceptual difference from region-boundary or
category-threshold choices. No change to the preserved labels is justified.

This critique checks consistency with the frozen observations and method,
not an independent replay of the report's source/metadata integrity claims.
Those remain supported, if verified, by the separately linked source check
and execution record. No source warning is cleared by this critique and no
human/qualified acceptance is supplied.
