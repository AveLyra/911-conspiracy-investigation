# Independent direct-Pearson method review

2026-09-13. Bounded synthetic-only arithmetic review. **PASS within the tested
core domain**, not a historical image correspondence or exposure-clock result.
No historical image/media, candidate scores, source frame tables or raw inputs
were opened. Only this review, [direct oracle](direct_oracle.py) and its
`fixtures/` artifacts were written by this arm.

## Controls, independence and checkpoint

Main AGENTS.md, WORKFLOW.md and START-HERE.md, the investigation charter,
[PROTOCOL](PROTOCOL.md) and [METHOD-01](METHOD-01.md) were read. Development-
verification and evidence-audit skills required explicit acceptance tests,
preservation of failures and separation of arithmetic verification from source
identity. No browser/UI work is relevant to this offline kernel; none occurred.

Protocol read pin:
`e445a976b664e6d2bd8c619d415cf0c1eb0ccc4866743082231b34f0a0f00537`.
Initial METHOD-01 read pin:
`53e08396b1f6919fd370c4e3faf8bc80e68f157ff8095c34d5703916a2a692de`.
The parent confirmed population variance (centered sum of squares divided by
overlap count) before producer comparison. The parent reported correcting its
initial centered-sum gate before historical evaluation; that report is not this
arm's inspection of an earlier producer or historical run.

The standard-library oracle was implemented without reading producer code.
Its corrected checkpoint and complete passing control receipt were frozen and
sent to the parent before opening `match_screen.py`. The complete 246-line
producer was then read to establish safe import and the exact callable/index
conventions. Import did not invoke image readers, screening, or producer controls.
The comparison adapter is necessarily post-producer-reading; the oracle is not.

## Mathematical/index contract

For offset `(dy,dx)`, pair template value `T[y,x]` with source value
`S[y+dy,x+dx]` only if the template mask, in-bounds condition and corresponding
source-valid flag all hold. Both masks are binary. Let this intersection have
`n` entries. Recompute **both means on that intersection**, then directly sum
centered products and squares with `math.fsum`. The score is
`sum((S-meanS)*(T-meanT))/sqrt(sum((S-meanS)^2)*sum((T-meanT)^2))`.
Coverage is `n/full_template_mask_count`; padding is unobserved, not black data.

The oracle returns all selected offsets, including rejected offsets, their
counts, coverage, means, centered sums, population variances, raw scores and
rejection reasons. Its default surface includes partially off-array positions;
the adapter selects exactly the producer's nonnegative, fully enclosed-window
positions. Source-valid holes/padding still make the effective overlap vary
within those windows. No score is clipped to manufacture a perfect match.

The producer's `correlate_valid` returns unnormalized window products. Six such
correlations recover `n`, sums, squared sums and cross-products. The centered
formula therefore has the same mathematical target as direct summation, provided
all statistics use the same valid overlap. The tested producer does so.

**Two wording qualifications:** FFT correlation is *linear rather than circular*,
evaluated numerically in binary64; it is not exact arithmetic. Also, the checked
producer accepts population variances strictly greater than `1e-8`, thus rejects
equality as well as values below it. METHOD-01 initially said “below”; the oracle
explicitly accepts positive equality. This boundary convention was reported to
the parent and is not silently declared equivalent. It does not affect the
tested nonconstant integer-grayscale overlaps. No arbitrary near-threshold or
large-offset floating-point-domain equivalence is certified.

## Actual tests and preserved failure

The first oracle execution had **15/16 controls pass**. Its sole failure was the
fixture's exact binary64 assertion `rho == 1`, not rejection of the positive
variance boundary. Separate square-root divisions rounded the score. The
[exact failed code](fixtures/direct-oracle-failed01.py) and a clearly labeled
[failed-receipt summary](fixtures/direct-controls-failed01.json) remain preserved.
Only that fixture assertion changed: require no rejection and closeness to one
at `1e-14`; oracle arithmetic and gates did not change.

The frozen corrected [oracle receipt](fixtures/direct-controls01.json) records
**16/16 passing controls**. Cases cover padding with a large excluded template
value (overlap template mean 4 instead of the global mean), full-mask coverage,
a source-valid hole, flat source/template, empty mask, count/coverage/variance
gates, positive variance-boundary convention, nonfinite/nonbinary rejection,
repeated-grid aliases and altered dynamic content with unchanged static pixels.
The periodic grid retains **18 perfect aliases**, not a unique identity. The
dynamic control retains static correlation +1 and dynamic correlation −1.

Sixty-four deterministic random small integer-array surfaces, seed 20260913,
cover **3,030 offsets**. A control-only exact `Fraction` raw-moment calculation,
enumerating pairs from the source side rather than the template side, agrees on
counts, means and defined/undefined score states. Maximum correlation difference
is `3.3306690738754696e-16`. This is finite test coverage, not a formal floating-
point error bound for all inputs.

The [comparison adapter](fixtures/compare_producer01.py) uses a separate seed,
29112008, and refuses changed oracle/producer pins. Its [saved receipt](fixtures/producer-comparison01.json)
records **73 checks passed**, comprising 71 surfaces, **1,593 offsets** and
492 finite scores. It checks full raw correlations, score admissibility, rho
and coverage against direct sums. Its random cases vary dimensions, binary
masks/valid arrays, zero versus 0.85 coverage and 2 versus 32 pixel gates.
Explicit cases add padding/overlap means, flat inputs, no valid source, repeated
geometry and static-versus-dynamic changes.

| Maximum observed error | Value | Adapter tolerance |
|---|---:|---:|
| Pearson score | `1.1357581541915351e-13` | `1e-9` |
| Coverage | `3.3306690738754696e-16` | `1e-12` |
| Unnormalized correlation | `1.1641532182693481e-10` | `1e-8` |

Producer overlap counts are represented through coverage times full mask count;
the receipt does not claim a separately exposed producer `n` array. Empty-mask
API behavior differs intentionally: the oracle emits rejection rows, while the
producer raises. Empty masks were not falsely counted as matching score surfaces.

## Actual commands, receipts and limits

Working directory: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
Executable: `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Python 3.12.14; NumPy version is recorded in the producer-comparison receipt.

```text
python3 -B research/sherlock-wtc7-investigation/peskin-figure-correspondence/direct_oracle.py --controls
python3 -B research/sherlock-wtc7-investigation/peskin-figure-correspondence/direct_oracle.py --controls --output research/sherlock-wtc7-investigation/peskin-figure-correspondence/fixtures/direct-controls01.json
python3 -B research/sherlock-wtc7-investigation/peskin-figure-correspondence/fixtures/compare_producer01.py --output research/sherlock-wtc7-investigation/peskin-figure-correspondence/fixtures/producer-comparison01.json
```

`python3` above denotes the exact executable specified above. The first command
produced the preserved fixture failure before correction. The corrected receipt
save initially encountered the worktree write-permission boundary and created
no file; an identical scoped-approved invocation completed successfully. The
comparison also completed successfully with scoped permission to save its own
receipt. Repeating the oracle receipt command intentionally produced
`FileExistsError`; its existing SHA remained unchanged. This expected rejection
is a create-only check, not a failed arithmetic comparison.

| Frozen artifact | SHA-256 |
|---|---|
| `direct_oracle.py` | `f1ecbbb6fc4c48c58786d43287ac65cdeb1a3428b93ca0ae5bec6bccf43a4e71` |
| `fixtures/direct-oracle-failed01.py` | `11528ec4cdac6be50d94ede28a795d25096b1ff671809f8933fad9be22192cec` |
| `fixtures/direct-controls-failed01.json` | `97e43a26fd32f454eb7cf30f116dac9971e20510e79d8f295be6ee8537a8c4f6` |
| `fixtures/direct-controls01.json` | `a1f0b82b35b1d4a4d5416bddd340aaac9d45da53dcb72efd76c7fd803297b813` |
| `fixtures/compare_producer01.py` | `6e36eb0d72ce1759e8900e33a457d04903f653d6ff7d8ad4a341760c8cae7531` |
| `fixtures/producer-comparison01.json` | `db673cc6d6a4fc11fc6026ffa1688ce35fd5934b83fcc7067f556b72b647f136` |
| Reviewed producer `match_screen.py` | `06a400fbb378dfa710dd86799792f8f615a40eea19e82c23b9f3e0592a3b64a8` |

This disposition verifies only the tested valid-window correlation/Pearson core.
It does not independently verify Pillow grayscale/resampling, the 13-scale canvas
mapping, mask-to-target geometry, translation signs in rendered overlays, search
exhaustiveness, candidate ranking, JPEG/source-generation robustness, dense
decoding, actual dynamic correspondence or historical timestamps. Producer
registration/resize controls were read but not run by this arm. High scores,
repeatable arithmetic and multiple computational readers do not identify a
unique historical exposure. No source acquisition, package install, browser,
runtime/global edit, canonical change, solver or transmission occurred.
