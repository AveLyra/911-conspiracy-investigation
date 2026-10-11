# CBS pilot synthesis review

2026-10-04 UTC. Reviewer `/root/stage2_visual`. Scientific wording review of
saved records only; no new media displays, historical computation or analysis.

## Verdict

**No outstanding material correction after readback.** The initial review
required one narrow wording correction, now verified applied. The report
fairly presents two bounded scene leads without promoting a numerical winner
to exact source identity or a physical finding.

The initial table required replacing **“Best available dynamic score and index”** with
**“Best dynamic score at each frame's best static transform”** (or equally
explicit wording). The reported Figure 142/full value 0.8463603130665975 at
564 is correct for the best static transform. The second retained transform
at that same frame has dynamic score 0.8546568037963987, however. The
initial heading could misleadingly mean the maximum over both retained transforms.
The protocol ranks dynamic scores at each frame's best static transform;
clarifying that restriction changes neither the reported number nor its leader.
At 2026-10-04 03:09:57 UTC the corrected report was reread completely: its
heading now has the requested restriction, followed by an explicit statement
that dynamic ranking does not maximize over both retained geometry alternatives.
The required correction is satisfied; the initial concern is preserved here.

## Substantive checks

- Figure 143/full static leader is 188 at 0.9892930085771138; its dynamic
  overlap is 0.7792207792207793 and its dynamic score is null. The report
  correctly treats this as **not testable under the fixed coverage gate**, not
  a mismatch, negative score or exclusion. Index 141 leads the five admitted
  full-arm dynamic comparisons at 0.8667625534404597. Static near-best members
  at 0.005 are correctly given as 118, 141, 165 and 188.
- Figure 142/full leads at 564 for both ranked metrics: static
  0.9184443190002042 and dynamic 0.8463603130665975. Its single-member near-best
  sets, parity-leader ranges, and both cross-view static ranges match the saved
  summary. Full/even/odd share leaders but remain correlated representations,
  not independent recordings. The report preserves that distinction.
- The eight-item shortlist agrees with the saved summary and root notes.
  Clip 7 indices 0 and 282 remain impaired/context-poor forced runners-up,
  not successful scene matches. The root's scores-known review is explicitly
  nonblind; no second visual reader or actual-human acceptance is invented.
- Coverage is correctly limited to 18 distinct frames, 108 combinations
  (54 paired and 54 cross-view), 24 metric groups and 72 sensitivity sets.
  The 1299 unscored frames remain unscored. Cross-view comparisons are not
  authenticated unrelated negatives or a false-match calibration.
- Exact exposure, absolute timing, glass state, fire severity, temperature,
  collapse mechanism and causal ranking remain unresolved. The proposed dense
  comparison remains a separate bounded execution step, not a completed result.

A useful optional clarification, not an additional acceptance gate: index 188's
full-arm static fit has only 0.872799137621272 overlap, while the other three
0.005-near-best static fits have full overlap within floating-point rounding.
These scores therefore do not all use identical content. The current report's
explicit non-uniqueness and missing-coverage limits already prevent a stronger
identity conclusion.

## Reviewed records and limits

| Record | SHA-256 |
| --- | --- |
| `report.md`, initial reviewed text | `fd46dc31d178dca3f29b6aec3fcf697758492f33fdf9c7da64f1ff2f3b324646` |
| `report.md`, corrected readback | `fd6a23a694c02918ba553a0c871f00938bd677cb26144473260cfd3471997905` |
| `root-observations.md` | `02ede4ebbe2eefd36476cf4ae7e5bf73adc99e02f45a60d334139ac3d07e83fd` |
| `pilot01/results.json` | `8058581b27d454bfb8b30624e620fdaecf266aa2af7d08207531aa8c903870e3` |
| `pilot01/summary.json` | `4af3dae359eeba6df1ba39bd06b44e40d95c25ef084fcbc097ee1437bdbb2bc1` |
| `artifact-review.md` | `40b83b2a3637e62af5101c9168311c43bd026642a1c7ae0d60a825d6e5fde642` |

Read the report and observation/audit text, all summary-group leader/coverage/
sensitivity fields, the shortlist, and relevant saved result rows using local
`cat`, `sed` and `jq`; checked pins with `shasum -a 256`. A long initial combined
display truncated the summary, so the relevant structured fields were reread
in compact form. No pixel scores, surfaces or artifact-audit assertions were
independently recomputed here. Runtime, storage and aggregate verification
claims are checked against the separate artifact audit, not newly timed or
executed by this reader. Root's additional direct-score verification and
synthetic-control execution are not independently revalidated by this wording
review. `execution.md` remains a separate verification record outside this
review. Only this critique was authored; no observations or results changed.
