# Metadata contract failure and diagnostic continuation

2026-10-04, after acquisition and before diagnostic extraction. The original
protocol and strict parser remain unchanged; this is an explicit continuation
after failure, not a repaired pass.

The first historical strict run (24f118, exit 1) stopped on a returned record
without folder_name. A read-only raw field-name check (c22ee2, exit 0) found
eight such occurrences, with no extra property names in the ten responses.
The archive omission is not a literal None, an empty string, evidence that the
PDF has no folder, or proof of an evidence-handling act.

Keep the strict eleven-property requirement failed. A separate diagnostic
script may inventory actual query coverage and record presence, using the
unchanged strict contract to label each row valid or quarantined. For the
observed exception, retain ten actually supplied scalar fields, missing-name
list, strict exception, raw property objects and query/one-based ordinal.
Never synthesize a folder label. If additional unknown schema exceptions,
duplicate properties, invalid scalar values/IDs, or cross-query conflicts occur,
stop or preserve them as unresolved; do not coerce them into a valid record.

Coverage counts include all source-returned records, not merely valid ones.
Report strict-valid and quarantine counts separately at occurrence and unique-ID
grain. An ID with supplied valid title/key/page/byte fields can be a candidate
locator despite its missing folder label, but cannot satisfy full metadata
acceptance. Compare independent diagnostic inventories only after both freezes.
No PDF content viewing, queries or pagination are added.

This failure narrows the completed claim to preserved search responses and an
independently checked diagnostic inventory. The original full-contract
extraction is not completed successfully and must remain visibly failed.

