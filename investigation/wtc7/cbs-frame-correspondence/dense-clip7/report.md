# Full Clip 7 comparison identifies closer Figure 5-142 candidates

2026-10-04 UTC. **Frame 538, followed by 539, is the strongest changing-detail
candidate for Figure 5-142 in all three fixed representations.** Neither was
in the nine-frame pilot, which favored 564. The complete 1128-frame comparison
and repeat have passed their artifact and retained-score checks; the six
predefined native candidates were inspected once each.

This strengthens source localization. It does **not** establish an exact
original exposure/field, historical window condition, exaggerated fire input,
steel temperature or collapse mechanism. All material remains working research.
The [separate synthesis critique](synthesis-review.md) found no material
correction. Its reviewer was separate from this synthesis/native reading but
had authored the adapter; it is not fully independent implementation review,
another visual observation or expert certification. This closes the bounded
source-comparison work, not the full investigation or actual-human acceptance.

## What the complete search changed

The [earlier pilot](../report.md) identified 564 from nine samples. Under the
unchanged method, the full-raster changing-region score rises from **0.846360
at 564** to **0.981219 at 538**. The advance is a stronger candidate within a
much more complete search, not a calibrated increase in identity probability.
The original pilot scores and all less-favorable results remain preserved.

| Representation | Best static score / index | Best dynamic score / index | Dynamic runner-up / index | Frames with an available dynamic score |
| --- | --- | --- | --- | ---: |
| Full stored raster | 0.957651 / 544 | 0.981219 / 538 | 0.979030 / 539 | 879 / 1128 |
| Even measured rows | 0.958560 / 540 | 0.979719 / 538 | 0.977014 / 539 | 880 / 1128 |
| Odd measured rows | 0.959189 / 544 | 0.981107 / 538 | 0.979238 / 539 | 884 / 1128 |

“Dynamic” is the fixed changing-image mask evaluated at **each frame's best
static transform**, without refitting that region or choosing the better of
the two retained transforms. The mask contains stationary background/architecture
as well as changing plume and bright detail; it is not a pure flame mask.
All three representations come from the same stored frames and are correlated.
Scores are correlations, not confidence levels, calibrated fire measurements
or independent historical corroboration.

At the predefined 0.005 score-distance threshold, the full and odd dynamic sets
are `{538,539}`; the even set is `{537,538,539}`. At 0.01 all three contain
`{537,538,539,540}`, and at 0.02 all contain `{536,537,538,539,540,541}`.
These are descriptive sensitivity sets, not statistical confidence intervals.
The complete six rankings and eighteen sets are retained in
[the aggregate summary](aggregate-a/summary.json). The view shortlist was the
predefined union of top-two static and top-two dynamic candidates, not every
near-best frame; no extra image was added after seeing the scores.

## Counterweights and uncertainty

All 1128 frames have valid static fits, but stationary geometry does not select
the same index as changing detail. At 0.005 from the static best there are eight
full-arm, seven even-arm and three odd-arm frames. Close alternatives survive;
there is no demonstrated unique-exposure separation between 538 and 539.

**249 full, 248 even and 244 odd candidates lack a dynamic score at their best
static fit**, all because they fail the fixed 85% mask-coverage rule. Those
frames are untested on that metric, not demonstrated mismatches. All six viewed
candidates have complete static and dynamic mask coverage at their selected
fits, but mask coverage is not complete building/facade visibility.

The result remains conditional on the fixed, discrete scale/translation search,
resampling and masks. Dynamic ranking inherits each candidate's selected static
alignment; it is not a direct raw-pixel measure of changing fire. No rotation,
shear, local warp, enhancement, additional mask or post-result retuning was used.
Unknown reference processing, measured-row/interlaced representation, native
softness and broadcast overlays remain limitations. Prior reference/pilot
familiarity is disclosed; these are not clean holdouts. Searching more frames
creates more opportunities for a high maximum, and no false-match probability
has been calibrated. The pilot's cross-view controls remain, but this dense
extension is paired-only, not a new exhaustive cross-view control study.

The strongest alternative to exact-exposure identity is a nearby exposure or
closely related recording sharing the architecture and a similar plume/bright
pattern, with processing/obscuration concealing distinguishing detail. A higher
score alone does not defeat that alternative. Conversely, the result is more
informative than generic architectural similarity: the predefined changing
region also localizes the leading valid candidates to a small neighboring set.

## Native image observations

After both artifact audits and root's direct-score check passed, root viewed
the unchanged full reference once and the six unique native candidates once,
in order: **538, 539, 540, 541, 543, 544**. The
[observation record](root-observations.md) preserves paths, hashes, scope and
individual limitations. No extra frame, crop, field rendering, enhancement or
audio was inspected. The separate artifact reviewer did not view these images;
this is one scores-known, nonblind computational-agent reading, not independent
human or expert confirmation.

The sign/support and foreground facade, main corner and rectangular/grid
regions, upper-right overhang, dark upper plume, lighter lower plume and bright
corner patch have a compatible broad arrangement. No obvious scene-order
contradiction is resolved in the shortlist. Fine transient boundaries are too
soft to certify an exact original field or confidently distinguish 538 from
539 by this reading.

The report image is visibly darker/more contrasty in important regions, with
more conspicuous orange band detail. The native video is softer/paler and its
lower broadcast banner hides the ONE WAY sign and context exposed in the report
image. That is compatible with the disclosed intensity adjustment but does not
verify the actual transformation or prove fabrication. No hidden content was
reconstructed, and brightness was not converted into heat, steel temperature,
glazing condition or fire-area measurements.

## Verification and actual coverage

The [frozen plan](PLAN.md) selected all 1128 indices and the unchanged numerical
method before new historical scoring. Separate method/implementation review,
corrected author and serial root **111-test** suites, and 34 supplementary
artifact-checker controls preceded historical execution. Earlier code/control
records and root's incomplete concurrent synthetic run remain preserved. No
test acceptance condition or historical score was relaxed to obtain a pass.

Two complete extractions produced identical frame records. Root's
[extraction review](extraction-review.md) checked all 2256 fresh plus nine pilot
PNG/RGB pairs and their source/metadata joins. All **36 scoring jobs** completed
serially; their **3384 comparisons per pass** reconciled in one complete
aggregate, including every saved surface, mask and all 27 paired pilot records.
No partial-run ranking or shortlist was used.

The [separate artifact audit](artifact-review.md) and root's independent rerun
each checked **228,846,384 saved static-score cells**, including 125,383,968
finite cells, all 13,536 retained transforms across repeats, six global groups,
eighteen near-best sets, 36 complete input maps and 9497 unchanged input hashes.
Every chunk contains all 2349 independently enumerated required dependencies;
an incomplete map cannot be hidden by a complete union. All material output
fields of the two audit results agree; only their contemporaneous free-space
snapshots differ. These audits sort saved surfaces and reconstruct coverage,
not independently recompute correlation at every lattice point.

Root's [separate direct-sum calculation](direct-verification.json) reproduced
**12,062 finite scores and 1474 unavailable-score decisions** at every one of
the **6768 retained transforms** in the aggregate's first-pass records. Maximum
difference was **2.61×10⁻¹⁴**, below the declared 10⁻⁹ tolerance. It uses separate
mask indexing and direct sums but shares Pillow/NumPy; it is selected-transform
verification, not a new decoder, full independent correlation surface or source
authentication. All 1140 inputs pinned by that check were unchanged at its end.

All **39 historical jobs** completed within their recorded resource limits.
The 36 score jobs took about 74.37–85.66 seconds each; aggregation took 68.83
seconds. Exact commands, preserved failures, resource observations, output
hashes and check scopes are in [the execution record](execution.md). Sampled
supervision is not a hard OS quota or an independent reconstruction of a
continuous resource trace.

Together with the [completed 189-frame Clip 3 lane](../dense-clip3/v2/report.md),
the declared **1317-frame paired population is now computationally covered**.
This unit adds the 1119 Clip 7 frames missing from the accepted pre-follow-up
coverage. It does not mean every frame was visually inspected, every dynamic
comparison was available, all eight catalogue clips were densely searched, or
the full investigation is complete. Repeats and representation arms do not
multiply the number of distinct source frames.
Here distinct means source positions, not authenticated unique historical
exposures or independent recordings.

## Evidence strength and the next discriminating test

| Claim | Layer and scoped strength | What would weaken or sharpen it |
| --- | --- | --- |
| The declared computation gives 538 then 539 the highest available changing-region scores in all three arms. | Derived, A within the pinned method; repeats and retained-score arithmetic agree. | A reproducible input, population, ranking or arithmetic error would overturn it. A different justified method would be a separately declared sensitivity test, not a replacement result. |
| Held Clip 7 supplies a strong scene/detail candidate for Figure 5-142. | Inferred, B; stronger than the sparse pilot, with a compatible bounded native reading. | Incompatible distinctive foreground/transient detail or a stronger authenticated competing source would weaken it. Shared source origin is not independently proved by catalogue labels. |
| Frame 538 is the exact original exposure/field used to make the report image. | Underdetermined, D. | A source-identifier/frame/field/processing chain or a separately tested, constrained derivation that resolves the neighboring alternatives would materially sharpen it. |
| This result establishes exaggerated fire inputs, validates NIST's structural sequence, or discriminates deliberate support removal. | Not established by this test. | Matched observations must be joined to specific model inputs and physical predictions; the source-candidate score supplies none of those consequences by itself. |

The inspected existing records identify the Figure 5-142 report JPEG and held
Clip 7 catalogue object, but no exact camera-to-report derivation was recovered
in that bounded check. The [report-attribution entry](../../fire-coverage-batch3/source-attributions.json)
discloses intensity adjustments and added labels; its 3:55–4:04 p.m. estimate
is not an independently authenticated clock. The exact remaining documentary
discriminator is the **Figure 5-142 still-generation/export record**, connecting
an original source identifier to frame/timecode/field and processing steps,
ideally with the unannotated still. Absence from the inspected records is not
proof of nonexistence, withholding, destruction or intent. Do not fill the gap
through unconstrained fitting and call it historical reproduction.

A useful physical comparison remains possible only at its own demonstrated
resolution and scope. The [geometry crosswalk](../../nist-acoustic-detectability/window-geometry-crosswalk-2026-09-28.md)
locates the northeast facade regions but does not establish the exact response-
model layout/glazing inputs. The [human response](../../nist-acoustic-detectability/window-state-human-review-user-2026-09-29.md)
marks 141-N12 and 143-N8 inspected, but not 142-N12; filled impression fields
are not a completed inspection or diagnostic pane classification. Floor 8
cannot silently stand in for Floor 12, and an earlier still cannot test
new collapse-time window loss. No completed same-window/model-input comparison
or newly calibrated acoustic detection opportunity follows from this lane.

Accordingly, **no collapse-cause ranking changes from this result alone**.
The next work should target the specific lineage/matched-observation gap rather
than rerun the same deterministic search or retune it to improve the winner.
Other charter work packages remain in scope. Original annotations, the separate
comparator ±1-pixel human record and all actual-human/matrix-save gates remain
unchanged. No legal/main edit, accepted Sherlock/Faraday finding, external
disclosure, staging, commit or push occurred. Generic implementation lessons
are locally deduplicated under SFB-005; archived-destination routing remains
unresolved, not a claimed delivery or product fix.
