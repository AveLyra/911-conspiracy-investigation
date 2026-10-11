# Execution and verification

October 8, 2026. Research only. The frozen [protocol](PROTOCOL.md) controls this
unit. The actual output is an ordinal correspondence-feasibility packet, not
a time-calibrated track. All work remains in the existing investigation
worktree on `research/sherlock-wtc7-investigation`, HEAD
`ca1c223335c20905d6608eb15c676f88cbfac734`, with intentional uncommitted WIP.

## Commands actually run

Working directory for these commands:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
The Python executable was
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
(3.12.14); Pillow was12.3.0. Below, `PY` and `U` are documentation abbreviations,
not claims that shell variables were set during execution:
`U=research/sherlock-wtc7-investigation/distant-view-source-screen/continuity-274-411`.

```text
PY -B U/derive.py --self-test
PY -B U/derive.py run --out run01
PY -B U/derive.py run --out run02
PY -B U/verify_independent.py --self-test
PY -B U/verify_independent.py --runs run01 run02
PY -B U/verify_independent.py --runs run01 run02 --roster ABS_U/root-observations.json --roster ABS_U/peer-observations.json
diff -rq U/run01 U/run02
```

`ABS_U` is the absolute worktree path plus `U`. Both checker invocations were
read-only; their actual stdout was saved through `apply_patch` after successful
JSON parsing, without rerunning or replacing the underlying results.

Root read the complete producer and checker before their historical execution.
The initial producer roster used index/left/right; before historical processing
it was changed to ordinal/from/to. Both versions passed the same16 synthetic
tests. Root reread the changed sections and independently reran the final16.
This is16 distinct producer controls, not32 independent tests. The checker's
12 controls also passed in both its author's run and root's run:28 distinct
current controls in total. No synthetic failure was treated as historical data.

The final producer SHA256 is
`f261b0f516c90b3ae274b8d3d49e7453e7a2c80eb323f9cdcf3ca176067ae68a`.
The checker SHA256 is
`c27e51e97abcecb8a2d176c40ae30484fe5069186a813e5e451f6f0ed2dccf7c`.
The final schema revision did not change the decoder or pixel derivation.

Both historical derivations returned0. Both decoded487,618,560 bytes with
aggregate SHA256
`4ffad6fee7b8f256be33ddbdebb2207394bdb3d2d72798c11aa679fe291555c5`;
all962 individual decoded and luma hashes matched the pinned earlier map
before images were saved. Both decoders had empty stderr, no timeout and no
waived warning. The full raw decode existed in memory only. Each run preserves
the first1,048,576 stdout bytes and the complete empty stderr, with captured
byte counts, hashes, status and elapsed time. The wrapper's failure paths were
tested with synthetic launch failure, timeout, nonzero exit, warnings and
oversize output; no such historical failure occurred in this unit.

The recursive comparison returned1 because elapsed-time execution receipts
and their hashes differ. Every other file was byte-identical. The independent
checker separately verified that the two top-level receipts differ only in
their execution-record pins, and checked each actual execution record.

## Independent packet check

The actual checker returned0. Its full stdout was retained verbatim as
[pre-view-verification.json](pre-view-verification.json), SHA256
`e9d751b20d749186117796316f5f481ddb700bab0051b81ffa559724d7a0e96a`,
before either new visual pass began. It verified658 file pins before/after,
962 source timestamp rows,962 saved decoded-hash rows per run,138 native PNGs,
138 crop PNGs and12 pages per run, all source/crop/page pixel mappings, page
order, six blank cells, labels and gutters. Across both byte-identical runs,
288 unique PNGs were losslessly decoded using a separately written PNG parser.
The second run's identical bytes permit cached decoding;576 saved PNG files
were checked, not576 independent images.

The checker does not import the producer. Its PNG parsing/filter reversal and
pixel-placement logic are separate. Labels share Pillow's default-font
renderer, so this is not independent font-rendering verification. It does not
independently decode the AVI; selected native pixels are checked against the
previous decoded luma hashes. Unselected raw pixels remain hash-record checks.
Hashes demonstrate consistency of held bytes, not historical authenticity.

There are47 missing stored PTS values among the138 selected frames, and no
missing best-effort values in this interval. The complete source still has329
missing stored PTS and one missing best-effort value. All remain separate and
nullable. The earlier original matching-timestamp requirement remains failed.

## Reader and semantic controls

Each reader was instructed to inspect only the12 fixed contact pages and full
native contexts274,342,411, use original-detail display, and stop if inadequate.
Root completed that exact coverage and froze its JSON before receiving peer
findings. Per-frame states and per-link judgments are explicit; range expansion
was used only to record identical judgments after visual inspection, not to
fill uninspected content. Actual viewing and its limits are recorded in each
first-pass file. Known endpoints mean this is not a blind historical holdout.

The producer and independent checker both structurally accepted root's138/137
rosters using their `validate_roster` and `check_roster` functions. Structural
checks cannot certify that a reader actually looked, that a reason is correct,
or that an O reason distinguishes obscured from not located. That last
distinction was explicitly communicated before reading as a semantic duty.
The [result](report.md) records both frozen passes and their comparison.

After both freezes, root reran the full independent checker with both absolute
roster paths: exit0,660 pins unchanged. The full result is
[final-verification.json](final-verification.json), SHA256
`4d98bc4c4f26a0b889466071419a8f3edeb090c1798e1ccae0db325cf5e34325`.
It structurally accepts both138/137 rosters and reports the same274–411
supported run. Root separately used the same `check_roster` function,
`collections.Counter` on each status array, and pairwise status comparisons
on the hash-checked saved rosters to create [comparison.json](comparison.json),
SHA256 `167bdfcca266ee6fbaf8d6be5213c629d85b64f78d9146768ecfceafc8178cc7`.
Its empty disagreement arrays follow from comparison of all138 frame and137
link statuses, not from comparing only totals. The two declared ordered
view-path lists were also compared and equal. Neither reading was rewritten.

The method reviewer reviewed the frozen protocol before execution and found
no material blocker, warning that native construction does not guarantee an
adequate display. The producer author later reviewed the execution and result
prose, without images or annotation contents. That limited closeout review
caught ambiguous wording that could conflate pre-view derivative order checks
with post-view reader-roster checks; the report now separates them and links
the actual receipts. Producer authorship limits this review's independence.
The different-agent pixel checker and separately frozen visual pass are
separate contributions, not additional historical sources or expert opinions.

Closeout checks: `git diff --check` passed for tracked worktree changes. An
initial auxiliary Markdown-link regex mistakenly parsed Python bracket/call
syntax inside the peer note's fenced code as a link and stopped. The check was
corrected to exclude fenced code (not to suppress a broken real link); the
replay resolved all20 actual links across the four unit Markdown files and
confirmed no trailing whitespace in those files, both scripts and the five
JSON outputs. JSON parsing, unchanged frozen-note hashes and equality of the
comparison's reader results with the final checker receipt also passed.
That first auxiliary failure did not change sources, observations or results.

No source, old result, raw/legal record, accepted annotation, main checkout,
Sherlock/Faraday accepted state, held comparison matrix, filing or transmission
was changed. No commit/push or additional source retrieval occurred. All prior
human and specialist gates remain; existing R1 human inputs are not reopened.
