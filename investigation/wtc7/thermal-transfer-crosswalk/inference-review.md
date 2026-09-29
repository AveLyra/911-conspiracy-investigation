# Independent lexical-coverage and source-role inference review

2026-09-12. Bounded code/inference review, not a second source scan or
arithmetic reproduction. The reviewer read current main AGENTS, this unit's
complete protocol and scanner, the minimized run result, the permitted
method-source review and the verification note. WORKFLOW/START-HERE and the
evidence-falsification/source-of-truth/development-verification safeguards
control this research-only artifact. No raw model/APDL/archive bodies, held
documents or held modern help pages were accessed; no source instruction,
macro, solver or historical pipeline was executed. The held-document notice
in the verification note was read as a restriction, not semantic authority.

## Reviewed state and scope

| Artifact | SHA-256 |
|---|---|
| PROTOCOL.md | `f79b1e78d01f7d4de1e994ed83d4f93b4a3a307714cdb53823be1e430ac0b34e` |
| scan_transfer.py | `c6e69416a50a20a26ac15da70fdd3cc6fb56178c07b50a35c06b4b3fb6c3cd53` |
| run01.json | `4754a59f0628a3ed91e913ce9aa5215254a4e476dcd17d9ee32e964eda2f8117` |

Line references below are to that pinned scanner. No root final report was
present at this review's initial completion. Parent's proposed typed follow-up
is a remedy to evaluate separately, not evidence already incorporated here.
Independent full-count comparison belongs to the other verifier; this review
does not relabel its own parsing of run01 as independent historical evidence.

The saved run reports 25,362 non-PNG archive bodies plus three APDL bodies,
477,970,521 total read bytes, 25,364 lexical records, one NUL-excluded record
and 272 excluded PNGs. The NUL record, ZIP15109, is 328 bytes with 328 NULs;
the report therefore does not leave an unexamined, partly textual prefix in
that specific member. This is still not permission to reinterpret that file
as ordinary source code. Archive and manifest pins delimit the source set;
they do not establish completeness of the historical software environment.

## Main inference issue: count agreement is not semantic closure

The strongest current result is positive and bounded: the admitted text has
large amounts of literal BF/BFE TEMP-label material and structured /INPUT
occurrences, while the two preselected full literal markers were not found.
The result contains 2,435,737 BF:TEMP and 5,240,592 BFE:TEMP classifications,
25,136 /INPUT starts and one /OUTPUT start. Source-role interpretation must
use the separate permitted primary-method review rather than infer command
semantics solely from names or token frequency.

The principal unresolved material is 35 distinct hashed unknown tokens
(10,225 occurrences) and 1,561 noncommand-unresolved segments. Of those,
10,216 unknown occurrences and 25 unresolved segments belong to the three
APDL files; nine unknown occurrences belong to the extensionless archive
member. The remaining 1,536 unresolved segments occur in core/slab/slno
filename-shape classes. None is classified here by guessing its source text.
The labels “core,” “member” or “hour_driver” are anchored filename-shape
classifications, not independently established execution roles.

These counts cannot be called “all unrecognized commands”: the scanner treats
syntactically similar assignments differently depending on whitespace, and
some noncommand forms could still be relevant to indirect calls or string
construction. Conversely, they cannot be called “possible exporters” merely
because unresolved. They are a finite semantic-work list, not evidence for
either hidden functionality or its absence.

## Actionable issues

### 1. Unknown-call and assignment coverage — material to an absence claim

At lines 44 and 123–145, only a restricted token start is parsed. An
unallowlisted alphabetic command-like token is retained as a hash/count but
without source locators. A percent-delimited synthetic indirect-token form
lands in noncommand-unresolved, with no token hash or locator. No macro name,
abbreviation, parameter substitution, assignment dependency or executable
call graph is resolved. Whether a particular indirect form is valid in the
historical language/version requires separate authorized documentation; this
review does not assume that every synthetic string is executable APDL.

Reproduced on the actual pure scanner function: `parameter=7` contributes one
noncommand-unresolved segment, while `parameter =7` contributes one unknown
token. Thus the current unknown count is not a stable count of unknown calls.
Empty `lexical_flags` does not mean full syntax was recognized or validated.

Remedy: a separately declared, bounded classification of these unknowns and
unresolved segments. Match hashes only against a fixed, non-sensitive command
dictionary; retain per-file/line/segment locators for unmatched token hashes;
distinguish anchored syntactic assignments and punctuation from unresolved
command-like starts without evaluating expressions. Do not assume every
unmatched token is a macro, or turn a dictionary match into version-specific
semantic or execution certification. Parent's proposed follow-up has this
appropriate scope. Do not rewrite this frozen lexical result after resolving
some of its labels.

### 2. Operational allowlist and input/output routes — material to closure

OPS at lines 24–26 is narrower than VOCAB. For example, *TREAD, PARSAV,
PARRES and SAVE are counted vocabulary but produce no operational locator or
argument hash. This is a coverage distinction visible from code, not a new
claim about their historical command semantics. A synthetic four-line input
containing those tokens produces all four counts and zero operations.
Those four tokens do not appear in run01's recognized aggregate counts, so
this particular omission does not create an observed missed occurrence.

Other recognized transfer/control vocabulary also receives counts rather
than argument-role locators. Command families not in VOCAB are merely hashed.
Any dictionary expansion should deliberately consider file routing, database
save/restore, table/text I/O, macro/abbreviation definition and invocation,
and external delegation, with authorized historical semantics kept separate.
No unrestricted token dump is needed to do that safely.

The 25,136 /INPUT operation records retain source line/segment and argument
hashes, not parsed targets or dependencies. A repeated argument hash is not a
proof of a particular opened member. Exact string matching alone also cannot
decide active working directory, omitted extensions/defaults, parameterized
filenames, case sensitivity, library search order or macro environment.

The single /OUTPUT at APDL03 line12 has the same limitation: run01 does not
identify its actual destination or resulting bytes, whether subsequent
listing/output forms could reach it, or whether any of it was executed. It
must not be called either a proven thermal exporter or definitively harmless
logging from this record alone. Ordinary solver/native output or an external
generator are also outside a literal text-keyword audit's execution evidence.

Remedy: quote-aware typed argument parsing, with output limited to anchored
safe extension/shape classes, exact target hashes, syntactic flags and
candidate source-ordinal matches. Distinguish exact, normalized, dynamic,
ambiguous, absent and unmatched cases. Match only the already inventoried
manifest/archive universe: no path following or source execution. Basename
matches are candidate links if duplicate or context-dependent. This can
improve a static dependency crosswalk; it cannot establish historical
invocation, reachable branches or complete runtime dependency closure.

### 3. Format handling — reproduced edge cases, no observed run01 exposure

Lines 116–121 consume the next physical line as format material whenever a
recognized format-bearing command occurred. If the next line starts with
*CFOPEN, it is flagged `format_candidate_unexpected_start` but not counted
as a possible command. That preserves a warning but not alternate parsing
or a command locator. The boolean expectation does not describe a general
language parser or validate all multi-command/multiline constructs.

The format branch appends the entire unstripped text to `code_marker_parts`
while the separately split comment remains in `comment_parts`. The synthetic
two-line input below yields the same thermal marker once as code and once
as comment:

```text
*VWRITE,1
(A) ! *LOAD_THERMAL_VARIABLE_NODE
```

This is a real code/comment-role contamination under the scanner's own
declared comment convention. A format record should have a distinct role;
its comment should not also become code evidence. The protocol expressly
requires separating such lexical material.

No format rows or any of the four recognized format-command counts appear
in run01. Therefore these reproduced defects do not currently change its
recorded marker miss or operation totals. Do not manufacture a historical
parser failure from a synthetic example; retain the issue for future code
and robust ambiguity handling. A follow-up should explicitly invalidate
strong negative claims if an ambiguous format boundary is encountered.

### 4. Exact-marker and numeric-start coverage — bounded lexical miss only

The two marker byte strings at lines 42–43 are not a general inventory of
thermal-output routes. Full literal strings are sought, including inside
quoted data, with code/comment location. The writer could in principle
construct text from fragments or rely on a separately supplied header; the
lexer does not concatenate or evaluate either. The synthetic *VWRITE using
separate `'*LOAD_THERMAL_'` and `'VARIABLE_NODE'` string fragments produces a
writer-command count but zero full-marker matches. This demonstrates lexical
coverage, not that this source contains or executes that construction.

The numeric classifier at lines 45/144 accepts a numeric *prefix*, not a
validated numeric record. Synthetic `12SYNTHETIC` is classified numeric data
without a flag. Numeric_data_segments therefore cannot support a claim that
all those records contain only numeric data. Similarly, TEMP-label detection
uses a comma split and literal label position, not complete field typing,
unit validation, selection-state evaluation or temperature computation.

The scanner also assumes LF physical lines and Latin-1 byte decoding; CR is
stripped only at the end of those lines. Encoding/line-ending assumptions
and restricted token grammar are not independently certified by a clean
lexical-flag count. No actual historical encoding defect is alleged here.

Remedy: report “neither selected full literal marker was found in the
interpreted text under this lexer.” Preserve recognized writer-command
counts independently of marker matches. Use separately validated full-field
typing only when needed for a specific role question, never general dynamic
evaluation as a shortcut to semantic closure.

## Permissible conclusions and disconfirmation tests

| Claim | Assessment | Decisive reason / next test |
|---|---|---|
| The saved run contains the stated lexical counts and selected marker misses. | A for the inspected derivative; primary-body reproduction is the separate verifier's task. | Scope is the pinned finite files and declared parser, not historical execution. |
| The files contain substantial input/loading material consistent with the separately documented ANSYS structural thermal-load branch. | B when combined with the permitted primary-method semantics and typed role checks. | Positive BF/BFE TEMP and driver-like /INPUT patterns support the role; file labels and counts alone are not the entire proof. |
| This pass has not identified the routine producing the released LS-DYNA nodal-temperature input. | B as a bounded investigation status, not proof of absence. | An identified writer/mapping routine plus upstream/destination linkage would reverse this status. |
| The files are only loaders, contain no exporter, or close every executable dependency. | D / not established. | Unknowns, unresolved segments, unparsed routing, external dependencies and execution state remain. |
| The LS-DYNA temperatures necessarily came from completed ANSYS structural-response results. | E as an inference from this pass. | The permitted method review distinguishes a separate LS-DYNA thermal-load set and a structural-damage transfer branch; neither scanner nor review proves that asserted source path. |
| An unmatched routine proves incorrect temperatures, deliberate withholding, concealment or a collapse mechanism. | E / unsupported by this work. | Missing implementation identification supplies no affirmative error, intent or causation evidence. |

The highest-value concrete link remains implementation and invocation evidence
for source thermal results → destination LS-DYNA identifiers/geometry → spatial
association/selection → serialized nodal-temperature cards, including time,
units, version and repeated-row handling. A typed static match advances only
the links it actually establishes. Later historic run records, source code
or a reproduced mapped-output match could corroborate or falsify that bridge.
Do not require a single monolithic exporter; the implementation may be a
chain of programs or routines.

## Verification of this review

Eight synthetic byte cases were executed against `body_scan` loaded with
`runpy.run_path(..., run_name='inference_synthetic_only')`. The guarded main
was not invoked, and neither `historical()` nor source-reading functions were
called. Tests were assignments with/without whitespace; four known but
unlocated vocabulary tokens; ordinary/delimited synthetic unknown starts;
format consumption of a command-looking row; format-comment marker roles;
fragmented quoted marker text; and numeric-prefix acceptance. Expected and
observed behavior is explicitly described above. This tests lexical edge
behavior only; it does not rerun or duplicate historical counts.

Only this file was written by this assignment. Producer protocol/code/results
remain unchanged. No browser was needed for this code-only review, and no
external semantic documentation was newly consulted. Root should review any
final report against these boundaries and incorporate independently verified
typed follow-up findings as a new result, not silently upgrade run01's scope.

## Addendum — report and completed typed follow-up review

2026-09-12. This addendum preserves, rather than replaces, the initial review
above. Its initial SHA-256 was
`419e3d02f2c8a40c0f6b1aeb817131a09a1eeff56d7644163483e75a2672c7bb`.
The reviewer now read the complete root report, full `crosswalk_details.py`,
its complete detail protocol and the independent supplement's full code;
inspected both detail outputs and the supplement's receipt, counts, limits
and selected records as minimized derivatives. No raw source body was revisited and
no new source scan, solver or external-document access was performed.

| Artifact reviewed in this addendum | SHA-256 |
|---|---|
| report.md | `100e25e81fa20598280ad68864b20140c91e46da6b6895f08322bfb1091d814a` |
| crosswalk_details.py | `a097aa7eb31fcab07ed57ec0dda123bcaae473e35698eca1804f74dd2d8b99e6` |
| DETAIL-PROTOCOL.md | `1ff4718d1b5dfb1eee7e3a313dfc49a4ec3ffb5ce5a2cb3666fdebb8d7fa2f11` |
| details02.json | `4072b415f7197a7c1bf9b4da8bc820d6dd5ae9e6f08422d823ffd0b4bb815f64` |
| details03.json | `a9d15ec021e306c2f9b9ee89422c459ad0b14439d35c8d4f207481ed094b7fdf` |
| verify_transfer_supplement.py | `70a67f093a7168ea8c11beb950233ea868ccbd622addf1f7b041d1a7be918df4` |
| independent-supplement02.json | `6ba520481f1f52e70124d451baa637dab3c7b1f2f2ba8f0f19b786f7e6b6693c` |
| verification-review.md, before root's supplement update | `75ae650b52f3cae1d5a6ff8b070fe78d2e5d23763713bb43d479ce274e578277` |

### What the new evidence legitimately advances

Both successful producer detail outputs retain 1,864 selected bodies and
469,040,000 bytes. The fixed supplemental vocabulary accounts for 9,849
prior unknown-token occurrences; syntactic assignment rules account for
five more there and 25 previously noncommand segments. The remaining producer
counts are exactly 371 unknown occurrences and 1,536 unresolved segments,
all the latter at physical line1. This confirms the report's stated
denominators without relabeling unknown expressions as harmless geometry.

The current follow-up code checks an exact leading EFBBBF prefix; details03
has zero positive results. The independent supplement also reports zero
leading BOMs, classifies all 1,536 residual segments as unresolved ASCII
syntax, and classifies the remaining 371 unknown occurrences as full
identifier-token syntax. Therefore “unresolved” now has a narrower known
syntactic scope. It is still not an identified command or a meaning/execution
finding. A generic BOM explanation is affirmatively unsupported here; no
encoding failure follows from that negative test.

Both successful detail outputs contain exactly these candidate groups:

- 25,032 /INPUT operations with .int classification: three exact basename
  candidates each and one same-archive-parent candidate.
- 96 /INPUT operations with .int classification: one candidate, same parent.
- Eight /INPUT operations with .apdl classification: zero candidates.
- One /OUTPUT operation with .out classification: zero candidates.

Every inspected operation has two argument fields and neither declared
percent-substitution nor path/directory flag. Those syntactic checks do not
cover all defaults or indirect language mechanisms. Exact candidate alias
matching now resolves a real gap left in run01's hashed arguments; it does
not resolve working directory, execution, semantic branch reachability,
renamed equivalents or the complete historical dependency environment.

The independent supplement records PASS, no comparison failures, all 18
declared controls passing, identical source pins before/after, 1,549
reconstructed differing hash buckets and 25,137 independently reconstructed
operation argument/candidate records. Code inspection confirms that it
rederives both hash recipes from each selected source segment and checks
field hashes, extension classes, syntax flags and candidate aliases against
the saved producer details. This is stronger than merely acknowledging
that the old argument hashes used different delimiters. It establishes
their correspondence under both recipes, not equal hash values or complete
lexer equivalence. The 318,922 comparison operations are not independent
historical measurements.

That supplement compares details02 and performs its own BOM check; it does
not name details03 as a pinned dependency. Do not call it a byte-for-byte
verification of the entire details03 result or its later producer code.
The recorded controls and code support the targeted scope actually compared.
The parent is responsible for preserving the separate original/control
versions and any source-run failure receipts in final validation.

### Report disposition and precise remaining correction

No material source-role, physical or causal overstatement was found in the
pinned report. Its “ANSYS-compatible temperature-loading material” conclusion
is explicitly nonexclusive, supported by the separate permitted primary
methods and positive syntax/candidate patterns. The eight unmatched APDL
references are qualified as an exact-name gap in a selected inventory; the
report does not equate that with nonexistence everywhere. The .out extension
is correctly treated as insufficient to establish generated content, a
thermal exporter or harmless logging. The zero-marker finding, unmet
mapping/run bridge, repeated-row uncertainty and unchanged causal ranking
remain explicit.

One concrete completeness correction is needed in the pinned report's last
verification paragraphs: they still describe only the original partial
comparison and defer to a later final verification disposition. Add the
completed supplement's affirmative result directly, while retaining the
original differences as history. Suggested substance:

> The post-schema independent supplement reconstructed all 1,549 differing
> hash buckets and all 25,137 operation argument/candidate records from the
> same pinned source bodies. It confirmed both delimiter-dependent hash
> recipes and the typed candidate results without equating the two lexers.
> It narrowed 371 remaining occurrences to identifier-token syntax and
> 1,536 first-line segments to unresolved ASCII syntax, with zero leading
> UTF-8 BOMs. These remain semantic limits, not exporter or execution findings.

The parent indicated that it is incorporating this update and final
validation; that proposed edit is not silently included in this addendum's
report hash. Later report versions require a narrow change check. The
initial review's “argument-content equivalence not established by run01
alone” concern is now addressed by this targeted supplement, while its
historical execution and semantic-closure cautions remain applicable.

Only this addendum was written. A read-only metadata-inspection helper first
assumed a controls-only JSON result was an object and exited with TypeError
after reporting the preceding results; the corrected helper explicitly
handled null results and completed. This was a review helper failure, not a
historical scan/control failure or a reason to rerun source processing.
