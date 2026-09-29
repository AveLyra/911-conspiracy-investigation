# APDL01 follow-up: structural element names, unresolved density values

2026-09-28. Working research; additive to the preserved [first-pass audit](report.md).
The [frozen five-field protocol](FOLLOWUP-PROTOCOL.md) was reviewed and tested
before native reading. No APDL instruction or model was executed.

## Result

Both implementations identify the same three element names: BEAM188, SHELL181
and MPC184. Both density fields have arithmetic shape involving identifiers;
their values, bindings and units remain unresolved. All five classifications
and original locator/field hashes agree exactly. Each implementation's repeated
receipts are byte-identical. The five-field task is closed without extending
into more source fields or following dependencies.

This strengthens the candidate's structural-response role identification. It
does not identify an intact-insulation heat-storage law, prove that such a law
was omitted, or validate the historical collapse calculation. No collapse-cause
ordering, causal grade, intent inference or legal finding changes.

## Exactly what was read and found

All locators are physical APDL01 lines, segment1. Full candidate bytes were read
for integrity; only these five records/fields were parsed in this follow-up.
Source identity remains SHA256
e79112addea5bd623c5a213de9d4e5c89725331309746f48d48a6505e7417f64,
212,384 bytes. The exact targets and earlier field hashes are in
[followup-targets.json](followup-targets.json).

| Line | Selected field | Observed classification | Permitted interpretation |
|---:|---|---|---|
| 27 | ET ENAME, local type1 | BEAM188; official-name match | Documented structural beam family; not proof of active geometry, options or execution. |
| 46 | MP DENS C0, material1 | identifier_arithmetic | At least one identifier in the admitted arithmetic shape; no value or binding resolved. |
| 281 | MP DENS C0, material2 | identifier_arithmetic | Same stripped-field hash as line46; not an independently known density value. |
| 2453 | ET ENAME, local type2 | SHELL181; official-name match | Documented structural shell family; no active thickness, formulation or material assignment inferred. |
| 2654 | ET ENAME, local type5 | MPC184; official-name match | Documented kinematic-constraint family; no complete connection implementation established. |

The dictionary was frozen prospectively from the official2024 R2 library:
139 plain base names, with16 subtype-display labels excluded. Root independently
checked the complete transcription against the same primary page. The separate
legacy companion was unavailable; the list is not every historical element.
All three observed names matched without expanding it. See the
[source and boundary note](element-allowlist-source.md). No hash inversion,
guessed alias, quoted-name normalization or retrospective list tuning occurred.

The density classifications describe syntax only, not successful APDL
evaluation. No identifiers, expression text, numeric result, unit system or
parameter definitions were disclosed or inferred. The two density values
therefore remain unknown. Do not describe this as resolving all five numerical
inputs. The original numeric-only first-pass result remains valid for its own
grammar and is preserved unchanged.

## Primary documentation and inferential ceiling

Ansys2024 R2 describes [BEAM188](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_elem/Hlp_E_BEAM188.html)
as a structural beam with displacement/rotation degrees of freedom and an
optional warping degree; it accepts temperature inputs as loads. Its description,
Loads and Input Summary sections support this role distinction. They do not
show how a historical upstream calculation generated those temperatures.

[SHELL181](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_elem/Hlp_E_SHELL181.html)
is a structural shell, with displacement/rotation behavior and temperature
body-load inputs. Its description and Other Input sections support a
structural-response role, not identification of a heat-transfer material law.
Its stress-evaluation-only option also illustrates why a name alone does not
establish an active stiffness, mass or load contribution.
[MPC184](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_elem/Hlp_E_MPC184.html)
represents kinematic constraints and joints; its active form and constraint
method depend on options. This source check uses those general descriptions,
not modern defaults as evidence of historical choices.

The strongest limitation is the distinction between declarations and execution.
An unused or overridden ET definition can be present in a file; assignments,
branch state, later option changes, units, included dependencies and exact solver
version are not established by these five fields. The first-pass mechanical
property vocabulary plus these names is positive structural-role evidence, not
proof that every unexamined operation in this file is structural or that the
model accurately represents the building. Modern documentation is neither a
historical execution log nor an independent physical experiment.

| Claim | Evidence layer / strength | What could defeat a broader inference |
|---|---|---|
| The three pinned ET fields match the stated public names. | Observed/derived;A within the fixed grammar, separately reproduced. | Source/target/field mismatch or a demonstrated parsing error. |
| The two selected density expressions have identifier-arithmetic shape. | Derived;A for the declared recognizer only. | A grammar or token-boundary error; shape does not establish value or validity. |
| These declarations support a structural-response role. | Inference;B for vocabulary, not active-run identity. | Historical library/assignment/execution evidence could change applicability. |
| This establishes omitted heat storage, exaggerated temperatures or historical cause. | Unsupported by this unit. | Requires actual upstream formulation, assignments and a discriminating reproduced consequence. |

## Verification and preserved failures

[Producer01](followup-producer-run01.json) and
[producer02](followup-producer-run02.json) share SHA256
788b5bfebd85653978dac5b568abd54cc958e5b56f7862baa7f11aa549996f67.
[Independent01](followup-independent-run01.json) and
[independent02](followup-independent-run02.json) share
62b58c30326c78fe6f72aaf5163a26495c97e446f9f85a1ac7bbcda0bfd5ca68.
Both sets were frozen before comparison. The independent implementer did not
see root follow-up code/results before its freeze; both used the same protocol,
source selection and public vocabulary. This checks implementation agreement,
not independent historical corroboration or a blind test of collapse theories.

[Comparison](compare_followup.py) verifies all five complete rows, source and
control pins, allowed output schema and two exact repeated pairs. Ten deliberately
altered comparison inputs were all rejected. The producer's11 final tests and
independent93 controls passed. [Separate review](followup-method-review.md)
retains a pre-native line-cap defect, its correction and targeted boundary checks,
plus ten independent-route synthetic checks. An intended overwrite-refusal test
preserved the existing synthetic receipt. No failed scientific run was hidden.
See [validation](followup-validation.md) and the
[independent execution record](followup-independent-review.md) for actual commands
and the narrower meanings of these checks.

## Stop and next discriminating dependency

Do not extend this five-field result into identifier tracing or repeat the
completed eight-input-call inventory. This candidate has supplied structural
vocabulary, not the sought active upstream thermal material setup. The missing
record remains a version/run-linked specification of protection assignment,
conductivity/density/heat capacity or enthalpy law, units, temperature-domain
continuation and the generating solver/input/output identities. A matched record
could permit a declared implementation/sensitivity test; its absence cannot
be replaced with guessed inputs or called evidence of deliberate manipulation.

The next bounded source task should return to the separate unresolved
specimen-linked furnace-sag validation claim: first inspect existing coverage
and remaining public primary-reference locators, then freeze a distinct source
route rather than repeat the closed searches. Acceptance is an exact model/
specimen/thermal-history/comparison join or a documented finite negative search,
not another general assertion of validation. No new native, drawing, graph-
digitization, expert, privacy or human-review authority follows from this plan.
