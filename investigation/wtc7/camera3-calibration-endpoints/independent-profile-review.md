# Independent profile arithmetic and bounded report review

## Disposition and scope

**Numerical PASS; report interpretation qualified as below.** The independent
calculation reproduces all declared source-pixel sums, means, lag correlations,
undefined control outcomes and maximizing-lag sets. No producer arithmetic,
dependency-pin or coverage failure was found. A coordinate-description
imprecision in the frozen declaration and first reviewed report is recorded
below; it does not alter the selected pixels or results.

This reviewer read `PROFILE-DECLARATION.md` and `profile_rows.py` completely
before examining profile-result values. The independent implementation does
not import the producer, use its numerical routines, or use its reported
maxima as an oracle. It reads only the three already preserved native PNGs
and the bounded declarations/receipts/dependencies. No source decode, image
interpretation, new production material, historical trajectory fit, physical
acceleration, external transfer or causal assessment occurred in this review.

The declaration is exploratory, not blind: the earlier observer's coarse
14–16-cycle assessment and root's endpoint enlargement viewing were already
known when this strip and analysis were selected. Agreement does not turn
that earlier assessment into an independently validated floor count.

## Frozen subjects and execution

| Artifact | SHA-256 |
|---|---|
| `PROFILE-DECLARATION.md` | `6eaea06dcc96e3d429f1ab845ffe02ffea21329c6845e156ea58c1339760de71` |
| `profile_rows.py` | `b28ace99e0c532937ddfcf247f6724ad9eea8d4533f035fd20b4b43bf4c65ca5` |
| `profile01.json` | `6cf5b643c0705f6ca95f2ddf2fb8e61e2eee891afeba806762f15c2b877c645e` |
| Independent `verify_profile.py` | `ccce8646eb4ad26f6f08d3534ec5423d9c6a7e449edec6f578dcb9d9b206590b` |
| `independent-profile01.json` | `663d223bbe97d1809e48756e60162c3df899d53c966d160bafa0ea4a2a160f1f` |
| Earlier `independent-products.md` | `431be1b22c7d3a2b77e6597a736872b4aba12b832690a95f56c001602792061e` |
| First fully reviewed `report.md` | `dc9210ef904ee99e98159b9c834f674789b6d95a8a2b7dba427bbb9394e16143` |

Executed in the dedicated investigation worktree:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera3-calibration-endpoints/verify_profile.py --out independent-profile01.json
```

Observed exit status: **0**, receipt status `pass`. Python 3.13.7 and Pillow
12.0.0 were used; Pillow only decodes the preserved PNG pixels. The verifier
checks 13 distinct consumed file/runtime pins before and after its work,
including the three native PNGs, its own code and all six producer-declared
dependency names. The producer's receipt contains end-of-run dependency
hashes; this review does not invent producer before/after checks that its
code did not perform. Current dependency agreement and the independent
run's before/after checks both pass.

Root subsequently produced `independent-profile-root01.json`. A direct
whole-JSON comparison found only the `command` field different; every other
field, including all independent values and pins, was equal. This reviewer
did not launch that root execution. A separate AST parse of the frozen
independent verifier succeeded. No original/frozen subject was edited.

## Independent arithmetic and actual coverage

The tolerance was fixed and communicated **before historical result values
were opened**: absolute correlation difference at most `1e-12`, exact
maximizing-lag list agreement using the declaration's `1e-12` tie tolerance,
and the declared norm cutoff `1e-10` intensity units. No ranking-dependent
tolerance adjustment was made.

For each native image, integer pixel bytes independently supply the 183 sums
over columns 402–411. Means are exact rational sums divided by ten. Ordinary
least-squares detrending uses the closed-form centered slope
`sum((x-xbar)*(y-ybar))/sum((x-xbar)^2)`, not the producer's least-squares
solver. Each lag's two overlap vectors are separately centered. Covariance
and variances use exact rational arithmetic, with a 60-digit Decimal square
root only for normalization. The norm cutoff is checked through the exact
squared threshold `1e-20`. Synthetic cosine inputs use an independently
generated scalar cosine sequence; constant and affine-ramp controls use
exact inputs. All independent correlations, overlap norms and discrepancies
are retained in the receipt, not just the favorable maxima.

| Verified quantity | Coverage and outcome |
|---|---|
| Native images | 3; indices 138, 141 and 168; pinned PNG files and decoded grayscale hashes |
| Integer row sums / row means | 549 / 549; all matched |
| Historical method/window results | 18 = 3 frames × 3 windows × 2 methods |
| Historical lag-correlation cells | 198 = 18 × 11 lags; all defined and matched |
| Synthetic control cases / cells | 9 / 99; all matched |
| Known-period controls | Periods 12, 13 and 14 under both methods; each maximizes at its true tested period |
| Undefined controls | Constant raw, constant detrended and affine ramp detrended; all 33 lag cells remain undefined and their maximum sets empty |
| Historical maximizing sets | All 18 are uniquely `[13]` within the tested integer lags 8–18 |

The largest absolute discrepancy across all defined historical and synthetic
correlations was approximately `1.192429e-15`, well inside the predeclared
`1e-12` limit. The smallest historical overlap norm was approximately
`60.944429`, far above the undefined cutoff. Independent lag-13 values range
from `0.9280163820216107` to `0.9716734611616163`. The smallest margin between
a historical maximum and its next-best tested lag is approximately
`0.136403706`; these outcomes are not borderline numerical ties.

## Refinement products and coordinate qualification

The earlier frozen [independent product review](independent-products.md)
already checks all twelve refinement PNGs: six unmarked nearest-neighbor
patches and six separately marked RGB query displays, across all three
native frames. It independently checked every unmarked output pixel against
12× source-pixel repetition (793,152 pixels total), and every overlay pixel
against an independently constructed cross mask. Each overlay has 104 red
pixels, with the central query pixel unpainted. All source/product pins and
declared identities matched. No image interpretation was part of that check.

The declared pixel-centre convention maps a source coordinate `x` in a
12× crop beginning at `x0` to `12*(x-x0)+5.5`, and likewise for `y`. Exact
binary64-coordinate arithmetic reproduced both declared display queries and
their inverse mapping. This checks the new analytical display convention,
**not the historical Tracker coordinate convention or a physical endpoint**.
The original run01 context crops remain unlabelled, despite the protocol's
coordinate-labelled-aid wording; exact metadata mappings were present. That
scoped presentation deviation is preserved, not retrospectively erased.

Another wording imprecision appears in the frozen profile declaration and
first reviewed report: the strip is said to exclude "both query
neighborhoods." It excludes both exact query locations, but overlaps the
upper refinement patch in `[402,202,412,210)` and the lower refinement patch
in `[402,377,412,385)`—80 native pixels in each intersection. The precise
report wording should be "excluding both exact query locations." The
declaration and computed strip remain frozen; this is a description
qualification, not evidence that the selected array differs from its box.

## Bounded report numerical and inferential review

The report identified above was read in full. Independently recomputing its
dimensional comparisons from the saved rounded coordinates gives vertical
separation `390.7276736493937 - 196.24035281146615 = 194.48732083792755`
pixels, and division by 13 gives `14.960563141379…` cycles. This is the
vertical component, not the slightly longer Euclidean tape span; the report
correctly distinguishes fixed-column repetition from a slanted endpoint
pair. The many saved coordinate digits do not imply that corresponding
architectural features were localized with that precision.

One assumed 12.75-ft interval is exactly 3.8862 m under the stated conversion.
Fourteen, fifteen and sixteen such intervals are respectively **54.4068 m,
58.2930 m and 62.1792 m**. With the same image span, their scale ratios are
exactly **14/15, 1 and 16/15**. An otherwise fixed conditional physical
acceleration estimate is linear in that length scale, so the stated
acceleration-scaling consequence follows. These illustrative alternatives
are not an observed ±6.7% uncertainty, probability distribution or evidence
that 14 or 16 is preferable to 15.

The numerical and inferential presentation fairly retains affirmative
evidence: strong repeated lag-13 correlations are positive support for an
approximately fifteen-cycle reading of the given span. Missing endpoint
identity does not make that evidence disappear or demonstrate contrivance.
Conversely, a maximum over integer lags 8–18 is not an exact or global
fundamental period, an independent count of physical storeys, a recovery of
the occluded endpoint, or a historical perspective-error bound. Similar
upper/lower maximizing lags do not prove affine projection. The report makes
these distinctions and correctly does not treat eighteen reused-window
results as eighteen independent evidence sources or correlations as
probabilities. No source expectation was used to calibrate toward g.

The source-document/floor-pair interpretation and observers' visual judgments
were assigned separate review; this mathematical review does not claim an
independent drawing survey or image reading. The report's proposal to test
the public trajectory conditionally is a future bounded scientific step,
not a result already obtained here or authority to transmit/export private
fields. There is no causal-ranking upgrade or force inference in this unit.

**Report disposition:** numerical and conditional-inference PASS, subject to
the specific query-neighborhood wording correction above. No other blocking
mathematical or inferential defect was found in the stated scope.

## Final correction confirmation

The corrected report SHA-256 is
`00d7e2a884d5b063a1a1ad14817e7b6954a57c181e4ec018c9e852ef4b88da43`.
The exact replacement is `excluding both query neighborhoods.` →
`excluding both exact query locations.` It occurs once. Reversing only that
replacement in memory reproduces the prior reviewed report hash
`dc9210ef904ee99e98159b9c834f674789b6d95a8a2b7dba427bbb9394e16143`;
there are no other report byte changes. The comparison exited 0.

**Final report disposition: PASS within the bounded numerical/inferential
scope above.** The frozen declaration's neighborhood wording imprecision
and the earlier report hash remain recorded as history. This confirmation
introduced no new calculation, source inspection or scientific inference.
