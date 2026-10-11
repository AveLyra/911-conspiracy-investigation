# First floor drawing metadata lookup

Declared October 5, 2026 before this unit's semantic search. Research only.
The previous S-S-1 rereading left the complete notched-beam mapping unresolved.
This lookup seeks an applicable underlying S-1, or a clearer same-revision
S-S-1, without assuming that a matching label establishes drawing contents,
revision, installation or model correspondence. Earlier findings are known;
this is prospective search discipline, not a blind study.

## Fixed local population

All paths below are relative to the already-held
`../municipal-originals-2026-10-04/`. No network, PDF content, OCR, images,
archives, source-code model payloads or new acquisition are in this unit.

1. `folder-document-locator/folders.json`.
2. `drawing-locator/control-response.json`.
3. `drawing-locator/skp3-response.json`.
4. `drawing-locator/skp4-response.json`.
5. `drawing-locator/sts7-response.json`.
6. `folder-document-locator/structural-response.json`.
7. `folder-document-locator/structural-front-response.json`.
8. `folder-document-locator/sprinkler-response.json`.
9. `folder-document-locator/sprinkler-front-response.json`.
10. `test-acceptance-locator/control-response.json`.
11. `test-acceptance-locator/date-response.json`.
12. `test-acceptance-locator/generator-response.json`.
13. `test-acceptance-locator/punch-response.json`.
14. `test-acceptance-locator/signoff-response.json`.
15. `job1854-followup-locator/apt-response.json`.
16. `job1854-followup-locator/break_glass-response.json`.
17. `job1854-followup-locator/control-response.json`.
18. `job1854-followup-locator/date_slash-response.json`.
19. `job1854-followup-locator/date_words-response.json`.
20. `job1854-followup-locator/fuel_pump-response.json`.
21. `job1854-followup-locator/load_shedding-response.json`.
22. `job1854-followup-locator/penn-response.json`.
23. `job1854-followup-locator/penn_phrase-response.json`.
24. `job1854-followup-locator/transient-response.json`.

The first file contains folder rows, not document rows. Search its `folder`
field only; retain source, box, counts, first Bates and one-based row ordinal.
For the other files search only returned `title` and supplied `folder_name`
scalar properties, separately, under `resultset.results`. Preserve the exact
result ID, property strings, one-based result ordinal and input-file identity.
Do not search echoed requests, available-property/facet definitions, paging
tokens or response transport metadata as if they were source descriptions.
Hash all 24 inputs. Reject duplicate JSON keys, duplicate property IDs,
multivalued/non-scalar selected fields or malformed row widths. Missing folder
properties remain missing; do not coerce them to the literal label `None`.
No missing field is an automatic nonmatch in an unobserved field.

## Fixed matching and disposition

Use case-insensitive matching on the original text with these Python regular
expressions. Matching does not rewrite source labels. The separator set in
sheet identifiers is whitespace, period, underscore, ASCII hyphen or en dash;
no OCR correction, fuzzy edit distance or inferred aliases are introduced.

```text
sheet:
(?<![A-Za-z0-9])(?:SKS[\s._–-]*S[\s._–-]*[12]|S[\s._–-]*S[\s._–-]*1|S[\s._–-]*1)(?![A-Za-z0-9])
first_floor:
(?<![A-Za-z0-9])(?:first|1st)[\s._–-]*(?:floor|fl)(?![A-Za-z0-9])
structural_context:
(?<![A-Za-z0-9])(?:structural|framing|beams?|notch(?:es|ed|ing)?|penetrations?|drawings?|sketch(?:es)?)(?![A-Za-z0-9])
```

Retain all matches, including source values other than `WTC 7`; distinguish
off-source matches rather than silently discarding them. For WTC 7 records,
an apparent sheet token is a naming lead, or a first-floor plus structural
context hit in the same record is a subject lead. A lone first-floor or
structural-context hit is a lower-specificity context lead. None is a verified
applicable drawing. Search every selected record; do not pick a top-N sample.
Treat source/box/folder as an exact context join, not source independence.
Retain repeated query appearances but deduplicate document IDs in summaries;
check repeated supplied properties for disagreement. Folder first Bates and
aggregate page counts are not substitutes for complete document membership.

As a coverage control, locate the already-known IDs 166828, 173199, 173529 and
173670 by exact first Bates/result key, independently of these text predicates.
They represent the held S-S-1 packet, May S-1 index, April comments and sketch
log respectively. Record absent control metadata as a coverage limit, not a
failed historical record. No additional content reading is authorized by the
control. Parent reports already establish capped searches and missing folders;
carry the actual per-response counts, estimates, next-page flags and service
termination into this result instead of assuming complete archive recall.

## Acceptance and next action

Deliver the frozen protocol, reproducible local query, complete matches and
coverage/pins, an independently checked receipt, and a concise disposition.
Test positive/negative token boundaries, field isolation, missing versus
literal None, duplicate/multivalue rejection and occurrence/ID accounting.
Use the existing stdout-derived JSON pattern; no new analysis framework or
notebook is needed for this scoped data-quality companion. Repository prose
remains local; no cloud Page or publication is requested.

For a plausible new record, the next separately declared source test must
establish actual sheet identity, historical date/revision, first-floor subject,
grid/member key and relationship to October15 S-S-1. May13 S-1 is not assumed
to be that revision. Otherwise report the scoped nonmatch and specify a finite
public title/content lookup as the next option; do not declare nonexistence,
concealment or expand into a folder/attachment crawl. CO23 seventh-floor and
CO40 backup questions remain separate. No exhausted image budget is reopened.

Main controls and the full charter retain authority. Source records, prior
observations and legal records remain unchanged; outputs are working research.
No cause-ranking change from metadata alone, no engine activation, sensitive
transfer, fee, outreach, promotion, staging, commit or push. The previous
coordinate response was a no-progress goal turn; this is its next safe action,
not a reduction of the investigation's completion requirements.

## Pre-execution review clarification

The independent protocol review, before semantic execution, identified that
the declared sheet expression also matches S-1 within A-S-1, S-1.1 or S-1-1.
Keep the expression and all such matches for recall, but call this category
`sheet-token lead`, not an exact standalone sheet identifier. Inspect the
complete original field for compound context in the disposition. Add those
synthetic cases. This changes interpretation before any result, not selection
after seeing hits. The initial protocol hash reviewed was
`604c43a4f1bd121d6cc5113330771fe8beda303eacfb9d1539cee9b3658e9fd8`.
