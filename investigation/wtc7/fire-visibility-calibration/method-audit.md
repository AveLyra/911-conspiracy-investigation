# Independent contract audit and calibration boundary

2026-09-15. Research-only. The context-limited `fire_denominator_audit` agent
read the old protocol, geometry, labels, summary code and report, but did not
inspect new labels before reviewing the new protocol. This is independent
reasoning about shared artifacts, not independent source acquisition or expert
fire engineering. Root independently read the relevant code and source records.

## Reproduced failure mechanism

Read-only original directory:
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-annotation/`.

- `summarize_annotations.py`, function `eligibility`, lines 333–336:
  every non-null `geometry_objection` and nonempty `quality_exclusions` is
  independently an exclusion. Reviewer supplies both for all 37 records;
  every reviewer record includes `glass_unknown`. Main supplies 13 geometry
  objections and 10 nonempty quality lists. Thus two blanket mechanisms each
  guarantee the reviewer's empty denominator, independent of threshold.
- Original protocol requires no **decisive** glare/smoke/boundary ambiguity;
  the field contract omits the severity distinction. Approximate visually
  framed candidates, aperture-only segmentation and authenticated physical
  openings were also not consistently distinguished by the two annotators.
- This does not explain away all physical disagreements. Opportunity intervals
  differ on otherwise similarly labeled units. Three appearance disputes concern
  actual morphology (e43 U05; ad43 R01C10/C11); one concerns smoke versus the
  obscured target (ad43 R01C03), and one concerns nondetection versus insufficient
  opportunity (ad43 U02). Fresh image inspection is necessary.
- Old code checks whether in-frame fraction is null, not whether it is zero.
  The actual 24 old complete candidates all have `[1,1]`; this is a prospective
  contract gap, not a changed historical result.

Old records remain unchanged. Rechecked SHA-256:

| Artifact | Hash |
|---|---|
| main-units-v1.json | `5a489e0f6dc7c9d01d0711c5dccbb7acc4e2ef22ecde62eab617df4e4f8f35cc` |
| reviewer-units-v1.json | `449b17e6d40b617cdd6a87fd3cf9a7a85088fe83d9b593de9b5b4cd79a14221a` |
| geometry-main-v1.json | `d7c593a6d7ccad9f1f403bf0ee8a2bfe5afd6d0c6e5dd446c3602e6a5e590a13` |
| PROTOCOL.md | `f3d7f028188aaa09edae486b84ec14c103d56142c094800ad11168e7d09a59ba` |

## Prospective review of the new pilot

The reviewer recommended keeping normal appearance classes membership-neutral,
unknown glazing as an inference caution unless its visual effects actually
prevent assessment, and positive localized features outside any eligible
candidate subset. A high-opportunity `non_evaluable` record needs a consistency
check rather than automatic inclusion, exclusion, or conversion to a negative.

Before either new historical record was saved, root incorporated a preliminary
opportunity gate followed by a `semantic_conflict` flag and final unknown status
for an otherwise eligible/non-evaluable pairing. Inputs remain unchanged.
The final protocol hash is
`ea5c641475f47ef7a72fcf25876ec89eca8078b2756303920c323affe2a969a5`.
The reviewer checked the full saved protocol and all ten text scenarios and
reported no blocking issue. Two implementation cautions were communicated
without sharing labels: exclusion takes precedence over unresolved factors,
while preserving both; uncertainty about obstruction severity belongs to
opportunity, not automatically to an otherwise established candidate identity.

The thirteen regions are purposively selected calibration examples, including
all five old appearance disagreements. Neither semantic agreement nor repeated
AI inspection establishes detection accuracy or a measurable burning-window
percentage. Root's familiarity with previous labels is explicitly disclosed.

## Claim ledger

| Claim | Type / grade | Support and replication | Alternative / weakening test |
|---|---|---|---|
| Old blanket fields mechanically force zero reviewer eligibility | Derived / A within saved records | Direct code and all-record field inventory; independent method audit, root code check | Counterexample row lacking both vetoes or a different executed rule would weaken it |
| All physical disagreement is merely bookkeeping | Unsupported / E as a blanket claim | Interval and morphology disagreements survive field diagnosis | Fresh visual agreement may narrow particular disagreements, not retroactively remove them |
| Revised semantics can distinguish caution from decisive obstruction | Method-dependent / C until actual paired pilot | Versioned protocol and text controls; real annotation comparison required | Continued axis confusion or outcome-dependent relabeling defeats the claim |
| Candidate counts quantify interior fire extent | Unsupported / E | No calibrated interior visibility, detection model or representative sample | Requires different independent evidence and a justified observation model; more agreeing AI labels alone cannot supply it |

## Completed pilot follow-up

After both labels were frozen, the same method auditor independently implemented
the protocol arithmetic without importing the producer. Sixteen synthetic
checks and both complete 78-row summaries passed; root read and replayed the
checker with an identical summary01 receipt. Root also independently recomputed
the old 37-row field counts and all five old appearance disagreements. The
[paired report](report.md) and [validation](validation.md) replace the
prospective ledger's pending-pilot state with actual outcomes, without
promoting its method-dependent visual judgments to measurements.

Both reviewers have identical eligible memberships in this purposive pilot,
but disagreed on excluded versus unknown for one cloud-covered candidate.
Three luminous-morphology differences, a substantive evaluability difference,
and a category-priority difference remain. The fresh reviewer independently
cross-checked the synthesis and required the semantic/substantive distinction
to remain explicit; root applied that clarification. No frozen label changed.
