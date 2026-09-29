# Independent R1 method and synthetic-arithmetic review

2026-09-24. Bounded research preparation, not an accepted historical
measurement, resolved reproduction, human review or causal finding.

## Scope and authority

This reader reviewed the complete corrected `PROTOCOL.md` and
`interval_controls.py`, replayed the synthetic-only test entry point, and ran
additional synthetic assertions in a stdout-only Python invocation. No source
image, new observation record, historical placement input or historical
calculation was opened or executed in this follow-up. Only this review was
authored. Main, raw sources, old protocols/annotations, producer code and
other owners' files remain untouched.

The main CHARTER controls. The evidence-falsification and source-of-truth skills
and their linked checklists were applied to keep mathematical verification,
candidate annotation, historical measurement and acceptance separate.
Earlier read-only prioritization reviewed current STATUS and the completion
audit's WP2/WP3/comparator sections; it did not independently remeasure their
results. That required comparator review exposed its embedded old numerical
table. This reader therefore does not claim numerical blindness and is not
acting as an independent historical annotator here.

## Original objection and corrected disposition

The original protocol, SHA-256
`ea7987cec989c7af7220492f4d21a563ce350167b10e2ce51623fa650b1bf597`,
deferred consequential structural/support-force/WTC7 use but permitted a
historical numerical reproduction/failure determination beforehand. The
objection was that the comparator-level evidentiary finding is itself
consequential; deferring a larger causal claim does not satisfy the charter's
requirement for human spot-checks before consequential automated measurement.

The corrected protocol, SHA-256
`2bbc5777dd39dde42a2945d1d049a1a46f8c4b61678308e328e803f0ffa2331a`,
now explicitly requires an actual human check of the exact native
feature/coordinate/envelope mappings **before historical numerical application
or a reproduction assessment**. It permits source checks, separately frozen
candidate placements and synthetic controls meanwhile. Final acceptance
includes the human check; until then the numerical test and old-table
comparison remain unrun. This resolves the identified gate defect in the
written protocol without weakening final acceptance or retroactively supplying
review. Root reports making this correction before historical image views;
this reviewer did not independently reconstruct the viewing chronology.

The reuse of a prior-informed second reader and uncertain prior exposure are
now explicit. Separate freezes can protect against exchange of new results;
they cannot establish event-level independence, numerical blindness or
independent historical evidence.

## Arithmetic assessment

For valid inclusive placement intervals, the implemented difference is

`[Rt.low - Bt.high - R0.high + B0.low,
  Rt.high - Bt.low - R0.low + B0.high]`.

This is the tight range of `(Rt - Bt) - (R0 - B0)` over the Cartesian product
of those four intervals. It is not a statistical confidence interval. Unknown
correlations do not justify narrowing it; a shared baseline also makes
successive frame comparisons dependent, not independent probability trials.

- Envelopes admit integer native y coordinates from 0 through 719, reject
  reversed/out-of-range/non-integer and boolean bounds, and retain `None` as
  missing rather than zero.
- `qualified_difference` checks all four identity states. An ambiguous or
  unlocalizable point yields unresolved even when bounds were supplied. A
  nominally localizable point with null bounds also yields unresolved.
- `both_positive` requires a strictly positive lower endpoint for both
  reference comparisons. Zero at either lower endpoint does not qualify.
- `confirmed_runs` checks three distinct increasing native indices differing
  by exactly one, with both references positive in all three rows. It returns
  every qualifying three-frame start; four consecutive positives legitimately
  yield two overlapping starts. Nonconsecutive selected positives do not
  qualify. A missing/zero-overlapping/disagreeing reference breaks confirmation.
- The code is a small synthetic helper, not a historical ingestion/schema
  validator. `both_positive` expects properly formed derived intervals;
  `confirmed_runs` validates ordering/uniqueness/type, not every possible
  malformed row or the full admitted-frame set. This is not an identified
  defect for the present synthetic-only scope. Any later historical adapter
  must validate its exact source/annotation contract rather than treating these
  helpers as an ingestion gate.

No arithmetic correction was identified within that declared domain.

## Actual verification

Workdir:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.

Read commands were bounded `sed` on the complete protocol/code and `rg --files`
for local test/control names. `shasum -a 256` checked the protocol and code.
The replay command was:

```sh
python3 -B research/sherlock-wtc7-investigation/comparator-r1-replication/interval_controls.py -v
```

Exit 0; all **13 tests passed**. Coverage includes singleton zero, common
translation, positive intervals, strict zero boundary, reference disagreement,
each missing operand, identity loss, invalid envelope/state, consecutive versus
nonconsecutive indices, missing middle reference, duplicate/reordered indices,
and endpoint enumeration of all 256 four-envelope combinations.

An additional independently authored stdout-only check, executed after reading
the implementation, used Python 3.14.0 and passed **369 assertions**:

- 256 combinations checked against exhaustive scalar evaluation of every
  integer in each small synthetic interval, not the implementation's endpoint
  formula;
- all 81 four-point identity-state combinations;
- a null bound at each of the four otherwise localizable points;
- all 16 combinations of missing, negative-lower, zero-lower and positive-lower
  reference results;
- six empty/short/consecutive/nonconsecutive index sequences;
- six middle-frame failures covering both references and missing/negative/zero
  lower bounds.

The exact additional invocation was:

```sh
python3 -B - <<'PY'
import importlib.util
import itertools
import sys
p = 'research/sherlock-wtc7-investigation/comparator-r1-replication/interval_controls.py'
spec = importlib.util.spec_from_file_location('r1_synthetic', p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
checks = 0
choices = [(0, 0), (0, 2), (3, 5), (7, 7)]
for boxes in itertools.product(choices, repeat=4):
    admissible = itertools.product(*(range(lo, hi + 1) for lo, hi in boxes))
    scalar_results = [(r - b) - (old_r - old_b) for r, b, old_r, old_b in admissible]
    assert m.difference(*boxes) == (min(scalar_results), max(scalar_results))
    checks += 1
states = ['localizable', 'ambiguous', 'unlocalizable']
for status in itertools.product(states, repeat=4):
    pts = [(s, (10, 12)) for s in status]
    expected = (-4, 4) if all(s == 'localizable' for s in status) else None
    assert m.qualified_difference(*pts) == expected
    checks += 1
for missing in range(4):
    pts = [('localizable', (10, 12))] * 4
    pts[missing] = ('localizable', None)
    assert m.qualified_difference(*pts) is None
    checks += 1
ref_values = [None, (-1, 4), (0, 4), (1, 4)]
for a, b in itertools.product(ref_values, repeat=2):
    expected = a == (1, 4) and b == (1, 4)
    assert m.both_positive(a, b) == expected
    checks += 1
positive = (1, 2)
for indices, expected in [([], []), ([0], []), ([0, 1], []), ([0, 1, 2], [0]), ([0, 1, 3], []), ([4, 5, 6, 7], [4, 5])]:
    assert m.confirmed_runs([(i, positive, positive) for i in indices]) == expected
    checks += 1
for middle in [None, (-1, 4), (0, 4)]:
    for missing_ref in [0, 1]:
        pair = [positive, positive]
        pair[missing_ref] = middle
        rows = [(4, positive, positive), (5, *pair), (6, positive, positive)]
        assert m.confirmed_runs(rows) == []
        checks += 1
print('python=' + sys.version.split()[0])
print('independent_synthetic_assertions=' + str(checks))
print('result=pass; historical_inputs=0; image_views=0')
PY
```

Output: `python=3.14.0`, `independent_synthetic_assertions=369`,
`result=pass; historical_inputs=0; image_views=0`; exit 0. This is a second
analytical check of synthetic arithmetic, not a pre-implementation blind oracle
or another historical measurement. No new receipt/framework files were created.

## Remaining gates and inferential ceiling

The 13 tests and 369 assertions do **not** check whether an AI reader can
correctly localize an image feature, read the native display coordinates, or
assign an adequate uncertainty envelope. The appropriate synthetic
display/localization control and actual human mapping check remain pending.
A software pass, source-pin agreement, generic approval or two AI readers
cannot supply either. This review does not authorize historical numerical
execution.

Even after those gates, the proposed result concerns positive-by apparent
R1 displacement relative to the declared scene references. It cannot recover
physical onset from earlier non-detection, establish stationary reference
geometry, remove rotation/parallax, authenticate capture cadence, or determine
support-removal timing or WTC7 cause. Both references constrain a narrow
common-motion alternative; they are not a complete camera model. The selected
six frames and shared baseline also do not establish a matched comparator
population or independent causal probabilities.

## Reviewed pins

| Artifact | SHA-256 |
|---|---|
| Main CHARTER.md | `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd` |
| Original protocol snapshot, read in prior review | `ea7987cec989c7af7220492f4d21a563ce350167b10e2ce51623fa650b1bf597` |
| Corrected PROTOCOL.md | `2bbc5777dd39dde42a2945d1d049a1a46f8c4b61678308e328e803f0ffa2331a` |
| interval_controls.py | `19de6bc2227005053397a1d3c26d9a1920108a0759bada60d22e4ee036c840a0` |

Disposition: **gate correction accepted as written; synthetic arithmetic
verified within scope; historical replication remains pending**.

## Local review-server follow-up — 2026-09-24

The user subsequently reported that the existing viewer could not provide
reliable pixel coordinates. Root's `viewer-scope.md` defines a bounded local
coordinate-review tool, not a human mapping pass. This reviewer read that
scope and the complete `serve_review.py`, authored only `test_server.py`, and
appended this section. The development-verification skill governed focused
tests and the separation of HTTP behavior from browser/UI acceptance.

### Static objections and their disposition

The initially inspected server had two narrow hardening gaps: its successful
responses received restrictive policy headers but its `send_error` responses
did not; and malformed absolute request targets could cause `urlsplit` to
raise instead of returning a controlled refusal. These were reported to root.
Root changed `end_headers` to supply the headers on success and error paths
and made `route_key` catch `ValueError`. This reviewer reread those changes.
They were implemented before any HTTP test reached a handler; there is no
executed pre-fix HTTP failure claimed here.

The source defines exactly nine routes: six named historical PNGs, one
synthetic PNG, the HTML root and its JavaScript. Historical/control images
have fixed expected hashes; HTML/JavaScript are pinned to their bytes when
`routes()` starts. Therefore live changes are refused, but a restart does
not compare UI bytes against an immutable prior audit manifest. Root's exact
deployed-version receipt remains necessary. This test suite does not call
`routes()` on the historical/UI files or independently recheck those images.
Its nine-route fixtures test handler behavior; source inspection supplies
the actual route-construction account.

### Tests actually run and retained execution failure

Command, from the worktree root:

```sh
python3 -B research/sherlock-wtc7-investigation/comparator-r1-replication/test_server.py
```

Runtime: **CPython 3.14.0**. No external requests, browser sessions or historical
image views were performed by this reviewer. Each HTTP test serves only
explicit temporary dummy bytes on an ephemeral `127.0.0.1` port, using the
built-in HTTP client. Tests remove only their own temporary fixture files;
the server has no test-authorized write path. Entry-point checks mock route
loading and the server constructor rather than loading actual assets.

First attempt, default sandbox: exit 1, **20 tests run, 2 passed and 18 setup
errors**. All 18 HTTP tests stopped at `socket.bind` with
`PermissionError: [Errno 1] Operation not permitted`. No handler assertions
ran in those 18 cases. That is an execution-permission limitation, not evidence
that those server behaviors passed or failed. Initial test-file hash was
`cef467b3cdedea5f1fe392b12003aa413f43c3ed35d5a292a908181caf2567b7`.

A one-line `addCleanup` registration was then added so fixture cleanup also
runs if setup fails. No assertion or acceptance criterion was relaxed. The
same command was rerun through a narrowly scoped permission escalation for
ephemeral loopback fixtures. **Exit 0: all 20 tests passed** on the corrected
server. The second run exercised:

- GET for all nine whitelisted dummy routes, exact payload/content type/length;
- HEAD with matching content length and no body;
- unknown paths, directory-like paths, existing but unlisted files, literal
  and encoded traversal, encoded slashes, queries/fragments and absolute targets;
- a malformed absolute target returning 404 rather than disconnecting;
- wrong Host values and different/null Origin values returning 403, with
  exact same-origin requests permitted;
- POST/PUT/PATCH/DELETE/OPTIONS returning 501, with fixture bytes unchanged;
- changed, missing or same-byte symlinked assets returning 409, including HEAD;
- no-store, nosniff, no-referrer, same-origin resource policy and restrictive
  CSP headers on success and representative 403/404/409/501 errors, with no
  `Access-Control-Allow-Origin` header;
- no directory listing or unlisted fixture-body exposure;
- mocked entry-point binding to `127.0.0.1`, server closure, and invalid-port
  refusal before route loading.

`shasum -a 256` checked source/test/scope pins after the successful run. The
server hash was the same corrected version in both test attempts. The exact
pins reviewed are:

| Artifact | SHA-256 |
|---|---|
| serve_review.py | `1ea233c4fa8074298f9791a305fa46f0b1ac3151ce00ce48c8edd7e99de48142` |
| test_server.py, final | `2ab32ba83583958b49ebbdb36b8a5327d47b02da2a7b995a4551588a402aa6a8` |
| viewer-scope.md | `913b02ea5c820e9eba75f7c2a7b01d8b5adac91ba9029f44c5f55bc166aa6645` |

### Security, UI and scientific ceiling

The tested Host/Origin checks, exact allowlist and response policies constrain
ordinary cross-origin browser access and rebinding-style requests using a
different authority. This is not a comprehensive security certification,
authenticated application, encrypted channel, resource-exhaustion test or
proof against every HTTP-parser/browser edge case. A local process can send
the allowed Host and Origin; same-user processes able to alter code/files
are outside this boundary. `ThreadingHTTPServer` is a small local tool, not a
public deployment. No external interface is offered by its entry point.

These HTTP tests do not validate JavaScript, rendered scaling, pointer/keyboard
coordinate conversion, image loading, marker placement or browser enforcement
of the response policies. No browser QA was performed by this reviewer;
root's separate synthetic/native-browser checks remain a distinct obligation.
Historical asset DOM checks are tool checks, not new feature observations.

Most importantly, neither these 20 HTTP tests nor browser QA can approve the
historical feature/coordinate/envelope mappings. The actual human and
appropriate synthetic localization gates remain separate. No historical
displacement calculation, old-table comparison, reproduction verdict or
causal-ranking change is supplied by this server review.
