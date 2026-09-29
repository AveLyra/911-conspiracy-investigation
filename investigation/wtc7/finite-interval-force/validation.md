# Finite-interval force: verification and limits

2026-09-24. Research-only. This verifies a conditional mathematical calculation,
not original footage, source calibration, actual force, or a collapse cause.

## Actual executions

From `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, root ran:

```text
/Users/admin/.pyenv/versions/3.13.7/bin/python3 research/sherlock-wtc7-investigation/finite-interval-force/calculate.py --out run01
/Users/admin/.pyenv/versions/3.13.7/bin/python3 research/sherlock-wtc7-investigation/finite-interval-force/calculate.py --out run02
```

Both exited 0, producing twelve cases and seventy-two threshold evaluations.
The output directories are create-only; rerunning those commands in this
populated checkout deliberately refuses to overwrite them. Each execution
checked fifteen polynomial/affine identities, sixteen bounded-error vertices,
all eight printing-error corners in every case, all seventy-two threshold
witnesses, and five malformed/missing/duplicate/null/nonuniform input cases.
The [receipt](run01/receipt.json) pins source table, held PDF, prospective
protocol, code and runtime before/after; all five stayed unchanged.

The separate reviewer implemented `oracle.py` without reading root's code or
results, froze and sent its hashes, then compared them. Its two actual commands,
exact control counts, same-code repeat and producer comparison are preserved
in [independent-review.md](independent-review.md). Independent here means a
separate implementation and derivation, not different historical measurements,
an uninformed question selection, or human engineering certification.

Root then read both implementations completely and ran a read-only
`/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B -` checker. It used `runpy`
with `run_name='verification_only'`, invoking `make_results(table)` and
`make_controls()` in the oracle and `calculate(table)` and `controls()` in
the producer, without invoking either file-writing main function. Both
recomputed result and control structures exactly equal their saved JSON.
Root separately compared all twelve cases and seventy-two thresholds between
implementations, including source time/row/position tokens and sign, clock
factor, half-span, both printing endpoints and both hinge coefficients.
It checked byte identity for both producer products and all three oracle
products across their two saved runs, the five producer input pins, and the
two oracle product hashes. Observed exit 0:

```json
{"read_only_replay_both_implementations_and_controls":"PASS","exact_cases":12,"exact_thresholds":72,"repeat_files_identical":5,"root_input_pins_unchanged":5,"oracle_product_pins":2,"runtime":"3.13.7"}
```

This replay also reproduces the oracle's results under root's Python 3.13.7;
the oracle's original receipt records Python 3.14.0. No library installation,
solver, network call, newly decoded media, or source modification was needed.

## Frozen artifacts

| Artifact | SHA256 |
|---|---|
| Prospective protocol | `f7595daaf9e9296979ec14b6fdcb5ebe45dee6da7243f6f5750f4dcb84934683` |
| Producer code | `d66e75a10f35413448ecf116365d868159971d0854f649de449cab5dbf98324d` |
| Producer results, both runs | `c3a79c48dff5ce9c04a25158aaf55085c76a2c6b25eabc6212eec146c6dec5c3` |
| Producer receipt | `0b02961235213d5725e7c99833b4c097c22e2f87c6d0d0e941f6249c80ff3cc8` |
| Independent code | `f0d5b88c8aa56b87f4f69e64bc18951b929ccb758c57fc0658f66625b5b18520` |
| Independent results, both runs | `e3902f6b5bf8eada0c5fa33efb54ab192e70a34668425e714118288f56b6314d` |
| Independent controls, both runs | `eed728b93f5f91b729461d45f59adb9f2468ac781bcf19fa0a873b3a929381d1` |
| Reviewed final report | `bd8b2d39f2229d8453fb1ea71dd0c8da8b45b58ca4b1fdc7037ecf542e09a44c` |
| Completed independent review | `245aca6145da097e8cd38392eab4e1f607fcbc5049e35d77421c05f2b2ab0fdb` |

Source table and held PDF hashes are in the prospective protocol and receipts.
The report's five requested precision edits were incorporated and the separate
reviewer reread its complete assembled text at the hash above. These corrected
weighted-mean language, lower-bound labels, completion wording, and integration
regularity; none changed the arithmetic. No numerical failure was observed in
the two producer runs, two oracle runs, or root's read-only replay.

## Acceptance ceiling and next discriminating task

Mathematical/conditional-table acceptance is met. Historical force measurement,
physical calibration, a specified mass system, its point/COM displacement
bound, and structural realizability are **not** verified. Printing allowance
is not a physical error budget. The four point cases cannot be combined into
one body's simultaneous history without additional evidence. No mechanism
ranking, human expert acceptance, legal fact promotion or engine activation.

Next independent task: audit whether held geometry and media can constrain
the non-affine separation of a chosen roof point from the COM of a specified
fixed material set. Read this report, the existing metric-motion and lateral-
geometry audits, and the main charter. A full-reasoning investigator should
identify the body/mass, visibility, projection and attachment dependencies;
either derive defensible bounds with their uncertainty or demonstrate the
unidentified degrees of freedom and name the minimum missing observations.
Do not insert an arbitrary deformation allowance, repeated fit variants, or
an unexplained compensating downward force as a substitute. Keep all work
research-only in this worktree.
