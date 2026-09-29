# Execution, diagnostics and acceptance

2026-09-19. This validates a bounded descriptive source check, not a scientific
cause finding or the entire investigation. The independent source and method
reviews remain separate from visual observations and human acceptance.

## Declared method and runtime

| File | SHA-256 |
|---|---|
| PROTOCOL.md | 7d0fb79d2a1a5cdfc92a7062221e75cd2a2a5caf5f85919c48d3d58bbabb0e2b |
| FRAME-PLAN.md | c5bc934477182bd6d9f85f893f9a57517090c5a3aa1d0492724f625cab9964af |
| sample_frames.py | bd4267da1f80cb565322caa67a0ab8b8e5de181e31eaf0b68e4505e8a4258a68 |

The frame plan's initial line-break typo was corrected before any derivative
run; the pinned version above is used in every receipt. No plan/helper change
followed the historical results. Sources are the two AVI hashes/sizes declared
there. Bundled Python3.12.14/Pillow12.3.0, installed FFmpeg/ffprobe7.1.1; versions
and exact subprocess command arrays are retained inside each run directory.
No new dependency installed or global setting changed. The helper is local
task code, not a validated Sherlock/Faraday media capability.

Actual root invocations, from the research worktree, use the prefix:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/late-fire-catalog-join/sample_frames.py
```

with these exact suffixes, in order (all exited0):

```sh
--control --out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/late-fire-catalog-join/control01
--out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/late-fire-catalog-join/run01
--out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/late-fire-catalog-join/run02
```

These record finished execution, not permission to overwrite those outputs.
Output directories are exclusive. Both history passes decoded all frames to
inventory and generated the predeclared sparse samples. All raw stdout/stderr,
including errors, remain in place.

## Synthetic checks

`control01` contains the generated125-frame96×64 FFV1 AVI with stereo PCM,
SAR4:3,30fps and exact red/green/blue ranges declared in the plan. Selection
0,60,120,124 yields exact expected RGB values and source PTS `index/30`.
Guess-on and guess-off output frame tables, PNG bytes and RGB pixels match.
Guess-on emits a guessed-stereo warning; guess-off retains two audio channels
without inferring a layout. This supports the limited input-option behavior
on the controlled video-only extraction, not arbitrary historical decoding.

Three deliberate negative controls reject a wrong hash, a wrong count and
an existing destination. Results are in `control01/control-results.json`.
The [method review](method-review.md) independently checks these outputs and
documents its additional guard checks. No claim is made that a synthetic
FFV1 fixture establishes full DV/image fidelity or a historical clock.

## Historical results and admission

| Source | Frame records/pass | Samples/pass | Probe/decode diagnostics | Admission |
|---|---:|---:|---|---|
| Dub5 15 | 475 | 9 | Empty probe stderr; no decode warning/error in either pass | Descriptive scene inspection only |
| Dub6 44 | 824 | 15 | Each decode has829 explicit error lines:542 concealment messages and287 missing AC EOB marker messages; probe also reports errors | Not admitted; images not viewed |

Dub6's probe stderr has580 physical lines per pass, including compressed
repeat messages; this is not580 independently located bad frames. Likewise829
decoder message lines are not a count of damaged images. The underlying
cause/source stage of the bitstream errors is unresolved. Deterministic
concealment can reproduce pixels while leaving fidelity uncertain.

All three comparison pairs (control guess-on/off and the two historical
run01/run02 pairs) have matching frame tables, exact PNG hashes and decoded
RGB hashes. Independently checked totals:56 PNG instances, comprising8 control
and48 historical outputs;2,848 frame inventory rows, comprising250 control and
2,598 historical records across the paired runs. Those totals include repeats
and refused products. There are only **nine unique admitted visual samples**,
not56 accepted historical observations.

**Helper limitation:** its receipt's `warnings_require_manual_review` array
lists decode diagnostics only; probe stderr is retained separately. Its
`automatic_checks: passed` string means the particular count/PTS/geometry/
hash checks succeeded, not that diagnostic review or visual admission passed.
This validation supplies the explicit per-source admission decision after
reviewing both stages. The helper/output wording is not silently rewritten
after the result. Before broader reuse, a narrow tested revision should
separate structural-check status from probe/decode diagnostic and admission
status; no such revision or new historical run is claimed here.

## Viewing and independent review

Root and the separate AI observer each viewed all nine Dub5 run01 PNGs at
original raster detail and both reference JPEGs. Neither viewed Dub6 frames,
listened to audio, performed continuous playback, measured fire extent or
temperature, or supplied human acceptance. No framing transforms were used.
The file samples are interlaced with SAR8:9; uncorrected displayed geometry
is not a metric calibration.

Frozen identities:

- Root first-pass note: `6903c2091cfd452353b1c9ad37dbc86fd04fd278f40ea23301f6145d5fc6e843`.
- Observer reference freeze: `826c186a422129ea74e1c37e8b18fd459306a3519af70fd12415cd930a8dfaf3`.
- Observer sample note: `9771e69ee6e6a8c18f791278c9160da2aac9b3679cd5a72361a62088e075041b`.
- Source review: `5e82ca34dca51175ff814ea04fbaad8e0a324257192a6e53b9d8bc62f78ae9fa`.

The source reviewer verified the current catalog/byte chain but did not perform
independent acquisition or visual review. The method reviewer checks common
generated outputs with its own arithmetic/image hashing; it is not a second
decoder or independent historical source. The visual observer had not read
root's candidate judgments before freezing its own. Root later read both
observer notes in full. Root's incorrect figure number for the copyright label
is explicitly corrected in report.md while its frozen note remains intact.

## Operational failures and boundaries

Web-tool InternalError/empty extraction did not establish source absence:
ordinary public HTML/API/browser routes supplied some records. AP's exact
current keyword result remains route-specific. One broad diagnostic search
printed too much repeated error text; subsequent inspection used category
counts and preserved logs, without deleting or suppressing the underlying
errors. Several early reads targeted not-yet-created review files and returned
not-found; these were scheduling errors, not missing source evidence.

An initial legal-record check guessed the nonexistent name
`/Users/admin/docs/911/tools/validate_record_spine.py` and exited2 without
running any validation. After locating the actual main script, the corrected
check is `python3 /Users/admin/docs/911/tools/validate_record.py --strict`, from
`/Users/admin/docs/911`. It concerns unchanged canonical legal records, not
media-source or scientific validity. Final results are appended below after
the last document/link checks.

The acquisition ledger records the uncertain browser-download click,
permission-denied Downloads check and transient retrieval-URL logging mistake.
Transport headers stay in ignored local-only files; no new sensitive outgoing
payload, upload, contact, fee, commit or push occurred. The archived Sherlock
feedback destination has not been reopened. No accepted engine evidence state,
main source, legal fact or pleading changed. Full goal active/incomplete.

## Final integration checks

Root read the completed source, method and visual notes and the entire
critical review. Three substantive wording corrections were incorporated;
the reviewer read the revised report and validation summary and confirmed
their resolution. Its review is textual, not another image pass or command
rerun. Root subsequently applied its two minor clarity suggestions (six
public queries; stream/loan-only) and added the review link. The method
review's final SHA-256 is
`7b9248a475524af05cdf7722d7455a8c12be22453ad21cab61bec32328db806c`;
critical review SHA-256 is
`60d6a58040bf9bdde93bb68eab0c3fc391f9a35f14b61582bdead6cbe06b545c`.
The final report SHA-256 is
`f5f163c53c9d2d6afb6c795047440c65e9beb07ecee4e9edc003d8578cda0668`.

Actual read-only bundled-Python checks: eight frozen control/observation/review
pins matched; sample_frames.py parsed with ast.parse; all42 `.json` files in
this unit parsed; all13 unit Markdown files passed trailing-whitespace checks;
all14 local Markdown links then present resolved. Adding the critical-review
link raises the final local-link count to15; the final repeated check below
also includes the critical-review pin, for nine pins. These counts exclude
binary/media files and do not represent global repository link validation.

`git diff --check -- research/README.md
research/sherlock-wtc7-investigation/STATUS.md
research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md` exited0. It covers
tracked navigation/feedback changes; the separate Markdown scan covers this
untracked unit. The corrected canonical check
`python3 /Users/admin/docs/911/tools/validate_record.py --strict`, run from
`/Users/admin/docs/911`, exited0: headers, issue/fact links and citation tags
pass. No legal record was changed, and that check does not validate these
scientific claims. `git check-ignore -v` confirms both retained transport-header
paths match the existing `**/*-local-only` ignore rule.

The final repeated nine-pin/AST/42-JSON/13-Markdown/15-link check and scoped
tracked-diff check passed after this appendix was added. The branch remains
research/sherlock-wtc7-investigation at e8d83d7 with intentional WIP; no commit
or push. No live download/decoder is pending. The next finite task is in the
current STATUS entry, not a rerun of completed source search or sparse samples.
