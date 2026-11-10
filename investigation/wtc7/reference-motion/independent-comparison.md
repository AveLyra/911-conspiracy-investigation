> **Historical research:** This is a dated computational record, not a new analysis or instruction. Local paths are redacted and omitted dependencies marked; see the [publication note](README.md).

# Independent comparison plan: declared before automatic outputs

2026-09-11. Status: comparison criteria declared; automatic run paths and outputs not yet received or viewed. This is a computational AI comparison to the existing subjective visual annotations, not independent human review, historical authentication, physical calibration or a new holdout. Prior visual familiarity is already disclosed in the frozen annotations.

## Frozen inputs and scope

Use the completed [independent annotations](independent-annotations.json), SHA-256 `c323d66d504c264df6792e7e5681b2d828dc6ab85db842bde0711a0e94b98b70`, and their [review notes](independent-annotations.md), SHA-256 `bd001a83628b0a7725292a9fd957651b7268c88f2b051fcb13fb446fb0fd882e`. Do not edit either file or the baseline configuration. The current [protocol](PROTOCOL.md) was read before this plan. It defines separately scored 19×19 and 27×27 baseline templates, independent fixed-seed searches and quality flags; its matching and camera-consistency gates remain distinct from this comparison.

The existing manual scope is six references × five evaluation frames × two cameras = **60 feature/frame annotation rows**. Compare each row separately to both template sizes, yielding **120 expected comparison records**. Per size, 48 rows have a manual coordinate/envelope and 12 do not (six ambiguous and six unavailable). No new manual coordinates, template seeds, frame selections, threshold tuning or reference exclusions are part of this comparison.

The root investigator will supply accepted run paths after its synthetic controls and historical processing. Only then read the output schema, receipts, pinned protocol/configuration and candidate records. Adapting field names to an actual schema is bookkeeping; any substantive criterion change must be written separately as post-output exploration and must not replace this plan.

## Join and provenance checks

1. Recheck both annotation-file hashes before comparison and at completion. Record supplied run paths, actual input/output hashes, code/configuration/protocol lineage and whether outputs represent completed or failed runs. Do not silently compare a failed or partial scope as a complete result.
2. Join by **camera/source ID, zero-based native frame index, reference ID, and template size**. Verify exact rational source PTS and native image identity against the annotation record. Preserve source indices; do not join by rounded seconds, row position or nearest time.
3. Preserve exactly one result for each of the 120 expected keys. Duplicate keys, unknown required identities, changed input hashes or mismatched PTS are explicit provenance/contract failures requiring resolution before a numerical agreement conclusion. Missing candidate records remain marked `missing_auto_record`, not silently dropped. Extra automatic frames/references are outside the manual evaluation scope and are not scored as additional independent manual tests.
4. Retain automatic winner coordinates, all supplied acceptance/rejection/undefined status and quality reasons, template size, and any relevant score/margin/boundary flags. Preserve an explicit rejected-seed result even when it has no winner coordinate. A candidate center must be valid finite coordinates under the declared native convention before a coordinate comparison; malformed values are not zero or missing-motion estimates.

## Coordinate and status comparison

For a manually localized row, compute automatic-minus-manual differences `dx` and `dy` in the original stored image coordinates. A candidate is **inside the subjective rectangular envelope** precisely when `abs(dx) <= halfwidth_x` and `abs(dy) <= halfwidth_y`, with inclusive bounds. Preserve the two signed differences and the declared halfwidths; do not substitute a circular, Euclidean or statistically weighted test. Compare absolute patch-center anchors as annotated, not a fitted/stabilized position or a baseline-subtracted physical displacement. Baseline role/localization uncertainty remains separately visible.

Retain these outcomes independently of the algorithm's gate status:

| Manual status | Automatic record | Comparison label and permitted reading |
|---|---|---|
| Localized | Finite winner inside envelope | `inside_manual_envelope`; agreement with this coarse visual localization only. Keep whether the winner passed or failed automatic gates. |
| Localized | Finite winner outside envelope | `outside_manual_envelope`; a coordinate disagreement requiring explanation, not automatically a proven algorithm error or a new manual correction. |
| Localized | No defined winner / seed rejected / missing row | `no_coordinate_comparison` with the exact automatic reason; do not treat as a zero error, a manual disappearance or an identity failure. |
| Ambiguous | Any automatic candidate/status | `manual_identity_ambiguous`; retain candidate coordinates/status but no manual-coordinate error or envelope test. |
| Unavailable | Any automatic candidate/status | `manual_feature_unavailable`; retain candidate coordinates/status but no guessed replacement point or envelope test. |

For accepted automatic candidates at ambiguous/unavailable manual rows, explicitly flag **automatic acceptance without manual identity support**. This is a consequential discrepancy between gate acceptance and what this visual pass could establish, but it does not by itself provide a calibrated false-positive rate. Conversely, rejection at a manually localized point is a procedure/threshold limitation, not proof that the feature disappeared. All rejected candidates remain in the ledger, including rejected candidates whose coordinates fall inside a manual envelope.

## Reporting and inferential limits

Produce an additive `independent-comparison.json` containing all 120 expected records and a concise result section below this preserved plan. If a small independent comparison script is needed, it must read frozen annotations and supplied outputs without importing or modifying the tracker. Record the script and result hashes. No decoder, network service, bridge or new source is used.

Report counts by camera and template size, separating automatic accepted/rejected/no-winner status from manual localized/ambiguous/unavailable status. State denominators explicitly. Among the 48 localized rows per size, show inside/outside/no-coordinate counts; separately retain the 12 rows per size for which manual coordinate agreement cannot be assessed. Report frame/reference-specific disagreements and differences between sizes. Do not pool unresolved rows into an “accuracy” percentage or turn subjective envelopes into confidence intervals. Two overlapping template sizes and repeat runs are sensitivity/reproduction checks on the same inputs, not independent corroboration.

Coordinate agreement does **not** establish that a patch is the same material point, that its object is stationary, or that a common transform applies to the target building. In particular, retain the hanging-banner motion risk, repeated-pattern alternatives, signal-lens ambiguity/illumination changes, overlapping structures at uncertain depths, and Camera 4's late loss of secure anchors. All Camera 2 repeated nominal manual coordinates mean only that this pass did not resolve movement beyond its envelopes; they cannot validate zero or subpixel camera motion.

A successful automatic multi-reference fit remains separate from manual agreement. This comparison does not recompute a camera correction, apply a transform to historical images, fit the building's motion, authenticate camera exposure timing, synchronize views or infer physical acceleration, structural failure timing or cause. Any later inspection prompted by a disagreement must be labeled post-output review and must preserve the original annotations and this planned comparison.

## Execution status

Awaiting root-supplied run paths. No automatic candidate outputs have been inspected and no numerical comparison has been run.
