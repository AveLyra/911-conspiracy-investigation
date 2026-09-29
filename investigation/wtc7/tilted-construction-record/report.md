# Does the saved project document the marking rule?

2026-09-24. Research-only source locator. **Independent raw-source verification
and root replay pass within the declared metadata scope.** No physical
measurement or causal ranking is made by this unit. Critical-review history
and the wording correction are retained in [critical-review.md](critical-review.md).

## Result within the inspected scope

The two independently checked hash-only exports find no `description`, `note`, `comment`,
`method`, `construction` or `history` property directly on the saved project's
root or any of its eight PointMass tracks. The fixed name/class stem search
also finds no candidates anywhere in the parsed element tree. This particular
description-field route therefore does not supply a marking or continuation
recipe for PM05/PM08.

That is **not** a finding that the analyst had no method, that no documentation
exists, or that the marks are invalid. The inspected root serializer normally
omits empty notes; the base track serializer is not among the held sources
reviewed here. Methods can be unsaved, stored under unrelated fields, embedded
in excluded comments or processing instructions, or documented elsewhere.
All saved text values remain hashed, not semantically reviewed.

The prior [exact-point audit](../tilted-point-frame-audit/report.md) remains
unchanged: a roof-edge observable need not be a continuously visible material
corner. Failure to recover a continuation recipe does not adjudicate the
physical accuracy of that broader observable.

## Fixed source, actual coverage and output limits

The [protocol](PROTOCOL.md) was declared before the historical read. Independent
preflight review clarified mixed text, parsed-element versus lexical coverage,
structured strings and unknown attributes **before results were inspected**.
No source-dependent search expansion or favorable omission was made.

Only the already-held public kit's exact named Tilted project was inspected,
in memory as inert ZIP/XML data. No Tracker execution, media decoding, external
retrieval or other project/version search occurred. The lineage is:

| Layer | SHA-256 |
|---|---|
| Parent public ZIP | `c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189` |
| Named nested TRZ | `7eee39a3f9c802343204d7f3f595478ab4c5a7c6c54ca8e2928c46c7ed8b7552` |
| Nested TRK, zero-based entry 4 | `babf332bd340c1e902870f14d4370eab4f3a54de388ce06c1ca85ae222b1b5da` |

The exported parsed structure has 1,769 elements and 3,220 attributes; selected
ownership is root plus all eight direct-collection PointMass objects. The root
has 19 direct properties, each PointMass has 8, for 83 selected direct-property
occurrences. No selected-owner duplicate/shape review flag was raised. This
is schema coverage, not evidence about the building.

| Scope | Saved result |
|---|---|
| Root target fields | All seven declared fields missing, including `name` and `description`. |
| All eight PointMass owners | Each has one nonempty `name`; the other six declared target fields are missing. Values were not displayed. |
| Global fixed name/class stem search | Zero hits among all parsed elements. This is a name search, not a content search. |
| Global literal type=`string` leaves | 138, all with nonempty parsed text; zero structured-string nodes. |
| Known leaf field labels | One each `semantic_version`, `length_unit`, `mass_unit`; ten each `name`, `footprint`; 115 leaf records with names outside the label allowlist. |

The 115 unlabelled string-leaf records are **not** described as irrelevant or
empty. Their identities, paths, sizes and text hashes are retained, but their
names/values were not generally printed or interpreted. Unknown fields and
other owners remain possible places for information; fixed-name nonmatches
cannot exclude them.

Exact selected target paths are PM05
`/*[1]/*[13]/*[7]/*[1]` and PM08
`/*[1]/*[13]/*[10]/*[1]`; these are element-child locators, not physical members.
Both have the same eight-property count and missing target-description states
as the other PointMass objects. Including all eight prevents a two-track-only
absence claim from concealing a relevant description on another selected track.

The [full sanitized ledger](run01/locator.json) preserves every parsed element,
attribute, direct text/tail, immediate-text segment, selected-owner property
and declared subset. XML comments and processing instructions are explicitly
excluded; CDATA and adjacent text are parsed character data, not preserved
lexical spelling. Complete parsed-element coverage is not complete possible-
documentation coverage. A hash proves captured-byte identity, not authenticity,
content relevance or historical procedure.

## What the held code supports

The separate [source semantics review](semantics.md) grounds interpretation in
exact held Java ranges. Root independently read the relevant root description,
notes-display and PointMass save/load passages.

- Root `description` is free-form panel notes, emitted by the inspected writer
  only when trim-nonempty. Its absence is ordinary serializer-compatible state,
  not evidence of deletion or concealment.
- `hide_description` controls automatic notes display. Its name is not evidence
  of hiding scientific evidence; no saved value was exposed or inferred here.
- Per-track descriptions exist at runtime, but PointMass delegates common
  serialization to TTrack. That base implementation was not found in the
  declared held-source filename search. Per-track `description` was a candidate
  locator, not a fully traced writer contract.
- The inspected per-frame record saves x/y, not annotator, feature definition,
  uncertainty, creation timestamp or a construction recipe. Keys can arise
  from automatic marking. Editing/undo capability is not a persisted history.

Those are claims about the inspected source revision, not proof that it was
the historical executable or the only persistence mechanism.

## Claim strength and strongest alternatives

| Claim | Type / current status | Strongest alternative or falsifier |
|---|---|---|
| The six declared description/rule fields are absent directly on the selected owners; the fixed name/class stem search returns zero hits. | Literal source-state calculation; producer repeat, separate raw parse and root replay pass. | A shared parser/coverage defect; a new implementation that finds a missed field within this exact declared scope would falsify the result. |
| This field route supplies no target-specific continuation recipe. | Bounded inference from those missing fields, not a general documentation search. | A rule under an uninspected name/owner, excluded XML token, different project or external record. |
| The analyst had no rule, fabricated marks, or necessarily tracked a material corner. | Unsupported by this unit. | Ordinary manual/automatic marking or a legitimate projected-edge construction is compatible with the present record. |
| Collapse cause or physical acceleration is resolved. | Not tested. | Source/scale/time/observable validation and the fire-to-failure or intervention evidence remain separate dependencies. |

## Verification and remaining work

The inherited helper's 17 synthetic controls pass; the new locator's final 13
controls pass in both the preparation run and root replay. The initial12-test
run is retained; the added test specifically checks producer/helper/protocol
pin refusal before source loading. Both fresh historical exports are
6,276,196 bytes, SHA-256
`bf47dd03fd41205794d1bce0d6b9893f773d2ff2aed6382d4b91b11d33ce4f6c`.
Root compared their actual bytes. A separate minidom implementation, without
importing the producer or its helper, then reconstructed and compared the
complete declared metadata structure directly from the pinned raw XML. Its
17 synthetic controls passed in both the author run and root replay; both
historical verifier runs passed. The author used Python 3.14.0; root used
3.12.14. Source, procedure and product fingerprints remained unchanged.

This establishes checked extraction within the fixed contract, not independent
historical evidence or physical validation. The implementations share source
bytes, the declared schema and Python standard-library XML dependencies.
Excluded tokens and unreviewed meanings remain excluded despite a passing
comparison. See the [independent verification record](verification.md) and
[execution record](validation.md) for commands, receipts and limits.

This result does not justify repeating these same target-name searches as
new evidence. It also does not authorize arbitrary metadata disclosure or an
assumption that the unknown leaves contain a method. The remaining source
question is a specifically linked construction/edit record or publication
version. A new independently defined roof-edge measurement would be a new
analysis, with its own prospective observable, uncertainty, calibration and
actual-human review gates—not a recovered original method.

Main/raw/legal sources, old derivatives and accepted Sherlock/Faraday engines
remain unchanged. The generic parser-coverage lesson is deduplicated under
existing feedback IDs and queued locally while the designated task remains
archived. No outreach, transfer, filing, source promotion, commit or push.
The full investigation and broader Luna attribution review remain incomplete.
