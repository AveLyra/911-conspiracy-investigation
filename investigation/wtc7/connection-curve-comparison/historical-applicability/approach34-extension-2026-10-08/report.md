# Approach integration: conditional coordinates, not established support

October 8, 2026. Research only. The E3/E4 approach annotations add 584
conditional graphical windows under the unchanged calculation rule. The
updated inventory now accounts for nineteen local regions, thirty-eight
original readings and 12,500 route records across all fourteen published
force/energy pairs. It is not a complete supported-domain inventory or a
model-discrepancy result.

Use [version 2, first run](run-v2-01.json) and its
[identical repeat](run-v2-02.json). The original runs remain preserved with
an explicitly documented dependency-check gap; they are not the fully
verified version. The [original protocol](PROTOCOL.md) and narrow
[version-2 repair](PROTOCOL-V2.md) control this unit.

## What changed

The earlier [conditional result](../conditional-envelopes-2026-10-08/report.md)
contained 3,915 windows in 10,840 records. All thirty-four prior reading objects,
their decisions and their axis boxes are reused exactly unchanged. Four
[new approach readings](../../native-footprint-pass/approach34/report.md)
contribute 1,660 more records: 584 conditional windows and 1,076 exclusions.
The combined derivative contains 4,499 windows and 8,001 excluded records.
Repeated copies and shared-source readers are not additional observations.

| New approach reading | Solid windows | Dash windows | Excluded records | Total records |
|---|---:|---:|---:|---:|
| E3 primary | 88 | 47 | 205 | 340 |
| E3 peer | 85 | 47 | 208 | 340 |
| E4 primary | 113 | 41 | 336 | 490 |
| E4 peer | 121 | 42 | 327 | 490 |

Each window retains two separate axis-registration alternatives, giving 1,168
new coordinate hulls. They are marginal bounds under shared calibration
variables, not independent errors or statistical confidence intervals. The
784 new base rectangle conversions include records subsequently withheld by
additional exclusions; that larger number is not additional supported data.

All fourteen pairs now have an identified, core-bearing local candidate for
both line styles somewhere in their completed targets, in both original reader
roles. This is a narrow annotation-label result. The previous E3/E4 absence
applies to their older terminal targets, not the newly recovered approaches.
The new inventory corrects that scope without filling hidden terminal traces.
Candidate presence is not correct identity, shared displacement support,
continuous curve recovery or readiness for consequential comparison.

## Method and retained alternatives

No source image was reread and no source annotation changed. The
[producer](extend.py) validates the complete new originals with the pinned
approach validator. A copy-only adapter translates the list-valued
`fragment_membership` field to the prior calculator's `fragments` schema.
Every original record, uncertainty band, note, flag and reference remains
in `new_source_originals`. All 228 bands are retained; multiple same-column
bands are not overwritten, merged or assigned to both models.

The prior calculator's geometry, masks, status/fragment rules, neighbor checks
and axis alternatives are unchanged. Conditional interpretation still requires:

- Hidentity: the particular reader's local model attribution is correct.
- Hsupport: that fragment's generating curve spans the whole native column.
- Hink0: its ordinate stays within the selected outer cell rectangle, without
  an added unselected-halo allowance.

Those are assumptions, not findings established by the calculated bounds.
The strongest competing reading is that identical selected ink can still
represent different ownership, a partial-column dash end, or an unobserved
continuation. Neither a wider hull nor agreement between readers settles those
questions. Local disagreements remain alternatives rather than being averaged.

Both E3 regions happen to use Im10; their target boxes and original paths
remain distinct. Adjacency at x365 does not join them or supply a missing
neighbor. E4's Im10 approach and Im9 terminal likewise remain separate. The
top strip edge and later empty records establish neither a physical endpoint
nor continuation. F7's missing Im1 dash attribution and all other pairs'
qualifications are unchanged.

## Versioned verification repair

The first version passed eight adapter tests, replayed exactly, and preserved
the substantive records. Independent method review nevertheless found three
omitted upstream pins. Following the older context's declared inputs revealed
three more: six existing dependencies in total were missing from its 120-pin
before/after receipt. This was a protocol-verification defect, not demonstrated
numerical error or altered source evidence.

The [version-2 wrapper](extend_v2.py) checks those dependency maps before invoking
the pinned original producer and verifies the full union afterward. It rejects
conflicting pins, checks map owners before reading them, and requires exact
substantive equality to version 1. Only version/status, input maps and explicit
repair provenance change. Both old runs, original code and failed verification
status remain available. All six missing dependencies match their declared
pins in the repaired execution; the additional current-method and preserved-run
pins bring the version-2 total to 131.

The two version-2 files each contain 7,033,282 bytes and share SHA256
`1c307f8b41d9fb0e1fbe928d4ea1cc177c6bb923ac897ec608fdfae07349a4be`.
Eight adapter tests, four wrapper tests and the twelve unchanged prior-calculator
tests pass. A separate synthetic demonstration shows why the membership adapter
is required: the legacy normalizer ignores this new field combination; the
adapter preserves two explicit members and withholds the otherwise apparently
single-fragment rectangle. No saved historical result used that unadapted route.

The separate [checker](independent_check.py) and its [receipt](independent-check.json)
verify every new decision, all 784 rectangle conversions and all 1,168 coordinate
hulls. All 228 bands, 34 prior reading objects and twelve unaffected pair
objects are preserved exactly. Its independently traversed approach-dependency
graph contains 37 files and fourteen JSON nodes; the complete required union
matches all 131 producer pins. Forty-five controls pass, including deliberately
altered decisions, hulls, bands, inventory fields, JSON types and missing pins.
Root read the checker and reproduced its complete saved receipt exactly.

The checker reuses two pinned independent helpers and its own copy adapter;
it does not import the producer, producer classifier or coordinate-mapping
functions. The old 10,840 decisions are checked for exact preservation, not
recalculated independently again in this unit. New arithmetic agreement does
not validate Hidentity, Hsupport or Hink0.

One checker preflight incorrectly required a linked narrative report in the
producer's dependency union (`844ac4`, diagnosed in `763e0f`). Review confirmed
that it supplies no unique parameter or rule absent from pinned inputs. That
report is separately pinned as checker review context; it is not an execution
input whose bytes the producer reads. The corrected classification preserves
all declared-map dependencies and numerical requirements. This preflight and
the substantive version-1 gap both remain in the receipt. Actual commands,
results and artifact pins are in [verification.json](verification.json).

## Claim limits and next evidence-bearing work

| Claim | Evidence layer and strength | Strongest limitation / next test |
|---|---|---|
| The new annotations add local candidates and 584 conditional windows. | Reproducible calculation; conditional on recorded attribution and the three hypotheses. | Source-specific ownership and enclosing-ink assumptions remain unvalidated. |
| All fourteen pairs now contain both-style candidates somewhere. | Derived label-presence count, directly checkable within these files. | Does not establish a common interval, continuous route or physical accuracy. |
| The approach recovery resolves the full curve comparison. | Unsupported. | All outside-target obligations, contacts, seams and actual curve-review requirements remain. |
| These results favor a collapse cause or demonstrate intentional model manipulation. | Unsupported. | This unit concerns published model-to-model calibration curves, not a reproduced historical load path or evidence of intent. |

The updated full inventory is `inventory` in the version-2 result. Twelve
non-E3/E4 pair objects are exactly the earlier objects. E3/E4 retain all old
regions and only add the two new targets and narrowly updated residual language.
Their Im11 origins, earlier/out-of-box material and joins remain pending or
unresolved. Qualitative residual descriptions are not exact complementary masks.
Do not reconstruct such masks from prose or repeat completed pixel censuses.

Next recover the previously identified F5 Im3 descent and F6 lower-Im1 crest
in declared finite source batches, or record source-specific limits if the
originals cannot support them. Read the full-region inventories and source
locators first, fix target/context geometry before new cell readings, and
preserve independent freezes, shared-color conflicts, clipping and exact
prior-overlap receipts. Existing local regions are reusable evidence, not new
independent observations. Other fourteen-pair obligations remain in the inventory.

The 42 paired human-review slots remain unselected until full support/identity
disposition; confirmed axes and legends need not be asked again. No common
support domain, physical/model discrepancy, historical solver, accepted Sherlock
finding, Faraday activation, cause ranking, legal promotion, disclosure, commit
or push occurs. The goal remains active and incomplete; these files are local,
intentional work in progress on `research/sherlock-wtc7-investigation`, base
`ca1c2233`. Generic schema feedback is queued locally under the unresolved
archived Sherlock destination, not delivered or verified as a product fix.
