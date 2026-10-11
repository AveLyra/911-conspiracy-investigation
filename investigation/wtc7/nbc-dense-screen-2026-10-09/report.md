# NBC candidate picture correspondence result

The denser screen found **no recognizable match to Excerpt C's third shot** in
the 652 inspected candidate images. This narrows two source leads; it does not
identify the reported bang, authenticate a soundtrack or change the collapse
assessment. The short candidate was inspected across every decoded frame. The
long candidate was sampled, so a brief intervening shot is not excluded.

Research only, October 9, 2026. The [protocol](PROTOCOL.md) fixed the two inputs,
selection, reference pictures, review sample and inference limits before this
unit's extraction and viewing. Prior sparse-screen findings were known. This
is a prospective extension of existing work, not retroactive preregistration,
blind validation, actual-human acceptance or expert forensic review.

## Changed evidence and provenance

The separate [acquisition packet](/Users/admin/docs/911-worktrees/nbc-media-acquisition-2026-10-09/research/sherlock-wtc7-investigation/nbc-media-acquisition-2026-10-09/README.md)
contains both previously catalogued public NBC candidates. Its
[manifest](/Users/admin/docs/911-worktrees/nbc-media-acquisition-2026-10-09/research/sherlock-wtc7-investigation/nbc-media-acquisition-2026-10-09/manifest.json)
pins the source URLs, acquisition route, byte counts and SHA-256 hashes. This
unit verified those local bytes before and after each extraction. It made no
new download and did not modify or copy the original videos.

Both belong to the same catalog branch, not two independently authenticated
witnesses. A public archive label is not proof of filming location or original
soundtrack. The source hashes establish acquired-byte identity, not historical
authenticity. The earlier connector-only acquisition failure remains valid
history, but it is no longer the current local-byte state for these two files.

| Candidate | Preserved source bytes | Decoded inventory | Inspected images | Maximum selected encoded-time gap |
| --- | ---: | ---: | ---: | ---: |
| collapse wtc.mpg | 2,703,430 | 295 | All 295 | 1/30 s |
| wtc5.mpeg.mpg | 99,297,340 | 10,648 | 357 | 1 s |

The long-file selection is the first decoded frame in each of 356 occupied
absolute one-second bins plus the final frame. These are encoded best-effort
timestamps, not authenticated event clocks. Three unselected inventory frames
lack original PTS; that is preserved rather than silently relabeling estimated
timestamps as stored PTS.

## Visual findings

The [complete root reading](root-visual-review.md) covers all 33 contact sheets
and the three existing C reference frames. The short candidate shows a city
and dust view framed by dark near-camera edges, then an edited overlap into
debris-covered escalators. Its identifiable buildings do not reproduce C's
dark right-hand facade, lower cupola-bearing building and intervening street.
The large-file sampled views show damaged interiors, framing and rubble, then
exterior debris-field views; none presents that target arrangement.

The [separate AI reading](peer-visual-review.md) covered the fixed eleven-sheet
sample, or 220 images, and the same three references. It found no recognizable
or ambiguous match. The peer had prior sparse-screen context but had not
received root's dense-screen findings. Root received the peer report before
finishing its own full reading. The agreement is therefore not two blind
readings and neither reader is an independent historical source.

These are qualitative observations, not automatic registration scores. They
support the bounded statement that no match was recognized in the inspected
images. Low resolution, dust obscuration, alternate framing and reader error
limit identification even in the short file. The long-file sample can miss
brief inserts and decoder corruption can hide information. The result is not
an exhaustive archive exclusion or proof that the scenes concern different
events. No native-frame follow-up was triggered by an ambiguous match.

## Reproduction and diagnostic limits

The implementation uses FFmpeg/FFprobe 7.1.1 and bundled Python 3.12.14 with
Pillow 12.3.0. The [technical review](technical-review.md) preserves exact
commands, versions, hashes, independently rebuilt selection and diagnostic
checks. From this directory, actual producer commands were:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 screen.py --test
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 screen.py run01
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 screen.py run02
```

All exited 0. The seven fixture checks passed before historical extraction.
Both output directories are preserved and the producer refuses to overwrite
them. Each [run receipt](run01/receipt.json) records command exits, source and
implementation pins, frame coverage and all derivative products; the
[second receipt](run02/receipt.json) records the independent execution repeat.
All 652 selected PNG pairs and 33 sheet pairs are byte-identical. This is
same-stack reproduction, not a different decoder validating source fidelity.

The separately authored [checker](independent_check.py) imports no producer
selection function. It rederives exact selections, checks all 1,304 PNGs across
both runs, joins inventory and decode timestamps, compares pixel checksums and
sheet placement, and verifies all 695 recorded products per run. Both the
reviewer and root executed the saved checker; execution details are in the
technical review and closeout below.

The short file produced no inventory/extraction warning or error matches in
the checked logs. The long file
retains damaged-texture, unavailable-motion-vector, concealment and
corrupt-decoded-frame messages. Complete stderr is authoritative; a filtered
summary and exit zero are not proof of clean media. Repeated concealed pixels
remain concealed pixels. No source repair was attempted.

Initial environment probing found no Pillow under default Homebrew Python;
the available bundled runtime resolved this without installation. The
reviewer's first independent parser captured a trailing comma in a timebase
and failed; its corrected replay passed without producer/data changes. These
failures are retained in the technical review, not presented as media defects.

## Consequence and next discriminating test

The local acquisition dependency is resolved for these two candidates. The
third-shot source/soundtrack dependency is not. No sound was listened to or
classified in this unit. In particular, the user's reported bang remains a
reported audible event of unresolved origin, not silence and not an identified
explosive charge. Neither a quieter intervention nor a fire mechanism gains
new discriminating support from these picture nonmatches.

A contrary recognizable native sequence in either candidate would reopen
the matching decision. Otherwise, the valuable next input remains a continuous
copy of C's distinctive third shot, with source/camera attribution and a
separately testable soundtrack chain. The long file's unsampled intervals can
receive a separately declared all-frame or validated correspondence pass if
exhaustive exclusion of this candidate is needed; that has not been performed.
Titles, a matching generic dust plume or an encoded audio stream cannot replace
that evidence.

The scoped WP1/WP3/WP4 checks also found no newly held native structural pair,
window-state/time joins or actual DistantView/F7 review responses. Those remain
separate dependencies, not conclusions that all public research is exhausted.
This new source test is substantive progress; the prior identity correction
was administrative progress, not collapse evidence. The full charter remains
active and incomplete.

No new distinct Sherlock defect arose: reference-only materialization,
diagnostic localization and stored-versus-best-effort clock distinctions are
already in the delivered feedback requirements. This local workaround is not
a verified Sherlock fix, and no duplicate feedback was sent. The evidence and
source-of-truth skills preserve that distinction; the development-verification
skill governs the bounded extraction checks. Documentation stays in the
existing local research format. No legal/raw record, frozen synthesis index,
human acceptance or accepted Sherlock/Faraday finding changes. No commit,
push, disclosure or publication occurred in this unit.

## Closeout checks

Root separately ran the saved checker from this directory:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B independent_check.py
```

It exited 0 and reproduced the full per-run and cross-run technical-review
counts, including 695 verified product pins per run, 652 matching PNG pairs
and 33 matching sheet pairs. Root also read both saved review records.

Final local checks parsed both Python files, checked whitespace and all twelve
local links across five Markdown files, and verified all three C reference
hashes against the acquisition record. `git diff --check` for the status update
exited 0. An initial success-message label mistakenly said six Markdown files;
the checks themselves ran over actual files. A fresh dynamically counted replay
correctly reported five. This was a reporting-count typo, not changed coverage.

The visual reviewer subsequently checked the report, root observations and
new status entry against the protocol and technical results. It found no
material overstatement of coverage or audio conclusions, but correctly flagged
root's unsupported description of a facade as residential. That word was
changed to windowed; no building-use identification is retained. No source,
protocol, producer or run output changed in this wording correction.

Two other changed-input locators were checked separately to choose later
work, not counted as new corroboration. The
[Wayback packet](/Users/admin/docs/911-worktrees/wtc7-wayback-replay-public-2026-10-09/investigation/wtc7/wayback-replay-capture-2026-10-09/report.md)
reports replay error-page entities, not acquired underlying media. Only its
report was inspected here; its raw-response hashes were not independently
reproduced. The
[contract-scope discrepancy note](/Users/admin/docs/911-worktrees/securacom-contract-scope-discrepancy-2026-10-09/research/wtc7/contracting-access-custody-audit/securacom-wtc-contract-scope-discrepancy-2026-10-09.md)
is a primary-record retrieval lead, not authenticated contract/access evidence
or a physical collapse input. Its cited underlying sources still require a
bounded primary-source audit before any evidentiary conclusion. These findings
do not justify repeating the stopped media retrievals or asserting global
evidence exhaustion.
