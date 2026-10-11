# Post-implementation method review

October 5, 2026. Research only. Scoped acceptance of the fixed local metadata method and its stated interpretive limits; no material correction required in the reviewed snapshot. This is not independent semantic extraction of the 24 raw inputs, historical authentication, an archive-completeness finding, or approval to acquire drawings.

## Actual review and tests

Read the complete revised [protocol](PROTOCOL.md), [query](lookup.py), [16-test suite](test_lookup.py), [report](report.md) and [execution record](verification.md). Read selected saved-result fields for accounting and controls. No PDF, source image, raw model, network response acquisition or new historical-content query was performed. The previously read evidence/source and scoped data-quality safeguards apply; the main control/charter versions remain those verified in the immediately preceding bounded review.

- Complete protocol/code read: `298a9c`, exit 0 (123 and 169 lines).
- Complete tests/report/verification read and file hashes, followed by `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_lookup.py`: `2d701f`, exit 0. **All 16 tests passed**, 0.008 s. This independently reruns the existing synthetic suite after results; it is not a pre-result test claim.
- Additional stdout-only synthetic checks and saved-result internal checks: `bca660`, exit 0. Actual interpreter: `/opt/homebrew/opt/python@3.14/bin/python3.14`. Bytecode writing was disabled. No test/output file was created.

The additional synthetic checks used `unittest.mock.patch.object(lookup, 'read', fake_reader)` so `run()` received a generated empty folder catalog and 23 generated responses, not historical records. All responses contained the same single synthetic document and subject label. Assertions passed for 23 returned appearances, one unique ID, 23 matched appearances, one matched ID, all 23 recorded memberships and zero property disagreements. Separate synthetic runs confirmed refusal of a duplicate result within one response and a malformed folder-row width. Direct `properties()` checks refused supplied folder-string values of null, list, object and boolean. Only the fixed protocol was read by the mocked `run()`.

Saved-result checks independently recomputed its internal counts and memberships, not its matches from raw metadata: 24 pins; 23 coverage rows; 302 occurrences; 208 unique IDs; per-document appearance totals matching query-ID frequencies; 11 matched appearances; eight unique matched document IDs, all classified context leads; 38 matching catalog rows, 36 labeled WTC 7; eight missing-folder appearances with eight distinct IDs; zero reported property disagreements. Both saved control occurrences of 166828 had no text matches.

## Implementation findings

1. **The declared search population and fields are implemented.** `run()` extracts exactly 24 unique paths from the protocol; catalog rows are searched through `folder` only. Search-response text is restricted by `selected_fields()` to supplied `title` and `folder_name`. Query echoes, response IDs, facets and transport fields are not searched for subject matches. Responses preserve actual result IDs, file/ordinal, supplied scalar properties and missing-search-field lists.
2. **Schema and grain are appropriately separated.** Catalog header/row width, source index and positive integer document/page counts are checked; those remain folder aggregates. Response property IDs and JSON object keys cannot repeat. Selected string fields cannot be coerced from null, object, list or boolean; required key/title/source/box fields are checked. The title/key identity check is a deliberate fixed-dataset contract, not a general parser for every possible future public title format.
3. **Missing is not literal `None`.** Omitted folder properties remain omitted and are recorded separately; a supplied string `None` remains an actual string. Matching only the observed title of a missing-folder record is not evidence of a nonmatch in the unobserved folder field. The report states this correctly.
4. **Occurrence and ID accounting are distinct.** Within-response duplicate keys are rejected. Across responses, memberships are preserved, IDs are deduplicated and property differences are separately recorded. The extra synthetic integration check tests this loop, whereas the original `test_occurrences_not_documents` primarily tests two token occurrences in one field.
5. **Substring clarification was implemented without moving the search boundary after results.** The regex retains `S-1` within `A-S-1`, `S-1.1` and `S-1-1`; the synthetic tests explicitly classify these as `sheet-token lead`, not exact standalone identifiers. Full original fields are retained for interpretation. There were no sheet-token matches in the saved result, but that outcome is not the reason for accepting the prior clarification.
6. **Coverage is preserved rather than inferred.** Requested/returned/estimated counts, results-key presence, next/previous-page flags, service termination and returned IDs are retained for every response. The saved result identifies the three capped responses as generator 50/144, punch 50/91 and penn 50/157, each `COUNT_LIMIT`. Empty response handling records whether `results` was actually present. None of this implies complete archive recall.

One bounded reuse limitation is worth retaining: `documents` stores the first occurrence's properties/matches and reports later property differences separately. If `disagreements` were nonempty, its first-occurrence summary would not resolve competing versions. Here the saved result reports none, and the report explicitly relies on agreement. This is not a material defect in this fixed result or a request for a new framework.

## Report and inference check

The eight saved document-level context leads are **166842, 167235, 167240, 167759, 167874, 168697, 173670 and 173834**, matching the report. They are not eight verified first-floor plans. The report correctly distinguishes these from the 38 catalog matches and from its shorter navigation table. Rebar labels remain lower-specificity context leads under the declared words, despite possible substantive relevance; no matching rule was retroactively widened to improve apparent recall.

The decisive contrary control is **166828**: a packet already known from earlier primary reading to contain S-S-1 is present in the searched metadata yet is a predicate nonmatch. The saved control locations are independent of token matching. Combined with the prior source reading, this demonstrates that this screen cannot support an exhaustive absence inference. It does not measure a general OCR/search recall rate. The report makes the correct narrower claim: no applicable S-1 or clearer same-revision S-S-1 was identified **by this metadata screen**, not that the drawing is absent, withheld or nonexistent.

The proposed finite public search is a separate prospective option, not a completed test or automatic acquisition permission. Exact query semantics, caps and a known-packet retrieval control would need preservation. Neither matching a first-floor label nor returning an adjacent ID would establish drawing revision, member endpoints, installation or a model omission. CO23 and CO40 remain separate. The report retains the meaningful positive context leads as well as the negative control; it does not discard them merely because the exact join failed.

No blocking inferential error was found. Final independent raw-metadata reconciliation and any closing pin/link checks remain separate work; this review does not certify those pending results.

## Reviewed snapshots

| File | SHA-256 |
|---|---|
| PROTOCOL.md | `d11b4009d5d88549cb48339cda373b156f50f97e64da5728c839084bc65c104f` |
| lookup.py | `ee178a581e73866cda97e4581e66f47306658981a31cb0bb022b2b74163ef31b` |
| test_lookup.py | `236675a9c92d6c44ae2d3f2c2dae226ab703404056b556478bc775cc0ffb582c` |
| result.json | `317f60e10c8987acffc5b6f0baed9a521deac9a2953dd6b9f9af930ff8a55219` |
| report.md | `2ab79449480f329ef1b02508dec0172b90d8495e038a689749eda4eafbb6b97d` |
| verification.md | `61401091dcf9dba15864f27147f5743be61022136938ca4bbb088214c2a6713f` |

Pins identify the reviewed bytes, not source authenticity or unchanged future report versions. Only this new method-review note was written; all reviewed files remain untouched by this reviewer.
