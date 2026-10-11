# Punctuated OEM identifier check

October 4, 2026, after the initial token search and before this supplemental
search. The selected catalog's line 87 spells the organization `O.E.M.` in
a fuel-line-route entry, NYC-WTC_000171753 / 98-145. Literal standalone `OEM`
did not match that form. The entry was seen in bounded surrounding context,
not in the first match list. Preserve that distinction.

Search the same twelve files once more, with case-insensitive alphanumeric
boundaries, for `O[\s._-]*E[\s._-]*M`, `98[\s._-]*145`, and the exact
171753 identifier, optionally preceded by the known NYC-WTC prefix and zeros.
Permit multiline matching as in the first pass. Report supplemental counts
separately and retain all first-pass results. No other added identifiers,
source files, binary review or acquisition is authorized by this supplement.

The purpose is to test a now-observed naming variant, not tune a search to
prove absence. If the entry remains only a catalog reference, the one-page
official route record is a concrete next retrieval candidate, not a held
original or verified original mechanical sheet. Sheet/revision and installation
joins remain unresolved until actual source content supports them.
