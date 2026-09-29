# Stage B annotation verification

September 20, 2026 UTC. Current scope is viewing, frozen annotation, metadata
and arithmetic; no new historical decode, source acquisition or control-suite
rerun. Prior executions remain in [stage-b-execution.md](stage-b-execution.md).

## Frozen inputs before exchange

Root saved and hashed its files before reading either observer Stage B file.
The observer had already sent only a procedural freeze notification and hashes.
Root then explicitly authorized exchange. All four hashes were freshly
rechecked after exchange began; they match:

| File | SHA-256 |
|---|---|
| root-stage-b.md | c01c9fe3628fae76417d11c166f5981706162c93362984c6114157a6a70e2bbf |
| root-stage-b-scope.md | 3135cf7600ab4b9cef7a60adef238cf653ce38a71fe7af64f54b98b3254124c3 |
| observer-stage-b.md | cea1a9c0db50d0ece47ceb19a877f97977d8348e47c61a84fc630ce5c54a6da5 |
| observer-stage-b-scope.md | 9794d0e106f87bdb0a8783c559992ec62757c9088ba993dd8d5a6da48e13809d |
| run01/camera2/selection.json | e297292a04a093d757b7693b9914abe4b88db4e6b836461f49c8dee411e78b2d |

## Actual current checks

Before viewing, root rechecked the main controls/charter, Stage B declaration,
run01 receipt, saved root verification pin, and all 458 run01 product
fingerprints. All passed. This checks unchanged files, not the truth of the
visible-event interpretation. The repo-orchestrator intake also completed;
intentional unrelated/uncommitted research was preserved.

After both annotation freezes, a read-only command executed with
`PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3`
from the investigation worktree. Its assertions performed these checks:

1. Rehash the four frozen Markdown files and selection JSON to the pins above.
2. Expand root's exact viewed-index set `{6593,6784,7013} ∪ [6689,6736] ∪
   [6881,6980]`; expand the observer's `{6593} ∪ [6650,6724] ∪ [6920,7013]`.
3. Require counts 151 and 170; intersection 99; union 222.
4. For all 222 union indices, check native PNG bytes and SHA against selection
   rows, and require `Fraction(source_pts) * Fraction(source_time_base)` to
   equal `Fraction(source_time_seconds_exact)`.
5. Require both observers' onset bracket, positive+1/+2 persistence frames,
   and last west-visible frame to be in their actual-viewing sets.
6. Use `fractions.Fraction` to calculate each east-bracket width and conditional
   elapsed lower enclosure. No finite upper bound is inserted.

**Actual result: exit 0/PASS.** Root width `1603/2997 = 0.5348682015… s`;
observer width `233/999 = 0.2332332332… s`. Elapsed lower enclosures are
`24101/2997 = 8.0417083750… s` and `24401/2997 = 8.1418084751… s`.
Correct arithmetic is not an independent validation of the selected features.

The observer separately reports a successful read-only 170-native-file hash/
byte traversal in its frozen note. Root's new 222-file union check includes
those files; this is an actual separate check, not merely adoption of the
observer's assertion. No original camera/tape custody or acquisition clock
was authenticated.

## Visible coverage and execution limitations

Root: all 27 sheets, 151 unique native images / 152 native displays. The first
attempt to display overview21–23 was truncated at compaction, so it was not
counted; the sheets were reopened completely. One later mistyped-path image
request failed before any image returned and was corrected. The failed path
is not missing media. Observer: all 27 sheets, 170 unique native images /184
native displays; its own lookup/path errors remain in the frozen scope note.

Neither passing product checks nor reviewing reduced thumbnails counts as
viewing every selected native frame. No new playback, stabilization, crop,
enhancement, metrical calibration, solver, source search or source-page render
was performed. This pass tests a projected visible sequence only. Frozen
records are never rewritten to manufacture agreement or remove censoring.

## Post-freeze and independent text review

The separate annotator completed [stage-b-exchange-review.md](stage-b-exchange-review.md),
SHA-256 `69657152ecda8ac6f9671c28473e493df2c96897fb30f3a159f7159846fed10d`.
Root read it completely. Its independent metadata/Fraction calculation passed;
it confirms nested onset brackets, shared conditional last-visible frame,
one-sided arithmetic and coverage-set counts. It is review by one of the two
annotators, not a third visual replication.

A third agent, `/root/stage_b_critical`, performed bounded **text and printed-
input arithmetic review only**, with no new historical pixels, primary-PDF
verification or extraction-metadata check. It independently reproduced the
two widths/lower enclosures and 151/170/99/222 coverage counts. Two P2 wording
concerns were returned and corrected in the new synthesis, not the freezes:

- Numerical inclusion of the 9.3/10.6/10.9 published values above the lower
  bound must not be labeled demonstrated model/view compatibility.
- The available source account does not establish an "infinitesimal" model
  timing origin. The synthesis now states the unmatched timing-origin issue
  accurately and adds the directional qualification: earlier undetected east
  motion would lengthen, not shorten, the elapsed interval for the same event.

No arithmetic/censoring error was found within that text-only review. It does
not certify the roof component association or primary-source attribution.
Final revised synthesis SHA-256:
`30a84c86239580446076b3eaf5e8d5fdf175090aa12c408027f4459365c0274a`.

## Documentation checks and continuation state

Actual checks run from the research worktree unless an absolute path specifies
main; these are documentation/record-integrity checks, not scientific acceptance:

- `git diff --check`: exit 0, no output. This checks tracked differences, not
  every untracked file; the explicit Markdown pass below covers this new unit.
- `python3 /Users/admin/docs/911/tools/validate_record.py --strict`: exit 0,
  `OK (headers + issue↔fact links + citation tags)`.
- Read-only Python traversal of the seven new annotation/scope/exchange/result/
  validation Markdown files: exit 0; all 12 then-present local Markdown links
  resolved; no trailing whitespace or conflict markers. Four freeze hashes
  remained identical. This preceded the final validation append; the final
  check below also covers that append and all final links.

Branch `research/sherlock-wtc7-investigation`, HEAD `e8d83d7`; intentional WIP
and unrelated worktree changes preserved. Recent research commits inspected:
`2661f35`, `c8ac14e`, `92bb398`. No commit/push. Current navigation is updated
in the existing STATUS.md/research README; generic annotation/censoring feedback
extends SFB-002/SFB-004 locally. The designated Sherlock task remains archived,
so no new feedback delivery, acknowledgment or fix is claimed. No acceptance
or case material crossed the Sherlock/Faraday/legal/privacy boundaries.

All bounded Stage B annotation/review work is terminal. The next task is the
prospectively declared, capped lossless display sensitivity test described in
the result/status; it has not been executed. An unresolved result must survive
that handoff without being mislabeled as a complete interval or a cause finding.

Final post-revision traversal returned **exit 0/PASS: seven Markdown files,
13 local links, six frozen/result hashes, no trailing whitespace or conflict
markers**. The final `git diff --check` also returned exit 0 with no output.
