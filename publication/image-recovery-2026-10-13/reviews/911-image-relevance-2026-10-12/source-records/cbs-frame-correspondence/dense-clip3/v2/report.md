# Full Clip 3 comparison: a stronger candidate, not exact-exposure proof

2026-10-04 UTC. **Frame 127 is now the leading changing-detail candidate for
report Figure 5-143 under the unchanged method.** It was absent from the nine-
frame pilot. All 189 frames have now been compared, twice, in all three declared
representations. This improves source localization; it does not determine fire
severity, window material, temperature or collapse cause.

Numerical execution, separate artifact audit, root audit rerun, direct-score
checking and the fixed native-image review are complete. The
[separate synthesis critique](synthesis-review.md) found no material correction;
its audit-chronology clarification is incorporated. This is completion of this
bounded source-comparison lane, not the investigation or human acceptance.

## What changed from the pilot

The [pilot](../../report.md) could only identify several similar geometry fits,
with frame 141 leading its available changing-detail scores. The complete search
finds a distinctly stronger changing-detail candidate at **127**, followed by
**128**, in every arm. Stationary geometry alone still cannot identify a moment:
its winners differ across arms and many frames score almost equally well.

| Representation | Best static score / index | Best dynamic score / index | Dynamic runner-up / index | Frames with an available dynamic score |
| --- | --- | --- | --- | ---: |
| Full stored raster | 0.991223 / 187 | 0.954733 / 127 | 0.940214 / 128 | 121 / 189 |
| Even measured rows | 0.990832 / 187 | 0.965416 / 127 | 0.932373 / 128 | 121 / 189 |
| Odd measured rows | 0.989870 / 135 | 0.948912 / 127 | 0.943462 / 128 | 119 / 189 |

Dynamic means the fixed changing-image region evaluated at **each frame's best
static transform**, without refitting. It includes architecture/background and
smoke as well as bright flame-like detail; it is not a pure fire mask. These
correlation scores are not probabilities or confidence levels. Full/even/odd
are correlated representations of the same recording, not independent cameras.

At the predefined score-distance thresholds 0.005, 0.01 and 0.02, the full-arm
dynamic sets are respectively `{127}`, `{127}`, and `{127,128}`. The even-row
sets contain only 127 at all three thresholds; the odd-row sets are `{127}`,
`{127,128}`, and `{127,128}`. These are descriptive sensitivity sets, not
statistical confidence intervals. All six complete rankings and all eighteen
sets are retained in [the aggregate](aggregate-a/summary.json).

There are important counterweights to a unique-exposure conclusion:

- The full-arm static 0.005-near-best set contains **53 frames**; even and odd
  contain 46 and 62. Repeated stationary architecture is weak temporal evidence.
- Full-arm static leader 187 has only about **89.4% static coverage**. Its dynamic
  coverage is **79.2%**, below the fixed 85% gate. It is untested on changing
  detail, not a demonstrated mismatch. Frame 127 has 100% static and about
  98.7% dynamic coverage at its selected transform in every arm.
- **68 full/even and 70 odd** dynamic candidates are unavailable, all because
  coverage fails. Therefore “leads” means among valid scores under this method,
  not proof against every untestable candidate. Coverage varies between fits.
- The published reference's intensity adjustment, field treatment and complete
  processing history remain unresolved. The fixed transform family is limited;
  matching under it does not reconstruct the entire historical image pipeline.
- The prior-informed reference and scenes are not clean holdouts. No false-match
  probability is calibrated. Pilot cross-view controls remain preserved but were
  not expanded to dense cross-view comparisons in this paired-only lane.
  Searching more frames also creates more opportunities for a high maximum;
  the increase over the pilot is not by itself calibrated exact-identity evidence.

## Verification and actual coverage

Two separately executed extractions passed the new diagnostic version and produced
189 identical frame records. The [extraction audit](extraction-review.md) checked
378 new PNG/RGB pairs plus nine pilot pairs, every PTS/metadata join, and the
preserved earlier refusal. Decoder logs differed only in runtime addresses,
output paths and processing speed. This is reproducibility of held bytes, not
independent camera custody or a second historical source.

Each scoring pass completed **567 comparisons**: 189 frames × three arms.
The combined aggregate reconciled all 567 material records and score/coverage
surfaces across repeats, all masks, nine pilot-frame identities and 27 paired
pilot comparisons. No chunk rankings were inspected before that aggregate.

The [independent artifact audit](artifact-review.md), independently rerun by
root, checked both complete passes: **38,343,942 saved cells**, including
29,573,586 finite scores, all 2268 retained transforms across repeats, six global
groups, eighteen near-best sets and 1674 unchanged input hashes. Its rankings
are reconstructed from the saved surfaces; it does not independently recompute
all correlation cells. Its floating-point coverage-check repair, made before
the first historical artifact-audit execution, is disclosed; no scientific
method or saved result was changed.

Root's separate direct-sum calculation reproduced **1856 finite scores and
412 unavailable-score decisions** across all **1134 retained transforms**;
maximum numerical difference was **6.30e-14**, below the declared 1e-9 tolerance.
It checks selected transforms rather than every correlation cell, and shares
Pillow/NumPy. [Exact commands, controls and receipts](execution.md) distinguish
fresh 16 supervisor and twice-passed 70 adapter controls from inherited prior
checks. All nine historical jobs completed within the unchanged monitored limits.

This lane adds 180 previously unscored Clip 3 frames. Together with the pilot's
nine Clip 7 samples, **198 of the declared 1317 distinct frames** are now scored;
**1119 remain unscored**, all in Clip 7. The two runs and three representations
do not multiply the number of distinct source frames.

## Fixed native-image check

After the artifact checks, root inspected the full reference once and all six
unique shortlisted native frames once in ascending order: **127, 128, 135, 156,
186, 187**. [The observation record](root-observations.md) preserves exact files,
hashes, actual viewing scope and the scores-known, nonblind status. No additional
frame, crop, enhancement, field rendering or audio was viewed.

The facade/corner and opening/grid arrangement is recognizable throughout the
shortlist. The broad changing bright/dark pattern at 127–128 is consistent with
the reference; later candidates retain geometry while the bright/veiled profile
and framing differ. The reference and footage visibly differ in contrast,
color, sharpness and overlaid content. Native softness, horizontal line structure
and concealed lower context prevent certification of an identical fine transient
pattern or a particular original field. This descriptive check is compatible
with the computational candidate but is not an independent blind confirmation.

## Interpretation and next discriminating work

The new result strengthens the source-candidate relationship between the held
Clip 3 and Figure 5-143, beyond matching stationary architecture. The strongest
objection remains that similar changing imagery, unknown reference processing,
interlaced acquisition and untested coverage can prevent exact exposure identity
even when a particular index wins reproducibly. A high score does not establish
which original field or exposure produced the report still or authenticate its
absolute time. No inference about exaggerated fire assumptions follows yet.

The next finite task is the full **1128-frame Clip 7** paired comparison against
Figure 5-142, using the existing fixed method and a separately reviewed resource
schedule. Retain this result and its uncertainty; do not retune masks to make
127 win more strongly. Exact exposure or consequential physical use would also
need an explicit original-field/processing-lineage test and the actual human
review required by the charter. The current result does not clear those gates.

All material remains research-only in this investigation worktree. The original
refused extraction, source files, masks and comparator ±1-native-y-pixel human
record are unchanged. No accepted Sherlock/Faraday result, matrix save, legal
promotion, external disclosure, staging, commit or push occurred. Generic local
parser lessons were deduplicated under SFB-002; the archived feedback destination
remains unresolved. Full goal active and incomplete.
