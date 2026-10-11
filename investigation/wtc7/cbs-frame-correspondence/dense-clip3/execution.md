# Full Clip 3 execution record

2026-10-04 UTC. This record distinguishes implementation, synthetic checks,
actual historical execution and refused admission. The full-frame attempt
stopped before scoring; see [report.md](report.md).

## Environment and frozen scope

Research checkout: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`,
branch `research/sherlock-wtc7-investigation`, HEAD `ca1c2233`. All previous WIP
is retained. No main/legal edits, network retrieval, installation, staging,
commit, push, disclosure or media display occurred in this unit.

Commands below abbreviate only the executable as `python3`; the actual binary
was `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Python 3.12.14, NumPy 2.3.5 and Pillow 12.3.0. C denotes this document's parent
directory's parent, `research/sherlock-wtc7-investigation/cbs-frame-correspondence`
inside the checkout. All output paths were create-only.

Root reread the sampler, its tests, the pilot implementation, current method
and reviews, and the new complete dense adapter/tests. The main charter and
repository controls remained authoritative. `repo_intake.py` and `git status`
confirmed the research worktree and intentional earlier WIP. The plan received
a separate prospective method review before historical execution.

| Fixed artifact | SHA-256 |
| --- | --- |
| PLAN.md | f2c67fc6da18ba040448a479065a3d563a06843a91a606384addc3022f70f924 |
| manifest.json | fc5b819e2079a2d7675e174f93b8584e733d5b735f9cc70f708ff1f2c54c752b |
| Parent PROTOCOL.md | 4cf06e45c4216fa8662c90b84d4a9f78278b6704b1fcae342746cc9f4c556faa |
| Parent regions.json | 5bec4e5a1275f3cfaafd82fc534065ff190b3278c33bc1a5beb8f482de111694 |
| Parent pilot.py | b561aaae16cb1d68f1252f7ca496c6de2fe0407f79219fa096bdd437cd00cee8 |
| Parent dense_clip3.py | 20a1015ace2b373255cd32dc7e7371fbd378c725c69050d3330ad5518a2dd24d |
| Parent test_dense_clip3.py | cb0e48f43e9632339f14f5ba37d6b74c78c07f6ec6508a9cec6246e38a717961 |
| guard.py used historically | 0f20129bd7102935347315599e0e2a30264f5075f1569353339eac439422dbe0 |
| test_guard.py | d6b24cf12ad0da7fcbc47785c6f428d91f040dc72ff22557a12787c303e45ee4 |
| Unchanged sample_sequence.py | c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d |

## Synthetic checks and preserved failures

No historical images were scored by these tests. Dense population wiring uses
1134 mocked comparisons, explicitly not numerical or historical validation.
The prior pilot's inherited 11/16/73 arithmetic records remain pinned; those
three suites were not rerun in this lane.

| Check and output directory | Actual result |
| --- | --- |
| Supervisor guard-controls01 | 16 tests, 5 failures; exit 1 |
| Supervisor guard-controls02 | 16 tests, 3 failures; exit 1 |
| Supervisor guard-controls03 | 16/16 passed in 1.786 s; exit 0 |
| Extractor sampler-controls01 | 14 tests, 1 failure caused by test child import from wrong working directory; exit 1 |
| Extractor sampler-controls02 | Unchanged tests, corrected working directory; 14/14 in 1.313 s; exit 0 |
| Parent pilot-controls01 | 25/25 in 1.676 s; exit 0 |
| Author dense-controls01 | 22/22 in 11.086 s; exit 0, reported terminal 7559/chunk 84047c |
| Root dense-controls-root01 | 22/22 in 11.858 s; exit 0, terminal 50469/chunk 14f56b |

Supervisor review initially identified surviving descendants, incomplete
failure receipts and interruption cleanup. Scoped corrections were made before
historical execution. The first two control runs retained immediate termination
permission errors and unknown leader status. The final code cleans up once,
preserves the initiating failure, reaps before checking the process group,
retries the same operation only inside the fixed grace, and records unresolved
cleanup as failure. The final controls checked actual descendant absence.
No underlying operating-system cause is established. See the independent
[supervisor review](supervisor-review.md), which inspected but did not rerun
the controls. Only synthetic fixture links were removed by their tests; no
source, historical output or failed receipt was deleted.

Actual test invocations, with their working directories:

```text
# checkout root, first three invocations with their respective output suffix
python3 -B research/sherlock-wtc7-investigation/cbs-frame-correspondence/dense-clip3/test_guard.py --out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-frame-correspondence/dense-clip3/guard-controls01
python3 -B research/sherlock-wtc7-investigation/cbs-frame-correspondence/dense-clip3/test_guard.py --out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-frame-correspondence/dense-clip3/guard-controls02
python3 -B research/sherlock-wtc7-investigation/cbs-frame-correspondence/dense-clip3/test_guard.py --out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-frame-correspondence/dense-clip3/guard-controls03
python3 -B research/sherlock-wtc7-investigation/late-fire-sequence/test_sample_sequence.py --out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-frame-correspondence/dense-clip3/sampler-controls01
python3 -B research/sherlock-wtc7-investigation/cbs-frame-correspondence/test_pilot.py --output /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-frame-correspondence/dense-clip3/pilot-controls01
# research/sherlock-wtc7-investigation/late-fire-sequence
python3 -B test_sample_sequence.py --out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-frame-correspondence/dense-clip3/sampler-controls02
# C, author then root
python3 -B test_dense_clip3.py --output dense-clip3/dense-controls01
python3 -B test_dense_clip3.py --output dense-clip3/dense-controls-root01
```

The first supervisor controls used code pin
`8871b9bf17cf619acb7bcb8b2512a2a7bd57f53e72a3e5dc115478816e9f13d6`;
the second used `ace47b8c929ca25463f38944f252f7932e25f1924a151cafd276b561b7bc12c9`.
The passing summary is pinned at
`0d40bd204977b6fca43ea4e2253750ebe39fe78ec8320cda542545cda2680b94`.
Each failed run remains separate. A passing later test is not a rewritten earlier
receipt. Initial source edits that failed patch context did not change files.

## Sole historical attempt

From C, root invoked `python3 -B dense-clip3/guard.py --job extract01 --` followed
by the exact sampler argument array saved in
[guard-extract01/start.json](guard-extract01/start.json). That record gives the
actual executable, source manifest, both declaration pins and output path;
the sampler's exact decoder arguments are in
[decode.command.json](extract01/vince-clip3/decode.command.json).

Terminal 17517 finished with exit 1, chunk `c30fc1`. The guard receipt records
3.530894458 seconds and 131,007,165 output bytes, below both reserved stop
thresholds. Lane bytes before its terminal receipt were 132,830,245; free space
afterward was 11,154,165,760 bytes. There was no limit breach or cleanup error.
Both underlying probe and decoder processes returned zero; the sampler returned
one because its strict diagnostic grammar refused final line 394. Its
source-identity hashes matched before and after. The schedule explicitly
prohibited broadening that grammar or automatic retries, so extract02 and all
six scoring jobs remain unrun. No decoder, source or scoring code was altered
after seeing the historical failure.

## Read only failure verification

Root's stdout-only bundled-Python assertion call (`python3 -B -` from C,
chunk `a6fa32`, exit zero) rehashed the sampler and original source, reproduced
the exact diagnostic refusal, verified the underlying decoder status, checked
all show-info PTS/geometry/SAR/field joins against the inventory, counted the
189 sequential PNG filenames, and asserted that frames.json, extract02 and
score directories were absent. It opened no PNG content. A single-space
substitution in a temporary in-memory log made the grammar parse; this was a
counterfactual localization test, not a saved repaired log or accepted run.

| Preserved failure artifact | SHA-256 |
| --- | --- |
| extract01/run-receipt.json | a061b18402e9d30e639bda4716d81e49753aeebc2cb657e8a7b00c74049692b8 |
| extract01/vince-clip3/receipt.json | 41d592cc774190e1f70e0e3250e92f53d44ee2d14dd8a08d836cb0e354848184 |
| extract01/vince-clip3/probe.stdout | 51478357670208fac974078a2a453d1fbb23d144e05f567767e85745c1b431f5 |
| extract01/vince-clip3/decode.stderr | 76ae78cabb327c0c7b9d18cccbf9d2366030d3396ebe02cc9138182db2213a98 |
| guard-extract01/receipt.json | 37dcdbccb50e9f2d8b1e3f0322504b283d76bf62794915207c1e1d79a71a3ac8 |

The separate [artifact review](artifact-review.md) supplies independent failure
checks, not a completed dense match. Final document/whitespace/pin verification
is recorded below only after execution. The next bounded task is the separately
versioned diagnostic repair described in the report. Full goal active/incomplete;
all scientific, actual-human and legal-promotion gates remain unchanged.

## Synthesis and final documentation checks

The separate synthesis reviewer found no material correction. Its
`synthesis-review.md` is pinned at
`7ad97fbadad8ee401c3417eade93df06f488fc00097ff58caf35bef9b9952c7b`.
It reviewed report pin
`574ca06d743866ab278f17191e12fc6e688e8ebc302a059f6f9aec69ae8ff102`
and execution pin
`994c6b641d3dcccaf7fe681dc967ca12fc9050b49b3451f5704a132e571b6e59`;
this final documentation-check paragraph was added afterward, not represented
as already reviewed text.

Root's stdout-only documentation assertions checked 12 fixed source/receipt/
review pins, seven Markdown documents, twelve local links, four Python source
syntax/whitespace checks, five passing control receipts, both navigation entries,
and absence of later historical runs. All checks passed. The one intentional
trailing-whitespace line is the artifact review's verbatim final log line;
it was checked byte-for-byte against the preserved original, not silently
trimmed or treated as a generic exception. `git diff --check` passed for tracked
changes; the separate checks covered these untracked authored files. No image,
historical score, source identity acceptance or new execution was produced by
documentation QA.
