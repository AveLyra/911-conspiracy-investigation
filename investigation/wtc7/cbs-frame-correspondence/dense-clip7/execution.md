# Full Clip 7 execution record

2026-10-04 UTC. Research-only continuation of the full paired source search.
The main-repository charter controls. Original sources, prior results, failed
products and user annotations are preserved. No legal/main edit, transmission,
canonical promotion, matrix save, staging, commit or push is part of this unit.

## Prospective scope

The [plan](PLAN.md), SHA-256
`0404e0a819e7d8392ad3a320a4cb018ecef02c4d9d3f72337d4b3d1d131f6d70`,
and [manifest](manifest.json), SHA-256
`ece7d7fbae14d3ec043c16eb845d74af617a06854c267b1e686e7b33d4e6e3ad`,
declare all 1128 source frames, two complete extractions, 18 scoring chunks per
pass and one complete aggregate. No new historical image or score was used to
select those parameters. The earlier pilot and reference familiarity are not
hidden or described as a clean holdout. A transcribed sampler-hash typo in the
draft plan was corrected before freezing and method review.

The [separate method review](method-review.md), SHA-256
`88bf85f1b800536d5cd3e60771bd288b118b0d501e367054f8403766061100bd`,
accepted the plan conditionally; this is not implementation or result approval.
The inclusive 3584 MiB lane, 128 MiB reserve and continuing 4096 MiB free-space
floor remain binding. Compression-based feasibility is an estimate, not a
guarantee. The declared jobs run serially; a failure stops further jobs without
deleting products or automatically enlarging limits.

## Controls before historical execution

Runtime for commands below:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
The working directory is the isolated investigation checkout, unless specified.

Root read the full parent dense adapter, V2 configuration/runner, relevant
tests, complete artifact checker and direct-score checker. A first lookup of
the uncommitted V2 checker from the main checkout failed; it was subsequently
read from its actual investigation checkout. No file was repaired or moved
to conceal that lookup failure.

Root adapted [verify_scores.py](verify_scores.py) from the completed Clip 3
direct-sum checker, changing the declared population/target paths and adding
aggregate terminal and before/end input gates. In tool command `567910`, the
bundled Python compiled and imported the script without running its historical
main, then tested correlation of an array with a positive affine transform,
its negative and a constant: all three checks passed. Calling main without
the required completed aggregate refused at the first receipt gate, before
loading historical scores or pixels. This is a small checker control, not the
full implementation suite or historical verification. The command exited zero.

## First implementation controls and prehistorical correction

Author ran `python3 -B test_controls.py --output controls-author01`, using the
runtime above (terminal 67778, final tool chunk `173c08`; basenames abbreviated
here, with actual absolute argument paths retained in the saved summary).
Exit 0: all **110** tests passed, with groups sampler 14, pilot 25, inherited
supervisor 16, new supervisor 13, dense 32 and version 10; no failures, errors,
skips, population mismatch or changed dependencies. Root read the saved summary
(`4e3035`), SHA-256
`67240be3d7d6102eb766d63a47a8f86dca1693b043375d16cb96993756e3b1c9`.
The 6768-comparison wiring test mocks numerical registration; it is not a
historical or numerical validation. Configured sampler synthetic decoding and
synthetic process-supervision tests actually ran. Controls record resource
samples at group boundaries, not a continuous trace. The lowest saved free-space
sample exceeds 9.07 GB; temporary synthetic fixtures were cleaned as declared,
while logs and retained test products remain in the inclusive lane.

That passing suite is **not the accepted historical-execution version**.
Author and separate reviewer identified a missing completeness check: merging
every supplied input map does not reject an omitted required source entry.
Before historical use, root authorized requiring each chunk's resolved map to
contain the fresh required source and paired-reference identities, with negative
tests and another fresh suite. This implements the frozen plan's completeness
rule; it changes neither masks nor numerical scoring. The earlier passing
receipt and its code hashes remain preserved, rather than being described as
a failed historical analysis or silently updated. Root's independent full-suite
rerun is still pending.

Root also read the complete adapted artifact-checker diff and independently ran
`python3 -B audit_artifacts.py --self-test` (`af43f6`, exit 0): all 28 synthetic
checks passed, no historical files opened. This was checker hash
`d01fe31c9b4ff09f9971f482f0f7adb0853b7ba00d3a24f6cc227f48452fa306`;
the subsequent per-chunk completeness correction may require a new checker
version and rerun. The direct-score checker hash at this point is
`09292f9e1866ba228a83bd47396a3af75949fb15898bb4e7839537d8e136027d`.

Historical execution and all Clip 7 numerical conclusions remain pending.

### Root's incomplete concurrent synthetic run

Root launched the corrected suite with the bundled Python, `-B test_controls.py
--output /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-frame-correspondence/dense-clip7/controls-root01`,
from this directory (terminal 46246, initial `1a6ccb`). This overlapped the
author's synthetic controls-author02 run. It ended with **exit 1**, final tool
chunk `0e971e`, after sampler 14, pilot 25 and inherited supervisor 16 passed.
There is no completed whole-suite summary for controls-root01, so it cannot
clear the historical gate.

The traceback is `test_controls.py:172 resource_check()` → `guard.py:33
p.stat().st_size`, raising `FileNotFoundError` on the other run's temporary
`controls-author02/temporary/tmpwt6bsyeg/extract02/vince-clip7/native/frame-000109.png`.
The shared-lane walk overlapped synthetic fixture cleanup. Root's concurrency
choice caused this avoidable operational exposure; it is not a historical
source or correlation failure. Partial control records remain untouched.
No ignore-missing rule, code relaxation or historical retry is authorized.
Wait for author controls to finish, then explicitly rerun unchanged code
serially in the new controls-root02 directory. The eventual checker must bind
that actual completed root run, not the incomplete first one.

## Corrected implementation: fresh author and serial root verification

The completeness correction was independently inspected before history. It
freezes one required map from freshly checked inputs plus the fixed paired
reference, then requires that map in every chunk before deduplication. Both
passes still share one conflict-rejecting map and retain the final recheck.
The omission control tests missing source and missing reference separately.
The unchanged scoring and sampler parent hashes remain in each control record.

Final production/control hashes before historical use:

| File | SHA-256 |
| --- | --- |
| dense.py | `2828059bb3392c335c0d1ea71e7b0727a2e41b9a50db63df260a65a142e8bdb9` |
| test_dense.py | `d55990270cd7a6f4954dde582997ad2479f1c7fd89093eee3a1f707e6b634def` |
| test_controls.py | `7983df94692181091b763865d2ee402208f9cf4bb800ad3373a1e9ad38d89dc6` |
| guard.py | `1ef728c8ee1827b6ad5d71a2e386b44f501f1fabba9a2ef16bee74fcb68892cc` |
| test_guard.py | `680aef3af6d66f74eaecd914c8033e5ba452b60acb1b803f11de055922334357` |
| run.py | `dbce88d6a896dd5e3ca5b1c2024f0fac1d52a09286766612463b3a873b1ab95e` |

Both completed runs used the bundled Python with `-B`, this directory as cwd,
and test_controls.py with the absolute `--output` path to the named directory.
Author's script argument was also absolute; root used the basename.

| Run | Terminal / final tool chunk | Result | Summary SHA-256 |
| --- | --- | --- | --- |
| controls-author02 | 41693 / `db4c2a` | Exit 0, 111 passed | `126c07192b8033508cbdb22aa7295bbcdf954dc328f41f8c93cd20fc0af96ffc` |
| controls-root02 | 8161 / `c3da0d` | Exit 0, 111 passed | `3c656d64ba2d435c86e8db240a2e52b899d94f653d6d75416e6eb9988ce10641` |

Each has exactly sampler 14, pilot 25, supervisor 16, new supervisor 13, dense
33 and version 10, with zero failures/errors/skips. Root's serial rerun began
only after author completion and a scoped process check returned no matching
live Clip 7 control process. The earlier outputs were not deleted or relabeled.
Root's read-only release preflight (`4cbd3d`, exit 0) accepted the fresh gate,
all 36 control/plan/manifest pins and the unattempted first job. It measured
3,803,542 lane bytes and 9,066,012,672 free bytes at that instant.

The artifact checker independently gained a per-chunk mandatory-input check;
a complete union cannot hide one incomplete map. Root inspected that delta and
ran all **34** synthetic checker controls (`fe8ab2`, exit 0), with zero historical
files opened. Its final prehistory hash is
`c7342eb153dcdfed1762d9d312b46a26b1e4d84f7a3eac6849a38eab0b99cfe8`.
It explicitly binds controls-root02; its intermediate 34-check version was
`022b0d946c8763d834d8ccb7b768aac6756b87f6f6a07a8b2f8a32931074df6b`.
The direct-score checker remains unchanged at its earlier recorded hash.

## Historical execution

Root read the complete [implementation review](implementation-review.md),
SHA-256 `17b338a58697d0b2249056341cb5b2adaf7e192884df3f02b69adb8dfdbd0f9a`,
before the first historical command. All historical jobs use the bundled Python
with `-B run.py --job <declared-name>`, this directory as cwd, absolute paths to
controls-root02/summary.json and its pilot-controls/summary.json, and the fixed
plan/manifest hashes recorded above. The supervisor saves each actual child
argument vector and raw streams. Historical jobs run serially.

| Completed job | Terminal / final chunk | Supervisor seconds | Job bytes |
| --- | --- | ---: | ---: |
| extract01 | 45225 / `15f9a4` | 25.260862249997444 | 883725454 |
| extract02 | 45632 / `7f0487` | 25.099711541901343 | 883725454 |
| score-a-01 | 90016 / `b6949f` | 78.30402449995745 | 34128942 |

Root inspected the first extraction's successful receipts (`b1e213`) before
starting the second. The [source/product check](extraction-review.md),
SHA-256 `c3e2708cb6696ad85d97ab2ad7b82c83342a177f6734c3c73dc61186983fc108`,
then verified every repeated row and all 2265 fresh/pilot PNG/RGB pairs, before
scoring. Both frames.json hashes are
`a7793e5d1f4a7faafe102029ebf99aede540021c83f292e5c9232de13622c13c`.
The first scoring job completed 189 comparisons for indices 0–62; root checked
completion, limits and unchanged dependencies (`4c0752`), not its rankings.
A premature receipt lookup while that job was still live returned missing-file;
it was not treated as completion/failure or used to restart the job.

Root launched one finite serial batch for **score-a-02…18, then score-b-01…18**
(terminal **95429**, initial tool chunk `650311`). The stdout-only coordinator
asserts that this exact 35-name list equals `run.JOBS[3:-1]`, invokes each reviewed
runner through `subprocess.run(..., check=True)`, and requires successful inner,
supervisor and wrapper terminal records before continuing. It prints job counts,
duration and bytes only; no partial ranks or score arrays are read. An exception
ends the batch, without retry, deletion or aggregation. The aggregate is a
separate final job only after all 36 scoring chunks are verified complete.

At this earlier checkpoint, terminal 95429 was live and the full aggregate,
artifact audit, retained-score arithmetic, fixed native views and synthesis
were pending. It was continued through its original handle, not duplicated or
restarted after observation timeouts. Later completion is recorded below.

### First-pass completion and parallel read-only lineage check

The same batch completed score-a-02 through score-a-18 and entered pass B.
Root's completion-only check (`dfddf4`, exit 0) read all eighteen A-pass inner,
supervisor and wrapper records: all completed, no recorded shutdown/snapshot
errors or changed dependencies, and the declared 189/171 comparison counts
sum to **3384**. No result arrays, ranks or images were read. The repeat pass,
aggregate and post-aggregate checks remain pending at this checkpoint.

While this serial batch ran, a separate reviewer inspected existing textual
source/index records, without new acquisition, media views, dense historical
results, tests or edits. Its bounded search recovered no exact camera-to-report
derivation for Figure 5-142. Root checked the cited entries directly (`04734f`,
`7fa2c6`, `7b7a85`, `cc9d56`, all exit 0). The existing
[report-attribution entry](../../fire-coverage-batch3/source-attributions.json)
documents physical page 272/printed 228, the preserved report JPEG, intensity
adjustments, added floor/column labels, and a reported 3:55–4:04 p.m. interval.
That interval is not an independently authenticated event clock.

The [captured candidate metadata](../../cbs-vince-source-screen/stage4/metadata-refresh.json)
identifies `Vince Demetri Clip 7.avi`, provider ID
`1CnLqGzglKNyLeNwTrXBR1kxHdogB96wh`; the
[acquisition record](../../cbs-vince-source-screen/stage4/acquisition.json)
pins the held 140334936-byte source. Neither inspected record supplies an
original tape/accession-to-Figure-5-142 frame/timecode/field pointer, a separate
unannotated camera-source still, or the detailed crop/resize/intensity/export
history. This is bounded non-recovery, not proof that those records do not
exist or were withheld. Catalogue names and 2019 repository timestamps do not
establish 2001 exposure identity or chronology.

The specific next lineage discriminator is the Figure 5-142 still-generation
record joining the source identifier to frame/timecode/field and processing
steps, ideally with the unannotated still. A computed candidate alone cannot
supply that documentary link. No source acquisition or legal demand was made.

### Preserved live continuation checkpoint

At this checkpoint, terminal **95429** was the only live serial score batch. Last observed
completion was **score-b-04**, followed by the start of **score-b-05** (tool
`343380`): 22 of 36 scoring jobs complete. No failure is recorded in the output
seen so far. This is a checkpoint, not completion of the full repeat/aggregate.
Continuation used `write_stdin`; no duplicate batch was launched. The aggregate
was not part of this batch and remained gated on all 36 scoring receipts.

After completed aggregation, the existing read-only artifact checker requires
`--extraction-review-sha256 c3e2708cb6696ad85d97ab2ad7b82c83342a177f6734c3c73dc61186983fc108`,
and both `--frames01-sha256` and `--frames02-sha256` set to
`a7793e5d1f4a7faafe102029ebf99aede540021c83f292e5c9232de13622c13c`.
The separate artifact reviewer is waiting for that explicit release. Root must
also verify the artifact result and run the retained-transform direct checker
before the fixed native-image views and synthesis. No audit or direct-score
historical pass is claimed at this checkpoint. Do not rerun completed synthetic
tests while the shared lane is live.

Continuation-document checks used bundled `python3 -B -` (`10642d`, exit 0):
six fixed plan/manifest/checker/control/extraction-review hashes unchanged,
three updated documents' newline/whitespace checks passed, all three new
lineage links resolved, and STATUS retained the live handle and explicit
incomplete state. `git diff --check` (`ed9370`, exit 0) passed for tracked
changes. These are documentation checks, not a historical score audit.

## Complete historical execution and post aggregate verification

The next goal turn resumed the actual live handle (`dc0c1b`), re-read current
main/worktree instructions and the full-scope charter, and rechecked fixed
code/control identities. The previous turn was progress plus a verified wait,
not a blocker. Root's current control gate (`f5f197`, exit 0) accepted all 34
dependencies; no tests or historical scores/images were read in that check.

The same batch completed all 35 remaining jobs, final tool `88cc99`, exit 0.
Root's pre-aggregation check (`616c5f`, exit 0) verified all 36 score jobs and
6768 comparison counts, 36 control/plan pins and 114 predecessor-terminal pins,
and confirmed aggregation was unattempted. Lane bytes were 2995258671 and free
bytes 8556589056 at that check. No partial rankings or images were inspected.

Root then ran the single declared `run.py --job aggregate-a` with the same
absolute root02 control paths and frozen plan/manifest hashes. Terminal 29056
(initial `b631eb`, final `a35dd8`) exited 0. Its supervisor records
**68.83327745902352 seconds**, **13003714 job bytes**, completed status and passed
wrapper end checks. Root's terminal check (`9f95ef`, exit 0) confirmed 1128 frames,
3384 comparisons, exact equality across the full repeat and all 27 pilot joins.
That receipt also exposed the aggregate's six-index shortlist, after complete
aggregation; no image was opened or partial-run shortlist used.

Root explicitly released the separate full artifact audit only after this
gate. It is read-only against historical inputs. Root also started two read-only
checks with bundled Python and `-B` from this directory: `verify_scores.py`
(terminal 25670, initial `d30e37`) and `audit_artifacts.py` with the three actual
pins above (terminal 48860, initial `0c30c0`). These were live at that checkpoint;
their actual completions are recorded below. No concurrent synthetic fixture
creation/deletion or new historical job overlapped these checks.

### Completed artifact and direct arithmetic checks

Root's direct checker ended with exit 0, final `36c785`: **3384 comparisons,
6768 retained transforms, 12062 finite scores, 1474 null decisions**, maximum
absolute error **2.609024107869118e-14** against the declared 1e-9 tolerance,
and **1140 unchanged dependencies**. Its three embedded synthetic correlation
checks also passed. [The stdout record](direct-verification.json) preserves
the exact result, SHA-256
`88ada69830343c46ad848d160c49c5cb5d97ba69d222b00a2ea55eae0f8d39e8`.
It uses direct sums/separate mask indexing but shared Pillow/NumPy, and checks
all retained transforms rather than every lattice correlation cell.

Root's full artifact rerun ended with exit 0, final `01650c`. Complete captured
stdout was saved as [root-artifact-audit.json](root-artifact-audit.json), hash
`6a95abd2f0dc2a3c4f9474d9fc0e48740e2c1902c6b7371144981550670d54d6`.
The separate reviewer ran the same frozen checker with the actual three pins,
terminal 66511, final `4161f8`, exit 0. Its complete stdout and readback are
[artifact-audit.json](artifact-audit.json), hash
`63b8895f37d9e7b9ac2551bc5c46e19508eafab24b959e8eb9bb120c0288ffad`.
There was no failed historical artifact-audit attempt or checker repair here.

Both audits checked **228846384 saved static-score cells** (125383968 finite),
13536 retained transforms across repeats, 2948 dynamic nulls at those transforms,
36 complete maps with 2349 mandatory identities each, 9291 unique saved
dependencies and 9497 total audit pins. All six groups/eighteen near-best sets,
1128 repeated frame rows, 27 pilot joins and 39 resource/job records passed.
Root's full saved-result comparison (`658c7a`, exit 0) found only the expected
contemporaneous free-space difference: root 7966609408 versus reviewer
7982333952 bytes. Every other result field, including the 3008302135 lane-byte
snapshot, agreed. Shared components and the independent extraction-review
dependency are explicitly disclosed; saved-surface sorting is not independent
recomputation of every correlation cell.

Root read the complete [artifact review](artifact-review.md) (`ef0adf`) before
writing the synthesis. The initial review hash was
`9e341015d0139e43220f539d96e1c2b2910d26a829484d784e5d89baf991a604`.
A chronology-only correction removed “later” from its description of root's
separate checks, which overlapped the reviewer audit. The final hash is
`33b0a27e45dfce532266da9308150a24b8a9752cba3cc801dbdb049641b9900e`;
no result, scope, checker or stdout changed.

The saved 39 resource rows show score durations 74.37439462495968–
85.66057741700206 seconds and score-directory bytes 30795067–34359972.
Summed supervisor durations are 3001.290571002639 seconds; this is not an
end-to-end wall-clock estimate including review and waiting. All historical
jobs met the recorded limits. Resource snapshots are not hard OS quotas.

### Complete results and fixed native views

Only after complete aggregation, root inspected the global results (`170154`)
and checked all best-static dynamic nulls (`59ed5e`): 249 full, 248 even and
244 odd, every one below the fixed coverage gate. All 1128 frames in each arm
retain two valid static transforms. Aggregate pins are:

- Summary: `191e9efd672ac33f833c35acc0637272ac53f52592040f2a8adb6e9f371aa09d`.
- First-pass results: `0d64451b232987e457997663caeff4bcefecbc0465e1fd14d21ff63dcda212e7`.
- Aggregate receipt: `6625308f1cfb653540729a7342c50c5af8c58d6c9b18f75f5ae44d98e9288457`.

After both audit passes were received/compared and the direct check passed,
root displayed the unchanged full Figure 5-142 reference once, then native
538,539,540,541,543,544 once each in ascending order, using `view_image` with
`detail: original`. No additional image, neighbor, crop, enhancement, field
rendering or audio was used. All seven displayed; no image-display failure.
The exact files/hashes and descriptive limits are in
[root-observations.md](root-observations.md), initial freeze
`e570dc1acea367e2ebcc5d9efeefe6b5293580dc0d8be53710b3306f1d66dae9`.
The observations are prior-informed and scores-known, not blind or actual-human
confirmation. The reviewer's full prose was read after these gated views;
its numerical pass and saved stdout were already verified beforehand.

Root's [report](report.md), initial critique snapshot
`85eabb3aaf0e8464bcdfa9fa87a3162ad17ac76da6f4faa963afbe7eaa46f863`,
was sent to a separate computational reviewer for synthesis critique. No
image rereading, new matcher run or original-record edit was requested.
Full investigation goal remains active/incomplete. A failed patch-context
match while updating this working execution log made no change; the actual
line wrap was read before the corrected edit. It was not an evidence failure.

### Synthesis critique and closure

Root read the complete [synthesis review](synthesis-review.md), SHA-256
`cc74625a1ac7ec265f5f34f216b4391383710b301468bcdd21d1924ecb3e2218`
(`90a421`). The reviewer's saved-record calculation (`78a634`, exit 0) rebuilt
all six rankings/eighteen sets, retained all null/coverage decisions, checked
complete material repeat equality, all 27 pilot comparisons, six view-manifest
joins and fourteen unchanged text/JSON inputs. It found **no material correction**.
This reviewer previously authored the adapter; it is separate from root's
synthesis/visual reading, not fully independent implementation authorship.
The context-only subreview likewise added no new source or visual observation.
Root changed only the report's pending-review status and added the completed
review link/independence qualification; numerical and observational findings
were not revised.

Root's pre-critique documentation checks (`274294`, exit 0) verified sixteen
fixed/result/review pins, the current 34-pin execution gate, eight Markdown
files and all 42 then-present local links, eight Python syntax/whitespace checks,
and three passed saved audit/direct-check JSONs. No full suite, historical
matcher or image view was rerun. Tracked whitespace checks also passed
(`73f9f1`, exit 0). Main charter and completed Clip 3 report hashes were rechecked
(`017884`) and remained `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`
and `d90d6b387a180015aba1cd2dccdb8df9270091f6ba900ac7faedd4d62c6eafce`.
The existing SFB-005 entry already covers the observed completeness/shared-lane
problems; no duplicate note, external delivery or verified Sherlock fix was
claimed. The known archived-destination question remains unresolved.

This completed unit closes the declared 1317-frame paired computational search,
not all catalogue footage, physical/model questions, human gates or the full
charter. The next task is the specific source-generation/matched-observation
discriminator, beginning with held metadata and exact documented source records.
No live historical/check process remains. Branch HEAD remains ca1c2233 with
intentional research WIP; no main/legal edit, accepted engine finding, matrix
save, staging, commit, push or external disclosure occurred. A subsequent
closure patch used an incorrect STATUS path and made no changes; the report's
unchanged hash was checked before applying the corrected path.

### Final documentation verification

Bundled `python3 -B -` from this directory (`822ca4`, exit 0) verified **17**
fixed/result/review hashes, the unchanged **34-pin** current control gate,
**nine** Markdown files and **49** resolved local prose links, **eight** Python
syntax/whitespace checks, both updated navigation entries and three passed
audit/direct-check JSONs. The final report hash is
`984f3132fae5016cc01bdf2a68831b2147963fc0db9fd541e4aa908ce96ff470`.
No full test suite, historical scoring or image view was rerun. Final observed
lane/free bytes were 3008367567/6567190528, within the declared boundaries.
`git diff --check` also passed (`f20f39`, exit 0). The repository-orchestration,
evidence-audit and source-authority skills kept the complete population,
unavailable scores, failures and nonphysical inference ceiling visible; the
context-distiller used the existing STATUS/navigation rather than a second
handoff authority. No new feedback delivery or source promotion followed.
