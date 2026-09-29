# Fire-image visibility calibration, version 2 pilot

2026-09-15. Research-only method calibration under the unchanged investigation
charter. This is a new, deliberately selected calibration sample, not a repair
of the frozen v1 labels or an independent historical validation set.

## Purpose and preserved inputs

Separate candidate identity, displayed-appearance opportunity, incidental
cautions, decisive exclusions and appearance. The v1 program treated every
nonempty objection/caution field as a veto. New fields must express the actual
decision; old objections must not simply be erased or auto-reclassified.

Read-only source directory:
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-annotation/`.
Geometry: `geometry-main-v1.json`, SHA-256
`d7c593a6d7ccad9f1f403bf0ee8a2bfe5afd6d0c6e5dd446c3602e6a5e590a13`.
The unchanged polygons locate image regions, not authenticated window IDs.

Images, shown complete at native resolution without new enhancement:

- `assets/run-01/images/A-e43e4088a4a2.jpg`, 720×478, SHA-256
  `6129afd898a56282579832595715ef2e1093b55d299b693810ac05c72af53469`.
- `assets/run-01/images/A-ad43dfe2413b.jpg`, 705×480, SHA-256
  `8a314243feac6b213548048597e20f5e981156a77a291938b93e3b76490958b3`.

These are report-embedded derivatives. Acquisition/clock authentication,
architectural survey and actual interior visibility are not supplied by them.
Root has seen prior annotations and both images. A fresh context-limited AI
annotator receives this protocol, geometry and images, not prior labels or
count outcomes. Embedded text and shared geometry preclude full blindness.
Neither reviewer is a qualified human forensic expert.

## Declared calibration sample

Before new structured records, select these 13 units:

- A-e43e4088a4a2: U02, U04, U05, U06.
- A-ad43dfe2413b: R01C03, R01C06, R01C08, R01C10, R01C11,
  R01C12, R02C05, R02C10, U02.

Selection deliberately includes all five v1 appearance-disagreement units,
clearer positive/dark comparison regions, unresolved bands, smoke, saturation,
material obstruction and an image-edge sliver. It is not random or held out.
The other 24 old units are not relabeled by inference from this pilot. No
building-wide or floor-wide fraction can be calculated from this selection.

## Fields and decision semantics

Each JSON row has `asset_id`, `unit_id`, `candidate_identity`,
`opportunity`, `cautions`, `decisive_exclusions`, `appearance` and `reason`.
Top-level fields identify reviewer, independence, protocol and geometry hashes.

`candidate_identity` is one of:

- `single_candidate`: visually attributable to one framed candidate region;
  minor sill/frame inclusion does not automatically disqualify it. This accepts
  a nominal image candidate, not a physical count or aperture-only segmentation.
- `unresolved`: not enough evidence to decide whether the proposed unit locates
  one candidate consistently; retain unknown, rather than forcing yes/no.
- `not_single`: positively recognized band/multiple regions, not one candidate.
- `clipped`: complete candidate extends outside image or behind foreground and
  its full extent is not established.

`opportunity` is null or one coarse interval `[0,.25]`, `[.25,.5]`,
`[.5,.75]`, `[.75,1]`. It estimates how much of the **fixed proposed region**
provides usable displayed-appearance detail, not fraction burning, clear
interior, a measured pixel fraction, or a statistical confidence interval.
Estimate from edges, texture, exposure and obstruction, not by taking bright
pixel area. Uniform darkness, haze or clipping can leave opportunity unknown or
low. Visible dark glazing may permit a surface description but says nothing
about fire behind it. Never increase opportunity just to include a positive.

`cautions` is a list of strings: localized frame overlap, unknown glazing,
possible reflection, localized saturation, blur, haze, uncertain source depth,
and other limitations that do not themselves prevent the stated description.
They remain visible in reporting and do not automatically veto eligibility.

`decisive_exclusions` is a list of `{code, reason}` records. Use only for an
observed limitation that independently prevents unit-level displayed-appearance
assessment (for example dominant obstruction, uninterpretable target identity,
or dominant overlay). State the effect, not merely the name of a nuisance.
If severity is uncertain, keep opportunity/identity unknown rather than force a
decisive exclusion. A decisive limitation and a localized positive may coexist.

`appearance` retains v1 categories: `flame_structure`, `ambiguous_glow`,
`smoke_only_source_unknown`, `no_flame_discernible`, `non_evaluable`.
Flame structure means morphology consistent with flame, not verified emitting
gas. No flame discernible is a statement about the visible portion only.
`non_evaluable` means no useful appearance conclusion can be made; explain why.
Appearance never automatically changes geometric eligibility or opportunity.
No-flame and unknown classes must not be merged.

## Deterministic bookkeeping and synthetic calibration

Classify the **selected candidate-appearance opportunity subset**, not a
burning-window denominator. No percentages are emitted. For each reviewer,
image, and threshold .25/.5/.75, keep eligible, unknown and excluded lists with
reasons. The preliminary opportunity gate is independent of appearance and
caution count; a contradictory non-evaluable record triggers review, not a
retrospective adjustment of its inputs.

- `not_single` or `clipped`, native axis span below 8 pixels, zero known
  in-frame upper bound, or an explicit decisive exclusion => excluded.
- Otherwise `unresolved` identity, null opportunity/in-frame interval, or an
  interval crossing the threshold => unknown.
- Opportunity lower bound >= threshold => eligible; upper < threshold =>
  excluded. Upper exactly equal with lower below remains unknown.
- Exclusion takes precedence while all unresolved reasons remain recorded.
- Preserve all appearance labels, including non-evaluable and positive labels
  outside eligible subsets. A preliminarily eligible/non-evaluable pairing is
  flagged `semantic_conflict` and reported as unknown pending review; preserve
  the preliminary result too. Do not recode it as no flame or drop the row.
  Do not force an empty subset to be nonempty.

Before historical labels, each annotator checks ten text scenarios: (1) single
candidate, [.5,.75], minor frame/glass cautions => eligible at .5;
(2) same region plus reasoned dominant obstruction => excluded;
(3) clipped localized positive => excluded; (4) multi-opening positive band
=> excluded; (5) unresolved identity otherwise adequate => unknown;
(6) single [.25,.5] at .5 => unknown; (7) single [0,.25] at .5 => excluded;
(8) single null opportunity => unknown; (9) single [.75,1], no discernible
flame => eligible but not evidence of no interior fire; (10) single [.5,.75]
and non-evaluable => preliminary eligible, final unknown with semantic-conflict
flag. Unless stated
otherwise scenarios assume adequate native spans and known in-frame fraction.
These are rule-comprehension controls, not visual-detection accuracy tests.

Reject duplicate/unknown/missing sample IDs, invalid enums/intervals, booleans
as numeric values, non-finite values, hash mismatches and missing reasons.
Check pins and full-source dimensions before summarizing. Save outputs to a
fresh destination, preserve failed attempts, and independently reproduce the
finite count arithmetic. No frame generation or synthetic historical images.

## Calibration decision and next work

Both annotators freeze their records before cross-review. Report every
identity/opportunity/exclusion/appearance difference separately; do not average
or adjudicate merely to improve agreement. A fresh annotator's agreement is not
expert or independent-camera validation. If field ambiguity persists, preserve
the pilot and version the needed clarification before remaining reannotation.

This pilot can establish whether explicit severity removes a bookkeeping
ambiguity; it cannot establish a fire prevalence, continuous chronology,
temperature, NIST input overestimate, structural consequence, or cause ranking.
Broader facade/time coverage and the previously source-pinned floor-specific
fire-input comparison remain required. Do not keep repeating this calibration
instead of completing those workstreams.
