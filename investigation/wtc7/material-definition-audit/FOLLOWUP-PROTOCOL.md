# Five-field follow-up: element names and density expression shapes

2026-09-28. Research only; additive to the preserved first-pass PROTOCOL.md and
receipts. The preceding material audit made progress; this is its finite next
test, not a new model run or a repetition of the input-call inventory. Main
AGENTS/WORKFLOW/START-HERE/CHARTER remain controlling and unchanged.

## Fixed scope and evidence boundary

Read only the same pinned APDL01 candidate (212,384 bytes; SHA256
`e79112addea5bd623c5a213de9d4e5c89725331309746f48d48a6505e7417f64`)
and its existing pinned manifest for selection/integrity. Full bytes are read
for hashing, but parse only the five declared physical lines/fields in
followup-targets.json. Preserve their first-pass segment and field hashes.
Exactly three ET ENAME fields and two MP DENS C0 fields, all segment1, are in
scope. Verify command, argument count, local/material ID, property label where
applicable, segment hash and stripped-field UTF8 hash against the fixed target
record. Any mismatch stops the test, without source text in diagnostics.

No arbitrary identifiers, density expressions, unrelated values, comments or
source filenames may be displayed or saved. No evaluation, parameter lookup,
include following, state interpretation, other native body, drawing, archive,
solver, transmission, canonical promotion or legal mutation. Stop after the
five fields whether they resolve or not. Hash matching guards identity; it is
not historical authentication. The first-pass results are not rewritten.

## Element-name rule

Before native reading, freeze element-allowlist.json and its source note from
official Ansys element-library documentation, including thermal/coupled and
structural entries rather than selecting guessed names. Take only exact plain
base names, not subtype descriptions. Record actual release and coverage;
the list is not asserted to cover every historical element. Strip surrounding
whitespace; require ASCII letters followed by ASCII digits, at most64 characters;
compare case-insensitively with this fixed set. Emit only a matching public
standard name and class official_name_match. Every other field is unresolved,
retaining its hash; do not strip quotes, guess aliases or expand the list after
observing outcomes. Do not invert hashes using candidate names.

After both independent outputs are frozen, matched names may be interpreted
using official individual element documentation. A current element description
does not certify historical defaults, assignments, execution, solver version,
loads, failure rules or physical fidelity. A coupled/contact element's name
alone does not identify its active degrees of freedom or thermal role.

## Density rule: shape only, never a value

Strip surrounding whitespace. Apply categories in this order:

1. Empty: blank.
2. More than256 characters: over_cap.
3. Either quote character anywhere: quote_bearing.
4. One signed ASCII decimal literal with optional E/D signed exponent and no
   internal whitespace, at most64 characters: numeric_literal.
5. One ASCII identifier, [A-Za-z_][A-Za-z0-9_]*, at most32 characters: identifier.
6. Otherwise attempt the bounded arithmetic shape below. If it succeeds with
   at least one identifier, identifier_arithmetic; with none, numeric_arithmetic.
7. Anything else: unsupported.

Arithmetic tokens: unsigned decimal with optional E/D signed exponent (at most64
characters); the same bounded identifier; +, -, *, /, **, (, ). Skip only ASCII
space, tab, CR and LF between tokens. Require complete consumption; at most128
tokens and at most16 nested parentheses. Start expecting an operand. In that
state, unary + or - leaves the state unchanged, ( opens a group, and a number
or identifier changes it to expecting an operator. In operator state, ) closes
an open group and leaves that state unchanged; a binary operator changes it to
operand state. End in operator state with all groups closed. Other adjacency,
empty groups, calls/indexing, commas, comparisons, percent substitution, quoted
strings and unsupported characters fail. This is a syntactic shape recognizer,
not certification of valid APDL syntax or mathematically defined arithmetic.
For example, 1/0 can have numeric_arithmetic shape without a defined value.
Parenthesized single operands enter the arithmetic category. No operator
precedence, identifier resolution, numerical evaluation or unit inference occurs.
Output only the category and original field hash, not tokens/counts or values.

## Verification and acceptance

Freeze this protocol, targets, official-name list, dependency and code hashes
before native runs. Reuse prior guarded source selection and quote-aware lexical
splitting only after checking code pins; never call their whole-source scan or
historical entry points. Preserve source size/line caps and before/after source,
manifest and control-file checks. Outputs are create-only followup receipts;
CLI/error messages are fixed codes. Synthetic tests cover quotes, delimiters,
unknown names, thermal and structural matches, expression limits, malformed
shapes, non-ASCII, privacy sentinels, pin mismatches and output refusal.

Root and a separately implemented classifier freeze their own five-row receipts
before comparison. They may reuse their respective prior source selectors and
share this protocol, targets and public list; do not claim blind discovery.
Independent code/privacy review precedes native reading. Compare all five
rows, hashes, classifications and any allowed names; run each implementation
twice for deterministic equality. Do not average disagreement or silently
widen the scope to fix an inconvenient nonmatch. Keep failed checks/repairs in
the validation record. Source parsing, independent reproduction, physical
validation and historical explanation remain separate.

## Deliverable and stopping rule

Save a bounded result/report with source-role interpretation and its strongest
objection, actual commands/results and next discriminating dependency. Link
from current research status/synthesis without promoting a cause or legal
finding. This cannot supply a missing upstream heat-storage law. Regardless
of outcome, close this five-field task and do not chase more native fields;
the actual version/run-linked thermal material setup remains a separate
dependency. No collapse-cause ordering follows from lexical classification.
