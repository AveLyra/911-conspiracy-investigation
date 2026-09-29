# Thermoelastic method-test verification

September 27, 2026. Research-only, standard-library exact arithmetic.
Main AGENTS/WORKFLOW/START-HERE/CHARTER control. No source PDFs, historical
thermal data or original drawings were newly inspected in this unit.

## Protocol and execution sequence

The prior source audit motivated a declared logical-transfer test. Fixtures
were constructed to test that inference, not randomly selected or blinded.
The initial protocol hash was
`020decb3dabf5327886961abdf0da5c6a8adafe3127e7446c30a738626ebaa72`.
Two independent reviewers identified an ambiguous displacement-increment
reference before numerical execution. The revised protocol explicitly reports
both d(n)-n (the probing load's cold length) and d(n)-p (the reference preload's
cold length), while the preloaded clamp always uses D=p. No numerical result
was discarded or selected to motivate the clarification.

The current frozen protocol is pinned below. Root developed `calculate.py`;
a separate agent developed `oracle.py` without reading/importing root code,
outputs or the other reviewer. A third agent froze an exact derivation without
reading either implementation or its output. All used the same declared
synthetic assumptions: independence of arithmetic, not of empirical inputs.

Root's 12 self-tests passed before its two saved runs. Each calculator produced
two separately saved, byte-identical outputs. The oracle's first output attempt
reached saving but encountered a sandbox PermissionError; no result file was
created. Scoped permission allowed both oracle saves. Root output saves also
used scoped permission. These were local authorization/execution events, not
mathematical failures. Existing destinations are create-only, not overwritten.

After independent outputs froze, root read both implementations and the frozen
derivation, then implemented `compare.py`. This is a post-freeze reconciliation
tool, not another independent experiment. The interrupted work was resumed
after the user's coordinate clarification; no protocol, program or saved
result was changed during finalization.

## Pinned artifacts

| File | SHA-256 |
|---|---|
| PROTOCOL.md | d9df71946dd097a4b6154d07fb07c8e0dff8206a91c1393f8251ceac9b817bc0 |
| calculate.py | 635b5a6b091e529e25c6c804b60fb18c46ba82705863615633890712a7131681 |
| oracle.py | 3cea4c4b1a4d9cd2efdeaeec121ff897013b1a708ff5a4fba01c822f391ab282 |
| compare.py | 2fbe5c7652989b15642d6d42b6571a7f2a207b6cc3fffddc4fa0afc2255504d3 |
| independent-review.md | 7d5b5c48225bd00e45f469046cf07e9d9db4efb3d9d1efc1a48124d741b924d8 |
| run01.json and run02.json, each 6,233 bytes | 4df08eff5cea878172efa4e2b6d5cf8d91b8310e4e4bbb92953e809c3761d5f3 |
| oracle-run01.json and oracle-run02.json, each 44,027 bytes | 349a15b2bfa9682f263c51610de4aefa22dd058b4d51d3b8c748c9f67d035e73 |

The independent review retains its initial freeze and the subsequent
pre-execution protocol clarification; its original derivation is not relabeled
as a post-result review. Hashes establish unchanged captured files, not physics.

## Actual commands and observed results

Working directory for these commands:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
Runtime: `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`,
Python 3.12.14. Below, `PYTHON` denotes that executable and `UNIT` denotes
`research/sherlock-wtc7-investigation/thermoelastic-equivalence`; these are
display abbreviations for the actual paths, not executable historical logs.

Initial completed computation phase:

```text
PYTHON -B UNIT/calculate.py --self-test
PYTHON -B UNIT/calculate.py --output UNIT/run01.json
PYTHON -B UNIT/calculate.py --output UNIT/run02.json
cmp UNIT/run01.json UNIT/run02.json
PYTHON -B UNIT/oracle.py --output UNIT/oracle-run01.json
PYTHON -B UNIT/oracle.py --output UNIT/oracle-run02.json
```

Root's commands returned exit 0 after the stated permission checks. Oracle
execution and create-only rejection are attributed to its separate agent's
receipt; root did not create the oracle outputs. Each fresh oracle run reports
125 passed checks: 105 positive controls, 4 counterexample checks, 9 expected
input rejections and 7 analytic identity checks. These are test dispositions,
not 125 independent experiments. The preserved output files support inspection.

Fresh root finalization commands, each actually rerun and exit 0:

```text
PYTHON -B UNIT/calculate.py --self-test
PYTHON -B UNIT/compare.py
wc -c UNIT/run01.json UNIT/run02.json UNIT/oracle-run01.json UNIT/oracle-run02.json
```

The 12 named root tests all pass. The comparator verifies seven fixed file
pins; root's complete `result()` payload equals its saved output. Oracle's
complete `run()` payload (nine states, all check dispositions and continuous
path) equals the corresponding saved payload. This **does not** regenerate
or independently validate the oracle CLI's descriptive metadata.

Across five common cases, the comparator checks 25 exact rational fields per
case: seven prescribed inputs (beta, three temperatures, three loads) and
18 derived values. Thus 125 fields match, comprising 35 inputs and 90 derived
values. The oracle's four extra control states are covered by full payload
replay and its controls, not by that five-case cross-comparison. Its continuous
path and root's path record are separately replayed, not included among the
125 matched fields. Root and oracle use opposite subtraction orientations in
their path polynomials; their signs are consistent with those definitions.

Comparator controls accept equivalent rational notation and reject three
deliberate unequal/malformed/non-string pairs. Exact arithmetic avoids decimal
rounding here; it does not calibrate constitutive law or empirical uncertainty.
Fresh module loading prevents oracle check-state accumulation across replays.

## Independent review and inferential limits

The frozen mechanics reviewer derived equilibrium/compatibility, exact fixture
values, iff transfer conditions, two-load identification and an all-s path
proof. It identified thermal realizability and unknown actual compliance as
the strongest limitations. This was algebraic review, not an executed script.

After freezing its own calculation, the oracle author separately inspected
root's complete calculator, comparator and saved payload, and reran root's
12 tests and the comparator: exit 0, no material mathematical/comparison bug
reported. It required explicit separation of input versus derived field
counts, run payload versus CLI metadata, and path checks versus scalar
comparisons. Those distinctions are incorporated above and in the report.
This later review is not claimed blind to peer output.

The mechanics reviewer subsequently read the complete report and this
verification record, plus the specified causal-synthesis additions. Exact
fixture values, force/reference conventions and path reasoning agreed with
its frozen derivation. It caught one compressed claim that could imply equal
compliance alone sufficed; both reports now explicitly require the accompanying
one-load match. The reviewer inspected the corrected passages and confirmed
that the issue was resolved. Its source-summary wording was also narrowed to
sag being "consistent with" finite-element calculations. No extra code,
hash, link or source-page checks are attributed to that reviewer.

Final root checks, all exit 0:

- `shasum -a 256` freshly matches all nine artifact entries/files above,
  including both pairs of saved outputs and the unchanged independent review.
- A stdout-only Python `compile` check accepts all three complete scripts;
  no bytecode or new result file is written.
- A stdout-only pathlib/re check covers ten touched Markdown files for
  trailing whitespace and conflict markers, 38 local link targets in the
  two method-test and three synthesis/scope/verification documents, and all
  19 causal-report footnote definitions. URL fragments and external sites
  are not checked; other navigation links are outside that link-check count.
- `git diff --check` passes. Main's tracked dirty-file listing is unchanged;
  main AGENTS/WORKFLOW/START-HERE/CHARTER hashes match their intake identities.

The code/output pins are immutable for this unit. Report, validation and
navigation are reviewed working derivatives, not generated result files or
new primary evidence. The repository remains on the research branch at
`2fab1389ba8529494dd206a948014cd41cbf97d2` with intentional uncommitted WIP.
The bounded next source test and unchanged gates are in STATUS. Generic
reference-state and sufficiency-premise lessons extend existing SFB-004/005
locally; the archived feedback destination is not silently reopened or replaced.

Neither a passing script nor a reviewer agreement validates
the historical NIST approximation, identifies a collapse mechanism or clears
the separate human, source-access or disclosure gates. No browser UI changed,
so no browser test was needed or claimed. No main/raw/legal/accepted-engine
change, canonical promotion, outreach, fee, disclosure, stage, commit or push.
