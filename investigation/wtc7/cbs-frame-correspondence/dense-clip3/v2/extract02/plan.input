# Full Clip 3 version 2 execution schedule

2026-10-04 UTC. This is a new prospective execution version, not a change to
the [refused first attempt](../report.md). Complete the same full Clip 3 source-
correspondence test under the unchanged [image method](../../PROTOCOL.md) and
the [first dense schedule](../PLAN.md), except for the explicitly stated
diagnostic and execution-identity changes below. No new historical pixels or
scores have been inspected to select this change. All earlier bytes, receipts,
annotations, masks and numerical rules remain unchanged.

## Reason and exact permitted change

The original parser refused a final summary containing a space-padded `fps`
value. In the official FFmpeg 7.1.1 source, `print_report` uses a width-three
field with one decimal below 9.95 and integer formatting otherwise. Its value
comes from output packets divided by elapsed processing time, not source PTS.
The two-digit integer branch therefore has one leading ASCII space.
[Primary source](https://github.com/FFmpeg/FFmpeg/blob/n7.1.1/fftools/ffmpeg.c#L577-L602).

Only the existing final-summary grammar fragment `fps={NUMBER}` may become
`fps= ?{NUMBER}`: zero or one U+0020 space, with the inherited NUMBER expression
unchanged. Do not use a generic whitespace expression, strip or normalize a
saved log, ignore a line, suppress diagnostics, or change any other expression
or cardinality. Keep raw subprocess streams exactly as received. The failed
version-1 extraction stays refused even if the new parser can parse its log.
No version-1 PNG or retrofitted manifest may enter the version-2 scoring inputs.

## Version identity and reuse

Use thin, explicit local adapters over hash-pinned components, not a second
numerical implementation. `sample_v2.py` loads a separate module from the
unchanged sampler (`c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d`),
asserts the original final-summary expression, and replaces only that fragment.
The configured module's execution identity must identify the adapter hash and
the original sampler as its parent, not falsely claim unchanged execution.
It may explicitly set its module file identity and parent-code field for the
existing receipt writer; the original file on disk is never changed.

`dense_v2.py` reuses the pinned dense adapter
`20a1015ace2b373255cd32dc7e7371fbd378c725c69050d3330ad5518a2dd24d`.
It supplies this version's output directory, configured sampler, adapter and
test identities, and fresh-control gate. It must pin all wrapper and inherited
source/test dependencies. Original numerical, source, PTS, PNG/RGB, chunk,
repeat and pilot-reconciliation functions stay unchanged. No silent stale
test identity or runtime configuration may be presented as an old code hash.

The supervisor remains `../guard.py`, hash
`0f20129bd7102935347315599e0e2a30264f5075f1569353339eac439422dbe0`.
`run.py` may construct only the declared extraction, scoring and aggregation
commands and invoke that supervisor. It must use the **parent dense-clip3
directory** for cumulative resource accounting, including version-1 failures,
not reset the budget at this version's subdirectory. Freeze and review actual
wrapper/test hashes and controls before historical execution.

## Inputs and finite sequence

Use a byte-identical copy of the earlier manifest, SHA-256
`fc5b819e2079a2d7675e174f93b8584e733d5b735f9cc70f708ff1f2c54c752b`:
exactly Clip 3's 189 indices 0 through 188, the original source path, byte count
and SHA-256. The same Figure 5-143 reference, masks, thirteen scales, fixed
translations and full/even/odd representations remain the only paired test.
Encoded time base is 333673/10000000; the metadata is not an event clock.

Create only these new historical outputs below this version's directory:

1. `extract01`, then `extract02`, each selecting all 189 indices.
2. `score-a-01`, `score-a-02`, `score-a-03`, then the corresponding `score-b-*`:
   indices 0–62, 63–125 and 126–188, respectively; 189 paired comparisons each.
   Pass A uses extract01 and pass B uses extract02.
3. A single `aggregate-a`, only after all six chunks succeed: reconcile all
   567 per-pass comparison records and surfaces, all masks, all 189 repeated
   PNG/RGB/PTS rows, the nine earlier pilot frame identities and its 27 paired
   score records. Then and only then compute the global per-arm shortlists.

Each invocation gets a separate create-only supervisor record. Run serially;
stop on refusal, missing receipt, unresolved cleanup or changed dependency.
No automatic retry, output overwrite or evidence deletion. Source identity is
checked before and after extraction and every score dependency rechecked.

## Resource bounds

Unchanged limits apply cumulatively to the parent dense-clip3 directory:
1536 MiB total, including the approximately 131-MB failed extraction and all
controls/logs; stop at the 1504-MiB reserve threshold. Keep at least 4096 MiB
free before and throughout execution. Each extraction/scoring invocation has
240 seconds and 256 MiB, with a 32-MiB output reserve. Aggregation has 60 seconds
and 16 MiB, reserving 1 MiB. Supervisor polling is 0.1 second with a one-second
termination grace. Record actual duration/bytes; these monitored thresholds
are not hard filesystem quotas. No budget enlargement is authorized here.

Two new RGB sets plus raw score/coverage arrays are estimated at about 1.01 GB;
the preserved failed run adds about 0.13 GB. Retain actual compressed bytes and
stop if the declared bounds are reached. Before controls/generated writes,
check the same budget and free-space floor. Temporary synthetic fixtures are
not historical evidence; retain their test logs and disclose any cleanup.

## Fresh controls and acceptance

Before decoding, pass fresh supervisor controls and the 14 inherited sampler
controls against the configured version-2 module, plus version-specific tests.
Before scoring, also pass the unchanged 25 pilot controls and 22 dense controls
against the version-2 configuration. Root independently reruns the new suite.
Disclose any inherited child test that still imports an original module and
add a corresponding version-2 optimized-mode check; do not relabel old-module
execution as new coverage. Numerical arithmetic checks retained from the pilot
remain prior checks unless actually rerun.

New tests must demonstrate the exact one-fragment delta, zero/one-space valid
cases (including decimal and integer producer branches), rejection of two
spaces, tabs, newlines, nonbreaking spaces, malformed numeric fields, warnings,
unknown lines and duplicate/missing summaries. Preserve all prior source/PTS/
PNG/RGB/cardinality and repeat-disagreement refusals. Test wrapper and parent
identity in receipts, stale controls, allowed command/output names, complete
source population and cumulative parent-directory budget selection. Mocked
population wiring is not numerical or historical validation.

Independent pre-execution review must check that wrappers do not mutate the
original disk files or relabel changed execution with the old identity. A
supervisor success alone does not admit extracted media. Preserve failed runs
even when later checks pass.

## Scientific interpretation and review

Keep all coverage failures, ties and per-arm 0.005/0.01/0.02 near-best sets.
Dynamic ranking uses each frame's best static transform; do not optimize it
independently or pool correlated representations. Pilot cross-view controls
remain pilot-only. After complete aggregation and independent artifact checks,
root may inspect the fixed union of top-two static and top-two dynamic frames
per arm: at most twelve native images, once each in ascending source-index
order, plus one unchanged full reference display. No neighboring frames,
enhancement, crops or new cues selected from outcomes. Record actual views.

Obtain separate synthesis critique. Deliver complete results, receipts,
uncertainty/coverage limits and the highest-value next test. A match score is
not exact exposure, window material, physical fire area, temperature, cause or
intent. Human consequential-measurement gates and matrix-save permission remain
unresolved. Clip 7 and all other charter work packages remain in scope; this
lane is not completion of the 1317-frame population or the investigation.
No new media acquisition, case disclosure, legal/main edit, engine acceptance,
staging, commit or push.
