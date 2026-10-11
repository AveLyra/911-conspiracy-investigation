# DistantView localization packet verification

October 8, 2026. A reproducible six-frame local viewer is available for a
**limited human localization pilot**, subject to the display limitation below.
The two generated packets are byte-identical; original historical images are
served unchanged. There are no entered historical coordinates or human
observations, no trajectory, and no change to a cause ranking.

The [human instructions](HUMAN-REVIEW.md) distinguish this pilot from the
completed R1 comparator review. The [frozen protocol](PROTOCOL.md) controls
selection and inference. Frames 274, 300, 342, 365, 388 and 411 are purposively
selected, previously viewed samples—not a random sample or clean holdout.

## Inputs and reproducibility

Both [packet01](packet01/manifest.json) and [packet02](packet02/manifest.json)
contain the same six files: three unchanged UI source copies, an exact pure
helper prefix, generated asset metadata and a manifest. Their manifest is
204,326 bytes, SHA256
`1c6b76f665ae63f43a722139317ba5890a9f1c7e25511f094a6f6fa4184e4bb6`.
The manifest itself is not served by the viewer.

All 660 predecessor pins and 17 packet-input pins were rechecked. The source
AVI remains SHA256
`a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e`.
The complete historical PNGs remain 704×480 grayscale; the separate synthetic
control remains 1280×720 RGB. Byte identity preserves the earlier image
products; this unit does not claim a new independent pixel decode. The
[prior verification](../continuity-274-411/final-verification.json) remains
unchanged, with its original scope limits.

Three selected images—300, 342 and 411—lack stored PTS. Their decoder
best-effort timestamps remain separately labeled; none is substituted as an
authenticated exposure time. All images retain their decoded ordinal and
exact nullable metadata.

The helper is exactly bytes [0,2524) of the pinned R1 coordinate source,
SHA256 `9cff4290fc41e27126b36402818b1ecb55057e003f819ecbe8cef53281d2e2c4`.
The unchanged R1 request handler serves exactly seven images and five UI/code
routes. It rejects non-allowlisted paths, wrong Host/Origin, changed/missing
assets and source symlinks; write methods are unimplemented. It is not a
security guarantee against arbitrary same-machine code.

## Executed checks

Working directory for these commands:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
`L` below is a task-specific shell variable for the new unit. Python was the
bundled 3.12.14 runtime; Node was 22.16.0. These are actual root executions,
not inferred from agent reports.

```sh
L=research/sherlock-wtc7-investigation/distant-view-source-screen/localization-review
node --test "$L/test_response.mjs" "$L/test_mapping.mjs" research/sherlock-wtc7-investigation/comparator-r1-replication/test_coordinate.cjs research/sherlock-wtc7-investigation/connection-curve-comparison/test_coordinate.mjs
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B "$L/build_packet.py" --self-test
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B "$L/serve_review.py" --self-test
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B "$L/build_packet.py" build --out packet01
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B "$L/build_packet.py" build --out packet02
node "$L/verify_packet.mjs" 55462
git diff --check
```

The build commands above were run once for each fresh directory. They refuse
existing outputs; they are not instructions to overwrite either saved packet.
The optional verifier port targets an already-running loopback server.

| Check | Actual outcome and ceiling |
| --- | --- |
| JavaScript suites | 55 test cases passed: 34 new mapping/response/lifecycle cases plus 21 existing shared cases. Pure synthetic mappings cover both image sizes, every pixel center at three scales, edges, fractional/negative origins, invalid inputs and nudges. Fake DOM tests cover loading/reset/error states, boxes, notes, inspection booleans and separate synthetic drafts. |
| Builder controls | 15 passed after the alias repair below. No historical coordinate or feature-accuracy test is implied. |
| HTTP and adapter controls | 26 passed under approved loopback execution: six adapter plus 20 inherited synthetic controls. Earlier sandbox-blocked runs were not passes. |
| Repeated packets | Both builds exited 0; all six products repeat byte-for-byte. Producer checks inputs before/after preparation and save. |
| Separate verifier | Passed for 660 predecessor and 17 packet pins, copies, exact helper bytes, nullable clocks, PNG headers and 12 routes. It imports neither builder nor image decoder. Its sequential check is not an independent before/after immutability witness. |
| Actual served bytes | All 12 route bodies matched pinned sizes/hashes. Manifest and protocol requests returned 404; POST 501; wrong Host and cross-origin requests 403; HEAD 200 with no body. CSP presence was checked here; fuller header expectations are in the shared tests. |

The 96 passing software test cases are not 96 independent scientific tests.
The separate checker still shares source records and the frozen manifest.
Root test receipts are `577bd0`, `15fec9`, `51c621`; builds `48fd28`,
`0aedfe`; separate filesystem check `02cfac`; final saved verifier execution
`6381b6`. Tool receipt IDs identify this session, not permanent external sources.

## Actual browser checks and unresolved display limit

The native in-app browser was used on the synthetic control. Initial and
restored viewport: 1280×720 CSS pixels, reported DPR 2. Temporary 800×700 and
1000×740 overrides reported DPR 1. These settings are not physical-device
calibration. The temporary override was reset and the original values rechecked.

An actual Fit-view click selected synthetic cell (600,200); right/down keys
changed it to (601,201). Fit/100%/200% zoom and scrolling retained the locked
cell. A box (600,200,601,201) remained pending until an explicit synthetic-only
draft action. Missing inspection confirmation and then a missing note were
rejected separately. The test note explicitly labeled the row automated and
synthetic, not human evidence. All six historical rows remained uninspected.

**Unresolved Fit-mode targeting miss:** a later DOM-derived click intended
for (500,180) produced (500,179). No delivered-event-coordinate log was
captured, so input quantization, geometry changes and a mapping issue are not
distinguished. It is not a successful exact-targeting test and is not a
general one-pixel error bound. The marker subsequently aligned with the
*reported* (500,179) cell within 0.007 CSS pixels on each axis; that establishes
internal display consistency, not the accuracy of the intended click.

A subsequent 100% click produced the intended (500,100); resizing retained
that reported cell. Accordingly, Fit is recommended only for overview, with
100%/200% and keyboard refinement for final endpoints, followed by checking
the marker and coordinate. Zoom alone is not a guarantee. Recurring mismatch
at fine-view settings would block coordinate use pending diagnosis. Independent
computational review agreed this explicit limitation permits the bounded human
pilot, not universal targeting or automated-localization validation.

All six historical image loads were checked through DOM dimensions and
metadata only: 704×480, blank inputs, no pending boxes. The first check of274
caught its loading state; a later check confirmed successful loading. No
historical screenshots, coordinate clicks, boxes or response entries occurred
in this UI QA. Returning to the synthetic control and clearing its draft left
zero historical rows and no synthetic practice row. Browser warning/error log
was empty at the check. [Synthetic-only UI capture](synthetic-viewer.jpg).

## Failures and review disposition

- Initial builder controls passed despite a real inherited dependency issue:
  `/opt/homebrew/bin/ffmpeg` is a symlink recorded alongside its canonical
  binary in the original receipt. Independent review caught the blanket
  symlink rejection before packet execution. The repaired checker allows only
  that literal, non-served alias, requiring both equal pins, the exact canonical
  target and stable link resolution. Five rejection/acceptance controls were
  added. General served/source/module symlink rejection is unchanged. Peer
  rerun of the complete inherited 660-pin closure passed.
- The UI author's first synthetic run was 24/25: a test helper's default
  parameter converted an intended undefined-status fixture to a valid status.
  Making the fixture explicitly undefined fixed the test; validation was not
  weakened. Root subsequently ran all 55 combined JavaScript tests.
- Initial HTTP tests could not bind in the sandbox. Approved loopback execution
  passed. The first separate live HTTP probe similarly failed with EPERM;
  it did not indicate that the server stopped, and no restart was performed.
- A subsequent ad-hoc HTTP check failed because its assumed refusal-code set
  omitted 501. The unchanged handler and original tests explicitly expect
  POST to return 501. The saved verifier now asserts that exact contract,
  preserving rather than weakening the no-write requirement. Both failed
  probes remain tool receipts `ce3707` and `a17417`.
- The Fit-mode miss above remains unresolved. It was not removed from the record
  or converted to a claimed display-resolution diagnosis.

## Version pins

| Artifact | SHA256 |
| --- | --- |
| Protocol | `1846d0e0cc532009e7941608ef39af3444fb01b365c670a19a08325af6c5046d` |
| Builder | `3deb0c8ed6c1a2cd367ceaf096dac1ac4250a790f73c331128dd8141fd168b6c` |
| Server adapter | `cf3e5ef2649b2f89eddbfa36c6986d10995146fc568a1f1854d690a56beccfea` |
| HTML | `f32657ca617bb3c4b815aada46b26a9d1b33c1223644d59fdf9139e24afabe74` |
| UI controller | `318904031cde1047be376679e4ed6649836c8ab3caad6f773c4ae763e91cdca6` |
| Response validator | `2e9f0c1acf98d2b63b9db6d20824b3e152cc55fedab84dabe789477bc53499d8` |
| New mapping tests | `197f60c3d1a86ef7733051b1b27e4623a149f86481e27e5891796bb9ef3c5c99` |
| Response and lifecycle tests | `53e07fdae709429f52a778e7f74e1a7885d2038bba8cd9a1e4e72d1a781c8e6a` |
| Separate verifier | `7c1f83ba072297e3ddbb39c1ba80760657181a8e53119cfdf46f2898910346fd` |
| Synthetic browser screenshot | `4dedd85d540bcedbe1200e924f839c7576649dd12185b6ffe17eb25d228f0835` |

## Local operation and next gate

Server started as execution session **43737**, PID **10697**, listening only
on `127.0.0.1:55462` as checked by `lsof`. This is a live local service, not
permanent hosting. Start command, only after checking the existing handle:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/distant-view-source-screen/localization-review/serve_review.py --packet packet01 --port 0
```

The viewer saves nothing and authenticates nobody. Only an actual user reply
can supply the human observations. The six-frame pilot remains incomplete
until all responses or explicit user-reported unavailability are preserved.
It does not certify the remaining132 frames or resolve material-point identity,
timing, projection, scale, deformation or the full structural causal chain.
An automated historical locator still requires its own frozen synthetic
accuracy/abstention challenge and the actual human spot-check.

The prior investigation unit made progress by finishing full-interval contour
coverage; the intervening acoustic clarification did not complete a new motion
measurement. This unit advances the next human-review prerequisite and stops
at the declared handoff. The full charter goal remains active and incomplete.
No main/raw/legal record, accepted Sherlock/Faraday state, historical source,
cause ranking, commit or push was changed. This packet postdates the unchanged
material-claim index snapshot and is not silently integrated into it.

The reduced-view targeting recurrence is deduplicated under existing
SFB-002/SFB-005. It is a local workflow observation, not a demonstrated Sherlock
defect. Feedback remains queued locally while the designated destination is
archived and the existing routing question is unanswered.
