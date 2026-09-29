# Bounded critical review of the construction-record report

2026-09-24. Research-only interpretation review. **Independent raw-source verification remains pending at this review stage.** This note does not clear that gate, review plaintext metadata, infer a marking history, or change any physical/causal assessment.

## Scope and reviewed versions

The reviewer read the entire initial and corrected `report.md`, current `validation.md`, the complete protocol and the held-code semantics note. The protocol and semantics were already read fully in the preceding bounded task and their current hashes were rechecked here. The only result input read was the sanitized `run01/locator.json`; no original TRK, omitted plaintext, other source version, media or new external source was opened.

| Artifact | Reviewed SHA-256 |
| --- | --- |
| Initial report | `233dc343e0fbcb13cbcca44415f9b9e8425a191845b5a656a890c02bb89e94aa` |
| Corrected preliminary report | `44d69bc6b860b2f2fd3c886048bd24390f83372276e69497939348ec606f1644` |
| Protocol | `47d55648820416cb92d35d562335a6332a8eff490c9a3e861ecda3a54cd6e030` |
| Semantics | `09d9b9b29cd34cbfcf1e1118665dfb73ea20a8e732e0364ce49fcd36cb550cd6` |
| Sanitized run01 locator | `bf47dd03fd41205794d1bce0d6b9893f773d2ff2aed6382d4b91b11d33ce4f6c` |

Review independence is limited: this reviewer authored the code-semantics note and earlier representation verifier, and reads the shared source-derived locator. It is not an independent human/expert review or independent historical evidence. The separate raw parser, not this note, must establish complete source-to-export fidelity.

## Material concern and resolution

The initial claim table said: “The fixed target fields and name/class stems are absent in this parsed project.” This was overbroad. The declared target set includes `name`, while every selected PointMass owner has one nonempty saved name. The claim table contradicted the report's otherwise correct coverage table.

The reviewer requested a distinction between the six description/rule fields and the separate global stem result. Root changed the row to:

> The six declared description/rule fields are absent directly on the selected owners; the fixed name/class stem search returns zero hits.

The corrected snapshot resolves the concern without broadening the search, changing the observations or suppressing the positive name-presence result. This correction is an interpretation/wording repair, not a repaired source-export result.

## Claims correctly kept bounded

- **Named-field absence is not all-method absence.** The report confines its positive absence statement to `description`, `note`, `comment`, `method`, `construction`, and `history` directly on root plus eight direct-collection PointMass owners. It separately labels the fixed stem search as a name/class search, not semantic content review.
- **Unknown strings are not dismissed.** The 115 string-leaf records without allowlisted field-name labels remain nonempty, hashed and unreviewed. This is a count of records/occurrences, not a finding of 115 distinct field names or 115 meaningful method candidates. Other owners, unrelated names and excluded XML tokens remain explicit limits.
- **Ownership is preserved.** PM05 and PM08 have exact element-child locators; the text does not equate those locators with physical members. All eight PointMass objects are included, but that does not make the selected-owner target search an all-owner method-content search.
- **Missing versus empty is not collapsed.** Root description is missing in the reported inventory. The code can omit empty/trim-whitespace notes, but the report does not claim to recover a formerly empty value or infer deliberate deletion.
- **Runtime description is not a verified track serializer.** The missing `TTrack.Loader` and distinction between candidate per-track field and traced root serializer remain visible. Source-revision claims are not promoted to historical executable identity.
- **No marking-history invention.** Keys are not called human observations; edit/undo capability is not called a persisted history. The report does not choose interpolation, manual marking, autotracking or a constructed edge as the historical method.
- **Observable qualification survives.** Failure to identify the original lower step foot is not used to invalidate every roof-edge observable. No numerical acceleration or cause follows from a missing recipe.
- **No duplicate-work or disclosure permission.** The next step does not rerun these same name searches as new evidence and does not authorize unrestricted reading/disclosure of the remaining metadata.

## Actual sanitized-output checks

Read-only `ruby -rjson -e ... run01/locator.json` commands inspected schema keys, selected-owner counts/paths and target occurrence states, then recomputed aggregate counts from the existing parsed ledger. They corroborated the report's internal summary: 1,769 element entries; 3,220 attribute entries summed from those elements; nine selected owners; 19 root plus eight properties on each of eight PointMass objects, totaling 83; seven root target fields missing; one nonempty name and six missing description/rule fields per PointMass; zero stem hits; 138 nonempty string-leaf records; zero structured-string records. The leaf-label tally is one each `semantic_version`, `length_unit`, `mass_unit`, ten each `name`, `footprint`, and 115 unlabelled records.

These checks independently aggregate **the producer's sanitized result**, not the raw XML. They cannot detect a raw-source element or text segment omitted from that result. No repeat byte-identity or producer/control test was independently rerun by this reviewer; the report's execution claims remain attributed to their receipts/root until the separate verifier's result is reviewed.

The first selected-owner display was unnecessarily large and truncated; it exposed only the sanitized hashes/technical labels, not source plaintext. A subsequent compact aggregation returned the relevant states/counts without truncation. No conclusion relies on unseen truncated content. `shasum -a 256` checked the listed inputs. These commands exited 0; no files or source artifacts were changed by the checks.

## Current disposition

**The one material wording concern is resolved in the corrected preliminary snapshot.** No further material interpretation overclaim was identified within this bounded review. The strongest remaining alternative is still that a rule was unsaved, differently stored, elsewhere documented, or unnecessary for a differently defined observable. The stage-1 inventory cannot select among those possibilities.

Independent raw-source verification and the corresponding report-status update remain outstanding here. A later disposition can review those exact receipts and the new report snapshot without altering this initial review, the source inventory, or prior observations. No causal ranking, broader investigation completion, scientific acceptance or plaintext disclosure is approved by this note.

## Final disposition after the separate verification runs

2026-09-24, later review stage. **The pending verification status above is retained as history and is superseded for this bounded metadata unit by the receipt review below.** The initial concern, source observations and earlier snapshot identities are unchanged.

The reviewer read the complete updated report, validation record, independent verification note, both actual historical verification receipts and both final 17-test control receipts. No original source/plaintext was opened and no locator or verifier was executed by this reviewer. Current reviewed snapshots:

| Artifact | SHA-256 |
| --- | --- |
| Final scoped `report.md` | `4b4199298855da5b8fa550bbf95e148cc67b98f63dad8d040a701a7d50a3c0a2` |
| `validation.md` | `7414d9588a024e9e297afcc0ee42335b45bf120923cef3eda882fd960fe65ab9` |
| `verification.md` | `6e616f5a890b53c124b6a8bd91ebe341928d86f3884e89c0b6e0c01329fadd46` |
| Author `verifier01/verification.json` | `faef2ce4ea53a8a9e8b170e8621cf9e61f48eeae48c2321fa4346db956e9e0ca` |
| Root `verifier02/verification.json` | `feff5818d860f83adf07e5d1a69b2da83e736b26cf8ad2d7eab9faa466d97e27` |
| Author `verifier-controls01/receipt.json` | `cf4770b3bf3594cbbc36d713350f2652c1f14a057e6124d10b3ab6b9f652213d` |
| Root `verifier-controls-root01/receipt.json` | `8e2400b6d5865bafd953bd0adc7ebb32f482f71cee9bfb7ea4c224a9cbb19b14` |

Both historical receipts state `pass_independent_dom_exact_metadata_and_repeat_check`, the same coverage counts and unchanged input fingerprints. Both control receipts record 17 tests, zero failures/errors and unchanged input fingerprints. The author used **Python 3.14.0**; root used **Python 3.12.14**. A fresh read-only Ruby JSON comparison independently confirmed that `python` is the **only differing top-level key/value** in each receipt pair, and that each receipt's `inputs_before` equals `inputs_after`. These are not byte-identical receipts and are not falsely described as the same environment.

That comparison used `ruby -rjson -e` with the two explicit receipt pairs, computed differing keys across each key union, asserted `diffs == ["python"]`, asserted unchanged before/after fingerprints, and printed only pair names, versions and the resulting booleans. It exited 0. Fresh `shasum -a 256` commands matched all final table entries. The verification note was initially not yet saved; it was read completely once present, rather than assuming the future note's contents.

The report correctly limits the pass to extraction under the fixed contract. It does not turn the independent parser into independent historical evidence: shared source bytes, schema and Python/XML dependencies remain acknowledged. The six named-field absence statement stays distinct from eight present PointMass names; 115 unlabelled string-leaf records remain unreviewed meanings, not dismissed evidence. Excluded comments/PIs, other owners/names, unsaved methods and different versions remain possible. The missing base-loader/historical-executable caveat is preserved.

**Final interpretation disposition:** no remaining material overclaim identified in the final scoped report snapshot. The raw-source comparison gate is reported completed on the basis of the inspected receipts, not a new source parse by this reviewer. This does not establish all-method absence, historical marking accuracy, original feature identity, physical acceleration, any collapse cause, actual-human acceptance, full-investigation completion or all-Luna clearance. The report expressly leaves the broader investigation and Luna attribution work incomplete. Future substantive report edits require their own review; this disposition covers only the pinned snapshots above.
