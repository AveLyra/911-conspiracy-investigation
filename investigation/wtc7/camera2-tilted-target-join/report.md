# Camera2 / Tilted target-frame correspondence

2026-09-24. Working research for Q07/Q10; not a physical-light finding, human
acceptance, expert report or completed investigation. Independent arithmetic
and [bounded critical review](critical-review.md) are complete.

## Result

**The comparison identifies specific review candidates without using the two
left-foreground bright points as matching targets.** Across all476 Tilted frames,
both declared width-resize branches select **312** for Camera2 **6925**, and
**357** for Camera2 **6970**, when scoring the fixed right-half or target-right
scene regions. Adjacent Camera2 queries select adjacent Tilted frames in those
regions. These are reproducible score minima, **not authenticated original
exposure correspondences**.

The background-only region sometimes selects neighboring frames instead. That
disagreement and all scores are retained. The fixed top-five-with-cutoff-ties
and neighbor rule produces13 review candidates for6925 and9 for6970. This is a
transparent viewing shortlist, not a confidence interval or complete set of
physically possible exposures.

No shortlisted Tilted image was visually inspected for the bright points in
this unit. Whether the appearances are retained in the alternate representation
is therefore **not yet tested**. No causal ranking changes.

## Fixed comparison and numerical result

The [protocol](PROTOCOL.md) preceded new scoring. The
[mask sanity check](mask-sanity.md) viewed only existing native Camera2 frames
6925 and6970, confirming the described upright is comfortably left of the fixed
image midpoint in both. No numeric point coordinates were measured or supplied
by the user. The mask stayed fixed; actual-human review remains a separate gate.

All six queries were compared against all476 native Tilted frames, with two
separately retained width-only resize branches, three fixed regions and the
existing every-fourth-pixel grid: **17,136 scored pairs**. Raw mean absolute
stored Y/luma-code difference determines ranks. Correlation remains diagnostic only;
all score arrays, ties and rank orders are preserved in
[scores](scores01/scores.json), with [summary](scores01/summary.json).

| Camera2 index | Right-half and target-right minimum, both branches | Background minimum, nearest / bilinear | Union shortlist count |
|---:|---:|---:|---:|
| 6924 | 311 | 311 / 311 | 9 |
| 6925 | 312 | 312 / 312 | 13 |
| 6926 | 313 | 312 / 313 | 13 |
| 6969 | 356 | 356 / 356 | 7 |
| 6970 | 357 | 356 / 356 | 9 |
| 6971 | 358 | 357 / 357 | 7 |

No minimum is at the0/475 domain boundary, and no branch/region has a reversed
winner sequence. Background-only repeated winners remain rather than being
forced into a one-to-one map. The right-half and target-right series are locally
consistent; this does not establish a global fixed offset or validate either
clip's physical clock. The overlapping regions/branches are not independent
historical witnesses.

The6925 shortlist is306–318 inclusive. The6970 shortlist is352–360 inclusive.
Adjacent-query shortlists extend the combined review domain to306–321 and
352–361; the exact per-query membership is retained, including the gap in the
6926 shortlist. A union must not overwrite which query admitted a candidate.

## Integrity and reproduction

The native extraction reuses the inspected prior command/parser under pinned
media, code, probe and frame-ledger identities. All476 full Y420 frame hashes,
luma hashes and saved clock rows agree with the earlier records. All476 native
grayscale PNGs round-trip to their source luma bytes. The complete raw stream
is246,758,400 bytes, SHA-256
`164f5725bde62da7da479f46aeea355c4a4bea86411be6c486734330578d2524`.
No decoder stderr or Python rendering warning was recorded. Those checks do
not authenticate the original camera recording or make it calibrated imagery.

Root checked all482 extraction products against their receipt. All input pins
were unchanged. Eleven extraction synthetic tests passed under both author and
root runs. Nine matcher tests passed under root and separate review, including
signed subtraction, constant/blended/tied examples, cutoff ties, neighboring
alternatives and excluded-region perturbation through both resize branches.
The concrete perturbation bounds are Tilted native x<350 and Camera2 x<300,
not every pixel left of the midpoint. This checks the local resampling footprint,
not all possible upstream compression or processing influences.

Two complete matcher runs reproduced all three score/summary/receipt files
byte-for-byte. That is same-program reproducibility, not independent historical
corroboration. A [separately implemented checker](check_scores.py) then verified
all482 native PNGs, all17,136 scored pairs and all complete ranks, ties and
shortlists. Integer differences and MAE agree exactly; the largest correlation
difference is1.24×10^-13 or less, within the predeclared1×10^-12 tolerance.
The [full replay result](independent-check01.json) retains recomputed arrays.
Root rechecked that output, exact arrays/summary and all517 input pins. Shared
Pillow resizing, NumPy and historical sources limit implementation independence;
there was no second historical capture or new exposure authentication. See
[validation](validation.md) for the executed checks and critical disposition.

The stored Tilted stream duration differs by two ticks from final-frame PTS
plus recorded duration. The input review retains this metadata distinction;
the declared476-frame domain was not trimmed using container duration.
Camera2's inherited assessed stereo-layout diagnostic remains in its source
record; this unit used its stored PNGs and did not re-decode Camera2 video.

## Claim strength, alternatives and next test

| Claim | Layer / assessment | Strongest limitation or falsifier |
|---|---|---|
| The fixed algorithm selects the listed minima. | Derived numerical result, A within the fixed input/method contract; independently replayed. | A source-pin, arithmetic, region or summary discrepancy. |
| The selected frames are useful candidates for paired content review. | Inference, C: method/representation dependent. | Poor scene agreement, unexamined alternatives, blending or temporal resampling. |
| The minima identify unique original exposures or an unedited physical clock. | Unsupported by this test, E. | Requires independent processing/exposure provenance, not a lower residual. |
| The points exist in the alternate copy, or are physical emissions. | Not tested here / underdetermined, D. | Paired observations can test appearance; physical provenance requires additional evidence. |

The strongest objection is shared processed ancestry: neighboring exposures,
field blending, interpolation or compression can create a best numerical match
without preserving a unique original exposure. A background scene can agree
while a transient differs; a tiny point can be altered by a different raster.
Conversely, this does not make comparison useless: selection by other scene
features supplies a non-point-based, inspectable set for the next test.

Next, declare a paired qualitative review of the frozen complete shortlist
union **306–321 and352–361** and the six Camera2 queries. Keep native unaltered
representations and all per-query associations, examine neighboring alternatives,
and freeze separate readers' descriptions before comparison. Determine whether
the upright region is comparably inspectable; absence in a poorer, unmatched
or blended representation is not physical absence. This proposal is not a
completed paired review or an approved quantitative light measurement.

Unknown ancestry means any agreement would at most establish cross-copy
appearance agreement, not an independent historical light source or exclusion
of upstream artifacts. The original-source/scene documentary route remains
open. Broader Luna reevaluation, human gates and structural/scientific work
remain incomplete; no legal, raw-source, accepted-engine or external change
is made by this result.
