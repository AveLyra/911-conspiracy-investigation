# Execution record

2026-09-20 UTC. Worktree branch `research/sherlock-wtc7-investigation`,
HEAD `e8d83d7`; unrelated WIP preserved. Main controls/full charter freshly
read/rechecked; repo intake run. Initial large read outputs clipped portions
of controls/charter; targeted reads recovered those portions before work.
The last `rg --files -g AGENTS.md research` returned1/no matches, not a failed
calculation. No main/raw/legal/accepted-engine changes or external transfer.

Before implementation, the separate method reviewer identified the full
common position window6.4–9.4 (not the proposed velocity endpoint9.2), exact
clock covariance, post-transition non-identifiability, onset-grid limitations,
and the need for exact optimality bounds. These are incorporated in PROTOCOL.md
before any new historical fits. The preliminary review ran no historical fit.

## Initial synthetic failure: preserved, not omitted

Command from worktree, Python3.13.7, NumPy2.3.4, SciPy1.16.2:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B research/sherlock-wtc7-investigation/acceleration-transition-test/calculate.py controls controls01.json
```

Scoped worktree write permission. Session92479 reached terminal exit1.
The first13 synthetic fits were saved; the upward-acceleration control then
failed its transformed-clock certificate. No historical fit had been run.
`controls01.json` retains incomplete status, input pins and traceback.
The exact initial implementation was copied without alteration to
`calculate-initial.py` before fixing the live producer; that file is preserved
history, not the current run source.

Cause: under time scaling alpha, the data-column coefficient on a scales by
alpha^2, but the final a<=0 constraint still has coefficient1. Its dual
multiplier must therefore scale by alpha^2. Keeping all multipliers unchanged
is only valid when that multiplier is zero. The independent verifier author
derived this correction separately before seeing producer code/results and
reported it before root inspected the control traceback. Other multipliers,
primal b/R and optimum residual stay unchanged; v/a scale as specified.

Correction: scale only the a-bound dual multiplier in clock checks. Also make
the protocol's ramp-boundary velocity/acceleration continuity checks explicit.
No source values, objective, model family, parameter range or acceptance bound
changed. The passing control attempt must use a fresh result filename and the
new source hash. No independent historical verification is claimed yet.

## Corrected controls and historical execution

Same executable/environment, current calculate.py SHA256
`94e53d45b979765526b6ff12bcf6a5064f0ebb96b04ec462d401fd5eadd2042b`.
All commands below use the same worktree cwd and interpreter prefix above:

```text
... calculate.py controls controls02.json
... calculate.py historical run01.json --controls controls02.json
```

Controls session11360: terminal exit0, all178 fits and534 clock certificates;
five invalid-input rejections, two certificate mutations rejected,20 piecewise
basis checks, three boundary-position and12 velocity/acceleration boundary
checks. `controls02.json` SHA256
`262c9433261a8dea030825a1ca304797ec743a2fe4fb9eccf440e1ed1e1e677b`.
Initial source SHA256 `a416f9386895638779c5d419333c7277ea58c9fc181ec6a2dec272d9a9af3eae`
matches controls01's original source pin; failed JSON SHA256
`7754956547fb932decada3add158eee9b24f80124b0c39b0cc7ce4eca5aea133`.

Historical session30601: terminal exit0, all656 fits and1968 clock certificates.
`run01.json` is1,385,468 bytes, SHA256
`879700371bc35bdb302ef98dbe8db35fdab8efa358633e702331ea99fb1f1d62`.
Both transcriptions match all64 selected positions and full common16-row
membership; source rows38–53. Full70-row source tables remain intact. Source,
code, protocol, prior controls and Python executable pins match before/after.
NumPy/SciPy versions are recorded, not full dependency-binary attestation.

Root then used a read-only inline Python pass to replay all2,502 exact
certificates (178+656 cases, three clock coordinate mappings each), check all
stored input pins, parse both producer versions, and compute the reported
short-ramp-minus-step differences. Session51000 reached terminal exit0.
That pass did not rerun optimization and is distinct from independent review.
No new browser, original footage, historical image annotation or structural
simulation was needed or performed.

The complete optimizer was then rerun to `run02.json` under the same command
with only the exclusive output filename changed. Session86138 reached terminal
exit0,656 fits/1968 clock checks. Root compared the complete bytes: run01/run02
are identical, sharing the run01 hash above. This is a deterministic repeat,
separate from independent proof checking. An attempted write to existing
controls02 returned the expected FileExistsError/exit1 without changing any
of six monitored code/protocol/control/result files. All656 historical cases
exceed the printing-only bound; all16 duration/target grid minima have a single
interior onset. Every historical active-basis reconstruction used the first
declared1e-7 proposal threshold; exact rational certificates, not that threshold,
decide validity.

The text critic checked saved summaries and protocol boundaries, without
rerunning fits/certificates. Its two corrections were adopted: restrict the
no-discard statement to the frozen common window, and state that the tiny
central-value residual ordering has not been proved stable over the printing
intervals. Neither a stable nor reversed order under perturbation is claimed.
The critique also required completion of this execution record; the full
successful commands/results above were added while that review was underway.

## Independent checking and root reproduction

The verifier/theorem were frozen before result access. Original code SHA256
`ec65077b2918b38163f74daed3c5884495d844af211e2535e2f33db3fd77af70`
is preserved as independent_verify-initial.py. Its first controls-only check
stopped at numeric activity_threshold metadata: root's schema clarification
had incorrectly implied that every scalar was a fraction string. The approved
one-line repair parses only that diagnostic through Fraction(str(value)),
still enforcing the three declared thresholds. All mathematical fields remain
strict rational strings and all exact proof checks are unchanged. Root inspected
the complete checker and the one-line original/current diff; diff's exit1
means the displayed difference, not a failed calculation. A separate metadata
inspection briefly mistook an integer count for a list; no mathematical file
or result was changed to repair that inspection.

The corrected checker completed all178 synthetic and656 historical cases,
all2,502 transformed certificates and exact duration minima/ties. Its saved
`verification01.json` SHA256 is
`a97c87608ba2ecab84f5a3b8b591f09143e6d754b86e0a5c87b16327713d5711`.
It derives its basis piecewise, uses the independent source transcription,
and imports neither producer nor optimizer. Its supplementary audit checks
all834 stored nonsingular bases, matching active constraints and dual support,
source_data literals/row IDs and stored producer input pins. It verifies that
the failed control output is the exact first13-fit prefix of the corrected
run and rejects incomplete controls and an existing verification output.

Root then ran the complete independent functions read-only under Python3.13.7:
self-tests, source read/reconciliation, verify_controls and verify_history,
compared the complete normalized returns to the saved verification, and rehashed
all seven before/after input pins. Session14059 reached terminal exit0:
178/656 cases and2,502 clock certificates reproduce exactly, including every
saved summary and winning clock-mapped parameter. This is stronger than copying
the verifier's success notice, but still shares one published evidence source.

The [independent review](independent-review.md) records its commands, failures,
freeze chronology and interpretation limits. No accepted Sherlock/Faraday claim
or legal fact was created. The existing source/certificate feedback issue was
extended with a synthetic grid-alias and active-bound covariance fixture;
the note remains local because the designated task is archived and routing is
unresolved. No message delivery or product fix is claimed.

Context-distiller handoff is in STATUS.md: completed bounded calculation,
preserved failures/uncertainty, intentional uncommitted WIP and the specific
DEM-04 empirical-study lead. That source's current accessibility/contents are
not yet verified. No existing closed zoom or unsuccessful retrieval route was
reopened and no broader completion claim was made.

Final focused checks: all four unit Python files parse; four Markdown files'
ten local links resolve; `git diff --check` passes for the research index,
STATUS.md and SHERLOCK-FEEDBACK.md. The original protocol hash remains
`3d9e0929ae092ac6c167c9e5e01bde4aa0bf2d830230fed79d6fd4547b2c614b`.
The current independent verifier hash is
`901ed517cb221e5168397d3c6779e6359785fe9b6b7503bed9c1763224ba9b88`;
its archived initial hash is unchanged. Both historical output hashes still
match. These checks cover this unit and touched indexes, not unrelated WIP or
the full repository. No UI/browser test applies to the local table calculation.
