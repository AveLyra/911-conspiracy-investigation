# Read-only complete-page viewer — implementation verification

Date: September 27, 2026. Implementer: reused `curve_render` AI agent. This is software/presentation verification, not independent historical evidence, expert approval, human registration acceptance or curve extraction. The development-verification, source-of-truth-guardian and evidence-falsification-auditor skills kept the change within presentation and explicit evidence/acceptance boundaries.

## Scope and interface

Only six new owned files were written: `serve_review.py`, `review.html`, `coordinate.mjs`, `test_coordinate.mjs`, `test_server.py`, and this note. Preserved source pages, receipts, PDF, previous unit and root registration were not edited. No images were viewed by the implementer, no graph ordinates were measured, and no new raster asset was generated.

The fixed server permits nine literal routes: `/`, `/coordinate.mjs`, `/control.png`, and `/pages/073.png`, `/pages/074.png`, `/pages/075.png`, `/pages/076.png`, `/pages/077.png`, `/pages/117.png`. It reuses only the pinned R1 `handler_for` after checking actual helper bytes **before** executing the module. It does not invoke R1's main or routes. `compile`/`exec` avoids import-cache writes in the old unit. The six source pages are complete 1700×2200 RGB 200-dpi renders; the existing synthetic control is 1280×720 RGB.

UI: variable-dimension fit/100%/200%, hover, click-lock, one-pixel arrow nudges, Escape/clear, frame-change reset, sticky readout and visible load errors. Pointer coordinates use the image's bounding rectangle with no added scroll offset; border/padding are zero. Right/bottom boundaries are excluded; marker center is pixel + 0.5. Coordinates are disabled until the exact expected natural dimensions load. A generation token prevents stale image callbacks from enabling a different page. No annotation persistence, upload, export or acceptance button exists.

The six optional page76 jumps copy the root's explicitly AI-proposed anchors (each ±3 render pixels in each axis), select 100%, center the viewport and bring it into the document viewport. The readout labels `AI PROPOSED`, separately from genuine `CLICK LOCKED` or `KEYBOARD ADJUSTED`. All selections remain unaccepted/unsaved. Candidate IDs are F0/Fright/Ftop/E0/Eright/Etop. There is no embedded-strip or PDF coordinate conversion; geometric containment alone would not establish clipped/composited visibility.

## Actual commands and results

Commands ran from the main checkout unless stated otherwise. `C` below is an explanatory abbreviation for `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/connection-curve-comparison`, not a shell variable set by these commands.

```text
node --version
v22.16.0
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --version
Python 3.12.14
node --test /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/connection-curve-comparison/test_coordinate.mjs
9 tests; 9 pass; 0 fail; exit 0
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/connection-curve-comparison/test_server.py
12 tests; OK; exit 0
```

The final Python run used scoped approval for temporary **127.0.0.1-only** HTTP test sockets, with synthetic response bodies and temporary directories. It made no external network request. Read-only preflight also checked real file bytes/IHDR metadata and receipt membership, not image interpretation. The HTTP controls cover all nine GET/HEAD routes, body/length, security headers, absent cross-origin permission, traversal/query/fragment/absolute URL refusal, wrong Host/Origin, mutating-method rejection, changed/missing/symlink asset rejection, error headers, loopback binding and invalid ports. Helper wrong-pin control proves refusal before executing adversarial synthetic code.

Node controls cover both dimensions, fit/1×/2×, fractional and negative viewport offsets, boundaries, invalid numeric inputs, exact integer roundtrips, center placement, nudges/clamping, seven literal image identities, six valid candidate centers, and a minimal fake-DOM load/error/stale-callback/candidate/click/nudge/clear/page-change lifecycle. The fake DOM does **not** prove browser layout or input quantization.

Failures preserved:

- Initial Node run: 7/9 passed. Two continuous-CSS exact-equality assertions failed: marker x `0.49999999999999994` versus `0.5`, and candidate scrollTop `529.5000000000001` versus `529.5`. Integer-pixel selections were not reported wrong. The producer now computes display scale first, then multiplies the pixel-center coordinate; scale is exactly 1 at 100%. Assertions and coordinate acceptance criteria were not loosened. The full final suite passed.
- Initial Python run: six non-HTTP cases passed; six HTTP setups errored with `PermissionError: [Errno 1] Operation not permitted` at localhost `socket.bind`. This was not an application assertion failure. The approved rerun passed all 12; no test was skipped or substituted.
- Parent's first native-browser QA found candidate centering inside the image viewport could leave that viewport below the page fold. The final producer adds `viewport.scrollIntoView({block: "center"})`, covered by the synthetic lifecycle assertion. Parent owns final native-browser replay; this note does not claim that replay complete.

A read-only direct preflight invoked `routes()` and `load_handler()` and returned exactly the nine routes and `handler_for`. All six page hashes matched the pinned render receipt before implementation and after final tests. `git diff --check --` on the five code/UI files in the research worktree returned exit 0, but these files were new/untracked and that command alone is not a substantive new-file check.

## Final code and controlling pins

| File | SHA-256 |
| --- | --- |
| serve_review.py | e34a62c065ea7c98fec7c3d7b9ab8b7e00c1bf77a1d2fb2757abd8000adc88ba |
| review.html | ce171408d734b54ed69645b88afd93b6e65b3fd04d2fc721b4ba96c645f7737c |
| coordinate.mjs | 2aa953692b4933f1c87217a387833210d0725774ce77f90a82f18317013520a2 |
| test_coordinate.mjs | 05a38c882cf52d422a950a806c77aac4a9394554824a0a761edbc0665e51bd85 |
| test_server.py | 7cfd7a1c8f07019e6df1acdb2523886f91f9962324024463ea9eeaa633a231e7 |
| ../comparator-r1-replication/serve_review.py | 1ea233c4fa8074298f9791a305fa46f0b1ac3151ce00ce48c8edd7e99de48142 |
| ../comparator-r1-replication/coordinate.js — inspected helper contract, not imported | 38cc0cd9b0947e05072ec8656c58e4fc4ca95d968bd1a903af26afe43db0b05b |
| ../comparator-r1-replication/localization-control/fixture.png | f0a96bf21d7ec0d2b8b486050d111b803dd708645fb1b3ad1659c3eda2edaf48 |
| render01/receipt.json | 47d33d33b1695b00b21b72f9bda4a5c42d037ca1fb8a095c450aab9ba0eac1f5 |
| registration-root.md | ec66ae85a45a0169b7e8cc61698cc522e75cda2f2905f4c283f45f88de1f55a7 |
| REGISTRATION-STAGE.md | 18e212edcf4950f370bd30119597b20f786015d61da03fe4aeb19b23125f004c |
| PROTOCOL.md | 1ec6fedc9110f9ef2001f69fd1e13ad3a316a904f057345af26a0118d3216e19 |
| NUMERICAL-PROTOCOL.md | e03c47c1945b9eb9fd0a040d757d5f5f66bf76791ced8944323d3c92d1120df3 |
| HUMAN-REVIEW-GATE.md | 2e6f34d2e2d6d423c440c8a56b4a3c4796429d59f4d0baf0cf03609341a271ee |
| technical-preparation.md | a4d820f468dd80932f4144048eba545e70129f994c4b93e0f02f6a7f88e54550 |

The six PNG byte counts and SHA-256 pins appear literally in both `serve_review.py` and `coordinate.mjs`; the Python test compares their exact equality and actual PNG headers against the saved receipt. Source PDF SHA-256: `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4`.

## Launch, residual limits and acceptance

```text
python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/connection-curve-comparison/serve_review.py --port 0
```

The process prints its actual loopback URL and UI hashes. Parent launches/restarts it and uses the native browser; implementer did not activate a persistent server. Startup pins source PDF/receipt/candidate/PNG files, with every served asset rehashed per request. UI HTML/module are pinned at process startup rather than baked into the server, so an intentional edit requires restart and renewed verification. This is not protection against arbitrary same-user modification. Header checks plus full byte pins do not independently audit PNG codec fidelity or a whole dependency closure.

Fit-level mouse coordinates can skip native cells because browser pointer events have finite screen resolution. Use 100%/200% or integer arrow nudges. CSS zoom/DPR/layout rounding do not add historical resolution. Parent observed fit quantization in the first browser pass; that is stated in the UI, not hidden as a pass. No browser-visual result here accepts a human anchor, a native-raster transform, legend identity, subsequent curve sample or physical inference. All scientific/human gates remain separate.
