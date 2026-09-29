# Independent thermal-file lexical verification

2026-09-12. Exploratory WP3/Q02/Q06/Q10. This is a lexical source-role audit,
not an APDL interpreter, executable reproduction, authenticated historical
dataflow, temperature determination, or causal/intent finding. Independent
source scanning and the bounded comparison of producer `run01.json` are complete.
Disposition: **PASS for the explicitly comparable scope**, with tokenizer,
comment-counter and argument-hash differences preserved below. This is not a
claim of complete lexer equivalence or a review of a later producer result.

## Scope and independence

Fresh main AGENTS and the complete new protocol were read. The previously
read workflow, navigation and charter continue to control this isolated
research unit. The evidence-falsification-auditor, source-of-truth-guardian
and development-verification skills require reproducible source locators,
coverage limits and separation from canonical/legal facts. Main, source
files, prior units and held material remain untouched. No source instruction
is executed; no archive member is extracted; PNG body bytes are not read;
no external payload, solver, commit, push or canonical promotion occurs.

Protocol SHA-256:
`f79b1e78d01f7d4de1e994ed83d4f93b4a3a307714cdb53823be1e430ac0b34e`.
The manifest is pinned to
`30234d45e528fd5590314b3be7b0cabb632560ab56f8bbfba88c9a564139badf`,
and the thermal ZIP to
`2fdb4a54008a00cfdf6d272044090139bd1ad8b0fe71e5b1c1ed3d76caa10181`.
Three APDL sources are selected in manifest order and labeled APDL01–03.
Archive aliases use one-based central-directory positions, including directory
positions, so duplicate filenames cannot silently select the wrong member.
APDL name hashes use exact manifest relative-path UTF-8 bytes; archive name
hashes use the exact decoded ZipInfo filename re-encoded in UTF-8. Neither
recipe emits those source paths. Filename hashing is not semantic name matching.

The independent scanner was developed and tested before any new producer code
or result access. No producer function is imported. The full script was frozen
before historical processing at SHA-256
`4184493f7fc64f10bcf1509aa38324ee2d95512d1dd8282694d9015d8baf586d`.
Parent supplied source paths/pins and the agreed quote/format conventions,
not historical scan counts. The prior header audit and known NUL exception
were already known. This is software independence over the same evidence,
not an independent historical origin or blind source selection.

## Lexical method and limits

Every admitted body is read to EOF and hashed within4MiB/member,
16384bytes/physical line,512MiB total and30000archive-entry gates. ZIP reads
verify member CRCs. Directory and PNG metadata is retained, but their bodies
are not scanned. Memory is measured after execution against768MiB, not enforced
by a per-allocation operating-system limit. Operational locators are capped
at10000/file. Original bytes are never rewritten to make them parse.

A NUL anywhere excludes the entire file from semantic interpretation, even
if an earlier prefix appears textual. Its byte/hash/CRC receipt and physical
line/NUL/non-ASCII counts remain available. Thus absence of a marker in the
interpreted subset is not a claim about that omitted semantic coverage.

Physical lines use LF, with a terminal LF not creating an extra empty line.
The lexer protects single/double quoted punctuation, including doubled quote
characters. Outside quotes, `!` begins a comment and `$` separates segments.
`/COM` is counted as a comment command and its argument markers are comment
markers. Empty comments are retained as comments. Unterminated quotes are
explicit issues, with affected segments uninterpreted rather than guessed.

The physical line immediately after *VWRITE/*MWRITE/*VREAD/*MREAD is a separate
format record; blank, absent or ambiguous records remain explicit. It is not
counted as an executed BF/BFE command. Marker locations distinguish ordinary
code, comments and format text. All are literal observations, including a
keyword appearing inside quoted data: none establishes execution or export.

Only full command tokens match the declared vocabulary. Numeric data,
parameter assignments and unknown tokens are distinguished. Unknowns retain
uppercase-token hashes/counts, never arbitrary names or arguments. Known
input/output operation locators retain argument hashes, not their text.
BF/BFE/D and related TEMP labels are counted only at their literal expected
argument position; no temperature values or solver results are inferred.
Dynamic strings/macros are not evaluated, so missing literal output markers
cannot rule out every dynamically constructed exporter.

## Earlier role-reference consultation — held, not controlling

Before the documentation hold, the verifier consulted the public links below
for generic role labels and saved these brief notes. The retrieved pages carry
a proprietary/confidential footer. Parent subsequently required stopping
further use/export pending privacy resolution. This section preserves that
chronology, **not current clearance or controlling semantic support**. No full
document body was downloaded or saved here, and no further retrieval/use is
planned. The frozen scanner's role labels are an explicit lexical taxonomy;
token/count comparison does not require those pages. Current interpretive
support must come from the separate permitted primary-method review. These
later editions also do not authenticate historical implementation:

- [*VWRITE, Release2024R2](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_VWRITE.html): formatted output and an immediately following format line, with quoted text possible inside the format.
- [*CFOPEN, Release2024R2](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_CFOPEN.html): file opening for output used by CFWRITE/VWRITE; the lexical occurrence alone does not identify file content or prove execution.
- [LDREAD, Release2026R1](https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_LDREAD.html): reading results and applying loads, not by itself writing an LS-DYNA file.
- [BFE, Release2024R2](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_BFE.html): element body loading, whose meaning depends on the label and analysis context.

No later-version repeated-load precedence rule is imported into the historical
LS-DYNA thermal-assignment question. Public source dataflow and historical-build
documentation remain the separate primary-method review's responsibility.

## Controls executed before source processing

The first18 groups passed in `independent-controls01.json`, SHA-256
`f7ebe4469b42b9359efb34872d301c30c1fc96d17a03d7c976c5b6e9f24ec399`.
Three additional empty-comment, numeric-whitespace and operation-cap cases
were added before the first body scan. All21 groups passed in
`independent-controls02.json`, SHA-256
`986c34dfba614f8a804b35cc9e6dbcb464975640b973cacea4f142ac52353efa`.

Controls include quote-protected/doubled-quote punctuation, comments and dollar
separators, full-token negative matches, format lines, quoted/dynamic markers,
NUL whole-file exclusion, unknown/numeric/assignment distinctions, line/member/
operation caps, and missing/unterminated records. An actual synthetic ZIP with
two same-name entries is read by ZipInfo ordinal and retains distinct bodies.
A corrupted stored member triggers the expected CRC failure. These controls
do not substitute for the actual full-body source scan and independent
comparison, which must be recorded separately.

## Actual independent source reconstruction

The first full historical body pass completed successfully with all 21 controls
passing, in 67.684012 seconds and 109,150,208 bytes observed peak RSS. Its
create-only checkpoint is `independent01.json`, SHA-256
`20b397590bc7d2831fdc0230f045c1d42fe4a68b1f35ff1345cfea9c1eb3eab9`.
It froze before access to the new producer code or results. No historical
source-processing failure occurred. The source-run receipt pins the full
script hash given above; that old full-script version is not separately saved,
but the unchanged independent core is retained before the literal
`# INDEPENDENT_CORE_END` boundary. Its SHA-256 is
`0aff3dc9d8084b3b3002d3588e74c2cc61202e01f6def6ac8e5e8f5015424f9b`.

The archive contains 25,639 entries: 25,634 regular files and 5 directories.
After excluding 272 PNG bodies, all 25,362 non-PNG archive bodies and all 3
APDL bodies were read to EOF: **25,365 bodies and 477,970,521 bytes**. The
archive-body subtotal is 477,264,192 bytes. Original manifest, APDL and ZIP
pins were checked before and after the scan; each admitted archive body has
its own SHA-256, byte count and CRC/EOF receipt. No archive-name duplicates
occurred in this corpus. PNG exclusion is body exclusion, not a pixel finding.

Exactly one body, `ZIP15109`, is excluded from all semantic counts: 328 bytes,
all NUL, SHA-256
`7b4499c3cc6e82a9da3100028f52af7f8c1e9ee60e33010a108e401989782962`,
CRC32 3046287943. The physical byte/line/hash receipt is retained; null semantic
fields are not numerical zeros. The interpreted denominator is therefore
**25,364 files**. Physical LF-line accounting, including the NUL body, totals
7,731,417 lines. No historical format record or lexical issue was reported by
the independent scanner.

Observed literal counts in that interpreted subset:

| Literal command/label | Count |
| --- | ---: |
| BF with TEMP at its declared argument position | 2,435,737 |
| BFE with TEMP at its declared argument position | 5,240,592 |
| /INPUT | 25,136 |
| /OUTPUT | 1 |
| Either protocol target marker, code/comment/format contexts | 0 |

APDL01 and APDL02 contain no operation in the independent input/output
allowlist. APDL03 contains `/OUTPUT` at physical line 12 and `/INPUT` at lines
15, 16 and 4275–4280. These are textual locators, not evidence that those
instructions executed, that referenced files were resolved, or that the output
contained LS-DYNA thermal assignments.

## Post-freeze producer comparison

The adapter was added strictly below the frozen core boundary after the
independent checkpoint froze. It reads the two saved numeric/hash/allowlisted
results, not the historical source bodies. It imports no producer code. Later
inspection of the producer's lexical definitions informed the explicit schema
limits below; this adapter is post-schema verification, not a second blind
discovery. No September supplemental files were inspected.

The compared producer result is `run01.json`, SHA-256
`4754a59f0628a3ed91e913ce9aa5215254a4e476dcd17d9ee32e964eda2f8117`;
the producer code pin is
`c6e69416a50a20a26ac15da70fdd3cc6fb56178c07b50a35c06b4b3fb6c3cd53`.
The final verifier code, including adapter, is SHA-256
`218490aa1cf64b7cc791a27275aba5c11f11e8213f6d20a8e24f419d7cddac2d`.
`independent-comparison01.json`, SHA-256
`29113ef800f4f5bba9f2c5cf0bcf586420f2a6507eff2649bbe68810a52af64e`,
completed exit 0 with `PASS_COMPARABLE_SCOPE`, no comparable-field failures,
all 21 independent controls passing, 0.643184 seconds and 259,588,096 bytes
observed peak RSS. Frozen input-result/code pins and the core prefix were
checked. This comparison did not perform a fresh source-body reconstruction.

Exact agreements cover the 25,637 regular-record/APDL aliases and name hashes;
272 metadata-only PNG exclusions; every read body's byte count, SHA-256,
physical line and NUL count; mapped lexical/NUL status and recorded EOF/CRC
evidence; all 25,137 operation command/line/segment locators; all 25,288
per-file producer-recognized command counts against independent full-token
hash counts; aggregate recognized command and BF/BFE TEMP counts; empty target
marker and issue inventories; and the common corpus totals. The adapter
performs 329,816 integer, 51,005 boolean and 228,608 value-equality checks.
Those are comparison operations, some overlapping, **not that many independent
measurements**. Root-reported eight controls are not substituted for the 21
independently executed controls.

### Differences retained, not coerced into agreement

- **Argument-hash recipe:** all 25,137 operation hash pairs differ. The
  producer hashes the post-command suffix including its comma delimiter;
  the independent scanner hashes the argument tail after the first comma.
  Every pair and locator is preserved. No raw argument was reread or rehashed
  to a common recipe, so argument-content equivalence is not independently
  established by this comparison.
- **Comment counter:** the producer counts nonempty `!` comment tails, while
  the independent scanner counts every outside-quote `!` delimiter, including
  empty comments. The saved APDL01 counts are 1556 versus 1587; APDL02,
  3884 versus 3894; APDL03, 345 versus 361. Common blank, comment-only and
  `/COM` counters agree. The definition difference explains why equality is
  not required; no new body pass separately localized each empty-tail case.
- **Unknown-token treatment:** after normalizing known vocabularies to token
  hashes, 1,549 differing hash buckets remain across 1,539 files. Those
  buckets contain 14 producer occurrences and 1,545 independent occurrences.
  Full per-file hashes/counts are retained. The implementations differ in
  treatment of whitespace-bearing first fields and unrecognized/malformed
  tokens; every producer-recognized command count nevertheless agrees. The
  unresolved unknown-token inventory is not a complete parsed-command census
  and is not dismissed as harmless merely because recognized counts agree.
- **Uncompared semantics:** producer filename-shape classes and case labels
  were not independently reconstructed; exact alias/name-hash identity was.
  The producer's marker search uses substrings, while this verifier uses
  full-token boundaries. Both report zero actual target occurrences, but
  their generic marker-recognition behavior is not equivalent. Format and
  unterminated-quote handling likewise differ outside this issue-free actual
  corpus. No historical execution, dynamic macro expansion, dependency graph,
  or solver interpretation is established.

The synthetic malformed/unknown controls therefore protect the independent
scanner's declared behavior, not a claim that every unknown source segment is
understood. Preserving these mismatches is required by the evidence and
source-of-truth safeguards; changing the denominator or silently treating them
as full agreement would overstate the verification.

## Bounded disposition and repeat command

The shared lexical counts and source coverage are independently reproduced.
They support the narrow observation that the interpreted corpus contains
many literal BF/BFE TEMP applications and no occurrence of the two literal
protocol markers. They do not identify the historical exporter, prove its
absence, resolve dynamically generated output, authenticate an ANSYS-to-LS-DYNA
transfer path, or answer the earlier duplicate-assignment precedence question.
An input/application file and an exporter are different evidentiary roles.
This result does not establish model fidelity, physical temperature, collapse
mechanism, wrongdoing or innocence. The separate primary-method review, and
its privacy limitations, must govern any broader role explanation.

For a consumer-only repeat from the isolated worktree, use a new create-only
output name; this does not rescan the historical bodies:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/thermal-transfer-crosswalk/verify_transfer.py --compare --output independent-comparison02.json
```

This bounded independent review is terminal. No later producer result or
root-authored synthesis report is claimed reviewed here. No additional source
inspection, documentation retrieval, output transmission or new unit begins.
