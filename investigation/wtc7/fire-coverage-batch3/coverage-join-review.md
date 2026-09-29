# Independent coverage-join review

2026-09-24. Bounded read-only review of `coverage-timeline.json` and
`coverage-timeline.md` after both full observation records froze. This
reviewer did not author the join, alter prior source records, view new image
pixels, acquire sources, rerun a physical model or add a physical inference.

The join passes the checked membership, source-pin, recurrence, dependency and
comparison-status requirements. No material correction is required in the
reviewed versions. This conclusion concerns the join's consistency with its
declared inputs, not the historical accuracy of NIST's credits, geometry,
timing or fire interpretation, and not completion of native annotation for
all 26 new targets, WP1 or the investigation.

## Exact membership and preservation

The prior inventory has 25 photographic figure entries, after excluding its
three geometry graphics. Its figure set is disjoint from the exact 26 new
targets listed in the frozen batch 3 protocol. Their union is exactly 51
unique figure rows in the JSON and exactly the same 51 rows, partition and
display order in the Markdown table.

Fifty rows have standalone JPEGs with 50 distinct asset IDs and 50 distinct
encoded-byte hashes. Their file bytes, sizes and key dimensions match their
preserved metadata. This counts stored report representations. It does not
establish 50 independent photographs, exposures, cameras, clocks or fire
events.

The remaining row is exactly figure 5-121. Its observation asset list is
empty, image field is null and status is `unscored_representation_gate_failure`.
It retains exactly 17 distinct source components and the failed receipt/addendum
pins. The receipt still says `accepted: false`, `png_written: false`, and no
assembly is asserted by the join. All 17 parent JPEG hashes match. Counting
50 standalone objects plus these 17 components gives 67 distinct selected
native PDF objects, not 67 scored observations or exposures. The unscored
row remains source coverage with a representation limit, not a no-fire result.

The new extraction contains exactly ten earlier selected assets as context:
5-125, 5-126, 5-135, 5-137, 5-148, 5-149, 5-150, 5-151, 5-157 and 5-158.
For each, the figure association, asset ID and actual JPEG bytes/hash agree
between the earlier inventory and new extraction. Each contributes one prior
row. None increases the 51-row union. The four other new context figures,
5-120, 5-127, 5-131 and 5-147, remain outside both selected sets.

The ten declared join input files, held source PDF, two full observation
freeze pins, all referenced row images, page renders and context text, failed
tile receipt/addendum and recurring context JPEGs were rehashed. There were
176 distinct files checked before and after the audit, with zero mismatches
or changes. Prior row image/page metadata agrees with the pinned inventory.
For all 26 new rows, 364 comparisons establish exact equality of 14 inherited
source fields per row: page numbers/render/text, floor list, source labels,
view, credit, processing, limits and timing label/interval/basis/source pages.
The reviewer separately read the prior and new source reviews and the pinned
prior source-comparison/FA table and its review. These remain attributed
secondary research records; this audit did not replace their complete-page
source inspections with a new independent image interpretation.

## Dependencies and clock limits

The two explicit same-exposure groups are preserved: 5-60/61 and 5-129/130.
The crop parent of 5-113, figure 5-64, stays outside the selected union.
Every group-to-row reference is reciprocal and names an included figure;
external parents/context are separately identified. No group-string count
is reported as an independent-source count.

The cross-batch CBS lobby/street series includes prior 5-137 without giving
each frame an independent clock. The Didik group preserves the relative
5-124/125/126 timing and distinguishes the inferred film time of 5-150.
The Peskin entries retain related-frame/viewpoint dependence. The Rabanne
group retains incomplete camera/clip/clock authentication. Institutional
NYPD/FDNY grouping and Spak name normalization remain credit dependencies,
not proof of one camera or independence from differently named sources.

The 5-152/157/158 viewpoint/sequence relation does not overwrite Unknown with
Fox or infer separate cameras from the different credit strings. The
explicit 157/158 clip relationship is distinguished from the less certain
152 viewpoint link. These distinctions match the pinned prior/new source
reviews and are retained in both the JSON and Markdown.

All 51 time records have `independently_authenticated: false`. The audit
verified that relative/approximate/unbounded entries such as 5-122, 5-125,
5-144/145/146, 5-152 and 5-157/158 were not converted to hard numeric
intervals. Figure 5-125 does not inherit 5-124's three-second precision.
The 5-109 and 5-111 a.m./p.m. conflicts remain explicit; 5-111 has no nominal
ordering time. Figure 5-156's published interval still ends at 17:21:45,
without silently clipping it to a collapse reference.

The fire/window-comparison, travel-time and typical-burning-duration bases
are preserved in the per-row timing text and join ambiguities. The timeline
therefore does not turn agreement using those same assumptions into an
independent validation of them. Display order is a navigation choice over
uncertain/overlapping estimates; the source expressly disclaims continuous
coverage, interpolation and a newly established event chronology.

## Location and FA comparison meaning

Recomputing facade tags gives north 37, south 6, east 9 and west 7. Corner
views overlap categories, and the north count includes the unscored 5-121
row. No new row has a south tag. These counts neither measure whole-facade
visibility nor count independent events.

Every row retains a floor-scope qualifier. The document explicitly defines
listed floors as source labels, visible/discussed locations or prose
attributions, not established burning floors. Some numeric lists summarize
prose-discussed floors while `source_label_details` preserves additional
printed numerals; they must not be treated as an exhaustive fire or window
denominator. In particular, 5-137 remains a floor 6-9 view with source
attention to 7/8, 5-153's floor-14 assignment remains qualified, and the
floor-9 reflection alternative in 5-144 remains a limit.

The seven FA-C01-C07 questions correspond to the pinned preexisting
source-input audit. Each retains an empty `matched_figure_links` array and
`no_complete_quantity_location_time_match` status. No row has a nonnull model
comparison result or imports/relabels an appearance observation. The Markdown
states the same zero-completed-match result and explains the missing
quantity, location and time correspondence for each question.

Zero completed matches is the recorded status of this fixed source join.
It is not a finding that no pertinent record exists elsewhere, that no
model discrepancy was discussed by the source, or that the model has been
independently validated. Native inputs/outputs, independent timing and
declared observation-to-model mappings remain missing for the proposed
tests. Source-image appearance has not been converted to gas/steel
temperature, heat release, structural consequence or cause.

## Actual reproducible check

The new `check_coverage_join.py` is a read-only standard-library audit. It
does not import the join producer or alter any checked file. It rejects
duplicate JSON keys, checks the exact sets and field equalities above,
recomputes recurrence and group links, checks Markdown order and FA status,
and hashes the actual files before/after. Read-only assertions test this
saved join; they are not an optical calibration or a new physical experiment.

Command, run from this batch directory:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B check_coverage_join.py
```

Result: exit 0, `accepted: true`, 1,745 assertions, 176 distinct files
rehashed before/after, 364 inherited new-row source-field equalities, and
`failures: []`. No failed join assertion was relaxed or repaired to pass.

Reviewed JSON SHA-256:
`08141aa6d221f80bec33501761b5f19030706bb1e0badfd035375bcb93c73aab`.
Reviewed Markdown SHA-256:
`9f387e007e2cf2fc659c7c3074214c44b35b9bb91c45eb409d29bc98720ebce7`.
Audit script SHA-256:
`9297094bccd7ca3110c18a3249908b95f705e4310037d031f8f84608e9f65dd2`.
The exact ten input paths and source pins remain in the reviewed JSON.

The strongest limitation is shared-source dependence: reproducing the join
shows that its uncertainty and lineage survived the transformation, not that
the underlying clocks, camera custody or floor assignments are independently
correct. Authenticated originals or a changed source attribution could
require a versioned correction. No such new evidence was acquired here.
