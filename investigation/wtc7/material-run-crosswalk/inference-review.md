# Independent material/run crosswalk code and inference review

Research only, 2026-09-12. This is a bounded code/inference review, not an
independent raw-source parser or solver run. The complete protocol, producer
code and its 11 controls were read. The minimized numeric run01 result was
inspected using selected cards and aggregate joins; it was not substituted
for the independent parser's source verification. No arbitrary source titles,
comments, raw bodies, held documents or external services were accessed.
Only this review file is owned by this assignment.

The repository's record/research boundary and evidence-falsification,
source-of-truth and development-verification safeguards apply. The charter
and raw files are unchanged; no legal or canonical fact is promoted.

| Reviewed artifact | SHA-256 |
|---|---|
| PROTOCOL.md | `4406af3500c495adc95edd1c86e07901f73e6cafa43a39bfc57a8920c34c552a` |
| map_materials.py | `dede959bc9f440b6b0bab8784e8c8b7c7a461cd7bcfef820487b3ff2538bc469` |
| run01.json | `b69c12ec0668c9bdf5f5ea59dbf483d2a959de7bd477c172efe69c2f03e33594` |

A root report and final independent comparison were not yet available at
this revision. Line references below use the pinned producer code.

## Positive bounded result

The missing-reference join at lines197–207 is performed over parts actually
referenced by counted element records, not all declared/unused parts. It
tests effective material IDs after the specified namespace offset and keeps
original IDs as separate fields. This is the correct distinction for the
declared static question. It is not evidence of executed, undeleted or
physically load-bearing elements in a historical run.

The selected derivative contains 23 element-referenced parts with 19 missing
effective material definitions. Their counted elements are 16,324 shell
records; all their referenced sections are present. Nineteen transformed
same-original-ID material candidates are supplied in the separate effective
namespace. They do not fill the 19 unresolved references under the declared
assembly. “No material definition with this original number exists anywhere”
would therefore be false; “no definition for this effective reference is
present in this declared static inventory” is the defensible statement.

Part98 is a useful counterexample to overgeneralization: its 1,106 counted
beam records reference section98 and material50, both supplied. The six
same-family beam-list matches are on this part. The missing-material result
does not apply to that part merely because it intersects the damage list.

The derivative's shell-list matches intersect seven of the missing-reference
parts: 712,731,742,751,761,772,803, with 206 matching shell records in total.
The remaining shell-list matches are in parts11 and27. The producer also
retains 355 discrete-element numerical matches to the beam list as
cross-family candidates. None of these numerical memberships is a deletion
action, a physical damage observation, or proof of the list's activation.
These counts should be accepted as independently reproduced only after the
separate parser confirms their scope and locators.

## Necessary scope qualifications and actionable checks

### 1. Reference absence is not zero physical support

PART cards retain all eight numeric fields, including nulls. However,
`effective()` normalizes a blank or zero SID/MID to integer0. Consumers must
read the raw `values` array to distinguish blank from explicit zero; the
normalized join field is not a physical zero property. A synthetic part
with blank SID/MID retains nulls in its card but has normalized zero
references. No selected historical missing reference in run01 is asserted
blank by this review.

An absent effective MAT definition leaves a constitutive dependency
unresolved. It does not establish zero stiffness, zero strength, an absent
physical connection, a deliberately removed column or the solver's handling
of the incomplete input. Unused definitions and same-number transformed
definitions are not automatic substitutes. A runnable historical environment
could involve another include, revision or restart; none should be guessed
or supplied to make the deck run.

Correction to avoid: do not write “the model had no supporting material in
these parts.” Use the exact missing effective-ID relationship and the
qualified inventory scope. The next discriminator is the actual effective
material source and run/dependency record that resolves each reference.

### 2. Offsets are a declared assembly assumption, not a general interpreter

Lines110–115 check the explicit include-transform shape and selected numeric
fields. The entire numeric transform cards are retained, but not every
field is part of the hard acceptance predicate. Lines261–262 then apply
+1000 to SRC-120 by caller choice, irrespective of a general include graph.
The parser does not derive arbitrary nested include transformations or
require that every parsed child was actually reached through an include.

For this source, the saved card identifies the intended SRC-120 branch and
the relevant namespace values. Independent numeric reconstruction plus the
permitted primary manual's exact field definitions must support the stated
part/material/section offsets. Nodes, elements and curve IDs are not changed
by this producer. Same-original-ID candidates are explicitly compared in
their separate effective namespace; their numerical resemblance is not
an authorized renumbering or evidence of historical material equivalence.

A synthetic unreferenced child with offset1000 is still inventoried as
part1025: this confirms the caller-driven behavior, not an observed bad
include in run01. Report “declared assembly inventory,” not “solver-resolved
complete deck.” Preserve the full transform-field values and identify
uninterpreted fields before making any broader transformation claim.

### 3. Element-family selection and duplicate coverage

The declared shell-thickness pairing correctly counts a connectivity record
once, consumes its separate thickness record, and fails incomplete pairs.
Missing required PART/MAT/SECTION/ELEMENT keyword variants fail closed rather
than silently disappearing into the inventory. Element counts are keyed by
effective PID and family; node and element IDs are not namespace-shifted.

Duplicate definitions are rejected by `insert()`, and duplicate IDs within
a damage set are rejected. The duplicate control does not test uniqueness
of all element IDs. The producer has no global or per-family element-ID
registry: two identical synthetic beam records are counted as two. Therefore
“duplicate IDs were checked” requires qualification as definition/set-ID
checks unless another independently inspected artifact provides element-ID
coverage. This is a potential counting limitation, not a finding of actual
duplicate historical element records.

The producer compares shell IDs only with the shell set, beam IDs with the
beam set, and discrete IDs against the beam set as a separately labeled
cross-family candidate. It does not search all arbitrary cross-family
combinations. A report should not call those 355 discrete matches 355 beam
elements or 355 performed deletions, nor describe the search as every
possible ID coincidence across every family.

Connectivity fields are checked for a limited numeric/positive-integer shape;
node existence, element quality, correct orientation, topology and physical
member identity are not validated. In particular, recognized *NODE bodies
are not reconstructed by this unit.

### 4. Material/section cards and curves are typed records, not complete laws

The row parser bounds fixed-width or comma-separated numeric fields,
preserves blanks and rejects nonnumeric/nonfinite fields. It does not by
itself authenticate historical field schemas, units, sign conventions,
mandatory card counts for every law, curve monotonicity or the validity of
material parameters. All material and section rows use the declared
eight-by-ten field layout; curve points use two twenty-character fields.
Current success is not evidence of universal format support.

The protocol appropriately requires a primary-source definition before
assigning a constitutive or curve-reference meaning to a particular ordinal
field. A matching curve ID and material ID do not form a reference merely
because their numbers match. A transformed counterpart's coefficient cannot
stand in for a missing law. Part98/material50 and the transformed candidate
cards can support a precise field-level comparison only to the extent that
the permitted historical documentation actually defines those fields.

### 5. Active cards, ignored keywords and omitted dependency scope

The parser ignores full-line comments and treats supported noncomment
keywords as inventory records. This is lexical activation, not historical
execution. It explicitly detects the two allowed DELETE_ELEMENT keyword
forms and rejects other DELETE_ELEMENT suffixes. Other control/initial-state,
restart, deletion or runtime mechanisms are not comprehensively interpreted;
unrecognized keyword hashes remain in the result. A synthetic unknown
control keyword is retained as an ignored occurrence, not rejected.

Consequently the empty `active_delete_cards` result means no noncomment
occurrence of those inspected DELETE_ELEMENT forms in the scanned files.
It does not prove that no element could have been removed by any historical
mechanism. SRC-116 is parsed as a separately supplied set source; this alone
does not include or activate it. SRC-118 is recognized only as an include
dependency and was not rescanned here; its prior thermal-only role must be
attributed to the earlier audit rather than newly established by this unit.

The parser rejects data after *END but does not require every source to
contain *END. A synthetic complete PART block without an end keyword is
accepted. This confirms that EOF success is bounded inventory extraction,
not a full executable input-validity certificate.

### 6. Failure preservation and prospective-selection guard

`MISSING_SELECTION` is the declared prior target set. The producer recomputes
the join and fails if that set changes; it does not simply emit the desired
list. This is a useful unexpected-result guard. It must not lead to discarding
a genuine disagreement because it is unexpected.

The current main routine writes its JSON only after all parsing, controls
and result construction succeed. It lacks the protocol's durable failure
receipt with completed-source/progress information. AuditError is reduced
to an error code, but other exceptions such as I/O/gzip errors are not handled
by a sanitized receipt wrapper. The output destination is arbitrary and
parent directories can be created; the script itself does not enforce the
worktree write boundary, though the task's actual selected output does.

These are concrete robustness/guardrail gaps, not evidence that the successful
run failed or its numbers are wrong. Preserve command outcomes externally
for any actual failures and add a wrapper in a separately declared future
revision rather than rewriting this frozen producer. No failed historical
run was independently induced or observed by this reviewer.

## Claim ledger and discriminating next evidence

| Claim | Type and strength | Limit / concrete discriminator |
|---|---|---|
| Under the declared offset assembly,23 element-referenced parts lack19 effective MAT definitions. | Derived static join; strong once independently reproduced. | A missing supported card, altered offset or differing independent join would change it; it is not a claim about all files everywhere. |
| Same-original-ID transformed definitions are present but do not satisfy the original effective references. | Derived namespace distinction. | An authenticated invocation/source mapping could establish another assembly; a number match alone cannot. |
| Part98's six same-family beam matches have a supplied section/material chain. | Derived ID match. | Does not establish historical damage activation or complete/valid constitutive behavior. |
| The historical solver removed every set member or had zero resistance at the property gaps. | Unsupported here. | Requires the actual active run state, applicable semantics and physical/mechanical evidence. |
| These absences identify deliberate intervention or validate the fire account. | Unsupported here. | Missing implementation is not an affirmative causal or intent observation. |

Highest-value next records/tests: the exact material/include or restart source
resolving the missing effective IDs; an authenticated assembly/invocation and
solver build; the actual damage activation/time record; documented field and
curve semantics for any selected constitutive comparison; and a reproducible
run-output match under those supplied dependencies. No guessed material
replacement, deletion activation or cause-ranking change is warranted.

## Review verification record

Four additional synthetic-only cases were run against the producer's Map
class loaded without calling its main or source readers: duplicate beam
records, a caller-offset part without an include, an EOF-ended PART block
without *END, and an ignored synthetic control keyword. Their observed
behaviors are described above. This is code-behavior evidence, not a second
raw-source read or independent numerical reconstruction. Producer controls
were read in full; run01 records11 passing groups. A large initial numeric
inspection display was truncated; subsequent bounded aggregate/selected-card
checks supplied the review's stated counts, and no claim of reading every
damage-match row is made. No producer or source file was modified.

## Addendum — final draft, numeric joins and primary-page check

2026-09-12. The initial review above is preserved; its prior hash was
`c8fc8e9c4406b79d5a3a483c17c4359e4a2e8a71550f7f3917e8d70a17f80aea`.
This addendum reviews the complete draft report and arithmetic code, the
method-source review, selected retained numbers and the independent
comparison's recorded scope. No raw production body was read or executed.

| Addendum input | SHA-256 |
|---|---|
| report.md | `3aa26d1afa723da8c69876ff3711964259562cf6824a142176ff93909cd7dee9` |
| method-source-review.md | `84e2c98335c2a00ee7615fe412f7eda4367fb72f84cc366185163f9d057b68e9` |
| summarize_materials.py | `b97edb66bc7a6c75b9a4e822f787014f8c3fd696b4946966dc54c68b5ba18732` |
| crosswalk-summary01.json | `5c8c8c468670a9f7c5a91e245b24e2b694636533d7ce954978d565615ecfa757` |
| independent-comparison02.json | `3997f9409c02bffc6c3d0d757da7b2b19d5336a1dcf5d27df52a2ee7f825ffcc` |

### Numeric and inference disposition

All 23 displayed missing-reference table rows match the retained arithmetic
in PID, MID, shell count, shell-list count and PART card line. The stated
16,324 shell records, 206 intersecting shell-list records out of1,543,
19 matching and four differing original PART numeric cards, 21 matching
title hashes and six same-family beams agree with the inspected derivative.
MID50 and section98's quoted numeric values were checked directly against
the retained full cards, including eight EPS/ES values, their first pair,
FAIL, LCSS, TDEL, ELFORM, CST and the TS/TT fields. This is a consumer check
of saved numbers, not a newly independent source extraction.

The completed independent comparison02 records PASS_COMPARABLE_SCOPE, no
failures,15 passing controls and zero maximum absolute numeric discrepancy.
Its coverage is four source receipts,459 part-reference rows,392 used-part
family rows,47 complete selected PART cards,24 full SECTION blocks,20 full
MAT blocks and1,904 damage matches. It explicitly does not independently
extract root curve arrays/field semantics or every unselected PART property
slot. Extra independent counterpart blocks have no full-card root comparison.
The reviewer inspected this receipt and its limits; the independent agent's
full source extraction and adapter review remain the authority for how those
checks were obtained.

The earlier comparison01 retains a FAIL/KeyError receipt with null result.
It is an adapter failure, not a source-physics discrepancy and not a passing
comparison. Preserve it in final validation alongside the corrected pass.
This addendum does not turn the initial producer's failure-wrapper or element-
ID-registry limitations into claims that actual source duplicates occurred.

The report's no-ranking sentence is appropriate. It explicitly declines to
infer exaggerated temperatures, false physical capacities, intent or a new
collapse-cause ranking from this inventory. Its counterpart discussion does
not substitute transformed laws into missing master-region references, and
its beam discussion does not call an unobserved failure attained. No material
causal or constitutive overstatement was found in those passages.

One specific wording correction is recommended: the table introduction's
bold “separate, unused” SRC-116 list can be read as established historical
non-use. Replace it with “separate, not activated in this inspected assembly”
or equivalent explicitly static wording. The inspected absence of an active
include/delete command does not authenticate historical non-use; NIST's
reported restart mechanism is a distinct unresolved link. This is an
attribution/temporal-scope qualification, not an allegation that it was used.

### Primary-page checks of the stated field meanings

The PDF skill required full-page visual review. This reviewer independently
viewed the existing public-source renders for M971 PDF1086–1089 and1502–1504;
NCSTAR1-9A PDF59,73–75,104; and NCSTAR1-9 PDF539–540. All three source PDFs
were rehashed and match the method review's pins:

- M971, May2007/Version971, SHA-256
  `f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d`.
- NCSTAR1-9A, SHA-256
  `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4`.
- NCSTAR1-9, SHA-256
  `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.

The existing render locations and reproduction commands are recorded in the
method-source review. This addendum does not claim a new download, new full
PDF extraction or historical executable match.

The manual pages support the draft's exact conditional distinctions:

- Positive MAT024 FAIL concerns plastic strain failure/deletion, not elapsed
  collapse time; TDEL concerns a minimum time-step criterion.
- Supplied EPS/ES pairs provide a stress–plastic-strain specification and
  override SIGY/ETAN; with the inspected zero LCSS and eight supplied pairs,
  zero SIGY/ETAN does not mean the law is missing.
- ELFORM1 selects the integrated Hughes-Liu beam formulation; CST1 selects
  circular tubular geometry. The selected TS fields are outer diameters and
  TT fields inner diameters, not cross-sectional areas. The manual notes
  element-level dimension overrides; a section-card interpretation is not
  proof of effective historical element dimensions.

The NIST pages support attributing simplified connection geometry, capacity
grouping, calibration of shell behavior/failure strain and added discrete
vertical support to the published LS-DYNA account. PDF104 describes material-
density scaling for the assumed live-load allocation, so the report correctly
does not treat the isolated RO value as necessarily physical steel density
or necessarily erroneous. The ANSYS break-element pages separately describe
USER102–105 and small post-failure stiffness; they do not map those types to
the selected LS-DYNA MIDs. The report maintains that implementation distinction.

These public statements are evidence of the described modeling choices, not
independent proof that every choice is physically valid, calibrated against
experiment or present in the authenticated historical input. Source units,
component-location mapping, executable version, initialization/restart and
output remain explicit limits. The proposed next calibration-source task
addresses a real dependency; it should continue distinguishing agreement
between related calibrated models from independent experimental validation.

Final validation/navigation and any later report edits remain the parent's
responsibility. This addendum covers the report hash above, not an unseen
later wording revision. Only the owned inference-review file was appended.

### Narrow final-report change check

The reviewer subsequently read the complete updated report, SHA-256
`a9afca6aa6221db2f96bb0d2720cadb7094532105f5e86661fb591b9315babcf`.
Exactly three text replacements account for the change from the reviewed
`3aa26d1a...` version: the recommended static-versus-historical list-use
qualification; an explicit distinction between root-repeated curve arrays
and independent source extraction; and fully written beam line locators
instead of abbreviated locators. Reversing all three replacements in memory
recovered the exact prior report SHA-256. No file was rewritten by this check.

These edits address the wording recommendation and preserve the established
numeric/manual conclusions. No further material source/inference correction
is requested for this report version. Final validation must still keep its
verification scope, retained adapter failure and unresolved historical/run
dependencies explicit.
