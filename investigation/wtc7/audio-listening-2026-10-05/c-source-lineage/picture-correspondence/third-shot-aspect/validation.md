# Third shot aspect execution record

October 8, 2026. Research-only computational and visual checks. Original
videos, extracted frames, previous results and legal records remain unchanged.
This file distinguishes preparation, execution and independent verification.

## Method and source inspection before scores

Root read the main instructions and complete charter, parent protocol, config,
report, producer/tests, relevant correlation core and previous independent
checker. Root viewed all three full native C references and early frame720
before declaration; no new coordinates were selected. Old results were known.
The separate prior-informed [method review](preparation-review.json) accepted
the two matched arms subject to tests, and supplied the exact factor/rounded
geometry/mask-count oracles. It identified the differing-valid-pixel confound;
the protocol added common-support diagnostics before implementation controls
or historical scores. Frozen protocol SHA256 is
`bc369159ff6aa3f71e204e72f9c01eb8749e81008f8271b83f8f31d0ca7ddc25`.

The held stream records inspected by root (268a41) both declare sample aspect
1:1. Early record SHA `232204059c66dcca2f11b72bc86fd54cc22a4408cc89567c27c51883243edd56`
at `../../screen01/early-copy-stream.json` reports320x224, display10:7;
compilation record SHA `16df4a9fc3d486ef7ad84e5216ca8f66b751604eb89df3c01ca7e897fe0b6b63`
at `../../../c-full-visual-review/run01/compilation-stream.json` reports1280x720,
display16:9. These are prior extraction metadata about held encodes, not new
decoding or evidence of original camera geometry/earlier transfer history.
They do not change the fixed factor or authorize another arm.

The literal relative paths in this record are from this directory. All commands
below use `/Users/admin/.pyenv/versions/3.13.7/bin/python3` with `-B`, abbreviated
P in prose only. Actual runtime is Python3.13.7, NumPy2.3.4, Pillow12.0.0.

## Synthetic checks and freeze

Producer `aspect_screen.py` SHA
`e835362b4677b83770bc55fb7fc69dcdca0b20f0a98fd17ef2d7350ab66ac535`;
tests `262959c4ae8afaca5f388d336e892129bbd214668af2d3eaef23bd2a725f12f4`.
Root read both completely. The new code reuses pinned parent/core components;
no old method or acceptance criterion was rewritten.

Author ran `P -B aspect_screen.py controls --run controls01`:11 core,9 parent
adapter and18 new tests passed (fc6404/c061ac). Controls receipt SHA
`f303b8b0c506fdc0be0291d91f02513d9c8e82942150cc10a3824a446efc6c18`.
Root independently ran `P -B aspect_screen.py controls --run controls02`
with scoped worktree-write approval: session30343, c684c9/6a8c38, exit0;
the same38 checks passed. Receipt SHA
`1d373c199580044c7733d7743aebb37fc43bfb3b56c6ed1619f3521cf91cd7d1`.
The controls include actual changed-evaluation/no-refit and same-cardinality/
different-valid-set examples, known synthetic aspect recovery, all228 mocked
pair iterations, old-factor equivalence at all21 scales and source/gate failures.

Root rechecked the fresh controls gate and19 method/runtime pins (fa90aa),
then saved [method-freeze.json](method-freeze.json) with apply_patch from the
verified machine output. Its ready status authorizes this computation only;
it is not a human review, source authentication or scientific acceptance.

## Historical execution

Root started precisely the two fixed runs with scoped worktree-write approval:

- `P -B aspect_screen.py screen --run aspect01 --controls controls02`,
  session74402, start416602.
- `P -B aspect_screen.py screen --run aspect02 --controls controls02`,
  session91037, start5ab3db.

At this record checkpoint those live runs have not yet been certified complete.
Their actual completion, product equality, independent arithmetic, bounded
visual review and final claim disposition must be recorded below before a
result is called verified. No audio resampling, causal ranking or engine
acceptance is performed by either command.

## Completed runs and independent replay

The above checkpoint is superseded by actual completion: aspect01 finished
exit0 (b33aea) in75.9348467909731s and aspect02 exit0 (4a0d55) in76.62726320803631s.
Both report228 pairs,114 paired comparisons and41 verified images. Root's
direct byte comparison (6aec4d) found all233 material products identical,
84,117,508 product bytes per run; method before/after states are equal.
No partial run or failed historical result was discarded.

The checker author froze code/tests after26 synthetic tests passed (52c960).
`P -B independent_check.py --receipt independent-check.json` first completed
verification but could not save its exclusive receipt because of sandbox
PermissionError (ff99dd/87e746). The unchanged narrowly escalated command
passed and saved it (8df88d/fe50bc). This is a save failure, not a failed
scientific check; no alternative write channel or relaxed assertion was used.

Root read final checker and all tests completely (8116f8,72219b,bf3f95), then
ran `P -B -m unittest -v test_independent_check.py`:26 passed in0.112s,
exit0 (6fdaa7). Root ran a read-only structured replay (d0f223/bfa7af):

```python
import json
from pathlib import Path
import independent_check as c
old = json.loads(Path('independent-check.json').read_text())
fresh = c.verify(c.HERE / 'aspect01', c.HERE / 'aspect02')
excluded = {'elapsed_s', 'command'}
assert {k:v for k,v in old.items() if k not in excluded} == {
    k:v for k,v in fresh.items() if k not in excluded}
```

Result passed; every substantive saved receipt field matched exactly. The
checker verified228 arm-pairs,444 retained transforms,233 products per run,
41 PNGs,69 pins,18 rank groups and114 paired records. Selected direct arithmetic
has1,305 numeric results and27 nulls; maximum score difference2.609024107869118e-14,
coverage4.440892098500626e-16. The228 common-support records contain22 unequal
sets and six missing-transform records; their diagnostic scores comprise428
numeric results and16 nulls. No source/clock/audio identity follows.

Material pins, root rechecked adce96:

- Method freeze `baac5ede271d9bffd9e07713363c1149f99524b071395dcd612f5ead87d78f88`.
- aspect01 receipt `544f7d81063f35fa137dfd5493c706b0a35c9c20f520c56db19f90e40a07d596`.
- aspect02 receipt `acc985f651b50fd2217d29e66181870242b83b2022661f48147651f4f29a3332`.
- Independent receipt `f86d8f630351dc32fa23fa64598b2547ed4292bf5803aac0124b6ff3286c99bf`.
- Independent checker `053c9242829136b4cc5908b11e3931dd7fcdde9e6956813a6d51e566b9ecbdb5`.
- Checker tests `2d75032894e99268e77c2e8a5dd1dfaa15a6dc7cc1c143c31607c4d6bab395cd`.

## Finite images, descriptive summaries and refusal

Root actually viewed15 native earlier images in three batches, indices
90,180,210,240,270 /300,540,570,600,630 /870,900,930,1049,1079;
the three C references were viewed before declaration and reopened before
the initial observations were saved. `tools.view_image(detail=original)`
pixels were displayed through `functions.exec`, without resampling or marking
the originals. Root observation SHA
`2b07c39a353fbea4e695c971ef03e0e5bf57cc3c1b8458228300941e957ad0bf`.
Separate reader reviewed the same exact union and saved its interpretation
without root's observations: SHA
`834299745da1f1930b124a323d60ceee5394b17118cb672c7d7449400dd50207`.
Root subsequently read that file fully (f8b3f0,f44093,dba59f); the separate
reader then compared root's frozen file (110532). No material disagreement.
Neither review is human acceptance or an independent recording.

Root's read-only Ruby aggregation of saved results initially failed from an
unclosed compact block (fc5b7b), then from system Ruby lacking Array#tally
(4a5cd3). Neither wrote files or produced accepted numbers. The corrected
plain group/count aggregation completed exit0 (65ad50), reporting all six
common-support delta distributions, availability and boundary counts used in
the report. It also exposed the unchanged alternative C14 static-evaluation
leader's1175/1363 coverage; no unqualified cross-support improvement is claimed.

Root inspected the actual producer's output-path refusal before testing it.
A Ruby Open3 wrapper snapshotted SHA256 of all235 existing aspect01 files,
invoked `P -B aspect_screen.py screen --run aspect01 --controls controls02`,
required child exit1 with FileExistsError, then checked identical file roster
and every hash (ac9613). Wrapper exit0: expected refusal passed; no third
historical computation, overwrite or output deletion occurred.

## Final report and navigation audit

A separate read-only audit compared the final report/validation with the frozen
protocol, rankings, paired summary and independent receipt. It found no
material correction: scores, medians, missingness, boundary counts, shortlist,
listed pins and claim/authorization limits matched. No historical scoring was
rerun by that reviewer. Root then checked nine local report/validation links,
all18 root-reviewed PNG bindings against the pinned input map, and exact
15-image shortlist membership (742019), all passing. `git diff --check` in the
investigation worktree passed (5dcd60). That Git check covers tracked diffs;
new report and review artifacts received the direct checks just described.

The first status/navigation/feedback patch was rejected by the patch parser
for a missing added-line marker; the corrected same-content patch succeeded.
No partial change from that rejected patch is treated as a successful update.
The current status and research map now link this completed bounded result.
Generic common-support feedback was deduplicated into SFB-002/SFB-004 locally,
not sent, acknowledged or represented as a Sherlock implementation fix.
Frozen inputs, prior run products, legal records and the human graph packet
were not edited. No commit, push, external transfer or bridge activation.
