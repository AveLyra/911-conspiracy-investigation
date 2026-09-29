# Peskin footage and NIST fire-figure correspondence

Research-only Q01/Q02 follow-up. **Full numerical pass, reproduction and bounded
visual review completed.** The investigation charter is unchanged.

## Question and source boundary

Can NIST NCSTAR 1-9 Figures 5-148 and 5-149 be associated with particular frames
in the already admitted Peskin access copy? The earlier review located the same
scene/source family but did not authenticate an exact frame, original camera
clock or compilation edit map. This unit tests that narrower correspondence
question; it is not a new structural or thermal calculation.

The video is the preserved 696,711,067-byte `peskin-commons-resumed.webm`, SHA256
`0f438006c27e3059e7a5a480d4a7ee5382c5a136945c2a0120e583e3456f324d`.
It is a joined access copy, not the original camera tapes or the separately
identified original clips. Stored geometry is 1620x1080, SAR 8:9, display 4:3;
the analysis retains stored pixels and source PTS in timebase 1/1000.

The target JPEG codestreams are `A-370a6ef2789a` (Figure 5-148) and
`A-e43e4088a4a2` (Figure 5-149), both 720x478. The full report page is physical
278 / printed 234. Their source captions disclose intensity adjustment and
added floor/column labels. Those labels and asserted clock times are not
independent image-match evidence. Target/full-page identity and actual visual
coverage are recorded in the [target review](independent-target-review.md).
Primary source lineage remains the earlier
[Peskin report](/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-originals/peskin/report.md)
and [validation](/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-originals/peskin/validation.md).

## Declared method and preserved corrections

[PROTOCOL](PROTOCOL.md) and [METHOD-01](METHOD-01.md) fix the initial 32 one-second
samples and the complete candidate interval PTS [2502,2534) seconds. Images are
mapped to a 180x120 numerical grid, not physically aspect-calibrated. Foreground
registration searches 13 scales and integer translations up to 25 grid pixels
per axis. Every static score/overlap surface is retained; each frame keeps its
two best static geometries. The separate dynamic score is evaluated at the
best static fit, never used to refit it. Dynamic regions contain windows/haze
as well as flame, so they are not pure-flame or temperature measurements.

The initial screen preserves 32 samples / 64 comparisons. Its strongest
coarse-layout leads are source bin 2521 for Figure 5-148 and 2524 for Figure
5-149, supported by the separately frozen [ten-frame visual review](initial-candidate-review.md).
That reviewer saw all ten shortlisted full frames and both targets before
reading numerical scores. Selection was still producer-derived and this was
not a blind or independent-source test.

[DENSE-01](DENSE-01.md) retains the full interval rather than refining only the
favorable seconds. [Execution safeguards](DENSE-GATES-01.md) tightened version,
storage, timestamp and prior-run reproduction checks. The first synthetic
parser version accepted a nonfinite displayed timestamp; its 21/22 result and
code snapshot remain preserved. The corrected version passed 63/63 controls,
independently replayed. The original mathematical core passed 11 controls and
the separately implemented direct-correlation comparison described in
[method review](method-review.md); these verify numerical behavior, not exposure.

The first dense segment passed, but the second stopped 25 in-scope frames short
and failed its exact probe/filter PTS-list gate. Its partial scores for 215 frames
are retained in `dense01`, excluded from accepted aggregate coverage. The
[continuation](DENSE-CONTINUATION-02.md) changes only the decoder read allowance
and fresh run slots/budgets, preserving the selected interval and matching
mathematics. The continuation passed 100/100 synthetic checks and an independent
[scoped review](dense-method-review-03.md). It is not a historical footage defect.

## Full-interval results

All 959 decoded frames in the declared interval were compared with both targets:
1,918 target-frame comparisons. Each of four segments matches its independently
invoked probe PTS list and eight existing sample-image pixel hashes. Exact
same-code reproduction compares all 1,918 score/overlap array pairs, complete
frame/result rows and all 59 saved native PNGs. The failed partial run is not
part of these counts. See [verification](validation.md),
[complete summary](reproduced-summary.json) and
[independent arithmetic review](independent-result-review.md).

Both declared metrics select the same leader for each target:

| Target | Leading access-copy PTS | Foreground correlation | Post-fit dynamic-region correlation |
|---|---:|---:|---:|
| Figure 5-148 | 2521.133 s | 0.997182 | 0.979408 |
| Figure 5-149 | 2524.203 s | 0.991739 | 0.986677 |

Both leaders use working-grid scale 1 and zero translation. These values are
descriptive scores, not match probabilities. The leaders are 3.070 presentation
seconds apart in this copy; that arithmetic is not an authenticated exposure
interval or proof of the report's historical clocks.

The predeclared dynamic-score bands for Figure 5-148 contain 3, 7 and 10 frames
within 0.005, 0.01 and 0.02 of its best score. The widest of those sets has two
disconnected groups spanning 2521.066–2521.400 s. Figure 5-149 retains only the
2524.203 s frame in each of those dynamic bands. Static bands are broader:
49 and 41 frames respectively within 0.02 of their static leaders. The full
disconnected sets are retained; these envelopes are neither confidence limits
nor exhaustive sets under every plausible image-generation model.

The fixed-fit regional check covers seven Figure 5-148 and five Figure 5-149
candidate-target pairs, all 86 declared diagnostics. For the Figure 5-149
leader, its three separate bright-fire-region correlations are 0.989518,
0.982473 and 0.981589; its two background structural regions are 0.988144 and
0.866490. It leads all six regional diagnostics among the five selected
alternatives. For Figure 5-148, the leader's three bright-region values are
0.961853, 0.965393 and 0.901251, and its four background regions range from
0.819278 to 0.961831. Other shortlisted frames perform better in several
individual Figure 5-148 regions. Thus the aggregate leader is not a universal
regional winner, and background detail remains imperfect.

The separate [dense visual review](dense-candidate-review.md) inspected all
12 globally shortlisted native images and both complete targets. It finds
strong multi-feature scene/composition correspondence for T148's indices
91–101 and T149's 185–187, without uniquely identifying one original exposure.
T148's index 77 is notably reframed, with an upper strong-fire row visible
at the top that is absent from the target's full composition. A different crop
is not excluded merely by that mismatch. Neighboring flame lobes, brightness,
blur and small framing differences remain unresolved.

This dense review is not wholly rank-blind: after viewing both targets and
the first five candidates, but before freezing any qualitative checkpoint,
the reviewer received root's score-aware leading-image identities and favorable
visual observations. The remaining seven images were viewed with that context.
The reviewer did not read numerical dense scores or regional results before
freezing the note. Actual coverage and disclosure are preserved; neither a
clean holdout nor a separately frozen pre-hint interpretation is claimed.

Root viewed both complete leading native images and both complete targets after
seeing the scores. Their foreground layout, background window bands and
spatially separated fire features show substantial agreement. The Figure 5-149
leader reproduces the clipped left bright feature and separated central/right
groups particularly well at scene level. Report/source contrast and fine
feature appearance differ, so this observation does not independently establish
pixel identity or an original exposure. Root's initial full-page/target and
three one-second candidate views are additional disclosed prior familiarity,
not unused comparison evidence.

## Interpretation and limitations

The [shortlist-review declaration](CANDIDATE-REVIEW-01.md) keeps global top-four
static/dynamic choices and the earlier descriptive score bands. It adds
background and spatially separated dynamic checks at the fixed foreground fit,
using regions chosen before dense candidate inspection. Foreground alignment
alone cannot authenticate the WTC 7 background plane. Full-frame visual review,
regional residuals, neighboring candidates, repeated geometry, blur, intensity
adjustment and intermediate generations must remain visible.

Even a high score is conditional on the transform family, masks, resampling
and source generation. The selected score bands are not confidence intervals;
failure to identify an exact exposure does not prove an erroneous caption or
invented fire. An access-copy PTS difference is not an authenticated historical
clock interval. Camera originals and edit/clock records remain separate leads.

A subsequent, separately declared photometric/visibility test can assess
which feature observations survive intensity adjustment, resampling, clipping
and neighboring-exposure alternatives. It cannot recover unseen interior fire
extent or steel temperature from these RGB images. This unit does not carry
out that next test.

## Causal and record boundaries

The positive finding is narrower than a collapse explanation: these two report
illustrations have strong counterparts for their depicted fire arrangements
in the independently accessed copy of the same source family. This comparison
does not support a claim that those arrangements were invented. Nor does it
test whether a modeled interior fire history was exaggerated.

No fire temperature, duration of interior exposure, member failure, demolition
mechanism, actor or intent follows from this image-matching unit. It adds no
independent source family and changes no causal ranking by itself. The broader
investigation remains active and incomplete. The supplementary model production
continues to be included under its existing source IDs and audits; this unit
neither reinstates blanket model-unavailability claims nor validates that model.

Main/raw/legal records remain untouched. No new acquisition, archive access,
solver, bridge, transmission, canonical promotion, commit or push. Generic
measurement lessons are deduplicated locally under SFB-002/SFB-004; delivery
remains pending the archived Sherlock destination's routing decision.
