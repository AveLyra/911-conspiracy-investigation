# Native-sequence helper: implementation and synthetic verification

2026-09-19. Working research software; no historical processing or scientific
acceptance by this implementation agent. Main AGENTS/WORKFLOW/START-HERE,
the main investigation CHARTER, and this unit's PROTOCOL govern. Used the
development-verification, evidence-falsification and source-of-truth skills.
Read the complete old helper, FRAME-PLAN and final method-review; preserve
them and all old outputs. Read the new protocol, plan and selection after
root saved them. Root independently chooses and executes historical samples.

## Narrow change and acceptance contract

`sample_sequence.py` is a separate evolution of old helper SHA-256
`bd4267da1f80cb565322caa67a0ab8b8e5de181e31eaf0b68e4505e8a4258a68`.
No old code is imported or monkeypatched. Native video-only decoding, integer
PTS, rational time base, PNG/pixel hashes and SAR/interlace retention remain.
No new image transformation, overview, inference or measurement was added.

- Explicit manifest schema, unique safe IDs, absolute source paths, SHA-256,
  byte/frame counts and nonempty strictly increasing integer indices. No
  automatic source, interval or threshold selection. Boolean/fractional,
  duplicated, decreasing and out-of-range indices refuse.
- Required manifest/plan hashes, preserved input snapshots and rechecks;
  code/parent/runtime pins. FFmpeg/ffprobe 7.1.1 is the declared version.
- Separate source identity, structural checks, probe diagnostics, decode
  diagnostics and derivative admission. No generic overall “checks passed.”
  A clean product is only a descriptive candidate pending independent/human
  review, with `scientific_or_human_acceptance: false`.
- Any warning-level probe stderr byte refuses. Decode rejects explicit
  warning/error/fatal/panic, invalid UTF-8, unexpected control characters,
  untagged or unparsed nonempty lines, unknown info/context/metadata and wrong
  required line cardinalities. Known info is full-line matched, not a blanket
  `[info]` allowance. Paths are exact. The grammar is deliberately limited to
  the inspected DV/FFV1 → PNG producer output; unfamiliar legitimate output
  still requires review rather than silent admission.
- Selected showinfo PTS/time base, count, geometry, SAR, format and interlace
  reconcile to inventory; final frame count and color-line count reconcile.
  Empty decode stdout is required. Same native dimensions/RGB PNG checks.
- Exclusive directories and files; command arguments, stdout, stderr and
  numeric process exit status retained on nonzero returns. Source identity is
  rehashed after attempted processing, including refusals where feasible.
  Explicit exceptions implement guards; Python `-O` does not disable them.

A bounded separate agent reviewed only the old method and two saved clean
logs while implementation proceeded. Its read-only prototype recognized all
60 lines and rejected 13 injected variants; those are its reported checks,
not additional independent decoding. Relevant grammar/control suggestions
were incorporated and locally tested below. This is not a second historical
source or human review.

## Commands and actual results

Working directory:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/late-fire-sequence`.

An initial ordinary-sandbox invocation could not create `control01` and stopped
before any test ran. Scoped worktree approval allowed the same command; no
main-checkout workaround was used. That first version passed 13 grouped tests
and remains preserved under `control01`. After the declared narrow hardening,
the exact final command was:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B test_sample_sequence.py --out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/late-fire-sequence/control02
```

**Result: 14 grouped tests, 0 failures, 0 errors; exit 0.** Test subcases cover:
explicit-index/schema negatives; wrong hash/count; missing/boolean/duplicate
PTS and geometry/time-base failures; probe-only diagnostics; all four decode
severity levels; unknown info, control characters and invalid encoding;
wrong summary count/geometry/SAR/format/interlace and duplicate summary;
existing destinations; nonzero probe/decode and retained numeric status;
optimized-interpreter rejection; plan-hash refusal; and full synthetic CLI.

The preserved 125-frame FFV1 three-color fixture is the only media decoded by
these tests. Its SHA-256 is
`03faf8b842dbec9ea7358b91f3cb0097a40a1b0719696b698025a4b79599b8c6`.
Two fresh direct samples and a full-manifest synthetic execution select
0,60,120,124. Tests verify exact red/green/blue/blue pixels, 96×64 RGB, SAR4:3,
times 0,2,4,62/15 and repeated frame/PNG/pixel identity. Old Dub5 clean and
Dub6 refused logs are read-only grammar fixtures; neither AVI was decoded.
The final synthetic gate is not evidence about DV correctness or fire physics.

Root should rerun the same suite with a **new** absolute output directory,
inspect the changed guards and then use the declared manifest/plan. No source
run was initiated here. Historical CLI contract:

```text
python3 -B sample_sequence.py --manifest ABS_SELECTION_JSON --manifest-sha256 HASH --plan ABS_FRAME_PLAN --plan-sha256 HASH --out ABS_NEW_DIRECTORY
```

## Frozen pins and limits

| File | SHA-256 |
| --- | --- |
| sample_sequence.py | `c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d` |
| test_sample_sequence.py | `cd997911f50d89d57c65906a1ac4eef3cda09ac4667a1f07307f9945068fcc43` |
| control01/test-results.json | `1e4d073145a92d45a155a64857290f7d62583ff3aa4bf929f800303e937fb352` |
| control02/test-results.json | `5241f8566563764c068d0060b33eb8a07d70f64dff236c6d9503e43d40ba1744` |
| selection.json (root-owned) | `21d9595609115deb0ea35a9cd81d8d01c38d92c06716eeb9dc1aa0285acc1867` |
| FRAME-PLAN.md (root-owned) | `4c2870ab8775dd4a8b33fdbd59d32fafc2940fb14d7cee6cc19df829ad476297` |

Most consequential limitation: a clean, repeated decoder output is not
independent decoder validation or historical authentication. The closed
grammar may conservatively refuse unfamiliar benign output; do not loosen it
against a historical result without a separately reviewed version/change.
No timing continuity, calibrated color, physical mechanism, expert opinion or
human spot-check is supplied. All outputs, including earlier controls and
refused-stage artifacts, remain separate and preserved. No legal/canonical
record, outbound channel, old helper or old freeze was changed.
