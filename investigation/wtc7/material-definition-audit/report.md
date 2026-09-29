# APDL01: material vocabulary is not a heat-storage implementation

2026-09-28. Research only. Source bytes control observations; the
[prospective protocol](PROTOCOL.md) controls this finite lexical test. No model
was executed and no legal record, raw input or original annotation was changed.

## Result

The inspected candidate supplies positive evidence of mechanical and thermal-
expansion property definitions. It does **not** identify the sought intact-
insulation heat-storage law. This is more informative than the earlier command
histogram, but it is not proof that the larger calculation omitted heat storage.

The producer reads all212,384 bytes/5,474 physical lines of the pinned APDL01
candidate and retains233 selected command rows:228 with wholly recognized
literal fields and five with unresolved fields. All MP/MPDATA property labels
are recognized: DENS twice, EX31, PRXY31 and CTEX31. None is C, ENTH or a
conductivity label. All five TB labels are MISO or CREEP; none is THERM or USER.
This negative statement concerns the selected literal command grammar, not
every executable way to define a property or every upstream dependency.

Line-count precision: the source has5,474 LF-split physical records but5,473
LF delimiter bytes. The final record lacks a trailing LF; the earlier phrase
"LF lines" must not be read as a count of newline characters.

Two separately implemented readers now agree on all233 selected locators,
statuses, argument counts and1,578 fields, including all five unresolved hashes.
Each reader's two successful receipts are byte-identical; root's replay of the
independent reader also matches its receipts exactly. Source/inference review
confirmed the stated counts and role limits and narrowed the next-test wording.
These are checks of source parsing, not reproduction of an engineering model.

## Located definitions and unresolved fields

All locators below are one-based physical lines in APDL01, segment1. The
source, filename and manifest hashes are fixed in the protocol; the actual
filename and arbitrary argument text are not exported. Complete recognized
fields and unresolved hashes are in [producer run01](producer-run01.json).

| Observed fields | Exact source coverage | Meaning and limit |
|---|---|---|
| MPDATA EX, PRXY, CTEX; material1 | EX67–77; PRXY79–89; CTEX104–114 | Eleven rows per label. Positive mechanical/expansion property vocabulary; not a reconstructed active temperature curve. |
| Same three labels; material2 | EX302–312; PRXY314–324; CTEX341–351 | Eleven rows per label. Material numbers do not identify physical components by themselves. |
| Same three labels; material4 | EX539–547; PRXY549–557; CTEX560–568 | Nine rows per label. No inferred material identity or unit conversion. |
| MP DENS; materials1/2 | 46,281 | Both first-value fields are unresolved and share one exact stripped-text hash. Their numerical density is not known from this audit. |
| TB MISO; materials1/2/4 | 121,358,578 | Recognized material-law vocabulary, with legacy command-position/version qualification below. |
| TB CREEP; materials1/2 | 256,493 | Positive creep-law vocabulary. Neither invocation nor effective historical creep behavior follows. |
| ET; local types1/2/5 | 27,2453,2654 | All three library-name/code fields are unresolved under the numeric-only first-pass grammar. No element identity is inferred from a hash or guessed name. |

The remaining selected rows are63 MPTEMP,49 TBTEMP and18 TBDATA. These
temperature/table commands do not by themselves distinguish heat-transfer
properties from temperature-dependent structural properties. Across all233
rows the producer preserves1,578 schema fields:1,008 blank,195 unsigned-integer,
270 numeric,100 allowlisted-label and five unresolved. Blank fields are not
silently turned into zeros or solver defaults. No table assembly, temperature-
property pairing, interpolation, reference-temperature correction or active
assignment was calculated.

## Interpretation supported by primary documentation

The official Ansys2024 R2 [MP reference](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_MP.html)
identifies EX as elastic modulus, PRXY as a Poisson ratio, CTEX as an
instantaneous thermal-expansion coefficient and DENS as mass density. It
separately identifies C and ENTH as specific heat and enthalpy. Thus thermal
expansion is not evidence of a heat-storage property: the former describes
deformation associated with a temperature change, not how heating produces
that temperature history.

The same-release [TB reference](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_TB.html)
distinguishes creep and plasticity from THERM properties; it identifies MISO
within modern PLASTIC options. The observed script instead places MISO directly
in the table-label slot. That lexical observation is preserved without calling
the historical syntax invalid or applying modern option/default rules to it.
Modern documentation supports the vocabulary distinction, not the historical
solver version, applicable units, run activation or physical fidelity.

## Coverage limits and strongest objection

The strongest objection to a mechanical-only whole-file claim is unexamined
language state and dependencies. This parser is not an APDL interpreter. It
counts36 DO loops, five IF commands and other control vocabulary without
executing them. It also counts265 TBPT commands without decoding their fields.
The producer records2,587 occurrences of26 unknown command-token hashes and
12 noncommand segments. Those are lexical buckets, not2,587 errors, absent
files or independent anomalies. No format or unmatched-quote flags occur in
this producer result; that does not certify all language semantics.

In particular, the three ET fields and two density values remain unresolved.
No dictionary attack against their hashes, source-text disclosure or inferred
element-role assignment is used to fill them. No other APDL or archive body
was read in this unit. Earlier unmatched APDL input calls were already examined
in the [thermal-transfer crosswalk](../thermal-transfer-crosswalk/report.md);
they are not newly discovered here and are not identified thermal-property
macros. Definitions, assignment, execution and historical authenticity remain
different questions.

## Claim ledger and consequence

| Claim | Layer / strength | Strongest limitation or falsifier |
|---|---|---|
| The candidate contains the stated literal labels, fields and locators. | Observed/derived;A within the declared grammar, separately reproduced. | A source-pin or field/locator mismatch would require correction. |
| The decoded labels provide positive mechanical/expansion-role evidence. | Inference;B within the documented vocabulary. | Historical-version or component/run evidence could change its interpretation or applicability. Density alone is not exclusively structural. |
| This first pass identifies no direct literal heat-storage definition in the selected grammar. | Bounded negative result;B, separately reproduced. | A missed supported row, unresolved dynamic definition or another dependency can defeat a broader absence claim. |
| NIST omitted heat storage, exaggerated heating or deliberately manipulated the collapse. | Unsupported by this unit. | Requires the actual thermal formulation/assignment and a discriminating reproduced consequence, not this vocabulary result. |

No collapse-cause ranking or causal-chain grade changes. The unit removes a
specific false shortcut: MP/MPTEMP commands in a released file do not establish
that the file contains the upstream heat-transfer law. Conversely, not finding
C/ENTH here cannot be treated as proof that the law was omitted elsewhere.

The remaining discriminating record is a version/run-linked heat-transfer
material setup: actual protection material assignments, conductivity/density/
specific-heat or enthalpy representation, units, temperature-domain continuation
and the executed solver/input identity. The next bounded local source test can
test whether the three unresolved ET library fields match a predeclared official
engineering-name allowlist, retaining nonmatches unresolved, and classify the
two density fields without evaluating them or displaying arbitrary identifiers.
Stop after these five fields: this is finite candidate-role discrimination, not
a replacement for locating the upstream thermal setup. Token classification
alone supplies neither a density value nor its units. Preserve this first-pass
result; no outcome of that narrow follow-up supplies the upstream heat-storage
law or authorizes expanding into arbitrary source text. Do not repeat the
already completed eight-input-call inventory or fill missing inputs by guesswork.

## Reproduction and preserved failures

[Producer01](producer-run01.json) and [producer02](producer-run02.json) share
SHA256 `289ad8ed8518179df34c11eec9242dda3507a205917deadb1f7fab45cd7aed14`.
[Independent03](independent-run03.json), [independent04](independent-run04.json)
and [root's replay](independent-run-root05.json) share
`57c1edcfaa1848a03ef0270a0a35952e644de7ee6bc3194be449624676b93652`.
The [comparison](compare_results.py) checks every selected field, its explicit
schema-role mapping, blank/numeric/unresolved state and retained trailing blanks.
It does not assert equality of differently defined auxiliary counters: the
independent reader has a smaller control vocabulary and hashes complete first
fields, while the producer recognizes a larger vocabulary and extracts leading
tokens. Its3,988/65 unknown-occurrence/hash buckets therefore are not the
producer's2,587/26 buckets. Neither set represents established model errors.

The [code/inference review](method-review.md) records two defects caught before
producer native reading, their fixes,25 producer tests and19 reviewer controls.
The [independent record](independent-review.md) preserves two SOURCE_CAP failure
receipts: its generic4MiB cap was incorrectly applied to a4,698,031-byte manifest,
before opening the APDL candidate. A separate exact-size/hash-checked manifest
allowance corrected that guard; the native-file cap stayed unchanged. The revised
independent code passed76 synthetic controls, replayed by root, before successful
source reads. It was developed without reading producer code/results; the shared
grammar and earlier command counts were known. Root was not outcome-blind.

See [validation](validation.md) for actual commands, failures and review gates.
No model run, legal promotion, transfer, stage, commit or push is implied.
