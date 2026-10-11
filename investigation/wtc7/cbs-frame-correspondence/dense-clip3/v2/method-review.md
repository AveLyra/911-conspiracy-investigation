# Full Clip 3 version 2: prospective method review

2026-10-04 UTC. Reviewer `/root/stage2_visual`.

**Conditionally adequate; no material plan correction required.** Acceptance
here concerns the declared method and finite schedule. Wrapper implementation,
fresh controls, admission and historical results remain unverified by this
review.

Read `PLAN.md` fully and checked its SHA-256 at 2026-10-04 03:59:34 UTC:
`e25d3568d8dbdd5f66d4d3004fb334d8eda2025cc3021860f64534d399902abe`.
The preceding refused attempt, its plan and the unchanged image protocol
remain separate records, not overwritten versions.

## Producer basis and scope of correction

The official FFmpeg **n7.1.1** `fftools/ffmpeg.c`, function `print_report`
(source line 548), uses `fps=%3.*f` with precision selected by `fps < 9.95`
at lines 594–598. It derives that value from output packets and elapsed
processing time, or zero during the initial short interval. A two-digit integer
therefore receives one leading space; the decimal branch must also remain
supported. This is processing throughput, not a source frame rate or historical
clock. [Official tagged source, lines 577–602](https://github.com/FFmpeg/FFmpeg/blob/n7.1.1/fftools/ffmpeg.c#L577-L602).

Those primary-source facts support the proposed local ASCII-space correction.
They do not support generic whitespace acceptance, rewriting logs, suppressing
unknown lines or retrospectively admitting version 1. Keeping the original
NUMBER grammar also avoids introducing an unrelated numeric-policy change.

## Required boundaries preserved in the plan

- Only the stated final-summary fragment changes. Raw logs, warning and
  control-character refusals, summary counts, source/PTS joins and PNG/RGB
  checks remain intact. Version-1 output cannot become version-2 score input.
- Configured wrappers must identify their changed execution and all parent
  dependencies. Reusing functions must not masquerade as execution of the old
  module unchanged. The plan explicitly requires that independent code check.
- Fresh configured controls, new negative format tests and an actual version-2
  optimized-mode check address the inherited child test's old-module limit.
  A claimed control count alone is insufficient if it exercises the wrong
  module or stale configuration. No such tests were run by this reviewer.
- Both full extractions and all six score chunks must complete and reconcile
  before one global aggregate and shortlist. The 189-frame population,
  567 comparisons per pass, unchanged numerical method, nulls/ties and
  maximum twelve native candidate views remain explicit. Cross-view controls
  remain pilot-only; Clip 7 is not dropped or declared complete.
- Cumulative accounting starts at the parent dense directory and includes the
  failed first attempt. The same total cap, continuing free-space floor,
  reserves, serial execution and no-automatic-retry rule remain operative.
- A successful repair or a stronger numerical match would not establish exact
  exposure, historical custody, fire severity, mechanism, intent, or actual-human
  acceptance. The larger search remains a retrieval test, not an independent
  validation sample.

No broader parser or measurement change is needed to answer the stated next
question. Unexpected producer branches should produce a preserved refusal and
separate review, not outcome-driven expansion during this scheduled run.

## Actual review actions

Read and hashed the new plan and its controlling predecessors; the unchanged
parent protocol, region and pilot pins matched those recorded in the plan.
The producer verification used the official tagged source, with a stdout-only
raw-source read to confirm actual source-line numbers; no source copy or media
was saved. No parser, wrapper, control suite, historical decoder or scoring
routine was executed here, and no historical image was opened or displayed.
Only this review file was authored. Implementation acceptance and the promised
synthetic/independent checks remain separate prerequisites, not findings of
this review.
